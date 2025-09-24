from bson import ObjectId
from tests.shared_test_data import USER_BASIC, USER_ORG_ADMIN, USER_BASIC_ORG2
from tests.utils import TestSpecList, remove_props

INF_ID1 = ObjectId("aa0000000000000000000000")
INF_ID2 = ObjectId("aa0000000000000000000001")

PV_ID1 = ObjectId("bb0000000000000000000000")
PV_ID2 = ObjectId("bb0000000000000000000001")

FEEDBACK_MIN_FIELDS = {
    "_id": ObjectId("000000000000000000000000"),
    "created_at": "2023-06-23T11:09:02.187618",
    "created_by_user_id": USER_BASIC["_id"],
    "created_by_org_id": USER_BASIC["org_id"],
    "inference_id": INF_ID1,
    "prompt_version_id": PV_ID1,
    "score": 1,
    "flag": None,
    "end_user_id": None,
    "feedback_for_part": None,
    "note": None,
    "metadata": None,
}

FEEDBACK_ALL_FIELDS = {
    **FEEDBACK_MIN_FIELDS,
    "_id": ObjectId("000000000000000000000001"),
    "flag": "flag",
    "note": "note",
    "end_user_id": "mrbean",
    "feedback_for_part": "scoring",
    "metadata": {"meta1": "v1"},
}


FEEDBACK_EXTRA_FIELD = {
    **FEEDBACK_MIN_FIELDS,
    "_id": ObjectId("000000000000000000000002"),
    "extra_field": "extra ",
}

FEEDBACK_INF_2 = {
    **FEEDBACK_MIN_FIELDS,
    "_id": ObjectId("000000000000000000000003"),
    "inference_id": INF_ID2,
}

FEEDBACK_USER_2 = {
    **FEEDBACK_MIN_FIELDS,
    "_id": ObjectId("000000000000000000000004"),
    "created_by_user_id": USER_ORG_ADMIN["_id"],
}
FEEDBACK_PV_2 = {
    **FEEDBACK_MIN_FIELDS,
    "_id": ObjectId("000000000000000000000005"),
    "prompt_version_id": PV_ID2,
}

FEEBACK_ORG2 = {
    **FEEDBACK_MIN_FIELDS,
    "_id": ObjectId("000000000000000000000006"),
    "created_by_user_id": USER_BASIC_ORG2["_id"],
    "created_by_org_id": USER_BASIC_ORG2["org_id"],
}


test_db_data = {
    "feedbacks": [
        FEEDBACK_ALL_FIELDS,
        FEEDBACK_MIN_FIELDS,
        FEEDBACK_EXTRA_FIELD,
        FEEDBACK_INF_2,
        FEEDBACK_USER_2,
        FEEDBACK_PV_2,
        FEEBACK_ORG2,
    ]
}

expected_with_no_filter = [
    FEEDBACK_ALL_FIELDS,
    FEEDBACK_MIN_FIELDS,
    remove_props(FEEDBACK_EXTRA_FIELD, "extra_field"),
    FEEDBACK_INF_2,
    FEEDBACK_USER_2,
    FEEDBACK_PV_2,
]

feedbacks_get_test_spec: TestSpecList = [
    #
    # list & filters
    #
    {
        "spec_id": "Basic list no filter should show own org only",
        "mock_user": USER_BASIC,
        "input": {},
        "expected": expected_with_no_filter,
    },
    {
        "spec_id": "filter by inference_id",
        "mock_user": USER_BASIC,
        "input": {"params": {"inference_id": str(INF_ID2)}},
        "expected": [FEEDBACK_INF_2],
    },
    {
        "spec_id": "filter by prompton_user_id",
        "mock_user": USER_BASIC,
        "input": {
            "params": {"prompton_user_id": str(FEEDBACK_USER_2["created_by_user_id"])}
        },
        "expected": [FEEDBACK_USER_2],
    },
    {
        "spec_id": "filter by prompt_version_id",
        "mock_user": USER_BASIC,
        "input": {
            "params": {"prompt_version_id": str(FEEDBACK_PV_2["prompt_version_id"])}
        },
        "expected": [FEEDBACK_PV_2],
    },
    {
        "spec_id": "combined filter",
        "mock_user": USER_BASIC,
        "input": {
            "params": {
                "prompt_version_id": str(FEEDBACK_MIN_FIELDS["prompt_version_id"]),
                "inference_id": str(FEEDBACK_MIN_FIELDS["inference_id"]),
                "prompton_user_id": str(FEEDBACK_MIN_FIELDS["created_by_user_id"]),
            }
        },
        "expected": [
            FEEDBACK_ALL_FIELDS,
            FEEDBACK_MIN_FIELDS,
            remove_props(FEEDBACK_EXTRA_FIELD, "extra_field"),
        ],
    },
    #
    # get feedback by id
    #
    {
        "spec_id": "get by feedback_id",
        "mock_user": USER_BASIC,
        "input": {"id": str(FEEDBACK_MIN_FIELDS["_id"])},
        "expected": FEEDBACK_MIN_FIELDS,
    },
    #
    #  Permission tests
    #
    {
        "spec_id": "Basic shouldn't get other org's",
        "mock_user": USER_BASIC,
        "input": {"id": FEEBACK_ORG2["_id"]},
        "expected": 404,
    },
    {
        "spec_id": "OrgAdmin shouldn't get other org's",
        "mock_user": USER_ORG_ADMIN,
        "input": {"id": FEEBACK_ORG2["_id"]},
        "expected": 404,
    },
    #
    # Invalid requests
    #
    {
        "spec_id": "malformed prompt_version_id",
        "mock_user": USER_BASIC,
        "input": {"params": {"prompt_version_id": "xxx"}},
        "expected": 422,
    },
]
