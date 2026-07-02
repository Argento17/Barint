"""
Rami Levy (רמי לוי) probe — BSIP0 acquisition v2.

Access method: static HTTP POST to the Rami Levy catalog JSON API.
No Playwright / browser required.

Verified endpoint (TASK-395, 2026-06-25, new_sources_probe_v1.md):
    POST https://www.rami-levy.co.il/api/catalog?
    Body: {"q": "<query>", "from": <offset>, "store": <store_id>}
    Response: {"data": [...], "total": N}

All 7 Tier-1 nutrition fields are in gs.Nutritional_Values keyed by
English field_name (Energy_per_100_grams, Fats_per_100_grams, etc.).
Hebrew ingredients are in gs.Ingredient_Sequence_and_Name.
Barcode is item["barcode"] (integer, cast to string).

BSIP0 gate (from acquisition_audit_v2.py):
    GATE_MIN_PRODUCTS    = 20
    GATE_NUTRITION_PCT   = 0.70   (energy_kcal_raw or carbs_raw or fat_raw or protein_raw)
    GATE_INGREDIENT_PCT  = 0.40

No OFF sources are used — all data is from the Rami Levy first-party API.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

# Ensure retailer_base can be imported when run as standalone script
sys.path.insert(0, str(Path(__file__).parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from retailer_base import RawProduct, RetailProbeResult, RetailSource

# ---------------------------------------------------------------------------
# Constants

API_URL = "https://www.rami-levy.co.il/api/catalog?"
IMAGE_BASE = "https://img.rami-levy.co.il"

# Store 331 verified by live fetch (new_sources_probe_v1.md §A.1.1).
# Additional candidate stores from available_in analysis: 82, 179, 279, 290, 306, 412.
# Using store 331 as primary; others as fallback if primary returns 0.
PRIMARY_STORE = 331
FALLBACK_STORES = [82, 179, 279, 290, 306, 412]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Type": "application/json",
    "Referer": "https://www.rami-levy.co.il/he/online/search",
    "Origin": "https://www.rami-levy.co.il",
    "uid": "0",
}

# Request tuning
PAGE_SIZE = 30          # API default; total/from pagination
REQUEST_TIMEOUT = 20    # seconds
BETWEEN_PAGE_DELAY = 0.4  # seconds between pagination requests
MAX_PAGES = 20          # safety cap (30 * 20 = 600 products max per query)

# Bread shelf queries (matching shufersal_probe.py SEARCH_QUERIES for breadth)
BREAD_QUERIES = ["לחם", "קרקר", "כוסמין", "שיפון", "פיתה", "לחמניה", "בגט"]

# ---------------------------------------------------------------------------
# Nutrition field name -> RawProduct field mapping
# API field_name (English, per-100g) → RawProduct attribute

NUTR_FIELD_MAP: dict[str, str] = {
    "Energy_per_100_grams":                   "energy_kcal_raw",
    "Fats_per_100_grams":                     "fat_raw",
    "Saturated_Fatty_Acids_per_100_grams":    "sat_fat_raw",   # bonus — stored in raw_source_json
    "Carbohydrates_per_100_grams":            "carbs_raw",
    "Sugars_from_Carbohydrates_per_100_grams": "sugar_raw",
    "Sodium_per_100_grams":                   "sodium_raw",
    "Proteins_per_100_grams":                 "protein_raw",
    "Dietary_Fibers_per_100_grams":           "fiber_raw",
    "Trans_Fatty_Acids_per_100_grams":        "trans_fat_raw",  # stored in raw_source_json
}

# Fields mapped directly to RawProduct attributes (subset that RawProduct defines)
DIRECT_ATTRS: set[str] = {
    "energy_kcal_raw",
    "fat_raw",
    "carbs_raw",
    "sugar_raw",
    "sodium_raw",
    "protein_raw",
    "fiber_raw",
}


# ---------------------------------------------------------------------------
# Low-level API helpers

def _post_catalog(query: str, from_idx: int = 0, store: int = PRIMARY_STORE) -> dict | None:
    """POST one page to the Rami Levy catalog API. Returns parsed JSON or None."""
    payload = {"q": query, "from": from_idx, "store": store}
    try:
        resp = requests.post(
            API_URL, json=payload, headers=HEADERS, timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return None


def _fetch_all_for_query(
    query: str, store: int = PRIMARY_STORE
) -> tuple[list[dict], int, str | None]:
    """
    Paginate through all results for a single query.

    Returns:
        (items, total_reported, error_msg_or_None)
    """
    all_items: list[dict] = []
    from_idx = 0
    total_reported = 0
    pages = 0

    while pages < MAX_PAGES:
        data = _post_catalog(query, from_idx, store)
        if data is None:
            return all_items, total_reported, f"API request failed at from={from_idx}"

        batch = data.get("data", [])
        if not isinstance(batch, list):
            return all_items, total_reported, f"Unexpected data type: {type(batch)}"

        total_reported = data.get("total", len(all_items) + len(batch))
        all_items.extend(batch)
        from_idx += len(batch)
        pages += 1

        if not batch or from_idx >= total_reported:
            break

        time.sleep(BETWEEN_PAGE_DELAY)

    return all_items, total_reported, None


def _discover_store(query: str) -> int:
    """
    Try PRIMARY_STORE; if it returns 0 products, try FALLBACK_STORES.
    Returns the first store ID that returns results, or PRIMARY_STORE as default.
    """
    data = _post_catalog(query, 0, PRIMARY_STORE)
    if data and data.get("data"):
        return PRIMARY_STORE
    for s in FALLBACK_STORES:
        data = _post_catalog(query, 0, s)
        if data and data.get("data"):
            return s
    return PRIMARY_STORE


# ---------------------------------------------------------------------------
# Field extraction helpers

def _extract_nutritional_values(gs: dict) -> dict[str, str]:
    """
    Parse gs.Nutritional_Values — a list of group objects, each containing a
    "fields" list of {field_name, value} entries.

    Returns a flat dict: {field_name -> value_string}
    """
    result: dict[str, str] = {}
    nutr_groups = gs.get("Nutritional_Values") or []
    for group in nutr_groups:
        if not isinstance(group, dict):
            continue
        for field in group.get("fields", []):
            if not isinstance(field, dict):
                continue
            fn = field.get("field_name", "")
            val = field.get("value", "")
            if fn and val is not None:
                result[fn] = str(val)
    return result


def _item_to_raw_product(
    item: dict, retailer_id: str, retailer_name: str, query: str, store: int
) -> RawProduct:
    """Convert one Rami Levy catalog item to a RawProduct."""
    now = datetime.utcnow().isoformat()
    gs: dict = item.get("gs") or {}

    # --- Identity ---
    barcode = str(item.get("barcode", "")).strip()
    # gs.name is the GS1 label name; item.name is the display name
    name_he = (
        gs.get("name") or item.get("name") or ""
    ).strip()
    brand = (gs.get("BrandName") or "").strip()

    # --- Image ---
    images_block = gs.get("images") or {}
    image_path = images_block.get("original", "")
    if image_path:
        image_url = IMAGE_BASE + image_path if not image_path.startswith("http") else image_path
    elif barcode:
        image_url = f"{IMAGE_BASE}/product/{barcode}/large.jpg"
    else:
        image_url = ""

    # --- Category hierarchy ---
    dept = item.get("department", {})
    dept_name = dept.get("name", "") if isinstance(dept, dict) else ""
    grp = item.get("group", {})
    grp_name = grp.get("name", "") if isinstance(grp, dict) else ""

    # --- Nutrition ---
    nutr_values = _extract_nutritional_values(gs)

    energy_kcal_raw = nutr_values.get("Energy_per_100_grams", "")
    fat_raw         = nutr_values.get("Fats_per_100_grams", "")
    carbs_raw       = nutr_values.get("Carbohydrates_per_100_grams", "")
    sugar_raw       = nutr_values.get("Sugars_from_Carbohydrates_per_100_grams", "")
    sodium_raw      = nutr_values.get("Sodium_per_100_grams", "")
    protein_raw     = nutr_values.get("Proteins_per_100_grams", "")
    fiber_raw       = nutr_values.get("Dietary_Fibers_per_100_grams", "")

    # Bonus fields stored in raw_source_json (not on RawProduct base but available for BSIP1)
    sat_fat_raw   = nutr_values.get("Saturated_Fatty_Acids_per_100_grams", "")
    trans_fat_raw = nutr_values.get("Trans_Fatty_Acids_per_100_grams", "")

    # --- Ingredients ---
    ingredients_raw = (gs.get("Ingredient_Sequence_and_Name") or "").strip()

    # --- Red label ---
    red_label_entries = gs.get("Food_Symbol_Red") or []
    red_label_codes = [
        e.get("code", "") for e in red_label_entries if isinstance(e, dict)
    ]

    # --- Source URL (canonical product page) ---
    item_id = item.get("id") or item.get("rl_catalog_id") or ""
    source_url = (
        f"https://www.rami-levy.co.il/he/online/{dept.get('id', '')}/product/{item_id}"
        if item_id else
        f"https://www.rami-levy.co.il/api/catalog? store={store} q={query}"
    )

    raw_source_json = {
        "barcode": barcode,
        "store": store,
        "query": query,
        "sat_fat_raw": sat_fat_raw,
        "trans_fat_raw": trans_fat_raw,
        "red_label_codes": red_label_codes,
        "country_of_origin": gs.get("Country_of_Origin", ""),
        "net_content": gs.get("Net_Content", {}),
        "all_nutr_values": nutr_values,
    }

    return RawProduct(
        retailer_id=retailer_id,
        retailer_name=retailer_name,
        source_url=source_url,
        scraped_at=now,
        name_he=name_he,
        name_en="",
        brand=brand,
        barcode=barcode,
        category_raw=dept_name,
        subcategory_raw=grp_name,
        energy_kcal_raw=energy_kcal_raw,
        protein_raw=protein_raw,
        carbs_raw=carbs_raw,
        fat_raw=fat_raw,
        fiber_raw=fiber_raw,
        sodium_raw=sodium_raw,
        sugar_raw=sugar_raw,
        ingredients_raw=ingredients_raw,
        ingredients_language="he" if ingredients_raw else "",
        image_urls=[image_url] if image_url else [],
        extraction_method="api_direct",
        extraction_confidence="high",
        raw_source_json=raw_source_json,
    )


# ---------------------------------------------------------------------------
# Probe class

class RamiLevyProbe(RetailSource):
    """
    Rami Levy grocery catalog probe via JSON POST API.

    requires_browser = False — no Playwright needed.
    Queries: BREAD_QUERIES by default; caller may pass custom queries.
    """

    retailer_id   = "rami_levy"
    retailer_name = "רמי לוי"
    retailer_url  = "https://www.rami-levy.co.il"
    requires_browser = False
    country = "IL"

    def __init__(
        self,
        queries: list[str] | None = None,
        store: int | None = None,
        max_products: int = 500,
    ):
        self.queries = queries or BREAD_QUERIES
        self._store = store   # None = auto-discover
        self.max_products = max_products

    def probe(self) -> RetailProbeResult:
        result = self._empty_result(
            access_method="http_static",
            access_status="pending",
        )

        try:
            self._run(result)
        except Exception as exc:
            result.access_status = "failed"
            result.blocker_type = "probe_exception"
            result.blocker_detail = str(exc)
            result.probe_notes.append(f"Probe crashed unexpectedly: {exc}")

        return result

    def _run(self, result: RetailProbeResult) -> None:
        # --- Store discovery ---
        store = self._store
        if store is None:
            store = _discover_store(self.queries[0])
            result.probe_notes.append(
                f"Store discovery: selected store {store} for query '{self.queries[0]}'"
            )
        else:
            result.probe_notes.append(f"Using specified store {store}")

        # --- Fetch ---
        all_items_raw: list[dict] = []
        seen_barcodes: set[str] = set()

        for query in self.queries:
            if len(all_items_raw) >= self.max_products:
                result.probe_notes.append(
                    f"Reached max_products cap ({self.max_products}), stopping queries"
                )
                break

            items, total_reported, err = _fetch_all_for_query(query, store)

            if err:
                result.probe_notes.append(f"Query '{query}': {err}")
                continue

            result.probe_notes.append(
                f"Query '{query}': fetched {len(items)} (API total={total_reported})"
            )

            # Deduplicate by barcode
            new_count = 0
            for item in items:
                bc = str(item.get("barcode", "")).strip()
                if bc and bc in seen_barcodes:
                    continue
                if bc:
                    seen_barcodes.add(bc)
                all_items_raw.append(item)
                new_count += 1
                if len(all_items_raw) >= self.max_products:
                    break

            result.probe_notes.append(
                f"Query '{query}': {new_count} new (deduplicated)"
            )

        result.probe_notes.append(
            f"Total raw items after dedup: {len(all_items_raw)}"
        )

        if not all_items_raw:
            # Try PATCH: different store
            fallback_store = next(
                (s for s in FALLBACK_STORES if s != store), None
            )
            if fallback_store:
                result.probe_notes.append(
                    f"Zero items from store {store}; retrying with fallback store {fallback_store}"
                )
                items, total_reported, err = _fetch_all_for_query(
                    self.queries[0], fallback_store
                )
                if items:
                    all_items_raw = items
                    store = fallback_store
                    result.probe_notes.append(
                        f"Fallback store {fallback_store} returned {len(items)} items"
                    )

        if not all_items_raw:
            result.access_status = "failed"
            result.blocker_type = "api_no_products"
            result.blocker_detail = (
                f"API responded but returned 0 products for all queries "
                f"({self.queries}) on store {store}"
            )
            return

        # --- Convert to RawProduct ---
        products: list[RawProduct] = []
        for item in all_items_raw:
            try:
                p = _item_to_raw_product(
                    item,
                    retailer_id=self.retailer_id,
                    retailer_name=self.retailer_name,
                    query=self.queries[0],
                    store=store,
                )
                products.append(p)
            except Exception as exc:
                result.probe_notes.append(
                    f"Skipping item (parse error): {exc} — "
                    f"barcode={item.get('barcode', '?')}"
                )

        result.products = products
        result.access_status = "accessible"
        result.http_status = 200

        n = len(products)
        n_nutr = sum(1 for p in products if p.has_nutrition())
        n_ingr = sum(1 for p in products if p.has_ingredients())
        result.probe_notes.append(
            f"Parsed {n} products | nutrition={n_nutr}/{n} ({n_nutr/n:.0%}) "
            f"| ingredients={n_ingr}/{n} ({n_ingr/n:.0%})"
        )


# ---------------------------------------------------------------------------
# BSIP0 gate (mirrors acquisition_audit_v2.py thresholds)

GATE_MIN_PRODUCTS  = 20
GATE_NUTRITION_PCT = 0.70
GATE_INGREDIENT_PCT = 0.40


def run_bsip0_gate(products: list[RawProduct]) -> dict:
    n = len(products)
    if n == 0:
        return {"passed": False, "reason": "zero_products", "n_products": 0}

    n_nutr = sum(1 for p in products if p.has_nutrition())
    n_ingr = sum(1 for p in products if p.has_ingredients())
    nutr_pct = n_nutr / n
    ingr_pct = n_ingr / n

    failures = []
    if n < GATE_MIN_PRODUCTS:
        failures.append(f"too_few_products: {n} < {GATE_MIN_PRODUCTS}")
    if nutr_pct < GATE_NUTRITION_PCT:
        failures.append(f"low_nutrition: {nutr_pct:.1%} < {GATE_NUTRITION_PCT:.0%}")
    if ingr_pct < GATE_INGREDIENT_PCT:
        failures.append(f"low_ingredients: {ingr_pct:.1%} < {GATE_INGREDIENT_PCT:.0%}")

    return {
        "passed": len(failures) == 0,
        "reason": "; ".join(failures) if failures else "all criteria met",
        "n_products": n,
        "n_nutrition": n_nutr,
        "n_ingredients": n_ingr,
        "nutrition_pct": round(nutr_pct, 4),
        "ingredient_pct": round(ingr_pct, 4),
        "failures": failures,
    }


# ---------------------------------------------------------------------------
# Per-field coverage report (Tier-1 + ingredients + barcode)

TIER1_NUTR_FIELDS = [
    ("energy_kcal", "Energy_per_100_grams"),
    ("fat",         "Fats_per_100_grams"),
    ("sat_fat",     "Saturated_Fatty_Acids_per_100_grams"),
    ("carbs",       "Carbohydrates_per_100_grams"),
    ("sugars",      "Sugars_from_Carbohydrates_per_100_grams"),
    ("sodium",      "Sodium_per_100_grams"),
    ("protein",     "Proteins_per_100_grams"),
]


def per_field_coverage(products: list[RawProduct]) -> dict:
    n = len(products)
    if n == 0:
        return {}

    coverage: dict[str, dict] = {}

    # Tier-1 nutrition fields (from raw_source_json.all_nutr_values)
    for bari_name, api_field in TIER1_NUTR_FIELDS:
        count = sum(
            1 for p in products
            if p.raw_source_json.get("all_nutr_values", {}).get(api_field, "") != ""
        )
        coverage[bari_name] = {
            "n": count,
            "total": n,
            "pct": round(count / n, 4),
            "api_field": api_field,
        }

    # Ingredients
    n_ingr = sum(1 for p in products if p.has_ingredients())
    coverage["ingredients"] = {"n": n_ingr, "total": n, "pct": round(n_ingr / n, 4)}

    # Barcode
    n_bc = sum(1 for p in products if p.barcode)
    coverage["barcode"] = {"n": n_bc, "total": n, "pct": round(n_bc / n, 4)}

    return coverage


# ---------------------------------------------------------------------------
# Standalone runner (end-to-end prove-out)

def _run_standalone(
    queries: list[str] | None = None,
    store: int | None = None,
    output_dir: Path | None = None,
) -> None:
    """
    Run the probe end-to-end on the bread shelf and report results.
    Writes JSON output to output_dir.
    """
    import argparse

    if queries is None:
        # Running as __main__ — parse CLI
        parser = argparse.ArgumentParser(description="Rami Levy BSIP0 probe")
        parser.add_argument("--store", type=int, default=None, help="Store ID (default: auto-discover)")
        parser.add_argument(
            "--queries",
            default=",".join(BREAD_QUERIES),
            help="Comma-separated Hebrew queries",
        )
        parser.add_argument(
            "--output-dir",
            default=r"C:\Bari\03_operations\bsip0\acquisition_v2\ramilevy_output",
            help="Directory to write output JSON",
        )
        parser.add_argument(
            "--max-products", type=int, default=500,
            help="Maximum products to fetch (deduped)",
        )
        args = parser.parse_args()
        queries = [q.strip() for q in args.queries.split(",") if q.strip()]
        store = args.store
        output_dir = Path(args.output_dir)
        max_products = args.max_products
    else:
        max_products = 500

    output_dir = output_dir or Path(r"C:\Bari\03_operations\bsip0\acquisition_v2\ramilevy_output")
    output_dir.mkdir(parents=True, exist_ok=True)

    run_id = f"ramilevy_bread_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}"
    print(f"\n=== Rami Levy BSIP0 Probe ===")
    print(f"Run ID : {run_id}")
    print(f"Queries: {queries}")
    print(f"Store  : {store or 'auto-discover'}")
    print(f"Output : {output_dir}")
    print()

    probe = RamiLevyProbe(queries=queries, store=store, max_products=max_products)
    result = probe.probe()

    print(f"Access status : {result.access_status}")
    print(f"Products found: {result.n_products()}")
    for note in result.probe_notes:
        print(f"  {note}")

    products = result.products

    # BSIP0 gate
    gate = run_bsip0_gate(products)
    print(f"\nBSIP0 Gate: {'PASSED' if gate['passed'] else 'FAILED'} — {gate['reason']}")
    print(f"  Products  : {gate['n_products']}")
    if gate['n_products'] > 0:
        print(f"  Nutrition : {gate['n_nutrition']}/{gate['n_products']} ({gate['nutrition_pct']:.1%})")
        print(f"  Ingredients: {gate['n_ingredients']}/{gate['n_products']} ({gate['ingredient_pct']:.1%})")

    # Per-field coverage
    coverage = per_field_coverage(products)
    if coverage:
        print(f"\nPer-field coverage ({len(products)} products):")
        print(f"  {'Field':<18} {'N':>5} {'Total':>6} {'Pct':>7}")
        print(f"  {'-'*40}")
        for fname, fc in coverage.items():
            pct_str = f"{fc['pct']:.1%}"
            print(f"  {fname:<18} {fc['n']:>5} {fc['total']:>6} {pct_str:>7}")

    # Write outputs
    report = {
        "run_id": run_id,
        "run_date": datetime.utcnow().isoformat(),
        "source": "rami_levy",
        "queries": queries,
        "store_used": result.probe_notes[0] if result.probe_notes else "",
        "access_status": result.access_status,
        "probe_notes": result.probe_notes,
        "bsip0_gate": gate,
        "per_field_coverage": coverage,
        "products": [p.to_dict() for p in products],
    }

    report_path = output_dir / f"{run_id}_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[wrote] {report_path}")

    # BSIP0 verification artifact (barcode + nutrition presence flat table)
    verification_rows = [
        {
            "barcode": p.barcode,
            "name_he": p.name_he,
            "has_nutrition": p.has_nutrition(),
            "has_ingredients": p.has_ingredients(),
            "energy_kcal_raw": p.energy_kcal_raw,
            "fat_raw": p.fat_raw,
            "carbs_raw": p.carbs_raw,
            "sugar_raw": p.sugar_raw,
            "sodium_raw": p.sodium_raw,
            "protein_raw": p.protein_raw,
            "fiber_raw": p.fiber_raw,
            "sat_fat_raw": p.raw_source_json.get("sat_fat_raw", ""),
            "ingredients_chars": len(p.ingredients_raw),
            "retailer_id": p.retailer_id,
            "source_url": p.source_url,
        }
        for p in products
    ]
    veri_path = output_dir / f"{run_id}_verification_table.json"
    veri_path.write_text(
        json.dumps(verification_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[wrote] {veri_path}")
    print("\nDone.")

    return gate, coverage, products


if __name__ == "__main__":
    _run_standalone()
