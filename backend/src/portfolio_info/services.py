from sqlalchemy.ext.asyncio import AsyncSession

from .models import PortfolioInfo


class PortfolioInfoManager:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_portfolio_info(self):
        info = PortfolioInfo(
            owner_name='Oleg Kuzmenko'
        )
        async with self.session.begin():
            self.session.add(info)
            await self.session.commit()

        lst = info.type_writer_infos
        print(lst)
        return info
