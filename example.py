import asyncio
from python_states.state_machine import StateMachine
from python_states.transition_matrix import TransitionMatrix
from python_states.input import Input
from python_states.epsilon import Epsilon

async def main():

    def accept():
        print("Accepted")

    def reject():
        print("Rejected")

    alpha = Input(["0", "1"])
    epsilon = Epsilon()
    
    tm = TransitionMatrix([
        ("q1", epsilon, accept, "q3"),
        ("q2", alpha["1"], None, "q4"),
        ("q2", alpha["0"], accept, "q4"),
        ("q4", alpha["1"], accept, "q3"),
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