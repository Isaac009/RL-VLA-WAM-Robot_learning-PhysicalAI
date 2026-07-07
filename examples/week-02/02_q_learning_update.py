"""Week 02, checkpoint 2: one Q-learning update, by hand.

Run:
    python examples/week-02/02_q_learning_update.py

The whole algorithm is one line applied over and over:

    Q(s, a) <- Q(s, a) + alpha * (target - Q(s, a))
    target   = reward + gamma * max_a' Q(next_state, a')

with one crucial exception: if `next_state` is terminal, there is no future,
so the `gamma * max ...` term is dropped. This is exactly why this week's
`env.py` separates `terminated` from `truncated` — after a timeout the world
would have continued, so the future term stays.

This checkpoint performs just two updates and prints every quantity, so the
arithmetic is checkable on paper. Full training over many episodes is
checkpoint 3.
"""

from __future__ import annotations

from env import ACTION_NAMES, LineWorld, RIGHT

ALPHA = 0.5  # learning rate: how far to move toward the target
GAMMA = 0.9  # discount: how much future reward is worth today


def q_update(
    q: list[list[float]],
    state: int,
    action: int,
    reward: float,
    next_state: int,
    terminated: bool,
) -> None:
    """Apply one Q-learning update in place, narrating each quantity."""
    best_next = 0.0 if terminated else max(q[next_state])
    target = reward + GAMMA * best_next
    td_error = target - q[state][action]
    old_value = q[state][action]
    q[state][action] = old_value + ALPHA * td_error

    print(f"  transition: state {state} --{ACTION_NAMES[action]}--> "
          f"state {next_state}, reward {reward:+.2f}, "
          f"terminated={terminated}")
    print(f"  best next value: max Q[{next_state}] = {best_next:.2f}"
          f"{'  (dropped: terminal state has no future)' if terminated else ''}")
    print(f"  target        = {reward:+.2f} + {GAMMA} * {best_next:.2f} "
          f"= {target:.2f}")
    print(f"  td_error      = {target:.2f} - {old_value:.2f} = {td_error:.2f}")
    print(f"  Q[{state}][{ACTION_NAMES[action]}] <- {old_value:.2f} "
          f"+ {ALPHA} * {td_error:.2f} = {q[state][action]:.2f}")


def main() -> None:
    env = LineWorld(size=5, max_steps=20)
    q = [[0.0] * len(ACTION_NAMES) for _ in range(env.size)]

    print("Update 1: the transition that touches the goal reward.")
    state = env.reset(position=3)
    result = env.step(RIGHT)
    q_update(q, state, RIGHT, result.reward, result.state, result.terminated)

    print()
    print("Update 2: one state further back. Nothing rewarding happens on")
    print("this step, yet the value still rises — the target bootstraps on")
    print("the entry we just learned. This is how the goal reward spreads")
    print("backward through the table, one update at a time.")
    state = env.reset(position=2)
    result = env.step(RIGHT)
    q_update(q, state, RIGHT, result.reward, result.state, result.terminated)

    print()
    print("Q-table after two updates (all other entries still 0.00):")
    print(f"  Q[3][right] = {q[3][RIGHT]:.2f}")
    print(f"  Q[2][right] = {q[2][RIGHT]:.2f}")
    print()
    print("Checkpoint 3 repeats this update over many episodes with an")
    print("exploration strategy, then compares the learned policy to the")
    print("Week 01 baselines.")


if __name__ == "__main__":
    main()
