import pytest
from sqlalchemy.future import Engine
from sqlmodel import Session
from src.db.models.user import User


@pytest.fixture
def user(ephemeral_test_engine: Engine) -> User:
    user = User(email='mary@doe.com')

    with Session(ephemeral_test_engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

    return user
