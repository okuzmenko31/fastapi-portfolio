import os

from typing import AsyncGenerator

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+asyncpg://postgres:password@localhost:5432/db_name?async_fallback=true'
)

engine = create_async_engine(DATABASE_URL,
                             future=True,
                             echo=True)

session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session() as async_session:
        yield async_session


def get_database_info() -> dict:
    return {
        'NAME': os.environ.get('DB_NAME', default='db_name'),
        'USER': os.environ.get('DB_USER', default='postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', default='postgres'),
        'HOST': os.environ.get('DB_HOST', default='localhost'),
        'PORT': os.environ.get('DB_PORT', default='5432')
    }


Base = declarative_base()
