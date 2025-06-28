# cycle_op.py

from apigate import fetch_market_data, fetch_wallet_data, CURRENCIES
from matrix_utils import (
    invert_prices,
    compute_id_percent,
    compute_quantid
)
from logtools import holo_wrapper
from datetime import datetime




# 🔥 Fetch wallet, market prices, delta %, and price change %

def build_matrix_structure(prices: dict[str, float]) -> dict[str, dict[str, float | None]]:
    matrix = {}

    for base in CURRENCIES:
        matrix[base] = {}
        for quote in CURRENCIES:
            if base == quote:
                continue  # skip self-pair
            pair = base + quote
            matrix[base][quote] = prices.get(pair, None)

    return matrix


@holo_wrapper
async def fetch_and_prepare_data():
    wallet = await fetch_wallet_data()
    prices, delta_flat, pct_flat = await fetch_market_data()
    return wallet, prices, delta_flat, pct_flat


# 🔥 Invert pairings and assemble full flat dictionaries
def assemble_flat_matrices(prices, delta_flat, pct_flat):
    inverted_prices = invert_prices(prices)
    inverted_delta = invert_prices(delta_flat)
    inverted_pct = invert_prices(pct_flat)

    benchmark_flat = {**prices, **inverted_prices}
    delta_full = {**delta_flat, **inverted_delta}
    pct_full = {**pct_flat, **inverted_pct}

    return benchmark_flat, delta_full, pct_full


# 🔥 Build full nested NxN matrix
def build_full_matrix(prices_flat: dict, assets: list[str]) -> dict:
    """
    Builds a square nested matrix of base → quote currencies.
    Fills in None for unavailable pairs and 1.0 for identity pairs.
    
    Args:
        prices_flat (dict): flat pairwise price dictionary, e.g. {"BTCUSDT": 26300.5}
        assets (list): list of assets to include in the matrix, e.g. ["BTC", "ETH", "USDT"]
    
    Returns:
        dict: nested dict of shape {base: {quote: value}}
    """
    matrix = {}

    for base in assets:
        matrix[base] = {}
        for quote in assets:
            if base == quote:
                matrix[base][quote] = 1.0
            elif f"{base}{quote}" in prices_flat:
                matrix[base][quote] = prices_flat[f"{base}{quote}"]
            elif f"{quote}{base}" in prices_flat:
                try:
                    matrix[base][quote] = 1 / prices_flat[f"{quote}{base}"]
                except ZeroDivisionError:
                    matrix[base][quote] = None
            else:
                matrix[base][quote] = None

    return matrix



# 🔥 Compute id_percent and quantid matrices
def compute_cycle_matrices(benchmark, delta, pct, currencies):
    id_percent = compute_id_percent(pct, benchmark, currencies)
    quantid = compute_quantid(id_percent, delta, currencies)
    return id_percent, quantid


# 🧠 Full assembler
@holo_wrapper
async def run_cycle_build():
    """
    🔥 Fetch data, compute matrices, assemble full cycle package.
    """
    wallet, prices, delta_flat, pct_flat = await fetch_and_prepare_data()

    benchmark_flat, delta_full, pct_full = assemble_flat_matrices(
        prices, delta_flat, pct_flat
    )

    # 🔗 Convert to full matrices ensuring all pairs are present
    benchmark = build_full_matrix(benchmark_flat, CURRENCIES)
    delta = build_full_matrix(delta_full, CURRENCIES)
    pct = build_full_matrix(pct_full, CURRENCIES)

    # 🔢 Compute derived matrices
    id_percent, quantid = compute_cycle_matrices(
        benchmark, delta, pct, CURRENCIES
    )

    # 🔥 Timestamp
    timestamp = datetime.utcnow().isoformat()

    # 🔥 Full matrix package
    cycle_matrix = {
        "benchmark": benchmark,
        "delta": delta,
        "pct": pct,
        "id_percent": id_percent,
        "quantid": quantid,
    }

    print(f"[cycle_op] ✅ Cycle built at {timestamp}")

    return wallet, cycle_matrix, timestamp
