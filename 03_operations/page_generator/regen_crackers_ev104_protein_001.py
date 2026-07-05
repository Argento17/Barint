#!/usr/bin/env python3
"""
regen_crackers_ev104_protein_001.py — EV-104 production implementation.

TASK-516/517 follow-up. Adds a category-relative protein scale for
category="cracker" (PROTEIN_SCALE_TABLES["cracker"] in constants.py), fixing
the compression bug where crackers/ricecakes fell back to the generic
"default" curve calibrated for 20-25g/100g supplement-style protein foods.

Approval chain (see 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md,
"EV-104"): Nutrition Agent proposed -> Product Agent D7 co-signed WITH CONDITIONS
-> Data Agent pilot (batch_run_crackers_ricecakes_ev104_protein_pilot.py) reconciled
the crosser count -> Nutrition cleared the one cap-clip -> Adversarial QA gave final
Condition-5 sign-off (306-product cross-category isolation check, zero non-cracker
movement).

This script does NOT re-run generate_page.py against a config (the shared
configs/crackers.json only lists corpus_dirs=[run_crackers_conform_001], not
the run_ricecakes_conform_001 pool merged into the live page under TASK-516 --
there is no single generator config covering the full 53-product corpus).
Instead it:

  1. Reads the freshly-written BSIP2 traces from BOTH production run dirs
     (run_crackers_conform_001 + run_ricecakes_conform_001 -- written by
     batch_run_crackers_conform_001.py / batch_run_ricecakes_conform_001.py,
     which must be run FIRST, with constants.py's new "cracker" row active).
  2. Loads the live, two-gate-signed-off crackers_frontend_v1.json.
  3. For each live product (by barcode), overwrites ONLY score/grade from the
     fresh trace. rank is recomputed (score desc, barcode asc tiebreak --
     same convention as finalize_crackers_v1_structure.py). Every other field
     (rowVerdict, insightLine, expansion.*, confidence_*, brand, name,
     imageUrl, retailer, id, _website_cluster, d4_additives,
     source_traceability_status) is left byte-identical -- this copy was
     confirmed by Product/Nutrition/QA to contain no grade-letter-specific
     language before this run (see EV-104 registry entry + this task's RT-1
     resolution note).
  4. Grade is taken from the trace's own `grade_estimate` (assembled by
     trace_writer.py from score_engine.py's score_product()), NOT
     recomputed independently -- confirmed identical to the floor-boundary
     policy (01_framework/governance/grade_boundary_policy_v1.json) by
     spot-check against the batch runner's printed output.
  5. Updates _meta with an EV-104 implementation record (crossers, deltas,
     distributions) without touching any other _meta key.
  6. Does NOT commit. Writes in place to the live path; orchestrator reviews
     and commits.

No copy authored. No score computed here -- scores/grades come straight from
the BSIP2 traces on disk.
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Bari")
LIVE_JSON = ROOT / "bari-web/src/data/comparisons/crackers_frontend_v1.json"

TRACE_DIRS = [
    ROOT / "02_products/crackers/bsip2_outputs/run_crackers_conform_001/products",
    ROOT / "02_products/crackers/bsip2_outputs/run_ricecakes_conform_001/products",
]

EVIDENCE_ID = "EV-104"
TASK = "TASK-516/517 follow-up"


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)


def load_traces_by_barcode(trace_dirs: list[Path]) -> dict[str, dict]:
    traces: dict[str, dict] = {}
    dupes: list[str] = []
    for tdir in trace_dirs:
        if not tdir.is_dir():
            raise FileNotFoundError(f"Trace dir missing: {tdir}")
        for pdir in sorted(tdir.iterdir()):
            if not pdir.is_dir():
                continue
            trace_path = pdir / "bsip2_trace.json"
            if not trace_path.is_file():
                continue
            trace = load_json(trace_path)
            bc = str(
                (trace.get("input_reference") or {}).get("barcode", "")
                or trace.get("barcode", "")
            ).strip()
            if not bc:
                continue
            if bc in traces:
                dupes.append(bc)
            traces[bc] = trace
    if dupes:
        print(f"WARNING: duplicate barcodes across trace dirs: {dupes}")
    return traces


def score_dist(scores: list[float]) -> dict:
    if not scores:
        return {}
    return {
        "count": len(scores),
        "min": min(scores),
        "max": max(scores),
        "median": statistics.median(scores),
        "mean": round(statistics.mean(scores), 3),
        "stdev": round(statistics.pstdev(scores), 3) if len(scores) > 1 else 0.0,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    print(f"=== {EVIDENCE_ID} production implementation: crackers protein scale ===")

    print(f"\n[1] Loading fresh BSIP2 traces from {len(TRACE_DIRS)} dirs...")
    traces = load_traces_by_barcode(TRACE_DIRS)
    print(f"    Traces loaded: {len(traces)}")

    print(f"\n[2] Loading live page: {LIVE_JSON}")
    live = load_json(LIVE_JSON)
    products = live["products"]
    print(f"    Live products: {len(products)}")

    old_grade_dist = dict(sorted(Counter(p.get("grade") for p in products).items()))
    old_scores = [p["score"] for p in products if p.get("score") is not None]
    old_dist = score_dist(old_scores)

    print("\n[3] Applying fresh score/grade from traces (copy fields untouched)...")
    crossers = []
    unmatched = []
    unchanged = 0

    for p in products:
        bc = str(p.get("barcode", "")).strip()
        trace = traces.get(bc)
        if trace is None:
            unmatched.append(bc)
            continue
        old_score = p.get("score")
        old_grade = p.get("grade")
        new_score = trace.get("final_score_estimate")
        new_grade = trace.get("grade_estimate")

        p["score"] = new_score
        p["grade"] = new_grade

        if old_grade != new_grade:
            crossers.append({
                "barcode": bc,
                "name": p.get("nameHe"),
                "old_score": old_score,
                "old_grade": old_grade,
                "new_score": new_score,
                "new_grade": new_grade,
                "delta": None if (old_score is None or new_score is None)
                else round(new_score - old_score, 3),
            })
        elif old_score == new_score:
            unchanged += 1

    if unmatched:
        print(f"    ERROR: {len(unmatched)} live products have no fresh trace: {unmatched}")
        return 1

    print(f"    Grade crossers: {len(crossers)}")
    for c in crossers:
        print(f"      {c['barcode']} {c['old_grade']}->{c['new_grade']}  "
              f"score {c['old_score']}->{c['new_score']}  delta={c['delta']}")
    print(f"    Unchanged (score+grade identical): {unchanged}")

    print("\n[4] Recomputing rank (score desc, barcode asc tiebreak)...")

    def sort_key(prod):
        s = prod.get("score")
        return (0 if s is None else -s, prod.get("barcode", ""))

    products_sorted = sorted(products, key=sort_key)
    for i, p in enumerate(products_sorted, start=1):
        p["rank"] = i
    live["products"] = products_sorted

    new_grade_dist = dict(sorted(Counter(p.get("grade") for p in products_sorted).items()))
    new_scores = [p["score"] for p in products_sorted if p.get("score") is not None]
    new_dist = score_dist(new_scores)

    print(f"    Grade dist OLD: {old_grade_dist}")
    print(f"    Grade dist NEW: {new_grade_dist}")
    print(f"    Score dist OLD: {old_dist}")
    print(f"    Score dist NEW: {new_dist}")

    print("\n[5] Updating _meta with EV-104 implementation record...")
    meta = live["_meta"]
    meta["ev104_protein_scale_implementation"] = {
        "evidence_id": EVIDENCE_ID,
        "task": TASK,
        "date": "2026-07-05",
        "change": (
            "Added PROTEIN_SCALE_TABLES['cracker'] to constants.py -- crackers/"
            "ricecakes previously fell back to the 'default' supplement-calibrated "
            "curve, compressing genuine 16g/100g seed-and-legume products into the "
            "bottom third of the protein dimension. No new dimension or code path -- "
            "a data addition to a table lookup_protein_scale() already reads."
        ),
        "approval_chain": (
            "Nutrition Agent proposed -> Product Agent D7 co-signed WITH CONDITIONS "
            "-> Data Agent pilot (54-product isolated run) reconciled crosser count "
            "-> Nutrition cleared 1 cap-clip case -> Adversarial QA Condition-5 "
            "sign-off (306-product cross-category isolation check, zero non-cracker "
            "movement)."
        ),
        "grade_crossers_count": len(crossers),
        "grade_crossers": crossers,
        "grade_distribution_old": old_grade_dist,
        "grade_distribution_new": new_grade_dist,
        "score_distribution_old": old_dist,
        "score_distribution_new": new_dist,
        "copy_touched": False,
        "copy_note": (
            "rowVerdict/insightLine/expansion.* left byte-identical for all 53 "
            "products, including all 13 crossers -- reviewed before this run and "
            "confirmed to describe product composition (percentages, sodium, "
            "fiber, protein, additive counts), never a specific grade letter or "
            "rank-band claim that a grade move would falsify."
        ),
        "source_run_ids": ["run_crackers_conform_001", "run_ricecakes_conform_001"],
        "engine_source": "03_operations/bsip2/proto_v0/src/constants.py (on-disk, not a monkey-patch)",
    }

    print(f"\n[6] Writing merged output to: {LIVE_JSON}")
    write_json(LIVE_JSON, live)
    print(f"    Written ({LIVE_JSON.stat().st_size} bytes)")

    print("\n=== SUMMARY ===")
    print(f"Products: {len(products_sorted)}")
    print(f"Grade crossers: {len(crossers)}")
    print(f"Grade dist NEW: {new_grade_dist}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
