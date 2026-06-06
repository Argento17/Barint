"""DSLD — NIH Dietary Supplement Label Database.

For: Nutrition Agent (supplement scoring logic) and Data Agent (supplement corpus). The
single largest data gap in pass 1: Bari scores supplements but had no structured source
for what's actually in them. DSLD provides ~150k+ supplement labels with structured
ingredient rows — name, quantity, unit, serving size, daily-value target group.

Free, no auth. US database — use it as authoritative for *generic actives and dose
ranges* (creatine 1.5g/serving, etc.), not as a catalog of Israeli SKUs. Pair with the
Research Agent's `literature` client to tier the evidence behind an active.

Docs: https://dsld.od.nih.gov/api-guide
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .http import get_json
from .provenance import Provenance, stamp

CLIENT_VERSION = "1.0"
API = "https://api.ods.od.nih.gov/dsld"


@dataclass
class SupplementIngredient:
    name: str
    quantity: float | None = None
    unit: str | None = None
    per_serving: str | None = None
    dv_percent: float | None = None


@dataclass
class SupplementLabel:
    dsld_id: str
    name: str
    brand: str | None = None
    serving_size: str | None = None
    ingredients: list[SupplementIngredient] = field(default_factory=list)
    provenance: Provenance | None = None  # US reference data — generic actives/doses only
    raw: dict = field(default_factory=dict)


def search(query: str, size: int = 10) -> list[dict]:
    """Search labels. Returns lightweight hits (id + name); fetch detail with get_label."""
    data = get_json(f"{API}/v9/search-filter", params={"q": query, "size": size})
    out = []
    for h in data.get("hits", []):
        src = h.get("_source", {})
        out.append({
            "dsld_id": h.get("_id"),
            "name": src.get("fullName") or src.get("productName"),
            "brand": src.get("brandName"),
        })
    return out


def _coerce_ingredients(rows: list[dict]) -> list[SupplementIngredient]:
    out: list[SupplementIngredient] = []
    for row in rows:
        name = row.get("name") or row.get("ingredientName") or ""
        qlist = row.get("quantity") or []
        q = qlist[0] if isinstance(qlist, list) and qlist else (
            qlist if isinstance(qlist, dict) else {})
        dv = None
        for tg in (q.get("dailyValueTargetGroup") or []):
            if tg.get("percent") is not None:
                dv = tg["percent"]; break
        out.append(SupplementIngredient(
            name=name,
            quantity=q.get("quantity"),
            unit=q.get("unit"),
            per_serving=(f"{q.get('servingSizeQuantity')} {q.get('servingSizeUnit')}".strip()
                         if q.get("servingSizeQuantity") else None),
            dv_percent=dv,
        ))
    return out


def get_label(dsld_id: str) -> SupplementLabel:
    """Fetch one full label with structured ingredient rows."""
    url = f"{API}/v9/label/{dsld_id}"
    d = get_json(url)
    rows = d.get("ingredientRows") or d.get("ingredients") or []
    return SupplementLabel(
        dsld_id=str(dsld_id),
        name=d.get("fullName") or d.get("productName") or "",
        brand=d.get("brandName"),
        serving_size=d.get("servingSizes", [{}])[0].get("minQuantity")
        if d.get("servingSizes") else None,
        ingredients=_coerce_ingredients(rows),
        provenance=stamp("dsld", str(dsld_id), url, CLIENT_VERSION),
        raw=d,
    )


if __name__ == "__main__":
    hits = search("creatine", size=3)
    print(f"search 'creatine': {len(hits)} hits")
    for h in hits:
        print(f"  [{h['dsld_id']}] {h['name']} — {h['brand']}")
    if hits:
        label = get_label(hits[0]["dsld_id"])
        print(f"label {label.dsld_id}: {label.name}")
        for ing in label.ingredients[:5]:
            print(f"  - {ing.name}: {ing.quantity} {ing.unit} per {ing.per_serving}")
