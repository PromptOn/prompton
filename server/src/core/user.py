from typing import Annotated
from fastapi import Depends, HTTPException
from src.endpoints.endpoint_exceptions import PermissionValidationError

from src.schemas.user import UserInDB, UserRoles
import src.core.auth as auth  # need to import in this format to allow monkeypatching in tests


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(auth.get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def get_current_org_admin_user(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """returns active user if they are an org admin or super admin otherwise raises PermissionValidationError
    If no user is logged in, raises HTTPException 400"""
    if current_user.role not in [UserRoles.ORG_ADMIN, UserRoles.SUPER_ADMIN]:
        raise PermissionValidationError(
            "Method Requires `OrgAdmin` or `SuperAdmin` role"
        )

    return current_user


async def get_current_super_user(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    if current_user.role != UserRoles.SUPER_ADMIN:
        raise PermissionValidationError("Method Requires `SuperAdmin` role")

    return current_user
