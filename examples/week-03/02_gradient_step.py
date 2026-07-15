"""Week 03, checkpoint 2: one gradient step on Bellman error.

Run:
    python examples/week-03/02_gradient_step.py

DQN uses a neural network. This checkpoint uses the smallest possible function
approximator instead:

    Q_theta(state, action) = bias[action] + slope[action] * normalized_state

The point is not model power. The point is seeing how a Bellman error changes
parameters instead of directly changing one Q-table cell.
"""

from __future__ import annotations

ACTION_RIGHT = 1
ALPHA = 0.5
TARGET = 0.44


def features(state: int, goal: int) -> list[float]:
    normalized_state = state / goal
    return [1.0, normalized_state]


def q_value(weights: list[list[float]], state: int, action: int, goal: int) -> float:
    return sum(w * x for w, x in zip(weights[action], features(state, goal)))


def main() -> None:
    goal = 4
    state = 2
    weights = [
        [0.05, 0.00],  # left:  bias, state slope
        [0.10, 0.00],  # right: bias, state slope
    ]

    x = features(state, goal)
    prediction_before = q_value(weights, state, ACTION_RIGHT, goal)
    td_error = TARGET - prediction_before
    loss_before = td_error * td_error

    print("Linear Q approximator")
    print("  Q_theta(s, a) = bias[a] + slope[a] * normalized_state")
    print(f"  features for state {state}, action right: [{x[0]:.2f}, {x[1]:.2f}]\n")

    print("Before update")
    print(f"  Q_theta({state}, right): {prediction_before:.2f}")
    print(f"  Bellman target: {TARGET:.2f}")
    print(f"  td_error: {td_error:.2f}")
    print(f"  squared Bellman error: {loss_before:.4f}\n")

    print("Gradient step on the right-action weights")
    for index, feature_value in enumerate(x):
        delta = ALPHA * td_error * feature_value
        weights[ACTION_RIGHT][index] += delta
        name = "bias" if index == 0 else "state slope"
        print(f"  {name:<11} += {delta:.3f}")

    prediction_after = q_value(weights, state, ACTION_RIGHT, goal)
    loss_after = (TARGET - prediction_after) ** 2

    print("\nAfter update")
    print(f"  Q_theta({state}, right): {prediction_after:.2f}")
    print(f"  squared Bellman error: {loss_after:.4f}")
    print("\nOnly the parameters for the action actually taken were updated.")
    print("Checkpoint 3 repeats this idea over many transitions.")


if __name__ == "__main__":
    main()
