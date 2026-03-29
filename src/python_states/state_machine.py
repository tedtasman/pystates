
import asyncio
from typing import Optional

from python_states.transition_matrix import TransitionMatrix



class StateMachine:
    
    def __init__(self, transition_matrix: TransitionMatrix, initial_state: str):
        if initial_state not in transition_matrix.states():
            raise ValueError(f'Initial state "{initial_state}" not in transition matrix')

        self.transition_matrix = transition_matrix
        self.current_state = initial_state

        self.__running = asyncio.Event()
        self.__stopping = False
        self.__runner = None

    def start(self):
        self.__stopping = False
        self.__running.set()
        self.__runner = asyncio.create_task(self.__run())

    async def stop(self, timeout: Optional[float] = None):
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
            print("current state:", self.current_state)
            triggered = await self.transition_matrix.event_trigger_wait(
                self.current_state,
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

            action = row[self.transition_matrix.ACTION]
            action(*args, **kwargs) if action else None
            
            self.current_state = row[self.transition_matrix.NEXT_STATE]
            await asyncio.sleep(0)