from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from pymongo.errors import DuplicateKeyError

from src.core.database import get_db
from src.endpoints.endpoint_exceptions import (
    EmailAlreadyExistsError,
    PermissionValidationError,
)
from src.schemas.base import DefaultPostResponse
from src.schemas.user import UserInDB, UserRoles
from src.core.user import (
    get_current_active_user,
    get_current_org_admin_user,
)
from src.endpoints.ApiResponses import ReqResponses
from src.schemas.user import UserCreate, UserRead
from src.crud.user import user_crud

router = APIRouter()

# TODO: signup endpoint


@router.get(
    "/users",
    tags=["users"],
    responses={**ReqResponses.GET_RESPONSES},
    response_model=List[UserRead],
)
async def get_users_list(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    res = await user_crud.get_multi(db, current_user)

    return res


@router.get(
    "/users/me",
    tags=["users"],
    responses={**ReqResponses.GET_RESPONSES},
    response_model=UserRead,
)
async def get_current_user(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    return await user_crud.get(db, current_user.id, current_user)


@router.get(
    "/users/{id}",
    tags=["users"],
    responses={**ReqResponses.GET_RESPONSES},
    response_model=UserRead,
)
async def get_user_by_id(
    id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db=Depends(get_db),
):
    return await user_crud.get(db, id, current_user)


@router.post(
    "/users",
    tags=["users"],
    responses={**ReqResponses.POST_RESPONSES},
    status_code=status.HTTP_201_CREATED,
)
async def add_new_user(
    user_to_add: UserCreate,
    current_user: Annotated[UserInDB, Depends(get_current_org_admin_user)],
    db=Depends(get_db),
) -> DefaultPostResponse:
    if (
        current_user.role != UserRoles.SUPER_ADMIN
        and user_to_add.org_id != current_user.org_id
    ):
        raise PermissionValidationError(
            f"`OrgAdmin` can only add user to own org. Not authorized to add user to `provided org_id` {user_to_add.org_id}."
        )

    if current_user.role != UserRoles.SUPER_ADMIN and (
        user_to_add.role not in (UserRoles.ORG_ADMIN, UserRoles.BASIC)
    ):
        raise PermissionValidationError(
            f"`OrgAdmin`can only add OrgAdmin or Baisc role users. Not authorized to add user with provided '{user_to_add.role}' role."
        )

    try:
        insert_res = await user_crud.create(db, user_to_add, current_user)
    except DuplicateKeyError:
        raise EmailAlreadyExistsError(email=user_to_add.email)

    return DefaultPostResponse(id=str(insert_res.inserted_id))


# TODO: update user (password, email, org?, role, disabled)
