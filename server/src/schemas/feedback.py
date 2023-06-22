from typing import Optional
from pydantic import Extra, Field
from src.schemas.base import (
    MongoBaseCreate,
    MongoBaseRead,
    MyBaseModel,
    PyObjectId,
)


class FeedbackBase(MyBaseModel):
    """Feedback for an inference. Can be from an end user or internal user, `end_user_id` is null if from internal user.
    Allows for different scoring methods and flags for internal evaluation and end user feedback.
    Eg. End users can thumbs down/up mapped to -1 +1 `score`, internal users rate between from 0 to 100 and can add a note.
    """

    inference_id: PyObjectId = Field(..., description="The inference being rated")
    end_user_id: Optional[str] = Field(
        None,
        description="API consumers' end user id If feedback from end user otherwise null",
    )
    score: int = Field(
        ...,
        description="Any arbitrary integer score. Rules are up to the API consumer",
    )
    flag: Optional[str] = Field(
        None,
        description="Any arbitrary string flagging of the inference. Rules are up to the API consumer.",
    )
    note: Optional[str] = Field(None)


class FeedbackCreate(FeedbackBase, extra=Extra.forbid):
    pass


class FeedbackInDB(FeedbackBase, MongoBaseCreate, extra=Extra.allow):
    prompt_version_id: PyObjectId


class FeedbackRead(MongoBaseRead, extra=Extra.ignore):
    prompt_version_id: Optional[PyObjectId] = None
