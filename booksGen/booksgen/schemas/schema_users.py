from datetime import datetime

from pydantic import BaseModel, ConfigDict, PrivateAttr

# Schema de criação
class UserSchema(BaseModel):
    username: str 
    name: str
    password: str
    model_config = ConfigDict(from_attributes=True)

# Schema de atualização PATCH
class UserSchemaP(BaseModel):
    id: int | None = None
    username: str | None
    name: str | None = None
    password: str | None
    model_config = ConfigDict(from_attributes=True)

# Schema do que será retornado
class UserSchemaPublic(BaseModel):
    id: int
    username: str
    name: str
    __password: str = PrivateAttr()
    create_all: datetime | None = None
    books: list
    model_config = ConfigDict(from_attributes=True)


class UserSchemaPublicAlterations(BaseModel):
    id: int
    username: str
    name: str


# Schema de listagem
class UserSchemaList(BaseModel):
    users: list[UserSchemaPublic] | UserSchemaPublic
