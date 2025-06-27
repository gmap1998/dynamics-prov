import httpx
import time

url = "https://api.binance.com/api/v3/time"
response = httpx.get(url)
binance_time = response.json()["serverTime"]
local_time = int(time.time() * 1000)

offset = binance_time - local_time

print(f"Binance Time: {binance_time}")
print(f"Local Time:   {local_time}")
print(f"Offset:       {offset} ms")
