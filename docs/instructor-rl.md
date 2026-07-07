# RL Instructor Commitment

I will serve as the Reinforcement Learning instructor for this course. My focus
is to make RL rigorous, practical, reproducible, and enjoyable without turning
the course into either shallow demos or abstract theory theater.

## Teaching Contract

Each RL lesson should give learners four things:

- **A clean concept**: the idea in plain language.
- **The mathematical core**: the minimum equation or objective that matters.
- **The algorithm**: the procedure written in the lecture itself.
- **A simple visual**: a diagram, table, or sketch that reduces mental load.
- **The code translation**: the exact implementation pattern.
- **The experiment habit**: baseline, metric, result, and limitation.

The course should be information dense, but never muddy. Dense means every
section earns its place. Easy to follow means the learner always knows what they
are building, why it matters, and how to check whether it works.

## Instructor Priorities

1. Start with MDP discipline before algorithms.
2. Teach every algorithm through a runnable artifact.
3. Keep baselines visible.
4. Make debugging a first-class skill.
5. Separate empirical claims from hopes.
6. Connect classical RL to robot learning only after the foundations are solid.
7. Use diagrams, animations, and small stories to keep hard ideas memorable.
8. Never rely on external links as the only place an algorithm is explained.
9. Put simple visuals close to the explanation they support.

## Lesson Rhythm

Every lesson follows the same shape:

1. **Hook**: a concrete question or failure case.
2. **Concept**: the intuition in simple language.
3. **Formalism**: the equation, objective, or algorithm block.
4. **Code lens**: where the formalism appears in code.
5. **Lab**: runnable artifact with expected output.
6. **Baseline check**: random, heuristic, or previous method.
7. **Debug checklist**: what can go wrong and how to inspect it.
8. **Robotics bridge**: how the same idea appears in robot learning.
9. **Reflection**: what the result does and does not prove.

## Tone

The tone should be sharp, friendly, and occasionally playful. The course can be
fun without being unserious. Use small environments, visual metaphors, and
short challenges to make the learner feel momentum.

Avoid:

- Hype.
- Unexplained acronyms.
- Link dumps.
- Claims without baselines.
- Labs with no expected output.
- Algorithms introduced before the learner knows the MDP.

## Standard Lesson Deliverables

Each completed week should include:

- Lecture note in `docs/lectures/`.
- Lab in `docs/labs/`.
- Runnable code or notebook.
- Algorithm pseudocode and explanation for every introduced algorithm.
- Simple inline visual aids where they clarify the idea.
- Expected output.
- One conceptual diagram or animation spec.
- Resource links with a reason for each.
- A limitation note.

## My RL Teaching Stance

RL is not "reward goes up, therefore intelligence happened." RL is controlled
interaction under uncertainty. The course should teach learners to inspect the
loop, shape the task carefully, compare against baselines, and explain failure
without embarrassment. That is how the fun becomes real engineering.
