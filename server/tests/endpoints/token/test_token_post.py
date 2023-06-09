import json
from httpx import AsyncClient
import pytest

from tests.endpoints.token.token_post_test_data import (
    test_db_data,
    login_form_test_specs,
)


@pytest.mark.slow
@pytest.mark.parametrize("mock_db", [test_db_data], indirect=True)
@pytest.mark.parametrize("test_spec", login_form_test_specs)
@pytest.mark.anyio
async def test_login_form_post(
    endpoint: AsyncClient, mock_db, mock_get_hashed_password, test_spec
):
    print(" --> test_spec: ", test_spec)
    expected_status_code = test_spec["expected"]["status_code"]
    expected_response = test_spec["expected"]["response"]

    response = await endpoint.post("/token", data=test_spec["input"])
    response_data = response.json()
    print(" <-- Response:\n", json.dumps(response_data, indent=4))

    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
    else:
        assert response_data == expected_response
