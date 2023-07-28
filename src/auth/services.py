import datetime
from datetime import timedelta
from typing import Union, Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists
from sqlalchemy import select

from .models import User, Roles
from .schemas import UserCreate, UserShow, JWTTokenData
from .hashing import Hashing

from src.settings.config import (JWT_ALGORITHM,
                                 SECRET_KEY,
                                 oauth2_scheme)
from src.settings.database import get_async_session


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

    async def get_user_by_field(
            self,
            model_field,
            value: str
    ):
        query = select(User).where(model_field == value)
        async with self.session.begin():
            res = await self.session.execute(query)
            user = res.scalar()
            return user

    async def get_user_by_email(self, email: str):
        return await self.get_user_by_field(User.email, email)

    async def get_user_by_username(self, username: str):
        return await self.get_user_by_field(User.username, username)

    async def get_user_by_username_or_email(self, value: str):
        user = await self.get_user_by_username(value)
        if user is None:
            user = await self.get_user_by_email(value)
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


class JWTTokenManager(UserManager):

    async def authenticate_user(self, auth_value: str, password: str):
        user = await self.get_user_by_username_or_email(auth_value)
        if user is None:
            return False
        if not Hashing.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    async def create_access_token(
            data: dict,
            expires_delta: Union[timedelta, None] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session)
):
    credentials_exception = HTTPException(
        detail='Could not validate credentials',
        status_code=401,
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        manager = JWTTokenManager(session)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        auth_value: str = payload.get('auth_value')
        if auth_value is None:
            raise credentials_exception
        token_data = JWTTokenData(username=auth_value)
    except JWTError:
        raise credentials_exception
    user = await manager.get_user_by_username_or_email(token_data.auth_value)
    if user is None:
        raise credentials_exception
    return user


async def get_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(
            detail='User is inactive!',
            status_code=400
        )
    return current_user
