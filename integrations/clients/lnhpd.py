"""Health Canada LNHPD — Licensed Natural Health Products Database.

For: supplement corpus worldwide benchmark (TASK-361). Read-only client; pulls
magnesium-primary NHP licences with elemental dose and form from the Health Canada
open API.

API: https://health-products.canada.ca/api/natural-licences/
Endpoints used:
  /productlicence/         — full product list (301k rows, ~65s; cached after first call)
  /medicinalingredient/{id} — structured ingredient rows per licence
  /productdose/{id}         — dose/serving info per licence

SSL: the certifi CA bundle is required. Do NOT disable verification. Set the
`CA_BUNDLE` constant or the REQUESTS_CA_BUNDLE env var if certifi is unavailable.

Provenance: all records born "candidate"; only BSIP0/QA promotes to "verified".
OFF is not used here — data is sourced exclusively from Health Canada LNHPD.
"""
from __future__ import annotations

import json
import os
import ssl
import time
import urllib.request
from dataclasses import dataclass, field

CLIENT_VERSION = "1.0"
API = "https://health-products.canada.ca/api/natural-licences"
USER_AGENT = "Bari/1.0 (+nutrition-scoring; contact tbarhaim@gmail.com)"

# Certifi CA bundle — required; never set to False
try:
    import certifi
    _DEFAULT_CAFILE = certifi.where()
except ImportError:
    _DEFAULT_CAFILE = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")

# Signals that identify multi-mineral combos where magnesium is incidental.
# Products whose names contain ANY of these are excluded from "magnesium-primary".
_COMBO_SIGNALS = [
    "calcium", "vitamin", "zinc", "multi", "mineral", "iron",
    "phosphorus", "potassium", "selenium", "chromium", "manganese",
    "copper", "boron", "iodine", "magnesium d", "mg d",
]


def _ssl_context(cafile: str | None = None) -> ssl.SSLContext:
    """Return a verified SSL context using the certifi bundle."""
    cf = cafile or _DEFAULT_CAFILE
    if not cf:
        raise RuntimeError(
            "SSL CA bundle not found. Install certifi (`pip install certifi`) "
            "or set SSL_CERT_FILE / REQUESTS_CA_BUNDLE to the path of a CA bundle. "
            "Do NOT disable certificate verification."
        )
    ctx = ssl.create_default_context(cafile=cf)
    return ctx


def _get_json(url: str, ctx: ssl.SSLContext, timeout: int = 30) -> object:
    """Simple GET with retry on 429/5xx, returns parsed JSON."""
    for attempt in range(3):
        req = urllib.request.Request(
            url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=timeout) as r:
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


def _unwrap(data: object) -> list:
    """Handle both paginated ({metadata, data: [...]}) and plain-list responses."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("data", [])
    return []


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

@dataclass
class LNHPDProduct:
    """One LNHPD licence with magnesium ingredient data."""
    licence: str
    lnhpd_id: int
    brand: str
    name: str
    dosage_form: str
    # ingredient
    elemental_mg_per_serving: float | None  # elemental Mg in mg; already elemental from API
    form: str | None                         # e.g. "Magnesium citrate", "Magnesium bisglycinate"
    # dose
    serving_size: str | None   # e.g. "3 capsule"
    servings_per_day: float | None
    source_url: str
    provenance: dict = field(default_factory=dict)


def list_magnesium_products(
    cafile: str | None = None,
    timeout_full_list: int = 120,
) -> list[LNHPDProduct]:
    """
    Fetch magnesium-primary NHP licences from LNHPD.

    "Magnesium-primary" means the product name contains "magnesium" AND does NOT
    contain multi-mineral combo signals (calcium, zinc, vitamin, etc.).  Duplicate
    lnhpd_ids (one product, multiple registered names) are deduplicated by keeping
    the first occurrence.

    Returns a list of LNHPDProduct with elemental_mg_per_serving populated where
    the API provides an ingredient row with ingredient_name="Magnesium".  Products
    where the dose is not determinable are still included with that field as None —
    callers can filter them out.

    SSL: uses certifi CA bundle.  Never disables verification.
    """
    ctx = _ssl_context(cafile)
    fetched_at = _now_iso()

    # 1. Pull full product list (~65s; 301k products)
    url_list = f"{API}/productlicence/?lang=en&type=json"
    all_products = _unwrap(
        _get_json(url_list, ctx, timeout=timeout_full_list)
    )

    # 2. Filter: "magnesium" in name, active licence (flag_product_status=1), not a combo
    def _is_combo(name: str) -> bool:
        nl = name.lower()
        return any(sig in nl for sig in _COMBO_SIGNALS)

    mg_primary = [
        p for p in all_products
        if "magnesium" in p.get("product_name", "").lower()
        and p.get("flag_product_status") == 1
        and not _is_combo(p.get("product_name", ""))
    ]

    # 3. Deduplicate by lnhpd_id
    seen: set[int] = set()
    unique: list[dict] = []
    for p in mg_primary:
        if p["lnhpd_id"] not in seen:
            seen.add(p["lnhpd_id"])
            unique.append(p)

    # 4. Per-product: fetch medicinal ingredient + dose
    results: list[LNHPDProduct] = []
    for p in unique:
        lnhpd_id = p["lnhpd_id"]
        source_url = f"https://health-products.canada.ca/nhpid-bdpsnh/monosearch-eng.jsp?id={lnhpd_id}"

        # Medicinal ingredient
        elemental_mg: float | None = None
        form: str | None = None
        try:
            ing_url = f"{API}/medicinalingredient/{lnhpd_id}?lang=en&type=json"
            ing_data = _unwrap(_get_json(ing_url, ctx, timeout=20))
            mg_rows = [
                row for row in ing_data
                if "magnesium" in row.get("ingredient_name", "").lower()
            ]
            if mg_rows:
                # Sum elemental Mg across all magnesium rows (multi-form blends)
                total = sum(
                    row.get("quantity") or 0.0 for row in mg_rows
                    if row.get("quantity_unit_of_measure", "").lower() == "mg"
                )
                elemental_mg = total if total > 0 else None
                # Form: prefer the source_material of the first row with a non-empty value
                for row in mg_rows:
                    if row.get("source_material"):
                        form = row["source_material"]
                        break
        except Exception:
            pass

        # Dose / serving
        serving_size: str | None = None
        servings_per_day: float | None = None
        try:
            dose_url = f"{API}/productdose/{lnhpd_id}?lang=en&type=json"
            dose_data = _unwrap(_get_json(dose_url, ctx, timeout=20))
            if dose_data:
                # Pick the Adults row (or first if none labelled Adults)
                adult_rows = [d for d in dose_data if "adult" in (d.get("population_type_desc") or "").lower()]
                row = adult_rows[0] if adult_rows else dose_data[0]
                qty = row.get("quantity_dose") or 0.0
                unit = row.get("uom_type_desc_quantity_dose") or ""
                if qty > 0 and unit:
                    serving_size = f"{qty:.4g} {unit}"
                freq = row.get("frequency") or 0.0
                servings_per_day = float(freq) if freq > 0 else None
        except Exception:
            pass

        results.append(LNHPDProduct(
            licence=p.get("licence_number", ""),
            lnhpd_id=lnhpd_id,
            brand=p.get("company_name", ""),
            name=p.get("product_name", ""),
            dosage_form=p.get("dosage_form", ""),
            elemental_mg_per_serving=round(elemental_mg, 2) if elemental_mg is not None else None,
            form=form,
            serving_size=serving_size,
            servings_per_day=servings_per_day,
            source_url=source_url,
            provenance={
                "source": "lnhpd",
                "source_id": str(lnhpd_id),
                "source_url": source_url,
                "fetched_at": fetched_at,
                "client_version": CLIENT_VERSION,
                "verification_status": "candidate",
            },
        ))
        time.sleep(0.2)  # polite pacing

    return results


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    print("Fetching LNHPD magnesium-primary product list (may take ~2–3 min)…")
    products = list_magnesium_products()
    print(f"Done. {len(products)} magnesium-primary NHP licences.")
    for p in products[:5]:
        print(f"  [{p.lnhpd_id}] {p.name} | {p.form} | {p.elemental_mg_per_serving} mg | {p.serving_size}")
