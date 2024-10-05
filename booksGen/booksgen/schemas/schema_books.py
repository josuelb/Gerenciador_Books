from pydantic import BaseModel

# Schema para o metodo post
class BookSchema(BaseModel):
    nameBook: str
    author: str
    yearBook: int
    edition: int
    genre: str
    isbn: int
    editionPublisher: str
    sumary: str
    pageNum: int 
    language: str
    state: str

# Schema de retorno
class BookSchemaPublic(BaseModel):
    id: int
    nameBook: str
    author: str
    yearBook: int
    edition: int
    genre: str
    isbn: int
    editionPublisher: str
    sumary: str
    pageNum: int 
    language: str
    state: str

# Schema de listagem 
class BookSchemaList(BaseModel):
    books: list[BookSchemaPublic]