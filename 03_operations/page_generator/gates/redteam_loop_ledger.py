#!/usr/bin/env python3
"""
redteam_loop_ledger.py — Stage 9 red-team loop cap + net-correction ledger
==========================================================================
Change-plan item 1 (owner-approved 2026-06-30). The terminal red-team loop
(build-page Stage 9: `C3-before -> Red-Team -> C3-after -> loop if any new
CRITICAL`) was *repeat-until-clean* with NO numeric cap and NO measure of net
correction. That lets the loop (a) spin indefinitely on a CRITICAL it can't
converge, and (b) churn already-clean consumer copy while chasing findings —
breaking more good output than it fixes. This deterministic ledger closes both
holes; it is the enforcement, not a prose rule (verifier-beats-prose).

What it enforces
----------------
1. HARD CAP — at most --max-rounds red-team rounds per page (default 3). A round
   beyond the cap is a NON-CONVERGENCE ESCALATION (exit 2), never another loop.
2. CONVERGENCE — if the final allowed round still has open CRITICALs, that is
   also a non-convergence escalation (exit 2): stop, route the open CRITICALs to
   the owning agent, surface to the orchestrator.
3. NET CORRECTION = criticals_resolved - regressions_introduced. A round with
   NEGATIVE net correction (the loop broke more good copy than it fixed) FAILS
   (exit 1): revert that round's copy churn before continuing.

The loop exists to drive CRITICALs to zero, never to churn clean copy. A clean
run is: each round resolves >= the CRITICALs it opens, introduces 0 regressions,
and reaches 0 open CRITICAL within the cap.

Ledger storage
--------------
One JSON ledger per page, written next to the page JSON as
`<page>_redteam_ledger.json` (override with --ledger). Each round appends an
entry; the ledger is the artifact attached to the telemetry after-action report.

Usage
-----
  python redteam_loop_ledger.py --page <frontend.json> --round N \
      --criticals-open A --criticals-resolved B \
      --copy-fields-changed C --regressions D \
      [--max-rounds 3] [--ledger <path>] [--reset]

  python redteam_loop_ledger.py --selftest      # acceptance test

Exit codes
----------
  0 = round recorded, within cap, net correction >= 0 (continue or DONE)
  1 = negative net correction this round (broke more than fixed — revert churn)
  2 = non-convergence escalation (cap exceeded, or cap reached with open CRITICAL)
  3 = usage / load error
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_MAX_ROUNDS = 3


def _ledger_path(page_path, override):
    if override:
        return override
    d = os.path.dirname(os.path.abspath(page_path))
    base = os.path.basename(page_path)
    if base.endswith(".json"):
        base = base[: -len(".json")]
    return os.path.join(d, base + "_redteam_ledger.json")


def _load_ledger(path):
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"page": None, "max_rounds": DEFAULT_MAX_ROUNDS, "rounds": []}


def _save_ledger(path, ledger):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)


def record_round(
    ledger,
    page,
    round_no,
    criticals_open,
    criticals_resolved,
    copy_fields_changed,
    regressions,
    max_rounds,
    now_iso,
):
    """
    Pure decision function — no I/O. Returns (exit_code, status, entry).
    Kept side-effect-free so the self-test can exercise every branch.
    """
    net_correction = criticals_resolved - regressions
    entry = {
        "round": round_no,
        "ts": now_iso,
        "criticals_open": criticals_open,
        "criticals_resolved": criticals_resolved,
        "copy_fields_changed": copy_fields_changed,
        "regressions": regressions,
        "net_correction": net_correction,
    }

    # (1) HARD CAP — a round beyond the cap is an escalation, never another loop.
    if round_no > max_rounds:
        entry["status"] = "ESCALATE_CAP_EXCEEDED"
        return 2, entry["status"], entry

    # (3) NET CORRECTION — broke more good copy than it fixed.
    if net_correction < 0:
        entry["status"] = "FAIL_NEGATIVE_NET_CORRECTION"
        return 1, entry["status"], entry

    # (2) CONVERGENCE — cap reached but CRITICALs still open.
    if round_no == max_rounds and criticals_open > 0:
        entry["status"] = "ESCALATE_NONCONVERGENCE_AT_CAP"
        return 2, entry["status"], entry

    if criticals_open == 0:
        entry["status"] = "DONE_ZERO_CRITICAL"
        return 0, entry["status"], entry

    entry["status"] = "CONTINUE"
    return 0, entry["status"], entry


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Stage 9 red-team loop cap + net-correction ledger")
    ap.add_argument("--selftest", action="store_true", help="run acceptance test and exit")
    ap.add_argument("--page", help="path to the page frontend JSON under red-team")
    ap.add_argument("--round", type=int, help="1-based red-team round number")
    ap.add_argument("--criticals-open", type=int, help="open CRITICAL findings AFTER this round")
    ap.add_argument("--criticals-resolved", type=int, help="CRITICALs resolved IN this round")
    ap.add_argument("--copy-fields-changed", type=int, default=0, help="consumer copy fields edited this round")
    ap.add_argument("--regressions", type=int, default=0, help="previously-clean fields this round broke")
    ap.add_argument("--max-rounds", type=int, default=DEFAULT_MAX_ROUNDS)
    ap.add_argument("--ledger", help="ledger JSON path (default: next to --page)")
    ap.add_argument("--reset", action="store_true", help="start a fresh ledger for this page")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(_selftest())

    required = [args.page, args.round, args.criticals_open, args.criticals_resolved]
    if any(v is None for v in required):
        print("ERROR: --page, --round, --criticals-open, --criticals-resolved are required", file=sys.stderr)
        sys.exit(3)

    path = _ledger_path(args.page, args.ledger)
    ledger = {"page": args.page, "max_rounds": args.max_rounds, "rounds": []} if args.reset else _load_ledger(path)
    ledger["page"] = args.page
    ledger["max_rounds"] = args.max_rounds

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    code, status, entry = record_round(
        ledger,
        args.page,
        args.round,
        args.criticals_open,
        args.criticals_resolved,
        args.copy_fields_changed,
        args.regressions,
        args.max_rounds,
        now_iso,
    )
    ledger["rounds"].append(entry)
    ledger["final_status"] = status
    _save_ledger(path, ledger)

    print(f"[redteam-ledger] round {args.round}/{args.max_rounds} -> {status}")
    print(f"  open_CRITICAL={args.criticals_open}  resolved={args.criticals_resolved}  "
          f"copy_changed={args.copy_fields_changed}  regressions={args.regressions}  "
          f"net_correction={entry['net_correction']}")
    print(f"  ledger: {path}")
    if code == 2:
        print("  ESCALATE: stop the loop, route open CRITICALs to the owning agent, "
              "surface to the orchestrator. Do NOT run another round.", file=sys.stderr)
    elif code == 1:
        print("  FAIL: this round broke more clean copy than it fixed. Revert this "
              "round's copy churn before continuing.", file=sys.stderr)
    sys.exit(code)


def _selftest():
    now = "2026-06-30T00:00:00Z"
    cases = [
        # (round, open, resolved, changed, regressions, max, expected_code, expected_status)
        (1, 2, 3, 4, 0, 3, 0, "CONTINUE"),                       # progress, still open
        (2, 0, 2, 1, 0, 3, 0, "DONE_ZERO_CRITICAL"),             # converged within cap
        (2, 1, 1, 5, 2, 3, 1, "FAIL_NEGATIVE_NET_CORRECTION"),   # broke 2, fixed 1 -> net -1
        (3, 1, 1, 0, 0, 3, 2, "ESCALATE_NONCONVERGENCE_AT_CAP"), # cap reached, still open
        (4, 0, 1, 0, 0, 3, 2, "ESCALATE_CAP_EXCEEDED"),          # 4th round on a cap of 3
        (3, 0, 1, 0, 0, 3, 0, "DONE_ZERO_CRITICAL"),             # converges exactly at cap
    ]
    failures = []
    for i, (r, o, res, ch, reg, mx, exp_code, exp_status) in enumerate(cases):
        code, status, _ = record_round({}, "test.json", r, o, res, ch, reg, mx, now)
        if code != exp_code or status != exp_status:
            failures.append((i, (r, o, res, ch, reg, mx), f"got ({code},{status})", f"want ({exp_code},{exp_status})"))
    if failures:
        print("REDTEAM LOOP LEDGER SELFTEST: FAIL")
        for f in failures:
            print("  ", f)
        return 1
    print("REDTEAM LOOP LEDGER SELFTEST: PASS")
    print(f"  {len(cases)} cases: cap, convergence-at-cap, and negative-net-correction all enforced.")
    return 0


if __name__ == "__main__":
    main()
