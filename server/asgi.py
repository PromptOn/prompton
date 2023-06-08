from typing import Callable
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
import logging  # TODO: repleace with structlog or loguru or something else and add cloud logging
import sys
from starlette.responses import JSONResponse
from mangum import Mangum

from server.core import database
from server.core.settings import settings
from server.endpoints import routers
from server.schemas import underTheHood
from server.core.database import get_db


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("multipart.multipart").setLevel(logging.WARNING)

# https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title="prompton-api",
    description="API for prompton - managing full lifecycle of AI chat prompts.",
    version="0.0.1",
)

app.include_router(routers)

handler = Mangum(app)  # handler for deploy FastAPI to lambdas

# TODO: configure CORS
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.on_event("startup")
async def startup():
    logging.info(" 🚀 " + __name__ + " starting up")
    await database.connect_db()


@app.on_event("shutdown")
async def shutdown():
    logging.info(" 👋" + __name__ + " shutting down")
    await database.disconnect_db()


@app.get("/", response_model=underTheHood.ApiStatusResponse, tags=["under the hood"])
async def root(db=Depends(get_db)) -> underTheHood.ApiStatusResponse:
    # TODO: proper db status check + handling exceptions including timeout.  move it to a health endpoint & figure what's to show on /
    dbstatus: underTheHood.DBStatus
    if db is None:
        dbstatus = underTheHood.DBStatus(status_code=0, status_message="not connected")
    else:
        dbstatus = underTheHood.DBStatus(
            status_code=1,
            status_message=str(await db.command("ping")),
        )

    status = underTheHood.ApiStatusResponse(
        version="0.0.1",
        message="prompton-api is running",
        dbstatus=dbstatus,
        github_sha=settings.GITHUB_SHA,
        github_env=settings.GITHUB_ENV,
    )
    return status
