from app.models.result import Result
from app.models.token import Token, TokenDataInDB
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.token import authenticate_user, create_access_token,  get_revoke_token
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
        data={"username": user.username}, expires_delta=accessTokenExpires, expires_date=dateExpires
    )
    return Token(
        access_token=accessToken,
        token_type="bearer",
        expires=accessTokenExpires,
        date_expires=dateExpires
    )

@router.post("/logout", response_model=Result)
async def revoke_token(token: TokenDataInDB = Depends(get_revoke_token)):
    if token.revoked == True:
        return Result(code=1,message="Token Revocado")
    else:
        return Result(code=0,message="No se pudo Revocar")