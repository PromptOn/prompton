# TODO: - test to read a record which doesn't pass the validation (ie. extra fields, missing name field)

from typing import Any, Dict
from bson import ObjectId

from tests.shared_test_data import ORG_ID1, ORG_ID2

PROMPT_ALL_FIELDS: Dict[str, Any] = {
    "_id": ObjectId("645d786f180786983c9eede6"),
    "created_at": "2023-05-15T15:46:02.051309",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "status": "Active",
    "name": "UC t1",
    "description": "t1 descri",
}

PROMPT_MIN_FIELDS: Dict[str, Any] = {
    "_id": ObjectId("645d786f180786983c9eede7"),
    "created_at": "2023-05-15T15:46:02.051309",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "status": "Active",
    "name": "UC t2 None description",
    "description": None,
}
PROMPT_ARCHIVED_ORG2: Dict[str, Any] = {
    "_id": ObjectId("645d786f180786983c9eede8"),
    "created_at": "2023-05-15T15:46:02.051309",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID2,
    "status": "Archived",
    "name": "UC t3 Arc",
    "description": "t3 descri",
}

PROMPT_EXTRA_FIELD: Dict[str, Any] = {
    "_id": ObjectId("645d786f180786983c9eede9"),
    "created_at": "2023-05-15T15:46:02.051309",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "status": "Archived",
    "name": "UC t3 Arc",
    "description": "t3 descri",
    "extra_field": "extra field in db, should be read but not be in response",
}
