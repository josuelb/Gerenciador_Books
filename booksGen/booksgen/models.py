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
    password: Mapped[str] = mapped_column(String(30))
    create_all: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    books: Mapped[list['BooksModel']] = relationship(
        init=False,
        back_populates="user",
        cascade="all, delete-orphan"
    )


@table_registry.mapped_as_dataclass
class BooksModel:
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        init=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    nomebook: Mapped[str] = mapped_column(
        String(100)
    )
    author: Mapped[str] = mapped_column(
        String(100)
    )
    yearbook: Mapped[int] = mapped_column()
    summary: Mapped[str] = mapped_column(
        String(400)
    )
    state: Mapped[BookState]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user: Mapped[UsersModel] = relationship(init=False, back_populates='books')

   