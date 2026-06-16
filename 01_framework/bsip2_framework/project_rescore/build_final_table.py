"""Final table builder for TASK-278 spread analysis."""
import json
import statistics
from pathlib import Path

CATEGORIES_DATA = {
    "milk": {
        "run_id": "run_005_headpin",
        "n_scored": 20,
        "sugar": {"med": 4.9, "iqr": 1.5, "scale": 2.2, "n": 9},
        "sat_fat": {"med": 0.3, "iqr": 2.0, "scale": 1.5, "n": 12},
        "sodium": {"med": 45.0, "iqr": 20.0, "scale": 14.8, "n": 18},
        "score_stdev": 15.07, "score_range": 51.5,
        "pct_floored": 0.0, "pct_scaling_absorbed": 0.0,
    },
    "bread": {
        "run_id": "real_bread_retail_003_v1",
        "n_scored": 256,
        "sugar": {"med": None, "iqr": None, "scale": None, "n": 7},
        "sat_fat": {"med": None, "iqr": None, "scale": None, "n": 0},
        "sodium": {"med": 382.0, "iqr": 60.0, "scale": 51.9, "n": 180},
        "score_stdev": 13.77, "score_range": 42.4,
        "pct_floored": 0.0, "pct_scaling_absorbed": 0.0,
    },
    "snack_bars": {
        "run_id": "run_snack_bars_001 (full traces); run_snackbars_007_headpin (authoritative, flat only)",
        "n_scored": 53,
        "sugar": {"med": 19.4, "iqr": 22.4, "scale": 17.3, "n": 48},
        "sat_fat": {"med": 3.2, "iqr": 4.6, "scale": 3.4, "n": 46},
        "sodium": {"med": 142.0, "iqr": 129.0, "scale": 127.5, "n": 46},
        "score_stdev": 15.7, "score_range": 56.7,
        "pct_floored": 43.4, "pct_scaling_absorbed": 9.4,
    },
    "cereals": {
        "run_id": "run_cereals_synthesis_001",
        "n_scored": 45,
        "sugar": {"med": 14.0, "iqr": 11.0, "scale": 8.9, "n": 45},
        "sat_fat": {"med": 1.2, "iqr": 1.0, "scale": 1.4, "n": 45},
        "sodium": {"med": 280.0, "iqr": 370.0, "scale": 274.3, "n": 45},
        "score_stdev": 17.03, "score_range": 60.7,
        "pct_floored": 11.1, "pct_scaling_absorbed": 0.0,
    },
    "hummus": {
        "run_id": "run_hummus_002",
        "n_scored": 69,
        "sugar": {"med": None, "iqr": None, "scale": None, "n": 0},
        "sat_fat": {"med": None, "iqr": None, "scale": None, "n": 0},
        "sodium": {"med": 393.0, "iqr": 33.0, "scale": 89.0, "n": 67},
        "score_stdev": 9.86, "score_range": 42.7,
        "pct_floored": 0.0, "pct_scaling_absorbed": 0.0,
    },
    "salty_snacks": {
        "run_id": "run_salty_snacks_002",
        "n_scored": 54,
        "sugar": {"med": 2.5, "iqr": 2.0, "scale": 1.5, "n": 54},
        "sat_fat": {"med": 2.0, "iqr": 4.0, "scale": 3.0, "n": 54},
        "sodium": {"med": 560.0, "iqr": 190.0, "scale": 140.8, "n": 54},
        "score_stdev": 16.51, "score_range": 66.1,
        "pct_floored": 7.4, "pct_scaling_absorbed": 0.0,
    },
    "juices": {
        "run_id": "run_juices_yohananof_002",
        "n_scored": 28,
        "sugar": {"med": 8.2, "iqr": 6.9, "scale": 5.5, "n": 25},
        "sat_fat": {"med": None, "iqr": None, "scale": None, "n": 0},
        "sodium": {"med": 10.0, "iqr": 7.0, "scale": 5.9, "n": 9},
        "score_stdev": 23.81, "score_range": 55.9,
        "pct_floored": 7.1, "pct_scaling_absorbed": 0.0,
    },
    "hard_cheeses": {
        "run_id": "run_hard_cheeses_001",
        "n_scored": 37,
        "sugar": {"med": 0.5, "iqr": 1.0, "scale": 1.4, "n": 37},
        "sat_fat": {"med": 17.5, "iqr": 8.0, "scale": 5.9, "n": 37},
        "sodium": {"med": 620.0, "iqr": 300.0, "scale": 296.5, "n": 37},
        "score_stdev": 17.35, "score_range": 46.6,
        "pct_floored": 2.7, "pct_scaling_absorbed": 0.0,
    },
    "butter": {
        "run_id": "butter_run_003",
        "n_scored": 39,
        "sugar": {"med": 0.1, "iqr": 0.6, "scale": 1.4, "n": 32},
        "sat_fat": {"med": 50.5, "iqr": 3.0, "scale": 2.2, "n": 39},
        "sodium": {"med": 11.0, "iqr": 635.0, "scale": 470.7, "n": 38},
        "score_stdev": 9.64, "score_range": 24.8,
        "pct_floored": 0.0, "pct_scaling_absorbed": 0.0,
    },
    "cheese_spreads": {
        "run_id": "run_cheese_004",
        "n_scored": 59,
        "sugar": {"med": 3.0, "iqr": 1.6, "scale": 1.4, "n": 34},
        "sat_fat": {"med": 5.4, "iqr": 12.8, "scale": 9.5, "n": 57},
        "sodium": {"med": 350.0, "iqr": 110.0, "scale": 81.5, "n": 59},
        "score_stdev": 14.47, "score_range": 62.8,
        "pct_floored": 1.7, "pct_scaling_absorbed": 0.0,
    },
    "yogurt": {
        "run_id": "run_yogurt_006_shipcfg2",
        "n_scored": 87,
        "sugar": {"med": 5.3, "iqr": 5.8, "scale": 4.3, "n": 73},
        "sat_fat": {"med": 2.0, "iqr": 0.8, "scale": 1.4, "n": 48},
        "sodium": {"med": 48.0, "iqr": 15.0, "scale": 11.9, "n": 87},
        "score_stdev": 16.52, "score_range": 57.8,
        "pct_floored": 0.0, "pct_scaling_absorbed": 0.0,
    },
    "brined_cheeses": {
        "run_id": "run_brined_005",
        "n_scored": 48,
        "sugar": {"med": 2.0, "iqr": 2.0, "scale": 1.4, "n": 48},
        "sat_fat": {"med": None, "iqr": None, "scale": None, "n": 0},
        "sodium": {"med": 1000.0, "iqr": 310.0, "scale": 229.8, "n": 48},
        "score_stdev": 9.45, "score_range": 39.4,
        "pct_floored": 0.0, "pct_scaling_absorbed": 0.0,
    },
    "cookies_coffee": {
        "run_id": "run_cookies_005_shelfrel_pilot",
        "n_scored": 58,
        "sugar": {"med": 21.5, "iqr": 6.9, "scale": 5.1, "n": 57},
        "sat_fat": {"med": 7.4, "iqr": 5.4, "scale": 4.0, "n": 57},
        "sodium": {"med": 220.0, "iqr": 96.0, "scale": 77.1, "n": 58},
        "score_stdev": 13.35, "score_range": 52.4,
        "pct_floored": 53.4, "pct_scaling_absorbed": 19.0,
    },
    "granola": {
        "run_id": "no_run",
        "n_scored": 0,
        "sugar": {"med": None, "iqr": None, "scale": None, "n": 0},
        "sat_fat": {"med": None, "iqr": None, "scale": None, "n": 0},
        "sodium": {"med": None, "iqr": None, "scale": None, "n": 0},
        "score_stdev": None, "score_range": None,
        "pct_floored": None, "pct_scaling_absorbed": None,
    },
    "frozen_vegetables": {
        "run_id": "run_frozen_vegetables_001",
        "n_scored": 53,
        "sugar": {"med": 1.4, "iqr": 1.1, "scale": 1.4, "n": 47},
        "sat_fat": {"med": None, "iqr": None, "scale": None, "n": 0},
        "sodium": {"med": 24.0, "iqr": 40.0, "scale": 29.7, "n": 47},
        "score_stdev": 10.92, "score_range": 40.9,
        "pct_floored": 0.0, "pct_scaling_absorbed": 0.0,
    },
    "maadanim": {
        "run_id": "run_maadanim_001",
        "n_scored": 200,
        "sugar": {"med": 9.7, "iqr": 11.9, "scale": 8.9, "n": 146},
        "sat_fat": {"med": 3.0, "iqr": 4.7, "scale": 3.5, "n": 100},
        "sodium": {"med": 60.0, "iqr": 120.0, "scale": 89.0, "n": 164},
        "score_stdev": 13.39, "score_range": 65.8,
        "pct_floored": 18.0, "pct_scaling_absorbed": 2.5,
    },
}

CLASSIFICATION = {
    "milk":            ("LAND",      "sat_fat"),
    "bread":           ("N-A",       "sodium"),
    "snack_bars":      ("COSMETIC",  "sugar"),
    "cereals":         ("LAND",      "sugar"),
    "hummus":          ("LAND",      "sodium"),
    "salty_snacks":    ("LAND",      "sodium"),
    "juices":          ("LAND",      "sugar"),
    "hard_cheeses":    ("LAND",      "sat_fat"),
    "butter":          ("COSMETIC",  "sat_fat"),
    "cheese_spreads":  ("LAND",      "sat_fat"),
    "yogurt":          ("LAND",      "sugar"),
    "brined_cheeses":  ("COSMETIC",  "sodium"),
    "cookies_coffee":  ("COSMETIC",  "sugar"),
    "granola":         ("N-A",       "N-A"),
    "frozen_vegetables": ("N-A",     "N-A"),
    "maadanim":        ("LAND",      "sugar"),
}

NOTES = {
    "milk": "0% floored, stdev=15.07. Sugar sparse (9/20 have data). Sat_fat is the class driver (3.4%/natural/goat tiers). Sugar term insufficient data.",
    "bread": "Sugar 97% null in traces (BSIP0 panel focus = fiber+sodium+fermentation). Sodium available 70%. No sugar term possible. N-A pending a nutrition-richer run.",
    "snack_bars": "43.4% floored (final_score<=33). High-sugar chocolate bars already at floor; relative term absorbed. IQR=22.4 wide but splits into bimodal corpus (date-bars vs chocolate). Not a sugar rollout candidate.",
    "cereals": "BEST CANDIDATE. Sugar IQR=11.0, scale=8.9. Score stdev=17.03, only 11% floored. Strong spread, low floor saturation. TASK-189 (sodium gap for granola) is separate; does not block cereal rollout.",
    "hummus": "Sugar/sat_fat null in all traces. Score spread real (stdev=9.86) but driven by ingredient quality/tahini, not sugar. Sodium IQR tight (33mg). LAND classification holds for sodium, but nutrient data is insufficient for sugar rollout.",
    "salty_snacks": "Sodium is the differentiator (IQR=190mg, scale=140.8). Score stdev=16.51, only 7.4% floored. Sugar low-variance (scale=1.5). Strong LAND but for sodium, not sugar.",
    "juices": "Highest score stdev of all categories (23.81). Sugar IQR=6.9, scale=5.5 — strong. Only 7.1% floored. Sugar is THE defining axis for juices. Strong LAND candidate.",
    "hard_cheeses": "Score spread genuine (stdev=17.35, range=46.6). 2.7% floored. 0% scaling absorption. Earlier 97.3% 'pinning' was HP_FAT_SODIUM_COMBO uniform penalty (~6pts), NOT absorption. Sat_fat (IQR=8g, scale=5.9) and sodium (IQR=300mg) are real levers. Sugar irrelevant (IQR=1.0, at scale floor).",
    "butter": "Compressed score range (24.8pts). Sat_fat tight IQR=3g (all butters are ~50g sat_fat). Sodium bimodal (salted vs unsalted, IQR=635mg). Genuine clustering — no rollout candidate.",
    "cheese_spreads": "Sat_fat has strongest scale (9.5g) driven by full-fat vs light vs plant-based. Score stdev=14.47, 1.7% floored. Good LAND candidate for sat_fat term.",
    "yogurt": "REFERENCE PILOT (confirmed LANDS). Sugar: med=5.3, IQR=5.8, scale=4.3. Bimodal (plain vs sweetened). Score stdev=16.52, 0% floored, 0% scaling absorption.",
    "brined_cheeses": "Sodium already graduated (SODIUM_LOAD_GENERAL_GRAD + SODIUM_SHELF_SURCHARGE). Adding a new relative term overlaps existing mechanism. COSMETIC in the sense of redundant, not floor-saturated.",
    "cookies_coffee": "REFERENCE PILOT (confirmed COSMETIC). 53.4% final_score<=33 (floor). Sugar IQR=6.9 but absorbed. 19% scaling absorption. Floor saturation dominates.",
    "granola": "No dedicated BSIP2 run. Products are inside run_cereals_synthesis_001 but not separately identified. TASK-189 open. N-A pending a labeled granola sub-corpus.",
    "frozen_vegetables": "Score-free display category (TASK-235). Scores exist in pipeline but not shown to users. N-A for rollout.",
    "maadanim": "Large corpus (200). Sugar IQR=11.9, scale=8.9. Score stdev=13.39, range=65.8. 18% floored but 82% have real spread. Strong secondary candidate after cereals/juices.",
}

def fmt(v, suffix=""):
    if v is None:
        return "null"
    return f"{v}{suffix}"

print("FINAL SPREAD ANALYSIS TABLE")
print("=" * 120)
print()

# Build ranked shortlist
land_cats = [(cat, CATEGORIES_DATA[cat]) for cat in CATEGORIES_DATA if CLASSIFICATION[cat][0] == "LAND"]

def land_score(item):
    cat, d = item
    stdev = d["score_stdev"] or 0
    pf = d["pct_floored"] or 0
    # Composite: stdev * (1 - pct_floored/100)
    return stdev * (1 - pf / 100)

land_cats.sort(key=land_score, reverse=True)

print("LAND RANKING (stdev * (1 - pct_floored):")
for rank, (cat, d) in enumerate(land_cats, 1):
    cls, nutrient = CLASSIFICATION[cat]
    score = land_score((cat, d))
    print(f"  #{rank}: {cat} — composite={score:.1f}, stdev={d['score_stdev']}, pct_floored={d['pct_floored']}%, candidate_nutrient={nutrient}")

print()
print("COSMETIC / N-A:")
for cat in CATEGORIES_DATA:
    cls, nutrient = CLASSIFICATION[cat]
    if cls in ("COSMETIC", "N-A"):
        d = CATEGORIES_DATA[cat]
        print(f"  {cls}: {cat} — pct_floored={d['pct_floored']}, stdev={d['score_stdev']}, nutrient={nutrient}")

print()
print("Produced data for: " + ", ".join(CATEGORIES_DATA.keys()))
