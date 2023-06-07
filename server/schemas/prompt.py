from enum import Enum
from typing import Optional
from pydantic import Extra, Field

from server.schemas.base import AllOptional, MongoBase, MyBaseModel, NameField


# TODO: do we actually need to restrict statuses? is active only special and we could allow any string?
class PromptStatus(str, Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"


class PromptCreate(MyBaseModel, extra=Extra.forbid):
    status: PromptStatus = Field(default=PromptStatus.ACTIVE)
    name: NameField
    description: Optional[str] = Field(None)


class PromptInDB(PromptCreate, MongoBase, extra=Extra.allow):
    pass


class PromptRead(PromptCreate, MongoBase, extra=Extra.ignore):
    pass


class PromptUpdate(PromptCreate, metaclass=AllOptional):
    pass
