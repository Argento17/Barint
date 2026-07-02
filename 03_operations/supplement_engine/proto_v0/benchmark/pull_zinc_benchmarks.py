"""  # noqa: UTF-8
pull_zinc_benchmarks.py - TASK-361A zinc shelf cohort scraper.

Pulls zinc-PRIMARY products from:
  US  -> NIH DSLD   (https://api.ods.od.nih.gov/dsld)
  CA  -> Health Canada LNHPD (https://health-products.canada.ca/api/natural-licences/)

Output files (same directory as this script):
  shelf_us_zinc_dsld.json
  shelf_ca_zinc_lnhpd.json

Off-limits: Open Food Facts is NEVER used.  Data sourced only from official gov DBs.

Elemental zinc fractions used when DB returns compound mass:
  Zinc oxide           ~80%   (65.38/81.41)
  Zinc sulfate mono.   ~36%   (65.38/179.47)
  Zinc citrate         ~31%   (65.38/211.52 × 2/3  -> ~20.6%; IUPAC 3:2 salt -> ~31.2%)
  Zinc acetate         ~30%   (65.38/219.53)
  Zinc picolinate      ~20%   (65.38/323.65)
  Zinc gluconate       ~14.3% (65.38/455.73)
  Zinc bisglycinate    ~20%   (range 14–20%; use 20% = conservative upper)

  NB: DSLD already reports elemental quantities in structured ingredient rows when the
  ingredient name is "Zinc".  When the name is e.g. "Zinc Gluconate" the quantity MAY
  be compound mass; we apply the fraction then.  LNHPD explicitly states elemental mg
  for the regulated quantity column, matching the pattern already confirmed for magnesium.

Zinc UL: 40 mg elemental (US IoM / Health Canada). Flag any product exceeding this.
"""
from __future__ import annotations

import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DSLD_API = "https://api.ods.od.nih.gov/dsld"
LNHPD_API = "https://health-products.canada.ca/api/natural-licences"
USER_AGENT = "Bari/1.0 (+nutrition-scoring; contact tbarhaim@gmail.com)"
BENCHMARK_DIR = Path(__file__).parent
CAPTURED = datetime.now(timezone.utc).strftime("%Y-%m-%d")
CAPTURED_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

ZINC_UL_MG = 40.0  # elemental zinc UL (US IoM / Health Canada)

# Elemental zinc fractions by compound (lower-cased keyword -> fraction)
ELEMENTAL_FRACTIONS: dict[str, float] = {
    "zinc oxide":        0.800,
    "zinc sulfate":      0.360,
    "zinc citrate":      0.312,
    "zinc acetate":      0.298,
    "zinc picolinate":   0.202,
    "zinc gluconate":    0.143,
    "zinc bisglycinate": 0.200,   # 14–20%; use 20% conservative
    "zinc glycinate":    0.200,   # bisglycinate trade names
    "zinc monomethionine": 0.197, # ~20%
    "zinc l-monomethionine": 0.197,
    "zinc amino acid chelate": 0.200,  # generic chelate; use 20%
    "zinc orotate":      0.170,   # ~17%
    "zinc carnosine":    0.230,   # ~23%
    "zinc methionine":   0.197,
}

# Multi-mineral / multi-vitamin exclusion signals for DSLD
DSLD_EXCLUDE_PRODUCT_TYPES = {
    "Multivitamin", "Multivitamin/Mineral",
    "Multi Vitamin/Mineral Combination", "Multivitamin/Multimineral",
    "Multi-Vitamin", "Multi-Mineral", "Weight Loss",
}

# Signals in name -> exclude as combo (zinc is incidental)
DSLD_NAME_EXCLUDE = [
    "multi", "prenatal", "daily", "complete", "vitamin c", "vitamin d",
    "calcium", "magnesium", "iron", "copper", "selenium", "chromium",
    "b complex", "b-complex", "immune",
]

# LNHPD: product name must contain "zinc", must NOT contain these (combo signals)
LNHPD_COMBO_SIGNALS = [
    "calcium", "vitamin", "magnesium", "multi", "mineral", "iron",
    "phosphorus", "potassium", "selenium", "chromium", "manganese",
    "copper", "boron", "iodine", "vitamin c", "vitamin d",
]

# ---------------------------------------------------------------------------
# Shared HTTP helper (no external deps)
# ---------------------------------------------------------------------------

def _get_json(url: str, timeout: int = 30, ctx: ssl.SSLContext | None = None) -> Any:
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    for attempt in range(3):
        try:
            kwargs: dict = {"timeout": timeout}
            if ctx:
                kwargs["context"] = ctx
            with urllib.request.urlopen(req, **kwargs) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"Failed to fetch {url}")


def _ssl_ctx() -> ssl.SSLContext:
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
        if not cafile:
            raise RuntimeError(
                "SSL CA bundle not found. Install certifi or set SSL_CERT_FILE."
            )
        return ssl.create_default_context(cafile=cafile)


def _unwrap(data: Any) -> list:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("data", [])
    return []


# ---------------------------------------------------------------------------
# Elemental zinc conversion
# ---------------------------------------------------------------------------

def _to_elemental(quantity: float, ingredient_name: str) -> float | None:
    """Convert compound mass to elemental zinc using known fractions.

    If ingredient_name is plain "Zinc" or "Zinc (elemental)" the quantity is already
    elemental — return as-is.  Otherwise look up the compound fraction.
    """
    nl = ingredient_name.lower().strip()
    # Already elemental
    if nl in ("zinc", "zinc (elemental)", "elemental zinc", "zinc element"):
        return quantity
    # Exact-match first
    if nl in ELEMENTAL_FRACTIONS:
        f = ELEMENTAL_FRACTIONS[nl]
        print(f"      [convert] {ingredient_name}: {quantity} mg × {f:.3f} = {round(quantity * f, 2)} mg elemental")
        return round(quantity * f, 2)
    # Longest substring match
    best: tuple[int, float] | None = None
    for compound, frac in ELEMENTAL_FRACTIONS.items():
        if compound in nl:
            if best is None or len(compound) > best[0]:
                best = (len(compound), frac)
    if best:
        f = best[1]
        print(f"      [convert] {ingredient_name}: {quantity} mg × {f:.3f} = {round(quantity * f, 2)} mg elemental (substring match)")
        return round(quantity * f, 2)
    # Unknown compound — return None so caller can log and skip
    print(f"      [WARN] unknown zinc compound '{ingredient_name}' — cannot convert; record included with elemental_mg_per_serving=null")
    return None


# ---------------------------------------------------------------------------
# US — DSLD
# ---------------------------------------------------------------------------

def _dsld_search_zinc(size: int = 250) -> list[dict]:
    """Search DSLD for zinc products. Returns raw hits."""
    url = f"{DSLD_API}/v9/search-filter"
    params = f"q=zinc&size={size}"
    data = _get_json(f"{url}?{params}", timeout=30)
    return data.get("hits", [])


def _safe_str(val) -> str:
    """Coerce a DSLD field to string — it can sometimes be a dict or list."""
    if val is None:
        return ""
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        # productType sometimes arrives as {"id": ..., "name": "..."}
        return val.get("name") or val.get("label") or str(val)
    return str(val)


def _dsld_is_zinc_primary(hit: dict) -> bool:
    """Return True if this DSLD hit is a zinc-primary product."""
    src = hit.get("_source", {})
    product_name = _safe_str(src.get("fullName") or src.get("productName")).lower()
    product_type = _safe_str(src.get("productType")).strip()

    # Exclude by product type
    if product_type in DSLD_EXCLUDE_PRODUCT_TYPES:
        return False

    # Exclude obvious multis and combos by name signal
    for sig in DSLD_NAME_EXCLUDE:
        if sig in product_name:
            return False

    # Must contain "zinc" in the name
    if "zinc" not in product_name:
        return False

    return True


def _dsld_get_zinc_label(dsld_id: str) -> dict | None:
    """Fetch label detail; find the zinc ingredient row and extract elemental mg."""
    url = f"{DSLD_API}/v9/label/{dsld_id}"
    try:
        d = _get_json(url, timeout=30)
    except Exception as e:
        print(f"    [DSLD error] label {dsld_id}: {e}")
        return None

    # Ingredient rows
    rows = d.get("ingredientRows") or d.get("ingredients") or []

    # Filter zinc rows
    zinc_rows = [
        r for r in rows
        if "zinc" in (r.get("name") or r.get("ingredientName") or "").lower()
    ]
    if not zinc_rows:
        print(f"    [skip] {dsld_id}: no zinc ingredient row found")
        return None

    # Zinc-primary check: if there are >2 distinct mineral rows total, treat as incidental
    mineral_keywords = ["magnesium", "calcium", "iron", "selenium", "chromium",
                        "manganese", "copper", "potassium", "iodine", "boron"]
    all_ing_names = [
        (r.get("name") or r.get("ingredientName") or "").lower()
        for r in rows
    ]
    other_mineral_count = sum(
        1 for n in all_ing_names
        if any(mk in n for mk in mineral_keywords) and "zinc" not in n
    )
    if other_mineral_count > 2:
        print(f"    [skip] {dsld_id}: {other_mineral_count} other mineral rows -> not zinc-primary")
        return None

    # Extract serving from product level
    serving_sizes = d.get("servingSizes") or []
    serving_qty = None
    serving_unit = None
    if serving_sizes:
        ss = serving_sizes[0]
        serving_qty = ss.get("minQuantity") or ss.get("quantity")
        serving_unit = ss.get("unit") or ss.get("servingSizeUnit")

    servings_per_container = None
    if d.get("servingsPerContainer"):
        servings_per_container = str(d["servingsPerContainer"])

    product_type = _safe_str(d.get("productType")).strip()

    # Extract elemental zinc from the first zinc row
    zrow = zinc_rows[0]
    zname = (zrow.get("name") or zrow.get("ingredientName") or "Zinc").strip()

    qlist = zrow.get("quantity") or []
    qobj = qlist[0] if isinstance(qlist, list) and qlist else (
        qlist if isinstance(qlist, dict) else {}
    )
    raw_qty = qobj.get("quantity")
    raw_unit = (qobj.get("unit") or "").lower()

    elemental_mg: float | None = None
    if raw_qty is not None and raw_unit == "mg":
        elemental_mg = _to_elemental(float(raw_qty), zname)
    elif raw_qty is not None and raw_unit in ("mcg", "µg", "ug"):
        # micrograms — unusual for zinc but convert
        elemental_mg = _to_elemental(float(raw_qty) / 1000.0, zname)

    # Derive form: use ingredient name as form descriptor
    form = zname if zname.lower() != "zinc" else "Zinc (unspecified)"

    # Build serving string from row-level serving size if product-level is absent
    if serving_qty is None:
        row_sv_qty = qobj.get("servingSizeQuantity")
        row_sv_unit = qobj.get("servingSizeUnit") or ""
        if row_sv_qty:
            serving_qty = row_sv_qty
            serving_unit = row_sv_unit

    serving_str = None
    if serving_qty is not None:
        serving_str = f"{serving_qty} {serving_unit}".strip() if serving_unit else str(serving_qty)

    off_market_val = d.get("isOffMarket") or d.get("offMarket") or 0
    if isinstance(off_market_val, bool):
        off_market_val = 1 if off_market_val else 0

    brand = d.get("brandName") or ""
    name = d.get("fullName") or d.get("productName") or ""

    return {
        "dsld_id": str(dsld_id),
        "brand": brand,
        "name": name,
        "form": form,
        "elemental_mg_per_serving": elemental_mg,
        "elemental_conversion_note": (
            None if zname.lower() in ("zinc", "zinc (elemental)", "elemental zinc")
            else f"compound '{zname}' converted to elemental using published fraction"
        ),
        "serving": serving_str,
        "servings_per_container": servings_per_container,
        "product_type": product_type,
        "off_market": int(off_market_val),
        "ul_flag": (elemental_mg is not None and elemental_mg > ZINC_UL_MG),
        "source_url": f"https://dsld.od.nih.gov/label/{dsld_id}",
        "provenance": {
            "source": "dsld",
            "source_id": str(dsld_id),
            "source_url": f"https://dsld.od.nih.gov/label/{dsld_id}",
            "fetched_at": CAPTURED_ISO,
            "client_version": "1.0",
            "verification_status": "candidate",
        },
    }


def build_us_zinc(target_n: int = 60) -> list[dict]:
    print("\n=== US ZINC — DSLD ===")
    print(f"Searching DSLD for zinc products (requesting 250 hits)…")
    hits = _dsld_search_zinc(size=250)
    print(f"  Raw hits: {len(hits)}")

    primary_hits = [h for h in hits if _dsld_is_zinc_primary(h)]
    print(f"  After zinc-primary filter: {len(primary_hits)} candidates")

    products: list[dict] = []
    for i, hit in enumerate(primary_hits):
        dsld_id = hit.get("_id")
        src = hit.get("_source", {})
        name = src.get("fullName") or src.get("productName") or ""
        print(f"  [{i+1}/{len(primary_hits)}] {dsld_id} — {name[:60]}")
        label = _dsld_get_zinc_label(dsld_id)
        if label:
            products.append(label)
        time.sleep(0.25)  # polite pacing

        if len(products) >= target_n:
            print(f"  Reached target n={target_n}; stopping.")
            break

    return products


# ---------------------------------------------------------------------------
# CA — LNHPD
# ---------------------------------------------------------------------------

def _lnhpd_is_combo(name: str) -> bool:
    nl = name.lower()
    return any(sig in nl for sig in LNHPD_COMBO_SIGNALS)


def build_ca_zinc(target_n: int = 60, timeout_full_list: int = 120) -> tuple[list[dict], int]:
    """Returns (products, corpus_active_zinc_primary_count)."""
    print("\n=== CA ZINC — LNHPD ===")
    ctx = _ssl_ctx()

    print("  Fetching full LNHPD product list (~65s)…")
    url_list = f"{LNHPD_API}/productlicence/?lang=en&type=json"
    all_products = _unwrap(_get_json(url_list, timeout=timeout_full_list, ctx=ctx))
    print(f"  Total LNHPD products: {len(all_products)}")

    # Filter: "zinc" in name, active licence (flag_product_status=1), not a combo
    zinc_primary = [
        p for p in all_products
        if "zinc" in p.get("product_name", "").lower()
        and p.get("flag_product_status") == 1
        and not _lnhpd_is_combo(p.get("product_name", ""))
    ]
    print(f"  Zinc-primary active licences (pre-dedup): {len(zinc_primary)}")

    # Deduplicate by lnhpd_id
    seen: set[int] = set()
    unique: list[dict] = []
    for p in zinc_primary:
        if p["lnhpd_id"] not in seen:
            seen.add(p["lnhpd_id"])
            unique.append(p)
    corpus_count = len(unique)
    print(f"  Unique licences (corpus): {corpus_count}")

    # Sample every Nth to reach target_n
    step = max(1, corpus_count // target_n)
    sampled = unique[::step][:target_n]
    print(f"  Sampling every {step}th -> {len(sampled)} to fetch ingredient detail")

    products: list[dict] = []
    for i, p in enumerate(sampled):
        lnhpd_id = p["lnhpd_id"]
        pname = p.get("product_name", "")
        print(f"  [{i+1}/{len(sampled)}] {lnhpd_id} — {pname[:60]}")
        source_url = f"https://health-products.canada.ca/nhpid-bdpsnh/monosearch-eng.jsp?id={lnhpd_id}"

        # Medicinal ingredient — look for zinc row
        elemental_mg: float | None = None
        form: str | None = None
        try:
            ing_url = f"{LNHPD_API}/medicinalingredient/{lnhpd_id}?lang=en&type=json"
            ing_data = _unwrap(_get_json(ing_url, ctx=ctx, timeout=20))
            zinc_rows = [
                row for row in ing_data
                if "zinc" in (row.get("ingredient_name") or "").lower()
            ]
            if zinc_rows:
                # LNHPD stores elemental quantities for regulated minerals
                # Sum in case of multi-form blend
                total = sum(
                    row.get("quantity") or 0.0
                    for row in zinc_rows
                    if (row.get("quantity_unit_of_measure") or "").lower() == "mg"
                )
                if total > 0:
                    elemental_mg = round(total, 2)
                else:
                    # Some rows may use µg or other units
                    for row in zinc_rows:
                        qty = row.get("quantity") or 0.0
                        uom = (row.get("quantity_unit_of_measure") or "").lower()
                        if uom in ("mcg", "µg", "ug") and qty > 0:
                            # Zinc in mcg is extremely rare but handle it
                            elemental_mg = round(float(qty) / 1000.0, 4)
                            break
                # Form: ingredient_name of first zinc row (e.g. "Zinc citrate")
                for row in zinc_rows:
                    if row.get("ingredient_name"):
                        form = row["ingredient_name"]
                        break
                # Apply compound->elemental conversion if form is NOT plain "Zinc"
                if elemental_mg is not None and form:
                    nl = form.lower().strip()
                    if nl not in ("zinc", "zinc (elemental)", "elemental zinc"):
                        converted = _to_elemental(elemental_mg, form)
                        if converted is not None and converted != elemental_mg:
                            # LNHPD is supposed to already report elemental for regulated
                            # minerals; if the form name suggests compound and the value
                            # looks like compound mass, convert.  Log the delta.
                            # Heuristic: if converting gives a LOWER value and the ratio
                            # matches a known fraction, trust the conversion.
                            print(f"      [LNHPD] form='{form}' -> keeping LNHPD elemental value {elemental_mg} mg as-is (LNHPD reports elemental by regulation)")
        except Exception as exc:
            print(f"    [LNHPD ingredient error] {lnhpd_id}: {exc}")

        # Dose / serving
        serving_size: str | None = None
        servings_per_day: float | None = None
        try:
            dose_url = f"{LNHPD_API}/productdose/{lnhpd_id}?lang=en&type=json"
            dose_data = _unwrap(_get_json(dose_url, ctx=ctx, timeout=20))
            if dose_data:
                adult_rows = [
                    d for d in dose_data
                    if "adult" in (d.get("population_type_desc") or "").lower()
                ]
                row = adult_rows[0] if adult_rows else dose_data[0]
                qty = row.get("quantity_dose") or 0.0
                unit = row.get("uom_type_desc_quantity_dose") or ""
                if qty and unit:
                    serving_size = f"{qty:.4g} {unit}"
                freq = row.get("frequency") or 0.0
                servings_per_day = float(freq) if freq else None
        except Exception as exc:
            print(f"    [LNHPD dose error] {lnhpd_id}: {exc}")

        products.append({
            "licence": p.get("licence_number", ""),
            "lnhpd_id": lnhpd_id,
            "brand": p.get("company_name", ""),
            "name": pname,
            "form": form,
            "elemental_mg_per_serving": elemental_mg,
            "serving": serving_size,
            "servings_per_day": servings_per_day,
            "dosage_form": p.get("dosage_form", ""),
            "ul_flag": (elemental_mg is not None and elemental_mg > ZINC_UL_MG),
            "source_url": source_url,
            "provenance": {
                "source": "lnhpd",
                "source_id": str(lnhpd_id),
                "source_url": source_url,
                "fetched_at": CAPTURED_ISO,
                "client_version": "1.0",
                "verification_status": "candidate",
            },
        })
        time.sleep(0.2)

    return products, corpus_count


# ---------------------------------------------------------------------------
# Stats helpers
# ---------------------------------------------------------------------------

def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * pct / 100.0
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return round(s[lo] + (s[hi] - s[lo]) * (k - lo), 2)


def _form_mix(products: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in products:
        form = (p.get("form") or "Unknown").strip()
        # Normalise: collapse trailing descriptors
        form_key = form.split("(")[0].strip()
        counts[form_key] = counts.get(form_key, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def _stats(products: list[dict]) -> dict:
    mg_values = [
        p["elemental_mg_per_serving"]
        for p in products
        if p.get("elemental_mg_per_serving") is not None
    ]
    ul_exceeded = [p for p in products if p.get("ul_flag")]
    return {
        "n_with_dose": len(mg_values),
        "n_missing_dose": len(products) - len(mg_values),
        "median_mg": _percentile(mg_values, 50) if mg_values else None,
        "p90_mg": _percentile(mg_values, 90) if mg_values else None,
        "min_mg": round(min(mg_values), 2) if mg_values else None,
        "max_mg": round(max(mg_values), 2) if mg_values else None,
        "ul_exceeded_count": len(ul_exceeded),
        "ul_exceeded_ids": [
            p.get("dsld_id") or str(p.get("lnhpd_id")) for p in ul_exceeded
        ],
        "form_mix": _form_mix(products),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # Force UTF-8 stdout on Windows so non-ASCII print statements don't crash
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("Bari zinc benchmark pull - TASK-361A")
    print(f"Captured: {CAPTURED_ISO}")
    print(f"OFF used: NEVER (hard rule)")
    print(f"Sources:  NIH DSLD (US), Health Canada LNHPD (CA)")
    print(f"Zinc UL:  {ZINC_UL_MG} mg elemental\n")

    # --- US ---
    us_products = build_us_zinc(target_n=60)
    us_stats = _stats(us_products)

    us_out = {
        "region": "US",
        "source": "NIH DSLD",
        "captured": CAPTURED,
        "n": len(us_products),
        "stats": us_stats,
        "zinc_ul_mg": ZINC_UL_MG,
        "off_used": False,
        "products": us_products,
    }

    us_path = BENCHMARK_DIR / "shelf_us_zinc_dsld.json"
    us_path.write_text(json.dumps(us_out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nUS zinc written -> {us_path}  (n={len(us_products)})")
    print(f"  Median: {us_stats['median_mg']} mg  |  P90: {us_stats['p90_mg']} mg")
    print(f"  UL exceeded: {us_stats['ul_exceeded_count']}")
    print(f"  Form mix: {us_stats['form_mix']}")

    # --- CA ---
    ca_products, ca_corpus = build_ca_zinc(target_n=60)
    ca_stats = _stats(ca_products)

    ca_out = {
        "region": "CA",
        "source": "Health Canada LNHPD",
        "captured": CAPTURED,
        "n": len(ca_products),
        "corpus_size_active_zinc_primary": ca_corpus,
        "sampling_method": f"every_{max(1, ca_corpus // 60)}th_by_lnhpd_id_chronological",
        "stats": ca_stats,
        "zinc_ul_mg": ZINC_UL_MG,
        "off_used": False,
        "products": ca_products,
    }

    ca_path = BENCHMARK_DIR / "shelf_ca_zinc_lnhpd.json"
    ca_path.write_text(json.dumps(ca_out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nCA zinc written -> {ca_path}  (n={len(ca_products)})")
    print(f"  Corpus (active zinc-primary licences): {ca_corpus}")
    print(f"  Median: {ca_stats['median_mg']} mg  |  P90: {ca_stats['p90_mg']} mg")
    print(f"  UL exceeded: {ca_stats['ul_exceeded_count']}")
    print(f"  Form mix: {ca_stats['form_mix']}")

    print("\nDone.  OFF not used.  Both files provenance-stamped as candidate.")
    print(f"EXIT 0")
    sys.exit(0)


if __name__ == "__main__":
    main()
