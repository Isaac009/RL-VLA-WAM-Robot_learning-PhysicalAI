# Lab 01 - Inspect a Tiny MDP

## Goal

Run a tiny environment and identify each part of the RL interaction loop.

## Visual Reference

Use the [MDP interaction loop diagram](../assets/images/week1_mdp_loop.svg) as
the map for this lab: observe state, choose action, receive reward and next
state, then repeat.

## Setup

This lab uses only the Python standard library. The environment lives in
`examples/week-01/env.py`; the rollout script is the first checkpoint:

```bash
python examples/week-01/01_random_policy.py
```

For the baseline comparison, run:

```bash
python examples/week-01/02_baseline_policy.py
```

## Tasks

1. Run checkpoint 1 once.
2. Identify the initial state.
3. Record the sequence of actions.
4. Record the sequence of rewards.
5. Explain why the episode ended.
6. Change the random seed and compare the rollout.
7. Change `max_steps` and explain the effect.
8. Run checkpoint 2.
9. Compare the random policy with the always-right heuristic.

## Expected Output

With the default seed, checkpoint 1 prints a random rollout that does not reach
the goal before timeout. The episode return is negative because the agent
collects the step penalty until the episode ends:

```text
Episode return: -0.20
```

Checkpoint 2 prints the first comparison table:

```text
policy          avg return  success rate
random                0.52          65%
always right          0.97         100%
```

## Baseline

The random policy is the baseline. It chooses actions without task knowledge.
The always-right policy is a heuristic comparison that encodes knowledge of
this specific environment.

A learned method in this LineWorld should beat random behavior. Matching the
always-right heuristic is excellent here, but only because the goal location is
fixed and simple.

## Metric

Use two metrics:

- **Average return**: the mean total reward per episode.
- **Success rate**: the percentage of episodes that reach the goal.

Both are needed. Success rate says whether the goal was reached; average return
also penalizes wandering.

## Reflection Questions

- What is the state representation?
- What is the action space?
- What is the reward function?
- Is the transition deterministic or stochastic?
- Why can the seed-7 rollout return `-0.20` while the random policy's average
  return over 100 episodes is positive?
- Why is `0.97` the maximum possible return in this environment?
- What would success look like if the goal moved each episode?

## Extension Challenge

Add a simple heuristic policy:

```text
Always move right.
```

Write your own version first; then check it against the second checkpoint:

```bash
python examples/week-01/02_baseline_policy.py
```

For an extra check, set `max_steps=5` in `examples/week-01/env.py`, rerun the
comparison, and explain which metric changes first.

## Limitation Note

Both metrics are averages over one fixed environment. They say nothing about
how either policy would do if the goal moved, if actions were noisy, or if the
state were a camera image. Week 02 starts addressing that weakness by learning
action values from experience.
