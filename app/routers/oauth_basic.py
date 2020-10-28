from app.models.token import Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.token import authenticate_user, create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from app import configuration
router = APIRouter()

@router.post("/auth", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    accessTokenExpires = timedelta(minutes=configuration.ACCESS_TOKEN_EXPIRE_MINUTES)
    dateExpires = datetime.utcnow() + accessTokenExpires
    accessToken = create_access_token(
        data={"username": user.username}, expires_delta=accessTokenExpires
    )
    return Token(
        access_token=accessToken,
        token_type="bearer",
        expires=accessTokenExpires,
        date_expires=dateExpires
    )