# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class PromptVersionProviders(str, enum.Enum):
    """
    Currently only OpenAI is supported
    """

    OPEN_AI = "OpenAI"

    def visit(self, open_ai: typing.Callable[[], T_Result]) -> T_Result:
        if self is PromptVersionProviders.OPEN_AI:
            return open_ai()
