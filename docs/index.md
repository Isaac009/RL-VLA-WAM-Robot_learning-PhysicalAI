# RL-VLA-WAM Robot Learning Course

A community course for learning robot reinforcement learning from first
principles, then extending toward vision-language-action policies and World
Action Models.

The course is built around a simple rule: **every concept should become a
runnable artifact, a baseline, and a measurable comparison.**

## Your First Hour

1. Clone the repository and run the first tiny environment:

    ```bash
    python examples/week-01/01_random_policy.py
    ```

    You will see a full reinforcement-learning loop — state, action, reward,
    termination — printed line by line, with no frameworks in the way.

2. Skim the [syllabus](syllabus.md) to see where the ten weeks lead.

3. Start [Week 01](lectures/week-01.md): read the lecture, do
   [Lab 01](labs/lab-01.md), then check yourself with the
   [quiz](quizzes/week-01.md).

Each week in the **Weeks** menu follows that same rhythm: lecture, lab, quiz,
with runnable checkpoints in the repository's `examples/` folder.

## What Makes This Course Different

- It begins with classical RL instead of jumping directly to large models.
- It treats environment design as a first-class research skill.
- It keeps random, heuristic, and classical baselines visible.
- It connects robot learning to VLA and WAM research without overclaiming.
- It is designed so community members can add labs, notes, and readings.

## How the Course Is Taught

Every lesson keeps the same rhythm: concept, math core, code lens, baseline,
metric, debugging checklist, robotics bridge, and limitation note. Good course
material helps learners *reproduce* an idea, not merely admire it — see the
[lesson plan](lesson-plan.md) for the full design rules and the
[instructor commitment](instructor-rl.md) for how lectures are held to them.

## Contributing

New labs, notes, and curated resources are welcome. Contributions should
include the learning goal, runnable code or a concrete exercise, expected
output, and a short note on limitations — the details are in the
[contribution guide](contribute.md).
