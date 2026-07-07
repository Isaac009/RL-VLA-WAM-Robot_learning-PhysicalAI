"""Step 1 of the RL mini-course: build and inspect a tiny MDP.

This file intentionally uses only the Python standard library. The point is to
understand the environment loop before adding NumPy, PyTorch, Gymnasium, robot
simulators, VLA models, or World Action Models.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


LEFT = 0
RIGHT = 1
ACTION_NAMES = {
    LEFT: "left",
    RIGHT: "right",
}


@dataclass
class StepResult:
    state: int
    reward: float
    done: bool


class LineWorld:
    """A minimal 1D world.

    State:
        The agent position, represented as an integer.

    Actions:
        0 moves left, 1 moves right.

    Reward:
        -0.01 for each non-terminal step, +1.0 for reaching the goal.
    """

    def __init__(self, size: int = 5, max_steps: int = 20) -> None:
        if size < 2:
            raise ValueError("size must be at least 2")

        self.size = size
        self.max_steps = max_steps
        self.goal = size - 1
        self.position = 0
        self.steps = 0

    def reset(self) -> int:
        self.position = 0
        self.steps = 0
        return self.position

    def step(self, action: int) -> StepResult:
        if action not in ACTION_NAMES:
            raise ValueError(f"unknown action: {action}")

        self.steps += 1

        if action == LEFT:
            self.position = max(0, self.position - 1)
        elif action == RIGHT:
            self.position = min(self.goal, self.position + 1)

        reached_goal = self.position == self.goal
        timed_out = self.steps >= self.max_steps
        # A single `done` flag conflates two different endings: reaching the
        # goal (termination) and running out of steps (truncation). Gymnasium
        # separates these into `terminated` and `truncated` because the
        # distinction changes value bootstrapping; we split them in Step 2.
        done = reached_goal or timed_out
        reward = 1.0 if reached_goal else -0.01

        return StepResult(state=self.position, reward=reward, done=done)

    def render(self) -> str:
        cells = ["."] * self.size
        cells[self.goal] = "G"
        cells[self.position] = "A"
        return " ".join(cells)


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
