"""Project Spine1 (TASK-252, Phase 2) — the yogurts pipeline as a declared DAG.

Declares the REAL run_yogurt_006 chain as Spine stages:

    bsip0 raw scrape + BSIP1 builder script
        -> [yogurt_bsip1_006]    88 BSIP1 records
        -> [yogurt_bsip2_006]    89 BSIP2 traces        (engine: score_engine.py)
        -> [yogurt_frontend_006] staging frontend JSON  (builder: build_yogurts_frontend_v006.py)

Two modes:

  IMPORT (default, the only mode allowed today):
      Adopts the EXISTING artifacts into the spine — stage fns are no-ops, the
      runner verifies every declared output exists, hashes all inputs/outputs,
      and records full lineage. From now on, if any input drifts (a trace
      regenerated, the engine edited), the affected stages report as stale.
      Nothing on disk is modified. This respects the TASK-249/250 hold:
      run_006 artifacts are pending owner sign-off + QA baseline freeze and
      MUST NOT be regenerated.

  EXECUTE (--execute, LOCKED):
      Would invoke the real scripts via subprocess. Refused until the TASK-250
      Ruling 3 owner sign-off + QA freeze land (see TASK-249 pre-go-live gate).

Usage:
  python spine_yogurts.py            # import/verify mode
  python spine_yogurts.py --execute  # refused while the go-live hold is active
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from runner import Stage, run_pipeline

REPO = Path(__file__).resolve().parents[2]

BSIP0_RAW = REPO / "02_products/yogurt_system/bsip0/yogurt_bsip0_raw_20260611T072535.json"
BSIP1_BUILDER = REPO / "03_operations/bsip0/scrape/shufersal_yogurt/02_build_bsip1_yogurt_006.py"
BSIP1_OUT_DIR = REPO / "03_operations/bsip1/run_yogurt_006/output"
BSIP2_RUNNER = REPO / "03_operations/bsip2/proto_v0/src/batch_run_yogurt_006.py"
SCORE_ENGINE = REPO / "03_operations/bsip2/proto_v0/src/score_engine.py"
TRACES_DIR = REPO / "02_products/yogurt_system/bsip2_outputs/run_yogurt_006/products"
FRONTEND_BUILDER = REPO / "02_products/yogurt_system/build_yogurts_frontend_v006.py"
STAGING_JSON = REPO / "02_products/yogurt_system/yogurts_frontend_v006_staging.json"

EXECUTE_LOCKED_REASON = (
    "EXECUTE mode is LOCKED: run_yogurt_006 artifacts are pending TASK-250 Ruling 3 "
    "owner sign-off and QA baseline freeze (TASK-249 pre-go-live gate). Regenerating "
    "them would mutate pending-verification artifacts. Use import mode."
)


def build_stages() -> list[Stage]:
    bsip1_records = sorted(BSIP1_OUT_DIR.glob("bsip1_*.json"))
    traces = sorted(TRACES_DIR.glob("*/bsip2_trace.json"))
    if not bsip1_records or not traces:
        sys.exit("run_yogurt_006 artifacts not found — nothing to declare")

    noop = lambda: None  # import mode: adopt existing outputs, verify + hash only
    return [
        Stage(
            "yogurt_bsip1_006",
            noop,
            inputs=[BSIP0_RAW, BSIP1_BUILDER],
            outputs=bsip1_records,
            code_version="task249",
        ),
        Stage(
            "yogurt_bsip2_006",
            noop,
            inputs=[*bsip1_records, BSIP2_RUNNER, SCORE_ENGINE],
            outputs=traces,
            code_version="task249+task250",
        ),
        Stage(
            "yogurt_frontend_006_staging",
            noop,
            inputs=[*traces, FRONTEND_BUILDER],
            outputs=[STAGING_JSON],
            code_version="task249+task250",
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Yogurts run_006 pipeline under Spine")
    parser.add_argument("--execute", action="store_true",
                        help="run the real scripts (LOCKED while go-live hold is active)")
    parser.add_argument("--db", default=None)
    args = parser.parse_args()

    if args.execute:
        sys.exit(EXECUTE_LOCKED_REASON)

    stages = build_stages()
    declared = {s.name: (len(s.inputs), len(s.outputs)) for s in stages}
    results = run_pipeline(stages, db_path=args.db)
    print("yogurts run_006 DAG under Spine (import/verify mode):")
    for name, status in results.items():
        ins, outs = declared[name]
        print(f"  {name:32s} {status:8s} inputs={ins:3d} outputs={outs}")
    stale = [n for n, s in results.items() if s == "ran"]
    if stale:
        print("note: 'ran' in import mode = state adopted/re-verified (inputs changed or first import)")
    else:
        print("all stages current: no input has drifted since last import")


if __name__ == "__main__":
    main()
