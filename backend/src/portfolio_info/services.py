from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, and_

from .models import PortfolioInfo, Social
from .schemas import PortfolioInfoSchema, SocialSchema


class PortfolioInfoManager:

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
                info.socials.append(social_obj)
        return socials_show

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
        socials = await self.create_socials(data.socials, info)
        async with self.session.begin():
            self.session.add(info)
            await self.session.commit()
        await self.session.refresh(info, attribute_names=['socials'])

        return PortfolioInfoSchema(
            owner_name=info.owner_name,
            socials=socials
        )
