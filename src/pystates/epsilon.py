from typing import Any

from pystates.event import Event

class Epsilon(Event):

    async def wait(self) -> tuple[Any, Any]:
        return ((), {})

    def poll(self) -> tuple[Any, Any] | None:
        return ((), {})