from tests.shared_test_data import (
    USER_BASIC,
    USER_ORG_ADMIN,
    USER_SUPER_ADMIN,
)
from tests.endpoints.promptVersions.promptVersions_test_records import (
    PROMPT_WITH_2_VER,
    PROMPT_WITH_1_VER,
    PROMPT_VER_LIVE,
    PROMPT_VER_DRAFT,
    PROMPT_VER_TESTING_EXTRA_FIELD,
    PROMPT_VER_ARCHIVED_ORG2,
)
from tests.utils import TestSpecList, remove_props


test_db_data = {
    "prompts": [PROMPT_WITH_2_VER, PROMPT_WITH_1_VER],
    "promptVersions": [
        PROMPT_VER_LIVE,
        PROMPT_VER_DRAFT,
        PROMPT_VER_TESTING_EXTRA_FIELD,
        PROMPT_VER_ARCHIVED_ORG2,
    ],
}

prompt_vers_org1 = [
    PROMPT_VER_LIVE,
    PROMPT_VER_DRAFT,
    remove_props(PROMPT_VER_TESTING_EXTRA_FIELD, "extra_field"),
]


promptVersions_get_test_spec: TestSpecList = [
    #
    # list & promptVersions
    #
    {
        "spec_id": "Basic list no filter should show own org only",
        "mock_user": USER_BASIC,
        "input": {},
        "expected": prompt_vers_org1,
    },
    {
        "spec_id": "Basic user list filter by prompt_id 2 res",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_id": PROMPT_WITH_2_VER["_id"]}},
        "expected": [
            PROMPT_VER_LIVE,
            remove_props(PROMPT_VER_TESTING_EXTRA_FIELD, "extra_field"),
        ],
    },
    {
        "spec_id": "Basic list filter by prompt_id 0 res",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_id": PROMPT_VER_ARCHIVED_ORG2["_id"]}},
        "expected": [],
    },
    {
        "spec_id": "SuperAdmin should list all orgs'",
        "mock_user": USER_SUPER_ADMIN,
        "input": {},
        "expected": prompt_vers_org1 + [PROMPT_VER_ARCHIVED_ORG2],
    },
    #
    # get promptVersions by id
    #
    {
        "spec_id": "Super Admin get by id other org",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": PROMPT_VER_LIVE["_id"]},
        "expected": PROMPT_VER_LIVE,
    },
    {
        "spec_id": "Basic get by id own org",
        "mock_user": USER_BASIC,
        "input": {"id": PROMPT_VER_DRAFT["_id"]},
        "expected": PROMPT_VER_DRAFT,
    },
    #
    #  Permission tests
    #
    {
        "spec_id": "Basic shouldn't get other org's",
        "mock_user": USER_BASIC,
        "input": {"id": PROMPT_VER_ARCHIVED_ORG2["_id"]},
        "expected": 404,
    },
    {
        "spec_id": "OrgAdmin shouldn't get other org's",
        "mock_user": USER_ORG_ADMIN,
        "input": {"id": PROMPT_VER_ARCHIVED_ORG2["_id"]},
        "expected": 404,
    },
    #
    # Invalid requests
    #
    {
        "spec_id": "malformed prompt_id",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"params": {"prompt_id": "xxx"}},
        "expected": 422,
    },
]
