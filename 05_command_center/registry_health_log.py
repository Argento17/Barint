#!/usr/bin/env python3
"""
Bari Command Center — Registry Health Time-Series + Degradation Alerts
======================================================================

CC sees the registry as a *snapshot* (command_center_live.json). What it could not see
was the *trend*: is the board getting healthier or sicker over time? Blocked count
creeping up, WIP breaching the limit, RETURNED/CHANGES_REQUESTED accumulating, alerts
multiplying, drift reappearing — each is invisible in any single read. This tool appends a
compact health snapshot to an append-only log every time it runs, then diffs the last two
to raise **degradation alerts**.

It also folds in a *ground-truth* signal via the GitHub artifact verifier
(integrations.clients.github_artifacts): if CI is failing on the default branch, that's a
registry-health problem CC should surface even when the task board looks clean.

Read-only against the dashboard (never edits command_center*.json). The only thing it
writes is its own append-only log.

Usage:
    python registry_health_log.py            # snapshot + append + print degradation report
    python registry_health_log.py --check     # diff only, do NOT append (dry run)
    python registry_health_log.py --history    # print the full recorded series
    python registry_health_log.py --no-gh      # skip the CI/GitHub probe (offline)

Log file (append-only JSONL): 05_command_center/registry_health_log.jsonl
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Interpreter guard — match generate_dashboard.py so PyYAML/deps + the integrations
# package resolve under the project venv regardless of which Python invoked us.
_VENV_PY = Path(r"C:\Bari") / ".venv" / "Scripts" / ("python.exe" if os.name == "nt" else "python")
if _VENV_PY.exists() and Path(sys.executable).resolve() != _VENV_PY.resolve():
    os.execv(str(_VENV_PY), [str(_VENV_PY), os.path.abspath(__file__), *sys.argv[1:]])

import json
from datetime import datetime, timezone

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

LIVE = _ROOT / "05_command_center" / "command_center_live.json"
LOG = _ROOT / "05_command_center" / "registry_health_log.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def snapshot(include_gh: bool = True) -> dict:
    """Build a compact health snapshot from the live dashboard (+ optional CI probe)."""
    data = json.loads(LIVE.read_text(encoding="utf-8"))
    ts = data.get("task_summary", {})
    drift = data.get("drift", {})
    drift_count = (
        drift.get("count")
        if isinstance(drift.get("count"), int)
        else len(drift.get("items", []) if isinstance(drift.get("items"), list) else [])
    )
    snap = {
        "at": _now(),
        "active": ts.get("active", 0),
        "in_progress": ts.get("in_progress", 0),
        "blocked": ts.get("blocked", 0),
        "returned": ts.get("returned", 0),
        "changes_requested": ts.get("changes_requested", 0),
        "closed": ts.get("closed", 0),
        "wip": ts.get("wip", 0),
        "wip_over_limit": len(ts.get("wip_over_limit", []) or []),
        "alerts": len(data.get("alerts", []) or []),
        "drift": drift_count or 0,
        "open_tasks": len(data.get("open_tasks", []) or []),
    }
    snap["ci"] = _ci_probe() if include_gh else {"skipped": True}
    return snap


def _ci_probe() -> dict:
    """Latest CI conclusion on the default branch. Honest tri-state: `available=False` means
    BLIND (gh missing/unauthed) — NOT 'CI passed'; `available=True, found=False` means no
    runs; otherwise the real conclusion. Degradation logic only alarms on a real failure."""
    try:
        from integrations.clients.github_artifacts import ci_status
        st = ci_status()  # self-guards gh availability and returns an `available` flag
        return {"available": st.get("available", False),
                "found": st.get("found"),
                "reason": st.get("reason"),
                "status": st.get("status"),
                "conclusion": st.get("conclusion"),
                "workflow": st.get("workflowName")}
    except Exception as e:  # noqa: BLE001 — CC never crashes on a probe
        return {"available": False, "error": f"{type(e).__name__}: {e}"}


def history() -> list[dict]:
    if not LOG.exists():
        return []
    out = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def append(snap: dict) -> None:
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(snap, ensure_ascii=False) + "\n")


# Metrics where an INCREASE since the previous snapshot is a degradation.
_WORSE_IF_UP = {
    "blocked": "BLOCKED tasks rose",
    "returned": "RETURNED tasks rose",
    "changes_requested": "CHANGES_REQUESTED tasks rose",
    "wip_over_limit": "owners breaching WIP limit rose",
    "alerts": "dashboard alerts rose",
    "drift": "registry/deliverable drift rose",
}


def degradation_report(curr: dict, prev: dict | None) -> list[str]:
    """Compare current vs previous snapshot; return human-readable degradation lines."""
    alerts: list[str] = []
    # CI is a degradation regardless of trend.
    ci = curr.get("ci", {})
    if ci.get("available") and ci.get("conclusion") not in (None, "success", "skipped"):
        alerts.append(f"CI FAILING on default branch: {ci.get('workflow')} "
                      f"-> {ci.get('conclusion')}")
    if prev is None:
        return alerts
    for key, label in _WORSE_IF_UP.items():
        delta = curr.get(key, 0) - prev.get(key, 0)
        if delta > 0:
            alerts.append(f"{label}: {prev.get(key, 0)} -> {curr.get(key, 0)} (+{delta})")
    # closed going backwards = a reopen/regression worth noting
    if curr.get("closed", 0) < prev.get("closed", 0):
        alerts.append(f"CLOSED count dropped: {prev['closed']} -> {curr['closed']} "
                      f"(task reopened/regressed)")
    return alerts


def main() -> int:
    args = set(sys.argv[1:])
    if "--history" in args:
        for s in history():
            print(f"{s['at']}  active={s.get('active')} blocked={s.get('blocked')} "
                  f"wip={s.get('wip')} alerts={s.get('alerts')} drift={s.get('drift')} "
                  f"closed={s.get('closed')}")
        return 0

    curr = snapshot(include_gh="--no-gh" not in args)
    prev = (history() or [None])[-1]
    report = degradation_report(curr, prev)

    print("Registry health snapshot @", curr["at"])
    print(f"  active={curr['active']}  in_progress={curr['in_progress']}  "
          f"blocked={curr['blocked']}  returned={curr['returned']}  "
          f"changes_requested={curr['changes_requested']}  wip={curr['wip']}")
    print(f"  alerts={curr['alerts']}  drift={curr['drift']}  closed={curr['closed']}  "
          f"ci={curr['ci'].get('conclusion') or curr['ci'].get('available')}")

    if report:
        print("\n  DEGRADATION SINCE LAST SNAPSHOT:")
        for line in report:
            print(f"    ! {line}")
    elif prev is not None:
        print("\n  No degradation since last snapshot.")

    if "--check" in args:
        print("\n(--check: dry run, snapshot NOT appended)")
    else:
        append(curr)
        print(f"\n  appended -> {LOG.name} ({len(history())} snapshots on record)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
