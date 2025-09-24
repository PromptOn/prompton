from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, status

from src.core.user import get_current_active_user
from src.core.database import get_db
from src.core.utils import str_to_ObjectId
from src.endpoints.ApiResponses import ReqResponses

from src.schemas.base import DefaultPostResponse
from src.schemas.feedback import FeedbackRead, FeedbackCreate
from src.crud.feedback import feedback_crud
from src.schemas.user import UserInDB


router = APIRouter()


@router.get(
    "/feedbacks",
    tags=["feedbacks"],
    responses={**ReqResponses.GET_RESPONSES},
    response_model=List[FeedbackRead],
)
async def get_feedbacks_list(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
    prompt_version_id: Optional[str] = None,
    prompton_user_id: Optional[str] = None,
    inference_id: Optional[str] = None,
):
    filter = {}

    # str_to_ObjectId raises if id malformed
    if prompt_version_id:
        filter["prompt_version_id"] = str_to_ObjectId(prompt_version_id)

    if prompton_user_id:
        filter["created_by_user_id"] = str_to_ObjectId(prompton_user_id)

    if inference_id:
        filter["inference_id"] = str_to_ObjectId(inference_id)

    res = await feedback_crud.get_multi(db, current_user=current_user, filter=filter)

    return res


@router.get(
    "/feedbacks/{id}",
    tags=["feedbacks"],
    response_model=FeedbackRead,
    responses={**ReqResponses.GET_RESPONSES},
)
async def get_feedback_by_id(
    id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    return await feedback_crud.get(db, id, current_user)


@router.post(
    "/feedbacks",
    tags=["feedbacks"],
    status_code=status.HTTP_201_CREATED,
    responses={**ReqResponses.POST_RESPONSES},
)
async def add_feedback(
    feedback: FeedbackCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
) -> DefaultPostResponse:
    """Feedback about an inference from an end user or from a PromptOn user.

    At least one of `score`, `flag` or `note` required

    `end_user_id` is null if from PromptOn user.

    `score` can be null if flagging or note only. Scoring method are for API consumer consideration. Eg. end users can thumbs down/up mapped to -1 +1 `score`, internal users rate between from 0 to 100.

    `flag` is any string when inference was flagged. Can be null if it is scoring or note only

    `feedback_for_part` is optional and can be used when the inference has multiple sections which require separate feedback.

    `metadata` is any dict for additional information.
    """

    insert_res = await feedback_crud.create(db, feedback, current_user)

    return DefaultPostResponse(id=str(insert_res.inserted_id))
