from fastapi import HTTPException

from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, and_, select

from .models import PortfolioInfo, Social
from .schemas import PortfolioInfoSchema, SocialSchema


class MainManager:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_exists(
            self,
            model,
            values_dict: dict
    ):
        values = (k == v for k, v in values_dict.items())
        query = exists(model).where(and_(values)).select()
        async with self.session.begin():
            res = await self.session.execute(query)
            result = res.scalar()
        return result


class SocialManager(MainManager):

    async def create_socials(self,
                             socials: list[SocialSchema],
                             info: PortfolioInfo):
        socials_show = []
        if socials is not None:
            for social in socials:
                values_dict = {
                    Social.name: social.name,
                    Social.link: social.link
                }
                if await self.check_exists(Social, values_dict):
                    raise HTTPException(
                        detail='Social with this name and link is already exists!',
                        status_code=400
                    )
                social_obj = Social(
                    name=social.name,
                    link=social.link
                )
                socials_show.append(
                    SocialSchema(
                        name=social.name,
                        link=social.link
                    )
                )
                async with self.session.begin():
                    info.socials.append(social_obj)
                    await self.session.commit()
        return socials_show


class PortfolioInfoManager(SocialManager):

    async def create_portfolio_info(self, data: PortfolioInfoSchema):
        values_dict = {
            PortfolioInfo.owner_name: data.owner_name
        }
        if await self.check_exists(PortfolioInfo, values_dict):
            raise HTTPException(
                detail='Portfolio Info with this owner is already exists!',
                status_code=400
            )
        info = PortfolioInfo(
            owner_name=data.owner_name
        )
        async with self.session.begin():
            self.session.add(info)
            await self.session.commit()

        return PortfolioInfoSchema(
            owner_name=info.owner_name
        )

    async def get_portfolio_info(self) -> Union[PortfolioInfo, None]:
        query = select(PortfolioInfo)
        async with self.session.begin():
            res = await self.session.execute(query)
            result = res.scalar()
        return result

    async def update_portfolio_info(self, data: PortfolioInfoSchema):
        info = await self.get_portfolio_info()
        if info is None:
            raise HTTPException(
                detail='First of all you need to create Portfolio Info!',
                status_code=400
            )
        if data.owner_name == info.owner_name:
            raise HTTPException(
                detail='Owner name must be different from the old one!',
                status_code=400
            )
        async with self.session.begin():
            info.owner_name = data.owner_name
            await self.session.commit()
        return PortfolioInfoSchema(
            owner_name=info.owner_name
        )
