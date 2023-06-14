from datetime import datetime
from enum import Enum
from typing import Any, List, Optional
from pydantic import Extra, Field
from src.schemas.openAI import (
    ChatGPTChatCompletitionRequest,
    ChatGPTChatCompletitionResponse,
    ChatGPTMessage,
    ChatGPTTokenUsage,
)

from src.schemas.base import (
    MongoBase,
    MyBaseModel,
    NonEmptyStrField,
    PyObjectId,
)
from src.schemas.promptVersion import PromptVersionProviders


class InferenceResponseStatus(str, Enum):
    REQUEST_RECEIVED = "RequestReceived"
    PROCESSED = "Processed"
    COMPLETITION_ERROR = "CompletitionError"
    COMPLETITION_TIMEOUT = "CompletitionTimeout"


# TODO: num_samples
# TODO: streaming
class InferenceBase(MyBaseModel):
    end_user_id: NonEmptyStrField
    source: NonEmptyStrField
    template_args: Optional[dict[str, str]] = Field(None)
    metadata: Optional[dict[str, Any]] = Field(None)
    request_timeout: Optional[float] = Field(None)


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


class InferenceInDB(InferenceBase, MongoBase, extra=Extra.allow):
    prompt_version_id: PyObjectId
    prompt_version_ids_considered: List[PyObjectId] = Field(
        [],
        description="If inference was by prompt_id then a list of all other prompt versions considered for this inference. I.e. all prompt versions in Live status at the time of the inference",
    )
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
