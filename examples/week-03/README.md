# Week 03 Examples - Bellman Error and DQN Mechanics

Runnable code for Week 03. These checkpoints are dependency-free so learners can
inspect the Bellman-error machinery before moving to full PyTorch DQN.

| File | What it shows |
| --- | --- |
| `env.py` | LineWorld with `terminated` / `truncated`, reused for the training checkpoint. |
| `01_bellman_error.py` | Compute a Bellman target, temporal-difference error, and squared loss by hand. |
| `02_gradient_step.py` | Turn Bellman error into one parameter update for a tiny Q approximator. |
| `03_train_linear_q.py` | Train a linear DQN-style approximator with a periodically synced target copy. |

Run each checkpoint from the repository root:

```bash
python examples/week-03/01_bellman_error.py
python examples/week-03/02_gradient_step.py
python examples/week-03/03_train_linear_q.py
```

## The One Equation

```text
target = reward + gamma * max_a' Q_target(next_state, a')
loss   = (target - Q_theta(state, action))^2
```

If the transition reaches a true terminal state, the future-value term is
dropped:

```text
target = reward
```

## Expected Output

Checkpoint 1 computes a non-terminal Bellman error:

```text
target: 0.44
td_error = target - prediction = 0.34
squared Bellman error: 0.1156
```

Checkpoint 2 performs one gradient step and reduces the local error:

```text
Before update
  Q_theta(2, right): 0.10
  Bellman target: 0.44
  squared Bellman error: 0.1156

After update
  Q_theta(2, right): 0.31
  squared Bellman error: 0.0163
```

Checkpoint 3 trains over many episodes and evaluates policies:

```text
policy          avg return  success rate
random                0.52          65%
always right          0.97         100%
linear-q              0.97         100%
```

## Why This Is Not Full DQN Yet

Full DQN uses a neural network, a replay buffer, and a target network. This week
isolates the Bellman-error objective and target-network idea with a tiny linear
approximator. Week 04 will make replay and target-network stability the main
story.

## Limitation Note

A linear approximator solving LineWorld is a useful teaching result, not a deep
RL benchmark. The correct claim is narrow: in this tiny deterministic world,
the Bellman-error update learned right-moving action values well enough to match
the heuristic baseline.
