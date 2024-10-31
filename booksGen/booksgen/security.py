"""

Security.py sera responsável pelo
todo processo de segurânça como:

Criação de tokens;
Validação de token user;
Criação de hashs de senhas;
etc

"""

import json
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated


from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from booksgen.settings import Settings
from booksgen.db.conection_bd import ConectionDB
from booksgen.db.connection_db_redis import ConnectionRedis
from booksgen.models import UsersModel
from booksgen.schemas.schema_users import UserSchemaPublic
from booksgen.schemas.schema_auth import TokenData

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_password_hash(password: str):
    return pwd_context.hash(password=password)

# Verifica se o hash origina da senha
def verify_password(
    plain_password:str,
    hashed_password:str
):
    pwd_response = pwd_context.verify(password=plain_password, hash=hashed_password)
    return pwd_response


# Criação de token
def create_access_token(data: dict):
    to_encode = data.copy()

    # Adiciona o tempo de expliração
    expire = datetime.now(
        tz=ZoneInfo(Settings().ZONE_INFO_HOUR)
    ) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp':expire})

    # Criando o JWT de fato
    encode_jwt = encode(to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)

    return encode_jwt

def get_current_user(
    session: Session = Depends(ConectionDB.get_session),
    token: str = Depends(oauth2_scheme),
    redis = Depends(ConnectionRedis().get_session_redis)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(
            token, 
            key=Settings().SECRET_KEY, 
            algorithms=[Settings().ALGORITHM]
        )
        
        usernameToken = payload.get('sub')

        if not usernameToken:
            raise credentials_exception
        
    except PyJWTError:
        raise credentials_exception
    
    user_cache = redis.get(f"user: {usernameToken}")

    if user_cache:
        user = json.loads(user_cache)
        user = UserSchemaPublic(**user)
        return user

    user_db: UsersModel = session.scalar(
        select(UsersModel).where(UsersModel.username == usernameToken)
    )

    if not user_db:
        raise credentials_exception
    
    user_dict = user_db.to_dict()
    redis.set(f"user: {usernameToken}", json.dumps(user_dict), ex=60*5)
    
    return user_db

