from typing import Any, TypeAlias
from collections.abc import Callable
import asyncio

from pystates.event import Event


Action: TypeAlias = Callable[..., object]
Row: TypeAlias = tuple[str, Event, Action, str]
EventPayload: TypeAlias = tuple[tuple[Any, ...], dict[str, Any]]

class Matrix:

    START_STATE = 0
    EVENT = 1
    ACTION = 2
    NEXT_STATE = 3

    def __init__(self, transitions: list[Row]):
        self.transitions = transitions

    def __contains__(self, item: str) -> bool:
        if any(row[0] == item for row in self.transitions):
            return True
        return False
    
    def states(self):
        return {row[0] for row in self.transitions}
    
    async def event_trigger_wait(self, current_state: str | None = None) -> tuple[Row, EventPayload] | None:
        eligible_rows = self.transitions
        if current_state is not None:
            eligible_rows = [
                row for row in self.transitions if row[self.START_STATE] == current_state
            ]

        if not eligible_rows:
            return None

        tasks: dict[asyncio.Task[EventPayload], Row] = {
            asyncio.create_task(row[self.EVENT].wait()): row
            for row in eligible_rows
        }

        done, pending = await asyncio.wait(
            set(tasks),
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

        first_done = next(iter(done))
        return tasks[first_done], first_done.result()