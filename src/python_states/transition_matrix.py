from typing import Any, TypeAlias
from collections.abc import Callable
import asyncio

from python_states.event import Event


Action: TypeAlias = Callable[..., object]
Row: TypeAlias = tuple[str, Event, Action | None, str]
EventPayload: TypeAlias = tuple[tuple[Any, ...], dict[str, Any]]

class TransitionMatrix:

    START_STATE = 0
    EVENT = 1
    ACTION = 2
    NEXT_STATE = 3

    def __init__(self, transitions: list[Row]):
        """State transition matrix 

        Args:
            transitions (list[Row]): list of transition edge entries with starting state, event, action, and end state
        """
        self.__transitions = transitions

    def __contains__(self, item: str) -> bool:
        if any(row[0] == item for row in self.__transitions):
            return True
        return False
    
    def states(self) -> set[str]:
        """Get the available states from the matrix

        Returns:
            set[str]: set of all states
        """
        return {row[0] for row in self.__transitions}
    
    async def event_trigger_wait(
        self,
        current_state: str,
        *,
        block: bool = True,
    ) -> tuple[Row, EventPayload] | None:
        """Wait for an event to be triggered from the current state

        Args:
            current_state (str): Current state machine state
            block (bool, optional): block to prevent early shutdown. Defaults to True.

        Returns:
            tuple[Row, EventPayload] | None: Transition matrix row and the args passed to Event.trigger
        """
        eligible_rows = self.__transitions
        if current_state is not None:
            eligible_rows = [
                row for row in self.__transitions if row[self.START_STATE] == current_state
            ]

        if not eligible_rows:
            return None

        if not block:
            for row in eligible_rows:
                payload = row[self.EVENT].poll()
                if payload is not None:
                    return row, payload
            return None

        tasks: dict[asyncio.Task[EventPayload], Row] = {
            asyncio.create_task(row[self.EVENT].wait()): row
            for row in eligible_rows
        }

        try:
            done, pending = await asyncio.wait(
                set(tasks),
                return_when=asyncio.FIRST_COMPLETED,
            )
        except asyncio.CancelledError:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

        for task in pending:
            task.cancel()

        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

        first_done = next(iter(done))
        return tasks[first_done], first_done.result()