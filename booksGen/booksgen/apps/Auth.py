"""

View responsável pela autenticação 
do usuario.

"""

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from booksgen.security import (
    verify_password,
    create_access_token,
    get_current_user
)
from booksgen.db.conection_bd import ConectionDB
from booksgen.schemas.schema_auth import TokenSchema
from booksgen.models import UsersModel

router_auth = APIRouter(prefix="/auth", tags=["auth"])
SESSION_DB: ConectionDB = ConectionDB()

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
SessionCurrent = Annotated[Session, Depends(SESSION_DB.get_session)]


class Auth:

    @router_auth.post(
        '/token',
        response_model=TokenSchema
    )
    def login_access_token(
        form_token: OAuth2Form,
        session: SessionCurrent
    ):
        db_user: UsersModel = session.scalar(
            select(UsersModel).where(
                (UsersModel.username == form_token.username)
            )
        )

        if not db_user or not verify_password(
            form_token.password, db_user.password
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Incorret Username or password'
            )
        
        access_token = create_access_token(
            data={"sub": db_user.username}
        )

        return {
            'access_token': access_token, 
            'token_type': 'Bearer'
        }
    
    @router_auth.post(
        "/refresh_token",
        response_model=TokenSchema
    )
    def refresh_access_token(
        user: UsersModel = Depends(get_current_user)
    ):
        new_access_token = create_access_token(
            data={"sub": user.username}
        )

        return {
            'access_token': new_access_token,
            'token_type': 'Bearer'
        }