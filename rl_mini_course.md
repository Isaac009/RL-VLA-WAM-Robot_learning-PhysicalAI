# Applied RL for Robot Learning and Physical AI

This repository is becoming a community course that starts with classical
reinforcement learning and grows toward robot learning, vision-language-action
policies, and World Action Models.

The canonical course site now lives in [`docs/`](docs/) and is configured with
MkDocs. This file remains as the short roadmap for contributors and learners who
open the repository directly.

## Course Principle

Every step should produce a runnable artifact and a measurable comparison.

- Start from a small environment.
- Define the MDP before choosing an algorithm.
- Keep a simple baseline.
- Log the exact rollout behavior.
- Only add complexity when the previous layer is understood.
- State limitations before making claims.

## Step 1: Understand the MDP

Run:

```bash
python getting_started.py
```

Then read:

- [`docs/syllabus.md`](docs/syllabus.md)
- [`docs/lectures/week-01.md`](docs/lectures/week-01.md)
- [`docs/labs/lab-01.md`](docs/labs/lab-01.md)
- [`docs/resources.md`](docs/resources.md)

## Roadmap

1. MDPs, rollouts, rewards, and baselines.
2. Tabular Q-learning.
3. Deep Q-learning.
4. Policy gradients and actor-critic methods.
5. PPO, SAC, and continuous control.
6. Robot simulation and manipulation benchmarks.
7. Imitation learning and robot datasets.
8. Vision-language-action policies.
9. World Action Models.
10. Reproducible final projects.

## Community Direction

This course should help learners reproduce ideas and understand tradeoffs. New
resources should be curated with a reason, not merely collected. New labs should
include setup, expected output, a baseline, and a limitation note.
