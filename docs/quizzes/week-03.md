# Week 03 Quiz - Bellman Error and DQN

Use this after [Week 03](../lectures/week-03.md) and
[Lab 03](../labs/lab-03.md). You should be able to answer most questions by
reading the checkpoint scripts and doing the arithmetic on paper.

## Concepts

1. Why does a Q-table stop being practical for large or continuous state
   spaces?

2. What does `Q_theta(state, action)` mean?

3. What is the role of `Q_target` in the Bellman target?

4. What is the difference between Bellman error and policy return?

5. Why is the Week 03 linear approximator not full DQN?

## Target and Loss Arithmetic

Use:

```text
gamma = 0.9
prediction = Q_theta(2, right) = 0.10
Q_target(3, left) = 0.20
Q_target(3, right) = 0.50
reward = -0.01
terminated = False
```

6. What is `max_a' Q_target(3, a')`?

7. What is the Bellman target?

8. What is the TD error?

9. What is the squared Bellman error?

Now use a terminal transition:

```text
prediction = Q_theta(3, right) = 0.50
reward = 1.00
terminated = True
```

10. What is the target?

11. What is the TD error?

12. What is the squared Bellman error?

## Interpretation

13. Why can a lower Bellman loss fail to produce a better policy?

14. Why does DQN use replay instead of training only on the most recent
    transition?

15. Why does DQN periodically copy the online network into a target network?

16. In checkpoint 2, why are only the right-action parameters updated?

17. In checkpoint 3, the linear-q policy matches the always-right heuristic in
    LineWorld. What exactly can we claim, and what should we not claim?

??? success "Answer Key"
    1. A table needs one entry for every state-action pair. Large, continuous,
       image-based, or robot-state spaces would require too many entries and
       would not generalize across similar states.

    2. It is the value predicted by a parameterized model with parameters
       `theta` for a particular state-action pair.

    3. `Q_target` supplies a delayed estimate of next-state value for the
       target. It keeps the target more stable than using the online network
       for everything at every update.

    4. Bellman error is a local training signal for value prediction. Policy
       return is the reward collected when acting in the environment.

    5. It has no neural network, no replay buffer, and only a tiny linear model.
       It teaches the Bellman-error mechanics, not the full DQN system.

    6. `max(0.20, 0.50) = 0.50`.

    7. `-0.01 + 0.9 * 0.50 = 0.44`.

    8. `0.44 - 0.10 = 0.34`.

    9. `0.34^2 = 0.1156`.

    10. The target is `1.00`, because terminal transitions drop the future
        value term.

    11. `1.00 - 0.50 = 0.50`.

    12. `0.50^2 = 0.2500`.

    13. The loss can be reduced on biased data, poor targets, or transitions
        that do not represent the states the policy must handle. The policy
        still needs environment evaluation.

    14. Replay samples older transitions so updates are less dominated by the
        newest correlated experience.

    15. The target network slows down one source of target motion. This often
        improves empirical stability, but does not guarantee convergence.

    16. The transition only observed the value prediction for taking `right` in
        that state. The update moves the parameters responsible for that
        predicted value.

    17. We can claim that a tiny Bellman-error-trained Q approximator learned
        the useful right-moving policy in this deterministic LineWorld under
        the given settings. We should not claim that this is a full DQN
        benchmark, that it solves deep RL, or that it transfers to robot tasks.
