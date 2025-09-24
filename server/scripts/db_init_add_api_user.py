""" DB Creates a DB user for the API
Not in use currently because using Mongo Atlas provided user
using the env vars:
 - MONGO_DATABASE, MONGO_USER, MONGO_PASSWORD,
 - MONGO_INITDB_ADMIN_URL, MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD

NB: this is practially a duplicate of the dev DB docker init script in mongo_init_docker-dev
"""
import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


async def run():
    # some env vars are only needed here so not in server.core.settings
    #   MONGO_INITDB_ADMIN_URL, MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD
    load_dotenv()

    db_client = AsyncIOMotorClient(os.getenv("MONGO_INITDB_ADMIN_URL"))
    db = db_client[os.getenv("MONGO_DATABASE")]

    print(
        "Connected to ",
        db.name,
        " database ",
        "as",
        os.getenv("MONGO_INITDB_ROOT_USERNAME"),
    )
    print("Creating user: ", os.getenv("MONGO_USER"))

    await db.command(
        "createUser",
        os.getenv("MONGO_USER"),
        pwd=os.getenv("MONGO_PASSWORD"),
        roles=[{"role": "readWrite", "db": os.getenv("MONGO_DATABASE")}],
    )

    db.log.insert_one(
        {"message": f"{__file__}: Initial user {os.getenv('MONGO_USER')} created."}
    )


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()


# Downgrade  (not tested as not in use  for now)
async def downgrade():
    db_client = AsyncIOMotorClient(os.getenv("MONGO_INITDB_ADMIN_URL"))
    db = db_client[os.getenv("MONGO_DATABASE")]

    await db.command("dropUser", os.getenv("MONGO_USER"))
