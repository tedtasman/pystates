import asyncio
from typing import Any

class Event():

    def __init__(self):
        self.queue: asyncio.Queue[tuple[Any, Any]] = asyncio.Queue(1)

    async def trigger(self, *args, **kwargs):
        await self.queue.put((args, kwargs))
    
    def trigger_nowait(self, *args, **kwargs):
        try:
            if not self.queue.empty():
                self.queue.get_nowait()
            self.queue.put_nowait((args, kwargs))
        except asyncio.QueueFull:
            print("Queue full")
        except asyncio.QueueEmpty:
            print("Queue empty")

    async def wait(self) -> tuple[Any, Any]:
        return await self.queue.get()

    def poll(self) -> tuple[Any, Any] | None:
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty:
            return None