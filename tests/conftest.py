from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fastapi_zero.app import app
from fastapi_zero.models import User, table_reg


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
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
