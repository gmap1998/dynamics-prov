# main.py 🔥 FastAPI App Entry

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router

import asyncio
from execution_controller import run_cycle_execution
from caches import METRONOME_INTERVAL

app = FastAPI(
    title="Holo Matrix API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
async def start_cycle_scheduler():
    async def cycle_loop():
        while True:
            await run_cycle_execution()
            await asyncio.sleep(METRONOME_INTERVAL)
    asyncio.create_task(cycle_loop())

@app.get("/")
def read_root():
    return {"Holo": "Matrix API is running", "version": "0.1.0"}
