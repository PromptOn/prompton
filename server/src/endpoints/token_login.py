from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm


from src.schemas.user import Token, LoginCredentialsPost
from src.endpoints.ApiResponses import ReqResponses

from src.core.database import get_db
from src.crud.user import user_crud

router = APIRouter()


@router.post(
    "/token",
    responses={
        **ReqResponses.INVALID_USERNAME_OR_PASSWORD,
        **ReqResponses.MALFORMED_REQUEST,
    },
    tags=["authentication"],
)
async def get_access_token_extended(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)
) -> Token:
    token = await user_crud.get_token(db, form_data.username, form_data.password)

    return token


@router.post(
    "/token_basic",
    responses={
        **ReqResponses.INVALID_USERNAME_OR_PASSWORD,
        **ReqResponses.MALFORMED_REQUEST,
    },
    tags=["authentication"],
)
async def get_access_token(
    # data: Dict[str, Union[str, SecretStr]],
    credentials: LoginCredentialsPost,
    db=Depends(get_db),
) -> Token:
    """Same functionality as /token but taking `username` and `password` args as `application/json` type instead of `application/x-www-form-urlencoded`

    Don't use it becuase it's a **temporary** workaround for client lib generator and will be removed in the future.
    """
    # TODO: check if newer fern version than 0.10.13 supports application/x-www-form-urlencoded so we can remove  /token_basic

    token = await user_crud.get_token(
        db, credentials.username, credentials.password.get_secret_value()
    )
    return token
