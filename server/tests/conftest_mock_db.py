import json
import pytest
from bson import ObjectId
from mongomock_motor import AsyncMongoMockClient
from pymongo import ASCENDING
from copy import deepcopy
from datetime import datetime

from src.asgi import app
from src.core.database import get_db
from tests.utils import bson_to_json


@pytest.fixture
async def mock_db(request):
    params = {}

    try:
        mock_client = AsyncMongoMockClient()
        mock_db = mock_client["prompton-api-testDB"]
        await mock_db.users.create_index("email", unique=True)

        if hasattr(request, "param") and hasattr(request.param, "items"):
            params = deepcopy(request.param)  # patch bc mongomock.insert_many mutates

            for collection, records in params.items():
                for rec in records:
                    # patch b/c mongomock doesn't populate created_at
                    if not rec.get("created_at"):
                        rec["created_at"] = datetime.now().isoformat()

                    # so we can provide _id as str in test fixtures
                    if "_id" in rec and not isinstance(rec["_id"], ObjectId):
                        rec["_id"] = ObjectId(rec["_id"])

                await mock_db[collection].insert_many(records)

        app.dependency_overrides[get_db] = lambda: mock_db
        yield mock_db
    finally:
        mock_client.close()  # pyright: ignore[reportGeneralTypeIssues]
