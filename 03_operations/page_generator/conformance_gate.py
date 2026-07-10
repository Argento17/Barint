#!/usr/bin/env python3
"""conformance_gate.py — CI wrapper around conformance.py (TASK-560).

`conformance.py --all` exits 1 whenever ANY live shelf fails a HARD check. That is the
right behavior for a human audit, but it makes a CI job permanently red while a single
documented, cross-lane decision is pending (today: bread's v3->v4 baseline cutover,
TASK-561). A permanently-red job trains everyone to ignore it -- the exact failure mode
that got argento_bari_ci.yml deleted.

So this gate is PROTECTIVE, not permissive. It mirrors the shadow/gold gates: block on a
REGRESSION, never on a documented standing state. Specifically it FAILS when

  * a shelf is non-conforming and is NOT in conformance_exceptions.json      (regression)
  * an excepted shelf fails DIFFERENT hard checks than the ones recorded     (regression)
  * an excepted shelf now conforms -> the entry is stale and must be deleted (anti-zombie)

An exception can therefore never rot into a silent permanent bypass, and a genuinely new
non-conformer still turns the job red. Every standing exception is printed on every run,
so nothing is dropped quietly.

Exit codes:  0 = clean (or only documented exceptions)
             1 = regression / stale exception -> fix before merge
             2 = harness error (conformance.py unrunnable, bad exceptions file)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
CONFORMANCE = THIS_DIR / "conformance.py"
EXCEPTIONS = THIS_DIR / "conformance_exceptions.json"


def load_exceptions() -> dict[str, dict]:
    if not EXCEPTIONS.is_file():
        return {}
    try:
        # utf-8-sig: agent-written JSON in this repo sometimes carries a BOM.
        data = json.loads(EXCEPTIONS.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        print(f"error: cannot parse {EXCEPTIONS.name}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    return data.get("exceptions", {})


def run_conformance() -> list[dict]:
    proc = subprocess.run(
        [sys.executable, str(CONFORMANCE), "--all", "--json"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    # conformance exits 1 when any shelf fails; that is data, not an error. Only a
    # missing/soft-broken harness (exit 2/3) or unparseable output is fatal here.
    if proc.returncode not in (0, 1) or not proc.stdout.strip():
        print(f"error: conformance.py exited {proc.returncode}", file=sys.stderr)
        print(proc.stderr[:2000], file=sys.stderr)
        raise SystemExit(2)
    try:
        return json.loads(proc.stdout)["results"]
    except Exception as exc:  # noqa: BLE001
        print(f"error: cannot parse conformance --json output: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


def main() -> int:
    exceptions = load_exceptions()
    results = run_conformance()

    by_stem = {r["stem"]: r for r in results}
    nonconforming = {r["stem"]: sorted(r.get("hard_failures") or []) for r in results
                     if not r["conforms"]}

    regressions: list[str] = []
    drifted: list[str] = []
    stale: list[str] = []

    for stem, failures in sorted(nonconforming.items()):
        if stem not in exceptions:
            regressions.append(f"{stem}: {', '.join(failures)}")
            continue
        recorded = sorted(exceptions[stem].get("hard_failures") or [])
        if failures != recorded:
            drifted.append(
                f"{stem}: now fails {failures}, exception records {recorded} "
                f"({exceptions[stem].get('task', 'no task')})")

    for stem, entry in sorted(exceptions.items()):
        if stem not in by_stem:
            stale.append(f"{stem}: no longer a live shelf -- delete the exception")
        elif by_stem[stem]["conforms"]:
            stale.append(f"{stem}: now CONFORMS -- delete the exception "
                         f"({entry.get('task', 'no task')} is done)")

    total = len(results)
    ok = sum(1 for r in results if r["conforms"])
    print(f"conformance: {ok}/{total} shelves conform.")

    if exceptions:
        print("\nDocumented standing exceptions (still enforced, never silent):")
        for stem, entry in sorted(exceptions.items()):
            state = "FAILING as recorded" if stem in nonconforming else "conforms"
            print(f"  - {stem:12s} [{state}]  {entry.get('task', '?')} "
                  f"({entry.get('owner', '?')})")
            reason = " ".join((entry.get("reason") or "").split())
            print(f"      {reason[:160]}{'...' if len(reason) > 160 else ''}")

    rc = 0
    if regressions:
        rc = 1
        print("\n::error::CONFORMANCE REGRESSION -- undocumented non-conforming shelf/shelves:")
        for r in regressions:
            print(f"  {r}")
        print("  A score-flip would leave these stale. Fix the shelf, or record a "
              "documented exception with an owning task in conformance_exceptions.json.")
    if drifted:
        rc = 1
        print("\n::error::EXCEPTION DRIFT -- an excepted shelf fails different checks than recorded:")
        for d in drifted:
            print(f"  {d}")
    if stale:
        rc = 1
        print("\n::error::STALE EXCEPTION -- delete these entries from conformance_exceptions.json:")
        for s in stale:
            print(f"  {s}")

    if rc == 0:
        print("\nGate PASS: no regression; only documented exceptions remain.")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
