"""Smoke tests for learner-facing course entry points."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_OUTPUT = {
    "getting_started.py": "Episode return: -0.20",
    "examples/week-01/01_random_policy.py": "Episode return: -0.20",
    "examples/week-01/02_baseline_policy.py": "always right          0.97",
    "examples/week-02/01_q_table_intro.py": "terminal state",
    "examples/week-02/02_q_learning_update.py": "Q[2][right] = 0.22",
    "examples/week-02/03_train_q_learning.py": "q-learning            0.97",
    "examples/week-03/01_bellman_error.py": (
        "half-squared optimization loss: 0.0578"
    ),
    "examples/week-03/02_gradient_step.py": (
        "half-squared optimization loss: 0.0081"
    ),
    "examples/week-03/03_train_linear_q.py": "linear-q              0.97",
    "examples/week-04/01_replay_buffer.py": (
        "does not\nprove that replay data are truly i.i.d."
    ),
    "examples/week-04/02_target_network_ablation.py": (
        "delayed target: 0.006766"
    ),
    "examples/week-04/03_dqn_stabilizers.py": (
        "LineWorld is too easy to demonstrate a stabilizer advantage."
    ),
}


class CourseExampleSmokeTests(unittest.TestCase):
    @staticmethod
    def run_script(script: str, cwd: Path) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, script],
            cwd=cwd,
            env=environment,
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )

    def test_every_checkpoint_runs_with_expected_output(self) -> None:
        for relative_path, expected in EXPECTED_OUTPUT.items():
            with self.subTest(script=relative_path):
                completed = self.run_script(relative_path, REPO_ROOT)
                self.assertIn(expected, completed.stdout)

    def test_week_checkpoints_also_run_inside_their_folders(self) -> None:
        for relative_path, expected in EXPECTED_OUTPUT.items():
            if not relative_path.startswith("examples/"):
                continue
            path = REPO_ROOT / relative_path
            with self.subTest(script=relative_path):
                completed = self.run_script(path.name, path.parent)
                self.assertIn(expected, completed.stdout)


if __name__ == "__main__":
    unittest.main()
