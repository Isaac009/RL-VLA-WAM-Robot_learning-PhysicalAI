# RL-VLA-WAM Robot Learning Course

A community course that starts with classical reinforcement learning and
builds, step by step, toward robot learning, vision-language-action policies,
and World Action Models. Every step produces a runnable artifact and a
measurable comparison against a baseline.

**Course site:** https://isaac009.github.io/RL-VLA-WAM-Robot_learning-PhysicalAI/

## Start Here

The first learning artifact is a dependency-free mini-course starter
(requires Python 3.10+):

```bash
python getting_started.py
```

This runs a tiny 1D environment so the core reinforcement learning loop is
visible before adding Gymnasium, PyTorch, robot simulators, VLA models, or
World Action Models.

Then read:

- [Syllabus](docs/syllabus.md) — the 10-week plan and learning outcomes.
- [Week 01 - MDPs and Baselines](docs/lectures/week-01.md)
- [Lab 01 - Inspect a Tiny MDP](docs/labs/lab-01.md)
- [`rl_mini_course.md`](rl_mini_course.md) — the short contributor roadmap.

## Approach

The course begins with well-specified MDPs, value functions, policy gradients,
and off-policy algorithms, using standard baselines (DQN, SAC, PPO, TD3) and
clear training recipes so results are reproducible and comparable. From that
foundation it progressively introduces multimodal conditioning, hierarchical
structure, and model-based components, so each added capability can be ablated
and measured against the classical baseline.

## Working on the Docs

The site in [`docs/`](docs/) is built with MkDocs Material and deployed by
[`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml).

```bash
python -m pip install -r requirements-docs.txt
python -m mkdocs serve            # local preview
python -m mkdocs build --strict   # CI-equivalent build
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution standards.

## License

Released under the [MIT License](LICENSE).
