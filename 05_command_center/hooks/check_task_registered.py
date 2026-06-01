#!/usr/bin/env python3
"""
UserPromptSubmit hook — warn when a TASK-XXX is referenced but not registered.
(TASK-125 / registry best-practice — the safety net for the TASK-124 failure.)

Reads the hook JSON on stdin ({"prompt": "..."}), finds TASK-NNN / TASK-NNNA ids
in the prompt, and for any that have NO C:\\Bari\\tasks\\TASK-*.md file, prints a
one-line reminder to stdout — which Claude Code adds to the model's context.

It NEVER blocks (always exit 0): referencing a task is not the same as opening one
(your "what happens if I close TASK-123?" mentions a task without opening it). The
reminder lets Claude/operator apply the task_creation_protocol classification rather
than forcing a file for every mention. Prints nothing when every referenced id
already exists — so it costs no tokens on the common path.
"""
import json
import re
import sys
from pathlib import Path

TASKS_DIR = Path(r"C:\Bari\tasks")
NEW_TASK = r"C:\Bari\05_command_center\new_task.py"


def main():
    try:
        raw = sys.stdin.buffer.read()                 # bytes — robust to BOM / encoding
        data = json.loads(raw.decode("utf-8-sig") or "{}")
    except Exception:
        return 0
    prompt = data.get("prompt", "") or ""

    ids, seen = [], set()
    for m in re.findall(r"\bTASK-\d+[A-Z]*\b", prompt):
        if m not in seen:
            seen.add(m)
            ids.append(m)

    missing = [t for t in ids if not (TASKS_DIR / f"{t}.md").exists()]
    if missing:
        print(
            f"[registry-guard] Referenced but NOT in the registry: {', '.join(missing)}. "
            f"If any names work being OPENED, register it FIRST per task_creation_protocol_v1 "
            f"(python \"{NEW_TASK}\" <id | --parent TASK-NNN> --title \"...\" --owner <agent>) "
            f"so it never becomes invisible like TASK-124. If it's only a passing reference, ignore this."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
