from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.settings.database import get_async_session

from .services import PortfolioInfoManager
from .schemas import PortfolioInfoSchema, SocialSchema, SocialUpdate

router = APIRouter(
    prefix='/portfolio_info',
    tags=['Portfolio Info']
)


@router.get('', response_model=PortfolioInfoSchema)
async def get_portfolio_info(
        session: AsyncSession = Depends(get_async_session)
):
    manager = PortfolioInfoManager(session)
    info = await manager.get_portfolio_info()
    if info is None:
        raise HTTPException(
            detail='Portfolio Info isn\'t created! Create it please.',
            status_code=400
        )
    return PortfolioInfoSchema(
        owner_name=info.owner_name
    )


@router.post('/create/', response_model=PortfolioInfoSchema)
async def create_portfolio_info(
        data: PortfolioInfoSchema,
        # owner=Depends(get_active_owner),
        session: AsyncSession = Depends(get_async_session)
) -> PortfolioInfoSchema:
    manager = PortfolioInfoManager(session)
    info = await manager.create_portfolio_info(data)
    return info


@router.put('/update/', response_model=PortfolioInfoSchema)
async def update_portfolio_info(
        data: PortfolioInfoSchema,
        session: AsyncSession = Depends(get_async_session)
) -> PortfolioInfoSchema:
    manager = PortfolioInfoManager(session)
    info = await manager.update_portfolio_info(data)
    return info


@router.post('/create_social/', response_model=SocialSchema)
async def create_social(
        data: SocialSchema,
        session: AsyncSession = Depends(get_async_session)
) -> SocialSchema:
    manager = PortfolioInfoManager(session)
    info = await manager.get_portfolio_info()
    if info is None:
        raise HTTPException(
            detail='First of all you need to create a Portfolio Info!',
            status_code=400
        )
    social = await manager.create_social(data, info)
    return social


@router.put('/update_social/', response_model=SocialSchema)
async def update_social(
        data: SocialUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> SocialSchema:
    manager = PortfolioInfoManager(session)
    social = await manager.update_social(data)
    return social
