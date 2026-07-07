"""Week 02, checkpoint 1: what is a Q-table?

Run:
    python examples/week-02/01_q_table_intro.py

The central object of tabular Q-learning:

    Q[state][action] = the return the agent expects to collect if it takes
                       `action` in `state` and acts well afterwards.

No training happens in this checkpoint. We only build the table, print it, and
learn to read it — the same discipline as Week 01: inspect the object before
running the algorithm on it.
"""

from __future__ import annotations

from env import ACTION_NAMES, LineWorld


def make_q_table(n_states: int, n_actions: int) -> list[list[float]]:
    """One row per state, one column per action, all values zero."""
    return [[0.0] * n_actions for _ in range(n_states)]


def print_q_table(q: list[list[float]]) -> None:
    for state, row in enumerate(q):
        print(f"State {state}:")
        for action, value in enumerate(row):
            print(f"  {ACTION_NAMES[action]:<5} -> {value:.2f}")
        print()


def main() -> None:
    env = LineWorld(size=5, max_steps=20)
    q = make_q_table(n_states=env.size, n_actions=len(ACTION_NAMES))

    print(f"World: {env.render()}  (goal at state {env.goal})")
    print(f"Q-table: {env.size} states x {len(ACTION_NAMES)} actions, "
          "initialized to zero\n")
    print_q_table(q)

    print("Every entry is 0.00: the agent believes nothing yet. A greedy")
    print("policy over this table has no reason to prefer right over left.")
    print()
    print("Before checkpoint 2, predict by hand: after learning, which entry")
    print(f"should be largest? (Hint: from state {env.goal - 1}, one action")
    print("collects the +1.0 goal reward immediately.)")


if __name__ == "__main__":
    main()
