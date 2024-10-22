from pydantic import BaseModel

class MessageDelete(BaseModel):
    message: str

class MessageJSON(BaseModel):
    allow: str