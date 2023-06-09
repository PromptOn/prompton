import json
from unittest import mock
import pytest
from deepdiff import DeepDiff

from src.core.completition import get_openai_chat_completition

from src.schemas.inference import InferenceCreate
from src.schemas.openAI import ChatGPTChatCompletitionRequest
from tests.core.inferenceProcessing_test_data import (
    expected_error_response,
    mock_completition_data,
    test_raw_request,
    expected_response,
)
from tests.shared_test_data import DEFAULT_RAW_COMPLETITION_REQUEST
from tests.utils import bson_to_json


@pytest.mark.parametrize("mock_openai", [mock_completition_data], indirect=True)
@pytest.mark.anyio
async def test_chat_completition(mock_openai):
    raw_request = ChatGPTChatCompletitionRequest.parse_obj(test_raw_request)

    resp = await get_openai_chat_completition(
        raw_request, "dummy api key", request_timeout=110
    )
    resp = bson_to_json(resp.dict())
    print(" <-- resp: ", json.dumps(resp, indent=4))

    comp_dur = resp.get("completition_duration_seconds")
    assert comp_dur and comp_dur >= 0
    diff = DeepDiff(
        expected_response,
        resp,
        exclude_paths=["completed_at", "completition_duration_seconds"],
        ignore_order=True,
    )
    print(" *** response vs expected resp diff: ", diff.pretty())

    assert diff == {}, "response does not match expected"


@mock.patch("openai.ChatCompletion.acreate", side_effect=Exception("mocked error"))
@pytest.mark.anyio
async def test_chat_completition_openai_exception(openai_mock):
    raw_request = ChatGPTChatCompletitionRequest.parse_obj(test_raw_request)

    resp = await get_openai_chat_completition(
        raw_request, "dummy api key", request_timeout=110
    )

    assert resp is not None

    resp = bson_to_json(resp.dict())
    print(" <-- resp: ", json.dumps(resp, indent=4))

    assert resp["completition_duration_seconds"] >= 0
    diff = DeepDiff(
        expected_error_response,
        resp,
        exclude_paths=["completed_at", "completition_duration_seconds"],
        ignore_order=True,
    )
    print(" *** error response vs expected resp diff: ", diff.pretty())

    assert diff == {}, "response does not match expected"
