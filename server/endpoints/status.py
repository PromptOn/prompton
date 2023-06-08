from fastapi import APIRouter, Depends

from server.core.settings import settings
from server.core.database import get_db
from server.schemas import apiStatus
from server.core.database import get_db

router = APIRouter()


@router.get(
    "/status", response_model=apiStatus.ApiStatusResponse, tags=["Server status"]
)
async def get_status(db=Depends(get_db)) -> apiStatus.ApiStatusResponse:
    # TODO: proper db status check + handling exceptions including timeout.  move it to a health endpoint & figure what's to show on /
    dbstatus: apiStatus.DBStatus
    if db is None:
        dbstatus = apiStatus.DBStatus(status_code=0, status_message="not connected")
    else:
        dbstatus = apiStatus.DBStatus(
            status_code=1,
            status_message=str(await db.command("ping")),
        )

    status = apiStatus.ApiStatusResponse(
        version="0.0.1",
        message="prompton-api is running",
        dbstatus=dbstatus,
        github_sha=settings.GITHUB_SHA,
        github_env=settings.GITHUB_ENV,
    )
    return status
