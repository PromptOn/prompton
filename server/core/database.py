from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


from server.core.settings import settings
import logging


# workaround for pylance error (Illegal type annotation: variable not allowed unless it is a type alias) likely b/c motor is not typed
DbClient = Optional[AsyncIOMotorClient]
Db = Optional[AsyncIOMotorDatabase]

db_client: DbClient = None
db: Db = None


async def get_db() -> Db:
    """Return database client instance."""
    return db


async def connect_db():
    """Create database connection."""
    global db_client
    global db
    logging.debug("connect_db")
    if db_client is not None:
        raise Exception("Database client is already initialized")

    db_client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = db_client[settings.MONGO_INITDB_DATABASE]


async def disconnect_db():
    """Close database connection."""
    global db_client
    logging.debug("disconnect_db")
    if db_client is not None:
        db_client.close()


# db_client: motor.AsyncIOMotorClient = motor.AsyncIOMotorClient(settings.DATABASE_URL)
# db: motor.AsyncIOMotorDatabase = db_client[settings.MONGO_INITDB_DATABASE]


# def get_db() -> motor.AsyncIOMotorDatabase:
#     return db


# client = motor.AsyncIOMotorClient(settings.DATABASE_URL)
# db = client[settings.MONGO_INITDB_DATABASE]
