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

The canonical week-by-week plan lives in the
[syllabus](docs/syllabus.md); this file intentionally does not duplicate it.
In one line: MDPs and baselines → tabular and deep Q-learning → policy
gradients, PPO, and SAC → robot simulation and imitation learning →
vision-language-action policies → World Action Models → a reproducible final
project.

## Community Direction

This course should help learners reproduce ideas and understand tradeoffs. New
resources should be curated with a reason, not merely collected. New labs should
include setup, expected output, a baseline, and a limitation note.
