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
    type_writer_infos: Mapped[list['TypeWriterInfo']] = relationship(back_populates='portfolio_info')


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
