from src.crud.base import CrudBase
from src.schemas.org import OrgInDB, OrgCreate, OrgUpdate


class OrgCRUD(CrudBase[OrgInDB, OrgCreate, OrgUpdate]):
    pass


org_crud = OrgCRUD(db_schema=OrgInDB, collection="orgs", org_id_check_field_name="_id")
