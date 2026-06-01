#!/usr/bin/env python3
"""
structure_guard.py — Monorepo layout invariants (TASK-131 → TASK-134)
=====================================================================

TASK-131 split the Agent OS and the website into two homes. TASK-134 (2026-06-01)
reversed that into a single monorepo: the website was folded into the Agent OS repo
as a git subtree under ``bari-web/``. This watchdog asserts the consolidated layout
so the old confusion (or a stray duplicate) cannot silently return:

  1. Agent OS lives at C:\\Bari and is a git repo.
  2. The website lives INSIDE the repo at C:\\Bari\\bari-web (package.json + src/).
  3. No leftover standalone C:\\bari-web (it was consolidated into the monorepo).
  4. The old colliding path C:\\Users\\HP\\bari no longer exists.
  5. No nested Agent-OS snapshot inside the website (no C:\\Bari\\bari-web\\Bari).
  6. node_modules under the website is NOT tracked by git.

This is a layout watchdog, intentionally separate from check_drift.py (which
watches registry/deliverable drift). Wire it into a pre-commit/CI hook if desired.

Usage:
    python structure_guard.py            # human-readable
    python structure_guard.py --quiet    # one-line machine summary

Exit codes:  0 = clean   1 = one or more invariants violated
"""

import subprocess
import sys
from pathlib import Path

AGENT_OS = Path(r"C:\Bari")
WEBSITE = AGENT_OS / "bari-web"
OLD_WEBSITE = Path(r"C:\bari-web")
OLD_COLLIDING = Path(r"C:\Users\HP\bari")


def check():
    violations = []

    if not AGENT_OS.is_dir():
        violations.append(f"Agent OS missing: {AGENT_OS}")
    elif not (AGENT_OS / ".git").is_dir():
        violations.append(f"Agent OS is not a git repo: {AGENT_OS}")

    if not WEBSITE.is_dir():
        violations.append(f"Website missing at expected path: {WEBSITE}")
    else:
        if not (WEBSITE / "package.json").is_file():
            violations.append(f"Website looks incomplete (no package.json): {WEBSITE}")
        if not (WEBSITE / "src").is_dir():
            violations.append(f"Website looks incomplete (no src/): {WEBSITE}")

    if OLD_WEBSITE.exists():
        violations.append(
            f"Leftover standalone website still exists: {OLD_WEBSITE} "
            "(should be consolidated into C:\\Bari\\bari-web and removed)"
        )

    if OLD_COLLIDING.exists():
        violations.append(f"Old colliding path still exists: {OLD_COLLIDING}")

    if (WEBSITE / "Bari").exists():
        violations.append(f"Agent-OS snapshot re-appeared inside website: {WEBSITE / 'Bari'}")

    # node_modules must never be tracked.
    if (AGENT_OS / ".git").is_dir():
        try:
            tracked = subprocess.run(
                ["git", "-C", str(AGENT_OS), "ls-files", "bari-web/node_modules/"],
                capture_output=True, text=True, timeout=30,
            ).stdout.strip()
            if tracked:
                violations.append("bari-web/node_modules is tracked by git (must be gitignored)")
        except Exception:
            pass  # git not available — skip this check rather than false-flag

    return violations


def main():
    quiet = "--quiet" in sys.argv
    violations = check()
    if quiet:
        print(f"{{\"clean\": {str(not violations).lower()}, \"violations\": {len(violations)}}}")
    elif violations:
        print(f"structure guard: {len(violations)} violation(s)")
        for v in violations:
            print(f"  ! {v}")
    else:
        print("structure guard: CLEAN — monorepo layout intact (C:\\Bari + C:\\Bari\\bari-web).")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
