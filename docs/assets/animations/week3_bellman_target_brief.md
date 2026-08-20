# Generation Brief: Week 3 Bellman Target Animation

## Goal
Visually demonstrate how DQN constructs a Bellman target and uses it to compute a half-squared optimization loss against the current prediction.

## Format
- **Type**: Self-contained HTML animation with CSS transitions.
- **Filename**: `week3_bellman_target.html`
- **Location**: `docs/assets/animations/`

## Visual Elements
- **Stage**: A bordered container acting as the canvas.
- **Nodes**:
  - `Reward (r)` (Green background)
  - `Next value (gamma max Q(s', a'))` (Purple background)
  - `Target (y)` (Teal background, starts hidden)
  - `Prediction (Q(s, a))` (Purple background)
  - `Loss ((y - Q)^2)` (Red background, starts hidden)
- **Formula**: `y = r + gamma max_a Q_target(s', a)` explicitly shown in monospace text.
- **Status text**: A text label at the bottom that updates to explain each step of the animation.

## Animation Sequence
The animation should loop continuously through these steps:
1. **Step 1**: Particles flow from the **Reward** and **Next value** nodes into the **Target** area.
2. **Step 2**: The **Target** node fades in and scales up.
3. **Step 3**: Particles flow from the newly formed **Target** and the **Prediction** node into the **Loss** area.
4. **Step 4**: The **Loss** node fades in and scales up.
5. **Reset**: The Target and Loss nodes hide, and the loop restarts.

## Accessibility & Responsiveness
- Must respect `prefers-reduced-motion` CSS media queries. When enabled, all animations should be disabled and all nodes (including Target and Loss) should be fully visible statically.
- Must use semantic tags (e.g., `<main aria-labelledby="...">`) and `aria-live="polite"` for the updating status text so screen readers can announce the sequence.
- Must be responsive and adjust node positions on smaller screens to prevent overlap.
