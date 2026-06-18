#!/usr/bin/env python3
"""
Bari Agent Performance Scorecard
=================================
Aggregates per-agent quality metrics from the task registry (C:\\Bari\\tasks\\TASK-*.md).
Follows Anthropic's multi-agent observability guidance: measure first-pass quality,
rework rate, cycle time, and verification accuracy — not just throughput.

Usage:
    python generate_scorecard.py              # print scorecard to stdout
    python generate_scorecard.py --json       # machine-readable JSON
    python generate_scorecard.py --save       # write agent_scorecard.json + print
    python generate_scorecard.py --digest     # one-paragraph summary per agent

Metrics computed:
    tasks_total          All tasks owned by the agent (any status)
    tasks_closed         CLOSED tasks
    tasks_in_progress    IN_PROGRESS tasks
    tasks_blocked        BLOCKED tasks
    tasks_returned       RETURNED tasks
    tasks_changes_req    CHANGES_REQUESTED tasks (open rework cycles)
    first_pass_rate      % closed tasks that have NO rework evidence (no cc_comments
                         with flag:verify/blocker, no CHANGES_REQUESTED history)
    cc_verified_rate     % of CLOSED tasks that have cc_reviewed set (CC validated)
    roadmap_tasks        tasks with roadmap_impact: true
    avg_cycle_days       mean days from created_at → completed_at (closed tasks only)
    p50_cycle_days       median cycle time
    claim_accuracy       % of verified closes where cc_comments raised NO flag:verify
                         or flag:blocker findings (proxy for return-block accuracy)
    health_score         Composite 0–100: (first_pass×0.4 + cc_verified×0.3 + claim_accuracy×0.3)
    trend_30d            health_score over the last 30 days vs. overall (directional)
"""

import json
import re
import sys
import argparse
from pathlib import Path
from datetime import date, datetime, timedelta
from statistics import mean, median

# ── Venv guard ────────────────────────────────────────────────────────────────
import os
_VENV_PY = Path(r"C:\Bari") / ".venv" / "Scripts" / ("python.exe" if os.name == "nt" else "python")
if _VENV_PY.exists() and Path(sys.executable).resolve() != _VENV_PY.resolve():
    os.execv(str(_VENV_PY), [str(_VENV_PY), os.path.abspath(__file__), *sys.argv[1:]])

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML required: C:\\Bari\\.venv\\Scripts\\python.exe -m pip install pyyaml")

# ── Paths ─────────────────────────────────────────────────────────────────────
BARI_ROOT  = Path(r"C:\Bari")
TASKS_DIR  = BARI_ROOT / "tasks"
HERE       = Path(__file__).resolve().parent
OUTPUT_FILE = HERE / "agent_scorecard.json"

VALID_STATUSES = {"IN_PROGRESS", "BLOCKED", "RETURNED", "CHANGES_REQUESTED", "CLOSED"}

# Agents whose tasks to include in the scorecard
KNOWN_AGENTS = [
    "cc-agent", "product-agent", "nutrition-agent", "data-agent",
    "frontend-agent", "design-agent", "qa-agent", "content-agent",
    "marketing-agent", "research-agent", "red-team-agent",
]


# ── Task parser ───────────────────────────────────────────────────────────────

def parse_task(path: Path) -> dict | None:
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"(?s)^---\s*\n(.*?)\n---\s*\n(.*)", raw)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    fm["_body"] = m.group(2)
    fm["_path"] = str(path)
    return fm


def parse_date(val) -> date | None:
    if val is None:
        return None
    try:
        if isinstance(val, (date, datetime)):
            return val if isinstance(val, date) else val.date()
        return date.fromisoformat(str(val).strip())
    except (ValueError, AttributeError):
        return None


def has_rework_evidence(task: dict) -> bool:
    """True if the task shows signs of a rework cycle."""
    body = task.get("_body", "")
    # Explicit CHANGES_REQUESTED in status history (mentioned in body)
    if "CHANGES_REQUESTED" in body:
        return True
    # cc_comments with flag:verify or flag:blocker (signifies CC found a gap)
    cc = str(task.get("cc_comments", "") or "")
    if "flag:verify" in cc or "flag:blocker" in cc:
        return True
    # close_reason that mentions "gap", "missing", "not found", "contradicts"
    cr = str(task.get("close_reason", "") or "").lower()
    if any(w in cr for w in ("gap", "missing field", "not found", "contradicts", "changes_requested")):
        return True
    return False


def claim_accuracy_ok(task: dict) -> bool:
    """True if no CC verification flag was raised on this task's close."""
    cc = str(task.get("cc_comments", "") or "")
    cr = str(task.get("close_reason", "") or "").lower()
    # A flag:verify means CC found a discrepancy; flag:blocker means a blocker surfaced
    if "flag:verify" in cc or "flag:blocker" in cc:
        return False
    # close_reason should not mention CHANGES_REQUESTED
    if "changes_requested" in cr:
        return False
    return True


# ── Scorecard builder ─────────────────────────────────────────────────────────

def build_agent_scorecard(tasks: list[dict], cutoff_days: int = 30) -> dict:
    today = date.today()
    cutoff = today - timedelta(days=cutoff_days)

    by_agent: dict[str, list[dict]] = {a: [] for a in KNOWN_AGENTS}
    unrouted = []

    for t in tasks:
        owner = str(t.get("owner", "")).strip()
        if owner in by_agent:
            by_agent[owner].append(t)
        else:
            unrouted.append(t)

    scorecard = {}
    for agent, agent_tasks in by_agent.items():
        if not agent_tasks:
            scorecard[agent] = _empty_metrics(agent)
            continue
        scorecard[agent] = _compute_metrics(agent, agent_tasks, cutoff)

    scorecard["_unrouted"] = {
        "agent": "_unrouted",
        "note": "Tasks with unknown or missing owner",
        "tasks_total": len(unrouted),
        "task_ids": [t.get("id", "?") for t in unrouted],
    }

    return scorecard


def _empty_metrics(agent: str) -> dict:
    return {
        "agent": agent,
        "tasks_total": 0,
        "tasks_closed": 0,
        "tasks_in_progress": 0,
        "tasks_blocked": 0,
        "tasks_returned": 0,
        "tasks_changes_req": 0,
        "first_pass_rate": None,
        "cc_verified_rate": None,
        "roadmap_tasks": 0,
        "avg_cycle_days": None,
        "p50_cycle_days": None,
        "claim_accuracy": None,
        "health_score": None,
        "trend_30d": None,
        "generated_at": str(date.today()),
        "note": "No tasks assigned",
    }


def _compute_metrics(agent: str, tasks: list[dict], cutoff: date) -> dict:
    today = date.today()

    status_counts = {s: 0 for s in VALID_STATUSES}
    for t in tasks:
        s = str(t.get("status", "")).upper()
        if s in status_counts:
            status_counts[s] += 1

    closed = [t for t in tasks if str(t.get("status", "")).upper() == "CLOSED"]
    recent_closed = [t for t in closed if (parse_date(t.get("completed_at")) or date.min) >= cutoff]

    # First-pass rate: closed tasks with no rework evidence
    fp_count = sum(1 for t in closed if not has_rework_evidence(t))
    first_pass_rate = round(fp_count / len(closed) * 100, 1) if closed else None

    # CC verified rate: closed tasks that have cc_reviewed set
    cc_ver = sum(1 for t in closed if t.get("cc_reviewed"))
    cc_verified_rate = round(cc_ver / len(closed) * 100, 1) if closed else None

    # Claim accuracy: of cc-reviewed closed tasks, % where CC raised no flag
    cc_reviewed_tasks = [t for t in closed if t.get("cc_reviewed")]
    acc_ok = sum(1 for t in cc_reviewed_tasks if claim_accuracy_ok(t))
    claim_accuracy = round(acc_ok / len(cc_reviewed_tasks) * 100, 1) if cc_reviewed_tasks else None

    # Cycle time
    cycle_days = []
    for t in closed:
        c = parse_date(t.get("created_at"))
        d = parse_date(t.get("completed_at"))
        if c and d and d >= c:
            cycle_days.append((d - c).days)
    avg_cycle = round(mean(cycle_days), 1) if cycle_days else None
    p50_cycle = round(median(cycle_days), 1) if cycle_days else None

    # Roadmap tasks
    roadmap = sum(1 for t in tasks if str(t.get("roadmap_impact", "")).lower() == "true")

    # Health score: composite 0-100
    health = None
    components = [x for x in [first_pass_rate, cc_verified_rate, claim_accuracy] if x is not None]
    if components:
        weights = [0.40, 0.30, 0.30]
        vals = [first_pass_rate or 0, cc_verified_rate or 0, claim_accuracy or 0]
        nweights = weights[: len(vals)]
        norm = sum(nweights)
        health = round(sum(v * w for v, w in zip(vals, nweights)) / norm, 1)

    # 30-day trend: health score over recent closed vs. overall
    trend = None
    if recent_closed and len(recent_closed) >= 2:
        fp_r = sum(1 for t in recent_closed if not has_rework_evidence(t))
        fpr_r = round(fp_r / len(recent_closed) * 100, 1)
        cc_r = sum(1 for t in recent_closed if t.get("cc_reviewed"))
        ccr_r = round(cc_r / len(recent_closed) * 100, 1)
        cc_rev_r = [t for t in recent_closed if t.get("cc_reviewed")]
        acc_r = sum(1 for t in cc_rev_r if claim_accuracy_ok(t))
        ca_r = round(acc_r / len(cc_rev_r) * 100, 1) if cc_rev_r else None
        vals_r = [fpr_r, ccr_r, ca_r or 0]
        health_r = round(sum(v * w for v, w in zip(vals_r, [0.4, 0.3, 0.3])), 1)
        if health is not None:
            trend = round(health_r - health, 1)

    return {
        "agent": agent,
        "tasks_total": len(tasks),
        "tasks_closed": len(closed),
        "tasks_in_progress": status_counts["IN_PROGRESS"],
        "tasks_blocked": status_counts["BLOCKED"],
        "tasks_returned": status_counts["RETURNED"],
        "tasks_changes_req": status_counts["CHANGES_REQUESTED"],
        "roadmap_tasks": roadmap,
        "first_pass_rate": first_pass_rate,
        "cc_verified_rate": cc_verified_rate,
        "claim_accuracy": claim_accuracy,
        "avg_cycle_days": avg_cycle,
        "p50_cycle_days": p50_cycle,
        "health_score": health,
        "trend_30d": trend,
        "generated_at": str(today),
        "closed_task_ids": [t.get("id", "?") for t in closed],
    }


def grade(score: float | None) -> str:
    if score is None:
        return "-"
    if score >= 90: return "A"
    if score >= 75: return "B"
    if score >= 60: return "C"
    if score >= 45: return "D"
    return "E"


def trend_arrow(t: float | None) -> str:
    if t is None: return "-"
    if t > 3:  return f"^ +{t}"
    if t < -3: return f"v {t}"
    return f"~ {t:+.1f}"


# ── Formatters ─────────────────────────────────────────────────────────────────

def print_scorecard(scorecard: dict, digest: bool = False):
    today = date.today()
    print(f"\n{'='*70}")
    print(f"  Bari Agent Performance Scorecard — {today}")
    print(f"  Powered by: C:\\Bari\\tasks\\TASK-*.md  (authoritative registry)")
    print(f"{'='*70}\n")

    agents = [k for k in scorecard if not k.startswith("_")]
    agents.sort()

    # Table header
    col_w = [22, 7, 7, 7, 7, 12, 12, 12, 10, 10]
    header = ["Agent", "Total", "Closed", "Active", "Rework", "1st-Pass%", "CC-Ver%", "ClaimAcc%", "Health", "Trend30d"]
    print("  " + "  ".join(f"{h:{w}}" for h, w in zip(header, col_w)))
    print("  " + "  ".join("-" * w for w in col_w))

    for agent in agents:
        m = scorecard[agent]
        active = m.get("tasks_in_progress", 0) + m.get("tasks_blocked", 0)
        row = [
            agent,
            str(m.get("tasks_total", 0)),
            str(m.get("tasks_closed", 0)),
            str(active),
            str(m.get("tasks_changes_req", 0)),
            f"{m['first_pass_rate']}%" if m.get("first_pass_rate") is not None else "-",
            f"{m['cc_verified_rate']}%" if m.get("cc_verified_rate") is not None else "-",
            f"{m['claim_accuracy']}%" if m.get("claim_accuracy") is not None else "-",
            f"{m['health_score']} / {grade(m.get('health_score'))}" if m.get("health_score") is not None else "-",
            trend_arrow(m.get("trend_30d")),
        ]
        print("  " + "  ".join(f"{v:{w}}" for v, w in zip(row, col_w)))

    unrouted = scorecard.get("_unrouted", {})
    if unrouted.get("tasks_total", 0):
        print(f"\n  Unrouted tasks (unknown owner): {unrouted['tasks_total']}")
        print(f"    IDs: {', '.join(unrouted.get('task_ids', []))}")

    print(f"\n  Metric definitions:")
    print(f"    1st-Pass%   = closed tasks with no rework evidence (CHANGES_REQUESTED / cc flag)")
    print(f"    CC-Ver%     = closed tasks where CC set cc_reviewed")
    print(f"    ClaimAcc%   = CC-reviewed tasks with no flag:verify or flag:blocker in cc_comments")
    print(f"    Health      = 1st-Pass×0.40 + CC-Ver×0.30 + ClaimAcc×0.30  (0–100)")
    print(f"    Trend30d    = health_score(last 30d closed) − health_score(all time)")
    print()

    if digest:
        print(f"  Digest (agents with health < 75 or rework > 0):\n")
        for agent in agents:
            m = scorecard[agent]
            h = m.get("health_score")
            rework = m.get("tasks_changes_req", 0)
            returned = m.get("tasks_returned", 0)
            if (h is not None and h < 75) or rework > 0 or returned > 0:
                print(f"  {agent}:")
                if h is not None and h < 75:
                    print(f"    Health {h} ({grade(h)}) — below target (75/B threshold)")
                if rework > 0:
                    print(f"    {rework} task(s) currently in CHANGES_REQUESTED")
                if returned > 0:
                    print(f"    {returned} task(s) in RETURNED (awaiting review)")
                fpr = m.get("first_pass_rate")
                if fpr is not None and fpr < 70:
                    print(f"    First-pass rate {fpr}% — rework is frequent; review delegation specs")
                print()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Ensure UTF-8 output on Windows consoles
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Bari agent performance scorecard")
    parser.add_argument("--json",   action="store_true", dest="as_json", help="Output JSON")
    parser.add_argument("--save",   action="store_true", help="Save agent_scorecard.json")
    parser.add_argument("--digest", action="store_true", help="Show digest (below-threshold agents only)")
    args = parser.parse_args()

    if not TASKS_DIR.exists():
        print(f"ERROR: tasks dir not found: {TASKS_DIR}", file=sys.stderr)
        sys.exit(1)

    tasks = []
    for f in TASKS_DIR.glob("TASK-*.md"):
        t = parse_task(f)
        if t is not None:
            tasks.append(t)

    if not tasks:
        print("No tasks found.", file=sys.stderr)
        sys.exit(1)

    scorecard = build_agent_scorecard(tasks)

    if args.as_json or args.save:
        payload = json.dumps(scorecard, indent=2, ensure_ascii=False, default=str)
        if args.save:
            OUTPUT_FILE.write_text(payload, encoding="utf-8")
            print(f"Saved: {OUTPUT_FILE}")
        if args.as_json:
            print(payload)
            return

    print_scorecard(scorecard, digest=args.digest)


if __name__ == "__main__":
    main()
