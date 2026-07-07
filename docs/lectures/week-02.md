# Week 02 - Tabular Q-Learning

## Objectives

By the end of this week, learners should be able to:

- Explain what a Q-table stores.
- Read `Q[state][action]` as an action-value estimate.
- Compute one Q-learning update by hand.
- Explain the Bellman target and temporal-difference error.
- Distinguish terminal endings from time-limit truncations.

## Reading Materials

Required:

- **Sutton and Barto, Reinforcement Learning: An Introduction**, Chapter 6:
  focus on temporal-difference learning and Q-learning. Use the official book
  page: [incompleteideas.net/book/the-book-2nd.html](https://incompleteideas.net/book/the-book-2nd.html).
- **OpenAI Spinning Up, Key Concepts in RL**: read value functions, the optimal
  Q-function, and Bellman equations:
  [spinningup.openai.com/en/latest/spinningup/rl_intro.html](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html).
- **Hugging Face Deep RL Course, Unit 2**: read the introduction to Q-learning
  and the Q-learning example:
  [huggingface.co/learn/deep-rl-course/unit2/introduction](https://huggingface.co/learn/deep-rl-course/unit2/introduction).

Optional:

- **Gymnasium Basic Usage**: revisit `terminated` and `truncated`; this week
  uses that distinction in the update target:
  [gymnasium.farama.org/introduction/basic_usage](https://gymnasium.farama.org/introduction/basic_usage/).

Reading target: after reading, you should be able to say what `Q(s, a)` means
and why the update uses reward plus estimated future value.

## Core Idea

Week 01 used a hand-written rule:

```text
Always move right.
```

Week 02 asks a better question:

```text
Can the agent learn that "right" is useful from experience?
```

Tabular Q-learning stores one value for every state-action pair:

```text
Q[state][action] = expected future return
```

At the beginning, the table is empty knowledge:

```text
Q[0][left]  = 0.00
Q[0][right] = 0.00
```

The agent has no reason to prefer left or right yet.

## Math Core

The update is:

```text
Q(s, a) <- Q(s, a) + alpha * (target - Q(s, a))

target = r + gamma * max_a' Q(s', a')
```

Where:

- `s` is the current state.
- `a` is the action taken.
- `r` is the reward received.
- `s'` is the next state.
- `alpha` is the learning rate.
- `gamma` discounts future value.
- `target - Q(s, a)` is the temporal-difference error.

If `s'` is terminal, the future term is dropped:

```text
target = r
```

There is no future after a true terminal state.

## Code Lens

Run:

```bash
python examples/week-02/01_q_table_intro.py
python examples/week-02/02_q_learning_update.py
```

The Week 02 environment lives in `examples/week-02/env.py`. It is almost the
same as Week 01, but the ending is more precise:

- `terminated=True`: the agent reached the goal.
- `truncated=True`: the step limit stopped the rollout.

Q-learning should drop the future-value term only on `terminated=True`.

## Visual Artifact

Open the [Week 02 Q-table heatmap](../assets/animations/week2_q_table.html).
It shows value estimates spreading backward through the table as rightward
actions become useful.

## What the Two Checkpoints Teach

Checkpoint 1:

```text
python examples/week-02/01_q_table_intro.py
```

This prints an empty Q-table. No learning happens yet. The goal is to inspect
the object before trusting an algorithm to mutate it.

Checkpoint 2:

```text
python examples/week-02/02_q_learning_update.py
```

This performs two hand-checkable updates:

```text
Q[3][right] = 0.50
Q[2][right] = 0.22
```

The first update touches the goal reward directly. The second update never
sees the goal, but it still increases because it bootstraps from the value
already learned at state 3.

That backward spread of value is the little engine inside Q-learning.

## Common Failure Modes

- Updating the wrong table cell.
- Forgetting to drop the future term at a terminal state.
- Dropping the future term at a timeout, which incorrectly treats truncation as
  death.
- Looking only at final policy behavior instead of inspecting the Q-values.
- Letting tie-breaking hide the fact that an untrained table knows nothing.

## Bridge to Robotics

Most robot tasks cannot use a small table because states and actions are too
large or continuous. But the idea survives:

```text
learn which actions are valuable in which situations
```

DQN later replaces the table with a neural network. Actor-critic methods later
replace or augment action-value tables with learned value functions. The table
is small, but the habit is foundational: inspect the value estimate, not just
the reward curve.

## Quiz

After the lab, complete the [Week 02 quiz](../quizzes/week-02.md). It checks
whether you can read a Q-table and compute a Bellman update by hand.
