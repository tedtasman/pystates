
import asyncio
from typing import Optional

from python_states.transition_matrix import TransitionMatrix



class StateMachine:
    
    def __init__(self, transition_matrix: TransitionMatrix, initial_state: str):
        """Core state machine object for state transition emulation

        Args:
            transition_matrix (TransitionMatrix): Transition matrix for state machine architecture
            initial_state (str): Starting state

        Raises:
            ValueError: If starting state not in transition matrix
        """
        if initial_state not in transition_matrix.states():
            raise ValueError(f'Initial state "{initial_state}" not in transition matrix')

        self.__transition_matrix = transition_matrix
        self.__current_state = initial_state

        self.__running = asyncio.Event()
        self.__stopping = False
        self.__runner = None

    def start(self):
        """Start state machine emulation
        """
        self.__stopping = False
        self.__running.set()
        self.__runner = asyncio.create_task(self.__run())

    async def stop(self, timeout: Optional[float] = None):
        """Stop state machine emulation after next iteration

        Args:
            timeout (Optional[float], optional): Maximum wait time. Defaults to None.
        """
        self.__stopping = True
        runner = self.__runner
        if runner is None or runner.done():
            self.__running.clear()
            return

        try:
            await asyncio.wait_for(
                runner,
                timeout=timeout,
            )
        finally:
            self.__running.clear()
            self.__stopping = False


    async def __run(self):
        while self.__running.is_set():
            triggered = await self.__transition_matrix.event_trigger_wait(
                self.__current_state,
                block=not self.__stopping,
            )
            if triggered is None:
                self.__running.clear()
                self.__runner = None
                break

            row, payload = triggered
            args, kwargs = payload
            args = args or ()
            kwargs = kwargs or {}

            action = row[self.__transition_matrix.ACTION]
            action(*args, **kwargs) if action else None
            
            self.__current_state = row[self.__transition_matrix.NEXT_STATE]
            await asyncio.sleep(0)