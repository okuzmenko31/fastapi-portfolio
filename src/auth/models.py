import uuid

from enum import Enum

from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.settings.database import Base


class Roles(str, Enum):
    role_visitor = 'role_visitor'
    role_owner = 'role_owner'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                           default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(35),
                                          unique=True,
                                          nullable=False)
    email: Mapped[str] = mapped_column(String(120),
                                       unique=True,
                                       nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[list] = mapped_column(ARRAY(String),
                                        nullable=False,
                                        default=[Roles.role_visitor])

    def __repr__(self):
        return f'User: {self.username}'

    @property
    def is_owner(self):
        return Roles.role_visitor in self.roles
