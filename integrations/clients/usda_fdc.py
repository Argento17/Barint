"""USDA FoodData Central — global nutrient composition (USDA ARS).

For: Nutrition + Data Agents. The most comprehensive free nutrient database in the
world (~600k entries: Foundation Foods, SR Legacy, Survey/FNDDS, Branded). It is the
standard enrichment fallback when a product label is incomplete and when Tzameret has
no entry for a generic ingredient — exactly the "micro + bioactive" depth OFF lacks.

Position in the source hierarchy: USDA FDC is the lab-measured *authoritative-generic*
reference — prefer it for actual composition values (breadth, micronutrients, bioactives).
Tzameret is **directional only** (owner directive 2026-06-04 — known data-quality issues;
NOT authoritative), useful for Israeli local context but never as the value of record.
Like every external source FDC is a CANDIDATE — it calibrates/justifies (with an
evidence-registry citation); the engine still reads the in-house BSIP0 panel. Never
substitutes a SKU's scanned panel.

Auth: a free api.data.gov key (FDC_API_KEY). Falls back to DEMO_KEY (low rate limit,
fine for smoke tests). Get a key: https://fdc.nal.usda.gov/api-key-signup.html
Docs: https://fdc.nal.usda.gov/api-guide.html
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from .http import HttpError, get_json
from .provenance import Provenance, stamp

CLIENT_VERSION = "1.0"
API = "https://api.nal.usda.gov/fdc/v1"

# USDA nutrient numbers are stable across releases — map to Bari's canonical per-100g keys
# (the same keys tzameret.COLMAP emits, so downstream code treats both sources alike).
NUTRIENT_MAP = {
    "208": "energy_kcal",
    "203": "protein_g",
    "204": "fat_g",
    "205": "carb_g",
    "291": "fiber_g",
    "307": "sodium_mg",
    "269": "sugar_g",
    "606": "satfat_g",
    "601": "cholesterol_mg",
    "301": "calcium_mg",
    "303": "iron_mg",
    "306": "potassium_mg",
    "605": "transfat_g",
}


def _api_key() -> str:
    return os.environ.get("FDC_API_KEY", "DEMO_KEY")


@dataclass
class FoodHit:
    fdc_id: int
    description: str
    data_type: str | None = None          # Foundation | SR Legacy | Branded | Survey (FNDDS)
    brand_owner: str | None = None
    gtin_upc: str | None = None           # barcode, when Branded — bridges to a SKU


@dataclass
class Food:
    fdc_id: int | None
    description: str
    data_type: str | None = None
    per: str = "100g"
    values: dict[str, float] = field(default_factory=dict)   # canonical keys, per 100g
    gtin_upc: str | None = None
    found: bool = True
    provenance: Provenance | None = None
    raw: dict = field(default_factory=dict)


def search(query: str, page_size: int = 10, data_type: list[str] | None = None) -> list[FoodHit]:
    """Search FDC. data_type filters to e.g. ['Foundation','SR Legacy'] for generic
    composition (recommended for ingredient enrichment) vs ['Branded'] for SKUs."""
    params = {"query": query, "pageSize": page_size, "api_key": _api_key()}
    if data_type:
        params["dataType"] = ",".join(data_type)
    data = get_json(f"{API}/foods/search", params=params)
    out: list[FoodHit] = []
    for f in data.get("foods", []):
        out.append(FoodHit(
            fdc_id=f.get("fdcId"),
            description=(f.get("description") or "").strip(),
            data_type=f.get("dataType"),
            brand_owner=f.get("brandOwner"),
            gtin_upc=f.get("gtinUpc"),
        ))
    return out


def get_food(fdc_id: int | str) -> Food:
    """Fetch one food's full nutrient panel, normalized to canonical per-100g keys.
    Foundation/SR Legacy are per 100g; Branded report per serving + per 100g where
    available — we read the 100g basis to stay comparable."""
    url = f"{API}/food/{fdc_id}"
    prov = stamp("usda_fdc", str(fdc_id), url, CLIENT_VERSION)
    try:
        data = get_json(url, params={"api_key": _api_key()})
    except HttpError as e:
        if e.status == 404:
            return Food(fdc_id=None, description="", found=False, provenance=prov)
        raise
    values: dict[str, float] = {}
    for fn in data.get("foodNutrients", []):
        nutr = fn.get("nutrient") or {}
        num = str(nutr.get("number") or "")
        key = NUTRIENT_MAP.get(num)
        if not key:
            continue
        amount = fn.get("amount")
        if amount is None:
            continue
        try:
            values[key] = float(amount)
        except (TypeError, ValueError):
            pass
    return Food(
        fdc_id=data.get("fdcId"),
        description=(data.get("description") or "").strip(),
        data_type=data.get("dataType"),
        values=values,
        gtin_upc=data.get("gtinUpc"),
        provenance=prov,
        raw={k: data.get(k) for k in ("fdcId", "description", "dataType", "publicationDate")},
    )


def lookup(query: str, prefer_generic: bool = True) -> Food | None:
    """Convenience: best-match composition for a generic ingredient name. Prefers
    Foundation/SR Legacy (generic, lab-measured) over Branded when prefer_generic."""
    dt = ["Foundation", "SR Legacy"] if prefer_generic else None
    hits = search(query, page_size=5, data_type=dt)
    if not hits and prefer_generic:
        hits = search(query, page_size=5)
    if not hits:
        return None
    return get_food(hits[0].fdc_id)


if __name__ == "__main__":
    key_state = "FDC_API_KEY set" if os.environ.get("FDC_API_KEY") else "DEMO_KEY (rate-limited)"
    print(f"USDA FoodData Central — {key_state}")
    for q in ("cheddar cheese", "lentils raw", "tahini"):
        f = lookup(q)
        if f and f.found:
            print(f"  {q}: fdc={f.fdc_id} [{f.data_type}] "
                  f"kcal={f.values.get('energy_kcal')} protein={f.values.get('protein_g')} "
                  f"fiber={f.values.get('fiber_g')} calcium={f.values.get('calcium_mg')}")
        else:
            print(f"  {q}: no match (or rate-limited on DEMO_KEY)")
