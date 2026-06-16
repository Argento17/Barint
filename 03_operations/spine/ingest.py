"""Project Spine1 (TASK-252) — read-only artifact ingestion.

Walks existing pipeline artifacts, hashes every file, and populates the spine
datastore. NEVER modifies a pipeline artifact (Phase 1 guard). Idempotent —
re-running upserts.

Sources swept:
  - 02_products/*/bsip2_outputs/run_*/products/*/bsip2_trace.json
      -> runs(bsip2), products, scores, artifacts, lineage(trace <- bsip1 record)
  - bari-web/src/data/comparisons/*.json
      -> runs(frontend, when _meta.run_id present), live_state, artifacts
  - 02_products/*/reports/*run_summary.json
      -> artifacts

Usage:
  python ingest.py            # full sweep, default spine.db
  python ingest.py --db X.db  # custom database path
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from spine_db import connect, record_artifact, record_lineage, utcnow

REPO = Path(__file__).resolve().parents[2]


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None


def ingest_bsip2_run(conn: sqlite3.Connection, run_dir: Path) -> int:
    """Ingest one bsip2_outputs/run_* folder. Returns trace count."""
    run_id = run_dir.name
    category = run_dir.parents[1].name  # 02_products/<category>/bsip2_outputs/<run>
    engine = None
    count = 0
    for trace_path in sorted(run_dir.glob("products/*/bsip2_trace.json")):
        trace = _load_json(trace_path)
        if not isinstance(trace, dict):
            print(f"  ! unreadable trace skipped: {trace_path}")
            continue
        ref = trace.get("input_reference") or {}
        key = ref.get("canonical_product_id") or ref.get("barcode") or trace_path.parent.name
        engine = engine or f"{trace.get('bsip2_version', '?')}/{trace.get('algorithm_version', '?')}"
        conn.execute(
            """INSERT INTO products (product_key, barcode, name_he, brand, category)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(product_key) DO UPDATE SET
                 barcode = excluded.barcode,
                 name_he = excluded.name_he,
                 brand = excluded.brand,
                 category = excluded.category""",
            (key, ref.get("barcode"), ref.get("product_name_he"), ref.get("brand"),
             trace.get("category")),
        )
        conn.execute(
            """INSERT INTO scores (run_id, product_key, score, grade, confidence_band,
                                   confidence_score, engine_category, nova_proxy, trace_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(run_id, product_key) DO UPDATE SET
                 score = excluded.score,
                 grade = excluded.grade,
                 confidence_band = excluded.confidence_band,
                 confidence_score = excluded.confidence_score,
                 engine_category = excluded.engine_category,
                 nova_proxy = excluded.nova_proxy,
                 trace_path = excluded.trace_path""",
            (run_id, key, trace.get("final_score_estimate"), trace.get("grade_estimate"),
             trace.get("confidence_band"), trace.get("confidence_score"),
             trace.get("category"), trace.get("nova_proxy"), str(trace_path)),
        )
        record_artifact(conn, trace_path, "bsip2_trace", run_id)
        src = ref.get("bsip1_source_path")
        if src:
            src_path = Path(src)
            if src_path.exists():
                record_artifact(conn, src_path, "bsip1_record", None)
            record_lineage(conn, trace_path, src_path)
        count += 1
    if count:
        # Reconcile deletions: a trace removed from the run (e.g. an excluded
        # misroute) must not survive as a stale score row.
        seen = {str(p) for p in run_dir.glob("products/*/bsip2_trace.json")}
        stale = [
            r["trace_path"] for r in conn.execute(
                "SELECT trace_path FROM scores WHERE run_id = ?", (run_id,)
            ) if r["trace_path"] not in seen
        ]
        for path in stale:
            conn.execute(
                "DELETE FROM scores WHERE run_id = ? AND trace_path = ?", (run_id, path)
            )
            conn.execute("DELETE FROM artifacts WHERE path = ?", (path,))
            conn.execute("DELETE FROM lineage WHERE child_path = ?", (path,))
            print(f"  - reconciled deletion: {Path(path).parent.name}")
        conn.execute(
            """INSERT INTO runs (run_id, layer, category, engine, generated_at, meta_json)
               VALUES (?, 'bsip2', ?, ?, ?, ?)
               ON CONFLICT(run_id, layer) DO UPDATE SET
                 engine = excluded.engine, meta_json = excluded.meta_json""",
            (run_id, category, engine, utcnow(), json.dumps({"trace_count": count})),
        )
    return count


def ingest_frontend_dir(conn: sqlite3.Connection, data_dir: Path) -> int:
    """Ingest website-consumable JSONs into live_state (+ runs for tagged files)."""
    count = 0
    for fp in sorted(data_dir.glob("*.json")):
        doc = _load_json(fp)
        if doc is None:
            print(f"  ! unreadable frontend json skipped: {fp.name}")
            continue
        meta = doc.get("_meta", {}) if isinstance(doc, dict) else {}
        if isinstance(doc, list):
            product_count = len(doc)
        elif isinstance(doc.get("products"), list):
            product_count = len(doc["products"])
        else:
            product_count = meta.get("product_count")
        digest = record_artifact(conn, fp, "frontend_json", meta.get("run_id"))
        conn.execute(
            """INSERT INTO live_state (data_file, category, version, run_id, product_count,
                                       generated_at, sha256, recorded_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(data_file) DO UPDATE SET
                 category = excluded.category,
                 version = excluded.version,
                 run_id = excluded.run_id,
                 product_count = excluded.product_count,
                 generated_at = excluded.generated_at,
                 sha256 = excluded.sha256,
                 recorded_at = excluded.recorded_at""",
            (str(fp), meta.get("category") or fp.stem.split("_frontend")[0],
             meta.get("version"), meta.get("run_id"), product_count,
             meta.get("generated"), digest, utcnow()),
        )
        if meta.get("run_id"):
            conn.execute(
                """INSERT INTO runs (run_id, layer, category, engine, generated_at, meta_json)
                   VALUES (?, 'frontend', ?, ?, ?, ?)
                   ON CONFLICT(run_id, layer) DO UPDATE SET
                     generated_at = excluded.generated_at, meta_json = excluded.meta_json""",
                (meta["run_id"], meta.get("category"), meta.get("engine"),
                 meta.get("generated"), json.dumps({"data_file": str(fp)})),
            )
        count += 1
    return count


def full_sweep(conn: sqlite3.Connection, repo: Path = REPO) -> dict[str, int]:
    stats = {"bsip2_runs": 0, "traces": 0, "frontend_files": 0, "run_summaries": 0}
    for run_dir in sorted(repo.glob("02_products/*/bsip2_outputs/run_*")):
        if not run_dir.is_dir():
            continue
        n = ingest_bsip2_run(conn, run_dir)
        if n:
            stats["bsip2_runs"] += 1
            stats["traces"] += n
            print(f"  {run_dir.parents[1].name}/{run_dir.name}: {n} traces")
    frontend_dir = repo / "bari-web" / "src" / "data" / "comparisons"
    if frontend_dir.is_dir():
        stats["frontend_files"] = ingest_frontend_dir(conn, frontend_dir)
    for summary in sorted(repo.glob("02_products/*/reports/*run_summary.json")):
        record_artifact(conn, summary, "run_summary")
        stats["run_summaries"] += 1
    conn.commit()
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Spine1 read-only artifact ingestion")
    parser.add_argument("--db", default=None, help="database path (default: spine.db)")
    args = parser.parse_args()
    conn = connect(args.db)
    try:
        stats = full_sweep(conn)
        print(f"\nIngest complete: {stats}")
        for table in ("runs", "products", "scores", "artifacts", "lineage", "live_state"):
            n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table}: {n}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
