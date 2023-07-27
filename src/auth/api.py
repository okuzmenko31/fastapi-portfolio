from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings.database import get_async_session

from .services import UserManager
from .token import AuthTokenManager
from .schemas import UserCreate, UserShow

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


async def get_managers(
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    user_manager = UserManager(session=session)
    token_manager = AuthTokenManager(session=session)
    return {
        'user_manager': user_manager,
        'token_manager': token_manager
    }


@router.post('/registration/')
async def create_user(
        data: UserCreate,
        managers: dict = Depends(get_managers)
) -> UserShow:
    user_manager: UserManager = managers['user_manager']
    token_manager: AuthTokenManager = managers['token_manager']
    token_manager.token_type = 'su'
    try:
        user: UserShow = await user_manager.create_new_user(data)
        await token_manager.send_tokenized_mail(
            url_main_part='/confirm_email_and_set_active/',
            email=user.email,
            router_prefix=router.prefix
        )
        return user
    except IntegrityError as error:
        raise HTTPException(detail=f'Database error: {error}',
                            status_code=503)


@router.post('/confirm_email_and_set_active/{token}/{email}')
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
