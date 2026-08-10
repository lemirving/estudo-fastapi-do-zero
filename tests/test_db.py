from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):

    with mock_db_time(model=User, time=datetime.now()) as time:
        # isso permite que tudo aconteça na data mock que eu
        # defini em conftest
        new_user = User(username="test", email="test@test", password="secret")

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == "test"))

    assert asdict(user) == {
        "id": 1,
        "username": "test",
        "email": "test@test",
        "password": "secret",
        "createdAt": time,  # com o tempo mock lá em cima,
        # podemos fazer o teste se
        # ta rolando, já que não tem como acessar o tempo do db
        # lá no mock_time, cria-se uma condiçao pra modificar o
        # created_at com o tempo q eu estabelecer
        # com isso, o time retornado será um time conhecido
    }
