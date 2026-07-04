"""Bari copy-eval harness (TASK-505) — versioned regression suite for Hebrew consumer copy.

Runs the DETERMINISTIC gates over a fixed dataset of known-good / known-bad copy
(dataset/cases.jsonl) and compares each verdict to the case's expected label,
promptfoo-style. A committed snapshot of gate verdicts (dataset/baseline.json)
turns the suite into a regression gate: any change in gate behavior vs the
baseline exits 1, whether the change is an improvement or a break — improvements
are re-frozen deliberately with --update-baseline, never silently.

Gates wired:
  * integrations/clients/hebrew_readability.py  -> analyze(text).is_clean  (always)
  * integrations/clients/hebrew_grammar_gate.py -> analyze(text).is_clean  (--with-grammar
    only; downloads a ~440MB model on first use, so it is opt-in and its verdicts are
    NEVER compared against the committed baseline — baseline is default-mode only)

Verdict convention (positive class = "the copy is defective"):
  predicted "fail"  = a gate flagged the text
  predicted "pass"  = no gate flagged the text
  TP = expected fail, predicted fail     FN = expected fail, predicted pass
  TN = expected pass, predicted pass     FP = expected pass, predicted fail
  SKIP = expected null (owner-label slot, e.g. translationese) — counted separately.

FNs are EXPECTED here for fabrication / stale-rank / relational-framing / (default-mode)
grammar cases: deterministic gates cannot see them. The suite exists to (a) freeze what
the deterministic layer does catch, and (b) keep the uncaught classes visible as the
calibration target for the LLM judge (see judge/calibration.md).

Usage:
  python 03_operations/evals/copy_evals/run_evals.py                  # default: readability only
  python 03_operations/evals/copy_evals/run_evals.py --with-grammar   # + DictaBERT grammar gate
  python 03_operations/evals/copy_evals/run_evals.py --update-baseline

Exit codes: 0 = no regression vs baseline; 1 = regression / missing baseline / dataset error.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]  # C:\Bari
CASES_PATH = HERE / "dataset" / "cases.jsonl"
BASELINE_PATH = HERE / "dataset" / "baseline.json"

sys.path.insert(0, str(REPO_ROOT))

from integrations.clients.hebrew_readability import analyze as readability_analyze  # noqa: E402


def _load_grammar_gate():
    """Opt-in: DictaBERT-morph grammar gate (~440MB model download on first use)."""
    try:
        from integrations.clients.hebrew_grammar_gate import analyze as grammar_analyze
        return grammar_analyze
    except Exception as exc:  # ImportError, RuntimeError (missing torch/transformers), etc.
        print(f"[warn] grammar gate unavailable ({type(exc).__name__}: {exc}) — "
              f"continuing readability-only.", file=sys.stderr)
        return None


def load_cases() -> list[dict]:
    cases, seen = [], set()
    with CASES_PATH.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            case = json.loads(line)
            for key in ("id", "text", "failure_class", "source"):
                if key not in case:
                    raise ValueError(f"cases.jsonl:{lineno}: missing key '{key}'")
            if "expected" not in case:
                raise ValueError(f"cases.jsonl:{lineno}: missing key 'expected'")
            if case["expected"] not in ("pass", "fail", None):
                raise ValueError(f"cases.jsonl:{lineno}: expected must be pass|fail|null")
            if case["id"] in seen:
                raise ValueError(f"cases.jsonl:{lineno}: duplicate id '{case['id']}'")
            seen.add(case["id"])
            cases.append(case)
    return cases



# HARD leak kinds that count as a predicted "fail" (TASK-506 D3 added
# sodium_term / brand_spelling / antithesis to the pre-existing three).
# em_dash and number_density are ADVISORY-only per owner ruling ("minimize",
# not "ban") and are deliberately excluded from this set — they never flip
# the predicted verdict, only appear in `reasons` if present is desired later.
_HARD_FAIL_LEAK_KINDS = (
    "framework", "score_mechanic", "recommendation",
    "sodium_term", "brand_spelling", "antithesis",
)


def run_gates(text: str, grammar_analyze) -> tuple[str, list[str]]:
    """Return (predicted 'pass'|'fail', reasons)."""
    reasons: list[str] = []
    report = readability_analyze(text)
    if not report.is_clean:
        for leak in report.leaks:
            if leak.kind in _HARD_FAIL_LEAK_KINDS:
                reasons.append(f"readability:{leak.kind}:'{leak.term}'")
    if grammar_analyze is not None:
        greport = grammar_analyze(text)
        if not greport.is_clean:
            for flag in greport.flags:
                reasons.append(f"grammar:{getattr(flag, 'kind', 'agreement')}")
    return ("fail" if reasons else "pass"), reasons


def classify(expected, predicted) -> str:
    if expected is None:
        return "SKIP"
    if expected == "fail":
        return "TP" if predicted == "fail" else "FN"
    return "FP" if predicted == "fail" else "TN"


def main() -> int:
    ap = argparse.ArgumentParser(description="Bari Hebrew copy-eval regression suite")
    ap.add_argument("--with-grammar", action="store_true",
                    help="also run the DictaBERT grammar gate (downloads ~440MB model "
                         "on first use; verdicts NOT compared to baseline)")
    ap.add_argument("--update-baseline", action="store_true",
                    help="re-freeze dataset/baseline.json from the current default-mode "
                         "verdicts (only after an intentional gate/dataset change)")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if args.with_grammar and args.update_baseline:
        print("ERROR: --update-baseline must run in default mode (baseline is "
              "readability-only; grammar verdicts are not frozen).", file=sys.stderr)
        return 1

    cases = load_cases()
    grammar_analyze = _load_grammar_gate() if args.with_grammar else None

    results = []
    for case in cases:
        predicted, reasons = run_gates(case["text"], grammar_analyze)
        outcome = classify(case["expected"], predicted)
        results.append({"case": case, "predicted": predicted,
                        "outcome": outcome, "reasons": reasons})

    # ---- per-case table -------------------------------------------------
    print(f"{'id':10} {'class':24} {'expected':9} {'predicted':10} {'outcome':8} reasons")
    print("-" * 100)
    for r in results:
        c = r["case"]
        exp = c["expected"] if c["expected"] is not None else "(null)"
        reason_str = "; ".join(r["reasons"])[:60] or "-"
        print(f"{c['id']:10} {c['failure_class']:24} {exp:9} {r['predicted']:10} "
              f"{r['outcome']:8} {reason_str}")

    # ---- confusion counts per failure class ------------------------------
    conf: dict[str, dict[str, int]] = defaultdict(lambda: {"TP": 0, "FP": 0, "TN": 0,
                                                           "FN": 0, "SKIP": 0})
    for r in results:
        conf[r["case"]["failure_class"]][r["outcome"]] += 1
    print("\nConfusion by failure class (positive = defective copy detected):")
    print(f"{'class':24} {'TP':>3} {'FP':>3} {'TN':>3} {'FN':>3} {'SKIP':>5}")
    totals = {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "SKIP": 0}
    for fclass in sorted(conf):
        row = conf[fclass]
        for k in totals:
            totals[k] += row[k]
        print(f"{fclass:24} {row['TP']:>3} {row['FP']:>3} {row['TN']:>3} "
              f"{row['FN']:>3} {row['SKIP']:>5}")
    print(f"{'TOTAL':24} {totals['TP']:>3} {totals['FP']:>3} {totals['TN']:>3} "
          f"{totals['FN']:>3} {totals['SKIP']:>5}")
    n_scored = sum(v for k, v in totals.items() if k != "SKIP")
    print(f"\n{len(results)} cases: {n_scored} scored, {totals['SKIP']} skipped "
          f"(expected: null — owner-label slots awaiting calibration; see judge/).")

    # ---- baseline regression check (default mode only) -------------------
    current = {r["case"]["id"]: r["predicted"] for r in results}
    if args.update_baseline:
        BASELINE_PATH.write_text(
            json.dumps({"mode": "readability_only", "verdicts": current},
                       indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        print(f"\nBaseline re-frozen -> {BASELINE_PATH}")
        return 0

    if args.with_grammar:
        print("\n[--with-grammar] baseline comparison SKIPPED (baseline freezes "
              "default-mode verdicts only). Informational run.")
        return 0

    if not BASELINE_PATH.exists():
        print("\nERROR: dataset/baseline.json missing. Run once with --update-baseline "
              "to freeze the expected gate verdicts, review the diff, and commit it.",
              file=sys.stderr)
        return 1

    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))["verdicts"]
    regressions = []
    for cid, pred in current.items():
        if cid not in baseline:
            regressions.append(f"{cid}: NEW CASE (not in baseline) -> {pred}")
        elif baseline[cid] != pred:
            regressions.append(f"{cid}: baseline={baseline[cid]} now={pred}")
    for cid in baseline:
        if cid not in current:
            regressions.append(f"{cid}: in baseline but missing from dataset")

    if regressions:
        print(f"\nREGRESSION vs baseline ({len(regressions)}):")
        for line in regressions:
            print(f"  - {line}")
        print("If the change is intentional (gate improved, case added), re-freeze with "
              "--update-baseline and commit both files.")
        return 1

    print("\nOK: all gate verdicts match dataset/baseline.json (no regression).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
