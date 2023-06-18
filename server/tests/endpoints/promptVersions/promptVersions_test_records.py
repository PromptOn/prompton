from typing import Any, Dict
from bson import ObjectId

from tests.shared_test_data import (
    ORG_ID1,
    ORG_ID2,
    DEFAULT_MODEL_CONFIG,
)

VALID_TEMPLATE = {"role": "system", "content": "bla ${var}", "name": None}
VALID_MODEL_CONFIG = {"model": "gpt-5", "temperature": 0.5, "max_tokens": 100}


PROMPT_WITH_2_VER = {
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaaa"),
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "status": "Active",
    "name": "propt 1",
}

PROMPT_WITH_1_VER = {
    "_id": ObjectId("bbbbbbbbbbbbbbbbbbbbbbbb"),
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "status": "Active",
    "name": "prompt 2",
}

PROMPT_WITH_1_VER_ORG2 = {
    "_id": ObjectId("cccccccccccccccccccccccc"),
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID2,
    "status": "Archived",
    "name": "prompt 3",
}


PROMPT_VER_LIVE_ID = ObjectId("645d786f180786983c9eede6")
PROMPT_VER_DRAFT_ID = ObjectId("645d786f180786983c9eede7")
PROMPT_VER_TESTING_ID = ObjectId("645d786f180786983c9eede8")
PROMPT_VER_ARCHIVED_ID = ObjectId("645d786f180786983c9eede9")

PROMPT_VER_LIVE: Dict[str, Any] = {
    "_id": str(PROMPT_VER_LIVE_ID),
    "created_at": "2023-05-15T15:46:02.051309",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "status": "Live",
    "name": "templ test 1",
    "description": "t1 desc",
    "prompt_id": PROMPT_WITH_2_VER["_id"],
    "provider": "OpenAI",
    "template": [{**VALID_TEMPLATE}],
    "model_config": {**DEFAULT_MODEL_CONFIG, **VALID_MODEL_CONFIG},
    "template_arg_names": ["var"],
}


PROMPT_VER_TESTING_EXTRA_FIELD: Dict[str, Any] = {
    **PROMPT_VER_LIVE,
    "_id": PROMPT_VER_TESTING_ID,
    "status": "Testing",
    "extra_field": "extra field should be ignored by read",
}

PROMPT_VER_ARCHIVED_ORG2: Dict[str, Any] = {
    **PROMPT_VER_LIVE,
    "_id": PROMPT_VER_ARCHIVED_ID,
    "created_by_org_id": ORG_ID2,
    "prompt_id": PROMPT_WITH_1_VER_ORG2["_id"],
    "status": "Archived",
}

PROMPT_VER_DRAFT: Dict[str, Any] = {
    "_id": PROMPT_VER_DRAFT_ID,
    "created_at": "2023-05-15T15:46:02.051309",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "status": "Draft",
    "name": "templ test 2",
    "description": None,
    "prompt_id": PROMPT_WITH_1_VER["_id"],
    "provider": "OpenAI",
    "template": [],
    "model_config": None,
    "template_arg_names": [],
}
