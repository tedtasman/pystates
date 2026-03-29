from typing import Any

from python_states.event import Event

class Input:

    def __init__(self, inputs: list[Any]):
        self.events = {input: Event() for input in inputs}

    def __getitem__(self, item: Any) -> Any:
        return self.events[item]
    
    def get(self, item: Any, default: Any = None) -> Any:
        return self.events.get(item, default)