from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_reg


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_reg.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_reg.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(model=User, time=datetime(2026, 8, 9)):
    """
    mapper -> mapper do próprio ORM
    connection -> o que estabelece a conexão, imagino que o session
    target -> o alvo dessa função
    """

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "createdAt"):
            target.createdAt = time  # defino com o tempo que eu desejo

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):  # fixture para que tenhamos um user para tests
    user = User(username="Teste", email="test@test.com", password="testtest")
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
