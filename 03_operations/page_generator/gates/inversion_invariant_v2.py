#!/usr/bin/env python3
"""
inversion_invariant_v2.py — BARI-INVERSION-TEST-001 (dimension-based, TASK-395 follow-up)
============================================================================================
SCORE-NEUTRAL: adds a check, changes NO scores, NO scoring logic.

WHY V2 EXISTS (diagnosis, 2026-07-01, brined_cheeses run):
  The v1 gate (inversion_invariant.py) tests dominance over a 4-signal PANEL
  (sugars_g, fat_saturated_g, red_label_count, fat_source_tier). Against the
  brined_cheeses run it fired 6 "inversions." All 6 were FALSE POSITIVES: in
  every firing pair the higher-scored product was strictly BETTER than the
  lower-scored one on nutrient_density, protein_quality, additive_quality,
  whole_food_integrity and/or processing_quality — axes the 4-signal panel
  cannot see because sodium and protein (the two signals that actually drive
  brined-cheese scores) are not in it. A guardrail that fires on legitimate
  low-sodium / high-protein orderings is worse than no guardrail: it teaches
  engineers to distrust or bypass it.

  The same corpus-wide sweep also found the OPPOSITE failure mode: the panel
  gate MISSED 17 pairs where the higher-scored product is worse-or-equal on
  EVERY ONE of the engine's 10 dimension_scores axes (calorie_density,
  fat_quality, glycemic_quality, satiety_support, nutrient_density,
  protein_quality unrecognized because none crossed the panel's fixed
  4-signal/3-of-4 threshold). Example: 7290011499051 ("גבינה פטה כבשים 20%",
  score 71.6) outranks 48413 ("גבינה מלוחה חמד16%", score 66.3) while scoring
  worse-or-equal on ALL 10 dimensions (strictly worse on nutrient_density,
  protein_quality, satiety_support, fat_quality) — a real, engine-native
  inversion the panel gate cannot detect because it doesn't sample those axes.

  Conclusion: a FIXED signal panel is the wrong abstraction for a
  category-agnostic dominance guardrail. It will always be either too narrow
  (false positives when the category's real drivers sit outside the panel,
  as in brined cheeses) or too narrow in the other direction (false negatives
  when a real inversion happens on axes the panel didn't anticipate). The
  panel would need re-tuning per category — which defeats the purpose of a
  guardrail meant to hold OFF and ON across every category, forever.

THE V2 PREDICATE (dimension-based, engine-native, category-agnostic):
  For any two eligible products A, B in the same scored run:
    Order by final_score_estimate; A = higher-scored, B = lower-scored (strict,
    ties excluded — same as v1).
    A INVERSION fires iff A is worse-or-equal to B on EVERY entry in
    `dimension_scores`, AND strictly worse on AT LEAST ONE entry.
    (I.e., B weakly-Pareto-dominates A on the engine's own 10-axis panel, yet
    A ranks above B in the published/candidate score.)

  This is the textbook Pareto-dominance definition applied to the engine's OWN
  computed axes rather than a hand-picked subset of raw label fields. It uses
  exactly the granularity the scoring model itself reasons in (dimension_scores
  is Stage 3 of score_engine.py, upstream of caps/penalties/floors), so it
  cannot false-positive from a missing panel signal — every one of the 10 axes
  is present on every scored product by construction (score_product always
  computes DIMENSION_WEIGHTS.keys()). It is category-agnostic: the dimension
  set and weights come from the trace itself (dimension_weights may vary by
  category/flag; this predicate reads them from the record, never assumes the
  global constant), so no category needs a bespoke panel.

  IMPORTANT — this predicate is deliberately silent on WHY a dimension-dominant
  product can still legitimately outscore its dominator in edge cases that are
  NOT inversions: caps_applied / penalties_applied / floors_applied are
  downstream ENGINE DECISIONS (e.g. a NOVA processing cap, a sodium-load
  penalty), not signals the dominance predicate should second-guess. The
  predicate operates on dimension_scores (pre-cap, pre-penalty) precisely
  because that is the engine's untainted judgment of "how good is this
  product on each axis" — if a downstream cap/penalty/floor then legitimately
  changes the ranking, that is the engine's scoring philosophy operating as
  designed, not a dominance violation. A true inversion is when NOTHING in the
  engine's own dimension judgment favors A, yet A still outranks B after the
  full pipeline.

  Edge rules:
    - Equal value on a dimension = neutral (counted in neither worse nor better).
    - A dimension missing from EITHER product's dimension_scores is skipped
      (never treated as a win/loss) — this can only happen if dimension_weights
      differ structurally between the two (e.g. a future category-specific
      dimension set); if the intersection is empty, the pair is SKIPPED
      (not a fire) and logged as an eligibility gap for review.
    - confidence_band == "insufficient" on either product: excluded from the
      HARD gate; logged as SUSPECTED (WARN), same policy as v1.
    - final_score_estimate == None or evaluation_status == "out_of_scope":
      excluded entirely, same as v1.
    - A FAIL = >= 1 inversion pair fires in the hard-gate pool.

  Deliberately NOT re-added: a raw-signal panel. Deliberately NOT added: any
  attempt to weight dimensions by dimension_weights before comparing — the
  fire decision is about ORDINAL dominance (worse-or-equal on every axis),
  which is weight-independent by construction (Pareto dominance holds under
  ANY monotonic weighting, so it doesn't matter that weights differ slightly
  by category/flag — see rationale doc for proof sketch).

Usage (standalone):
  python inversion_invariant_v2.py --run <bsip2_products_dir>
      [--out <report.json>]
      [--exit-zero-on-warn]

Exit codes:
  0 = no inversion pairs fired (PASS)
  1 = >= 1 inversion pair fired (FAIL)
  2 = usage / load error

Integration with run_gates.py:
  from inversion_invariant_v2 import gate_inversion_invariant_v2
  gates.append(gate_inversion_invariant_v2(traces.values()))
  # traces.values() is exactly the list[dict] produced by load_bsip2_traces(run_dir)
  # already used for gate_grade_integrity — no new loader needed.

Coexistence with the reframed fixture test
(C:/bari_p277/03_operations/bsip2/proto_v0/src/test_bari_inversion_001.py):
  That fixture asserts a SINGLE pinned pair (74184 vs 61245, cookies) stays
  non-inverted under both BARI_PROC_CONTINUOUS_V1 states — a fast regression
  tripwire for CI. It should be SUPERSEDED at the predicate level (swap its
  inline `a_nutritionally_worse_than_b` mirror for this module's
  `dimension_dominance_fires`, import via sys.path exactly as it already
  imports score_engine/signal_extractor/etc.) but COEXIST at the test level —
  keep it as a fast single-pair CI smoke test; it is not a substitute for the
  corpus-wide gate here, which needs a full run directory and is meant to run
  in run_gates.py / the activation harness, not as a standalone pytest-style
  fixture. Recommendation: rename its predicate import so both share ONE
  source of truth (this module) instead of two hand-maintained copies of the
  same logic drifting apart — that drift is exactly what caused v1's panel to
  go stale.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

GATE_ID = "9 INVERSION-INVARIANT-V2-DIMENSION"


# ---------------------------------------------------------------------------
# Dominance predicate
# ---------------------------------------------------------------------------

def dimension_dominance_fires(dims_a: dict, dims_b: dict) -> tuple[bool, list[str], list[str], list[str]]:
    """
    Pareto-dominance predicate over the engine's own dimension_scores.

    A INVERSION fires iff A (higher-scored) is worse-or-equal to B on EVERY
    shared dimension, AND strictly worse on at least one.

    Returns:
      fires        - True if B weakly-Pareto-dominates A (an inversion)
      worse_on     - dimensions where A < B  (evidence for the inversion)
      better_on    - dimensions where A > B  (any entry here means NO fire —
                       A has at least one legitimate edge over B)
      skipped      - dimensions present in only one of the two records
                       (excluded from the comparison; logged for transparency)
    """
    keys_a = set(dims_a.keys())
    keys_b = set(dims_b.keys())
    shared = keys_a & keys_b
    skipped = sorted(keys_a.symmetric_difference(keys_b))

    worse_on: list[str] = []
    better_on: list[str] = []

    for k in sorted(shared):
        va = _num_or_none(dims_a.get(k))
        vb = _num_or_none(dims_b.get(k))
        if va is None or vb is None:
            skipped.append(k)
            continue
        if va > vb:
            better_on.append(k)
        elif va < vb:
            worse_on.append(k)
        # equal -> neutral, contributes to neither list

    if not shared or len(shared) == len(skipped):
        # No comparable dimensions at all — cannot judge dominance either way.
        return False, worse_on, better_on, skipped

    fires = (len(better_on) == 0) and (len(worse_on) >= 1)
    return fires, worse_on, better_on, skipped


def _num_or_none(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Record helpers (shared conventions with v1 — kept identical for parity)
# ---------------------------------------------------------------------------

def get_product_id(trace: dict) -> str:
    ref = trace.get("input_reference") or {}
    bc = str(ref.get("barcode", "")).strip()
    name = str(ref.get("product_name_he", "")).strip()
    pid = ref.get("canonical_product_id", "")
    if name:
        return f"{bc} ({name})"
    return bc or pid or "(unknown)"


def get_barcode(trace: dict) -> str:
    ref = trace.get("input_reference") or {}
    return str(ref.get("barcode", "")).strip()


def load_traces_from_run_dir(run_dir: Path) -> list[dict]:
    """Identical loader contract to v1 (flat bsip2_trace_*.json or nested subdir/bsip2_trace.json)."""
    traces: list[dict] = []
    if not run_dir.is_dir():
        print(f"ERROR: run directory not found: {run_dir}", file=sys.stderr)
        return traces
    for entry in sorted(run_dir.iterdir()):
        if entry.is_file() and entry.name.startswith("bsip2_trace_") and entry.suffix == ".json":
            try:
                traces.append(json.loads(entry.read_text(encoding="utf-8")))
            except Exception as exc:
                print(f"WARN: could not load {entry.name}: {exc}", file=sys.stderr)
        elif entry.is_dir():
            trace_file = entry / "bsip2_trace.json"
            if trace_file.is_file():
                try:
                    traces.append(json.loads(trace_file.read_text(encoding="utf-8")))
                except Exception as exc:
                    print(f"WARN: could not load {trace_file}: {exc}", file=sys.stderr)
    return traces


# ---------------------------------------------------------------------------
# GateResult — duplicated minimal shim so this module has no import-time
# dependency on run_gates.py. If run_gates.GateResult is available at call
# site, gate_inversion_invariant_v2 can be called with a foreign GateResult
# class too (only .fail/.warn/.info/.skip/.header()/.lines/.status are used).
# ---------------------------------------------------------------------------

class GateResult:
    def __init__(self, name):
        self.name = name
        self.status = "PASS"
        self.lines: list[str] = []

    def fail(self, msg):
        self.status = "FAIL"
        self.lines.append(f"  FAIL: {msg}")

    def warn(self, msg):
        if self.status == "PASS":
            self.status = "WARN"
        self.lines.append(f"  WARN: {msg}")

    def info(self, msg):
        self.lines.append(f"  INFO: {msg}")

    def skip(self, msg):
        self.status = "SKIP"
        self.lines.append(f"  SKIP: {msg}")

    def header(self):
        return f"[{self.status}] G{self.name}"


# ---------------------------------------------------------------------------
# Gate entry point
# ---------------------------------------------------------------------------

def gate_inversion_invariant_v2(traces: list[dict]) -> GateResult:
    """
    Run BARI-INVERSION-TEST-001 (dimension-based) on a list of BSIP2 trace
    records from the same scored run. Flag-agnostic by construction — it
    reads final_score_estimate and dimension_scores, whatever scoring flags
    produced them; it does not branch on any BARI_* env var itself.
    """
    g = GateResult(GATE_ID)

    eligible: list[dict] = []
    excluded_null_score = 0
    excluded_out_of_scope = 0
    for t in traces:
        if t.get("final_score_estimate") is None:
            excluded_null_score += 1
            continue
        if t.get("evaluation_status") == "out_of_scope":
            excluded_out_of_scope += 1
            continue
        eligible.append(t)

    g.info(f"Total traces loaded: {len(traces)}")
    g.info(f"Excluded (null score): {excluded_null_score}")
    g.info(f"Excluded (out_of_scope): {excluded_out_of_scope}")
    g.info(f"Eligible for inversion check: {len(eligible)}")

    if len(eligible) < 2:
        g.skip("Fewer than 2 eligible products — inversion check not applicable")
        return g

    hard_eligible: list[dict] = []
    suspected: list[dict] = []
    missing_dims: list[dict] = []
    for t in eligible:
        if not t.get("dimension_scores"):
            missing_dims.append(t)
            continue
        cb = (t.get("confidence_band") or "").strip().lower()
        (suspected if cb == "insufficient" else hard_eligible).append(t)

    g.info(f"Hard-gate eligible (confidence_band != insufficient, dimension_scores present): {len(hard_eligible)}")
    g.info(f"Suspected-only (confidence_band == insufficient, logged WARN): {len(suspected)}")
    if missing_dims:
        g.warn(f"{len(missing_dims)} eligible trace(s) had NO dimension_scores — excluded from "
               f"the dimension gate entirely (cannot Pareto-compare); ids: "
               f"{[get_product_id(t) for t in missing_dims]}")

    hard_pairs = _find_inversion_pairs(hard_eligible)
    firing_pairs = [p for p in hard_pairs if p["fires"]]

    g.info(f"Total ordered pairs checked (hard): {len(hard_pairs)}")
    g.info(f"Inversion pairs firing (FAIL): {len(firing_pairs)}")
    g.info(f"Non-firing pairs: {len(hard_pairs) - len(firing_pairs)}")

    for pair in firing_pairs:
        g.fail(
            "INVERSION: A(higher-scored) is dimension-dominated by B(lower-scored) "
            "on the engine's own dimension_scores\n"
            f"    A(higher rank): id={pair['a_id']} | score={pair['a_score']}\n"
            f"    B(lower rank):  id={pair['b_id']} | score={pair['b_score']}\n"
            f"    A worse on ({len(pair['worse_on'])} dimensions): {pair['worse_on']}\n"
            f"    A better on: {pair['better_on'] or '(none -- full inversion)'}\n"
            f"    A dimension_scores: {pair['dims_a']}\n"
            f"    B dimension_scores: {pair['dims_b']}"
        )

    # Suspected pool — same pairwise check, WARN-only, never blocks.
    if suspected:
        susp_pool = hard_eligible + suspected
        susp_pairs = _find_inversion_pairs(susp_pool, only_involving=suspected)
        susp_firing = [p for p in susp_pairs if p["fires"]]
        for pair in susp_firing:
            g.warn(
                f"SUSPECTED (confidence_band=insufficient on one side): "
                f"A(higher)={pair['a_id']} score={pair['a_score']} vs "
                f"B(lower)={pair['b_id']} score={pair['b_score']} "
                f"A-worse-on={pair['worse_on']}"
            )

    if not firing_pairs and g.status == "PASS":
        g.info("No inversion pairs found — gate PASS")

    return g


def _find_inversion_pairs(products: list[dict], only_involving: list[dict] | None = None) -> list[dict]:
    """
    Enumerate ordered (A=higher, B=lower) pairs by final_score_estimate
    (strict; ties skipped) and test dimension_dominance_fires on each.

    If only_involving is given, restrict to pairs where at least one product
    is in that set (used for the suspected-pool WARN pass, to avoid
    re-flagging pairs already covered by the hard pool).
    """
    only_ids = {id(t) for t in only_involving} if only_involving else None
    pairs: list[dict] = []
    n = len(products)
    for i in range(n):
        for j in range(i + 1, n):
            t1, t2 = products[i], products[j]
            if only_ids is not None and id(t1) not in only_ids and id(t2) not in only_ids:
                continue
            s1 = t1.get("final_score_estimate") or 0
            s2 = t2.get("final_score_estimate") or 0
            if s1 == s2:
                continue
            t_a, t_b = (t1, t2) if s1 > s2 else (t2, t1)
            score_a, score_b = (s1, s2) if s1 > s2 else (s2, s1)

            dims_a = t_a.get("dimension_scores") or {}
            dims_b = t_b.get("dimension_scores") or {}
            fires, worse_on, better_on, skipped = dimension_dominance_fires(dims_a, dims_b)

            pairs.append({
                "fires": fires,
                "a_id": get_product_id(t_a),
                "b_id": get_product_id(t_b),
                "a_score": score_a,
                "b_score": score_b,
                "dims_a": dims_a,
                "dims_b": dims_b,
                "worse_on": worse_on,
                "better_on": better_on,
                "skipped_dims": skipped,
            })
    return pairs


# ---------------------------------------------------------------------------
# Standalone CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="BARI-INVERSION-TEST-001 v2: dimension-based dominance gate"
    )
    parser.add_argument("--run", required=True, help="Path to BSIP2 run products directory")
    parser.add_argument("--out", default=None, help="Optional path to write JSON report")
    parser.add_argument("--exit-zero-on-warn", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run)
    traces = load_traces_from_run_dir(run_dir)
    if not traces:
        print(f"ERROR: no trace files found in: {run_dir}", file=sys.stderr)
        return 2

    print(f"Loaded {len(traces)} trace records from {run_dir}", file=sys.stderr)

    g = gate_inversion_invariant_v2(traces)

    print(g.header())
    for line in g.lines:
        print(line)
    print()

    if args.out:
        report = {"gate": GATE_ID, "status": g.status, "run_dir": str(run_dir), "lines": g.lines}
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Report written to: {args.out}", file=sys.stderr)

    if g.status == "FAIL":
        return 1
    if g.status == "WARN" and not args.exit_zero_on_warn:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
