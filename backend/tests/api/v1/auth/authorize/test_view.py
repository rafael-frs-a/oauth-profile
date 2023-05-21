import pytest
import typing
from fastapi import status
from fastapi.testclient import TestClient
from src.api import config


def test_missing_data(client: TestClient) -> None:
    payload: dict[typing.Any, typing.Any] = {}
    response = client.post('/api/v1/auth/authorize', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


def test_invalid_data(client: TestClient) -> None:
    payload = {
        'callbackUrl': 'invalid-url',
        'redirectAfterLogoutUrl': 'invalid-url',
    }
    response = client.post('/api/v1/auth/authorize', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


@pytest.mark.parametrize(
    'redirect_logout_url',
    [None, 'http://localhost:3000/profile']
)
def test_success(client: TestClient, redirect_logout_url: typing.Optional[str]) -> None:
    payload = {
        'callbackUrl': f'{config.FRONTEND_URL}/login/callback',
        'redirectAfterLogoutUrl': redirect_logout_url,
    }
    response = client.post('/api/v1/auth/authorize', json=payload)

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['success']
    assert not response_json['errors']
    response_data = response_json['data']
    assert response_data['authorizationUrl']
    assert response_data['logoutUrl']
    assert response_data['nonce']
