from bson import ObjectId

from tests.shared_test_data import USER_BASIC
from tests.utils import TestSpecList


test_specs_post: TestSpecList = [
    {
        "spec_id": "all fields",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                "status": "Active",
                "name": "  all fields  ",
                "description": "descri",
            }
        },
        "expected": {
            "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
            "created_by_org_id": ObjectId("bbbbbbbbbbbbbbbbbbbbbbb1"),
            "status": "Active",
            "name": "all fields",
            "description": "descri",
        },
    },
    {
        "spec_id": "no description",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"status": "Active", "name": "no description"}},
        "expected": {
            "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
            "created_by_org_id": ObjectId("bbbbbbbbbbbbbbbbbbbbbbb1"),
            "status": "Active",
            "name": "no description",
            "description": None,
        },
    },
    {
        "spec_id": "archive status",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"status": "Archived", "name": "archive item"}},
        "expected": {
            "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
            "created_by_org_id": ObjectId("bbbbbbbbbbbbbbbbbbbbbbb1"),
            "status": "Archived",
            "name": "archive item",
            "description": None,
        },
    },
    {
        "spec_id": "no status",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"name": "no status item"}},
        "expected": {
            "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
            "created_by_org_id": ObjectId("bbbbbbbbbbbbbbbbbbbbbbb1"),
            "status": "Active",
            "name": "no status item",
            "description": None,
        },
    },
    #
    # Invalid requests
    #
    {
        "spec_id": "invalid status",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"status": "foo", "name": "blah"}},
        "expected": 422,
    },
    {
        "spec_id": "missing name field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"status": "Active"}},
        "expected": 422,
    },
    {
        "spec_id": "none name field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"status": "Active", "name": None}},
        "expected": 422,
    },
    {
        "spec_id": "empty name field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"name": "  "}},
        "expected": 422,
    },
    {
        "spec_id": "invalid extra field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"foo": "moo", "name": "blah"}},
        "expected": 422,
    },
    {
        "spec_id": "created_at non-editable",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"created_at": "2023-05-12T10:12:35", "name": "b"}},
        "expected": 422,
    },
    {
        "spec_id": "_id non-editable",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"_id": "ffffffffffffffffffffffff", "name": "blah"}},
        "expected": 422,
    },
    {
        "spec_id": "empty json",
        "mock_user": USER_BASIC,
        "input": {"request_body": {}},
        "expected": 422,
    },
    {
        "spec_id": "empty string",
        "mock_user": USER_BASIC,
        "input": {"request_body": ""},
        "expected": 422,
    },
    {
        "spec_id": "None",
        "mock_user": USER_BASIC,
        "input": {"request_body": None},
        "expected": 422,
    },
]
