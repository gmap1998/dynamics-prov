# db_cont.py 🔥 Mongo Save/Load Manager

import os
from datetime import datetime
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import DESCENDING
from bson import ObjectId
from logtools import holo_wrapper


# === 🔧 Load Mongo ===
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "holo_db")

if not MONGO_URI:
    raise ValueError("⚠️ MONGO_URI not set in .env")

client = AsyncIOMotorClient(MONGO_URI)
db: AsyncIOMotorDatabase = client[DATABASE_NAME]

cycle_collection = db["cycle_matrices"]


# === 🔗 Utility: Mongo Parser ===
def parse_mongo_document(doc):
    if not doc:
        return {}
    doc = dict(doc)
    doc["_id"] = str(doc.get("_id"))
    return doc


# === 🔗 Get Async DB (for future usage) ===
def get_async_db() -> AsyncIOMotorDatabase:
    return db


# === 💾 Save Cycle ===
@holo_wrapper
async def save_cycle_async(wallet, cycle_matrix, timestamp):
    payload = {
        "wallet": wallet,
        "timestamp": timestamp,
        **cycle_matrix,
        "saved_at": timestamp,
    }
    result = await cycle_collection.insert_one(payload)
    print(f"[db_cont] ✅ Cycle saved with ID {result.inserted_id}")
    return str(result.inserted_id)


# === 🔍 Load Latest Cycle ===
@holo_wrapper
async def load_latest_cycle():
    doc = await cycle_collection.find_one(sort=[("timestamp", DESCENDING)])
    if doc:
        doc = parse_mongo_document(doc)
        print(f"[db_cont] 🔍 Loaded latest cycle {doc.get('_id')}")
    else:
        print("[db_cont] ⚠️ No cycle found in DB")
    return doc


# === 🔍 Load by Timestamp ===
@holo_wrapper
async def load_cycle_by_timestamp(ts: str):
    doc = await cycle_collection.find_one({"timestamp": ts})
    if doc:
        doc = parse_mongo_document(doc)
        print(f"[db_cont] 🔍 Loaded cycle for timestamp {ts}")
    else:
        print(f"[db_cont] ⚠️ No cycle found for timestamp {ts}")
    return doc


# === 🗒️ List Saved Timestamps ===
@holo_wrapper
async def list_timestamps():
    cursor = cycle_collection.find({}, {"timestamp": 1}).sort("timestamp", -1)
    timestamps = [doc["timestamp"] async for doc in cursor if "timestamp" in doc]
    print(f"[db_cont] 🗒️ Found {len(timestamps)} timestamps")
    return timestamps


# === 🏗️ Setup Indexes (Optional but Recommended) ===
def setup_indexes():
    cycle_collection.create_index([("timestamp", DESCENDING)])
    print("[db_cont] ✅ Index on 'timestamp' ensured")


# === ⚠️ Admin Tool: Purge Cycles ===
async def purge_cycles(confirm=False):
    if confirm:
        result = await cycle_collection.delete_many({})
        print(f"[db_cont] ⚠️ Purged {result.deleted_count} cycle matrices")
    else:
        print("[db_cont] ❌ Purge aborted. Set confirm=True to proceed.")
