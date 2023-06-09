from tests.endpoints.prompts.prompts_test_records import (
    PROMPT_ALL_FIELDS,
    PROMPT_MIN_FIELDS,
    PROMPT_ARCHIVED_ORG2,
    PROMPT_EXTRA_FIELD,
)
from tests.shared_test_data import (
    USER_BASIC,
    USER_ORG_ADMIN,
    USER_SUPER_ADMIN,
)
from tests.utils import MockDBData, TestSpecList, remove_props

test_db_data = {
    "prompts": [
        PROMPT_ALL_FIELDS,
        PROMPT_MIN_FIELDS,
        PROMPT_ARCHIVED_ORG2,
        PROMPT_EXTRA_FIELD,
    ],
}

org1_prompts = [
    PROMPT_ALL_FIELDS,
    PROMPT_MIN_FIELDS,
    remove_props(PROMPT_EXTRA_FIELD, "extra_field"),
]


test_specs_get: TestSpecList = [
    #
    # list prompts
    #
    {
        "spec_id": "Basic user should list own org prompts ",
        "mock_user": USER_BASIC,
        "input": {},
        "expected": org1_prompts,
    },
    {
        "spec_id": "SuperAdmin should list all org prompts ",
        "mock_user": USER_SUPER_ADMIN,
        "input": {},
        "expected": org1_prompts + [PROMPT_ARCHIVED_ORG2],
    },
    #
    # get prompt by id
    #
    {
        "spec_id": "Basic user get (all fields)",
        "mock_user": USER_BASIC,
        "input": {"id": PROMPT_ALL_FIELDS["_id"]},
        "expected": PROMPT_ALL_FIELDS,
    },
    {
        "spec_id": "Basic user get (min fields))",
        "mock_user": USER_BASIC,
        "input": {"id": str(PROMPT_MIN_FIELDS["_id"])},
        "expected": PROMPT_MIN_FIELDS,
    },
    {
        "spec_id": "Basic user get (extra field)",
        "mock_user": USER_BASIC,
        "input": {"id": PROMPT_EXTRA_FIELD["_id"]},
        "expected": remove_props(PROMPT_EXTRA_FIELD, "extra_field"),
    },
    {
        "spec_id": "SuperAdmin should get other org's",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": PROMPT_ARCHIVED_ORG2["_id"]},
        "expected": PROMPT_ARCHIVED_ORG2,
    },
    #
    #  Permission tests
    #
    {
        "spec_id": "Basic shouldn't get other org's",
        "mock_user": USER_BASIC,
        "input": {"id": PROMPT_ARCHIVED_ORG2["_id"]},
        "expected": 404,
    },
    {
        "spec_id": "OrgAdmin shouldn't get other org's",
        "mock_user": USER_ORG_ADMIN,
        "input": {"id": PROMPT_ARCHIVED_ORG2["_id"]},
        "expected": 404,
    },
]
