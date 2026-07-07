# Week 01 - MDPs and Baselines

## Objectives

By the end of this week, learners should be able to:

- Define state, action, reward, transition, and termination.
- Explain why a random policy is useful.
- Read a simple environment loop.
- Distinguish "the agent failed" from "the environment is ill-defined."

## Reading Materials

Required:

- **Sutton and Barto, Reinforcement Learning: An Introduction**, Chapter 3:
  focus on the agent-environment interface, goals, rewards, returns, and MDPs.
  Use the official book page: [incompleteideas.net/book/the-book-2nd.html](https://incompleteideas.net/book/the-book-2nd.html).
- **Gymnasium Basic Usage**: read the sections on the agent-environment loop,
  `reset()`, `step()`, rewards, `terminated`, and `truncated`:
  [gymnasium.farama.org/introduction/basic_usage](https://gymnasium.farama.org/introduction/basic_usage/).
- **OpenAI Spinning Up, Key Concepts in RL**: skim states, observations,
  action spaces, trajectories, reward, and return:
  [spinningup.openai.com/en/latest/spinningup/rl_intro.html](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html).

Optional:

- **Hugging Face Deep RL Course, Unit 1**: a friendly second pass on the RL
  loop and vocabulary:
  [huggingface.co/learn/deep-rl-course/unit1/introduction](https://huggingface.co/learn/deep-rl-course/unit1/introduction).

Reading target: do not try to memorize every term. After reading, you should be
able to point to one line of code for "state", "action", "reward", and
"episode ended."

## Core Idea

Reinforcement learning starts with an interaction loop:

1. The agent observes a state.
2. The agent chooses an action.
3. The environment returns the next state, reward, and done signal.
4. The process repeats until the episode ends.

Before adding neural networks, simulators, or foundation models, the loop must
be inspectable.

## Visual Artifact

![MDP interaction loop](../assets/images/week1_mdp_loop.svg)

## Mini Example

In `examples/week-01/01_random_policy.py`, the state is the agent position in
a 1D world (the environment itself lives in `examples/week-01/env.py`). The
actions are left and right. The reward is `-0.01` for each non-goal move and
`+1.0` for reaching the goal.

This tiny setup is deliberately small. It lets us see the full rollout, line by
line, before hiding the environment behind a framework.

## Lesson 1.3 - What Did We Actually Measure?

Running `examples/week-01/02_baseline_policy.py` prints the course's first
comparison table:

```text
policy          avg return  success rate
random                0.52          65%
always right          0.97         100%
```

How to read it:

- **Average return**: how much reward the policy collects per episode, on
  average. It is graded — every wasted step costs `-0.01`, so a policy that
  wanders before reaching the goal scores lower than one that goes straight
  there.
- **Success rate**: how often the policy reaches the goal at all. It is
  binary per episode — it cannot distinguish a 4-step solution from a
  19-step one.
- **Baseline**: the random policy is the reference point. 0.52 average
  return and 65% success is what "no intelligence at all" achieves in this
  environment. Any method that cannot beat it has learned nothing.
- **Limitation**: "always right" wins because it already knows the goal is
  on the right. It is a ceiling for this environment, not a method.

Two details worth pausing on:

1. **One rollout is an anecdote; an average is a measurement.** The single
   seed-7 episode in checkpoint 1 returned `-0.20`, yet the same random
   policy averages `+0.52` over 100 episodes. Never judge a policy from one
   episode.
2. **The two metrics can disagree.** A policy that always reaches the goal
   but wanders first has a 100% success rate and a mediocre average return.
   Which metric matters depends on the task — a delivery robot that always
   arrives late is not a success. Choosing the metric is part of defining
   the problem.

This sets up Week 02's question: can an agent *learn* "go right" from
experience, instead of being told? That is where tabular Q-learning enters —
see `examples/week-02/`.

## Discussion Questions

1. Why does the non-goal step penalty encourage shorter paths?
2. What would happen if the goal reward were also `-0.01`?
3. Why is timeout termination important?
4. What information would a robot arm reaching task need in its state?
5. What would be a bad reward function for a robot reaching task?

## Bridge to Robotics

For a robot reaching task, the same MDP questions remain:

- State might include joint angles, end-effector pose, target pose, and camera
  observations.
- Action might be joint velocity, torque, end-effector delta pose, or a higher
  level skill command.
- Reward might combine distance-to-target, task completion, collision penalties,
  and control smoothness.
- Termination might happen on success, collision, timeout, or unsafe state.

The algorithm matters, but the MDP usually decides whether learning is possible.

## Quiz

After the lab, complete the [Week 01 quiz](../quizzes/week-01.md). It checks
whether you can read a rollout, compute a return, and explain why baselines
matter.
