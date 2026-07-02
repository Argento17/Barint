"""
Compute exact worked numbers for the spec:
- 47% oats vs 39% direct oats under v5
- Granola 28%eff oats vs 39% oats under v5
"""
import sys
sys.path.insert(0, "C:/Bari/03_operations/bsip2/proto_v0/analysis")

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

def compute_score_v5_verbose(markers, label=""):
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

    print(f"  [{label}] grain_ctx={has_grain_whole}, total_stated={total_stated_pct:.4f}, remaining={remaining_mass:.4f}, total_pos_w={total_pos_weight:.4f}")
    for m in markers:
        w = eff_w(m)
        penalty = " (*0.5 non-grain)" if (has_grain_whole and m["class"]=="whole" and m["label"] in NON_GRAIN_WHOLE) else ""
        print(f"    {m['label']:35s} {m['class']:10s} pct={str(m.get('stated_pct')):10s} pos={m.get('position')} -> eff_w={w:.4f}{penalty}")

    ww = sum(eff_w(m) for m in markers if m["class"] == "whole")
    rw = sum(eff_w(m) for m in markers if m["class"] == "refined")
    tot = ww + rw
    dr = ww / tot
    highest = max(markers, key=eff_w)
    anchor_class = highest["class"]
    dr_raw = dr
    NUDGE = 0.05
    if anchor_class == "refined" and dr > 0.5:
        dr = max(0.5, dr - NUDGE)
    elif anchor_class == "whole" and dr < 0.5:
        dr = min(0.5, dr + NUDGE)
    score = round(10 + dr * 85, 1)
    print(f"    ww={ww:.4f} rw={rw:.4f} dom_ratio_raw={dr_raw:.4f} anchor={anchor_class} -> adj_ratio={dr:.4f} -> SCORE={score}")
    return score

m_47oat = [
    {"label":"oat_flakes_plain","class":"whole","position":1,"stated_pct":47.0},
    {"label":"sugar","class":"refined","position":3,"stated_pct":None},
    {"label":"veg_oil_sg","class":"refined","position":4,"stated_pct":None},
    {"label":"glucose_syrup","class":"refined","position":5,"stated_pct":None},
    {"label":"glucose","class":"refined","position":5,"stated_pct":None},
    {"label":"refined_wheat_flour","class":"refined","position":6,"stated_pct":None},
]
m_39oat_raisins = [
    {"label":"oat_flakes_plain","class":"whole","position":1,"stated_pct":39.0},
    {"label":"veg_oil_sg","class":"refined","position":2,"stated_pct":None},
    {"label":"sugar","class":"refined","position":3,"stated_pct":None},
    {"label":"glucose_syrup","class":"refined","position":4,"stated_pct":None},
    {"label":"refined_wheat_flour","class":"refined","position":5,"stated_pct":None},
    {"label":"raisins","class":"whole","position":6,"stated_pct":None},
]
m_38oat_nuts = [
    {"label":"oat_flakes_plain","class":"whole","position":1,"stated_pct":38.0},
    {"label":"veg_oil_sg","class":"refined","position":2,"stated_pct":None},
    {"label":"sugar","class":"refined","position":3,"stated_pct":None},
    {"label":"glucose_syrup","class":"refined","position":4,"stated_pct":None},
    {"label":"glucose","class":"refined","position":4,"stated_pct":None},
    {"label":"refined_wheat_flour","class":"refined","position":5,"stated_pct":None},
    {"label":"nuts","class":"whole","position":6,"stated_pct":4.7},
    {"label":"peanuts","class":"whole","position":6,"stated_pct":0.1269},
    {"label":"almonds","class":"whole","position":8,"stated_pct":0.047},
]
m_granola = [
    {"label":"oat_flakes_plain","class":"whole","position":1,"stated_pct":27.95},
    {"label":"refined_wheat_flour","class":"refined","position":2,"stated_pct":None},
    {"label":"veg_oil_sg","class":"refined","position":3,"stated_pct":None},
    {"label":"sugar","class":"refined","position":4,"stated_pct":None},
    {"label":"corn_flour_refined","class":"refined","position":5,"stated_pct":None},
    {"label":"dates","class":"whole","position":6,"stated_pct":None},
    {"label":"barley_malt","class":"whole","position":7,"stated_pct":None,"half_weight":True},
    {"label":"glucose_syrup","class":"refined","position":9,"stated_pct":None},
    {"label":"glucose","class":"refined","position":9,"stated_pct":None},
]

print("===  WORKED NUMBERS FOR SPEC  ===")
print()
print("Case 1: RP-03 47% direct oats vs 38% direct oats + nuts 4.7%")
s1 = compute_score_v5_verbose(m_47oat, "47%oat")
print()
s2 = compute_score_v5_verbose(m_38oat_nuts, "38%oat+nuts")
print(f"  VERDICT: {s1} > {s2} => {'PASS RP-03' if s1 > s2 else 'FAIL'}")

print()
print("Case 2: RP-08 47% direct oats vs 39% direct oats + raisins pos-only")
s3 = compute_score_v5_verbose(m_47oat, "47%oat")
print()
s4 = compute_score_v5_verbose(m_39oat_raisins, "39%oat+raisins")
print(f"  VERDICT: {s3} > {s4} => {'PASS RP-08' if s3 > s4 else 'FAIL'}")

print()
print("Case 3: RP-04 granola 28%eff vs 39% direct (CORRECTED: 39% should be HIGHER)")
s5 = compute_score_v5_verbose(m_granola, "granola 28%eff")
print()
s6 = compute_score_v5_verbose(m_39oat_raisins, "39%oat+raisins")
print(f"  Gold-set expected: 39%direct > 28%eff")
print(f"  v5 result: {s6} > {s5} => {'CORRECT (gold-set correction confirmed)' if s6 > s5 else 'WRONG'}")
