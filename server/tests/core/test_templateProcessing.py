from pydantic import parse_obj_as
import pytest

from src.core.templateProcessing import (
    get_arg_identifiers,
    get_populated_template,
)
from src.schemas.openAI import ChatGPTMessageTemplate
from tests.core.templateProcessing_test_data import (
    test_arglist_data,
    test_pop_data,
)


@pytest.mark.anyio
@pytest.mark.parametrize("test_data", test_arglist_data)
async def test_get_arg_identifiers(test_data):
    template = parse_obj_as(ChatGPTMessageTemplate, test_data["input"])

    # convert to set as order doesn't matter
    assert set(get_arg_identifiers(template)) == set(test_data["expected"])


@pytest.mark.anyio
async def test_get_arg_identifiers_none():
    assert get_arg_identifiers(None) == []  # pyright: ignore[reportGeneralTypeIssues]


@pytest.mark.anyio
@pytest.mark.parametrize("test_data", test_pop_data)
async def test_populate_template(test_data):
    template = parse_obj_as(ChatGPTMessageTemplate, test_data["input"]["template"])
    excepted = parse_obj_as(ChatGPTMessageTemplate, test_data["expected"])
    # convert to set as order doesn't matter
    assert (
        get_populated_template(template, test_data["input"]["arg_values"]) == excepted
    )
