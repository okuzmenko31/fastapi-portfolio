from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException

from .models import User
from .schemas import JWTTokenData
from .services import UserManager, JWTTokenManager
from .token import AuthTokenManager

from src.settings.database import get_async_session
from src.settings.config import oauth2_scheme, SECRET_KEY, JWT_ALGORITHM, DEBUG


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


async def get_current_user_token(
        token: str = Depends(oauth2_scheme)
):
    return token


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
