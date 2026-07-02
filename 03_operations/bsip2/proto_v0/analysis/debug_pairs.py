"""Debug script for analyzing v4 formula tie mechanics in RP-03/04/08."""

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

def compute_score_detailed(markers, label=""):
    pct_markers = [m for m in markers if m.get("stated_pct") is not None]
    pos_markers  = [m for m in markers if m.get("stated_pct") is None]
    total_stated_pct = sum(m["stated_pct"] for m in pct_markers) / 100.0
    total_stated_pct = min(total_stated_pct, 1.0)
    remaining_mass   = max(0.0, 1.0 - total_stated_pct)
    total_pos_weight = sum(pos_weight(m.get("position")) for m in pos_markers)

    def eff_w(m):
        if m.get("stated_pct") is not None:
            w = m["stated_pct"] / 100.0
        else:
            if total_pos_weight > 0:
                w = (pos_weight(m.get("position")) / total_pos_weight) * remaining_mass
            else:
                w = 0.0
        if m.get("half_weight"): w *= 0.5
        return w

    print(f"\n--- {label} ---")
    print(f"  total_stated={total_stated_pct:.4f}, remaining={remaining_mass:.4f}, total_pos_w={total_pos_weight:.4f}")
    for m in markers:
        w = eff_w(m)
        hw = m.get("half_weight", False)
        print(f"  {m['label']:35s} {m['class']:10s} pct={str(m.get('stated_pct')):10s} pos={m.get('position')} eff_w={w:.4f} half={hw}")

    whole_weight   = sum(eff_w(m) for m in markers if m["class"] == "whole")
    refined_weight = sum(eff_w(m) for m in markers if m["class"] == "refined")
    total_weight = whole_weight + refined_weight
    if total_weight < 0.01:
        print("  No markers — None")
        return None

    dominance_ratio = whole_weight / total_weight
    highest = max(markers, key=eff_w)
    anchor_class = highest["class"]
    dr_before = dominance_ratio

    if anchor_class == "refined" and dominance_ratio > 0.5:
        dominance_ratio = max(0.5, dominance_ratio - 0.15)
    elif anchor_class == "whole" and dominance_ratio < 0.5:
        dominance_ratio = min(0.5, dominance_ratio + 0.15)

    score = 10.0 + dominance_ratio * 85.0
    print(f"  whole_w={whole_weight:.4f}, refined_w={refined_weight:.4f}")
    print(f"  dom_ratio_raw={dr_before:.4f}, anchor={anchor_class}, dom_ratio_adj={dominance_ratio:.4f}")
    print(f"  SCORE = {round(score, 1)}")
    return round(score, 1)


# RP-03: 7290016883176 (oats 47%) vs 7290011131371 (oats 38% + nuts 4.7%)
m_47oat = [
    {"label": "oat_flakes_plain",     "class": "whole",   "position": 1, "stated_pct": 47.0},
    {"label": "sugar",                "class": "refined",  "position": 3, "stated_pct": None},
    {"label": "veg_oil_sg",           "class": "refined",  "position": 4, "stated_pct": None},
    {"label": "glucose_syrup",        "class": "refined",  "position": 5, "stated_pct": None},
    {"label": "glucose",              "class": "refined",  "position": 5, "stated_pct": None},
    {"label": "refined_wheat_flour",  "class": "refined",  "position": 6, "stated_pct": None},
]

m_38oat_nuts = [
    {"label": "oat_flakes_plain",     "class": "whole",   "position": 1, "stated_pct": 38.0},
    {"label": "veg_oil_sg",           "class": "refined",  "position": 2, "stated_pct": None},
    {"label": "sugar",                "class": "refined",  "position": 3, "stated_pct": None},
    {"label": "glucose_syrup",        "class": "refined",  "position": 4, "stated_pct": None},
    {"label": "glucose",              "class": "refined",  "position": 4, "stated_pct": None},
    {"label": "refined_wheat_flour",  "class": "refined",  "position": 5, "stated_pct": None},
    {"label": "nuts",                 "class": "whole",   "position": 6, "stated_pct": 4.7},
    {"label": "peanuts",              "class": "whole",   "position": 6, "stated_pct": 0.1269},
    {"label": "almonds",              "class": "whole",   "position": 8, "stated_pct": 0.047},
]

# RP-08: same 47oat vs 39oat+raisins
m_39oat_raisins = [
    {"label": "oat_flakes_plain",     "class": "whole",   "position": 1, "stated_pct": 39.0},
    {"label": "veg_oil_sg",           "class": "refined",  "position": 2, "stated_pct": None},
    {"label": "sugar",                "class": "refined",  "position": 3, "stated_pct": None},
    {"label": "glucose_syrup",        "class": "refined",  "position": 4, "stated_pct": None},
    {"label": "refined_wheat_flour",  "class": "refined",  "position": 5, "stated_pct": None},
    {"label": "raisins",              "class": "whole",   "position": 6, "stated_pct": None},
]

# RP-04: granola (oats 27.95% effective) vs 39oat+raisins
m_granola = [
    {"label": "oat_flakes_plain",     "class": "whole",   "position": 1, "stated_pct": 27.95},
    {"label": "refined_wheat_flour",  "class": "refined",  "position": 2, "stated_pct": None},
    {"label": "veg_oil_sg",           "class": "refined",  "position": 3, "stated_pct": None},
    {"label": "sugar",                "class": "refined",  "position": 4, "stated_pct": None},
    {"label": "corn_flour_refined",   "class": "refined",  "position": 5, "stated_pct": None},
    {"label": "dates",                "class": "whole",   "position": 6, "stated_pct": None},
    {"label": "barley_malt",          "class": "whole",   "position": 7, "stated_pct": None, "half_weight": True},
    {"label": "glucose_syrup",        "class": "refined",  "position": 9, "stated_pct": None},
    {"label": "glucose",              "class": "refined",  "position": 9, "stated_pct": None},
]

print("=" * 60)
print("RP-03: oats 47% vs oats 38% + nuts 4.7%")
print("=" * 60)
s1 = compute_score_detailed(m_47oat, "7290016883176 (oats 47%)")
s2 = compute_score_detailed(m_38oat_nuts, "7290011131371 (oats 38% + nuts)")
print(f"\n  RESULT: {s1} vs {s2} => {'PASS' if s1 and s2 and s1 > s2 else 'FAIL'}")

print("\n" + "=" * 60)
print("RP-08: oats 47% vs oats 39% + raisins (position only)")
print("=" * 60)
s3 = compute_score_detailed(m_47oat, "7290016883176 (oats 47%)")
s4 = compute_score_detailed(m_39oat_raisins, "7290011131388 (oats 39% + raisins)")
print(f"\n  RESULT: {s3} vs {s4} => {'PASS' if s3 and s4 and s3 > s4 else 'FAIL'}")

print("\n" + "=" * 60)
print("RP-04: granola 27.95% effective vs oats 39% + raisins")
print("=" * 60)
s5 = compute_score_detailed(m_granola, "7290011131975 (granola 27.95% eff)")
s6 = compute_score_detailed(m_39oat_raisins, "7290011131388 (oats 39% + raisins)")
print(f"\n  RESULT: {s5} vs {s6} => {'PASS' if s5 and s6 and s5 > s6 else 'FAIL'}")

print("\n\n" + "=" * 60)
print("NOW: Proposed fix — grain-weighted scoring")
print("Non-grain whole markers get 0.5x weight in grain context")
print("=" * 60)

def compute_score_v5(markers, grain_context=True):
    """
    v5: non-grain whole contributors (nuts/seeds/dried-fruit) get 0.5x weight
    when the product is grain-context (has at least one grain whole marker).
    """
    GRAIN_WHOLE = {
        "whole_wheat_flour", "whole_wheat_grain", "whole_spelt_flour", "whole_spelt_grain",
        "whole_oat_flour", "whole_oat", "whole_oat_flakes", "whole_rye_flour", "whole_rye_grain",
        "whole_corn_flour", "whole_barley_flour", "whole_rice", "oat_groats", "hulled_oats",
        "oat_flakes_plain", "quinoa", "buckwheat",
        "bare_wheat_first_80pct",
    }
    NON_GRAIN_WHOLE = {
        "nuts", "almonds", "peanuts", "pistachios", "cashews",
        "seeds_specific", "seeds_generic", "sesame_seeds", "chia_seeds", "flax_seeds",
        "dates", "raisins", "tahini", "olive_oil", "butter_dairy",
    }
    # barley_malt and sourdough_starter already have half_weight=True

    # Determine if this is a grain context
    has_grain_whole = any(m["label"] in GRAIN_WHOLE for m in markers)

    pct_markers = [m for m in markers if m.get("stated_pct") is not None]
    pos_markers  = [m for m in markers if m.get("stated_pct") is None]
    total_stated_pct = sum(m["stated_pct"] for m in pct_markers) / 100.0
    total_stated_pct = min(total_stated_pct, 1.0)
    remaining_mass   = max(0.0, 1.0 - total_stated_pct)
    total_pos_weight = sum(pos_weight(m.get("position")) for m in pos_markers)

    def eff_w(m):
        if m.get("stated_pct") is not None:
            w = m["stated_pct"] / 100.0
        else:
            if total_pos_weight > 0:
                w = (pos_weight(m.get("position")) / total_pos_weight) * remaining_mass
            else:
                w = 0.0
        if m.get("half_weight"): w *= 0.5
        # Non-grain whole contributors in grain context get additional 0.5x
        if has_grain_whole and m["class"] == "whole" and m["label"] in NON_GRAIN_WHOLE:
            w *= 0.5
        return w

    whole_weight   = sum(eff_w(m) for m in markers if m["class"] == "whole")
    refined_weight = sum(eff_w(m) for m in markers if m["class"] == "refined")
    total_weight = whole_weight + refined_weight
    if total_weight < 0.01: return None

    dominance_ratio = whole_weight / total_weight
    highest = max(markers, key=eff_w)
    anchor_class = highest["class"]

    if anchor_class == "refined" and dominance_ratio > 0.5:
        dominance_ratio = max(0.5, dominance_ratio - 0.15)
    elif anchor_class == "whole" and dominance_ratio < 0.5:
        dominance_ratio = min(0.5, dominance_ratio + 0.15)

    score = 10.0 + dominance_ratio * 85.0
    return round(score, 1)

print("\nRP-03:")
a = compute_score_v5(m_47oat)
b = compute_score_v5(m_38oat_nuts)
print(f"  47%oat={a}, 38%+nuts={b} => {'PASS' if a and b and a > b else 'FAIL'}")

print("RP-08:")
c = compute_score_v5(m_47oat)
d = compute_score_v5(m_39oat_raisins)
print(f"  47%oat={c}, 39%+raisins={d} => {'PASS' if c and d and c > d else 'FAIL'}")

print("RP-04:")
e = compute_score_v5(m_granola)
f = compute_score_v5(m_39oat_raisins)
print(f"  granola27.95%={e}, 39%+raisins={f} => {'PASS' if e and f and e > f else 'FAIL'}")
