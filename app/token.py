from app.database import is_revoked, set_revoke_token
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

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]= None
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(database.db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode.update({"id": str(uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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
        username: str = payload.get("username")
        id: str = payload.get("id")
        if username is None or id is None:
            raise credentials_exception
        # Verify if token not is revoked
        if is_revoked(id):
            raise credentials_exception
        token_data = TokenData(username=username, id=id)
    except JWTError:
        raise credentials_exception
    user = get_user(database.db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_revoke_token(token: str= Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        id: str = payload.get("id")
        if is_revoked(id):
            raise credentials_exception
        if username is None or id is None:
            raise credentials_exception
        token_data = TokenData(username=username, id=id)
    except JWTError:
        raise credentials_exception
    set_revoke_token(id)
    return id




async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
