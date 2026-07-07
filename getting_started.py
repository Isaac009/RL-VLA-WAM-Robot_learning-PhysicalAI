"""Quick start: runs the first Week 01 example.

Course code lives in `examples/`, one folder per week, so each checkpoint can
be run and read independently. This root script only exists so the very first
command in the README stays short:

    python getting_started.py

is equivalent to:

    python examples/week-01/01_random_policy.py
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

WEEK_01 = Path(__file__).resolve().parent / "examples" / "week-01"


def main() -> None:
    sys.path.insert(0, str(WEEK_01))
    runpy.run_path(str(WEEK_01 / "01_random_policy.py"), run_name="__main__")


if __name__ == "__main__":
    main()
