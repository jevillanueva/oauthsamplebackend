import uvicorn

from app import configuration
from .routers import users, oauth_google, oauth_basic

from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI

TITLE= "Oauth Base"
DESCRIPTION = "API base to login Bearer using Oauth2 Google"
app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=configuration.VERSION,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)
@app.get("/api/", tags=["Index"])
def read_root():
    return {"title": TITLE, "description": DESCRIPTION, "version": configuration.VERSION}


app.add_middleware(SessionMiddleware, secret_key=configuration.SECRET_KEY_MIDDLEWARE)
app.include_router(oauth_basic.router, prefix="/api", tags=["Security Basic"])
app.include_router(oauth_google.router, prefix="/api/google", tags=["Security Google"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])




