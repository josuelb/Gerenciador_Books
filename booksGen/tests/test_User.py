from http import HTTPStatus

from booksgen.schemas.schema_users import UserSchemaPublic


def test_list_user(client, token):
    response = client.get(
        f"/users/",
        headers={'Authorization': f'Bearer {token}'}
    )
    

    assert response.status_code == HTTPStatus.OK
    
    users = response.json()["users"]

    assert users["id"] == 1

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

def test_updated_user(client, user, token):
    jsonResponse = {
        'username': 'testStore',
        'name': 'test',
        'password': 'passtest'
    }
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=jsonResponse
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "testStore",
        "name": "test",
    }


def test_deleted_user(client, user, token):
    response = client.delete(
        url=f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted'
    }

def test_head_user_OK(client, user, token):
    response = client.head(
        f"/users/head/{user.id}",
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK

def test_options_users_JSON(client, user):
    response = client.options(
        f"/users/options"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "allow": "GET, POST, PUT, DELETE, OPTIONS"
    }
