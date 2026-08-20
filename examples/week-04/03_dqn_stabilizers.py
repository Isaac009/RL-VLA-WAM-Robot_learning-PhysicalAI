"""Week 04, checkpoint 3: controlled comparison of Q-learning stabilizers.

This is a four-way ablation for a linear Q approximator, not a full DQN
benchmark. Every variant receives the same number of environment interactions,
the same number of optimizer steps, and the same fixed evaluation starts.
Replay variants intentionally reuse a minibatch at each optimizer step.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from env import LineWorld


LEFT = 0
RIGHT = 1
GAMMA = 0.95
LEARNING_RATE = 0.15
EPSILON = 0.20
TRAIN_STEPS = 400
WARMUP_STEPS = 8
BATCH_SIZE = 8
TARGET_SYNC_UPDATES = 8
EVAL_STARTS = tuple(state for state in range(4) for _ in range(25))


@dataclass(frozen=True)
class Transition:
    state: int
    action: int
    reward: float
    next_state: int
    terminated: bool
    truncated: bool


@dataclass(frozen=True)
class Evaluation:
    average_return: float
    success_rate: float


@dataclass
class TrainResult:
    model: "LinearQ"
    losses: list[float]
    optimizer_updates: int


class ReplayBuffer:
    def __init__(self, capacity: int = 200) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.buffer: list[Transition] = []
        self.position = 0

    def push(self, transition: Transition) -> None:
        if len(self.buffer) < self.capacity:
            self.buffer.append(transition)
        else:
            self.buffer[self.position] = transition
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size: int, rng: random.Random) -> list[Transition]:
        if len(self.buffer) < batch_size:
            raise ValueError(
                f"cannot sample {batch_size} transitions from {len(self.buffer)}"
            )
        return rng.sample(self.buffer, batch_size)

    def __len__(self) -> int:
        return len(self.buffer)


class LinearQ:
    """Two parameters per action: a bias and normalized-state slope."""

    def __init__(self, weights: list[list[float]] | None = None) -> None:
        source = weights or [[0.0, 0.0], [0.0, 0.0]]
        self.weights = [row[:] for row in source]

    @staticmethod
    def features(state: int) -> tuple[float, float]:
        return 1.0, state / 4.0

    def predict(self, state: int, action: int) -> float:
        return sum(
            weight * feature
            for weight, feature in zip(
                self.weights[action], self.features(state)
            )
        )

    def max_q(self, state: int) -> float:
        return max(self.predict(state, action) for action in (LEFT, RIGHT))

    def best_action(self, state: int) -> int:
        left = self.predict(state, LEFT)
        right = self.predict(state, RIGHT)
        return RIGHT if right > left else LEFT

    def clone(self) -> "LinearQ":
        return LinearQ(self.weights)

    def copy_from(self, source: "LinearQ") -> None:
        self.weights = [row[:] for row in source.weights]


def update_from_batch(
    online: LinearQ,
    target_source: LinearQ,
    batch: list[Transition],
) -> float:
    """Apply one optimizer step to the mean half-squared Bellman loss."""
    gradients = [[0.0, 0.0], [0.0, 0.0]]
    total_loss = 0.0

    for transition in batch:
        if transition.terminated:
            target = transition.reward
        else:
            target = (
                transition.reward
                + GAMMA * target_source.max_q(transition.next_state)
            )

        prediction = online.predict(transition.state, transition.action)
        error = target - prediction
        total_loss += 0.5 * error * error

        for index, feature in enumerate(online.features(transition.state)):
            gradients[transition.action][index] += error * feature / len(batch)

    for action in (LEFT, RIGHT):
        for index in range(2):
            online.weights[action][index] += (
                LEARNING_RATE * gradients[action][index]
            )

    return total_loss / len(batch)


def train_agent(
    use_replay: bool,
    use_delayed_target: bool,
    seed: int,
) -> TrainResult:
    rng = random.Random(seed)
    env = LineWorld(size=5, max_steps=20)
    online = LinearQ()
    delayed = online.clone()
    replay = ReplayBuffer(capacity=200)
    losses: list[float] = []
    optimizer_updates = 0
    state = env.reset()

    for interaction in range(TRAIN_STEPS):
        if rng.random() < EPSILON:
            action = rng.choice([LEFT, RIGHT])
        else:
            action = online.best_action(state)

        result = env.step(action)
        transition = Transition(
            state=state,
            action=action,
            reward=result.reward,
            next_state=result.state,
            terminated=result.terminated,
            truncated=result.truncated,
        )
        replay.push(transition)

        if interaction + 1 >= WARMUP_STEPS:
            batch = (
                replay.sample(BATCH_SIZE, rng)
                if use_replay
                else [transition]
            )
            target_source = delayed if use_delayed_target else online
            losses.append(update_from_batch(online, target_source, batch))
            optimizer_updates += 1

            if (
                use_delayed_target
                and optimizer_updates % TARGET_SYNC_UPDATES == 0
            ):
                delayed.copy_from(online)

        state = (
            env.reset()
            if result.terminated or result.truncated
            else result.state
        )

    return TrainResult(
        model=online,
        losses=losses,
        optimizer_updates=optimizer_updates,
    )


def evaluate_model(model: LinearQ) -> Evaluation:
    env = LineWorld(size=5, max_steps=20)
    returns: list[float] = []
    successes = 0

    for start in EVAL_STARTS:
        state = env.reset(start=start)
        episode_return = 0.0

        while True:
            result = env.step(model.best_action(state))
            episode_return += result.reward
            state = result.state

            if result.terminated or result.truncated:
                returns.append(episode_return)
                successes += int(result.terminated)
                break

    return Evaluation(
        average_return=sum(returns) / len(returns),
        success_rate=successes / len(returns),
    )


def evaluate_baseline(name: str, seed: int = 10_000) -> tuple[str, Evaluation]:
    rng = random.Random(seed)
    env = LineWorld(size=5, max_steps=20)
    returns: list[float] = []
    successes = 0

    for start in EVAL_STARTS:
        env.reset(start=start)
        episode_return = 0.0

        while True:
            action = (
                rng.choice([LEFT, RIGHT])
                if name == "random"
                else RIGHT
            )
            result = env.step(action)
            episode_return += result.reward

            if result.terminated or result.truncated:
                returns.append(episode_return)
                successes += int(result.terminated)
                break

    return name, Evaluation(
        average_return=sum(returns) / len(returns),
        success_rate=successes / len(returns),
    )


def population_std(values: list[float]) -> float:
    mean = sum(values) / len(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def main() -> None:
    seeds = [42, 123, 456, 789, 2026]
    configurations = [
        ("online only", False, False),
        ("target only", False, True),
        ("replay only", True, False),
        ("replay + target", True, True),
    ]

    print("=== Week 04 Checkpoint 3: Controlled Stabilizer Comparison ===")
    print(f"Training seeds: {seeds}")
    print(
        f"Budget per seed: {TRAIN_STEPS} interactions, "
        f"{TRAIN_STEPS - WARMUP_STEPS + 1} optimizer steps"
    )
    print(
        f"Evaluation: {len(EVAL_STARTS)} fixed starts shared by every policy\n"
    )

    print("Baselines under the same evaluation protocol:")
    print(f"{'policy':<18}{'avg return':>14}{'success rate':>16}")
    for name in ("random", "always right"):
        _, evaluation = evaluate_baseline(name)
        print(
            f"{name:<18}"
            f"{evaluation.average_return:>14.4f}"
            f"{evaluation.success_rate:>15.1%}"
        )

    print("\nLearned variants:")
    print(
        f"{'variant':<18}{'mean return':>14}{'seed std':>12}"
        f"{'success rate':>16}{'updates':>10}"
    )

    mean_returns: list[float] = []
    for name, use_replay, use_delayed_target in configurations:
        evaluations: list[Evaluation] = []
        update_counts: list[int] = []

        for seed in seeds:
            trained = train_agent(
                use_replay=use_replay,
                use_delayed_target=use_delayed_target,
                seed=seed,
            )
            evaluations.append(evaluate_model(trained.model))
            update_counts.append(trained.optimizer_updates)

        returns = [evaluation.average_return for evaluation in evaluations]
        success_rates = [
            evaluation.success_rate for evaluation in evaluations
        ]
        mean_return = sum(returns) / len(returns)
        mean_returns.append(mean_return)

        print(
            f"{name:<18}"
            f"{mean_return:>14.4f}"
            f"{population_std(returns):>12.4f}"
            f"{sum(success_rates) / len(success_rates):>15.1%}"
            f"{min(update_counts):>10}"
        )
        formatted_returns = ", ".join(f"{value:+.4f}" for value in returns)
        print(f"  per-seed returns: [{formatted_returns}]")

    observed_range = max(mean_returns) - min(mean_returns)
    print("\nInterpretation:")
    if observed_range < 1e-9:
        print("All four variants achieved the same policy-level result.")
        print("LineWorld is too easy to demonstrate a stabilizer advantage.")
    else:
        print(
            f"The observed mean-return range is {observed_range:.4f} under "
            "this local budget."
        )
        print("Treat it as a scoped observation, not a general ranking.")
    print("Checkpoints 1 and 2 isolate the replay-order and target-motion")
    print("mechanics. A harder neural benchmark is required for DQN claims.")


if __name__ == "__main__":
    main()
