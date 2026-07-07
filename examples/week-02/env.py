"""LineWorld for Week 02: same dynamics, more honest endings.

Adapted from `examples/week-01/env.py` with two changes:

1. `StepResult` now separates `terminated` (the agent reached the goal, so
   there is no future to learn about) from `truncated` (we stopped the episode
   at a step limit, but the world itself would have continued). Week 01 folded
   both into one `done` flag. Q-learning needs the distinction: the update
   target may only drop the future term when the state is truly terminal.
2. `reset()` accepts an optional start position, so lessons can inspect a
   single transition anywhere in the world.

Still standard library only.
"""

from __future__ import annotations

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
    terminated: bool
    truncated: bool

    @property
    def done(self) -> bool:
        return self.terminated or self.truncated


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

    def reset(self, position: int = 0) -> int:
        if not 0 <= position < self.goal:
            raise ValueError(f"start position must be in [0, {self.goal - 1}]")

        self.position = position
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

        terminated = self.position == self.goal
        truncated = self.steps >= self.max_steps and not terminated
        reward = 1.0 if terminated else -0.01

        return StepResult(
            state=self.position,
            reward=reward,
            terminated=terminated,
            truncated=truncated,
        )

    def render(self) -> str:
        cells = ["."] * self.size
        cells[self.goal] = "G"
        cells[self.position] = "A"
        return " ".join(cells)
