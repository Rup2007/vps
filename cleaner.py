# cleaner.py

import asyncio
from datetime import datetime, timedelta
from pymongo import MongoClient
import os

# Load environment variables
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DATABASE_NAME")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Auto-delete files older than 10 minutes
async def clear_mongodb_collections_every_10_minutes():
    while True:
        try:
            expiry_time = datetime.utcnow() - timedelta(minutes=10)
            # 👇 This is the line you're asking about
            result = db.file_records.delete_many({"created_at": {"$lt": expiry_time}})
            print(f"[Cleaner] Deleted {result.deleted_count} expired documents.")
        except Exception as e:
            print(f"[Cleaner Error] {e}")
        await asyncio.sleep(600)  # wait for 10 minutes before repeating
