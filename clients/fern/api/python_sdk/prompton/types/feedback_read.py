# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime


class FeedbackRead(pydantic.BaseModel):
    """
    Base model for reading from MongoDB. Same as MongoBaseCreate but assumes all DB base fields are populated so generated clients doesn't requrie None checks
    """

    id: str = pydantic.Field(alias="_id")
    created_at: str
    created_by_user_id: str
    created_by_org_id: str
    inference_id: str = pydantic.Field(description=("The inference being rated\n"))
    end_user_id: typing.Optional[str] = pydantic.Field(
        description=("API consumers' end user id If feedback from end user otherwise null\n")
    )
    feedback_for_part: typing.Optional[str] = pydantic.Field(
        description=(
            "Specifies which part of the output the feedback is about. Can be used when the inference has multiple sections which require separate feedback\n"
        )
    )
    score: typing.Optional[int] = pydantic.Field(
        description=(
            "Any integer score. Rules are up to the API consumer. Can be null if it was flagging or note only\n"
        )
    )
    flag: typing.Optional[str] = pydantic.Field(
        description=("Any string when inference was flagged. Can be null if it is scoring or note only\n")
    )
    note: typing.Optional[str]
    metadata: typing.Optional[typing.Dict[str, typing.Any]]
    prompt_version_id: typing.Optional[str]

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
