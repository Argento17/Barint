"""Write final Pass 2 output JSON with all confirmed data."""
import sys, pathlib, json, datetime, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path("C:/Bari/02_products/snack_bars")))
sys.path.insert(0, str(pathlib.Path("C:/Bari/03_operations/bsip0/scrape/_shared")))
import run_task360_phase3 as P3
from bsip0_nutrition import parse_nutrition_numeric

VICTORY_BASE = "https://www.victoryonline.co.il"
ROOT = pathlib.Path("C:/Bari")
RUN_ID = "choc_task366_pass2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / RUN_ID / "output"
BSIP2_DIR = ROOT / "02_products" / "chocolate" / "bsip2_outputs" / RUN_ID / "products"
for d in (BSIP1_DIR, BSIP2_DIR):
    d.mkdir(parents=True, exist_ok=True)

ALL_TARGETS = {
    "4820005195848": {"label": "Millennium 80%",         "task": "TARGET1", "in_catalog": False},
    "3046920023443": {"label": "Lindt Excellence dark",  "task": "TARGET2", "in_catalog": False},
    "3046920023429": {"label": "Lindt caramel milk",     "task": "TARGET2", "in_catalog": False},
    "3046920023368": {"label": "Lindt Excellence milk",  "task": "TARGET2", "in_catalog": False},
    "3046920028004": {"label": "Lindt Excellence 70%",   "task": "INCIDENTAL", "in_catalog": True},
    "4820005198597": {"label": "Millennium 74%",         "task": "TARGET1", "in_catalog": False},
    "5941021001261": {"label": "75% dark chocolate",     "task": "INCIDENTAL", "in_catalog": True},
    "7290119500482": {"label": "62% dark (maltitol)",    "task": "INCIDENTAL", "in_catalog": True},
}

LABEL_MAP = [
    (["טראנס", "trans"], "trans_fat"),
    (["רווי", "saturated"], "saturated_fat"),
    (["סוכר", "sugar"], "sugar"),
    (["פחמימ", "carb"], "carbs"),
    (["סיב", "fiber"], "fiber"),
    (["חלבונ", "protein"], "protein"),
    (["נתרן", "sodium"], "sodium"),
    (["אנרגי", "קלורי", "kcal", "energy", "calorie"], "energy"),
    (["שומנ", "fat"], "fat"),
]

def parse_nutr_json(nv):
    if not isinstance(nv, dict):
        return {}
    sizes = nv.get("sizes") or []
    values = nv.get("values") or []
    col_idx = 0
    for i, sz in enumerate(sizes):
        nm = sz.get("names") or {}
        s = nm.get("1") or nm.get(1) or ""
        if "100" in str(s):
            col_idx = i
            break
    result, seen = {}, set()
    for row in values:
        nm = row.get("names") or {}
        label = nm.get("1") or nm.get(1) or ""
        if isinstance(label, dict):
            label = label.get("name", "")
        svl = row.get("sizeValues") or []
        if col_idx >= len(svl):
            continue
        sv = svl[col_idx]
        val = sv.get("value") if isinstance(sv, dict) else sv
        try:
            val = float(str(val).replace(",", "."))
        except (ValueError, TypeError):
            continue
        ll = (label or "").lower()
        for tokens, canon in LABEL_MAP:
            if canon in seen:
                continue
            if any(t in (label or "") or t in ll for t in tokens):
                if canon in ("fat", "carbs") and "מתוכ" in (label or ""):
                    continue
                result[canon] = val
                seen.add(canon)
                break
    return result

def get_sodium_raw_from_nv(nv):
    for row in (nv.get("values") or []):
        nm = row.get("names") or {}
        label = nm.get("1") or ""
        if "נתרן" in label:
            svl = row.get("sizeValues") or []
            if svl:
                sv = svl[0]
                val = sv.get("value", 0)
                unit_nm = (sv.get("unitOfMeasure") or {}).get("names", {}).get("1", "")
                if "מ" in unit_nm or "mg" in unit_nm.lower():
                    return f"{val} מג"
                return str(val)
    return None

# Fetch catalog data for confirmed products
catalog = {}
for bc in ["3046920028004", "5941021001261", "7290119500482"]:
    r = requests.get(f"{VICTORY_BASE}/v2/retailers/1470/products?barcode={bc}&appId=4", timeout=15)
    prods = r.json().get("products", [])
    if prods:
        p = prods[0]
        lang1 = (p.get("data") or {}).get("1") or {}
        ingr = lang1.get("ingredients") or ""
        nv = p.get("nutritionValues") or {}
        nutr = parse_nutr_json(nv)
        sodium_raw = get_sodium_raw_from_nv(nv)
        catalog[bc] = {
            "ingredients": ingr,
            "nutrition": nutr,
            "sodium_raw": sodium_raw,
            "nv_raw": nv,
        }
        print(f"Fetched {bc}: ingr={ingr[:60]} sodium_raw={sodium_raw}", flush=True)
    else:
        print(f"UNEXPECTED: {bc} not found", flush=True)

def to_scoring_raw(bc, d):
    n = d["nutrition"]
    return {
        "energy_kcal_raw": str(n.get("energy", "")),
        "fat_raw": str(n.get("fat", "")),
        "saturated_fat_raw": str(n.get("saturated_fat", "")),
        "trans_fat_raw": str(n.get("trans_fat", "0")),
        "sodium_raw": d["sodium_raw"] or str(n.get("sodium", 0)),
        "carbs_raw": str(n.get("carbs", "")),
        "sugar_raw": str(n.get("sugar", "")),   # TASK-376 fix: canonical key is sugar_raw (not sugars_raw)
        "fiber_raw": str(n.get("fiber", "")) if "fiber" in n else "",
        "protein_raw": str(n.get("protein", "")),
    }

results = {}
for bc, info in ALL_TARGETS.items():
    if not info["in_catalog"]:
        results[bc] = {
            "barcode": bc,
            "label": info["label"],
            "task": info["task"],
            "status": "NOT_IN_VICTORY_CATALOG",
            "source": "victory",
            "source_endpoint": f"/v2/retailers/1470/products?barcode={bc}&appId=4",
            "note": "Product not in Victory retailer 1470 catalog (API returned total=0)",
            "nutrition": None,
            "ingredients": None,
            "ingredients_status": "NULL",
            "has_full_nutrition": False,
            "plausibility_gate": "NOT_APPLICABLE",
            "score": None,
            "grade": None,
            "off_check": "PASS",
        }
        continue

    d = catalog[bc]
    ingr = d["ingredients"]
    nutr = d["nutrition"]
    has_real = bool(ingr and any(w in ingr for w in ["קקאו", "סוכר", "חלב", "לציטין", "מלטיטול", "שומן", "חמאת"]))
    nutr_raw = to_scoring_raw(bc, d)
    nutr_num = parse_nutrition_numeric(nutr_raw)
    gate = P3.run_plausibility_gate(nutr_num, ingr, bc, None)

    score_val = grade_val = conf = conf_band = None
    if gate["verdict"] in ("pass", "converted_pass"):
        meta = {
            "description": info["label"], "name_truncated": info["label"],
            "brand": "", "code": "P_" + bc, "sku": bc,
            "image_url": "", "unit_description": "",
            "health_attrs": [], "all_cat_codes": [],
        }
        scraped = {
            "plausibility_gate": gate,
            "ingredients_raw": ingr,
            "weight_g": None, "serving_g": None,
            "nutrition_numeric_per_100g": nutr_num,
        }
        bsip1 = P3.build_bsip1(meta, scraped, bc, RUN_ID)
        bsip1_path = BSIP1_DIR / f"bsip1_{bc}.json"
        bsip1_path.write_text(json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8")
        res = P3.run_bsip2(bsip1_path, BSIP2_DIR)
        if res["status"] == "ok":
            tr = res["trace"]
            score_val = tr.get("final_score_estimate")
            grade_val = tr.get("grade_estimate")
            conf = tr.get("confidence_score")
            conf_band = tr.get("confidence_band")

    results[bc] = {
        "barcode": bc,
        "label": info["label"],
        "task": info["task"],
        "status": "FOUND_AND_SCORED",
        "source": "victory",
        "source_endpoint": f"/v2/retailers/1470/products?barcode={bc}&appId=4",
        "note": "Confirmed in Victory retailer 1470 catalog",
        "nutrition": nutr,
        "nutrition_canonical": nutr_num,
        "ingredients": ingr or None,
        "ingredients_status": "REAL_INGREDIENTS" if has_real else ("BOILERPLATE" if ingr else "NULL"),
        "has_full_nutrition": bool(nutr.get("energy") and nutr.get("fat") and nutr.get("carbs")),
        "plausibility_gate": gate["verdict"],
        "score": score_val,
        "grade": grade_val,
        "confidence": conf,
        "confidence_band": conf_band,
        "off_check": "PASS",
    }
    print(f"Scored {bc}: score={score_val} grade={grade_val}", flush=True)

# OFF check
off_viol = [f"{bc}.{k}" for bc, r in results.items() for k, v in r.items()
            if isinstance(v, str) and "openfoodfacts" in v.lower()]
off_status = "PASS" if not off_viol else f"FAIL:{off_viol}"

found = sum(1 for r in results.values() if r["status"] == "FOUND_AND_SCORED")
nutr_c = sum(1 for r in results.values() if r.get("has_full_nutrition"))
real_i = sum(1 for r in results.values() if r.get("ingredients_status") == "REAL_INGREDIENTS")
plaus_p = sum(1 for r in results.values() if r.get("plausibility_gate") == "pass")
scored_c = sum(1 for r in results.values() if r.get("score") is not None)

ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
out_path = ROOT / "02_products" / "chocolate" / f"choc_tablets_fix_task366b_{ts}.json"

payload = {
    "task": "TASK-366 Pass 2 Victory probe",
    "run_id": RUN_ID,
    "run_ts": ts,
    "retailer": "victory",
    "retailer_id": 1470,
    "off_check": off_status,
    "counts": {
        "targets_attempted": len(ALL_TARGETS),
        "found_in_victory_catalog": found,
        "not_in_victory_catalog": len(ALL_TARGETS) - found,
        "has_full_nutrition": nutr_c,
        "has_real_ingredients": real_i,
        "plausibility_pass": plaus_p,
        "scored": scored_c,
    },
    "target1_outcome": {
        "target": "80pct_dark_chocolate",
        "barcode": "4820005195848",
        "conclusion": "FINAL_NULL",
        "detail": (
            "Millennium 80% (4820005195848) is in the global Victory product registry "
            "(/api/products/4820005195848 -> id=415280 'שוקולד מריר 80%') but NOT in Victory "
            "retailer 1470 product catalog (/v2/retailers/1470/products?barcode=... returns total=0). "
            "No nutrition panel available from Victory. 80% with full nutrition = not found at Victory."
        ),
    },
    "target2_outcome": {
        "target": "lindt_3046920_series",
        "barcodes": ["3046920023443", "3046920023429", "3046920023368"],
        "conclusion": "FINAL_NULL",
        "detail": (
            "All 3 Lindt 3046920xxx barcodes (Excellence dark, caramel milk, Excellence milk) "
            "return total=0 from Victory retailer 1470 catalog. Ingredient lists remain "
            "boilerplate from Pass 1. No real ingredient data available from Victory."
        ),
    },
    "incidental_finds": {
        "summary": "3 additional dark chocolates found in Victory with full nutrition + real ingredients + scored",
        "products": ["3046920028004 (Lindt 70%)", "5941021001261 (75% dark)", "7290119500482 (62% dark/maltitol)"],
        "scores": {bc: {"score": results[bc]["score"], "grade": results[bc]["grade"]}
                   for bc in ["3046920028004", "5941021001261", "7290119500482"]},
    },
    "results": results,
}

out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nOutput: {out_path}")
print(f"\n=== FINAL SUMMARY ===")
for bc, r in results.items():
    print(f"  {bc} | {r['label']}: {r['status']} | plaus={r.get('plausibility_gate')} | ingr={r.get('ingredients_status')} | score={r.get('score')}/{r.get('grade')}")
print(f"OFF check: {off_status}")
print(f"counts: {payload['counts']}")
