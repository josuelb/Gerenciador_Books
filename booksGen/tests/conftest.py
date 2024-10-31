import pytest 

from http import HTTPStatus
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from booksgen.main import app
from booksgen.models import (
    UsersModel,
    BooksModel,
    BookState, 
    BookGenere,
    table_registry
)
from booksgen.db.conection_bd import ConectionDB
from booksgen.settings import Settings
from booksgen.security import (
    get_password_hash, 
    create_access_token
)

@pytest.fixture
def client(session):
    def get_session_override():
        return session
    
    app.dependency_overrides[ConectionDB.get_session] = get_session_override
    with TestClient(app) as client:
        yield client 

    app.dependency_overrides.clear()

@pytest.fixture
def session():
    engine = create_engine(url=Settings().DATABASE_TESTS_URI)

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)

@pytest.fixture
def user(session):
    pwd = "testtest"
    user: UsersModel = UsersModel("testStore", "test", password=get_password_hash(pwd))
    
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd

    return user

@pytest.fixture
def book(session, user):
    book: BooksModel = BooksModel(
        namebook="Sample Book",
        author="Author Name",
        yearbook=1999,
        edition=1,
        genere=BookGenere.fantasy,
        ISBN=1234567,
        editionPublisher="Publisher Name",
        summary="This is summary",
        pageNum=20,
        language="pt",
        state=BookState.start,
        user_id=user.id
    )

    session.add(book)
    session.commit()
    session.refresh(book)

    return book

@pytest.fixture
def token(client, user):
    response = client.post(
        "/auth/token",
        data={
            "username": user.username, 
            "password": user.clean_password
        }
    )


    assert response.status_code == HTTPStatus.OK
    jwt = response.json()

    assert 'access_token' in jwt

    return jwt['access_token']
