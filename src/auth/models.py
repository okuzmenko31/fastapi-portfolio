import datetime
import uuid

import sqlalchemy.types as types

from enum import Enum

from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func

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
                                        default=[Roles.role_visitor],
                                        nullable=False)

    def __repr__(self):
        return f'User: {self.username}'

    @property
    def is_owner(self):
        return Roles.role_owner in self.roles


class TokenChoicesTypes(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super().__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]


class AuthToken(Base):
    __tablename__ = 'auth_tokens'

    TOKEN_TYPES = {
        'su': 'su',
        'ce': 'ce',
        'pr': 'pr'
    }
    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                           default=uuid.uuid4)
    token: Mapped[str] = mapped_column(String(32),
                                       unique=True,
                                       nullable=False)
    token_type: Mapped[str] = mapped_column(TokenChoicesTypes(TOKEN_TYPES),
                                            nullable=False)
    token_owner: Mapped[str] = mapped_column(String(150),
                                             nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                       server_default=func.now())
    expired: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'Owner: {self.token_owner}. Type: {self.token_type}'
