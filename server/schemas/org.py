from typing import Dict, List
from pydantic import Extra
from server.schemas.base import (
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


class OrgRead(OrgBase, MongoBase, extra=Extra.ignore):
    pass


class OrgUpdate(OrgBase, metaclass=AllOptional, extra=Extra.forbid):
    pass
