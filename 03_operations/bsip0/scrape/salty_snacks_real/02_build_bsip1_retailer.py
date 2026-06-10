"""
BSIP1 — Salty snacks REAL retailer-panel build (TASK-237).

REPLACES 02_build_bsip1.py (which consumed OFF). NO Open Food Facts.

Reads the retailer BSIP0 (bsip0_salty_snacks_retailer_raw.json — real Yochananof
product-modal nutrition + Hebrew ingredients) and emits one BSIP1 v0.1 product JSON per
product into 02_products/salty_snacks/bsip1_outputs/ (the dir the BSIP2 batch runner reads).

No curation/dedup: the 38-product identity set is already fixed (TASK-228). A product
whose retailer page genuinely lacks BOTH nutrition and ingredients is DROPPED (cannot be
scored); a product with a panel but no ingredients is kept as panel-only.

panel_source = retailer_product_page (yochananof). Trans "<0.5"/"L 0.5" declarations are
carried as fat_trans_g == 0.5 so the engine's existing threshold_declaration convention
(== 0.5 → no penalty) handles them natively. No manual data_corrections.
"""
import sys, json, re, pathlib
from datetime import datetime, timezone
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BSIP0 = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip0_outputs\bsip0_salty_snacks_retailer_raw.json")
# Authoritative real Yochananof product images (HTTP-200, EAN-keyed), already verified for
# the fixed 38-product identity set. Images were NEVER an OFF datum — they came from the
# Yochananof catalog harvest — so reusing this EAN->image map preserves the real images
# while the OFF NUTRITION/INGREDIENTS are fully replaced by retailer-panel values.
IMG_SOURCE = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip0_outputs\bsip0_salty_snacks_real_raw.json")
OUT_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")


def load_image_map() -> dict:
    d = json.loads(IMG_SOURCE.read_text(encoding="utf-8"))
    return {p["barcode"]: p.get("image_url") for p in d.get("products", []) if p.get("image_url")}


def clean_ing_list(text: str) -> list:
    if not text:
        return []
    # split on commas/semicolons and Hebrew " ו" conjunction before a Hebrew word
    parts = re.split(r"[,;]| ו(?=[א-ת])", text)
    out = []
    for p in parts:
        p = p.strip(" .")
        if p and len(p) > 1:
            out.append(p)
    return out[:30]


def basis_error(nn: dict) -> bool:
    """Detect a whole-panel per-SERVING basis mislabeled as per-100g.

    Dry salty snacks (crackers, rice cakes, pretzels, crisps, popcorn) run ~350-540
    kcal/100g. A panel declaring "ל100 גרם" but reporting < 200 kcal whose macros
    Atwater-reproduce that low kcal (carbs*4 + fat*9 + protein*4 ~= stated kcal) is a
    per-serving panel mislabeled per-100g — every macro is scaled together, so it is
    self-consistent but on the wrong basis and UNRECOVERABLE (the page exposes no numeric
    serving size). Publishing it per-100g distorts cross-product comparison (it looks far
    lighter than a correctly-per-100g sibling). Same defect class as TASK-234 BASIS_ERROR.
    Honest action: DROP, never rescale-guess, never backfill from OFF. Surfaced for re-QA."""
    e = nn.get("energy_kcal")
    if e is None or e >= 200:
        return False
    c = nn.get("carbohydrates_g") or 0
    fa = nn.get("fat_g") or 0
    pr = nn.get("protein_g") or 0
    atwater = c * 4 + fa * 9 + pr * 4
    if atwater <= 0:
        return False
    ratio = atwater / e
    # macros reproduce the low kcal (consistent panel) -> the whole panel is per-serving
    return 0.75 <= ratio <= 1.3


def has_core_macros(nn: dict) -> bool:
    """Scoreable if the calorie-density + sodium drivers are present. Energy + carbs +
    sodium are the load-bearing salty-snack signals; total fat may be absent on a
    near-fat-free panel (sat-fat present instead), and protein is a secondary field —
    a real retailer panel that omits one of those is still scoreable. Only a panel with
    NO nutrition at all (the Calbee import) is dropped. We never backfill from OFF."""
    return nn.get("energy_kcal") is not None \
        and nn.get("carbohydrates_g") is not None \
        and nn.get("sodium_mg") is not None \
        and (nn.get("fat_g") is not None or nn.get("fat_saturated_g") is not None)


def main():
    d = json.loads(BSIP0.read_text(encoding="utf-8"))
    products = d["products"]
    img_map = load_image_map()

    # wipe + rebuild bsip1 dir (remove ALL prior OFF-era records)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for f in OUT_DIR.glob("bsip1_snack_*.json"):
        f.unlink()
    # also clear the FABRICATED backup pollution from the live dir if present
    for f in OUT_DIR.glob("*.json"):
        f.unlink()

    now = datetime.now(timezone.utc).isoformat()
    written, dropped, panel_only = 0, [], []

    for p in products:
        ean = p["barcode"]
        nn = p.get("normalized_nutrition_per_100g") or {}
        ing_text = (p.get("ingredients_text_he") or "").strip()
        prov = p.get("nutrition_provenance") or {}
        thr = prov.get("threshold_declared") or {}
        # Panel source is carried THROUGH from BSIP0 so a TASK-241 Shufersal-rescued
        # product is honestly stamped shufersal_product_page (not the default Yochananof).
        panel_src = p.get("panel_source") or "retailer_product_page"
        panel_retailer = p.get("retailer") or "yochananof"

        # DROP if no scoreable panel (cannot score without core macros)
        if not has_core_macros(nn):
            dropped.append({"barcode": ean, "name": p["name_he"], "drop_class": "no_panel",
                            "reason": "retailer page has no nutrition panel (and no ingredients); "
                                      "not scoreable; NOT backfilled from OFF"})
            continue

        # DROP if the retailer panel is per-serving mislabeled per-100g (unrecoverable basis)
        if basis_error(nn):
            dropped.append({"barcode": ean, "name": p["name_he"], "drop_class": "basis_error",
                            "energy_kcal": nn.get("energy_kcal"),
                            "reason": "retailer page declares 'ל100 גרם' but the whole panel is on a "
                                      "per-serving basis (kcal<200, Atwater-consistent); unrecoverable "
                                      "(no numeric serving size); publishing per-100g distorts the shelf. "
                                      "Dropped per TASK-234 basis-error precedent; NOT backfilled from OFF"})
            continue

        # Real Yochananof image: prefer the authoritative EAN-keyed map; fall back to
        # whatever the scraper captured. Never empty when the map has it.
        image_url = img_map.get(ean) or p.get("image_url") or ""

        ing_list = clean_ing_list(ing_text)
        has_ing = bool(ing_text) and len(ing_list) >= 1
        if not has_ing:
            panel_only.append(ean)

        suf = "sufficient" if has_ing else "partial"
        pid = f"bsip1_snack_{ean}"
        rec = {
            "schema_version": "bsip1_v0_1",
            "file_type": "product",
            "canonical_product_id": pid,
            "barcode": ean,
            "canonical_name_he": p["name_he"],
            "canonical_name_en": "",
            "brand": p.get("brand") or "",
            "package_size_g": None,
            "source_retailers": [panel_retailer],
            "sub_pool": p["sub_pool"],
            "category": "salty_snack",
            "image_url": image_url,
            "image_urls": [image_url] if image_url else [],
            "price_ils": None,
            "normalized_nutrition_per_100g": {
                "energy_kcal": nn.get("energy_kcal"),
                "fat_g": nn.get("fat_g"),
                "fat_saturated_g": nn.get("fat_saturated_g"),
                "fat_trans_g": nn.get("fat_trans_g"),
                "sodium_mg": nn.get("sodium_mg"),
                "carbohydrates_g": nn.get("carbohydrates_g"),
                "sugars_g": nn.get("sugars_g"),
                "dietary_fiber_g": nn.get("dietary_fiber_g"),
                "protein_g": nn.get("protein_g"),
            },
            "ingredients_text_he": ing_text,
            "ingredients_list": ing_list,
            "ingredients_raw": ing_text,
            "ingredient_count": len(ing_list),
            "claims_raw": "",
            "claims": [],
            # NOVA: inferred by the engine's nova_proxy from the real ingredient list.
            # No OFF nova_group is injected. Panel-only products get a low-confidence proxy.
            "nova_proxy": None,
            "nova_confidence": None,
            "additive_categories": [],
            "additive_count": 0,
            "allergens_contains": [],
            "allergens_may_contain": [],
            "data_sufficiency": suf,
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": "consistent",
            "ingredient_text_quality": "clean" if has_ing else "absent",
            "canonical_trust_score": 0.85 if has_ing else 0.7,
            "canonical_trust_level": "high" if has_ing else "medium",
            "canonical_risk_flags": [] if has_ing else ["ingredients_unavailable"],
            "confidence": {
                "identity_confidence": "high",
                "barcode_confidence": "confirmed",
                "nutrition_confidence": "confirmed_per_100g",
                "matched_by": (
                    "yochananof_catalog_real_ean + shufersal_product_page_panel (gtin13_exact, TASK-241)"
                    if panel_src == "shufersal_product_page"
                    else "yochananof_catalog_real_ean + retailer_product_page_panel"
                ),
                "observation_count": 1,
            },
            "conflicts_summary": [],
            "missing_fields": [] if has_ing else ["ingredients_text_he"],
            "inferred_fields": [],
            "audit_ref": None,
            "enrichment_run_id": "run_salty_snacks_bsip1_retailer_001",
            "enriched_at": now,
            "panel_provenance": {
                "panel_source": panel_src,
                "retailer": panel_retailer,
                "acquisition": ("shufersal_product_page (name-search, gtin13_exact identity match, TASK-241)"
                                if panel_src == "shufersal_product_page"
                                else "yochananof_storefront_product_modal"),
                "trans_threshold_declared": list(thr.keys()),
                "raw_rows": prov.get("raw_rows"),
                "shufersal_product_code": prov.get("shufersal_product_code"),
                "shufersal_product_url": prov.get("shufersal_product_url"),
                "no_off": True,
            },
            "panel_source": panel_src,
            "identity_source": "yochananof_catalog_harvest_real_ean",
        }
        (OUT_DIR / f"{pid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        written += 1

    from collections import Counter
    kept_bc = set()
    for f in OUT_DIR.glob("bsip1_snack_*.json"):
        kept_bc.add(json.loads(f.read_text("utf-8"))["barcode"])
    kept = [p for p in products if p["barcode"] in kept_bc]
    print(f"BSIP1 written: {written} products -> {OUT_DIR}")
    print(f"  with real ingredients: {written - len(panel_only)} | panel-only: {len(panel_only)} {panel_only}")
    no_panel = [d for d in dropped if d.get("drop_class") == "no_panel"]
    basis_err = [d for d in dropped if d.get("drop_class") == "basis_error"]
    print(f"  dropped total: {len(dropped)}  (no_panel: {len(no_panel)}, basis_error: {len(basis_err)})")
    for dr in dropped:
        print(f"    DROP [{dr.get('drop_class')}]", dr["barcode"], dr["name"], "-", dr["reason"][:60])
    # machine-readable drop manifest for the run record / re-QA
    (OUT_DIR.parent / "reports" / "salty_snacks_retailer_drops.json").write_text(
        json.dumps(dropped, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  subpool dist:", dict(Counter(p["sub_pool"] for p in kept)))


if __name__ == "__main__":
    main()
