from typing import Any

from python_states.event import Event

class Epsilon(Event):
    def __init__(self):
        """An epsilon event to immediately trigger a transition on the next iteration.
        """
        return

    async def wait(self) -> tuple[Any, Any]:
        """Wait for the event to be triggered. Epsilon Event immediately returns.

        Returns:
            tuple[Any, Any]: The args passed to trigger. Always empty for Epsilon Event.
        """
        return ((), {})

    def poll(self) -> tuple[Any, Any] | None:
        """Check for pending trigger. Epsilon Event immediately returns.

        Returns:
            tuple[Any, Any] | None: The args passed to trigger. Always empty for Epsilon Event.
        """
        return ((), {})