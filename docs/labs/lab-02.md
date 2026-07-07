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

## Baseline Connection

Week 01 showed that the hand-written "always right" policy gets the best score
in LineWorld. Week 02 is not allowed to encode that rule directly. Instead, it
starts learning action values from transitions.

## Metric

For this lab, the metric is not success rate yet. The check is arithmetic:

```text
Did the table cell move toward the Bellman target?
```

Full policy evaluation returns in the next checkpoint, where we train across
many episodes.

## Reflection Questions

- What does `Q[3][right]` mean in plain language?
- Why does the first update drop the future-value term?
- Why does the second update keep the future-value term?
- What would go wrong if a timeout were treated like a terminal goal state?
- Why is inspecting the table useful before training an agent for many
  episodes?

## Extension

Change `ALPHA` in `examples/week-02/02_q_learning_update.py` from `0.5` to
`1.0`.

Before running the script, predict:

- What should `Q[3][right]` become?
- What should `Q[2][right]` become?

Then run the script and compare.

## Limitation Note

The two updates in this lab are hand-picked. A real learning agent must explore
the environment, collect transitions, and update the table many times. That is
the next step.
