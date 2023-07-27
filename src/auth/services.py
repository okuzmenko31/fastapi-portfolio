from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists
from sqlalchemy import select

from .models import User, Roles
from .schemas import UserCreate, UserShow
from .hashing import Hashing


class SessionInitializer:

    def __init__(self, session: AsyncSession):
        self.session = session


class UserUniqueFieldsChecker(SessionInitializer):

    async def check_unique_field(
            self,
            model_field,
            value: str
    ):
        query = exists(User).where(model_field == value).select()
        async with self.session.begin():
            res = await self.session.execute(query)
            result = res.scalar()
        return result

    async def check_unique_email(self, email: str):
        return await self.check_unique_field(User.email, email)

    async def check_unique_username(self, username: str):
        return await self.check_unique_field(User.username, username)

    async def raise_unique_failed_message(self, field_name: str):
        raise HTTPException(
            detail=f'User with this {field_name} is already registered!',
            status_code=400
        )

    async def check_all_fields_unique(
            self,
            email: str,
            username: str
    ):
        if await self.check_unique_email(email):
            await self.raise_unique_failed_message('email')
        elif await self.check_unique_username(username):
            await self.raise_unique_failed_message('username')


class UserCreationManager(UserUniqueFieldsChecker):

    async def _create_user(
            self,
            username: str,
            email: str,
            password: str,
            as_owner=False
    ):
        await self.check_all_fields_unique(email, username)
        new_user = User(
            username=username,
            email=email,
            hashed_password=password
        )
        if as_owner:
            new_user.roles = [
                Roles.role_owner
            ]
        async with self.session.begin():
            self.session.add(new_user)
            await self.session.flush()
        return new_user

    async def create_new_user(
            self,
            data: UserCreate,
            as_owner=False
    ) -> UserShow:
        user = await self._create_user(
            username=data.username,
            email=data.email,
            password=Hashing.get_hashed_password(data.password),
            as_owner=as_owner
        )
        return UserShow(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_owner=user.is_owner,
            roles=user.roles
        )


class UserManager(UserCreationManager):

    async def get_user_by_email(self, email: str):
        async with self.session.begin():
            query = select(User).where(User.email == email)
            res = await self.session.execute(query)
            user = res.scalar()
            return user

    async def set_user_active(self, user: User) -> UserShow:
        async with self.session.begin():
            user.is_active = True
            await self.session.commit()
        return UserShow(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_owner=user.is_owner,
            roles=user.roles
        )
