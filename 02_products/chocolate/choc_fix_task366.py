"""
TASK-366 — Two chocolate-tablet data fixes.

TASK A: Re-scrape 3 Lindt barcodes whose ingredients were captured as allergen
        boilerplate instead of real ingredients. Verify ct-025 ingredients are real.
        Re-score on corrected ingredients.

TASK B: Fill the 65-90% dark cocoa ladder gap (priority: genuine 70% and 80%).
        Scrape from Shufersal (primary), run plausibility gate, score via the
        existing chocolate lens.

Output: choc_tablets_fix_task366_<ts>.json  (data file only — NOT the frontend JSON)
OFF is banned. Missing data = NULL, not fabricated.
"""
from __future__ import annotations

import datetime
import glob
import json
import pathlib
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")
sys.path.insert(0, str(ROOT / "02_products" / "snack_bars"))
sys.path.insert(0, str(ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"))

from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw, parse_nutrition_numeric
from plausibility_gate import classify_chocolate
import run_task360_phase3 as P3

# ── Shufersal scraper config ──────────────────────────────────────────────────
BASE = "https://www.shufersal.co.il"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}
PAGE_DELAY = 1.2  # seconds between product-page fetches

TS = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / f"task366_{TS}" / "output"
BSIP2_DIR = ROOT / "02_products" / "chocolate" / "bsip2_outputs" / f"task366_{TS}" / "products"
for d in (BSIP1_DIR, BSIP2_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _get(url: str, timeout: int = 25) -> requests.Response | None:
    try:
        return requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


def scrape_product_page(code: str) -> dict | None:
    """
    Scrape a single Shufersal product by product-code (e.g. 'P_3046920023429').
    Returns parsed fields or None on HTTP failure.
    """
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url)
    if not r or r.status_code != 200:
        print(f"  [SKIP] {code} → HTTP {r.status_code if r else 'None'}")
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    product_url = r.url

    # ── ld+json ──
    ld_name, ld_gtin, ld_images, ld_brand = "", "", [], ""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                brand_obj = ld.get("brand", "")
                ld_brand = brand_obj.get("name", "") if isinstance(brand_obj, dict) else (brand_obj or "")
                ld_images = ld.get("image", [])
                if isinstance(ld_images, str):
                    ld_images = [ld_images]
                break
        except Exception:
            pass

    # ── nutrition ──
    nutr_raw = parse_nutrition_list(soup)
    nutr_src = extract_nutrition_raw(soup)

    # ── ingredients ──
    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:1400]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{30,})", text)
            if m:
                ingredients_raw = m.group(1)[:1400]
                break

    barcode = ld_gtin or code.replace("P_", "").replace("p_", "")
    weight_g = None
    if ld_name:
        for pat in (
            re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.I),
            re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.I),
            re.compile(r"(\d[\d,.]*)\s*g\b", re.I),
        ):
            m = pat.search(ld_name)
            if m:
                try:
                    val = float(m.group(1).replace(",", "."))
                    if "ק" in m.group(0):
                        val *= 1000
                    if 15 < val < 2000:
                        weight_g = val
                        break
                except ValueError:
                    pass

    return {
        "retailer_id": "shufersal",
        "source_url": product_url,
        "code": code,
        "scraped_at": datetime.datetime.utcnow().isoformat(),
        "name_he": ld_name,
        "brand": ld_brand,
        "barcode": barcode,
        "weight_g": weight_g,
        "nutrition": {
            "energy_kcal_raw": nutr_raw.get("energy", ""),
            "protein_raw": nutr_raw.get("protein", ""),
            "carbs_raw": nutr_raw.get("carbs", ""),
            "fat_raw": nutr_raw.get("fat", ""),
            "fiber_raw": nutr_raw.get("fiber", ""),
            "sodium_raw": nutr_raw.get("sodium", ""),
            "sugar_raw": nutr_raw.get("sugar", ""),
            "saturated_fat_raw": nutr_raw.get("saturated_fat", ""),
        },
        "nutrition_raw_source": nutr_src,
        "ingredients_raw": ingredients_raw,
        "image_urls": [u for u in ld_images[:3] if u],
    }


# ── Boilerplate detector ──────────────────────────────────────────────────────
ALLERGEN_BOILERPLATE = "כפי שרשום על גבי האריזה עלול להכיל"

def is_boilerplate(ingr: str) -> bool:
    return ALLERGEN_BOILERPLATE in (ingr or "")


def has_real_ingredients(ingr: str) -> bool:
    """True if ingredient string looks like a real ingredient list (has cocoa/food words)."""
    if not ingr or is_boilerplate(ingr):
        return False
    # Must have at least one real ingredient word
    real_markers = ["קקאו", "סוכר", "חלב", "שומן", "שמן", "חמאה", "וניל", "לציטין", "אמולגטור"]
    return any(m in ingr for m in real_markers)


# ── Score a product through the existing chocolate lens ──────────────────────

def score_product(p: dict, run_id: str) -> dict | None:
    """
    Run BSIP1 + BSIP2 through the existing chocolate scoring path.
    Returns a score record or None on failure.
    """
    name = p.get("name_he") or p.get("name", "")
    barcode = p.get("barcode", "")
    nutr_num = parse_nutrition_numeric(p["nutrition"])

    if nutr_num.get("energy_kcal") is None and nutr_num.get("carbohydrates_g") is None:
        print(f"  [NO_NUTRITION] {barcode} — cannot score")
        return None

    gate = P3.run_plausibility_gate(
        nutr_num, p.get("ingredients_raw", ""), barcode, p.get("weight_g")
    )
    if gate["verdict"] not in ("pass", "converted_pass"):
        print(f"  [GATE_FAIL] {barcode} → {gate['verdict']}: {gate.get('reason')}")
        return None

    meta = {
        "description": name,
        "name_truncated": name,
        "brand": p.get("brand", ""),
        "code": p.get("code", "P_" + barcode),
        "sku": barcode,
        "image_url": (p.get("image_urls") or [""])[0],
        "unit_description": "",
        "health_attrs": [],
        "all_cat_codes": [],
    }
    scraped = {
        "plausibility_gate": gate,
        "ingredients_raw": p.get("ingredients_raw", ""),
        "weight_g": p.get("weight_g"),
        "serving_g": None,
        "nutrition_numeric_per_100g": nutr_num,
    }
    bsip1 = P3.build_bsip1(meta, scraped, barcode, run_id)
    bsip1_path = BSIP1_DIR / f"bsip1_{barcode}.json"
    bsip1_path.write_text(json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8")

    res = P3.run_bsip2(bsip1_path, BSIP2_DIR)
    if res["status"] != "ok":
        print(f"  [BSIP2_ERROR] {barcode}: {res.get('error')}")
        return None

    tr = res["trace"]
    sc_val = tr.get("final_score_estimate", tr.get("score"))
    return {
        "barcode": barcode,
        "name": name,
        "brand": p.get("brand", ""),
        "score": round(sc_val, 1) if sc_val is not None else None,
        "grade": tr.get("grade_estimate", tr.get("grade")),
        "category": classify_chocolate(name),
        "engine_category": tr.get("category"),
        "plausibility_verdict": gate["verdict"],
        "kcal": nutr_num.get("energy_kcal"),
        "fat_g": nutr_num.get("fat_g"),
        "sat_fat_g": nutr_num.get("saturated_fat_g"),
        "sugar_g": nutr_num.get("sugars_g"),
        "sodium_mg": nutr_num.get("sodium_mg"),
        "protein_g": nutr_num.get("protein_g"),
        "fiber_g": nutr_num.get("dietary_fiber_g"),
        "ingredients_raw": p.get("ingredients_raw", ""),
        "image_url": (p.get("image_urls") or [""])[0],
        "retailer": p.get("retailer_id", "shufersal"),
        "source_url": p.get("source_url", ""),
        "scoring_trace": {
            "category": tr.get("category"),
            "sugar_g": nutr_num.get("sugars_g"),
            "sat_fat_g": nutr_num.get("saturated_fat_g"),
        },
    }


# ═════════════════════════════════════════════════════════════════════════════
# TASK A — Re-scrape the 4 target barcodes
# ═════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("TASK A — Re-scrape ingredient-boilerplate products")
print("="*70)

# Load the existing frontend JSON to get before-scores
frontend_path = ROOT / "bari-web" / "src" / "data" / "comparisons" / "chocolate_tablets_frontend_v1.json"
frontend = json.load(open(frontend_path, encoding="utf-8"))
before_scores = {p["barcode"]: {"id": p["id"], "score": p["score"], "grade": p["grade"]} for p in frontend["products"]}

TASK_A_TARGETS = [
    {"id": "ct-004", "barcode": "3046920023429", "code": "P_3046920023429", "name_expected": "שוקולד חלב חתיכות קרמל", "note": "Lindt caramel milk — 3046920 prefix"},
    {"id": "ct-005", "barcode": "3046920023368", "code": "P_3046920023368", "name_expected": "שוקולד חלב מעולה", "note": "Lindt 'מעולה' milk — verify name/brand"},
    {"id": "ct-006", "barcode": "3046920023443", "code": "P_3046920023443", "name_expected": "שוקולד מריר מעולה", "note": "Lindt 'מעולה' dark — verify name/brand"},
    {"id": "ct-025", "barcode": "7290112331984", "code": "P_7290112331984", "name_expected": "שוקולד פרה קראנצ' בסקויט", "note": "Verify real ingredients (has text but verify קקאו term)"},
]

RUN_ID = f"task366_{TS}"
task_a_results = []

for target in TASK_A_TARGETS:
    print(f"\n--- {target['id']} | {target['barcode']} | {target['note']}")
    time.sleep(PAGE_DELAY)
    p = scrape_product_page(target["code"])

    if p is None:
        task_a_results.append({
            "id": target["id"],
            "barcode": target["barcode"],
            "name_scraped": None,
            "name_expected": target["name_expected"],
            "brand_scraped": None,
            "barcode_name_mismatch": None,
            "ingredients_status": "SCRAPE_FAILED",
            "ingredients_corrected": None,
            "before_score": before_scores.get(target["barcode"], {}).get("score"),
            "before_grade": before_scores.get(target["barcode"], {}).get("grade"),
            "after_score": None,
            "after_grade": None,
            "score_changed": None,
            "note": "HTTP fetch failed — field is NULL",
        })
        continue

    name_scraped = p.get("name_he", "")
    brand_scraped = p.get("brand", "")
    ingr = p.get("ingredients_raw", "")

    print(f"  Scraped name : {name_scraped}")
    print(f"  Brand        : {brand_scraped}")
    print(f"  Barcode      : {p.get('barcode')}")
    print(f"  Ingredients  : {ingr[:200]}")

    # Barcode/name consistency check
    # 3046920 prefix is Lindt International (Switzerland) — expect Lindt brand
    mismatch_note = None
    if target["barcode"].startswith("3046920"):
        if brand_scraped and "לינדט" not in brand_scraped and "lindt" not in brand_scraped.lower():
            mismatch_note = f"3046920 barcode but brand={brand_scraped!r} — expected Lindt"
        # "מעולה" in Hebrew is an Elite (עלית) brand word, but these barcodes are 3046920 (Lindt)
        if "מעולה" in (name_scraped or "") and brand_scraped and "לינדט" in brand_scraped:
            mismatch_note = (mismatch_note or "") + " | name contains 'מעולה' (Elite association) but brand=Lindt — verify this is correct on-shelf"

    # Ingredients status
    if is_boilerplate(ingr):
        ingr_status = "STILL_BOILERPLATE"
        ingr_corrected = None
    elif has_real_ingredients(ingr):
        ingr_status = "REAL_INGREDIENTS"
        ingr_corrected = ingr
    elif ingr:
        ingr_status = "TEXT_BUT_UNVERIFIED"
        ingr_corrected = ingr
    else:
        ingr_status = "NULL"
        ingr_corrected = None

    print(f"  Ingr status  : {ingr_status}")

    # Re-score
    before = before_scores.get(target["barcode"], {})
    after_score_rec = None
    if ingr_corrected or ingr_status == "STILL_BOILERPLATE":
        # Still attempt scoring — the score is based on nutrition, ingredients affect D4 only
        after_score_rec = score_product(p, RUN_ID)

    task_a_results.append({
        "id": target["id"],
        "barcode": target["barcode"],
        "name_scraped": name_scraped,
        "name_expected": target["name_expected"],
        "brand_scraped": brand_scraped,
        "barcode_name_mismatch": mismatch_note,
        "ingredients_status": ingr_status,
        "ingredients_corrected": ingr_corrected,
        "before_score": before.get("score"),
        "before_grade": before.get("grade"),
        "after_score": after_score_rec["score"] if after_score_rec else None,
        "after_grade": after_score_rec["grade"] if after_score_rec else None,
        "score_changed": (
            after_score_rec["score"] != before.get("score") if after_score_rec else None
        ),
        "nutrition_per_100g": after_score_rec and {
            k: v for k, v in [
                ("kcal", after_score_rec.get("kcal")),
                ("fat_g", after_score_rec.get("fat_g")),
                ("sat_fat_g", after_score_rec.get("sat_fat_g")),
                ("sugar_g", after_score_rec.get("sugar_g")),
                ("sodium_mg", after_score_rec.get("sodium_mg")),
                ("protein_g", after_score_rec.get("protein_g")),
                ("fiber_g", after_score_rec.get("fiber_g")),
            ]
        },
        "retailer_source": "shufersal",
        "source_url": p.get("source_url", ""),
    })

print("\n=== TASK A SUMMARY ===")
for r in task_a_results:
    print(f"  {r['id']} | {r['barcode']} | ingr={r['ingredients_status']} | "
          f"score {r['before_score']}→{r['after_score']} | "
          f"grade {r['before_grade']}→{r['after_grade']} | "
          f"mismatch={r['barcode_name_mismatch']}")


# ═════════════════════════════════════════════════════════════════════════════
# TASK B — Fill 65-90% cocoa ladder gaps
# ═════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("TASK B — Fill 65-90% cocoa ladder (priority: 70% and 80%)")
print("="*70)

# Candidates: not in existing corpus, prioritised by cocoa %
TASK_B_TARGETS = [
    # Priority 1: genuine 70% (multiple products to ensure at least one gets real data)
    {"code": "P_3046920028004", "name_expected": "שוקולד מריר לינדט 70%", "cocoa_pct": 70, "priority": "HIGH"},
    {"code": "P_7290018893401", "name_expected": "צ'וקטה שוקולד מריר 70%", "cocoa_pct": 70, "priority": "HIGH"},
    {"code": "P_7290112914705", "name_expected": "שוקולד מריר מעולה 70%", "cocoa_pct": 70, "priority": "HIGH"},
    # Priority 2: 80%
    {"code": "P_4820005195848", "name_expected": "שוקולד מריר 80%", "cocoa_pct": 80, "priority": "HIGH"},
    # Mid-range: 72%, 74%, 75% (fill natural ladder steps)
    {"code": "P_7296073726562", "name_expected": "שוקולד מריר ללת\"ס 72%", "cocoa_pct": 72, "priority": "MED"},
    {"code": "P_4820005198597", "name_expected": "שוקולד מריר 74%", "cocoa_pct": 74, "priority": "MED"},
    {"code": "P_7296073747802", "name_expected": "שוקולד מריר פרימיום 75%", "cocoa_pct": 75, "priority": "MED"},
    {"code": "P_5941021001261", "name_expected": "שוקולד מריר 75%", "cocoa_pct": 75, "priority": "MED"},
    # Bonus: 62% (fills between existing 60% and 70%)
    {"code": "P_7290119500482", "name_expected": "טוסו שוקולד מריר 62%", "cocoa_pct": 62, "priority": "LOW"},
]

task_b_results = []
task_b_scored = []

for target in TASK_B_TARGETS:
    code = target["code"]
    print(f"\n--- {code} | {target['name_expected']} | {target['cocoa_pct']}% | {target['priority']}")
    time.sleep(PAGE_DELAY)
    p = scrape_product_page(code)

    if p is None:
        task_b_results.append({
            "code": code,
            "name_expected": target["name_expected"],
            "cocoa_pct_nominal": target["cocoa_pct"],
            "status": "SCRAPE_FAILED",
            "retailer": "shufersal",
        })
        print(f"  SCRAPE_FAILED")
        continue

    name = p.get("name_he", "")
    barcode = p.get("barcode", "")
    ingr = p.get("ingredients_raw", "")

    print(f"  Name     : {name}")
    print(f"  Barcode  : {barcode}")
    print(f"  Brand    : {p.get('brand')}")
    print(f"  Ingr     : {ingr[:150]}")

    # Score
    scored = score_product(p, RUN_ID)

    if scored is None:
        task_b_results.append({
            "code": code,
            "barcode": barcode,
            "name_scraped": name,
            "name_expected": target["name_expected"],
            "cocoa_pct_nominal": target["cocoa_pct"],
            "status": "NO_SCORE",
            "ingredients": ingr or None,
            "retailer": "shufersal",
            "source_url": p.get("source_url", ""),
        })
        continue

    rec = {
        "code": code,
        "barcode": barcode,
        "name": name,
        "brand": scored["brand"],
        "cocoa_pct_nominal": target["cocoa_pct"],
        "priority": target["priority"],
        "status": "SCORED",
        "score": scored["score"],
        "grade": scored["grade"],
        "engine_category": scored["engine_category"],
        "plausibility_verdict": scored["plausibility_verdict"],
        "nutrition_per_100g": {
            "energy_kcal": scored["kcal"],
            "fat_g": scored["fat_g"],
            "saturated_fat_g": scored["sat_fat_g"],
            "sugars_g": scored["sugar_g"],
            "sodium_mg": scored["sodium_mg"],
            "protein_g": scored["protein_g"],
            "dietary_fiber_g": scored["fiber_g"],
        },
        "ingredients": ingr or None,
        "image_url": scored["image_url"],
        "retailer": "shufersal",
        "source_url": scored["source_url"],
        "scoring_trace_signals": scored["scoring_trace"],
    }
    task_b_results.append(rec)
    task_b_scored.append(rec)
    print(f"  SCORED → {scored['score']} / {scored['grade']}")

print("\n=== TASK B SUMMARY ===")
for r in task_b_results:
    print(f"  {r.get('cocoa_pct_nominal')}% | {r.get('name', r.get('name_expected'))} | "
          f"status={r['status']} | score={r.get('score')} | grade={r.get('grade')}")


# ═════════════════════════════════════════════════════════════════════════════
# Cocoa ladder coverage after fix
# ═════════════════════════════════════════════════════════════════════════════

import re as _re

def _extract_pct(name: str) -> int | None:
    m = _re.search(r'(\d{2,3})%', name or "")
    return int(m.group(1)) if m else None

existing_pcds = {
    p["barcode"]: _extract_pct(p["name"])
    for p in frontend["products"]
}
from collections import Counter
existing_dist = Counter(v for v in existing_pcds.values() if v)
new_dist = Counter(
    r.get("cocoa_pct_nominal") for r in task_b_scored
    if r["status"] == "SCORED"
)
print("\n=== COCOA % LADDER COVERAGE ===")
print("Before (frontend):", dict(sorted(existing_dist.items())))
print("New (task B scored):", dict(sorted(new_dist.items())))
combined = dict(existing_dist)
for k, v in new_dist.items():
    combined[k] = combined.get(k, 0) + v
print("Combined:", dict(sorted(combined.items())))


# ═════════════════════════════════════════════════════════════════════════════
# Write output file
# ═════════════════════════════════════════════════════════════════════════════

# OFF check
OFF_CHECK = "PASS - no Open Food Facts data used; sources are direct Shufersal product page scrapes only"

out = {
    "run_id": RUN_ID,
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    "off_check": OFF_CHECK,
    "sources": ["shufersal (primary)"],
    "task_a": {
        "description": "Re-scrape 4 products with ingredient-boilerplate issue; corrected ingredients + re-score",
        "count_targets": len(TASK_A_TARGETS),
        "count_scraped_ok": sum(1 for r in task_a_results if r["ingredients_status"] != "SCRAPE_FAILED"),
        "count_real_ingredients_found": sum(1 for r in task_a_results if r["ingredients_status"] == "REAL_INGREDIENTS"),
        "count_still_boilerplate": sum(1 for r in task_a_results if r["ingredients_status"] == "STILL_BOILERPLATE"),
        "count_null": sum(1 for r in task_a_results if r["ingredients_status"] == "NULL"),
        "results": task_a_results,
    },
    "task_b": {
        "description": "Fill 65-90% dark cocoa ladder; priority 70% and 80%",
        "count_targets": len(TASK_B_TARGETS),
        "count_scored": len(task_b_scored),
        "count_failed": len(task_b_results) - len(task_b_scored),
        "cocoa_pct_coverage_before": dict(sorted(existing_dist.items())),
        "cocoa_pct_coverage_new": dict(sorted(new_dist.items())),
        "cocoa_pct_coverage_combined": dict(sorted(combined.items())),
        "results": task_b_results,
    },
    "bsip1_dir": str(BSIP1_DIR),
    "bsip2_dir": str(BSIP2_DIR),
    "plausibility_gate": "run_task360_phase3.run_plausibility_gate — per-100g sanity enforced",
    "scoring_engine": "score_chocolate_task362.py lens (unchanged) via run_task360_phase3",
    "integration_status": "DATA_ONLY — do not integrate to frontend; awaiting orchestrator verification",
}

out_path = ROOT / "02_products" / "chocolate" / f"choc_tablets_fix_task366_{TS}.json"
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nOutput written: {out_path}")
print(f"Task A: {out['task_a']['count_scraped_ok']}/{out['task_a']['count_targets']} scraped, "
      f"{out['task_a']['count_real_ingredients_found']} real ingr, "
      f"{out['task_a']['count_still_boilerplate']} still boilerplate")
print(f"Task B: {out['task_b']['count_scored']}/{out['task_b']['count_targets']} scored")
print(f"OFF check: {OFF_CHECK}")
