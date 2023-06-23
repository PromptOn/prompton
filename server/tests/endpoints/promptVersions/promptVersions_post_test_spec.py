from tests.endpoints.promptVersions.promptVersions_test_records import (
    PROMPT_WITH_1_VER,
    PROMPT_WITH_1_VER_ORG2,
)
from tests.shared_test_data import DEFAULT_MODEL_CONFIG, USER_BASIC
from tests.utils import TestSpecList

test_db_data = {"prompts": [PROMPT_WITH_1_VER, PROMPT_WITH_1_VER_ORG2]}

VALID_PROMPT_ID = str(PROMPT_WITH_1_VER["_id"])
VALID_TEMPLATE = {"role": "system", "content": "bla ${var}"}
VALID_CONFIG = {"model": "gpt-5"}

MIN_VALID = {"name": "n", "prompt_id": VALID_PROMPT_ID}

MIN_VALID_LIVE = {
    **MIN_VALID,
    "status": "Live",
    "template": [VALID_TEMPLATE],
    "model_config": VALID_CONFIG,
}

MIN_VALID_TESTING = {**MIN_VALID_LIVE, "status": "Testing"}

DRAFT_FULL_PROMPT_VER = {
    "status": "Draft",
    "name": "templ test 1",
    "description": "t1 desc",
    "prompt_id": VALID_PROMPT_ID,
    "provider": "OpenAI",
    "template": [{**VALID_TEMPLATE, "name": "me"}],
    "model_config": VALID_CONFIG,
}

EXPECTED_CREATED_BY = {
    "created_by_user_id": "aaaaaaaaaaaaaaaaaaaaaaa1",
    "created_by_org_id": "bbbbbbbbbbbbbbbbbbbbbbb1",
}

test_specs_post: TestSpecList = [
    {
        "spec_id": "draft all fields",
        "mock_user": USER_BASIC,
        "input": {"request_body": DRAFT_FULL_PROMPT_VER},
        "expected": {
            **DRAFT_FULL_PROMPT_VER,
            **EXPECTED_CREATED_BY,
            "model_config": {**DEFAULT_MODEL_CONFIG, **VALID_CONFIG},
            "template_arg_names": ["var"],
        },
    },
    {
        "spec_id": "draft min fields",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"name": "  t2 ", "prompt_id": VALID_PROMPT_ID}},
        "expected": {
            **EXPECTED_CREATED_BY,
            "status": "Draft",
            "name": "t2",
            "description": None,
            "prompt_id": VALID_PROMPT_ID,
            "provider": "OpenAI",
            "template": [],
            "model_config": None,
            "template_arg_names": [],
        },
    },
    {
        "spec_id": "Testing no model_config",
        "mock_user": USER_BASIC,
        "input": {"request_body": MIN_VALID_TESTING},
        "expected": {
            **EXPECTED_CREATED_BY,
            **MIN_VALID_TESTING,
            "provider": "OpenAI",
            "description": None,
            "template": [{**VALID_TEMPLATE, "name": None}],
            "model_config": {**DEFAULT_MODEL_CONFIG, **VALID_CONFIG},
            "template_arg_names": ["var"],
        },
    },
    {
        "spec_id": "Live",
        "mock_user": USER_BASIC,
        "input": {"request_body": MIN_VALID_LIVE},
        "expected": {
            **EXPECTED_CREATED_BY,
            **MIN_VALID_LIVE,
            "provider": "OpenAI",
            "description": None,
            "template": [{**VALID_TEMPLATE, "name": None}],
            "model_config": {**DEFAULT_MODEL_CONFIG, **VALID_CONFIG},
            "template_arg_names": ["var"],
        },
    },
    #
    # Permissions tests
    #
    {
        "spec_id": "shouldn't create prompt_version for other org's prompt",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {
                **DRAFT_FULL_PROMPT_VER,
                "prompt_id": PROMPT_WITH_1_VER_ORG2["_id"],
            }
        },
        "expected": 404,
    },
    #  requests validations
    #
    {
        "spec_id": "missing prompt_id field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {"name": "x"}},
        "expected": 422,
    },
    {
        "spec_id": "non existing prompt_id",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {**MIN_VALID, "prompt_id": "ffffffffffffffffffffffff"}
        },
        "expected": 404,
    },
    {
        "spec_id": "invalid prompt_id",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID, "prompt_id": "x"}},
        "expected": 422,
    },
    {
        "spec_id": "missing name field",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {**MIN_VALID, "name": None, "prompt_id": VALID_PROMPT_ID}
        },
        "expected": 422,
    },
    {
        "spec_id": "empty name field",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {**MIN_VALID, "name": "  ", "prompt_id": VALID_PROMPT_ID}
        },
        "expected": 422,
    },
    {
        "spec_id": "created_at non-editable",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID, "created_at": "2023-05-12T10:12:35"}},
        "expected": 422,
    },
    {
        "spec_id": "_id non-editable",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID, "_id": "ffffffffffffffffffffffff"}},
        "expected": 422,
    },
    {
        "spec_id": "model_config string",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID, "model_config": "x"}},
        "expected": 422,
    },
    {
        "spec_id": "invalid extra field",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID, "foo": "moo"}},
        "expected": 422,
    },
    {
        "spec_id": "invalid provider",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID, "provider": "ClosedAI"}},
        "expected": 422,
    },
    #
    # non draft Status validations
    #
    {
        "spec_id": "Live missing model",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {**MIN_VALID_LIVE, "model_config": {"temperature": 1}}
        },
        "expected": 422,
    },
    {
        "spec_id": "Live none model",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID_LIVE, "model_config": {"model": None}}},
        "expected": 422,
    },
    {
        "spec_id": "Live empty model",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID_LIVE, "model_config": {"model": ""}}},
        "expected": 422,
    },
    {
        "spec_id": "Live none template",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID_LIVE, "template": None}},
        "expected": 422,
    },
    {
        "spec_id": "Testing template update",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID_TESTING, "template": None}},
        "expected": 422,
    },
    #
    # Template validations
    #
    {
        "spec_id": "template missing role",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {**MIN_VALID, "template": [{"content": "x", "name": "y"}]}
        },
        "expected": 422,
    },
    {
        "spec_id": "template missing content",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {**MIN_VALID, "template": [{"role": "user", "name": "y"}]}
        },
        "expected": 422,
    },
    {
        "spec_id": "template invalid role",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {**MIN_VALID, "template": [{"role": "x", "content": "y"}]}
        },
        "expected": 422,
    },
    {
        "spec_id": "template extra field",
        "mock_user": USER_BASIC,
        "input": {
            "request_body": {**MIN_VALID, "template": [{**VALID_TEMPLATE, "foo": 1}]}
        },
        "expected": 422,
    },
    {
        "spec_id": "template empty array",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID, "template": []}},
        "expected": 422,
    },
    {
        "spec_id": "template empty json",
        "mock_user": USER_BASIC,
        "input": {"request_body": {**MIN_VALID, "template": [{}]}},
        "expected": 422,
    },
    #
    # generic edge cases
    #
    {
        "spec_id": "empty json",
        "mock_user": USER_BASIC,
        "input": {"request_body": {}},
        "expected": 422,
    },
    {
        "spec_id": "empty body",
        "mock_user": USER_BASIC,
        "input": {"request_body": ""},
        "expected": 422,
    },
    {
        "spec_id": "None body",
        "mock_user": USER_BASIC,
        "input": {"request_body": None},
        "expected": 422,
    },
]
