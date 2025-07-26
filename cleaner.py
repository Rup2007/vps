# cleaner.py

import asyncio
from datetime import datetime, timedelta
from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DATABASE_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

async def clear_mongodb_collections_every_10_minutes():
    while True:
        try:
            expiry_time = datetime.utcnow() - timedelta(minutes=10)
            result = db.file_records.delete_many({"created_at": {"$lt": expiry_time}})
            print(f"[Cleaner] Deleted {result.deleted_count} expired documents.")
        except Exception as e:
            print(f"[Cleaner Error] {e}")
        await asyncio.sleep(600)  # Run every 10 minutes
