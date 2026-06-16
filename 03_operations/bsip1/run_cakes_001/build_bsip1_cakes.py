# BSIP1 builder + merge + corpus-filter — Cakes + Hard Cookies (run_cakes_001 / TASK-283).
# Merges the TWO retailer BSIP0 raws (Shufersal + Yochananof), dedups by barcode,
# applies the sufficiency gate (full macros + real ingredient list -> IN_SCORED, else
# TRANSPARENCY_NULL per the missing-data discard rule), and builds BSIP1 records for the
# IN_SCORED set. OFF ban: absolute (no OFF field anywhere). Reuses the proven cookies
# parsing incl. Fix-A (_rfind_outside_parens) so ingredient truncation can't recur.
import sys, json, re, glob, pathlib, datetime, logging
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(r"C:\Bari")
sys.path.insert(0, str(ROOT/"03_operations"/"bsip0"/"scrape"/"_shared"))
sys.path.insert(0, str(ROOT/"03_operations"/"bsip1"/"core"))
from bsip0_nutrition import parse_nutrition_numeric
from ingredient_enricher import enrich as enrich_ingredients
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s"); log = logging.getLogger(__name__)

BSIP0_DIR = ROOT/"02_products"/"cakes_hard_cookies"/"bsip0_outputs"
RUN_DIR   = ROOT/"02_products"/"cakes_hard_cookies"/"factory_run_001"
BSIP1_OUT = ROOT/"03_operations"/"bsip1"/"run_cakes_001"/"output"
RUN_ID = "run_cakes_001"
RUN_DIR.mkdir(parents=True, exist_ok=True); BSIP1_OUT.mkdir(parents=True, exist_ok=True)


def _rfind_outside_parens(text, marker):
    last, depth, mlen = -1, 0, len(marker)
    for i, ch in enumerate(text):
        if ch == "(": depth += 1
        elif ch == ")": depth = max(0, depth - 1)
        if depth == 0 and text[i:i+mlen] == marker: last = i
    return last


def extract_clean_ingredients(raw):
    if not raw: return ""
    text = raw
    # Cut at the FIRST nutrition/marketing/disclaimer boundary — real ingredients always
    # precede these. 'ערכים תזונתיים' (nutrition header) is the main storefront bleed.
    for m in ["ערכים תזונתיים", "הנתונים המדויקים", "יתכנו טעויות", "התמונות והתאריכים",
              "יש לקרוא", "אין להסתמך", "מידע אלרגני"]:
        idx = text.find(m)
        if idx != -1: text = text[:idx]
    for m in ["מכיל גלוטן חיטה עלול", "מכיל גלוטן", "עלול להכיל", "מכיל:", "מכיל חלב"]:
        idx = _rfind_outside_parens(text, m)
        if idx != -1: text = text[:idx]
    text = re.sub(r"^\s*רכיבים\s*[:\-]?\s*", "", text.strip())
    return text.strip().rstrip(",;").strip()


def build_ingredients_list(ing_text):
    if not ing_text: return []
    items, current, depth = [], "", 0
    for char in ing_text:
        if char == "(": depth += 1; current += char
        elif char == ")": depth -= 1; current += char
        elif char in (",", ";") and depth == 0:
            s = current.strip().rstrip(".");
            if s and len(s) > 1: items.append(s)
            current = ""
        else: current += char
    if current.strip(): items.append(current.strip().rstrip("."))
    return [i for i in items if i and len(i) > 1]


def _has_nutrition(p):
    n = p.get("nutrition", {})
    return bool(n.get("energy_kcal_raw")) and bool(n.get("fat_raw")) and bool(n.get("carbs_raw") or n.get("protein_raw"))


def load_latest(retailer):
    fs = sorted(glob.glob(str(BSIP0_DIR/f"cakes_{retailer}_bsip0_raw_*.json")))
    if not fs: return []
    d = json.loads(pathlib.Path(fs[-1]).read_text(encoding="utf-8"))
    return d.get("products", d if isinstance(d, list) else [])


def merge():
    shuf = load_latest("shufersal"); yoh = load_latest("yohananof")
    log.info("loaded shufersal=%d yohananof=%d", len(shuf), len(yoh))
    by_bc = {}
    for p in shuf + yoh:
        bc = str(p.get("barcode", "")).strip()
        if not bc or len(bc) < 6: continue
        cur = by_bc.get(bc)
        # prefer the record that has BOTH nutrition and ingredients; else keep first, merge retailers/image
        if cur is None:
            p["source_retailers"] = [p["retailer_id"]]; by_bc[bc] = p
        else:
            if p["retailer_id"] not in cur["source_retailers"]:
                cur["source_retailers"].append(p["retailer_id"])
            cand_full = _has_nutrition(p) and bool(p.get("ingredients_raw"))
            cur_full = _has_nutrition(cur) and bool(cur.get("ingredients_raw"))
            if cand_full and not cur_full:
                p["source_retailers"] = cur["source_retailers"]; by_bc[bc] = p
            elif not cur.get("image_urls") and p.get("image_urls"):
                cur["image_urls"] = p["image_urls"]
    return list(by_bc.values())


def build_bsip1(product, ts):
    barcode = str(product.get("barcode", "")); name_he = product.get("name_he", "")
    raw_ing = product.get("ingredients_raw", "") or ""
    nn = parse_nutrition_numeric(product.get("nutrition", {})); nn.pop("_integrity", [])
    ing_text = extract_clean_ingredients(raw_ing); ing_list = build_ingredients_list(ing_text)
    retailers = product.get("source_retailers", [product.get("retailer_id", "")])
    missing = [k for k, v in nn.items() if v is None and k in ("energy_kcal", "fat_g", "protein_g", "sodium_mg")]
    trust = 0.78 if len(retailers) >= 2 else 0.72
    flags = (["multi_retailer_confirmed"] if len(retailers) >= 2 else ["single_source"])
    if not ing_text: trust -= 0.1; flags.append("no_ingredient_text")
    doc = {
        "schema_version": "bsip1_v0_1", "file_type": "product",
        "canonical_product_id": f"bsip1_cakes_{barcode}", "barcode": barcode,
        "canonical_name_he": name_he, "brand": product.get("brand", ""), "weight_g": product.get("weight_g"),
        "category": "cake_cookie", "source_retailers": retailers,
        "image_url": (product.get("image_urls") or [None])[0],
        "normalized_nutrition_per_100g": nn,
        "energy_kcal": nn.get("energy_kcal"), "fat_g": nn.get("fat_g"),
        "fat_saturated_g": nn.get("fat_saturated_g"), "fat_trans_g": nn.get("fat_trans_g"),
        "protein_g": nn.get("protein_g"), "carbohydrates_g": nn.get("carbohydrates_g"),
        "sugars_g": nn.get("sugars_g"), "sodium_mg": nn.get("sodium_mg"),
        "dietary_fiber_g": nn.get("dietary_fiber_g"), "cholesterol_mg": nn.get("cholesterol_mg"),
        "ingredients_text_he": ing_text if ing_text else None,
        "ingredients_list": ing_list, "ingredient_count": len(ing_list),
        "ingredient_text_quality": "good" if len(ing_list) >= 3 else ("present" if ing_text else "absent"),
        "allergens_contains": [], "allergens_may_contain": [],
        "off_source_used": False, "nova_proxy": None, "nova_confidence": None, "nova_notes": [],
        "detected_additives": [], "additive_count": 0,
        "confidence": round(max(0.1, min(1.0, trust)), 2), "canonical_trust_level": "high" if trust >= 0.75 else "medium",
        "canonical_risk_flags": flags, "missing_fields": missing, "inferred_fields": [],
        "data_sufficiency": "sufficient" if not missing else "partial",
        "provenance": {"source": "+".join(retailers) + "_direct_scrape", "fetched_at": product.get("scraped_at", ""),
                       "source_url": product.get("source_url", ""), "panel_source": "storefront",
                       "verification_status": "candidate", "off_used": False},
        "enrichment_timestamp": ts, "run_id": RUN_ID,
    }
    return enrich_ingredients(doc)


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    merged = merge()
    log.info("merged unique barcodes: %d", len(merged))
    # sufficiency gate -> corpus_filter
    # Precise savory-scope exclusion: broad 'קראנץ' (crunch) pulled in breaded chicken
    # schnitzel + meatballs that pass the nutrition+ingredients gate. These terms never
    # appear in a legitimate cake/hard-cookie name (verified against the corpus).
    SAVORY = ["עוף", "שניצל", "קציצות", "נקניק", "המבורגר", "שווארמה", "שוארמה",
              "צ'ונגו", "קבב", "בשר", "בורקס", "חזה", "כנפי", "פסטרמה", "סלמי", "נתחי"]
    decisions = []
    for p in merged:
        bc = str(p["barcode"]); full_nutr = _has_nutrition(p)
        ing_ok = len(build_ingredients_list(extract_clean_ingredients(p.get("ingredients_raw", "")))) >= 3
        is_savory = any(s in p.get("name_he", "") for s in SAVORY)
        if is_savory:
            decision, reason = "OUT_OF_SCOPE", "savory_not_cake_cookie"
        elif full_nutr and ing_ok:
            decision, reason = "IN_SCORED", ""
        else:
            decision, reason = "TRANSPARENCY_NULL", ("no_full_nutrition" if not full_nutr else "ingredient_list_too_short")
        decisions.append({"barcode": bc, "name_he": p.get("name_he", ""), "decision": decision,
                          "retailers": p.get("source_retailers", []), "reason": reason})
    in_scored = [d for d in decisions if d["decision"] == "IN_SCORED"]
    corpus = {"stage": "2_corpus_filter", "category_slug": "cakes-hard-cookies", "run_id": "factory_run_001",
              "generated": ts[:10], "owner": "Data Agent (autonomous run #8)", "off_used": False,
              "off_note": "OFF ban absolute (TASK-238). Nutrition+ingredients are direct storefront scrape only; NULL stays NULL.",
              "retailers": ["shufersal", "yohananof"],
              "sufficiency_gate": "energy_kcal AND fat AND (carbs OR protein) present AND ingredient_list>=3 -> IN_SCORED; else TRANSPARENCY_NULL (discard).",
              "counts": {"merged": len(merged), "in_scored": len(in_scored),
                         "transparency_null": sum(1 for d in decisions if d["decision"] == "TRANSPARENCY_NULL"),
                         "out_of_scope": sum(1 for d in decisions if d["decision"] == "OUT_OF_SCOPE")},
              "products": decisions}
    (RUN_DIR/"corpus_filter.json").write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding="utf-8")
    (BSIP0_DIR/"cakes_merged_bsip0_raw.json").write_text(
        json.dumps({"meta": {"retailers": ["shufersal", "yohananof"], "count": len(merged), "off_used": False},
                    "products": merged}, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("corpus_filter: merged=%d IN_SCORED=%d TRANSPARENCY_NULL=%d",
             len(merged), len(in_scored), len(decisions) - len(in_scored))

    in_bc = {d["barcode"] for d in in_scored}
    built, errors, ing_cov, multi = 0, [], 0, 0
    for p in merged:
        if str(p["barcode"]) not in in_bc: continue
        try:
            doc = build_bsip1(p, ts)
            (BSIP1_OUT/f"bsip1_cakes_{doc['barcode']}.json").write_text(
                json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            built += 1
            if doc.get("ingredients_text_he"): ing_cov += 1
            if len(doc["source_retailers"]) >= 2: multi += 1
        except Exception as e:
            errors.append({"barcode": p["barcode"], "error": str(e)})
            import traceback; traceback.print_exc()
    print(f"\n=== BSIP1 run_cakes_001 ===")
    print(f"merged={len(merged)} IN_SCORED={len(in_scored)} built={built} errors={len(errors)}")
    print(f"ingredient_coverage={ing_cov}/{built}  multi_retailer_confirmed={multi}")
    print(f"corpus_filter: {RUN_DIR/'corpus_filter.json'}")
    print(f"BSIP1 output: {BSIP1_OUT}")
    if errors: print("ERRORS:", errors[:5])


if __name__ == "__main__":
    main()
