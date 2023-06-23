from pymongo.results import InsertOneResult

from src.crud.base import CrudBase
from src.crud.inference import inference_crud
from src.schemas.feedback import FeedbackInDB, FeedbackCreate, FeedbackUpdate
from src.schemas.user import UserInDB


class FeedbackCRUD(CrudBase[FeedbackInDB, FeedbackCreate, FeedbackUpdate]):
    async def create(
        self, db, obj_in: FeedbackCreate, current_user: UserInDB
    ) -> InsertOneResult:
        inf = await inference_crud.get_raw(
            db,
            obj_in.inference_id,
            current_user=current_user,
            projection={"prompt_version_id": 1},
        )

        prompt_version_id = inf["prompt_version_id"]

        fb_in_raw = obj_in.dict(by_alias=True, exclude_unset=True)
        fb_in_db = self.db_schema(**fb_in_raw, prompt_version_id=prompt_version_id)

        fb_in_db_raw = fb_in_db.dict(by_alias=True, exclude_unset=False)

        insert_res = await super().create_from_raw(db, fb_in_db_raw, current_user)

        return insert_res


feedback_crud = FeedbackCRUD(
    db_schema=FeedbackInDB,
    collection="feedbacks",
    org_id_check_field_name="created_by_org_id",
)
