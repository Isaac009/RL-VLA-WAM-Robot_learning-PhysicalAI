"""Week 03, checkpoint 3: train a tiny DQN-style Q approximator.

Run:
    python examples/week-03/03_train_linear_q.py

This is not full DQN. Full DQN uses a neural network, replay buffer, and target
network. This checkpoint keeps only the Bellman-error loss and a periodically
synced target copy so the mechanics stay visible and dependency-free.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from env import ACTION_NAMES, LineWorld

TRAIN_EPISODES = 300
EVAL_EPISODES = 100
ALPHA = 0.15
GAMMA = 0.9
EPSILON = 0.2
TARGET_SYNC_EPISODES = 20
SEED = 7


@dataclass
class TrainResult:
    weights: list[list[float]]
    losses: list[float]


def make_weights() -> list[list[float]]:
    return [[0.0, 0.0] for _ in ACTION_NAMES]


def copy_weights(weights: list[list[float]]) -> list[list[float]]:
    return [row[:] for row in weights]


def features(state: int, goal: int) -> list[float]:
    return [1.0, state / goal]


def q_value(weights: list[list[float]], state: int, action: int, goal: int) -> float:
    return sum(weight * feature for weight, feature in zip(weights[action], features(state, goal)))


def greedy_action(weights: list[list[float]], state: int, goal: int) -> int:
    left = q_value(weights, state, 0, goal)
    right = q_value(weights, state, 1, goal)
    return 1 if right >= left else 0


def epsilon_greedy_action(
    weights: list[list[float]],
    state: int,
    goal: int,
    epsilon: float,
    rng: random.Random,
) -> int:
    if rng.random() < epsilon:
        return rng.randrange(len(ACTION_NAMES))
    return greedy_action(weights, state, goal)


def train(seed: int = SEED) -> TrainResult:
    rng = random.Random(seed)
    env = LineWorld(size=5, max_steps=20)
    weights = make_weights()
    target_weights = copy_weights(weights)
    losses: list[float] = []

    for episode in range(TRAIN_EPISODES):
        state = env.reset()
        done = False

        while not done:
            action = epsilon_greedy_action(weights, state, env.goal, EPSILON, rng)
            result = env.step(action)

            if result.terminated:
                target = result.reward
            else:
                future = max(
                    q_value(target_weights, result.state, next_action, env.goal)
                    for next_action in range(len(ACTION_NAMES))
                )
                target = result.reward + GAMMA * future

            prediction = q_value(weights, state, action, env.goal)
            td_error = target - prediction
            losses.append(td_error * td_error)

            for index, feature_value in enumerate(features(state, env.goal)):
                weights[action][index] += ALPHA * td_error * feature_value

            state = result.state
            done = result.terminated or result.truncated

        if (episode + 1) % TARGET_SYNC_EPISODES == 0:
            target_weights = copy_weights(weights)

    return TrainResult(weights=weights, losses=losses)


def evaluate_policy(policy_name: str, choose_action, episodes: int = EVAL_EPISODES) -> tuple[str, float, float]:
    env = LineWorld(size=5, max_steps=20)
    total_return = 0.0
    successes = 0

    for episode in range(episodes):
        rng = random.Random(10_000 + episode)
        state = env.reset()
        done = False
        episode_return = 0.0

        while not done:
            action = choose_action(state, env.goal, rng)
            result = env.step(action)
            episode_return += result.reward
            state = result.state
            done = result.terminated or result.truncated

        total_return += episode_return
        successes += int(state == env.goal)

    return policy_name, total_return / episodes, successes / episodes


def print_values(weights: list[list[float]]) -> None:
    env = LineWorld(size=5, max_steps=20)
    for state in range(env.size):
        if state == env.goal:
            print(f"state {state}: terminal state (no action chosen after goal)")
            continue
        left = q_value(weights, state, 0, env.goal)
        right = q_value(weights, state, 1, env.goal)
        best = ACTION_NAMES[1 if right >= left else 0]
        print(f"state {state}: left={left:5.2f}  right={right:5.2f}  best={best}")


def main() -> None:
    result = train()
    recent_loss = sum(result.losses[-100:]) / 100

    print(
        "Training linear Q approximator: "
        f"{TRAIN_EPISODES} episodes, alpha={ALPHA}, gamma={GAMMA}, "
        f"epsilon={EPSILON}, target_sync={TARGET_SYNC_EPISODES}"
    )
    print(f"Average Bellman loss over last 100 updates: {recent_loss:.4f}\n")

    print("Predicted action values:")
    print_values(result.weights)

    policies = [
        evaluate_policy("random", lambda state, goal, rng: rng.choice([0, 1])),
        evaluate_policy("always right", lambda state, goal, rng: 1),
        evaluate_policy("linear-q", lambda state, goal, rng: greedy_action(result.weights, state, goal)),
    ]

    print("\nEvaluation: 100 episodes per policy")
    print("\npolicy          avg return  success rate")
    for name, avg_return, success_rate in policies:
        print(f"{name:<14}{avg_return:>12.2f}{success_rate:>13.0%}")

    print("\nThe approximator matches the heuristic in this tiny world, but this")
    print("is still a narrow result. It shows the Bellman-error training")
    print("mechanism, not general deep-RL competence.")


if __name__ == "__main__":
    main()
