# Week 04 - Replay and Target Networks

[Download Lecture Slide Deck (PDF)](week-04-slides.pdf){ .md-button .md-button--primary }

## Why This Matters

Function approximation, bootstrapping, and off-policy data can interact
unpredictably. Deep Q-learning may oscillate or diverge, especially when each
update uses the newest correlated transition and the same network supplies both
the prediction and its moving target.

Experience replay and delayed target networks are practical stabilizers. They
often help, but they do not make samples perfectly independent or guarantee
convergence. This week separates what the mechanisms do from what a particular
experiment actually proves.

## Learning Objectives

By the end of this week, learners should be able to:

- Implement a fixed-capacity circular replay buffer.
- Explain how replay changes training order and reuses experience.
- Explain why replay samples are not literally i.i.d.
- Construct Bellman targets with a delayed target network.
- Preserve the distinction between termination and truncation.
- Design and interpret a controlled multi-seed ablation.
- Recognize a valid null result instead of inventing a treatment effect.

## Reading Materials

Required:

- **Sutton and Barto, Reinforcement Learning: An Introduction**, Section 11.3:
  read the deadly triad discussion to understand why function approximation,
  bootstrapping, and off-policy learning can be unstable. Use the
  [official PDF](http://incompleteideas.net/book/RLbook2020.pdf).
- **Mnih et al., Human-level control through deep reinforcement learning**:
  focus on experience replay and the periodically updated target network in
  the original DQN system. Read the
  [Nature paper](https://doi.org/10.1038/nature14236).
- **PyTorch DQN tutorial**: inspect the replay memory, target-network target,
  termination mask, and optimization step in a maintained implementation:
  [Reinforcement Learning (DQN) Tutorial](https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html).

Optional:

- **Schaul et al., Prioritized Experience Replay**: compare uniform replay with
  TD-error-weighted sampling and note the need for importance weights:
  [arXiv:1511.05952](https://arxiv.org/abs/1511.05952).
- **Lillicrap et al., Continuous Control with Deep Reinforcement Learning**:
  inspect soft target updates used in DDPG:
  [arXiv:1509.02971](https://arxiv.org/abs/1509.02971).

Reading target: be able to say what replay changes, what a delayed target
changes, and what neither mechanism guarantees.

## Concept

### Replay Changes Training Order

Environment interaction arrives chronologically:

```text
t=0 -> t=1 -> t=2 -> t=3 -> t=4
```

A replay buffer stores transitions and samples a training batch in a different
order:

```text
buffer:        [t=0, t=1, t=2, t=3, ..., t=200]
sampled batch: [t=91, t=4, t=173, t=38, ...]
```

This reduces local temporal adjacency and allows old transitions to be reused.
It does **not** prove that samples from an evolving finite buffer are
independent and identically distributed.

### A Delayed Network Slows Target Motion

```text
online network Q_theta    -> prediction Q_theta(s, a)
delayed network Q_target  -> next-state value for target y

every C optimizer steps:
Q_target <- Q_theta
```

The delayed network makes the regression target piecewise constant between
synchronizations. It reduces one source of feedback, but targets still change
when the delayed network is updated and when the replay distribution changes.

## Visual Artifact

Use the [Replay Buffer and Target Network Visualizer](../assets/animations/week4_replay_buffer.html)
to collect transitions, sample a minibatch, perform a real linear Bellman
update, and synchronize the target weights.

## Equation

Store enough information to separate task termination from a time limit:

$$
(s, a, r, s', \text{terminated}, \text{truncated})
$$

The Bellman target masks only true termination:

$$
y =
\begin{cases}
r, & \text{if terminated}, \\
r + \gamma \max_{a'} Q_{\text{target}}(s', a'),
& \text{otherwise}.
\end{cases}
$$

A truncation still ends the current rollout, but it does not necessarily mean
the underlying state has zero future value.

For a minibatch $B$, use the mean half-squared Bellman loss:

$$
\mathcal{L}(\theta)
=
\frac{1}{|B|}
\sum_{j \in B}
\frac{1}{2}
\left(y_j - Q_\theta(s_j, a_j)\right)^2.
$$

The target is treated as a constant during this optimizer step. Gradients
update the online parameters, not the delayed parameters.

## Algorithm: DQN with Replay and a Delayed Target

The full algorithm uses neural networks. This week's runnable checkpoints use
a linear approximator so every quantity remains inspectable.

```text
Initialize online network Q_theta
Initialize delayed network Q_target as a copy of Q_theta
Initialize replay buffer D with capacity N
Set optimizer-step counter u = 0

Observe initial state s

For each environment interaction:
    Choose action a with epsilon-greedy behavior from Q_theta
    Execute a
    Observe reward r, next state s', terminated, truncated
    Store (s, a, r, s', terminated, truncated) in D

    If D contains at least batch_size transitions:
        Sample a minibatch uniformly from D

        For each transition:
            If terminated:
                y = r
            Else:
                y = r + gamma * max_a' Q_target(s', a')

        prediction = Q_theta(s, a) for the sampled actions
        loss = mean(0.5 * (y - prediction)^2)
        Update only theta by gradient descent
        u = u + 1

        If u is a multiple of target_sync_updates:
            Q_target <- Q_theta

    If terminated or truncated:
        reset the environment
    Else:
        s <- s'
```

Replay is most straightforward with off-policy algorithms such as Q-learning,
because the target policy can differ from the policies that generated old
transitions. On-policy data can sometimes be reused with bounded staleness or
corrections, but ordinary on-policy updates should not silently train on
arbitrary old replay.

## Code Lens

Run:

```bash
python examples/week-04/01_replay_buffer.py
python examples/week-04/02_target_network_ablation.py
python examples/week-04/03_dqn_stabilizers.py
```

Checkpoint 1 compares all-pairs original-timeline spacing in two equal-size
sample sets:

```text
sample set               mean pair gap    adjacent-pair rate
sequential rollout               11.00                 6.2%
uniform replay batch             76.92                 0.6%
```

Checkpoint 2 measures actual target motion:

```text
Mean absolute change between consecutive targets:
  online target:  0.014529
  delayed target: 0.006766
```

Checkpoint 3 compares four configurations under the same interaction budget,
optimizer-step count, and fixed evaluation starts:

```text
variant              mean return    seed std    success rate   updates
online only               0.9850      0.0000         100.0%       393
target only               0.9850      0.0000         100.0%       393
replay only               0.9850      0.0000         100.0%       393
replay + target           0.9850      0.0000         100.0%       393
```

The replay variants process eight sampled transitions per optimizer step; the
non-replay variants process the newest transition once. The comparison is
matched for interactions and parameter-update count, not transition
evaluations or compute. That disclosed difference is the intended data-reuse
mechanism, but it prevents a claim about compute efficiency.

That table is a **null result**: all four methods solve this tiny problem.
LineWorld is useful for checking mechanics, but too easy to establish a
policy-level advantage from replay or delayed targets.

## Metric

Week 04 uses three levels of measurement:

- **All-pairs original-timeline gap**: checks whether an equal-size sample set
  spans a broader portion of the stored interaction timeline.
- **Mean absolute target change**: measures target motion directly.
- **Average return, success rate, and per-seed returns**: evaluate policies
  under one shared protocol.

Standard deviation across seeds is useful only beside the mean, per-seed
results, and a fixed evaluation protocol. A small standard deviation can mean
consistently good performance, consistently bad performance, or an evaluation
task that is too easy.

## Baseline

Under the same mixed-start evaluation protocol:

```text
policy                avg return    success rate
random                    0.6162           72.0%
always right              0.9850          100.0%
```

Every learned variant matches the heuristic. The evidence supports only this
claim:

> Under this 400-interaction, five-seed LineWorld protocol, all four linear-Q
> configurations learned the same right-moving policy.

It does not support a ranking among the four configurations.

## Failure Mode

Common mistakes:

- Calling replay samples i.i.d. instead of saying temporal adjacency is
  reduced.
- Sampling before enough transitions exist.
- Letting an unbounded buffer exhaust memory.
- Failing to copy initial online weights into the delayed network.
- Synchronizing every optimizer step and then assuming a meaningful delay
  remains.
- Using a very stale target and assuming slower movement is automatically
  better.
- Dropping bootstrap after truncation instead of only after true termination.
- Comparing variants with different interaction or optimizer-step budgets
  without reporting the difference.
- Calling a linear approximator a full DQN.
- Narrating a stabilizer advantage when all measured results are equal.

## Robotics Bridge

Replay is attractive in robotics because physical interactions are expensive
and stored transitions can support multiple updates. That reuse introduces new
questions:

- Does the buffer represent current sensors, controllers, and task conditions?
- Are rare successes and safety-critical failures sufficiently represented?
- Are simulated and real transitions mixed deliberately?
- Does stale data create distribution mismatch?
- Is the update-to-data ratio reported?

Prioritized replay can increase sampling of high-TD-error transitions, but high
TD error is not identical to importance, rarity, or safety. Sampling priorities
and correction weights must be inspected.

## Limitation Note

This week demonstrates replay sample spacing, target motion, and controlled
comparison design with a deterministic linear model. It does not demonstrate
neural DQN instability, Atari-scale learning, or transfer to robot control. A later
benchmark may reveal differences, but those differences must be measured
rather than assumed.

## Resources

- [Lab 04 - Replay Buffer and Target Network Ablation](../labs/lab-04.md):
  reproduce the three diagnostics and interpret the null result.
- [Week 04 examples](https://github.com/Isaac009/RL-VLA-WAM-Robot_learning-PhysicalAI/tree/main/examples/week-04):
  dependency-free runnable checkpoints.
- [PyTorch DQN tutorial](https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html):
  a maintained full neural implementation.
- [CleanRL DQN implementation](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/dqn.py):
  a compact single-file reference.

## Quiz

Complete the [Week 04 quiz](../quizzes/week-04.md) after the lab. It checks
replay mechanics, delayed targets, termination masking, and whether you can
interpret an inconclusive ablation without overclaiming.
