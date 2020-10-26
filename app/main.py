from typing import Optional
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from .routers import users, oauth_google
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

app.include_router(oauth_google.router,prefix="/google",   tags=["google"])

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}