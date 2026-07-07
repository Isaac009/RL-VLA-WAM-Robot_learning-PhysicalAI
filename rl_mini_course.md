# Applied RL for Robot Learning and Physical AI

This mini-course builds from classical reinforcement learning foundations
toward robot learning, vision-language-action systems, and learned World Action
Models. The course starts deliberately small: before training large policies,
we first make the state, action, reward, transition, and evaluation loop fully
explicit.

## Course Principle

Every step should produce a runnable artifact and a measurable comparison.

- Start from a small environment.
- Define the MDP before choosing an algorithm.
- Keep a simple baseline.
- Log the exact rollout behavior.
- Only add complexity when the previous layer is understood.

## Step 1: Understand the MDP

Before training any agent, define the problem as a Markov Decision Process.

An MDP has five core pieces:

- **State**: What the agent observes.
- **Action**: What the agent can choose.
- **Reward**: The scalar feedback signal.
- **Transition**: How the world changes after an action.
- **Episode termination**: When the rollout ends.

The first coding goal is not to solve the task. It is to build a tiny
environment, run a random policy, and verify that states, actions, rewards, and
termination behave exactly as expected.

## Step 1 Exercise

Run:

```bash
python getting_started.py
```

The script implements a tiny 1D world:

- The agent starts at position `0`.
- The goal is at the right end of the line.
- The agent can move left or right.
- Reaching the goal gives a positive reward.
- Every non-goal move has a small penalty to encourage shorter paths.

## What To Check

After running the script, answer these questions:

1. What is the state?
2. What are the actions?
3. What reward does the agent receive before reaching the goal?
4. What reward does the agent receive at the goal?
5. What does the random policy tell us as a baseline?
6. What would change if this were a robot arm reaching problem?

## Roadmap

### Step 2: Tabular Q-Learning

Add a Q-table to the same environment and compare the learned policy against
the random baseline.

### Step 3: Deep Q-Networks

Replace the table with a neural network and introduce replay buffers, target
networks, and Bellman error.

### Step 4: Policy Gradients and Actor-Critic Methods

Move from discrete toy control to continuous control, where actions can
represent torque, velocity, or position commands.

### Step 5: Robot Simulation

Move into a robotics simulator and define clear task metrics such as reaching
success, collision rate, path length, control smoothness, and energy cost.

### Step 6: Vision-Language-Action Conditioning

Condition policies on visual observations and language goals, while preserving
classical RL baselines for comparison.

### Step 7: World Action Models

Introduce learned predictive models that estimate how actions change the world,
then compare model-based planning or imagination against direct policy learning.
