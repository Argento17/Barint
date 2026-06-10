"""
Build salty_snacks_frontend_v2.json from BSIP2 run_salty_snacks_002 traces.
TASK-216 — Extrusion NOVA Detection Fix. EV-043 signal active.
"""
import sys, io, json, pathlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

TRACES_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002\products")
BSIP1_DIR  = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")
OUT_PATH   = pathlib.Path(r"C:\Bari\02_products\salty_snacks\salty_snacks_frontend_v2.json")
OUT_WEB    = pathlib.Path(r"C:\bari\bari-web\src\data\comparisons\salty_snacks_frontend_v2.json")


def grade_from_score(score) -> str:
    if score is None: return "?"
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"


def confidence_badge(lvl) -> str:
    if lvl in ("sufficient", "high"): return "verified"
    return "partial"


def confidence_label(lvl) -> str:
    if lvl in ("sufficient", "high"): return "נתונים מלאים"
    return "נתונים חלקיים"


def retailer_he(r: str) -> str:
    return {"shufersal": "שופרסל", "yohananof": "יוחננוף",
            "carrefour": "קרפור"}.get(r, r)


def load_bsip1() -> dict:
    by_pid = {}
    for f in BSIP1_DIR.glob("bsip1_snack_*.json"):
        d = json.loads(f.read_text("utf-8"))
        pid = d.get("canonical_product_id")
        if pid:
            by_pid[pid] = d
    return by_pid


def load_traces() -> list:
    out = []
    for pid_dir in TRACES_DIR.iterdir():
        tp = pid_dir / "bsip2_trace.json"
        if tp.exists():
            out.append(json.loads(tp.read_text("utf-8")))
    return out


def build_insight_line(trace, b1) -> str:
    signals = trace.get("L1_observed_signals") or {}
    nova = trace.get("nova_proxy")
    score = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate", "?")
    fat_g = signals.get("fat_g")
    sodium_mg = signals.get("sodium_mg")
    fiber_g = signals.get("dietary_fiber_g")
    caps = trace.get("caps_applied") or []
    pens = trace.get("penalties_applied") or []

    parts = []

    # Primary: binding cap story
    if caps:
        top_cap = caps[0].get("rule", "")
        if "SODIUM" in top_cap and sodium_mg:
            parts.append(f"{round(sodium_mg)} מ\"ג נתרן ל-100 גרם")
        elif "SUGAR" in top_cap:
            sugar_g = signals.get("sugars_g")
            if sugar_g:
                parts.append(f"{round(sugar_g, 1)} גרם סוכר ל-100 גרם")
        elif "NOVA" in top_cap:
            parts.append(f"NOVA {nova} — עיבוד גבוה")

    # Secondary: fat
    if fat_g and fat_g > 25 and "שומן" not in " ".join(parts):
        parts.append(f"{round(fat_g)} גרם שומן ל-100 גרם")

    # Sodium fact always
    if sodium_mg and not any("נתרן" in p for p in parts):
        parts.append(f"{round(sodium_mg)} מ\"ג נתרן")

    # Fiber bonus
    if fiber_g and fiber_g >= 7 and not any("סיבים" in p for p in parts):
        parts.append(f"{round(fiber_g, 1)} גרם סיבים")

    if not parts:
        parts.append(f"ציון {round(score)}/{grade}" if score else "נתונים חלקיים")

    return " — ".join(parts[:3])


def main():
    bsip1_by_pid = load_bsip1()
    traces = load_traces()
    print(f"Traces loaded: {len(traces)}, BSIP1 records: {len(bsip1_by_pid)}")

    products = []
    skipped = {}

    for trace in traces:
        ref = trace.get("input_reference") or {}
        pid = ref.get("canonical_product_id") or trace.get("canonical_product_id") or ""
        score = trace.get("final_score_estimate")
        suf = trace.get("data_sufficiency")

        if suf == "insufficient" or score is None:
            skipped[pid] = "insufficient_data"
            continue

        b1 = bsip1_by_pid.get(pid, {})
        signals = trace.get("L1_observed_signals") or {}
        grade = grade_from_score(score)

        name_he = (ref.get("product_name_he") or ref.get("canonical_name_he")
                   or b1.get("canonical_name_he") or "")
        brand = b1.get("brand") or ref.get("brand") or ""
        retailers = b1.get("source_retailers") or ["unknown"]
        retailer = retailers[0]
        sub_pool = b1.get("sub_pool") or "chips"
        nova = trace.get("nova_proxy")

        conf_raw = trace.get("confidence_band") or b1.get("data_sufficiency") or "partial"
        img_urls = b1.get("image_urls") or []
        image_url = img_urls[0] if img_urls else b1.get("image_url") or ""

        nutrition = {
            "energyKcal": signals.get("energy_kcal"),
            "protein":    signals.get("protein_g"),
            "fat":        signals.get("fat_g"),
            "carbs":      signals.get("carbohydrates_g"),
            "fiber":      signals.get("dietary_fiber_g"),
            "sodium":     signals.get("sodium_mg"),
            "sugar":      signals.get("sugars_g"),
            "saturatedFat": signals.get("fat_saturated_g"),
        }

        # Limiting factors from caps / penalties
        limiting = []
        for cap in (trace.get("caps_applied") or []):
            rule = cap.get("rule", "")
            if "SODIUM" in rule: limiting.append("sodium")
            elif "SUGAR" in rule: limiting.append("sugar")
            elif "NOVA" in rule: limiting.append("processing")
            elif "SAT_FAT" in rule: limiting.append("saturated_fat")
        for pen in (trace.get("penalties_applied") or []):
            rule = pen.get("rule", "")
            if "HP_FAT" in rule and "fat" not in limiting: limiting.append("fat")
            elif "SEED_OIL" in rule and "seed_oil" not in limiting: limiting.append("seed_oil")
            elif "LONG" in rule and "ingredient_count" not in limiting: limiting.append("ingredient_count")
        limiting = list(dict.fromkeys(limiting))[:4]

        insight = build_insight_line(trace, b1)
        row_verdict = f"{name_he}: {insight}."

        record = {
            "id": pid,
            "name": name_he,
            "brand": brand,
            "imageUrl": image_url,
            "score": round(score),
            "grade": grade,
            "insightLine": insight,
            "confidence": confidence_badge(conf_raw),
            "subPool": sub_pool,
            "novaGroup": nova,
            "retailer": retailer,
            "retailer_he": retailer_he(retailer),
            "limitingFactors": limiting,
            "ingredientCount": signals.get("ingredient_count") or 0,
            "expansion": {
                "nutrition": nutrition,
                "ingredients": b1.get("ingredients_text_he") or "",
                "confidenceLabel": confidence_label(conf_raw),
                "servingNote": "ל-100 גרם",
            },
            "rowVerdict": row_verdict,
            "provenance": "bsip1_manual_corpus",
        }
        products.append(record)

    products.sort(key=lambda p: -(p.get("score") or 0))

    from collections import Counter
    grade_dist = dict(Counter(p["grade"] for p in products))
    subpool_dist = dict(Counter(p["subPool"] for p in products))
    nova_dist = dict(Counter(str(p["novaGroup"]) for p in products))
    retailer_dist = dict(Counter(p["retailer"] for p in products))

    output = {
        "_meta": {
            "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "category": "salty-snacks",
            "category_he": "חטיפים מלוחים",
            "run_id": "run_salty_snacks_002",
            "product_count": len(products),
            "scored_count": len(products),
            "schema": "BariProductVM[]",
            "version": "v2",
            "change_note": "EV-043 industrial-extrusion NOVA 4 signal (TASK-216). Bamba and all puffed-subpool extruded snacks correctly classified NOVA 4.",
            "sub_pools": ["chips", "popcorn", "puffed", "baked", "rice_cakes", "pretzels"],
            "provenance": (
                "TASK-213 + TASK-216 salty snacks category launch with extrusion fix. "
                f"Corpus: {len(products)} products after dedup. "
                f"Retailers: {dict(retailer_dist)}. "
                f"Grade dist: {grade_dist}. NOVA dist: {nova_dist}."
            ),
            "grade_distribution": grade_dist,
            "subpool_distribution": subpool_dist,
            "nova_distribution": nova_dist,
            "retailer_breakdown": dict(retailer_dist),
        },
        "products": products,
    }

    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written: {OUT_PATH}")

    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written: {OUT_WEB}")
    print(f"Total products: {len(products)}")
    print(f"Grade distribution: {grade_dist}")
    print(f"Sub-pool distribution: {subpool_dist}")
    print(f"NOVA distribution: {nova_dist}")
    print(f"Skipped: {len(skipped)} — {skipped}")


if __name__ == "__main__":
    main()
