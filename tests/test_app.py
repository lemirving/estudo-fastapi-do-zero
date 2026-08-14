from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act - Executa a coisa(SUT)
    - Garanta que A é A

    """

    response = client.get("/")
    assert response.json() == {"message": "Hello World"}
    assert response.status_code == HTTPStatus.OK
