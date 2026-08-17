from dataclasses import asdict
from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):

    with mock_db_time(model=User, time=datetime.now()) as time:
        # isso permite que tudo aconteça na data mock que eu
        # defini em conftest
        new_user = User(username="test", email="test@test", password="secret")

        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == "test")
        )

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
