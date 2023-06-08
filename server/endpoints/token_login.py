from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from server.core.database import get_db
from server.core.settings import settings
from server.core.auth import authenticate_user, create_access_token
from server.schemas.user import Token
from server.endpoints.ApiResponses import ReqResponses

router = APIRouter()


@router.post(
    "/token",
    responses={
        **ReqResponses.NOT_AUTHENTICATED,
        **ReqResponses.MALFORMED_REQUEST,
    },
    response_model=Token,
    tags=["authentication"],
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # TODO: add user: prefix to sub
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
