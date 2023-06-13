from typing import Any, Dict, Generic, List, Type, TypeVar
from bson import ObjectId

from pydantic import BaseModel
from pymongo import ReturnDocument
from pymongo.results import InsertOneResult, UpdateResult


from src.core.utils import to_ObjectId
from src.endpoints.endpoint_exceptions import (
    ItemNotFoundException,
    NoItemUpdatedException,
)
from src.schemas.base import MongoBase
from src.schemas.user import UserInDB, UserRoles


DBModelType = TypeVar("DBModelType", bound=MongoBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
UpdateResponseSchemaType = TypeVar("UpdateResponseSchemaType", bound=BaseModel)

# TODO: catch pymongo.errors.ServerSelectionTimeoutError and return 503


class CrudBase(
    Generic[
        DBModelType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    def __init__(
        self,
        db_schema: Type[DBModelType],
        collection: str,
        org_id_check_field_name: str | None = None,
    ):
        """
        Base class with default CRUD methods in DB.
        If org_id_check_field_name is provided, then all operations are filtered by the current_user's org_id
        """
        self.db_schema = db_schema
        self.collection = collection
        self.org_id_check_field_name = org_id_check_field_name

    async def get_raw(
        self, db, id: str | ObjectId, current_user: UserInDB | None = None
    ) -> dict[str, Any]:
        """Returns a one item by id as a dict from the database"""

        filter_with_permissions = self._add_org_id_filter(
            current_user, {"_id": to_ObjectId(id)}
        )

        if (
            item := await db[self.collection].find_one(filter_with_permissions)
        ) is None:
            raise ItemNotFoundException(id, self.collection)

        return item

    async def get(
        self, db, id: str | ObjectId, current_user: UserInDB | None = None
    ) -> DBModelType:
        """Returns a one item by id as Pydantic object from the database"""

        item_raw = await self.get_raw(db, id, current_user)

        item = self.db_schema.parse_obj(item_raw)

        return item

    async def find_one(self, db, filter: dict[str, Any]) -> DBModelType | None:
        """Returns a one item by filter as Pydantic object from the database
        Returns None if no item found"""
        item_raw = await db[self.collection].find_one(filter)

        if item_raw:
            item = self.db_schema.parse_obj(item_raw)
            return item
        else:
            return None

    async def get_multi_raw(
        self,
        db,
        current_user: UserInDB | None = None,
        *,
        filter: Dict[str, Any] | None = None,
        projection: Dict[str, Any] | None = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> List[dict[str, Any]]:
        filter_with_permissions = self._add_org_id_filter(current_user, filter)

        items = (
            await db[self.collection]
            .find(filter_with_permissions, projection=projection)
            .skip(skip)
            .limit(limit)
            .to_list(limit)
        )

        return items

    async def get_multi(
        self,
        db,
        current_user: UserInDB | None = None,
        *,
        filter: Dict[str, Any] | None = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> List[DBModelType]:
        items_raw = await self.get_multi_raw(
            db, current_user, filter=filter, skip=skip, limit=limit
        )

        items = [self.db_schema.parse_obj(item) for item in items_raw]

        return items

    async def create_from_raw(
        self, db, obj_in_raw: dict[str, Any], current_user: UserInDB
    ) -> InsertOneResult:
        """Inserts item from passed `obj_in_raw` dict and returns pymongo InsertOneResult obj with `inserted_id`

        NB: Make sure you pass `obj_in_raw` created from the DB pydantic schema to run validations, field defaults etc. defined in schema
        """
        if obj_in_raw.get("created_by_user_id") or obj_in_raw.get("created_by_org_id"):
            raise Exception(
                "create_from_raw was called with created_by_user_id or created_by_org_id set "
                + self.collection
            )

        if not obj_in_raw.get("created_at"):
            raise Exception("create_from_raw was called with created_at not set")

        obj_in_raw["created_by_user_id"] = current_user.id
        obj_in_raw["created_by_org_id"] = current_user.org_id
        insert_result = await db[self.collection].insert_one(obj_in_raw)
        #  Can insert_result.inserted_id be None/empty withtout insert_one raising ?

        return insert_result

    async def create(
        self,
        db,
        obj_in: CreateSchemaType,
        current_user: UserInDB,
    ) -> InsertOneResult:
        """Inserts item from passed `obj_in` Pydantic obj values and returns pymongo InsertOneResult obj with `inserted_id`"""

        obj_in_raw = obj_in.dict(by_alias=True, exclude_unset=True)

        obj_in_db = self.db_schema(**obj_in_raw)
        obj_in_db_raw = obj_in_db.dict(by_alias=True, exclude_unset=False)

        insert_result: InsertOneResult = await self.create_from_raw(
            db, obj_in_db_raw, current_user
        )

        return insert_result

    async def is_item_exists(
        self, db, id: str | ObjectId | None, current_user: UserInDB | None = None
    ):
        """Returns True if item exists in the collection with provided `id`
        Raises if `id` is invalid bson.ObjectId
        """
        filter_with_permissions = self._add_org_id_filter(
            current_user, {"_id": to_ObjectId(id)}
        )

        if await db[self.collection].count_documents(filter_with_permissions, limit=1):
            return True

        return False

    async def assert_item_exists(
        self, db, id: str | ObjectId | None, current_user: UserInDB | None = None
    ):
        """Raises ItemNotFoundException if item with provided `id` does not exist in the collection
        Raises if `id` is invalid bson.ObjectId
        """
        if not await self.is_item_exists(db, id, current_user):
            raise ItemNotFoundException(id, self.collection)

    async def update_from_raw(
        self,
        db,
        id: str | ObjectId,
        obj_in_raw: dict[str, Any],
        current_user: UserInDB | None = None,
    ) -> UpdateResult:
        """Updates item with passed `obj_in_raw` dict values and returns pymongo UpdateResults obj with `modified_count`
        Throws NoItemUpdatedExcpetion if no item updated
         NB: Make sure you pass `obj_in_raw` created from the DB pydantic schema to run validations, field defaults etc. defined in schema
        """
        filter_with_permissions = self._add_org_id_filter(
            current_user, {"_id": to_ObjectId(id)}
        )
        update_result: UpdateResult = await db[self.collection].update_one(
            filter_with_permissions, {"$set": obj_in_raw}
        )

        if update_result.modified_count == 0:
            raise NoItemUpdatedException(id, self.collection)

        return update_result

    async def update(
        self,
        db,
        id: str | ObjectId,
        obj_in: UpdateSchemaType,
        current_user: UserInDB | None = None,
    ) -> UpdateResult:
        """Updates item with passed `obj_in` pydantic object values and returns pymongo UpdateResults obh with `modified_count`
        Throws NoItemUpdatedExcpetion if no item updated
        """
        obj_in_raw = obj_in.dict(exclude_unset=True)

        update_result = await self.update_from_raw(db, id, obj_in_raw, current_user)

        return update_result

    async def update_from_raw_and_fetch(
        self,
        db,
        id: str | ObjectId,
        obj_in_raw: dict[str, Any],
        current_user: UserInDB | None = None,
    ) -> DBModelType:
        """Updates item with passed `obj_in_raw` dict values and returns updated Pydantic object from the database.

        Throws NoItemUpdatedExcpetion if no item updated

        NB: Make sure you create `obj_in_raw`` from the DB pydantic schema to run validations, field defaults etc. defined in schema
        """
        filter_with_permissions = self._add_org_id_filter(
            current_user, {"_id": to_ObjectId(id)}
        )
        updated_item_raw = await db[self.collection].find_one_and_update(
            filter_with_permissions,
            {"$set": obj_in_raw},
            return_document=ReturnDocument.AFTER,
        )

        if not updated_item_raw:
            raise NoItemUpdatedException(id, self.collection)

        updated_obj = self.db_schema.parse_obj(updated_item_raw)

        return updated_obj

    async def update_and_fetch(
        self,
        db,
        id: str | ObjectId,
        obj_in: UpdateSchemaType,
        current_user: UserInDB | None = None,
    ) -> DBModelType:
        """Updates item with passed pydantic object values and returns updated item from the database
        Throws NoItemUpdatedExcpetion if no item updated
        """

        obj_in_raw = obj_in.dict(exclude_unset=True)

        updated_obj = await self.update_from_raw_and_fetch(
            db, id, obj_in_raw, current_user
        )

        return updated_obj

    # def remove(self, db, *, id: int) -> DeleteResult:
    #     obj = db.query(self.model).get(id)
    #     db.delete(obj)
    #     db.commit()
    #     return obj

    def _add_org_id_filter(
        self,
        current_user: UserInDB | None,
        existig_filter: Dict[str, Any] | None = None,
    ) -> Dict[str, Any] | None:
        if self.org_id_check_field_name:
            if not current_user:  # it should not get here, Depends will raise before
                raise Exception("User must be logged in to access this resource")

            if current_user.role == UserRoles.SUPER_ADMIN:
                return existig_filter

            org_filter = {self.org_id_check_field_name: current_user.org_id}
            if existig_filter:
                return {"$and": [existig_filter, org_filter]}
            else:
                return org_filter
        else:
            return existig_filter
