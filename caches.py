# caches.py 🔥 Runtime Memory Cache

import time


# ⏱️ Metronome interval (matches frontend refresh)
METRONOME_INTERVAL = 8  # seconds


class CycleCache:
    def __init__(self):
        self.data = {
            "wallet": {},
            "benchmark": {},
            "delta": {},
            "pct": {},
            "id_percent": {},
            "quantid": {},
            "timestamp": None,
            "last_cycle_time": 0
        }

    def save(self, wallet, cycle_matrix, timestamp):
        self.data["wallet"] = wallet
        self.data.update(cycle_matrix)
        self.data["timestamp"] = timestamp
        self.data["last_cycle_time"] = time.time()
        print(f"[caches] 💾 Cache saved with timestamp {timestamp}")

    def load(self):
        return self.data.copy()

    def clear(self):
        for key in self.data.keys():
            self.data[key] = {} if isinstance(self.data[key], dict) else None
        self.data["last_cycle_time"] = 0
        print("[caches] 🔥 Cache cleared")

    def is_expired(self):
        now = time.time()
        last = self.data.get("last_cycle_time", 0)
        return (now - last) >= METRONOME_INTERVAL

    def __getitem__(self, item):
        return self.data.get(item, None)


# 🔥 Singleton cache instance
cache = CycleCache()


# 🔥 Metronome lock check
def can_run_cycle():
    now = time.time()
    last = cache.data.get("last_cycle_time", 0)
    if (now - last) >= METRONOME_INTERVAL:
        cache.data["last_cycle_time"] = now
        return True
    return False


# 💾 Save full snapshot
def save_full_cache(wallet, cycle_matrix, timestamp):
    cache.save(wallet, cycle_matrix, timestamp)


# 🔥 Retrieve current cache
def get_full_cache():
    return cache.load()


# 🔥 Clear cache completely
def clear_cache():
    cache.clear()
