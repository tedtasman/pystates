from typing import Any

from python_states.event import Event

class Input:

    def __init__(self, inputs: list[Any]):
        """A list of many events mapped to inputs

        Args:
            inputs (list[Any]): A list of possible inputs
        """ 
        self.__events = {input: Event() for input in inputs}

    def __getitem__(self, item: Any) -> Any:
        return self.__events[item]
    
    def get(self, item: Any, default: Any = None) -> Event | Any:
        """Get the event corresponding to an input. Behaves the same as dict.get        

        Args:
            item (Any): Input to get    
            default (Any, optional): Fallback to return if item is not found. Defaults to None.

        Returns:
            Any: The event if found, or default
        """
        return self.__events.get(item, default)