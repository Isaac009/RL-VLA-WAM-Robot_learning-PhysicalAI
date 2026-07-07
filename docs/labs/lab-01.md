# Lab 01 - Inspect a Tiny MDP

## Goal

Run a tiny environment and identify each part of the RL interaction loop.

## Visual Reference

Use the [MDP interaction loop diagram](../assets/images/week1_mdp_loop.svg) as
the map for this lab: observe state, choose action, receive reward and next
state, then repeat.

## Setup

This lab uses only the Python standard library.

```bash
python getting_started.py
```

## Tasks

1. Run the script once.
2. Identify the initial state.
3. Record the sequence of actions.
4. Record the sequence of rewards.
5. Explain why the episode ended.
6. Change the random seed and compare the rollout.
7. Change `max_steps` and explain the effect.

## Expected Observation

With the default seed, the random policy does not reach the goal before timeout.
The episode return is negative because the agent collects the step penalty until
the episode ends.

## Questions to Answer

- What is the state representation?
- What is the action space?
- What is the reward function?
- Is the transition deterministic or stochastic?
- What is the baseline policy?
- What would success look like?

## Extension

Add a simple heuristic policy:

```text
Always move right.
```

Compare its episode return to the random policy. This prepares the next lab,
where we add tabular Q-learning.
