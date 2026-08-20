# Week 04 Examples - Replay and Delayed Targets

Runnable code for [Week 04](../../docs/lectures/week-04.md) and
[Lab 04](../../docs/labs/lab-04.md). All checkpoints use only the Python
standard library.

## File Map

| File | Purpose |
| --- | --- |
| `env.py` | The same deterministic LineWorld dynamics used in Week 03. |
| `01_replay_buffer.py` | Implement a circular buffer and measure how sampling changes timeline adjacency. |
| `02_target_network_ablation.py` | Compare target motion with online and periodically synchronized parameters. |
| `03_dqn_stabilizers.py` | Run a controlled four-way stabilizer comparison with a linear Q approximator. |

The third filename keeps the DQN connection visible, but the implementation is
not a full DQN: it has no neural network. It isolates replay and delayed-target
mechanics before a heavier framework is introduced.

## Run from the Repository Root

```bash
python examples/week-04/01_replay_buffer.py
python examples/week-04/02_target_network_ablation.py
python examples/week-04/03_dqn_stabilizers.py
```

You can also run each checkpoint from inside this directory:

```bash
cd examples/week-04
python 01_replay_buffer.py
python 02_target_network_ablation.py
python 03_dqn_stabilizers.py
```

## What to Expect

Checkpoint 1 shows that a sampled minibatch contains transitions from distant
original timesteps:

```text
sample set               mean pair gap    adjacent-pair rate
sequential rollout               11.00                 6.2%
uniform replay batch             76.92                 0.6%
```

Checkpoint 2 shows lower average target motion for delayed parameters:

```text
online target:  0.014529
delayed target: 0.006766
```

Checkpoint 3 holds interaction steps, optimizer steps, and evaluation starts
fixed. Every learned variant reaches the same result:

```text
variant              mean return    seed std    success rate   updates
online only               0.9850      0.0000         100.0%       393
target only               0.9850      0.0000         100.0%       393
replay only               0.9850      0.0000         100.0%       393
replay + target           0.9850      0.0000         100.0%       393
```

## Interpretation

The first two checkpoints demonstrate mechanisms. The third produces a null
policy-level result because deterministic LineWorld is easy for every variant.
That does not show the stabilizers are useless; it shows this environment
cannot distinguish them.

The correct next experiment is a pre-specified harder benchmark with the same
budgets and multiple seeds. It is not to rewrite the conclusion until one
method appears to win.

## Limitation Note

These scripts use a linear approximator, a tiny state space, and short CPU-only
runs. They support claims about local mechanics and this exact evaluation
protocol, not neural DQN convergence or robot-control performance.
