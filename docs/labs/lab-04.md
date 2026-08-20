# Lab 04 - Replay Buffer and Target Network Ablation

## Goal

Inspect what replay and delayed targets change, then run a controlled
multi-seed comparison without claiming an advantage that the measurements do
not show.

## Visual Reference

Use the [Replay Buffer and Target Network Visualizer](../assets/animations/week4_replay_buffer.html)
to connect buffer insertion, uniform sampling, Bellman targets, online updates,
and target synchronization.

## Setup

This lab uses only the Python standard library. Run commands from the
repository root:

```bash
python examples/week-04/01_replay_buffer.py
python examples/week-04/02_target_network_ablation.py
python examples/week-04/03_dqn_stabilizers.py
```

The same commands also work after changing into `examples/week-04/` and
removing the directory prefix.

## Tasks

1. Run checkpoint 1.
2. Compare all-pairs original-timeline gaps for equal-size sequential and
   replay sample sets.
3. Explain why uniform replay often spreads a sample set across stored time
   without making data truly i.i.d.
4. Inspect the first five sampled transitions and identify termination and
   truncation fields.
5. Run checkpoint 2.
6. Find the steps where the delayed target changes.
7. Recompute the mean absolute target change from the printed history.
8. Explain why slower target motion does not prove better policy return.
9. Run checkpoint 3.
10. Verify that every variant receives 400 interactions and 393 optimizer
    steps.
11. Verify that every learned policy uses the same 100 evaluation starts.
12. Identify why replay variants still process more transition samples per
    optimizer step than non-replay variants.
13. Compare random, always-right, online-only, target-only, replay-only, and
    replay-plus-target results.
14. State the supported conclusion and one tempting unsupported conclusion.

## Expected Output

Checkpoint 1:

```text
=== Week 04 Checkpoint 1: Replay Sample Diagnostics ===
Transitions collected: 234
Replay buffer size: 234
Sampled batch size: 32

sample set               mean pair gap    adjacent-pair rate
sequential rollout               11.00                 6.2%
uniform replay batch             76.92                 0.6%
```

Checkpoint 2:

```text
Mean absolute change between consecutive targets:
  online target:  0.014529
  delayed target: 0.006766
```

Checkpoint 3:

```text
Baselines under the same evaluation protocol:
policy                avg return    success rate
random                    0.6162           72.0%
always right              0.9850          100.0%

Learned variants:
variant              mean return    seed std    success rate   updates
online only               0.9850      0.0000         100.0%       393
target only               0.9850      0.0000         100.0%       393
replay only               0.9850      0.0000         100.0%       393
replay + target           0.9850      0.0000         100.0%       393
```

The final interpretation should say that all four variants achieved the same
policy-level result and that LineWorld is too easy to show a stabilizer
advantage.

## Baseline

The random policy is the no-knowledge baseline. The always-right heuristic is
the environment-specific ceiling under the mixed-start evaluation protocol.

The online-only linear learner is the algorithmic baseline for the stabilizer
comparison. Target-only, replay-only, and replay-plus-target each add a
controlled mechanism.

## Metric

- **Mean all-pairs original-timestep gap** and **adjacent-pair rate** inspect
  how broadly each equal-size sample set spans the stored timeline.
- **Mean absolute target change** inspects how quickly targets move.
- **Average return** and **episode success rate** measure policy behavior.
- **Per-seed returns** expose whether a mean hides failed runs.
- **Interaction and optimizer-step counts** verify two matched budgets. Replay
  still evaluates eight transition samples per update versus one without
  replay, so compute is not matched.

Do not interpret one metric as another. Reduced target motion is not policy
return, and low seed variance is not automatically good performance.

## Reflection Questions

- Why is a sampled replay batch not literally i.i.d.?
- What information is lost if a transition stores only one `done` flag?
- Why does truncation end a rollout while still allowing bootstrap?
- What changes when the target synchronization interval is one?
- Why can a very stale target slow or distort learning?
- Why is a four-way comparison more informative than comparing only online
  learning with replay-plus-target?
- Why is the Week 04 result a null result rather than evidence that
  stabilizers are useless?
- What environment properties would make a stabilizer comparison more
  informative?

## Extension Challenge

Create `examples/week-04/04_harder_lineworld.py` without changing the earlier
checkpoints. Introduce one controlled difficulty, such as stochastic action
slip or a larger state space.

Before running:

- Specify the new MDP and what changed.
- Keep the interaction, optimizer-step, and evaluation budgets equal.
- Predict which diagnostic might change.
- Pre-register what result would count as evidence and what would remain
  inconclusive.

Run at least five seeds and report every per-seed return. Do not promise that
the stabilizers will win.

## Limitation Note

This lab uses a deterministic five-state environment and a linear
approximator. It demonstrates replay sample spacing, delayed-target motion, and
a disclosed comparison structure. It does not test a neural DQN, match compute
across variants, or establish that these mechanisms improve every task.
