# Week 01 Quiz - MDPs and Baselines

Use this as a self-check after completing [Week 01](../lectures/week-01.md)
and [Lab 01](../labs/lab-01.md). The point is not memorization; it is to make
sure you can inspect an RL loop and explain what happened.

## Concepts

1. In LineWorld, what is the state?

2. In LineWorld, what is the action space?

3. What is the difference between a reward and a return?

4. Why is a random policy useful even though it is not intelligent?

5. Why is the "always right" policy not a learning method?

## Rollout Reading

Consider this partial rollout:

```text
state=0  world=A . . . G
action=right  state=1  reward=-0.01  done=False
action=right  state=2  reward=-0.01  done=False
action=right  state=3  reward=-0.01  done=False
action=right  state=4  reward= 1.00  done=True
```

6. Did the agent reach the goal or time out?

7. What is the episode return?

8. How many actions did the agent take?

## Measurement

Suppose two policies produce this result over 100 episodes:

```text
policy          avg return  success rate
random                0.52          65%
always right          0.97         100%
```

9. Which policy is better in this environment?

10. Why can average return be more informative than success rate alone?

11. Why should we be careful before claiming that "always right" is generally
    good?

## Short Coding Check

12. In the environment loop, what three things must happen repeatedly until
    `done=True`?

13. If you changed the non-goal reward from `-0.01` to `0.00`, what behavior
    would the reward function stop encouraging?

??? success "Answer Key"
    1. The state is the agent's integer position on the line.

    2. The action space is two discrete actions: `left` and `right`.

    3. A reward is feedback from one step. A return is the accumulated reward
       over an episode.

    4. A random policy gives a baseline: what performance looks like before
       adding skill, heuristics, or learning.

    5. It encodes prior knowledge that the goal is on the right. It does not
       discover that behavior from experience.

    6. It reached the goal.

    7. `-0.01 - 0.01 - 0.01 + 1.00 = 0.97`.

    8. Four actions.

    9. "Always right" is better in this specific LineWorld.

    10. Success rate only says whether the goal was reached. Average return
        also captures path efficiency because every wasted step has a penalty.

    11. It depends on this environment's layout. If the goal could be elsewhere
        or obstacles existed, always moving right could fail.

    12. Choose an action, call the environment step, and update the current
        state/return from the result.

    13. It would stop encouraging shorter paths. A slow path and a direct path
        could receive the same terminal reward if both reach the goal.
