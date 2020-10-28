from datetime import timedelta
from http.client import HTTPException

from fastapi.encoders import jsonable_encoder
from app import configuration
from app.token import create_access_token
from fastapi import APIRouter, status
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()
oauth = OAuth()
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
ACCESS_TOKEN_EXPIRE_MINUTES = configuration.ACCESS_TOKEN_EXPIRE_MINUTES
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
    client_id=configuration.GOOGLE_CLIENT_ID,
    client_secret=configuration.GOOGLE_CLIENT_SECRET,
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth(request: Request):
    print("#" * 30)
    print(request)
    print("#" * 30)
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    oauth.google.parse
    print(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.get("email")}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/client")
async def auth(request: Request):
    try:
        body_bytes = await request.body()
        auth_code = jsonable_encoder(body_bytes)
        print("!"*30)
        print (auth_code)
        print("!"*30)
        idInfo = id_token.verify_oauth2_token(
            auth_code, requests.Request(), configuration.GOOGLE_CLIENT_ID
        )
        print("#"*30)
        print(idInfo)
        print("#"*30)
        if idInfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"username": idInfo.get("email")}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    except: 
        return HTTPException(
            status.HTTP_400_BAD_REQUEST, "Unable to validate Google Login"
        )
