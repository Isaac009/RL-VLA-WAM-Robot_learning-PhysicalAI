"""Week 01, checkpoint 2: beat the random agent with a heuristic baseline.

Run:
    python examples/week-01/02_baseline_policy.py

The heuristic here is the one from Lab 01's extension exercise: always move
right. Comparing it to the random policy over many episodes is the course's
first measurable comparison — a metric (average return, success rate), a
baseline (random), and a challenger (heuristic).

Limitation note: "always right" is optimal only because LineWorld's goal is
always on the right edge. It encodes knowledge of this specific environment,
not a learning method. Week 02 replaces it with tabular Q-learning, which has
to discover the same behavior from experience.
"""

from __future__ import annotations

import random
from typing import Callable

from env import LEFT, LineWorld, RIGHT

Policy = Callable[[int, random.Random], int]


def random_policy(state: int, rng: random.Random) -> int:
    return rng.choice([LEFT, RIGHT])


def always_right(state: int, rng: random.Random) -> int:
    return RIGHT


def run_episode(env: LineWorld, policy: Policy, seed: int) -> tuple[float, bool]:
    rng = random.Random(seed)
    state = env.reset()
    total_reward = 0.0

    while True:
        action = policy(state, rng)
        result = env.step(action)
        state = result.state
        total_reward += result.reward

        if result.done:
            reached_goal = state == env.goal
            return total_reward, reached_goal


def evaluate(policy: Policy, episodes: int = 100) -> tuple[float, float]:
    env = LineWorld(size=5, max_steps=20)
    returns = []
    successes = 0

    for episode in range(episodes):
        episode_return, reached_goal = run_episode(env, policy, seed=episode)
        returns.append(episode_return)
        successes += int(reached_goal)

    average_return = sum(returns) / len(returns)
    success_rate = successes / episodes
    return average_return, success_rate


def main() -> None:
    episodes = 100
    policies: dict[str, Policy] = {
        "random": random_policy,
        "always right": always_right,
    }

    print(f"LineWorld(size=5, max_steps=20), {episodes} episodes per policy\n")
    print(f"{'policy':<14}{'avg return':>12}{'success rate':>14}")

    for name, policy in policies.items():
        average_return, success_rate = evaluate(policy, episodes)
        print(f"{name:<14}{average_return:>12.2f}{success_rate:>13.0%}")

    print(
        "\nThe heuristic wins here because it encodes knowledge of this exact"
        "\nenvironment. Week 02 asks: can an agent learn the same behavior"
        "\nfrom experience alone?"
    )


if __name__ == "__main__":
    main()
