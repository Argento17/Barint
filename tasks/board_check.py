#!/usr/bin/env python3
"""Registry ↔ DISPATCH_BOARD drift checker (read-only)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TASK_ID_RE = re.compile(r"TASK-\d+[A-Z]*")
OPEN_STATES = frozenset({"IN_PROGRESS", "BLOCKED", "RETURNED", "CHANGES_REQUESTED"})
VALID_STATUSES = OPEN_STATES | {"CLOSED"}
TASK_FILE_RE = re.compile(r"^TASK-\d+[A-Z]*\.md$")


def parse_frontmatter(path: Path) -> tuple[str | None, str | None, str | None]:
    """Parse YAML frontmatter; return (id, status, error_reason)."""
    try:
        # utf-8-sig: several registry files carry a BOM (agent-written; known repo
        # history) -- plain utf-8 would misreport them as missing the delimiter.
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return None, None, f"unreadable: {exc}"

    if not text.startswith("---"):
        return None, None, "missing frontmatter delimiter"

    end = text.find("\n---", 3)
    if end == -1:
        return None, None, "unclosed frontmatter"

    block = text[3:end]
    task_id: str | None = None
    status: str | None = None
    in_block_scalar = False

    for line in block.splitlines():
        if in_block_scalar:
            if line and (line[0] == " " or line[0] == "\t"):
                continue
            in_block_scalar = False

        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if ":" not in line:
            continue

        key, _, raw_value = line.partition(":")
        key = key.strip()
        value = raw_value.strip()

        if value == ">":
            in_block_scalar = True
            continue

        if key == "id":
            task_id = value or None
        elif key == "status":
            status = value or None

    errors: list[str] = []
    if not task_id:
        errors.append("missing or empty id:")
    if not status:
        errors.append("missing or empty status:")
    elif status not in VALID_STATUSES:
        errors.append(f"invalid status: {status}")

    stem = path.stem
    if task_id and stem != task_id:
        errors.append(f"filename {path.name} ≠ frontmatter id {task_id}")

    if errors:
        return task_id, status, "; ".join(errors)
    return task_id, status, None


def collect_task_files(tasks_dir: Path) -> list[Path]:
    files: list[Path] = []
    for directory in (tasks_dir, tasks_dir / "closed"):
        if not directory.is_dir():
            continue
        for path in directory.iterdir():
            if path.is_file() and TASK_FILE_RE.match(path.name):
                files.append(path)
    return files


def load_registry(tasks_dir: Path) -> tuple[dict[str, dict], list[tuple[str, str]]]:
    """Return registry map and BADFILE findings."""
    registry: dict[str, dict] = {}
    badfiles: list[tuple[str, str]] = []

    for path in collect_task_files(tasks_dir):
        task_id, status, error = parse_frontmatter(path)
        rel = path.relative_to(tasks_dir).as_posix()

        if error:
            label = task_id or path.stem
            badfiles.append((label, f"{rel}: {error}"))

        if task_id:
            if task_id in registry:
                badfiles.append(
                    (task_id, f"duplicate id in {rel} and {registry[task_id]['rel']}")
                )
            else:
                registry[task_id] = {
                    "status": status,
                    "path": path,
                    "rel": rel,
                    "in_closed": path.parent.name == "closed",
                }

    return registry, badfiles


def read_board(tasks_dir: Path) -> str:
    board_path = tasks_dir / "DISPATCH_BOARD.md"
    return board_path.read_text(encoding="utf-8")


def board_mentions(board_text: str) -> set[str]:
    return set(TASK_ID_RE.findall(board_text))


def section_header_task_ids(board_text: str) -> list[tuple[str, str]]:
    """Return (task_id, header_line) for ids in ## headers without ✅/CLOSED."""
    stale_candidates: list[tuple[str, str]] = []
    for line in board_text.splitlines():
        if not line.startswith("##"):
            continue
        if "✅" in line or "CLOSED" in line:
            continue
        for task_id in TASK_ID_RE.findall(line):
            stale_candidates.append((task_id, line.strip()))
    return stale_candidates


def check_misfiled(registry: dict[str, dict]) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for task_id, info in sorted(registry.items()):
        status = info["status"]
        in_closed = info["in_closed"]
        if status == "CLOSED" and not in_closed:
            findings.append(
                (task_id, f"status CLOSED but file still in tasks/ ({info['rel']})")
            )
        elif status and status != "CLOSED" and in_closed:
            findings.append(
                (task_id, f"status {status} but file in tasks/closed/ ({info['rel']})")
            )
    return findings


def check_ghost(
    tasks_dir: Path, registry: dict[str, dict], mentions: set[str]
) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for path in sorted(tasks_dir.glob("TASK-*.md")):
        if not path.is_file():
            continue
        task_id = path.stem
        info = registry.get(task_id)
        if not info or info.get("in_closed"):
            continue
        status = info.get("status")
        if status in OPEN_STATES and task_id not in mentions:
            findings.append(
                (task_id, f"open ({status}) but not mentioned on DISPATCH_BOARD")
            )
    return findings


def check_stale_active(
    registry: dict[str, dict], header_hits: list[tuple[str, str]]
) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    seen: set[str] = set()
    for task_id, header in header_hits:
        if task_id in seen:
            continue
        info = registry.get(task_id)
        if info and info.get("status") == "CLOSED":
            seen.add(task_id)
            findings.append(
                (task_id, f"active section header but registry CLOSED ({header[:80]})")
            )
    return sorted(findings, key=lambda x: x[0])


def check_unknown(registry: dict[str, dict], mentions: set[str]) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for task_id in sorted(mentions):
        if task_id not in registry:
            findings.append((task_id, "mentioned on board but no registry file"))
    return findings


def format_report(findings: dict[str, list[tuple[str, str]]]) -> str:
    labels = {
        "ghost": "GHOST",
        "stale_active": "STALE-ACTIVE",
        "unknown": "UNKNOWN",
        "badfile": "BADFILE",
        "misfiled": "MISFILED",
    }
    lines: list[str] = []
    total = 0
    for key in ("ghost", "stale_active", "unknown", "badfile", "misfiled"):
        items = findings[key]
        if not items:
            continue
        lines.append(f"[{labels[key]}]")
        for task_id, reason in items:
            lines.append(f"{task_id}  {reason}")
        lines.append("")
        total += len(items)

    if total == 0:
        lines.append("No drift detected.")
    else:
        lines.append(f"Summary: {total} finding(s) across {sum(1 for v in findings.values() if v)} check(s).")
    return "\n".join(lines)


def findings_to_json(findings: dict[str, list[tuple[str, str]]]) -> dict[str, list[dict[str, str]]]:
    return {
        key: [{"id": task_id, "reason": reason} for task_id, reason in items]
        for key, items in findings.items()
    }


def run_checks(tasks_dir: Path) -> dict[str, list[tuple[str, str]]]:
    board_text = read_board(tasks_dir)
    mentions = board_mentions(board_text)
    registry, badfiles = load_registry(tasks_dir)

    return {
        "ghost": check_ghost(tasks_dir, registry, mentions),
        "stale_active": check_stale_active(registry, section_header_task_ids(board_text)),
        "unknown": check_unknown(registry, mentions),
        "badfile": badfiles,
        "misfiled": check_misfiled(registry),
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Registry ↔ DISPATCH_BOARD drift checker")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    tasks_dir = Path(__file__).resolve().parent
    if not tasks_dir.is_dir():
        print(f"error: tasks directory missing: {tasks_dir}", file=sys.stderr)
        return 2

    board_path = tasks_dir / "DISPATCH_BOARD.md"
    if not board_path.is_file():
        print(f"error: DISPATCH_BOARD.md missing: {board_path}", file=sys.stderr)
        return 2

    try:
        findings = run_checks(tasks_dir)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    total = sum(len(v) for v in findings.values())

    if args.json:
        print(json.dumps(findings_to_json(findings), indent=2))
    else:
        print(format_report(findings))

    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
