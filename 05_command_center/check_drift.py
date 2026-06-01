#!/usr/bin/env python3
"""
Bari Command Center v3 — Drift Watchdog
=======================================

The lightweight companion to generate_dashboard.py. It does NOT regenerate the
dashboard; it re-evaluates the three drift conditions against the *currently
served* command_center.json and refreshes only the drift alerts (+ meta), so the
served view stays honest between full regenerations.

This is what answers the TASK-084 success criterion: if a deliverable for
TASK-075 appears and nobody updates a registry file, running this (manually, on a
file-watch hook, or on a cron) flags the inconsistency automatically.

Drift conditions (shared with the generator via build_drift_alerts):
    1. PHANTOM_TASK   — deliverable references a task ID with no tasks/TASK-*.md
    2. CLOSURE_DRIFT  — registry task still open, but a deliverable authored by it exists
    3. SNAPSHOT_DRIFT — a source file is newer than command_center.json
    4. REGISTRY_UNPARSEABLE — a TASK-*.md exists but has no parseable frontmatter

Usage:
    cd C:\\Bari\\05_command_center
    python check_drift.py            # refresh drift alerts in command_center.json
    python check_drift.py --quiet    # same, machine-readable summary only

Exit codes (so it can gate a pre-commit / CI hook):
    0  no drift
    1  drift detected (alerts written)
    2  command_center.json missing — run generate_dashboard.py first
"""

import json
import sys
from datetime import datetime

import generate_dashboard as gd


def check(quiet=False):
    out = gd.OUTPUT_FILE
    if not out.exists():
        print("command_center.json not found — run generate_dashboard.py first.")
        return 2

    dashboard = json.loads(out.read_text(encoding="utf-8"))
    ref_mtime = out.stat().st_mtime

    tasks, unparseable = gd.load_tasks()
    registry_ids = {t["id"] for t in tasks} | {u["id"] for u in unparseable}
    returns      = gd.scan_task_returns()

    drift = gd.build_drift_alerts(tasks, returns, registry_ids, unparseable, ref_mtime=ref_mtime)

    # Preserve operational (non-drift) alerts; replace the drift ones with fresh.
    kept = [a for a in dashboard.get("alerts", []) if a.get("type") not in gd.DRIFT_TYPES]
    dashboard["alerts"] = gd.finalize_alerts(kept + drift)
    dashboard["drift"] = gd.summarize_drift(drift)

    # Freshness verdict (TASK-092 finding #1): set the stale flag the HTML banner
    # reads, so a stale snapshot can never be served silently.
    now = datetime.now().isoformat(timespec="seconds")
    meta = dashboard.setdefault("meta", {})
    meta["drift_checked_at"] = now
    snap_alert = next((a for a in drift if a["type"] == "SNAPSHOT_DRIFT"), None)
    meta["stale"] = bool(snap_alert)
    meta["stale_reason"] = snap_alert["message"] if snap_alert else None

    out.write_text(json.dumps(dashboard, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = dashboard["drift"]["counts"]
    if quiet:
        print(json.dumps({"clean": dashboard["drift"]["clean"], "counts": counts}))
    else:
        if dashboard["drift"]["clean"]:
            print("drift check: CLEAN — registry and deliverables agree, snapshot fresh.")
        else:
            print(f"drift check: {len(drift)} condition(s) detected")
            for a in sorted(drift, key=lambda x: gd.SEV_ORDER.get(x['severity'], 9)):
                print(f"  ! [{a['severity']}] {a['type']}: {a['message']}")
            print(f"  summary: phantom={counts['PHANTOM_TASK']} "
                  f"closure={counts['CLOSURE_DRIFT']} snapshot={counts['SNAPSHOT_DRIFT']} "
                  f"unparseable={counts.get('REGISTRY_UNPARSEABLE', 0)}")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(check(quiet="--quiet" in sys.argv))
