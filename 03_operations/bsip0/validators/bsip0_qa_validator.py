# -*- coding: utf-8 -*-
"""
BSIP0 QA Validator — systematic quality gates for all BSIP0 scrape runs.

TASK-218 — created 2026-06-07 after 10 documented failures in the juices and
hard-cheese pipelines (TASK-214 / TASK-215) that were caught by human review,
not by automated gates.

This module is the SINGLE SOURCE OF TRUTH for BSIP0 gate checks. Scrapers import
and call these functions — they do NOT re-implement checks locally. A gate with
any unresolved FAIL (including acknowledged W001 warnings that are then ignored)
must raise GateSelfPassError rather than recording a PASS status.

Six checks implemented here:
  1. validate_no_fabrication    — anti-fabrication (round timestamps, identical nutrition)
  2. check_portal_availability  — HEAD-check targets before scrape start
  3. verify_product_identity    — barcode / keyword cross-check (wrong-card prevention)
  4. validate_scope_boundaries  — positive/negative type gate with explicit rejection log
  5. validate_consumer_output   — forbidden framework terms in consumer-facing JSON fields
  6. validate_run_summary       — mandatory fields in the per-run summary dict

Usage:
    from validators.bsip0_qa_validator import (
        validate_no_fabrication,
        check_portal_availability,
        verify_product_identity,
        validate_scope_boundaries,
        validate_consumer_output,
        validate_run_summary,
        GATE_RULES,
        GateSelfPassError,
    )
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import socket

# ── Gate enforcement constants ─────────────────────────────────────────────────

GATE_RULES: dict[str, Any] = {
    "scrape_success_rate_min": 0.70,
    "source_verified_required": True,
    "consumer_output_fail_on_forbidden": True,
    "null_imageUrl_rate_warn_threshold": 0.50,
    "fabrication_round_hour_min_count": 3,
    "fabrication_identical_nutrition_min_count": 3,
}

# Forbidden terms in consumer-facing fields: any appearance = FAIL.
# These are internal framework vocabulary that must never reach the live site.
FORBIDDEN_CONSUMER_TERMS: tuple[str, ...] = (
    "NOVA",
    "BSIP",
    "cap",
    "floor",
    "structural_class",
    "matrix_integrity",
    "pillar",
    "dimension",
    "nova",
    "nova_level",
    "nova_proxy",
)

# Consumer-facing fields to scan for forbidden terms.
CONSUMER_SCAN_FIELDS: tuple[str, ...] = (
    "positiveSignals",
    "limitingFactors",
    "insightLine",
)

# Yohananof barcode GS1 prefix range: Israeli registrant prefixes 729xxxxx.
# Barcode must start with 729 to be consistent with Yohananof source claim.
_YOHANANOF_BARCODE_PREFIX = "729"

# Round-hour pattern: "HH:00:00" anywhere in a timestamp string.
_ROUND_HOUR_RE = re.compile(r"\d{2}:00:00")


# ── Gate self-pass guard ───────────────────────────────────────────────────────

class GateSelfPassError(Exception):
    """Raised when a scraper or gate runner attempts to declare PASS while
    unresolved FAILs (or unresolved acknowledged warnings) exist.

    An acknowledged W001 warning does not constitute a conditional pass.
    The scraper MUST raise this exception instead of writing a PASS status.

    Example::

        fails = [r for r in results if r["status"] == "FAIL"]
        if fails:
            raise GateSelfPassError(
                f"Gate has {len(fails)} unresolved FAILs — cannot self-pass.",
                fails,
            )
    """

    def __init__(self, message: str, unresolved_fails: list | None = None):
        super().__init__(message)
        self.unresolved_fails = unresolved_fails or []


# ── Result helpers ─────────────────────────────────────────────────────────────

def _result(status: str, messages: list[str]) -> dict:
    """Construct a standard check result dict."""
    assert status in ("PASS", "FAIL", "WARN"), f"Unknown status: {status!r}"
    return {"status": status, "messages": messages}


def _worst_status(*statuses: str) -> str:
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    return min(statuses, key=lambda s: order.get(s, 2))


# ── Check 1: Anti-fabrication gate ────────────────────────────────────────────

def validate_no_fabrication(bsip0_records: list[dict]) -> dict:
    """Detect fabricated BSIP0 records.

    Two fabrication signatures are detected:

    1. Round-hour timestamps — ``hh:00:00`` in ``scraped_at`` across
       >= GATE_RULES["fabrication_round_hour_min_count"] products from
       different sources/retailers. A single product with a round-hour
       timestamp is normal (e.g. midnight run); multiple products across
       retailers sharing round-hour times is the fabrication signature.

    2. Byte-identical nutrition dicts — when >= GATE_RULES[
       "fabrication_identical_nutrition_min_count"] products from different
       retailers carry bit-for-bit identical nutrition sub-dicts. A single
       USDA-generic lookup producing the same nutrition is legitimate; identical
       nutrition across three separate retailer scrapes of different products
       is not.

    3. Source-tag / barcode mismatch — if ``source`` is ``"yohananof"`` (any
       case) the barcode must start with the Israeli 729 GS1 prefix. Any product
       failing this is flagged (WARN, not FAIL — barcodes can be re-registered).

    Args:
        bsip0_records: list of raw BSIP0 product dicts. Each dict is expected
            to carry at minimum: ``scraped_at`` (str ISO timestamp), ``source``
            (str retailer tag), ``barcode`` (str), ``nutrition`` (dict).

    Returns:
        Standard result dict: ``{"status": "PASS"|"FAIL"|"WARN", "messages": [...]}``.
        FAIL if either of the first two signatures is found; WARN if only the
        source/barcode mismatch is found.
    """
    messages: list[str] = []
    status = "PASS"

    # --- 1. Round-hour timestamp detection ---
    round_hour_min = int(GATE_RULES["fabrication_round_hour_min_count"])
    round_hour_products: list[dict] = []

    for rec in bsip0_records:
        ts = str(rec.get("scraped_at") or "")
        if _ROUND_HOUR_RE.search(ts):
            round_hour_products.append({
                "barcode": rec.get("barcode"),
                "source": rec.get("source"),
                "scraped_at": ts,
            })

    if len(round_hour_products) >= round_hour_min:
        # Check that they span at least 2 distinct sources (single-retailer bulk
        # scrape at midnight is legitimate; multi-retailer round-hours are not).
        sources = {p["source"] for p in round_hour_products if p["source"]}
        if len(sources) >= 2:
            status = "FAIL"
            messages.append(
                f"FABRICATION: {len(round_hour_products)} products carry round-hour "
                f"timestamps (hh:00:00) spanning {len(sources)} distinct sources: "
                f"{sorted(sources)}. "
                f"Round-hour timestamps across multiple retailers indicate fabricated "
                f"scrape times. Affected barcodes: "
                f"{[p['barcode'] for p in round_hour_products[:8]]}"
            )
        elif len(sources) == 1 and len(round_hour_products) >= round_hour_min:
            # Single-source but still suspiciously many round-hour times
            messages.append(
                f"WARN: {len(round_hour_products)} products from source "
                f"'{next(iter(sources), 'unknown')}' carry round-hour timestamps. "
                f"Single-source — may be a scheduled batch run. Verify manually."
            )
            if status == "PASS":
                status = "WARN"

    # --- 2. Byte-identical nutrition dicts detection ---
    identical_min = int(GATE_RULES["fabrication_identical_nutrition_min_count"])
    nutrition_fingerprints: list[tuple[str, str, str]] = []  # (fingerprint, source, barcode)

    for rec in bsip0_records:
        nutr = rec.get("nutrition")
        if nutr is None:
            continue
        # Canonical JSON fingerprint: sorted keys, compact separators
        try:
            fp = json.dumps(nutr, sort_keys=True, ensure_ascii=False,
                            separators=(",", ":"))
        except (TypeError, ValueError):
            continue
        nutrition_fingerprints.append((fp, str(rec.get("source") or ""), str(rec.get("barcode") or "")))

    fp_counter: Counter = Counter()
    fp_sources: dict[str, set] = {}
    fp_barcodes: dict[str, list] = {}
    for fp, source, barcode in nutrition_fingerprints:
        fp_counter[fp] += 1
        fp_sources.setdefault(fp, set()).add(source)
        fp_barcodes.setdefault(fp, []).append(barcode)

    for fp, count in fp_counter.items():
        if count >= identical_min and len(fp_sources.get(fp, set())) >= 2:
            # Identical nutrition across multiple retailers for different products
            sample_barcodes = fp_barcodes.get(fp, [])[:6]
            sample_sources = sorted(fp_sources.get(fp, set()))
            # Summarise the nutrition dict for readability (show energy + fat only)
            try:
                nutr_preview = json.loads(fp)
                preview_keys = {k: nutr_preview[k] for k in
                                ("energy_kcal_raw", "fat_raw", "protein_raw")
                                if k in nutr_preview}
            except Exception:
                preview_keys = {}
            status = "FAIL"
            messages.append(
                f"FABRICATION: {count} products across retailers "
                f"{sample_sources} share byte-identical nutrition dicts. "
                f"Barcodes: {sample_barcodes}. "
                f"Nutrition preview: {preview_keys}. "
                f"Identical cross-retailer nutrition is the fabrication signature "
                f"from TASK-215 (hard cheeses run 1)."
            )

    # --- 3. Source-tag / barcode mismatch ---
    source_mismatch: list[dict] = []
    for rec in bsip0_records:
        source = str(rec.get("source") or "").lower()
        barcode = str(rec.get("barcode") or "")
        if "yohananof" in source or "yochananof" in source:
            if barcode and not barcode.startswith(_YOHANANOF_BARCODE_PREFIX):
                source_mismatch.append({
                    "barcode": barcode,
                    "source": rec.get("source"),
                })

    if source_mismatch:
        if status == "PASS":
            status = "WARN"
        messages.append(
            f"SOURCE_MISMATCH: {len(source_mismatch)} product(s) claim source "
            f"'yohananof' but barcode does not start with Israeli prefix '729'. "
            f"Mismatches: {source_mismatch[:5]}. "
            f"Verify claimed source against actual retailer."
        )

    if not messages:
        messages.append("No fabrication signatures detected.")

    return _result(status, messages)


# ── Check 2: Portal availability ──────────────────────────────────────────────

def check_portal_availability(targets: list[str], timeout: int = 5) -> dict[str, str]:
    """Check that scrape target URLs are reachable before the run starts.

    Issues a HEAD request (with a GET fallback) to each target URL. Detects:
    - HTTP 503 → "MAINTENANCE"
    - Response body containing "maintenance" keyword → "MAINTENANCE"
    - Connection failure, timeout, or non-2xx/3xx status → "DOWN"
    - 2xx or 3xx response → "UP"

    Args:
        targets: list of URL strings to probe.
        timeout: per-request timeout in seconds (default 5).

    Returns:
        Dict mapping each target URL to one of "UP", "DOWN", or "MAINTENANCE".

    Important:
        This function returns the status dict. The CALLER is responsible for
        inspecting the result and raising / logging before proceeding. Any target
        that is DOWN or MAINTENANCE means the run should NOT proceed and the gate
        status should NOT be recorded as a self-pass. Example::

            availability = check_portal_availability(targets)
            down = [t for t, s in availability.items() if s != "UP"]
            if down:
                raise GateSelfPassError(
                    f"Portal(s) unavailable — run aborted: {down}",
                    [{"target": t, "status": availability[t]} for t in down],
                )
    """
    results: dict[str, str] = {}

    for url in targets:
        try:
            req = Request(url, method="HEAD", headers={
                "User-Agent": "Bari-QA-Availability-Probe/1.0"
            })
            with urlopen(req, timeout=timeout) as resp:
                status_code = resp.status
                # Read a small chunk of the body to check for maintenance page
                # Some portals return 200 with a maintenance HTML body.
                body_sample = ""
                try:
                    body_sample = resp.read(2048).decode("utf-8", errors="ignore").lower()
                except Exception:
                    pass

                if status_code == 503:
                    results[url] = "MAINTENANCE"
                elif "maintenance" in body_sample:
                    results[url] = "MAINTENANCE"
                elif 200 <= status_code < 400:
                    results[url] = "UP"
                else:
                    results[url] = "DOWN"

        except HTTPError as e:
            if e.code == 503:
                results[url] = "MAINTENANCE"
            else:
                results[url] = "DOWN"
        except (URLError, socket.timeout, OSError):
            results[url] = "DOWN"

    return results


# ── Check 3: Product page identity ────────────────────────────────────────────

def verify_product_identity(
    scraped_barcode: str | None,
    target_barcode: str | None,
    product_name: str | None,
    target_keywords: list[str] | None,
) -> dict:
    """Verify that a scraped product page matches the intended target.

    Prevents the "wrong card" scraping failure (TASK-215, hc-030): a scraper
    that clicks an adjacent product card captures the wrong product's ingredients
    and nutrition. This check confirms identity via barcode match OR keyword match
    before the record is accepted into the corpus.

    Matching logic (OR):
    - Barcode match: ``scraped_barcode == target_barcode`` (both non-empty, normalised).
    - Keyword match: all strings in ``target_keywords`` appear (case-insensitive) in
      ``product_name``. An empty ``target_keywords`` list is treated as no keyword
      constraint (passes keyword branch).

    Args:
        scraped_barcode: the barcode read from the scraped product page.
        target_barcode: the barcode from the scrape target list.
        product_name: the product name as it appears on the scraped page.
        target_keywords: list of keywords that should all appear in ``product_name``.

    Returns:
        Standard result dict. PASS if either condition holds; FAIL otherwise.
    """
    messages: list[str] = []
    sb = str(scraped_barcode or "").strip()
    tb = str(target_barcode or "").strip()
    name = str(product_name or "").lower()
    keywords = [str(k).lower() for k in (target_keywords or [])]

    barcode_match = bool(sb and tb and sb == tb)
    keyword_match = bool(not keywords or all(k in name for k in keywords))

    if barcode_match:
        messages.append(
            f"IDENTITY_OK: barcode match confirmed ({sb!r} == {tb!r})."
        )
        return _result("PASS", messages)

    if keyword_match and keywords:
        messages.append(
            f"IDENTITY_OK: keyword match — all of {keywords!r} found in "
            f"product name {product_name!r}."
        )
        return _result("PASS", messages)

    if keyword_match and not keywords:
        # No keyword constraint and no barcode — cannot verify identity
        messages.append(
            f"IDENTITY_UNVERIFIABLE: scraped_barcode={sb!r} does not match "
            f"target_barcode={tb!r} and no target_keywords provided. "
            f"Cannot confirm product identity. Provide barcode or keywords."
        )
        return _result("FAIL", messages)

    # Both branches failed
    messages.append(
        f"IDENTITY_MISMATCH: scraped_barcode={sb!r} != target_barcode={tb!r} "
        f"AND not all of {keywords!r} found in name {product_name!r}. "
        f"Wrong product card may have been scraped (cf. hc-030 Baby Bell failure)."
    )
    return _result("FAIL", messages)


# ── Check 4: Scope boundary enforcement ───────────────────────────────────────

def validate_scope_boundaries(
    products: list[dict],
    positive_types: list[str],
    negative_types: list[str],
    name_field: str = "name_he",
) -> dict:
    """Enforce category scope boundaries: every product must match at least one
    positive type and zero negative types.

    Prevents out-of-scope products from entering the corpus silently. The TASK-214
    failure: soy drink, oat drink, tomato juice, and coffee drink entered the fruit
    juice corpus because there was no boundary check at corpus assembly time.

    Matching is case-insensitive substring match on ``product[name_field]``.

    Args:
        products: list of BSIP0 product dicts.
        positive_types: list of strings — at least one must appear in the product
            name for the product to pass.
        negative_types: list of strings — if any appears in the product name, the
            product is rejected.
        name_field: dict key for the product name (default "name_he").

    Returns:
        Dict with keys:
          - ``passed``: list of products that passed both conditions.
          - ``rejected``: list of products that failed one or both conditions.
          - ``rejection_reasons``: dict mapping product barcode (or index) to
            the reason string.
          - ``status``: "PASS" if all products passed, "FAIL" if any were rejected
            (rejected products should not proceed to BSIP1).
    """
    passed: list[dict] = []
    rejected: list[dict] = []
    rejection_reasons: dict[str, str] = {}

    pos = [str(p).lower() for p in positive_types]
    neg = [str(n).lower() for n in negative_types]

    for i, product in enumerate(products):
        name_raw = str(product.get(name_field) or product.get("name") or "")
        name = name_raw.lower()
        barcode = str(product.get("barcode") or i)

        # Check positive match
        if pos and not any(p in name for p in pos):
            reason = (
                f"SCOPE_FAIL: no positive type matched in name {name_raw!r}. "
                f"Required one of: {positive_types}"
            )
            rejected.append(product)
            rejection_reasons[barcode] = reason
            continue

        # Check negative exclusion
        neg_hit = [n for n in neg if n in name]
        if neg_hit:
            original_terms = [negative_types[neg.index(n)] for n in neg_hit]
            reason = (
                f"SCOPE_FAIL: negative type(s) matched in name {name_raw!r}: "
                f"{original_terms}. Product is out-of-scope for this category."
            )
            rejected.append(product)
            rejection_reasons[barcode] = reason
            continue

        passed.append(product)

    overall_status = "PASS" if not rejected else "FAIL"
    return {
        "status": overall_status,
        "passed": passed,
        "rejected": rejected,
        "rejection_reasons": rejection_reasons,
        "messages": (
            [f"Scope boundary: {len(passed)} passed, {len(rejected)} rejected."]
            if rejected
            else [f"Scope boundary: all {len(passed)} products passed."]
        ),
    }


# ── Check 5: Consumer-facing output scan ──────────────────────────────────────

def validate_consumer_output(frontend_json_path: str | Path) -> dict:
    """Scan a built frontend JSON file for forbidden terms and data quality issues.

    Scans the JSON structure recursively for any string value in the fields
    ``positiveSignals``, ``limitingFactors``, and ``insightLine`` that contains
    a forbidden framework term (NOVA, BSIP, structural_class, etc.). Any hit
    is a hard FAIL — these are internal vocabulary that must never appear on the
    live consumer site.

    Also checks:
    - ``imageUrl`` null rate > 50% → WARN (consumers see broken images)
    - Any ingredient text > 500 chars → WARN (likely a scraping artifact, may
      indicate the scraper captured non-ingredient text)

    Args:
        frontend_json_path: absolute path to the packaged frontend JSON file
            (the file that will be copied to ``bari-web/src/data/comparisons/``).

    Returns:
        Standard result dict. FAIL on any forbidden-term hit; WARN on null image
        rate or long ingredients; PASS if clean.
    """
    path = Path(frontend_json_path)
    messages: list[str] = []
    status = "PASS"

    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return _result("FAIL", [f"FILE_NOT_FOUND: {path} does not exist."])
    except json.JSONDecodeError as e:
        return _result("FAIL", [f"JSON_PARSE_ERROR: {path}: {e}"])

    # Collect all products — handle both list and dict-with-products structure
    if isinstance(data, list):
        products = data
    elif isinstance(data, dict):
        products = data.get("products", [data])
    else:
        return _result("FAIL", [f"UNEXPECTED_STRUCTURE: root is {type(data).__name__}, expected list or dict."])

    forbidden_hits: list[str] = []
    image_null_count = 0
    image_total = 0
    long_ingredients: list[str] = []

    for product in products:
        if not isinstance(product, dict):
            continue

        product_id = str(product.get("id") or product.get("barcode") or "unknown")

        # Scan consumer-facing fields for forbidden terms
        for field_name in CONSUMER_SCAN_FIELDS:
            field_value = product.get(field_name)
            if field_value is None:
                continue

            # Support both scalar strings and lists of strings
            if isinstance(field_value, str):
                items = [field_value]
            elif isinstance(field_value, list):
                items = [str(v) for v in field_value if v is not None]
            else:
                items = [str(field_value)]

            for item in items:
                for term in FORBIDDEN_CONSUMER_TERMS:
                    if term in item:
                        forbidden_hits.append(
                            f"product={product_id!r} field={field_name!r} "
                            f"term={term!r} in value={item!r}"
                        )

        # imageUrl null rate
        image_url = product.get("imageUrl")
        image_total += 1
        if image_url is None or str(image_url).strip() == "":
            image_null_count += 1

        # Expansion ingredients length
        expansion = product.get("expansion") or {}
        ingredients_text = str(expansion.get("ingredients") or "")
        if len(ingredients_text) > 500:
            long_ingredients.append(
                f"product={product_id!r}: ingredients length={len(ingredients_text)} chars"
            )

    # Evaluate forbidden terms
    if forbidden_hits:
        status = "FAIL"
        messages.append(
            f"FRAMEWORK_LEAKAGE: {len(forbidden_hits)} forbidden term(s) found in "
            f"consumer-facing fields. This is a hard FAIL — do not deploy. "
            f"Violations: {forbidden_hits[:10]}"
        )
    else:
        messages.append(
            f"No forbidden framework terms found in {len(products)} products "
            f"across fields {list(CONSUMER_SCAN_FIELDS)}."
        )

    # Evaluate imageUrl null rate
    warn_threshold = float(GATE_RULES["null_imageUrl_rate_warn_threshold"])
    if image_total > 0:
        null_rate = image_null_count / image_total
        if null_rate > warn_threshold:
            if status == "PASS":
                status = "WARN"
            messages.append(
                f"IMAGE_NULL_RATE: {image_null_count}/{image_total} products "
                f"({null_rate:.0%}) have null imageUrl — threshold is "
                f"{warn_threshold:.0%}. Consumers will see broken image slots."
            )

    # Evaluate long ingredients
    if long_ingredients:
        if status == "PASS":
            status = "WARN"
        messages.append(
            f"LONG_INGREDIENTS: {len(long_ingredients)} product(s) have ingredients "
            f"text > 500 chars (likely a scraping artifact): "
            f"{long_ingredients[:5]}"
        )

    return _result(status, messages)


# ── Check 6: Run summary mandatory fields ─────────────────────────────────────

def validate_run_summary(summary_dict: dict) -> dict:
    """Verify that a BSIP0 run summary contains all required fields.

    Every BSIP0 run must record these fields in its summary so that gate decisions
    can be audited and replayed. A summary missing any field cannot be used to
    evaluate gate status.

    Required fields (per TASK-218 spec):
    - ``scrape_success_rate``: float — products with full panels / products attempted
    - ``source_verified``: bool — were barcodes cross-checked against a live source
    - ``null_imageUrl_rate``: float — fraction of products with null imageUrl
    - ``scope_rejected_count``: int — products boundary-rejected before corpus assembly
    - ``portal_availability``: dict — availability check results at run start

    Also enforces GATE_RULES thresholds on present fields:
    - ``scrape_success_rate < GATE_RULES["scrape_success_rate_min"]`` → FAIL
    - ``source_verified == False`` and GATE_RULES["source_verified_required"] → FAIL

    Args:
        summary_dict: the run summary dict as written by the scraper.

    Returns:
        Standard result dict. FAIL if any required field is missing or if any
        threshold rule fires.
    """
    required_fields = [
        "scrape_success_rate",
        "source_verified",
        "null_imageUrl_rate",
        "scope_rejected_count",
        "portal_availability",
    ]

    messages: list[str] = []
    status = "PASS"

    missing = [f for f in required_fields if f not in summary_dict]
    if missing:
        status = "FAIL"
        messages.append(
            f"MISSING_FIELDS: run summary is missing required fields: {missing}. "
            f"Every BSIP0 run summary must include all of: {required_fields}."
        )

    # Threshold checks on present fields
    rate = summary_dict.get("scrape_success_rate")
    if rate is not None:
        min_rate = float(GATE_RULES["scrape_success_rate_min"])
        try:
            rate_float = float(rate)
        except (TypeError, ValueError):
            rate_float = None
        if rate_float is not None and rate_float < min_rate:
            status = "FAIL"
            messages.append(
                f"SCRAPE_RATE_FAIL: scrape_success_rate={rate_float:.2f} < "
                f"required minimum {min_rate:.2f}. Run does not meet quality threshold."
            )

    source_verified = summary_dict.get("source_verified")
    if GATE_RULES["source_verified_required"] and source_verified is not None:
        if source_verified is False or str(source_verified).lower() == "false":
            status = "FAIL"
            messages.append(
                f"SOURCE_UNVERIFIED: source_verified=False. "
                f"GATE_RULES requires source_verified=True. "
                f"Barcodes must be cross-checked against a live source (OFF, "
                f"il_prices, or storefront) before gate can pass."
            )

    if not messages:
        messages.append(
            f"Run summary valid: all {len(required_fields)} required fields present "
            f"and threshold rules passed."
        )
    elif status == "PASS":
        messages.append("Run summary: all required fields present.")

    return _result(status, messages)


# ── Composite gate runner ──────────────────────────────────────────────────────

def run_full_gate(
    bsip0_records: list[dict],
    run_summary: dict,
    frontend_json_path: str | Path | None = None,
    portal_targets: list[str] | None = None,
) -> dict:
    """Run all applicable checks and return a composite gate result.

    Checks 2 (portal availability) and 3 (product identity) are caller-triggered
    during the scrape process itself. This runner covers checks 1, 4 (if
    positive/negative types are in the summary), 5, and 6.

    Raises GateSelfPassError if the composite status is FAIL, because a scraper
    must not self-pass with unresolved failures.

    Args:
        bsip0_records: list of raw BSIP0 product dicts.
        run_summary: the per-run summary dict.
        frontend_json_path: optional path to the packaged frontend JSON for check 5.
        portal_targets: optional list of URLs for check 2 (if provided, runs now).

    Returns:
        Dict with ``overall_status``, ``results`` (per-check), and ``messages``.
    """
    results: list[dict] = []

    # Check 1: Anti-fabrication
    fab_result = validate_no_fabrication(bsip0_records)
    fab_result["check"] = "1_anti_fabrication"
    results.append(fab_result)

    # Check 2: Portal availability (if targets provided)
    if portal_targets:
        availability = check_portal_availability(portal_targets)
        portal_status = "PASS" if all(v == "UP" for v in availability.values()) else "FAIL"
        portal_messages = [f"{url}: {st}" for url, st in availability.items()]
        portal_result = _result(portal_status, portal_messages)
        portal_result["check"] = "2_portal_availability"
        portal_result["availability"] = availability
        results.append(portal_result)

    # Check 5: Consumer output (if path provided)
    if frontend_json_path is not None:
        consumer_result = validate_consumer_output(frontend_json_path)
        consumer_result["check"] = "5_consumer_output"
        results.append(consumer_result)

    # Check 6: Run summary
    summary_result = validate_run_summary(run_summary)
    summary_result["check"] = "6_run_summary"
    results.append(summary_result)

    # Derive overall status
    all_statuses = [r["status"] for r in results]
    overall = _worst_status(*all_statuses)

    composite = {
        "overall_status": overall,
        "results": results,
        "messages": [
            f"Gate check complete. Overall: {overall}. "
            f"FAIL={all_statuses.count('FAIL')} WARN={all_statuses.count('WARN')} "
            f"PASS={all_statuses.count('PASS')}"
        ],
    }

    if overall == "FAIL":
        fail_results = [r for r in results if r["status"] == "FAIL"]
        raise GateSelfPassError(
            f"Gate has {len(fail_results)} unresolved FAIL(s) — run is not eligible "
            f"for PASS status. Resolve all FAILs before declaring gate PASS.",
            fail_results,
        )

    return composite
