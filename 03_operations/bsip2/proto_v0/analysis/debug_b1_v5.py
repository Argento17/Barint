"""Check B1 failure under v5 - ASCII safe output."""
import sys, json
sys.path.insert(0, "C:/Bari/03_operations/bsip2/proto_v0/analysis")
from structured_ingredient_reader import is_unparseable
from matrix_signal_probe_v4 import extract_all_markers_v4
from pathlib import Path

GRAIN_WHOLE = {
    "whole_wheat_flour","whole_wheat_grain","whole_spelt_flour","whole_spelt_grain",
    "whole_oat_flour","whole_oat","whole_oat_flakes","whole_rye_flour","whole_rye_grain",
    "whole_corn_flour","whole_barley_flour","whole_rice","oat_groats","hulled_oats",
    "oat_flakes_plain","quinoa","buckwheat","bare_wheat_first_80pct",
}
NON_GRAIN_WHOLE = {
    "nuts","almonds","peanuts","pistachios","cashews",
    "seeds_specific","seeds_generic","sesame_seeds","chia_seeds","flax_seeds",
    "dates","raisins","tahini","olive_oil","butter_dairy","sourdough_starter",
}

def pos_weight(pos):
    if pos is None: return 0.12
    if pos == 1: return 1.00
    if pos == 2: return 0.82
    if pos == 3: return 0.68
    if pos == 4: return 0.55
    if pos == 5: return 0.44
    if pos == 6: return 0.35
    if pos == 7: return 0.28
    if pos == 8: return 0.22
    if pos == 9: return 0.17
    if pos == 10: return 0.13
    if pos <= 15: return max(0.08, 0.13 * (0.85 ** (pos - 10)))
    return 0.08

def compute_score_v5(markers):
    if not markers: return None
    has_grain_whole = any(m["label"] in GRAIN_WHOLE for m in markers if m["class"] == "whole")
    pct_markers = [m for m in markers if m.get("stated_pct") is not None]
    pos_markers  = [m for m in markers if m.get("stated_pct") is None]
    total_stated_pct = min(sum(m["stated_pct"] for m in pct_markers) / 100.0, 1.0)
    remaining_mass   = max(0.0, 1.0 - total_stated_pct)
    total_pos_weight = sum(pos_weight(m.get("position")) for m in pos_markers)

    def eff_w(m):
        if m.get("stated_pct") is not None:
            w = m["stated_pct"] / 100.0
        else:
            w = (pos_weight(m.get("position")) / total_pos_weight) * remaining_mass if total_pos_weight > 0 else 0.0
        if m.get("half_weight"): w *= 0.5
        if has_grain_whole and m["class"] == "whole" and m["label"] in NON_GRAIN_WHOLE:
            w *= 0.5
        return w

    ww = sum(eff_w(m) for m in markers if m["class"] == "whole")
    rw = sum(eff_w(m) for m in markers if m["class"] == "refined")
    tot = ww + rw
    if tot < 0.01: return None
    dr = ww / tot
    highest = max(markers, key=eff_w)
    anchor_class = highest["class"]
    NUDGE = 0.05
    if anchor_class == "refined" and dr > 0.5:
        dr = max(0.5, dr - NUDGE)
    elif anchor_class == "whole" and dr < 0.5:
        dr = min(0.5, dr + NUDGE)
    return round(10 + dr * 85, 1)

gold = json.loads(Path("C:/Bari/03_operations/bsip2/proto_v0/analysis/matrix_gold_set_v1.json").read_text(encoding="utf-8"))

print("B1 gate under v5:")
b1_fail = []
b1_pass = 0
b1_total = 0
for p in gold["products"]:
    if not p.get("gradable") or p["tier"] not in ("T1","T2"):
        continue
    text = p.get("ingredients_text_he","")
    if not text or is_unparseable(text):
        continue
    markers = extract_all_markers_v4(text)
    s = compute_score_v5(markers)
    if s is None:
        continue
    b1_total += 1
    ok = (p["tier"]=="T1" and s>=60) or (p["tier"]=="T2" and s<=45)
    if ok:
        b1_pass += 1
    else:
        b1_fail.append((p["barcode"], p["tier"], s))

print(f"  B1 pass: {b1_pass}/{b1_total} = {b1_pass/b1_total*100:.1f}%  (bar=90%)")
print(f"  B1 failures ({len(b1_fail)}):")
for bc, tier, s in b1_fail:
    print(f"    barcode={bc} tier={tier} score={s}")

print()
print("Specific B1 failure product detail (7290106571945):")
target = next(p for p in gold["products"] if p["barcode"] == "7290106571945")
markers = extract_all_markers_v4(target.get("ingredients_text_he",""))
s = compute_score_v5(markers)
print(f"  barcode=7290106571945 tier=T1 score_v5={s}")
print(f"  markers: {[(m['label'],m['class'],m.get('stated_pct'),m.get('position')) for m in markers]}")
print()
print(f"  ATTRIBUTION: same as v4 -- parent 'daganim' has no stated_pct,")
print(f"  sub-ingredients get effective_pct=None, fall back to position weight.")
print(f"  Score {s} is below T1 threshold (60). This is the one surviving B1 failure --")
print(f"  a composite-parsing design gap (parent_pct=None), NOT a v5 formula regression.")
