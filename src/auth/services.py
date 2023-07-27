from fastapi import Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists
from sqlalchemy import select

from src.settings.database import get_async_session

from .models import User, Roles
from .schemas import UserCreate, UserShow
from .hashing import Hashing


class SessionInitializer:
    def __init__(self, session: AsyncSession):
        self.session = session


class UserCreationManager(SessionInitializer):

    async def check_unique_email(
            self,
            email: str,
    ):
        query = exists(User).where(User.email == email).select()
        async with self.session.begin():
            res = await self.session.execute(query)
            result = res.scalar()
        return result

    async def _create_user(
            self,
            username: str,
            email: str,
            password: str,
    ):
        check_email = await self.check_unique_email(email=email)
        if check_email:
            raise HTTPException(
                detail='User with this email is already registrered!',
                status_code=400
            )
        new_user = User(
            username=username,
            email=email,
            hashed_password=password
        )
        async with self.session.begin():
            self.session.add(new_user)
            await self.session.flush()
        return new_user

    async def create_new_user(self, data: UserCreate) -> UserShow:
        user = await self._create_user(
            username=data.username,
            email=data.email,
            password=Hashing.get_hashed_password(data.password)
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
