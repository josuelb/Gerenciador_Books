from fastapi import FastAPI

from booksgen.apps.users import router_users
from booksgen.apps.Books import router_books
from booksgen.apps.Auth import router_auth

app = FastAPI()
app.include_router(router=router_users)
app.include_router(router=router_books)
app.include_router(router=router_auth)