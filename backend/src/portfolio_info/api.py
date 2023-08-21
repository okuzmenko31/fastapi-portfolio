from fastapi import Depends
from fastapi.routing import APIRouter

from starlette.responses import JSONResponse
from starlette import status

from src.auth.dependencies import get_active_owner

from .services import PortfolioInfoManager, portfolio_info_manager
from .schemas import (PortfolioInfoSchema,
                      SocialSchema,
                      AllSocialsShow)
from .exceptions import PortfolioInfoDoesNotExists

router = APIRouter(
    prefix='/portfolio_info',
    tags=['Portfolio Info']
)


@router.get('', response_model=PortfolioInfoSchema)
async def get_portfolio_info(
        manager: PortfolioInfoManager = Depends(portfolio_info_manager)
):
    info = await manager.get_portfolio_info()
    if info is None:
        raise PortfolioInfoDoesNotExists
    return PortfolioInfoSchema(
        owner_name=info.owner_name
    )


@router.post('/create/', response_model=PortfolioInfoSchema)
async def create_portfolio_info(
        data: PortfolioInfoSchema,
        _owner=Depends(get_active_owner),
        manager: PortfolioInfoManager = Depends(portfolio_info_manager)
) -> PortfolioInfoSchema:
    info = await manager.create_portfolio_info(data)
    return info


@router.put('/update/', response_model=PortfolioInfoSchema)
async def update_portfolio_info(
        data: PortfolioInfoSchema,
        _owner=Depends(get_active_owner),
        manager: PortfolioInfoManager = Depends(portfolio_info_manager)
) -> PortfolioInfoSchema:
    info = await manager.update_portfolio_info(data)
    return info


@router.delete('/delete/')
async def delete_portfolio_info(
    manager: PortfolioInfoManager = Depends(portfolio_info_manager)
):
    await manager.delete_portfolio_info()
    return JSONResponse(content={
        'detail': 'Portfolio info was successfully deleted!'
    }, status_code=status.HTTP_200_OK)


@router.get('/socials/', response_model=AllSocialsShow)
async def get_socials(
        manager: PortfolioInfoManager = Depends(portfolio_info_manager)
) -> AllSocialsShow:
    info = await manager.get_portfolio_info()
    socials = await manager.get_socials(info)
    return socials


@router.post('/create_social/', response_model=SocialSchema)
async def create_social(
        data: SocialSchema,
        _owner=Depends(get_active_owner),
        manager: PortfolioInfoManager = Depends(portfolio_info_manager)
) -> SocialSchema:
    info = await manager.get_portfolio_info()
    if info is None:
        raise PortfolioInfoDoesNotExists
    social = await manager.create_social(data, info)
    return social


@router.put('/update_social/{social_id}/', response_model=SocialSchema)
async def update_social(
        social_id: str,
        data: SocialSchema,
        _owner=Depends(get_active_owner),
        manager: PortfolioInfoManager = Depends(portfolio_info_manager)
) -> SocialSchema:
    social = await manager.update_social(data, social_id)
    return social


@router.delete('/delete_social/{social_id}/')
async def delete_social(
        social_id: str,
        _owner=Depends(get_active_owner),
        manager: PortfolioInfoManager = Depends(portfolio_info_manager)
):
    await manager.delete_social(social_id)
    return JSONResponse(
        content={
            'success': 'You successfully deleted this social!'
        }, status_code=status.HTTP_200_OK
    )
