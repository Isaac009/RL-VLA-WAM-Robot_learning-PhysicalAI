# Contributing

Thank you for helping improve the RL-VLA-WAM robot learning course.

This repository values educational clarity, runnable artifacts, and careful
claims. Contributions should help learners understand and reproduce ideas.

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
- Include setup instructions.
- Prefer runnable examples.
- Include expected output when possible.
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
