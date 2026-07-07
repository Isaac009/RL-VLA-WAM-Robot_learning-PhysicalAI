# Contributing

Thank you for helping improve the RL-VLA-WAM robot learning course.

This repository values educational clarity, runnable artifacts, and careful
claims. Contributions should help learners understand and reproduce ideas.

## Repository Layout

- **Docs explain.** Lectures and the teaching narrative live in
  `docs/lectures/`.
- **Labs instruct.** Learner-facing exercises live in `docs/labs/`.
- **Examples run.** Runnable code lives in `examples/week-NN/`, one numbered
  file per checkpoint (`01_...py`, `02_...py`), each runnable on its own.
  Shared code for a week (such as its environment) lives beside the
  checkpoints in that week's folder.
- **`src/` is for reusable library code only**, and only once real repetition
  across weeks makes it necessary. While the course is still teaching
  concepts, prefer `examples/`.

Numbered checkpoint files exist so learners can run each stage independently
and the lesson history stays visible — avoid editing an earlier checkpoint in
place to turn it into the next one.

## Contribution Types

- Course notes.
- Labs and assignments.
- Code examples.
- Resource links.
- Benchmark notes.
- Documentation fixes.

## Standards

For course material:

- Define the learning goal.
- Include required and optional reading materials for each lecture.
- Write any introduced algorithm directly in the lecture with pseudocode and
  explanation; do not rely on external links alone.
- Include setup instructions.
- Prefer runnable examples.
- Include expected output when possible.
- Include a quiz or self-check with an answer key for each lecture.
- State limitations.
- Avoid broad claims from narrow experiments.

For resources:

- Link to the primary source when possible.
- Explain why the resource belongs.
- Mention compute, hardware, or access constraints.
- Avoid adding long uncategorized link lists.

## Local Docs

Install the docs dependencies:

```bash
python -m pip install -r requirements-docs.txt
```

Run the local site:

```bash
python -m mkdocs serve
```

Build the site:

```bash
python -m mkdocs build --strict
```
