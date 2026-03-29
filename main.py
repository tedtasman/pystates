import asyncio
from pystates.state_machine import StateMachine
from pystates.transition_matrix import TransitionMatrix
from pystates.input import Input
from pystates.epsilon import Epsilon

async def main():

    def accept():
        print("Accepted")

    def reject():
        print("Rejected")

    alpha = Input(["0", "1"])
    epsilon = Epsilon()

    tm = TransitionMatrix([
        ("q1", epsilon, accept, "q3"),
        ("q2", alpha["1"], None, "q1"),
        ("q2", alpha["0"], accept, "q4"),
        ("q2", alpha["1"], accept, "q3"),
        ("q4", alpha["0"], reject, "q5"),
    ])
    sm = StateMachine(tm, "q2")

    sm.start()


    for char in "1111":
        alpha[char].trigger_nowait()
        await asyncio.sleep(0)

    await sm.stop()



if __name__ == "__main__":
    asyncio.run(main())