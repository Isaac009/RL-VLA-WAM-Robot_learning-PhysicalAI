# Week 04 Quiz - Replay and Target Networks

Use this after [Week 04](../lectures/week-04.md) and
[Lab 04](../labs/lab-04.md). The quiz checks mechanics and experimental
interpretation, not memorized slogans.

## Concepts

1. What two properties of online RL data make supervised-style optimization
   difficult?

2. What are the three components of the deadly triad?

3. What does uniform experience replay change about training order?

4. Why should replay samples not be called literally i.i.d.?

5. Why are old replay transitions straightforward to use with Q-learning but
   more delicate for an ordinary on-policy update?

6. What is the purpose of a delayed target network?

7. Does a delayed target network guarantee convergence? Explain.

## Arithmetic and Mechanics

Suppose a circular replay buffer has capacity four and currently contains:

```text
index 0: (s=0, a=right, r=-0.01, s'=1, terminated=False)
index 1: (s=1, a=right, r=-0.01, s'=2, terminated=False)
index 2: (s=2, a=right, r=-0.01, s'=3, terminated=False)
index 3: (s=3, a=right, r=+1.00, s'=4, terminated=True)
```

8. Which item is overwritten by the next insertion?

For the transition at index 1, use:

```text
gamma = 0.9
Q_online(1, right) = 0.10
Q_target(2, left) = 0.15
Q_target(2, right) = 0.40
```

9. What is the Bellman target?

10. What is the TD error?

11. What is the squared Bellman error?

12. What is the half-squared optimization loss?

13. For the terminal transition at index 3, what is the target?

14. If `theta_online=0.80`, `theta_target=0.40`, and `tau=0.10`,
    what is the soft-updated target parameter?

## Termination and Truncation

15. Which flag controls whether the future-value term is dropped?

16. Which condition ends the current rollout?

17. Why can treating every truncation as terminal bias a value estimate?

## Interpreting Evidence

18. In the Week 04 ablation, all four learned variants return `0.9850` with
    100% success. What can be concluded?

19. Why is zero seed standard deviation not enough to prove a method is stable
    in general?

20. Name two budgets or protocols that must be held fixed in a fair ablation.

21. If target synchronization happens after every optimizer step, what useful
    property of the delayed network is largely removed?

22. Can a small replay buffer always be called unstable? Why or why not?

??? success "Answer Key"
    1. Consecutive transitions are temporally correlated, and bootstrapped
       targets can move as value parameters change.

    2. Function approximation, bootstrapping, and off-policy learning.

    3. It samples stored transitions in a randomized order and reuses older
       experience, often spreading a minibatch across more of the stored
       timeline than a contiguous recent window.

    4. Samples come from a finite, changing buffer; sampling without
       replacement also introduces dependence within a batch.

    5. Q-learning targets a greedy policy independently of the behavior policy
       that collected a transition, assuming adequate coverage. Ordinary
       on-policy objectives depend on the current policy distribution, so
       stale data generally require limits or corrections.

    6. It supplies next-state values from parameters that remain fixed between
       synchronizations, slowing one source of target motion.

    7. No. It is a practical stabilizer, not a general convergence guarantee
       for nonlinear off-policy learning.

    8. The item at index 0, because the circular write pointer wraps around.

    9. `-0.01 + 0.9 * max(0.15, 0.40) = 0.35`.

    10. `0.35 - 0.10 = +0.25`.

    11. `0.25^2 = 0.0625`.

    12. `0.5 * 0.0625 = 0.03125`.

    13. `1.00`; true termination drops the future-value term.

    14. `0.10 * 0.80 + 0.90 * 0.40 = 0.44`.

    15. `terminated` controls the bootstrap mask.

    16. Either `terminated` or `truncated` ends the current rollout.

    17. A time limit may stop data collection even though the underlying state
        has future value. Forcing that value to zero changes the target.

    18. Under this exact LineWorld protocol, all four configurations learned
        the same useful policy. The experiment does not rank the stabilizers.

    19. Every method can be consistently good, consistently bad, or tested on
        a task that is too easy. The mean, per-seed outcomes, task, and budget
        are also required.

    20. Examples include environment interactions, optimizer steps,
        evaluation start states, evaluation episodes, exploration settings,
        and random seeds.

    21. The target parameters track the online parameters almost immediately,
        so there is little or no delayed-target interval.

    22. No. Capacity is a task-dependent tradeoff involving coverage,
        recency, memory, and sampling. It must be evaluated rather than
        declared unstable from one number.
