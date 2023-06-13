import pytest
from httpx import AsyncClient

from src.asgi import app

# for additional mocking :
from .conftest_mock_db import *
from .conftest_mock_openai import *
from .conftest_mock_auth import *


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
