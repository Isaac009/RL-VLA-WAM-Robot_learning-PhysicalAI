# Week 01 Examples - MDPs and Baselines

Runnable code for [Week 01](../../docs/lectures/week-01.md) and
[Lab 01](../../docs/labs/lab-01.md). Everything here uses only the Python
standard library (3.10+).

| File | What it shows |
| --- | --- |
| `env.py` | `LineWorld`, the tiny 1D MDP shared by this week's checkpoints. |
| `01_random_policy.py` | A single random-policy rollout, printed step by step. |
| `02_baseline_policy.py` | Random vs. "always right" heuristic over 100 episodes. |

Run each checkpoint from the repository root:

```bash
python examples/week-01/01_random_policy.py
python examples/week-01/02_baseline_policy.py
```

## Expected Output

Checkpoint 1 prints a full rollout and ends with:

```text
Episode return: -0.20
```

With the default seed, the random policy times out before reaching the goal,
so the return is the accumulated step penalty.

Checkpoint 2 prints a comparison table. The random policy reaches the goal in
some episodes but not others; the heuristic succeeds every time with the
maximum possible return (`0.97`: three step penalties, then the goal reward).

## Limitation Note

The "always right" heuristic is optimal only because LineWorld's goal is
always on the right edge — it encodes environment knowledge, not learning.
Week 02 introduces tabular Q-learning, which must discover the same behavior
from experience.
