import json
from typing import Any, List
from bson import ObjectId
from httpx import AsyncClient
import pytest
from deepdiff import DeepDiff

from server.tests.utils import (
    MockDBData,
    TestSpecList,
    assert_base_db_records,
    bson_to_json,
    format_test_specs,
)


def generate_pytest_post(
    endpoint_path: str,
    mock_db_data: MockDBData | None,
    collection_name: str,
    test_specs_post: TestSpecList,
    *,
    test_name: str | None = None,
    additional_fixture_names: List[str] | None = None,
):
    """Generate a pytest function to test an endpoint POST method.
    0. calls each fixture  in `additional_fixture_names` param if provided (mostly for extra mocks eg. `mock_get_hashed_password`)
    1. mocks db data using `mock_db_data` if None passed it mocks with an empty DB
    2. mocks user based on `test_specs_post[].mock_user`
    3. calls endpoint PATCH with url param `test_specs_post[].input.id`,
        uses request body defined in `test_specs_post[].input.request_body`
    4. compares response to expected data (DeepDiff)
        If expected is int then it only validates response_code against it (used for testing validation errors)
    5. Reads db record from `collection_name` by  `test_specs_post[].input.id`
    6. Compares db data vs. `test_specs_post[].expected` .
        if `test_specs_post[].expected_db` is provided then it compares against that instead of `test_specs_post[].expected`.

    Test name is generated from `endpoint_path` if not provided.
    """
    if not test_name:
        test_name = endpoint_path

    spec_user_tuples, ids = format_test_specs(test_specs_post)

    @pytest.mark.parametrize(
        "test_spec, mock_user", spec_user_tuples, ids=ids, indirect=["mock_user"]
    )
    @pytest.mark.parametrize("mock_db", [mock_db_data], indirect=True)
    @pytest.mark.anyio
    async def test_func(endpoint: AsyncClient, mock_db, mock_user, test_spec, request):
        if additional_fixture_names:
            for fixture_name in additional_fixture_names:
                request.getfixturevalue(fixture_name)

        input = test_spec.get("input", {})
        request_body = bson_to_json(input.get("request_body", {}))
        expected_response = bson_to_json(test_spec["expected"])
        print(" --> expected response:", json.dumps(expected_response, indent=4))
        expected_db = bson_to_json(test_spec.get("expected_db", expected_response))

        input_id = input.get("id")
        url = f"{endpoint_path}/{input_id}" if input_id else endpoint_path
        print(" --> request url:", url, "request_body: ", request_body)

        if test_spec.get("mock_exception"):
            raise Exception(
                "mock_exception present in test_spec but post_test_generator does not support it yet"
            )

        response = await endpoint.post(url, json=request_body)
        response_data = response.json()
        print(
            f" <-- Response status code: {response.status_code}\n Response data:\n{json.dumps(response_data, indent=4)}"
        )

        if isinstance(expected_response, int):
            assert response.status_code == expected_response
            return

        assert response.status_code == 201

        resp_id = response_data["id"]

        actual_db = await mock_db[collection_name].find_one({"_id": ObjectId(resp_id)})
        actual_db = bson_to_json(actual_db)
        print(" <-- DB data: ", json.dumps(actual_db, indent=4))
        if isinstance(actual_db, dict) and isinstance(expected_db, dict):
            print(" !!!***", type(actual_db.get("role")), type(expected_db.get("role")))

        # expected vs db (check if id and created_at included in response)
        assert_base_db_records(resp_id, actual_db)
        diff = DeepDiff(
            expected_db,
            actual_db,
            ignore_order=True,
            exclude_paths=[
                "created_at",
                "_id",
                "root['response']['completition_duration_seconds']",  # khmm...
            ],
        )
        print(" *** db data vs. expected diff: \n", diff.pretty())
        assert diff == {}, "response data and db should match"

    test_func.__name__ = f"test_{test_name}_post"
    return test_func
