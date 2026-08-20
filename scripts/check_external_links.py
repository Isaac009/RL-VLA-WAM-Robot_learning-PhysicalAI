"""Report Markdown links that are definitively missing.

The checker fails on HTTP 404 and 410. Authentication, rate limiting, and
transient server failures are reported as warnings so a third-party outage
does not block the course deployment.
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"\]\((https?://[^)\s]+)\)")
MISSING_CODES = {404, 410}
LOCAL_REPO_PREFIX = (
    "https://github.com/Isaac009/"
    "RL-VLA-WAM-Robot_learning-PhysicalAI/tree/main/"
)


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in REPO_ROOT.rglob("*.md")
        if ".git" not in path.parts and "site" not in path.parts
    )


def discover_links() -> dict[str, list[str]]:
    locations: dict[str, list[str]] = {}
    for path in markdown_files():
        relative = path.relative_to(REPO_ROOT)
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            for url in LINK_PATTERN.findall(line):
                locations.setdefault(url, []).append(
                    f"{relative}:{line_number}"
                )
    return locations


def check(url: str) -> tuple[str, int | str]:
    if url.startswith(LOCAL_REPO_PREFIX):
        local_target = REPO_ROOT / url.removeprefix(LOCAL_REPO_PREFIX)
        return (
            ("ok", "local")
            if local_target.exists()
            else ("missing", "local")
        )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "RL-course-link-checker/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return "ok", response.status
    except urllib.error.HTTPError as error:
        if error.code in MISSING_CODES:
            return "missing", error.code
        return "warning", error.code
    except (urllib.error.URLError, TimeoutError) as error:
        detail = error.reason if hasattr(error, "reason") else error
        return "warning", str(detail)


def main() -> int:
    missing = 0
    links = discover_links()
    print(f"Checking {len(links)} unique external Markdown links")

    for url, locations in links.items():
        status, detail = check(url)
        print(f"{status.upper():<7} {detail!s:<8} {url}")
        if status == "missing":
            missing += 1
            print(f"         referenced by {', '.join(locations)}")

    if missing:
        print(f"\nFound {missing} definitively missing link(s).")
        return 1

    print("\nNo HTTP 404 or 410 links found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
