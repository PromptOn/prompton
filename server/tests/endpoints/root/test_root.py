import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_read_main(endpoint: AsyncClient):
    response = await endpoint.head("/")

    assert response.status_code == 200
