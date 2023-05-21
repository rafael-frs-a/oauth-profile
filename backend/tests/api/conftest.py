import pytest
from fastapi.testclient import TestClient
from src.app import app
from tests.api.error import views as error_views


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def pytest_configure() -> None:
    app.include_router(error_views.router, prefix='/test')
