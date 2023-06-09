from typing import Optional
from pydantic import BaseModel, Extra, Field, ConstrainedStr
from datetime import datetime
from bson import ObjectId
import pydantic


class NonEmptyStrField(ConstrainedStr):
    strip_whitespace = True
    min_length = 1


NameField = NonEmptyStrField


class DefaultPostResponse(BaseModel):
    """Standard response for POST requests. Contains the id of the created item."""

    id: str = Field(..., description="The id of the created item")


class MyBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid
        # TODO: orjson  or ujson for better performance https://github.com/zhanymkanov/fastapi-best-practices#8-custom-base-model-from-day-0

        json_encoders = {ObjectId: str}


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoBaseCreate(MyBaseModel):
    """Base model for creating a record in MongoDB. Populates `id` and `created_at` when not passed.
    `created_by_user_id` and `created_by_org_id` fields should be populated by base CRUD class
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_user_id: Optional[PyObjectId] = None
    created_by_org_id: Optional[PyObjectId] = None


class MongoBaseRead(MyBaseModel):
    """Base model for reading from MongoDB. Same as MongoBaseCreate but assumes all DB base fields are populated so generated clients doesn't requrie None checks"""

    id: PyObjectId = Field(alias="_id")
    created_at: datetime
    created_by_user_id: PyObjectId
    created_by_org_id: PyObjectId


class AllOptional(pydantic.main.ModelMetaclass):
    """Make all fields optional on class but keep validators. Using it PATCH schema can be based on Base/Create schema
    `class PromptUpdate(AllOptional, PromptBase):`

    If you like rabbit holes: https://stackoverflow.com/questions/67699451/make-every-field-as-optional-with-pydantic/72365032
    """

    def __new__(mcls, name, bases, namespaces, **kwargs):
        cls = super().__new__(mcls, name, bases, namespaces, **kwargs)
        for field in cls.__fields__.values():
            field.required = False
        return cls
