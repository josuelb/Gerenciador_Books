"""
View do Users, na qual tem a responsabilidade de 
fazer os retornos dos metodos http da url.
"""

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from booksgen.db.conection_bd import ConectionDB
from booksgen.models import UsersModel
from booksgen.schemas.schema_users import (
    UserSchema, 
    UserSchemaPublic, 
    UserSchemaPublicAlterations,
    UserSchemaList
)
from booksgen.schemas.schema_messages import MessageDelete

router_users = APIRouter(prefix='/users', tags=["users"])
sessionDB = ConectionDB()
SessionCurrent = Annotated[Session, Depends(sessionDB.get_session)]


class Users:

    @router_users.get(
        '/',
        response_model=UserSchemaList,
        status_code=HTTPStatus.OK
    )
    def read_users(
        session: SessionCurrent
    ):
        users = session.scalars(
            select(UsersModel)
        ).all()
        
        if not users:
            return {'Users': None}

        return {'Users': users}
    
    @router_users.post(
        '/',
        status_code=HTTPStatus.CREATED,
        response_model=UserSchemaPublic
    )
    def created_user(
        session: SessionCurrent, user: UserSchema
    ):
        db_user = session.scalar(
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

    @router_users.delete(
        '/{user_id}',
        status_code=HTTPStatus.OK,
        response_model=MessageDelete
    )
    def deleted_user(
        user_id: int,
        session: SessionCurrent
    ):
        db_user=session.scalar(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        )

        if not db_user:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Not enough permissions'
            )

        session.delete(db_user)
        session.commit()

        return {'message': 'User deleted'}

