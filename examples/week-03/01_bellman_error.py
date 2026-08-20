"""Week 03, checkpoint 1: compute Bellman error by hand.

Run:
    python examples/week-03/01_bellman_error.py

This checkpoint does not train anything. It shows the object that DQN minimizes:
the squared error between a bootstrapped Bellman target and the model's current
prediction for Q(s, a).
"""

from __future__ import annotations

GAMMA = 0.9


def bellman_target(reward: float, next_values: list[float], terminated: bool) -> float:
    if terminated:
        return reward
    return reward + GAMMA * max(next_values)


def report_case(
    name: str,
    prediction: float,
    reward: float,
    next_values: list[float],
    terminated: bool,
) -> None:
    target = bellman_target(reward, next_values, terminated)
    td_error = target - prediction
    squared_error = td_error * td_error
    loss = 0.5 * squared_error

    print(name)
    print(f"  prediction Q_theta(s, a): {prediction:.2f}")
    print(f"  reward: {reward:+.2f}")
    print(f"  next values from Q_target: {next_values}")
    print(f"  terminated: {terminated}")
    if terminated:
        print("  target = reward")
    else:
        print("  target = reward + gamma * max(next_values)")
    print(f"  target: {target:.2f}")
    print(f"  td_error = target - prediction = {td_error:.2f}")
    print(f"  squared Bellman error: {squared_error:.4f}")
    print(f"  half-squared optimization loss: {loss:.4f}")
    print()


def main() -> None:
    print(f"gamma = {GAMMA}\n")

    report_case(
        name="Non-terminal transition: state 2 --right--> state 3",
        prediction=0.10,
        reward=-0.01,
        next_values=[0.20, 0.50],
        terminated=False,
    )

    report_case(
        name="Terminal transition: state 3 --right--> goal",
        prediction=0.50,
        reward=1.00,
        next_values=[0.0, 0.0],
        terminated=True,
    )

    print("Checkpoint 2 turns this error into a weight update.")


if __name__ == "__main__":
    main()
