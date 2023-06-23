from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute

from src.endpoints.status import router as statusRouter
from src.endpoints.prompts import router as promptsRouter
from src.endpoints.promptVersions import router as promptVersionsRouter
from src.endpoints.inferences import router as inferencesRouter
from src.endpoints.token_login import router as tokenRouter
from src.endpoints.orgs import router as orgsRouter
from src.endpoints.users import router as usersRouter
from src.endpoints.feedbacks import router as feedbackRouter


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.

    See: https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


all_routers = APIRouter()
all_routers.include_router(statusRouter)
all_routers.include_router(tokenRouter)
all_routers.include_router(promptsRouter)
all_routers.include_router(promptVersionsRouter)
all_routers.include_router(inferencesRouter)
all_routers.include_router(orgsRouter)
all_routers.include_router(usersRouter)
all_routers.include_router(feedbackRouter)
