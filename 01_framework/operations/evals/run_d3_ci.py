#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_d3_ci.py — Deliverable 3 consolidated CI runner
TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1

Runs every D3 gate plus the existing deterministic regression suites and
aggregates pass/fail. Any failure -> non-zero exit (CI red).

Gates:
  1. run_copy_golden_diff.py        (verified deterministic copy only)
  2. run_schema_validation_gate.py  (D3b — schema validity >= 98%)
  3. run_pairwise_review_gate.py    (D3b — pairwise verdict ledger + unsafe-wording scan)
  4. run_cls06_check.py             (closure false-close negative control)
  5. check_llm_import_tripwire.py   (no unregistered LLM import outside .venv)
  6. run_router_regression.py       (EXISTING — must stay green)
  7. run_regression_check.py        (EXISTING — must stay green)
"""
import sys, io, subprocess
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"

GATES = [
    ("copy_golden_diff",    [sys.executable, str(HERE / "run_copy_golden_diff.py")], HERE),
    ("schema_validation",   [sys.executable, str(HERE / "run_schema_validation_gate.py")], HERE),   # D3b
    ("pairwise_review",     [sys.executable, str(HERE / "run_pairwise_review_gate.py")], HERE),      # D3b
    ("cls06_negative_ctrl", [sys.executable, str(HERE / "run_cls06_check.py")], HERE),
    ("llm_import_tripwire", [sys.executable, str(HERE / "check_llm_import_tripwire.py")], HERE),
    ("router_regression",   [sys.executable, str(SRC / "run_router_regression.py")], SRC),
    ("regression_check",    [sys.executable, str(SRC / "run_regression_check.py")], SRC),
]


def main():
    results = []
    for name, cmd, cwd in GATES:
        print(f"\n===== {name} =====")
        proc = subprocess.run(cmd, cwd=str(cwd))
        results.append((name, proc.returncode))
    print("\n" + "=" * 60)
    failed = [n for n, rc in results if rc != 0]
    for n, rc in results:
        print(f"  {'PASS' if rc == 0 else 'FAIL'}  {n}  (exit {rc})")
    print("=" * 60)
    if failed:
        print(f"D3 CI: FAIL -> {failed}")
        return 1
    print("D3 CI: ALL GREEN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
