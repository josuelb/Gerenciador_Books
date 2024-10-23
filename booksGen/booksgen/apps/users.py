"""
View do Users, na qual tem a responsabilidade de 
fazer os retornos dos metodos http da url.
"""

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from booksgen.db.conection_bd import ConectionDB
from booksgen.models import UsersModel
from booksgen.schemas.schema_users import (
    UserSchema, 
    UserSchemaPublic, 
    UserSchemaPublicAlterations,
    UserSchemaList, 
    UserSchemaP
)
from booksgen.schemas.schema_messages import (
    MessageDelete,
    MessageJSON
)

router_users = APIRouter(prefix='/users', tags=["users"])
sessionDB = ConectionDB()
SessionCurrent = Annotated[Session, Depends(sessionDB.get_session)]


class Users:

    @router_users.get(
        '/{user_id}',
        response_model=UserSchemaList,
        status_code=HTTPStatus.OK
    )
    def read_users(
        user_id: int,
        session: SessionCurrent
    ):
        db_users: UsersModel = session.scalars(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        )
        
        if not db_users:
            raise HTTPException(
                status_code=HTTPStatus.NO_CONTENT,
                detail="User invalid or not exist"
            )

        return UserSchemaList(users=db_users)
    
    @router_users.post(
        '/',
        status_code=HTTPStatus.CREATED,
        response_model=UserSchemaPublic
    )
    def created_user(
        session: SessionCurrent, user: UserSchema
    ):
        db_user: UsersModel = session.scalar(
            select(UsersModel).where(
                UsersModel.username==user.username
            )
        )

        if db_user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username already exists"
            )
        
        db_user = UsersModel(
            username = user.username, 
            name = user.name,
            password = user.password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user
    
    @router_users.put(
       "/{user_id}",
       status_code=HTTPStatus.OK,
       response_model=UserSchemaPublicAlterations
    )
    def updated_user(
        user_id:int,
        user: UserSchema,
        session: SessionCurrent
    ):
        db_user = session.scalar(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        )

        if not db_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='User not found'
            )
        
        db_user.username = user.username
        db_user.name = user.name
        db_user.password = user.password

        session.commit()
        session.refresh(db_user)

        return db_user

    @router_users.patch(
        '/{user_id}',
        status_code=HTTPStatus.OK,
        response_model=UserSchemaPublic
    )
    def updated_user_one(
        user_id: int,
        user_update: UserSchemaP,
        session: SessionCurrent
    ):
        db_user = session.scalar(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        )

        if not db_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not exist"
            )
        
        for key, value in vars(user_update).items():
            if value != None:
                setattr(
                    db_user, 
                    key, 
                    value
                )
        
        session.commit()

        return db_user

    @router_users.delete(
        '/{user_id}',
        status_code=HTTPStatus.OK,
        response_model=MessageDelete
    )
    def deleted_user(
        user_id: int,
        session: SessionCurrent
    ):
        db_user= session.scalar(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        )

        if db_user is None:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Not enough permissions'
            )

        session.delete(db_user)
        session.commit()

        return MessageDelete(message='User deleted')

    @router_users.head(
        "/head/{user_id}",
        status_code=HTTPStatus.OK
    )
    def head_user(
        user_id: int,
        session: SessionCurrent
    ):
        db_user: UsersModel = session.scalar(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        )

        if not db_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, 
                detail="User data not location"
            )
        
        return Response(status_code=HTTPStatus.OK)

    @router_users.options(
        "/options/{user_id}",
        status_code=HTTPStatus.OK,
        response_model=MessageJSON
    )
    def options_users(
        user_id: int,
        session: SessionCurrent
    ):
        return MessageJSON(allow="GET, POST, PUT, DELETE, OPTIONS")
