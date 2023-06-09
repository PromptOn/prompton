from typing import Any, Dict
from httpx import AsyncClient
import pytest
from src.asgi import app

from tests.utils import get_all_endpoint_methods, method_mapping

no_auth_white_list_paths = [
    "/",
    "/status",
    "/docs/oauth2-redirect",
    "/redoc",
    "/openapi.json",
    "/token",
]

all_endpoints = get_all_endpoint_methods(app)

auth_required_endpoints_list = [
    e for e in all_endpoints if e["path"] not in no_auth_white_list_paths
]


@pytest.mark.parametrize(
    "auth_required_endpoint",
    auth_required_endpoints_list,
    ids=lambda x: f"{x['method']} {x['path']}",
)
@pytest.mark.anyio
async def test_end_point_auth(endpoint: AsyncClient, auth_required_endpoint):
    print(f" --> end_point: {auth_required_endpoint}")
    method_name = auth_required_endpoint.get("method")
    path_to_call = auth_required_endpoint.get("path")

    args: Dict[str, Any] = (
        {"json": {}} if method_name in ["POST", "PATCH", "PUT"] else {}
    )
    print(method_name, path_to_call)

    method_to_call = method_mapping.get(method_name)
    assert method_to_call

    # valid ObjectId, but not in db
    response = await method_to_call(endpoint, f"{path_to_call}", **args)

    response_data = response.json()
    print(
        f" <-- response status_code: {response.status_code}\n   data: {response_data}]"
    )

    assert response.status_code == 401

    # assert response.status_code == test_item["expected"]["status_code"]
