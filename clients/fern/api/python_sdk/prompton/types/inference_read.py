# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .inference_read_response import InferenceReadResponse
from .inference_request_data import InferenceRequestData
from .inference_response_status import InferenceResponseStatus


class InferenceRead(pydantic.BaseModel):
    id: typing.Optional[str] = pydantic.Field(alias="_id")
    created_at: typing.Optional[str]
    created_by_user_id: typing.Optional[str]
    created_by_org_id: typing.Optional[str]
    end_user_id: str = pydantic.Field(description=("`non-empty`\n"))
    source: str = pydantic.Field(description=("`non-empty`\n"))
    template_args: typing.Optional[typing.Dict[str, str]]
    metadata: typing.Optional[typing.Dict[str, typing.Any]]
    request_timeout: typing.Optional[float]
    prompt_version_id: str
    prompt_id: str
    prompt_version_name: typing.Optional[str]
    status: typing.Optional[InferenceResponseStatus]
    request: typing.Optional[InferenceRequestData]
    response: typing.Optional[InferenceReadResponse]

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