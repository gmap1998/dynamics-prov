# execution_controller.py 🔥 Cycle Runner & Metronome Lock

from caches import save_full_cache, get_full_cache, can_run_cycle
from cycle_op import run_cycle_build
from db_cont import save_cycle_async, load_latest_cycle
from logtools import holo_wrapper


# 🔗 Async execution runner
@holo_wrapper
async def run_cycle_execution():
    """
    🔥 Run one execution of the cycle:
    Fetch → Compute → Cache → Save to DB → Return Snapshot
    """
    if not can_run_cycle():
        print("[execution] ⏳ Metronome lock — skipping execution")
        return get_full_cache()

    print("[execution] 🔥 Running cycle...")
    wallet, cycle_matrix, timestamp = await run_cycle_build()

    # 💾 Save to cache
    save_full_cache(wallet, cycle_matrix, timestamp)

    # 💾 Save to DB
    await save_cycle_async(wallet, cycle_matrix, timestamp)

    print("[execution] ✅ Cycle complete.")
    return get_full_cache()


# 🔍 Load latest cycle from DB and push into cache
@holo_wrapper
async def load_latest_into_cache():
    """
    🔍 Fetch the latest cycle document from DB
    → Load it into cache for instant availability.
    """
    doc = await load_latest_cycle()

    if doc:
        wallet = doc.get("wallet", {})
        cycle_matrix = {
            "benchmark": doc.get("benchmark", {}),
            "delta": doc.get("delta", {}),
            "pct": doc.get("pct", {}),
            "id_percent": doc.get("id_percent", {}),
            "quantid": doc.get("quantid", {}),
        }
        timestamp = doc.get("timestamp")

        save_full_cache(wallet, cycle_matrix, timestamp)

        print("[execution] 🧠 Cache populated from DB snapshot.")
    else:
        print("[execution] ⚠️ No cycle found in DB to populate cache.")

