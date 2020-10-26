from datetime import timedelta
from app import configuration
from app.token import create_access_token
from fastapi import APIRouter
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request

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
    print (redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    print (user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.get("email")}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
