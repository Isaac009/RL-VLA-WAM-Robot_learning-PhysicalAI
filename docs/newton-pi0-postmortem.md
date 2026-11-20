---
title: "Newton + π₀ Post-Mortem"
hide:
  - navigation
---

# Case Study: Debugging $\pi_0$ and Physics-Based Action Selection in Project Newton

<div class="np-hero" markdown="1">
<div class="np-eyebrow">CASE STUDY · OPENPI π₀ × NVIDIA PROJECT NEWTON</div>
<div class="np-title" role="heading" aria-level="1">Debugging π₀ and Test-Time Physics Selection in Project Newton</div>
<p class="np-subtitle">An end-to-end empirical post-mortem of 3-cube stacking with Physical Intelligence's <strong>π₀ (OpenPI)</strong> VLA and <strong>SolverMuJoCo</strong>: isolating four hidden engineering bugs that lifted the base policy from <code>0/10</code> to <code>20/25 (80.0%)</code>, and documenting why 0.8 s test-time physics reranking fails to improve closed-loop execution over a healthy base VLA.</p>
<div class="np-meta-tags">
<span class="np-chip">Policy: π₀ LoRA (ckpt 5000, loss 0.0105)</span>
<span class="np-chip">Simulator: Project Newton (SolverMuJoCo)</span>
<span class="np-chip">Dataset: 156 Verified Trajectories (39k Frames)</span>
<span class="np-chip">Evaluation: n = 25 Disjoint Layouts · K = 8</span>
</div>
<div class="np-actions" markdown="1">

[Interactive Explorer ↗](assets/animations/newton_pi0_postmortem.html){ .np-pill-btn .np-pill-btn--primary }
[GitHub Repo ↗](https://github.com/Isaac009/RL-VLA-WAM-Robot_learning-PhysicalAI){ .np-pill-btn target="_blank" rel="noopener" }
<a class="np-pill-btn" href="#experimental-results">Results (n = 25) ↓</a>
<a class="np-pill-btn" href="#visual-failure-analysis">Rollout Videos ↓</a>
<a class="np-pill-btn" href="#citation">BibTeX ↓</a>

</div>
<div class="np-tldr">
<span class="np-tldr-badge">TL;DR</span>
<div class="np-tldr-row">
<div class="np-tldr-label">Q</div>
<div class="np-tldr-text">Does short-horizon MuJoCo test-time reranking improve a Vision-Language-Action policy once the base pipeline is properly debugged?</div>
</div>
<div class="np-tldr-row">
<div class="np-tldr-label">A</div>
<div class="np-tldr-text">Fixing closed-loop quaternion normalization (<code>12.58σ</code> shock), wrist self-occlusion (<code>~78%</code>), lagged targets, and spawn deadlocks lifts nominal <strong>π₀ (K = 1)</strong> from <code>0/10</code> to <code>20/25 (80.0%)</code>. Against this strong base VLA, 8-step physics rollouts achieve high local rank correlation (Spearman <code>ρ = 0.830–0.850</code>) yet yield no closed-loop gain (paired McNemar <code>p ≥ 0.2188</code>) and introduce tight-cluster finger grazes when over-intervening.</div>
</div>
</div>
</div>

<div class="np-frame-card">
  <svg viewBox="0 0 960 300" width="100%" role="img" aria-label="Pipeline diagram mapping the seven diagnosed issues across observation, π₀ inference, physics vs. geometric selection, and simulation backend">
    <rect x="0" y="0" width="960" height="300" rx="12" fill="#f8fafc"/>
    <defs>
      <marker id="npArrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
        <polygon points="0 0, 8 3, 0 6" fill="#475569"/>
      </marker>
      <marker id="npArrowOrange" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
        <polygon points="0 0, 8 3, 0 6" fill="#d9480f"/>
      </marker>
    </defs>

    <!-- Node 1: Sensors & State -->
    <rect x="22" y="42" width="175" height="145" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="109" y="66" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">1. Observations &amp; State</text>
    <text x="109" y="88" text-anchor="middle" font-size="11" fill="#475569">Overview RGB (base_0_rgb)</text>
    <text x="109" y="106" text-anchor="middle" font-size="11" fill="#475569">Wrist RGB (right_wrist_0_rgb)</text>
    <text x="109" y="124" text-anchor="middle" font-size="11" fill="#475569">9D TCP + Calibrated Grip</text>
    <rect x="34" y="138" width="151" height="36" rx="7" fill="#fef2f2" stroke="#fca5a5"/>
    <text x="109" y="153" text-anchor="middle" font-size="10" font-weight="700" fill="#b91c1c">Bugs #1 &amp; #2 Fixed Here</text>
    <text x="109" y="167" text-anchor="middle" font-size="9.5" fill="#7f1d1d">12.58σ std=0 · ~78% wrist block</text>

    <line x1="197" y1="114" x2="245" y2="114" stroke="#475569" stroke-width="2" marker-end="url(#npArrow)"/>

    <!-- Node 2: OpenPI Policy -->
    <rect x="252" y="42" width="185" height="145" rx="12" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>
    <text x="344" y="66" text-anchor="middle" font-size="12" font-weight="700" fill="#1e3a8a">2. OpenPI π₀ Flow Policy</text>
    <text x="344" y="88" text-anchor="middle" font-size="11" fill="#475569">156 Demos · 39k Frames</text>
    <text x="344" y="106" text-anchor="middle" font-size="11" fill="#475569">K = 8 VLA Candidates:</text>
    <text x="344" y="123" text-anchor="middle" font-size="10.5" fill="#1d4ed8">3 Flow + 4×(±6mm) + (+10mm Z)</text>
    <rect x="264" y="138" width="161" height="36" rx="7" fill="#eff6ff" stroke="#bfdbfe"/>
    <text x="344" y="153" text-anchor="middle" font-size="10" font-weight="700" fill="#1d4ed8">Bugs #3 &amp; #4 Fixed Here</text>
    <text x="344" y="167" text-anchor="middle" font-size="9.5" fill="#1e40af">Cmd targets · num_workers=0</text>

    <!-- Branch Arrows -->
    <path d="M 437 86 L 502 64" stroke="#047857" stroke-width="2" fill="none" marker-end="url(#npArrow)"/>
    <path d="M 437 142 L 502 186" stroke="#d9480f" stroke-width="2" fill="none" marker-end="url(#npArrowOrange)"/>

    <!-- Branch A: Nominal pi0 -->
    <rect x="510" y="24" width="210" height="78" rx="12" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="1.5"/>
    <text x="615" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">Nominal π₀ (A⁽⁰⁾, K = 1)</text>
    <text x="615" y="66" text-anchor="middle" font-size="13" font-weight="800" fill="#047857">0/10 → 20/25 (80.0%)</text>
    <text x="615" y="84" text-anchor="middle" font-size="10" fill="#065f46">543 ms/chunk · Zero overrides</text>

    <!-- Branch B: Test-time Twin / Geo Selector -->
    <rect x="510" y="122" width="210" height="152" rx="12" fill="#ffffff" stroke="#fdba74" stroke-width="1.5"/>
    <text x="615" y="145" text-anchor="middle" font-size="12" font-weight="700" fill="#9a3412">3. Test-Time Selector (K = 8)</text>
    <text x="615" y="165" text-anchor="middle" font-size="10.5" fill="#475569">Non-privileged Wrist Estimator B_t</text>
    <text x="615" y="182" text-anchor="middle" font-size="10.5" fill="#1e293b">CPU MuJoCo Twin (8-step / 0.8 s)</text>
    <text x="615" y="199" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0284c7">Local ρ = 0.830–0.850 (vs 0.544)</text>
    <rect x="522" y="212" width="186" height="50" rx="7" fill="#fff7ed" stroke="#fed7aa"/>
    <text x="615" y="227" text-anchor="middle" font-size="9.8" font-weight="700" fill="#9a3412">Bugs #5–#7 Fixed Here</text>
    <text x="615" y="241" text-anchor="middle" font-size="9.2" fill="#7c2d12">CPU 0.0 drift · δ=0.0701 · fid=16.0</text>
    <text x="615" y="254" text-anchor="middle" font-size="9.2" fill="#b45309">19/25 est · 20/25 oracle · ~8.3 s/chunk</text>

    <!-- Node 4: Closed-loop execution -->
    <path d="M 720 64 L 774 128" stroke="#475569" stroke-width="2" fill="none" marker-end="url(#npArrow)"/>
    <path d="M 720 198 L 774 156" stroke="#d9480f" stroke-width="2" fill="none" marker-end="url(#npArrowOrange)"/>

    <rect x="780" y="76" width="158" height="148" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="859" y="101" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">4. Closed-Loop Env</text>
    <text x="859" y="121" text-anchor="middle" font-size="10.5" fill="#475569">Project Newton Exec</text>
    <text x="859" y="139" text-anchor="middle" font-size="10.5" fill="#475569">25 Disjoint Layouts</text>
    <line x1="796" y1="154" x2="922" y2="154" stroke="#e2e8f0" stroke-width="1"/>
    <text x="859" y="174" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0f172a">McNemar p ≥ 0.2188</text>
    <text x="859" y="191" text-anchor="middle" font-size="9.8" fill="#64748b">~14 overrides/ep risk</text>
    <text x="859" y="207" text-anchor="middle" font-size="9.8" fill="#b91c1c">tight-cluster grazes</text>
  </svg>
  <p class="np-caption">
    <strong>System Overview &amp; Bug Attribution.</strong> Isolating bugs #1–#4 lifted base nominal π₀ from <code>0/10</code> to <code>20/25</code>. Fixing twin determinism (#5), gate calibration (#6), and fidelity scaling (#7) gave strong local chunk ranking (<code>ρ = 0.850</code>), but closed-loop reranking still could not surpass the repaired base policy.
  </p>
</div>

<div class="np-kpi-grid">
  <div class="np-kpi">
    <div class="np-kpi-num np-kpi-num--ok">0/10 → 20/25</div>
    <div class="np-kpi-lbl"><strong>80.0%</strong> nominal π₀ 3-stack rate (95% CI: 59.3–93.2%) after base fixes</div>
  </div>
  <div class="np-kpi">
    <div class="np-kpi-num np-kpi-num--accent">12.58σ Shock</div>
    <div class="np-kpi-lbl">Silent closed-loop OOD explosion from <code>state.std[4] == 0.0</code></div>
  </div>
  <div class="np-kpi">
    <div class="np-kpi-num np-kpi-num--blue">0.850 vs 0.411</div>
    <div class="np-kpi-lbl">Same-state Spearman rank correlation (Physics vs Geometric heuristic)</div>
  </div>
  <div class="np-kpi">
    <div class="np-kpi-num">p ≥ 0.2188</div>
    <div class="np-kpi-lbl">Every paired McNemar test across <code>n = 25</code> (no end-to-end gain)</div>
  </div>
</div>

<div class="np-spotlight">
  <div class="np-card-label">Central Finding</div>
  <p class="np-question-line">
    High short-horizon twin accuracy (ρ = 0.85) does not translate into closed-loop episode gains once the base VLA is healthy.
  </p>
</div>

<div class="np-two-col">
  <div class="np-card">
    <div class="np-card-label">1. Engineering Trap</div>
    <h3>Why Early Physics Reranking Looked Essential</h3>
    <p>An initially broken <code>0/10</code> base π₀ policy made hybrid test-time physics planning appear indispensable (<code>6/10</code> oracle, <code>3/10</code> estimated). In reality, π₀ was suffering from zero-std normalization spikes, wrist self-occlusion, and lagged target logging—causing synthetic planner improvements to mask basic policy pipeline defects.</p>
  </div>
  <div class="np-card">
    <div class="np-card-label">2. Negative Empirical Result</div>
    <h3>When Test-Time Rollouts Hurt Instead of Help</h3>
    <p>After fixing the policy down to <code>loss = 0.0105</code> (<code>20/25</code>), intervening <code>11.6–14.8</code> times/episode via an <code>0.8 s</code> continuous shaping proxy added <code>8.0–14.5 s/chunk</code> latency and introduced tight-cluster finger grazes (<code>unseen_tight_00</code>), while a simple geometric filter matched <code>20/25</code> under mismatch.</p>
  </div>
</div>

---

## Experimental Results

Benchmark results below are evaluated across **`n = 25` strictly disjoint unseen layouts** (`fixed_5` + `indist_10` + `tight_10`) using `pi0_newton_stack_v2` (`ckpt 5000`, `K = 8` matched candidate budget, CPU MuJoCo determinism).

<div id="experimental-results" class="np-card">
  <div class="np-card-label">Interactive Benchmark Explorer · n = 25 Unseen Layouts</div>
  <div class="np-controls">
    <div class="np-btn-group" aria-label="Regime filter">
      <button type="button" class="np-btn is-active" data-np-group="all">All 11 Methods</button>
      <button type="button" class="np-btn" data-np-group="matched">Matched (Regimes 1 &amp; 2)</button>
      <button type="button" class="np-btn" data-np-group="mismatch">Mismatched (Regime 3)</button>
    </div>
    <div class="np-btn-group" aria-label="Split filter">
      <button type="button" class="np-btn is-active" data-np-split="overall">Overall (n=25)</button>
      <button type="button" class="np-btn" data-np-split="fixed">Fixed (n=5)</button>
      <button type="button" class="np-btn" data-np-split="indist">In-Dist (n=10)</button>
      <button type="button" class="np-btn" data-np-split="tight">Tight Cluster (n=10)</button>
    </div>
  </div>
  <div id="np-bar-chart" style="margin:0.75rem 0 0.25rem;"></div>
</div>

<div class="np-table-wrap">
  <table class="np-table np-table--bench">
    <thead>
      <tr>
        <th>Method &amp; Regime</th>
        <th>2-Stk</th>
        <th>3-Stack [95% CI]</th>
        <th>Splits (f/i/t)</th>
        <th>Base</th>
        <th>Int / Abs</th>
        <th>Lat (ms)</th>
        <th>ρ (G / P)</th>
      </tr>
    </thead>
    <tbody id="np-tbl-body">
      <tr class="is-best"><td><code>nominal_pi0</code><span class="np-tbl-sub">Matched (K=1)</span></td><td>21/25</td><td><strong>20/25 (80.0%)</strong><span class="np-tbl-sub">CI 59.3–93.2%</span></td><td>5/5, 8/10, 7/10</td><td>12.6 mm</td><td>0.0 / 0.0</td><td>543</td><td>—</td></tr>
      <tr><td><code>flow_geom_est</code><span class="np-tbl-sub">Estimated State</span></td><td>21/25</td><td>19/25 (76.0%)<span class="np-tbl-sub">CI 54.9–90.6%</span></td><td>5/5, 7/10, 7/10</td><td>28.5 mm</td><td>25.5 / 0.0</td><td>669</td><td>.366 / .841</td></tr>
      <tr><td><code>flow_phys_est</code><span class="np-tbl-sub">Estimated State</span></td><td>19/25</td><td>18/25 (72.0%)<span class="np-tbl-sub">CI 50.6–87.9%</span></td><td>5/5, 7/10, 7/10</td><td>26.8 mm</td><td>11.6 / 0.0</td><td>8,831</td><td>.411 / <strong>.850</strong></td></tr>
      <tr><td><code>anchored_geom_est</code><span class="np-tbl-sub">Estimated State</span></td><td>19/25</td><td>17/25 (68.0%)<span class="np-tbl-sub">CI 46.5–85.1%</span></td><td>4/5, 6/10, 7/10</td><td>23.7 mm</td><td>26.6 / 0.0</td><td>258</td><td>.496 / .830</td></tr>
      <tr class="is-highlight"><td><code>anchored_phys_est</code><span class="np-tbl-sub">Estimated State</span></td><td>21/25</td><td>19/25 (76.0%)<span class="np-tbl-sub">CI 54.9–90.6%</span></td><td>5/5, 8/10, 6/10</td><td>13.3 mm</td><td>14.0 / 0.0</td><td>8,301</td><td>.544 / <strong>.848</strong></td></tr>
      <tr class="is-best"><td><code>anchored_phys_oracle</code><span class="np-tbl-sub">Oracle State</span></td><td>21/25</td><td><strong>20/25 (80.0%)</strong><span class="np-tbl-sub">CI 59.3–93.2%</span></td><td>5/5, 8/10, 7/10</td><td>12.6 mm</td><td>14.6 / 0.0</td><td>8,284</td><td>—</td></tr>
      <tr><td><code>nominal_pi0_mismatch</code><span class="np-tbl-sub">Mismatch (K=1)</span></td><td>19/25</td><td>15/25 (60.0%)<span class="np-tbl-sub">CI 38.7–78.9%</span></td><td>4/5, 6/10, 5/10</td><td>12.5 mm</td><td>0.0 / 0.0</td><td>90</td><td>—</td></tr>
      <tr class="is-best"><td><code>anchored_geom_mismatch</code><span class="np-tbl-sub">Est. + Mismatch</span></td><td>20/25</td><td><strong>20/25 (80.0%)</strong><span class="np-tbl-sub">CI 59.3–93.2%</span></td><td>5/5, 8/10, 7/10</td><td><strong>5.8 mm</strong></td><td>25.6 / 0.0</td><td>254</td><td>.413 / .748</td></tr>
      <tr><td><code>anchored_phys_single_mismatch</code><span class="np-tbl-sub">Est. + Mismatch</span></td><td>19/25</td><td>16/25 (64.0%)<span class="np-tbl-sub">CI 42.5–82.0%</span></td><td>3/5, 7/10, 6/10</td><td>6.9 mm</td><td>14.8 / 0.0</td><td>7,968</td><td>.445 / .718</td></tr>
      <tr><td><code>anchored_phys_ensemble_nogate</code><span class="np-tbl-sub">Mismatch + Ens (M=3)</span></td><td>18/25</td><td>17/25 (68.0%)<span class="np-tbl-sub">CI 46.5–85.1%</span></td><td>4/5, 6/10, 7/10</td><td>14.6 mm</td><td>14.0 / 0.0</td><td>14,460</td><td>.479 / .735</td></tr>
      <tr><td><code>anchored_phys_ensemble_gated</code><span class="np-tbl-sub">Mismatch + Gate (δ=0.0701)</span></td><td>20/25</td><td>17/25 (68.0%)<span class="np-tbl-sub">CI 46.5–85.1%</span></td><td>5/5, 5/10, 7/10</td><td>20.2 mm</td><td>10.0 / 5.5</td><td>13,614</td><td>—</td></tr>
    </tbody>
  </table>
</div>

<div class="np-two-col">
  <div class="np-card">
    <div class="np-card-label">Statistical Comparison (McNemar Exact Tests)</div>
    <h3>No Significant End-to-End Advantage</h3>
    <p><strong>Matched regime:</strong> <code>anchored_phys_est</code> (<code>19/25</code>) vs. <code>nominal_pi0</code> (<code>20/25</code>) yields <code>p = 1.0</code> (1 only vs. 2 only). <code>anchored_phys_oracle</code> (<code>20/25</code>) vs. <code>anchored_phys_est</code> is also <code>p = 1.0</code>.</p>
    <p><strong>Mismatched regime:</strong> <code>anchored_phys_single_mismatch</code> (<code>16/25</code>) vs. <code>nominal_pi0_mismatch</code> (<code>15/25</code>) yields <code>p = 1.0</code>, and vs. <code>anchored_geom_mismatch</code> (<code>20/25</code>) yields <code>p = 0.2188</code>.</p>
    <p><strong>Ensemble gating:</strong> Calibrating <code>δ = 0.0701</code> on <code>calib_5</code> prevented degenerate hovering (<code>5.5</code> abstentions/ep vs. <code>21/24</code>), doubling accepted override true advantage (<code>0.196 → 0.384</code>), yet matched <code>nogate</code> at <code>17/25</code> (<code>p = 1.0</code>).</p>
  </div>
  <div class="np-card">
    <div class="np-card-label">Training Progression (probe_checkpoints_v3.json)</div>
    <h3>Nominal π₀ Base Policy Probe (n = 6)</h3>
    <svg viewBox="0 0 420 155" width="100%" role="img" aria-label="Checkpoint probe progression across training steps 1000 to 5000">
      <rect x="0" y="0" width="420" height="155" rx="8" fill="#f8fafc"/>
      <line x1="42" y1="120" x2="395" y2="120" stroke="#cbd5e1" stroke-width="1"/>
      <line x1="42" y1="22" x2="395" y2="22" stroke="#e2e8f0" stroke-dasharray="3,3"/>
      <line x1="42" y1="71" x2="395" y2="71" stroke="#e2e8f0" stroke-dasharray="3,3"/>
      <text x="36" y="25" text-anchor="end" font-size="9.5" fill="#64748b">100%</text>
      <text x="36" y="74" text-anchor="end" font-size="9.5" fill="#64748b">50%</text>
      <text x="36" y="123" text-anchor="end" font-size="9.5" fill="#64748b">0%</text>
      <!-- Bars for S3 rate out of 6 -->
      <rect x="58" y="103" width="38" height="17" rx="4" fill="#94a3b8"/>
      <text x="77" y="98" text-anchor="middle" font-size="9.5" font-weight="700" fill="#334155">1/6</text>
      <text x="77" y="136" text-anchor="middle" font-size="9.5" fill="#475569">1000</text>
      <rect x="130" y="87" width="38" height="33" rx="4" fill="#64748b"/>
      <text x="149" y="82" text-anchor="middle" font-size="9.5" font-weight="700" fill="#334155">2/6</text>
      <text x="149" y="136" text-anchor="middle" font-size="9.5" fill="#475569">2000</text>
      <rect x="202" y="38" width="38" height="82" rx="4" fill="#0ea5e9"/>
      <text x="221" y="33" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0369a1">5/6</text>
      <text x="221" y="136" text-anchor="middle" font-size="9.5" fill="#475569">3000</text>
      <rect x="274" y="71" width="38" height="49" rx="4" fill="#3b82f6"/>
      <text x="293" y="66" text-anchor="middle" font-size="9.5" font-weight="700" fill="#1d4ed8">3/6</text>
      <text x="293" y="136" text-anchor="middle" font-size="9.5" fill="#475569">4000</text>
      <rect x="346" y="54" width="38" height="66" rx="4" fill="#047857"/>
      <text x="365" y="49" text-anchor="middle" font-size="9.5" font-weight="700" fill="#047857">4/6*</text>
      <text x="365" y="136" text-anchor="middle" font-size="9.5" font-weight="700" fill="#047857">5000</text>
    </svg>
    <p style="margin-top:0.55rem;">Across <code>1 newton_train_01 + 5 calib_5</code> probe episodes, mean base disturbance dropped from <code>35.3 mm</code> (ckpt 2000) to <code>9.8 mm</code> (ckpt 5000, *which scored <strong>20/25</strong> on the full disjoint evaluation).</p>
  </div>
</div>

---

## Visual Failure Analysis

In `unseen_tight_00`, both `nominal_pi0` and `anchored_phys_est` achieve clean `0.0 mm` base cube alignment. However, when lifting **Red** in a tight cluster (`7.2–9.2 cm` spacing), one continuous shaping override at chunk 6 nudges a gripper finger edge against **Green**, wedging both cubes up together.

<div class="np-two-col">
  <div class="np-frame-card" style="margin:0;">
    <img src="../assets/newton_pi0/tight00_nominal_c8.png" alt="nominal_pi0 grasping Red cleanly" />
    <p class="np-caption"><span class="np-badge np-badge--ok">S3 = True</span> <code>nominal_pi0</code> (<code>unseen_tight_00</code>): lifts Red cleanly while Green stays untouched on the tabletop.</p>
  </div>
  <div class="np-frame-card" style="margin:0;">
    <img src="../assets/newton_pi0/tight00_phys_c8.png" alt="anchored_phys_est wedging Green against Red" />
    <p class="np-caption"><span class="np-badge np-badge--bad">S3 = False</span> <code>anchored_phys_est</code> (<code>unseen_tight_00</code>): a local shaping override grazes Green against Red, lifting both together.</p>
  </div>
</div>

<div id="visual-failure-analysis" class="np-card" style="margin-top:1.25rem;">
  <div class="np-card-label">Interactive Rollout Video Comparator (13 Recorded Evaluations)</div>
  <div class="np-controls" style="margin-top:0.4rem;">
    <div class="np-btn-group" aria-label="Layout selector">
      <button type="button" class="np-btn is-active" data-np-ep="unseen_tight_00">unseen_tight_00 (Regression Case)</button>
      <button type="button" class="np-btn" data-np-ep="fixed_mm_ep0">fixed_mm_ep0 (Matched Baseline)</button>
      <button type="button" class="np-btn" data-np-ep="calib_00">calib_00 (Holdout Split)</button>
    </div>
    <button type="button" class="np-btn" id="np-sync-play">Play / Sync Both</button>
  </div>
  <div class="np-two-col" style="margin-bottom:0.25rem;">
    <div class="np-frame-card" style="margin:0;">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:0.5rem;margin-bottom:0.55rem;">
        <label for="np-vid-left-sel" style="font-size:0.78rem;font-weight:700;">Left Policy:</label>
        <select id="np-vid-left-sel" class="np-btn" style="border-radius:8px;max-width:250px;"></select>
      </div>
      <video id="np-vid-left" controls muted playsinline preload="metadata" src="../assets/newton_pi0/videos/eval_nominal_pi0_unseen_tight_00.mp4"></video>
      <p class="np-caption" id="np-vid-left-cap"><code>nominal_pi0</code> on <code>unseen_tight_00</code> (S3=True, Base=0.0 mm).</p>
    </div>
    <div class="np-frame-card" style="margin:0;">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:0.5rem;margin-bottom:0.55rem;">
        <label for="np-vid-right-sel" style="font-size:0.78rem;font-weight:700;">Right Policy:</label>
        <select id="np-vid-right-sel" class="np-btn" style="border-radius:8px;max-width:250px;"></select>
      </div>
      <video id="np-vid-right" controls muted playsinline preload="metadata" src="../assets/newton_pi0/videos/eval_anchored_phys_est_unseen_tight_00.mp4"></video>
      <p class="np-caption" id="np-vid-right-cap"><code>anchored_phys_est</code> on <code>unseen_tight_00</code> (S3=False, Base=0.0 mm).</p>
    </div>
  </div>
</div>

---

## Root Causes & Verified Fixes

Below is the dual-camera observability repair alongside all seven engineering root causes isolated and verified across data, policy normalization, simulation determinism, and gating.

<div class="np-obs-grid">
  <div class="np-frame-card" style="margin:0;">
    <img src="../assets/newton_pi0/ep0_wrist_mosaic.png" alt="Wrist camera mosaic showing self-occlusion" />
    <p class="np-caption"><strong>Before (Wrist-Only):</strong> At <code>t = 60, 75</code> and <code>t = 150–220</code>, the carried cube fills ~78% (<code>39,067 / 50,176</code> px) of the wrist frame, occluding placement targets.</p>
  </div>
  <div class="np-frame-card" style="margin:0;">
    <img src="../assets/newton_pi0/ep0_overview_check.png" alt="Overview workspace camera" />
    <p class="np-caption"><strong>Fix (Dual-Camera Input):</strong> Mapping <code>overview_image → base_0_rgb</code> alongside <code>right_wrist_0_rgb</code> gives every policy and baseline identical global visibility.</p>
  </div>
</div>

<div class="np-bug-grid">
  <div class="np-card">
    <div class="np-bug-head"><span class="np-bug-num">Bug #1 · Normalization</span><span class="np-badge np-badge--ok">0/5 → 20/25</span></div>
    <h3>Closed-Loop Quaternion Shock (<code>12.58σ</code>)</h3>
    <p class="np-kv"><strong>Symptom:</strong> Training loss reached <code>0.0847</code>, yet closed-loop rollouts failed <code>0/5</code> on <code>calib_5</code> and drifted off targets by chunk 1.</p>
    <p class="np-kv"><strong>Root Cause:</strong> Near-constant downward wrist poses caused <code>state.std[4] == 0.00000</code> and <code>actions.std[4] == 7.8e-6</code>; tiny <code>~1e-4</code> closed-loop IK deviations scaled by <code>1 / (std + 1e-6)</code> into <code>12.58σ</code> spikes while <code>DeltaActions(7, -2)</code> accumulated rotational drift.</p>
    <p class="np-kv"><strong>Fix:</strong> Clamped quaternion standard deviations (<code>std[3:7] &gt;= 0.05</code>) in <code>norm_stats.json</code> and restricted deltas to 3D translation via <code>DeltaActions(make_bool_mask(3, -6))</code>.</p>
  </div>

  <div class="np-card">
    <div class="np-bug-head"><span class="np-bug-num">Bug #2 · Observability</span><span class="np-badge np-badge--ok">Dual-Cam Parity</span></div>
    <h3>Wrist-Only Self-Occlusion (<code>~78%</code> Blindness)</h3>
    <p class="np-kv"><strong>Symptom:</strong> Even after fixing quaternions, wrist-only π₀ scored <code>0/5</code> on randomized target layouts in <code>calib_5</code>.</p>
    <p class="np-kv"><strong>Root Cause:</strong> During carry, the held 5 cm block fills ~78% of wrist pixels directly beneath the lens, hiding Blue and Green targets.</p>
    <p class="np-kv"><strong>Fix:</strong> Implemented <code>NewtonStackInputs</code> wiring both <code>overview_image → base_0_rgb</code> and <code>image → right_wrist_0_rgb</code> with <code>image_mask=True</code> uniformly across all evaluated policies and selectors.</p>
  </div>

  <div class="np-card">
    <div class="np-bug-head"><span class="np-bug-num">Bug #3 · Control &amp; Data</span><span class="np-badge np-badge--ok">loss = 0.0105</span></div>
    <h3>PD Tracking Lag &amp; <code>0.026 m</code> Gripper Cliff</h3>
    <p class="np-kv"><strong>Symptom:</strong> The initial 18-episode dataset logged achieved states <code>states[t+1]</code> (<code>g = 0.021 m</code>), sitting adjacent to <code>agent.py</code>'s <code>&lt; 0.026 m</code> pinch cliff and lacking off-center recovery trajectories.</p>
    <p class="np-kv"><strong>Fix:</strong> Generated <strong>156 verified <code>S3=True, base_disturb &lt; 4.0 mm</code> episodes</strong> (<code>39,000</code> frames at 10 Hz, strictly disjoint from <code>calib_5 + fixed_5 + indist_10 + tight_10</code>) logging smooth commands (<code>0.000 / 0.040</code>), tight clusters (<code>7.2–9.2 cm</code>), and off-axis funneling paths.</p>
  </div>

  <div class="np-card">
    <div class="np-bug-head"><span class="np-bug-num">Bug #4 · DataLoader</span><span class="np-badge np-badge--ok">3h Hang → 3.6 s</span></div>
    <h3><code>TorchDataLoader(spawn)</code> Deadlock on 39k Frames</h3>
    <p class="np-kv"><strong>Symptom:</strong> <code>compute_norm_stats.py</code> spun at <code>5394% CPU</code> and LeRobot loading with <code>num_workers=4</code> deadlocked <code>&gt;3 h</code> even under <code>JAX_PLATFORMS=cpu</code> on a 124-core node.</p>
    <p class="np-kv"><strong>Fix:</strong> Set <code>num_workers=0</code> in <code>TrainConfig</code> (<code>3.6 s</code> startup) and computed exact <code>DeltaActions</code> <code>RunningStats</code> directly over the 156 Parquet episodes in <strong>1.37 s</strong>.</p>
  </div>

  <div class="np-card">
    <div class="np-bug-head"><span class="np-bug-num">Bug #5 · Determinism</span><span class="np-badge np-badge--ok">2.75 cm → 0.0</span></div>
    <h3>GPU Simulation Divergence &amp; Warm-Start Leak</h3>
    <p class="np-kv"><strong>Symptom:</strong> GPU <code>mujoco_warp</code> rollouts diverged up to <code>2.75 cm</code> (<code>dJ = 80.26</code>) across identical random seeds due to parallel atomic reductions and residual solver state.</p>
    <p class="np-kv"><strong>Fix:</strong> Standardized both execution and twin environments on <code>use_mujoco_cpu=True</code> and invoked <code>twin_env.solver.reset(twin_env.state_0, flags=0)</code> before every candidate rollout (<code>0.0</code> probe drift).</p>
  </div>

  <div class="np-card">
    <div class="np-bug-head"><span class="np-bug-num">Bugs #6 &amp; #7 · Calibration</span><span class="np-badge np-badge--blue">ρ = 0.863 calib</span></div>
    <h3>Abstention Gate &amp; Fidelity Weight Rescaling</h3>
    <p class="np-kv"><strong>Symptom:</strong> An uncalibrated <code>5.5 mm</code> gate hovered <code>21/24</code> chunks/episode (<code>0/10</code> success), while <code>fid = 0.4</code> caused <code>96%</code> override churn against <code>20–30</code> physics rollout scores.</p>
    <p class="np-kv"><strong>Fix:</strong> Separated non-overlapping test splits (<code>eval_layouts_v3.json</code>), rescaled <code>fid = 16.0</code> over anchored candidates (<code>3</code> flow + <code>4× ±6 mm</code> XY + <code>+10 mm</code> Z), and calibrated <code>δ = 0.0701</code> on held-out <code>calib_5</code> (lifting selected override advantage <code>0.196 → 0.384</code>).</p>
  </div>
</div>

---

## Upstream Context vs. Empirical Findings

<div class="np-table-wrap">
  <table class="np-table">
    <thead>
      <tr>
        <th>Issue Encountered</th>
        <th>Upstream Status</th>
        <th>Upstream Context vs. Behavior Observed Here</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong><code>std[4] == 0.0</code> quaternion shock (<code>12.58σ</code>)</strong></td>
        <td><span class="np-badge np-badge--warn">Partial (<code>openpi</code> #814, #454)</span></td>
        <td>Upstream reports training loss explosions under quantile normalization for constant DOFs. Here, Z-score <strong>training converged cleanly (<code>loss = 0.0847</code>)</strong>, failing silently only at closed-loop inference.</td>
      </tr>
      <tr>
        <td><strong>Wrist-only self-occlusion (<code>~78%</code> block)</strong></td>
        <td><span class="np-badge np-badge--warn">Partial (<code>LiberoInputs</code>)</span></td>
        <td>Standard multi-view configs wire <code>base_0_rgb + wrist</code>, while single-wrist templates (<code>mindmap_policy.py</code>) induce Markov blindness once grasped 5 cm cubes fill ~78% of wrist pixels.</td>
      </tr>
      <tr>
        <td><strong><code>TorchDataLoader(spawn)</code> deadlock on LeRobot</strong></td>
        <td><span class="np-badge np-badge--warn">Partial (RLDS <code>config.py</code>)</span></td>
        <td>OpenPI notes <code>num_workers=0</code> for RLDS while leaving LeRobot at <code>num_workers=2</code>. On 39k dual-camera frames across 124 cores, <code>num_workers &gt; 0</code> deadlocked <code>&gt;3 h</code>.</td>
      </tr>
      <tr>
        <td><strong><code>states[t+1]</code> PD lag &amp; <code>0.026 m</code> gripper cliff</strong></td>
        <td><span class="np-badge np-badge--blue">New Finding</span></td>
        <td>Logging achieved states (<code>0.021 m</code>) rather than commanded targets (<code>0.000 m</code>) near a binary <code>&lt; 0.026 m</code> close threshold introduced double PD lag and fragile grasp margins.</td>
      </tr>
      <tr>
        <td><strong><code>mujoco_warp</code> GPU divergence &amp; warm-start</strong></td>
        <td><span class="np-badge np-badge--ok">Tracked Upstream</span></td>
        <td>Measured <code>~2.75 cm</code> GPU divergence (<code>dJ = 80.26</code>) vs. <code>0.0</code> repeatability via <code>use_mujoco_cpu=True</code> and <code>solver.reset(..., flags=0)</code>.</td>
      </tr>
      <tr>
        <td><strong>Greedy shaping vs. fidelity scale (<code>fid = 0.4</code>)</strong></td>
        <td><span class="np-badge np-badge--blue">New Finding</span></td>
        <td>Reusing geometric trust-region weights (<code>0.4</code>) against physics shaping scales (<code>20–30</code>) triggered overrides on <code>96%</code> of chunks until rescaled to <code>fid = 16.0</code>.</td>
      </tr>
      <tr>
        <td><strong>8-step physics reranking vs. <code>80%</code> base VLA</strong></td>
        <td><span class="np-badge np-badge--bad">Negative Boundary</span></td>
        <td>Unlike wins reported on weaker baselines or dynamic tasks (<em>GPC+</em>, <em>VeriVLA</em>, <em>CheckVLA</em>, <em>SIMPACT</em>), <code>0.8 s</code> physics reranking did not improve over an <code>80%</code> VLA on rigid stacking.</td>
      </tr>
    </tbody>
  </table>
</div>

---

## Lessons Learned & Next Steps

<div class="np-two-col" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr));">
  <div class="np-card">
    <div class="np-card-label">Takeaway 01</div>
    <h3>Fix Base Observability &amp; Normalization First</h3>
    <p>Until zero-std normalization spikes (<code>12.58σ</code>), wrist occlusion (<code>~78%</code>), and target alignment were repaired, a <code>0/10</code> policy concealed real model capacity behind synthetic planner gains.</p>
  </div>
  <div class="np-card">
    <div class="np-card-label">Takeaway 02</div>
    <h3>Same-State ρ Does Not Guarantee Episode Wins</h3>
    <p>Intervening ~14×/episode with a <code>0.8 s</code> shaping proxy against an <code>80%</code> base policy adds <code>8.3–14.5 s/chunk</code> overhead and causes tight-cluster contact risks (<code>unseen_tight_00</code>).</p>
  </div>
  <div class="np-card">
    <div class="np-card-label">Takeaway 03</div>
    <h3>Switch from Shaping Argmax to Safety Vetoes</h3>
    <p>Physics twins should preserve <code>A^(0)</code> by default unless an explicit hazard (collision, tilt, drop, slip) triggers, and be evaluated on dynamics-critical regimes where geometry fails.</p>
  </div>
</div>

---

## Citation & Artifacts {#citation}

For the underlying evaluation methodology and baseline comparison checklist used throughout this study, see the [WAM evaluation discipline](wam-research-notes.md) and the standalone [Interactive Explorer](assets/animations/newton_pi0_postmortem.html).

<div class="np-bib-wrap">
  <div class="np-bib-head">
    <span>BibTeX Citation</span>
    <button type="button" class="np-btn" id="np-copy-bib">Copy BibTeX</button>
  </div>
  <div class="np-bib-body">
<pre style="margin:0;background:transparent;border:none;padding:0;font-family:var(--md-code-font-family);"><code>@misc{isaac009_newton_pi0_postmortem_2026,
  title  = {Case Study: Debugging $\pi_0$ and Physics-Based Action Selection in Project Newton},
  author = {RL-VLA-WAM Robot Learning Course Contributors},
  year   = {2026},
  url    = {https://isaac009.github.io/RL-VLA-WAM-Robot_learning-PhysicalAI/newton-pi0-postmortem/}
}</code></pre>
  </div>
</div>

<script>
(function () {
  var METHODS = [
    { name: "nominal_pi0", group: "matched", overall: [20, 25], fixed: [5, 5], indist: [8, 10], tight: [7, 10], color: "#047857" },
    { name: "flow_geom_est", group: "matched", overall: [19, 25], fixed: [5, 5], indist: [7, 10], tight: [7, 10], color: "#64748b" },
    { name: "flow_phys_est", group: "matched", overall: [18, 25], fixed: [5, 5], indist: [7, 10], tight: [7, 10], color: "#0284c7" },
    { name: "anchored_geom_est", group: "matched", overall: [17, 25], fixed: [4, 5], indist: [6, 10], tight: [7, 10], color: "#64748b" },
    { name: "anchored_phys_est", group: "matched", overall: [19, 25], fixed: [5, 5], indist: [8, 10], tight: [6, 10], color: "#1d4ed8" },
    { name: "anchored_phys_oracle", group: "matched", overall: [20, 25], fixed: [5, 5], indist: [8, 10], tight: [7, 10], color: "#047857" },
    { name: "nominal_pi0_mismatch", group: "mismatch", overall: [15, 25], fixed: [4, 5], indist: [6, 10], tight: [5, 10], color: "#d97706" },
    { name: "anchored_geom_mismatch", group: "mismatch", overall: [20, 25], fixed: [5, 5], indist: [8, 10], tight: [7, 10], color: "#047857" },
    { name: "anchored_phys_single_mismatch", group: "mismatch", overall: [16, 25], fixed: [3, 5], indist: [7, 10], tight: [6, 10], color: "#d9480f" },
    { name: "anchored_phys_ensemble_nogate", group: "mismatch", overall: [17, 25], fixed: [4, 5], indist: [6, 10], tight: [7, 10], color: "#d9480f" },
    { name: "anchored_phys_ensemble_gated", group: "mismatch", overall: [17, 25], fixed: [5, 5], indist: [5, 10], tight: [7, 10], color: "#d9480f" }
  ];

  var curGroup = "all", curSplit = "overall";
  var chartEl = document.getElementById("np-bar-chart");
  function renderChart() {
    if (!chartEl) return;
    chartEl.innerHTML = "";
    METHODS.filter(function (m) { return curGroup === "all" || m.group === curGroup; }).forEach(function (m) {
      var k = m[curSplit][0], n = m[curSplit][1];
      var pct = (100 * k / n).toFixed(1);
      var row = document.createElement("div");
      row.className = "np-bar-row";
      row.innerHTML = "<div><code>" + m.name + "</code></div><div class=\"np-bar-track\"><div class=\"np-bar-fill\" style=\"width:" + pct + "%;background:" + m.color + ";\"></div></div><div><strong>" + k + "/" + n + "</strong> (" + pct + "%)</div>";
      chartEl.appendChild(row);
    });
  }
  document.querySelectorAll("[data-np-group]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll("[data-np-group]").forEach(function (b) { b.classList.remove("is-active"); });
      btn.classList.add("is-active");
      curGroup = btn.getAttribute("data-np-group");
      renderChart();
    });
  });
  document.querySelectorAll("[data-np-split]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll("[data-np-split]").forEach(function (b) { b.classList.remove("is-active"); });
      btn.classList.add("is-active");
      curSplit = btn.getAttribute("data-np-split");
      renderChart();
    });
  });
  renderChart();

  // Multi-episode rollout video switcher across the 13 recorded MP4s
  var VIDEOS = {
    unseen_tight_00: [
      { key: "nominal_pi0", label: "nominal_pi0 (S3=True, Base=0.0 mm)", file: "eval_nominal_pi0_unseen_tight_00.mp4" },
      { key: "anchored_phys_est", label: "anchored_phys_est (S3=False, graze at c6)", file: "eval_anchored_phys_est_unseen_tight_00.mp4" },
      { key: "anchored_geom_est", label: "anchored_geom_est", file: "eval_anchored_geom_est_unseen_tight_00.mp4" },
      { key: "flow_phys_est", label: "flow_phys_est", file: "eval_flow_phys_est_unseen_tight_00.mp4" },
      { key: "anchored_phys_ensemble_gated", label: "anchored_phys_ensemble_gated", file: "eval_anchored_phys_ensemble_gated_unseen_tight_00.mp4" }
    ],
    fixed_mm_ep0: [
      { key: "nominal_pi0", label: "nominal_pi0 (fixed_mm_ep0)", file: "eval_nominal_pi0_fixed_mm_ep0.mp4" },
      { key: "anchored_phys_est", label: "anchored_phys_est (fixed_mm_ep0)", file: "eval_anchored_phys_est_fixed_mm_ep0.mp4" },
      { key: "anchored_geom_est", label: "anchored_geom_est (fixed_mm_ep0)", file: "eval_anchored_geom_est_fixed_mm_ep0.mp4" },
      { key: "flow_phys_est", label: "flow_phys_est (fixed_mm_ep0)", file: "eval_flow_phys_est_fixed_mm_ep0.mp4" },
      { key: "anchored_phys_ensemble_gated", label: "anchored_phys_ensemble_gated (fixed_mm_ep0)", file: "eval_anchored_phys_ensemble_gated_fixed_mm_ep0.mp4" }
    ],
    calib_00: [
      { key: "nominal_pi0", label: "nominal_pi0 (calib_00)", file: "eval_nominal_pi0_calib_00.mp4" },
      { key: "anchored_phys_est", label: "anchored_phys_est (calib_00)", file: "eval_anchored_phys_est_calib_00.mp4" },
      { key: "anchored_geom_est", label: "anchored_geom_est (calib_00)", file: "eval_anchored_geom_est_calib_00.mp4" }
    ]
  };
  var basePath = "../assets/newton_pi0/videos/";
  var curEp = "unseen_tight_00";
  var selL = document.getElementById("np-vid-left-sel");
  var selR = document.getElementById("np-vid-right-sel");
  var vidL = document.getElementById("np-vid-left");
  var vidR = document.getElementById("np-vid-right");
  var capL = document.getElementById("np-vid-left-cap");
  var capR = document.getElementById("np-vid-right-cap");

  function syncVideoSelects() {
    if (!selL || !selR) return;
    var items = VIDEOS[curEp] || [];
    selL.innerHTML = "";
    selR.innerHTML = "";
    items.forEach(function (it, idx) {
      var oL = new Option(it.key, it.file);
      var oR = new Option(it.key, it.file);
      selL.add(oL);
      selR.add(oR);
      if (idx === 0) selL.selectedIndex = 0;
      if (idx === 1) selR.selectedIndex = 1;
    });
    updateVideos();
  }
  function updateVideos() {
    var items = VIDEOS[curEp] || [];
    var itL = items[selL.selectedIndex] || items[0];
    var itR = items[selR.selectedIndex] || items[0];
    if (itL) { vidL.src = basePath + itL.file; capL.innerHTML = "<code>" + curEp + "</code> · " + itL.label; }
    if (itR) { vidR.src = basePath + itR.file; capR.innerHTML = "<code>" + curEp + "</code> · " + itR.label; }
  }
  document.querySelectorAll("[data-np-ep]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll("[data-np-ep]").forEach(function (b) { b.classList.remove("is-active"); });
      btn.classList.add("is-active");
      curEp = btn.getAttribute("data-np-ep");
      syncVideoSelects();
    });
  });
  if (selL && selR) {
    selL.addEventListener("change", updateVideos);
    selR.addEventListener("change", updateVideos);
    syncVideoSelects();
  }
  var syncBtn = document.getElementById("np-sync-play");
  if (syncBtn && vidL && vidR) {
    syncBtn.addEventListener("click", function () {
      vidL.currentTime = 0;
      vidR.currentTime = 0;
      vidL.play().catch(function () {});
      vidR.play().catch(function () {});
    });
  }
  var copyBtn = document.getElementById("np-copy-bib");
  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      var bib = copyBtn.closest(".np-bib-wrap").querySelector("code").textContent;
      var markCopied = function () {
        copyBtn.textContent = "Copied!";
        setTimeout(function () { copyBtn.textContent = "Copy BibTeX"; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(bib).then(markCopied).catch(function () {
          var ta = document.createElement("textarea");
          ta.value = bib;
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand("copy"); } catch (e) {}
          document.body.removeChild(ta);
          markCopied();
        });
      } else {
        markCopied();
      }
    });
  }
})();
</script>
