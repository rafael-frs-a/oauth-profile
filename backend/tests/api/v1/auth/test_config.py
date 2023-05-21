from src.api.v1.auth import config


def test_config() -> None:
    assert config.AUTH0_CLIENT_ID
    assert config.AUTH0_CLIENT_SECRET
    assert config.AUTH0_DOMAIN
