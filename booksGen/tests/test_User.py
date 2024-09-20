from http import HTTPStatus

from booksgen.schemas.schema_users import UserSchemaPublic

# Teste de criação
def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "test@190",
            "name": "test",
            "password": "testtest"
        }   
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["username"] == "test@190"

