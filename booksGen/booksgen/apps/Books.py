"""
View responsável pelo gerenciamento de books
do users.
"""

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from booksgen.db.conection_bd import ConectionDB
from booksgen.schemas.schema_books import (
    BookSchema,
    BookSchemaPublic,
    BookSchemaList, 
    BookSchemaP
)
from booksgen.schemas.schema_messages import MessageDelete
from booksgen.models import (
    BooksModel, 
    BookGenere, 
    BookState,
    UsersModel
)

router_books = APIRouter(prefix="/users/books", tags=['Books'])
sessionDB = ConectionDB()
SessionCurrent = Annotated[Session, Depends(sessionDB.get_session)]


class Books:
    @router_books.get(
        '/{user_id}',
        response_model=BookSchemaList,
        status_code=HTTPStatus.OK
    )
    def read_books(
        user_id: int,
        session: SessionCurrent
    ):
        books = session.scalars(
            select(BooksModel).where(
                BooksModel.user_id == user_id
            )
        )

        if not books:
            return {"books": None}

        return {"books": books}
    
    @router_books.post(
        '/{user_id}/', 
        response_model=BookSchemaPublic,
        status_code=HTTPStatus.CREATED
    )
    def created_book(
        user_id: int,
        bookCurrent: BookSchema,
        session: SessionCurrent
    ):
        db_book = session.scalar(
            select(BooksModel).where(
                (BooksModel.ISBN == bookCurrent.ISBN) &
                (BooksModel.user_id == user_id)
            )
        )

        if db_book: 
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Book already exists"
            )

        db_book = BooksModel(
            namebook = bookCurrent.namebook,
            author = bookCurrent.author,
            yearbook = bookCurrent.yearbook,
            edition = bookCurrent.edition,
            genere = bookCurrent.genere,
            ISBN = bookCurrent.ISBN,
            editionPublisher = bookCurrent.editionPublisher,
            summary = bookCurrent.summary,
            pageNum = bookCurrent.pageNum, 
            language = bookCurrent.language,
            state = bookCurrent.state,
            user_id = user_id
        )    

        session.add(db_book)
        session.commit()
        session.refresh(db_book)

        print(db_book)

        return db_book
    

    @router_books.put(
        '/{user_id}/{book_id}/',
        response_model=BookSchemaPublic,
        status_code=HTTPStatus.OK
    )
    def update_all_book(
        user_id: int,
        book_id: int,
        BookCurrent: BookSchema,
        session: SessionCurrent
    ):
        db_book = session.scalar(
            select(BooksModel).where(
                (BooksModel.user_id == user_id) &
                (BooksModel.id == book_id)
            )
        )

        if not db_book:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Book NOT exists"
            )

        for key in vars(db_book).keys():
            if hasattr(BookCurrent, key):
                setattr(
                    db_book, 
                    key, 
                    getattr(BookCurrent, key)
                )
    
        session.commit()

        return db_book

    @router_books.patch(
        '/{user_id}/{book_id}/',
        status_code=HTTPStatus.OK,
        response_model=BookSchemaPublic
    )
    def update_select_book(
        user_id: int,
        book_id: int,
        BookCurrent: BookSchemaP,
        session: SessionCurrent
    ):
        db_book: BooksModel = session.scalar(
            select(BooksModel).where(
                (BooksModel.user_id == user_id) &
                (BooksModel.id == book_id)
            )
        )

        if not db_book:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Book NOT exists"
            )

        for key,value in vars(BookCurrent).items():
            if value is not None:
                setattr(
                    db_book,
                    key,
                    value
                )
            
        session.commit()

        return db_book

    @router_books.delete(
        '/delete_one/{user_id}/{book_id}/',
        status_code=HTTPStatus.OK,
        response_model=MessageDelete
    )
    def delete_one_book(
        user_id: int,
        book_id: int,
        session: SessionCurrent
    ):
        db_book: BooksModel = session.scalar(
            select(BooksModel).where(
                (BooksModel.user_id == user_id) &
                (BooksModel.id == book_id)
            )
        )

        if not db_book:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Book NOT exists"
            )
        
        session.delete(db_book)
        session.commit()

        return MessageDelete(message=f"ID {book_id} Book successfully deleted")
        
    @router_books.delete(
        '/{user_id}/all/',
        status_code=HTTPStatus.OK,
        response_model=MessageDelete
    )
    def delete_All_book(
        user_id: int,
        session: SessionCurrent
    ):
        while True:
            db_book: BooksModel = session.scalar(
                select(BooksModel).where(
                    BooksModel.user_id == user_id
                )
            )

            if not db_book:
                break
            
            session.delete(db_book)
            session.commit()

        user: UsersModel = session.scalar(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        )

        return MessageDelete(message=f"All such user's books {user.username} been successfully deleted")
