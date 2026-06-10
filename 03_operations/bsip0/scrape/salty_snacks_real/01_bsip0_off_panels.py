"""
BSIP0 — Salty snacks REAL rebuild (TASK-228).

Identity + image source: Yochananof storefront catalog harvest (yoh_named_catalog.json) —
  real EAN (embedded in image URL filename) + real product name + real api.yochananof.co.il
  image URL (HTTP 200 verified).
Panel source: Open Food Facts by REAL EAN (nutrition per 100g + ingredients_text_he).
  EDPG: OFF panel is a CANDIDATE, provenance-stamped, promoted only after BSIP0/QA pass.

Output: 02_products/salty_snacks/bsip0_outputs/bsip0_salty_snacks_real_raw.json
Keeps only products with a real image AND a usable OFF panel (>= core macros).
"""
import sys, json, re, pathlib, time
from datetime import datetime, timezone
sys.path.insert(0, r"C:\Bari")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from integrations.clients.open_food_facts import get_product

HERE = pathlib.Path(__file__).parent
CANDS = pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\shufersal_frozen_vegetables\rescraper\salty_candidates.json")
OUT_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip0_outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "bsip0_salty_snacks_real_raw.json"

# salty-snack subpool inference from Hebrew name
def subpool(name: str) -> str:
    n = name
    if any(k in n for k in ["פופקורן"]): return "popcorn"
    if any(k in n for k in ["פריכ", "חטיף אורז", "פצפוצי אורז", "פריכיות"]): return "rice_cakes"
    if any(k in n for k in ["בייגלה", "בייגל", "מקלות מלוח"]): return "pretzels"
    if any(k in n for k in ["במבה", "ביסלי", "חטיף תירס", "מקלות תירס", "צ'יפס עגבני", "מאנצ"]): return "puffed"
    if any(k in n for k in ["עדשים", "חומוס", "קטני", "אפוי", "וואווז", "fitness", "פיטנס", "חיטה מלאה"]): return "baked"
    if any(k in n for k in ["תפוצ", "תפוציפס", "פרינגלס", "דוריטוס", "צ'יפס", "ציפס", "נאצ", "קרקר", "טורטיה"]): return "chips"
    return "chips"

def brand_from(name: str, off_brand) -> str:
    if off_brand: return off_brand.split(",")[0].strip()
    for b, en in [("במבה", "Osem"), ("ביסלי", "Osem"), ("תפוצ", "Strauss"), ("פרינגלס", "Pringles"),
                  ("דוריטוס", "Doritos"), ("אפרופו", "Osem")]:
        if b in name: return en
    return ""

def norm_nutriments(n: dict) -> dict:
    def g(*keys):
        for k in keys:
            v = n.get(k)
            if v is not None:
                try: return float(v)
                except (TypeError, ValueError): pass
        return None
    sodium = g("sodium_100g")
    salt = g("salt_100g")
    sodium_mg = None
    if sodium is not None:
        sodium_mg = round(sodium * 1000)
    elif salt is not None:
        sodium_mg = round(salt * 400)  # salt g → sodium mg (salt*0.4*1000)
    return {
        "energy_kcal": g("energy-kcal_100g", "energy-kcal_value"),
        "fat_g": g("fat_100g"),
        "fat_saturated_g": g("saturated-fat_100g"),
        "fat_trans_g": g("trans-fat_100g"),
        "sodium_mg": sodium_mg,
        "carbohydrates_g": g("carbohydrates_100g"),
        "sugars_g": g("sugars_100g"),
        "dietary_fiber_g": g("fiber_100g"),
        "protein_g": g("proteins_100g"),
    }

def main():
    cands = json.loads(CANDS.read_text(encoding="utf-8"))
    print(f"Candidates: {len(cands)}")
    kept, no_panel, not_found, err = [], [], [], []
    for i, c in enumerate(cands, 1):
        ean = c["ean"]
        try:
            p = get_product(ean)
        except Exception as e:
            err.append({"ean": ean, "error": str(e)}); continue
        if not p.found:
            not_found.append(ean); continue
        if not p.has_panel:
            no_panel.append(ean); continue
        nn = norm_nutriments(p.nutriments)
        # require core macros present
        if nn["energy_kcal"] is None or nn["protein_g"] is None or nn["fat_g"] is None:
            no_panel.append(ean); continue
        prov = p.provenance.__dict__ if p.provenance else {}
        rec = {
            "barcode": ean,
            "name_he": c["name"],
            "name_off": p.name,
            "brand": brand_from(c["name"], p.brand),
            "image_url": c["image"],            # REAL yochananof image (200-verified)
            "sub_pool": subpool(c["name"]),
            "normalized_nutrition_per_100g": nn,
            "ingredients_text_he": p.ingredients_text or "",
            "nova_group_off": p.nova_group,
            "off_completeness": p.completeness,
            "panel_provenance": prov,
            "identity_source": "yochananof_catalog_harvest",
            "panel_source": "open_food_facts",
        }
        kept.append(rec)
        if i % 25 == 0:
            print(f"  [{i}/{len(cands)}] kept={len(kept)}")
        time.sleep(0.15)

    bsip0 = {
        "schema_version": "bsip0_v1",
        "run_id": "salty_snacks_real_001",
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "category": "salty_snacks",
        "retailer": "yochananof",
        "acquisition_method": "yochananof_catalog_harvest + open_food_facts_panel_by_real_ean",
        "scrape_date": datetime.now().strftime("%Y-%m-%d"),
        "identity_source": "yochananof storefront catalog (real EAN + real image URL)",
        "panel_source": "open_food_facts (candidate panel by real EAN; EDPG-gated)",
        "candidate_count": len(cands),
        "product_count": len(kept),
        "completeness": {
            "with_panel": len(kept),
            "off_not_found": len(not_found),
            "off_no_usable_panel": len(no_panel),
            "errors": len(err),
        },
        "provenance": {
            "identity": "yochananof_catalog_harvest (yoh_named_catalog.json, real EAN in image URL)",
            "panel": "open_food_facts by real EAN",
            "edpg_note": "OFF panels are candidate; promoted to verified only after BSIP0/QA gate",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        },
        "products": kept,
    }
    OUT.write_text(json.dumps(bsip0, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nBSIP0 written: {OUT}")
    print(f"Kept (real img + usable panel): {len(kept)}")
    print(f"OFF not found: {len(not_found)} | no usable panel: {len(no_panel)} | errors: {len(err)}")

if __name__ == "__main__":
    main()
