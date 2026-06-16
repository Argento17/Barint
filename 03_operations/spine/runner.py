"""Project Spine1 (TASK-252) — lean DAG runner.

A Stage declares what it reads (inputs) and what it writes (outputs); the
runner enforces the contract and the spine remembers everything:

  1. Stages are topologically ordered: whoever produces a path runs before
     whoever consumes it. Cycles are an error.
  2. Each stage gets a signature = sha256(name + code_version + input hashes).
  3. A stage is SKIPPED when the same signature already ran OK and all its
     recorded outputs still exist with unchanged hashes (resume/incremental:
     editing one input re-runs only the stages downstream of it).
  4. After a stage runs, outputs must exist (output contract), are hashed and
     recorded as artifacts, and lineage rows link every output to every input.

Stdlib only. This is not a Dagster replacement — it is the minimal contract
that makes the pipeline resumable, auditable, and queryable.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from spine_db import connect, record_artifact, record_lineage, sha256_file, utcnow


@dataclass
class Stage:
    name: str
    fn: Callable[[], None]
    inputs: list[Path] = field(default_factory=list)
    outputs: list[Path] = field(default_factory=list)
    code_version: str = "v0"


class StageFailed(RuntimeError):
    pass


def _signature(stage: Stage) -> str:
    h = hashlib.sha256()
    h.update(stage.name.encode("utf-8"))
    h.update(stage.code_version.encode("utf-8"))
    for raw in sorted(str(p) for p in stage.inputs):
        h.update(raw.encode("utf-8"))
        p = Path(raw)
        h.update(sha256_file(p).encode("ascii") if p.exists() else b"<missing>")
    return h.hexdigest()


def _toposort(stages: list[Stage]) -> list[Stage]:
    by_name = {s.name: s for s in stages}
    if len(by_name) != len(stages):
        raise ValueError("duplicate stage names")
    producer_of = {str(o): s.name for s in stages for o in s.outputs}
    order: list[Stage] = []
    done: set[str] = set()

    def visit(stage: Stage, chain: tuple[str, ...]) -> None:
        if stage.name in done:
            return
        if stage.name in chain:
            raise ValueError(f"stage cycle: {' -> '.join(chain)} -> {stage.name}")
        for inp in stage.inputs:
            dep = producer_of.get(str(inp))
            if dep and dep != stage.name:
                visit(by_name[dep], chain + (stage.name,))
        done.add(stage.name)
        order.append(stage)

    for s in stages:
        visit(s, ())
    return order


def _outputs_intact(outputs_json: str | None) -> bool:
    recorded = json.loads(outputs_json or "[]")
    if not recorded:
        return False
    for rec in recorded:
        p = Path(rec["path"])
        if not p.exists() or sha256_file(p) != rec["sha256"]:
            return False
    return True


def run_pipeline(
    stages: list[Stage],
    db_path: Path | str | None = None,
    force: bool = False,
) -> dict[str, str]:
    """Execute stages in dependency order. Returns {stage_name: 'ran'|'skipped'}."""
    conn = connect(db_path)
    results: dict[str, str] = {}
    try:
        for stage in _toposort(stages):
            sig = _signature(stage)
            prev = conn.execute(
                "SELECT status, outputs_json FROM stage_runs WHERE stage_name = ? AND signature = ?",
                (stage.name, sig),
            ).fetchone()
            if prev and prev["status"] == "ok" and not force and _outputs_intact(prev["outputs_json"]):
                results[stage.name] = "skipped"
                continue

            started = utcnow()
            try:
                stage.fn()
                missing = [str(o) for o in stage.outputs if not Path(o).exists()]
                if missing:
                    raise StageFailed(f"output contract violated, missing: {missing}")
            except Exception as exc:
                conn.execute(
                    """INSERT OR REPLACE INTO stage_runs
                       (stage_name, signature, status, started_at, finished_at, outputs_json, error)
                       VALUES (?, ?, 'failed', ?, ?, NULL, ?)""",
                    (stage.name, sig, started, utcnow(), str(exc)),
                )
                conn.commit()
                if isinstance(exc, StageFailed):
                    raise
                raise StageFailed(f"{stage.name}: {exc}") from exc

            out_records = []
            for out in stage.outputs:
                digest = record_artifact(conn, out, "stage_output")
                out_records.append({"path": str(out), "sha256": digest})
                for inp in stage.inputs:
                    record_lineage(conn, out, inp)
            conn.execute(
                """INSERT OR REPLACE INTO stage_runs
                   (stage_name, signature, status, started_at, finished_at, outputs_json, error)
                   VALUES (?, ?, 'ok', ?, ?, ?, NULL)""",
                (stage.name, sig, started, utcnow(), json.dumps(out_records)),
            )
            conn.commit()
            results[stage.name] = "ran"
    finally:
        conn.close()
    return results
