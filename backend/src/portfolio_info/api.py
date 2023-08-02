from fastapi import Depends
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.settings.database import get_async_session

from .services import PortfolioInfoManager

router = APIRouter(
    prefix='/portfolio_info',
    tags=['Portfolio Info']
)


@router.post('/create/')
async def create_portfolio_info(
        session: AsyncSession = Depends(get_async_session)
):
    manager = PortfolioInfoManager(session)
    info = await manager.create_portfolio_info()
    return {}
