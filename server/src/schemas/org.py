from typing import Dict
from pydantic import Extra, Field, SecretStr
from src.schemas.base import (
    AllOptional,
    MongoBaseCreate,
    MongoBaseRead,
    MyBaseModel,
    NonEmptyStrField,
)


class OrgBase(MyBaseModel):
    name: NonEmptyStrField
    access_keys: Dict[str, str] | None = None
    oauth_domain: str | None = Field(
        None,
        description="APEX domain for oauth single sign on. Anyone with an email address ending in this domain will be able to register to the org after google account sign in. Only Google OAuth is supported for now.",
    )


class OrgCreate(OrgBase, extra=Extra.forbid):
    pass


class OrgInDB(OrgBase, MongoBaseCreate, extra=Extra.allow):
    pass


class OrgRead(MongoBaseRead, extra=Extra.ignore):
    name: str
    access_keys: Dict[str, SecretStr] | None = None


class OrgUpdate(OrgBase, metaclass=AllOptional, extra=Extra.forbid):
    pass
