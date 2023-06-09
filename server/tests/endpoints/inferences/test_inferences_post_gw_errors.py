import json
from bson import ObjectId
import pytest
from httpx import AsyncClient
from deepdiff import DeepDiff

from tests.endpoints.inferences.inferences_post_test_spec import (
    post_openai_error_test_specs,
    test_db_data,
)

from tests.utils import bson_to_json, format_test_specs

# Not using  post_test_genarator,
#    calling a fixture (mock_openai_exception_factory) with parameters from  post_test_genarator is too much hassle

spec_user_tuples, ids = format_test_specs(post_openai_error_test_specs)


@pytest.mark.parametrize(
    "test_spec, mock_user", spec_user_tuples, ids=ids, indirect=["mock_user"]
)
@pytest.mark.parametrize("mock_db", [test_db_data], indirect=True)
@pytest.mark.anyio
async def test_inference_post_openai_errors(
    endpoint: AsyncClient, mock_db, mock_user, mock_openai_exception_factory, test_spec
):
    input = test_spec.get("input", {})
    request_body = bson_to_json(input.get("request_body", {}))
    expected_response = bson_to_json(test_spec["expected"])
    expected_db = bson_to_json(test_spec.get("expected_db", expected_response))

    input_id = input.get("id")
    url = f"/inferences/{input_id}" if input_id else "/inferences"
    print(" --> request:", url, request_body)

    mock_openai_exception_factory(test_spec["mock_exception"])
    response = await endpoint.post("/inferences", json=request_body)

    response_data = response.json()
    print(" <-- Response data:\n", json.dumps(response_data, indent=4))

    assert response.status_code == 502

    resp_id = response_data["detail"]["inference_id"]

    actual_db = await mock_db.inferences.find_one({"_id": ObjectId(resp_id)})
    actual_db = bson_to_json(actual_db)

    print(" <-- DB data:\n", json.dumps(actual_db, indent=4))

    # response vs expected
    assert response_data["detail"]["inference_id"] == resp_id
    diff = DeepDiff(
        expected_response,
        response_data,
        ignore_order=True,
        exclude_paths=["root['detail']['inference_id']"],
    )
    print(" *** response vs expected diff:\n", diff.pretty())
    assert diff == {}, "response data should be as expected"

    # expected vs db (check if id and created_at included in response)
    assert actual_db["_id"] == resp_id
    assert actual_db["response"]["completition_duration_seconds"] >= 0
    diff = DeepDiff(
        expected_db,
        actual_db,
        ignore_order=True,
        exclude_paths=[
            "created_at",
            "_id",
            "root['response']['completed_at']",
            "root['response']['error']['details']",
            "root['response']['completition_duration_seconds']",
        ],
    )
    print(" *** db vs expected diff:\n", diff.pretty())
    assert diff == {}, "db data should be as expected"
