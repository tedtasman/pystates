import asyncio
from typing import Any

class Event():

    def __init__(self):
        self.queue: asyncio.Queue[tuple[Any, Any]] = asyncio.Queue(1)

    async def trigger(self, *args, **kwargs):
        await self.queue.put((args, kwargs))

    async def wait(self) -> tuple[Any, Any]:
        return await self.queue.get()