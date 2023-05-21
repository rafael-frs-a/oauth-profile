import typing
import httpx
import respx
from fastapi import status
from fastapi.testclient import TestClient
from src.api import utils
from src.api.v1.auth.enums import TokenType


def test_missing_data(client: TestClient) -> None:
    payload: dict[typing.Any, typing.Any] = {}
    response = client.post('/api/v1/auth/login', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


def test_invalid_data(client: TestClient) -> None:
    payload = {
        'code': 'test-code',
        'callbackUrl': 'invalid-url',
        'redirectAfterLogoutUrl': 'invalid-url',
        'nonce': 'test-nonce',
    }

    response = client.post('/api/v1/auth/login', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


@respx.mock
def test_invalid_nonce(client: TestClient, auth0_oauth_url: str) -> None:
    payload = {
        'code': 'test-code',
        'callbackUrl': 'http://localhost:3000/login/callback',
        'redirectAfterLogoutUrl': 'http://localhost:3000/profile',
        'nonce': 'test-nonce',
    }

    respx.post(auth0_oauth_url).mock(return_value=httpx.Response(status_code=status.HTTP_200_OK))
    response = client.post('/api/v1/auth/login', json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


@respx.mock
def test_auth0_failed_response(client: TestClient, auth0_oauth_url: str, valid_nonce: str) -> None:
    payload = {
        'code': 'test-code',
        'callbackUrl': 'http://localhost:3000/login/callback',
        'redirectAfterLogoutUrl': 'http://localhost:3000/profile',
        'nonce': valid_nonce,
    }

    respx.post(auth0_oauth_url).mock(return_value=httpx.Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY))
    response = client.post('/api/v1/auth/login', json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


@respx.mock
def test_authentication_not_supported(client: TestClient, auth0_oauth_url: str, valid_nonce: str) -> None:
    payload = {
        'code': 'test-code',
        'callbackUrl': 'http://localhost:3000/login/callback',
        'redirectAfterLogoutUrl': 'http://localhost:3000/profile',
        'nonce': valid_nonce,
    }

    token_payload = {'name': 'John Doe', 'nonce': valid_nonce}
    id_token = utils.make_app_token(token_payload)
    auth0_response = {
        'access_token': 'test-access-token',
        'id_token': id_token,
    }

    respx.post(auth0_oauth_url).mock(return_value=httpx.Response(
        status_code=status.HTTP_200_OK,
        json=auth0_response
    ))

    response = client.post('/api/v1/auth/login', json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']
    assert response_json['errors'][0]['message'] == 'Authentication method not supported'


@respx.mock
def test_success(client: TestClient, auth0_oauth_url: str, valid_nonce: str) -> None:
    payload = {
        'code': 'test-code',
        'callbackUrl': 'http://localhost:3000/login/callback',
        'redirectAfterLogoutUrl': 'http://localhost:3000/profile',
        'nonce': valid_nonce,
    }

    token_payload = {'email': 'john@doe.com', 'nonce': valid_nonce}
    id_token = utils.make_app_token(token_payload)
    auth0_response = {
        'access_token': 'test-access-token',
        'id_token': id_token,
    }

    respx.post(auth0_oauth_url).mock(return_value=httpx.Response(
        status_code=status.HTTP_200_OK,
        json=auth0_response
    ))

    response = client.post('/api/v1/auth/login', json=payload)

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['success']
    assert not response_json['errors']
    assert response_json['data']
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
