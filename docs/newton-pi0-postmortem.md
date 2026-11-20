# Case Study: Debugging $\pi_0$ and Physics-Based Action Selection in Project Newton

This reference note documents a complete end-to-end investigation into test-time physics reranking around Physical Intelligence's **$\pi_0$ (`openpi`)** Vision-Language-Action (VLA) policy in **NVIDIA Project Newton (`SolverMuJoCo`)** for 3-cube stacking. Following the [WAM evaluation discipline](wam-research-notes.md), we report both the **engineering root causes** that lifted the base VLA from `0/10` to `20/25` (`80.0%`) and the **negative empirical result** showing why myopic 8-step physics reranking failed to beat a strong nominal policy or geometric heuristic end-to-end.

[Open Interactive Evaluation &amp; Failure Explorer](assets/animations/newton_pi0_postmortem.html){ .md-button .md-button--primary }

---

## Executive Summary

An initially broken `0/10` base $\pi_0$ policy made scripted/hybrid test-time physics planning appear artificially essential (`6/10` oracle, `3/10` estimated). Isolating and repairing four underlying data, normalization, observability, and determinism bugs transformed the picture:

1. **Nominal $\pi_0$ (`K = 1`) jumped from `0/10` to `20/25` (`80.0%`, 95% CI: `59.3–93.2%`)** on `n = 25` disjoint unseen layouts (`fixed_5 + indist_10 + tight_10`).
2. **Short-horizon physics rollouts rank local chunks accurately:** Across same-state oracle audits, physics scoring achieved **Spearman $\rho = 0.830\text{--}0.850$** (matched) and **$0.718\text{--}0.748$** (mismatched) versus **$0.366\text{--}0.544$** for geometric scoring.
3. **High local rank correlation did not produce closed-loop episode gains:** Every paired two-sided McNemar test across `n = 25` had **$p \ge 0.2188$** (`anchored_phys_est`: `19/25` vs. `nominal_pi0`: `20/25`, $p = 1.0$; `anchored_phys_single_mismatch`: `16/25` vs. `anchored_geom_mismatch`: `20/25`, $p = 0.2188$).

---

## Did Upstream Researchers Report These Issues?

!!! note "Summary of Upstream vs. New Empirical Findings"
    Isolated infrastructure symptoms (training-time zero-std instabilities, RLDS `num_workers=0`, and GPU atomic non-determinism) appear in upstream OpenPI and Newton/MuJoCo-Warp threads, while the **closed-loop inference shock**, **39k LeRobot `spawn` deadlock**, **gripper threshold PD lag**, **fidelity scale mismatch**, and **negative closed-loop boundary against an `80%` VLA** were surfaced directly by our diagnostics.

| Issue Encountered | Reported Upstream? | Upstream Context vs. Distinct Behavior Observed Here |
| --- | --- | --- |
| **`std[4] == 0.0` quaternion shock (`12.5σ`)** | **Partial** (`openpi` #814, #454) | OpenPI Issue #814 discusses *training loss explosions* under quantile normalization when DOFs are static. In our setup, Z-score **training converged cleanly (`loss = 0.0847`)**; catastrophic failure triggered silently **only during closed-loop execution** when `1e-4` IK flexion divided by `1e-6` hit `12.58σ`. |
| **Wrist-only self-occlusion (`~80%` cube view)** | **Partial** (`LiberoInputs` / FoV papers) | Standard multi-view configs wire `base_0_rgb + wrist`, whereas single-wrist templates (`mindmap_policy.py`) induce Markov blindness once grasped 5 cm cubes fill ~78–80% of wrist pixels on randomized target locations. |
| **`TorchDataLoader(spawn)` deadlock on LeRobot** | **Partial** (RLDS note in `config.py`) | OpenPI documents `num_workers=0` specifically for RLDS while defaulting LeRobot to `num_workers=2`. On a 124-core node with 39k dual-camera frames, `num_workers > 0` hung indefinitely (`>3h` even under `JAX_PLATFORMS=cpu`) and `compute_norm_stats.py` spun at `5394% CPU`. |
| **`states[t+1]` PD lag & `0.026 m` gripper cliff** | **No** | Logging achieved states (`0.021 m`) instead of commanded targets (`0.000 m`) under a `< 0.026 m` pinch controller introduced double PD lag and fragile `5 mm` grasp margins. |
| **`mujoco_warp` GPU non-determinism & warm-start leak** | **Yes** (`newton` / `mujoco_warp`) | Upstream tracks GPU atomic reduction divergence vs. CPU MuJoCo. We measured `~2.75 cm` GPU divergence (`dJ = 80.26`) vs. `0.0` repeatability using `use_mujoco_cpu=True` and `solver.reset(..., flags=0)`. |
| **Greedy shaping vs. fidelity scale (`fid = 0.4`)** | **No** | Copying `fid = 0.4` from geometric scoring (`dist = 2.0`) into physics rollout scoring (`20–30`) triggered overrides on `96%` of chunks until rescaled to `fid = 16.0`. |
| **8-step physics reranking failing vs. `80%` base VLA** | **No** *(negative boundary)* | Test-time rollout papers (*GPC+*, *VeriVLA*, *CheckVLA*, *SIMPACT*) report wins on weaker or dynamic regimes; against a strong `80%` VLA on quasi-static stacking, `0.8 s` physics reranking did not improve success and caused tight-cluster finger grazes. |

---

## Seven Root Causes & Exact Fixes Applied

### 1. Closed-Loop Quaternion Normalization Shock (`12.5σ`)
- **Symptom:** Open-loop error on training `episode_000000` was already `4.0–13.6 mm`, yet closed-loop rollouts failed `0/5` on held-out `calib_5` and drifted off cubes by chunk 1.
- **Root Cause:** Constant downward wrist orientation in demos yielded `state.std[4] == 0.00000` and `actions.std[4] == 7.8e-6`. Small `~1e-4` closed-loop IK deviations scaled inside `(state - mean) / (std + 1e-6)` up to **`12.58σ`**, corrupting `state_proj` tokens; `DeltaActions(7, -2)` further accumulated quaternion deltas.
- **Fix:** Clamped quaternion standard deviations (`std[3:7] >= 0.05`) in `norm_stats.json` and restricted deltas to 3D translation via `DeltaActions(make_bool_mask(3, -6))`.

### 2. Wrist-Only Partial Observability (`~80%` Occlusion)
- **Symptom:** Even after pinning quaternions, wrist-only $\pi_0$ failed `0/5` on `calib_5`.
- **Root Cause:** Inspecting training frames revealed the held cube occupies `~39,067 / 50,176` pixels (`~78%`) right underneath the lens during carry, occluding `Blue` and `Green`.
- **Fix:** Added a dual-camera transform (`NewtonStackInputs`) feeding both `overview_image -> base_0_rgb` and `image -> right_wrist_0_rgb` with `image_mask=True` across **all** baselines and selectors identically.

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem;margin:1rem 0;">
  <div>
    <img src="../assets/newton_pi0/ep0_wrist_mosaic.png" alt="Wrist camera mosaic showing self-occlusion" style="width:100%;border-radius:8px;border:1px solid #cbd5e1;" />
    <p><small><strong>Before (Wrist-Only):</strong> During transport (<code>t=60, 75</code> and <code>t=150–220</code>), the held block fills ~80% of the wrist view.</small></p>
  </div>
  <div>
    <img src="../assets/newton_pi0/ep0_overview_check.png" alt="Overview workspace camera" style="width:100%;border-radius:8px;border:1px solid #cbd5e1;" />
    <p><small><strong>Fix (Dual-Camera):</strong> Wiring <code>overview_image -> base_0_rgb</code> gives every method identical workspace visibility.</small></p>
  </div>
</div>

### 3. Double PD Tracking Lag, Gripper Cliff & Demo Coverage
- **Symptom:** The original 18-episode dataset stored achieved next states `states[t+1]` (`g = 0.021 m`) directly adjacent to `agent.py`'s `< 0.026 m` closing threshold and lacked off-center visual recovery paths.
- **Fix:** Generated **156 verified `S3=True, base_disturb < 4.0mm` trajectories** (`39,000` frames at 10 Hz, strictly disjoint from `calib_5 + fixed_5 + indist_10 + tight_10`) storing smooth commanded actions `cmds[t]` (`0.000 / 0.040`), tight cube clusters (`7.2–9.2 cm`), and off-axis mid-approach recovery curves. Trained `pi0_newton_stack_v2` (`action_horizon=16`, `batch_size=32`, `peak_lr=1e-4`, 5,000 steps) down to **`loss = 0.0105`**.

### 4. `TorchDataLoader(spawn)` Deadlock & `compute_norm_stats` Hang
- **Symptom:** `compute_norm_stats.py` thrashed at `5394% CPU`; `num_workers=4` DataLoader benchmarks hung `>3 h` even under `JAX_PLATFORMS=cpu`.
- **Fix:** Set `num_workers=0` in `TrainConfig` (`3.6 s` startup) and computed exact `DeltaActions` `RunningStats` directly over all 156 Parquet episodes in **`1.37 s`**.

### 5. GPU Simulation Non-Determinism & Warm-Start State Leakage
- **Symptom:** GPU `mujoco_warp` rollouts diverged up to `2.75 cm` (`dJ = 80.26`) across identical seeds.
- **Fix:** Standardized both execution and twin environments on `use_mujoco_cpu=True` and called `twin_env.solver.reset(twin_env.state_0, flags=0)` before every candidate rollout (`0.0` determinism probe error).

### 6. Uncalibrated Abstention Gate & Overlapping Benchmarks
- **Symptom:** Uncalibrated Regime-3 threshold (`5.5 mm`) hovered `21/24` chunks/episode (`0/10` success); `train_ep1/3` previously spawned overlapping cubes.
- **Fix:** Separated non-overlapping test layouts (`eval_layouts_v3.json`), calibrated `gate_delta = 0.0701` cleanly on held-out `calib_5` (`gate_calibration_v3.json`, `n_pairs=81, n_selected=40`, lifting accepted override mean true advantage from `0.196 -> 0.384`), and verified non-degeneracy (`10.0` overrides, `5.5` abstentions per test episode).

### 7. Fidelity Weight Scale Mismatch (`fid = 0.4 -> 16.0`)
- **Symptom:** Greedy `±1.2 cm` perturbations with `fid = 0.4` overrode `A^(0)` on `~96%` of chunks (`calib_02` failure).
- **Fix:** Refined `anchored` candidates (`3` stochastic $\pi_0$ flow draws + `4× ±6 mm` XY + `1× +10 mm Z` clearance hold) and rescaled `fid = 16.0` to match the `20–30` physics rollout reward scale (`physics_spearman = 0.863` on `calib_5`).

---

## Disjoint Evaluation Results (`n = 25`: `fixed_5 + indist_10 + tight_10`, `ckpt 5000`, `K = 8`)

| Method | Regime | 2-Stack | 3-Stack (95% CI) | Splits (`fix`/`ind`/`tgh`) | Base Disturb | Int / Abs | Lat (ms) | Spearman (`Geom`/`Phys`) |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `nominal_pi0` | Matched (`K=1`) | 21/25 | **20/25** (`80.0%`, 59.3–93.2) | 5/5, 8/10, 7/10 | 12.6 mm | 0.0 / 0.0 | 543 | — |
| `flow_geom_est` | Est. State | 21/25 | 19/25 (`76.0%`, 54.9–90.6) | 5/5, 7/10, 7/10 | 28.5 mm | 25.5 / 0.0 | 669 | 0.366 / 0.841 |
| `flow_phys_est` | Est. State | 19/25 | 18/25 (`72.0%`, 50.6–87.9) | 5/5, 7/10, 7/10 | 26.8 mm | 11.6 / 0.0 | 8,831 | 0.411 / **0.850** |
| `anchored_geom_est` | Est. State | 19/25 | 17/25 (`68.0%`, 46.5–85.1) | 4/5, 6/10, 7/10 | 23.7 mm | 26.6 / 0.0 | 258 | 0.496 / 0.830 |
| `anchored_phys_est` | Est. State | 21/25 | 19/25 (`76.0%`, 54.9–90.6) | 5/5, 8/10, 6/10 | 13.3 mm | 14.0 / 0.0 | 8,301 | 0.544 / **0.848** |
| `anchored_phys_oracle` | Oracle State | 21/25 | **20/25** (`80.0%`, 59.3–93.2) | 5/5, 8/10, 7/10 | 12.6 mm | 14.6 / 0.0 | 8,284 | — |
| `nominal_pi0_mismatch` | Mismatch (`K=1`) | 19/25 | 15/25 (`60.0%`, 38.7–78.9) | 4/5, 6/10, 5/10 | 12.5 mm | 0.0 / 0.0 | 90 | — |
| `anchored_geom_mismatch` | Est. + Mismatch | 20/25 | **20/25** (`80.0%`, 59.3–93.2) | 5/5, 8/10, 7/10 | **5.8 mm** | 25.6 / 0.0 | 254 | 0.413 / 0.748 |
| `anchored_phys_single_mismatch` | Est. + Mismatch | 19/25 | 16/25 (`64.0%`, 42.5–82.0) | 3/5, 7/10, 6/10 | 6.9 mm | 14.8 / 0.0 | 7,968 | 0.445 / 0.718 |
| `anchored_phys_ensemble_nogate` | Mismatch + Ens (`M=3`) | 18/25 | 17/25 (`68.0%`, 46.5–85.1) | 4/5, 6/10, 7/10 | 14.6 mm | 14.0 / 0.0 | 14,460 | 0.479 / 0.735 |
| `anchored_phys_ensemble_gated` | Mismatch + Gate (`δ=0.0701`) | 20/25 | 17/25 (`68.0%`, 46.5–85.1) | 5/5, 5/10, 7/10 | 20.2 mm | 10.0 / 5.5 | 13,614 | — |

### Visual Inspection of Failure (`unseen_tight_00`)

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem;margin:1rem 0;">
  <div>
    <img src="../assets/newton_pi0/tight00_nominal_c8.png" alt="nominal_pi0 grasping Red cleanly" style="width:100%;border-radius:8px;border:1px solid #cbd5e1;" />
    <p><small><code>nominal_pi0</code> (<strong>S3=True</strong>): lifts Red cleanly while Green stays untouched.</small></p>
  </div>
  <div>
    <img src="../assets/newton_pi0/tight00_phys_c8.png" alt="anchored_phys_est lifting Red and Green together" style="width:100%;border-radius:8px;border:1px solid #cbd5e1;" />
    <p><small><code>anchored_phys_est</code> (<strong>S3=False</strong>): a local finger-edge graze wedges Green against Red and lifts both together.</small></p>
  </div>
</div>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem;margin:1rem 0;">
  <div>
    <video controls muted playsinline preload="metadata" style="width:100%;border-radius:8px;border:1px solid #cbd5e1;" src="../assets/newton_pi0/videos/eval_nominal_pi0_unseen_tight_00.mp4"></video>
    <p><small><code>nominal_pi0</code> on <code>unseen_tight_00</code> (S3=True, Base=0.0mm).</small></p>
  </div>
  <div>
    <video controls muted playsinline preload="metadata" style="width:100%;border-radius:8px;border:1px solid #cbd5e1;" src="../assets/newton_pi0/videos/eval_anchored_phys_est_unseen_tight_00.mp4"></video>
    <p><small><code>anchored_phys_est</code> on <code>unseen_tight_00</code> (S3=False, Base=0.0mm).</small></p>
  </div>
</div>

---

## Lessons Learned

1. **Fix base policy normalization and observability first:** Until zero-std scaling (`12.5σ`), wrist self-occlusion (`~80%`), and lagged targets were repaired, a `0/10` policy concealed real model capacity behind synthetic planner gains.
2. **Same-state short-horizon accuracy ($\rho = 0.85$) does not guarantee episode wins:** Overriding an `80%` VLA ~14 times/episode with an 8-step (`0.8 s`) shaping proxy adds `8–14 s/chunk` latency and introduces tight-cluster contact risks (`unseen_tight_00`).
3. **Target physics-sensitive regimes and veto-style triggers:** For rigid pick-and-place where $\pi_0$ already performs well, physics twins should act strictly as high-threshold safety vetoes preserving `A^(0)` unless an explicit failure (collision/drop/topple) is predicted—or be evaluated on tasks where dynamics (slip, COM toppling, compliance) actually dominate geometry.
