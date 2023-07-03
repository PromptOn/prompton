"""Performs initial setup of the database:
- indexes
- initial SuperAdmin user + org set in env vars:
   - PROMPTON_ORG_NAME, PROMPTON_ORG_OPENAI_API_KEY
   - PROMPTON_USER_EMAIL, PROMPTON_USER_PASSWORD_HASH
Should be part of a db migrations system when we have more than one migration to run.

NB: this is practically a duplicate of the dev DB docker init scripts in mongo_init_docker-dev
"""
import asyncio
import os
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from datetime import datetime
from dotenv import load_dotenv

from src.core.settings import settings
from src.core.database import get_db


async def run():
    db = await get_db()
    print("Connected to ", db.name, " database", settings.DATABASE_URL)

    # some env vars are only needed here so not in server.core.settings
    #    PROMPTON_ORG_OPENAI_API_KEY, PROMPTON_ORG_NAME, PROMPTON_USER_EMAIL, PROMPTON_USER_PASSWORD_HASH
    load_dotenv()

    print("Creating indexes")
    await db.users.create_index([("email", ASCENDING)], unique=True)

    await db.orgs.create_index([("oauth_domain", ASCENDING)])

    await db.users.create_index([("created_by_org_id", ASCENDING)])
    await db.orgs.create_index([("created_by_org_id", ASCENDING)])
    await db.prompts.create_index([("created_by_org_id", ASCENDING)])
    await db.promptVersions.create_index([("created_by_org_id", ASCENDING)])
    await db.inferences.create_index([("created_by_org_id", ASCENDING)])
    await db.feedbacks.create_index([("created_by_org_id", ASCENDING)])

    await db.promptVersions.create_index([("prompt_id", ASCENDING)])

    await db.inferences.create_index([("prompt_id", ASCENDING)])
    await db.inferences.create_index([("prompt_version_id", ASCENDING)])
    await db.inferences.create_index([("end_user_id", ASCENDING)])
    await db.inferences.create_index([("client_ref_id", ASCENDING)])

    await db.feedbacks.create_index([("inference_id", DESCENDING)])
    await db.feedbacks.create_index([("prompt_version_id", DESCENDING)])
    await db.feedbacks.create_index([("created_by_user_id", ASCENDING)])

    print("Adding inital user: ", os.getenv("PROMPTON_USER_EMAIL"))
    org = {
        "created_at": datetime.utcnow(),
        "created_by_user_id": ObjectId("000000000000000000000000"),
        "created_by_org_id": ObjectId("000000000000000000000000"),
        "name": os.getenv("PROMPTON_ORG_NAME"),
        "access_keys": {"openai_api_key": os.getenv("PROMPTON_ORG_OPENAI_API_KEY")},
    }

    res = await db.orgs.insert_one(org)

    user = {
        "created_at": datetime.utcnow(),
        "created_by_user_id": ObjectId("000000000000000000000000"),
        "created_by_org_id": res.inserted_id,
        "org_id": res.inserted_id,
        "role": "SuperAdmin",
        "email": os.getenv("PROMPTON_USER_EMAIL"),
        "hashed_password": os.getenv("PROMPTON_USER_PASSWORD_HASH"),
    }

    await db.users.insert_one(user)


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()


# Downgrade  (not tested as not in use  for now)
async def downgrade():
    db = await get_db()

    index_drop_tasks = [
        db.users.drop_index("email_1"),
        db.users.drop_index("created_by_org_id_1"),
        db.orgs.drop_index("created_by_org_id_1"),
        db.prompts.drop_index("created_by_org_id_1"),
        db.promptVersions.drop_index("created_by_org_id_1"),
        db.inferences.drop_index("created_by_org_id_1"),
        db.promptVersions.drop_index("prompt_id_1"),
        db.inferences.drop_index("prompt_id_1"),
        db.inferences.drop_index("prompt_version_id_1"),
    ]

    await asyncio.gather(*index_drop_tasks)

    doc_delete_tasks = [
        db.users.delete_one({"email": os.getenv("PROMPTON_USER_EMAIL")}),
        db.orgs.delete_one({"name": os.getenv("PROMPTON_ORG_NAME")}),
    ]

    await asyncio.gather(*doc_delete_tasks)
