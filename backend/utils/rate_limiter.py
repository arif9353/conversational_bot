import asyncio
import time

class FixedIntervalRateLimiter:
    def __init__(self, interval: float):
        self.interval = interval
        self.last_call = 0
        self.lock = asyncio.Lock()

    async def wait_for_slot(self):
        async with self.lock:
            now = time.time()
            elapsed = now - self.last_call

            if elapsed < self.interval:
                await asyncio.sleep(self.interval - elapsed)

            self.last_call = time.time()


rate_limiter = FixedIntervalRateLimiter(interval=7)