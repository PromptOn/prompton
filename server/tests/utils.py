"""Misc utils for tests which are easier to import from here than using confest.py fixtures"""

import copy
from enum import Enum
import re
from types import NoneType
from typing import Any, Callable, Coroutine, Dict, List, TypeVar, TypedDict
import bson
from httpx import AsyncClient, Response as HttpxResponse
from datetime import datetime


MockDBData = Dict[str, List[Dict[str, Any]]]


class TestInput(TypedDict, total=False):
    request_body: Dict[str, Any] | None | str
    request_data: Dict[str, Any] | None
    params: Dict[str, Any]
    id: str


class TestSpecMin(TypedDict):
    spec_id: str
    mock_user: Dict[str, Any] | None
    input: TestInput
    expected: Dict[str, Any] | List[Any] | int


class TestSpec(TestSpecMin, total=False):
    mock_exception: Exception
    expected_db: Dict[str, Any] | List[Any]
    expected_status_code: int


TestSpecList = List[TestSpec]

TListOrDict = TypeVar("TListOrDict", Dict[str, Any], List[Dict[str, Any]])


def remove_props(d: TListOrDict, props_to_remove: list[str] | str) -> TListOrDict:
    """Remove properties from a dict or list of dicts (recurses to list but not to the dict).
    does not mutate the passed dict."""
    if isinstance(props_to_remove, str):
        props_to_remove = [props_to_remove]

    if isinstance(d, list):
        return [remove_props(item, props_to_remove) for item in d]
    else:
        _d = copy.deepcopy(d)
        for prop in props_to_remove:
            _d.pop(prop, None)

    return _d


def format_test_specs(specs: TestSpecList):
    spec_user_tuples = [(spec, spec.get("mock_user", {})) for spec in specs]
    ids = [spec["spec_id"] for spec in specs]
    return spec_user_tuples, ids


def _mask_access_keys(org: Dict[str, Any]) -> Dict[str, Any]:
    masked_org = org.copy()
    access_keys = org.get("access_keys")
    if access_keys:
        masked_org["access_keys"] = {k: "**********" for k in access_keys.keys()}

    return masked_org


def mask_access_keys(
    orgs: List[Dict[str, Any]] | Dict[str, Any]
) -> List[Dict[str, Any]] | Dict[str, Any]:
    if isinstance(orgs, list):
        masked_orgs = []
        for org in orgs:
            masked_org = _mask_access_keys(org)
            masked_orgs.append(masked_org)

        return masked_orgs
    else:
        return _mask_access_keys(orgs)


def bson_obj_to_json(data):
    # should revisit this mayham
    if isinstance(data, bson.ObjectId):
        return str(data)
    elif isinstance(data, bson.Int64):
        return int(data)
    elif isinstance(data, bson.Timestamp) or isinstance(data, bson.DatetimeMS):
        return data.as_datetime().isoformat()
    elif isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, bson.Binary):
        raise NotImplementedError("Binary not implemented in bson_obj_to_json")
    elif isinstance(data, bson.DBRef):
        raise NotImplementedError("Binary not implemented in bson_obj_to_json")
    elif isinstance(data, bson.Regex):
        raise NotImplementedError("Regex not implemented in bson_obj_to_json")
    elif isinstance(data, bson.Code):
        raise NotImplementedError("bson.Code not implemented in bson_obj_to_json")
    elif isinstance(data, bson.MaxKey):
        raise NotImplementedError("bson.MaxKey not implemented in bson_obj_to_json")
    elif isinstance(data, bson.MinKey):
        raise NotImplementedError("bson.MinKey not implemented in bson_obj_to_json")
    elif isinstance(data, list):
        return [bson_obj_to_json(item) for item in data]
    elif isinstance(data, dict):
        return {k: bson_obj_to_json(v) for k, v in data.items()}
    elif isinstance(data, (tuple, set)):  # can be done if needed
        raise NotImplementedError("tuple and set not implemented in bson_obj_to_json")
    elif issubclass(type(data), Enum):
        return data.value
    elif isinstance(data, (int, float, str, bool, NoneType)):
        return data

    else:
        return str(data)


def bson_to_json(bson_dict: Dict[str, Any]) -> Dict[str, Any]:
    """convert ObjectIds and timestamps to str. Mostly used to prep data read from db for comparison with DeepDiff"""
    res: Dict[str, Any] = bson_obj_to_json(bson_dict)  # pyright: ignore
    return res
    # return json.loads(json.dumps(bson_dict, default=lambda o: str(o)))


def assert_base_db_records(expected_id, record):
    # we could  move these asserts to POST  test generator to simplify things
    assert record.get("created_at"), "created_at missing"
    assert record.get("_id"), "_id missing"
    assert record["_id"] == expected_id
    created_at_str = str(record["created_at"])
    datetime.fromisoformat(created_at_str)  # exception if invalid


AsyncClientMethodType = Callable[..., Coroutine[Any, Any, HttpxResponse]]
method_mapping: Dict[str, AsyncClientMethodType] = {
    "GET": AsyncClient.get,
    "PATCH": AsyncClient.patch,
    "DELETE": AsyncClient.delete,
    "PUT": AsyncClient.put,
    "POST": AsyncClient.post,
}


def get_all_endpoint_methods(app) -> List[Dict[str, str]]:
    def remove_params_from_path(path):
        return re.sub(r"{.*?}", "", path)

    end_point_methods = []

    for route in app.routes:
        if hasattr(route, "endpoint") and hasattr(route, "methods"):
            for method in route.methods:
                if method not in ["HEAD"]:
                    endpoint = {
                        "path": route.path,
                        "path_no_params": remove_params_from_path(route.path),
                        "method": method,
                    }
                    end_point_methods.append(endpoint)

    # print("get_all_endpoints =", json.dumps(end_point_methods, indent=4))
    return end_point_methods
