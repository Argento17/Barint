"""
gold_check.py — Bari Gold Set Accuracy Gate (TASK-421 / rebuilt from spec P238-P242).

For each seed entry in gold_set_seed_v0.json:
  1. Score the product by importing score_corpus from shadow_backtest.py
     (no duplicate scoring path — reuses the same pipeline the shadow diff uses).
  2. Compare the engine's actual grade + score to the expected band/range.
  3. Emit PASS / ADVISORY / FAIL / UNVERIFIABLE per entry.
  4. Report per-dimension direction as ADVISORY side-notes only — dimensions
     NEVER affect the pass/fail verdict (per C3 ruling P240/P241/P242).

Pass/Fail semantics (P241/P242):
  PASS      = grade in grade_band AND score in score_range
  ADVISORY  = grade in grade_band BUT score within +/-3 of a range edge (borderline)
              OR a PASS entry that has dimension side-notes (labels it PASS, not ADVISORY)
  FAIL      = grade NOT in grade_band, OR score clearly outside range (>3 beyond edge)
  UNVERIFIABLE = corpus source absent from this checkout

Per P242: a grade+score MATCH that carries dimension notes is labelled PASS, not ADVISORY.
          ADVISORY is reserved only for a true borderline (grade in band, score +/-3 of edge).

Headline metric: grade+score agreement = (PASS + ADVISORY) / scorable

Exit codes:
  0 = all scorable entries PASS (ADVISORY is a pass variant; no FAILs)
  1 = advisories present, no FAILs (borderline matches only)
  2 = ≥1 FAIL
  3 = zero entries could be scored (all UNVERIFIABLE, or harness crash)

DISAGREEMENTS section: every FAIL with pid, name, expected band/range, actual
score/grade, classified as "needs_nutrition_review" (engine_divergence |
seed_defect | policy_ambiguous is a later Nutrition Agent step — not guessed here).

Usage:
  python gold_check.py [--seed PATH] [--verbose]
"""

import argparse
import json
import os
import pathlib
import sys

# Force UTF-8 stdout so Hebrew names and Unicode symbols print on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_HERE = pathlib.Path(__file__).parent.resolve()
DEFAULT_SEED = _HERE / "gold_set_seed_v0.json"

# shadow_backtest.py lives here
SHADOW_SRC = _HERE.parents[1] / "bsip2" / "proto_v0" / "src"


def _grade_to_score_range(grade: str) -> tuple[int, int]:
    """Return the (min, max) score range for a grade (per constants.py cutoffs)."""
    return {
        "S": (90, 100),
        "A": (80, 89),
        "B": (65, 79),
        "C": (50, 64),
        "D": (35, 49),
        "E": (0, 34),
    }.get(grade, (0, 0))


def _dim_direction(score: float | None) -> str:
    """Map a 0-100 dimension score to low/medium/high."""
    if score is None:
        return "unknown"
    if score >= 67:
        return "high"
    if score >= 34:
        return "medium"
    return "low"


BORDERLINE_MARGIN = 3  # +/-3 points from range edge = ADVISORY not FAIL


def _verdict(grade: str | None, score: float | None, expected: dict) -> tuple[str, str]:
    """
    Compute (verdict, reason) for one entry.
    Returns ("PASS"/"ADVISORY"/"FAIL", reason_string).
    """
    grade_band = expected.get("grade_band", [])
    sr = expected.get("score_range", [0, 100])
    sr_min, sr_max = int(sr[0]), int(sr[1])

    if grade is None or score is None:
        return "FAIL", f"engine returned no grade or score (grade={grade}, score={score})"

    grade_match = grade in grade_band
    score_in_range = sr_min <= score <= sr_max

    if grade_match and score_in_range:
        return "PASS", f"grade {grade} in {grade_band} and score {score:.1f} in [{sr_min},{sr_max}]"

    if grade_match and not score_in_range:
        # Borderline: grade matches but score is just outside range
        dist = min(abs(score - sr_min), abs(score - sr_max))
        if dist <= BORDERLINE_MARGIN:
            return "ADVISORY", (
                f"grade {grade} in {grade_band} but score {score:.1f} is +/-{dist:.1f} "
                f"from range [{sr_min},{sr_max}] edge (borderline)"
            )
        return "FAIL", (
            f"grade {grade} in {grade_band} but score {score:.1f} is outside "
            f"[{sr_min},{sr_max}] by {dist:.1f} points"
        )

    # grade does not match
    return "FAIL", (
        f"grade {grade} not in expected {grade_band} "
        f"(score {score:.1f}, expected [{sr_min},{sr_max}])"
    )


def _dim_notes(entry_expected_dims: dict, actual_dims: dict | None) -> list[str]:
    """Compare expected dimension directions to actual. Advisory only."""
    notes = []
    if not entry_expected_dims or not isinstance(actual_dims, dict):
        return notes
    for dim, expected_dir in entry_expected_dims.items():
        actual_score = actual_dims.get(dim)
        actual_dir = _dim_direction(actual_score)
        if actual_dir != expected_dir:
            eng_str = f"{actual_score:.1f}" if isinstance(actual_score, (int, float)) else str(actual_score)
            notes.append(
                f"  DIM ADVISORY [{dim}]: expected {expected_dir}, "
                f"engine={eng_str} ({actual_dir})"
            )
    return notes


def score_one_corpus(corpus_cfg: dict) -> dict | None:
    """
    Score one corpus using shadow_backtest.score_corpus.
    Returns {pid: snapshot} or None if source is absent.
    """
    if str(SHADOW_SRC) not in sys.path:
        sys.path.insert(0, str(SHADOW_SRC))

    # Import here (inside scoring section) to allow flag purge
    from shadow_backtest import score_corpus, lookup_shelf_rel, resolve_sources

    source = corpus_cfg["source"]
    merged_flags = corpus_cfg["merged_flags"]
    corpus_name = corpus_cfg["name"]

    # Check all source paths exist
    src_paths = resolve_sources(source)
    missing = [str(p) for p in src_paths if not p.exists()]
    if missing:
        return None  # UNVERIFIABLE — source not in this checkout

    shelf_rel = lookup_shelf_rel(corpus_name, source)
    return score_corpus(source, merged_flags, shelf_rel)


def run_check(seed_path: pathlib.Path, verbose: bool = False) -> int:
    """
    Main gold_check logic. Returns exit code (0/1/2/3).
    """
    # Load seed
    try:
        data = json.loads(seed_path.read_bytes().decode("utf-8"))
    except FileNotFoundError:
        print(f"ERROR: seed file not found: {seed_path}", file=sys.stderr)
        return 3
    except json.JSONDecodeError as e:
        print(f"ERROR: seed file is not valid JSON: {e}", file=sys.stderr)
        return 3

    entries = data.get("entries", [])
    if not entries:
        print("ERROR: seed file has no entries.", file=sys.stderr)
        return 3

    # Load shadow registry for corpus source + default flags
    # _HERE = 03_operations/shadow/goldset; parents[0]=shadow; parents[1]=03_operations; parents[2]=repo_root
    registry_path = _HERE.parents[0] / "shadow_registry_v1.json"
    try:
        registry = json.loads(registry_path.read_bytes().decode("utf-8"))
    except Exception as e:
        print(f"ERROR: cannot load shadow registry: {e}", file=sys.stderr)
        return 3

    engine_defaults = registry.get("engine_default_flags", {})
    registry_corpora = {c["name"]: c for c in registry.get("corpora", [])}

    # Build per-corpus scoring config from SEED flags (each entry carries its own
    # exact merged flag config — use that, not the registry defaults alone, so
    # the gold check scores each product under its DECLARED expected-band flags).
    # Group entries by (corpus, frozen flags key) to minimize re-imports.
    # Actually: each entry's scoring_flags is already the merged config. We score
    # each unique (corpus, flags) combination once, then look up by pid.
    #
    # Important: entries with the same corpus+flags pair share one score run.
    # Entries with the same pid but different flags (e.g. A-003 vs G-003) get
    # separate runs (different flag keys). This is correct.

    # Build unique corpus runs
    runs: dict[str, dict] = {}  # run_key -> {source, merged_flags, name}
    entry_run_keys: list[str] = []  # parallel to entries

    for entry in entries:
        corpus_name = entry.get("corpus", "")
        reg_corpus = registry_corpora.get(corpus_name)
        if reg_corpus is None:
            entry_run_keys.append(None)
            continue
        source = reg_corpus.get("source")
        # Use entry's declared scoring_flags as the merged config
        merged_flags = dict(engine_defaults)
        merged_flags.update(entry.get("scoring_flags", {}))
        # Make a stable key from flags
        flags_key = json.dumps(sorted(merged_flags.items()))
        run_key = f"{corpus_name}::{flags_key}"
        if run_key not in runs:
            runs[run_key] = {"name": corpus_name, "source": source, "merged_flags": merged_flags}
        entry_run_keys.append(run_key)

    # Execute each unique run
    run_results: dict[str, dict | None] = {}  # run_key -> {pid: snapshot} or None
    for run_key, cfg in runs.items():
        if verbose:
            print(f"  Scoring corpus '{cfg['name']}' ...")
        try:
            result = score_one_corpus(cfg)
            run_results[run_key] = result
        except Exception as e:
            print(f"  WARNING: corpus '{cfg['name']}' scoring raised: {type(e).__name__}: {e}", file=sys.stderr)
            run_results[run_key] = None

    # Evaluate each entry
    results_by_entry: list[dict] = []
    for idx, entry in enumerate(entries):
        run_key = entry_run_keys[idx]
        eid = entry.get("id", f"<{idx}>")
        pid = entry.get("pid", "")
        name = ""
        corpus_name = entry.get("corpus", "")
        expected = entry.get("expected", {})
        expected_dims = expected.get("dimensions", {})

        if run_key is None or corpus_name not in registry_corpora:
            results_by_entry.append({
                "id": eid, "pid": pid, "name": name, "corpus": corpus_name,
                "verdict": "UNVERIFIABLE", "reason": f"corpus '{corpus_name}' not in shadow registry",
                "dim_notes": []
            })
            continue

        corpus_scores = run_results.get(run_key)
        if corpus_scores is None:
            results_by_entry.append({
                "id": eid, "pid": pid, "name": name, "corpus": corpus_name,
                "verdict": "UNVERIFIABLE", "reason": "corpus source absent from this checkout",
                "dim_notes": []
            })
            continue

        snapshot = corpus_scores.get(pid)
        if snapshot is None:
            results_by_entry.append({
                "id": eid, "pid": pid, "name": pid, "corpus": corpus_name,
                "verdict": "UNVERIFIABLE", "reason": f"pid '{pid}' not found in corpus run output",
                "dim_notes": []
            })
            continue

        if "error" in snapshot:
            results_by_entry.append({
                "id": eid, "pid": pid, "name": snapshot.get("name", pid), "corpus": corpus_name,
                "verdict": "FAIL", "reason": f"engine error: {snapshot['error']}",
                "actual_score": None, "actual_grade": None,
                "dim_notes": []
            })
            continue

        actual_score = snapshot.get("score")
        actual_grade = snapshot.get("grade")
        actual_dims = snapshot.get("dims") or {}
        name = snapshot.get("name", pid)

        verdict, reason = _verdict(actual_grade, actual_score, expected)
        dim_notes = _dim_notes(expected_dims, actual_dims)

        results_by_entry.append({
            "id": eid, "pid": pid, "name": name, "corpus": corpus_name,
            "verdict": verdict, "reason": reason,
            "actual_score": actual_score, "actual_grade": actual_grade,
            "expected_band": expected.get("grade_band"),
            "expected_range": expected.get("score_range"),
            "dim_notes": dim_notes,
        })

    # ---------------------------------------------------------------- report --
    pass_count = sum(1 for r in results_by_entry if r["verdict"] == "PASS")
    advisory_count = sum(1 for r in results_by_entry if r["verdict"] == "ADVISORY")
    fail_count = sum(1 for r in results_by_entry if r["verdict"] == "FAIL")
    unverifiable_count = sum(1 for r in results_by_entry if r["verdict"] == "UNVERIFIABLE")
    scorable = len(results_by_entry) - unverifiable_count
    agreement = pass_count + advisory_count

    print("=" * 70)
    print("BARI GOLD SET ACCURACY GATE")
    print(f"Seed: {seed_path}")
    print(f"Entries: {len(entries)} total / {scorable} scorable / {unverifiable_count} unverifiable")
    print()
    print(f"PASS:          {pass_count:3d}")
    print(f"ADVISORY:      {advisory_count:3d}  (grade+score borderline match)")
    print(f"FAIL:          {fail_count:3d}")
    print(f"UNVERIFIABLE:  {unverifiable_count:3d}  (source absent)")
    print()
    if scorable > 0:
        pct = 100.0 * agreement / scorable
        print(f"grade+score agreement: {agreement}/{scorable} ({pct:.1f}%)")
    else:
        print("grade+score agreement: N/A (0 scorable entries)")
    print()

    # Per-entry detail
    print("-" * 70)
    print("PER-ENTRY RESULTS")
    print("-" * 70)
    for r in results_by_entry:
        v = r["verdict"]
        marker = {"PASS": "[PASS]", "ADVISORY": "[ADV ]", "FAIL": "[FAIL]", "UNVERIFIABLE": "[UNV ]"}.get(v, v)
        score_str = f"{r.get('actual_score', 'N/A'):.1f}" if isinstance(r.get("actual_score"), (int, float)) else "N/A"
        grade_str = r.get("actual_grade") or "N/A"
        print(f"{marker} {r['id']:7s}  {r['corpus']:25s}  score={score_str:6s}  grade={grade_str}  | {r['reason']}")
        if verbose and r.get("dim_notes"):
            for note in r["dim_notes"]:
                print(f"          (informational, does not affect pass/fail){note}")
    print()

    # Disagreements — all FAILs listed for Nutrition Agent review
    fails = [r for r in results_by_entry if r["verdict"] == "FAIL"]
    if fails:
        print("=" * 70)
        print("DISAGREEMENTS (needs_nutrition_review)")
        print("Classification (engine_divergence|seed_defect|policy_ambiguous)")
        print("is a Nutrition Agent determination — not guessed here.")
        print("-" * 70)
        for r in fails:
            score_str = f"{r.get('actual_score', 'N/A'):.1f}" if isinstance(r.get("actual_score"), (int, float)) else "N/A"
            grade_str = r.get("actual_grade") or "N/A"
            print(f"  id:     {r['id']}")
            print(f"  pid:    {r['pid']}")
            print(f"  name:   {r.get('name', '')}")
            print(f"  corpus: {r['corpus']}")
            print(f"  expected_band:  {r.get('expected_band')}")
            print(f"  expected_range: {r.get('expected_range')}")
            print(f"  actual_score:   {score_str}")
            print(f"  actual_grade:   {grade_str}")
            print(f"  reason:         {r['reason']}")
            print(f"  classification: needs_nutrition_review")
            if r.get("dim_notes"):
                print("  dim_notes (informational):")
                for note in r["dim_notes"]:
                    print(f"    {note.strip()}")
            print()
        print("=" * 70)

    # Unverifiable list
    unv = [r for r in results_by_entry if r["verdict"] == "UNVERIFIABLE"]
    if unv:
        print("UNVERIFIABLE ENTRIES (excluded from agreement denominator):")
        for r in unv:
            print(f"  {r['id']:7s}  {r['pid']:45s}  {r['reason']}")
        print()

    # Dimension advisory section (always shown, labeled informational)
    dim_entries = [r for r in results_by_entry if r.get("dim_notes") and r["verdict"] in ("PASS", "ADVISORY", "FAIL")]
    if dim_entries:
        print("-" * 70)
        print("DIMENSION ADVISORY NOTES (informational — does not affect pass/fail)")
        print("-" * 70)
        for r in dim_entries:
            print(f"  {r['id']:7s} [{r['verdict']}] {r.get('name', r['pid'])[:50]}")
            for note in r["dim_notes"]:
                print(f"    {note.strip()}")
        print()

    # Determine exit code
    if scorable == 0:
        print("EXIT 3: zero scorable entries.")
        return 3
    if fail_count > 0:
        print(f"EXIT 2: {fail_count} FAIL(s) — disagreements sent to needs_nutrition_review.")
        return 2
    if advisory_count > 0:
        print(f"EXIT 1: {advisory_count} ADVISORY (borderline) — no hard FAILs.")
        return 1
    print("EXIT 0: all scorable entries PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bari Gold Set Accuracy Gate — scores seed products and checks expected bands."
    )
    parser.add_argument(
        "--seed",
        type=pathlib.Path,
        default=DEFAULT_SEED,
        help=f"Path to gold seed JSON (default: {DEFAULT_SEED})",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print per-entry dimension advisory notes in the main results table",
    )
    args = parser.parse_args()

    seed_path = args.seed
    if not seed_path.is_absolute():
        seed_path = pathlib.Path.cwd() / seed_path

    print(f"gold_check.py — Bari Gold Set Accuracy Gate")
    print(f"Seed: {seed_path}")
    print()

    try:
        return run_check(seed_path, verbose=args.verbose)
    except Exception as e:
        import traceback
        print(f"HARNESS CRASH: {type(e).__name__}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
