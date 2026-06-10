#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_cls06_check.py — Deliverable 3 (TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1)

Closure-verification NEGATIVE CONTROL. Reads the synthetic fixture
fixtures/cls06_returned_fixture.md (which lives OUTSIDE tasks/ so it is never
treated as a real task), verifies each DoD item claimed `done` against its
artifact at file level, and asserts the correct decision is RETURNED — NOT CLOSED.

A verifier that would CLOSE this fixture has committed a false-close; this check
fails loudly in that case.

Exit 0 = decision == gold (RETURNED) and != CLOSED. Non-zero otherwise.
"""
import sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    import yaml
except ImportError:
    print("PyYAML required"); sys.exit(2)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FIXTURE = HERE / "fixtures" / "cls06_returned_fixture.md"


def parse_frontmatter(text):
    if not text.startswith("---"):
        raise ValueError("no frontmatter")
    end = text.index("\n---", 3)
    return yaml.safe_load(text[3:end])


def verify(fm):
    """Decide CLOSED vs RETURNED by checking each done-claimed artifact at file level."""
    unmet = []
    for item in fm.get("dod", []):
        if item.get("claim") == "done":
            artifact = REPO / item["artifact"]
            if not artifact.exists():
                unmet.append(item["id"])
    decision = "CLOSED" if not unmet else "RETURNED"
    return decision, unmet


def main():
    if not FIXTURE.exists():
        print(f"FAIL: fixture missing at {FIXTURE}"); return 1
    fm = parse_frontmatter(FIXTURE.read_text(encoding="utf-8"))
    gold = fm.get("gold_decision")
    decision, unmet = verify(fm)
    print(f"fixture claimed_status : {fm.get('claimed_status')}")
    print(f"unmet DoD items (artifact missing): {unmet}")
    print(f"verifier decision      : {decision}")
    print(f"gold decision          : {gold}")
    ok = (decision == gold) and (decision != "CLOSED")
    print("-" * 50)
    if ok:
        print("PASS: negative control held — false-close correctly prevented (RETURNED).")
        return 0
    print("FAIL: verifier did not return the gold decision (possible false-close).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
