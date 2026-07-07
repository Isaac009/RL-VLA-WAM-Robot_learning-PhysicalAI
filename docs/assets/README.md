# Course Assets Status

This directory contains the visual assets (diagrams and animations) generated for the RL Mini-Course.

## Status Tracking

| Week | Concept | Format | Status | Location | Review note |
|------|---------|--------|--------|----------|-------------|
| 1 | MDP Loop | SVG | **reviewed** | [`images/week1_mdp_loop.svg`](images/week1_mdp_loop.svg) | Ready for Week 1 lecture/lab. |
| 2 | Q-Table Heatmap | HTML | **reviewed** | [`animations/week2_q_table.html`](animations/week2_q_table.html) | Aligned with LineWorld and tabular Q-learning. |
| 3 | Bellman Target | HTML | **reviewed** | [`animations/week3_bellman_target.html`](animations/week3_bellman_target.html) | Ready for DQN/Bellman-error lesson. |
| 4 | Replay Buffer | HTML | *v0 placeholder* | [`animations/week4_replay_buffer.html`](animations/week4_replay_buffer.html) | Structural placeholder only; needs real animation. |
| 5 | Policy Gradient | HTML | *v0 placeholder* | [`animations/week5_policy_gradient.html`](animations/week5_policy_gradient.html) | Structural placeholder only; needs distribution shift. |
| 6 | Actor-Critic | SVG | *v0 placeholder* | [`images/week6_actor_critic.svg`](images/week6_actor_critic.svg) | Placeholder only; needs actor/critic panels. |
| 7 | PPO Clip | SVG | *v0 placeholder* | [`images/week7_ppo_clip.svg`](images/week7_ppo_clip.svg) | Placeholder only; needs clipped/unclipped plot. |
| 8 | Robot Reaching MDP | SVG | *v0 placeholder* | [`images/week8_robot_mdp.svg`](images/week8_robot_mdp.svg) | Placeholder only; needs robot state/action/reward layout. |
| 9 | VLA Flow | SVG | *v0 placeholder* | [`images/week9_vla_flow.svg`](images/week9_vla_flow.svg) | Placeholder only; needs image/language/action flow. |
| 10 | WAM Storyboard | SVG | *v0 placeholder* | [`images/week10_wam_storyboard.svg`](images/week10_wam_storyboard.svg) | Placeholder only; needs multi-panel future prediction storyboard. |

**Status Definitions:**
- `v0 placeholder`: Draft file exists, but the teaching content is not complete.
- `reviewed`: Polished to teaching quality. Ready for use in lessons.
- `needs revision`: Feedback received, waiting for updates.

## Instructor Review Notes

- Weeks 1-3 are acceptable for use in the first course pass.
- Weeks 4-10 should not be presented as final teaching diagrams yet.
- All SVG assets should retain `<title>`, `<desc>`, `role="img"`, `aria-labelledby`, and a stable `viewBox`.
- All HTML animations should remain self-contained and respect `prefers-reduced-motion`.
