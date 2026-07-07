# Artifact Generator Brief

This page gives instructions for assistants that generate diagrams, images,
slides, animations, or visual assets for the course.

The goal is not decoration. Every artifact should help a learner understand,
debug, or remember an RL concept.

## Visual Style

- Clean educational diagrams.
- High contrast.
- Minimal clutter.
- Short labels.
- Consistent color meaning across the course.
- Prefer simple geometric layouts over busy scenes.
- Use playful touches only when they clarify the idea.

## Color Semantics

Use colors consistently:

- State: blue.
- Action: orange.
- Reward: green.
- Value estimate: purple.
- Error or instability: red.
- Baseline: gray.
- Learned policy: teal.

## Accessibility Rules

- Do not rely on color alone.
- Use text labels or patterns in addition to color.
- Keep text large enough for slides and mobile reading.
- Avoid thin lines and low-contrast annotations.
- Provide alt text for every static image.

## Output Formats

Preferred formats:

- Static diagrams: SVG or PNG.
- Animated explainers: GIF, MP4, or web-friendly HTML animation.
- Code-native animations: Manim, matplotlib animation, or lightweight HTML/CSS.

Store generated artifacts under:

```text
docs/assets/
```

Suggested subfolders:

```text
docs/assets/images/
docs/assets/animations/
docs/assets/storyboards/
```

## Standard Artifact Spec

Every artifact request should include:

```text
Title:
Lesson:
Concept:
Learner takeaway:
Format:
Canvas or aspect ratio:
Required elements:
Motion, if animated:
Labels:
Color semantics:
Alt text:
Do not include:
```

## Week-by-Week Artifact Queue

### Week 1: MDP Loop

Create a loop diagram with four nodes:

```text
State -> Agent -> Action -> Environment -> Reward + Next State
```

Learner takeaway: RL is an interaction loop, not a standalone predictor.

### Week 2: Q-Table Heatmap

Show a small table with states as rows and actions as columns. Animate values
changing after episodes.

Learner takeaway: Q-learning turns experience into action-value estimates.

### Week 3: Bellman Target

Show the target:

```text
r + gamma * max_a Q_target(s', a)
```

as pieces flowing into a loss calculation.

Learner takeaway: DQN trains by matching a prediction to a bootstrapped target.

### Week 4: Replay Buffer

Animate transitions entering a buffer and random batches being sampled.

Learner takeaway: replay reduces correlation and reuses experience.

### Week 5: Policy Gradient

Show an action distribution before and after a high-reward action.

Learner takeaway: policy gradients increase the probability of useful actions.

### Week 6: Actor-Critic

Create a two-panel diagram:

- Actor proposes an action.
- Critic estimates whether the action was better or worse than expected.

Learner takeaway: the critic gives the actor a lower-noise learning signal.

### Week 7: PPO Clip

Show the unclipped and clipped objective curves.

Learner takeaway: PPO limits how far policy updates move in one step.

### Week 8: Robot Reaching MDP

Show robot state, action, reward, and termination for a reaching task.

Learner takeaway: robot learning is still MDP design, just with harder sensors
and actions.

### Week 9: VLA Flow

Show image, language instruction, policy model, and robot action.

Learner takeaway: VLA policies condition action generation on perception and
language.

### Week 10: WAM Storyboard

Show observation and action leading to predicted future frames, then a selected
action.

Learner takeaway: WAM-style training asks whether future prediction improves
control.

## Example Prompt for a Static Diagram

```text
Create a clean educational SVG diagram for Week 1 of an RL course.
Concept: Markov Decision Process interaction loop.
Learner takeaway: RL is a repeated loop between agent and environment.
Canvas: 16:9.
Required elements: state, agent, action, environment, reward, next state.
Use blue for state, orange for action, green for reward, gray for baseline.
Use short labels only. Avoid decorative backgrounds.
Alt text: Diagram showing the RL interaction loop where the agent observes a
state, chooses an action, receives reward and next state from the environment,
then repeats.
```

## Example Prompt for an Animation

```text
Create a 12-second animation for Week 2 of an RL course.
Concept: Q-learning update.
Learner takeaway: one transition updates one cell of the Q-table.
Scene 1: agent moves in a 1D world.
Scene 2: transition tuple appears: (s, a, r, s').
Scene 3: the corresponding Q-table cell highlights.
Scene 4: the cell value moves slightly toward the Bellman target.
Keep labels large and readable. Use no background music. Export as MP4 and GIF.
```
