# Lab 02 - Inspect a Q-Table

## Goal

Build intuition for tabular Q-learning before running a full training loop.
This lab is deliberately small: first read an empty Q-table, then compute two
updates by hand.

## Setup

This lab uses only the Python standard library.

```bash
python examples/week-02/01_q_table_intro.py
python examples/week-02/02_q_learning_update.py
python examples/week-02/03_train_q_learning.py
```

## Tasks

1. Run checkpoint 1.
2. Identify how many states and actions the table has.
3. Explain why all entries begin at `0.00`.
4. Predict which table entry should become largest after learning.
5. Run checkpoint 2.
6. Write down the values of `alpha` and `gamma`.
7. Recompute the first update by hand.
8. Recompute the second update by hand.
9. Explain why `Q[2][right]` increases even though the immediate reward is
   `-0.01`.
10. Run checkpoint 3.
11. Record the learned Q-table.
12. Compare random, always-right, and Q-learning by average return and success
    rate.
13. Explain why matching the always-right baseline is a success here, but not a
    broad claim about all environments.

## Expected Observation

Checkpoint 1 prints an empty table:

```text
State 0:
  left  -> 0.00
  right -> 0.00
```

Checkpoint 2 ends with:

```text
Q[3][right] = 0.50
Q[2][right] = 0.22
```

Checkpoint 3 trains over many episodes and evaluates policies:

```text
policy          avg return  success rate
random                0.52          65%
always right          0.97         100%
q-learning            0.97         100%
```

## Baseline Connection

Week 01 showed that the hand-written "always right" policy gets the best score
in LineWorld. Week 02 is not allowed to encode that rule directly. Instead, it
starts learning action values from transitions.

## Metric

For checkpoints 1 and 2, the metric is arithmetic:

```text
Did the table cell move toward the Bellman target?
```

For checkpoint 3, the metrics return from Week 01:

- average return
- success rate

The new comparison asks whether the learned greedy policy can match the simple
hand-written heuristic.

## Reflection Questions

- What does `Q[3][right]` mean in plain language?
- Why does the first update drop the future-value term?
- Why does the second update keep the future-value term?
- What would go wrong if a timeout were treated like a terminal goal state?
- Why is inspecting the table useful before training an agent for many
  episodes?
- Why does checkpoint 3 evaluate the greedy policy instead of the exploratory
  epsilon-greedy behavior?
- What does Q-learning discover that the always-right heuristic already knew?

## Extension

Change `ALPHA` in `examples/week-02/02_q_learning_update.py` from `0.5` to
`1.0`.

Before running the script, predict:

- What should `Q[3][right]` become?
- What should `Q[2][right]` become?

Then run the script and compare.

## Limitation Note

This lab still uses a tiny deterministic world. Q-learning matching the
always-right heuristic is a good local result, not a general robotics result.
Week 03 starts moving toward function approximation, where a table is no
longer enough.
