from pydantic import BaseModel, ConfigDict

from booksgen.models import BookGenere, BookState
from booksgen.models import UsersModel

# Schema para o metodo post
class BookSchema(BaseModel):
    namebook: str
    author: str
    yearbook: int
    edition: int
    genere: BookGenere
    ISBN: int
    editionPublisher: str
    summary: str
    pageNum: int 
    language: str
    state: BookState

    model_config = ConfigDict(from_attributes=True)

# Schema para o metodo put
class BookSchemaP(BaseModel):
    namebook: str | None = None
    author: str | None = None
    yearbook: int | None = None
    edition: int | None = None
    genere: BookGenere = None
    ISBN: int | None = None
    editionPublisher: str | None = None
    summary: str | None = None
    pageNum: int | None = None 
    language: str | None = None
    state: BookState = None


# Schema de retorno
class BookSchemaPublic(BaseModel):
    id: int
    namebook: str
    author: str
    yearbook: int
    edition: int
    genere: BookGenere
    ISBN: int
    editionPublisher: str
    summary: str
    pageNum: int 
    language: str
    state: BookState
    user_id: int

    model_config = ConfigDict(from_attributes=True)

# Schema de listagem 
class BookSchemaList(BaseModel):
    books: list[BookSchemaPublic]