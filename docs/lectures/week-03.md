# Week 03 - Bellman Error and DQN

[Download Lecture Slide Deck (PDF)](week-03-slides.pdf){ .md-button .md-button--primary }

## Why This Matters

A Q-table works when the state-action space is tiny. Robot learning does not
stay tiny for long: states can be joint angles, camera embeddings, histories,
or language-conditioned observations. Deep Q-learning keeps the Bellman target
from Week 02, but replaces the table with a function approximator.

This week teaches the pressure point: the agent trains a model by minimizing
Bellman error. If that error is constructed incorrectly, the learned policy can
look busy while learning the wrong thing.

## Learning Objectives

By the end of this week, learners should be able to:

- Explain why a Q-table does not scale to large or continuous state spaces.
- Define a Bellman target for terminal and non-terminal transitions.
- Compute a squared Bellman error by hand.
- Explain the difference between `Q_theta` and `Q_target`.
- Describe the DQN training loop, including replay and target networks.
- Evaluate a learned Q approximator against random and heuristic baselines.

## Reading Materials

Required:

- **Sutton and Barto, Reinforcement Learning: An Introduction**, Chapter 6 and
  the start of Chapter 9: review temporal-difference learning, then skim how
  prediction changes when values are approximated. Use the official PDF:
  [http://incompleteideas.net/book/RLbook2020.pdf](http://incompleteideas.net/book/RLbook2020.pdf).
- **Mnih et al., Human-level control through deep reinforcement learning**:
  read the abstract and focus on the idea of combining Q-learning with a deep
  network, replay, and a target network:
  [https://doi.org/10.1038/nature14236](https://doi.org/10.1038/nature14236).
- **PyTorch DQN tutorial**: skim the model, replay memory, target network, and
  optimization sections. This is the implementation path for a full DQN:
  [https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html](https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html).

Optional:

- **OpenAI Spinning Up, Key Concepts in RL**: revisit Q-functions and Bellman
  equations if the target/loss connection still feels slippery:
  [https://spinningup.openai.com/en/latest/spinningup/rl_intro.html](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html).

Reading target: after reading, you should be able to say what the target is,
what the prediction is, and which network supplies each one.

## Concept

Week 02 stored values directly:

```text
Q[state][action]
```

Week 03 predicts them with parameters:

```text
Q_theta(state, action)
```

A table asks, "What number is stored in this cell?" A function approximator
asks, "What number does my model predict for this state-action pair?"

### Simple Visual: Table to Function

```text
Week 02: tabular Q-learning

state, action  ->  lookup cell  ->  Q[state][action]

Week 03: DQN idea

state, action  ->  model with parameters theta  ->  Q_theta(state, action)
```

The tradeoff is powerful but dangerous. A table update changes one cell. A
function-approximation update changes parameters that can affect many states.
That is why the loss, data distribution, replay buffer, and target network all
matter.

## Visual Artifact

Open the [Week 03 Bellman target animation](../assets/animations/week3_bellman_target.html).
It shows reward and next-state value becoming a target, then the target being
compared against the current prediction.

## Equation

For one transition:

```text
(state, action, reward, next_state, terminated)
```

The Bellman target is:

```text
if terminated:
    y = reward
else:
    y = reward + gamma * max_a' Q_target(next_state, a')
```

The prediction is:

```text
prediction = Q_theta(state, action)
```

The Bellman error, squared diagnostic, and optimization loss are:

```text
td_error = y - Q_theta(state, action)
squared_error = (td_error)^2
loss(theta) = 0.5 * (td_error)^2
```

The factor `0.5` makes the gradient especially easy to read: its derivative
cancels the factor of two from the square. Gradient descent then changes
`theta` so the prediction moves toward the target. Reporting the unsmoothed
`squared_error` is still useful for hand arithmetic; the two quantities differ
only by a constant scale.
The target is usually computed with a delayed copy of the model, written here
as `Q_target`, so the target does not move every time the online network moves.

### Simple Visual: Prediction Versus Target

```text
reward + discounted next value  ->  target y
current model prediction        ->  Q_theta(s, a)

difference                      ->  td_error
half the squared difference     ->  optimization loss
```

A smaller Bellman loss is useful only if the targets are meaningful and the
policy improves under evaluation.

## Algorithm: DQN Training Loop

Full DQN uses the same target/loss idea, but trains from batches of stored
transitions.

```text
Initialize online network Q_theta
Initialize target network Q_target as a copy of Q_theta
Initialize replay buffer

For each environment step:
    Choose an action, usually epsilon-greedy from Q_theta
    Step the environment
    Store (state, action, reward, next_state, terminated, truncated) in replay

    Sample a minibatch of transitions from replay

    For each transition in the minibatch:
        If terminated:
            target = reward
        Else:
            target = reward + gamma * max_a' Q_target(next_state, a')

        prediction = Q_theta(state, action)
        loss = mean(0.5 * (target - prediction)^2)

    Update Q_theta by gradient descent on the loss

    Every fixed number of steps:
        Copy Q_theta into Q_target
```

DQN combines three important operational components:

1. **Replay buffer**: samples across stored history, reducing the dominance of
   adjacent recent transitions.
2. **Target network**: usually slows how quickly the target values move.
3. **Epsilon-greedy exploration**: gives non-greedy actions a nonzero sampling
   probability; it does not guarantee adequate coverage.

This week uses a smaller dependency-free version to isolate the loss. Week 04
makes replay and target-network stability the main experiment.

## Algorithm Walkthrough in LineWorld

Suppose the model currently predicts:

```text
Q_theta(2, right) = 0.10
```

The target network estimates the next state:

```text
Q_target(3, left)  = 0.20
Q_target(3, right) = 0.50
```

The transition is non-terminal:

```text
state 2 --right--> state 3, reward -0.01
```

So:

```text
y = -0.01 + 0.9 * max(0.20, 0.50)
  = -0.01 + 0.45
  = 0.44
```

The Bellman error is:

```text
td_error = 0.44 - 0.10 = 0.34
squared_error = 0.34^2 = 0.1156
loss = 0.5 * 0.1156 = 0.0578
```

Training nudges the model so `Q_theta(2, right)` moves closer to `0.44`.

## Code Lens

Run:

```bash
python examples/week-03/01_bellman_error.py
python examples/week-03/02_gradient_step.py
python examples/week-03/03_train_linear_q.py
```

Checkpoint 1 computes the Bellman target and loss. Checkpoint 2 performs one
parameter update. Checkpoint 3 repeats the idea over many LineWorld episodes
with epsilon-greedy exploration and a periodically synced target copy.

As in Week 02, exact value ties break toward `left`. The untrained model
therefore does not receive the useful `always right` behavior for free.

The checkpoint 3 model is intentionally tiny:

```text
Q_theta(state, action) = bias[action] + slope[action] * normalized_state
```

That is not full DQN. It is a transparent bridge from tabular Q-learning to
neural Q-learning.

## Metric

Week 03 has two levels of measurement:

- **Local loss**: did a Bellman-error update move the prediction toward the
  target?
- **Policy evaluation**: did the learned greedy policy improve average return
  and success rate against baselines?

Checkpoint 3 reports both the recent Bellman loss and the familiar policy
comparison:

```text
policy          avg return  success rate
random                0.52          65%
always right          0.97         100%
linear-q              0.97         100%
```

Do not trust loss alone. A model can reduce loss on poor targets, biased data,
or a narrow replay distribution and still fail as a policy.

## Baseline

Use the same baselines as Weeks 01 and 02:

- **Random**: no task knowledge.
- **Always right**: a hand-written heuristic that knows this fixed LineWorld.
- **Week 02 tabular Q-learning**: the simpler learned reference method.

The Week 03 claim is narrow:

```text
A tiny Q approximator trained with Bellman-error updates learned the useful
right-moving policy in this deterministic LineWorld.
```

It is not a claim that deep Q-learning is solved, robust, or robot-ready.

## Failure Mode

Common mistakes in Week 03:

- Using the online network for both prediction and a rapidly moving target.
- Forgetting to drop the future term on true terminal transitions.
- Dropping the future term on time-limit truncations.
- Reporting loss without policy evaluation.
- Believing a lower Bellman loss always means better control.
- Treating the dependency-free linear example as full DQN.
- Forgetting that function approximation can change many predictions at once.

## Robotics Bridge

Robot-learning states are rarely small table indices. A reaching policy might
condition on joint angles, end-effector pose, target pose, camera features, or
a language-conditioned goal. In those settings, value functions are usually
approximated by models.

The DQN lesson to carry forward is not "use DQN for every robot task." The
lesson is:

```text
when a learned value function drives action selection, audit the target,
the data distribution, the baseline, and the metric.
```

For continuous robot actions, later methods such as actor-critic, DDPG, TD3,
SAC, and PPO become more natural than vanilla DQN. The Bellman-error discipline
still matters.

## Limitation Note

The runnable model is a two-feature linear approximator in deterministic
LineWorld. It demonstrates Bellman-target and gradient mechanics, not neural
DQN stability, high-dimensional generalization, or robot-control performance.

## Resources

- [Lab 03 - Bellman Error as a Loss](../labs/lab-03.md): the hands-on workflow
  for this lecture.
- [Week 03 examples](https://github.com/Isaac009/RL-VLA-WAM-Robot_learning-PhysicalAI/tree/main/examples/week-03): runnable checkpoints and expected output.
- [Week 03 Bellman target animation](../assets/animations/week3_bellman_target.html): visual intuition for target construction and squared error.

## Quiz

After the lab, complete the [Week 03 quiz](../quizzes/week-03.md). It checks
whether you can compute a Bellman target, explain DQN stabilizers, and avoid
overclaiming from a tiny function-approximation result.
