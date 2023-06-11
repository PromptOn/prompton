# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .chat_gpt_chat_completition_response import ChatGptChatCompletitionResponse
from .chat_gpt_message import ChatGptMessage
from .chat_gpt_token_usage import ChatGptTokenUsage


class InferenceResponseData(pydantic.BaseModel):
    completed_at: typing.Optional[str]
    completition_duration_seconds: typing.Optional[float]
    is_client_connected_at_finish: typing.Optional[bool]
    is_error: typing.Optional[bool] = pydantic.Field(alias="isError")
    first_message: ChatGptMessage
    token_usage: ChatGptTokenUsage
    raw_response: ChatGptChatCompletitionResponse

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
