from typing import Any, Dict
from bson import ObjectId


DEFAULT_MODEL_CONFIG = {
    "model": None,
    "temperature": None,
    "top_p": None,
    "stop": None,
    "max_tokens": None,
    "stop": None,
    "presence_penalty": None,
    "frequency_penalty": None,
    "logit_bias": None,
}

DEFAULT_RAW_COMPLETITION_REQUEST = {
    **DEFAULT_MODEL_CONFIG,
    "n": 1,
    "stream": False,
    "user": None,
}


ORG_ID1 = ObjectId("bbbbbbbbbbbbbbbbbbbbbbb1")
ORG_ID2 = ObjectId("bbbbbbbbbbbbbbbbbbbbbbb2")

ORG1: Dict[str, Any] = {
    "_id": ORG_ID1,
    "created_at": "2023-05-15T15:46:02.051309",
    "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
    "created_by_org_id": ObjectId("ffffffffffffffffffffffff"),
    "name": "org1",
    "access_keys": {"openai_api_key": "1234567890"},
}


ORG2 = {
    "_id": ORG_ID2,
    "created_at": "2021-05-15T15:46:02.051309",
    "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
    "created_by_org_id": ObjectId("ffffffffffffffffffffffff"),
    "name": "org2",
    "access_keys": None,
}


USER_BASIC: Dict[str, Any] = {
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_at": "2021-05-15T15:46:02.051309",
    "org_id": ORG_ID1,
    "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
    "created_by_org_id": ObjectId("ccccccccccccccccccccccc1"),
    "email": "basic@me.ai",
    "role": "Basic",
    "disabled": False,
    "hashed_password": "$2b$12$JhlMpZQbm09aYUqpgz4gjOBD9k/vOE0QfgzXBMCwpbRbINDEScCY6",
}

USER_PROMPT_ADMIN: Dict[str, Any] = {
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa2"),
    "created_at": "2021-05-15T15:46:02.051309",
    "org_id": ORG_ID1,
    "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
    "created_by_org_id": ObjectId("ccccccccccccccccccccccc1"),
    "email": "promptadmin@me.ai",
    "role": "PromptAdmin",
    "disabled": False,
    "hashed_password": "$2b$12$JhlMpZQbm09aYUqpgz4gjOBD9k/vOE0QfgzXBMCwpbRbINDEScCY6",
}


DEFAULT_MOCKED_USER = USER_BASIC

USER_BASIC_ORG2 = {
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa3"),
    "created_at": "2021-05-15T15:46:02.051309",
    "org_id": ORG_ID2,
    "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
    "created_by_org_id": ObjectId("ccccccccccccccccccccccc1"),
    "email": "basic2@me.ai",
    "role": "Basic",
}

USER_PROMPT_ADMIN_ORG2 = {
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa4"),
    "created_at": "2021-05-15T15:46:02.051309",
    "org_id": ORG_ID2,
    "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
    "created_by_org_id": ObjectId("ccccccccccccccccccccccc1"),
    "email": "promptadmin2@me.ai",
    "role": "PromptAdmin",
}

USER_ORG_ADMIN = {
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa5"),
    "created_at": "2021-05-15T15:46:02.051309",
    "org_id": ORG_ID1,
    "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
    "created_by_org_id": ObjectId("ccccccccccccccccccccccc1"),
    "name": "orgadmin@me.ai",
    "role": "OrgAdmin",
    "hashed_password": "$2b$12$JhlMpZQbm09aYUqpgz4gjOBD9k/vOE0QfgzXBMCwpbRbINDEScCY6",
}

USER_ORG_ADMIN_ORG2 = {
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa6"),
    "created_at": "2021-05-15T15:46:02.051309",
    "org_id": ORG_ID2,
    "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
    "created_by_org_id": ObjectId("ccccccccccccccccccccccc1"),
    "name": "orgadmin2@me.ai",
    "role": "OrgAdmin",
    "hashed_password": "$2b$12$JhlMpZQbm09aYUqpgz4gjOBD9k/vOE0QfgzXBMCwpbRbINDEScCY6",
}

USER_SUPER_ADMIN = {
    "_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa7"),
    "created_at": "2021-05-15T15:46:02.051309",
    "org_id": ObjectId("ccccccccccccccccccccccc1"),
    "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
    "created_by_org_id": ObjectId("ccccccccccccccccccccccc1"),
    "email": "superadmin@me.ai",
    "role": "SuperAdmin",
    "hashed_password": "$2b$12$JhlMpZQbm09aYUqpgz4gjOBD9k/vOE0QfgzXBMCwpbRbINDEScCY6",
}
