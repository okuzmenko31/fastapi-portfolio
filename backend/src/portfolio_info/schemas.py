from typing import Optional

from pydantic import BaseModel


class MainSchema(BaseModel):
    class Config:
        from_attributes = True


class SocialSchema(MainSchema):
    name: str
    link: str


class PortfolioInfoSchema(MainSchema):
    owner_name: str


class CreateSocials(MainSchema):
    socials: list[SocialSchema]
