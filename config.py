from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # === 🔗 DB Config ===
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "dynamics_prototype"

    # === 🌐 Server Config ===
    PORT: int = 8000
    FASTAPI_ENV: str = "development"
    FASTAPI_SECRET_KEY: str = (
        "7817e749e04598aa1beb3cab3b0564c36ff4d8bbc93cdcdfd810045b7d107b11"
    )
    VITE_API_URL: str = "http://localhost:8000"

    # === 🔑 Binance API ===
    BINANCE_API_KEY: str = "YOUR_BINANCE_API_KEY"
    BINANCE_SECRET_KEY: str = "YOUR_BINANCE_SECRET_KEY"

    # === ⚙️ Backend Operational Defaults ===
    DEFAULT_TIER: str = "standard"
    DEFAULT_MODE: str = "neutral"
    DEFAULT_EXPECTED_IMPRINT: float = 1.0
    DEFAULT_EXPECTED_LUGGAGE: float = 1.0

    # === 🧭 Metadata ===
    APP_VERSION: str = "0.9.0-alpha"

    class Config:
        env_file = ".env"


settings = Settings()
