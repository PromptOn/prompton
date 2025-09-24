import json
from typing import List
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


def generate_pytest_post(
    endpoint_path: str,
    mock_db_data: MockDBData | None,
    collection_name: str | None,
    test_specs_post: TestSpecList,
    *,
    test_name: str | None = None,
    additional_fixture_names: List[str] | None = None,
):
    """Generate a pytest function to test an endpoint POST method.
    0. calls each fixture  in `additional_fixture_names` param if provided (mostly for extra mocks eg. `mock_get_hashed_password`)
    1. mocks db data using `mock_db_data` if None passed it mocks with an empty DB
    2. mocks user based on `test_specs_post[].mock_user`
    3. calls endpoint POST with url param `test_specs_post[].input.id`,
        uses request body defined in `test_specs_post[].input.request_body`
    4. If expected is int then it only validates response_code against it (used for testing validation errors)
        DOES NOT compare response data to expected data
    5. If `collection_name` is not None it Reads db record from `collection_name` by  `test_specs_post[].input.id`
    6. Compares db data vs. `test_specs_post[].expected` .
        if `test_specs_post[].expected_db` is provided then it compares against that instead of `test_specs_post[].expected`.

    Custom DB validation:
         Set `test_specs_post[x].expected_db` in `TestSpec` to a `CustomValidatorFn` type.
         This function will be called with the `actual_db` .
         It should return True or False but better to do assert within the function so easier to find where test failed.

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
        # TODO: clean this up: refactor TestSpec into expected.response, expected.status_code, expected.db  structure & test only against which is provided. Or try to find a framework? PyRest-Python or similar?
        #
        # Prepare
        #

        if additional_fixture_names:
            for fixture_name in additional_fixture_names:
                request.getfixturevalue(fixture_name)

        input = test_spec.get("input", {})
        request_body = bson_to_json(input.get("request_body", None))
        request_data = bson_to_json(input.get("request_data", None))

        expected_response = bson_to_json(test_spec["expected"])
        print(" --> expected response:", json.dumps(expected_response, indent=4))
        expected_db_json = bson_to_json(test_spec.get("expected_db", expected_response))

        input_id = input.get("id")
        url = f"{endpoint_path}/{input_id}" if input_id else endpoint_path
        print(
            f" --> request url: {url}\n  Request_body: {request_body} \n  Request_data:  {request_data}"
        )

        #
        # ACT
        #

        if test_spec.get("mock_exception"):
            raise Exception(
                "mock_exception present in test_spec but post_test_generator does not support it yet"
            )

        response = await endpoint.post(url, json=request_body, data=request_data)
        response_data = response.json()
        print(
            f" <-- Response status code: {response.status_code}\n Response data:\n{json.dumps(response_data, indent=4)}"
        )

        # TODO: test expected response data vs. actual response data - ignore values for DeepDiff which are passed as type and only do typecheck.
        if callable(expected_response):
            assert expected_response(expected_response, response_data)

        #
        # EXPECTED status_code vs actual
        #
        if isinstance(expected_response, int):
            assert response.status_code == expected_response
            return  # we expected an error , we only validate response code
        elif "expected_status_code" in test_spec:
            # this is for special case for getter via post which returns 200 instead of 201 (/token* only now)
            assert response.status_code == test_spec["expected_status_code"]
        else:
            assert response.status_code == 201

        #
        # EXPECTED db vs actual db if collection_name passed
        #
        if collection_name:
            resp_id = response_data["id"]

            actual_db = await mock_db[collection_name].find_one(
                {"_id": ObjectId(resp_id)}
            )
            actual_db_json = bson_to_json(actual_db)
            print(" <-- DB data: ", json.dumps(actual_db_json, indent=4))

            if callable(test_spec.get("expected_db", None)):
                custom_db_validator = test_spec["expected_db"]
                print(
                    " <--- calling CustomValidatorFn specified in TestSpec with actual_db"
                )
                assert custom_db_validator(actual_db)

            else:
                assert_base_db_records(resp_id, actual_db_json)
                diff = DeepDiff(
                    expected_db_json,
                    actual_db_json,
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
