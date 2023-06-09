import json
from bson import ObjectId
from httpx import AsyncClient
import pytest
from deepdiff import DeepDiff

from tests.utils import (
    MockDBData,
    TestSpecList,
    assert_base_db_records,
    bson_to_json,
    format_test_specs,
)


def generate_pytest_patch(
    endpoint_path: str,
    mock_db_data: MockDBData | None,
    collection_name: str,
    test_specs_patch: TestSpecList,
    test_name: str | None = None,
):
    """Generate a pytest function to test an endpoint PATCH method.
    1. mocks db data using `mock_db_data` if None passed it mocks with an empty DB
    2. mocks user based on `test_specs_patch[].mock_user`
    3. calls endpoint PATCH with url param `test_specs_patch[].input.id`,
        uses request body defined in `test_specs_patch[].input.request_body`
    4. compares response to expected data (DeepDiff)
        If expected is int then it only validates response_code against it (used for testing validation errors)
    5. Reads db record from `collection_name` by  `test_specs_patch[].input.id`
    6. Compares db data vs. `test_specs_patch[].expected` .
        if `test_specs_patch[].expected_db` is provided then it compares against that instead of `test_specs_patch[].expected`.

    Test name is generated from `endpoint_path` if not provided.
    """
    if not test_name:
        test_name = endpoint_path

    spec_user_tuples, ids = format_test_specs(test_specs_patch)

    @pytest.mark.parametrize(
        "test_spec, mock_user", spec_user_tuples, ids=ids, indirect=["mock_user"]
    )
    @pytest.mark.parametrize("mock_db", [mock_db_data], indirect=True)
    @pytest.mark.anyio
    async def test_func(endpoint: AsyncClient, mock_db, mock_user, test_spec):
        input = test_spec.get("input", {})
        request_body = bson_to_json(input.get("request_body", {}))
        print(" ** request_body:", request_body)
        expected_response = bson_to_json(test_spec["expected"])
        print(" ** expected_response:", expected_response)
        expected_db = bson_to_json(test_spec.get("expected_db", expected_response))

        input_id = str(input.get("id"))
        url = f"{endpoint_path}/{input_id}" if input_id else endpoint_path
        print(" --> request:", url, request_body)

        response = await endpoint.patch(url, json=request_body)

        response_data = response.json()
        print(
            f" <-- Resp :\n {response.status_code} {json.dumps(response_data, indent=4)}"
        )

        if isinstance(expected_response, int):
            assert response.status_code == expected_response
            return

        assert response.status_code == 200

        actual_db = await mock_db[collection_name].find_one({"_id": ObjectId(input_id)})
        actual_db = bson_to_json(actual_db)
        print(" <-- DB data:\n", json.dumps(actual_db, indent=4))

        resp_id = response_data["_id"]

        # response vs expected
        assert resp_id == input_id
        diff = DeepDiff(expected_response, response_data, ignore_order=True)
        print(" *** response vs db diff", diff.pretty())
        assert diff == {}, "response and expected should match"

        # db vs expected
        assert_base_db_records(resp_id, actual_db)

        diff = DeepDiff(expected_db, actual_db, ignore_order=True)
        print(" *** db vs expected diff", diff.pretty())
        assert diff == {}, "db data and expected should match"

    test_func.__name__ = f"test_{test_name}_patch"
    return test_func
