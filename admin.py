from fastapi import APIRouter, HTTPException
#from db_mongo import db, load_latest_cycle
from validators import validate_cycle_document, get_missing_keys
import requests

admin_router = APIRouter(prefix="/admin")


@admin_router.get("/db/inspect")
async def db_inspect():
    doc = await load_latest_cycle()
    if not doc:
        return {
            "status": "empty",
            "message": "❌ No cycle document found in database."
        }

    missing = get_missing_keys(doc)

    return {
        "status": "ok" if not missing else "error",
        "missing_keys": missing,
        "present_keys": list(doc.keys()),
        "timestamp": doc.get("timestamp"),
        "cycle_id": doc.get("cycle_id")
    }


@admin_router.get("/db/clean")
@admin_router.post("/db/clean")
async def db_clean():
    result = await db["cycle_matrices"].delete_many({})
    return {
        "status": "ok",
        "message": f"Deleted {result.deleted_count} cycle documents"
        }


@admin_router.get("/db/status")
async def db_status():
    count = await db["cycle_matrices"].count_documents({})
    return {
        "status": "ok",
        "message": f"Cycle matrix collection has {count} documents."
    }


def fetch_available_binance_pairs():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    symbols = response.json()["symbols"]
    available_pairs = {symbol["symbol"] for symbol in symbols}
    return available_pairs


def check_missing_pairs(currencies):
    available_pairs = fetch_available_binance_pairs()
    missing_pairs = []

    for base in currencies:
        for quote in currencies:
            if base == quote:
                continue
            pair = base + quote
            reverse = quote + base

            if pair not in available_pairs and reverse not in available_pairs:
                missing_pairs.append(pair)

    return missing_pairs


@admin_router.get("/binance/pairs")
def binance_pair_checker():
    currencies = ["BTC", "ETH", "BNB", "USDT", "USDC", "DOGE", "BRL", "JPY", "EUR"]
    missing = check_missing_pairs(currencies)

    return {
        "status": "ok",
        "missing_pairs": missing,
        "total_missing": len(missing)
    }

