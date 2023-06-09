from tests.shared_test_data import (
    ORG1,
    ORG2,
    USER_BASIC,
    USER_ORG_ADMIN,
    USER_SUPER_ADMIN,
)
from tests.utils import TestSpecList, mask_access_keys


test_db_data = {"orgs": [ORG1, ORG2]}


test_specs_get: TestSpecList = [
    # list orgs
    {
        "spec_id": "SuperAdmin org list",
        "mock_user": USER_SUPER_ADMIN,
        "input": {},
        "expected": mask_access_keys(test_db_data["orgs"]),
        "expected_db": test_db_data["orgs"],
    },
    # get org by id
    {
        "spec_id": "basic user own org /me",
        "mock_user": USER_BASIC,
        "input": {"id": "me"},
        "expected": mask_access_keys(ORG1),
    },
    {
        "spec_id": "basic user own org",
        "mock_user": USER_BASIC,
        "input": {"id": str(ORG1["_id"])},
        "expected": mask_access_keys(ORG1),
    },
    {
        "spec_id": "OrgAdmin user own org",
        "mock_user": USER_ORG_ADMIN,
        "input": {"id": str(ORG1["_id"])},
        "expected": mask_access_keys(ORG1),
    },
    {
        "spec_id": "SuperAdmin user should get other org",
        "mock_user": USER_SUPER_ADMIN,
        "input": {"id": str(ORG2["_id"])},
        "expected": mask_access_keys(ORG2),
    },
    #
    #  Permission tests
    #
    {
        "spec_id": "OrgAdmins shouldn't list orgs",
        "mock_user": USER_ORG_ADMIN,
        "input": {},
        "expected": 403,
    },
    {
        "spec_id": "BasicUser shouldn't list orgs",
        "mock_user": USER_BASIC,
        "input": {},
        "expected": 403,
    },
    {
        "spec_id": "OrgAdmin shouldn't get other orgs",
        "mock_user": USER_ORG_ADMIN,
        "input": {"id": str(ORG2["_id"])},
        "expected": 404,
    },
    {
        "spec_id": "BasicUser shouldn't get other orgs",
        "mock_user": USER_BASIC,
        "input": {"id": str(ORG2["_id"])},
        "expected": 404,
    },
]
