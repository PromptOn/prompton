from tests.shared_test_data import (
    ORG1,
    ORG2,
    USER_BASIC,
    USER_ORG_ADMIN,
    USER_SUPER_ADMIN,
)
from tests.utils import TestSpecList


test_db_data = {"orgs": [ORG1, ORG2]}


test_specs_patch: TestSpecList = [
    {
        "spec_id": "all fields",
        "mock_user": USER_ORG_ADMIN,
        "input": {
            "id": str(ORG1["_id"]),
            "request_body": {
                "name": "Hoo Inc",
                "oauth_domain": "you.ai",
                "access_keys": {"ClosedAI": "666"},
            },
        },
        "expected": {
            **ORG1,
            "name": "Hoo Inc",
            "oauth_domain": "you.ai",
            "access_keys": {"openai_api_key": "**********", "ClosedAI": "**********"},
        },
        "expected_db": {
            **ORG1,
            "name": "Hoo Inc",
            "oauth_domain": "you.ai",
            "access_keys": {**ORG1["access_keys"], "ClosedAI": "666"},
        },
    },
    {
        "spec_id": "super admin other org",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": str(ORG2["_id"]), "request_body": {"name": "Hoo Inc"}},
        "expected": {**ORG2, "name": "Hoo Inc"},
    },
    #
    # Permission validations
    #
    {
        "spec_id": "OrgAdmin shouldn't update other org",
        "mock_user": USER_ORG_ADMIN,
        "input": {"id": str(ORG2["_id"]), "request_body": {"name": "Hoo Inc"}},
        "expected": 403,
    },
    {
        "spec_id": "BASIC shouldn't update own org",
        "mock_user": USER_BASIC,
        "input": {"id": str(ORG1["_id"]), "request_body": {"name": "Hoo Inc"}},
        "expected": 403,
    },
    #
    # Access keys updates
    #
    {
        "spec_id": "access_keys to None",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": str(ORG1["_id"]), "request_body": {"access_keys": None}},
        "expected": {**ORG1, "access_keys": None},
    },
    # Basic input validations
    #
    {
        "spec_id": "empty name field",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": str(ORG1["_id"]), "request_body": {"name": "  "}},
        "expected": 422,
    },
    {
        "spec_id": "invalid extra field",
        "mock_user": USER_SUPER_ADMIN,
        "input": {
            "id": str(ORG1["_id"]),
            "request_body": {"name": "foo", "foo": "moo"},
        },
        "expected": 422,
    },
    {
        "spec_id": "created_at non-editable",
        "mock_user": USER_SUPER_ADMIN,
        "input": {
            "id": str(ORG1["_id"]),
            "request_body": {"created_at": "2023-05-12T10:12:35", "name": "b"},
        },
        "expected": 422,
    },
    {
        "spec_id": "_id non-editable",
        "mock_user": USER_SUPER_ADMIN,
        "input": {
            "id": str(ORG1["_id"]),
            "request_body": {"_id": "ffffffffffffffffffffffff", "name": "blah"},
        },
        "expected": 422,
    },
    {
        "spec_id": "invalid access_keys",
        "mock_user": USER_SUPER_ADMIN,
        "input": {
            "id": str(ORG1["_id"]),
            "request_body": {
                "name": "name",
                "access_keys": "should be dict",
            },
        },
        "expected": 422,
    },
    {
        "spec_id": "None body",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": str(ORG1["_id"]), "request_body": None},
        "expected": 422,
    },
]
