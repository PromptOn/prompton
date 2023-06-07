from server.tests.shared_test_data import (
    DEFAULT_MODEL_CONFIG,
    USER_BASIC,
    USER_BASIC_ORG2,
)
from server.tests.endpoints.promptVersions.promptVersions_test_records import (
    PROMPT_WITH_2_VER,
    PROMPT_WITH_1_VER,
    PROMPT_VER_LIVE,
    PROMPT_VER_ARCHIVED_ORG2,
    PROMPT_VER_DRAFT,
    PROMPT_VER_TESTING_EXTRA_FIELD,
    VALID_MODEL_CONFIG,
    VALID_TEMPLATE,
)
from server.tests.utils import TestSpecList


test_db_data = {
    "prompts": [PROMPT_WITH_1_VER, PROMPT_WITH_2_VER],
    "promptVersions": [
        PROMPT_VER_LIVE,
        PROMPT_VER_DRAFT,
        PROMPT_VER_TESTING_EXTRA_FIELD,
        PROMPT_VER_ARCHIVED_ORG2,
    ],
}

PV_DRAFT_ID = str(PROMPT_VER_DRAFT["_id"])

test_specs_patch: TestSpecList = [
    {
        "spec_id": "all fields on Draft",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_DRAFT["_id"]),
            "request_body": {
                "name": "  new name  ",  # note the leading and trailing spaces - it should stored trimmed
                "description": "hello",
                "provider": "OpenAI",
                "prompt_id": PROMPT_WITH_1_VER["_id"],
                "template": [{**VALID_TEMPLATE}],
                "model_config": {"temperature": 0.4},
            },
        },
        "expected": {
            **PROMPT_VER_DRAFT,
            "name": "new name",
            "description": "hello",
            "provider": "OpenAI",
            "prompt_id": PROMPT_WITH_1_VER["_id"],
            "template": [{**VALID_TEMPLATE}],
            "template_arg_names": ["var"],
            "model_config": {**DEFAULT_MODEL_CONFIG, "temperature": 0.4},
        },
        "expected_db": {
            **PROMPT_VER_DRAFT,
            "name": "new name",
            "description": "hello",
            "provider": "OpenAI",
            "prompt_id": PROMPT_WITH_1_VER["_id"],
            "template": [{**VALID_TEMPLATE}],
            "template_arg_names": ["var"],
            "model_config": {"temperature": 0.4},
        },
    },
    {
        "spec_id": "description on Live",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_LIVE["_id"]),
            "request_body": {"description": "hah"},
        },
        "expected": {**PROMPT_VER_LIVE, "description": "hah"},
    },
    {
        "spec_id": "Live to Archived",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_LIVE["_id"]),
            "request_body": {"status": "Archived"},
        },
        "expected": {**PROMPT_VER_LIVE, "status": "Archived"},
    },
    {
        "spec_id": "Draft to Live",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_DRAFT["_id"]),
            "request_body": {
                "status": "Live",
                "template": [{**VALID_TEMPLATE}],
                "model_config": VALID_MODEL_CONFIG,
            },
        },
        "expected": {
            **PROMPT_VER_DRAFT,
            "status": "Live",
            "template": [{**VALID_TEMPLATE}],
            "template_arg_names": ["var"],
            "model_config": {**DEFAULT_MODEL_CONFIG, **VALID_MODEL_CONFIG},
        },
        "expected_db": {
            **PROMPT_VER_DRAFT,
            "status": "Live",
            "template": [{**VALID_TEMPLATE}],
            "template_arg_names": ["var"],
            "model_config": {**VALID_MODEL_CONFIG},
        },
    },
    #
    # status change validations:
    {
        "spec_id": "no Live to Draft",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_LIVE["_id"]),
            "request_body": {"status": "Draft"},
        },
        "expected": 422,
    },
    {
        "spec_id": "no Testing to Draft",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_TESTING_EXTRA_FIELD["_id"]),
            "request_body": {"status": "Draft"},
        },
        "expected": 422,
    },
    {
        "spec_id": "no Archived to Draft",
        "mock_user": USER_BASIC_ORG2,
        "input": {
            "id": str(PROMPT_VER_ARCHIVED_ORG2["_id"]),
            "request_body": {"status": "Draft"},
        },
        "expected": 422,
    },
    {
        "spec_id": "Live need template",
        "mock_user": USER_BASIC,
        "input": {
            "id": PV_DRAFT_ID,
            "request_body": {"status": "Live", "template": None, "model": "GPT-4"},
        },
        "expected": 422,
    },
    {
        "spec_id": "Live need model",
        "mock_user": USER_BASIC,
        "input": {
            "id": PV_DRAFT_ID,
            "request_body": {"status": "Live", "model_config": {"model": None}},
        },
        "expected": 422,
    },
    #
    # non-draft model , model_config and template should be unmutable
    #
    {
        "spec_id": "Live no model update",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_LIVE["_id"]),
            "request_body": {"model": "GPT-5"},
        },
        "expected": 422,
    },
    {
        "spec_id": "Live no model_config update",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_LIVE["_id"]),
            "request_body": {"model_config": VALID_MODEL_CONFIG},
        },
        "expected": 422,
    },
    {
        "spec_id": "Live no model_config None",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_LIVE["_id"]),
            "request_body": {"model_config": None},
        },
        "expected": 422,
    },
    {
        "spec_id": "Live no template update",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_LIVE["_id"]),
            "request_body": {"template": [VALID_TEMPLATE]},
        },
        "expected": 422,
    },
    {
        "spec_id": "Live no prompt_id update",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_LIVE["_id"]),
            "request_body": {"prompt_id": PROMPT_WITH_2_VER["_id"]},
        },
        "expected": 422,
    },
    {
        "spec_id": "Live no name update",
        "mock_user": USER_BASIC,
        "input": {"id": str(PROMPT_VER_LIVE["_id"]), "request_body": {"name": "oi"}},
        "expected": 422,
    },
    #
    # Archived and Testing should have the same restrictions as Live, testing only template update:
    #
    {
        "spec_id": "Archived no template update",
        "mock_user": USER_BASIC_ORG2,
        "input": {
            "id": str(PROMPT_VER_ARCHIVED_ORG2["_id"]),
            "request_body": {"template": [VALID_TEMPLATE]},
        },
        "expected": 422,
    },
    {
        "spec_id": "Testing no template update",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_TESTING_EXTRA_FIELD["_id"]),
            "request_body": {"template": [VALID_TEMPLATE]},
        },
        "expected": 422,
    },
    #
    #  permissions test
    #
    {
        "spec_id": "shouldn't update other org's prompt_version",
        "mock_user": USER_BASIC,
        "input": {
            "id": str(PROMPT_VER_ARCHIVED_ORG2["_id"]),
            "request_body": {"description": "x"},
        },
        "expected": 404,
    },
    #
    #  test basic validations:
    #
    {
        "spec_id": "invalid prompt_id",
        "mock_user": USER_BASIC,
        "input": {"id": PV_DRAFT_ID, "request_body": {"prompt_id": "invalid"}},
        "expected": 422,
    },
    {
        "spec_id": "non existent prompt_id",
        "mock_user": USER_BASIC,
        "input": {
            "id": PV_DRAFT_ID,
            "request_body": {"prompt_id": "ffffffffffffffffffffffff"},
        },
        "expected": 404,
    },
    {
        "spec_id": "invalid status",
        "mock_user": USER_BASIC,
        "input": {"id": PV_DRAFT_ID, "request_body": {"status": "foo", "name": "blah"}},
        "expected": 422,
    },
    {
        "spec_id": "invalid extra field",
        "mock_user": USER_BASIC,
        "input": {"id": PV_DRAFT_ID, "request_body": {"foo": "moo", "name": "blah"}},
        "expected": 422,
    },
    {
        "spec_id": "empty name",
        "mock_user": USER_BASIC,
        "input": {"id": PV_DRAFT_ID, "request_body": {"name": ""}},
        "expected": 422,
    },
    {
        "spec_id": "name only whitespaces",
        "mock_user": USER_BASIC,
        "input": {"id": PV_DRAFT_ID, "request_body": {"name": " \t \n "}},
        "expected": 422,
    },
    {
        "spec_id": "created_at non-editable",
        "mock_user": USER_BASIC,
        "input": {
            "id": PV_DRAFT_ID,
            "request_body": {"created_at": "2023-05-12T10:12:35.995000", "name": "b"},
        },
        "expected": 422,
    },
    {
        "spec_id": "_id non-editable",
        "mock_user": USER_BASIC,
        "input": {"id": PV_DRAFT_ID, "request_body": {"_id": "foo", "name": "blah"}},
        "expected": 422,
    },
    {
        "spec_id": "Template need one msg",
        "mock_user": USER_BASIC,
        "input": {"id": PV_DRAFT_ID, "request_body": {"template": []}},
        "expected": 422,
    },
    {
        "spec_id": "Invalid model_config",
        "mock_user": USER_BASIC,
        "input": {"id": PV_DRAFT_ID, "request_body": {"model_config": {"foo": "bar"}}},
        "expected": 422,
    },
]
