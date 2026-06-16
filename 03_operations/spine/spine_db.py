"""Project Spine1 (TASK-252) — datastore layer.

SQLite via stdlib: zero new dependencies on the pipeline machine. The DB file
(spine.db) is generated state and gitignored; schema.sql is the source of truth.
"""
from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SPINE_DIR = Path(__file__).resolve().parent
DEFAULT_DB = SPINE_DIR / "spine.db"
SCHEMA_SQL = SPINE_DIR / "schema.sql"


def connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    """Open (and if needed initialize) a spine database."""
    conn = sqlite3.connect(db_path or DEFAULT_DB)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))
    return conn


def sha256_file(path: Path | str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def record_artifact(
    conn: sqlite3.Connection, path: Path | str, kind: str, run_id: str | None = None
) -> str:
    """Hash and upsert an artifact row. Returns the sha256 digest."""
    p = Path(path)
    digest = sha256_file(p)
    st = p.stat()
    mtime = datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(timespec="seconds")
    conn.execute(
        """INSERT INTO artifacts (path, kind, sha256, bytes, mtime, run_id, recorded_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(path) DO UPDATE SET
             kind = excluded.kind,
             sha256 = excluded.sha256,
             bytes = excluded.bytes,
             mtime = excluded.mtime,
             run_id = COALESCE(excluded.run_id, artifacts.run_id),
             recorded_at = excluded.recorded_at""",
        (str(p), kind, digest, st.st_size, mtime, run_id, utcnow()),
    )
    return digest


def record_lineage(
    conn: sqlite3.Connection,
    child: Path | str,
    parent: Path | str,
    relation: str = "derived_from",
) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO lineage (child_path, parent_path, relation) VALUES (?, ?, ?)",
        (str(child), str(parent), relation),
    )
