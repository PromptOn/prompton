from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from src.core.user import get_current_active_user

from src.endpoints.endpoint_exceptions import (
    NotImplementedException,
)
from src.schemas.prompt import PromptUpdate, PromptRead, PromptCreate
from src.core.database import get_db
from src.endpoints.ApiResponses import ReqResponses
from src.crud.prompt import prompt_crud
from src.schemas.user import UserInDB


router = APIRouter()


# Based on  https://github.com/PacktPublishing/Building-Data-Science-Applications-with-FastAPI/blob/main/chapter6/mongodb/models.py


# TODO: add filter by status and name (search by name?)
# TODO: add pagination or cursor
# TODO: ordering?
# TODO: return number of prompteVersions (optional?)
@router.get(
    "/prompts",
    tags=["prompts"],
    responses={**ReqResponses.GET_RESPONSES},
    response_model=List[PromptRead],
)
async def get_prompts_list(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    res = await prompt_crud.get_multi(db, current_user=current_user)

    return res


@router.get(
    "/prompts/{id}",
    tags=["prompts"],
    response_model=PromptRead,
    responses={**ReqResponses.GET_RESPONSES},
)
async def get_prompt_by_id(
    id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    return await prompt_crud.get(db, id, current_user)


@router.post(
    "/prompts",
    tags=["prompts"],
    status_code=status.HTTP_201_CREATED,
    responses={**ReqResponses.POST_RESPONSES},
)
async def add_prompt(
    prompt: PromptCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    insert_res = await prompt_crud.create(db, prompt, current_user)

    return {"id": str(insert_res.inserted_id)}


@router.patch(
    "/prompts/{id}",
    tags=["prompts"],
    response_model=PromptRead,
    responses={**ReqResponses.PATCH_RESPONSES},
)
async def update_prompt(
    prompt_patch: PromptUpdate,
    id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    prompt = await prompt_crud.update_and_fetch(db, id, prompt_patch, current_user)

    return prompt


@router.delete(
    "/prompts/{id}",
    tags=["prompts"],
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    responses={
        **ReqResponses.INVALID_ITEM_ID,
        **ReqResponses.NOT_IMPLEMENTED,
    },
)
async def delete_prompt(
    id: str, current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    #  TODO: implement delete (only if no promptVersions)
    """Not implemented"""
    raise NotImplementedException("delete prompt")
