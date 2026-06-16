"""Read-only lineage viewer for the Spine e2e pipeline (P46).

Prints stage_runs and artifact lineage for the most recent end-to-end pipeline
execution recorded in spine.db. Stdlib only; opens the database read-only.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

SPINE_DIR = Path(__file__).resolve().parent
REPO = SPINE_DIR.parents[1]
DEFAULT_DB = SPINE_DIR / "spine.db"

E2E_STAGE_ORDER = (
    "extract_bsip0",
    "build_bsip1",
    "score_products",
    "generate_page",
    "gate_page",
    "build_copy_inputs",
    "author_copy",
    "merge_copy_and_gate",
)


def connect_readonly(db_path: Path) -> sqlite3.Connection:
    uri = f"file:{db_path.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (name,),
    ).fetchone()
    return row is not None


def _short_path(path: str) -> str:
    try:
        return str(Path(path).resolve().relative_to(REPO))
    except ValueError:
        return path


def _artifact_kind(path: str) -> str:
    p = path.replace("\\", "/").lower()
    if "/_fixtures_e2e/raw/" in p or p.endswith(".html"):
        return "raw"
    if "/bsip0/" in p or "/bsip0_" in p:
        return "bsip0"
    if "/bsip1/" in p or "/bsip1_" in p:
        return "bsip1"
    if "bsip2_trace.json" in p:
        return "bsip2_trace"
    if "/page/" in p and p.endswith(".json"):
        return "page"
    if "gates_report" in p:
        return "gate"
    if "/copy/" in p:
        return "copy"
    return "other"


def _parse_outputs(outputs_json: str | None) -> list[str]:
    if not outputs_json:
        return []
    try:
        records = json.loads(outputs_json)
    except json.JSONDecodeError:
        return []
    return [rec["path"] for rec in records if isinstance(rec, dict) and "path" in rec]


def _latest_e2e_run(conn: sqlite3.Connection) -> tuple[sqlite3.Row | None, list[sqlite3.Row]]:
    anchor = conn.execute(
        """SELECT stage_name, signature, status, started_at, finished_at, outputs_json, error
           FROM stage_runs
           WHERE stage_name = 'merge_copy_and_gate' AND status = 'ok'
           ORDER BY finished_at DESC
           LIMIT 1"""
    ).fetchone()
    if anchor is None:
        return None, []

    anchor_started = anchor["started_at"]
    stages: list[sqlite3.Row] = []
    for name in E2E_STAGE_ORDER:
        row = conn.execute(
            """SELECT stage_name, signature, status, started_at, finished_at, outputs_json, error
               FROM stage_runs
               WHERE stage_name = ? AND status = 'ok' AND started_at <= ?
               ORDER BY started_at DESC
               LIMIT 1""",
            (name, anchor_started),
        ).fetchone()
        if row:
            stages.append(row)

    stages.sort(key=lambda r: r["started_at"] or "")
    return anchor, stages


def _collect_run_paths(stage_rows: list[sqlite3.Row]) -> set[str]:
    paths: set[str] = set()
    for row in stage_rows:
        for path in _parse_outputs(row["outputs_json"]):
            paths.add(str(Path(path).resolve()))
    return paths


def _lineage_closure(conn: sqlite3.Connection, seed_paths: set[str]) -> set[str]:
    if not seed_paths:
        return set()

    known = set(seed_paths)
    frontier = list(seed_paths)
    while frontier:
        child = frontier.pop()
        parents = conn.execute(
            "SELECT parent_path FROM lineage WHERE child_path = ?",
            (child,),
        ).fetchall()
        for row in parents:
            parent = str(Path(row["parent_path"]).resolve())
            if parent not in known:
                known.add(parent)
                frontier.append(parent)
    return known


def _print_stage_runs(stages: list[sqlite3.Row]) -> None:
    print("=== Stage runs (most recent e2e pipeline) ===")
    if not stages:
        print("  (no stage runs found)")
        return
    for row in stages:
        print(
            f"  {row['stage_name']:25s}  status={row['status']:7s}  "
            f"finished_at={row['finished_at']}"
        )


def _print_lineage(conn: sqlite3.Connection, run_paths: set[str]) -> None:
    print("\n=== Artifact lineage (child <- parent) ===")
    if not run_paths:
        print("  (no output artifacts for this run)")
        return

    closure = _lineage_closure(conn, run_paths)
    edges = conn.execute(
        "SELECT child_path, parent_path, relation FROM lineage ORDER BY child_path, parent_path"
    ).fetchall()
    run_edges = [
        e
        for e in edges
        if str(Path(e["child_path"]).resolve()) in closure
        and str(Path(e["parent_path"]).resolve()) in closure
    ]
    if not run_edges:
        print("  (no lineage edges for this run)")
        return

    by_kind: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for edge in run_edges:
        child = str(Path(edge["child_path"]).resolve())
        parent = str(Path(edge["parent_path"]).resolve())
        kind = _artifact_kind(child)
        by_kind[kind].append((child, parent, edge["relation"]))

    kind_order = ("raw", "bsip0", "bsip1", "bsip2_trace", "page", "gate", "copy", "other")
    print("\n  Chain summary: raw -> bsip0 -> bsip1 -> bsip2_trace -> page -> gate -> copy")
    for kind in kind_order:
        items = by_kind.get(kind)
        if not items:
            continue
        unique_children = sorted({_short_path(c) for c, _, _ in items})
        print(f"\n  [{kind}]")
        for child_short in unique_children:
            print(f"    {child_short}")
            parents = sorted(
                {
                    _short_path(p)
                    for c, p, _ in items
                    if _short_path(c) == child_short
                }
            )
            for parent_short in parents:
                print(f"      <- {parent_short}")

    print("\n  Full edges:")
    for edge in run_edges:
        child_short = _short_path(str(Path(edge["child_path"]).resolve()))
        parent_short = _short_path(str(Path(edge["parent_path"]).resolve()))
        print(f"    {child_short}")
        print(f"      <- {parent_short}  [{edge['relation']}]")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    db_path = DEFAULT_DB
    if not db_path.exists():
        print(f"no runs found (database missing: {_short_path(str(db_path))})")
        return 0

    conn = connect_readonly(db_path)
    try:
        if not _table_exists(conn, "stage_runs"):
            print("no runs found (stage_runs table missing)")
            return 0

        count = conn.execute("SELECT COUNT(*) FROM stage_runs").fetchone()[0]
        if count == 0:
            print("no runs found (stage_runs is empty)")
            return 0

        anchor, stages = _latest_e2e_run(conn)
        if anchor is None:
            print("no runs found (no completed merge_copy_and_gate stage)")
            return 0

        _print_stage_runs(stages)

        if _table_exists(conn, "lineage"):
            run_paths = _collect_run_paths(stages)
            _print_lineage(conn, run_paths)
        else:
            print("\n=== Artifact lineage (child <- parent) ===")
            print("  (lineage table missing)")
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
