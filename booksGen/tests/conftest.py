import pytest 

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

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

@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[ConectionDB().get_session] = get_session_override
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
    user: UsersModel = UsersModel("testStore", "test", "testtest")

    session.add(user)
    session.commit()
    session.refresh(user)

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