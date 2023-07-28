from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings.database import get_async_session
from src.settings.config import ACCESS_TOKEN_EXPIRE_MINUTES

from .models import User

from .services import UserManager, JWTTokenManager, get_active_user
from .token import AuthTokenManager
from .schemas import UserCreate, UserShow, JWTTokenSchema, UserLogin

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


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


@router.post('/registration/', response_model=UserShow)
async def create_user(
        data: UserCreate,
        managers: dict = Depends(get_managers)
) -> UserShow:
    user_manager: UserManager = managers['user_manager']
    token_manager: AuthTokenManager = managers['token_manager']
    token_manager.token_type = 'su'
    try:
        as_owner = False
        if data.secret_phrase is not None:
            as_owner = True
        user: UserShow = await user_manager.create_new_user(data, as_owner)
        await token_manager.send_tokenized_mail(
            url_main_part='/confirm_email_and_set_active/',
            email=user.email,
            router_prefix=router.prefix
        )
        return user
    except IntegrityError as error:
        raise HTTPException(detail=f'Database error: {error}',
                            status_code=503)


@router.post('/confirm_email_and_set_active/{token}/{email}/',
             response_model=UserShow)
async def confirm_email_and_set_active(
        token: str,
        email: str,
        managers: dict = Depends(get_managers)
):
    token_manager: AuthTokenManager = managers['token_manager']
    token_data = await token_manager.get_token_data(
        token=token,
        email=email
    )
    if token_data.token:
        user_manager: UserManager = managers['user_manager']
        user = await user_manager.get_user_by_email(email=email)
        return await user_manager.set_user_active(user=user)
    else:
        raise HTTPException(
            detail=token_data.error,
            status_code=400
        )


@router.post('/login/', response_model=JWTTokenSchema)
async def login_for_access_token(
        data: UserLogin,
        managers: dict = Depends(get_managers)
):
    jwt_manager: JWTTokenManager = managers['jwt_token_manager']
    user = await jwt_manager.authenticate_user(
        auth_value=data.auth_value,
        password=data.password
    )
    if not user:
        raise HTTPException(
            detail='Incorrect username/email or password!',
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await jwt_manager.create_access_token(
        data={'auth_value': data.auth_value},
        expires_delta=access_token_expires
    )
    return JWTTokenSchema(
        access_token=access_token,
        token_type='bearer'
    )


@router.get("/me/", response_model=UserShow)
async def read_users_me(
        current_user: User = Depends(get_active_user)
):
    return UserShow(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        is_owner=current_user.is_owner,
        roles=current_user.roles
    )
