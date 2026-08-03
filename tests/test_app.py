from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act - Executa a coisa(SUT)
    - Garanta que A é A

    """

    client = TestClient(app)
    response = client.get("/")
    assert response.json() == {"message": "hello world"}
    assert response.status_code == HTTPStatus.OK
