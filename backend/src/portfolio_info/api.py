from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.settings.database import get_async_session

from .services import PortfolioInfoManager
from .schemas import PortfolioInfoSchema, CreateSocials, SocialSchema

router = APIRouter(
    prefix='/portfolio_info',
    tags=['Portfolio Info']
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


@router.post('/create_socials/', response_model=list[SocialSchema])
async def create_socials(
        data: CreateSocials,
        session: AsyncSession = Depends(get_async_session)
) -> list[SocialSchema]:
    manager = PortfolioInfoManager(session)
    info = await manager.get_portfolio_info()
    if info is None:
        raise HTTPException(
            detail='First of all you need to create Portfolio Info!',
            status_code=400
        )
    socials = await manager.create_socials(data.socials, info)
    return socials
