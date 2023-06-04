from typing import Optional
from pydantic import BaseModel, Extra, Field, ConstrainedStr, root_validator, validator
from datetime import datetime
from bson import DatetimeMS, ObjectId
import pydantic


class NonEmptyStrField(ConstrainedStr):
    strip_whitespace = True
    min_length = 1


NameField = NonEmptyStrField


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


class MongoBase(MyBaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_user_id: Optional[PyObjectId] = None
    created_by_org_id: Optional[PyObjectId] = None


class AllOptional(pydantic.main.ModelMetaclass):
    """Make all fields optional on class. Using this PATCH schema can be based on Base/Create schema
    Usage:

    `class ItemPatch(ItemBase, metaclass=AllOptional):`
    """

    def __new__(cls, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)
