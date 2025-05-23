import os
import asyncio
from datetime import datetime
from typing import Optional

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

from utilities.constructor import construct_day
from utilities.types import DayModel

load_dotenv()

async def connect_db() -> Optional[AsyncIOMotorDatabase]:
    url = os.getenv('MONGO_URL')
    print(f"[connect_db] url is {url}")
    if url:
        try:
            client: AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(url)
            db: AsyncIOMotorDatabase | None = client['wordweb']

            await db.command('ping')
            print('Successfully connected to the database.')
            return db
        except PyMongoError as e:
            print('Internal server error:', e)
            return None
    else:
        print('Error retrieving URL from environment variables.')
        return None


async def get_existing_day_model(db: AsyncIOMotorDatabase, day: str) -> Optional[DayModel]:
    try:
        print(f"[get_existing_day_model] Looking for existing model with day = {day}")
        document = await db.wordwebs.find_one({"daylist_id": day})
        if document:
            print(f"[get_existing_day_model] Found existing document: {document}")
            return DayModel(**document)
        else:
            print(f"[get_existing_day_model] No existing document found for day = {day}")
            return None
    except PyMongoError as e:
        print(f"[get_existing_day_model] MongoDB error: {e}")
        return None
    except Exception as e:
        print(f"[get_existing_day_model] Unexpected error: {e}")
        return None


async def save_day_model(db: AsyncIOMotorDatabase, day_model: DayModel) -> Optional[DayModel]:
    now = datetime.now().strftime("%Y_%m_%d")
    print(f"[save_day_model] time is {now}")
    try:
        existing = await get_existing_day_model(db, now)
        if existing:
            print("[save_day_model] Day model already exists, returning existing.")
            return existing

        day_dict = day_model.model_dump(exclude_none=True)
        print(f"[save_day_model] Inserting new model: {day_dict}")
        result = await db.wordwebs.insert_one(day_dict)

        if result.inserted_id:
            print("[save_day_model] SUCCESSFULLY INSERTED MODEL!")
            return day_model
        else:
            print("[save_day_model] Failed to insert day model")
            return None
    except PyMongoError as e:
        print(f"[save_day_model] MongoDB error: {e}")
        return None
    except Exception as e:
        print(f"[save_day_model] Unexpected error: {e}")
        return None


async def store_list_model() -> Optional[DayModel]:
    db: Optional[AsyncIOMotorDatabase| None]  = await connect_db()
    if db is None:
        print("[store_list_model] Could not connect to DB")
        return None

    try:
        print("[store_list_model] Constructing day model...")
        result: Optional[DayModel] = await construct_day()

        if not result:
            print("[store_list_model] Could not construct a valid DayModel.")
            return None

        print(f"[store_list_model] Got DayModel: {result}")
        saved_model = await save_day_model(db, result)
        return saved_model
    except Exception as e:
        print(f"[store_list_model] Error storing day list: {e}")
        return None


if __name__ == "__main__":
    test_result = asyncio.run(store_list_model())
    print(f"[main] Final result: {test_result}")
