from enum import Enum
from pydantic import EmailStr, Extra, SecretStr

from src.schemas.base import (
    AllOptional,
    MongoBaseCreate,
    MongoBaseRead,
    MyBaseModel,
    NonEmptyStrField,
    PyObjectId,
)


class Token(MyBaseModel):
    access_token: str
    token_type: str


class TokenData(MyBaseModel):
    email: str


class UserRoles(str, Enum):
    BASIC = "Basic"
    ORG_ADMIN = "OrgAdmin"
    SUPER_ADMIN = "SuperAdmin"


class User(MyBaseModel):
    full_name: NonEmptyStrField | None = None
    disabled: bool = False
    role: UserRoles = UserRoles.BASIC
    org_id: PyObjectId


class UserCreate(User, extra=Extra.forbid):
    email: EmailStr
    plain_password: NonEmptyStrField
    pass


class UserInDB(User, MongoBaseCreate, extra=Extra.allow):
    email: str
    hashed_password: str


class UserRead(User, MongoBaseRead, extra=Extra.ignore):
    # we ignore extra fields to prevent hashed_password to be returned
    # override all fields with default values as mandatory so clients don't need to check None values
    email: str
    disabled: bool
    pass


class UserUpdate(UserCreate, metaclass=AllOptional):
    pass


class LoginCredentialsPost(MyBaseModel):
    username: EmailStr
    password: SecretStr


class OauthUserInfo(MyBaseModel, extra=Extra.allow):
    email: EmailStr
    name: str
