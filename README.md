# Python States

State Machines are great. Programming them isn't. python_states solves this issue by abstracting away all of the boilerplate emulation and transition handling. As a result, implementing a state machine is as simple as defining a state transition matrix and providing a starting state.

## Usage

1. Clone the repository:

```bash
git clone git@github.com:tedtasman/python_states.git
```

2. Install dependencies with uv:

```bash
uv sync
```

3. Run the project:

```bash
uv run python main.py
```

## Future work

1. Concurrent execution, which would add support for NFAs and other non-deterministic state machines
2. Documentation...
