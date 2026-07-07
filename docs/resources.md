# Resources

This page is curated for usefulness, not completeness. A resource should help a
learner understand, reproduce, or evaluate robot learning systems.

Links were reviewed when this page was created in July 2026.

## Foundations

| Resource | Why it is here |
| --- | --- |
| [Sutton and Barto, Reinforcement Learning: An Introduction](https://incompleteideas.net/book/the-book-2nd.html) | The standard foundation for MDPs, dynamic programming, temporal-difference learning, and policy gradients. |
| [David Silver's RL Course](https://www.davidsilver.uk/teaching/) | Clear lecture-style explanations of classical RL concepts. |
| [OpenAI Spinning Up](https://spinningup.openai.com/en/latest/) | Practical explanations of deep RL algorithms and implementation choices. |
| [Hugging Face Deep RL Course](https://huggingface.co/learn/deep-rl-course/unit0/introduction) | Free hands-on course with approachable notebooks and community exercises. |

## Core RL Tooling

| Resource | Why it is here |
| --- | --- |
| [Gymnasium](https://gymnasium.farama.org/) | Maintained standard API for RL environments, including custom environment guidance. |
| [CleanRL](https://docs.cleanrl.dev/) | Single-file implementations that make algorithm details easier to inspect. |
| [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/) | Reliable PyTorch implementations for applied baselines and experiments. |
| [PettingZoo](https://pettingzoo.farama.org/) | Standard interface for multi-agent RL environments. |

## Robot Simulation and Benchmarks

| Resource | Why it is here |
| --- | --- |
| [Gymnasium-Robotics](https://robotics.farama.org/) | Robotics environments with goal-conditioned tasks and a familiar Gymnasium style. |
| [MuJoCo](https://mujoco.readthedocs.io/en/stable/overview.html) | Physics engine widely used in robot learning, control, and simulation research. |
| [robosuite](https://robosuite.ai/docs/overview.html) | Manipulation-focused simulation framework with benchmark tasks and robot controllers. |
| [ManiSkill](https://maniskill.readthedocs.io/en/latest/) | Robot simulation and training framework with manipulation tasks, GPU simulation, and VLA/IL baselines. |
| [Meta-World](https://metaworld.farama.org/) | Benchmark for multi-task and meta-RL manipulation with many distinct tasks. |
| [LIBERO](https://libero-project.github.io/main.html) | Benchmark suite often used for language-conditioned robot manipulation and VLA evaluation. |

## Robot Data, Imitation Learning, and VLAs

| Resource | Why it is here |
| --- | --- |
| [LeRobot](https://huggingface.co/docs/lerobot/index) | Open tooling for real-world robotics datasets, policies, and robot deployment workflows. |
| [Open X-Embodiment / RT-X](https://robotics-transformer-x.github.io/) | Large cross-embodiment robot learning dataset and model reference point. |
| [OpenVLA](https://openvla.github.io/) | Open-source VLA model with code, checkpoints, and fine-tuning materials. |
| [Octo](https://octo-models.github.io/) | Open generalist robot policy designed for flexible observations, actions, and fine-tuning. |
| [Diffusion Policy](https://diffusion-policy.cs.columbia.edu/) | Important imitation-learning baseline for visuomotor control. |
| [pi0](https://www.pi.website/blog/pi0) | Generalist robot policy work useful for understanding continuous VLA action generation. |

## World Action Models

| Resource | Why it is here |
| --- | --- |
| [Fast-WAM](https://yuantianyuan01.github.io/FastWAM/) | Clear WAM framing around whether future imagination is needed at inference or mainly useful as training supervision. |

## How to Add a Resource

Open a pull request that adds one row and answers:

- What problem does this resource help a learner solve?
- What level is it for: beginner, intermediate, or advanced?
- Is it theory, code, dataset, benchmark, or paper?
- Does it require paid tools, special hardware, or large compute?
- What should learners be careful not to overclaim after using it?
