# -*- coding: utf-8 -*-
"""
BSIP0 EXIT GATE — shared (TASK-239 base + P-04 G10/G11/G12).

The structural barrier between BSIP0 scrape output and BSIP1/BSIP2 enrichment.
A FAIL here blocks the corpus from entering BSIP1. Parameterized over any BSIP0
output file (retailer- and category-agnostic).

Usage:
    python _shared/bsip0_gate.py <bsip0_output.json> [--category CAT]

Exit code: 0 = PASS/WARN, 1 = FAIL (gate blocks BSIP1).

Checks (all HARD-FAIL unless marked WARN):
  G1  OFF contamination          — Open Food Facts in ANY field/variant  (HARD FAIL)
  G2  nutrition basis            — selected_basis must be per_100g; insufficient = FAIL
  G3  multi-table detection      — competing_table_count>1 with non-per_100g selection = FAIL
  G4  duplicate barcode          — same barcode twice in the corpus  (HARD FAIL)
  G5  conflicting identity       — same barcode, different name_he   (HARD FAIL)
  G6  numeric sanity             — nutrition_implausible() signatures (sat>fat, sodium>2000,
                                   fat-understated, energy>900 kcal)  (HARD FAIL)
  G7  ingredient coverage        — share of products with real ingredients  (WARN below thresh)
  G8  ingredients_raw_source     — presence OR a recorded reason for absence (WARN)
  G9  run-summary contract       — required run-level fields present (HARD FAIL)
  G10 image reachability         — HTTP-200 check on each image URL with retry; alt-network note
                                   for cross-origin images  (WARN per product, HARD FAIL if >50% unreachable)
  G11 EAN-13 checksum            — validates barcode check digit  (WARN per invalid barcode)
  G12 scope-boundary scan        — product names checked against basic non-food/out-of-scope tokens;
                                   category-agnostic (uses hard-coded negative token list)  (HARD FAIL)
  G13 cross-category acquisition — TASK-498. Two complementary signals, both checked against the
                                   run's declared --category (or the doc's own "category" field):
                                     (1) acquisition_query ownership — the BSIP0 search term that
                                         pulled a record in is checked against CATEGORY_QUERY_OWNERSHIP;
                                         a term owned by a DIFFERENT category is flagged.
                                     (2) product-form head noun — the record's own name is checked
                                         against PRODUCT_FORM_HEAD_NOUNS; a name carrying another
                                         category's defining physical-form noun (e.g. "חטיף"/bar-form
                                         inside a dessert run) is flagged even when the query term is
                                         the run's own.
                                   WARN by default; pass --strict-cross-category to make it HARD FAIL.
                                   Root cause: free-text retailer search does loose token matching, so
                                   a query like "מעדן פרוטאין" (protein DESSERT, maadanim's OWN term)
                                   can also return actual protein BARS (snack_bars' product form) — see
                                   run_maadanim_001 (TASK-477/TASK-409): 5/33 protein-bars-corpus
                                   barcodes duplicated into that dessert run this way. Signal (1) alone
                                   does not catch this instance (the query WAS maadanim's own); signal
                                   (2) is what actually flags 3 of the 5 real barcodes by name. The
                                   remaining 2 (brand "נייטשר פרוטאין", no disclosing name token or
                                   foreign query term) are a known, reported residual gap — see the
                                   PRODUCT_FORM_HEAD_NOUNS docstring for what would close it.
"""
from __future__ import annotations

import argparse
import io
import json
import logging
import re
import sys
import pathlib
import socket
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

if hasattr(sys.stdout, "buffer") and (getattr(sys.stdout, "encoding", "") or "").lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bsip0_nutrition as bn  # noqa: E402

log = logging.getLogger(__name__)

# ── OFF contamination tokens (TASK-238/239) ────────────────────────────────────
OFF_TOKENS: tuple[str, ...] = (
    "open food facts", "openfoodfacts", "open_food_facts",
    ".openfoodfacts.org", "off_url", "off_image", "off_nutrition",
    "off_ingredients", "source=openfoodfacts",
)
_OFF_BARE_RE = re.compile(r"^\s*off\s*$", re.IGNORECASE)

INGREDIENT_COVERAGE_WARN = 0.50

# Out-of-scope tokens for G12 (basic non-food / wrong-category signal).
# These supplement any category-specific gates the caller provides.
OUT_OF_SCOPE_TOKENS: tuple[str, ...] = (
    "שמפו", "ניקוי", "חיתול", "סוכריות", "גלידה",
    "שוקולד", "חטיף", "ביסלי", "מסטיק", "סיגריה",
    "דטרגנט", "מרכך", "אקונומיקה", "שקית", "כלי",
)


# ── String enumeration helper ──────────────────────────────────────────────────

def _iter_strings(obj: Any, path: str = ""):
    """Yield (json_path, lowercased_string) for every string key and value."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str):
                yield f"{path}.{k}", k.lower()
            yield from _iter_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _iter_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj.lower()


def _worst_status(*statuses: str) -> str:
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    return min(statuses, key=lambda s: order.get(s, 2))


def _check_result(check: str, status: str, messages: list[str]) -> dict:
    return {"check": check, "status": status, "messages": messages}


# ── G1: OFF contamination ──────────────────────────────────────────────────────

def gate_off_contamination(records: list[dict], full_doc: Any) -> dict:
    hits: list[str] = []
    for jpath, s in _iter_strings(full_doc):
        for tok in OFF_TOKENS:
            if tok in s:
                hits.append(f"{jpath}: token '{tok}' in {s[:80]!r}")
        jl = jpath.lower()
        if (any(jl.endswith(suf) for suf in ("source", "panel_source", "identity_source"))
                or "cache" in jl or "trace" in jl or "provenance" in jl) and _OFF_BARE_RE.match(s):
            hits.append(f"{jpath}: standalone 'OFF' value in provenance/source/cache/trace field")
    status = "FAIL" if hits else "PASS"
    msg = ([f"OFF_CONTAMINATION: {len(hits)} hit(s): {hits[:10]}"]
           if hits else ["No Open Food Facts contamination found."])
    return _check_result("G1_off_contamination", status, msg)


# ── G2/G3: nutrition basis + multi-table ───────────────────────────────────────

def gate_nutrition_basis(records: list[dict]) -> dict:
    fails: list[str] = []
    no_basis: list[str] = []
    multitable_unsafe: list[str] = []
    scored = 0
    for p in records:
        nr = p.get("nutrition_raw") or p.get("nutrition") or {}
        if isinstance(nr, dict) and not nr:
            continue
        scored += 1
        basis = p.get("nutrition_basis")
        code = str(p.get("barcode") or p.get("product_code") or "?")
        if not isinstance(basis, dict):
            no_basis.append(code)
            continue
        if basis.get("insufficient"):
            fails.append(f"{code}: basis insufficient (competing={basis.get('competing_table_count')}, "
                         f"header={basis.get('selected_table_header')!r})")
            continue
        sel = basis.get("selected_basis")
        comp = basis.get("competing_table_count", 1)
        if sel != "per_100g":
            if comp and comp > 1:
                multitable_unsafe.append(f"{code}: {comp} tables, selected_basis={sel!r} (not per_100g)")
            else:
                no_basis.append(f"{code}: single table, basis={sel!r}")
    fail_all = fails + multitable_unsafe
    status = "FAIL" if fail_all else ("WARN" if no_basis else "PASS")
    msgs = []
    if fail_all:
        msgs.append(f"BASIS_FAIL: {len(fail_all)} product(s) lack a per-100g basis: {fail_all[:10]}")
    if no_basis:
        msgs.append(f"BASIS_WARN: {len(no_basis)} product(s) have unknown/missing basis metadata: {no_basis[:8]}")
    if not msgs:
        msgs.append(f"All {scored} paneled products selected a per-100g basis.")
    return _check_result("G2_G3_nutrition_basis", status, msgs)


# ── G4/G5: duplicate barcode + conflicting identity ────────────────────────────

def gate_identity(records: list[dict]) -> dict:
    by_barcode: dict[str, list] = defaultdict(list)
    for p in records:
        bc = str(p.get("barcode") or p.get("barcode_ld") or p.get("barcode_data_attr") or "").strip()
        if bc:
            by_barcode[bc].append(p)
    dup, conflict = [], []
    for bc, group in by_barcode.items():
        if len(group) > 1:
            names = {str(g.get("name_he") or g.get("name") or "") for g in group}
            dup.append(f"{bc} x{len(group)}")
            if len(names) > 1:
                conflict.append(f"{bc}: {sorted(names)[:3]}")
    status = "FAIL" if (dup or conflict) else "PASS"
    msgs = []
    if dup:
        msgs.append(f"DUPLICATE_BARCODE: {len(dup)}: {dup[:10]}")
    if conflict:
        msgs.append(f"CONFLICTING_IDENTITY: {len(conflict)} barcode(s) map to >1 name: {conflict[:10]}")
    if not msgs:
        msgs.append(f"No duplicate/conflicting barcodes across {len(by_barcode)} keyed products.")
    return _check_result("G4_G5_identity", status, msgs)


# ── G6: numeric sanity ─────────────────────────────────────────────────────────

def _nutrition_for_guard(p: dict) -> dict:
    nutr = p.get("nutrition_raw") or p.get("nutrition") or {}
    out: dict = {}
    keymap = {"energy": "energy_kcal_raw", "fat": "fat_raw", "saturated_fat": "saturated_fat_raw",
              "carbs": "carbs_raw", "sugar": "sugar_raw", "protein": "protein_raw",
              "sodium": "sodium_raw", "fiber": "fiber_raw"}
    for label, value in nutr.items():
        field = bn.classify_nutr_label(label)
        if field in keymap and keymap[field] not in out:
            out[keymap[field]] = value
    return out


def gate_numeric_sanity(records: list[dict]) -> dict:
    flagged = []
    for p in records:
        nr = p.get("nutrition_raw") or p.get("nutrition") or {}
        if not nr:
            continue
        reason = bn.nutrition_implausible(_nutrition_for_guard(p))
        if reason:
            code = str(p.get("barcode") or p.get("product_code") or "?")
            flagged.append(f"{code}: {reason}")
    status = "FAIL" if flagged else "PASS"
    msgs = ([f"NUMERIC_SANITY: {len(flagged)} implausible panel(s): {flagged[:8]}"]
            if flagged else ["All panels passed numeric sanity."])
    return _check_result("G6_numeric_sanity", status, msgs)


# ── G7/G8: ingredient coverage + raw-source preservation ───────────────────────

def gate_ingredients(records: list[dict]) -> dict:
    total = len(records)
    with_ing = sum(1 for p in records if str(p.get("ingredients_raw") or "").strip())
    cov = with_ing / total if total else 0.0
    no_src = [str(p.get("barcode") or "?") for p in records
              if not p.get("ingredients_raw_source")
              and not p.get("ingredients_raw_source_reason")]
    status = "WARN" if (cov < INGREDIENT_COVERAGE_WARN or no_src) else "PASS"
    msgs = [f"Ingredient coverage: {with_ing}/{total} ({cov:.0%})."]
    if cov < INGREDIENT_COVERAGE_WARN:
        msgs.append(f"COVERAGE_WARN: ingredient coverage {cov:.0%} < {INGREDIENT_COVERAGE_WARN:.0%}.")
    if no_src:
        msgs.append(f"RAW_SOURCE_WARN: {len(no_src)} product(s) carry neither an "
                    f"ingredients_raw_source nor an absence reason.")
    return _check_result("G7_G8_ingredients", status, msgs)


# ── G9: run-summary contract ───────────────────────────────────────────────────

def gate_run_summary(full_doc: dict) -> dict:
    required = ["run_id", "category", "retailer", "panel_source", "provenance", "products"]
    missing = [f for f in required if f not in full_doc]
    prov = full_doc.get("provenance") or {}
    if isinstance(prov, dict) and "source" not in prov:
        missing.append("provenance.source")
    status = "FAIL" if missing else "PASS"
    msgs = ([f"RUN_SUMMARY: missing required field(s): {missing}"]
            if missing else ["Run-summary contract satisfied."])
    return _check_result("G9_run_summary", status, msgs)


# ── G10: image reachability ────────────────────────────────────────────────────

def _probe_url(url: str, timeout: int = 8, max_retries: int = 2) -> tuple[int | None, str | None]:
    """Return (status_code, error_msg). Retries on transient failures."""
    last_err: str | None = None
    for attempt in range(1 + max_retries):
        try:
            req = Request(url, method="GET", headers={
                "User-Agent": "Bari-Gate-ImageProbe/1.0",
                "Accept": "image/*,*/*;q=0.8",
            })
            with urlopen(req, timeout=timeout) as resp:
                return resp.status, None
        except HTTPError as e:
            return e.code, None
        except (URLError, socket.timeout, OSError) as e:
            last_err = str(e)[:120]
            if attempt < max_retries:
                time.sleep(1)
        except Exception as e:
            last_err = str(e)[:120]
            break
    return None, last_err


def gate_image_reachability(records: list[dict]) -> dict:
    unreachable: list[str] = []
    alt_network_notes: list[str] = []
    checked = 0
    for p in records:
        urls: list[str] = []
        raw = p.get("imageUrl")
        if isinstance(raw, str) and raw.strip():
            urls.append(raw.strip())
        raw_list = p.get("image_urls")
        if isinstance(raw_list, list):
            urls.extend(u for u in raw_list if isinstance(u, str) and u.strip())
        if not urls:
            continue
        checked += 1
        for url in urls:
            if not url.startswith("http"):
                continue
            status_code, err = _probe_url(url)
            if status_code is None:
                unreachable.append(f"{p.get('barcode') or '?'}: {url[:80]} — {err}")
            elif status_code != 200:
                unreachable.append(f"{p.get('barcode') or '?'}: {url[:80]} — HTTP {status_code}")
            # alt-network note for cross-origin image hosts
            if "cloudinary.com" in url or "shufersal.co.il" in url or "cloudfront.net" in url:
                alt_network_notes.append(f"{p.get('barcode') or '?'}: {url[:60]} — CDN-hosted, "
                                         "may be unreachable from CI runners without Israeli resolvers")

    null_count = sum(1 for p in records if not p.get("imageUrl") and not p.get("image_urls"))
    total = len(records)
    null_rate = null_count / total if total else 0.0
    unreachable_rate = len(unreachable) / checked if checked else 0.0

    msgs: list[str] = []
    status = "PASS"

    if null_rate > 0.5:
        msgs.append(f"IMAGE_NULL_RATE: {null_count}/{total} ({null_rate:.0%}) products have no image URL.")
        status = "WARN"

    if unreachable:
        # HARD FAIL if >50% of checked images are unreachable
        if unreachable_rate > 0.5:
            status = "FAIL"
            msgs.append(f"IMAGE_UNREACHABLE_FAIL: {len(unreachable)}/{checked} ({unreachable_rate:.0%}) "
                        f"images unreachable: {unreachable[:6]}")
        else:
            status = _worst_status(status, "WARN")
            msgs.append(f"IMAGE_UNREACHABLE_WARN: {len(unreachable)}/{checked} images unreachable: {unreachable[:6]}")

    if alt_network_notes:
        msgs.append(f"ALT_NETWORK: {len(alt_network_notes)} image(s) from CDN hosts "
                    f"(may need Israeli DNS): {alt_network_notes[:4]}")

    if not msgs:
        msgs.append(f"All {checked} product images reachable (HTTP 200).")
    return _check_result("G10_image_reachability", status, msgs)


# ── G11: EAN-13 checksum validation ────────────────────────────────────────────

def _ean13_checksum_valid(barcode: str) -> bool:
    """Validate EAN-13 check digit (last digit). Returns True for non-13-digit strings.

    EAN-13 weighting: positions 1,3,5,7,9,11 (0-indexed even) get weight 1;
    positions 2,4,6,8,10,12 (0-indexed odd) get weight 3.
    """
    digits = [c for c in barcode if c.isdigit()]
    if len(digits) != 13:
        return True  # non-EAN-13 barcodes are not flagged by this check
    nums = [int(d) for d in digits]
    total = sum(nums[i] * (1 if i % 2 == 0 else 3) for i in range(12))
    expected = (10 - (total % 10)) % 10
    return expected == nums[12]


def gate_barcode_checksum(records: list[dict]) -> dict:
    invalid: list[str] = []
    for p in records:
        bc = str(p.get("barcode") or "").strip()
        if not bc:
            continue
        if not _ean13_checksum_valid(bc):
            invalid.append(f"{bc} (product: {p.get('name_he') or p.get('name') or '?'})")
    status = "WARN" if invalid else "PASS"
    msgs = ([f"BARCODE_CHECKSUM: {len(invalid)} barcode(s) failed EAN-13 check digit: {invalid[:10]}"]
            if invalid else ["All barcodes pass EAN-13 checksum validation."])
    return _check_result("G11_barcode_checksum", status, msgs)


# ── G12: scope-boundary scan ───────────────────────────────────────────────────

def gate_scope_boundary(records: list[dict], extra_negative: list[str] | None = None) -> dict:
    negative_tokens = list(OUT_OF_SCOPE_TOKENS)
    if extra_negative:
        negative_tokens.extend(extra_negative)

    rejected: list[str] = []
    for p in records:
        name = str(p.get("name_he") or p.get("name") or "").lower()
        for tok in negative_tokens:
            if tok.lower() in name:
                rejected.append(f"{p.get('barcode') or '?'}: {tok!r} in name "
                                f"{(p.get('name_he') or p.get('name') or '')[:60]!r}")
                break

    status = "FAIL" if rejected else "PASS"
    msgs = ([f"SCOPE_BOUNDARY: {len(rejected)} product(s) matched out-of-scope tokens: {rejected[:10]}"]
            if rejected else ["No out-of-scope products detected by token scan."])
    return _check_result("G12_scope_boundary", status, msgs)


# ── G13: cross-category acquisition-query collision ────────────────────────────
#
# TASK-498 root cause: a BSIP0 scraper's QUERY_PLAN is written to maximize recall
# for ITS OWN category, using loose Hebrew free-text search terms against the
# retailer's search endpoint. That endpoint does substring/token matching, not
# category-scoped matching — so a query intended for one category's product type
# can return a physically different product type that happens to share a word
# (most commonly "פרוטאין"/"protein", "בריאות"/health, or a brand name spanning
# multiple physical formats). The record then gets written into the WRONG
# category's BSIP1 output as if it belonged there, with nothing downstream
# checking that a query term actually "belongs" to the run's own category.
#
# Confirmed instance: run_maadanim_001 (dairy desserts) used the query
# "מעדן פרוטאין" ("protein dessert") and picked up 5 barcodes that are true
# protein BARS (owned by snack_bars' own "חטיף פרוטאין"/"חטיף חלבון" query
# terms) — 7290019401018, 7290019401049, 7290019401544, 8410076610379,
# 8410076610386. It did not taint any live score (maadanim never shipped from
# that BSIP1 dir), but it is exactly the shape of a FUTURE contamination if a
# tool ever barcode-globs across `03_operations/bsip1/run_*/output/` without
# corpus-scoping.
#
# This registry is deliberately small and additive: it only lists terms that are
# CONFIRMED to be one category's own defining product-type vocabulary (the
# "mainstream" head-noun queries a scraper is built around), not every query a
# scraper happens to try. Extend it whenever a new scraper's QUERY_PLAN is
# authored — treat it the same as adding a new EXCLUDE_SIGNALS entry.
CATEGORY_QUERY_OWNERSHIP: dict[str, tuple[str, ...]] = {
    "snack_bars": (
        "חטיף דגנים", "חטיף שיבולת שועל", "חטיף גרנולה", "חטיף תמרים",
        "מאגדת דגנים", "חטיף חלבון", "חטיף פרוטאין", "protein bar", "פרו בר",
        "חטיף חלבון פרו", "מקס ברנר חלבון",
    ),
    "maadanim": (
        "מעדן", "מעדנים", "פודינג", "מוס", "קינוח", "מילקי", "עדנה", "יופלה",
        "מילקי בר", "מעדן חלבון", "פרוביו", "מעדן פרוטאין", "מעדן ילדים",
        "קינוח ילדים", "מעדן ללא סוכר", "מעדן דיאט", "מעדן קל",
    ),
    "cereals": (
        "דגני בוקר", "קורנפלקס", "גרנולה",
    ),
    "cookies_coffee": (
        "עוגיות", "ביסקוויט",
    ),
    "yogurt": (
        "יוגורט", "יוגורט יווני", "יוגורט ביו",
    ),
    "hummus": (
        "חומוס", "ממרח חומוס", "חומוס שום",
    ),
    "cheese": (
        "גבינת קוטג'", "גבינה לבנה", "לבנה",
    ),
    "butter": (
        "חמאה", "חמאה מחלב", "חמאת שמנת",
    ),
    "brined_cheeses": (),  # populated on demand; empty = no owned-term check yet
    "olive_oil": (
        "שמן זית", "שמן זית כתית מעולה", "extra virgin olive oil",
    ),
    "cakes_hard_cookies": (
        "עוגה", "עוגת שוקולד", "עוגת שמרים",
    ),
    "chocolate": (
        "שוקולד פרה", "טבלת שוקולד", "שוקולד מריר",
    ),
}

# Product-FORM head-noun registry — the second, complementary signal G13 checks.
#
# Re-running the query-term-ownership check alone against the real
# run_maadanim_001 data (all 5 confirmed cross-category records) showed it is
# INSUFFICIENT on its own: all 5 records carry acquisition_query="מעדן פרוטאין",
# which IS maadanim's own registered term (QUERY_PLAN tier "specialty") — the
# scraper wasn't using someone else's query, its OWN legitimately-scoped term
# just happened to also match a different physical product form because the
# retailer's free-text search is loose. Query-term ownership cannot catch that
# case by construction.
#
# The complementary signal: a product's NAME contains a head noun that is a
# different category's defining physical product FORM (not a flavor/claim
# word). "חטיף" (snack/bar) names a physical form incompatible with "מעדן"
# (spoonable dessert) regardless of protein positioning. This is a one-way,
# low-false-positive check — verified against all 200 real run_maadanim_001
# records: exactly the true bar-form products carry "חטיף" in the name (0 of
# the other 196 legitimate dessert records do).
#
# Known residual gap (reported honestly, not hidden): 2 of the 5 real
# collision barcodes (8410076610379, 8410076610386, brand "נייטשר פרוטאין")
# carry NEITHER a foreign query term NOR a foreign head-noun in the name — the
# brand name alone does not disclose physical form. Closing that last gap
# needs either (a) a barcode-registry cross-check against sibling categories'
# already-built corpora (deferred — no uniform corpus file layout to key off
# today, see task investigation notes) or (b) a maintained brand→category
# lookup. Out of scope for this pass; flagged here for a future ticket rather
# than papered over.
# DELIBERATELY CONSERVATIVE: only "חטיף" is registered. A precision check against
# ALL 200 real run_maadanim_001 records (not just the 5 known collisions) showed
# candidate nouns like "קורנפלקס"/"דגני בוקר" (cereals) and "עוגיות" (cookies)
# produce FALSE POSITIVES here — e.g. "מילקי טופ קורנפלקס" and "יופלה טופ תות
# קורנפלקס" are genuine dairy desserts with a cornflake TOPPING ingredient, not
# cereal-category products; a naive substring-in-name match can't tell "head
# noun" from "ingredient mention." "חטיף" was verified clean over the same 200
# records (4 hits, all 4 genuine bar-form products, 0 false positives) before
# being added. Do NOT add a new noun here without the same full-run precision
# check — false positives here would spuriously WARN legitimate future runs.
#
# (Separately, that same precision run surfaced 5 "עוגיות ... ללת\"ס" wafer-
# cookie barcodes in run_maadanim_001 that plausibly ARE a second real
# cookies_coffee/maadanim collision — but this was NOT part of the confirmed
# TASK-477 finding this task was scoped to fix, and "עוגיות" is not clean
# enough to register without further precision work. Flagged here for a
# follow-up ticket, not silently added.)
PRODUCT_FORM_HEAD_NOUNS: dict[str, tuple[str, ...]] = {
    "snack_bars": ("חטיף",),
}


def _terms_owned_by_other_categories(this_category: str) -> dict[str, str]:
    """Map lowercased query-term -> owning category, for every category that is
    NOT this_category. Used to flag a record acquired via a term this run's own
    category does not recognize as its own."""
    owned_elsewhere: dict[str, str] = {}
    for cat, terms in CATEGORY_QUERY_OWNERSHIP.items():
        if cat == this_category:
            continue
        for t in terms:
            owned_elsewhere.setdefault(t.strip().lower(), cat)
    return owned_elsewhere


def gate_cross_category_acquisition(records: list[dict], category: str | None,
                                     strict: bool = False) -> dict:
    """G13 — flag records acquired via a query term owned by a DIFFERENT category.

    category: the run's own declared category (e.g. "maadanim"). If None or not
    present in CATEGORY_QUERY_OWNERSHIP, this check is a no-op PASS (we only
    check categories we have a registered vocabulary for — absence of a registry
    entry is not itself evidence of contamination).
    """
    if not category or category not in CATEGORY_QUERY_OWNERSHIP:
        return _check_result(
            "G13_cross_category_acquisition", "PASS",
            [f"No registered query-ownership vocabulary for category={category!r}; "
             f"skipped (not evidence of contamination, just no registry entry)."],
        )

    owned_elsewhere = _terms_owned_by_other_categories(category)
    own_terms = {t.strip().lower() for t in CATEGORY_QUERY_OWNERSHIP.get(category, ())}
    own_head_nouns = {n.strip() for n in PRODUCT_FORM_HEAD_NOUNS.get(category, ())}

    flagged: list[str] = []
    for p in records:
        code = str(p.get("barcode") or p.get("product_code") or "?")
        name = str(p.get("name_he") or p.get("canonical_name_he") or p.get("name") or "")
        q = str(p.get("acquisition_query") or "").strip().lower()

        # Signal 1: acquired via a query term explicitly owned by another category.
        if q and q not in own_terms:
            other_cat = owned_elsewhere.get(q)
            if other_cat:
                flagged.append(f"{code} ({name[:60]!r}): acquired via {q!r}, which is "
                                f"{other_cat}'s own query term, not {category}'s")
                continue

        # Signal 2: the record's own name carries a DIFFERENT category's product-
        # FORM head noun (e.g. "חטיף"/bar-form inside a maadanim/dessert run) —
        # catches same-query collisions signal 1 cannot (see PRODUCT_FORM_HEAD_NOUNS
        # docstring: this is what actually flags 3 of the 5 real run_maadanim_001
        # barcodes, since all 5 share maadanim's own acquisition_query).
        for other_cat, head_nouns in PRODUCT_FORM_HEAD_NOUNS.items():
            if other_cat == category:
                continue
            for noun in head_nouns:
                if noun in own_head_nouns:
                    continue
                if noun and noun in name:
                    flagged.append(f"{code} ({name[:60]!r}): name contains {noun!r}, "
                                    f"{other_cat}'s product-form head noun, not a "
                                    f"{category} product form")
                    break
            else:
                continue
            break

    status = ("FAIL" if strict else "WARN") if flagged else "PASS"
    msgs = ([f"CROSS_CATEGORY_ACQUISITION: {len(flagged)} record(s) suspected cross-category "
             f"(query-term or product-form-noun mismatch): {flagged[:10]}"]
            if flagged else
            [f"No cross-category query-term or product-form collisions detected for "
             f"category={category!r}."])
    return _check_result("G13_cross_category_acquisition", status, msgs)


# ── Runner ─────────────────────────────────────────────────────────────────────

def run_gate(doc: Any, extra_negative_tokens: list[str] | None = None,
             category: str | None = None, strict_cross_category: bool = False) -> dict:
    records = doc.get("products") if isinstance(doc, dict) else doc
    if not isinstance(records, list):
        records = []
    full_doc = doc if isinstance(doc, dict) else {"products": records}

    # category: explicit arg wins; otherwise fall back to the doc's own declared
    # category field (gate_run_summary already requires "category" to be present).
    effective_category = category or (full_doc.get("category") if isinstance(full_doc, dict) else None)

    checks = [
        gate_off_contamination(records, full_doc),
        gate_nutrition_basis(records),
        gate_identity(records),
        gate_numeric_sanity(records),
        gate_ingredients(records),
        gate_run_summary(full_doc),
        gate_image_reachability(records),
        gate_barcode_checksum(records),
        gate_scope_boundary(records, extra_negative_tokens),
        gate_cross_category_acquisition(records, effective_category, strict=strict_cross_category),
    ]
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    overall = min((c["status"] for c in checks), key=lambda s: order[s])
    return {
        "gate": "bsip0_exit_gate_v2",
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "product_count": len(records),
        "overall_status": overall,
        "summary": {
            "FAIL": sum(1 for c in checks if c["status"] == "FAIL"),
            "WARN": sum(1 for c in checks if c["status"] == "WARN"),
            "PASS": sum(1 for c in checks if c["status"] == "PASS"),
        },
        "checks": checks,
    }


# ── CLI ────────────────────────────────────────────────────────────────────────

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="BSIP0 Exit Gate (shared v2)")
    parser.add_argument("input", nargs="?", default=None,
                        help="Path to BSIP0 raw JSON file (required)")
    parser.add_argument("--category", help="Category name for scope scan + G13 query-ownership check")
    parser.add_argument("--extra-negative", nargs="*", default=[],
                        help="Extra out-of-scope tokens for G12")
    parser.add_argument("--strict-cross-category", action="store_true",
                        help="Make G13 a HARD FAIL instead of WARN (TASK-498)")
    args = parser.parse_args(argv[1:])

    path = args.input
    if not path:
        print("Usage: python bsip0_gate.py <bsip0_output.json> [--category CAT] [--strict-cross-category]")
        return 1

    input_path = pathlib.Path(path)
    if not input_path.exists():
        print(f"INPUT NOT FOUND: {input_path}")
        return 1

    doc = json.loads(input_path.read_text(encoding="utf-8"))
    result = run_gate(doc, extra_negative_tokens=args.extra_negative,
                       category=args.category, strict_cross_category=args.strict_cross_category)

    print("=" * 64)
    print(f"BSIP0 EXIT GATE — {input_path.name}")
    if args.category:
        print(f"Category: {args.category}")
    print("=" * 64)
    for c in result["checks"]:
        print(f"[{c['status']:4}] {c['check']}")
        for m in c["messages"]:
            print(f"        - {m}")
    print("-" * 64)
    print(f"OVERALL: {result['overall_status']}  "
          f"(FAIL={result['summary']['FAIL']} WARN={result['summary']['WARN']} "
          f"PASS={result['summary']['PASS']}) over {result['product_count']} products")
    print("=" * 64)
    return 0 if result["overall_status"] != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
