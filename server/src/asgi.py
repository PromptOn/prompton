from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
import logging  # TODO: repleace with structlog or loguru or something else and add cloud logging
import sys

from mangum import Mangum
from fastapi.openapi.docs import get_swagger_ui_html

from src.core import database
from src.endpoints import routers


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("multipart.multipart").setLevel(logging.WARNING)

# https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title="prompton-api",
    description="API for prompton - managing full lifecycle of AI chat prompts.",
    version="0.0.1",
    docs_url=None,
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


@app.head("/")  # allow head for quick health check
@app.get("/", include_in_schema=False)
async def swagger_docs():
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.headers["Cache-Control"] = "public, max-age=600"
    return response
