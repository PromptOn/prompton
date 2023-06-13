import random
from pymongo.results import InsertOneResult


from src.crud.base import CrudBase
from src.core.templateProcessing import get_populated_template

from src.crud.promptVersion import promptVersion_crud
from src.endpoints.endpoint_exceptions import (
    EndPointValidationError,
    ItemNotFoundException,
)
from src.schemas.base import PyObjectId
from src.schemas.inference import (
    InferenceInDB,
    InferenceCreateByPromptVersionId,
    InferenceCreateByPromptId,
    InferenceRequestData,
    InferenceUpdate,
)
from src.schemas.openAI import ChatGPTChatCompletitionRequest
from src.schemas.promptVersion import PromptVersionStatus
from src.schemas.user import UserInDB


class InferenceCRUD(
    CrudBase[InferenceInDB, InferenceCreateByPromptVersionId, InferenceUpdate]
):
    async def create(
        self,
        db,
        obj_in: InferenceCreateByPromptVersionId | InferenceCreateByPromptId,
        current_user: UserInDB,
    ) -> InsertOneResult:
        update_data_obj = await self.process_create_data(
            db, current_user=current_user, obj_in=obj_in
        )
        update_raw = update_data_obj.dict(by_alias=True)
        update_res = await super().create_from_raw(db, update_raw, current_user)

        return update_res

    async def process_create_data(
        self,
        db,
        *,
        current_user: UserInDB,
        obj_in: InferenceCreateByPromptVersionId | InferenceCreateByPromptId,
    ) -> InferenceInDB:
        selected_prompt_version_id: PyObjectId | None = None
        prompt_version_ids_considered = []

        if isinstance(obj_in, InferenceCreateByPromptVersionId):
            selected_prompt_version_id = obj_in.prompt_version_id

        else:
            # Random pick from LIVE prompt versions with the given prompt_id
            prompt_versions_results = await promptVersion_crud.get_multi_raw(
                db,
                current_user,
                filter={
                    "prompt_id": obj_in.prompt_id,
                    "status": PromptVersionStatus.LIVE.value,
                },
                projection={"_id": 1},
            )

            if prompt_versions_results == []:
                raise ItemNotFoundException(
                    f"No { PromptVersionStatus.LIVE.value} promptVersions found for prompt_id: {obj_in.prompt_id}"
                )

            prompt_version_ids_considered = [d["_id"] for d in prompt_versions_results]

            random_index = random.randint(0, len(prompt_version_ids_considered) - 1)
            selected_prompt_version_id = prompt_version_ids_considered[random_index]

            prompt_version_ids_considered.pop(random_index)

            if selected_prompt_version_id is None:
                raise Exception(
                    f"Received None _id from promptVersions query for prompt_id: {obj_in.prompt_id} "
                )

        prompt_version = await promptVersion_crud.get(
            db, selected_prompt_version_id, current_user=current_user
        )  # raises ItemNotFound HTTP if not found or not permitted

        if prompt_version.status == PromptVersionStatus.DRAFT:
            raise EndPointValidationError(
                "Inference on promptVersion in Draft `status` is not allowed. Change the status of promptVersion to Testing or Live first"
            )

        template_pop = None

        if obj_in.template_args is None:
            template_pop = prompt_version.template
        else:
            template_pop = get_populated_template(
                prompt_version.template, obj_in.template_args
            )

        raw_request = ChatGPTChatCompletitionRequest.parse_obj(
            {
                **prompt_version.model_config.dict(),
                "messages": template_pop,
                "user": obj_in.end_user_id,
            }
        )

        inference_request_data = InferenceRequestData(
            provider=prompt_version.provider,
            raw_request=raw_request,
        )

        inferenceDB = InferenceInDB(
            prompt_id=prompt_version.prompt_id,
            prompt_version_id=selected_prompt_version_id,
            prompt_version_name=prompt_version.name,
            prompt_version_ids_considered=prompt_version_ids_considered,
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
