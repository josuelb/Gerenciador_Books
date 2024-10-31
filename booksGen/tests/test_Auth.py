from http import HTTPStatus


def test_login_access_token(client, user):
    response = client.post(
        "/auth/token",
        data={
            "username": user.username, 
            "password": user.clean_password
        }
    )

    jwt = response.json()

    assert response.status_code == HTTPStatus.OK
    assert jwt["access_token"] is not None
    assert jwt["token_type"] == 'Bearer'