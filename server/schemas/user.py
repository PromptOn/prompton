from enum import Enum
from pydantic import EmailStr, Extra, Field

from server.schemas.base import (
    AllOptional,
    MongoBase,
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


class UserInDB(User, MongoBase, extra=Extra.allow):
    email: str
    hashed_password: str


class UserRead(User, MongoBase, extra=Extra.ignore):
    # we ignore extra fields to prevent hashed_password to be returned
    email: str
    pass


class UserUpdate(UserCreate, metaclass=AllOptional):
    pass
