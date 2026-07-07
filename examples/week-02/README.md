# Week 02 Examples - Tabular Q-learning

Runnable code for Week 02. The guiding question, carried over from
[Lesson 1.3](../../docs/lectures/week-01.md): can an agent *learn* "go right"
from experience, instead of being told? Standard library only (Python 3.10+).

| File | What it shows |
| --- | --- |
| `env.py` | LineWorld, adapted from Week 01: `done` is now split into `terminated` / `truncated`, and `reset()` takes a start position. |
| `01_q_table_intro.py` | Build and read an empty Q-table. No learning yet. |
| `02_q_learning_update.py` | Two Q-learning updates by hand, every quantity printed. |
| `03_train_q_learning.py` | *(planned)* Train over episodes, compare to the Week 01 baselines. |

Run each checkpoint from the repository root:

```bash
python examples/week-02/01_q_table_intro.py
python examples/week-02/02_q_learning_update.py
```

## The One Equation

```text
Q(s, a) <- Q(s, a) + alpha * (target - Q(s, a))
target   = reward + gamma * max_a' Q(next_state, a')   # future term dropped
                                                       # if terminated
```

## Expected Output

Checkpoint 1 prints the empty table in this shape:

```text
State 0:
  left  -> 0.00
  right -> 0.00
```

Checkpoint 2 narrates two updates and ends with:

```text
Q[3][right] = 0.50
Q[2][right] = 0.22
```

`Q[3][right]` moves halfway (`alpha = 0.5`) toward the goal reward. The
second update never sees the goal, yet `Q[2][right]` still rises, because its
target bootstraps on `Q[3]` — this backward spread of value is the heart of
the algorithm.

## Why `terminated` vs `truncated` Matters Here

The update target drops the `gamma * max Q(next_state)` term only when the
episode *terminated* (the goal was reached — there is no future). After a
*truncation* (step limit), the world would have continued, so the future term
stays. Folding both into one `done` flag, as Week 01 did, would teach the
agent that timeouts are dead ends.

## Limitation Note

These two checkpoints hand-pick informative transitions. A real agent has to
find them by exploring, which is why checkpoint 3 needs an exploration
strategy before the comparison against the Week 01 baselines is fair.
