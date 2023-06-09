from src.crud.base import CrudBase
from src.schemas.prompt import PromptInDB, PromptCreate, PromptUpdate


class PromptCRUD(CrudBase[PromptInDB, PromptCreate, PromptUpdate]):
    pass


prompt_crud = PromptCRUD(
    db_schema=PromptInDB,
    collection="prompts",
    org_id_check_field_name="created_by_org_id",
)
