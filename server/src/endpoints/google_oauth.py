import json
import logging
from fastapi import Depends, FastAPI, Request
from urllib.parse import urlencode, parse_qs

from src.core.settings import settings

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from src.core.database import get_db
from src.crud.user import user_crud
from src.endpoints.endpoint_exceptions import OAuthSignInFailed


app = FastAPI(
    title="prompton-api-google-oauth",
    description="PromptOn Google Ouath2 endpoints",
    version="0.0.1",
    docs_url="/",
)


starlette_session_secret = (
    settings.STARLETTE_SESSION_SECRET.get_secret_value()
    if settings.STARLETTE_SESSION_SECRET
    else None
)
app.add_middleware(SessionMiddleware, secret_key=starlette_session_secret)


if settings.GOOGLE_CLIENT_SECRET and settings.GOOGLE_CLIENT_ID:
    starlette_config = Config(
        environ={
            "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID.get_secret_value(),
            "GOOGLE_CLIENT_SECRET": settings.GOOGLE_CLIENT_SECRET.get_secret_value(),
        }
    )

    oauth = OAuth(starlette_config)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

else:
    logging.warning(
        "No Google OAuth2 credentials found. Google OAuth2 will not work. set GOOGLE_CLIENT_SECRET and GOOGLE_CLIENT_ID env variables."
    )


@app.get("/login")
async def login(request: Request):
    if not oauth.google:
        raise Exception(
            "Google OAuth2 is not setup. Check GOOGLE_CLIENT_SECRET and GOOGLE_CLIENT_ID env variables."
        )
    redirect_uri = request.url_for("callback")
    request.session["original_query_params"] = urlencode(
        request.query_params.multi_items(), doseq=True
    )

    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/callback")
async def callback(request: Request, db=Depends(get_db)):
    if not oauth.google:
        raise OAuthSignInFailed(
            "Google OAuth2 is not setup. Check GOOGLE_CLIENT_SECRET and GOOGLE_CLIENT_ID env variables."
        )

    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    if user:
        request.session["user_email"] = user.get("email")
        request.session["user"] = user

        original_query_params = parse_qs(
            request.session.get("original_query_params", "")
        )

        logged_in_redirect_uri = original_query_params.get(
            "logged_in_redirect_uri", ["/oauth/logged_in"]
        )[0]

        del original_query_params["logged_in_redirect_uri"]

        if not user.get("email_verified"):
            raise OAuthSignInFailed("Google Email is not verified.")

        headers = {}

        token = await user_crud.get_token_after_oauth(db, user)

        if token.access_token and user.get("email"):
            headers = {"X-Access-Token": token.access_token, "X-User-Email": user.email}
            request.session["access_token"] = token.access_token
            # TODO: access_token in query param is a workaround until we figure how to read session cookie with streamlit
            original_query_params["access_token"] = [token.access_token]
            query_params_str = urlencode(original_query_params, doseq=True)

            return RedirectResponse(
                f"{logged_in_redirect_uri}?{query_params_str}", headers=headers
            )
    raise OAuthSignInFailed("Failed to fetch user info from Google.")


@app.get("/logout")
async def logout(request):
    request.session.pop("user", None)
    return RedirectResponse(url="/test")


@app.get("/logged_in")
async def logged_in(request: Request):
    """FIXME: this is a debug page, remove it in production"""
    access_token = request.session.get("access_token")
    user_email = request.session.get("user_email")
    user = request.session.get("user")

    user = json.dumps(user, indent=4).replace("\n", "<br/>")
    html = f"""user_email: {user_email} <br/>
        <a href="/google_oauth/logout">logout</a> <br/>
        <a href="/google_oauth/login">login</a><br/><br/>
        token: <pre>{access_token}></pre>
        user: <pre>{user}</pre> """

    return HTMLResponse(html)
