from typing import Any, Optional
from pydantic import Extra, Field, root_validator
from src.schemas.base import (
    MongoBaseCreate,
    MongoBaseRead,
    MyBaseModel,
    PyObjectId,
)


class FeedbackBase(MyBaseModel):
    inference_id: PyObjectId = Field(..., description="The inference being rated")
    end_user_id: Optional[str] = Field(
        None,
        description="API consumers' end user id If feedback from end user otherwise null",
    )
    feedback_for_part: Optional[str] = Field(
        None,
        description="Specifies which part of the output the feedback is about. Can be used when the inference has multiple sections which require separate feedback",
    )
    score: Optional[int] = Field(
        None,
        description="Any integer score. Rules are up to the API consumer. Can be null if it was flagging or note only",
    )
    flag: Optional[str] = Field(
        None,
        description="Any string when inference was flagged. Can be null if it is scoring or note only",
    )
    note: Optional[str] = Field(None)
    metadata: Optional[dict[str, Any]] = Field(None)


class FeedbackCreate(FeedbackBase, extra=Extra.forbid):
    @root_validator
    def mandatory_field_validation(cls, values):
        """Check if either `score`, `flag` or `note` is provided"""
        if not (values.get("score") or values.get("flag") or values.get("note")):
            raise ValueError(
                "At least one of `score`, `flag` or `note` must be provided"
            )
        return values


class FeedbackUpdate(FeedbackBase, extra=Extra.forbid):
    """Only placeholder for now as no feedback update feature"""

    # TODO: decide what we allow to update with FeedbackUpdate and by whom (if need it at all)
    pass


class FeedbackInDB(FeedbackBase, MongoBaseCreate, extra=Extra.allow):
    prompt_version_id: PyObjectId


class FeedbackRead(FeedbackBase, MongoBaseRead, extra=Extra.ignore):
    prompt_version_id: Optional[PyObjectId] = None
