from tests.shared_test_data import USER_BASIC
from tests.utils import TestSpecList
from tests.endpoints.inferences.inference_test_records import (
    PROCESSED_INFERENCE,
    PROCESSED_INFERENCE_ORG2,
)

test_db_data = {"inferences": [PROCESSED_INFERENCE, PROCESSED_INFERENCE_ORG2]}


test_specs_post: TestSpecList = [
    {
        "spec_id": "all fields",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                "inference_id": str(PROCESSED_INFERENCE["_id"]),
                "end_user_id": "mrbean",
                "feedback_for_part": "scoring",
                "score": -1,
                "flag": "Inappropriate",
                "note": "this is a note",
                "metadata": {"meta1": "v1"},
            }
        },
        "expected": {
            "created_by_user_id": str(USER_BASIC["_id"]),
            "created_by_org_id": str(USER_BASIC["org_id"]),
            "end_user_id": "mrbean",
            "inference_id": str(PROCESSED_INFERENCE["_id"]),
            "prompt_version_id": str(PROCESSED_INFERENCE["prompt_version_id"]),
            "feedback_for_part": "scoring",
            "score": -1,
            "flag": "Inappropriate",
            "note": "this is a note",
            "metadata": {"meta1": "v1"},
        },
    },
    {
        "spec_id": "score only",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                "inference_id": str(PROCESSED_INFERENCE["_id"]),
                "score": -1,
            }
        },
        "expected": {
            "created_by_user_id": str(USER_BASIC["_id"]),
            "created_by_org_id": str(USER_BASIC["org_id"]),
            "end_user_id": None,
            "inference_id": str(PROCESSED_INFERENCE["_id"]),
            "prompt_version_id": str(PROCESSED_INFERENCE["prompt_version_id"]),
            "feedback_for_part": None,
            "score": -1,
            "flag": None,
            "note": None,
            "metadata": None,
        },
    },
    {
        "spec_id": "flag only",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                "inference_id": str(PROCESSED_INFERENCE["_id"]),
                "flag": "boring",
            }
        },
        "expected": {
            "created_by_user_id": str(USER_BASIC["_id"]),
            "created_by_org_id": str(USER_BASIC["org_id"]),
            "end_user_id": None,
            "inference_id": str(PROCESSED_INFERENCE["_id"]),
            "prompt_version_id": str(PROCESSED_INFERENCE["prompt_version_id"]),
            "feedback_for_part": None,
            "score": None,
            "flag": "boring",
            "note": None,
            "metadata": None,
        },
    },
    {
        "spec_id": "note only",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                "inference_id": str(PROCESSED_INFERENCE["_id"]),
                "note": "I like this",
            }
        },
        "expected": {
            "created_by_user_id": str(USER_BASIC["_id"]),
            "created_by_org_id": str(USER_BASIC["org_id"]),
            "end_user_id": None,
            "inference_id": str(PROCESSED_INFERENCE["_id"]),
            "prompt_version_id": str(PROCESSED_INFERENCE["prompt_version_id"]),
            "feedback_for_part": None,
            "score": None,
            "flag": None,
            "note": "I like this",
            "metadata": None,
        },
    },
    {
        "spec_id": "Non existent inference",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                "inference_id": "ffffffffffffffffffffffff",
                "score": -1,
            }
        },
        "expected": 404,
    },
    {
        "spec_id": "Other orgs inference",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                "inference_id": str(PROCESSED_INFERENCE_ORG2["_id"]),
                "score": -1,
            }
        },
        "expected": 404,
    },
    {
        "spec_id": "missing mandatory fields",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"inference_id": str(PROCESSED_INFERENCE["_id"])}},
        "expected": 422,
    },
]
