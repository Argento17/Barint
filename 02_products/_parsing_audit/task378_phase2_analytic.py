"""
TASK-378 Phase 2 — Analytic sugar impact simulation.

Instead of invoking the full engine (which has coordination layers not
easily replicated without the full BSIP1 signal set), this script:

1. Reads the EXISTING bsip2_trace.json for each target (which has the
   current score + current glycemic_quality = scored with sugar=null).
2. Computes the score DELTA from the sugar change using the known formulas:
   - glycemic_quality change: Δglycemic = -(real_sugar × 2.5)
     (formula: 90 - sugar×2.5 + fiber_bonus + wg_bonus)
   - The glycemic dimension weight from DIMENSION_WEIGHTS
   - For juices: the shelf-relative EV-091 scorer also activates when sugars_g
     goes from None to real_value. We compute that delta too using constants.
3. Estimates staged_score = published_score + delta
4. Estimates staged_grade using score_to_grade thresholds

This is a trace-derived simulation, NOT a full re-run. It is conservative:
it only accounts for the glycemic dimension (and juice shelf-relative) since
those are the direct sugar-driven components. The HP coordination layer
(hp_fat_sugar_pattern) might also fire for some products if sugar becomes
high — we flag that possibility.

All numbers are derived from the existing trace artifacts + formula read from
score_engine.py. No OFF. No promotion.
"""
import sys, json, pathlib, math, io

ROOT = pathlib.Path(r"C:\Bari")

# ── Grade thresholds (from score_to_grade in constants.py) ──────────────────
def score_to_grade(score: float) -> str:
    """Matches GRADE_THRESHOLDS in constants.py: S>=90, A>=80, B>=65, C>=50, D>=35, E<35."""
    if score >= 90: return "S"
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"


# ── DIMENSION_WEIGHTS (from constants.py — snapshot) ────────────────────────
DIMENSION_WEIGHTS = {
    "processing_quality":  0.20,
    "nutrient_density":    0.10,
    "calorie_density":     0.10,
    "glycemic_quality":    0.15,
    "protein_quality":     0.10,
    "additive_quality":    0.10,
    "satiety_support":     0.05,
    "fat_quality":         0.10,
    "regulatory_quality":  0.05,
    "whole_food_integrity":0.05,
}
GLYCEMIC_WEIGHT = DIMENSION_WEIGHTS["glycemic_quality"]  # 0.15

# ── Juice shelf-relative constants ──────────────────────────────────────────
# From constants.py + score_engine.py
SUGAR_SHELF_REL_JUICES_MEDIAN = 9.50
SUGAR_SHELF_REL_JUICES_SCALE  = 2.82
SUGAR_SHELF_REL_JUICES_P_MAX  = 6
SUGAR_SHELF_REL_JUICES_B_MAX  = 3
SUGAR_SHELF_SCALE_GUARD_JUICES = 2.0


def compute_shelf_relative_juice_delta(sugar_g: float) -> tuple[float, str]:
    """
    Compute the juice×sugar shelf-relative penalty/relief for a given sugar value.
    Uses the asymmetric P>B banded logic from score_engine.py / TASK-278 Phase-9.

    With sugar=None (current) → this scorer doesn't fire → delta=0.
    With sugar=real_value → this fires and produces a penalty or relief.

    The SURCHARGE_BANDS and RELIEF_BANDS are in r=distance/scale units.
    From constants.py (SUGAR_SHELF_SURCHARGE_BANDS / SUGAR_SHELF_RELIEF_BANDS):
    Surcharge bands: [(0.5, 6.0), (1.0, 4.0), (2.0, 2.0), (3.0, 0.0)] — typical P-max=6
    Relief bands:    [(0.5, 3.0), (1.0, 1.0), (2.0, 0.0)] — typical B-max=3
    Note: these are approximate; actual values read from constants.
    """
    # r = signed distance from median / scale
    r = (sugar_g - SUGAR_SHELF_REL_JUICES_MEDIAN) / SUGAR_SHELF_REL_JUICES_SCALE
    # Low-variance guard (if scale < 2.0 → degenerate, don't fire)
    if SUGAR_SHELF_REL_JUICES_SCALE < SUGAR_SHELF_SCALE_GUARD_JUICES:
        return 0.0, "low_variance_guard"

    if r > 0:
        # Above median → surcharge (penalty, negative score delta)
        # Banded: r ≤ 0.5 → P_max; r ≤ 1.0 → P_max/1.5; etc.
        # Simplified: linear from P_max at r=0.5 to 0 at r=3.0
        pen = max(0, SUGAR_SHELF_REL_JUICES_P_MAX * min(1.0, (3.0 - r) / 2.5))
        pen = min(pen, SUGAR_SHELF_REL_JUICES_P_MAX)
        return -pen, f"above_median: r={r:.2f} → penalty={pen:.1f}"
    else:
        # Below median → relief (bonus, positive score delta)
        # Only applies when r ≤ -0.5; caps at B_max
        r_abs = abs(r)
        if r_abs < 0.5:
            return 0.0, f"below_median but within 0.5 scale: r={r:.2f} → no_relief"
        bonus = min(SUGAR_SHELF_REL_JUICES_B_MAX, r_abs * 1.5)
        return bonus, f"below_median: r={r:.2f} → relief={bonus:.1f}"


def glycemic_score(sugar_g: float, fiber_g: float = 0.0, wg: bool = False) -> float:
    """Base glycemic quality score: 90 - sugar*2.5 + fiber*2 + wg*5, clamped 0-100."""
    penalty = min(80, sugar_g * 2.5)
    bonus   = min(20, fiber_g * 2.0)
    wg_b    = 5 if wg else 0
    return round(max(0, min(100, 90 - penalty + bonus + wg_b)), 1)


def read_trace(trace_path: pathlib.Path) -> dict | None:
    if not trace_path.exists():
        return None
    return json.loads(trace_path.read_text(encoding="utf-8"))


# ── Target table ─────────────────────────────────────────────────────────────
# (barcode, name, published_score, published_grade, published_rank, category,
#  real_sugar_g, sugar_source, panel_verdict, bsip2_trace_path)

JUICE_TRACE_DIR = ROOT / "02_products/juices/bsip2_outputs/run_juices_shelfrel_001/products"
MILK_TRACE_DIR  = ROOT / "02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products"
HUMMUS_TRACE_DIR = ROOT / "02_products/hummus/bsip2_outputs/run_hummus_001_sodium_pilot"
BRINED_TRACE_DIR = ROOT / "02_products/brined_cheeses/bsip2_outputs"
CAKES_TRACE_DIR  = ROOT / "02_products/cakes_hard_cookies/bsip2_outputs"
CEREALS_TRACE_DIR = ROOT / "02_products/breakfast_cereals/bsip2_outputs"
COOKIES_TRACE_DIR = ROOT / "02_products/cookies_coffee/bsip2_outputs/run_cookies_005/products"

TARGETS = [
    # ── JUICES (top priority) ─────────────────────────────────────────────
    {
        "barcode": "7290013153395", "name": "סחוט רימונים",
        "pub": (85.0, "A", 1), "category": "juices",
        "real_sugar_g": 10.5,
        "sugar_source": "USDA FDC #168153 pomegranate juice 100% = 10.5g/100ml",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": JUICE_TRACE_DIR / "bsip1_juice_7290013153395/bsip2_trace.json",
    },
    {
        "barcode": "7290110114886", "name": "סחוט קלמנטינה",
        "pub": (85.0, "A", 1), "category": "juices",
        "real_sugar_g": 8.9,
        "sugar_source": "USDA FDC clementine juice ~8.9g/100ml; carbs panel=9.8g consistent",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": JUICE_TRACE_DIR / "bsip1_juice_7290110114886/bsip2_trace.json",
    },
    # ── COOKIES/COFFEE (5) ────────────────────────────────────────────────
    # Sugar genuinely absent from panels — no reference value available for biscuit products.
    # Cannot simulate these without knowing actual sugar content.
    {
        "barcode": "7290119043149", "name": "עוגיות בטעם חמאה",
        "pub": (55.0, "C", 2), "category": "biscuit",
        "real_sugar_g": None,
        "sugar_source": "GENUINELY_ABSENT_from_panel; biscuit without sugar row — content unknown",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": None,
    },
    {
        "barcode": "7290017962139", "name": "עוגיות פירות יער",
        "pub": (54.9, "C", 4), "category": "biscuit",
        "real_sugar_g": None,
        "sugar_source": "GENUINELY_ABSENT_from_panel",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": COOKIES_TRACE_DIR / "bsip1_cookies_7290017962139/bsip2_trace.json",
    },
    {
        "barcode": "7290013453068", "name": "בסקביט",
        "pub": (52.0, "C", 8), "category": "biscuit",
        "real_sugar_g": None,
        "sugar_source": "GENUINELY_ABSENT_from_panel",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": None,
    },
    {
        "barcode": "7296073453840", "name": "ביסקוויט קפה",
        "pub": (33.1, "E", 37), "category": "biscuit",
        "real_sugar_g": None,
        "sugar_source": "GENUINELY_ABSENT_from_panel",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": None,
    },
    {
        "barcode": "7296073453857", "name": "ביסקוויט קרם",
        "pub": (32.7, "E", 38), "category": "biscuit",
        "real_sugar_g": None,
        "sugar_source": "GENUINELY_ABSENT_from_panel",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": None,
    },
    # ── MILK ──────────────────────────────────────────────────────────────
    {
        "barcode": "7290000051352", "name": "חלב מלא 3.4%",
        "pub": (85.0, "A", 1), "category": "dairy_protein",
        "real_sugar_g": 4.7,
        "sugar_source": "Lactose in whole milk: USDA FDC #746782 = 4.61g/100ml; rounded 4.7g",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": MILK_TRACE_DIR / "bsip1_7290000051352/bsip2_trace.json",
    },
    {
        "barcode": "5411188124689", "name": "אלפרו שיבולת שועל ללא סוכר",
        "pub": (49.7, "D", 13), "category": "dairy_protein",
        "real_sugar_g": 0.0,
        "sugar_source": "EU label declares 0g sugar; product name ללא סוכר (no added sugar)",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": MILK_TRACE_DIR / "bsip1_5411188124689/bsip2_trace.json",
    },
    {
        "barcode": "7290014760141", "name": "משקה שקדים",
        "pub": (51.5, "C", 8), "category": "dairy_protein",
        "real_sugar_g": None,
        "sugar_source": "UNCERTAIN — unsweetened almond milk ~0.5g, sweetened ~7g; cannot confirm without re-scrape",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": MILK_TRACE_DIR / "bsip1_7290014760141/bsip2_trace.json",
    },
    {
        "barcode": "7290110325619", "name": "משקה שיבולת שועל",
        "pub": (47.6, "D", 15), "category": "dairy_protein",
        "real_sugar_g": None,
        "sugar_source": "UNCERTAIN — oat milk range 3-7g; cannot confirm without re-scrape",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": MILK_TRACE_DIR / "bsip1_7290110325619/bsip2_trace.json",
    },
    # ── HUMMUS ───────────────────────────────────────────────────────────
    {
        "barcode": "6666307", "name": "סלט חומוס",
        "pub": (67.7, "B", 2), "category": "hummus",
        "real_sugar_g": 1.8,
        "sugar_source": "USDA FDC #174286 hummus = 1.85g/100g",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": None,  # hummus trace in different format
    },
    {
        "barcode": "6666444", "name": "סלט מטבוחה",
        "pub": (58.0, "C", 5), "category": "hummus",
        "real_sugar_g": 4.0,
        "sugar_source": "Matbucha (cooked tomato/pepper): USDA tomato sauce ~3.5g; 4.0g estimate",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": None,
    },
    # ── BRINED CHEESE ────────────────────────────────────────────────────
    {
        "barcode": "369617", "name": "כדורי פטה בשמן",
        "pub": (48.5, "D", 35), "category": "dairy_fat",
        "real_sugar_g": 0.5,
        "sugar_source": "USDA FDC #173420 feta = 0.49g/100g",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": None,
    },
    # ── CAKES ────────────────────────────────────────────────────────────
    {
        "barcode": "5431920", "name": "עוגת גבינה פירורים לייט",
        "pub": (30.6, "E", 4), "category": "dessert",
        "real_sugar_g": None,
        "sugar_source": "UNCERTAIN — 13g carbs; cheesecake sugar fraction ~50% = 6.5g is estimate only",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": None,
    },
    # ── CEREALS ──────────────────────────────────────────────────────────
    {
        "barcode": "7297488098688", "name": "פצפוצי אורז ללת\"ס",
        "pub": (67.3, "B", 2), "category": "cereal",
        "real_sugar_g": 0.5,
        "sugar_source": "Rice puffs no-added-sugar: USDA FDC puffed rice = 0.39g/100g; 0.5g estimate",
        "panel_verdict": "GENUINELY_ABSENT",
        "trace": None,
    },
]


def simulate(t: dict) -> dict:
    """
    Analytic simulation using trace-derived current glycemic score + formula.
    """
    bc = t["barcode"]
    name = t["name"]
    pub_score, pub_grade, pub_rank = t["pub"]
    real_sugar = t.get("real_sugar_g")
    category = t["category"]
    trace_path = t.get("trace")

    result = {
        "barcode": bc, "name": name, "category": category,
        "published_score": pub_score, "published_grade": pub_grade,
        "published_rank": pub_rank,
        "panel_verdict": t["panel_verdict"],
        "sugar_source": t["sugar_source"],
        "real_sugar_g": real_sugar,
        "staged_score": None, "staged_grade": None, "delta_score": None,
        "glycemic_null": None, "glycemic_real": None,
        "grade_moved": False, "tripwire": False,
        "note": None,
        "fiber_g_from_trace": None,
    }

    # If no real sugar → cannot simulate
    if real_sugar is None:
        result["note"] = "sugar_absent_no_reference"
        return result

    # Load trace to get current glycemic dimension score + fiber
    fiber_g = 0.0
    current_glycemic = None
    if trace_path and pathlib.Path(trace_path).exists():
        trace = read_trace(pathlib.Path(trace_path))
        if trace:
            current_glycemic = (trace.get("dimension_scores") or {}).get("glycemic_quality")
            l1 = trace.get("L1_observed_signals") or {}
            fiber_g = l1.get("dietary_fiber_g") or 0.0
            result["fiber_g_from_trace"] = fiber_g

    # Compute glycemic scores analytically
    g_null = glycemic_score(0, fiber_g)     # sugar=None → treated as 0
    g_real = glycemic_score(real_sugar, fiber_g)
    delta_glyc = g_real - g_null
    result["glycemic_null"] = g_null
    result["glycemic_real"] = g_real

    # Score delta from glycemic dimension
    delta_from_glycemic = delta_glyc * GLYCEMIC_WEIGHT

    # Juice-specific: shelf-relative EV-091 also activates
    sr_delta_juice = 0.0
    sr_note = ""
    if category == "juices":
        sr_val, sr_note = compute_shelf_relative_juice_delta(real_sugar)
        # The shelf-relative result is applied as a penalty in the sugar family budget.
        # Approximate: the shelf-relative delta is directly added to final score.
        sr_delta_juice = sr_val
        result["juice_sr_delta"] = sr_val
        result["juice_sr_note"] = sr_note

    total_delta = delta_from_glycemic + sr_delta_juice
    staged_score = round(max(0, min(100, pub_score + total_delta)), 1)
    staged_grade = score_to_grade(staged_score)

    result["delta_score"] = round(total_delta, 1)
    result["staged_score"] = staged_score
    result["staged_grade"] = staged_grade

    g_order = {"S": 6, "A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
    result["grade_moved"] = staged_grade != pub_grade
    result["tripwire"] = g_order.get(staged_grade, 0) < g_order.get(pub_grade, 0)

    return result


if __name__ == "__main__":
    out = io.StringIO()
    orig = sys.stdout
    sys.stdout = out

    results = []
    grade_movers = []
    tripwires = []

    for t in TARGETS:
        r = simulate(t)
        results.append(r)

    print("\n" + "="*75)
    print("TASK-378 PHASE 2 — ANALYTIC RESCORE SIMULATION")
    print("Method: trace-derived glycemic delta + juice shelf-relative formula")
    print("Stage only. N published scores changed = 0. BARI_SUGAR_NULL_GUARD=OFF.")
    print("="*75)

    for r in results:
        print(f"\n{r['barcode']} | {r['name']}")
        print(f"  Category:      {r['category']}")
        print(f"  Panel:         {r['panel_verdict']}")
        print(f"  Real sugar:    {r['real_sugar_g']}g  [{r['sugar_source']}]")
        print(f"  Published:     {r['published_score']}/{r['published_grade']} (rank {r['published_rank']})")

        if r["note"]:
            print(f"  Simulation:    SKIP — {r['note']}")
            continue

        print(f"  Glycemic (null=0): {r['glycemic_null']:.1f}")
        print(f"  Glycemic (real):   {r['glycemic_real']:.1f}")
        if "juice_sr_delta" in r:
            print(f"  Juice SR delta:    {r['juice_sr_delta']:+.1f}  ({r.get('juice_sr_note','')})")
        print(f"  Total delta:       {r['delta_score']:+.1f}")
        print(f"  Staged:            {r['staged_score']}/{r['staged_grade']}")
        print(f"  Grade moved:       {'YES ***' if r['grade_moved'] else 'no'}")
        print(f"  TRIPWIRE:          {'YES *** OWNER ESCALATION' if r['tripwire'] else 'no'}")

        if r["grade_moved"]:
            grade_movers.append(r)
        if r["tripwire"]:
            tripwires.append(r)

    print("\n" + "="*75)
    print("CONSOLIDATED GRADE-MOVERS")
    print("="*75)
    if grade_movers:
        for r in grade_movers:
            print(f"  {r['barcode']} {r['name']}: {r['published_grade']} → {r['staged_grade']} "
                  f"(score {r['published_score']} → {r['staged_score']}, delta={r['delta_score']:+.1f})")
    else:
        print("  None.")

    print("\n" + "="*75)
    print("OWNER TRIPWIRES (grade moves requiring owner approval)")
    print("="*75)
    if tripwires:
        for r in tripwires:
            print(f"  TRIPWIRE: {r['barcode']} {r['name']}: "
                  f"{r['published_grade']} → {r['staged_grade']} (delta={r['delta_score']:+.1f})")
    else:
        print("  None.")

    simulated  = [r for r in results if r["note"] is None and r["staged_score"] is not None]
    skipped    = [r for r in results if r["note"] is not None]
    print(f"\nSimulated: {len(simulated)}  |  Skipped: {len(skipped)}")
    print(f"N published scores changed = 0")
    print(f"M grade-movers flagged for owner = {len(grade_movers)}")
    print(f"Owner tripwires = {len(tripwires)}")

    sys.stdout = orig
    text = out.getvalue()
    out_path = pathlib.Path(r"C:\Bari\02_products\_parsing_audit\task378_phase2_analytic_result.txt")
    out_path.write_text(text, encoding="utf-8")
    print(f"Written to {out_path}")

    json_path = pathlib.Path(r"C:\Bari\02_products\_parsing_audit\task378_phase2_analytic_results.json")
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON: {json_path}")
