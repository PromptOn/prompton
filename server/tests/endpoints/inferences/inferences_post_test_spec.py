from bson import ObjectId
import openai
from server.tests.conftest_mock_openai import mock_completition_data
from server.tests.endpoints.inferences.inference_test_records import (
    DRAFT_PROMPT_VERSION_DB,
    LIVE_PROMPT_VERSION_DB,
    PROMPT_ID1,
    VALID_TEMPLATE,
)

from server.tests.shared_test_data import (
    DEFAULT_RAW_COMPLETITION_REQUEST,
    ORG1,
    USER_BASIC,
    USER_SUPER_ADMIN,
)
from server.tests.utils import TestInput, TestSpecList


FILLED_TEMPLATE = {
    "role": "system",
    "content": "a1: v1 a2: v2",
    "name": None,
}

VALID_REQ = {
    "prompt_version_id": str(LIVE_PROMPT_VERSION_DB["_id"]),
    "endUserId": "u1",
    "source": "source1",
}

ORG2_NO_ACCESS_KEYS = {
    **ORG1,
    "_id": ObjectId("bbbbbbbbbbbbbbbbbbbbbbbf"),
    "name": "org2",
    "access_keys": None,
}

USER_BASIC_ORG2_NO_ACCESS_KEY = {
    **USER_BASIC,
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaaf"),
    "email": "noaccesskey@x.ai",
    "org_id": ORG2_NO_ACCESS_KEYS["_id"],
}

LIVE_PROMPT_VERSION_DB_ORG2 = {
    **LIVE_PROMPT_VERSION_DB,
    "_id": ObjectId("cccccccccccccccccccccccf"),
    "created_by_org_id": ORG2_NO_ACCESS_KEYS["_id"],
}

test_db_data = {
    "users": [USER_BASIC, USER_BASIC_ORG2_NO_ACCESS_KEY],
    "orgs": [ORG1, ORG2_NO_ACCESS_KEYS],
    "promptVersions": [
        LIVE_PROMPT_VERSION_DB,
        DRAFT_PROMPT_VERSION_DB,
        LIVE_PROMPT_VERSION_DB_ORG2,
    ],
}

min_input: TestInput = {
    "request_body": {
        "prompt_version_id": str(LIVE_PROMPT_VERSION_DB["_id"]),
        "endUserId": "u1",
        "source": "s1",
    }
}

all_input: TestInput = {
    "request_body": {
        "prompt_version_id": str(LIVE_PROMPT_VERSION_DB["_id"]),
        "endUserId": "u1",
        "source": "s1",
        "request_timeout": 120.1,
        "template_args": {"arg1": "v1", "arg2": "v2"},
        "metadata": {"meta1": "m1"},
    }
}


expected_all_fields_head = {
    "created_by_user_id": USER_BASIC["_id"],
    "created_by_org_id": ORG1["_id"],
    "endUserId": "u1",
    "source": "s1",
    "template_args": {"arg1": "v1", "arg2": "v2"},
    "metadata": {"meta1": "m1"},
    "prompt_id": PROMPT_ID1,
    "prompt_version_id": LIVE_PROMPT_VERSION_DB["_id"],
    "prompt_version_name": "prompt v1",
    "status": "Processed",
    "metadata": {"meta1": "m1"},
    "request_timeout": 120.1,
    "request": {
        "provider": "OpenAI",
        "raw_request": {
            **DEFAULT_RAW_COMPLETITION_REQUEST,  # type: ignore[arg-type]
            **LIVE_PROMPT_VERSION_DB["model_config"],
            "messages": [FILLED_TEMPLATE],
            "user": "u1",
        },
    },
}

expected_min_fields_head = {
    "created_by_user_id": USER_BASIC["_id"],
    "created_by_org_id": ORG1["_id"],
    "endUserId": "u1",
    "source": "s1",
    "template_args": None,
    "metadata": None,
    "prompt_id": PROMPT_ID1,
    "prompt_version_id": LIVE_PROMPT_VERSION_DB["_id"],
    "prompt_version_name": "prompt v1",
    "status": "Processed",
    "metadata": None,
    "request_timeout": None,
    "request": {
        "provider": "OpenAI",
        "raw_request": {
            **DEFAULT_RAW_COMPLETITION_REQUEST,  # type: ignore[arg-type]
            **LIVE_PROMPT_VERSION_DB["model_config"],
            "messages": [VALID_TEMPLATE],
            "user": "u1",
        },
    },
}


test_specs_post: TestSpecList = [
    {
        "spec_id": "all input params",
        "mock_user": USER_BASIC,
        "input": all_input,
        "expected": {
            **expected_all_fields_head,
            "response": {
                "isError": False,
                "completition_duration_seconds": 6.6,  # value ignored in tests
                "is_client_connected_at_finish": True,
                "first_message": {"name": None, **mock_completition_data["choices"][0]["message"]},  # type: ignore[index]
                "token_usage": mock_completition_data["usage"],
                "raw_response": mock_completition_data,
            },
        },
    },
    {
        "spec_id": "min input params",
        "mock_user": USER_BASIC,
        "input": min_input,
        "expected": {
            **expected_min_fields_head,
            "response": {
                "isError": False,
                "completition_duration_seconds": 6.6,  # value ignored in tests
                "is_client_connected_at_finish": True,
                "first_message": {"name": None, **mock_completition_data["choices"][0]["message"]},  # type: ignore[index]
                "token_usage": mock_completition_data["usage"],
                "raw_response": mock_completition_data,
            },
        },
    },
    #
    # Permission tests
    #
    {
        "spec_id": "user shouldn't inference other orgs promptversion",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                "prompt_version_id": str(LIVE_PROMPT_VERSION_DB_ORG2["_id"]),
                "endUserId": "u1",
                "source": "s1",
            }
        },
        "expected": 404,
    },
    #  request  validations
    #
    {
        "spec_id": "no org token",
        "mock_user": USER_BASIC_ORG2_NO_ACCESS_KEY,
        "input": {
            "request_body": {
                "prompt_version_id": str(LIVE_PROMPT_VERSION_DB_ORG2["_id"]),
                "endUserId": "u1",
                "source": "s1",
            }
        },
        "expected": 400,
    },
    {
        "spec_id": "invalid prompt_version_id",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**VALID_REQ, "prompt_version_id": "xxxx"}},
        "expected": 422,
    },
    {
        "spec_id": "non existent prompt_version_id",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                **VALID_REQ,
                "prompt_version_id": ObjectId("ffffffffffffffffffffffff"),
            }
        },
        "expected": 404,
    },
    {
        "spec_id": "should not inference on draft promptVersion",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                **VALID_REQ,
                "prompt_version_id": str(DRAFT_PROMPT_VERSION_DB["_id"]),
            }
        },
        "expected": 422,
    },
    {
        "spec_id": "empty source field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**VALID_REQ, "source": " "}},
        "expected": 422,
    },
    {
        "spec_id": "None source field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**VALID_REQ, "source": None}},
        "expected": 422,
    },
    {
        "spec_id": "empty endUserId field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**VALID_REQ, "endUserId": " "}},
        "expected": 422,
    },
    {
        "spec_id": "None endUserId field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**VALID_REQ, "endUserId": None}},
        "expected": 422,
    },
    {
        "spec_id": "invalid extra field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**VALID_REQ, "foo": "moo"}},
        "expected": 422,
    },
]

post_openai_error_test_specs: TestSpecList = [
    {
        "spec_id": "mock openai apiError",
        "mock_user": USER_BASIC,
        "input": all_input,
        "mock_exception": openai.APIError("mocked error"),
        "expected": {
            "detail": {
                "message": "OpenAI API Error",
                "openAI_error_class": "openai.error.APIError",
                "openAI_message": "mocked error",
                "openAI_error": None,
            }
        },
        "expected_db": {
            **expected_all_fields_head,
            "status": "CompletitionError",
            "response": {
                "isError": True,
                "completition_duration_seconds": 6.6,
                "is_client_connected_at_finish": True,
                "error": {
                    "error_class": "openai.error.APIError",
                    "error": None,
                    "message": "mocked error",
                },
            },
        },
    },
    {
        "spec_id": "mock openai timeout",
        "mock_user": USER_BASIC,
        "input": min_input,
        "mock_exception": openai.error.Timeout(  # pyright: ignore[reportGeneralTypeIssues]
            "mocked timeout"
        ),
        "expected": {
            "detail": {
                "message": "OpenAI API Timeout Error",
                "openAI_error_class": "openai.error.Timeout",
                "openAI_message": "mocked timeout",
                "openAI_error": None,
            }
        },
        "expected_db": {
            **expected_min_fields_head,
            "status": "CompletitionTimeout",
            "response": {
                "isError": True,
                "completition_duration_seconds": 6.6,  # value ignored in tests
                "is_client_connected_at_finish": True,
                "error": {
                    "error_class": "openai.error.Timeout",
                    "error": None,
                    "message": "mocked timeout",
                },
            },
        },
    },
]
