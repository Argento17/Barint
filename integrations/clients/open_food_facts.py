"""Open Food Facts client — DISABLED (PROJECT-WIDE BAN, TASK-238 / TASK-242).

This client is permanently disabled. Per the owner hard rule (CLAUDE.md "Hard rules",
reconfirmed 2026-06-10) Open Food Facts is BANNED as a Bari data source — nutrition,
ingredients, names, barcodes, images, serving sizes, category, fallback, enrichment,
validation, "temporary" fills, comparison JSON, frontend display, generated copy, scoring
traces, and confidence — anywhere, any field, any category, forever. "Unknown is
acceptable; OFF is not." Any OFF dependency is a launch blocker.

Every public entry point raises `OffDisabledError` on call. The implementation below is
retained only so the disable is auditable and so re-enabling requires a deliberate, written
owner policy change — NOT to be invoked. Do not remove the guard.

Docs (historical): https://openfoodfacts.github.io/openfoodfacts-server/api/
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .http import HttpError, get_json
from .provenance import Provenance, stamp

CLIENT_VERSION = "1.0-disabled"
API = "https://world.openfoodfacts.org/api/v2"

# PROJECT-WIDE OFF BAN (TASK-238 / TASK-242). Flip ONLY via a written owner policy change.
OFF_DISABLED = True


class OffDisabledError(RuntimeError):
    """Raised on any attempt to use the Open Food Facts client (banned data source)."""


def _enforce_off_ban() -> None:
    if OFF_DISABLED:
        raise OffDisabledError(
            "Open Food Facts is a banned Bari data source (CLAUDE.md hard rule, "
            "TASK-238). This client is permanently disabled. Unknown is acceptable; "
            "OFF is not."
        )
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
    """DISABLED — raises OffDisabledError. (Historically: fetch one product by barcode.)"""
    _enforce_off_ban()
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
    """DISABLED — raises OffDisabledError. (Historically: fetch many barcodes.)"""
    _enforce_off_ban()
    return {bc: get_product(bc, timeout=timeout) for bc in barcodes}


if __name__ == "__main__":
    # Live smoke test — a well-known Israeli barcode (Tnuva / Coca-Cola IL vary; use a
    # globally-present one so the test is stable regardless of IL coverage).
    for bc in ("737628064502", "3017620422003"):  # Thai Kitchen, Nutella
        p = get_product(bc)
        print(f"{bc}: found={p.found} name={p.name!r} nova={p.nova_group} "
              f"panel={p.has_panel} kcal={p.nutriments.get('energy-kcal_100g')} "
              f"image={'yes' if p.image_url else 'no'}")
