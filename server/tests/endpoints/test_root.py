import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_read_main(endpoint: AsyncClient, mock_db, mock_user):
    response = await endpoint.get("/")
    db_status = str(await mock_db.command("ping"))

    assert response.status_code == 200
    assert response.json() == {
        "version": "0.0.1",
        "message": "prompton-api is running",
        "dbstatus": {"status_code": 1, "status_message": "{'ok': 1.0}"},
        "github_sha": None,
        "github_env": None,
    }


# TODO: 404 tests
