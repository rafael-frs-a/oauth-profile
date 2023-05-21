import pytest
from src.api.v1.auth import config


@pytest.fixture
def auth0_oauth_url() -> str:
    return f'{config.AUTH0_BASE_URL}/oauth/token'
