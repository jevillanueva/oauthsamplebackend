from app.models.token import Token
from datetime import datetime, timedelta
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
    redirect_uri = request.url_for("auth_server_side")
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth_server_side(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dateExpires = datetime.utcnow() + accessTokenExpires
    accessToken = create_access_token(
        data={"username": user.get("email")}, expires_delta=accessTokenExpires
    )
    return Token(
            access_token=accessToken,
            token_type="bearer",
            expires=accessTokenExpires,
            date_expires=dateExpires,
        )


@router.post("/auth/client")
async def auth_client_side(request: Request):
    try:
        body_bytes = await request.body()
        auth_code = jsonable_encoder(body_bytes)
        idInfo = id_token.verify_oauth2_token(
            auth_code, requests.Request(), configuration.GOOGLE_CLIENT_ID
        )
        if idInfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Wrong issuer.")

        accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        dateExpires = datetime.utcnow() + accessTokenExpires
        accessToken = create_access_token(
            data={"username": idInfo.get("email")}, expires_delta=accessTokenExpires
        )
        return Token(
            access_token=accessToken,
            token_type="bearer",
            expires=accessTokenExpires,
            date_expires=dateExpires,
        )
    except:
        return HTTPException(
            status.HTTP_400_BAD_REQUEST, "Unable to validate Google Login"
        )
