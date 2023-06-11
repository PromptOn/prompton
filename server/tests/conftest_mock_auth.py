from functools import partial
import pytest

from src.asgi import app
from tests.shared_test_data import DEFAULT_MOCKED_USER

from tests.utils import get_all_endpoint_methods
from src.core import auth
from src.schemas.user import UserRead


@pytest.fixture(
    params=get_all_endpoint_methods(app),
    ids=lambda x: f"{x.get('method')} {x.get('path')}",
    scope="session",
)
def endpoint_method_from_all(request):
    # method name is weird here but it makes more sense when applying to test functions
    return request.param


@pytest.fixture()
def mock_user(request):
    """Mock user for testing. For the a dafult basic role user just add `mock_user` param to the test function arg list.
    To override the default user decorate the test:
    `@pytest.mark.parametrize("mock_user", [{"disabled": True}], indirect=True)`"""

    try:
        mocked_user = DEFAULT_MOCKED_USER
        if request.param:
            mocked_user = {**mocked_user, **request.param}

    except AttributeError:  # don't ask...
        mocked_user = DEFAULT_MOCKED_USER

    mocked_user_obj = UserRead(**mocked_user)

    async def mock_get_current_user():
        return mocked_user_obj

    app.dependency_overrides[auth.get_current_user] = mock_get_current_user

    yield

    del app.dependency_overrides[auth.get_current_user]


@pytest.fixture()
def mock_get_hashed_password(monkeypatch):
    # NB: this doesn't work if `from ...auth import get_hashed_password` is used in the code?
    def mock_password_hash(request):
        return "monkeypatched_hashed_password"

    monkeypatch.setattr(
        auth,
        "get_hashed_password",
        mock_password_hash,
    )


@pytest.fixture()
def mock_verify_password_factory(monkeypatch):
    def _mock_verify_password(request):
        def mock_verify_password(*args, **kwargs):
            return request

        monkeypatch.setattr(
            auth,
            "verify_password",
            mock_verify_password,
        )

    return _mock_verify_password
