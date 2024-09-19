from pydantic import BaseModel, ConfigDict

# Schema de criação
class UserSchema(BaseModel):
    username: str 
    name: str
    password: str

# Schema do que será retornado
class UserSchemaPublic(BaseModel):
    id: int
    username: str
    name: str
    password: str
    model_config = ConfigDict(from_attributes=True)

# Schema de listagem
class UserSchemaList(BaseModel):
    users: list[UserSchemaPublic]
