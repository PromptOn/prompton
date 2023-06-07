from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from pymongo import MongoClient

import logging

from server.core.settings import settings


# motor_asyncio is not typed so we use pymongo types. motor_asyncio is a wrapper for pymongo
DbClient = MongoClient  # it's actually an AsyncIOMotorClient
Db = Database  # it's actually an AsyncIOMotorDatabase

db_client: DbClient | None = None
db: Db | None = None


async def get_db() -> Db:
    """Return database client instance."""
    if db is None:
        raise Exception("Database is not initialized")
    return db


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
