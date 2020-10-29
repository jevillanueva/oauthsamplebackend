from app.services.user_service import get_user
from app.services.token_service import insert_token, revoke_token, token_revoke
from app.models.token import TokenData, TokenDataInDB
from app.models.user import User, UserInDB
from fastapi.exceptions import HTTPException
from fastapi import status
from app import configuration
from pydantic import BaseModel
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime,  timedelta
from fastapi import Depends
from app import database
from uuid import uuid4
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = configuration.SECRET_KEY
ALGORITHM = configuration.ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = get_user(UserInDB(username=username))
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta, expires_date: datetime):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    jti = str(uuid4())
    to_encode.update({"exp": expire})
    to_encode.update({"jti": jti})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    token = TokenDataInDB(
        jti = jti,
        expire_at = expires_date,
    )
    ret = insert_token(token)
    return encoded_jwt

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print (payload)
        token_data = TokenDataInDB(**payload)
        if token_data.username is None:
            raise credentials_exception
        # Verify if token not is revoked
        if token_revoke(token_data):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(UserInDB(username=token_data.username))
    if user is None:
        raise credentials_exception
    return user

async def get_revoke_token(token: str= Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenDataInDB(**payload)
        if token_data.username is None:
            raise credentials_exception
        if token_revoke(token_data):
            raise credentials_exception
        ret = revoke_token(token_data)
        return ret
    except JWTError:
        raise credentials_exception



async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
