# apigate.py 🔥 Binance API Client

import os
import time
import hmac
import hashlib
from urllib.parse import urlencode

import httpx
from dotenv import load_dotenv
from logtools import holo_wrapper


# 🔧 Load API credentials
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.binance.com"

headers = {
    "X-MBX-APIKEY": API_KEY
}


# 🔗 Currencies
# Unified list of assets available for matrix operations
CURRENCIES = [
    "USDT",
    "BTC",
    "ETH",
    "BNB",
    "DOGE",
    "USDC",
    "BRL",
    "EUR",
    "JPY",
]

def build_matrix_structure(prices: dict[str, float]) -> dict[str, dict[str, float | None]]:
    matrix = {}
    for base in CURRENCIES:
        matrix[base] = {}
        for quote in CURRENCIES:
            if base == quote:
                continue
            pair = base + quote
            matrix[base][quote] = prices.get(pair, None)
    return matrix

# 🔥 Generate all coin pairs
def generate_all_pairs(coins):
    return [f"{base}{quote}" for base in coins for quote in coins if base != quote]


ALL_PAIRS = generate_all_pairs(CURRENCIES)


# 🔐 Signature Helpers
def get_timestamp():
    return int(time.time() * 1000)


def create_signature(query_string):
    return hmac.new(
        API_SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


# 🔗 URL Generator with Signature
def create_signed_url(endpoint, params=None):
    if params is None:
        params = {}

    params["timestamp"] = get_timestamp()
    params["recvWindow"] = 5000  # Optional: extend window to prevent timing issues

    query_string = urlencode(params)
    signature = create_signature(query_string)

    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
    return url


# 🌐 Public Request
async def send_public_request(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    if params:
        url += "?" + urlencode(params)

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
    resp.raise_for_status()
    return resp.json()


# 🔐 Signed Request (Wallet, Private Endpoints)
async def send_signed_request(endpoint, params=None):
    if params is None:
        params = {}
    params["timestamp"] = int(time.time() * 1000)
    params["recvWindow"] = 5000

    query_string = urlencode(params)
    signature = hmac.new(
        API_SECRET.encode(), query_string.encode(), hashlib.sha256
    ).hexdigest()

    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)

    resp.raise_for_status()
    return resp.json()

# 📈 Market Data Fetch
@holo_wrapper
async def fetch_market_data():
    data = await send_public_request("/api/v3/ticker/24hr")

    prices = {}
    delta = {}
    pct = {}

    for item in data:
        symbol = item.get("symbol")
        if symbol in ALL_PAIRS:
            try:
                prices[symbol] = round(float(item["lastPrice"]), 8)
                delta[symbol] = round(float(item["priceChange"]), 8)
                pct[symbol] = round(float(item["priceChangePercent"]), 8)
            except (ValueError, KeyError):
                continue

    missing = [pair for pair in ALL_PAIRS if pair not in prices]
    if missing:
        print(f"[apigate] ⚠️ Missing pairs: {missing}")

    print(f"[apigate] ✅ Market fetched: {len(prices)} pairs")
    return prices, delta, pct


# 💰 Wallet Balance Fetch
@holo_wrapper
async def fetch_wallet_data():
    data = await send_signed_request("/api/v3/account")

    balances = {}
    for item in data.get("balances", []):
        asset = item["asset"]
        free = float(item["free"])
        locked = float(item["locked"])
        total = free + locked

        if asset in CURRENCIES and total > 0:
            balances[asset] = round(total, 8)

    print(f"[apigate] ✅ Wallet fetched: {len(balances)} assets")
    return balances
