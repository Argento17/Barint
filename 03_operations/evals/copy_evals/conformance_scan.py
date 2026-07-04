#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conformance_scan.py — TASK-506 D1 (+ D1-extension, TASK-506 Part A)

Reusable Hebrew copy-conformance scanner for Bari comparison pages.

Walks the ACTIVE bari-web/src/data/comparisons/*_frontend_v*.json files (one
per live category — see ACTIVE_FILES below, resolved by tracing the Next.js
data-loader imports, not by filename recency) AND the hardcoded Hebrew
string-literal copy in each category's *-page-data.ts loader (hero /
prologue / category-note-fallback / methodology — see ACTIVE_TS_FILES below,
same resolution method), and flags consumer-copy strings against the
editorial standard codified in the 2026-07-04 owner naturalness-labeling
session:

  - sodium_term    (DETERMINISTIC)        "סודיום"/"סודים" instead of "נתרן"
  - brand_spelling (DETERMINISTIC-w/review) standalone "ברי" instead of "בארי"
  - em_dash        (count, minimize)       U+2014 "—"
  - antithesis     (owner ban)             "X, not Y" / "ו/אלא לא" framing
  - number_density (advisory heuristic)    >=4 nutrition figures restated in one line

TOOLING ONLY. This script never writes to any *_frontend_v*.json or
*-page-data.ts — it only reads them and emits reports under
03_operations/reports/copy_conformance/. The product-descriptions FREEZE
(owner ruling) means no lane may use this script's output to auto-edit
consumer copy; it exists to feed the owner's manual rewrite pass.

Usage:
    python conformance_scan.py
    python conformance_scan.py --json-only     # skip the .md report
    python conformance_scan.py --category bread  # single category, for iteration

Rules now live in copy_rules.py (TASK-506 D3) — this module imports them
rather than defining them, so the scanner and the copy sign-off gate
(integrations/clients/hebrew_readability.py) share ONE implementation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]
COMPARISONS_DIR = REPO_ROOT / "bari-web" / "src" / "data" / "comparisons"
TS_PAGE_DATA_DIR = REPO_ROOT / "bari-web" / "src" / "lib" / "comparisons"
REPORT_DIR = REPO_ROOT / "03_operations" / "reports" / "copy_conformance"

# Shared rule implementation (TASK-506 D3) — same directory, no sys.path hack needed.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import copy_rules  # noqa: E402

# ---------------------------------------------------------------------------
# Active-file resolution
# ---------------------------------------------------------------------------
# Resolved 2026-07-04 (TASK-506 D1) by grepping every `*-page-data.ts` loader
# under bari-web/src/lib/comparisons for its `import rawCorpus from
# "@/data/comparisons/<file>.json"` line — NOT by filename version number,
# since several categories have superseded JSON files still sitting in the
# directory (see ORPHAN_FILES below). Re-verify this map if a new version
# ships; do not assume "highest vN" is live.
ACTIVE_FILES: dict[str, str] = {
    "bread": "bread_frontend_v4.json",
    "brined_cheeses": "brined_cheeses_frontend_v2.json",
    "cakes_hard_cookies": "cakes_hard_cookies_frontend_v1.json",
    "cereals": "cereals_frontend_v2.json",
    "cheese": "cheese_frontend_v4.json",
    "chocolate_bars": "chocolate_bars_frontend_v1.json",
    "chocolate_tablets": "chocolate_tablets_frontend_v1.json",
    "cookies_coffee": "cookies_coffee_frontend_v2.json",
    "crackers": "crackers_frontend_v1.json",
    "granola": "granola_frontend_v2.json",
    "hard_cheeses": "hard_cheeses_frontend_v4.json",
    "hummus": "hummus_frontend_v5.json",
    "juices": "juices_frontend_v3.json",
    "milk": "milk_frontend_v1.json",
    "protein_combined": "protein_combined_frontend_v2.json",
    "snacks": "snacks_frontend_v5.json",
}

# JSON files present in the directory but NOT imported by any -page-data.ts
# loader (verified by `grep -rn "<filename>" bari-web/src`). Kept here so the
# scanner never silently picks these up if a future glob-based rewrite is
# attempted, and so the orphan is visible in the report.
ORPHAN_FILES: list[str] = [
    "bread_frontend_v3.json",  # superseded by bread_frontend_v4.json; zero imports
]

# ---------------------------------------------------------------------------
# Active TS page-data file per category (TASK-506 Part A — D1 coverage
# extension). Consumer copy also lives OUTSIDE the JSON family: hardcoded
# Hebrew string literals in bari-web/src/lib/comparisons/*-page-data.ts (hero /
# prologue / category-note-fallback / methodology). Resolved the SAME way as
# ACTIVE_FILES above — by grepping each *-page-data.ts for the exact
# `"@/data/comparisons/<active json>.json"` import line, not by filename
# guessing (two categories, bread and hummus, have more than one *-page-data.ts
# file on disk; only the one importing the ACTIVE json is live).
ACTIVE_TS_FILES: dict[str, str] = {
    "bread": "bread-comparison-page-data.ts",
    "brined_cheeses": "brined-cheeses-page-data.ts",
    "cakes_hard_cookies": "cakes-hard-cookies-page-data.ts",
    "cereals": "cereals-page-data.ts",
    "cheese": "cheese-page-data.ts",
    "chocolate_bars": "chocolate-bars-comparison-page-data.ts",
    "chocolate_tablets": "chocolate-tablets-comparison-page-data.ts",
    "cookies_coffee": "cookies-coffee-page-data.ts",
    "crackers": "crackers-page-data.ts",
    "granola": "granola-page-data.ts",
    "hard_cheeses": "hard-cheeses-page-data.ts",
    "hummus": "hummus-comparison-page-data.ts",
    "juices": "juices-page-data.ts",
    "milk": "milk-page-data.ts",
    "protein_combined": "protein-bars-comparison-page-data.ts",
    "snacks": "snacks-comparison-page-data.ts",
}

# ---------------------------------------------------------------------------
# Rules — imported from copy_rules.py (TASK-506 D3), the single shared
# implementation also used by the copy sign-off gate
# (integrations/clients/hebrew_readability.py). No local regex duplication.
# ---------------------------------------------------------------------------

# Re-exported for any external caller that imported these names directly off
# this module before D3 (kept for backward compatibility; the canonical home
# is now copy_rules.py).
SODIUM_TERM_RE = copy_rules.SODIUM_TERM_RE
BRAND_SPELLING_RE = copy_rules.BRAND_SPELLING_RE
EM_DASH_CHAR = copy_rules.EM_DASH_CHAR
ANTITHESIS_RE = copy_rules.ANTITHESIS_RE

rule_sodium_term = copy_rules.rule_sodium_term
rule_brand_spelling = copy_rules.rule_brand_spelling
rule_em_dash = copy_rules.rule_em_dash
rule_antithesis = copy_rules.rule_antithesis
rule_number_density = copy_rules.rule_number_density

# Ordered so deterministic rules surface first in reports.
RULES = copy_rules.RULES


def scan_text(text: str) -> list[dict]:
    """Run all rules against one copy string. Returns list of fired-rule dicts."""
    if not isinstance(text, str) or not text.strip():
        return []
    fired = []
    for rule_fn in RULES:
        result = rule_fn(text)
        if result:
            fired.append(result)
    return fired


# ---------------------------------------------------------------------------
# Field extraction — schema varies per category; this is deliberately
# name-driven (not path-driven) so it tolerates the known shape variants
# (positiveSignals as list[str] OR list[{text,...}]; consumerExplanation as
# str OR dict; bariInterpretation using label/interpretation OR
# label_he/explanation_he).
# ---------------------------------------------------------------------------

def _add(rows: list[tuple[str, str]], field: str, value: Any) -> None:
    if isinstance(value, str) and value.strip():
        rows.append((field, value))


def extract_product_fields(product: dict) -> list[tuple[str, str]]:
    """Return [(field_label, text), ...] for one product's consumer-copy strings."""
    rows: list[tuple[str, str]] = []

    _add(rows, "rowVerdict", product.get("rowVerdict"))
    _add(rows, "insightLine", product.get("insightLine"))
    _add(rows, "consumerTakeaway", product.get("consumerTakeaway"))

    # Top-level consumerExplanation (rare legacy shape; crackers-style)
    ce_top = product.get("consumerExplanation")
    if isinstance(ce_top, str):
        _add(rows, "consumerExplanation", ce_top)
    elif isinstance(ce_top, dict):
        for k in ("context", "takeaway", "whyRated"):
            _add(rows, f"consumerExplanation.{k}", ce_top.get(k))
        for listname in ("good", "watchOut"):
            for i, item in enumerate(ce_top.get(listname) or []):
                _add(rows, f"consumerExplanation.{listname}[{i}]", item)

    exp = product.get("expansion")
    if isinstance(exp, dict):
        _add(rows, "expansion.comparisonContext", exp.get("comparisonContext"))
        _add(rows, "expansion.bottomLine", exp.get("bottomLine"))

        ce = exp.get("consumerExplanation")
        if isinstance(ce, str):
            _add(rows, "expansion.consumerExplanation", ce)
        elif isinstance(ce, dict):
            for k in ("context", "takeaway", "whyRated"):
                _add(rows, f"expansion.consumerExplanation.{k}", ce.get(k))
            for listname in ("good", "watchOut"):
                for i, item in enumerate(ce.get(listname) or []):
                    _add(rows, f"expansion.consumerExplanation.{listname}[{i}]", item)

        for listname in ("limitingFactors", "positiveSignals"):
            items = exp.get(listname) or []
            for i, item in enumerate(items):
                if isinstance(item, str):
                    _add(rows, f"expansion.{listname}[{i}]", item)
                elif isinstance(item, dict):
                    _add(rows, f"expansion.{listname}[{i}].text", item.get("text"))

    d3 = product.get("d3_processing_signal")
    if isinstance(d3, dict):
        _add(rows, "d3_processing_signal.note_he", d3.get("note_he"))
        _add(rows, "d3_processing_signal.note_he_mobile", d3.get("note_he_mobile"))

    for i, additive in enumerate(product.get("d4_additives") or []):
        if isinstance(additive, dict):
            _add(rows, f"d4_additives[{i}].explanation_he", additive.get("explanation_he"))

    for i, bi in enumerate(product.get("bariInterpretation") or []):
        if isinstance(bi, dict):
            _add(rows, f"bariInterpretation[{i}].label",
                 bi.get("label") or bi.get("label_he"))
            _add(rows, f"bariInterpretation[{i}].interpretation",
                 bi.get("interpretation") or bi.get("explanation_he"))

    return rows


def extract_page_copy_fields(page_copy: dict) -> list[tuple[str, str]]:
    """Return [(field_label, text), ...] for category-level page_copy narrative
    fields (hero / prologue / caveat / methodology). Filter chip labels and
    shelf-lens option labels are deliberately excluded — UI chrome, not
    editorial narrative."""
    rows: list[tuple[str, str]] = []

    hero = page_copy.get("hero")
    if isinstance(hero, dict):
        for k in ("title", "tagline", "eyebrow", "categoryNameHe", "topProduct"):
            _add(rows, f"page_copy.hero.{k}", hero.get(k))
    _add(rows, "page_copy.heroTitle", page_copy.get("heroTitle"))
    _add(rows, "page_copy.prologue", page_copy.get("prologue"))
    _add(rows, "page_copy.category_caveat", page_copy.get("category_caveat"))
    _add(rows, "page_copy.categoryCaveat", page_copy.get("categoryCaveat"))

    caveat = page_copy.get("caveat")
    if isinstance(caveat, dict):
        _add(rows, "page_copy.caveat.title", caveat.get("title"))
        _add(rows, "page_copy.caveat.body", caveat.get("body"))
        for i, note in enumerate(caveat.get("notes") or []):
            if isinstance(note, dict):
                _add(rows, f"page_copy.caveat.notes[{i}].title", note.get("title"))
                _add(rows, f"page_copy.caveat.notes[{i}].body", note.get("body"))

    methodology = page_copy.get("methodology")
    if isinstance(methodology, dict):
        for k in ("body", "text", "sourceNote"):
            _add(rows, f"page_copy.methodology.{k}", methodology.get(k))

    return rows


def extract_meta_fields(meta: dict) -> list[tuple[str, str]]:
    """_meta.categoryCaveat is a special case: crackers-page-data.ts reads it
    directly and renders it as the category caveat box (with a hardcoded TS
    fallback when absent) — so despite living under `_meta`, it IS
    consumer-facing and must be scanned. No other `_meta.*` field is rendered."""
    rows: list[tuple[str, str]] = []
    _add(rows, "_meta.categoryCaveat", meta.get("categoryCaveat"))
    return rows


# ---------------------------------------------------------------------------
# TS page-data literal extraction (TASK-506 Part A — D1 coverage extension)
# ---------------------------------------------------------------------------
# Consumer copy that lives directly as Hebrew string literals in
# bari-web/src/lib/comparisons/*-page-data.ts — hero titles/taglines, the
# prologue sentence arrays, the category-note *_FALLBACK constant (rendered
# only when the JSON's _meta.categoryCaveat is absent), and methodology line
# arrays. Deliberately conservative: only `const <Name> = ...;` declarations
# whose NAME matches one of the known copy-carrying suffixes are scanned, and
# only the STRING LITERALS inside that declaration's value are kept — and only
# if the literal contains at least one Hebrew character. This naturally
# excludes: TS type annotations, English identifiers/URLs, and any
# declaration that is a pure reference to JSON-sourced content (e.g.
# `cheesePrologueSentences = _pageCopy.prologue;` has no literal to extract —
# that content is already covered by the JSON-side page_copy scan, so nothing
# is double-counted). Filter-chip / shelf-lens option labels live in separate
# `*-shelf-filters.ts` files and are out of scope here, mirroring the JSON-side
# exclusion of the same UI-chrome category (see extract_page_copy_fields).

_TS_DECL_RE = re.compile(
    r"(?:export\s+)?const\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?::[^=;]*)?=\s*"
)
_TS_LITERAL_RE = re.compile(
    r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'|`((?:[^`\\]|\\.)*)`'
)
_TS_TARGET_NAME_PATTERNS = (
    re.compile(r"Hero$"),
    re.compile(r"PrologueSentences$"),
    re.compile(r"MethodologyLines$"),
    re.compile(r"CategoryNote$", re.IGNORECASE),
    re.compile(r"_FALLBACK$"),
)
_HEB_CHAR_RE = re.compile(r"[א-ת]")


def _is_ts_target_name(name: str) -> bool:
    return any(p.search(name) for p in _TS_TARGET_NAME_PATTERNS)


def _find_ts_statement_end(src: str, start: int) -> int:
    """Index of the first top-level ';' (bracket-depth 0), skipping over
    string/template literals so a ';' inside a string doesn't end the scan
    early. Falls back to end-of-source if unterminated (defensive only)."""
    depth = 0
    i, n = start, len(src)
    while i < n:
        c = src[i]
        if c in "\"'`":
            quote = c
            i += 1
            while i < n and src[i] != quote:
                if src[i] == "\\":
                    i += 1
                i += 1
            i += 1
            continue
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif c == ";" and depth <= 0:
            return i
        i += 1
    return n


def extract_ts_page_data_literals(source: str) -> list[tuple[str, str]]:
    """Return [(field_label, text), ...] of Hebrew prose string literals found
    inside copy-carrying `const` declarations in one *-page-data.ts source."""
    rows: list[tuple[str, str]] = []
    for m in _TS_DECL_RE.finditer(source):
        name = m.group(1)
        if not _is_ts_target_name(name):
            continue
        val_start = m.end()
        val_end = _find_ts_statement_end(source, val_start)
        span = source[val_start:val_end]
        idx = 0
        for lit_m in _TS_LITERAL_RE.finditer(span):
            text = lit_m.group(1) or lit_m.group(2) or lit_m.group(3) or ""
            if _HEB_CHAR_RE.search(text):
                rows.append((f"ts:{name}[{idx}]", text))
                idx += 1
    return rows


def scan_ts_category(category: str, ts_filename: str) -> tuple[list[dict], int]:
    """Scan one category's *-page-data.ts for Hebrew literal copy. Returns
    (flagged_lines, lines_scanned) — mirrors the JSON-side scan shape, tagged
    with source: 'ts' so the report can keep JSON- and TS-sourced flags
    visually separable."""
    fpath = TS_PAGE_DATA_DIR / ts_filename
    source = fpath.read_text(encoding="utf-8")
    rows = extract_ts_page_data_literals(source)
    flagged: list[dict] = []
    for field, text in rows:
        fired = scan_text(text)
        if fired:
            flagged.append({
                "barcode": None,
                "name": "(page-level copy)",
                "field": field,
                "text": text,
                "source": "ts",
                "source_file": ts_filename,
                "rules": [r["rule"] + (" (advisory)" if r.get("advisory") else "") for r in fired],
                "counts": {r["rule"]: r["count"] for r in fired},
                "detail": fired,
            })
    return flagged, len(rows)


# ---------------------------------------------------------------------------
# Per-category scan
# ---------------------------------------------------------------------------

def scan_category(category: str, filename: str, ts_filename: str | None = None) -> dict:
    fpath = COMPARISONS_DIR / filename
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)

    flagged_lines: list[dict] = []
    products = data.get("products", [])

    for idx, product in enumerate(products):
        barcode = product.get("barcode") or product.get("id") or f"__index_{idx}"
        name = product.get("name") or product.get("name_he") or ""
        for field, text in extract_product_fields(product):
            fired = scan_text(text)
            if fired:
                flagged_lines.append({
                    "barcode": str(barcode),
                    "name": name,
                    "field": field,
                    "text": text,
                    "source": "json",
                    "rules": [r["rule"] + (" (advisory)" if r.get("advisory") else "") for r in fired],
                    "counts": {r["rule"]: r["count"] for r in fired},
                    "detail": fired,
                })

    page_copy = data.get("page_copy")
    if isinstance(page_copy, dict):
        for field, text in extract_page_copy_fields(page_copy):
            fired = scan_text(text)
            if fired:
                flagged_lines.append({
                    "barcode": None,
                    "name": "(page-level copy)",
                    "field": field,
                    "text": text,
                    "source": "json",
                    "rules": [r["rule"] + (" (advisory)" if r.get("advisory") else "") for r in fired],
                    "counts": {r["rule"]: r["count"] for r in fired},
                    "detail": fired,
                })

    meta = data.get("_meta")
    if isinstance(meta, dict):
        for field, text in extract_meta_fields(meta):
            fired = scan_text(text)
            if fired:
                flagged_lines.append({
                    "barcode": None,
                    "name": "(page-level copy)",
                    "field": field,
                    "text": text,
                    "source": "json",
                    "rules": [r["rule"] + (" (advisory)" if r.get("advisory") else "") for r in fired],
                    "counts": {r["rule"]: r["count"] for r in fired},
                    "detail": fired,
                })

    total_product_lines_scanned = sum(len(extract_product_fields(p)) for p in products)

    ts_lines_scanned = 0
    ts_source_file = None
    if ts_filename:
        ts_flagged, ts_lines_scanned = scan_ts_category(category, ts_filename)
        flagged_lines.extend(ts_flagged)
        ts_source_file = ts_filename

    return {
        "active_file": filename,
        "ts_file": ts_source_file,
        "product_count": len(products),
        "lines_scanned": total_product_lines_scanned + ts_lines_scanned,
        "lines_scanned_json": total_product_lines_scanned,
        "lines_scanned_ts": ts_lines_scanned,
        "lines_flagged": len(flagged_lines),
        "lines_flagged_json": sum(1 for l in flagged_lines if l.get("source") == "json"),
        "lines_flagged_ts": sum(1 for l in flagged_lines if l.get("source") == "ts"),
        "lines": flagged_lines,
    }


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

RULE_ORDER = ["sodium_term", "brand_spelling", "em_dash", "antithesis", "number_density"]


# Known substring/token collisions discovered during the first full-corpus run
# (2026-07-04). These are NOT filtered out of the rule output — the rules run
# exactly as specified (sodium_term is literal-substring DETERMINISTIC;
# brand_spelling is the standalone-token regex given in the spec) — but they
# are surfaced here so the owner's manual rewrite pass can discount them
# instead of "fixing" a false positive. Same constants as copy_rules.py's
# gate-safe exclusion classes (TASK-506 D3) — reused here, not redefined.
_SODIUM_CHEM_PREFIXES = copy_rules._SODIUM_CHEM_PREFIXES  # e.g. "דיסודיום דיפוספט"
_BRAND_LOANWORD_PRECEDE = copy_rules._BRAND_LOANWORD_PRECEDE  # e.g. "גוג'י ברי"


def _known_fp_notes(inventory: dict) -> list[str]:
    sodium_chem_hits = 0
    brand_loanword_hits = 0
    for cat_data in inventory.values():
        for line in cat_data["lines"]:
            if "sodium_term" in line["counts"]:
                for prefix in _SODIUM_CHEM_PREFIXES:
                    if f"{prefix}סודיום" in line["text"] or f"{prefix} סודיום" in line["text"]:
                        sodium_chem_hits += 1
                        break
            if "brand_spelling" in line["counts"]:
                for w in _BRAND_LOANWORD_PRECEDE:
                    if w in line["text"] and "ברי" in line["text"]:
                        # crude but sufficient: co-occurrence of the loanword marker
                        idx = line["text"].find(w)
                        if 0 <= line["text"].find("ברי", idx) - (idx + len(w)) <= 3:
                            brand_loanword_hits += 1
                            break
    notes = []
    if sodium_chem_hits:
        notes.append(
            f"- **sodium_term** matched inside a chemical/additive compound name "
            f"(e.g. \"דיסודיום דיפוספט\" / disodium diphosphate) in **{sodium_chem_hits}** line(s). "
            f"These are ingredient/additive names, not editorial sodium-prose — "
            f"do not rewrite them to \"נתרן\"; the substring match is a known collision, not a defect."
        )
    if brand_loanword_hits:
        notes.append(
            f"- **brand_spelling** matched \"ברי\" as part of a transliterated loanword "
            f"(e.g. \"גוג'י ברי\" / goji berry) in **{brand_loanword_hits}** line(s). "
            f"This is not the Bari brand token — skip these in the rewrite pass."
        )
    return notes


def _rule_totals(inventory: dict) -> dict[str, int]:
    totals = {r: 0 for r in RULE_ORDER}
    for cat_data in inventory.values():
        for line in cat_data["lines"]:
            for rule_name, count in line["counts"].items():
                totals[rule_name] = totals.get(rule_name, 0) + count
    return totals


def render_markdown(inventory: dict, scanned_meta: dict) -> str:
    lines: list[str] = []
    lines.append("# Copy Conformance Inventory — TASK-506 D1 (+ Part A coverage extension)\n")
    lines.append(
        "Generated by `03_operations/evals/copy_evals/conformance_scan.py`. "
        "Tooling-only report; feeds the owner's manual rewrite pass under the "
        "product-descriptions freeze. No consumer copy was edited to produce this file.\n"
    )
    lines.append(
        "**Coverage extension (TASK-506 Part A):** this run also scans hardcoded Hebrew "
        "string literals in each category's `*-page-data.ts` loader (hero / prologue / "
        "category-note-fallback / methodology — e.g. `crackersPrologueSentences`, "
        "`CRACKERS_CATEGORY_NOTE_FALLBACK`), not just the `*_frontend_v*.json` corpus. "
        "Every flagged line below is tagged **[json]** or **[ts]** so the two sources stay "
        "visually separable; the JSON-vs-TS split per category is in its own table.\n"
    )

    lines.append("## Totals across all scanned categories\n")
    totals = _rule_totals(inventory)
    lines.append("| Rule | Total occurrences | Categories affected | Advisory? |")
    lines.append("|---|---|---|---|")
    for rule in RULE_ORDER:
        cats_affected = sum(
            1 for cat_data in inventory.values()
            if any(rule in line["counts"] for line in cat_data["lines"])
        )
        advisory = "yes" if rule == "number_density" else "no"
        lines.append(f"| {rule} | {totals.get(rule, 0)} | {cats_affected}/{len(inventory)} | {advisory} |")
    total_flagged_lines = sum(c["lines_flagged"] for c in inventory.values())
    total_scanned_lines = sum(c["lines_scanned"] for c in inventory.values())
    total_scanned_json = sum(c.get("lines_scanned_json", 0) for c in inventory.values())
    total_scanned_ts = sum(c.get("lines_scanned_ts", 0) for c in inventory.values())
    total_flagged_json = sum(c.get("lines_flagged_json", 0) for c in inventory.values())
    total_flagged_ts = sum(c.get("lines_flagged_ts", 0) for c in inventory.values())
    lines.append(
        f"\n**{total_flagged_lines}/{total_scanned_lines} scanned copy lines flagged** "
        f"across {len(inventory)} categories (product-level fields + page_copy/_meta caveat "
        f"fields + `*-page-data.ts` literals, all summed into this denominator).\n"
        f"\n- **[json]** source (`*_frontend_v*.json`): {total_flagged_json}/{total_scanned_json} flagged\n"
        f"- **[ts]** source (`*-page-data.ts` literals, Part A extension): "
        f"{total_flagged_ts}/{total_scanned_ts} flagged\n"
    )

    lines.append("## Per-category counts\n")
    lines.append("| Category | Active file | Active ts file | Products | Lines scanned | Lines flagged | sodium_term | brand_spelling | em_dash | antithesis | number_density(adv) |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for cat, cat_data in sorted(inventory.items()):
        c = {r: 0 for r in RULE_ORDER}
        for line in cat_data["lines"]:
            for rule_name, count in line["counts"].items():
                c[rule_name] = c.get(rule_name, 0) + count
        lines.append(
            f"| {cat} | {cat_data['active_file']} | {cat_data.get('ts_file') or '-'} | "
            f"{cat_data['product_count']} | "
            f"{cat_data['lines_scanned']} | {cat_data['lines_flagged']} | "
            f"{c['sodium_term']} | {c['brand_spelling']} | {c['em_dash']} | "
            f"{c['antithesis']} | {c['number_density']} |"
        )

    lines.append("\n## Per-category JSON vs TS split (Part A)\n")
    lines.append("| Category | [json] scanned | [json] flagged | [ts] scanned | [ts] flagged |")
    lines.append("|---|---|---|---|---|")
    for cat, cat_data in sorted(inventory.items()):
        lines.append(
            f"| {cat} | {cat_data.get('lines_scanned_json', 0)} | "
            f"{cat_data.get('lines_flagged_json', 0)} | "
            f"{cat_data.get('lines_scanned_ts', 0)} | "
            f"{cat_data.get('lines_flagged_ts', 0)} |"
        )

    if scanned_meta.get("orphans"):
        lines.append("\n## Orphaned JSON files (present, not imported by any route)\n")
        for o in scanned_meta["orphans"]:
            lines.append(f"- `{o}`")

    fp_notes = _known_fp_notes(inventory)
    if fp_notes:
        lines.append("\n## Known false-positive classes (found this run — read before rewriting)\n")
        lines.append(
            "The rules below ran exactly per the TASK-506 spec (literal substring / "
            "standalone-token regex). These specific collisions are not rule bugs — "
            "they are the expected cost of a deterministic regex on free text. "
            "Flagged here so they are not mistaken for real violations:\n"
        )
        lines.extend(fp_notes)

    lines.append("\n## Flagged lines, grouped by rule\n")
    for rule in RULE_ORDER:
        rule_lines = []
        for cat, cat_data in sorted(inventory.items()):
            for line in cat_data["lines"]:
                if rule in line["counts"]:
                    rule_lines.append((cat, line))
        if not rule_lines:
            continue
        advisory_tag = " (ADVISORY — not a hard violation)" if rule == "number_density" else ""
        lines.append(f"### {rule}{advisory_tag} — {len(rule_lines)} lines\n")
        for cat, line in rule_lines:
            barcode = line["barcode"] or "-"
            src_tag = f"[{line.get('source', 'json')}]"
            lines.append(
                f"- **[{cat}]** {src_tag} `{barcode}` — {line['name']} — "
                f"field `{line['field']}` (count={line['counts'][rule]})"
            )
            lines.append(f"  > {line['text']}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Bari copy-conformance scanner (TASK-506 D1)")
    parser.add_argument("--category", default=None, help="Scan a single category only (for iteration)")
    parser.add_argument("--json-only", action="store_true", help="Skip writing the .md report")
    parser.add_argument("--out-dir", default=str(REPORT_DIR), help="Output directory for reports")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    categories = ACTIVE_FILES if not args.category else {args.category: ACTIVE_FILES[args.category]}

    full_inventory: dict[str, dict] = {}
    for cat, filename in categories.items():
        ts_filename = ACTIVE_TS_FILES.get(cat)
        result = scan_category(cat, filename, ts_filename=ts_filename)
        full_inventory[cat] = result
        print(
            f"[{cat}] {filename} + {ts_filename}: "
            f"{result['lines_flagged']}/{result['lines_scanned']} lines flagged "
            f"(json {result['lines_flagged_json']}/{result['lines_scanned_json']}, "
            f"ts {result['lines_flagged_ts']}/{result['lines_scanned_ts']})"
        )

    # inventory.json — only categories/lines with >=1 flag are meaningful;
    # we still emit the category envelope (active_file, counts) for every
    # scanned category so denominators are visible even when zero lines fire.
    inventory_json = {
        cat: {
            "active_file": data["active_file"],
            "ts_file": data["ts_file"],
            "product_count": data["product_count"],
            "lines_scanned": data["lines_scanned"],
            "lines_scanned_json": data["lines_scanned_json"],
            "lines_scanned_ts": data["lines_scanned_ts"],
            "lines_flagged": data["lines_flagged"],
            "lines_flagged_json": data["lines_flagged_json"],
            "lines_flagged_ts": data["lines_flagged_ts"],
            "lines": data["lines"],
        }
        for cat, data in full_inventory.items()
    }

    inventory_path = out_dir / "inventory.json"
    with open(inventory_path, "w", encoding="utf-8") as f:
        json.dump(inventory_json, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {inventory_path}")

    if not args.json_only:
        md = render_markdown(full_inventory, {"orphans": ORPHAN_FILES})
        report_path = out_dir / "inventory_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Wrote {report_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
