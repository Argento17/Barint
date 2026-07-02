"""
SIE Supplement Corpus v3 — Pre-Launch QA Audit
================================================
Deterministic checks over _corpus_run_full_v3.json.
Produces _qa_report.md and prints a PASS/FAIL summary.

Checks
------
1. TRACEABILITY     every scored SKU has a non-null dose AND a traceable source
2. OFF BAN          zero Open Food Facts references anywhere in corpus + cache + skus_full
3. NO FABRICATION   no scored SKU carries name_derived source with omega-3 active;
                    name_derived entries flagged with dose are enumerated (not a hard-fail
                    if the dose is derived from the product name itself — but any
                    name_derived + omega-3 combo IS a hard fail)
4. DISTRIBUTION     recompute grade distribution; compare to JSON header AND reported values
5. UNSCOREABLE      verify outcome field encodes reason implicitly (premarket vs incomplete);
                    check counts add up (scored + incomplete + premarket == total)

Usage
-----
    python qa_audit.py

Exit codes
----------
    0  all checks PASS
    1  one or more FAIL
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
# SUPP-EV-027/028 (2026-06-19, TASK-356): v8 corpus fixes
# RT7-H2: zinc label_basis=elemental (same MOH convention as iron SUPP-EV-025).
# RT7-H3: magnesium carbonate added to compound_forms_identity (CID 11029, fraction 0.288).
# RT7-H1: elemental-basis form=None safety guard — compare directly to UL (no max_fraction).
# qa_audit.py defaults to v8; falls back to v7, v6, v5, v4, v3.
_V8 = HERE / "_corpus_run_full_v8.json"
_V7 = HERE / "_corpus_run_full_v7.json"
_V6 = HERE / "_corpus_run_full_v6.json"
_V5 = HERE / "_corpus_run_full_v5.json"
_V4 = HERE / "_corpus_run_full_v4.json"
_V3 = HERE / "_corpus_run_full_v3.json"
CORPUS_FILE = (_V8 if _V8.exists() else
               (_V7 if _V7.exists() else
                (_V6 if _V6.exists() else
                 (_V5 if _V5.exists() else
                  (_V4 if _V4.exists() else _V3)))))
CACHE_DIR = HERE / "cache"
SKUS_FULL_DIR = HERE / "skus_full"
REPORT_FILE = HERE / "_qa_report.md"

# ── reported expected values ──────────────────────────────────────────────────
# v8 expected values (SUPP-EV-027/028, TASK-356, 2026-06-19):
# RT7-H2 (SUPP-EV-027): zinc label_basis=elemental root fix. Israeli MOH declares chelated
# zinc as ELEMENTAL mg (same convention as iron, SUPP-EV-025). No compound conversion applied.
#   SP-0033984037250 (Solgar Zinc Picolinate 22mg): B/68.4 → B/77.5 (improved within B band)
#   SP-7290006437563 (Altman Zinc Picolinate 25mg): B/69.7 → B/77.5 (improved within B band)
#   SP-7290018365359 (Tink Zinc 50mg, name_derived): E/34 (cap_1) → E/20 (veto_safety)
#     — 50mg elemental > 40mg UL → VETO (grade stays E, binding changes to veto_safety)
# RT7-H3 (SUPP-EV-028): magnesium carbonate added to compound_forms_identity.
#   PubChem CID 11029, MW 84.31, elemental_mg_fraction=0.288.
#   SP-7290015429245 (Amorphicure Mg Carbonate 160mg): C/59.2 → D/49
#     — 160 × 0.288 = 46.1mg elemental < fairy_floor (0.5 × 300 = 150mg) → cap_2 → D/49
# RT7-H1 (SUPP-EV-027): elemental-basis form=None safety guard fix.
#   When label_basis="elemental" and form=None: compare amount directly to UL.
#   (No max_fraction multiply — that would reduce an already-elemental value → false-safe.)
#   No current products affected by H1 other than the Tink Zinc already captured above.
# v7 base: S=11, A=9, B=16, C=4, D=15, E=23 (78 scored)
# v8 delta from v7:
#   SP-7290015429245 (Amorphicure Mg Carbonate 160mg): C/59.2 → D/49  (-C, +D)
#   Net: C=4→3 (-1), D=15→16 (+1). S/A/B/E unchanged. scored=78 (unchanged).
# SUPP-EV-022/023/024/025/026/v7 fixes fully retained. Total scored=78, shelf=118 unchanged.
REPORTED_GRADE_DIST: dict[str, int] = {
    "S": 11, "A": 9, "B": 16, "C": 3, "D": 16, "E": 23
}
REPORTED_SCORED = 78
REPORTED_INCOMPLETE = 26
REPORTED_PREMARKET = 11
REPORTED_PEDIATRIC = 3
REPORTED_TOTAL = 118

# OFF patterns (must be zero)
OFF_PATTERNS = [
    r"openfoodfacts",
    r"world\.openfoodfacts",
]
OFF_REGEX = re.compile("|".join(OFF_PATTERNS), re.IGNORECASE)

# ── helpers ───────────────────────────────────────────────────────────────────

def load_corpus() -> dict[str, Any]:
    with open(CORPUS_FILE, encoding="utf-8") as fh:
        return json.load(fh)


def scored_results(results: list) -> list:
    return [r for r in results if r.get("outcome") == "scored"]


def unscoreable_results(results: list) -> list:
    return [r for r in results if r.get("outcome") != "scored"]


# ── Check 1: TRACEABILITY ─────────────────────────────────────────────────────

def check_traceability(results: list) -> tuple[bool, list[str], list[str]]:
    """
    Every scored SKU must have:
      - at least one active with a non-null amount (dose)
      - a non-empty source_url in panel.provenance
    Returns (pass, missing_dose_list, missing_source_list).
    """
    missing_dose: list[str] = []
    missing_source: list[str] = []

    for r in scored_results(results):
        sku = r["sku_id"]
        panel = r.get("panel") or {}
        actives = panel.get("actives") or []
        prov = panel.get("provenance") or {}
        src_url = prov.get("source_url") or ""

        # dose check: at least one active must have a non-null amount
        has_dose = any(
            a.get("amount") is not None for a in actives if isinstance(a, dict)
        )
        if not has_dose:
            missing_dose.append(
                f"  - {sku} ({r.get('acquisition_method','?')}) | "
                f"name_he={r.get('name_he','')}"
            )

        # source check: source_url must exist (name_derived:// is synthetic but still
        # present, so empty string = real failure)
        if not src_url:
            missing_source.append(
                f"  - {sku} ({r.get('acquisition_method','?')}) | "
                f"name_he={r.get('name_he','')}"
            )

    passed = not missing_dose and not missing_source
    return passed, missing_dose, missing_source


# ── Check 2: OFF BAN ──────────────────────────────────────────────────────────

def check_off_ban() -> tuple[bool, list[str]]:
    """
    Scan corpus JSON, cache/*.json, skus_full/*.json for OFF references.
    Returns (pass, hit_list).
    """
    hits: list[str] = []

    def scan_file(filepath: Path, label: str) -> None:
        try:
            text = filepath.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            hits.append(f"  - UNREADABLE: {label} ({exc})")
            return
        if OFF_REGEX.search(text):
            hits.append(f"  - {label}")

    scan_file(CORPUS_FILE, "corpus/_corpus_run_full_v3.json")

    for f in sorted(CACHE_DIR.glob("*.json")):
        scan_file(f, f"cache/{f.name}")

    for f in sorted(SKUS_FULL_DIR.glob("*.json")):
        scan_file(f, f"skus_full/{f.name}")

    return (len(hits) == 0, hits)


# ── Check 3: NO FABRICATION ───────────────────────────────────────────────────

def check_fabrication(results: list) -> tuple[bool, list[str], list[str]]:
    """
    Hard fail: any scored SKU with engine_active==omega3 AND
    acquisition_method==name_derived. Omega-3 dose cannot be inferred from name.

    Warning (enumerated, not hard-fail): all other name_derived scored SKUs that
    carry a numeric dose (expected — dose comes from product name pattern) are
    listed for auditor review.
    """
    hard_fails: list[str] = []
    nd_dose_flags: list[str] = []

    for r in scored_results(results):
        acq = r.get("acquisition_method", "")
        active = r.get("engine_active", "")
        sku = r["sku_id"]

        if acq != "name_derived":
            continue

        panel = r.get("panel") or {}
        actives = panel.get("actives") or []
        doses = [
            f"{a.get('amount')} {a.get('unit','')}"
            for a in actives
            if isinstance(a, dict) and a.get("amount") is not None
        ]
        dose_str = ", ".join(doses) if doses else "no dose"

        if active == "omega3":
            hard_fails.append(
                f"  - {sku} | active={active} | acq=name_derived | "
                f"dose={dose_str} | name_he={r.get('name_he','')}"
            )
        else:
            nd_dose_flags.append(
                f"  - {sku} | active={active} | dose={dose_str} | "
                f"grade={r.get('engine_output',{}).get('grade','?')} | "
                f"name_he={r.get('name_he','')}"
            )

    passed = len(hard_fails) == 0
    return passed, hard_fails, nd_dose_flags


# ── Check 4: DISTRIBUTION INTEGRITY ──────────────────────────────────────────

def check_distribution(corpus: dict) -> tuple[bool, dict[str, int], dict[str, int], str]:
    """
    Recompute grade distribution from results[].engine_output.grade.
    Compare to corpus header grade_distribution AND reported expected values.
    Returns (pass, computed_dist, header_dist, detail_str).
    """
    results = corpus.get("results", [])
    computed: dict[str, int] = {}
    for r in scored_results(results):
        g = (r.get("engine_output") or {}).get("grade")
        if g:
            computed[g] = computed.get(g, 0) + 1

    header_dist_raw = corpus.get("grade_distribution") or {}
    header_dist: dict[str, int] = {k: int(v) for k, v in header_dist_raw.items()}

    lines: list[str] = []
    all_ok = True

    # computed vs header
    for grade in sorted(set(list(computed.keys()) + list(header_dist.keys()))):
        cv = computed.get(grade, 0)
        hv = header_dist.get(grade, 0)
        rv = REPORTED_GRADE_DIST.get(grade, 0)
        ok_h = cv == hv
        ok_r = cv == rv
        symbol = "OK" if (ok_h and ok_r) else "MISMATCH"
        if not (ok_h and ok_r):
            all_ok = False
        lines.append(
            f"  {grade}: computed={cv}  header={hv}  reported={rv}  [{symbol}]"
        )

    total_scored_computed = sum(computed.values())
    total_scored_reported = REPORTED_SCORED
    if total_scored_computed != total_scored_reported:
        all_ok = False
        lines.append(
            f"  TOTAL SCORED: computed={total_scored_computed} "
            f"!= reported={total_scored_reported}  [MISMATCH]"
        )
    else:
        lines.append(
            f"  TOTAL SCORED: computed={total_scored_computed} == reported={total_scored_reported}  [OK]"
        )

    return all_ok, computed, header_dist, "\n".join(lines)


# ── Check 5: UNSCOREABLE COMPLETENESS ────────────────────────────────────────

def check_unscoreable(corpus: dict) -> tuple[bool, list[str]]:
    """
    Every non-scored result must have outcome in
    {unscoreable_incomplete, unscoreable_premarket}.
    Counts must match header.
    Also verify total = scored + incomplete + premarket == shelf_n.
    """
    results = corpus.get("results", [])
    issues: list[str] = []

    counts_header = corpus.get("counts") or {}
    header_scored = int(counts_header.get("scored", 0))
    header_incomplete = int(counts_header.get("unscoreable_incomplete", 0))
    header_premarket = int(counts_header.get("unscoreable_premarket", 0))
    header_total = int(corpus.get("shelf_n", 0))

    computed_scored = len(scored_results(results))
    computed_incomplete = sum(
        1 for r in results if r.get("outcome") == "unscoreable_incomplete"
    )
    computed_premarket = sum(
        1 for r in results if r.get("outcome") == "unscoreable_premarket"
    )
    computed_total = len(results)

    # Check unknown outcomes
    # RT-3/SUPP-EV-022: `unscoreable_pediatric` is a legitimate outcome (v4+)
    valid_outcomes = {"scored", "unscoreable_incomplete", "unscoreable_premarket",
                      "unscoreable_pediatric"}
    unknown_outcomes = [
        f"  - {r['sku_id']}: outcome={r.get('outcome')}"
        for r in results
        if r.get("outcome") not in valid_outcomes
    ]
    if unknown_outcomes:
        issues.append(f"Unknown outcome values ({len(unknown_outcomes)}):")
        issues.extend(unknown_outcomes)

    computed_pediatric = sum(
        1 for r in results if r.get("outcome") == "unscoreable_pediatric"
    )
    header_pediatric = int(counts_header.get("unscoreable_pediatric", 0))

    # Count checks — pediatric is a new outcome; mismatch vs REPORTED_PEDIATRIC only
    # if the v4 corpus is in use (v3 has 0 pediatric by definition).
    def _check(label: str, computed: int, header: int, reported: int) -> None:
        if computed != header:
            issues.append(
                f"{label}: computed={computed} != header={header}  [MISMATCH vs header]"
            )
        if computed != reported:
            issues.append(
                f"{label}: computed={computed} != reported={reported}  [MISMATCH vs reported]"
            )

    _check("scored", computed_scored, header_scored, REPORTED_SCORED)
    _check("unscoreable_incomplete", computed_incomplete, header_incomplete, REPORTED_INCOMPLETE)
    _check("unscoreable_premarket", computed_premarket, header_premarket, REPORTED_PREMARKET)
    # Pediatric: only check against REPORTED_PEDIATRIC if it's been updated (non-zero or v4 run)
    if REPORTED_PEDIATRIC > 0 or header_pediatric > 0:
        _check("unscoreable_pediatric", computed_pediatric, header_pediatric, REPORTED_PEDIATRIC)

    if computed_total != header_total:
        issues.append(
            f"total records: computed={computed_total} != shelf_n={header_total}  [MISMATCH]"
        )
    if computed_total != REPORTED_TOTAL:
        issues.append(
            f"total records: computed={computed_total} != reported_total={REPORTED_TOTAL}  [MISMATCH]"
        )

    # Arithmetic: all outcome buckets must sum to total
    all_buckets = (computed_scored + computed_incomplete + computed_premarket
                   + computed_pediatric)
    if all_buckets != computed_total:
        issues.append(
            f"Count arithmetic broken: {computed_scored}+{computed_incomplete}"
            f"+{computed_premarket}+{computed_pediatric}(pediatric) != {computed_total}"
        )

    # Report actual counts (for the report)
    summary_lines = [
        f"  scored:                  computed={computed_scored}  header={header_scored}  reported={REPORTED_SCORED}",
        f"  unscoreable_incomplete:  computed={computed_incomplete}  header={header_incomplete}  reported={REPORTED_INCOMPLETE}",
        f"  unscoreable_premarket:   computed={computed_premarket}  header={header_premarket}  reported={REPORTED_PREMARKET}",
        f"  unscoreable_pediatric:   computed={computed_pediatric}  header={header_pediatric}  reported={REPORTED_PEDIATRIC}  (v4+)",
        f"  total:                   computed={computed_total}  header={header_total}  reported={REPORTED_TOTAL}",
    ]

    return (len(issues) == 0), issues, summary_lines


# ── Report writer ─────────────────────────────────────────────────────────────

def write_report(
    results_summary: dict[str, Any],
    path: Path,
) -> None:
    lines: list[str] = []
    a = lines.append

    a("# SIE Supplement Corpus v3 — QA Audit Report")
    a("")
    a(f"**Corpus file:** `_corpus_run_full_v3.json`  ")
    a(f"**Audit script:** `qa_audit.py`  ")
    a(f"**Date:** run deterministically from corpus JSON — no network calls  ")
    a("")

    overall = all(results_summary[k]["passed"] for k in results_summary)
    a(f"## Overall Verdict: {'PASS' if overall else 'FAIL'}")
    a("")

    check_labels = {
        "traceability": "Check 1: TRACEABILITY",
        "off_ban": "Check 2: OFF BAN",
        "fabrication": "Check 3: NO FABRICATION",
        "distribution": "Check 4: DISTRIBUTION INTEGRITY",
        "unscoreable": "Check 5: UNSCOREABLE COMPLETENESS",
    }

    for key, label in check_labels.items():
        info = results_summary[key]
        status = "PASS" if info["passed"] else "FAIL"
        a(f"---")
        a(f"### {label}: {status}")
        a("")
        for detail_line in info.get("details", []):
            a(detail_line)
        a("")

    a("---")
    a("*Generated by qa_audit.py — read-only, no engine or corpus files modified.*")

    path.write_text("\n".join(lines), encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    print("=" * 70)
    print("SIE SUPPLEMENT CORPUS v3 — PRE-LAUNCH QA AUDIT")
    print("=" * 70)

    corpus = load_corpus()
    results = corpus.get("results", [])

    # ── Check 1 ───────────────────────────────────────────────────────────────
    t_pass, missing_dose, missing_source = check_traceability(results)
    print(f"\n[CHECK 1] TRACEABILITY: {'PASS' if t_pass else 'FAIL'}")
    print(f"  Scored SKUs: {len(scored_results(results))}")
    if missing_dose:
        print(f"  Missing dose ({len(missing_dose)}):")
        for l in missing_dose: print(l)
    else:
        print("  Missing dose: 0  [OK]")
    if missing_source:
        print(f"  Missing source_url ({len(missing_source)}):")
        for l in missing_source: print(l)
    else:
        print("  Missing source_url: 0  [OK]")

    trace_details: list[str] = []
    trace_details.append(f"- Scored SKU count: {len(scored_results(results))}")
    if missing_dose:
        trace_details.append(f"- **FAIL: {len(missing_dose)} scored SKUs missing dose:**")
        trace_details.extend(missing_dose)
    else:
        trace_details.append("- Missing dose: 0 — OK")
    if missing_source:
        trace_details.append(f"- **FAIL: {len(missing_source)} scored SKUs missing source_url:**")
        trace_details.extend(missing_source)
    else:
        trace_details.append("- Missing source_url: 0 — OK")

    # ── Check 2 ───────────────────────────────────────────────────────────────
    off_pass, off_hits = check_off_ban()
    print(f"\n[CHECK 2] OFF BAN: {'PASS' if off_pass else 'FAIL'}")
    files_scanned = (
        1
        + len(list(CACHE_DIR.glob("*.json")))
        + len(list(SKUS_FULL_DIR.glob("*.json")))
    )
    print(f"  Files scanned: {files_scanned}")
    if off_hits:
        print(f"  OFF hits ({len(off_hits)}):")
        for l in off_hits: print(l)
    else:
        print("  OFF references: 0  [OK]")

    off_details: list[str] = [f"- Files scanned: {files_scanned}"]
    if off_hits:
        off_details.append(f"- **FAIL: {len(off_hits)} files contain OFF references:**")
        off_details.extend(off_hits)
    else:
        off_details.append("- OFF references found: 0 — OK")

    # ── Check 3 ───────────────────────────────────────────────────────────────
    fab_pass, fab_fails, nd_flags = check_fabrication(results)
    print(f"\n[CHECK 3] NO FABRICATION: {'PASS' if fab_pass else 'FAIL'}")
    print(f"  name_derived scored total: {len([r for r in scored_results(results) if r.get('acquisition_method')=='name_derived'])}")
    if fab_fails:
        print(f"  HARD FAIL — omega3+name_derived scored ({len(fab_fails)}):")
        for l in fab_fails: print(l)
    else:
        print("  omega3+name_derived scored: 0  [OK]")
    print(f"  name_derived entries with numeric dose (audit enumeration): {len(nd_flags)}")

    fab_details: list[str] = []
    fab_details.append(
        f"- name_derived scored count: "
        f"{len([r for r in scored_results(results) if r.get('acquisition_method')=='name_derived'])}"
    )
    if fab_fails:
        fab_details.append(
            f"- **HARD FAIL: {len(fab_fails)} scored omega-3 SKUs from name_derived "
            f"(dose cannot be verified from product name):**"
        )
        fab_details.extend(fab_fails)
    else:
        fab_details.append("- omega3+name_derived scored: 0 — OK")
    if nd_flags:
        fab_details.append(
            f"- Enumeration (non-omega3 name_derived with numeric dose — dose from "
            f"product name, expected): {len(nd_flags)} entries"
        )
        for l in nd_flags:
            fab_details.append(l)

    # ── Check 4 ───────────────────────────────────────────────────────────────
    dist_pass, computed_dist, header_dist, dist_detail = check_distribution(corpus)
    print(f"\n[CHECK 4] DISTRIBUTION INTEGRITY: {'PASS' if dist_pass else 'FAIL'}")
    print(dist_detail)

    dist_details: list[str] = ["```", dist_detail, "```"]

    # ── Check 5 ───────────────────────────────────────────────────────────────
    unsc_pass, unsc_issues, unsc_summary = check_unscoreable(corpus)
    print(f"\n[CHECK 5] UNSCOREABLE COMPLETENESS: {'PASS' if unsc_pass else 'FAIL'}")
    for l in unsc_summary: print(l)
    if unsc_issues:
        print(f"  Issues ({len(unsc_issues)}):")
        for l in unsc_issues: print(f"    {l}")

    unsc_details: list[str] = list(unsc_summary)
    if unsc_issues:
        unsc_details.append(f"- **FAIL: {len(unsc_issues)} issues:**")
        unsc_details.extend([f"  {l}" for l in unsc_issues])
    else:
        unsc_details.append("- All counts consistent and outcomes valid — OK")

    # ── Summary ───────────────────────────────────────────────────────────────
    results_summary = {
        "traceability": {"passed": t_pass, "details": trace_details},
        "off_ban": {"passed": off_pass, "details": off_details},
        "fabrication": {"passed": fab_pass, "details": fab_details},
        "distribution": {"passed": dist_pass, "details": dist_details},
        "unscoreable": {"passed": unsc_pass, "details": unsc_details},
    }

    write_report(results_summary, REPORT_FILE)

    overall = all(v["passed"] for v in results_summary.values())
    print("\n" + "=" * 70)
    checks = [
        ("TRACEABILITY", t_pass),
        ("OFF BAN", off_pass),
        ("NO FABRICATION", fab_pass),
        ("DISTRIBUTION", dist_pass),
        ("UNSCOREABLE", unsc_pass),
    ]
    for name, passed in checks:
        print(f"  {name:<20}: {'PASS' if passed else 'FAIL'}")
    print("-" * 70)
    print(f"  OVERALL: {'PASS' if overall else 'FAIL'}")
    print("=" * 70)
    print(f"\nReport written to: {REPORT_FILE}")

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
