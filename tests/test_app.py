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


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"username": "alice", "email": "alice@example.com", "password": "secret"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "email": "alice@example.com",
        "username": "alice",
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [{"id": 1, "email": "alice@example.com", "username": "alice"}]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={"username": "bob", "email": "bob@example.com", "password": "secret"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"username": "bob", "email": "bob@example.com", "id": 1}


def test_delete_user(client):
    response = client.delete("users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"username": "bob", "email": "bob@example.com", "id": 1}


def test_update_user_should_return_not_found__exercicio(client):
    response = client.put(
        "/users/666",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Deu ruim, não encontrei"}


def test_update_user_not_found(client):
    response = client.put(
        "/users/666",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Deu ruim, não encontrei"}


def test_get_user_not_found(client):
    response = client.get("/users/666")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Deu ruim, não encontrei"}


def test_get_user___exercicio(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }
