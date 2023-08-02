import uuid

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey

from src.settings.database import Base


class PortfolioInfo(Base):
    __tablename__ = 'portfolio_info'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                           default=uuid.uuid4)
    owner_name: Mapped[str] = mapped_column(String(40),
                                            nullable=False)
    type_writer_infos: Mapped[list['TypeWriterInfo']] = relationship(back_populates='portfolio_info',
                                                                     lazy='selectin')
    socials: Mapped[list['Social']] = relationship(back_populates='portfolio_info',
                                                   lazy='selectin')

    def __repr__(self):
        return f'Info about {self.owner_name}'


class Social(Base):
    __tablename__ = 'socials'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                           default=uuid.uuid4)
    portfolio_info_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('portfolio_info.id'))
    portfolio_info: Mapped['PortfolioInfo'] = relationship(back_populates='socials')
    name: Mapped[str] = mapped_column(String(35),
                                      nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f'Social: {self.name}. Link: {self.link}'


class TypeWriterInfo(Base):
    __tablename__ = 'type_writer_info'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                           default=uuid.uuid4)
    info: Mapped[str] = mapped_column(String(150),
                                      nullable=False)
    portfolio_info_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('portfolio_info.id'))
    portfolio_info: Mapped['PortfolioInfo'] = relationship(back_populates='type_writer_infos')

    def __repr__(self):
        return f'Info: {self.info}'
