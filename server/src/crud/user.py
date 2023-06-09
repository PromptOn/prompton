from pymongo.results import InsertOneResult

from src.crud.base import CrudBase

from src.schemas.user import UserInDB, UserCreate, UserUpdate

import src.core.auth as auth
from src.crud.org import org_crud


class UserCRUD(CrudBase[UserInDB, UserCreate, UserUpdate]):
    async def create(
        self, db, obj_in: UserCreate, current_user: UserInDB
    ) -> InsertOneResult:
        await org_crud.assert_item_exists(db, obj_in.org_id, current_user=current_user)

        user_data = obj_in.dict(by_alias=True, exclude_unset=True)
        user_data.pop("plain_password")
        user_data["hashed_password"] = auth.get_hashed_password(obj_in.plain_password)

        user_in_db = UserInDB(**user_data)

        user_in_db_raw = user_in_db.dict(by_alias=True, exclude_unset=False)

        insert_result = await super().create_from_raw(db, user_in_db_raw, current_user)

        return insert_result


user_crud = UserCRUD(
    db_schema=UserInDB, collection="users", org_id_check_field_name="org_id"
)
