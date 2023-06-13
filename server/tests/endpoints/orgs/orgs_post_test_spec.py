from tests.shared_test_data import (
    USER_BASIC,
    USER_ORG_ADMIN,
    USER_SUPER_ADMIN,
)
from tests.utils import TestSpecList


test_specs_post: TestSpecList = [
    {
        "spec_id": "all fields",
        "mock_user": USER_SUPER_ADMIN,
        "input": {
            "request_body": {
                "name": "  org name  ",
                "access_keys": {"OpenAI": "1234567890"},
            }
        },
        "expected": {
            "created_by_user_id": USER_SUPER_ADMIN["_id"],
            "created_by_org_id": USER_SUPER_ADMIN["org_id"],
            "name": "org name",
            "access_keys": {"OpenAI": "1234567890"},
        },
    },
    {
        "spec_id": "min fields",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {"name": "org x"}},
        "expected": {
            "created_by_user_id": USER_SUPER_ADMIN["_id"],
            "created_by_org_id": USER_SUPER_ADMIN["org_id"],
            "name": "org x",
            "access_keys": None,
        },
    },
    #
    # Permission validations
    #
    {
        "spec_id": "OrgAdmin shouldn't add",
        "mock_user": USER_ORG_ADMIN,
        "input": {"request_body": {"name": "org x"}},
        "expected": 403,
    },
    {
        "spec_id": "Basic shouldn't add",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"name": "org x"}},
        "expected": 403,
    },
    #
    # Basic input validations
    #
    {
        "spec_id": "empty name field",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {"name": "  "}},
        "expected": 422,
    },
    {
        "spec_id": "invalid extra field",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {"foo": "moo", "name": "blah"}},
        "expected": 422,
    },
    {
        "spec_id": "created_at non-editable",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {"created_at": "2023-05-12T10:12:35", "name": "b"}},
        "expected": 422,
    },
    {
        "spec_id": "_id non-editable",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {"_id": "ffffffffffffffffffffffff", "name": "blah"}},
        "expected": 422,
    },
    {
        "spec_id": "invalid access_keys",
        "mock_user": USER_SUPER_ADMIN,
        "input": {
            "request_body": {
                "name": "name",
                "access_keys": "should be dict",
            }
        },
        "expected": 422,
    },
    {
        "spec_id": "empty json",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": {}},
        "expected": 422,
    },
    {
        "spec_id": "empty string",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": ""},
        "expected": 422,
    },
    {
        "spec_id": "None",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"request_body": None},
        "expected": 422,
    },
]
