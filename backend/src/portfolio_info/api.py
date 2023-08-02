from fastapi import Depends
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.settings.database import get_async_session

from .services import PortfolioInfoManager
from .schemas import PortfolioInfoSchema

router = APIRouter(
    prefix='/portfolio_info',
    tags=['Portfolio Info']
)


@router.post('/create/', response_model=PortfolioInfoSchema)
async def create_portfolio_info(
        data: PortfolioInfoSchema,
        session: AsyncSession = Depends(get_async_session)
) -> PortfolioInfoSchema:
    manager = PortfolioInfoManager(session)
    info = await manager.create_portfolio_info(data)
    return info
