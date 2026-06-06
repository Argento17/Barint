"""Open Food Facts client — product nutrition + ingredients by barcode.

For: Data Agent (corpus enrichment) and Nutrition Agent (panel ground-truth).
Pairs with il_prices: the price feed yields the barcode, OFF yields the panel.

OFF is a free, no-auth, community database. Coverage of Israeli branded products is
partial — always treat a miss as "not found", never as "no such product". OFF data is
crowd-sourced; for scoring, prefer it as a *candidate* panel to be QA-gated, not as a
sealed source of truth.

Docs: https://openfoodfacts.github.io/openfoodfacts-server/api/
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .http import HttpError, get_json
from .provenance import Provenance, stamp

CLIENT_VERSION = "1.0"
API = "https://world.openfoodfacts.org/api/v2"
# Fields we actually consume — keeps payloads small and intent explicit.
FIELDS = (
    "code,product_name,product_name_he,brands,quantity,nutriments,"
    "ingredients_text,ingredients_text_he,nova_group,nutriscore_grade,"
    "additives_tags,labels_tags,categories_tags,countries_tags,completeness,"
    "image_url,image_front_url,image_front_small_url"
)


@dataclass
class OffProduct:
    barcode: str
    found: bool
    name: str | None = None
    brand: str | None = None
    quantity: str | None = None
    nova_group: int | None = None
    nutriscore: str | None = None
    ingredients_text: str | None = None
    nutriments: dict[str, Any] = field(default_factory=dict)
    additives: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    completeness: float | None = None
    image_url: str | None = None          # front-of-pack image (frontend imagery req.)
    image_small_url: str | None = None
    provenance: Provenance | None = None  # source/fetch stamp — candidate until QA-gated
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def has_panel(self) -> bool:
        """True when at least core macros are present (worth scoring)."""
        n = self.nutriments
        return bool(n) and any(
            k in n for k in ("energy-kcal_100g", "proteins_100g", "fat_100g")
        )


def _pick_name(p: dict[str, Any]) -> str | None:
    return p.get("product_name_he") or p.get("product_name") or None


def _pick_ingredients(p: dict[str, Any]) -> str | None:
    return p.get("ingredients_text_he") or p.get("ingredients_text") or None


def get_product(barcode: str, timeout: int = 25) -> OffProduct:
    """Fetch one product by barcode. Never raises on 'not found' — returns found=False."""
    barcode = str(barcode).strip()
    url = f"{API}/product/{barcode}.json"
    prov = stamp("open_food_facts", barcode, url, CLIENT_VERSION)
    try:
        data = get_json(url, params={"fields": FIELDS}, timeout=timeout)
    except HttpError as e:
        if e.status == 404:
            return OffProduct(barcode=barcode, found=False, provenance=prov)
        raise
    if data.get("status") != 1 or "product" not in data:
        return OffProduct(barcode=barcode, found=False, provenance=prov)
    p = data["product"]
    return OffProduct(
        barcode=barcode,
        found=True,
        name=_pick_name(p),
        brand=(p.get("brands") or None),
        quantity=(p.get("quantity") or None),
        nova_group=p.get("nova_group"),
        nutriscore=(p.get("nutriscore_grade") or None),
        ingredients_text=_pick_ingredients(p),
        nutriments=p.get("nutriments", {}) or {},
        additives=p.get("additives_tags", []) or [],
        labels=p.get("labels_tags", []) or [],
        completeness=p.get("completeness"),
        image_url=(p.get("image_front_url") or p.get("image_url") or None),
        image_small_url=(p.get("image_front_small_url") or None),
        provenance=prov,
        raw=p,
    )


def get_products(barcodes: list[str], timeout: int = 25) -> dict[str, OffProduct]:
    """Fetch many barcodes sequentially. Returns {barcode: OffProduct}."""
    return {bc: get_product(bc, timeout=timeout) for bc in barcodes}


if __name__ == "__main__":
    # Live smoke test — a well-known Israeli barcode (Tnuva / Coca-Cola IL vary; use a
    # globally-present one so the test is stable regardless of IL coverage).
    for bc in ("737628064502", "3017620422003"):  # Thai Kitchen, Nutella
        p = get_product(bc)
        print(f"{bc}: found={p.found} name={p.name!r} nova={p.nova_group} "
              f"panel={p.has_panel} kcal={p.nutriments.get('energy-kcal_100g')} "
              f"image={'yes' if p.image_url else 'no'}")
