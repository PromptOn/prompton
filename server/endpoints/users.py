from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from pymongo.errors import DuplicateKeyError

from server.core.database import get_db
from server.endpoints.endpoint_exceptions import (
    EmailAlreadyExistsError,
    PermissionValidationError,
)
from server.schemas.user import UserInDB, UserRoles
from server.core.user import (
    get_current_active_user,
    get_current_org_admin_user,
)
from server.endpoints.ApiResponses import ReqResponses
from server.schemas.user import UserCreate, UserRead
from server.crud.user import user_crud

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
):
    if (
        current_user.role != UserRoles.SUPER_ADMIN
        and user_to_add.org_id != current_user.org_id
    ):
        raise PermissionValidationError(
            f"Not authorized to add user to `org_id` {user_to_add.org_id}.  `OrgAdmin` can only add user to own org"
        )

    try:
        insert_res = await user_crud.create(db, user_to_add, current_user)
    except DuplicateKeyError:
        raise EmailAlreadyExistsError(email=user_to_add.email)

    return {"id": str(insert_res.inserted_id)}


# TODO: update user (password, email, org?, role, disabled)
