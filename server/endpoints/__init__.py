from fastapi import APIRouter

from .status import router as statusRouter
from .prompts import router as promptsRouter
from .promptVersions import router as promptVersionsRouter
from .inferences import router as inferencesRouter
from .token_login import router as tokenRouter
from .orgs import router as orgsRouter
from .users import router as usersRouter

routers = APIRouter()
routers.include_router(statusRouter)
routers.include_router(tokenRouter)
routers.include_router(promptsRouter)
routers.include_router(promptVersionsRouter)
routers.include_router(inferencesRouter)
routers.include_router(orgsRouter)
routers.include_router(usersRouter)


__all__ = ["routers"]
