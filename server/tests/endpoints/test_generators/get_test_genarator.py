import json
from typing import List
from httpx import AsyncClient
import pytest
from tests.shared_test_data import DEFAULT_MOCKED_USER
from tests.utils import (
    MockDBData,
    TestSpecList,
    bson_to_json,
    format_test_specs,
)

from deepdiff import DeepDiff


def generate_pytest_get(
    endpoint_path: str,
    mock_db_data: MockDBData | None,
    test_specs_get: TestSpecList,
    test_name: str | None = None,
):
    """Generate a pytest function to test an endpoint GET method.
    1. mocks db data using `mock_db_data` if None passed it mocks with an empty DB
    2. mocks user based on `test_specs_get.mock_user`
    3. calls endpoint GET with params defined in `test_specs_get[].input.params` (using `input.id` as url param if provided)
    4. compares response to expected data (DeepDiff)
        If expected is int then it only validates response_code against it (used for testing validation errors)

    Test name is generated from `endpoint_path` if not provided.
    """
    if not test_name:
        test_name = endpoint_path

    spec_user_tuples, ids = format_test_specs(test_specs_get)

    @pytest.mark.parametrize(
        "test_spec, mock_user", spec_user_tuples, ids=ids, indirect=["mock_user"]
    )
    @pytest.mark.parametrize("mock_db", [mock_db_data], indirect=True)
    @pytest.mark.anyio
    async def test_func(endpoint: AsyncClient, mock_db, mock_user, test_spec):
        expected = bson_to_json(test_spec["expected"])
        print(" *** Expected:\n", json.dumps(expected, indent=4))

        input = bson_to_json(test_spec.get("input", {}))
        input_params = input.get("params", {})
        input_id = input.get("id")
        url = f"{endpoint_path}/{input_id}" if input_id else endpoint_path
        print(" --> Request url:", url, "params:", input_params)

        response = await endpoint.get(url, params=input_params)

        response_data = response.json()
        print(
            f" <-- Response status code: {response.status_code}\n Response data:\n{json.dumps(response_data, indent=4)}"
        )

        if isinstance(expected, int):
            assert response.status_code == expected
            return

        assert response.status_code == 200

        # response vs expected data
        print(f"response_data len: {len(response_data)}  expected len: {len(expected)}")
        assert len(response_data) == len(expected)

        diff = DeepDiff(expected, response_data, ignore_order=True)
        print(" *** response vs expected diff:\n", diff.pretty())
        assert diff == {}, "response and expected data should match"

    test_func.__name__ = f"test_{test_name}_get"
    return test_func


def generate_pytest_get_empty(
    endpoint_path: str,
    test_name: str | None = None,
    mock_users: List[dict] | None = None,
):
    # TODO: we could get rid of this method making generate_pytest_get to accept None for `mock_db_data`
    if not test_name:
        test_name = endpoint_path + "_empty"

    if not mock_users:
        mock_users = [DEFAULT_MOCKED_USER]

    @pytest.mark.parametrize("mock_user", mock_users, indirect=True)
    @pytest.mark.anyio
    async def test_func(endpoint: AsyncClient, mock_db, mock_user):
        print(" --> Request url:", endpoint_path)

        response = await endpoint.get(endpoint_path)
        print(" <-- Response data:\n", json.dumps(response.json(), indent=4))

        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 0

    test_func.__name__ = f"test_{test_name}_get"
    return test_func
