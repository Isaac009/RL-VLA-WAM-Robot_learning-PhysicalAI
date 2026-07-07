"""Week 01, checkpoint 1: watch a random policy interact with a tiny MDP.

Run:
    python examples/week-01/01_random_policy.py

A random policy is the first baseline of the course. It answers the question
"what does doing nothing clever look like?" so that every later method has
something honest to beat.
"""

from __future__ import annotations

import random

from env import ACTION_NAMES, LEFT, LineWorld, RIGHT


def run_random_episode(env: LineWorld, seed: int | None = None) -> float:
    rng = random.Random(seed)
    state = env.reset()
    total_reward = 0.0

    print("Initial")
    print(f"state={state}  world={env.render()}")

    while True:
        action = rng.choice([LEFT, RIGHT])
        result = env.step(action)
        total_reward += result.reward

        print(
            f"action={ACTION_NAMES[action]:>5}  "
            f"state={result.state}  "
            f"reward={result.reward:>5.2f}  "
            f"done={result.done}  "
            f"world={env.render()}"
        )

        if result.done:
            break

    return total_reward


def main() -> None:
    env = LineWorld(size=5, max_steps=20)
    total_reward = run_random_episode(env, seed=7)
    print(f"\nEpisode return: {total_reward:.2f}")


if __name__ == "__main__":
    main()
