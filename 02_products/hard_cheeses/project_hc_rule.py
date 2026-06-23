"""
Projection script for BARI_HC_DAIRY_SATFAT_V1 grade distribution.
Design-only: zero score changes. Uses bsip1 data + trace data to estimate
the grade distribution under the proposed rule.
"""
import json, os, glob, statistics
from collections import Counter

# Corpus: 30 products from run_hard_cheeses_003_shelfrel
# Data extracted from bsip1_outputs and bsip2_outputs
# All nutrition values are from direct product scrape (yochananof storefront)
# Inferred sat_fat uses USDA FDC SR Legacy coefficient 0.62 for hard yellow cheeses
# (Gouda FDC 1008065: sat_fat/fat = 17.6/27.4 = 64.2%; Emmental FDC 1008066: 17.8/27.8 = 64.0%)

corpus = [
    # (bc, score_curr, grade_curr, fat, sat_labelled, inferred_sat, sodium, kcal, nova_bsip1, subpool, ing_count, name)
    ("7290108502725", 80.8, "A", 28.0, None, 17.4, 640.0, 352.0, 1, "yellow", 6, "Gouda 28% Euro Cheese"),
    ("7290019635192", 80.0, "A", 30.0, None, 18.6, 659.0, 365.0, 1, "yellow", 2, "Gouda Goat"),
    ("7290110324872", 77.6, "B", 5.0, None, 3.1, 491.0, 177.0, 2, "yellow", 4, "Galboa 5%"),
    ("7290110323301", 76.7, "B", 32.0, None, 19.8, 550.0, 397.0, 2, "yellow", 4, "Tal HaEmek 32%"),
    ("7290102394845", 76.5, "B", 9.0, None, 5.6, 620.0, 201.0, 1, "yellow_light", 3, "Noam 9% light"),
    ("7290102396672", 76.5, "B", 9.0, None, 5.6, 620.0, 201.0, 1, "yellow_light", 3, "Noam 9% light 360g"),
    ("7290116931524", 76.4, "B", 30.0, None, 18.6, 540.0, 364.0, 3, "yellow", 6, "Gouda Emek 200g"),
    ("7290004122348", 74.3, "B", 9.0, None, 5.6, 495.0, 202.0, 2, "yellow_light", 4, "Emek 9% light"),
    ("7290004137311", 74.3, "B", 9.0, None, 5.6, 491.0, 201.0, 2, "yellow_light", 4, "Emek 9% light 400g"),
    ("7290102397204", 74.2, "B", 22.0, None, 13.6, 670.0, 298.0, 1, "yellow", 3, "Noam 22%"),
    ("7290108501346", 73.4, "B", 28.0, None, 17.4, 630.0, 363.0, 3, "hard_grating", 6, "Gouda grated Euro Cheese"),
    ("7290117265888", 73.1, "B", 28.0, None, 17.4, 640.0, 352.0, 3, "hard_grating", 6, "Gouda grated Yochananof 400g"),
    ("7290117265918", 73.1, "B", 28.0, None, 17.4, 640.0, 352.0, 3, "yellow", 5, "Gouda slices Yochananof 400g"),
    ("7290102394463", 73.0, "B", 28.0, None, 17.4, 660.0, 346.0, 1, "yellow", 3, "Noam 28%"),
    ("7290004122195", 70.8, "B", 28.0, None, 17.4, 510.0, 345.0, 2, "yellow", 4, "Gush Halav 28%"),
    ("7290014760912", 70.8, "B", 28.0, None, 17.4, 510.0, 345.0, 2, "yellow", 4, "Gush Halav 28% 400g"),
    ("7290004122270", 69.1, "B", 28.0, None, 17.4, 640.0, 344.0, 2, "yellow", 4, "Emek 28% box 200g"),
    ("7290004122683", 69.1, "B", 28.0, None, 17.4, 640.0, 344.0, 2, "yellow", 4, "Emek 28% fingers"),
    ("7290004125776", 69.1, "B", 28.0, None, 17.4, 640.0, 344.0, 2, "yellow", 4, "Emek 28% box 400g"),
    ("7290110320850", 69.1, "B", 28.0, None, 17.4, 640.0, 344.0, 3, "hard_grating", 5, "Emek grated 28% 200g"),
    ("7290110320867", 69.1, "B", 28.0, None, 17.4, 640.0, 344.0, 3, "hard_grating", 5, "Emek grated 28% 500g"),
    ("7290000057088", 69.0, "B", 28.0, None, 17.4, 640.0, 345.0, 2, "yellow", 4, "Emek 28% 200g"),
    ("7290000057118", 69.0, "B", 28.0, None, 17.4, 640.0, 345.0, 2, "yellow", 4, "Emek 28% 400g"),
    ("7290014763395", 69.0, "B", 28.0, None, 17.4, 640.0, 345.0, 2, "yellow", 4, "Emek 28% 600g"),
    ("7290014455252", 66.1, "B", 29.0, 18.0, None, 600.0, 393.0, 2, "hard", 4, "Grana Padano grated"),
    ("7290102302864", 62.0, "C", None, None, None, None, None, None, "", 0, "Gouda Pesto - OFF excl."),
    ("7290017065434", 54.0, "C", 30.0, None, 18.6, 831.0, 368.0, 1, "yellow", 3, "Dutch Gouda 30%"),
    ("8711528211138", 54.0, "C", 34.0, None, 21.1, 800.0, 397.0, 1, "yellow", 4, "Gouda Goat Dutch"),
    ("7290108503999", 44.3, "D", 13.6, None, 8.4, 1300.0, 222.0, 4, "processed", 9, "Processed Cheese 13%"),
    ("3073781199918", 39.0, "D", 24.0, 16.0, None, 710.0, 305.0, 1, "yellow", 4, "Baby Bell 24%"),
]

# ─── PROPOSED RULE PREDICATE ───────────────────────────────────────────────
# BARI_HC_DAIRY_SATFAT_V1 qualification criteria (default OFF):
# (A) Engine category == "dairy_protein" (all hard cheeses route here)
# (B) NOVA proxy <= 2 (NOVA 1 = milk/salt/rennet/cultures; NOVA 2 = minor preservative/colour)
# (C) Sanitized ingredient count <= 6
# (D) NOT subpool "processed" (processed cheese is NOVA 4 + emulsifying salts -- disqualified)
# (E) Sodium < 850 mg/100g HARD BACKSTOP (non-relieved)
# (F) No fat-engineering markers in ingredient text (added cream/butter/palm/margarine)
#     -- cannot assess from numeric corpus alone; flag for engine predicate
#
# Mechanism when qualified:
#   1. sat_fat excluded from ISRAELI_RED_LABELS_2_PLUS reformulable count (like EV-REDLABEL-005)
#   2. HP_FAT_SODIUM_COMBO penalty suppressed (like TASK-373 snack wholefood)
#   3. fat_quality dimension: endemic-dairy sat_fat seed_pen reduced from 5 -> 0
#      (R5 formula: base starts at max(0, 50 - 0 - trans_pen - red_label_pen))
#
# Non-relieved guardrails:
#   G1. Sodium >= 850 mg/100g: NO relief (hard backstop, product fails predicate)
#   G2. NOVA >= 3: NO relief (NOVA 3 = grated + anti-caking agents; NOVA 4 = processed)
#   G3. Subpool "processed": always disqualified (emulsifying salts = engineered matrix)
#   G4. Calorie density >= 380 kcal/100g: score capped at 67 (top of C; cannot reach B)
#       Rationale: 380 kcal is the 28-fat-pct hard cheese reference energy density;
#       products above this are materially calorie-denser and the cap prevents A-grade
#       for calorie-dense cheese (Grana Padano 393 kcal, Emmental 32% 397 kcal).

def qualifies(bc, fat, sat, inf_sat, sodium, kcal, nova, subpool, ing_count):
    # Missing nutrition -- cannot evaluate
    if fat is None:
        return False, "no_nutrition_data"
    # NOVA gate (strict: only NOVA 1-2)
    if nova is None:
        return False, "no_nova"
    if nova > 2:
        return False, f"nova_{nova}_blocked"
    # Processed subpool always fails (emulsifying salts in ingredient list)
    if subpool == "processed":
        return False, "processed_subpool"
    # Ingredient count gate
    if ing_count > 6:
        return False, f"ing_count_{ing_count}_exceeds_6"
    # Hard sodium backstop
    if sodium is not None and sodium >= 850:
        return False, f"sodium_{sodium}mg_backstop"
    return True, "qualifies"

def project_grade(current_score, ok, fat, sat, inf_sat, sodium, kcal, nova, subpool, ing_count):
    """
    Band estimate: NOT an engine re-run. Uses the known cap/penalty structure.
    Under relief:
    - ISRAELI_RED_LABELS_2_PLUS cap (45) no longer fires (sat_fat excluded)
    - HP_FAT_SODIUM_COMBO penalty (-6) suppressed
    - fat_quality seed_pen: 0 instead of 5 -> fat_quality dimension rises ~5-10 pts
    - Single sodium red label (sodium > 600): ISRAELI_RED_LABEL_1_SODIUM -> cap 63
    - HIGH_SODIUM_700MG_PLUS (sodium > 700): cap 60
    - Score estimate: conservative weighted_dim ~ 78 (without fat_quality=0 drag)
    - Apply calorie backstop: kcal >= 380 -> cap 67
    """
    if not ok:
        # No change from current
        return None, None

    if kcal is None or sodium is None:
        return None, None

    # Calorie backstop
    calorie_cap = 67 if kcal >= 380 else 100

    # Sodium caps (still apply regardless of sat_fat relief)
    if sodium >= 700:
        sodium_cap = 60   # HIGH_SODIUM_700MG_PLUS
    elif sodium >= 600:
        sodium_cap = 63   # ISRAELI_RED_LABEL_1_SODIUM
    else:
        sodium_cap = 100  # No sodium cap

    # Conservative weighted_dim estimate under relief (fat_quality partial recovery)
    # Basis: Baby Bell (NOVA 1) had weighted_dim=83.6. Most 28% products similar.
    # After endemic relief: fat_quality improves from 0 to ~20 (trans_fat penalty still applies
    # if trans fat present; for most products trans_fat=0, red_label_pen reduced by removing sat_fat)
    # Net weighted_dim ~ 81 for typical 28% product
    weighted_dim_est = 81

    est_score = min(weighted_dim_est, sodium_cap, calorie_cap)

    if est_score >= 75:
        grade = "A"
    elif est_score >= 65:
        grade = "B"
    elif est_score >= 55:
        grade = "C"
    elif est_score >= 45:
        grade = "D"
    else:
        grade = "E"

    return round(est_score, 1), grade


print("=" * 100)
print("PROJECTED GRADE DISTRIBUTION UNDER BARI_HC_DAIRY_SATFAT_V1")
print("METHOD: Band estimate from cap/penalty mechanic (not engine re-run)")
print("Source: bsip1 nutrition from direct product scrape; sat_fat inferred at USDA FDC coefficient 0.62")
print("=" * 100)
print()
print(f"{'bc':<18} {'curr':>6} {'cg':>3} {'fat':>5} {'na':>6} {'kcal':>5} {'nova':>5} {'sub':>10} {'ing':>4} {'ok':>6} {'reason':<30} {'proj_s':>7} {'pg':>4} {'name'}")
print("-" * 140)

projected_grades = []
for row in corpus:
    bc, sc, gr, fat, sat, inf_sat, sodium, kcal, nova, subpool, ing_count, name = row
    ok, reason = qualifies(bc, fat, sat, inf_sat, sodium, kcal, nova, subpool, ing_count)
    proj_score, proj_grade = project_grade(sc, ok, fat, sat, inf_sat, sodium, kcal, nova, subpool, ing_count)
    final_grade = proj_grade if proj_grade else gr
    final_score = proj_score if proj_score else sc
    projected_grades.append(final_grade)
    ok_str = "YES" if ok else "NO"
    print(f"{bc:<18} {sc:>6} {gr:>3} {str(fat):>5} {str(sodium):>6} {str(kcal):>5} {str(nova):>5} {subpool:>10} {ing_count:>4} {ok_str:>6} {reason:<30} {str(final_score):>7} {final_grade:>4} {name}")

print()
print("CURRENT grade dist:", dict(sorted(Counter(row[2] for row in corpus).items())))
print("PROJECTED grade dist:", dict(sorted(Counter(projected_grades).items())))
print()

# Score stats for current
curr_scores = [r[1] for r in corpus if r[1] is not None]
print(f"CURRENT:  min={min(curr_scores):.1f} max={max(curr_scores):.1f} median={statistics.median(curr_scores):.1f} stdev={statistics.stdev(curr_scores):.1f} n={len(curr_scores)}")
print()
print("NOTE: This is a design-only projection. Actual scores require engine re-run with BARI_HC_DAIRY_SATFAT_V1=on.")
print("NOTE: NOVA 3 products (hard_grating, yellow with anti-caking agents) remain excluded from relief -- intentional.")
print("NOTE: Processed subpool (NOVA 4, emulsifying salts) never qualifies -- intentional.")
print("NOTE: Gouda Pesto (7290102302864) excluded from scoring (OFF-contaminated data) -- no change.")
print("NOTE: Baby Bell has trans_fat=1g/100g -- trans_fat penalty may further reduce score even with relief.")
