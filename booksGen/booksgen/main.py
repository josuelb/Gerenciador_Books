from fastapi import FastAPI

from booksgen.apps.users import router_users

app = FastAPI()
app.include_router(router=router_users)