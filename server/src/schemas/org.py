from typing import Dict
from pydantic import Extra, SecretStr
from src.schemas.base import (
    AllOptional,
    MongoBase,
    MyBaseModel,
    NonEmptyStrField,
)


class OrgBase(MyBaseModel):
    name: NonEmptyStrField
    access_keys: Dict[str, str] | None = None


class OrgCreate(OrgBase, extra=Extra.forbid):
    pass


class OrgInDB(OrgBase, MongoBase, extra=Extra.allow):
    pass


class OrgRead(MongoBase, extra=Extra.ignore):
    name: str
    access_keys: Dict[str, SecretStr] | None = None


class OrgUpdate(OrgBase, metaclass=AllOptional, extra=Extra.forbid):
    pass
