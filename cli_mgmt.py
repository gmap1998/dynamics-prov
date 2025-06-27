import asyncio
import sys
from db_mgmt import (
    get_last_matrix,
    get_last_cycle,
    matrices_exist,
    load_cycle_by_timestamp,
    count_documents,
    list_collections,
    create_indexes,
    drop_collection,
    purge_test_data,
    db_healthcheck
)


# 🚀 Command Router
async def main():
    if len(sys.argv) < 2:
        print("[cli_mgmt] ❌ No command provided.")
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        collections = await list_collections()
        print("📜 Collections:", collections)

    elif command == "health":
        health = await db_healthcheck()
        print("🩺 DB Health Snapshot:", health)

    elif command == "last-matrix":
        doc = await get_last_matrix()
        print("🔍 Last Matrix:", doc)

    elif command == "last-cycle":
        doc = await get_last_cycle()
        print("🔍 Last Cycle:", doc)

    elif command == "count":
        if len(sys.argv) < 3:
            print("[cli_mgmt] ❌ Provide collection name.")
            return
        coll = sys.argv[2]
        count = await count_documents(coll)
        print(f"🔢 {coll} has {count} documents")

    elif command == "drop":
        if len(sys.argv) < 3:
            print("[cli_mgmt] ❌ Provide collection name.")
            return
        coll = sys.argv[2]
        await drop_collection(coll)

    elif command == "purge":
        await purge_test_data()

    elif command == "indexes":
        await create_indexes()

    elif command == "exists":
        exists = await matrices_exist()
        print(f"🔍 Matrices exist: {exists}")

    elif command == "load":
        if len(sys.argv) < 3:
            print("[cli_mgmt] ❌ Provide timestamp.")
            return
        ts = sys.argv[2]
        doc = await load_cycle_by_timestamp(ts)
        print(f"🔍 Cycle for {ts}:", doc)

    else:
        print(f"[cli_mgmt] ❌ Unknown command: {command}")
        print_help()


# 📜 Help Menu
def print_help():
    print("""
[cli_mgmt] Available Commands:
- list                  → List all collections
- health                → DB health snapshot
- last-matrix           → Show last matrix document
- last-cycle            → Show last cycle document
- count [collection]    → Count documents in collection
- drop [collection]     → Drop a collection
- purge                 → Purge test data (timestamp starting 'test')
- indexes               → Create indexes
- exists                → Check if matrices exist
- load [timestamp]      → Load cycle by timestamp
""")


# 🏁 Entry Point
if __name__ == "__main__":
    asyncio.run(main())
