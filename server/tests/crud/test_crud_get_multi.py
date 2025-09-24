import json
from bson import ObjectId

import pytest

from src.crud.prompt import prompt_crud
from src.schemas.base import PyObjectId
from src.schemas.user import UserInDB, UserRoles
from tests.utils import bson_to_json


PROMPT_BASE = {
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "status": "Active",
    "name": "UC t2 None description",
    "description": None,
}
PROMPT1 = {
    **PROMPT_BASE,
    "id": PyObjectId("648886d7f38b7183b2a97897"),
    "created_at": "2023-06-13T15:10:15.363000+00:00",
}
PROMPT2 = {
    "id": PyObjectId("648c7d1c6baa7a4759f6647c"),
    "created_at": "2023-06-16T15:17:48.531000+00:00",
    **PROMPT_BASE,
}

PROMPT3 = {
    "id": PyObjectId("648e9e68aaa77b3ed5c09e73"),
    "created_at": "2023-06-18T06:04:24.939000+00:00",
    **PROMPT_BASE,
}


test_db_data = {"prompts": [PROMPT1, PROMPT2, PROMPT3]}

mock_user = UserInDB(
    email="test@test.co",
    org_id=PyObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    role=UserRoles.SUPER_ADMIN,
    hashed_password="test",
)


@pytest.mark.parametrize("mock_db", [test_db_data], indirect=True)
@pytest.mark.anyio
async def test_get_multi_sort(mock_db):
    expected_default_sort = bson_to_json([PROMPT3, PROMPT2, PROMPT1])
    expected_reverse_sort = bson_to_json([PROMPT1, PROMPT2, PROMPT3])

    actual_prompts = await prompt_crud.get_multi(mock_db, mock_user)
    actual_prompts_json = [bson_to_json(p.dict()) for p in actual_prompts]
    print(f" <--- actual_prompts_json: {json.dumps(actual_prompts_json, indent=4)}")

    assert actual_prompts_json == expected_default_sort

    actual_prompts = await prompt_crud.get_multi(mock_db, mock_user, sort=("_id", 1))
    actual_prompts_json = [bson_to_json(p.dict()) for p in actual_prompts]

    assert actual_prompts_json == expected_reverse_sort
