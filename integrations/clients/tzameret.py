"""Tzameret — Israeli MoH national food-composition database.

For: Nutrition Agent. The Ministry of Health's "צמרת" table is a *local-context* Israeli
composition source for generic / whole foods (raw produce, dairy basics, legumes, staples)
where OFF is sparse.

⚠️ DIRECTIONAL ONLY (owner directive 2026-06-04). Tzameret carries known data-quality
problems — some entries are questionable. It is **NOT authoritative** and must **never** be
treated as ground truth or a calibration anchor. Use it only as a *directional, local-context
hint*; when an actual composition value matters, prefer a lab-measured generic reference
(USDA FoodData Central) and/or the product's own scanned BSIP0 panel. Any tzameret-derived
value that would inform a scoring decision needs corroboration + EV-### + D7 co-sign — a
tzameret number alone is not enough.

STATUS: NEEDS-ENV-VERIFY. gov.il was SSL-blocked from the build sandbox, so neither path
below is live-confirmed here. Both are built against documented contracts — verify in
the owner's network before relying on them. Do NOT treat as verified.

Two paths, in order of dependability:
  1. load_table(path)  — RELIABLE. Tzameret is fundamentally a downloadable composition
     table. Download the official file once (CSV/TSV export), point this at it. No
     network, no endpoint guessing. This is the recommended path.
  2. ckan_search(...)  — data.gov.il exposes a CKAN datastore API
     (https://data.gov.il/api/3/action/datastore_search). The Tzameret resource_id must
     be confirmed in-env (set TZAMERET_RESOURCE_ID); the default below is a placeholder
     and will not work until verified.

Schema note: Tzameret columns are Hebrew. COLMAP maps the common ones to canonical
keys; extend it once you see the real export header (it varies by release).
"""
from __future__ import annotations

import csv
import os
from dataclasses import dataclass, field

from .http import get_json
from .provenance import Provenance, stamp

CLIENT_VERSION = "1.0"
CKAN_BASE = "https://data.gov.il/api/3/action/datastore_search"
# Placeholder — confirm the real Tzameret resource id on data.gov.il in-env.
DEFAULT_RESOURCE_ID = os.environ.get("TZAMERET_RESOURCE_ID", "")

# Real headers of the MoH "nutrition-database" per-100g export (data.gov.il), verified
# 2026-06-03 against moh_mitzrachim.csv. Columns are transliterated English; the food
# NAME column (shmmitzrach) holds Hebrew text. Values are per 100g edible portion.
COLMAP = {
    "shmmitzrach": "name",          # שם מצרך — Hebrew food name
    "smlmitzrach": "code",          # סמל מצרך — official food number
    "food_energy": "energy_kcal",
    "protein": "protein_g",
    "total_fat": "fat_g",
    "carbohydrates": "carb_g",
    "total_dietary_fiber": "fiber_g",
    "sodium": "sodium_mg",
    "total_sugars": "sugar_g",      # present in some releases
    "saturated_fat": "satfat_g",
    "calcium": "calcium_mg",
    "iron": "iron_mg",
    "cholesterol": "cholesterol_mg",
}


@dataclass
class FoodComposition:
    code: str | None
    name: str
    per: str = "100g"
    values: dict[str, float] = field(default_factory=dict)
    provenance: Provenance | None = None  # MoH authoritative-generic — not the SKU panel
    raw: dict = field(default_factory=dict)


def _coerce(row: dict) -> FoodComposition:
    canon: dict[str, float] = {}
    name = ""
    code = None
    for k, v in row.items():
        key = COLMAP.get((k or "").strip())
        if key == "name":
            name = (v or "").strip()
        elif key == "code":
            code = (v or "").strip() or None
        elif key:
            try:
                canon[key] = float(str(v).replace(",", "").strip())
            except (ValueError, AttributeError):
                pass
    return FoodComposition(code=code, name=name, values=canon, raw=row)


def load_table(path: str, encoding: str = "utf-8-sig") -> list[FoodComposition]:
    """RELIABLE path: load a locally-downloaded Tzameret CSV/TSV export."""
    delim = "\t" if path.lower().endswith((".tsv", ".tab")) else ","
    out: list[FoodComposition] = []
    with open(path, encoding=encoding, newline="") as f:
        for row in csv.DictReader(f, delimiter=delim):
            fc = _coerce(row)
            if fc.name:
                fc.provenance = stamp("tzameret", fc.code, path, CLIENT_VERSION)
                out.append(fc)
    return out


def ckan_search(query: str, resource_id: str | None = None, limit: int = 20) -> list[FoodComposition]:
    """FLAGGED path: query data.gov.il CKAN. Requires a verified resource_id in-env."""
    rid = resource_id or DEFAULT_RESOURCE_ID
    if not rid:
        raise RuntimeError(
            "Tzameret CKAN resource_id not set. Confirm it on data.gov.il and set "
            "TZAMERET_RESOURCE_ID, or use load_table() with a downloaded export."
        )
    data = get_json(CKAN_BASE, params={"resource_id": rid, "q": query, "limit": limit})
    records = data.get("result", {}).get("records", [])
    out = []
    for r in records:
        fc = _coerce(r)
        fc.provenance = stamp("tzameret", fc.code, f"{CKAN_BASE}?resource_id={rid}",
                              CLIENT_VERSION)
        out.append(fc)
    return out


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Hebrew-safe on Windows
    print("Tzameret client — NEEDS-ENV-VERIFY (gov.il SSL-blocked in build sandbox).")
    print("Reliable path: download the official MoH צמרת export, then:")
    print('  from integrations.clients.tzameret import load_table')
    print('  foods = load_table(r"C:\\\\Bari\\\\integrations\\\\data\\\\tzameret.csv")')
    if DEFAULT_RESOURCE_ID:
        try:
            res = ckan_search("חלב", limit=2)
            print(f"CKAN live: {len(res)} records; first={res[0].name if res else None}")
        except Exception as e:  # noqa: BLE001
            print(f"CKAN attempt failed (expected until verified): {type(e).__name__}: {e}")
