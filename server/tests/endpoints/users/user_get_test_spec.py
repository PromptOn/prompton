import copy
import json
from typing import Any, Dict, List

from bson import ObjectId
from tests.shared_test_data import (
    ORG_ID2,
    USER_BASIC,
    USER_ORG_ADMIN,
    USER_SUPER_ADMIN,
)
from tests.utils import TestSpecList, remove_props

DB_DEFAULTS = {
    "disabled": False,
    "full_name": None,
    "created_at": "2023-05-15T15:46:02.051309",
}

U_MISSING_FIELDS = {**DB_DEFAULTS, **USER_BASIC}

U_ALL_FIELDS: Dict[str, Any] = {
    **DB_DEFAULTS,
    **USER_BASIC,
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaa01"),
    "email": "all@field.ai",
    "full_name": "hey",
}

U_INVALID_EMAIL: Dict[str, Any] = {
    **DB_DEFAULTS,
    **USER_BASIC,
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaa05"),
    "email": "invalid email format",
}


U_EXTRA_FIELD: Dict[str, Any] = {
    **DB_DEFAULTS,
    **USER_BASIC,
    "email": "extra@field.ai",
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaa11"),
    "extra_field": "extra",
}

U_ORG2: Dict[str, Any] = {
    **DB_DEFAULTS,
    **USER_BASIC,
    "org_id": ORG_ID2,
    "email": "org2@field.ai",
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaa13"),
    "extra_field": "extra",
}


test_db_data = {
    "users": [U_ALL_FIELDS, U_MISSING_FIELDS, U_EXTRA_FIELD, U_INVALID_EMAIL, U_ORG2],
}


#  hashed password and any extra fields should not be returned (UserRead class has Extra.ignore set for this)
org1_users = remove_props(
    [U_ALL_FIELDS, U_MISSING_FIELDS, U_EXTRA_FIELD, U_INVALID_EMAIL],
    ["hashed_password", "extra_field"],
)
org2_users = remove_props([U_ORG2], ["hashed_password", "extra_field"])


test_specs_get: TestSpecList = [
    #
    # get user list
    #
    {
        "spec_id": "SuperAdmin should list all users",
        "mock_user": USER_SUPER_ADMIN,
        "input": {},
        "expected": org1_users + org2_users,
    },
    {
        "spec_id": "OrgAdmin should list their org's users",
        "mock_user": USER_ORG_ADMIN,
        "input": {},
        "expected": org1_users,
    },
    {
        "spec_id": "Basic should  list their own org's users",
        "mock_user": USER_BASIC,
        "input": {},
        "expected": org1_users,
    },
    #
    # get user by id
    #
    {
        "spec_id": "Basic should get other user in own org",
        "mock_user": USER_BASIC,
        "input": {"id": U_ALL_FIELDS["_id"]},
        "expected": remove_props(U_ALL_FIELDS, "hashed_password"),
    },
    {
        "spec_id": "OrgAdmin should get their org's user",
        "mock_user": USER_ORG_ADMIN,
        "input": {"id": U_ALL_FIELDS["_id"]},
        "expected": remove_props(U_ALL_FIELDS, "hashed_password"),
    },
    {
        "spec_id": "SuperAdmin should get any org's user (+missing fields)",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": str(U_MISSING_FIELDS["_id"])},
        "expected": remove_props(U_MISSING_FIELDS, "hashed_password"),
    },
    {
        "spec_id": "should read stored invalid email",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": U_INVALID_EMAIL["_id"]},
        "expected": remove_props(U_INVALID_EMAIL, "hashed_password"),
    },
    {
        "spec_id": "Basic should read themselves by id",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": U_ALL_FIELDS["_id"]},
        "expected": remove_props(U_ALL_FIELDS, "hashed_password"),
    },
    {
        "spec_id": "Basic should get themselves by /me",
        "mock_user": U_ALL_FIELDS,
        "input": {"id": "me"},
        "expected": remove_props(U_ALL_FIELDS, "hashed_password"),
    },
    {
        "spec_id": "should not return password hash",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": U_EXTRA_FIELD["_id"]},
        "expected": remove_props(U_EXTRA_FIELD, ["hashed_password", "extra_field"]),
    },
    #
    # permissions tests
    #
    {
        "spec_id": "OrgAdmin should not get user in other org",
        "mock_user": USER_ORG_ADMIN,
        "input": {"id": U_ORG2["_id"]},
        "expected": 404,
    },
    {
        "spec_id": "Basic should not get user in other org",
        "mock_user": USER_BASIC,
        "input": {"id": U_ORG2["_id"]},
        "expected": 404,
    },
]
