from typing import List, Annotated
from fastapi import APIRouter, Depends, Request, status

from server.core.database import get_db
from server.crud.org import org_crud
from server.schemas.user import UserInDB
from server.core.user import get_current_active_user
from server.core.completition import get_openai_chat_completition

from server.core.utils import str_to_ObjectId
from server.crud.inference import inference_crud
from server.endpoints.ApiResponses import ReqResponses
from server.endpoints.endpoint_exceptions import (
    ItemNotFoundException,
    MalformedRequestError,
    OpenAIError,
)

from server.schemas.inference import (
    InferenceCreate,
    InferencePostResponse,
    InferenceRead,
    InferenceResponseError,
    InferenceResponseStatus,
    InferenceUpdate,
)


router = APIRouter()

# TODO: feedbacks. distiguish end user and 3rd party feedback. should be in separate collection


# TODO: add filter by status
# TODO: add pagination or cursor
# TODO: ordering?
@router.get(
    "/inferences",
    tags=["inferences"],
    response_model=List[InferenceRead],
    responses={**ReqResponses.MalformedRequestError},
)
async def get_inferences_list(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
    prompt_version_id: str | None = None,
    prompt_id: str | None = None,
):
    if prompt_version_id and prompt_id:
        raise MalformedRequestError(
            "Can't filter by both `prompt_version_id` and `prompt_id`. Choose one."
        )

    filter = None

    if prompt_version_id:
        prompt_version_id_oid = str_to_ObjectId(
            prompt_version_id
        )  # raises if malformed
        filter = {"prompt_version_id": prompt_version_id_oid}
    elif prompt_id:
        prompt_id_oid = str_to_ObjectId(prompt_id)  # raises if malformed
        filter = {"prompt_id": prompt_id_oid}

    inferences = await inference_crud.get_multi(db, current_user, filter=filter)

    return inferences


@router.get(
    "/inferences/{id}",
    tags=["inferences"],
    response_model=InferenceRead,
    responses={**ReqResponses.INVALID_ITEM_ID},
)
async def get_inference_by_id(
    id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    return await inference_crud.get(db, id, current_user)


# TODO: Inference by prompt_id - should use one of (or the latest?) live version
# TODO: ability to log inference request and response separately and without calling completition - so one can call their completion on their own or log historic data
@router.post(
    "/inferences",
    tags=["inferences"],
    status_code=status.HTTP_201_CREATED,
    responses={
        **ReqResponses.POST_CREATED,
        **ReqResponses.OPENAI_ERROR,
        **ReqResponses.OPENAI_TIMEOUT,
    },
)
async def new_inference(
    request: Request,
    inferenceRequest: InferenceCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
) -> InferencePostResponse:
    # NB: The processing doesn't stop if client disconnects See: https://github.com/tiangolo/fastapi/discussions/8805

    try:
        user_org = await org_crud.get(db, current_user.org_id, current_user)
    except ItemNotFoundException:
        raise MalformedRequestError(
            f"Current user is not associated with a valid organization - user's org_id {current_user.org_id} doesn't exists. Can't create inferences."
        )

    if not user_org.access_keys or not user_org.access_keys.get("openai_api_key"):
        raise MalformedRequestError(
            f"Curren user's organization doesn't have openai_api_key set. Can't create inferences. Set access_keys.openai_api_key for org_id {user_org.id}."
        )

    openai_api_key = user_org.access_keys.get("openai_api_key")

    if not openai_api_key or not openai_api_key.strip():
        raise MalformedRequestError(
            f"Curren user's organization openai_api_key key is empty. Can't create inferences. Set access_keys.openai_api_key for org_id {user_org.id}."
        )

    new_inference = await inference_crud.create(db, inferenceRequest, current_user)

    # we could avoid re-fetching by refactoring inference_crud.create - get back to it if performanance is an issue
    inferenceDB = await inference_crud.get(db, new_inference.inserted_id, current_user)

    inferenceResponse = await get_openai_chat_completition(
        inferenceDB.request.raw_request,
        openai_api_key,
        request_timeout=inferenceRequest.request_timeout,
    )

    #  this logic should be in inference_crud.update but requires refactor to get back calculated status without refetching
    if isinstance(inferenceResponse, InferenceResponseError):
        inferenceResponse.isError = True

        if inferenceResponse.error.get("error_class") == "openai.error.Timeout":
            status = InferenceResponseStatus.COMPLETITION_TIMEOUT
        else:
            status = InferenceResponseStatus.COMPLETITION_ERROR

    else:
        inferenceResponse.isError = False
        status = InferenceResponseStatus.PROCESSED

    inferenceResponse.is_client_connected_at_finish = (
        not await request.is_disconnected()
    )

    inferenceUpdate = InferenceUpdate(status=status, response=inferenceResponse)
    _ = await inference_crud.update(db, inferenceDB.id, inferenceUpdate, current_user)

    if isinstance(inferenceResponse, InferenceResponseError):
        if status == InferenceResponseStatus.COMPLETITION_TIMEOUT:
            raise OpenAIError(
                inference_id=inferenceDB.id,
                error=inferenceResponse.error,
                message="OpenAI API Timeout Error",
            )
        else:  # status == InferenceResponseStatus.COMPLETITION_ERROR
            raise OpenAIError(
                inference_id=inferenceDB.id,
                error=inferenceResponse.error,
                message="OpenAI API Error",
            )

    response = InferencePostResponse(id=inferenceDB.id, response=inferenceResponse)

    return response
