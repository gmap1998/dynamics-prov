# matrix_utils.py 🔥 Matrix Operations and Calculations

from typing import Dict, Optional


# === ⚙️ Types ===
Matrix = Dict[str, Dict[str, Optional[float]]]


# === 🛡️ Safe Division ===
def safe_divide(numerator: float, denominator: float) -> Optional[float]:
    if denominator is None or denominator == 0:
        return None
    return round(numerator / denominator, 8)


# === 🔄 Invert flat price pairs (BTCUSDT → USDTBTC) ===
def invert_prices(prices: Dict[str, float]) -> Dict[str, float]:
    inverses = {}
    for pair, price in prices.items():
        base, quote = split_pair(pair)
        if base and quote:
            inverse_pair = f"{quote}{base}"
            try:
                inverses[inverse_pair] = round(1 / price, 8) if price else None
            except ZeroDivisionError:
                inverses[inverse_pair] = None
    return inverses


# === 🔀 Convert flat pair dict → nested matrix {base: {quote: value}} ===
def convert_flat_to_nested(flat: Dict[str, float]) -> Matrix:
    nested: Matrix = {}
    for pair, value in flat.items():
        base, quote = split_pair(pair)
        if base and quote:
            nested.setdefault(base, {})[quote] = value
    return nested


# === 🔢 Split pair string into (base, quote) ===
def split_pair(pair: str) -> tuple[Optional[str], Optional[str]]:
    known = ["BTC", "ETH", "BNB", "DOGE", "USDC", "USDT", "BRL", "EUR", "JPY"]
    for coin in known:
        if pair.startswith(coin):
            other = pair[len(coin):]
            if other in known and coin != other:
                return coin, other
    return None, None


# === 📈 Compute id_percent matrix ===
def compute_id_percent(
    current: Matrix, benchmark: Matrix, coins: list
) -> Matrix:
    result: Matrix = {}
    for base in coins:
        result[base] = {}
        for quote in coins:
            if base == quote:
                continue
            c = current.get(base, {}).get(quote)
            b = benchmark.get(base, {}).get(quote)
            result[base][quote] = (
                safe_divide((c - b), b) if c is not None and b else None
            )
    return result


# === 📈 Compute quantid matrix ===
def compute_quantid(
    id_percent: Matrix, delta: Matrix, coins: list
) -> Matrix:
    result: Matrix = {}
    for base in coins:
        result[base] = {}
        for quote in coins:
            if base == quote:
                continue
            idp = id_percent.get(base, {}).get(quote)
            dlt = delta.get(base, {}).get(quote)
            if idp is not None and dlt is not None:
                result[base][quote] = round(((idp + 1) * dlt), 8)
            else:
                result[base][quote] = None
    return result


# === 🏷️ Format for Display (Frontend) ===
def format_for_display(matrix: Matrix) -> dict:
    """Replace None with '—' for frontend."""
    display = {}
    for base, quotes in matrix.items():
        display[base] = {}
        for quote, value in quotes.items():
            if value is None:
                display[base][quote] = "—"
            else:
                display[base][quote] = (
                    round(value, 6) if isinstance(value, float) else value
                )
    return display
