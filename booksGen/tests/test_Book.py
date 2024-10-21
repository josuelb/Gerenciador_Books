from http import HTTPStatus

from booksgen.schemas.schema_books import BookSchemaPublic
from booksgen.models import BookState, BookGenere


# Test de criação
def test_created_book(client, user):
    book_test = {
        "namebook" : "Sample Book",
        "author" : "Author Name",
        "yearbook" : 1999,
        "edition" : 1,
        "genere" : BookGenere.fantasy,
        "ISBN" : 1234567,
        "editionPublisher" : "Publisher Name",
        "summary" : "This is a summary.",
        "pageNum" :  20,
        "language" : "pt",
        "state" : BookState.start
    }
    
    response = client.post(
        f"/users/books/{user.id}/",
        json=book_test
    )


    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "namebook" : "Sample Book",
        "author" : "Author Name",
        "yearbook" : 1999,
        "edition" : 1,
        "genere" : BookGenere.fantasy,
        "ISBN" : 1234567,
        "editionPublisher" : "Publisher Name",
        "summary" : "This is a summary.",
        "pageNum" :  20,
        "language" : "pt",
        "state" : BookState.start,
        "user_id": user.id
    }


def test_list_all_books(client, user):
    response = client.get(
        f'/users/books/{user.id}'
    )


    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"books": []}

def test_update_all_book(client, user, book):
    book_auteration = {
        "namebook": "Updated Sample Book",
        "author": "Updated Author Name",
        "yearbook": 2000,
        "edition": 2,
        "genere": BookGenere.fantasy,
        "ISBN": 7654321,
        "editionPublisher": "Updated Publisher Name",
        "summary": "This is an updated summary.",
        "pageNum": 100,
        "language": "en",
        "state": BookState.read
    }

    response = client.put(
        f'/users/books/{user.id}/{book.id}/', 
        json=book_auteration
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": book.id,
        "namebook": "Updated Sample Book",
        "author": "Updated Author Name",
        "yearbook": 2000,
        "edition": 2,
        "genere": BookGenere.fantasy,
        "ISBN": 7654321,
        "editionPublisher": "Updated Publisher Name",
        "summary": "This is an updated summary.",
        "pageNum": 100,
        "language": "en",
        "state": BookState.read,
        "user_id": user.id
    }

def test_update_select_book(client, user, book):
    response = client.patch(
        f'/users/books/{user.id}/{book.id}/', 
        json={
            "editionPublisher": "Updated Publisher Name"
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": book.id,
        "namebook" : "Sample Book",
        "author" : "Author Name",
        "yearbook" : 1999,
        "edition" : 1,
        "genere" : BookGenere.fantasy,
        "ISBN" : 1234567,
        "editionPublisher": "Updated Publisher Name",
        "summary" : "This is summary",
        "pageNum" :  20,
        "language" : "pt",
        "state" : BookState.start,
        "user_id": user.id
    }

def test_delete_one_book(client, user, book):
    response = client.delete(
        f'/users/books/delete_one/{user.id}/{book.id}/'
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": f"ID {book.id} Book successfully deleted"
    }

def test_delete_all_books(client, user):
    response = client.delete(
        f'/users/books/{user.id}/all/'
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": f"All such user's books {user.username} been successfully deleted"
    }

