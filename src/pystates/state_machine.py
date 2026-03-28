
import asyncio

from pystates.transition import Matrix



class StateMachine:
    
    def __init__(self, transition_matrix: Matrix, initial_state: str):
        if initial_state not in transition_matrix.states():
            raise ValueError(f'Initial state "{initial_state}" not in transition matrix')

        self.transition_matrix = transition_matrix
        self.current_state = initial_state

        self.__running = asyncio.Event()
        self.__runner = None

    def start(self):
        self.__running.set()
        self.__runner = asyncio.create_task(self.__run())

    async def stop(self):
        self.__running.clear()
        runner = self.__runner
        if runner is None:
            return
        if not runner.done():
            runner.cancel()

        if runner is not asyncio.current_task():
            try:
                await runner
            except asyncio.CancelledError:
                pass

        self.__runner = None


    async def __run(self):
        print("HELLO??")
        while self.__running.is_set():
            print("waiting for triggers")
            triggered = await self.transition_matrix.event_trigger_wait(self.current_state)
            if triggered is None:
                self.__runner = None
                break

            row, payload = triggered
            args, kwargs = payload

            action = row[self.transition_matrix.ACTION]
            action(*args, **kwargs)

            self.current_state = row[self.transition_matrix.NEXT_STATE]