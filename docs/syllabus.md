# Syllabus

## Audience

This course is for students, researchers, and builders who want a practical path
from reinforcement learning fundamentals to robot learning and Physical AI.

The ideal learner has basic Python knowledge and enough linear algebra,
probability, and machine learning background to read loss functions and training
loops. Advanced robotics experience is helpful but not required at the start.

## Learning Outcomes

By the end of the course, learners should be able to:

- Formulate a task as an MDP.
- Build and evaluate random, heuristic, and learned baselines.
- Implement tabular Q-learning from scratch.
- Explain the purpose of replay buffers, target networks, and Bellman error.
- Train and evaluate policy-gradient and actor-critic agents.
- Design robot-learning experiments with clear metrics and failure analysis.
- Read VLA and WAM papers with a grounded understanding of what the policy,
  data, action representation, and evaluation protocol are doing.
- Add a new course resource or lab in a reproducible format.

## Weekly Plan

| Week | Topic | Main artifact |
| --- | --- | --- |
| 1 | MDPs, rollouts, random baselines | Tiny dependency-free environment |
| 2 | Tabular Q-learning | Q-table learner and baseline comparison |
| 3 | Deep Q-learning | PyTorch DQN on a simple control task |
| 4 | Policy gradients and actor-critic | Continuous-control actor-critic agent |
| 5 | PPO and SAC in practice | CleanRL or Stable-Baselines3 experiment |
| 6 | Robot simulation | Reaching or manipulation benchmark |
| 7 | Imitation learning and datasets | Dataset inspection and behavior cloning |
| 8 | VLA policies | Action representation and fine-tuning notes |
| 9 | World Action Models | World-model supervision and control interface |
| 10 | Final project | Reproducible robot-learning mini-project |

## Lesson Format

Each week follows a consistent teaching pattern:

- Hook: a concrete puzzle, failure case, or robot-learning question.
- Concept: the idea in plain language.
- Math core: the minimal equation or objective.
- Code lens: the exact implementation pattern.
- Lab: runnable code with expected output.
- Baseline: random, heuristic, or previous method.
- Metric: what is measured and why.
- Failure mode: the most likely thing to debug.
- Robotics bridge: how the idea appears in robot learning.
- Limitation note: what the result does not prove.

See [Lesson Plan](lesson-plan.md) for the full instructor plan.

## Evaluation Philosophy

The course uses comparison rather than isolated demos.

Every meaningful lab should include:

- A random or heuristic baseline.
- A learned method.
- A metric that matches the task.
- Multiple seeds when training instability matters.
- A short failure analysis.
- A clear statement of what the result does and does not show.

## Final Project

Choose one robot-learning or control problem and produce:

- MDP definition.
- Baseline policy.
- Learned policy.
- Training or evaluation curves.
- Rollout examples.
- Failure cases.
- Short reproducibility notes.

The final project should avoid broad claims. A good claim looks like:

> In this specific simulated reaching task, under this reward and seed budget,
> PPO improved success rate over the random baseline.
