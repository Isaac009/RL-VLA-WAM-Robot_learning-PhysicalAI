"""Week 04, checkpoint 1: inspect replay order without claiming i.i.d. data.

Uniform replay sampling can spread a minibatch across more of the stored
timeline and reuse older transitions. It does not make an evolving replay
distribution literally independent and identically distributed.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from env import LineWorld


@dataclass(frozen=True)
class Transition:
    step_id: int
    state: int
    action: int
    reward: float
    next_state: int
    terminated: bool
    truncated: bool


class ReplayBuffer:
    """Fixed-capacity circular buffer for transition tuples."""

    def __init__(self, capacity: int = 512) -> None:
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


def pairwise_gaps(step_ids: list[int]) -> list[int]:
    """Original-timeline gaps for every unordered pair in a sample set."""
    return [
        abs(right - left)
        for index, left in enumerate(step_ids)
        for right in step_ids[index + 1 :]
    ]


def mean_pairwise_gap(step_ids: list[int]) -> float:
    gaps = pairwise_gaps(step_ids)
    return sum(gaps) / len(gaps) if gaps else 0.0


def adjacent_pair_rate(step_ids: list[int]) -> float:
    """Fraction of all sample pairs adjacent in the original timeline."""
    gaps = pairwise_gaps(step_ids)
    return sum(gap == 1 for gap in gaps) / len(gaps) if gaps else 0.0


def main() -> None:
    rng = random.Random(42)
    env = LineWorld(size=5, max_steps=20)
    replay = ReplayBuffer(capacity=512)
    collected: list[Transition] = []

    step_id = 0
    for _ in range(20):
        state = env.reset(start=rng.randint(0, 3))

        while True:
            action = rng.choice([0, 1])
            result = env.step(action)
            transition = Transition(
                step_id=step_id,
                state=state,
                action=action,
                reward=result.reward,
                next_state=result.state,
                terminated=result.terminated,
                truncated=result.truncated,
            )
            collected.append(transition)
            replay.push(transition)
            step_id += 1
            state = result.state

            if result.terminated or result.truncated:
                break

    batch = replay.sample(batch_size=32, rng=rng)
    sequential_ids = [
        transition.step_id for transition in collected[: len(batch)]
    ]
    sampled_ids = [transition.step_id for transition in batch]

    print("=== Week 04 Checkpoint 1: Replay Sample Diagnostics ===")
    print(f"Transitions collected: {len(collected)}")
    print(f"Replay buffer size: {len(replay)}")
    print(f"Sampled batch size: {len(batch)}\n")
    print(f"{'sample set':<22}{'mean pair gap':>16}{'adjacent-pair rate':>22}")
    print(
        f"{'sequential rollout':<22}"
        f"{mean_pairwise_gap(sequential_ids):>16.2f}"
        f"{adjacent_pair_rate(sequential_ids):>21.1%}"
    )
    print(
        f"{'uniform replay batch':<22}"
        f"{mean_pairwise_gap(sampled_ids):>16.2f}"
        f"{adjacent_pair_rate(sampled_ids):>21.1%}"
    )

    print("\nFirst five sampled transitions:")
    for transition in batch[:5]:
        action_name = "right" if transition.action == 1 else "left"
        print(
            f"  t={transition.step_id:>3}: "
            f"s={transition.state} --{action_name}--> "
            f"s'={transition.next_state}, r={transition.reward:+.2f}, "
            f"terminated={transition.terminated}, "
            f"truncated={transition.truncated}"
        )

    print("\nThis replay sample spans the stored timeline more broadly than the")
    print("equal-size sequential window. This one diagnostic does not")
    print("prove that replay data are truly i.i.d.")


if __name__ == "__main__":
    main()
