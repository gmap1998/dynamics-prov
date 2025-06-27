# main.py 🔥 FastAPI App Entry

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router

app = FastAPI(
    title="Holo Matrix API",
    version="0.1.0"
)

# 🔗 Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Include API routes
app.include_router(router)


# 🏠 Root endpoint
@app.get("/")
def read_root():
    return {"Holo": "Matrix API is running", "version": "0.1.0"}
