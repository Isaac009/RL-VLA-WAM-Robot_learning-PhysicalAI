# RL-VLA-WAM-Robot_learning-PhysicalAI
A modular codebase that begins with classical RL foundations and extends through perception, vision‑language grounding, and a learned World Action Model to enable robust, goal‑conditioned robot behavior and sim‑to‑real transfer.

## Overview starting with Classical Reinforcement Learning
Begin with Classical RL: well‑specified MDPs, value functions, policy gradients, and off‑policy algorithms form the backbone for stable learning. Use standard baselines (DQN, SAC, PPO, TD3) and clear training recipes so results are reproducible and comparable. From this foundation, progressively introduce multimodal conditioning, hierarchical structure, and model‑based components so that each added capability can be ablated and measured against the classical baseline.

## Start Here

The first learning artifact is a dependency-free mini-course starter:

```bash
python getting_started.py
```

This runs a tiny 1D environment so the core reinforcement learning loop is
visible before adding Gymnasium, PyTorch, robot simulators, VLA models, or
World Action Models.

See [`rl_mini_course.md`](rl_mini_course.md) for the step-by-step course plan.
