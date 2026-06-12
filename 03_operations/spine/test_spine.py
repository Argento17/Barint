"""Project Spine1 (TASK-252) — test suite. Run: python -m pytest test_spine.py -v"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from ingest import ingest_bsip2_run, ingest_frontend_dir
from runner import Stage, StageFailed, _toposort, run_pipeline
from spine_db import connect


# ---------- runner ----------

def _copy_upper(src: Path, dst: Path):
    def fn():
        dst.write_text(src.read_text(encoding="utf-8").upper(), encoding="utf-8")
    return fn


def _make_chain(tmp_path: Path):
    """raw.txt -> [extract] -> mid.txt -> [package] -> out.txt"""
    raw = tmp_path / "raw.txt"
    mid = tmp_path / "mid.txt"
    out = tmp_path / "out.txt"
    raw.write_text("hello spine", encoding="utf-8")
    extract = Stage("extract", _copy_upper(raw, mid), inputs=[raw], outputs=[mid])
    package = Stage("package", _copy_upper(mid, out), inputs=[mid], outputs=[out])
    return raw, mid, out, extract, package


def test_runner_runs_then_skips(tmp_path):
    db = tmp_path / "spine_test.db"
    raw, mid, out, extract, package = _make_chain(tmp_path)

    first = run_pipeline([extract, package], db_path=db)
    assert first == {"extract": "ran", "package": "ran"}
    assert out.read_text(encoding="utf-8") == "HELLO SPINE"

    second = run_pipeline([extract, package], db_path=db)
    assert second == {"extract": "skipped", "package": "skipped"}


def test_runner_reruns_downstream_on_input_change(tmp_path):
    db = tmp_path / "spine_test.db"
    raw, mid, out, extract, package = _make_chain(tmp_path)
    run_pipeline([extract, package], db_path=db)

    raw.write_text("changed input", encoding="utf-8")
    result = run_pipeline([extract, package], db_path=db)
    assert result == {"extract": "ran", "package": "ran"}
    assert out.read_text(encoding="utf-8") == "CHANGED INPUT"


def test_runner_reruns_when_output_tampered(tmp_path):
    db = tmp_path / "spine_test.db"
    raw, mid, out, extract, package = _make_chain(tmp_path)
    run_pipeline([extract, package], db_path=db)

    out.write_text("tampered", encoding="utf-8")  # break recorded output hash
    result = run_pipeline([extract, package], db_path=db)
    assert result["extract"] == "skipped"
    assert result["package"] == "ran"
    assert out.read_text(encoding="utf-8") == "HELLO SPINE"


def test_runner_output_contract(tmp_path):
    db = tmp_path / "spine_test.db"
    ghost = tmp_path / "never_written.txt"
    bad = Stage("bad", lambda: None, inputs=[], outputs=[ghost])
    with pytest.raises(StageFailed, match="output contract"):
        run_pipeline([bad], db_path=db)
    conn = connect(db)
    row = conn.execute("SELECT status FROM stage_runs WHERE stage_name='bad'").fetchone()
    conn.close()
    assert row["status"] == "failed"


def test_toposort_orders_producers_first(tmp_path):
    raw, mid, out, extract, package = _make_chain(tmp_path)
    ordered = _toposort([package, extract])  # deliberately reversed
    assert [s.name for s in ordered] == ["extract", "package"]


def test_toposort_detects_cycle(tmp_path):
    a_path, b_path = tmp_path / "a", tmp_path / "b"
    a = Stage("a", lambda: None, inputs=[b_path], outputs=[a_path])
    b = Stage("b", lambda: None, inputs=[a_path], outputs=[b_path])
    with pytest.raises(ValueError, match="cycle"):
        _toposort([a, b])


def test_runner_records_lineage_and_artifacts(tmp_path):
    db = tmp_path / "spine_test.db"
    raw, mid, out, extract, package = _make_chain(tmp_path)
    run_pipeline([extract, package], db_path=db)
    conn = connect(db)
    parents = {
        r["parent_path"]
        for r in conn.execute("SELECT parent_path FROM lineage WHERE child_path = ?", (str(out),))
    }
    artifact = conn.execute("SELECT kind FROM artifacts WHERE path = ?", (str(out),)).fetchone()
    conn.close()
    assert str(mid) in parents
    assert artifact["kind"] == "stage_output"


# ---------- ingest ----------

def _write_fixture_trace(run_dir: Path, key: str, barcode: str, score: float, grade: str,
                         bsip1_path: Path):
    product_dir = run_dir / "products" / key
    product_dir.mkdir(parents=True)
    (product_dir / "bsip2_trace.json").write_text(json.dumps({
        "bsip2_version": "proto_v0",
        "algorithm_version": "0.4.1",
        "input_reference": {
            "canonical_product_id": key,
            "barcode": barcode,
            "product_name_he": "מוצר בדיקה",
            "brand": "טסט",
            "bsip1_source_path": str(bsip1_path),
        },
        "category": "dairy_protein",
        "nova_proxy": 2,
        "confidence_band": "high",
        "confidence_score": 0.9,
        "final_score_estimate": score,
        "grade_estimate": grade,
    }, ensure_ascii=False), encoding="utf-8")


def test_ingest_bsip2_run(tmp_path):
    db = tmp_path / "spine_test.db"
    bsip1 = tmp_path / "bsip1_rec.json"
    bsip1.write_text("{}", encoding="utf-8")
    run_dir = tmp_path / "bsip2_outputs" / "run_test_001"
    _write_fixture_trace(run_dir, "p1", "111", 82.0, "A", bsip1)
    _write_fixture_trace(run_dir, "p2", "222", 51.5, "C", bsip1)

    conn = connect(db)
    n = ingest_bsip2_run(conn, run_dir)
    conn.commit()
    assert n == 2

    scores = conn.execute(
        "SELECT product_key, score, grade FROM scores WHERE run_id='run_test_001' ORDER BY product_key"
    ).fetchall()
    assert [(r["product_key"], r["score"], r["grade"]) for r in scores] == [
        ("p1", 82.0, "A"), ("p2", 51.5, "C"),
    ]
    run = conn.execute("SELECT layer, engine FROM runs WHERE run_id='run_test_001'").fetchone()
    assert run["layer"] == "bsip2" and run["engine"] == "proto_v0/0.4.1"
    lineage = conn.execute(
        "SELECT COUNT(*) FROM lineage WHERE parent_path = ?", (str(bsip1),)
    ).fetchone()[0]
    conn.close()
    assert lineage == 2  # both traces derive from the bsip1 record


def test_ingest_frontend_dir(tmp_path):
    db = tmp_path / "spine_test.db"
    data_dir = tmp_path / "comparisons"
    data_dir.mkdir()
    (data_dir / "testcat_frontend_v9.json").write_text(json.dumps({
        "_meta": {"category": "testcat", "version": "v9", "run_id": "run_test_001",
                  "product_count": 2, "generated": "2026-06-11T00:00:00Z"},
        "products": [{"id": 1}, {"id": 2}],
    }), encoding="utf-8")
    (data_dir / "legacy_frontend_v1.json").write_text(json.dumps([{"id": 1}]), encoding="utf-8")

    conn = connect(db)
    n = ingest_frontend_dir(conn, data_dir)
    conn.commit()
    assert n == 2

    tagged = conn.execute(
        "SELECT category, version, run_id, product_count FROM live_state WHERE data_file LIKE '%testcat%'"
    ).fetchone()
    assert (tagged["category"], tagged["version"], tagged["run_id"], tagged["product_count"]) == \
        ("testcat", "v9", "run_test_001", 2)
    legacy = conn.execute(
        "SELECT run_id, product_count FROM live_state WHERE data_file LIKE '%legacy%'"
    ).fetchone()
    assert legacy["run_id"] is None and legacy["product_count"] == 1
    frontend_run = conn.execute(
        "SELECT category FROM runs WHERE run_id='run_test_001' AND layer='frontend'"
    ).fetchone()
    conn.close()
    assert frontend_run["category"] == "testcat"
