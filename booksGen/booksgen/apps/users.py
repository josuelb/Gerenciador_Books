"""
View do Users, na qual tem a responsabilidade de 
fazer os retornos dos metodos http da url.
"""

import json
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from booksgen.db.conection_bd import ConectionDB
from booksgen.db.connection_db_redis import ConnectionRedis
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
from booksgen.security import (
    get_current_user,
    get_password_hash
)
from booksgen.db.connection_db_redis import ConnectionRedis


router_users = APIRouter(prefix='/users', tags=["users"])
SessionCurrent = Annotated[Session, Depends(ConectionDB.get_session)]

def SETTING_MEMORY_CACHE(user, Redis):
    try:
        Redis.set(f"user:{user.username}", json.dumps(user.dict()), ex=60*5)
    except:
        HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Cache Memory Error"
        )


class Users:

    @router_users.get(
        '/',
        response_model=UserSchemaList,
        status_code=HTTPStatus.OK
    )
    def read_users(
        UserCurrent: UsersModel = Depends(get_current_user)
    ):
        if not UserCurrent:
            raise HTTPException(
                status_code=HTTPStatus.BAD_CONTENT,
                detail="Not enough permission"
            )

        return {"users": UserCurrent}
    
    @router_users.post(
        '/',
        status_code=HTTPStatus.CREATED,
        response_model=UserSchemaPublic
    )
    def created_user(
        session: SessionCurrent, 
        user: UserSchema, 
        redis = Depends(ConnectionRedis().get_session_redis)
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
            password = get_password_hash(user.password)
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        SETTING_MEMORY_CACHE(db_user, redis)        

        return db_user
    
    @router_users.put(
       "/{user_id}",
       status_code=HTTPStatus.OK,
       response_model=UserSchemaPublicAlterations
    )
    def updated_user(
        user_id:int,
        user: UserSchemaP,
        session: SessionCurrent,
        redis = Depends(ConnectionRedis().get_session_redis)
    ):
        user_db = session.scalar(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        ) 

        if user_db.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_CONTENT,
                detail="Not enough permission"
            )
        
        user_db.username = user.username
        user_db.name = user.name
        user_db.password = user.password

        session.commit()
        session.refresh(user_db)

        SETTING_MEMORY_CACHE(user_db, redis)

        return user_db

    @router_users.patch(
        '/{user_id}',
        status_code=HTTPStatus.OK,
        response_model=UserSchemaPublic
    )
    def updated_user_one(
        user_id: int,
        user_update: UserSchemaP,
        session: SessionCurrent,
        redis = Depends(ConnectionRedis().get_session_redis)
    ):
        user_db = session.scalar(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        )  

        if user_db.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_CONTENT,
                detail="Not enough permission"
            )

        for key, value in vars(user_update).items():
            if value != None:
                setattr(
                    user_db, 
                    key, 
                    value
                )
        
        session.commit()
        session.refresh(user_db)

        SETTING_MEMORY_CACHE(user_db, redis)

        return user_db

    @router_users.delete(
        '/{user_id}',
        status_code=HTTPStatus.OK,
        response_model=MessageDelete
    )
    def deleted_user(
        user_id: int,
        session: SessionCurrent,
    ):
        user_db = session.scalar(
            select(UsersModel).where(
                UsersModel.id == user_id
            )
        )  

        if user_db.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_CONTENT,
                detail="Not enough permission"
            )
        
        session.delete(user_db)
        session.commit()

        return MessageDelete(message='User deleted')

    @router_users.head(
        "/head/{user_id}",
        status_code=HTTPStatus.OK
    )
    def head_user(
        user_id: int,
        session: SessionCurrent, 
        UserCurrent: UsersModel = Depends(get_current_user)  
    ):

        if not UserCurrent:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, 
                detail="User data not location"
            )
        
        return Response(status_code=HTTPStatus.OK)

    @router_users.options(
        "/options",
        status_code=HTTPStatus.OK,
        response_model=MessageJSON
    )
    def options_users(
        session: SessionCurrent
    ):
        return MessageJSON(allow="GET, POST, PUT, DELETE, OPTIONS")
