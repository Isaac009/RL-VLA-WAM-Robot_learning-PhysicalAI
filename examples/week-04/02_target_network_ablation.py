"""Week 04, checkpoint 2: measure online and delayed target motion.

The example repeatedly updates one linear prediction so learners can see the
difference between a target that changes every update and one that changes only
when delayed parameters synchronize. This is a mechanism diagnostic, not a
policy-performance or convergence result.
"""

from __future__ import annotations


class LinearQ:
    """Linear model Q(s, a) = bias[a] + slope[a] * (s / 4)."""

    def __init__(self, weights: list[list[float]] | None = None) -> None:
        source = weights or [[0.10, 0.20], [0.15, 0.40]]
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
        return max(self.predict(state, action) for action in (0, 1))

    def update(
        self, state: int, action: int, target: float, learning_rate: float
    ) -> float:
        error = target - self.predict(state, action)
        for index, feature in enumerate(self.features(state)):
            self.weights[action][index] += learning_rate * error * feature
        return error

    def clone(self) -> "LinearQ":
        return LinearQ(self.weights)

    def copy_from(self, source: "LinearQ") -> None:
        self.weights = [row[:] for row in source.weights]


def simulate_targets(
    use_delayed_target: bool,
    sync_interval: int = 6,
    update_steps: int = 24,
) -> tuple[list[float], list[float]]:
    online = LinearQ()
    delayed = online.clone()
    target_history: list[float] = []
    absolute_errors: list[float] = []

    state, action, next_state = 2, 1, 3
    reward = -0.01
    gamma = 0.95

    for update_index in range(update_steps):
        if (
            use_delayed_target
            and update_index > 0
            and update_index % sync_interval == 0
        ):
            delayed.copy_from(online)

        target_source = delayed if use_delayed_target else online
        target = reward + gamma * target_source.max_q(next_state)
        error = online.update(
            state=state,
            action=action,
            target=target,
            learning_rate=0.15,
        )
        target_history.append(target)
        absolute_errors.append(abs(error))

    return target_history, absolute_errors


def mean_absolute_change(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    changes = [
        abs(current - previous)
        for previous, current in zip(values, values[1:])
    ]
    return sum(changes) / len(changes)


def main() -> None:
    update_steps = 24
    sync_interval = 6
    online_targets, online_errors = simulate_targets(
        use_delayed_target=False,
        update_steps=update_steps,
    )
    delayed_targets, delayed_errors = simulate_targets(
        use_delayed_target=True,
        sync_interval=sync_interval,
        update_steps=update_steps,
    )

    print("=== Week 04 Checkpoint 2: Target Motion Diagnostic ===")
    print(
        f"Update steps: {update_steps} | "
        f"Delayed-target sync interval: {sync_interval}\n"
    )
    print(f"{'step':<6}{'online target':>20}{'delayed target':>20}")
    print("-" * 46)
    for index in (0, 2, 5, 6, 8, 11, 17, 23):
        print(
            f"{index + 1:<6}"
            f"{online_targets[index]:>12.4f}"
            f"  err={online_errors[index]:.4f}"
            f"{delayed_targets[index]:>12.4f}"
            f"  err={delayed_errors[index]:.4f}"
        )

    print("\nMean absolute change between consecutive targets:")
    print(f"  online target:  {mean_absolute_change(online_targets):.6f}")
    print(f"  delayed target: {mean_absolute_change(delayed_targets):.6f}")
    print("\nThe delayed target is piecewise constant between synchronizations.")
    print("This diagnostic shows target motion only; it does not establish")
    print("better return, lower seed variance, or guaranteed convergence.")


if __name__ == "__main__":
    main()
