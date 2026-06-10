#!/usr/bin/env python3
"""
new_task.py — open a Bari registry task in one command  (TASK-125)
==================================================================

The Task Creation Protocol (`task_creation_protocol_v1.md`) requires a task to be
registered the instant it is opened — *before* work begins — or the work is
invisible to the Command Center. That step is manual and easy to skip; this tool
makes the right thing the easy thing. It writes a schema-correct
`C:\\Bari\\tasks\\TASK-NNN.md` at IN_PROGRESS (or BLOCKED) and regenerates the
dashboard, so a new task shows under Active Work immediately.

It deliberately automates *nothing else*: it is a manual, deliberate act per the
protocol (no CI gate, no watcher). It only ever CREATES a new file — it never
edits or clobbers an existing task (ids are sequential and never reused).

Usage:
    cd C:\\Bari\\05_command_center
    python new_task.py --title "Build X" --owner frontend-agent
    python new_task.py 126 --title "Build X" --owner data-agent --priority HIGH
    python new_task.py 127 --title "Wait on Y" --owner qa-agent \\
        --status BLOCKED --blocker "waiting on TASK-126" --depends-on TASK-126
    python new_task.py --title "..." --owner content-agent --summary "what it delivers"

If the id is omitted, the next sequential id (max existing + 1) is allocated.
Open states are IN_PROGRESS (default) or BLOCKED only — RETURNED/CHANGES_REQUESTED/
CLOSED are lifecycle outcomes the Controller records later, never an opening state
(protocol §3).
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

BARI_ROOT = Path(r"C:\Bari")
TASKS_DIR = BARI_ROOT / "tasks"
CLOSED_DIR = TASKS_DIR / "closed"          # archived CLOSED files (id-allocation must see these)
HERE = Path(__file__).resolve().parent


def _all_task_files(pattern):
    """Every task file matching pattern across the live registry AND the closed
    archive. ID allocation must scan both so a freshly-closed (moved) task can
    never have its number re-issued."""
    files = list(TASKS_DIR.glob(pattern))
    if CLOSED_DIR.exists():
        files += list(CLOSED_DIR.glob(pattern))
    return files
GENERATOR = HERE / "generate_dashboard.py"

# Regenerate under the project venv, never whatever interpreter happens to be on
# PATH — the system Python lacks PyYAML and silently fails the regen (TASK-127).
# generate_dashboard.py also self-guards, so this is belt-and-suspenders.
import os as _os
_VENV_PY = BARI_ROOT / ".venv" / "Scripts" / ("python.exe" if _os.name == "nt" else "python")
REGEN_PY = str(_VENV_PY) if _VENV_PY.exists() else sys.executable

# Canonical owner slugs (mirrors command_center_v4.html OWNER_SHORT).
KNOWN_OWNERS = {
    "product-agent", "nutrition-agent", "research-agent", "data-agent",
    "frontend-agent", "design-agent", "qa-agent", "content-agent", "marketing-agent",
}
OPEN_STATES = ("IN_PROGRESS", "BLOCKED")          # protocol §3
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
    ap.add_argument("--no-regen", action="store_true", help="skip the dashboard regenerate")
    args = ap.parse_args()

    # ── validate ──────────────────────────────────────────────────────────────
    status = args.status.strip().upper()
    if status not in OPEN_STATES:
        sys.exit(f"error: a task may only OPEN at {' or '.join(OPEN_STATES)} "
                 f"(got {status!r}). RETURNED/CHANGES_REQUESTED/CLOSED are outcomes "
                 f"the Controller records later — protocol §3.")
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

    # ── compose frontmatter (field order = protocol §4) ───────────────────────
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

    # ── regenerate so the task is visible (protocol §5) ───────────────────────
    if args.no_regen:
        print("  (skipped regenerate — run `python generate_dashboard.py` to show it)")
        return 0
    gen = subprocess.run([REGEN_PY, str(GENERATOR)], cwd=str(HERE),
                         capture_output=True, text=True)
    if gen.returncode != 0:
        print("  WARNING: task file written but regenerate failed:\n"
              + (gen.stderr or gen.stdout)[-400:], file=sys.stderr)
        return 1
    print("  dashboard regenerated — task now visible under Active Work"
          + (" / Blockers" if status == "BLOCKED" else "") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
