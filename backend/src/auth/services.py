import datetime

from enum import Enum

from datetime import timedelta
from typing import Union, Optional

from fastapi import Depends
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, insert, update

from .models import User, Roles, JWTTokensBlackList
from .schemas import UserCreate, UserShow, JWTTokenData
from .hashing import Hashing

from src.settings.config import (JWT_ALGORITHM,
                                 SECRET_KEY,
                                 oauth2_scheme,
                                 DEBUG)
from src.settings.database import get_async_session
from .token import AuthTokenManager


class SessionInitializer:

    def __init__(self, session: AsyncSession):
        self.session = session


class OperationType(str, Enum):
    operation_select = 'select'
    operation_exists = 'exists'
    operation_update = 'update'


class UserOperationsByFields(SessionInitializer):
    """
    This method provides methods with
    operations for selecting, updating
    or getting exists of users.
    """

    @staticmethod
    async def get_operation(operation_type: OperationType):
        """
        This method returns operation
        by provided 'operation_type'
        (e.g. 'select()', 'update()', 'exists()').
        """
        if operation_type == OperationType.operation_select:
            return select(User)
        elif operation_type == OperationType.operation_exists:
            return exists(User).select()
        elif operation_type == OperationType.operation_update:
            return update(User)

    async def field_operation_scalar(
            self,
            model_field,
            value: str,
            operation_type: OperationType
    ):
        """
        This method returns scalar result of
        query which was created with operation.
        e.g. we want to return user by username:
        query = operation.where(model_field == value)
        the same with:
        select(User).where(User.username == username_value)

        :param model_field: Model field (e.g. 'User.username')
        :param value: value for filtering (e.g 'test_username')
        :param operation_type: OperationType instance
        """
        operation = await self.get_operation(operation_type)
        query = operation.where(model_field == value)
        async with self.session.begin():
            res = await self.session.execute(query)
            result = res.scalar()
        return result

    async def field_update_operation(
            self,
            user: User,
            values_dict
    ):
        """
        This method makes update() operation
        for provided user and values dict.

        :param user: User model instance
        :param values_dict: dict with values (e.g. {'username': 'test_username'})
        """
        operation = await self.get_operation(OperationType.operation_update)
        stmt = operation.where(User.id == user.id).values(values_dict)
        async with self.session.begin():
            await self.session.execute(stmt)
            await self.session.commit()

    async def set_user_new_field_value(
            self,
            user: User,
            field_name: str,
            value: str
    ):
        """
        This method creates values_dict by
        provided 'field_name' and 'value' and
        calls 'field_update_operation' method
        for making update() operation.

        :param user: User model instance
        :param field_name: name of the model field (e.g 'username')
        :param value: value for updating.
        """
        values_dict = {f'{field_name}': value}
        await self.field_update_operation(user, values_dict)


class UserUniqueFieldsChecker(UserOperationsByFields,
                              SessionInitializer):
    """
    Class for checking user's unique fields.
    For example: 'username'.
    """

    async def check_unique_field(
            self,
            model_field,
            value: str
    ) -> bool:
        """
        Method which returns boolean of
        User exists by provided 'model_field'
        and 'value'. For example:
        'model_field' - 'User.username'
        'value' - 'test_username'

        :param model_field: model class attribute (e.g. 'User.username')
        :param value: value for filtering (e.g. 'test_username')
        :return: returns boolean of user exists
        """
        return await self.field_operation_scalar(
            model_field=model_field,
            value=value,
            operation_type=OperationType.operation_exists
        )

    async def check_email_exists(self, email: str):
        return await self.check_unique_field(User.email, email)

    async def check_username_exists(self, username: str):
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
        """
        This method checks by unique provided
        'email' and 'username' and raises
        an HTTPException if values are not unique.

        :param email: provided email
        :param username: provided username
        """
        if await self.check_email_exists(email):
            await self.raise_unique_failed_message('email')
        elif await self.check_username_exists(username):
            await self.raise_unique_failed_message('username')


class UserCreationManager(UserUniqueFieldsChecker):
    """
    Manager which provides methods for
    user's creation.
    """

    async def _create_user(
            self,
            username: str,
            email: str,
            password: str,
            secret_phrase: Optional[str] = None
    ):
        """
        This method creates new user by
        provided 'username', 'email' and
        'password'.
        """
        await self.check_all_fields_unique(email, username)
        new_user = User(
            username=username,
            email=email,
            hashed_password=password
        )
        if secret_phrase is not None:
            # if secret phrase was provided, and it was correct,
            # owner role will be added to the user's roles list
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
            secret_phrase: Union[str, None] = None
    ) -> UserShow:
        """
        This method calls '_create_user' method to
        create user with provided data and after
        returns 'UserShow' instance with portfolio_info about
        created user.
        """
        user = await self._create_user(
            username=data.username,
            email=data.email,
            password=Hashing.get_hashed_password(data.password),
            secret_phrase=secret_phrase
        )
        return UserShow(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_owner=user.is_owner,
            roles=user.roles
        )


class UserPasswordManager(SessionInitializer):
    """
    This Manager provides methods for
    checking, updating and setting
    the password.
    """

    @staticmethod
    async def new_dont_equals_to_old(user: User, new_password):
        """
        This method raises HTTPException if provided
        'new_password' equals to user's 'old_password'.
        In another case it will return None.

        :param user: User model instance
        :param new_password: user's new password
        """
        if Hashing.verify_password(new_password, user.hashed_password):
            raise HTTPException(
                detail='New password must be different from the old one!',
                status_code=400
            )

    @staticmethod
    async def get_hashed_password(password: str):
        return Hashing.get_hashed_password(password)

    async def set_new_password(self, user: User, new_password: str):
        """
        Method checks 'new_password' and sets it
        for the provided user.

        :param user: User model instance
        :param new_password: provided 'new_password' value
        """
        await self.new_dont_equals_to_old(user, new_password)
        new_hashed_password = await self.get_hashed_password(new_password)
        stmt = update(User).where(User.id == user.id).values(hashed_password=new_hashed_password)
        async with self.session.begin():
            await self.session.execute(stmt)
            await self.session.commit()

    @staticmethod
    async def check_old_password(user: User, password: str):
        """
        Returns True if provided password equals
        to encoded 'hashed_password' of user.
        """
        return Hashing.verify_password(password, user.hashed_password)

    async def change_password(
            self,
            user: User,
            old_password: str,
            new_password: str
    ):
        if not await self.check_old_password(user, old_password):
            raise HTTPException(
                detail='The old password is incorrect!',
                status_code=400
            )
        await self.set_new_password(user, new_password)


class UserManager(UserCreationManager,
                  UserPasswordManager):
    """
    This manager includes methods of
    managers which provides methods for
    user creation, password setting or
    changing etc. Also, manager provides
    methods for getting user's, checking
    exists, setting some fields values
    with provided data etc.
    """

    async def set_new_value_by_field(
            self,
            user: User,
            field_name: str,
            value: str
    ):
        await self.set_user_new_field_value(user, field_name, value)

    async def set_new_email(self, user: User, email: str):
        await self.set_new_value_by_field(user, 'email', email)

    async def get_user_by_field(
            self,
            model_field,
            value: str
    ):
        return await self.field_operation_scalar(
            model_field=model_field,
            value=value,
            operation_type=OperationType.operation_select
        )

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
        """
        This method makes provided user
        'is_active' field to True. By
        default, it's False.
        """
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

    async def get_all_users(self) -> list[UserShow]:
        users_lst = []
        query = select(User)
        async with self.session.begin():
            res = await self.session.execute(query)
            result_row = res.all()
        for user in result_row:
            user_show = UserShow(
                id=user[0].id,
                username=user[0].username,
                email=user[0].email,
                is_active=user[0].is_active,
                is_owner=user[0].is_owner,
                roles=user[0].roles
            )
            users_lst.append(user_show)
        return users_lst

    async def authenticate_user(self, auth_value: str, password: str):
        """
        This method is trying to authenticate user
        by provided 'auth_value' ('username' or 'email')
        and 'password'. If all is ok, method will return user.

        :param auth_value: value for authenticating
        :param password: password
        """
        user = await self.get_user_by_username_or_email(auth_value)
        if user is None:
            return False
        if not Hashing.verify_password(password, user.hashed_password):
            return False
        if not user.is_active:
            return False
        return user


class JWTTokenManager(UserManager):
    """
    Manager which provides methods
    for operations with JWT Tokens.
    """

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

    async def add_token_to_blacklist(self, token: str):
        """
        This method adds JWT Token to the blacklist
        by provided str token value. We need this to
        logout user.

        :param token: str value of JWT token
        """
        stmt = insert(JWTTokensBlackList).values(jwt_token=token)
        async with self.session.begin():
            await self.session.execute(stmt)
            await self.session.commit()

    async def token_in_blacklist(self, token: str):
        """
        This method trying to find token
        in blacklist.

        :param token: str value of JWT token
        """
        query = exists(JWTTokensBlackList).where(
            JWTTokensBlackList.jwt_token == token
        ).select()
        async with self.session.begin():
            res = await self.session.execute(query)
            result = res.scalar()
        return result


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
        if await manager.token_in_blacklist(token=token):
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        auth_value: str = payload.get('auth_value')
        if auth_value is None:
            raise credentials_exception
        token_data = JWTTokenData(auth_value=auth_value)
    except JWTError:
        raise credentials_exception
    user = await manager.get_user_by_username_or_email(token_data.auth_value)
    if user is None:
        raise credentials_exception
    return user


async def get_active_user(
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            detail='User is inactive!',
            status_code=400
        )
    return current_user


async def get_active_owner(
        current_user: User = Depends(get_active_user)
):
    if not DEBUG:
        if not current_user.is_owner:
            raise HTTPException(
                detail='Only owner can have access to this endpoint!',
                status_code=403
            )
    return current_user


async def get_current_user_token(
        token: str = Depends(oauth2_scheme)
):
    return token


async def get_managers(
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    user_manager = UserManager(session=session)
    token_manager = AuthTokenManager(session=session)
    jwt_token_manager = JWTTokenManager(session=session)
    return {
        'user_manager': user_manager,
        'token_manager': token_manager,
        'jwt_token_manager': jwt_token_manager
    }
