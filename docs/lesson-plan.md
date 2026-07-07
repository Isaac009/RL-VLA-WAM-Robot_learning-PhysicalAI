# Lesson Plan

This plan organizes the course into disciplined, artifact-driven lessons. Each
week is dense enough to be useful but small enough to complete.

## Lesson Design Rules

- One major idea per lesson.
- One runnable artifact per lesson.
- One baseline per lab.
- One visual artifact per lesson.
- One limitation note per result.
- No algorithm without an environment.
- No robot-learning claim without a metric.

## Ten-Week Core Track

| Week | Theme | Core question | Build artifact | Visual artifact |
| --- | --- | --- | --- | --- |
| 1 | MDPs and baselines | What exactly is the agent interacting with? | Tiny 1D environment and random rollout | MDP loop diagram |
| 2 | Tabular Q-learning | How can experience become a table of action values? | Q-table learner for LineWorld | Q-table heatmap over training |
| 3 | Bellman error and DQN | How do we replace a table with a neural network? | PyTorch DQN on a simple control task | Bellman target animation |
| 4 | Replay and target networks | Why does naive deep RL become unstable? | Replay buffer and target network ablation | Replay buffer sampling animation |
| 5 | Policy gradients | How can a policy improve actions directly? | REINFORCE or actor-only baseline | Probability-shift animation |
| 6 | Actor-critic and advantage | How do we reduce policy-gradient noise? | Simple actor-critic agent | Actor/critic two-panel diagram |
| 7 | PPO and SAC | What do practical continuous-control agents optimize? | PPO or SAC baseline with logs | PPO clipping graph |
| 8 | Robot simulation | How does RL change when actions move a robot? | Reaching or manipulation environment | Robot reaching state/action diagram |
| 9 | Imitation learning and VLAs | What changes when actions are learned from demonstrations? | Dataset inspection and behavior cloning | Observation-language-action flow |
| 10 | WAMs and final project | Can world prediction improve action selection? | Final project with baseline and limitation note | WAM rollout/imagination storyboard |

## Weekly Page Template

Each lecture page should contain:

- **Why this matters**: one paragraph.
- **Learning objectives**: three to five bullets.
- **Concept**: intuition.
- **Math core**: minimal formalism.
- **Code lens**: where the math appears in code.
- **Common failure modes**: debugging guidance.
- **Robotics bridge**: how the idea appears in robot learning.
- **Resources**: two to four curated links.

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
- The limitation note is honest.
- The lesson fits into the course arc.
