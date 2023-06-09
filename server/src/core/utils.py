from typing import Any
from bson import ObjectId, errors as bson_errors
from fastapi import HTTPException, status


def to_ObjectId(id: Any) -> ObjectId:
    """Attempts to convert to bson ObjectId or raises HTTP_422_UNPROCESSABLE_ENTITY if id is not valid"""
    if isinstance(id, ObjectId):
        return id

    try:
        return ObjectId(id)

    except (bson_errors.InvalidId, TypeError) as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid item id supplied: {str(error)}",
        )


def str_to_ObjectId(id: str) -> ObjectId:
    """Converts string to bson ObjectId or raises HTTP_422_UNPROCESSABLE_ENTITY if id is not valid format"""
    return to_ObjectId(id)
