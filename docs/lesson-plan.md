# Lesson Plan

This plan organizes the course into disciplined, artifact-driven lessons. Each
week is dense enough to be useful but small enough to complete.

## Lesson Design Rules

- One major idea per lesson.
- One runnable artifact per lesson.
- One baseline per lab.
- One visual artifact per lesson.
- Simple inline visuals near the concept they explain.
- One reading list per lecture.
- One quiz per lecture.
- One explicit algorithm block per algorithm lecture.
- One limitation note per result.
- No algorithm without an environment.
- No robot-learning claim without a metric.

## Ten-Week Core Track

| Week | Theme | Core question | Build artifact | Visual artifact |
| --- | --- | --- | --- | --- |
| 1 | MDPs and baselines | What exactly is the agent interacting with? | Tiny 1D environment and random rollout | [MDP loop diagram](assets/images/week1_mdp_loop.svg) |
| 2 | Tabular Q-learning | How can experience become a table of action values? | Q-table learner for LineWorld | [Q-table heatmap](assets/animations/week2_q_table.html) |
| 3 | Bellman error and DQN | How do we replace a table with a neural network? | PyTorch DQN on a simple control task | [Bellman target animation](assets/animations/week3_bellman_target.html) |
| 4 | Replay and target networks | Why does naive deep RL become unstable? | Replay buffer and target network ablation | [Replay buffer placeholder](assets/animations/week4_replay_buffer.html) |
| 5 | Policy gradients | How can a policy improve actions directly? | REINFORCE or actor-only baseline | [Policy gradient placeholder](assets/animations/week5_policy_gradient.html) |
| 6 | Actor-critic and advantage | How do we reduce policy-gradient noise? | Simple actor-critic agent | [Actor/critic placeholder](assets/images/week6_actor_critic.svg) |
| 7 | PPO and SAC | What do practical continuous-control agents optimize? | PPO or SAC baseline with logs | [PPO clipping placeholder](assets/images/week7_ppo_clip.svg) |
| 8 | Robot simulation | How does RL change when actions move a robot? | Reaching or manipulation environment | [Robot reaching placeholder](assets/images/week8_robot_mdp.svg) |
| 9 | Imitation learning and VLAs | What changes when actions are learned from demonstrations? | Dataset inspection and behavior cloning | [VLA flow placeholder](assets/images/week9_vla_flow.svg) |
| 10 | WAMs and final project | Can world prediction improve action selection? | Final project with baseline and limitation note | [WAM storyboard placeholder](assets/images/week10_wam_storyboard.svg) |

## Weekly Page Template

Each lecture page should contain:

- **Why this matters**: one paragraph.
- **Learning objectives**: three to five bullets.
- **Reading materials**: required and optional sources with a reason for each.
- **Concept**: intuition.
- **Math core**: minimal formalism.
- **Algorithm**: pseudocode written in the lecture, not only linked externally.
- **Simple visuals**: compact diagrams, tables, or flow sketches placed near
  the explanation.
- **Code lens**: where the math appears in code.
- **Common failure modes**: debugging guidance.
- **Robotics bridge**: how the idea appears in robot learning.
- **Resources**: two to four curated links.
- **Quiz link**: a self-check page with answer key.

Each lab page should contain:

- Goal.
- Setup.
- Tasks.
- Expected output.
- Baseline.
- Metric.
- Reflection questions.
- Extension challenge.
- Limitation note.

## Discipline Markers

Every lesson should visibly mark:

- **Concept**: the new idea.
- **Equation**: the formal object.
- **Code**: the implementation pattern.
- **Metric**: the measurement.
- **Baseline**: the comparison.
- **Failure mode**: the most likely thing to break.

These markers make the course easier to scan without watering down the
technical content.

## Fun Without Losing Rigor

Use small challenges:

- "Beat the random agent."
- "Make the Q-table explain itself."
- "Find the reward bug."
- "Freeze the target network and watch training calm down."
- "Design a robot reward that does not cheat."

The fun should come from seeing ideas become working systems.

## Lesson Readiness Checklist

A lesson is ready to publish when:

- The code runs from a clean checkout.
- The expected output is documented.
- The baseline is clear.
- The visual artifact has a generation brief.
- The lecture includes at least one simple inline visual when it helps explain
  the concept.
- The lecture has required readings.
- Any algorithm introduced in the lecture is written down and explained there.
- The quiz has an answer key.
- The limitation note is honest.
- The lesson fits into the course arc.
