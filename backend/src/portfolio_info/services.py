from fastapi import HTTPException

from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, and_, select, delete

from .models import PortfolioInfo, Social
from .schemas import (PortfolioInfoSchema,
                      SocialSchema,
                      AllSocialsShow)


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

    async def get_social_by_id(self, social_id) -> Union[Social, None]:
        query = select(Social).where(Social.id == social_id)
        async with self.session.begin():
            res = await self.session.execute(query)
            result = res.scalar()
        if result is None:
            raise HTTPException(
                detail='Social with provided id does not exists!',
                status_code=400
            )
        return result

    async def create_social(
            self,
            data: SocialSchema,
            info: PortfolioInfo
    ) -> SocialSchema:
        values_dict = {
            Social.name: data.name,
            Social.link: data.link
        }
        if await self.check_exists(Social, values_dict):
            raise HTTPException(
                detail='Social with this name and link is already exists!',
                status_code=400
            )
        social = Social(
            name=data.name,
            link=data.link
        )
        async with self.session.begin():
            info.socials.append(social)
            await self.session.commit()
        return SocialSchema(
            name=social.name,
            link=social.link
        )

    async def update_social(
            self,
            data: SocialSchema,
            social_id: str
    ) -> SocialSchema:
        social = await self.get_social_by_id(social_id)
        values_dict = {
            Social.name: data.name,
            Social.link: data.link
        }
        if await self.check_exists(Social, values_dict):
            raise HTTPException(
                detail='Please, provide new name and link for this social.',
                status_code=400
            )
        async with self.session.begin():
            social.name = data.name
            social.link = data.link
            await self.session.commit()
        return SocialSchema(
            name=social.name,
            link=social.link
        )

    async def delete_social(self, social_id: str):
        stmt = delete(Social).where(Social.id == social_id)
        async with self.session.begin():
            await self.session.execute(stmt)
            await self.session.commit()

    async def get_socials(self, info: PortfolioInfo) -> AllSocialsShow:
        socials_lst = []
        async with self.session.begin():
            socials = info.socials
            for social in socials:
                socials_lst.append(
                    SocialSchema(
                        name=social.name,
                        link=social.link
                    )
                )
        return AllSocialsShow(
            socials=socials_lst
        )


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
