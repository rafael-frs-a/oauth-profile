import pytest
import typing
import sqlalchemy_utils as sa_utils
from sqlalchemy.future import Engine
from sqlmodel import SQLModel, create_engine
from src.db import config, engine, utils


@pytest.fixture(autouse=True, scope='session')
def ephemeral_test_engine() -> typing.Generator[Engine, None, None]:
    config.DB_NAME = 'test_' + config.DB_NAME
    db_url = None
    local_engine = None

    try:
        db_url = utils.create_db_if_not_exists()
        local_engine = create_engine(db_url, echo=True)
        local_engine.connect
        SQLModel.metadata.create_all(local_engine)
        engine.async_engine = engine.make_async_engine()

        yield local_engine
    finally:
        if local_engine:
            local_engine.dispose()

        if db_url and sa_utils.database_exists(db_url):
            sa_utils.drop_database(db_url)
