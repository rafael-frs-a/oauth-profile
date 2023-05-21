import typing
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from . import utils


def make_async_engine() -> AsyncEngine:
    return create_async_engine(
        utils.get_db_connection_string(async_conn=True),
        echo=True,
        future=True,
        poolclass=NullPool
    )


async_engine = make_async_engine()


@asynccontextmanager
async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
