"""

Aqui será criado os modelos que seram
usados no DB, seja qual for.

"""

from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()

class BookState(str, Enum):
    added = "Added"
    start = "Start or Reading"
    read = "Read"
    not_read = "Not Read"

class BookGenere(str, Enum):
    romance = "Romance"
    fantasy = "Fantasy"
    mystery = "Mystery"
    horror = "Horror"
    thriller = "Thriller"
    sci_fi = "Science Fiction"
    crime = "Crime"
    classics = "Classics"
    adventure = "Adventure"
    manga = "Mangas"


@table_registry.mapped_as_dataclass
class UsersModel:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        init=False, 
        unique=True, 
        primary_key=True, 
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    create_all: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    books: Mapped[list['BooksModel']] = relationship(
        init=False,
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "created_all": self.create_all.isoformat() if self.create_all else None,
            "books": [book.to_dict() for book in self.books] if self.books else []
        }
        


@table_registry.mapped_as_dataclass
class BooksModel:
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        init=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    namebook: Mapped[str] = mapped_column(
        String(100)
    )
    author: Mapped[str] = mapped_column(
        String(100)
    )
    yearbook: Mapped[int] = mapped_column()
    edition: Mapped[int] = mapped_column()
    genere: Mapped[BookGenere] = mapped_column()
    ISBN: Mapped[int] = mapped_column()
    editionPublisher: Mapped[
        str
    ] = mapped_column(String(500))
    
    summary: Mapped[str] = mapped_column(
        String(400)
    )
    pageNum: Mapped[int] = mapped_column()
    language: Mapped[str] = mapped_column(
        String(5)
    )

    state: Mapped[BookState] = mapped_column()

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user: Mapped[UsersModel] = relationship(init=False, back_populates='books')
   
    def to_dict(self):
        return {
            "id": self.id,
            "namebook": self.namebook,
            "author": self.author,
            "yearbook": self.yearbook,
            "edition": self.edition,
            "genere": self.genere,
            "ISBN": self.ISBN,
            "editionPublisher": self.editionPublisher,
            "summary": self.summary,
            "pageNum": self.pageNum,
            "language": self.language,
            "state": self.state,
            "user_id": self.user_id
        }