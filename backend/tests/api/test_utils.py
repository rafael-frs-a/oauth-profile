from datetime import datetime, timedelta
from src.api import utils


def test_decode_app_token() -> None:
    response = utils.decode_app_token('invalid-token')

    assert not response.success
    assert response.errors
    assert len(response.errors) == 1
    assert response.errors[0].message == 'Invalid token'

    payload = {'id': 123, 'exp': datetime.utcnow() - timedelta(seconds=1)}
    token = utils.make_app_token(payload)
    response = utils.decode_app_token(token)

    assert not response.success
    assert response.errors
    assert len(response.errors) == 1
    assert response.errors[0].message == 'Expired token'

    payload = {'id': 123, 'exp': datetime.utcnow() + timedelta(seconds=10)}
    token = utils.make_app_token(payload)
    response = utils.decode_app_token(token)

    assert response.success
    assert not response.errors
    assert response.data
    assert response.data['id'] == payload['id']
