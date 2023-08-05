import uuid

from pydantic import BaseModel


class MainSchema(BaseModel):
    class Config:
        from_attributes = True


class SocialSchema(MainSchema):
    name: str
    link: str


class PortfolioInfoSchema(MainSchema):
    owner_name: str


class AllSocialsShow(MainSchema):
    socials: list[SocialSchema]
