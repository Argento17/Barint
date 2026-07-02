"""
Debug script: trace full marker extraction + scoring decomposition for barcode 481180
Read-only investigation for TASK-395 QA findings.
"""
import sys
import json
import re
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\analysis")

from structured_ingredient_reader import parse_ingredients, is_unparseable, _extract_groups, _strip_groups

# The exact ingredient text from matrix_gold_set_v2.json
TEXT = (
    "קמח חיטה לבן (מכיל גלוטן) (75% מהקמח, 40% מהלחם), מים, "
    "מחמצת חיטה לבן 18% (קמח חיטה לבן (מכיל גלוטן), מים), "
    "קמח חיטה מלא (נטחן מגרעין החיטה בשלמותו (מכיל גלוטן)) (25% מסך הקמחים, 15% מהלחם), "
    "מלח, גלוטן חיטה, חומר משמר (E282)."
)

out = []

out.append("=== RAW INGREDIENT TEXT ===")
out.append(TEXT)
out.append("")

out.append("=== PARSED RECORDS (structured_ingredient_reader.py) ===")
records = parse_ingredients(TEXT)
for i, r in enumerate(records):
    out.append(f"Record {i+1}: pos={r.get('position')} level={r.get('level')} stated_pct={r.get('stated_pct')} effective_pct={r.get('effective_pct')} has_own_sub={r.get('has_own_sub')}")
    out.append(f"  raw: {r.get('raw', '')}")
    out.append(f"  qualifiers: {r.get('qualifiers', [])}")
    out.append("")

# Now replicate extract_markers_from_record_v4 from the probe
MARKERS = [
    (r"קמח חיטה מלאה?", "whole_wheat_flour", "whole", False),
    (r"חיטה מלאה", "whole_wheat_grain", "whole", False),
    (r"קמח (?:חיטת )?כוסמין מלא", "whole_spelt_flour", "whole", False),
    (r"כוסמין מלא", "whole_spelt_grain", "whole", False),
    (r"קמח שיבולת שועל מלא", "whole_oat_flour", "whole", False),
    (r"שיבולת שועל מלאה?", "whole_oat", "whole", False),
    (r"פתיתי שיבולת שועל מלאה?|פתיתי שיבולת שועל מלאים", "whole_oat_flakes", "whole", False),
    (r"קמח שיפון מלא", "whole_rye_flour", "whole", False),
    (r"שיפון מלא", "whole_rye_grain", "whole", False),
    (r"קמח תירס מלא", "whole_corn_flour", "whole", False),
    (r"קמח שעורה מלא", "whole_barley_flour", "whole", False),
    (r"אורז מלא|קמח(?:\s+מ)?אורז מלא", "whole_rice", "whole", False),
    (r"קינואה(?:\s+מלאה)?", "quinoa", "whole", False),
    (r"כוסמת", "buckwheat", "whole", False),
    (r"גריסי שיבולת שועל", "oat_groats", "whole", False),
    (r"שיבולת שועל קלופה", "hulled_oats", "whole", False),
    (r"שיבולת שועל(?!\s+מלאה?)(?!\s+מלאים)", "oat_flakes_plain", "whole", False),
    (r"לתת שעורה|מיצוי לתת שעורה", "barley_malt", "whole", True),
    (r"אגוז(?:י)?\s+(?:פקאן|לוז|מלך|מקדמיה|ברזיל)|אגוזים", "nuts", "whole", False),
    (r"שקד(?:ים)?", "almonds", "whole", False),
    (r"בוטנ(?:ים|ות)?", "peanuts", "whole", False),
    (r"פיסטוק(?:ים)?", "pistachios", "whole", False),
    (r"קשיו", "cashews", "whole", False),
    (r"גרעיני?\s+(?:חמנ(?:ייה|יה)|דלעת|פשתן)", "seeds_specific", "whole", False),
    (r"גרעינים", "seeds_generic", "whole", False),
    (r"שומשום(?!\s+לבן)", "sesame_seeds", "whole", False),
    (r"זרעי?\s+צ'יה|צ'יה", "chia_seeds", "whole", False),
    (r"גרעיני פשתן|פשתן", "flax_seeds", "whole", False),
    (r"עדשים", "lentils", "whole", False),
    (r"חומוס(?!\s+שחור)", "chickpeas", "whole", False),
    (r"תמר(?:ים)?", "dates", "whole", False),
    (r"צימוקים", "raisins", "whole", False),
    (r"מחמצת", "sourdough_starter", "whole", False),
    (r"חמאה(?!\s+קקאו)(?!\s+שמן)", "butter_dairy", "whole", False),
    (r"שמן זית", "olive_oil", "whole", False),
    (r"טחינה|ממרח שומשום", "tahini", "whole", False),
    # Refined
    (r"קמח כוסמין לבן", "white_spelt_flour", "refined", False),
    (r"קמח חיטה(?!\s+מלאה?)(?!\s+מלא)", "refined_wheat_flour", "refined", False),
    (r"גריסי תירס", "corn_grits", "refined", False),
    (r"קמח תירס(?!\s+מלא)", "corn_flour_refined", "refined", False),
    (r"סמולינה(?:\s+מתירס)?", "semolina", "refined", False),
    (r"קמח אורז(?!\s+מלא)", "rice_flour_refined", "refined", False),
    (r"אורז לבן", "white_rice", "refined", False),
    (r"עמילן תירס", "corn_starch", "refined", False),
    (r"עמילן חיטה", "wheat_starch", "refined", False),
    (r"עמילן אורז", "rice_starch", "refined", False),
    (r"עמילן(?!\s+תירס)(?!\s+חיטה)(?!\s+אורז)", "generic_starch", "refined", False),
    (r"(?<!\S)סוכר(?!\s+קנים\s+אורגני)", "sugar", "refined", False),
    (r"סירופ\s+גלוקוז(?:-פרוקטוז)?|סירופ\s+גלוקוזה(?:-פרוקטוזה)?", "glucose_syrup", "refined", False),
    (r"סירופ\s+סוכר\s+אינברטי|סוכר\s+אינברטי", "inverted_sugar", "refined", False),
    (r"גלוקוז(?!\s+מיובש)(?![א-ת])", "glucose", "refined", False),
    (r"דקסטרוז|דקסטרוזה", "dextrose", "refined", False),
    (r"דקסטרין", "dextrin", "refined", False),
    (r"פרוקטוז", "fructose", "refined", False),
    (r"מלטודקסטרין", "maltodextrin", "refined", False),
    (r"שמן דקל(?!ים)(?!\s+אדום)", "palm_oil", "refined", False),
    (r"שמן דקלים", "palm_oil_pl", "refined", False),
    (r"שמנים\s+צמחיים", "veg_oils_pl", "refined", False),
    (r"שמן\s+צמחי(?!ים)", "veg_oil_sg", "refined", False),
    (r"שומן\s+צמחי", "hydrogenated_veg_fat", "refined", False),
    (r"מרגרינה", "margarine", "refined", False),
    (r"שמן\s+קוקוס", "coconut_oil", "refined", False),
]

def _pos_weight(pos):
    if pos is None: return 0.12
    if pos == 1:    return 1.00
    if pos == 2:    return 0.82
    if pos == 3:    return 0.68
    if pos == 4:    return 0.55
    if pos == 5:    return 0.44
    if pos == 6:    return 0.35
    if pos == 7:    return 0.28
    if pos == 8:    return 0.22
    if pos == 9:    return 0.17
    if pos == 10:   return 0.13
    if pos <= 15:   return max(0.08, 0.13 * (0.85 ** (pos - 10)))
    return 0.08

def _name_only_text(record):
    raw = record["raw"]
    if not record.get("has_own_sub"):
        return raw
    groups = _extract_groups(raw)
    if not groups:
        return raw
    name_end = groups[0]["start"]
    return raw[:name_end].strip()

out.append("=== PER-RECORD MARKER EXTRACTION ===")
all_candidates = []
for record in records:
    text_for_match = _name_only_text(record)
    pos = record.get("position")
    stated = record.get("effective_pct") if record.get("effective_pct") is not None else record.get("stated_pct")
    out.append(f"Record pos={pos} stated_pct={stated} text_for_match={repr(text_for_match[:80])}")
    for pattern, label, grain_class, half_weight in MARKERS:
        m = re.search(pattern, text_for_match, re.IGNORECASE)
        if m:
            out.append(f"  MATCH: label={label} class={grain_class} matched={repr(m.group())} stated_pct={stated} pos={pos}")
            all_candidates.append({
                "label": label, "class": grain_class, "position": pos,
                "stated_pct": stated, "half_weight": half_weight, "matched_text": m.group()
            })
    out.append("")

out.append("=== DEDUPLICATION (best effective_weight wins per label) ===")
seen_labels = {}
for m in all_candidates:
    label = m["label"]
    ew_new = m["stated_pct"] / 100.0 if m["stated_pct"] is not None else _pos_weight(m["position"])
    if label not in seen_labels:
        seen_labels[label] = m
        out.append(f"  ADD: {label} ew={ew_new:.4f} pos={m['position']} stated={m['stated_pct']}")
    else:
        ew_old_m = seen_labels[label]
        ew_old = ew_old_m["stated_pct"] / 100.0 if ew_old_m["stated_pct"] is not None else _pos_weight(ew_old_m["position"])
        if ew_new > ew_old:
            seen_labels[label] = m
            out.append(f"  REPLACE: {label} old_ew={ew_old:.4f} new_ew={ew_new:.4f}")
        else:
            out.append(f"  KEEP existing: {label} kept_ew={ew_old:.4f} discarded_ew={ew_new:.4f} (new was lower)")

final_markers = list(seen_labels.values())
out.append("")
out.append("=== FINAL MARKERS (after dedup) ===")
for m in final_markers:
    ew = m["stated_pct"] / 100.0 if m["stated_pct"] is not None else _pos_weight(m["position"])
    out.append(f"  {m['label']} class={m['class']} stated_pct={m['stated_pct']} pos={m['position']} base_ew={ew:.4f}")

out.append("")
out.append("=== SCORING CALCULATION (v5.1 formula) ===")
pct_markers = [m for m in final_markers if m.get("stated_pct") is not None]
pos_markers  = [m for m in final_markers if m.get("stated_pct") is None]
total_stated_pct = sum(m["stated_pct"] for m in pct_markers) / 100.0
total_stated_pct = min(total_stated_pct, 1.0)
remaining_mass   = max(0.0, 1.0 - total_stated_pct)
total_pos_weight = sum(_pos_weight(m.get("position")) for m in pos_markers)
out.append(f"  total_stated_pct (capped at 1.0): {total_stated_pct:.4f}")
out.append(f"  remaining_mass: {remaining_mass:.4f}")
out.append(f"  total_pos_weight (position-based markers only): {total_pos_weight:.4f}")

# Guard
GRAIN_WHOLE_LABELS = {
    "whole_wheat_flour", "whole_wheat_grain",
    "whole_spelt_flour", "whole_spelt_grain",
    "whole_oat_flour", "whole_oat", "whole_oat_flakes",
    "whole_rye_flour", "whole_rye_grain",
    "whole_corn_flour", "whole_barley_flour", "whole_rice",
    "oat_groats", "hulled_oats", "oat_flakes_plain",
    "quinoa", "buckwheat", "bare_wheat_first_80pct",
}
NON_GRAIN_WHOLE_LABELS = {
    "nuts", "almonds", "peanuts", "pistachios", "cashews",
    "seeds_specific", "seeds_generic", "sesame_seeds",
    "chia_seeds", "flax_seeds",
    "dates", "raisins",
    "tahini", "olive_oil", "butter_dairy",
}
GRAIN_CONTEXT_ABS_FLOOR = 0.05
GRAIN_CONTEXT_REL_FLOOR = 0.50

def bw_no_penalty(m):
    if m.get("stated_pct") is not None:
        w = m["stated_pct"] / 100.0
    else:
        w = (_pos_weight(m.get("position")) / total_pos_weight) * remaining_mass if total_pos_weight > 0 else 0.0
    if m.get("half_weight"):
        w *= 0.5
    return w

grain_whole_ew = sum(bw_no_penalty(m) for m in final_markers if m["class"] == "whole" and m["label"] in GRAIN_WHOLE_LABELS)
non_grain_whole_ew = sum(bw_no_penalty(m) for m in final_markers if m["class"] == "whole" and m["label"] in NON_GRAIN_WHOLE_LABELS)
abs_cond = grain_whole_ew >= GRAIN_CONTEXT_ABS_FLOOR
rel_cond = (non_grain_whole_ew == 0.0 or grain_whole_ew >= GRAIN_CONTEXT_REL_FLOOR * non_grain_whole_ew)
has_grain_context = abs_cond and rel_cond

out.append(f"  grain_whole_ew: {grain_whole_ew:.4f} (abs_floor=0.05, abs_cond={abs_cond})")
out.append(f"  non_grain_whole_ew: {non_grain_whole_ew:.4f} (rel_floor=0.50x, rel_cond={rel_cond})")
out.append(f"  has_grain_context: {has_grain_context}")
out.append("")

out.append("=== PER-MARKER EFFECTIVE WEIGHT (v5.1) ===")
whole_weight = 0.0
refined_weight = 0.0
for m in final_markers:
    if m.get("stated_pct") is not None:
        w = m["stated_pct"] / 100.0
    else:
        w = (_pos_weight(m.get("position")) / total_pos_weight) * remaining_mass if total_pos_weight > 0 else 0.0
    if m.get("half_weight"):
        w *= 0.5

    is_sourdough = m["label"] == "sourdough_starter"
    is_non_grain = m["class"] == "whole" and m["label"] in NON_GRAIN_WHOLE_LABELS
    is_grain = m["class"] == "whole" and m["label"] in GRAIN_WHOLE_LABELS

    eff = w
    note = ""
    if is_sourdough:
        eff = 0.0
        note = "NC-2b: zeroed (sourdough neutral)"
    elif is_non_grain and has_grain_context:
        eff = w * 0.5
        note = "M-2 penalty 0.5x"

    if m["class"] == "whole":
        whole_weight += eff
    else:
        refined_weight += eff

    out.append(f"  {m['label']:<30} class={m['class']:<8} stated={str(m['stated_pct']):<6} pos={m['position']} base_w={w:.4f} eff_w={eff:.4f}  {note}")

total_weight = whole_weight + refined_weight
dominance_ratio = whole_weight / total_weight if total_weight > 0 else 0.0
out.append("")
out.append(f"  whole_weight:   {whole_weight:.4f}")
out.append(f"  refined_weight: {refined_weight:.4f}")
out.append(f"  total_weight:   {total_weight:.4f}")
out.append(f"  dominance_ratio (whole/total): {dominance_ratio:.4f}")

# M-1 anchor
highest = max(final_markers, key=lambda m2: (
    m2["stated_pct"] / 100.0 if m2["stated_pct"] is not None else _pos_weight(m2["position"])
))
anchor_class = highest["class"]
out.append(f"  highest-ew marker: {highest['label']} (class={anchor_class})")

ANCHOR_NUDGE = 0.05
dr_orig = dominance_ratio
if anchor_class == "refined" and dominance_ratio > 0.5:
    dominance_ratio = max(0.5, dominance_ratio - ANCHOR_NUDGE)
    out.append(f"  M-1 anchor nudge: refined dominant, ratio {dr_orig:.4f} -> {dominance_ratio:.4f}")
elif anchor_class == "whole" and dominance_ratio < 0.5:
    dominance_ratio = min(0.5, dominance_ratio + ANCHOR_NUDGE)
    out.append(f"  M-1 anchor nudge: whole dominant, ratio {dr_orig:.4f} -> {dominance_ratio:.4f}")
else:
    out.append(f"  M-1 anchor nudge: no change (anchor={anchor_class}, ratio={dr_orig:.4f})")

score = 10.0 + dominance_ratio * 85.0
out.append(f"  FINAL SCORE: {round(score, 1)}")

out.append("")
out.append("=== DOUBLE-COUNTING INVESTIGATION: קמח חיטה לבן ===")
out.append("Label text structure:")
out.append("  Top-level: 'קמח חיטה לבן (75% מהקמח, 40% מהלחם)' -> stated_pct=40 at position 1")
out.append("  Sub-composite inside מחמצת: 'מחמצת חיטה לבן 18% (קמח חיטה לבן, מים)' -> is this parsed as a separate record?")
out.append("")
out.append("Check if a second 'refined_wheat_flour' match appears in any sub-record:")
for i, r in enumerate(records):
    raw = r.get("raw", "")
    text_nm = _name_only_text(r)
    m = re.search(r"קמח חיטה(?!\s+מלאה?)(?!\s+מלא)", text_nm, re.IGNORECASE)
    if m:
        out.append(f"  Record {i+1} pos={r.get('position')} level={r.get('level')} stated={r.get('stated_pct')} eff={r.get('effective_pct')}")
        out.append(f"    name_only: {repr(text_nm[:100])}")
        out.append(f"    'refined_wheat_flour' pattern MATCHES here")
out.append("")
out.append("Dedup outcome for 'refined_wheat_flour': only ONE instance survives (seen_labels dedup).")
out.append("The question: which instance won the dedup race — the top-level (stated_pct=40, pos=1)")
out.append("or the sub-composite instance (stated_pct=? via effective_pct, pos=?)?")

output_path = r"C:\Bari\03_operations\bsip2\proto_v0\analysis\_debug_481180_output.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"Written to {output_path}")
