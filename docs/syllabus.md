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

| Week | Topic | Main artifact | Status |
| --- | --- | --- | --- |
| 1 | MDPs, rollouts, random baselines | Tiny dependency-free environment | Released |
| 2 | Tabular Q-learning | Q-table learner and baseline comparison | Released |
| 3 | Bellman error and DQN mechanics | Linear Q approximator and Bellman-loss training | Released |
| 4 | Replay and target networks | Controlled replay and delayed-target diagnostics | Released |
| 5 | Policy gradients | REINFORCE or actor-only baseline | Planned |
| 6 | Actor-critic and advantage | Simple actor-critic agent | Planned |
| 7 | PPO and SAC in practice | PPO or SAC baseline with logs | Planned |
| 8 | Robot simulation | Reaching or manipulation benchmark | Planned |
| 9 | Imitation learning and VLAs | Dataset inspection and behavior cloning | Planned |
| 10 | WAMs and final project | Final project with baseline and limitation note | Planned |

## Lesson Format

Each week follows a consistent teaching pattern:

- Hook: a concrete puzzle, failure case, or robot-learning question.
- Reading materials: required and optional sources.
- Concept: the idea in plain language.
- Math core: the minimal equation or objective.
- Code lens: the exact implementation pattern.
- Lab: runnable code with expected output.
- Baseline: random, heuristic, or previous method.
- Metric: what is measured and why.
- Failure mode: the most likely thing to debug.
- Robotics bridge: how the idea appears in robot learning.
- Quiz: self-check questions with an answer key.
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
