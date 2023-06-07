import copy
import string
from typing import Set
from server.schemas.openAI import ChatGPTMessageTemplate, ChatGPTMessage


class TemplateString(string.Template):
    """we only allow ${arg_name} style. (no $arg_name). Escape is double $${"""

    delimiter = "$"
    idpattern = None  # type: ignore[assignment]
    braceidpattern = r"(?a:[_a-z][_a-z0-9]*)"


def get_arg_identifiers(template: ChatGPTMessageTemplate):
    """Return a list of all the identifiers in the template, i.e ${arg_name1} and ${arg_name2} etc."""
    res: Set[str] = set()

    if template is not None:
        for msg in template:
            for key, val in msg:
                if val is not None:
                    res.update(TemplateString(val).get_identifiers())

    return list(res)


def get_populated_template(template: ChatGPTMessageTemplate, args: dict[str, str]):
    res: ChatGPTMessageTemplate = []

    if template is not None and args is not None:
        for msg in template:
            res.append(
                ChatGPTMessage(
                    **{
                        key: None
                        if val is None
                        else TemplateString(val).safe_substitute(args)
                        for key, val in msg
                    }  # type: ignore[arg-type]
                )
            )
    if args is None:
        res = copy.deepcopy(template)

    return res
