from datetime import datetime, timedelta
from fastapi import status
from fastapi.testclient import TestClient
from src.api import utils
from src.api.v1.auth.enums import TokenType
from src.db.models.user import User


def test_user_not_found(client: TestClient) -> None:
    token_payload = {
        'user_id': 123,
        'exp': datetime.utcnow() + timedelta(seconds=10),
        'type': TokenType.ACCESS_TOKEN.name,
    }
    token = utils.make_app_token(token_payload)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/v1/user/profile', headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert not response_json['success']
    assert response_json['errors']


def test_success(client: TestClient, user: User) -> None:
    token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=10),
        'type': TokenType.ACCESS_TOKEN.name,
    }
    token = utils.make_app_token(token_payload)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/v1/user/profile', headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['success']
    assert not response_json['errors']
    assert response_json['data']
    assert response_json['data']['email'] == user.email
    assert response_json['data']['compiledProfile'] is not None
    assert response_json['data']['history'] is not None
