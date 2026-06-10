"""
Build juices_frontend_v1.json from BSIP2 run_juices_001 traces.
TASK-214.

Frontend fields:
  id, name, brand, score, grade, retailer(s), imageUrl, insightLine,
  limitingFactors, subPool, confidence, volumeMl, sugarPer100ml,
  fruitContentPct, novaGroup.

Insight lines are derived from real trace data — no fabrication.
"""
from __future__ import annotations
import sys, json, pathlib, datetime, re

ROOT = pathlib.Path(r"C:\Bari")
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / "run_juices_001" / "output"
BSIP2_DIR = ROOT / "02_products" / "juices" / "bsip2_outputs" / "run_juices_001" / "products"
WEB_OUT = ROOT / "bari-web" / "src" / "data" / "comparisons"
LOCAL_OUT = ROOT / "02_products" / "juices"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Insight line generation from trace data ────────────────────────────────────
# Template rules — derive from actual scores and nutrition signals.
# These are NOT fabricated: they are derived from the sugar_per_100ml, nova, and score.

def insight_line(name: str, sp: str, score: float, grade: str,
                 sugar: float | None, nova: int | None,
                 kcal: float | None, fruit_pct: float | None) -> str:
    """Generate insight line from real trace signals."""
    s = sugar or 0.0
    k = kcal or 0.0

    # Fresh-squeezed / cold-pressed — best in category
    if nova == 1 and grade in ("A", "B"):
        return f"הקרוב ביותר לפרי שלם — עיבוד מינימלי, {s:.1f}ג סוכר ל-100מ\"ל (הטוב בקטגוריה)"
    if nova == 1 and grade == "C":
        return f"עיבוד מינימלי, אך {s:.0f}ג סוכר ל-100מ\"ל — הסוכר נשאר גם ב\"סחוט קר\""

    # Lemon juice — special (very low sugar, acidic)
    if "לימון" in name and s < 4.0:
        return f"חמוץ ונמוך בסוכר ({s:.1f}ג/100מ\"ל) — ממיר, לא שייה ישירה"

    # Grape tiroush — very high sugar
    if ("תירוש" in name or "ענבים" in name) and s > 14.0:
        return f"{s:.0f}ג סוכר ל-100מ\"ל — כוס 200מ\"ל מכילה {s*2:.0f}ג סוכר, יותר מקולה"

    # 100% juice with natural sugars in normal range
    if sp == "juice_100" and nova == 3 and 7.0 <= s <= 11.0:
        return f"100% פרי, {s:.1f}ג סוכר ל-100מ\"ל — ללא סיבים, ללא תחושת שובע"

    # 100% juice high sugar (e.g. grape)
    if sp == "juice_100" and s > 11.0:
        return f"100% מיץ אך {s:.0f}ג סוכר ל-100מ\"ל — ריכוז מתוק כמו משקאות ממותקים"

    # Nectar — added sugar on top of fruit sugar
    if sp == "nectar" and grade == "C":
        return f"נקטר: סוכר מוסף על גבי סוכר הפרי — {s:.0f}ג/100מ\"ל, {s*2:.0f}ג בכוס"

    # Nectar that looks lower in sugar (concentrate-sweetened)
    if sp == "nectar" and s < 10.0:
        return f"נקטר: מראית עין — גם ריכוז פרי הוא סוכר, {s:.1f}ג/100מ\"ל"

    # Fruit drink — low fruit, mostly water + sugar
    if sp == "fruit_drink":
        pct_str = f", {fruit_pct:.0f}% פרי" if fruit_pct else ""
        return f"משקה פירות{pct_str} — בעיקר מים וסוכר, {s:.0f}ג/100מ\"ל"

    # Smoothie
    if sp == "smoothie":
        return f"שייק עם סיבים ({s:.1f}ג סוכר) — טוב מנקטר, אך לא מחליף פרי שלם"

    # Default
    return f"{s:.1f}ג סוכר ל-100מ\"ל — קרא/י את התווית לפני הבחירה"


def limiting_factors(sp: str, sugar: float | None, nova: int | None,
                     fruit_pct: float | None) -> list[str]:
    """Derive limiting factors from real trace signals."""
    factors = []
    s = sugar or 0.0

    # Sugar load is always a factor for juices
    if s >= 14.0:
        factors.append("סוכר גבוה מאוד")
    elif s >= 10.0:
        factors.append("סוכר גבוה")
    elif s >= 6.0:
        factors.append("סוכר טבעי — אין סיבים")

    # Processing
    if nova == 4:
        factors.append("עיבוד גבוה — תוספים ו/או סוכר מוסף")
    elif nova == 3:
        factors.append("ללא סיבים — עיבוד סטנדרטי")

    # Fruit content
    if sp == "fruit_drink":
        factors.append("תכולת פרי נמוכה")
    elif sp == "nectar":
        factors.append("נקטר — לא 100% פרי")

    # Satiety
    if sp != "smoothie":
        factors.append("ללא שובע — נוזלי")

    return factors[:3]  # cap at 3


def confidence_from_trust(b1: dict) -> str:
    """Map trust level to display confidence."""
    trust = b1.get("canonical_trust_level", "medium")
    nutrition_conf = (b1.get("confidence") or {}).get("nutrition_confidence", "")
    if "off_candidate" in str(b1.get("canonical_risk_flags", [])) and "inferred_per_100ml" not in nutrition_conf:
        return "medium"
    if "fdc_type_reference" in str(b1.get("canonical_risk_flags", [])):
        return "low"
    return {"high": "high", "medium": "medium", "low": "low"}.get(trust, "medium")


def build_frontend():
    products = []
    # Collect all BSIP2 traces
    for prod_dir in sorted(BSIP2_DIR.iterdir()):
        tf = prod_dir / "bsip2_trace.json"
        if not tf.exists():
            continue
        with open(tf, encoding="utf-8") as f:
            trace = json.load(f)

        barcode = (trace.get("input_reference") or {}).get("barcode", "")
        b1f = BSIP1_DIR / f"bsip1_{barcode}.json"
        if not b1f.exists():
            continue
        with open(b1f, encoding="utf-8") as f:
            b1 = json.load(f)

        score = trace.get("final_score_estimate")
        grade = trace.get("grade_estimate")
        if score is None or grade is None:
            continue

        nn = b1.get("normalized_nutrition_per_100g") or {}
        sugar = nn.get("sugars_g")
        kcal = nn.get("energy_kcal")
        nova = b1.get("nova_group_candidate")
        sp = b1.get("juice_sub_pool", "juice_100")
        vol = b1.get("volume_ml") or b1.get("package_size_ml")
        fruit_pct = b1.get("fruit_content_pct")
        name = b1.get("canonical_name_he", "")
        brand = b1.get("brand")
        retailers = b1.get("source_retailers") or []
        image = b1.get("image_url")

        # Generate insight line from real signals
        il = insight_line(name, sp, score, grade, sugar, nova, kcal, fruit_pct)
        lf = limiting_factors(sp, sugar, nova, fruit_pct)
        conf = confidence_from_trust(b1)

        # Sub-pool: merge cold_pressed into juice_100 if < 3 products
        # (we have exactly 3, so keep it)
        display_pool = sp

        # Routing flag for misrouted product
        routing_flag = None
        if trace.get("category") not in ("beverage", "default", None):
            routing_flag = f"engine_routed_to_{trace.get('category')}_not_beverage"

        product_entry = {
            "id": b1.get("canonical_product_id"),
            "barcode": barcode,
            "name": name,
            "brand": brand,
            "score": round(score, 1),
            "grade": grade,
            "retailers": retailers,
            "imageUrl": image,
            "insightLine": il,
            "limitingFactors": lf,
            "subPool": display_pool,
            "confidence": conf,
            "volumeMl": vol,
            "sugarPer100ml": round(sugar, 1) if sugar is not None else None,
            "kcalPer100ml": round(kcal, 0) if kcal is not None else None,
            "fruitContentPct": fruit_pct,
            "novaGroup": nova,
        }
        if routing_flag:
            product_entry["routingFlag"] = routing_flag

        products.append(product_entry)

    # Sort by score descending
    products.sort(key=lambda p: p["score"], reverse=True)

    # Sub-pool summary
    pool_counts = {}
    for p in products:
        pool_counts[p["subPool"]] = pool_counts.get(p["subPool"], 0) + 1

    grade_dist = {}
    for p in products:
        grade_dist[p["grade"]] = grade_dist.get(p["grade"], 0) + 1

    sugar_vals = [p["sugarPer100ml"] for p in products if p["sugarPer100ml"] is not None]

    frontend = {
        "schemaVersion": "bari_frontend_v1",
        "categorySlug": "juices",
        "categoryNameHe": "מיצים ומשקאות פירות",
        "pipelineRun": "run_juices_001",
        "generatedAt": datetime.datetime.now().isoformat(),
        "nutritionUnit": "per_100ml",
        "nutritionUnitNote": "ערכי התזונה הם ל-100 מ\"ל — הקטגוריה היחידה בבארי שנמדדת בנפח",
        "categoryNote": "מיץ פרי אינו פרי. ב-200 מ\"ל מיץ תפוזים יש כ-17 גרם סוכר, ללא סיבים וללא תחושת שובע. הציון משקף את עומס הסוכר, מידת העיבוד, ותכולת הפרי האמיתית — לא את ה'בריאות' שעל תווית הקדמית.",
        "subPoolTaxonomy": {
            "juice_100": "100% מיץ פירות",
            "nectar": "נקטר (25–99% פרי)",
            "fruit_drink": "משקה פירות (<25% פרי)",
            "smoothie": "שייק פירות",
            "cold_pressed": "סחוט קר"
        },
        "poolCounts": pool_counts,
        "gradeDistribution": grade_dist,
        "sugarRangeG100ml": {
            "min": round(min(sugar_vals), 1) if sugar_vals else None,
            "max": round(max(sugar_vals), 1) if sugar_vals else None,
        },
        "totalProducts": len(products),
        "products": products,
    }

    # Write local
    local_path = LOCAL_OUT / "juices_frontend_v1.json"
    with open(local_path, "w", encoding="utf-8") as f:
        json.dump(frontend, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(products)} products → {local_path}")

    # Copy to bari-web
    WEB_OUT.mkdir(parents=True, exist_ok=True)
    web_path = WEB_OUT / "juices_frontend_v1.json"
    with open(web_path, "w", encoding="utf-8") as f:
        json.dump(frontend, f, ensure_ascii=False, indent=2)
    print(f"Copied → {web_path}")

    # Print sample insights
    print("\n=== Sample Insight Lines ===")
    for p in products[:10]:
        print(f"  [{p['grade']}] {p['score']:.1f}  {p['name'][:40]}")
        print(f"       → {p['insightLine']}")

    return frontend


if __name__ == "__main__":
    build_frontend()
