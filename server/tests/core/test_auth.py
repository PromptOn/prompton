from bson import ObjectId
import pytest

from src.core.auth import (
    get_hashed_password,
    verify_password,
    authenticate_user,
)
from src.schemas.user import UserInDB

PASSWORD_HASH_foo = "$2b$12$4MvKPux4R8AWrA/FFTW5muiVrYKqS.7NlQOA6N81U0lATUoijV4NK"
PASSWORD_HASH_bar = "$2b$12$ZYZMqs2CsDA./fueQkwQceorkm1xOLm5j6yGLF206.Glfwncbo2PG"

# TODO: test rest of core.auth  methods


@pytest.mark.slow  # ~ 1s +
@pytest.mark.anyio
async def test_password_hashing():
    password = "foo"
    password_hash1 = get_hashed_password(password)
    password_hash2 = get_hashed_password(password)

    assert password_hash1 != password_hash2
    assert len(password_hash1) == 60
    assert verify_password(password, password_hash1)
    assert verify_password(password, password_hash2)
    assert not verify_password(password, PASSWORD_HASH_bar)


test_db_data = {
    "users": [
        {
            "_id": "645d786f180786983c9eede6",
            "created_at": "2021-05-24 09:31:09.680517",
            "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
            "created_by_org_id": ObjectId("bbbbbbbbbbbbbbbbbbbbbbb1"),
            "email": "hal@gov.ai",
            "disabled": False,
            "full_name": "hey",
            "role": "Basic",
            "org_id": ObjectId("ffffffffffffffffffffffff"),
            "hashed_password": PASSWORD_HASH_foo,
        },
    ]
}

test_authenticate_user_test_spec = [
    pytest.param(
        {
            "input": {
                "email": "hal@gov.ai",
                "password": "foo",
                "verify_password_response": True,
            },
            "expected": test_db_data["users"][0],
        },
        id="sucess auth",
    ),
    pytest.param(
        {
            "input": {
                "email": "hal@gov.ai",
                "password": "wrong",
                "verify_password_response": False,
            },
            "expected": False,
        },
        id="wrong pass",
    ),
    pytest.param(
        {
            "input": {
                "email": "donald@gov.us",
                "password": "bar",
                "verify_password_response": True,
            },
            "expected": False,
        },
        id="nonexistent email",
    ),
    pytest.param(
        {
            "input": {
                "email": None,
                "password": "bar",
                "verify_password_response": True,
            },
            "expected": False,
        },
        id="none email",
    ),
]


# TODO: test for auth via /token endpoint too
@pytest.mark.parametrize("mock_db", [test_db_data], indirect=True)
@pytest.mark.parametrize("test_spec", test_authenticate_user_test_spec)
@pytest.mark.anyio
async def test_authenticate_user(mock_db, mock_verify_password_factory, test_spec):
    print(" --> test_spec: ", test_spec)
    mock_verify_password_factory(test_spec["input"]["verify_password_response"])

    user = await authenticate_user(
        email=test_spec["input"]["email"],
        password=test_spec["input"]["password"],
        db=mock_db,
    )
    print(" <-- authenticate_user resp: ", user)

    if test_spec["expected"]:
        assert user
        assert user == UserInDB.parse_obj(test_spec["expected"])
    else:
        assert user == False
