from typing import Type
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


from server.core.settings import settings
import logging

DbClient = Type[AsyncIOMotorClient]
Db = Type[AsyncIOMotorDatabase]

db_client: DbClient | None = None
db: Db | None = None


async def get_db() -> Db:
    """Return database client instance."""
    global db
    if db is None:
        await connect_db()
    if db is None:
        raise Exception("DB connection failed")
    return db


async def get_client() -> DbClient:
    """Return database client instance."""
    global db_client
    if db_client is None:
        await connect_db()
    if db_client is None:
        raise Exception("DB connection failed")
    return db_client


async def connect_db():
    """Create database connection."""
    global db_client
    global db
    logging.debug("connect_db")
    if db_client is not None:
        raise Exception("Database client is already initialized")

    db_client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = db_client[settings.MONGO_DATABASE]


async def disconnect_db():
    """Close database connection."""
    global db_client
    logging.debug("disconnect_db")
    if db_client is not None:
        db_client.close()
