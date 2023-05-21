import typing
from datetime import datetime, timedelta
from fastapi import status
from fastapi.testclient import TestClient
from src.api import utils
from src.api.v1.auth.enums import TokenType


def test_missing_data(client: TestClient) -> None:
    payload: dict[typing.Any, typing.Any] = {}
    response = client.post('/api/v1/auth/refresh-token', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


def test_invalid_token(client: TestClient) -> None:
    payload = {'refreshToken': 'invalid-token'}
    response = client.post('/api/v1/auth/refresh-token', json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


def test_expired_token(client: TestClient) -> None:
    token_payload = {
        'user_id': 123,
        'exp': datetime.utcnow() - timedelta(seconds=1),
        'type': TokenType.REFRESH_TOKEN.name,
    }
    refresh_token = utils.make_app_token(token_payload)
    payload = {'refreshToken': refresh_token}
    response = client.post('/api/v1/auth/refresh-token', json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


def test_wrong_kind_token(client: TestClient) -> None:
    token_payload = {
        'user_id': 123,
        'exp': datetime.utcnow() + timedelta(seconds=10),
        'type': TokenType.ACCESS_TOKEN.name,
    }
    refresh_token = utils.make_app_token(token_payload)
    payload = {'refreshToken': refresh_token}
    response = client.post('/api/v1/auth/refresh-token', json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


def test_success(client: TestClient) -> None:
    token_payload = {
        'user_id': 123,
        'exp': datetime.utcnow() + timedelta(seconds=10),
        'type': TokenType.REFRESH_TOKEN.name,
    }
    refresh_token_payload = utils.make_app_token(token_payload)
    payload = {'refreshToken': refresh_token_payload}
    response = client.post('/api/v1/auth/refresh-token', json=payload)

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['success']
    assert not response_json['errors']
    assert response_json['data']['accessToken']
    assert response_json['data']['refreshToken']

    decode_result = utils.decode_app_token(response_json['data']['accessToken'])
    assert decode_result.success, decode_result.errors
    assert decode_result.data
    access_token = decode_result.data
    assert access_token['user_id'] is not None
    assert access_token['type'] == TokenType.ACCESS_TOKEN.name

    decode_result = utils.decode_app_token(response_json['data']['refreshToken'])
    assert decode_result.success, decode_result.errors
    assert decode_result.data
    refresh_token = decode_result.data
    assert refresh_token['user_id'] == access_token['user_id']
    assert refresh_token['type'] == TokenType.REFRESH_TOKEN.name
