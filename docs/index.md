# RL-VLA-WAM Robot Learning Course

This is a community-oriented course for learning robot reinforcement learning
from first principles, then extending toward vision-language-action policies
and World Action Models.

The course is built around a simple rule: every concept should eventually become
a runnable artifact, a baseline, and a measurable comparison.

## Start Here

Run the first tiny environment:

```bash
python examples/week-01/01_random_policy.py
```

(`python getting_started.py` at the repository root is a shortcut for the
same script.)

Then read:

- [Syllabus](syllabus.md)
- [RL Instructor Commitment](instructor-rl.md)
- [Lesson Plan](lesson-plan.md)
- [Week 01 - MDPs and Baselines](lectures/week-01.md)
- [Lab 01 - Inspect a Tiny MDP](labs/lab-01.md)
- [Week 01 Quiz](quizzes/week-01.md)
- [Artifact Generator Brief](artifact-generator-brief.md)
- [Resources](resources.md)

## What Makes This Course Different

- It begins with classical RL instead of jumping directly to large models.
- It treats environment design as a first-class research skill.
- It keeps random, heuristic, and classical baselines visible.
- It connects robot learning to VLA and WAM research without overclaiming.
- It is designed so community members can add labs, notes, and readings.

## Course Arc

1. MDPs, rollouts, rewards, and baselines.
2. Tabular Q-learning and Bellman updates.
3. Deep Q-learning and replay buffers.
4. Policy gradients, PPO, SAC, and continuous control.
5. Robot simulation, manipulation benchmarks, and sim-to-real caveats.
6. Imitation learning and offline robot datasets.
7. Vision-language-action models.
8. World Action Models and model-based robot control.

## Community Standard

Good course material should help learners reproduce an idea, not merely admire
it. Contributions should include the learning goal, runnable code or a concrete
exercise, expected output, and a short note on limitations.

## Teaching Standard

The RL track is taught with a consistent rhythm: concept, math core, code lens,
baseline, metric, debugging checklist, robotics bridge, and limitation note.
That rhythm keeps the course disciplined while leaving room for playful visual
explainers and small challenges.
