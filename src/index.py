import os
import asyncio
from datetime import datetime
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

from utilities.constructor import construct_day
from utilities.custom_types import DayModel

load_dotenv()

# ---------- Database Connection ----------
def get_db_client() -> Optional[AsyncIOMotorClient]:
    url = os.getenv('MONGO_URL')
    if not url:
        print("[get_db_client] Error: MONGO_URL not set in environment variables.")
        return None
    return AsyncIOMotorClient(url)

async def ping_db(db: AsyncIOMotorDatabase) -> bool:
    try:
        await db.command('ping')
        print("[ping_db] Successfully connected to the database.")
        return True
    except PyMongoError as e:
        print(f"[ping_db] Database connection error: {e}")
        return False

# ---------- Day Model Utilities ----------
async def get_existing_day_model(db: AsyncIOMotorDatabase, day: str) -> Optional[DayModel]:
    try:
        document = await db['word-webs'].find_one({"daylist_id": day})
        if document:
            print(f"[get_existing_day_model] Found existing document for day {day}")
            return DayModel(**document)
        else:
            print(f"[get_existing_day_model] No document found for day {day}")
            return None
    except Exception as e:
        print(f"[get_existing_day_model] Error: {e}")
        return None

async def insert_day_model(db: AsyncIOMotorDatabase, day_model: DayModel) -> Optional[DayModel]:
    try:
        result = await db['word-webs'].insert_one(day_model.model_dump(exclude_none=True))
        if result.inserted_id:
            print("[insert_day_model] Successfully inserted new day model.")
            return day_model
        else:
            print("[insert_day_model] Failed to insert day model.")
            return None
    except Exception as e:
        print(f"[insert_day_model] Error inserting day model: {e}")
        return None

# ---------- Main Flow ----------
async def store_list_model() -> Optional[DayModel]:
    client = get_db_client()
    if client is None:
        return None

    db = client['wordweb']
    if not await ping_db(db):
        return None

    today_str = datetime.now().strftime("%Y_%W")
    existing_model = await get_existing_day_model(db, today_str)
    if existing_model:
        print("[store_list_model] Returning existing day model.")
        return existing_model

    print("[store_list_model] Constructing new day model...")
    new_model = await construct_day()
    if not new_model:
        print("[store_list_model] Failed to construct day model.")
        return None

    saved_model = await insert_day_model(db, new_model)
    return saved_model

if __name__ == "__main__":
    final_result = asyncio.run(store_list_model())
    print(f"[main] Final result: {final_result}")
