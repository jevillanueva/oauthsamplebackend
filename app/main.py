from app.token import Token, User, authenticate_user, create_access_token, get_current_active_user, get_revoke_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from passlib.utils import test_crypt
from app import configuration
from .routers import users, oauth_google

from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Depends, HTTPException, status

from datetime import  timedelta

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=configuration.SECRET_KEY_MIDDLEWARE)
app.include_router(oauth_google.router, prefix="/google", tags=["google"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=configuration.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def readUsersMe(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/revoke")
async def read_own_items(id: str = Depends(get_revoke_token)):
    return {"id": id}