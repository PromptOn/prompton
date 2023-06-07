from bson import ObjectId
import pytest


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
login_form_test_specs = [
    pytest.param(
        {
            "input": {"username": "hal@gov.ai", "password": "foo"},
            "expected": {
                "status_code": 200,
                "response": {"token_type": "bearer"},
            },  # + "access_token"
        },
        id="valid password",
    ),
    pytest.param(
        {
            "input": {"username": "hal@gov.ai", "password": "wrong"},
            "expected": {
                "status_code": 401,
                "response": {"detail": "Incorrect username or password"},
            },
        },
        id="invalid password",
    ),
    pytest.param(
        {
            "input": {"username": "xx", "password": "wrong"},
            "expected": {
                "status_code": 401,
                "response": {"detail": "Incorrect username or password"},
            },
        },
        id="invalid username",
    ),
]
