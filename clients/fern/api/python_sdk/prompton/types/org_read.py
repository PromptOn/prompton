# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime


class OrgRead(pydantic.BaseModel):
    id: typing.Optional[str] = pydantic.Field(alias="_id")
    created_at: typing.Optional[str]
    created_by_user_id: typing.Optional[str]
    created_by_org_id: typing.Optional[str]
    name: str = pydantic.Field(description=("`non-empty`\n"))
    access_keys: typing.Optional[typing.Dict[str, str]]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        allow_population_by_field_name = True
        json_encoders = {dt.datetime: serialize_datetime}
