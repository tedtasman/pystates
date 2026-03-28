import asyncio
from pystates.state_machine import StateMachine
from pystates.transition import Matrix
from pystates.event import Event

async def main():

    def swing_open():
        print("Opening")

    def swing_closed():
        print("Closing")

    push = Event()
    pull = Event()

    tm = Matrix([
        ("closed", push, swing_open, "open"),
        ("open", pull, swing_closed, "closed")
    ])
    sm = StateMachine(tm, "closed")

    sm.start()

    await push.trigger()

    await pull.trigger()

    await sm.stop()

if __name__ == "__main__":
    asyncio.run(main())