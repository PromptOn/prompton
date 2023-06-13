# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime


class InferenceCreateByPromptVersionId(pydantic.BaseModel):
    end_user_id: str = pydantic.Field(description=('<span style="white-space: nowrap">`non-empty`</span>\n'))
    source: str = pydantic.Field(description=('<span style="white-space: nowrap">`non-empty`</span>\n'))
    template_args: typing.Optional[typing.Dict[str, str]]
    metadata: typing.Optional[typing.Dict[str, typing.Any]]
    request_timeout: typing.Optional[float]
    prompt_version_id: str

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}