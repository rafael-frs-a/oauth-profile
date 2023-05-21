import urllib.parse
import sqlalchemy_utils as sa_utils
from . import config


def create_db_if_not_exists() -> str:
    url = get_db_connection_string(async_conn=False)

    if not sa_utils.database_exists(url):
        sa_utils.create_database(url)

    return url


def get_db_connection_string(async_conn: bool = False, escape_interpolation: bool = False) -> str:
    def _escape_value(value: str) -> str:
        result = urllib.parse.quote_plus(value)
        return result.replace('%', '%%') if escape_interpolation else result

    escaped_username = _escape_value(config.DB_USERNAME)
    escaped_password = _escape_value(config.DB_PASSWORD)
    escaped_db_name = _escape_value(config.DB_NAME)

    if async_conn:
        return f'postgresql+asyncpg://{escaped_username}:{escaped_password}@{config.DB_HOST}:{config.DB_PORT}/{escaped_db_name}'

    return f'postgresql://{escaped_username}:{escaped_password}@{config.DB_HOST}:{config.DB_PORT}/{escaped_db_name}'
