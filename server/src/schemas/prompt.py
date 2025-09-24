from enum import Enum
from typing import Optional
from pydantic import Extra, Field

from src.schemas.base import (
    AllOptional,
    MongoBaseCreate,
    MongoBaseRead,
    MyBaseModel,
    NameField,
)


class PromptStatus(str, Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"


class PromptCreate(MyBaseModel, extra=Extra.forbid):
    status: PromptStatus = Field(
        default=PromptStatus.ACTIVE,
        description="Prompt status for client consideration only, currently not used in server logic.",
    )
    name: NameField
    description: Optional[str] = Field(None)


class PromptInDB(PromptCreate, MongoBaseCreate, extra=Extra.allow):
    pass


class PromptRead(PromptCreate, MongoBaseRead, extra=Extra.ignore):
    # override status to be mandatory so clients don't need to check None values
    status: PromptStatus


class PromptUpdate(PromptCreate, metaclass=AllOptional):
    pass
