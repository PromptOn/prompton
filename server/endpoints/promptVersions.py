from typing import List, Annotated
from fastapi import APIRouter, Depends, status


from server.core.database import get_db
from server.schemas.user import UserInDB
from server.core.user import get_current_active_user
from server.core.utils import str_to_ObjectId
from server.schemas.promptVersion import (
    PromptVersionCreate,
    PromptVersionUpdate,
    PromptVersionRead,
)
from server.endpoints.ApiResponses import ReqResponses
from server.crud.promptVersion import promptVersion_crud

router = APIRouter()


# TODO: add pagination or cursor
# TODO: ordering?
# TODO: auto version numbering? could replace name field. shall we worry about concurrency or naiv approach enough?
# TODO: return number of inferences (optional?)
@router.get(
    "/promptVersions", tags=["promptVersions"], response_model=List[PromptVersionRead]
)
async def get_promptVersions_list(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
    prompt_id: str | None = None,
):
    filter = None

    if prompt_id:
        prompt_id_oid = str_to_ObjectId(prompt_id)  # will raise if malfromed oid
        filter = {"prompt_id": prompt_id_oid}

    promptVersions = await promptVersion_crud.get_multi(db, current_user, filter=filter)

    return promptVersions


@router.get(
    "/promptVersions/{id}",
    tags=["promptVersions"],
    response_model=PromptVersionRead,
    responses={**ReqResponses.INVALID_ITEM_ID},
)
async def get_promptVersion_by_id(
    id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    promptVersion = await promptVersion_crud.get(db, id, current_user=current_user)
    return promptVersion


@router.post(
    "/promptVersions",
    tags=["promptVersions"],
    status_code=status.HTTP_201_CREATED,
    responses={**ReqResponses.POST_CREATED},
)
async def add_promptVersion(
    promptVersion: PromptVersionCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    insert_res = await promptVersion_crud.create(
        db, promptVersion, current_user=current_user
    )

    return {"id": str(insert_res.inserted_id)}


@router.patch(
    "/promptVersions/{id}",
    tags=["promptVersions"],
    response_model=PromptVersionRead,
    responses={**ReqResponses.INVALID_ITEM_ID, **ReqResponses.PATH_UPDATED},
)
async def update_promptVersion(
    promptVersion_patch: PromptVersionUpdate,
    id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    promptVersion_updated = await promptVersion_crud.update_and_fetch(
        db, id, promptVersion_patch, current_user
    )

    return promptVersion_updated
