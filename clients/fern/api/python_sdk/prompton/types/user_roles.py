# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class UserRoles(str, enum.Enum):
    """
    An enumeration.
    """

    BASIC = "Basic"
    PROMPT_ADMIN = "PromptAdmin"
    ORG_ADMIN = "OrgAdmin"
    SUPER_ADMIN = "SuperAdmin"

    def visit(
        self,
        basic: typing.Callable[[], T_Result],
        prompt_admin: typing.Callable[[], T_Result],
        org_admin: typing.Callable[[], T_Result],
        super_admin: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is UserRoles.BASIC:
            return basic()
        if self is UserRoles.PROMPT_ADMIN:
            return prompt_admin()
        if self is UserRoles.ORG_ADMIN:
            return org_admin()
        if self is UserRoles.SUPER_ADMIN:
            return super_admin()
