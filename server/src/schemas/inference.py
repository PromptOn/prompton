from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import Extra, Field
from src.schemas.openAI import (
    ChatGPTChatCompletitionRequest,
    ChatGPTChatCompletitionResponse,
    ChatGPTTokenUsage,
)

from src.schemas.base import MongoBaseCreate, MongoBaseRead, MyBaseModel, PyObjectId
from src.schemas.promptVersion import PromptVersionProviders


class InferenceResponseStatus(str, Enum):
    REQUEST_RECEIVED = "RequestReceived"
    PROCESSED = "Processed"
    COMPLETITION_ERROR = "CompletitionError"
    COMPLETITION_TIMEOUT = "CompletitionTimeout"


# TODO: num_samples
# TODO: streaming
class InferenceBase(MyBaseModel):
    end_user_id: str | None = Field(
        None,
        description="The API consumer's internal user reference for metrics. It is also relayed to the provider as part of the request if the provider supports it (eg. OpenAI's user field).",
    )
    source: str | None = Field(
        None,
        description="The API consumer's source for metrics (e.g. AndroidApp etc).",
    )
    client_ref_id: str | None = Field(
        None,
        description="The API consumer's internal reference id to able to link references to their sessions.",
    )
    template_args: Optional[dict[str, str]] = Field(None)
    metadata: Optional[dict[str, Any]] = Field(None)
    request_timeout: Optional[float] = Field(
        None,
        description="Provider request timout in seconds. If not provided, then Prompton API's default timeout for the provider will be used (90sec or `DEFAULT_OPENAI_REQUEST_TIMEOUT_SECONDS` env var if provided).",
    )


class InferenceCreateByPromptVersionId(InferenceBase, extra=Extra.forbid):
    prompt_version_id: PyObjectId


class InferenceCreateByPromptId(InferenceBase, extra=Extra.forbid):
    """Create inference by `prompt_id`. It can only be used if there is at least one 'Live' status prompt version for the provided `prompt_id`.
    If there are multiple prompt versions in Live status it will pick one randomly. Useful for split testing prompt versions.
    It stores all other `prompt_version_id`s in Live status at the time of the inference in `prompt_version_ids_considered` field.
    """

    prompt_id: PyObjectId


class InferenceResponseBase(MyBaseModel):
    completed_at: datetime = Field(default_factory=datetime.utcnow)
    completition_duration_seconds: Optional[float] = None
    is_client_connected_at_finish: Optional[bool] = None


class InferenceResponseError(InferenceResponseBase):
    isError: bool = True
    error: Any


class InferenceResponseData(InferenceResponseBase):
    isError: bool = False
    # time_to_first: int = Field(None) # if streaming
    token_usage: ChatGPTTokenUsage
    raw_response: ChatGPTChatCompletitionResponse


class InferenceRequestData(MyBaseModel):
    provider: PromptVersionProviders
    raw_request: ChatGPTChatCompletitionRequest


class InferenceUpdate(MyBaseModel, extra=Extra.forbid):
    status: InferenceResponseStatus
    response: InferenceResponseData | InferenceResponseError


class InferenceInDBBase(InferenceBase, extra=Extra.allow):
    prompt_version_id: PyObjectId
    prompt_version_ids_considered: List[PyObjectId] = Field(
        ...,
        description="If inference was by prompt_id then a list of all other prompt versions considered for this inference. I.e. all prompt versions in Live status at the time of the inference",
    )
    prompt_id: PyObjectId
    prompt_version_name: str
    status: InferenceResponseStatus
    request: InferenceRequestData
    response: Optional[InferenceResponseData | InferenceResponseError] = Field(None)


class InferenceInDB(InferenceInDBBase, MongoBaseCreate, extra=Extra.allow):
    """Same as InferenceRead but status and base DB fields are not mandatory to be populated by pydantic defaults"""

    pass


class InferenceRead(InferenceInDBBase, MongoBaseRead, extra=Extra.ignore):
    # Same as InferenceInDB but fields with default values are mandatory so clients don't need to check None values
    prompt_version_ids_considered: List[PyObjectId]
    template_args: Dict[str, str]
    pass


class InferencePostResponse(MyBaseModel, extra=Extra.ignore):
    """Used for FastAPI response model"""

    id: PyObjectId
    response: InferenceResponseData | InferenceResponseError
