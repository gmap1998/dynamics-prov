import argparse
import asyncio
from db_mongo import purge_cycles, load_latest_cycle, setup_indexes
from caches import reset_cache
from strategy import (
    get_strategy_config,
    set_strategy_config,
    get_strategy_aux
)
from pprint import pprint


# === 🔥 Async CLI Utilities ===
async def show_latest_cycle():
    data = load_latest_cycle()
    pprint(data)


async def show_strategy_config():
    from db_mongo import get_async_db
    db = get_async_db()
    config = await get_strategy_config(db)
    pprint(config.dict())


async def set_strategy_args(args):
    from db_mongo import get_async_db
    db = get_async_db()
    result = await set_strategy_config(
        db,
        config=args
    )
    print(result)


async def show_strategy_aux():
    from db_mongo import get_async_db
    db = get_async_db()
    data = await get_strategy_aux(db)
    pprint([entry.dict() for entry in data])


# === 🚦 Main CLI Entrypoint ===
def main():
    parser = argparse.ArgumentParser(description="🔥 Dynamics CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # === DB Commands ===
    parser_purge = subparsers.add_parser("purge", help="Purge DB")
    parser_purge.add_argument("--confirm", action="store_true")

    subparsers.add_parser("init", help="Initialize DB indexes")
    subparsers.add_parser("inspect", help="Show latest cycle")
    subparsers.add_parser("reset-cache", help="Clear local cache")

    # === Strategy Commands ===
    subparsers.add_parser("show-strategy", help="Show strategy config")
    parser_set_strategy = subparsers.add_parser("set-strategy", help="Set strategy config")
    parser_set_strategy.add_argument("--tier", required=True)
    parser_set_strategy.add_argument("--mode", required=True)
    parser_set_strategy.add_argument("--imprint", type=float, default=1.0)
    parser_set_strategy.add_argument("--luggage", type=float, default=1.0)

    subparsers.add_parser("show-aux", help="Show strategy aux table")

    args = parser.parse_args()

    if args.command == "purge":
        if args.confirm:
            purge_cycles(confirm=True)
        else:
            print("⚠️ Purge aborted. Pass --confirm to execute.")

    elif args.command == "init":
        setup_indexes()

    elif args.command == "inspect":
        asyncio.run(show_latest_cycle())

    elif args.command == "reset-cache":
        reset_cache()

    elif args.command == "show-strategy":
        asyncio.run(show_strategy_config())

    elif args.command == "set-strategy":
        from pydantic import BaseModel

        class ArgsAsConfig(BaseModel):
            tier: str
            mode: str
            expectedImprint: float
            expectedLuggage: float

        config = ArgsAsConfig(
            tier=args.tier,
            mode=args.mode,
            expectedImprint=args.imprint,
            expectedLuggage=args.luggage
        )
        asyncio.run(set_strategy_args(config))

    elif args.command == "show-aux":
        asyncio.run(show_strategy_aux())

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
