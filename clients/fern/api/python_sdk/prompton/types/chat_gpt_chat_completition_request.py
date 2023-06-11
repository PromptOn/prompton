# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .chat_gpt_chat_completition_request_stop import ChatGptChatCompletitionRequestStop
from .chat_gpt_message import ChatGptMessage


class ChatGptChatCompletitionRequest(pydantic.BaseModel):
    model: typing.Optional[str] = pydantic.Field(description=("`non-empty`\n"))
    temperature: typing.Optional[float]
    top_p: typing.Optional[float]
    stop: typing.Optional[ChatGptChatCompletitionRequestStop]
    max_tokens: typing.Optional[int]
    presence_penalty: typing.Optional[float]
    frequency_penalty: typing.Optional[float]
    logit_bias: typing.Optional[typing.Dict[str, int]]
    messages: typing.List[ChatGptMessage]
    n: typing.Optional[int]
    stream: typing.Optional[bool]
    user: typing.Optional[str]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}