"""Week 02, checkpoint 3: train tabular Q-learning and compare baselines.

Run:
    python examples/week-02/03_train_q_learning.py

The first two checkpoints inspected the Q-table and performed two updates by
hand. This checkpoint repeats the same update over many episodes with
epsilon-greedy exploration, then evaluates the learned greedy policy against
the Week 01 baselines.
"""

from __future__ import annotations

import random
from typing import Callable

from env import ACTION_NAMES, LEFT, LineWorld, RIGHT


ALPHA = 0.5
GAMMA = 0.9
EPSILON = 0.2
TRAIN_EPISODES = 200
EVAL_EPISODES = 100

Policy = Callable[[int, random.Random], int]
QTable = list[list[float]]


def make_q_table(n_states: int, n_actions: int) -> QTable:
    return [[0.0] * n_actions for _ in range(n_states)]


def random_policy(state: int, rng: random.Random) -> int:
    return rng.choice([LEFT, RIGHT])


def always_right(state: int, rng: random.Random) -> int:
    return RIGHT


def greedy_action(q: QTable, state: int) -> int:
    """Choose the best action, breaking ties toward left for transparency."""
    row = q[state]
    return max(range(len(row)), key=lambda action: row[action])


def epsilon_greedy(q: QTable, state: int, rng: random.Random) -> int:
    if rng.random() < EPSILON:
        return rng.choice([LEFT, RIGHT])
    return greedy_action(q, state)


def q_learning_update(
    q: QTable,
    state: int,
    action: int,
    reward: float,
    next_state: int,
    terminated: bool,
) -> None:
    best_next = 0.0 if terminated else max(q[next_state])
    target = reward + GAMMA * best_next
    td_error = target - q[state][action]
    q[state][action] += ALPHA * td_error


def train_q_learning(seed: int = 0) -> QTable:
    env = LineWorld(size=5, max_steps=20)
    q = make_q_table(n_states=env.size, n_actions=len(ACTION_NAMES))
    rng = random.Random(seed)

    for _ in range(TRAIN_EPISODES):
        state = env.reset()

        while True:
            action = epsilon_greedy(q, state, rng)
            result = env.step(action)
            q_learning_update(
                q=q,
                state=state,
                action=action,
                reward=result.reward,
                next_state=result.state,
                terminated=result.terminated,
            )
            state = result.state

            if result.done:
                break

    return q


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
            return total_reward, result.terminated


def evaluate(policy: Policy, episodes: int = EVAL_EPISODES) -> tuple[float, float]:
    env = LineWorld(size=5, max_steps=20)
    returns = []
    successes = 0

    for episode in range(episodes):
        episode_return, reached_goal = run_episode(env, policy, seed=10_000 + episode)
        returns.append(episode_return)
        successes += int(reached_goal)

    return sum(returns) / len(returns), successes / episodes


def learned_policy_from(q: QTable) -> Policy:
    def policy(state: int, rng: random.Random) -> int:
        return greedy_action(q, state)

    return policy


def print_q_table(q: QTable, terminal_state: int) -> None:
    for state, row in enumerate(q):
        if state == terminal_state:
            print(f"state {state}: terminal state (no action chosen after goal)")
            continue

        left = row[LEFT]
        right = row[RIGHT]
        best = ACTION_NAMES[greedy_action(q, state)]
        print(f"state {state}: left={left:>5.2f}  right={right:>5.2f}  best={best}")


def main() -> None:
    env = LineWorld(size=5, max_steps=20)
    q = train_q_learning(seed=0)
    learned_policy = learned_policy_from(q)

    policies: dict[str, Policy] = {
        "random": random_policy,
        "always right": always_right,
        "q-learning": learned_policy,
    }

    print(
        "Training: "
        f"{TRAIN_EPISODES} episodes, alpha={ALPHA}, gamma={GAMMA}, "
        f"epsilon={EPSILON}\n"
    )
    print("Learned Q-table:")
    print_q_table(q, terminal_state=env.goal)

    print(f"\nEvaluation: {EVAL_EPISODES} episodes per policy\n")
    print(f"{'policy':<14}{'avg return':>12}{'success rate':>14}")

    for name, policy in policies.items():
        average_return, success_rate = evaluate(policy, EVAL_EPISODES)
        print(f"{name:<14}{average_return:>12.2f}{success_rate:>13.0%}")

    print(
        "\nThe learned policy matches the simple heuristic in this tiny world."
        "\nThat is a success only in this narrow environment. The point is not"
        "\nthat Q-learning is magic; the point is that it discovered the useful"
        "\naction values from experience instead of being handed the rule."
    )


if __name__ == "__main__":
    main()
