import asyncio
from typing import Any

class Event():

    def __init__(self):
        """An event to trigger a state transition
        """
        self.__queue: asyncio.Queue[tuple[Any, Any]] = asyncio.Queue(1)

    async def trigger(self, *args, **kwargs):
        """Trigger the state transition. Blocks if trigger has previously been set and transition has not yet occurred
        """
        await self.__queue.put((args, kwargs))
    
    def trigger_nowait(self, *args, **kwargs):
        """Trigger the state transition without blocking.
        """
        try:
            if not self.__queue.empty():
                self.__queue.get_nowait()
            self.__queue.put_nowait((args, kwargs))
        except asyncio.QueueFull:
            print("Queue full")
        except asyncio.QueueEmpty:
            print("Queue empty")

    async def wait(self) -> tuple[Any, Any]:
        """Wait for the event to be triggered

        Returns:
            tuple[Any, Any]: The args passed to trigger
        """
        return await self.__queue.get()

    def poll(self) -> tuple[Any, Any] | None:
        """Check for pending trigger

        Returns:
            tuple[Any, Any] | None: The args passed to trigger
        """
        try:
            return self.__queue.get_nowait()
        except asyncio.QueueEmpty:
            return None