import pytest 

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from booksgen.main import app
from booksgen.models import UsersModel, table_registry
from booksgen.db.conection_bd import ConectionDB

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
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.drop_all(engine)

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