from typing import Any, Dict, List
from bson import ObjectId
import pytest

from server.tests.shared_test_data import (
    ORG1,
    ORG2,
    USER_BASIC,
    USER_ORG_ADMIN,
    USER_SUPER_ADMIN,
)
from server.tests.utils import TestSpecList

MIN_VALID: Dict[str, Any] = {
    "email": "x@y.z",
    "plain_password": "z",
    "org_id": ORG1["_id"],
}

test_db_data = {
    "orgs": [ORG1, ORG2],
    "users": [
        USER_BASIC,
        USER_ORG_ADMIN,
        USER_SUPER_ADMIN,
    ],
}

test_specs_post: TestSpecList = [
    {
        "spec_id": "all fields",
        "mock_user": USER_ORG_ADMIN,
        "input": {
            "request_body": {
                "email": " he+y@hoo.ai ",
                "disabled": False,
                "full_name": " hey ",
                "role": "Basic",
                "org_id": ORG1["_id"],
                "plain_password": "secret",
            }
        },
        "expected": {
            "email": "he+y@hoo.ai",
            "disabled": False,
            "full_name": "hey",
            "role": "Basic",
            "org_id": ORG1["_id"],
            "hashed_password": "monkeypatched_hashed_password",
            "created_by_user_id": USER_ORG_ADMIN["_id"],
            "created_by_org_id": USER_ORG_ADMIN["org_id"],
        },
    },
    {
        "spec_id": "min fields",
        "mock_user": USER_ORG_ADMIN,
        "input": {"request_body": MIN_VALID},
        "expected": {
            "email": "x@y.z",
            "disabled": False,
            "full_name": None,
            "role": "Basic",
            "org_id": ORG1["_id"],
            "hashed_password": "monkeypatched_hashed_password",
            "created_by_user_id": USER_ORG_ADMIN["_id"],
            "created_by_org_id": USER_ORG_ADMIN["org_id"],
        },
    },
    {
        "spec_id": "SuperAdmin should add non own org_id user",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {**MIN_VALID, "org_id": ORG2["_id"]}},
        "expected": {
            "email": "x@y.z",
            "disabled": False,
            "full_name": None,
            "role": "Basic",
            "org_id": ORG2["_id"],
            "hashed_password": "monkeypatched_hashed_password",
            "created_by_user_id": USER_SUPER_ADMIN["_id"],
            "created_by_org_id": USER_SUPER_ADMIN["org_id"],
        },
    },
    #
    # Permissions validations
    #
    {
        "spec_id": "Basic role shouldn't add user",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID, "org_id": ORG1["_id"]}},
        "expected": 403,
    },
    {
        "spec_id": "OrgAdmin shouldn't add non own org user",
        "mock_user": USER_ORG_ADMIN,
        "input": {"request_body": {**MIN_VALID, "org_id": ORG2["_id"]}},
        "expected": 403,
    },
    #
    # Data integrity validations
    #
    {
        "spec_id": "Non existent org_id",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {**MIN_VALID, "org_id": "ffffffffffffffffffffffff"}},
        "expected": 404,
    },
    {
        "spec_id": "Duplicate email",
        "mock_user": USER_ORG_ADMIN,
        "input": {"request_body": {**MIN_VALID, "email": " basic@me.ai "}},
        "expected": 422,
    },
    #
    # Format validations
    #
    {
        "spec_id": "empty email field",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {**MIN_VALID, "email": "  "}},
        "expected": 422,
    },
    {
        "spec_id": "malformed email",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {**MIN_VALID, "email": "x@za"}},
        "expected": 422,
    },
    {
        "spec_id": "no extra field",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {**MIN_VALID, "foo": "moo"}},
        "expected": 422,
    },
    {
        "spec_id": "malformed org_id",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {**MIN_VALID, "org_id": "malformed"}},
        "expected": 422,
    },
    {
        "spec_id": "created_at non-editable",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {**MIN_VALID, "created_at": "2023-05-12T10:12:35"}},
        "expected": 422,
    },
    {
        "spec_id": "_id non-editable",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {**MIN_VALID, "_id": "ffffffffffffffffffffffff"}},
        "expected": 422,
    },
    {
        "spec_id": "empty json body",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {}},
        "expected": 422,
    },
    {
        "spec_id": "empty string body",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": ""},
        "expected": 422,
    },
    {
        "spec_id": "None body",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": None},
        "expected": 422,
    },
]
