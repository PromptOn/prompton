from bson import ObjectId
from tests.utils import TestSpecList

PASSWORD_HASH_foo = "$2b$12$4MvKPux4R8AWrA/FFTW5muiVrYKqS.7NlQOA6N81U0lATUoijV4NK"

test_db_data = {
    "users": [
        {
            "_id": ObjectId("645d786f180786983c9eede6"),
            "created_at": "2021-05-24 09:31:09.680517",
            "created_by_user_id": ObjectId("645d786f180786983c9eede6"),
            "created_by_org_id": ObjectId("ccccccccccccccccccccccc1"),
            "email": "hal@gov.ai",
            "disabled": False,
            "full_name": "hey",
            "role": "Basic",
            "org_id": "ffffffffffffffffffffffff",
            "hashed_password": PASSWORD_HASH_foo,
        },
    ]
}


test_specs_token_post: TestSpecList = [
    {
        "spec_id": "valid password",
        "mock_user": None,
        "input": {"request_data": {"username": "hal@gov.ai", "password": "foo"}},
        "expected": {"token_type": "bearer", "access_token": str},
        "expected_status_code": 200,
    },
    {
        "spec_id": "invalid password",
        "mock_user": None,
        "input": {"request_data": {"username": "hal@gov.ai", "password": "wrong"}},
        "expected": 401,
    },
    {
        "spec_id": "invalid username",
        "mock_user": None,
        "input": {"request_data": {"username": "hello@fake.ai", "password": "wrong"}},
        "expected": 401,
    },
]

test_specs_token_basic_post: TestSpecList = [
    {
        "spec_id": "valid password",
        "mock_user": None,
        "input": {"request_body": {"username": "hal@gov.ai", "password": "foo"}},
        "expected": {"token_type": "bearer", "access_token": str},
        "expected_status_code": 200,
    },
    {
        "spec_id": "invalid email username",
        "mock_user": None,
        "input": {"request_body": {"username": "not@email.", "password": "wrong"}},
        "expected": 422,
    },
    {
        "spec_id": "invalid password",
        "mock_user": None,
        "input": {"request_body": {"username": "hal@gov.ai", "password": "wrong"}},
        "expected": 401,
    },
    {
        "spec_id": "invalid username",
        "mock_user": None,
        "input": {"request_body": {"username": "hello@fake.ai", "password": "wrong"}},
        "expected": 401,
    },
]
