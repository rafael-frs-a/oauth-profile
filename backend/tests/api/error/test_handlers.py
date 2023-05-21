import httpx
import pytest
from datetime import datetime, timedelta
from fastapi import status
from fastapi.testclient import TestClient
from src.api import utils
from src.api.v1.auth.enums import TokenType
from . import views


def _check_401_authentication_error(response: httpx.Response) -> None:
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']
    assert len(response_json['errors']) == 1
    assert response_json['errors'][0]['header'] == 'Authorization'
    assert response_json['errors'][0]['status'] == status.HTTP_401_UNAUTHORIZED


def test_401_token_missing(client: TestClient) -> None:
    response = client.get('/test/error/401')
    _check_401_authentication_error(response)


def test_401_invalid_token(client: TestClient) -> None:
    headers = {'Authorization': 'Bearer invalid-token'}
    response = client.get('/test/error/401', headers=headers)
    _check_401_authentication_error(response)


def test_401_token_expired(client: TestClient) -> None:
    token_payload = {
        'user_id': 123,
        'exp': datetime.utcnow() - timedelta(seconds=1),
        'type': TokenType.ACCESS_TOKEN.name,
    }
    token = utils.make_app_token(token_payload)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/test/error/401', headers=headers)
    _check_401_authentication_error(response)


def test_401_token_wrong_type(client: TestClient) -> None:
    token_payload = {
        'user_id': 123,
        'exp': datetime.utcnow() + timedelta(seconds=10),
        'type': TokenType.REFRESH_TOKEN.name,
    }
    token = utils.make_app_token(token_payload)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/test/error/401', headers=headers)
    _check_401_authentication_error(response)


def test_401_success(client: TestClient) -> None:
    token_payload = {
        'user_id': 123,
        'exp': datetime.utcnow() + timedelta(seconds=10),
        'type': TokenType.ACCESS_TOKEN.name,
    }
    token = utils.make_app_token(token_payload)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/test/error/401', headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['success']
    assert not response_json['errors']


def test_404(client: TestClient) -> None:
    response = client.get('/fake-non-existent-route')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors'][0]['message'] == 'Not found'


def test_405(client: TestClient) -> None:
    response = client.post('/test/error/405')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors'][0]['message'] == 'Method not allowed'

    response = client.get('/test/error/405')
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['success']
    assert not response_json['errors']


def test_418(client: TestClient) -> None:
    response = client.get('/test/error/418')
    assert response.status_code == status.HTTP_418_IM_A_TEAPOT
    response_json = response.json()
    assert response_json['success']
    assert response_json['data'] == '🍵'
    assert not response_json['errors']


def test_server_error(client: TestClient) -> None:
    with pytest.raises(views.TestException):
        client.get('/test/error/500')
