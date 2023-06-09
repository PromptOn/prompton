import pytest
from httpx import AsyncClient
from deepdiff import DeepDiff


@pytest.mark.anyio
async def test_read_main(endpoint: AsyncClient):
    expected_response = {
        "version": "0.0.1",
        "message": "prompton-api is running",
        "dbstatus": {"status_code": 1, "status_message": "{'ok': 1.0}"},
    }  # +github_sha, github_env present

    response = await endpoint.get("/status")

    assert response.status_code == 200
    actual_response = response.json()

    diff = DeepDiff(
        expected_response,
        actual_response,
        ignore_order=True,
        exclude_paths=["github_sha", "github_env"],
    )

    print(" *** actual  vs. expected diff: \n", diff.pretty())
    assert diff == {}, "expected and actual response  should match"

    assert "github_sha" in actual_response
    assert "github_env" in actual_response
