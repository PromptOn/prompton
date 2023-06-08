from bson import ObjectId
from pymongo.results import InsertOneResult


from server.crud.base import CrudBase
from server.core.templateProcessing import get_populated_template

from server.crud.promptVersion import promptVersion_crud
from server.endpoints.endpoint_exceptions import EndPointValidationError
from server.schemas.inference import (
    InferenceInDB,
    InferenceCreate,
    InferenceRequestData,
    InferenceUpdate,
)
from server.schemas.openAI import ChatGPTChatCompletitionRequest
from server.schemas.promptVersion import PromptVersionStatus
from server.schemas.user import UserInDB


class InferenceCRUD(CrudBase[InferenceInDB, InferenceCreate, InferenceUpdate]):
    async def create(
        self, db, obj_in: InferenceCreate, current_user: UserInDB
    ) -> InsertOneResult:
        update_data_obj = await self.process_create_data(
            db, current_user=current_user, obj_in=obj_in
        )
        update_raw = update_data_obj.dict(by_alias=True)
        update_res = await super().create_from_raw(db, update_raw, current_user)

        return update_res

    async def process_create_data(
        self, db, *, current_user: UserInDB, obj_in: InferenceCreate
    ) -> InferenceInDB:
        promptVersion = await promptVersion_crud.get(
            db, obj_in.prompt_version_id, current_user=current_user
        )  # raises ItemNotFound HTTP if not found or not permitted

        if promptVersion.status == PromptVersionStatus.DRAFT:
            raise EndPointValidationError(
                "Inference on promptVersion in Draft `status` is not allowed. Change the status of promptVersion to Testing or Live first"
            )

        template_pop = None

        if obj_in.template_args is None:
            template_pop = promptVersion.template
        else:
            template_pop = get_populated_template(
                promptVersion.template, obj_in.template_args
            )

        raw_request = ChatGPTChatCompletitionRequest.parse_obj(
            {
                **promptVersion.model_config.dict(),
                "messages": template_pop,
                "user": obj_in.end_user_id,
            }
        )

        inference_request_data = InferenceRequestData(
            provider=promptVersion.provider,
            raw_request=raw_request,
        )

        inferenceDB = InferenceInDB(
            prompt_id=promptVersion.prompt_id,
            prompt_version_id=obj_in.prompt_version_id,
            prompt_version_name=promptVersion.name,
            end_user_id=obj_in.end_user_id,
            source=obj_in.source,
            template_args=obj_in.template_args,
            metadata=obj_in.metadata,
            request=inference_request_data,
            request_timeout=obj_in.request_timeout,
            response=None,
        )

        return inferenceDB


inference_crud = InferenceCRUD(
    db_schema=InferenceInDB,
    collection="inferences",
    org_id_check_field_name="created_by_org_id",
)
