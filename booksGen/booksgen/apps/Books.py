"""
View responsável pelo gerenciamento de books
do users.
"""

import json
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from booksgen.db.conection_bd import ConectionDB
from booksgen.db.connection_db_redis import ConnectionRedis
from booksgen.schemas.schema_books import (
    BookSchema,
    BookSchemaPublic,
    BookSchemaList, 
    BookSchemaP
)
from booksgen.schemas.schema_messages import MessageDelete
from booksgen.models import (
    BooksModel, 
    UsersModel
)
from booksgen.security import get_current_user

router_books = APIRouter(prefix="/users/books", tags=['Books'])
SessionCurrent = Annotated[Session, Depends(ConectionDB.get_session)]
UserCurrent = Annotated[UsersModel, Depends(get_current_user)]

def SETTING_MEMORY_CACHE(book: BooksModel, Redis):
    try:
        Redis.set(f"books_{book.user_id}:{book.id}", json.dumps(book.dict()), ex=60*3)
    except:
        HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Cache Memory Error"
        )


class Books:

    @router_books.get(
        '/',
        response_model=BookSchemaList,
        status_code=HTTPStatus.OK
    )
    def read_books(
        session: SessionCurrent,
        userCurrent: UserCurrent,
        redis = Depends(ConnectionRedis().get_session_redis)
    ):
        books_cache = redis.get(f"book_{userCurrent.id}")
        if books_cache:
            books_cache = BookSchemaPublic(**books_cache)
            return {"books": books_cache}

        books = session.scalars(
            select(BooksModel).where(
                BooksModel.user_id == userCurrent.id
            )
        )

        if not books:
            return {"books": None}
        
        num_book = 0
        for book in books:
            if num_book>4:
                break
            SETTING_MEMORY_CACHE(book, redis)
            num_book += 1

        return {"books": books}
    
    @router_books.post(
        '/{user_id}/', 
        response_model=BookSchemaPublic,
        status_code=HTTPStatus.CREATED
    )
    def created_book(
        bookCurrent: BookSchema,
        session: SessionCurrent,
        userCurrent: UserCurrent,
        redis = Depends(ConnectionRedis().get_session_redis)
    ):
        db_book = session.scalar(
            select(BooksModel).where(
                (BooksModel.ISBN == bookCurrent.ISBN) &
                (BooksModel.user_id == userCurrent.id)
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
            user_id = userCurrent.id
        )    

        session.add(db_book)
        session.commit()
        session.refresh(db_book)

        SETTING_MEMORY_CACHE(db_book, redis)

        return db_book
    

    @router_books.put(
        '/{book_id}/',
        response_model=BookSchemaPublic,
        status_code=HTTPStatus.OK
    )
    def update_book(
        book_id: int,
        BookCurrent: BookSchema,
        session: SessionCurrent,
        userCurrent: UserCurrent,
        redis = Depends(ConnectionRedis().get_session_redis)
    ):
        db_book = session.scalar(
            select(BooksModel).where(
                (BooksModel.user_id == userCurrent.id) &
                (BooksModel.id == book_id)
            )
        )

        if not db_book:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Book NOT exists"
            )

        for key, value in vars(BookCurrent).items():
            if value is not None:
                setattr(
                    db_book, 
                    key, 
                    value
                )
    
        session.commit()
        session.refresh(db_book)

        SETTING_MEMORY_CACHE(db_book, redis)

        return db_book
    
    @router_books.patch(
        '/{book_id}/',
        status_code=HTTPStatus.OK,
        response_model=BookSchemaPublic
    )
    def update_select_book(
        book_id: int,
        BookCurrent: BookSchemaP,
        session: SessionCurrent,
        userCurrent: UserCurrent,
        redis = Depends(ConnectionRedis().get_session_redis)
    ):
        db_book: BooksModel = session.scalar(
            select(BooksModel).where(
                (BooksModel.user_id == userCurrent.id) &
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
        session.refresh(db_book)

        SETTING_MEMORY_CACHE(db_book, redis)

        return db_book

    @router_books.delete(
        '/delete_one/{book_id}/',
        status_code=HTTPStatus.OK,
        response_model=MessageDelete
    )
    def delete_one_book(
        book_id:int,
        session: SessionCurrent,
        userCurrent: UserCurrent
    ):
        db_book: BooksModel = session.scalar(
            select(BooksModel).where(
                (BooksModel.user_id == userCurrent.id) &
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
        session: SessionCurrent,
        userCurrent: UserCurrent
    ):
        while True:
            db_book: BooksModel = session.scalar(
                select(BooksModel).where(
                    BooksModel.user_id == userCurrent.id
                )
            )

            if not db_book:
                break
            
            session.delete(db_book)
            session.commit()
            session.refresh()

        return MessageDelete(message=f"All such user's books {userCurrent.username} been successfully deleted")
