from server.tests.shared_test_data import USER_BASIC
from server.tests.endpoints.prompts.prompts_test_records import (
    PROMPT_MIN_FIELDS,
    PROMPT_ARCHIVED_ORG2,
)
from server.tests.utils import TestSpecList


test_db_data = {"prompts": [PROMPT_MIN_FIELDS, PROMPT_ARCHIVED_ORG2]}

# TODO: test permissions: can only patch own org's prompts
test_specs_patch: TestSpecList = [
    {
        "spec_id": "all fields",
        "mock_user": USER_BASIC,
        "input": {
            "id": PROMPT_MIN_FIELDS["_id"],
            "request_body": {"status": "Archived", "name": "n", "description": "de"},
        },
        "expected": {
            **PROMPT_MIN_FIELDS,
            "status": "Archived",
            "name": "n",
            "description": "de",
        },
    },
    {
        "spec_id": "no description",
        "mock_user": USER_BASIC,
        "input": {
            "id": PROMPT_MIN_FIELDS["_id"],
            "request_body": {"description": None},
        },
        "expected": {**PROMPT_MIN_FIELDS, "description": None},
    },
    {
        "spec_id": "archive status",
        "mock_user": USER_BASIC,
        "input": {
            "id": PROMPT_MIN_FIELDS["_id"],
            "request_body": {"status": "Archived", "name": "archive item"},
        },
        "expected": {**PROMPT_MIN_FIELDS, "status": "Archived", "name": "archive item"},
    },
    {
        "spec_id": "no status",
        "mock_user": USER_BASIC,
        "input": {"id": PROMPT_MIN_FIELDS["_id"], "request_body": {"name": "no stat"}},
        "expected": {**PROMPT_MIN_FIELDS, "name": "no stat"},
    },
    #
    # Permission check
    #
    {
        "spec_id": "shouldn't update other org's prompt",
        "mock_user": USER_BASIC,
        "input": {
            "id": PROMPT_ARCHIVED_ORG2["_id"],
            "request_body": {"description": "x"},
        },
        "expected": 404,
    },
    #
    # Invalid requests
    #
    {
        "spec_id": "invalid status",
        "mock_user": USER_BASIC,
        "input": {"id": PROMPT_MIN_FIELDS["_id"], "request_body": {"status": "x"}},
        "expected": 422,
    },
    {
        "spec_id": "invalid extra field",
        "mock_user": USER_BASIC,
        "input": {
            "id": PROMPT_MIN_FIELDS["_id"],
            "request_body": {"foo": "x", "name": "x"},
        },
        "expected": 422,
    },
    {
        "spec_id": "created_at non-editable",
        "mock_user": USER_BASIC,
        "input": {
            "id": PROMPT_MIN_FIELDS["_id"],
            "request_body": {"created_at": "2023-05-12T10:12:35.995000", "name": "b"},
        },
        "expected": 422,
    },
    {
        "spec_id": "_id non-editable",
        "mock_user": USER_BASIC,
        "input": {
            "id": PROMPT_MIN_FIELDS["_id"],
            "request_body": {"_id": "foo", "name": "b"},
        },
        "expected": 422,
    },
    {
        "spec_id": "none name fielde",
        "mock_user": USER_BASIC,
        "input": {"id": PROMPT_MIN_FIELDS["_id"], "request_body": {"name": None}},
        "expected": 422,
    },
]
