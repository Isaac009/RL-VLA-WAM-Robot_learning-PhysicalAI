# Week 01 - MDPs and Baselines

## Why This Matters

Reinforcement learning is not "reward goes up, therefore intelligence happened."
It is controlled interaction under uncertainty. Before we trust an algorithm, we
must be able to name the state, action, reward, transition, termination rule,
baseline, and metric.

This week builds that discipline in the smallest possible world.

## Learning Objectives

By the end of this week, learners should be able to:

- Define state, action, reward, transition, and termination.
- Explain why a random policy is useful.
- Read a simple environment loop.
- Compute a simple episode return.
- Distinguish "the agent failed" from "the environment is ill-defined."

## Reading Materials

Required:

- **Sutton and Barto, Reinforcement Learning: An Introduction**, Chapter 3:
  focus on the agent-environment interface, goals, rewards, returns, and MDPs.
  Use the official PDF: [http://incompleteideas.net/book/RLbook2020.pdf](http://incompleteideas.net/book/RLbook2020.pdf).
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

## Concept

Reinforcement learning starts with an interaction loop:

1. The agent observes a state.
2. The agent chooses an action.
3. The environment returns the next state, reward, and ending signals.
4. The process repeats until the episode ends.

Before adding neural networks, simulators, or foundation models, the loop must
be inspectable.

### Simple Visual: Interaction Loop

```text
state_t  ->  agent  ->  action_t
   ^                         |
   |                         v
next state, reward <- environment
```

The agent controls actions. The environment controls state changes, rewards,
and episode endings.

## Visual Artifact

![MDP interaction loop](../assets/images/week1_mdp_loop.svg)

## Equation

A finite Markov decision process is often written as:

```text
MDP = (S, A, P, R, gamma)
```

Where:

- `S` is the set of states.
- `A` is the set of actions.
- `P(s' | s, a)` is the transition rule.
- `R(s, a, s')` is the reward rule.
- `gamma` is the discount factor for future rewards.

For this week's LineWorld:

```text
S = {0, 1, 2, 3, 4}
A = {left, right}
start = 0
goal = 4
reward = +1.00 at the goal, otherwise -0.01 per step
```

The episode return used by the examples is the sum of rewards:

```text
G = r_0 + r_1 + ... + r_T
```

In this tiny undiscounted rollout, a shorter path has a larger return because
every unnecessary move costs `-0.01`.

## Algorithm: Random Rollout Baseline

This is not a learning algorithm yet. It is the minimum experiment every later
algorithm must beat.

```text
Create the environment
Reset the environment and observe the initial state
Set episode_return = 0

While the episode is not done:
    Choose a random action
    Step the environment with that action
    Observe next_state, reward, done
    Add reward to episode_return
    Render or print the transition

Report episode_return
```

Read the algorithm as a contract: if a later learner cannot outperform this
random baseline, we have not demonstrated learning.

## Code Lens

In `examples/week-01/01_random_policy.py`, the state is the agent position in a
1D world. The environment itself lives in `examples/week-01/env.py`. The
actions are left and right. The reward is `-0.01` for each non-goal move and
`+1.0` for reaching the goal.

This tiny setup is deliberately small. It lets us see the full rollout, line by
line, before hiding the environment behind a framework.

Run the first checkpoint:

```bash
python examples/week-01/01_random_policy.py
```

Then run the baseline comparison:

```bash
python examples/week-01/02_baseline_policy.py
```

## Metric

The baseline comparison prints:

```text
policy          avg return  success rate
random                0.52          65%
always right          0.97         100%
```

How to read it:

- **Average return**: how much reward the policy collects per episode, on
  average. It is graded. Every wasted step costs `-0.01`, so a policy that
  wanders before reaching the goal scores lower than one that goes straight
  there.
- **Success rate**: how often the policy reaches the goal at all. It is binary
  per episode. It cannot distinguish a 4-step solution from a 19-step one.

One rollout is an anecdote; an average is a measurement. The single seed-7
episode in checkpoint 1 returned `-0.20`, yet the same random policy averages
`+0.52` over 100 episodes.

## Baseline

The random policy is the first baseline. It represents "no task knowledge" in
this environment. Any method that cannot beat it has not earned our trust.

The "always right" policy is a diagnostic heuristic. It wins because it already
knows the goal is on the right:

```text
policy(state) = right
```

That makes it a useful ceiling for LineWorld, not a general RL method. Week 02
asks whether an agent can learn this behavior from experience instead of being
told.

## Failure Mode

Common mistakes in Week 01:

- Judging a policy from one rollout instead of many episodes.
- Treating success rate as the only metric.
- Forgetting that a timeout is an environment design choice.
- Comparing a learned method to no baseline.
- Calling the always-right heuristic "intelligent" when it simply encodes the
  answer for this toy world.

The two metrics can disagree. A policy that always reaches the goal but wanders
first has a 100% success rate and a mediocre average return. Which metric
matters depends on the task. A delivery robot that always arrives late is not a
success.

## Discussion Questions

1. Why does the non-goal step penalty encourage shorter paths?
2. What would happen if the goal reward were also `-0.01`?
3. Why is timeout termination important?
4. What information would a robot arm reaching task need in its state?
5. What would be a bad reward function for a robot reaching task?

## Robotics Bridge

For a robot reaching task, the same MDP questions remain:

- State might include joint angles, end-effector pose, target pose, and camera
  observations.
- Action might be joint velocity, torque, end-effector delta pose, or a higher
  level skill command.
- Reward might combine distance-to-target, task completion, collision
  penalties, and control smoothness.
- Termination might happen on success, collision, timeout, or unsafe state.

The algorithm matters, but the MDP usually decides whether learning is
possible.

## Resources

- [Lab 01 - Inspect a Tiny MDP](../labs/lab-01.md): the hands-on checklist for
  this lecture.
- [Week 01 examples](https://github.com/Isaac009/RL-VLA-WAM-Robot_learning-PhysicalAI/tree/main/examples/week-01): runnable checkpoints
  and expected behavior.
- [Course resources](../resources.md): curated references for the full track.

## Quiz

After the lab, complete the [Week 01 quiz](../quizzes/week-01.md). It checks
whether you can read a rollout, compute a return, and explain why baselines
matter.
