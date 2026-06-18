# BSIP1 builder -- Cookies-near-coffee (run_cookies_001) / TASK-275/P68
# Uses parse_nutrition_numeric (EV-046) + ingredient_enricher. OFF ban: absolute.
# Fix-A (TASK-275): allergen-strip now uses _rfind_outside_parens() to avoid
# truncating ingredient text at gluten notices embedded in parentheticals like
# "(מכיל גלוטן)" — the old rfind() fired on those and produced 16 truncated records.
import sys, json, re, pathlib, logging, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(r"C:\Bari")
sys.path.insert(0, str(ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"))
sys.path.insert(0, str(ROOT / "03_operations" / "bsip1" / "core"))
from bsip0_nutrition import parse_nutrition_numeric
from ingredient_enricher import enrich as enrich_ingredients
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)
BSIP0_FILE = ROOT/"02_products"/"cookies_coffee"/"bsip0_outputs"/"cookies_coffee_bsip0_raw_20260613T163431.json"
CORPUS_FILE = ROOT/"02_products"/"cookies_coffee"/"factory_run_001"/"corpus_filter.json"
BSIP1_OUTPUT = ROOT/"03_operations"/"bsip1"/"run_cookies_001"/"output"
RUN_ID = "run_cookies_001"
BSIP1_OUTPUT.mkdir(parents=True, exist_ok=True)

def _rfind_outside_parens(text, marker):
    """Return the LAST position of marker that occurs at parenthesis depth 0.
    Returns -1 if not found, or found only inside parentheses.
    Fix-A (TASK-275): the old rfind() matched allergen phrases embedded in
    parenthetical sub-groups like '(מכיל גלוטן)' inside ingredient items,
    truncating the text at the first parenthetical sub-group. This helper
    only matches at depth 0 (outside any parentheses).
    """
    last = -1
    depth = 0
    mlen = len(marker)
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if depth == 0 and text[i:i+mlen] == marker:
            last = i
    return last

def extract_clean_ingredients(raw):
    if not raw: return ""
    text = raw
    # Strip trailing retailer marketing / metadata noise (rfind is safe here:
    # these markers never appear inside ingredient parentheticals).
    for m in ["הנתונים המדויקים","יתכנו טעויות","התמונות והתאריכים"]:
        idx = text.rfind(m)
        if idx != -1: text = text[:idx]
    # Strip allergen/gluten declarations ONLY when outside parentheses.
    # Bug-A: these phrases like "מכיל גלוטן" appear in parentheticals
    # "(מכיל גלוטן)" that are sub-groups of the first ingredient; old rfind()
    # matched there and truncated 16/58 products to a single token.
    for m in ["מכיל גלוטן חיטה עלול","מכיל גלוטן","עלול להכיל","מכיל:","מכיל חלב"]:
        idx = _rfind_outside_parens(text, m)
        if idx != -1: text = text[:idx]
    text = re.sub(r"\s*\d+[\d.,]*\s*(גרם|מג|קל|kcal|mg|g).*$","",text.strip(),flags=re.UNICODE)
    text = text.strip().rstrip(",. ")
    return text if len(text) >= 5 else ""

def build_ingredients_list(ing_text):
    if not ing_text: return []
    items, current, depth = [], "", 0
    for char in ing_text:
        if char == "(": depth += 1; current += char
        elif char == ")": depth -= 1; current += char
        elif char in (",",";") and depth == 0:
            s = current.strip().rstrip(".")
            if s and len(s) > 1: items.append(s)
            current = ""
        else: current += char
    if current.strip(): items.append(current.strip().rstrip("."))
    return [i for i in items if i and len(i) > 1]

def build_bsip1(product, ts):
    barcode = str(product.get("barcode",""))
    name_he = product.get("name_he","")
    brand = product.get("brand","")
    raw_ing = product.get("ingredients_raw","") or ""
    image_url = (product.get("image_urls") or [None])[0]
    price = product.get("price")
    source_url = product.get("source_url","")
    scraped_at = product.get("scraped_at","")
    nn = parse_nutrition_numeric(product.get("nutrition",{}))
    integrity = nn.pop("_integrity",[])
    ing_text = extract_clean_ingredients(raw_ing)
    ing_list = build_ingredients_list(ing_text)
    fat=nn.get("fat_g"); sat=nn.get("fat_saturated_g")
    sugar=nn.get("sugars_g"); carbs=nn.get("carbohydrates_g")
    kcal=nn.get("energy_kcal"); prot=nn.get("protein_g")
    sugar_le_carbs = True if (sugar is None or carbs is None) else (sugar<=carbs+0.15)
    satfat_le_fat  = True if (sat is None or fat is None) else (sat<=fat+0.15)
    kcal_plausible = True if kcal is None else (100<=kcal<=700)
    macros_ok      = True if prot is None else (prot<100)
    missing=[k for k,v in nn.items() if v is None and k in ("energy_kcal","fat_g","protein_g","sodium_mg")]
    trust_score=0.75; risk_flags=["single_source_shufersal"]
    if not (sugar_le_carbs and satfat_le_fat): trust_score-=0.2; risk_flags.append("consistency_warning")
    if not kcal_plausible: trust_score-=0.1; risk_flags.append("kcal_implausible")
    if not ing_text: trust_score-=0.1; risk_flags.append("no_ingredient_text")
    if integrity: trust_score-=0.1; risk_flags.append("nutrition_integrity_warning")
    trust_score=round(max(0.1,min(1.0,trust_score)),2)
    trust_level="high" if trust_score>=0.80 else ("medium" if trust_score>=0.50 else "low")
    doc = {
        "schema_version":"bsip1_v0_1","file_type":"product",
        "canonical_product_id":f"bsip1_cookies_{barcode}",
        "barcode":barcode,"canonical_name_he":name_he,"brand":brand,
        "weight_g":None,"category":"snack_bar_granola",
        "source_retailers":["shufersal"],
        "retailer_prices":{"shufersal":float(price) if price else None},
        "image_url":image_url,"normalized_nutrition_per_100g":nn,
        "energy_kcal":nn.get("energy_kcal"),"fat_g":nn.get("fat_g"),
        "fat_saturated_g":nn.get("fat_saturated_g"),"fat_trans_g":nn.get("fat_trans_g"),
        "protein_g":nn.get("protein_g"),"carbohydrates_g":nn.get("carbohydrates_g"),
        "sugars_g":nn.get("sugars_g"),"sodium_mg":nn.get("sodium_mg"),
        "dietary_fiber_g":nn.get("dietary_fiber_g"),"cholesterol_mg":nn.get("cholesterol_mg"),
        "ingredients_text_he":ing_text if ing_text else None,
        "ingredients_list":ing_list,"ingredient_count":len(ing_list),
        "ingredient_text_quality":"good" if len(ing_list)>=3 else ("present" if ing_text else "absent"),
        "allergens_contains":[],"allergens_may_contain":[],
        "off_source_used":False,"nova_proxy":None,"nova_confidence":None,"nova_notes":[],
        "detected_additives":[],"additive_count":0,
        "confidence":trust_score,"canonical_trust_level":trust_level,
        "canonical_trust_score":trust_score,"canonical_risk_flags":risk_flags,
        "missing_fields":missing,"inferred_fields":[],
        "consistency_checks":{"sugar_le_carbs":sugar_le_carbs,"satfat_le_fat":satfat_le_fat,
                               "kcal_plausible":kcal_plausible,"macros_ok":macros_ok},
        "nutrition_integrity":integrity,
        "nutrition_consistency_status":"consistent" if (sugar_le_carbs and satfat_le_fat and not integrity) else "warnings",
        "data_sufficiency":"sufficient" if not missing else "partial",
        "bsip1_trust_level":trust_level,"bsip1_trust_score":trust_score,"bsip1_risk_flags":risk_flags,
        "provenance":{"source":"shufersal_direct_scrape","fetched_at":scraped_at,
                       "source_url":source_url,"panel_source":"shufersal_storefront",
                       "verification_status":"candidate","off_used":False},
        "enrichment_timestamp":ts,"run_id":RUN_ID,
    }
    return enrich_ingredients(doc)

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== BSIP1 Cookies-near-coffee (run_cookies_001) -- TASK-275/P68 ===")
    log.info("Fix-A: allergen-strip now uses _rfind_outside_parens (depth-0 only).")
    log.info("Uses: parse_nutrition_numeric (EV-046) + ingredient_enricher. OFF ban: absolute.")
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    in_scored = {str(p["barcode"]) for p in corpus["products"] if p["decision"]=="IN_SCORED"}
    log.info("IN_SCORED barcodes: %d", len(in_scored))
    bsip0_raw = json.loads(BSIP0_FILE.read_text(encoding="utf-8"))
    to_build = [p for p in bsip0_raw if str(p.get("barcode","")) in in_scored]
    log.info("BSIP0 matched to IN_SCORED: %d", len(to_build))
    if len(to_build) != 61:
        log.warning("Expected 61 IN_SCORED, got %d -- check barcode alignment", len(to_build))
    built, errors, ing_coverage = [], [], 0
    for product in to_build:
        barcode = str(product.get("barcode","")); name = product.get("name_he","")
        try:
            doc = build_bsip1(product, ts)
            out = BSIP1_OUTPUT / f"bsip1_cookies_{barcode}.json"
            out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            built.append(doc)
            if doc.get("ingredients_text_he"): ing_coverage += 1
            log.info("  BSIP1 %-40s ing=%s cnt=%s", name[:38], "yes" if doc.get("ingredients_text_he") else "no", doc.get("ingredient_count"))
        except Exception as e:
            log.error("  BSIP1 ERROR %s: %s", barcode, e)
            import traceback; traceback.print_exc()
            errors.append({"barcode":barcode,"name":name,"error":str(e)})
    ing_pct = ing_coverage / len(to_build) * 100 if to_build else 0
    log.info("BSIP1 done. Built=%d errors=%d ing_coverage=%d/%d (%.0f%%)",
             len(built), len(errors), ing_coverage, len(to_build), ing_pct)
    if ing_pct < 15:
        log.warning("COVERAGE GATE: only %.0f%% (threshold 15%%) -- WARNING", ing_pct)
    else:
        log.info("Coverage gate: %.0f%% -- PASS", ing_pct)
    print(chr(10)+"=== BSIP1 run_cookies_001 complete ===")

    print(f"Built: {len(built)}/{len(to_build)}, errors: {len(errors)}")
    print(f"Ingredient coverage: {ing_coverage}/{len(to_build)} ({ing_pct:.0f}%)")
    print(f"Output: {BSIP1_OUTPUT}")
    if errors: print("ERRORS:", errors)

if __name__ == "__main__":
    main()
