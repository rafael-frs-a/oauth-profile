from src.db import config


def test_config() -> None:
    assert config.DB_USERNAME
    assert config.DB_PASSWORD
    assert config.DB_HOST
    assert config.DB_PORT
    assert config.DB_NAME
    assert config.DB_ENCRYPTION_KEY
