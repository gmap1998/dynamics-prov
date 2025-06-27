# routers.py 🔥 API Endpoints

from fastapi import APIRouter, HTTPException
from execution_controller import run_cycle_execution, load_latest_into_cache
from apigate import fetch_market_data, fetch_wallet_data
from caches import get_full_cache
from db_cont import list_timestamps
from logtools import holo_wrapper

router = APIRouter(
    prefix="/api",
    tags=["HoloAPI"]
)


# 🚀 Run Cycle
@router.post("/cycle/run")
@holo_wrapper
async def run_cycle():
    result = await run_cycle_execution()
    return {"status": "success", "data": result}


# 📥 Load latest cycle into cache
@router.get("/cycle/load_latest")
@holo_wrapper
async def load_latest():
    await load_latest_into_cache()
    return {"status": "cache updated"}


# 📊 Dashboard Snapshot
@router.get("/dashboard")
@holo_wrapper
async def get_dashboard():
    cache = get_full_cache()
    if not cache or not cache.get("timestamp"):
        raise HTTPException(status_code=404, detail="Cache is empty")
    return cache


# 💰 Wallet Snapshot (live fetch)
@router.get("/wallet")
@holo_wrapper
async def get_wallet():
    wallet = await fetch_wallet_data()
    return wallet


# 📈 Market Snapshot (live fetch)
@router.get("/market")
@holo_wrapper
async def get_market():
    prices, delta, pct = await fetch_market_data()
    return {"benchmark": prices, "delta": delta, "pct": pct}


# 🩺 API Status & Cache Status
@router.get("/status")
@holo_wrapper
async def api_status():
    cache = get_full_cache()
    timestamps = await list_timestamps()
    return {
        "cache": {
            "timestamp": cache.get("timestamp"),
            "wallet": bool(cache.get("wallet")),
            "matrix": bool(cache.get("benchmark")),
            "id_percent": bool(cache.get("id_percent")),
            "delta": bool(cache.get("delta")),
            "quantid": bool(cache.get("quantid")),
        },
        "db": {
            "cycle_count": len(timestamps),
            "latest_timestamp": timestamps[0] if timestamps else None,
        }
    }
# 🚀 Matrix by Type
@router.get("/matrix/{matrix_type}")
@holo_wrapper
async def get_matrix_by_type(matrix_type: str):
    valid_types = ["benchmark", "delta", "pct", "id_percent", "quantid"]

    if matrix_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid matrix type. Valid types are: {valid_types}"
        )

    cache = get_full_cache()
    if not cache or not cache.get("timestamp"):
        raise HTTPException(status_code=404, detail="Cache is empty")

    matrix = cache.get(matrix_type)
    if matrix is None:
        raise HTTPException(
            status_code=404,
            detail=f"Matrix '{matrix_type}' not found in cache"
        )

    return {
        "matrix_type": matrix_type,
        "timestamp": cache.get("timestamp"),
        "matrix": matrix
    }
