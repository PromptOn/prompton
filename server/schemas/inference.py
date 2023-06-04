from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import Extra, Field
from server.schemas.openAI import (
    ChatGPTChatCompletitionRequest,
    ChatGPTChatCompletitionResponse,
    ChatGPTMessage,
    ChatGPTTokenUsage,
)

from server.schemas.base import (
    MongoBase,
    MyBaseModel,
    NonEmptyStrField,
    PyObjectId,
)
from server.schemas.promptVersion import PromptVersionProviders


class InferenceResponseStatus(str, Enum):
    REQUEST_RECEIVED = "RequestReceived"
    PROCESSED = "Processed"
    COMPLETITION_ERROR = "CompletitionError"
    COMPLETITION_TIMEOUT = "CompletitionTimeout"


# TODO: num_samples
# TODO: streaming
class InferenceBase(MyBaseModel):
    endUserId: NonEmptyStrField
    source: NonEmptyStrField
    template_args: Optional[dict[str, str]] = Field(None)
    metadata: Optional[dict[str, Any]] = Field(None)
    request_timeout: Optional[float] = Field(None)
    prompt_version_id: PyObjectId


class InferenceCreate(InferenceBase, extra=Extra.forbid):
    pass


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
    first_message: ChatGPTMessage
    token_usage: ChatGPTTokenUsage
    raw_response: ChatGPTChatCompletitionResponse


class InferenceRequestData(MyBaseModel):
    provider: PromptVersionProviders
    raw_request: ChatGPTChatCompletitionRequest


class InferenceUpdate(MyBaseModel, extra=Extra.forbid):
    status: InferenceResponseStatus
    response: InferenceResponseData | InferenceResponseError


class InferenceInDB(InferenceBase, MongoBase, extra=Extra.allow):
    prompt_id: PyObjectId
    prompt_version_name: str = Field(None)
    status: Optional[InferenceResponseStatus] = Field(
        default=InferenceResponseStatus.REQUEST_RECEIVED
    )
    request: InferenceRequestData = Field(None)
    response: Optional[InferenceResponseData | InferenceResponseError] = Field(None)


class InferenceRead(InferenceInDB, extra=Extra.ignore):
    pass


class InferencePostResponse(MyBaseModel, extra=Extra.ignore):
    """Used for FastAPI response model"""

    id: PyObjectId
    response: InferenceResponseData | InferenceResponseError
