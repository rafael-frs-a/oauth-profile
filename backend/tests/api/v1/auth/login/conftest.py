import pytest
from datetime import datetime, timedelta
from src.api import utils


@pytest.fixture
def valid_nonce() -> str:
    token_payload = {
        'id': 'test-id',
        'exp': datetime.utcnow() + timedelta(seconds=10),
    }
    return utils.make_app_token(token_payload)
