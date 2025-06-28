import functools
import time

def holo_wrapper(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        print(f"🌀 [ENTER] {func.__name__} | args={args}, kwargs={kwargs}")
        try:
            result = await func(*args, **kwargs)
            elapsed = round(time.time() - start, 4)
            print(f"✅ [EXIT] {func.__name__} | result={result} | time={elapsed}s")
            return result
        except Exception as e:
            elapsed = round(time.time() - start, 4)
            print(f"❌ [ERROR] {func.__name__} | {e} | time={elapsed}s")
            raise e
    return wrapper
