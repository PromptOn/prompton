from typing import Any, Dict
import pytest
from httpx import AsyncClient
from tests.shared_test_data import USER_SUPER_ADMIN

from tests.utils import method_mapping

test_items = [
    pytest.param(
        {
            "id": "ffffffffffffffffffffffff",
            "expected": {
                "status_code": 404,
                "response_data": {
                    "detail_startswith": "Item id ffffffffffffffffffffffff not found or current user has no permission to access it"
                },
            },
        },
        id="not found",
    ),
    pytest.param(
        {
            "id": "xxx",
            "expected": {
                "status_code": 422,
                "response_data": {
                    "detail_startswith": "Invalid item id supplied: 'xxx' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
                },
            },
        },
        id="invalid id",
    ),
]

endpoints = {
    "GET": [
        "/prompts",
        "/promptVersions",
        "/inferences",
        "/orgs",
        "/users",
        "/feedbacks",
    ],
    "PATCH": ["/promptVersions", "/prompts", "/orgs"]
    # TODO: add "/users" when user's PATCH  implemented
    # "DELETE": ["/prompts", "/promptVersions"]
}


@pytest.mark.parametrize(
    "method,endpoint_path",
    [(method, endpoint) for method in endpoints for endpoint in endpoints[method]],
)
@pytest.mark.parametrize("test_item", test_items)
@pytest.mark.parametrize("mock_user", [USER_SUPER_ADMIN], indirect=True)
@pytest.mark.anyio
async def test_invalid_item_ids(
    endpoint: AsyncClient,
    mock_db,
    mock_user,
    method,
    endpoint_path,
    test_item,
):
    expected = test_item["expected"]
    method_to_call = method_mapping.get(method)

    args: Dict[str, Any] = (
        {"json": {}} if method in ["POST", "PATCH", "PUT", "DELETE"] else {}
    )

    print(f" --> method: {method} endpoint_path: {endpoint_path} args: {args}")

    assert method_to_call is not None

    # valid ObjectId, but not in db
    response = await method_to_call(
        endpoint, f"{endpoint_path}/{test_item['id']}", **args
    )

    response_data = response.json()
    print(
        f" <-- response status_code: {response.status_code}\n   data: {response_data}]"
    )

    assert response.status_code == expected["status_code"]
    actual_detail = str(response_data["detail"])
    assert actual_detail.startswith(expected["response_data"]["detail_startswith"])
    # diff = DeepDiff(response_data, expected["response_data"], ignore_order=True)
    # assert diff == {}
