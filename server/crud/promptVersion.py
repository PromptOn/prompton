from bson import ObjectId
from pymongo.results import UpdateResult, InsertOneResult

from server.crud.base import CrudBase
from server.crud.prompt import prompt_crud
from server.core.templateProcessing import get_arg_identifiers


from server.endpoints.endpoint_exceptions import EndPointValidationError
from server.schemas.promptVersion import (
    PromptVersionInDB,
    PromptVersionCreate,
    PromptVersionUpdate,
    PromptVersionStatus,
)
from server.schemas.user import UserInDB


class PromptVersionCRUD(
    CrudBase[PromptVersionInDB, PromptVersionCreate, PromptVersionUpdate]
):
    async def create(
        self, db, obj_in: PromptVersionCreate, current_user: UserInDB
    ) -> InsertOneResult:
        await prompt_crud.assert_item_exists(
            db, obj_in.prompt_id, current_user=current_user
        )

        pv_in_raw = obj_in.dict(by_alias=True, exclude_unset=True)
        pv_in_db = self.db_schema(**pv_in_raw)

        pv_in_db.template_arg_names = pv_in_db.template_arg_names = get_arg_identifiers(
            pv_in_db.template
        )

        pv_in_db_raw = pv_in_db.dict(by_alias=True, exclude_unset=False)

        insert_res = await super().create_from_raw(db, pv_in_db_raw, current_user)

        return insert_res

    async def update(
        self,
        db,
        id: str | ObjectId,
        obj_in: PromptVersionUpdate,
        current_user: UserInDB | None = None,
    ) -> UpdateResult:
        """`template` , `model` are mandatory for non DRAFT promptVersions
        Only `status` and `description` allowed to change on non DRAFT promptVersions.
        `status` cannot set to DRAFT with update
        """
        update_data_raw = await self.process_update_data(
            db, id, obj_in, current_user=current_user
        )

        update_res = await super().update_from_raw(db, id, update_data_raw)

        return update_res

    async def update_and_fetch(
        self,
        db,
        id: str | ObjectId,
        obj_in: PromptVersionUpdate,
        current_user: UserInDB | None = None,
    ) -> PromptVersionInDB:
        if current_user is None:
            raise EndPointValidationError(
                "Not authenticated"
            )  # it should not get here if coming from endpoint

        update_data_raw = await self.process_update_data(db, id, obj_in, current_user)

        update_obj = await super().update_from_raw_and_fetch(
            db, id, update_data_raw, current_user
        )

        return update_obj

    async def process_update_data(
        self,
        db,
        id: str | ObjectId,
        obj_in: PromptVersionUpdate,
        current_user: UserInDB | None,
    ):
        """Populate calculated fields and returns raw update_data dict. raises EndPointValidationError if any validation fails"""
        # consider  disallowing any change on non Draft promptVersions if it turns out to be a pain to maintain code&tests
        update_data = obj_in.dict(by_alias=True, exclude_unset=True)

        if "prompt_id" in update_data:
            await prompt_crud.assert_item_exists(
                db, obj_in.prompt_id, current_user=current_user
            )

        if "template" in update_data:
            update_data["template_arg_names"] = get_arg_identifiers(obj_in.template)

        #  validations depending in current status
        pv_stored = await self.get(db, id=id, current_user=current_user)

        if pv_stored.status != PromptVersionStatus.DRAFT:
            if (
                "status" in update_data
                and update_data["status"] == PromptVersionStatus.DRAFT
            ):
                raise EndPointValidationError(
                    "`status` change to Draft not allowed. Create a new promptVersion instead"
                )

        MUTABLE_PROPS = ["description", "status"]
        if any(
            key not in MUTABLE_PROPS for key in update_data
        ) and pv_stored.status in [
            PromptVersionStatus.TESTING,
            PromptVersionStatus.LIVE,
            PromptVersionStatus.ARCHIVED,
        ]:
            raise EndPointValidationError(
                f"Only the change of {MUTABLE_PROPS} fields allowed on non Draft promptVersions. Create a new promptVersion instead"
            )

        # Draft -> non Draft status mandatory field checks. It's enough check if fields are present, format checks then done by PromptVersionPatch
        if (
            "status" in update_data
            and update_data.get("status") != PromptVersionStatus.DRAFT
        ):
            model_update = (
                update_data["model_config"].get("model")
                if update_data.get("model_config")
                else None
            )

            if not model_update and (
                not pv_stored.model_config or not pv_stored.model_config.model
            ):
                raise EndPointValidationError(
                    "`model_config.model` field is mandatory to change status to non Draft"
                )

            if not (update_data.get("template") or pv_stored.template):
                raise EndPointValidationError(
                    "`template` field is mandatory to change status to non Draft"
                )

        # Disabled this feature for now - it might useful but confusing UX as other nested fields work differently
        # if update_data.get("model_config") and pv_stored.model_config:
        #     # with model_config we are accepting partial updates
        #     update_data["model_config"] = {
        #         **pv_stored.model_config.dict(by_alias=True, exclude_unset=True),
        #         **update_data["model_config"],
        #     }

        return update_data  # all checks passed & fields updated, good to update


promptVersion_crud = PromptVersionCRUD(
    db_schema=PromptVersionInDB,
    collection="promptVersions",
    org_id_check_field_name="created_by_org_id",
)
