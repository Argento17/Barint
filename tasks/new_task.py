#!/usr/bin/env python3
"""
new_task.py — open a Bari registry task in one command  (TASK-125)
==================================================================

The registry (`C:\\Bari\\tasks\\`) is the single source of truth. A task must be
registered the instant it is opened — *before* work begins — or the work is
invisible to the orchestrator. That step is manual and easy to skip; this tool
makes the right thing the easy thing. It writes a schema-correct
`C:\\Bari\\tasks\\TASK-NNN.md` at IN_PROGRESS (or BLOCKED).

It deliberately automates *nothing else*: it is a manual, deliberate act (no CI
gate, no watcher). It only ever CREATES a new file — it never edits or clobbers
an existing task (ids are sequential and never reused).

This is the post-command-center tool: there is no derived dashboard to regenerate
anymore. The registry IS the state; `tasks/DISPATCH_BOARD.md` is the live view.
(Command center retired 2026-06-13; the orchestrator reads the registry directly.)

Usage:
    python C:\\Bari\\tasks\\new_task.py --title "Build X" --owner frontend-agent
    python C:\\Bari\\tasks\\new_task.py 126 --title "Build X" --owner data-agent --priority HIGH
    python C:\\Bari\\tasks\\new_task.py 127 --title "Wait on Y" --owner qa-agent \\
        --status BLOCKED --blocker "waiting on TASK-126" --depends-on TASK-126
    python C:\\Bari\\tasks\\new_task.py --title "..." --owner content-agent --summary "what it delivers"

If the id is omitted, the next sequential id (max existing + 1) is allocated.
Open states are IN_PROGRESS (default) or BLOCKED only — RETURNED/CHANGES_REQUESTED/
CLOSED are lifecycle outcomes the orchestrator records later, never an opening state.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

BARI_ROOT = Path(r"C:\Bari")
TASKS_DIR = BARI_ROOT / "tasks"
CLOSED_DIR = TASKS_DIR / "closed"          # archived CLOSED files (id-allocation must see these)


def _all_task_files(pattern):
    """Every task file matching pattern across the live registry AND the closed
    archive. ID allocation must scan both so a freshly-closed (moved) task can
    never have its number re-issued."""
    files = list(TASKS_DIR.glob(pattern))
    if CLOSED_DIR.exists():
        files += list(CLOSED_DIR.glob(pattern))
    return files


# Canonical owner slugs.
KNOWN_OWNERS = {
    "product-agent", "nutrition-agent", "research-agent", "data-agent",
    "frontend-agent", "design-agent", "qa-agent", "content-agent", "marketing-agent",
    "red-team-agent",
}
OPEN_STATES = ("IN_PROGRESS", "BLOCKED")
PRIORITIES = ("CRITICAL", "HIGH", "MEDIUM", "LOW")


def existing_ids():
    ids = []
    for f in _all_task_files("TASK-*.md"):
        m = re.match(r"TASK-(\d+)", f.stem)
        if m:
            ids.append(int(m.group(1)))
    return ids


def normalize_id(raw):
    """'126' / 'TASK-126' / '125a' -> 'TASK-126' / 'TASK-125A' (number zero-padded
    to 3 digits; an optional trailing letter denotes a sub-task)."""
    s = str(raw).strip().upper()
    m = re.match(r"(?:TASK-)?0*(\d+)([A-Z]*)$", s)
    if not m:
        return None
    return f"TASK-{int(m.group(1)):03d}{m.group(2)}"


def next_subtask_id(objective_id):
    """Next free letter sub-task under an objective: TASK-125 -> TASK-125A/B/..."""
    used = set()
    pat = re.compile(rf"^{re.escape(objective_id)}([A-Z]+)$")
    for f in _all_task_files(f"{objective_id}[A-Z]*.md"):
        m = pat.match(f.stem)
        if m:
            used.add(m.group(1))
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in used:
            return f"{objective_id}{c}"
    sys.exit(f"error: {objective_id} already has sub-tasks A–Z; use an explicit id.")


def id_list(arg):
    """'TASK-100, 101' -> '[TASK-100, TASK-101]' ; '' -> '[]'."""
    if not arg:
        return "[]"
    out = []
    for part in re.split(r"[,\s]+", arg.strip()):
        if not part:
            continue
        nid = normalize_id(part)
        if not nid:
            sys.exit(f"error: '{part}' is not a valid TASK id")
        out.append(nid)
    return "[" + ", ".join(out) + "]"


def main():
    ap = argparse.ArgumentParser(description="Open a Bari registry task (protocol-correct).")
    ap.add_argument("id", nargs="?", help="task id: TASK-NNN (objective) or TASK-NNNA (sub-task); "
                                          "default: next sequential objective")
    ap.add_argument("--parent", help="objective id to add a sub-task under (auto-allocates the next letter)")
    ap.add_argument("--title", required=True, help="one-line human-readable title")
    ap.add_argument("--owner", required=True, help="agent slug, e.g. frontend-agent")
    ap.add_argument("--priority", default="MEDIUM", help="CRITICAL|HIGH|MEDIUM|LOW (default MEDIUM)")
    ap.add_argument("--status", default="IN_PROGRESS", help="IN_PROGRESS (default) or BLOCKED")
    ap.add_argument("--blocker", help="free-text reason (required when --status BLOCKED)")
    ap.add_argument("--depends-on", default="", help="comma-separated TASK ids this waits on")
    ap.add_argument("--blocks", default="", help="comma-separated TASK ids waiting on this")
    ap.add_argument("--category-id", default=None, help="comparison category id, or omit for null")
    ap.add_argument("--summary", default=None, help="1-3 line summary of what the task delivers")
    args = ap.parse_args()

    # ── validate ──────────────────────────────────────────────────────────────
    status = args.status.strip().upper()
    if status not in OPEN_STATES:
        sys.exit(f"error: a task may only OPEN at {' or '.join(OPEN_STATES)} "
                 f"(got {status!r}). RETURNED/CHANGES_REQUESTED/CLOSED are outcomes "
                 f"the orchestrator records later.")
    if status == "BLOCKED" and not (args.blocker and args.blocker.strip()):
        sys.exit("error: --status BLOCKED requires --blocker \"reason\".")

    priority = args.priority.strip().upper()
    if priority not in PRIORITIES:
        sys.exit(f"error: --priority must be one of {', '.join(PRIORITIES)}")

    owner = args.owner.strip()
    if owner not in KNOWN_OWNERS:
        print(f"warning: owner '{owner}' is not a known agent slug "
              f"({', '.join(sorted(KNOWN_OWNERS))}). Creating anyway.", file=sys.stderr)

    if args.parent:
        parent = normalize_id(args.parent)
        if not parent or not re.match(r"^TASK-\d+$", parent):
            sys.exit(f"error: --parent must be an objective id like TASK-125 (got {args.parent!r})")
        if not (TASKS_DIR / f"{parent}.md").exists():
            sys.exit(f"error: parent objective {parent} does not exist — create it first.")
        tid = next_subtask_id(parent)
    elif args.id is not None:
        tid = normalize_id(args.id)
        if not tid:
            sys.exit(f"error: '{args.id}' is not a valid task id")
        # a sub-task (TASK-125A) requires its objective (TASK-125) to exist
        sub = re.match(r"^(TASK-\d+)[A-Z]+$", tid)
        if sub and not (TASKS_DIR / f"{sub.group(1)}.md").exists():
            sys.exit(f"error: {tid} is a sub-task but its objective {sub.group(1)} "
                     f"does not exist — create the objective first.")
    else:
        nxt = (max(existing_ids()) + 1) if existing_ids() else 1
        tid = f"TASK-{nxt:03d}"

    path = TASKS_DIR / f"{tid}.md"
    if path.exists():
        sys.exit(f"error: {path.name} already exists — ids are never reused. "
                 f"Pick a new id (omit the id to auto-allocate the next one).")

    # ── compose frontmatter ───────────────────────────────────────────────────
    today = date.today().isoformat()
    summary = (args.summary or args.title).strip()
    lines = [
        "---",
        f"id: {tid}",
        f"title: {args.title.strip()}",
        f"owner: {owner}",
        f"status: {status}",
        f"priority: {priority}",
        f"created_at: {today}",
    ]
    if status == "BLOCKED":
        # YAML double-quoted scalar; collapse any embedded double-quotes to keep it valid
        safe = args.blocker.strip().replace('"', "'")
        lines.append(f'blocker: "{safe}"')
    lines += [
        f"depends_on: {id_list(args.depends_on)}",
        f"blocks: {id_list(args.blocks)}",
        f"category_id: {args.category_id if args.category_id else 'null'}",
        "summary: >",
        f"  {summary}",
        "---",
        "",
        f"# {tid} — {args.title.strip()}",
        "",
        "<!-- opened with new_task.py; fill in context / scope / the deliverable -->",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"created {path}")
    print(f"  {tid}  {status}  {priority}  owner={owner}")
    print("  add it to tasks/DISPATCH_BOARD.md when you dispatch it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
