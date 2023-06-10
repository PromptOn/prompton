from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Body, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.endpoints.endpoint_exceptions import InvalidUserNameOrPassword

from src.core.database import get_db
from src.core.settings import settings
from src.core.auth import authenticate_user, create_access_token
from src.schemas.user import Token
from src.endpoints.ApiResponses import ReqResponses

router = APIRouter()


@router.post(
    "/token",
    responses={
        **ReqResponses.INVALID_USERNAME_OR_PASSWORD,
        **ReqResponses.MALFORMED_REQUEST,
    },
    response_model=Token,
    tags=["authentication"],
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db=Depends(get_db),
):
    user = await authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise InvalidUserNameOrPassword

    # TODO: add user: prefix to sub
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
