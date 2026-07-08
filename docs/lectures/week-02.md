# Week 02 - Tabular Q-Learning

## Why This Matters

Week 01 showed that a hand-written rule can solve LineWorld. Week 02 asks a
more useful question: can an agent discover that rule from interaction data?
Tabular Q-learning is the smallest place where rewards, future value,
exploration, and a measurable learned policy all meet.

## Learning Objectives

By the end of this week, learners should be able to:

- Explain what a Q-table stores.
- Read `Q[state][action]` as an action-value estimate.
- Compute one Q-learning update by hand.
- Explain the Bellman target and temporal-difference error.
- Distinguish terminal endings from time-limit truncations.

## Reading Materials

Required:

- **Sutton and Barto, Reinforcement Learning: An Introduction**, Chapter 6:
  focus on temporal-difference learning and Q-learning. Use the official book
  PDF: [http://incompleteideas.net/book/RLbook2020.pdf](http://incompleteideas.net/book/RLbook2020.pdf).
- **OpenAI Spinning Up, Key Concepts in RL**: read value functions, the optimal
  Q-function, and Bellman equations:
  [spinningup.openai.com/en/latest/spinningup/rl_intro.html](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html).
- **Hugging Face Deep RL Course, Unit 2**: read the introduction to Q-learning
  and the Q-learning example:
  [huggingface.co/learn/deep-rl-course/unit2/introduction](https://huggingface.co/learn/deep-rl-course/unit2/introduction).

Optional:

- **Gymnasium Basic Usage**: revisit `terminated` and `truncated`; this week
  uses that distinction in the update target:
  [gymnasium.farama.org/introduction/basic_usage](https://gymnasium.farama.org/introduction/basic_usage/).

Reading target: after reading, you should be able to say what `Q(s, a)` means
and why the update uses reward plus estimated future value.

## Concept

Week 01 used a hand-written rule:

```text
Always move right.
```

Week 02 asks a better question:

```text
Can the agent learn that "right" is useful from experience?
```

Tabular Q-learning stores one value for every state-action pair:

```text
Q[state][action] = expected future return
```

At the beginning, the table is empty knowledge:

```text
Q[0][left]  = 0.00
Q[0][right] = 0.00
```

The agent has no reason to prefer left or right yet.

### Simple Visual: Empty Table

```text
             action
state        left      right
-----        ----      -----
0            0.00      0.00
1            0.00      0.00
2            0.00      0.00
3            0.00      0.00
4            terminal state: no action chosen after goal
```

State 4 is still listed because the table has one row per state. It is not a
decision point after the episode terminates.

Think of each non-terminal cell as one question:

```text
"If I am in this state and take this action, how much return do I expect?"
```

## Equation

The update is:

```text
Q(s, a) <- Q(s, a) + alpha * (target - Q(s, a))

target = r + gamma * max_a' Q(s', a')
```

Where:

- `s` is the current state.
- `a` is the action taken.
- `r` is the reward received.
- `s'` is the next state.
- `alpha` is the learning rate.
- `gamma` discounts future value.
- `target - Q(s, a)` is the temporal-difference error.

If `s'` is terminal, the future term is dropped:

```text
target = r
```

There is no future after a true terminal state.

### Simple Visual: One Cell Moves

```text
before update
Q[3][right] = 0.00

target from transition
state 3 --right--> goal, reward +1.00
target = 1.00

after update with alpha = 0.5
Q[3][right] = 0.50
```

The table does not magically fill itself in. One transition moves one cell.

## Algorithm: Tabular Q-Learning

This is the algorithm for the tabular case, where the number of states and
actions is small enough to store a table.

```text
Create Q[state][action] and initialize every value to 0

For each episode:
    Reset the environment and observe the starting state s

    While the episode is not over:
        Choose an action a
            often epsilon-greedy:
                with probability epsilon: choose a random action
                otherwise: choose argmax_a Q[s][a]

        Take action a in the environment
        Observe reward r, next state s', terminated, truncated

        If terminated:
            target = r
        Else:
            target = r + gamma * max_a' Q[s'][a']

        td_error = target - Q[s][a]
        Q[s][a] = Q[s][a] + alpha * td_error

        Move to the next state:
            s = s'

        If terminated or truncated:
            stop this episode
```

Read it slowly. There are only four moving parts:

1. **A table** stores the agent's current guesses.
2. **A behavior rule** chooses actions, usually with exploration.
3. **A target** says what the current value should move toward.
4. **An update** nudges one table cell toward that target.

The algorithm does not update the whole table at once. Each transition updates
one entry:

```text
the entry for the state you were in and the action you took
```

That is why repeated experience matters. The value of the goal first appears
near the goal, then spreads backward through bootstrapping.

## Algorithm Walkthrough in LineWorld

Suppose the agent starts near the goal:

```text
state 3, action right -> state 4, reward +1.00, terminated=True
```

Because the next state is terminal:

```text
target = reward = 1.00
```

With `alpha = 0.5`, the update is:

```text
Q[3][right] <- 0.00 + 0.5 * (1.00 - 0.00)
             = 0.50
```

Now one step farther back:

```text
state 2, action right -> state 3, reward -0.01, terminated=False
```

This state is not terminal, so the update uses the best known future value:

```text
target = -0.01 + 0.9 * max Q[3]
       = -0.01 + 0.9 * 0.50
       = 0.44
```

Then:

```text
Q[2][right] <- 0.00 + 0.5 * (0.44 - 0.00)
             = 0.22
```

This is the first important "aha": even though the immediate reward was
negative, the value increased because the future looked good.

### Simple Visual: Value Spreads Backward

```text
start:          A   .   .   .   G
states:         0   1   2   3   4

after update 1:
Q[3][right] = 0.50       value touches the goal neighbor

after update 2:
Q[2][right] = 0.22       value starts moving backward

eventually:
Q[0][right], Q[1][right], Q[2][right], Q[3][right]
all learn that "right" points toward future reward
```

## Code Lens

Run:

```bash
python examples/week-02/01_q_table_intro.py
python examples/week-02/02_q_learning_update.py
python examples/week-02/03_train_q_learning.py
```

The Week 02 environment lives in `examples/week-02/env.py`. It is almost the
same as Week 01, but the ending is more precise:

- `terminated=True`: the agent reached the goal.
- `truncated=True`: the step limit stopped the rollout.

Q-learning should drop the future-value term only on `terminated=True`.

## Visual Artifact

Open the [Week 02 Q-table heatmap](../assets/animations/week2_q_table.html).
It shows value estimates spreading backward through the table as rightward
actions become useful.

## What the Three Checkpoints Teach

Checkpoint 1:

```text
python examples/week-02/01_q_table_intro.py
```

This prints an empty Q-table. No learning happens yet. The goal is to inspect
the object before trusting an algorithm to mutate it.

Checkpoint 2:

```text
python examples/week-02/02_q_learning_update.py
```

This performs two hand-checkable updates:

```text
Q[3][right] = 0.50
Q[2][right] = 0.22
```

The first update touches the goal reward directly. The second update never
sees the goal, but it still increases because it bootstraps from the value
already learned at state 3.

That backward spread of value is the little engine inside Q-learning.

Checkpoint 3:

```text
python examples/week-02/03_train_q_learning.py
```

This repeats the same update over 200 episodes using epsilon-greedy
exploration:

```text
with probability epsilon = 0.2: explore randomly
otherwise: choose the action with the highest current Q-value
```

After training, the learned Q-table prefers `right` in every non-terminal
state:

```text
state 0: left= 0.62  right= 0.70  best=right
state 1: left= 0.62  right= 0.79  best=right
state 2: left= 0.70  right= 0.89  best=right
state 3: left= 0.79  right= 1.00  best=right
state 4: terminal state (no action chosen after goal)
```

Then it evaluates three policies:

```text
policy          avg return  success rate
random                0.52          65%
always right          0.97         100%
q-learning            0.97         100%
```

## Metric

Week 02 keeps the Week 01 metrics so the comparison is disciplined:

- **Average return**: the mean total reward per episode.
- **Success rate**: the percentage of episodes that reach the goal.

Checkpoint 3 evaluates the greedy policy learned from the Q-table, not the
exploratory epsilon-greedy behavior used during training.

## Baseline

The random policy is the no-knowledge baseline. The always-right heuristic is
the hand-written ceiling for this fixed LineWorld. Q-learning is successful here
only if it can discover the same right-moving behavior from transitions.

This is the Week 02 result:

```text
Q-learning learned the same behavior as the hand-written heuristic.
```

Keep the claim narrow. It learned the useful policy in this tiny deterministic
LineWorld. That does not prove Q-learning is generally superior to simple
rules; it proves the table update plus exploration can discover this rule from
experience.

## Common Failure Modes

- Updating the wrong table cell.
- Forgetting to drop the future term at a terminal state.
- Dropping the future term at a timeout, which incorrectly treats truncation as
  death.
- Looking only at final policy behavior instead of inspecting the Q-values.
- Letting tie-breaking hide the fact that an untrained table knows nothing.
- Evaluating only the training episodes, where exploration noise is still
  present, instead of evaluating the learned greedy policy.

## Robotics Bridge

Most robot tasks cannot use a small table because states and actions are too
large or continuous. But the idea survives:

```text
learn which actions are valuable in which situations
```

DQN later replaces the table with a neural network. Actor-critic methods later
replace or augment action-value tables with learned value functions. The table
is small, but the habit is foundational: inspect the value estimate, not just
the reward curve.

## Resources

- [Lab 02 - Inspect a Q-Table](../labs/lab-02.md): the hand-calculation and
  checkpoint workflow.
- [Week 02 examples](https://github.com/Isaac009/RL-VLA-WAM-Robot_learning-PhysicalAI/tree/main/examples/week-02): runnable Q-table
  checkpoints and expected output.
- [Week 02 Q-table heatmap](../assets/animations/week2_q_table.html): visual
  intuition for value spreading backward.

## Quiz

After the lab, complete the [Week 02 quiz](../quizzes/week-02.md). It checks
whether you can read a Q-table and compute a Bellman update by hand.
