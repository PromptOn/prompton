import pytest

MSG = {
    "role": "system",
    "content": "${arg1} x ${arg1} z ${arg2}",
    "name": "string ${arg2} x ${arg1}",
}

test_pop_data = [
    pytest.param(
        {
            "input": {
                "arg_values": {"arg1": "v1", "arg2": "v2"},
                "template": [{**MSG}],
            },
            "expected": [
                {"role": "system", "content": "v1 x v1 z v2", "name": "string v2 x v1"}
            ],
        },
        id="base case",
    ),
    pytest.param(
        {
            "input": {
                "arg_values": {"arg1": "v1"},
                "template": [{"role": "user", "content": "${arg1} x"}],
            },
            "expected": [{"role": "user", "content": "v1 x"}],
        },
        id="missing name field",
    ),
    pytest.param(
        {
            "input": {
                "arg_values": {"arg1": "v1", "arg2": "v2"},
                "template": [
                    {"role": "system", "content": "$${arg1} x ${arg1 } z $${arg2}"}
                ],
            },
            "expected": [{"role": "system", "content": "${arg1} x ${arg1 } z ${arg2}"}],
        },
        id="Escaping",
    ),
    pytest.param(
        {
            "input": {
                "arg_values": {"arg1": "v1", "argX": "x"},
                "template": [{**MSG}],
            },
            "expected": [
                {
                    "role": "system",
                    "content": "v1 x v1 z ${arg2}",
                    "name": "string ${arg2} x v1",
                }
            ],
        },
        id="missing and extra arg",
    ),
    pytest.param(
        {
            "input": {
                "arg_values": None,
                "template": [{**MSG}],
            },
            "expected": [
                {
                    "role": "system",
                    "content": "${arg1} x ${arg1} z ${arg2}",
                    "name": "string ${arg2} x ${arg1}",
                }
            ],
        },
        id="None arg",
    ),
    pytest.param(
        {
            "input": {
                "arg_values": {},
                "template": [{**MSG}],
            },
            "expected": [
                {
                    "role": "system",
                    "content": "${arg1} x ${arg1} z ${arg2}",
                    "name": "string ${arg2} x ${arg1}",
                }
            ],
        },
        id="empty arg",
    ),
    pytest.param(
        {
            "input": {
                "arg_values": {"arg1": "v1"},
                "template": [],
            },
            "expected": [],
        },
        id="empty template",
    ),
]


test_arglist_data = [
    pytest.param(
        {
            "input": [
                {
                    "role": "system",
                    "content": "${arg1} x ${arg1} z ${arg2}",
                    "name": "string ${arg3} x ${arg2}",
                }
            ],
            "expected": ["arg1", "arg2", "arg3"],
        },
        id="all args",
    ),
    pytest.param(
        {
            "input": [
                {
                    "role": "system",
                    "content": "${arg1} x ${arg1} z ${arg2}",
                    "name": "string ${arg3} x ${arg2}",
                },
                {
                    "role": "system",
                    "content": "${arg1} x ${arg2} z",
                    "name": "blah ${arg1} x ${arg3}",
                },
            ],
            "expected": ["arg1", "arg2", "arg3"],
        },
        id="multi msgs",
    ),
    pytest.param(
        {
            "input": [
                {
                    "role": "system",
                    "content": "blah { } blah {blah}",
                    "name": "$${escaped} $arg3} x $ {arg2}",
                }
            ],
            "expected": [],
        },
        id="no args",
    ),
    pytest.param(
        {
            "input": [
                {
                    "role": "system",
                    "content": "blah ${hah}",
                }
            ],
            "expected": ["hah"],
        },
        id="no name",
    ),
    pytest.param(
        {
            "input": [],
            "expected": [],
        },
        id="empty template",
    ),
]
