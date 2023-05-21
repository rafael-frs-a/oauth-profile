from src.api import config


def test_config() -> None:
    assert config.SECRET_KEY
    assert config.ALLOWED_ORIGINS
