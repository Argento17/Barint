#!/usr/bin/env python3
"""
inversion_invariant.py — BARI-INVERSION-TEST-001
=================================================
Deterministic within-category nutritional-dominance guardrail.

SCORE-NEUTRAL: adds a check, changes NO scores, NO scoring logic.

Predicate (corrected 2026-06-24, TASK-395 follow-up):
  For any two products A, B in the same scored shelf / run directory,
  flag an INVERSION when ALL hold:
    (i)   same category corpus (both loaded from the same --run directory)
    (ii)  score(A) > score(B)  [strict; ties excluded]
    (iii) A (higher-scored) is nutritionally WORSE than B (lower-scored):
            A is strictly worse on >= 3 of these 4 ROBUST PANEL signals
            AND not better on ANY of the 4:
              - sugars_g            (lower better)
              - fat_saturated_g     (lower better)
              - red_label_count     (lower better)
              - fat_source_tier     {whole_food=1, unspecified=2, seed_oil=3, palm_oil=4} (lower better)
    (iv)  NEITHER product has confidence_band == "insufficient"
          (excluded from hard gate; logged as SUSPECTED inversion for review)
    (v)   NEITHER product has final_score == null or evaluation_status == "out_of_scope"

  additive_marker_count is a SUPPORTING signal only: reported in output for each
  firing pair but NEVER blocks a fire and NEVER required. This is intentional —
  additive_marker_count is the most parser-fragile field (the motivating Chokita
  parser bug assigned count=2 instead of the real 4+, which vetoed the inversion
  under the old 5-signal predicate). A guardrail must not be vetoed by the signal
  it was built to protect against.

  Edge rules:
    - Equal value on a signal = neutral (no dominance, no loss).
    - fat_source_tier: palm_oil -> 4, else seed_oil -> 3,
      else ingredients present but neither -> 2, else no ingredients -> MISSING.
    - When fat_source_tier is MISSING for either product:
      dominance requires >= 2 of the remaining 3 panel signals (not 3 of 4).
    - A FAIL = >= 1 inversion pair fires.

Usage (standalone):
  python inversion_invariant.py --run <bsip2_products_dir>
      [--out <report.json>]
      [--exit-zero-on-warn]    # treat only-suspected (excluded) inversions as exit 0

Exit codes:
  0 = no inversion pairs fired (PASS)
  1 = >= 1 inversion pair fired (FAIL)
  2 = usage / load error

Output: prints each firing pair with both products' id, score, and 4 panel signal
        values plus additive_marker_count (supporting, informational only).
        Suspected inversions (confidence_band=insufficient) are logged as WARN, not FAIL.

Integration with run_gates.py:
  Import gate_inversion_invariant(products) where products is a list of dicts
  each containing the trace data. The function returns a GateResult-compatible object.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GATE_ID = "9 INVERSION-INVARIANT"

# The 4 robust panel signals used in the hard dominance predicate (lower = better on all).
# additive_marker_count is excluded from the hard predicate (parser-fragile; supporting only).
PANEL_SIGNALS = ["sugars_g", "fat_saturated_g", "red_label_count", "fat_source_tier"]

# Supporting signal: reported in output but NEVER blocks or requires a fire.
SUPPORTING_SIGNAL = "additive_marker_count"

# All signal names for display (panel + supporting)
SIGNAL_NAMES = PANEL_SIGNALS + [SUPPORTING_SIGNAL]

FAT_SOURCE_TIER_PALM   = 4
FAT_SOURCE_TIER_SEED   = 3
FAT_SOURCE_TIER_UNK    = 2  # ingredients present but neither palm nor seed
FAT_SOURCE_TIER_MISSING = None  # no ingredient data at all


# ---------------------------------------------------------------------------
# Field extraction — robust to missing fields per spec edge rules
# ---------------------------------------------------------------------------

def extract_signals(trace: dict) -> dict:
    """
    Extract the 5 inversion signals from a BSIP2 trace record.
    Returns a dict with keys matching SIGNAL_NAMES; None = missing/unknown.

    Field paths:
      sugars_g          <- L1_observed_signals.sugars_g
      fat_saturated_g   <- L1_observed_signals.fat_saturated_g
      red_label_count   <- L3_inferred_classifications.red_label_count
      fat_source_tier   <- derived from L3.has_palm_oil / has_seed_oil
                          (MISSING when ingredient list is absent)
      additive_marker_count <- L3_inferred_classifications.additive_marker_count
    """
    L1 = trace.get("L1_observed_signals") or {}
    L3 = trace.get("L3_inferred_classifications") or {}

    sugars_g = _float_or_none(L1.get("sugars_g"))
    fat_sat_g = _float_or_none(L1.get("fat_saturated_g"))
    red_label_count = _int_or_none(L3.get("red_label_count"))
    additive_marker_count = _int_or_none(L3.get("additive_marker_count"))

    # fat_source_tier derivation
    has_palm = L3.get("has_palm_oil")
    has_seed = L3.get("has_seed_oil")

    # Determine if ingredient data is present at all.
    # If both fields are absent (None, not False), treat tier as MISSING.
    if has_palm is None and has_seed is None:
        fat_tier = FAT_SOURCE_TIER_MISSING
    elif has_palm:
        fat_tier = FAT_SOURCE_TIER_PALM
    elif has_seed:
        fat_tier = FAT_SOURCE_TIER_SEED
    else:
        fat_tier = FAT_SOURCE_TIER_UNK  # ingredients present, neither oil type

    return {
        "sugars_g": sugars_g,
        "fat_saturated_g": fat_sat_g,
        "red_label_count": red_label_count,
        "fat_source_tier": fat_tier,
        "additive_marker_count": additive_marker_count,
    }


def _float_or_none(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _int_or_none(v: Any) -> int | None:
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Dominance check
# ---------------------------------------------------------------------------

def a_nutritionally_worse_than_b(sig_a: dict, sig_b: dict) -> tuple[bool, list[str], list[str], dict]:
    """
    Return (inversion_fires, a_worse_panel_signals, a_better_panel_signals, supporting_info).

    Checks whether A (the higher-scored product) is nutritionally WORSE than B
    (the lower-scored product) — i.e., the scoring ranked A above B despite A
    being nutritionally inferior on the 4 robust panel signals.

    HARD PREDICATE (4 panel signals only):
      INVERSION fires when A is strictly WORSE on >= 3 of the 4 panel signals
      AND not BETTER on ANY of the 4:
        - sugars_g, fat_saturated_g, red_label_count, fat_source_tier

    additive_marker_count is EXCLUDED from the hard predicate. It is the most
    parser-fragile signal (the motivating Chokita bug assigned count=2 instead of
    the real 4+, which vetoed the inversion under the old 5-signal predicate).
    It is returned in supporting_info for display only — it NEVER blocks a fire.

    Since higher value = worse on all 4 panel signals (lower is better):
      - sugars_g, fat_saturated_g: higher = worse
      - red_label_count, fat_source_tier: higher = worse

    "A strictly worse on signal S" means: sig_a[S] > sig_b[S]
    "A better on signal S" means: sig_a[S] < sig_b[S]
    Equal = neutral (counted in neither).

    Edge rule for fat_source_tier MISSING:
      If EITHER product's fat_source_tier is None, skip that signal entirely
      and require >= 2 of the remaining 3 panel signals for the inversion to fire.

    Returns:
      fires             - True if inversion condition met
      a_worse_sigs      - list of panel signals where A is strictly worse
      a_better_sigs     - list of panel signals where A is strictly better
                          (any entry here prevents the inversion from firing)
      supporting_info   - dict with additive_marker_count values for both products
                          (informational; not used in the fire decision)
    """
    tier_a = sig_a.get("fat_source_tier")
    tier_b = sig_b.get("fat_source_tier")
    tier_missing = (tier_a is None or tier_b is None)

    # Build the active panel signal list, skipping fat_source_tier if either is missing.
    # additive_marker_count is deliberately excluded from PANEL_SIGNALS.
    active_panel = [s for s in PANEL_SIGNALS
                    if not (s == "fat_source_tier" and tier_missing)]

    a_worse_sigs: list[str] = []
    a_better_sigs: list[str] = []

    for sig in active_panel:
        va = sig_a.get(sig)
        vb = sig_b.get(sig)

        # If either value is missing, skip this signal (treat as neutral)
        if va is None or vb is None:
            continue

        # Higher value = worse (all 4 panel signals: lower is better)
        if va > vb:
            a_worse_sigs.append(sig)   # A (higher-scored) is worse = inversion evidence
        elif va < vb:
            a_better_sigs.append(sig)  # A (higher-scored) is better = no inversion
        # Equal = neutral, not added to either list

    # Threshold: 3 of 4 panel signals, or 2 of 3 if fat_source_tier missing
    threshold = 2 if tier_missing else 3

    fires = (len(a_worse_sigs) >= threshold) and (len(a_better_sigs) == 0)

    # Supporting signal: additive_marker_count (informational only, not used in fire decision)
    supporting_info = {
        "additive_marker_count_a": sig_a.get(SUPPORTING_SIGNAL),
        "additive_marker_count_b": sig_b.get(SUPPORTING_SIGNAL),
    }

    return fires, a_worse_sigs, a_better_sigs, supporting_info


# ---------------------------------------------------------------------------
# Product loader — handles the flat bsip2_trace_<barcode>.json pattern
# AND the nested subdir bsip2_trace.json pattern used by run_gates.py
# ---------------------------------------------------------------------------

def load_traces_from_run_dir(run_dir: Path) -> list[dict]:
    """
    Load BSIP2 trace records from a run products directory.
    Supports two layouts:
      A) Flat: bsip2_trace_<barcode>.json directly in run_dir
         (used by cookies/coffee: run_cookies_task393_final/products/)
      B) Nested: <barcode>/bsip2_trace.json subdirectory layout
         (used by run_gates.py's load_bsip2_traces)

    Returns list of trace dicts. Load errors are printed to stderr and skipped.
    """
    traces: list[dict] = []

    if not run_dir.is_dir():
        print(f"ERROR: run directory not found: {run_dir}", file=sys.stderr)
        return traces

    for entry in sorted(run_dir.iterdir()):
        # Pattern A: flat JSON files named bsip2_trace_*.json
        if entry.is_file() and entry.name.startswith("bsip2_trace_") and entry.suffix == ".json":
            try:
                rec = json.loads(entry.read_text(encoding="utf-8"))
                traces.append(rec)
            except Exception as exc:
                print(f"WARN: could not load {entry.name}: {exc}", file=sys.stderr)

        # Pattern B: subdirectory containing bsip2_trace.json
        elif entry.is_dir():
            trace_file = entry / "bsip2_trace.json"
            if trace_file.is_file():
                try:
                    rec = json.loads(trace_file.read_text(encoding="utf-8"))
                    traces.append(rec)
                except Exception as exc:
                    print(f"WARN: could not load {trace_file}: {exc}", file=sys.stderr)

    return traces


def get_product_id(trace: dict) -> str:
    """Extract a human-readable product identifier from a trace record."""
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


# ---------------------------------------------------------------------------
# Gate result container (matches run_gates.py GateResult API)
# ---------------------------------------------------------------------------

class GateResult:
    def __init__(self, name: str) -> None:
        self.name = name
        self.status = "PASS"
        self.lines: list[str] = []

    def fail(self, msg: str) -> None:
        self.status = "FAIL"
        self.lines.append(f"  FAIL: {msg}")

    def warn(self, msg: str) -> None:
        if self.status == "PASS":
            self.status = "WARN"
        self.lines.append(f"  WARN: {msg}")

    def info(self, msg: str) -> None:
        self.lines.append(f"  INFO: {msg}")

    def skip(self, msg: str) -> None:
        self.status = "SKIP"
        self.lines.append(f"  SKIP: {msg}")

    def header(self) -> str:
        return f"[{self.status}] G{self.name}"


# ---------------------------------------------------------------------------
# Core gate logic
# ---------------------------------------------------------------------------

def gate_inversion_invariant(traces: list[dict]) -> GateResult:
    """
    Run BARI-INVERSION-TEST-001 on a list of BSIP2 trace records.

    All traces are assumed to be from the same scored shelf/run directory
    (same category corpus = condition i satisfied).

    Returns a GateResult with status PASS/FAIL/WARN/SKIP.
    """
    g = GateResult(GATE_ID)

    # Filter: exclude null-score and out_of_scope
    eligible: list[dict] = []
    excluded_null_score = 0
    excluded_out_of_scope = 0
    for t in traces:
        score = t.get("final_score_estimate")
        status = t.get("evaluation_status", "")
        if score is None:
            excluded_null_score += 1
            continue
        if status == "out_of_scope":
            excluded_out_of_scope += 1
            continue
        eligible.append(t)

    total = len(traces)
    g.info(f"Total traces loaded: {total}")
    g.info(f"Excluded (null score): {excluded_null_score}")
    g.info(f"Excluded (out_of_scope): {excluded_out_of_scope}")
    g.info(f"Eligible for inversion check: {len(eligible)}")

    if len(eligible) < 2:
        g.skip("Fewer than 2 eligible products — inversion check not applicable")
        return g

    # Partition by confidence_band
    hard_eligible: list[dict] = []
    suspected: list[dict] = []  # confidence_band == "insufficient"
    for t in eligible:
        cb = (t.get("confidence_band") or "").strip().lower()
        if cb == "insufficient":
            suspected.append(t)
        else:
            hard_eligible.append(t)

    g.info(f"Hard-gate eligible (confidence_band != insufficient): {len(hard_eligible)}")
    g.info(f"Suspected-only (confidence_band == insufficient, logged WARN): {len(suspected)}")

    # Precompute signals for all products
    sig_cache: dict[str, dict] = {}
    id_cache: dict[str, str] = {}
    for t in eligible:
        bc = get_barcode(t)
        sig_cache[bc] = extract_signals(t)
        id_cache[bc] = get_product_id(t)

    # --- Hard gate: pairs from hard_eligible only ---
    hard_pairs = _find_inversion_pairs(hard_eligible, sig_cache, id_cache)
    firing_pairs = [p for p in hard_pairs if p["fires"]]
    non_firing_pairs = [p for p in hard_pairs if not p["fires"]]

    total_pairs = len(hard_pairs)
    g.info(f"Total ordered pairs checked (hard): {total_pairs}")
    g.info(f"Inversion pairs firing (FAIL): {len(firing_pairs)}")
    g.info(f"Non-firing pairs: {len(non_firing_pairs)}")

    for pair in firing_pairs:
        a_id = pair["a_id"]
        b_id = pair["b_id"]
        a_score = pair["a_score"]
        b_score = pair["b_score"]
        a_worse_sigs = pair["a_worse_signals"]
        a_better_sigs = pair["a_better_signals"]
        sig_a = pair["sig_a"]
        sig_b = pair["sig_b"]
        supp = pair.get("supporting_info", {})

        # Format signal table (panel signals + supporting)
        sig_table = _format_signal_table(sig_a, sig_b, a_worse_sigs)
        additive_note = (
            f"additive_marker_count: A={supp.get('additive_marker_count_a')} "
            f"B={supp.get('additive_marker_count_b')} "
            f"[SUPPORTING — informational only, not used in fire decision]"
        )

        g.fail(
            f"INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)\n"
            f"    A(higher rank): id={a_id} | score={a_score}\n"
            f"    B(lower rank):  id={b_id} | score={b_score}\n"
            f"    A worse on ({len(a_worse_sigs)} panel signals): {a_worse_sigs}\n"
            f"    A better on: {a_better_sigs if a_better_sigs else '(none -- full inversion)'}\n"
            f"    Panel signal values (A vs B): {sig_table}\n"
            f"    Supporting: {additive_note}"
        )

    # --- Suspected inversions: pairs involving at least one insufficient product ---
    # Check all-eligible pairs but skip pairs already in the hard set
    hard_bcs = {get_barcode(t) for t in hard_eligible}
    all_pairs = _find_inversion_pairs(eligible, sig_cache, id_cache)
    suspected_firing = [
        p for p in all_pairs
        if p["fires"]
        and not (p["a_bc"] in hard_bcs and p["b_bc"] in hard_bcs)
    ]

    if suspected_firing:
        g.warn(f"SUSPECTED inversions (confidence=insufficient, excluded from hard gate): {len(suspected_firing)}")
        for pair in suspected_firing:
            supp = pair.get("supporting_info", {})
            g.warn(
                f"  SUSPECTED: A(higher)={pair['a_id']} score={pair['a_score']} "
                f"vs B(lower)={pair['b_id']} score={pair['b_score']} "
                f"A-worse-on={pair['a_worse_signals']} "
                f"additive[A={supp.get('additive_marker_count_a')} B={supp.get('additive_marker_count_b')}]"
            )

    if len(firing_pairs) == 0 and g.status != "FAIL":
        if g.status == "PASS":
            g.info("No inversion pairs found — gate PASS")

    return g


def _find_inversion_pairs(products: list[dict],
                          sig_cache: dict[str, dict],
                          id_cache: dict[str, str]) -> list[dict]:
    """
    Enumerate all ordered (A, B) pairs where score(A) > score(B) (strict).
    For each, test whether B nutritionally dominates A.
    Returns list of pair dicts with 'fires' bool.

    To avoid double-counting (A,B) and (B,A) as two separate inversions,
    we iterate i < j and assign A = higher-scoring, B = lower-scoring.
    """
    pairs: list[dict] = []
    n = len(products)
    for i in range(n):
        for j in range(i + 1, n):
            t1 = products[i]
            t2 = products[j]
            s1 = t1.get("final_score_estimate") or 0
            s2 = t2.get("final_score_estimate") or 0

            # Strict: skip ties
            if s1 == s2:
                continue

            # Assign A = higher score (should rank first), B = lower score
            if s1 > s2:
                t_a, t_b = t1, t2
                score_a, score_b = s1, s2
            else:
                t_a, t_b = t2, t1
                score_a, score_b = s2, s1

            bc_a = get_barcode(t_a)
            bc_b = get_barcode(t_b)
            sig_a = sig_cache.get(bc_a, {})
            sig_b = sig_cache.get(bc_b, {})

            # Check: is A (higher-scored) nutritionally worse than B (lower-scored)?
            # Inversion = higher-ranked product is nutritionally inferior on panel signals.
            fires, a_worse_sigs, a_better_sigs, supporting_info = a_nutritionally_worse_than_b(sig_a, sig_b)

            pairs.append({
                "fires": fires,
                "a_bc": bc_a,
                "b_bc": bc_b,
                "a_id": id_cache.get(bc_a, bc_a),
                "b_id": id_cache.get(bc_b, bc_b),
                "a_score": score_a,
                "b_score": score_b,
                "sig_a": sig_a,
                "sig_b": sig_b,
                "a_worse_signals": a_worse_sigs,
                "a_better_signals": a_better_sigs,
                "supporting_info": supporting_info,
            })
    return pairs


def _format_signal_table(sig_a: dict, sig_b: dict, worse_signals: list[str]) -> str:
    """Format a compact panel signal comparison string for the FAIL message.
    Only formats the 4 hard panel signals; the supporting signal is reported separately."""
    parts = []
    for s in PANEL_SIGNALS:
        va = sig_a.get(s)
        vb = sig_b.get(s)
        marker = " [WORSE]" if s in worse_signals else ""
        parts.append(f"{s}: A={va} B={vb}{marker}")
    return " | ".join(parts)


# ---------------------------------------------------------------------------
# Standalone CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    # Force UTF-8 on stdout/stderr (Windows CP1252 default breaks output)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="BARI-INVERSION-TEST-001: nutritional dominance inversion gate"
    )
    parser.add_argument(
        "--run", required=True,
        help="Path to BSIP2 run products directory "
             "(flat bsip2_trace_<barcode>.json files or nested subdirs with bsip2_trace.json)"
    )
    parser.add_argument(
        "--out", default=None,
        help="Optional path to write JSON report"
    )
    parser.add_argument(
        "--exit-zero-on-warn", action="store_true",
        help="Exit 0 even when there are suspected inversions (WARN-only) but no hard FAIL"
    )
    args = parser.parse_args()

    run_dir = Path(args.run)
    traces = load_traces_from_run_dir(run_dir)

    if not traces:
        print(f"ERROR: no trace files found in: {run_dir}", file=sys.stderr)
        return 2

    print(f"Loaded {len(traces)} trace records from {run_dir}", file=sys.stderr)

    g = gate_inversion_invariant(traces)

    # Print gate output
    print(g.header())
    for line in g.lines:
        print(line)
    print()

    # Optional JSON report
    if args.out:
        report = {
            "gate": GATE_ID,
            "status": g.status,
            "run_dir": str(run_dir),
            "lines": g.lines,
        }
        out_path = Path(args.out)
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Report written to: {args.out}", file=sys.stderr)

    if g.status == "FAIL":
        return 1
    if g.status == "WARN" and not args.exit_zero_on_warn:
        return 0  # WARN is informational, not a blocking failure
    return 0


if __name__ == "__main__":
    sys.exit(main())
