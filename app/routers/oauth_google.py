import json
from fastapi import APIRouter
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
import app.configuration as conf

router = APIRouter()
oauth = OAuth()
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
    client_id=conf.GOOGLE_CLIENT_ID,
    client_secret=conf.GOOGLE_CLIENT_SECRET,
)



@router.route('/')
async def homepage(request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/google/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/google/login">login</a>')

@router.route("/login")
async def login(request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route("/auth")
async def auth(request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    print (user)
    request.session["user"] = dict(user)
    return RedirectResponse(url="/")

@router.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')