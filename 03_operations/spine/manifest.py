"""Project Spine1 (TASK-252, Phase 3) — live-state manifest generator (ADD-2).

Emits live_manifest.json: one entry per website data file — category, version,
run_id, product count, sha256, plus the grade distribution reconstructed from
the datastore when the producing run is known. This is the machine-readable
answer to "what is live?" — consumed by smoke_test.py and humans alike.

Usage:
  python ingest.py        # refresh spine.db first
  python manifest.py      # -> live_manifest.json
"""
from __future__ import annotations

import json
from pathlib import Path

from spine_db import connect, utcnow

SPINE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = SPINE_DIR / "live_manifest.json"


def build_manifest(db_path: Path | str | None = None) -> dict:
    conn = connect(db_path)
    entries = []
    try:
        for row in conn.execute(
            "SELECT data_file, category, version, run_id, product_count, generated_at, sha256 "
            "FROM live_state ORDER BY data_file"
        ):
            entry = {
                "data_file": Path(row["data_file"]).name,
                "path": row["data_file"],
                "category": row["category"],
                "version": row["version"],
                "run_id": row["run_id"],
                "product_count": row["product_count"],
                "generated_at": row["generated_at"],
                "sha256": row["sha256"],
            }
            if row["run_id"]:
                grades = {
                    g["grade"]: g["n"]
                    for g in conn.execute(
                        "SELECT grade, COUNT(*) n FROM scores WHERE run_id = ? GROUP BY grade",
                        (row["run_id"],),
                    )
                }
                if grades:
                    entry["trace_grade_distribution"] = grades
            entries.append(entry)
    finally:
        conn.close()
    return {
        "_meta": {
            "generated": utcnow(),
            "source": "spine.db (TASK-252)",
            "entry_count": len(entries),
            "note": "trace_grade_distribution counts ALL traces of the run, "
                    "including products blocked at frontend packaging.",
        },
        "files": entries,
    }


def main() -> None:
    manifest = build_manifest()
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"live_manifest.json written: {manifest['_meta']['entry_count']} entries")
    for e in manifest["files"]:
        print(f"  {e['data_file']:42s} v={str(e['version'] or '?'):16s} "
              f"run={str(e['run_id'] or '-'):28s} products={e['product_count']}")


if __name__ == "__main__":
    main()
