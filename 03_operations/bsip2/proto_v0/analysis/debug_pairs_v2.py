"""
Debug script v2: The root cause of all three ties is the ANCHOR CAP.

The anchor logic clamps dominance_ratio to exactly 0.5 whenever:
  - raw dom_ratio < 0.5 (more refined than whole by weight)
  - anchor is whole (highest-weight marker is a whole ingredient)

This is architecturally correct but creates a large 'dead zone' in the
sensitive mixed band (dom_ratio 0.35-0.49 all map to score=52.5).

Need to understand the geometry:
  dom_ratio < 0.5, anchor=whole => adj = min(0.5, raw+0.15)
  For raw in [0.35, 0.50): adj = 0.50 always => score = 52.5 always
  For raw in [0.10, 0.35): adj = raw+0.15 => score = 10 + (raw+0.15)*85

So any product with raw dom_ratio in [0.35, 0.50) and whole anchor
gets locked to 52.5. That's the tie factory.
"""

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


# Show the dead-zone geometry
print("=" * 60)
print("DEAD ZONE ANALYSIS: dom_ratio -> score under v4 formula")
print("(anchor=whole, raw dom_ratio < 0.5)")
print("=" * 60)
for raw in [0.30, 0.35, 0.37, 0.39, 0.41, 0.43, 0.45, 0.47, 0.49, 0.50, 0.52, 0.55]:
    adj = min(0.5, raw + 0.15) if raw < 0.5 else raw
    score = 10 + adj * 85
    print(f"  raw={raw:.2f} => adj={adj:.2f} => score={score:.1f}")

print()
print("=" * 60)
print("PROPOSED REDESIGNS: Break the dead zone")
print("=" * 60)

print()
print("OPTION A: Remove the +0.15 boost entirely; map raw dominance linearly")
print("  score = 10 + raw_dom_ratio * 85")
for raw in [0.38, 0.39, 0.43, 0.47]:
    score = 10 + raw * 85
    print(f"  raw={raw:.2f} => score={score:.1f}")

print()
print("OPTION B: Reduce boost to +0.08 (half the current +0.15)")
print("  adj = min(0.5, raw+0.08) if raw<0.5 and anchor=whole")
for raw in [0.38, 0.39, 0.43, 0.47]:
    adj = min(0.5, raw + 0.08)
    score = 10 + adj * 85
    print(f"  raw={raw:.2f} => adj={adj:.2f} => score={score:.1f}")

print()
print("OPTION C: Non-grain penalty (0.5x) to shrink whole_w + remove cap")
print("  => raw dom_ratio changes, then NO ANCHOR CAP, score=10+raw*85")

def compute_raw_dom_ratio(markers, grain_penalty=False):
    GRAIN_WHOLE = {
        "whole_wheat_flour","whole_wheat_grain","whole_spelt_flour","whole_spelt_grain",
        "whole_oat_flour","whole_oat","whole_oat_flakes","whole_rye_flour","whole_rye_grain",
        "whole_corn_flour","whole_barley_flour","whole_rice","oat_groats","hulled_oats",
        "oat_flakes_plain","quinoa","buckwheat","bare_wheat_first_80pct",
    }
    NON_GRAIN_WHOLE = {
        "nuts","almonds","peanuts","pistachios","cashews",
        "seeds_specific","seeds_generic","sesame_seeds","chia_seeds","flax_seeds",
        "dates","raisins","tahini","olive_oil","butter_dairy",
    }
    has_grain_whole = any(m["label"] in GRAIN_WHOLE for m in markers if m["class"]=="whole")

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
        if grain_penalty and has_grain_whole and m["class"]=="whole" and m["label"] in NON_GRAIN_WHOLE:
            w *= 0.5
        return w

    ww = sum(eff_w(m) for m in markers if m["class"]=="whole")
    rw = sum(eff_w(m) for m in markers if m["class"]=="refined")
    tot = ww + rw
    if tot < 0.01: return None, None, None
    return ww/tot, ww, rw


# Products
m_47oat = [
    {"label":"oat_flakes_plain","class":"whole","position":1,"stated_pct":47.0},
    {"label":"sugar","class":"refined","position":3,"stated_pct":None},
    {"label":"veg_oil_sg","class":"refined","position":4,"stated_pct":None},
    {"label":"glucose_syrup","class":"refined","position":5,"stated_pct":None},
    {"label":"glucose","class":"refined","position":5,"stated_pct":None},
    {"label":"refined_wheat_flour","class":"refined","position":6,"stated_pct":None},
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
m_39oat_raisins = [
    {"label":"oat_flakes_plain","class":"whole","position":1,"stated_pct":39.0},
    {"label":"veg_oil_sg","class":"refined","position":2,"stated_pct":None},
    {"label":"sugar","class":"refined","position":3,"stated_pct":None},
    {"label":"glucose_syrup","class":"refined","position":4,"stated_pct":None},
    {"label":"refined_wheat_flour","class":"refined","position":5,"stated_pct":None},
    {"label":"raisins","class":"whole","position":6,"stated_pct":None},
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

print()
print("Raw dom_ratios with grain_penalty=True (non-grain whole at 0.5x):")
for name, markers in [
    ("47%oat (RP-03/08 higher)", m_47oat),
    ("38%oat+nuts (RP-03 lower)", m_38oat_nuts),
    ("39%oat+raisins (RP-04/08 lower)", m_39oat_raisins),
    ("granola 27.95% (RP-04 higher)", m_granola),
]:
    dr, ww, rw = compute_raw_dom_ratio(markers, grain_penalty=True)
    if dr is not None:
        score_no_cap = 10 + dr * 85
        print(f"  {name:40s} dom_ratio={dr:.4f} ww={ww:.4f} rw={rw:.4f} score_no_cap={score_no_cap:.1f}")

print()
print("=" * 60)
print("PROPOSED FORMULA v5:")
print("  1. Non-grain whole markers: 0.5x weight in grain-context products")
print("  2. First-ingredient anchor: CAPPED at +/-0.05 (not 0.15)")
print("     Rationale: smaller nudge means less dead-zone; monotonicity preserved")
print("=" * 60)

def compute_score_v5(markers):
    GRAIN_WHOLE = {
        "whole_wheat_flour","whole_wheat_grain","whole_spelt_flour","whole_spelt_grain",
        "whole_oat_flour","whole_oat","whole_oat_flakes","whole_rye_flour","whole_rye_grain",
        "whole_corn_flour","whole_barley_flour","whole_rice","oat_groats","hulled_oats",
        "oat_flakes_plain","quinoa","buckwheat","bare_wheat_first_80pct",
    }
    NON_GRAIN_WHOLE = {
        "nuts","almonds","peanuts","pistachios","cashews",
        "seeds_specific","seeds_generic","sesame_seeds","chia_seeds","flax_seeds",
        "dates","raisins","tahini","olive_oil","butter_dairy",
    }
    has_grain_whole = any(m["label"] in GRAIN_WHOLE for m in markers if m["class"]=="whole")

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
        if has_grain_whole and m["class"]=="whole" and m["label"] in NON_GRAIN_WHOLE:
            w *= 0.5
        return w

    ww = sum(eff_w(m) for m in markers if m["class"]=="whole")
    rw = sum(eff_w(m) for m in markers if m["class"]=="refined")
    tot = ww + rw
    if tot < 0.01: return None

    dr = ww / tot
    highest = max(markers, key=eff_w)
    anchor_class = highest["class"]

    # Reduced anchor: +/-0.05 instead of +/-0.15
    ANCHOR_NUDGE = 0.05
    if anchor_class == "refined" and dr > 0.5:
        dr = max(0.5, dr - ANCHOR_NUDGE)
    elif anchor_class == "whole" and dr < 0.5:
        dr = min(0.5, dr + ANCHOR_NUDGE)

    return round(10 + dr * 85, 1)

print()
for name, markers in [
    ("47%oat (RP-03/08 higher)", m_47oat),
    ("38%oat+nuts (RP-03 lower)", m_38oat_nuts),
    ("39%oat+raisins (RP-04/08 lower)", m_39oat_raisins),
    ("granola 27.95% (RP-04 higher)", m_granola),
]:
    s = compute_score_v5(markers)
    print(f"  v5 score: {name:40s} = {s}")

print()
s_47 = compute_score_v5(m_47oat)
s_38n = compute_score_v5(m_38oat_nuts)
s_39r = compute_score_v5(m_39oat_raisins)
s_gr = compute_score_v5(m_granola)
print("RP-03: 47%oat vs 38%+nuts =>", s_47, "vs", s_38n, "=>", "PASS" if s_47 and s_38n and s_47 > s_38n else "FAIL")
print("RP-08: 47%oat vs 39%+raisins =>", s_47, "vs", s_39r, "=>", "PASS" if s_47 and s_39r and s_47 > s_39r else "FAIL")
print("RP-04: granola27.95% vs 39%+raisins =>", s_gr, "vs", s_39r, "=>", "PASS" if s_gr and s_39r and s_gr > s_39r else "FAIL")

# Now also check that existing passing pairs still pass
print()
print("=" * 60)
print("Checking: do existing passing pairs still pass under v5?")
print("=" * 60)
# RP-01: bread 71.2% whole vs cracker 30.5%
m_bread_100ww = [
    {"label":"whole_wheat_flour","class":"whole","position":1,"stated_pct":58.0},
    {"label":"refined_wheat_flour","class":"refined","position":2,"stated_pct":None},
    {"label":"sugar","class":"refined","position":3,"stated_pct":None},
]
m_cracker_305 = [
    {"label":"whole_wheat_flour","class":"whole","position":1,"stated_pct":30.5},
    {"label":"rice_flour_refined","class":"refined","position":2,"stated_pct":25.5},
    {"label":"refined_wheat_flour","class":"refined","position":3,"stated_pct":17.0},
    {"label":"whole_rice","class":"whole","position":5,"stated_pct":6.8},
]
s1 = compute_score_v5(m_bread_100ww)
s2 = compute_score_v5(m_cracker_305)
print(f"RP-01: 58%whole bread={s1} vs 30.5%whole cracker={s2} => {'PASS' if s1 and s2 and s1>s2 else 'FAIL'}")
