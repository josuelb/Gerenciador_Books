from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..settings import Settings

uri_db = Settings().DATABASE_URI
engine = create_engine(url=uri_db)

class ConectionDB:
    @staticmethod
    def get_session():
        with Session(engine) as session:
            yield session
