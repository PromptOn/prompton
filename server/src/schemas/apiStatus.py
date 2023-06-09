from src.schemas.base import MyBaseModel


class DBStatus(MyBaseModel):
    status_code: int
    status_message: str


class ApiStatusResponse(MyBaseModel):
    version: str
    message: str
    dbstatus: DBStatus
    github_sha: str | None
    github_env: str | None
