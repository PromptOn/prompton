from typing import Any, Dict
from bson import ObjectId

from tests.shared_test_data import ORG_ID1, ORG_ID2

VALID_TEMPLATE = {"role": "system", "content": "a1: ${arg1} a2: ${arg2}", "name": None}

# with 1 inference ORG1
PROMPT_ID1 = ObjectId("6468b05c1e5a37458856d10a")
PROMPT_VERSION_ID1 = ObjectId("646bae490e5a37458856d10b")
# with 2 inferences ORG1
PROMPT_ID2 = ObjectId("6468b05c1e5a37458856d10c")
PROMPT_VERSION_ID2 = ObjectId("646bae490e5a37458856d10d")

# with 1 inferce ORG2
PROMPT_ID3 = ObjectId("6468b05c1e5a374588560000")
PROMPT_VERSION_ID3 = ObjectId("646bae490e5a374588511111")

LIVE_PROMPT_VERSION_DB: Dict[str, Any] = {
    "_id": ObjectId("645d786f180786983c9eede6"),
    "created_at": "2023-05-15T15:46:02.051309",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "status": "Live",
    "name": "prompt v1",
    "description": "t1 desc",
    "prompt_id": PROMPT_ID1,
    "provider": "OpenAI",
    "template": [{**VALID_TEMPLATE}],
    "model_config": {"model": "gpt-5", "temperature": 0.5, "max_tokens": 100},
    "template_arg_names": ["arg1", "arg2"],
}


DRAFT_PROMPT_VERSION_DB = {
    **LIVE_PROMPT_VERSION_DB,
    "_id": ObjectId("645d786f180786983c9eede7"),
    "status": "Draft",
}

PROCESSED_INFERENCE: Dict[str, Any] = {
    "_id": ObjectId("646e2a7367fc70e33b657c7b"),
    "created_at": "2023-05-24T15:17:07.799000",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "client_ref_id": "xxx",
    "end_user_id": "mock_me_softly",
    "source": "openaidocs",
    "template_args": {"arg1": "v1", "arg2": "v2"},
    "metadata": {"meta1": "m1"},
    "request_timeout": None,
    "prompt_id": PROMPT_ID1,
    "prompt_version_id": PROMPT_VERSION_ID1,
    "prompt_version_name": "random number v1",
    "prompt_version_ids_considered": [
        ObjectId("ffffffffffffffffffffffff"),
        ObjectId("eeeeeeeeeeeeeeeeeeeeeeee"),
    ],
    "status": "Processed",
    "request": {
        "provider": "OpenAI",
        "raw_request": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.92,
            "top_p": 0.5,
            "stop": "string",
            "max_tokens": 100,
            "presence_penalty": -0.5,
            "frequency_penalty": -0.4,
            "logit_bias": {"24": -7, "42": 90},
            "messages": [
                {
                    "role": "user",
                    "content": "Give me a random number between 0 and 100. Only answer with a number",
                    "name": None,
                }
            ],
            "n": 1,
            "stream": False,
            "user": "mock_me_softly",
        },
    },
    "response": {
        "completed_at": "2023-05-24T15:17:17.802000",
        "completition_duration_seconds": 1.1,
        "is_client_connected_at_finish": True,
        "isError": False,
        "token_usage": {
            "prompt_tokens": 25,
            "completion_tokens": 1,
            "total_tokens": 26,
        },
        "raw_response": {
            "id": "mockid",
            "object": "chat.completion",
            "created": 1684779054,
            "model": "gpt-5",
            "usage": {
                "prompt_tokens": 25,
                "completion_tokens": 1,
                "total_tokens": 26,
            },
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "71",
                        "name": None,
                    },
                    "finish_reason": "stop",
                    "index": 0,
                }
            ],
        },
    },
}

PROCESSED_INFERENCE_ORG2 = {
    **PROCESSED_INFERENCE,
    "_id": "646e2a7367fc70e33b65eeee",
    "created_by_org_id": ORG_ID2,
    "prompt_id": PROMPT_ID3,
    "prompt_version_id": PROMPT_VERSION_ID3,
}

ERROR_INFERENCE = {
    "extra_field": "should be ignored when read",
    "_id": ObjectId("646e2acb67fc70e33b657c7c"),
    "created_at": "2023-05-24T15:18:35.524000",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "end_user_id": "fail_me_softly",
    "client_ref_id": None,
    "source": "openaidocs",
    "template_args": {},
    "metadata": None,
    "request_timeout": None,
    "prompt_id": PROMPT_ID2,
    "prompt_version_id": PROMPT_VERSION_ID2,
    "prompt_version_name": "random number v1",
    "prompt_version_ids_considered": [],
    "status": "CompletitionError",
    "request": {
        "provider": "OpenAI",
        "raw_request": {
            "model": "gpt-3.5-turbo",
            "temperature": None,
            "top_p": None,
            "stop": None,
            "max_tokens": 100,
            "presence_penalty": None,
            "frequency_penalty": None,
            "logit_bias": None,
            "messages": [
                {
                    "role": "user",
                    "content": "Give me a random number between 0 and 100. Only answer with a number",
                    "name": None,
                }
            ],
            "n": 1,
            "stream": False,
            "user": "fail_me_softly",
        },
    },
    "response": {
        "completed_at": "2023-05-24T15:18:45.531000",
        "completition_duration_seconds": 1.1,
        "is_client_connected_at_finish": True,
        # TODO: ignore extra fields in nested schemas. see core/test_pydantic_bases.py
        # "extra_field2": "nested extra field should be ignoreded too",
        "isError": True,
        "error": {
            "error_class": "openai.error.APIError",
            "message": "mocking error",
            "details": {
                "_message": "mocking error",
                "http_body": None,
                "http_status": None,
                "json_body": None,
                "headers": {},
                "code": None,
                "request_id": None,
                "error": None,
                "organization": None,
            },
        },
    },
}

TIMEOUT_INFERENCE = {
    "_id": ObjectId("646e2bc83e429d729096e9a3"),
    "created_at": "2023-05-24T15:22:48.248000",
    "created_by_user_id": ObjectId("aaaaaaaaaaaaaaaaaaaaaaa1"),
    "created_by_org_id": ORG_ID1,
    "client_ref_id": None,
    "end_user_id": None,
    "source": None,
    "template_args": {},
    "metadata": None,
    "request_timeout": None,
    "prompt_id": PROMPT_ID2,
    "prompt_version_id": PROMPT_VERSION_ID2,
    "prompt_version_name": "random number v1",
    "prompt_version_ids_considered": [],
    "status": "CompletitionTimeout",
    "request": {
        "provider": "OpenAI",
        "raw_request": {
            "model": "gpt-3.5-turbo",
            "temperature": None,
            "top_p": None,
            "stop": None,
            "max_tokens": 100,
            "presence_penalty": None,
            "frequency_penalty": None,
            "logit_bias": None,
            "messages": [
                {
                    "role": "user",
                    "content": "Give me a random number between 0 and 100. Only answer with a number",
                    "name": None,
                }
            ],
            "n": 1,
            "stream": False,
            "user": "timeout_me_softly",
        },
    },
    "response": {
        "completed_at": "2023-05-24T15:22:58.256000",
        "completition_duration_seconds": 1.1,
        "is_client_connected_at_finish": True,
        "isError": True,
        "error": {
            "error_class": "openai.error.Timeout",
            "message": "timeout error",
            "details": {
                "_message": "timeout error",
                "http_body": None,
                "http_status": None,
                "json_body": None,
                "headers": {},
                "code": None,
                "request_id": None,
                "error": None,
                "organization": None,
            },
        },
    },
}
