from enum import Enum
from typing import List, Optional

from pydantic import Field

from src.schemas.base import MyBaseModel, NonEmptyStrField


class ChatGPTRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatGPTMessage(MyBaseModel):
    role: ChatGPTRole
    content: str
    name: Optional[str]


ChatGPTMessageTemplate = List[ChatGPTMessage]


class ChatGPTChatCompletitionConfig(MyBaseModel):
    model: NonEmptyStrField | None
    temperature: float = Field(None, ge=0.0)
    top_p: float = Field(None, ge=0.0, le=1.0)
    stop: List[str] | str = Field(None)
    max_tokens: int = Field(None, ge=1)
    presence_penalty: float = Field(None, ge=-2.0, le=2.0)
    frequency_penalty: float = Field(None, ge=-2.0, le=2.0)
    logit_bias: dict[int, int] = Field(None)


class ChatGPTChatCompletitionRequest(ChatGPTChatCompletitionConfig, MyBaseModel):
    messages: ChatGPTMessageTemplate
    n: int = Field(1, ge=1)
    stream: bool = Field(False)
    user: str = Field(None)


class ChatGPTTokenUsage(MyBaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatGPTCompletitionChoice(MyBaseModel):
    message: ChatGPTMessage
    finish_reason: str
    index: int


class ChatGPTChatCompletitionResponse(MyBaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: ChatGPTTokenUsage
    choices: List[ChatGPTCompletitionChoice]
