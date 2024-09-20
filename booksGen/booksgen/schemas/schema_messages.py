from pydantic import BaseModel

class MessageDelete(BaseModel):
    message: dict