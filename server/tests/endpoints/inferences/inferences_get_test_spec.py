from tests.endpoints.inferences.inference_test_records import (
    ERROR_INFERENCE,
    PROCESSED_INFERENCE,
    PROCESSED_INFERENCE_ORG2,
    PROMPT_ID1,
    PROMPT_ID2,
    PROMPT_VERSION_ID1,
    PROMPT_VERSION_ID2,
    TIMEOUT_INFERENCE,
)
from tests.shared_test_data import (
    USER_BASIC,
    USER_ORG_ADMIN,
    USER_SUPER_ADMIN,
)
from tests.utils import TestSpecList, MockDBData, remove_props

inferences_get_test_db: MockDBData = {
    "inferences": [
        PROCESSED_INFERENCE,
        ERROR_INFERENCE,
        TIMEOUT_INFERENCE,
        PROCESSED_INFERENCE_ORG2,
    ]
}

org1_inferences = [
    PROCESSED_INFERENCE,
    ERROR_INFERENCE,
    TIMEOUT_INFERENCE,
]
org2_inferences = [PROCESSED_INFERENCE_ORG2]


test_spec_get: TestSpecList = [
    #
    # list inferences no filter / filter by prompt_id / filter by prompt_version_id
    #
    {
        "spec_id": "SuperAdmin should list all inferences",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"params": {}},
        "expected": remove_props(org1_inferences, "extra_field") + org2_inferences,
    },
    {
        "spec_id": "Basic user should only list own org inferences",
        "mock_user": USER_BASIC,
        "input": {"params": {}},
        "expected": remove_props(org1_inferences, "extra_field"),
    },
    {
        "spec_id": "filter by prompt_id 0 res",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_id": "ffffffffffffffffffffffff"}},
        "expected": [],
    },
    {
        "spec_id": "filter by prompt_id 1 res",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_id": PROMPT_ID1}},
        "expected": [PROCESSED_INFERENCE],
    },
    {
        "spec_id": "filter by prompt_id 2 res",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_id": PROMPT_ID2}},
        "expected": [remove_props(ERROR_INFERENCE, "extra_field"), TIMEOUT_INFERENCE],
    },
    {
        "spec_id": "filter by prompt_version_id 0 res",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_version_id": "ffffffffffffffffffffffff"}},
        "expected": [],
    },
    {
        "spec_id": "filter by prompt_version_id 1 res",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_version_id": PROMPT_VERSION_ID1}},
        "expected": [PROCESSED_INFERENCE],
    },
    {
        "spec_id": "filter by prompt_version_id 2 res",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_version_id": PROMPT_VERSION_ID2}},
        "expected": [remove_props(ERROR_INFERENCE, "extra_field"), TIMEOUT_INFERENCE],
    },
    #
    # Get inference by inference id
    #
    {
        "spec_id": "get Processed inference by id",
        "mock_user": USER_BASIC,
        "input": {"id": str(PROCESSED_INFERENCE["_id"])},
        "expected": PROCESSED_INFERENCE,
    },
    {
        "spec_id": "get TimeOut inference by id",
        "mock_user": USER_BASIC,
        "input": {"id": str(TIMEOUT_INFERENCE["_id"])},
        "expected": TIMEOUT_INFERENCE,
    },
    {
        "spec_id": "get Error inference by id",
        "mock_user": USER_BASIC,
        "input": {"id": str(ERROR_INFERENCE["_id"])},
        "expected": remove_props(ERROR_INFERENCE, "extra_field"),
    },
    #
    #  Permission tests
    #
    {
        "spec_id": "OrgAdmin shouldn't get other orgs",
        "mock_user": USER_ORG_ADMIN,
        "input": {"id": str(PROCESSED_INFERENCE_ORG2["_id"])},
        "expected": 404,
    },
    {
        "spec_id": "BasicUser shouldn't get other orgs",
        "mock_user": USER_BASIC,
        "input": {"id": str(PROCESSED_INFERENCE_ORG2["_id"])},
        "expected": 404,
    },
    #
    # Invalid requests
    #
    {
        "spec_id": "malformed prompt_id",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_id": "xxx"}},
        "expected": 422,
    },
    {
        "spec_id": "malformed prompt_version_id",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_version_id": "xx"}},
        "expected": 422,
    },
    {
        "spec_id": "both prompt_version_id & prompt_id",
        "mock_user": USER_BASIC,
        "input": {
            "params": {
                "prompt_id": PROMPT_ID1,
                "prompt_version_id": PROMPT_VERSION_ID1,
            },
        },
        "expected": 400,
    },
]
