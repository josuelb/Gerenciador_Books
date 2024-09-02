from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..settings import uri_db

engine = create_engine(url=uri_db)

class ConectionDB:
    @staticmethod
    def get_session():
        with Session(engine) as session:
            yield session
