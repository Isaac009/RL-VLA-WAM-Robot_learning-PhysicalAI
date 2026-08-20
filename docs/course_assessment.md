# Course Readiness Assessment

**Last reviewed:** 21 August 2026

This assessment reports what is present and reproducible in the repository. It
does not score planned material as if it had already been taught or tested.

## Release Status

| Week | Topic | Status | Evidence |
| --- | --- | --- | --- |
| 01 | MDPs and baselines | Released | Lecture, lab, quiz, visual, and two runnable policy checkpoints |
| 02 | Tabular Q-learning | Released | Lecture, lab, quiz, Q-table visualizer, and three runnable checkpoints |
| 03 | Bellman error and function approximation | Released | Lecture, lab, quiz, animated target visual, and three linear-Q checkpoints |
| 04 | Replay and delayed targets | Released | Lecture, lab, quiz, interactive visualizer, and three controlled diagnostics |
| 05-10 | Policy gradients through WAMs | Planned | Topics and asset stubs exist; complete teaching packages do not yet exist |

The repository is ready to teach Weeks 01-04. It is not yet a complete
ten-week course.

## What Is Strong

- **Progressive executable path:** learners move from observation and baselines
  to tabular learning, then function approximation, replay, and delayed targets.
- **Algorithms are written in the lectures:** external readings extend the
  explanation; they do not replace it.
- **Claims are bounded:** Week 04 reports that all tested variants solve the
  tiny LineWorld task and explicitly treats this as a null comparison, not
  evidence that stabilizers are unnecessary.
- **Metrics are named:** return, success rate, Bellman loss, target change, and
  sample-spacing diagnostics are kept distinct.
- **Repository roles are clear:** docs explain, labs instruct, examples run,
  and shared source modules appear only when repetition justifies them.

## Remaining Risks

1. **Tiny-environment ceiling effects.** LineWorld is useful for inspecting
   mechanics but cannot establish deep-RL stability or robotics performance.
2. **Weeks 05-10 are curriculum promises.** Each still needs a lecture, lab,
   quiz, reviewed visual, runnable checkpoints, and evidence-based limitation
   note before release.
3. **Week 04 is a linear bridge, not a neural DQN implementation.** The lecture
   gives the full algorithm, while the runnable example isolates its mechanics
   without claiming neural-network equivalence.
4. **Visual review remains partly manual.** JavaScript syntax and site builds
   are checked automatically, but browser rendering and accessibility should
   also be reviewed before each public release.

## Verification Record

The August 2026 audit completed the following checks:

```bash
python -m unittest discover -s tests -v
python scripts/check_external_links.py
python -m mkdocs build --strict
```

- All learner-facing Python entrypoints for Weeks 01-04 passed from the
  repository root and from their week folders.
- All 34 Markdown web links resolved or mapped to an existing local
  same-repository path; no HTTP 404 or 410 response remained.
- The Week 02 and Week 04 animation scripts passed JavaScript syntax checks.
- The Week 03 and Week 04 slide sources compiled successfully with Tectonic.

## Next Release Gate

Week 05 should not be marked released until its policy-gradient derivation,
Monte Carlo estimator, baseline comparison, runnable checkpoints, lab, quiz,
visual, and limitation note all pass the same checks. Any empirical claim must
name the environment, seeds, evaluation protocol, metric, and observed scope.
