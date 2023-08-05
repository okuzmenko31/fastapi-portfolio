from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from src.settings.config import ACCESS_TOKEN_EXPIRE_MINUTES

from .models import User
from .services import (UserManager,
                       JWTTokenManager,
                       get_active_user,
                       get_current_user_token,
                       get_managers, get_active_owner)
from .token import AuthTokenManager
from .schemas import (UserCreate,
                      UserShow,
                      JWTTokenSchema,
                      UserLogin,
                      EmailSchema,
                      PasswordResetSchema,
                      ChangePasswordSchema,
                      ChangeEmailSchema)

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/registration/')
async def create_user(
        data: UserCreate,
        managers: dict = Depends(get_managers)
) -> JSONResponse:
    try:
        user_manager: UserManager = managers['user_manager']
        token_manager: AuthTokenManager = managers['token_manager']
        token_manager.token_type = 'su'

        user: UserShow = await user_manager.create_new_user(data, data.secret_phrase)
        msg: str = await token_manager.send_tokenized_mail(
            url_main_part='/confirm_email_and_set_active/',
            email=user.email,
            router_prefix=router.prefix
        )
        return JSONResponse(content={
            'message': msg
        }, status_code=200)
    except IntegrityError as error:
        raise HTTPException(detail=f'Database error: {error}',
                            status_code=503)


@router.post('/confirm_email_and_set_active/{token}/{email}/')
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
        await user_manager.set_user_active(user=user)
        return JSONResponse(
            content={
                'detail': 'You successfully registered and confirmed your email!'
            }, status_code=200
        )
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
            detail='Incorrect username/email or password! Or account is not confirmed!',
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


@router.post('/logout/')
async def logout(token: str = Depends(get_current_user_token),
                 managers: dict = Depends(get_managers)):
    manager: JWTTokenManager = managers['jwt_token_manager']
    await manager.add_token_to_blacklist(token)
    return {
        'status_code': 200,
        'detail': 'You successfully logged out!'
    }


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


@router.post('/password_reset_request/')
async def reset_password_request(data: EmailSchema,
                                 managers: dict = Depends(get_managers)):
    manager: UserManager = managers['user_manager']
    user = await manager.get_user_by_email(email=data.email)
    if user is None:
        return JSONResponse(content={
            'error': 'User with provided email does not exists!'
        }, status_code=400)
    token_manager: AuthTokenManager = managers['token_manager']
    token_manager.token_type = 'pr'
    msg = await token_manager.send_tokenized_mail(url_main_part='/password_reset/',
                                                  email=data.email,
                                                  router_prefix=router.prefix)
    return JSONResponse(content={
        'success': msg
    }, status_code=200)


@router.put('/password_reset/{token}/{email}/')
async def reset_password(token: str,
                         email: str,
                         data: PasswordResetSchema,
                         managers: dict = Depends(get_managers)):
    manager: AuthTokenManager = managers['token_manager']
    token_data = await manager.get_token_data(
        token=token,
        email=email,
        delete_token=False
    )
    if token_data.token:
        user_manager: UserManager = managers['user_manager']
        user = await user_manager.get_user_by_email(email=email)
        await user_manager.set_new_password(user, data.password)
        await manager.delete_exists_token(token=token_data.token.token)

        return JSONResponse(content={
            'success': 'Successful password reset!'
        }, status_code=200)
    else:
        raise HTTPException(
            detail=token_data.error,
            status_code=400
        )


@router.put('/change_password/')
async def change_password(
        data: ChangePasswordSchema,
        current_user: User = Depends(get_active_user),
        managers: dict = Depends(get_managers)
):
    manager: UserManager = managers['user_manager']
    await manager.change_password(current_user, data.old_password, data.password)

    return JSONResponse(content={
        'success': 'You successfully changed your password!'
    }, status_code=200)


@router.post('/change_email_request/')
async def change_email(
        data: ChangeEmailSchema,
        current_user: User = Depends(get_active_user),
        managers: dict = Depends(get_managers)
):
    user_manager: UserManager = managers['user_manager']
    if current_user.email == data.email:
        raise HTTPException(
            detail='You cannot change your email to the one you have now!',
            status_code=400
        )
    if await user_manager.check_email_exists(data.email):
        raise HTTPException(
            detail='User with provided email is already exists!',
            status_code=400
        )
    token_manager: AuthTokenManager = managers['token_manager']
    token_manager.token_type = 'ce'
    msg = await token_manager.send_tokenized_mail(url_main_part='/change_email_confirmation/',
                                                  email=data.email,
                                                  router_prefix=router.prefix)
    return JSONResponse(content={
        'success': msg
    }, status_code=200)


@router.put('/change_email_confirmation/{token}/{email}/')
async def change_email_confirm(
        token: str,
        email: str,
        current_user: User = Depends(get_active_user),
        managers: dict = Depends(get_managers)

):
    manager: AuthTokenManager = managers['token_manager']
    token_data = await manager.get_token_data(
        token=token,
        email=email
    )
    if token_data.token:
        user_manager: UserManager = managers['user_manager']
        await user_manager.set_new_email(current_user, email)

        return JSONResponse(content={
            'success': 'You successfully confirmed new email!'
        }, status_code=200)
    else:
        raise HTTPException(
            detail=token_data.error,
            status_code=400
        )


@router.get('/all_users/', response_model=list[UserShow])
async def get_all_users(
        managers: dict = Depends(get_managers),
) -> list[UserShow]:
    user_manager: UserManager = managers['user_manager']
    result = await user_manager.get_all_users()
    return result
