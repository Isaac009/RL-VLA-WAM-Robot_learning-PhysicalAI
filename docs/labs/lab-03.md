# Lab 03 - Bellman Error as a Loss

## Goal

Turn the Week 02 Q-learning update into a supervised-looking loss: build a
Bellman target, compare it with `Q_theta(state, action)`, and update parameters
so the prediction moves toward the target.

## Visual Reference

Use the [Bellman target animation](../assets/animations/week3_bellman_target.html)
as the map for this lab: reward plus next-state value becomes a target; the
prediction is compared to that target; half the squared difference becomes the
optimization loss.

## Setup

This lab uses only the Python standard library.

```bash
python examples/week-03/01_bellman_error.py
python examples/week-03/02_gradient_step.py
python examples/week-03/03_train_linear_q.py
```

## Tasks

1. Run checkpoint 1.
2. Write down the prediction, reward, next-state values, target, TD error, and
   squared Bellman error for the non-terminal transition.
3. Explain why the terminal transition drops the future-value term.
4. Run checkpoint 2.
5. Identify the feature vector for `state=2`.
6. Recompute the right-action bias update by hand.
7. Recompute the right-action state-slope update by hand.
8. Explain why only the parameters for the action taken are updated.
9. Run checkpoint 3.
10. Confirm that exact value ties break toward `left`, so the untrained model
    does not already implement the heuristic.
11. Record the average Bellman loss over the last 100 updates.
12. Record the predicted action values for states 0 through 3.
13. Compare random, always-right, and linear-q by average return and success
    rate.
14. Explain why matching the heuristic is a useful result here but not a broad
    DQN claim.

## Expected Output

Checkpoint 1 includes:

```text
target: 0.44
td_error = target - prediction = 0.34
squared Bellman error: 0.1156
half-squared optimization loss: 0.0578
```

Checkpoint 2 reduces the local loss:

```text
Before update
  Q_theta(2, right): 0.10
  Bellman target: 0.44
  squared Bellman error: 0.1156
  half-squared optimization loss: 0.0578

After update
  Q_theta(2, right): 0.31
  squared Bellman error: 0.0163
  half-squared optimization loss: 0.0081
```

Checkpoint 3 trains over many episodes and evaluates policies:

```text
Average half-squared Bellman loss over last 100 updates: 0.0002

policy          avg return  success rate
random                0.52          65%
always right          0.97         100%
linear-q              0.97         100%
```

## Baseline

The baselines stay visible:

- random policy
- always-right heuristic
- Week 02 tabular Q-learning result as the simpler learned reference

The Week 03 model is not allowed to encode "go right" directly. It must learn
from Bellman-error updates over transitions.

## Metric

Use two metrics:

- **Bellman loss**: local training signal for the value approximator.
- **Average return and success rate**: policy-level evaluation against
  baselines.

Bellman loss is a training diagnostic, not the final result. The policy still
has to be evaluated in the environment.

## Reflection Questions

- What is the difference between `Q_theta` and `Q_target`?
- Why is the target network useful even though it is only a delayed copy?
- What would go wrong if the target used future value after true termination?
- Why can loss decrease while the policy is still bad?
- What does the linear approximator share across states that a Q-table does
  not?
- Why is this checkpoint not enough to claim that we implemented full DQN?
- What extra machinery does full DQN add beyond this lab?

## Extension Challenge

Change `TARGET_SYNC_EPISODES` in `examples/week-03/03_train_linear_q.py` from
`20` to `1`, then to `100`.

Before running each setting, predict:

- Will the recent Bellman loss become smoother or noisier?
- Will the final greedy policy still choose `right` in every non-terminal
  state?
- Why might this question become more serious in larger environments?

Then run the script and compare.

## Limitation Note

This lab uses a tiny deterministic world and a two-parameter-per-action linear
model. It teaches the Bellman-error mechanism behind DQN, but it is not a deep
network benchmark and not a robot-learning result. The correct claim is narrow:
in this LineWorld, the approximator learned a useful greedy policy under the
given settings.
