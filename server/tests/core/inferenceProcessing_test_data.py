from src.schemas.openAI import ChatGPTMessage

VALID_TEMPLATE = {"role": "system", "content": "bla ${arg1}", "name": None}


test_raw_request = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.5,
    "max_tokens": 100,
    "messages": [ChatGPTMessage.parse_obj({**VALID_TEMPLATE})],
    "user": "enduser",
}

mock_completition_data = {
    "id": "mockid",
    "object": "chat.completion",
    "created": 1684779054,
    "model": "gpt-5",
    "usage": {"prompt_tokens": 25, "completion_tokens": 1, "total_tokens": 26},
    "choices": [
        {
            "message": {"role": "assistant", "content": "MOCKED!", "name": None},
            "finish_reason": "stop",
            "index": 0,
        }
    ],
}


expected_response = {
    "isError": False,
    "completition_duration_seconds": 66.6,  # ignored in test
    "is_client_connected_at_finish": None,
    "first_message": mock_completition_data["choices"][0]["message"],  # type: ignore[index]
    "token_usage": mock_completition_data["usage"],
    "raw_response": mock_completition_data,
}

expected_error_response = {
    "completed_at": "2023-05-24 09:31:09.680517",
    "completition_duration_seconds": 66.6,  # ignored in test
    "is_client_connected_at_finish": None,
    "isError": True,
    "error": {
        "error_class": "builtins.Exception",
        "error": None,
        "message": "mocked error",
        "details": {},
    },
}
