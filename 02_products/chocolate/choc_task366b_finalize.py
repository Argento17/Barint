"""
TASK-366 Pass 2 Victory — finalize results.

Confirmed findings:
- 3046920028004 (Lindt 70%): FOUND in v2 API — full nutrition + real ingredients
- 5941021001261 (75% dark): FOUND in v2 API — full nutrition + real ingredients
- 7290119500482 (62% dark): FOUND in v2 API — full nutrition + real ingredients
- 4820005195848 (Millennium 80%): NOT in Victory retailer 1470 product catalog (total=0)
- 3046920023443/029/368 (Lindt dark/caramel/milk): NOT in Victory catalog (total=0)
- 4820005198597 (Millennium 74%): NOT in Victory catalog (total=0)

Note: the /api/products/{barcode} endpoint is a GLOBAL product registry (all Israeli barcodes),
not Victory-specific stock. total=0 from /v2/retailers/1470/products?barcode=... means not available.

Data source for nutrition: /v2/retailers/1470/products?barcode={bc}&appId=4 (direct REST, no browser)
"""
import sys, re, json, pathlib, datetime, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VICTORY_BASE = "https://www.victoryonline.co.il"
RETAILER_ID = 1470

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

def parse_nutr_json(nv: dict) -> dict:
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

def plausibility_check(n: dict, bc: str) -> tuple[bool, str]:
    if not n:
        return False, "NO_NUTRITION"
    required = {"energy", "fat", "carbs"}
    missing = required - set(n.keys())
    if missing:
        return False, f"MISSING_KEYS:{missing}"
    e = n["energy"]; f = n["fat"]; c = n["carbs"]
    p = n.get("protein", 0)
    s = n.get("sugar", 0)
    so = n.get("saturated_fat", 0)
    na = n.get("sodium", 0)
    # Chocolate per-100g ranges
    if not (400 <= e <= 700):
        return False, f"ENERGY_OOB:{e}"
    if not (20 <= f <= 65):
        return False, f"FAT_OOB:{f}"
    if not (0 <= c <= 65):
        return False, f"CARBS_OOB:{c}"
    ms = f + c + p
    if not (50 <= ms <= 115):
        return False, f"MACRO_SUM_OOB:{ms}"
    if s > c + 2:
        return False, f"SUGAR_EXCEEDS_CARBS:{s}>{c}"
    if so > f + 1:
        return False, f"SATFAT_EXCEEDS_FAT:{so}>{f}"
    return True, "PASS"

def is_boilerplate(s: str) -> bool:
    if not s:
        return True
    # Real ingredients contain substance words
    substance_words = ["קקאו", "סוכר", "חלב", "לציטין", "שומן", "שקדים", "אגוז", "קמח", "מלח", "חמאה", "מלטיטול"]
    if any(w in s for w in substance_words):
        return False
    return True

# ── Fetch the 3 confirmed products from Victory ────────────────────────────────
print("=== Fetching confirmed Victory products ===", flush=True)

found_data = {}
for bc in ["3046920028004", "5941021001261", "7290119500482"]:
    r = requests.get(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products?barcode={bc}&appId=4", timeout=15)
    data = r.json()
    if data.get("total", 0) > 0:
        p = data["products"][0]
        lang1 = (p.get("data") or {}).get("1") or {}
        ingr = lang1.get("ingredients") or lang1.get("componentsString") or ""
        nutr = parse_nutr_json(p.get("nutritionValues") or {})
        found_data[bc] = {
            "nutritionValues_raw": p.get("nutritionValues"),
            "ingredients": ingr,
            "nutrition": nutr,
            "productId": p.get("id"),
            "name_from_api": (p.get("data") or {}).get("1", {}).get("shortDescription", ""),
        }
        print(f"  {bc}: ingr={ingr[:80]} nutr={nutr}", flush=True)
    else:
        print(f"  {bc}: UNEXPECTED total=0 — aborting", flush=True)

# ── Build full results ────────────────────────────────────────────────────────
ALL_TARGETS = {
    "4820005195848": {"label": "Millennium 80%",         "task": "TARGET1"},
    "3046920023443": {"label": "Lindt Excellence dark",  "task": "TARGET2"},
    "3046920023429": {"label": "Lindt caramel milk",     "task": "TARGET2"},
    "3046920023368": {"label": "Lindt Excellence milk",  "task": "TARGET2"},
    "3046920028004": {"label": "Lindt 70%",              "task": "TARGET1"},
    "4820005198597": {"label": "Millennium 74%",         "task": "TARGET1"},
    "5941021001261": {"label": "75% dark",               "task": "TARGET1"},
    "7290119500482": {"label": "62% dark",               "task": "TARGET1"},
}

results = {}
for bc, info in ALL_TARGETS.items():
    if bc in found_data:
        fd = found_data[bc]
        nutr = fd["nutrition"]
        ingr = fd["ingredients"]
        bplate = is_boilerplate(ingr)
        plaus_ok, plaus_reason = plausibility_check(nutr, bc)
        results[bc] = {
            "barcode": bc,
            "label": info["label"],
            "task": info["task"],
            "status": "FOUND_AND_SCRAPED",
            "source": "victory",
            "source_endpoint": f"/v2/retailers/1470/products?barcode={bc}&appId=4",
            "product_name_victory": info.get("name_from_api", ""),
            "nutrition": nutr,
            "ingredients": ingr or None,
            "ingredients_status": (
                "REAL_INGREDIENTS" if ingr and not bplate else
                "BOILERPLATE" if ingr else "NULL"
            ),
            "has_full_nutrition": bool(nutr.get("energy") and nutr.get("fat") and nutr.get("carbs")),
            "plausibility_gate": f"PASS" if plaus_ok else f"FAIL:{plaus_reason}",
            "plausibility_detail": plaus_reason,
        }
    else:
        results[bc] = {
            "barcode": bc,
            "label": info["label"],
            "task": info["task"],
            "status": "NOT_IN_VICTORY_CATALOG",
            "source": "victory",
            "source_endpoint": f"/v2/retailers/1470/products?barcode={bc}&appId=4",
            "product_name_victory": None,
            "nutrition": None,
            "ingredients": None,
            "ingredients_status": "NULL",
            "has_full_nutrition": False,
            "plausibility_gate": "NOT_APPLICABLE",
            "plausibility_detail": "Product not in Victory retailer 1470 catalog (total=0)",
        }

print(f"\n=== Plausibility Results ===", flush=True)
for bc, r in results.items():
    print(f"  {bc}: {r['status']} | plaus={r['plausibility_gate']} | ingr={r['ingredients_status']}", flush=True)

# ── Score via chocolate lens ──────────────────────────────────────────────────
print("\n=== Scoring ===", flush=True)
import sys as _sys
_sys.path.insert(0, str(pathlib.Path(r"C:\Bari\02_products\chocolate")))

try:
    import run_task360_phase3 as P3
    scorer_ok = True
    print("  Scorer loaded OK", flush=True)
except ImportError as e:
    scorer_ok = False
    print(f"  Scorer not available: {e}", flush=True)

for bc, r in results.items():
    if r["status"] != "FOUND_AND_SCRAPED" or r["plausibility_gate"] != "PASS":
        r["score"] = None
        r["grade"] = None
        continue
    if not scorer_ok:
        r["score"] = None
        r["grade"] = None
        continue
    try:
        bsip1 = P3.build_bsip1(
            barcode=bc,
            name=r.get("product_name_victory") or r["label"],
            nutrition=r["nutrition"],
            ingredients=r.get("ingredients") or "",
            source="victory_pass2",
        )
        scored = P3.run_bsip2(bsip1)
        r["score"] = scored.get("score")
        r["grade"] = scored.get("grade")
        r["score_trace"] = scored.get("trace", {})
        print(f"  {bc} ({r['label']}): score={r['score']} grade={r['grade']}", flush=True)
    except Exception as e:
        r["score"] = None
        r["grade"] = None
        print(f"  {bc}: scoring error — {e}", flush=True)

# ── OFF check ────────────────────────────────────────────────────────────────
off_violations = []
for bc, r in results.items():
    for k, v in r.items():
        if isinstance(v, str) and "openfoodfacts" in v.lower():
            off_violations.append(f"{bc}.{k}")
off_status = "PASS" if not off_violations else f"FAIL:{off_violations}"

# ── Write output ──────────────────────────────────────────────────────────────
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
out_path = pathlib.Path(r"C:\Bari\02_products\chocolate") / f"choc_tablets_fix_task366b_{ts}.json"

# Counts for return contract
found_count = sum(1 for r in results.values() if r["status"] == "FOUND_AND_SCRAPED")
nutrition_count = sum(1 for r in results.values() if r.get("has_full_nutrition"))
real_ingr_count = sum(1 for r in results.values() if r.get("ingredients_status") == "REAL_INGREDIENTS")
plaus_count = sum(1 for r in results.values() if r.get("plausibility_gate") == "PASS")
scored_count = sum(1 for r in results.values() if r.get("score") is not None)

payload = {
    "task": "TASK-366 Pass 2 Victory probe",
    "run_ts": ts,
    "retailer": "victory",
    "retailer_id": RETAILER_ID,
    "off_check": off_status,
    "counts": {
        "targets_attempted": len(ALL_TARGETS),
        "found_in_catalog": found_count,
        "not_in_catalog": len(ALL_TARGETS) - found_count,
        "has_full_nutrition": nutrition_count,
        "has_real_ingredients": real_ingr_count,
        "plausibility_pass": plaus_count,
        "scored": scored_count,
    },
    "findings": {
        "target1_80pct": {
            "barcode": "4820005195848",
            "conclusion": "NOT_IN_VICTORY_CATALOG",
            "note": "Millennium 80% present in global product registry (/api/products/) but not stocked in Victory retailer 1470",
        },
        "target2_lindt_series": {
            "3046920023443": "NOT_IN_VICTORY_CATALOG",
            "3046920023429": "NOT_IN_VICTORY_CATALOG",
            "3046920023368": "NOT_IN_VICTORY_CATALOG",
            "note": "All 3 Lindt 3046920xxx barcodes absent from Victory retailer 1470",
        },
        "incidental_finds": [
            bc for bc, r in results.items() if r["status"] == "FOUND_AND_SCRAPED"
        ],
    },
    "results": results,
}

# Remove large raw nutritionValues from payload (it's in findings)
out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nOutput: {out_path}", flush=True)

print(f"\n{'='*60}", flush=True)
print("FINAL SUMMARY", flush=True)
print(f"{'='*60}", flush=True)
print(f"Targets attempted: {len(ALL_TARGETS)}", flush=True)
print(f"Found in Victory catalog: {found_count}/{len(ALL_TARGETS)}", flush=True)
print(f"Full nutrition panel: {nutrition_count}", flush=True)
print(f"Real ingredients: {real_ingr_count}", flush=True)
print(f"Plausibility PASS: {plaus_count}", flush=True)
print(f"Scored: {scored_count}", flush=True)
print(f"OFF check: {off_status}", flush=True)
print(f"\nPer-product:", flush=True)
for bc, r in results.items():
    print(
        f"  {bc} | {r['label']}: {r['status']} | "
        f"plaus={r.get('plausibility_gate')} | "
        f"ingr={r.get('ingredients_status')} | "
        f"score={r.get('score')}/{r.get('grade')}",
        flush=True
    )
print(f"\nOutput file: {out_path}", flush=True)
