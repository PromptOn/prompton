from bson import ObjectId
from pydantic import BaseModel, Extra, ValidationError
import pytest

from src.schemas.base import AllOptional


class MyBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid
        # TODO: orjson  or ujson for better performance https://github.com/zhanymkanov/fastapi-best-practices#8-custom-base-model-from-day-0

        json_encoders = {ObjectId: str}


class FooNest(MyBaseModel):
    boo: int


class FooBase(MyBaseModel):
    root: int
    nest: FooNest


class FooCreate(FooBase, extra=Extra.forbid):
    pass


class FooInDB(FooCreate, MyBaseModel, extra=Extra.allow):
    pass


class FooPatch(FooCreate, metaclass=AllOptional):
    pass


class FooRead(FooCreate, MyBaseModel, extra=Extra.ignore):
    pass


@pytest.mark.anyio
async def test_pydantic_allow_extra():
    test_no_extra = {"root": 2, "nest": {"boo": 2}}
    test_root_extra = {"root": 2, "nest": {"boo": 2}, "extra": "extra val"}

    test_nested_extra = {"root": 2, "nest": {"boo": 2, "extra": "xxx"}}

    # all should work with without extra
    for obj in [FooInDB, FooRead, FooPatch]:
        parsed = obj.parse_obj(test_no_extra)
        assert parsed.dict() == test_no_extra

    # FooInDB should allow extra
    parsed = FooInDB.parse_obj(test_root_extra)
    assert parsed.dict() == test_root_extra

    # THIS RAISES: ValidationError
    # See: https://stackoverflow.com/questions/76481931/how-to-set-pydantic-extra-allow-extra-ignore-on-nested-class-fields
    # parsed = FooInDB.parse_obj(test_nested_extra)
    # assert parsed.dict() == test_nested_extra

    # FooRead should ignore extra
    parsed = FooRead.parse_obj(test_root_extra)
    assert parsed.dict() == test_no_extra

    # THIS RAISES: ValidationError
    # parsed = FooRead.parse_obj(test_nested_extra)
    # assert parsed.dict() == test_no_extra

    # FooPatch should forbid extra
    with pytest.raises(ValidationError):
        FooPatch.parse_obj(test_root_extra)

    with pytest.raises(ValidationError):
        FooPatch.parse_obj(test_nested_extra)

    print(parsed)
