"""Tiny LineWorld environment for Week 03 function-approximation examples."""

from __future__ import annotations

from dataclasses import dataclass

ACTION_NAMES = ("left", "right")
ACTION_DELTAS = (-1, 1)


@dataclass(frozen=True)
class StepResult:
    state: int
    reward: float
    terminated: bool
    truncated: bool


class LineWorld:
    """A deterministic 1D environment with a goal on the right."""

    def __init__(self, size: int = 5, max_steps: int = 20) -> None:
        if size < 2:
            raise ValueError("LineWorld needs at least two states")
        self.size = size
        self.goal = size - 1
        self.max_steps = max_steps
        self.state = 0
        self.steps = 0

    def reset(self, start: int = 0) -> int:
        if not 0 <= start < self.size:
            raise ValueError(f"start must be in [0, {self.size - 1}]")
        self.state = start
        self.steps = 0
        return self.state

    def step(self, action: int) -> StepResult:
        if action not in (0, 1):
            raise ValueError("action must be 0 (left) or 1 (right)")

        self.steps += 1
        self.state = min(self.goal, max(0, self.state + ACTION_DELTAS[action]))
        terminated = self.state == self.goal
        truncated = self.steps >= self.max_steps and not terminated
        reward = 1.0 if terminated else -0.01
        return StepResult(self.state, reward, terminated, truncated)

    def render(self) -> str:
        cells = ["."] * self.size
        cells[self.goal] = "G"
        if self.state != self.goal:
            cells[self.state] = "A"
        return " ".join(cells)
