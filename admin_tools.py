from db_mongo import (
    cycle_collection,
    setup_indexes,
    load_latest_cycle,
    matrices_exist_in_db
)
from caches import (
    save_current_delta,
    save_cache_quantid
)
from pprint import pprint


# === 🔥 Purge DB ===
def purge_cycles(confirm=False):
    if confirm:
        result = cycle_collection.delete_many({})
        print(f"🔥 Purged {result.deleted_count} cycles from DB.")
    else:
        print("⚠️ Dry run — pass confirm=True to execute purge.")


# === 🏗️ Initialize DB (Indexes) ===
def initialize_db():
    setup_indexes()
    print("✅ DB indexes created and initialized.")


# === 🔍 Inspect Latest Cycle ===
def show_latest_cycle():
    if not matrices_exist_in_db():
        print("⚠️ No cycles in DB.")
        return
    latest = load_latest_cycle()
    print("📦 Latest Cycle Matrix:")
    pprint(latest)


# === 🗑️ Reset Cache ===
def reset_cache():
    save_current_delta({})
    save_cache_quantid({})
    print("🗑️ Cache cleared.")


# === 🚀 CLI Entrypoint ===
if __name__ == "__main__":
    print("🔥 Dynamics Admin Tool")
    print("Available functions:")
    print(" - purge_cycles(confirm=True)")
    print(" - initialize_db()")
    print(" - show_latest_cycle()")
    print(" - reset_cache()")
