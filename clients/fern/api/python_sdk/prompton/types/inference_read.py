# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .inference_read_response import InferenceReadResponse
from .inference_request_data import InferenceRequestData
from .inference_response_status import InferenceResponseStatus


class InferenceRead(pydantic.BaseModel):
    """
    Base model for reading from MongoDB. Same as MongoBaseCreate but assumes all DB base fields are populated so generated clients doesn't requrie None checks
    """

    id: str = pydantic.Field(alias="_id")
    created_at: str
    created_by_user_id: str
    created_by_org_id: str
    end_user_id: typing.Optional[str] = pydantic.Field(
        description=(
            "The API consumer's internal user reference for metrics. It is also relayed to the provider as part of the request if the provider supports it (eg. OpenAI's user field).\n"
        )
    )
    source: typing.Optional[str] = pydantic.Field(
        description=("The API consumer's source for metrics (e.g. AndroidApp etc).\n")
    )
    client_ref_id: typing.Optional[str] = pydantic.Field(
        description=("The API consumer's internal reference id to able to link references to their sessions.\n")
    )
    template_args: typing.Dict[str, str]
    metadata: typing.Optional[typing.Dict[str, typing.Any]]
    request_timeout: typing.Optional[float] = pydantic.Field(
        description=(
            "Provider request timout in seconds. If not provided, then Prompton API's default timeout for the provider will be used (90sec or `DEFAULT_OPENAI_REQUEST_TIMEOUT_SECONDS` env var if provided).\n"
        )
    )
    prompt_version_id: str
    prompt_version_ids_considered: typing.List[str]
    prompt_id: str
    prompt_version_name: str
    status: InferenceResponseStatus
    request: InferenceRequestData
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
