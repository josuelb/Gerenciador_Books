from http import HTTPStatus

from booksgen.schemas.schema_users import UserSchemaPublic


def test_list_user(client, user):
    response = client.get(
        f"/users/{user.id}"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["users"][0]["id"] == user.id

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

# Test de atualização
def test_updated_user(client, user):
    jsonResponse = {
        'username': 'testStore',
        'name': 'test',
        'password': 'passtest'
    }
    response = client.put(
        f'/users/{user.id}',
        json=jsonResponse
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "testStore",
        "name": "test",
    }


# Test de deletação 
def test_deleted_user(client, user):
    response = client.delete(
        url=f'/users/{user.id}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted'
    }

def test_head_user_OK(client, user):
    response = client.head(
        f"/users/head/{user.id}"
    )

    assert response.status_code == HTTPStatus.OK

def test_options_users_JSON(client, user):
    response = client.options(
        f"/users/options/{user.id}"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "allow": "GET, POST, PUT, DELETE, OPTIONS"
    }
