#!/usr/bin/env python3
"""
Bari Insight-Line Editorial Balance Validator
validate_insight_lines.py

Validates a tagged insight-line set against editorial thresholds defined in
insight_line_spec_v1.md. Checks ratio balance, contradiction fatigue,
weak-line patterns, and abstract/framework language.

Usage:
    python validate_insight_lines.py input.json
    python validate_insight_lines.py input.json --category "מעדנים"
    python validate_insight_lines.py input.json --output report.json
    cat input.json | python validate_insight_lines.py -

Input JSON schema:
    [
      {
        "product": "Product name (Hebrew)",
        "line":    "Insight line text (Hebrew)",
        "type":    "T1" | "T2" | "T3"
      }
    ]

Output: human-readable report to stdout + optional JSON report file.
"""

import sys
import io
import json
import re
import argparse
from dataclasses import dataclass, field
from typing import Optional

# Force UTF-8 stdout so Hebrew characters survive Windows cp1252 terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Thresholds  (from insight_line_spec_v1.md + mobile_geometry_checklist_v1.md)
# ---------------------------------------------------------------------------

THRESHOLDS = {
    "T1": {"min": 0.50, "max": 0.60, "label": "Composition Fact"},
    "T2": {"min": 0.20, "max": 0.30, "label": "Contradiction"},
    "T3": {"min": 0.15, "max": 0.20, "label": "Position Fact"},
}

MAX_WORDS = 12                # hard limit per spec
MIN_WORDS = 3                 # below this is too sparse to be an observation

# Contradiction-fatigue thresholds
CONSECUTIVE_T2_WARN   = 3    # 3+ consecutive T2 lines → WARN
CONSECUTIVE_T2_SEVERE = 5    # 5+ consecutive T2 lines → FAIL
WINDOW_SIZE           = 10   # sliding window width
WINDOW_T2_WARN        = 4    # 4+ T2 in any 10-line window → WARN
WINDOW_T2_SEVERE      = 6    # 6+ T2 in any 10-line window → FAIL


# ---------------------------------------------------------------------------
# Pattern lists  (Hebrew — matched as substrings or regex)
# ---------------------------------------------------------------------------

# Words / phrases that constitute editorial judgment (never allowed)
FORBIDDEN = [
    "לא בריא",
    "לא מומלץ",
    "כדאי להימנע",
    "מטעה",
    "גרוע",
    "מצוין",
    "מומלץ לקנות",
    "בריא יותר",
    "בריא פחות",
    "לא כדאי",
    "הימנעו",
    "אל תקנו",
    "אסור לאכול",
    "מסוכן",
]

# Causal connectors that turn an observation into an explanation
CAUSAL = [
    "בגלל ש",
    "בגלל",
    "לכן ",
    "ולכן",
    "משמע ש",
    "משמע",
    "כתוצאה מ",
    "לפיכך",
    " כי ה",   # "כי" mid-sentence acting as "because" (space-padded to avoid false matches)
    " כי ה",
]

# Internal framework terms that must never reach consumer surfaces
FRAMEWORK_TERMS = [
    "NOVA",
    "nova",
    "BSIP",
    "bsip",
    " cap",
    "cap=",
    "routing",
    "dimension",
    "structural_class",
    "additive_marker",
    "processing_quality",
    "glycemic_quality",
    "hard_anchor",
    "score_engine",
    "binding_cap",
    "data_sufficiency",
    "nova_proxy",
]

# Vague patterns that provide no specific observation (regex)
VAGUE_PATTERNS = [
    (r"^ציון (נמוך|גבוה|ממוצע|בינוני)$",
     "bare score label — no product observation"),
    (r"קטגוריית ביניים",
     "framework-adjacent: 'קטגוריית ביניים' has no consumer meaning"),
    (r"מוצר ביניים",
     "vague: 'מוצר ביניים' has no specific content"),
    (r"ציון קרוב לממוצע(?!\s*ה)",
     "references internal category average — not consumer-facing"),
    (r"ציון ממוצע(?!\s*של\s*\d)",
     "vague score reference without specific number"),
    (r"ציון (נמוך|גבוה) יחסית$",
     "hedged score label — remove 'יחסית' or add a specific number"),
    (r"רמת איכות",
     "vague quality label — specify what was observed"),
]

# Score-explanation patterns: lines that explain the score (not the product)
SCORE_EXPLANATION = [
    r"הציון נמוך כי",
    r"הציון גבוה כי",
    r"הציון נמוך בגלל",
    r"הציון גבוה בגלל",
    r"הציון נמוך ל",
    r"קיבל ציון נמוך",
    r"קיבל ציון גבוה",
    r"הציון שלו",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class InsightLine:
    index: int
    product: str
    line: str
    type_label: str       # "T1", "T2", or "T3"
    word_count: int = 0

    def __post_init__(self):
        self.word_count = len(self.line.split())


@dataclass
class Issue:
    severity: str         # "FAIL", "WARN", "INFO"
    check: str            # check category name
    line_index: Optional[int]
    product: Optional[str]
    line: Optional[str]
    message: str


@dataclass
class ValidationReport:
    category: str
    total_lines: int
    counts: dict
    ratios: dict
    issues: list = field(default_factory=list)
    verdict: str = "PASS"   # PASS | WARN | FAIL

    def add(self, issue: Issue):
        self.issues.append(issue)
        if issue.severity == "FAIL" and self.verdict != "FAIL":
            self.verdict = "FAIL"
        elif issue.severity == "WARN" and self.verdict == "PASS":
            self.verdict = "WARN"


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

class InsightLineValidator:

    def __init__(self, lines: list[InsightLine], category: str = ""):
        self.lines = lines
        self.category = category
        self.total = len(lines)
        self.counts = {"T1": 0, "T2": 0, "T3": 0, "UNKNOWN": 0}
        self.ratios = {}

        for ln in lines:
            label = ln.type_label.upper()
            if label in self.counts:
                self.counts[label] += 1
            else:
                self.counts["UNKNOWN"] += 1

        for t in ("T1", "T2", "T3"):
            self.ratios[t] = self.counts[t] / self.total if self.total > 0 else 0.0

        self.report = ValidationReport(
            category=self.category,
            total_lines=self.total,
            counts=dict(self.counts),
            ratios=dict(self.ratios),
        )

    # --- Check 1: ratio balance ------------------------------------------------

    def check_ratios(self):
        """Validate T1/T2/T3 distribution against spec thresholds."""
        for t, spec in THRESHOLDS.items():
            ratio = self.ratios[t]
            pct = ratio * 100
            lo = spec["min"] * 100
            hi = spec["max"] * 100

            if t == "T2" and ratio > THRESHOLDS["T2"]["max"]:
                excess_pp = pct - hi
                sev = "FAIL" if excess_pp > 10 else "WARN"
                self.report.add(Issue(
                    severity=sev,
                    check="ratio_balance",
                    line_index=None,
                    product=None,
                    line=None,
                    message=(
                        f"{t} ({spec['label']}): {pct:.1f}% — "
                        f"exceeds {hi:.0f}% ceiling by {excess_pp:.1f}pp. "
                        f"Convert ~{round((ratio - spec['max']) * self.total)} "
                        f"T2 lines to T1."
                    ),
                ))
            elif ratio < spec["min"]:
                gap_pp = lo - pct
                self.report.add(Issue(
                    severity="WARN",
                    check="ratio_balance",
                    line_index=None,
                    product=None,
                    line=None,
                    message=(
                        f"{t} ({spec['label']}): {pct:.1f}% — "
                        f"below {lo:.0f}% floor by {gap_pp:.1f}pp."
                    ),
                ))
            elif ratio > spec["max"]:
                self.report.add(Issue(
                    severity="INFO",
                    check="ratio_balance",
                    line_index=None,
                    product=None,
                    line=None,
                    message=(
                        f"{t} ({spec['label']}): {pct:.1f}% — "
                        f"slightly above {hi:.0f}% ceiling. Monitor."
                    ),
                ))

        if self.counts["UNKNOWN"] > 0:
            self.report.add(Issue(
                severity="WARN",
                check="ratio_balance",
                line_index=None,
                product=None,
                line=None,
                message=(
                    f"{self.counts['UNKNOWN']} line(s) have unrecognised type labels. "
                    f"Valid labels: T1, T2, T3."
                ),
            ))

    # --- Check 2: contradiction fatigue ----------------------------------------

    def check_contradiction_fatigue(self):
        """Detect consecutive T2 runs and high-density windows."""
        # Consecutive runs
        run_start = None
        run_len = 0
        runs = []

        for i, ln in enumerate(self.lines):
            if ln.type_label.upper() == "T2":
                if run_len == 0:
                    run_start = i
                run_len += 1
            else:
                if run_len >= CONSECUTIVE_T2_WARN:
                    runs.append((run_start, i - 1, run_len))
                run_len = 0
                run_start = None
        if run_len >= CONSECUTIVE_T2_WARN:
            runs.append((run_start, len(self.lines) - 1, run_len))

        for start, end, length in runs:
            sev = "FAIL" if length >= CONSECUTIVE_T2_SEVERE else "WARN"
            self.report.add(Issue(
                severity=sev,
                check="contradiction_fatigue",
                line_index=start,
                product=None,
                line=None,
                message=(
                    f"Lines {start + 1}–{end + 1}: {length} consecutive T2 "
                    f"(contradiction) lines. "
                    + ("Severe fatigue risk — reorder or convert." if length >= CONSECUTIVE_T2_SEVERE
                       else "Reorder T2 lines with T1 lines between them.")
                ),
            ))

        # Sliding window density
        if self.total >= WINDOW_SIZE:
            for w_start in range(self.total - WINDOW_SIZE + 1):
                window = self.lines[w_start: w_start + WINDOW_SIZE]
                t2_in_window = sum(1 for ln in window if ln.type_label.upper() == "T2")
                if t2_in_window >= WINDOW_T2_WARN:
                    sev = "FAIL" if t2_in_window >= WINDOW_T2_SEVERE else "WARN"
                    self.report.add(Issue(
                        severity=sev,
                        check="contradiction_fatigue",
                        line_index=w_start,
                        product=None,
                        line=None,
                        message=(
                            f"Window lines {w_start + 1}–{w_start + WINDOW_SIZE}: "
                            f"{t2_in_window} T2 lines in {WINDOW_SIZE}-line window "
                            f"(threshold: {WINDOW_T2_WARN}). "
                            f"Distribute contradiction lines more evenly."
                        ),
                    ))

    # --- Check 3: weak lines ----------------------------------------------------

    def check_weak_lines(self):
        """Detect lines that are too short, too long, or structurally empty."""
        for ln in self.lines:
            # Length check
            if ln.word_count > MAX_WORDS:
                self.report.add(Issue(
                    severity="WARN",
                    check="weak_line",
                    line_index=ln.index,
                    product=ln.product,
                    line=ln.line,
                    message=(
                        f"Line too long: {ln.word_count} words "
                        f"(max {MAX_WORDS}). Cut or split."
                    ),
                ))

            if ln.word_count < MIN_WORDS:
                self.report.add(Issue(
                    severity="WARN",
                    check="weak_line",
                    line_index=ln.index,
                    product=ln.product,
                    line=ln.line,
                    message=(
                        f"Line too short: {ln.word_count} words — "
                        f"too sparse to be a useful observation. Add a specific fact."
                    ),
                ))

            # Forbidden words
            for fw in FORBIDDEN:
                if fw in ln.line:
                    self.report.add(Issue(
                        severity="FAIL",
                        check="weak_line",
                        line_index=ln.index,
                        product=ln.product,
                        line=ln.line,
                        message=f"Forbidden word/phrase: \"{fw}\" — editorial judgment. Remove.",
                    ))

            # Causal connectors
            for cw in CAUSAL:
                if cw in ln.line:
                    self.report.add(Issue(
                        severity="WARN",
                        check="weak_line",
                        line_index=ln.index,
                        product=ln.product,
                        line=ln.line,
                        message=(
                            f"Causal connector: \"{cw.strip()}\" — "
                            f"line explains the score instead of observing the product. "
                            f"Cut at the causal word."
                        ),
                    ))

            # Score-explanation patterns
            for pattern in SCORE_EXPLANATION:
                if re.search(pattern, ln.line):
                    self.report.add(Issue(
                        severity="WARN",
                        check="weak_line",
                        line_index=ln.index,
                        product=ln.product,
                        line=ln.line,
                        message=(
                            f"Score explanation: line describes why the score is "
                            f"what it is, not what the product is. Rewrite as "
                            f"an observation."
                        ),
                    ))

    # --- Check 4: abstract language ---------------------------------------------

    def check_abstract_language(self):
        """Detect framework terms, vague patterns, and internal language."""
        for ln in self.lines:
            # Framework terms
            for term in FRAMEWORK_TERMS:
                if term in ln.line:
                    self.report.add(Issue(
                        severity="FAIL",
                        check="abstract_language",
                        line_index=ln.index,
                        product=ln.product,
                        line=ln.line,
                        message=(
                            f"Framework term: \"{term}\" — "
                            f"internal architecture language. "
                            f"Replace with consumer-facing equivalent "
                            f"(see insight_line_spec_v1.md category translation table)."
                        ),
                    ))

            # Vague patterns
            for pattern, explanation in VAGUE_PATTERNS:
                if re.search(pattern, ln.line):
                    self.report.add(Issue(
                        severity="WARN",
                        check="abstract_language",
                        line_index=ln.index,
                        product=ln.product,
                        line=ln.line,
                        message=f"Vague pattern: {explanation}",
                    ))

    # --- Run all checks ---------------------------------------------------------

    def run(self) -> ValidationReport:
        self.check_ratios()
        self.check_contradiction_fatigue()
        self.check_weak_lines()
        self.check_abstract_language()
        return self.report


# ---------------------------------------------------------------------------
# Deduplication: collapse overlapping window warnings into one per cluster
# ---------------------------------------------------------------------------

def deduplicate_window_issues(report: ValidationReport) -> ValidationReport:
    """
    Sliding-window checks produce overlapping reports for the same T2 cluster.
    Strategy: group window issues into non-overlapping clusters by finding
    contiguous runs of window-start positions, then keep only the worst
    (highest-severity, highest T2 count) issue from each cluster.
    """
    window_issues   = [i for i in report.issues
                       if i.check == "contradiction_fatigue"
                       and "Window lines" in i.message]
    other_issues    = [i for i in report.issues
                       if not (i.check == "contradiction_fatigue"
                               and "Window lines" in i.message)]

    if not window_issues:
        return report

    # Sort by start position
    window_issues.sort(key=lambda i: i.line_index if i.line_index is not None else 0)

    # Group into non-overlapping clusters: a new cluster starts when the
    # current window start is >= previous cluster end.
    clusters: list[list[Issue]] = []
    current_cluster: list[Issue] = []
    cluster_end = -1

    for issue in window_issues:
        start = issue.line_index or 0
        end   = start + WINDOW_SIZE

        if start >= cluster_end:
            if current_cluster:
                clusters.append(current_cluster)
            current_cluster = [issue]
            cluster_end = end
        else:
            current_cluster.append(issue)
            cluster_end = max(cluster_end, end)

    if current_cluster:
        clusters.append(current_cluster)

    # From each cluster keep the worst issue:
    # FAIL beats WARN; within same severity, pick the one with the highest
    # T2 count (extracted from the message string).
    def _t2_count(issue: Issue) -> int:
        m = re.search(r"(\d+) T2 lines in", issue.message)
        return int(m.group(1)) if m else 0

    sev_rank = {"FAIL": 2, "WARN": 1, "INFO": 0}

    kept = []
    for cluster in clusters:
        best = max(cluster,
                   key=lambda i: (sev_rank.get(i.severity, 0), _t2_count(i)))
        kept.append(best)

    report.issues = other_issues + kept
    # Re-evaluate verdict after dedup
    report.verdict = "PASS"
    for issue in report.issues:
        if issue.severity == "FAIL":
            report.verdict = "FAIL"
            break
        if issue.severity == "WARN" and report.verdict == "PASS":
            report.verdict = "WARN"

    return report


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

_SEV_SYMBOL = {"FAIL": "✗", "WARN": "△", "INFO": "·"}
_SEV_LABEL  = {"FAIL": "FAIL", "WARN": "WARN", "INFO": "INFO"}


def _section(title: str) -> str:
    return f"\n{'─' * 60}\n{title}\n{'─' * 60}"


def format_report(report: ValidationReport) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("  BARI INSIGHT-LINE EDITORIAL BALANCE VALIDATOR")
    lines.append("=" * 60)

    cat = report.category or "(no category specified)"
    lines.append(f"  Category : {cat}")
    lines.append(f"  Lines    : {report.total_lines}")
    lines.append("")

    # --- Ratio summary -------------------------------------------------------
    lines.append(_section("RATIO ANALYSIS"))
    lines.append("")
    for t, spec in THRESHOLDS.items():
        count = report.counts[t]
        ratio = report.ratios[t]
        pct   = ratio * 100
        lo    = spec["min"] * 100
        hi    = spec["max"] * 100
        bar   = "█" * round(pct / 5)
        target = f"[{lo:.0f}–{hi:.0f}%]"

        if t == "T2" and ratio > spec["max"]:
            status = " ← OVER LIMIT"
        elif ratio < spec["min"]:
            status = " ← UNDER"
        elif ratio > spec["max"]:
            status = " ← OVER"
        else:
            status = " ✓"

        lines.append(
            f"  {t} {spec['label']:<20} "
            f"{count:3d}/{report.total_lines} "
            f"({pct:4.1f}%) {target:<12} {bar:<14}{status}"
        )

    if report.counts["UNKNOWN"]:
        lines.append(f"\n  ⚠ {report.counts['UNKNOWN']} lines have unrecognised type labels.")

    # --- Issues by category --------------------------------------------------
    checks_order = ["ratio_balance", "contradiction_fatigue", "weak_line", "abstract_language"]
    check_labels = {
        "ratio_balance":        "RATIO BALANCE ISSUES",
        "contradiction_fatigue":"CONTRADICTION FATIGUE",
        "weak_line":            "WEAK LINE DETECTION",
        "abstract_language":    "ABSTRACT / FRAMEWORK LANGUAGE",
    }

    for check in checks_order:
        issues_in_check = [i for i in report.issues if i.check == check]
        if not issues_in_check:
            lines.append(_section(check_labels[check]))
            lines.append("  No issues.")
            continue

        lines.append(_section(check_labels[check]))
        for issue in issues_in_check:
            sym  = _SEV_SYMBOL[issue.severity]
            slab = _SEV_LABEL[issue.severity]
            if issue.line_index is not None:
                loc = f"Line {issue.line_index + 1}"
                if issue.product:
                    loc += f"  [{issue.product}]"
            else:
                loc = "Global"

            lines.append(f"\n  {sym} {slab}  {loc}")
            if issue.line:
                lines.append(f"    \"{issue.line}\"")
            lines.append(f"    → {issue.message}")

    # --- Verdict -------------------------------------------------------------
    lines.append("")
    lines.append("=" * 60)
    counts_by_sev = {s: sum(1 for i in report.issues if i.severity == s)
                     for s in ("FAIL", "WARN", "INFO")}
    sev_str = "  |  ".join(
        f"{s}: {counts_by_sev[s]}"
        for s in ("FAIL", "WARN", "INFO")
        if counts_by_sev[s] > 0
    ) or "No issues"

    verdict_label = {
        "PASS": "PASS  ✓  Ready for launch.",
        "WARN": "WARN  △  Review flagged items before launch.",
        "FAIL": "FAIL  ✗  Must resolve FAIL conditions before launch.",
    }[report.verdict]

    lines.append(f"  VERDICT : {verdict_label}")
    lines.append(f"  Issues  : {sev_str}")
    lines.append("=" * 60)

    return "\n".join(lines)


def build_json_report(report: ValidationReport) -> dict:
    return {
        "category":    report.category,
        "total_lines": report.total_lines,
        "counts":      report.counts,
        "ratios":      {k: round(v, 4) for k, v in report.ratios.items()},
        "thresholds":  {k: {"min": v["min"], "max": v["max"]} for k, v in THRESHOLDS.items()},
        "verdict":     report.verdict,
        "issue_counts": {
            s: sum(1 for i in report.issues if i.severity == s)
            for s in ("FAIL", "WARN", "INFO")
        },
        "issues": [
            {
                "severity":   i.severity,
                "check":      i.check,
                "line_index": i.line_index,
                "product":    i.product,
                "line":       i.line,
                "message":    i.message,
            }
            for i in report.issues
        ],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def load_input(source: str) -> list[dict]:
    if source == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(source).read_text(encoding="utf-8")
    return json.loads(raw)


def parse_lines(data: list[dict]) -> list[InsightLine]:
    result = []
    for i, item in enumerate(data):
        result.append(InsightLine(
            index=i,
            product=item.get("product", ""),
            line=item.get("line", ""),
            type_label=item.get("type", "UNKNOWN").strip().upper(),
        ))
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Bari Insight-Line Editorial Balance Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "input",
        help="Path to JSON input file, or '-' to read from stdin",
    )
    parser.add_argument(
        "--category",
        default="",
        help="Category label for the report header (e.g. מעדנים)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write JSON report",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 on any WARN (not just FAIL)",
    )
    args = parser.parse_args()

    try:
        data  = load_input(args.input)
        lines = parse_lines(data)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"ERROR loading input: {e}", file=sys.stderr)
        sys.exit(2)

    if not lines:
        print("ERROR: no lines found in input.", file=sys.stderr)
        sys.exit(2)

    validator = InsightLineValidator(lines, category=args.category)
    report    = validator.run()
    report    = deduplicate_window_issues(report)

    print(format_report(report))

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(
            json.dumps(build_json_report(report), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\nJSON report written: {args.output}")

    if report.verdict == "FAIL":
        sys.exit(1)
    if args.strict and report.verdict == "WARN":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    from pathlib import Path
    main()
