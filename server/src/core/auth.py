from datetime import timedelta, datetime

from typing import Annotated
from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import ExpiredSignatureError, JWTError, jwt
from src.core.database import get_db

from src.core.settings import settings
from src.crud.user import user_crud
from src.endpoints.endpoint_exceptions import CredentialExpiredError
from src.schemas.user import TokenData, UserInDB


class CredentialsException(Exception):
    # this is not exposed to the user, it's captured by caller and appropriate HTTP exception raised
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name="JWT")


def get_hashed_password(password: str) -> str:
    # salt is generated by bcrypt: https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str, db):
    user = await user_crud.find_one(db, {"email": email})

    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta_minutes: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta_minutes:
        expire = datetime.utcnow() + expires_delta_minutes
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db=Depends(get_db)
) -> UserInDB:
    """returns user associated with token. raises if token is invalid or expired"""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        email: str | None = payload.get("sub")

        if email is None:
            raise CredentialsException("email is None")

        token_data = TokenData(email=email)

    except ExpiredSignatureError:
        raise CredentialExpiredError()

    except JWTError as jwt_error:
        print("\n!!!!! \n token ", str(jwt_error), "\n!!!!! \n")
        raise CredentialsException(jwt_error)

    user = await user_crud.find_one(db, filter={"email": token_data.email})

    if user is None:
        raise CredentialsException("user is None")

    return user