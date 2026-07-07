# WAM Research Notes

World Action Models are an emerging research direction. In this course, WAM is
treated as an experimental extension of classical robot learning, not as a
settled recipe.

## Working Definition

A World Action Model learns representations that connect observations, actions,
and predicted future world states. In robot learning, this can support planning,
representation learning, policy learning, or action generation.

## Why It Matters

Classical RL often learns directly from reward. VLA policies often map image and
language inputs directly to actions. WAM-style systems ask whether learning to
predict world evolution can improve control.

The key research question is not simply:

> Can the model imagine the future?

The more useful question is:

> Does world-model supervision improve action selection, robustness, data
> efficiency, or evaluation?

## Course Treatment

The course will introduce WAMs only after learners understand:

- MDPs and baselines.
- Value learning and policy learning.
- Continuous robot control.
- Imitation learning and robot datasets.
- VLA action representations.

## Evaluation Rules

WAM experiments should report:

- Task and benchmark.
- Observation and action representation.
- Whether future prediction is used during training, inference, or both.
- Latency.
- Success rate.
- Baseline VLA or imitation-learning method.
- Failure modes.

## Reading Anchor

Fast-WAM is a useful discussion point because it asks whether WAM gains come
from explicit test-time imagination or from video co-training during training:

- [Fast-WAM project page](https://yuantianyuan01.github.io/FastWAM/)

This course will use that kind of question-driven framing rather than treating
new model families as automatic progress.
