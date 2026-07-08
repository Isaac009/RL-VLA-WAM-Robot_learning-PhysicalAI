# Week 02 Quiz - Tabular Q-Learning

Use this after [Week 02](../lectures/week-02.md) and
[Lab 02](../labs/lab-02.md). You should be able to answer most questions by
reading the two checkpoint scripts and doing the arithmetic on paper.

## Concepts

1. What does `Q[state][action]` store?

2. Why does an empty Q-table usually start with all zeros?

3. In LineWorld, why should `Q[3][right]` eventually become large?

4. What is the temporal-difference error?

5. What is the difference between `terminated` and `truncated`?

## Update Arithmetic

Use:

```text
alpha = 0.5
gamma = 0.9
Q(s, a) <- Q(s, a) + alpha * (target - Q(s, a))
```

6. If the agent moves from state 3 to the goal with reward `+1.00`, and the
   next state is terminal, what is the target?

7. If `Q[3][right]` starts at `0.00`, what is its value after one update using
   the target from question 6?

8. Now suppose the agent moves from state 2 to state 3 with reward `-0.01`,
   and `max Q[3] = 0.50`. What is the target?

9. If `Q[2][right]` starts at `0.00`, what is its value after one update using
   the target from question 8?

## Interpretation

10. Why can a state-action value increase even when the immediate reward is
    negative?

11. Why should the future-value term be dropped after true termination?

12. Why should the future-value term usually not be dropped after a time-limit
    truncation?

13. Why is checkpoint 2 not enough to claim that we have trained an agent?

14. In checkpoint 3, why do we use epsilon-greedy behavior during training?

15. Why do we evaluate the greedy policy after training instead of evaluating
    the exploratory training behavior directly?

16. The trained Q-learning policy matches the always-right heuristic in
    LineWorld. What exactly can we claim, and what should we not claim?

17. Why does the printed Q-table still include a row for the terminal goal
    state if no action is chosen there?

??? success "Answer Key"
    1. It stores an estimate of the return expected after taking an action in
       a state and then acting well afterwards.

    2. Zero is a neutral initial guess. At the start, the agent has not yet
       learned evidence that one action is better than another.

    3. From state 3, moving right reaches the goal immediately and receives
       `+1.00`.

    4. The temporal-difference error is `target - Q(s, a)`: the gap between the
       bootstrapped target and the current estimate.

    5. `terminated` means the task truly ended, such as reaching the goal.
       `truncated` means the episode was stopped by a limit, such as max steps.

    6. The target is `1.00`.

    7. `0.00 + 0.5 * (1.00 - 0.00) = 0.50`.

    8. `-0.01 + 0.9 * 0.50 = 0.44`.

    9. `0.00 + 0.5 * (0.44 - 0.00) = 0.22`.

    10. Because the future can be valuable enough to outweigh the immediate
        penalty.

    11. A terminal state has no future continuation to bootstrap from.

    12. A truncation is an artificial stop. The underlying world may have
        continued, so treating it as terminal can bias the value estimate.

    13. The transitions were hand-picked. Training requires exploration,
        repeated updates, and evaluation against baselines.

    14. Epsilon-greedy behavior lets the agent sometimes try actions that do
        not currently look best, so it can collect experience and avoid being
        trapped by early guesses.

    15. During training, exploration intentionally injects random actions.
        Evaluation asks what the learned table recommends after training, so
        the greedy policy is the cleaner measurement.

    16. We can claim that tabular Q-learning learned the optimal right-moving
        behavior in this tiny deterministic LineWorld under the given settings.
        We should not claim that Q-learning is generally better than
        hand-written rules or that it will scale directly to complex robot
        tasks.

    17. The table has one row per state, so the terminal state is part of the
        table shape. It is marked terminal because the policy should not choose
        another action after the goal ends the episode.
