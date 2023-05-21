from fastapi import status
from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    response = client.get('/health-check')
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['success']
    assert not response_json['errors']
