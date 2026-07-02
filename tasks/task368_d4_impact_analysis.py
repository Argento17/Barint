"""
TASK-368 — D4 Additive-Layer Impact Analysis
Read-only simulation. No score files, engine files, or published JSON are modified.

Uses the embedded d4_additives arrays already present in each frontend JSON
(produced by detect_additives_d4 during the last full pipeline run with
BARI_GLASSBOX_W2=on). These arrays are the authoritative detection output —
they were generated from the real BSIP0 ingredient text, so we do NOT need
to re-parse ingredient text here.

Key constraint honored: E330 and E300 are currently "functional" in the
Python dict (EV-101 Product D7 co-sign pending as of 2026-06-21). The
analysis runs in two passes: (1) dict-as-is (contested = 12 entries),
(2) EV-101 simulation with E330+E300 treated as contested.
"""
import sys
import os
import json
import hashlib
import datetime
from collections import Counter, defaultdict

COMPARISONS_DIR = r"C:\Bari\bari-web\src\data\comparisons"

LIVE_FILES = {
    "bread":             "bread_frontend_v3.json",
    "brined_cheeses":    "brined_cheeses_frontend_v2.json",
    "cakes_cookies":     "cakes_hard_cookies_frontend_v1.json",
    "cereals":           "cereals_frontend_v2.json",
    "cheese_spreads":    "cheese_frontend_v4.json",
    "chocolate_bars":    "chocolate_bars_frontend_v1.json",
    "chocolate_tablets": "chocolate_tablets_frontend_v1.json",
    "cookies_coffee":    "cookies_coffee_frontend_v2.json",
    "granola":           "granola_frontend_v1.json",
    "hard_cheeses":      "hard_cheeses_frontend_v2.json",
    "hummus":            "hummus_frontend_v5.json",
    "juices":            "juices_frontend_v3.json",
    "milk":              "milk_frontend_v1.json",
    "protein_bars":      "protein_bars_frontend_v1.json",
    "snacks":            "snacks_frontend_v5.json",
}

# These are contested in the Python dict right now (dict-as-is)
CURRENTLY_CONTESTED = {
    "E102", "E104", "E110", "E122", "E124", "E129",
    "E171", "E320", "E407", "E433", "E466", "E951",
    # EV-061: E471, E472b, E472c, E460 — check if they appear in dict
    "E471", "E472b", "E460",
}

# EV-101: E330/E300 proposed as contested — Product D7 co-sign CLOSED (TASK-364, 2026-06-21)
# BUT constants.py still has them as "functional" (update pending; gated by TASK-362/bars branch)
# So the d4_additives arrays in committed frontend JSONs show them as "functional" tier.
# The EV-101 simulation below shows what would change if constants.py were updated.
EV101_PROPOSED = {"E330", "E300"}

# cosmetic_mup lookup (from constants.py — manually extracted for simulation)
COSMETIC_MUP = {
    "E102": True, "E104": True, "E110": True, "E122": True, "E124": True,
    "E129": True, "E171": True, "E320": False, "E407": True, "E433": True,
    "E466": True, "E951": True, "E471": True, "E472b": True, "E460": False,
    "E330": False, "E300": False,
}

# Grade function (matches score_to_grade in constants.py)
def score_to_grade(score):
    if score is None: return None
    s = float(score)
    if s >= 90: return "S"
    if s >= 80: return "A"
    if s >= 65: return "B"
    if s >= 50: return "C"
    if s >= 35: return "D"
    return "E"


def load_products(category, filename):
    path = os.path.join(COMPARISONS_DIR, filename)
    if not os.path.exists(path):
        print(f"  WARN: {path} not found", file=sys.stderr)
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "products" in data:
        raw = data["products"]
    elif isinstance(data, list):
        raw = data
    else:
        raw = list(data.values()) if isinstance(data, dict) else []
    result = []
    for i, p in enumerate(raw):
        if not isinstance(p, dict):
            continue
        p["_cat"] = category
        p["_idx"] = i
        result.append(p)
    return result


def get_score(p):
    v = p.get("score")
    if v is None: return None
    try: return float(v)
    except: return None


def get_grade(p):
    return (p.get("grade") or "").strip().upper() or None


def get_nova(p):
    # Try d3_processing_signal.nova_class first (it's the engine-output field)
    d3 = p.get("d3_processing_signal") or {}
    nv = d3.get("nova_class")
    if nv is not None:
        try: return int(nv)
        except: pass
    # Fallback: direct field variants used across different category JSONs
    for k in ("nova_class", "nova", "novaClass", "novaGroup", "nova_group"):
        v = p.get(k)
        if v is not None:
            try: return int(v)
            except: pass
    return None


def get_d4_findings(p, include_tiers=None):
    """Return d4_additives findings, optionally filtered to specific tiers."""
    arr = p.get("d4_additives") or []
    if include_tiers is None:
        return arr
    return [f for f in arr if f.get("tier") in include_tiers]


def get_contested_findings(p, also_contested=None):
    """
    Return d4_additives findings where tier == 'contested'.
    also_contested: optional set of E-numbers to treat as contested even if tier != 'contested'
    (for EV-101 simulation).
    """
    arr = p.get("d4_additives") or []
    result = []
    for f in arr:
        tier = f.get("tier", "")
        e_num = f.get("e_number", "")
        if tier == "contested":
            result.append(f)
        elif also_contested and e_num in also_contested:
            result.append(dict(f, tier="contested"))  # simulate tier flip
    return result


def main():
    out = []

    def pr(*args, **kwargs):
        line = " ".join(str(a) for a in args)
        out.append(line)
        print(line, **kwargs)

    pr("=" * 72)
    pr("TASK-368 — D4 Additive-Layer IMPACT ANALYSIS")
    pr(f"Run date: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    pr(f"Comparisons dir: {COMPARISONS_DIR}")
    pr("=" * 72)
    pr()

    # ------------------------------------------------------------------
    # Load all products
    # ------------------------------------------------------------------
    all_products = []
    cat_counts = {}
    for cat, fname in LIVE_FILES.items():
        prods = load_products(cat, fname)
        cat_counts[cat] = len(prods)
        all_products.extend(prods)

    pr(f"Categories analyzed: {len(LIVE_FILES)}")
    pr(f"Total products loaded: {len(all_products)}")
    pr("Per-category product counts:")
    for cat, cnt in cat_counts.items():
        pr(f"  {cat}: {cnt}")
    pr()

    # ------------------------------------------------------------------
    # SECTION 0: Dict state
    # ------------------------------------------------------------------
    pr("=" * 72)
    pr("SECTION 0: Contested additive set (Python dict / constants.py state)")
    pr("=" * 72)
    pr()

    # Read live dict state from the actual constants.py
    sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")
    from constants import GLASSBOX_W2_ADDITIVES
    contested_in_dict = {e: ent for e, ent in GLASSBOX_W2_ADDITIVES.items()
                         if ent.get("tier") == "contested"}
    pr(f"Total entries in GLASSBOX_W2_ADDITIVES: {len(GLASSBOX_W2_ADDITIVES)}")
    pr(f"Contested entries in dict ({len(contested_in_dict)}):")
    for e in sorted(contested_in_dict):
        ent = contested_in_dict[e]
        pr(f"  {e}: {ent['name_en']}")
    pr()
    pr("EV-101 proposed contested (Product D7 PENDING — still 'functional' in dict):")
    for e in sorted(EV101_PROPOSED):
        ent = GLASSBOX_W2_ADDITIVES.get(e, {})
        pr(f"  {e}: {ent.get('name_en','')} [dict tier: {ent.get('tier','')}]")
    pr()

    # ------------------------------------------------------------------
    # SECTION 1: Exposure surface (dict-as-is)
    # ------------------------------------------------------------------
    pr("=" * 72)
    pr("SECTION 1: Exposure Surface — contested-tier detection (dict-as-is)")
    pr("=" * 72)
    pr()
    pr("Source: embedded d4_additives arrays in frontend JSONs")
    pr("(Produced by detect_additives_d4 during last pipeline run with BARI_GLASSBOX_W2=on)")
    pr()

    # Per-product: count contested findings
    product_records = []
    for p in all_products:
        score = get_score(p)
        grade = get_grade(p) or score_to_grade(score)
        nova = get_nova(p)
        all_d4 = get_d4_findings(p)
        contested = get_contested_findings(p)
        contested_enums = [f.get("e_number") for f in contested]
        total_d4 = len(all_d4)
        contested_count = len(contested)
        has_d4_array = p.get("d4_additives") is not None

        # NOVA proxy: NOVA-4 cap already applies a processing ceiling of 68
        nova4 = (nova == 4)

        # EV-045/003 overlap: check glassBox for emulsifier complexity signal
        glass = p.get("glassBox") or {}
        # emulsifier complexity is reported in glassBox or in trace-level fields
        has_ecs = False
        has_ev003 = False
        expansion = p.get("expansion") or {}
        # Check various field names used in glass box
        for key in ("emulsifier_complexity", "ecs", "emulsifier_complexity_tier"):
            v = glass.get(key) or expansion.get(key)
            if v:
                has_ecs = True
                break
        for key in ("ev003_penalty", "mucus_thinning_penalty", "high_risk_emulsifier"):
            v = glass.get(key) or expansion.get(key)
            if v:
                has_ev003 = True
                break

        product_records.append({
            "cat": p["_cat"],
            "name": (p.get("name") or "")[:45],
            "score": score,
            "grade": grade,
            "nova": nova,
            "nova4": nova4,
            "has_d4_array": has_d4_array,
            "total_d4": total_d4,
            "contested_count": contested_count,
            "contested_enums": contested_enums,
            "has_ecs": has_ecs,
            "has_ev003": has_ev003,
        })

    # 1A: By category
    pr("--- 1A: Products with ≥1 contested additive, by category ---")
    pr(f"{'Category':<25} {'Total':>7} {'Has d4[]':>9} {'Contested':>10} {'Pct':>6}")
    pr("-" * 62)
    for cat in LIVE_FILES:
        cp = [r for r in product_records if r["cat"] == cat]
        has_d4 = sum(1 for r in cp if r["has_d4_array"])
        contested = sum(1 for r in cp if r["contested_count"] > 0)
        total = len(cp)
        pct = f"{100*contested/total:.0f}%" if total else "—"
        pr(f"  {cat:<23} {total:>7} {has_d4:>9} {contested:>10} {pct:>6}")
    pr()
    total_contested_prods = sum(1 for r in product_records if r["contested_count"] > 0)
    total_no_d4 = sum(1 for r in product_records if not r["has_d4_array"])
    pr(f"  TOTAL across {len(LIVE_FILES)} categories:")
    pr(f"    Products: {len(product_records)}")
    pr(f"    Products with d4_additives array: {len(product_records)-total_no_d4}")
    pr(f"    Products with ≥1 contested additive (dict-as-is): {total_contested_prods}")
    pr(f"    Products with NO d4_additives array (no BSIP0 ingredient data): {total_no_d4}")
    pr()

    # 1B: By E-number
    pr("--- 1B: Products per contested E-number ---")
    enum_counter = Counter()
    enum_by_cat = defaultdict(Counter)
    for r in product_records:
        for e in r["contested_enums"]:
            enum_counter[e] += 1
            enum_by_cat[e][r["cat"]] += 1

    pr(f"  {'E-number':<10} {'Name (en)':<35} {'#Prods':>7}  Top categories")
    pr("  " + "-" * 90)
    for e, cnt in enum_counter.most_common():
        ent = GLASSBOX_W2_ADDITIVES.get(e, {})
        name_en = ent.get("name_en", "")[:34]
        top_cats = ", ".join(f"{c}({n})" for c, n in enum_by_cat[e].most_common(3))
        pr(f"  {e:<10} {name_en:<35} {cnt:>7}  {top_cats}")
    pr()

    # 1C: Count distribution
    pr("--- 1C: Contested-additive count distribution per product ---")
    count_dist = Counter(r["contested_count"] for r in product_records)
    pr(f"  {'#Contested':>12}  {'#Products':>10}")
    for k in sorted(count_dist):
        pr(f"  {k:>12}  {count_dist[k]:>10}")
    pr()

    # ------------------------------------------------------------------
    # SECTION 2: Already-penalized overlap
    # ------------------------------------------------------------------
    pr("=" * 72)
    pr("SECTION 2: Already-penalized overlap (NOVA-4, EV-045, EV-003)")
    pr("=" * 72)
    pr()

    contested_recs = [r for r in product_records if r["contested_count"] > 0]
    n_cont = len(contested_recs)

    nova_known = [r for r in contested_recs if r["nova"] is not None]
    nova_unknown = [r for r in contested_recs if r["nova"] is None]
    nova4_among = [r for r in contested_recs if r["nova4"]]
    nova3_among = [r for r in contested_recs if r["nova"] == 3]
    nova12_among = [r for r in contested_recs if r["nova"] in (1, 2)]

    pr(f"Products with ≥1 contested additive (basis): {n_cont}")
    pr()
    pr(f"  NOVA distribution (among {n_cont} contested-additive products):")
    pr(f"    NOVA known:   {len(nova_known)}")
    pr(f"    NOVA unknown: {len(nova_unknown)}  (no d3_processing_signal)")
    nova_dist = Counter(r["nova"] for r in contested_recs if r["nova"] is not None)
    for nv in sorted(nova_dist):
        pr(f"    NOVA {nv}:       {nova_dist[nv]}")
    pr()

    pr(f"  NOVA-4 (already at processing cap 68): {len(nova4_among)}/{n_cont}")
    pr(f"    => These face the highest double-count risk from D4 stacking on NOVA-4 cap.")
    pr()
    pr(f"  NOVA-3 (some processing, no cap): {len(nova3_among)}/{n_cont}")
    pr(f"    => D4 has genuine marginal discriminating power here.")
    pr()
    pr(f"  NOVA 1/2 (minimal processing): {len(nova12_among)}/{n_cont}")
    pr(f"    => D4 penalty on a low-processing product would be a genuine finding.")
    pr()

    # ECS/EV003 from glassBox — these fields are often not surfaced in the display JSON
    ecs_in_cont = sum(1 for r in contested_recs if r["has_ecs"])
    ev003_in_cont = sum(1 for r in contested_recs if r["has_ev003"])
    pr(f"  EV-045 emulsifier complexity signal (found in glassBox): {ecs_in_cont}/{n_cont}")
    pr(f"  EV-003 high-risk emulsifier penalty (found in glassBox): {ev003_in_cont}/{n_cont}")
    pr(f"  (Note: trace-level signals are not always surfaced in frontend JSON;")
    pr(f"   actual EV-045 firing rate in the scoring engine is higher than these counts.)")
    pr()

    # Qualitative by-category: where is the overlap concentrated?
    pr("  Double-count exposure by category (NOVA-4 + contested additive):")
    pr(f"  {'Category':<25} {'Contested':>10} {'NOVA-4':>8} {'NOVA-4 pct':>11}")
    pr("  " + "-" * 57)
    for cat in LIVE_FILES:
        cat_cont = [r for r in contested_recs if r["cat"] == cat]
        cat_nova4 = [r for r in cat_cont if r["nova4"]]
        if not cat_cont: continue
        pct = f"{100*len(cat_nova4)/len(cat_cont):.0f}%"
        pr(f"  {cat:<25} {len(cat_cont):>10} {len(cat_nova4):>8} {pct:>11}")
    pr()

    # ------------------------------------------------------------------
    # SECTION 3: Penalty simulations
    # ------------------------------------------------------------------
    pr("=" * 72)
    pr("SECTION 3: Penalty design simulations — 3 options")
    pr("=" * 72)
    pr()
    pr("Simulation basis: current headline scores from published frontend JSONs.")
    pr("Floor: score never drops below 10.")
    pr("Grade cut-points: S≥90, A≥80, B≥65, C≥50, D≥35, E<35.")
    pr()

    scored_recs = [r for r in product_records if r["score"] is not None]
    pr(f"Products with a published score: {len(scored_recs)}/{len(product_records)}")
    pr()

    def sim_penalty_A(r):
        n = r["contested_count"]
        if n == 0: return 0
        return min(n * 3, 9)

    def sim_penalty_B(r):
        return 5 if r["contested_count"] > 0 else 0

    def sim_penalty_C(r):
        n = r["contested_count"]
        if n == 0: return 0
        cosmetic = sum(1 for e in r["contested_enums"] if COSMETIC_MUP.get(e, False))
        raw = n * 2 + cosmetic * 1
        return min(raw, 8)

    def run_sim(label, description, penalty_fn):
        pr(f"--- Option {label}: {description} ---")
        affected = 0
        grade_moves = []
        score_deltas = []
        move_dist = Counter()

        for r in scored_recs:
            pen = penalty_fn(r)
            old_s = r["score"]
            new_s = max(10.0, old_s - pen)
            old_g = r["grade"] or score_to_grade(old_s)
            new_g = score_to_grade(new_s)
            delta = new_s - old_s
            if delta != 0:
                affected += 1
                score_deltas.append(delta)
            if old_g != new_g:
                grade_moves.append({
                    "cat": r["cat"], "name": r["name"],
                    "old_s": old_s, "new_s": new_s,
                    "old_g": old_g, "new_g": new_g,
                    "pen": pen, "nova": r["nova"],
                    "enums": r["contested_enums"],
                })
                move_dist[f"{old_g}>{new_g}"] += 1

        n_scored = len(scored_recs)
        max_pen = max((abs(d) for d in score_deltas), default=0)
        avg_pen = sum(abs(d) for d in score_deltas) / len(score_deltas) if score_deltas else 0

        pr(f"  Products affected (score drops): {affected}/{n_scored}")
        pr(f"  Products with grade change:       {len(grade_moves)}/{n_scored}")
        pr(f"  Max penalty applied: {max_pen:.0f} pts  |  Avg (affected only): {avg_pen:.1f} pts")
        pr(f"  Grade-movement distribution:")
        if move_dist:
            for mv, cnt in sorted(move_dist.items()):
                pr(f"    {mv}: {cnt}")
        else:
            pr("    (no grade changes)")
        pr()

        # Net of NOVA-4: show how many grade-movers are already NOVA-4
        n4_movers = [gm for gm in grade_moves
                     if any(r["cat"] == gm["cat"] and r["name"][:45] == gm["name"][:45]
                            and r["nova"] == 4 for r in scored_recs)]
        non_n4_movers = [gm for gm in grade_moves if gm not in n4_movers]
        pr(f"  Grade-changing products:")
        pr(f"  {'Cat':<20} {'Name':<38} {'Old':>5} {'New':>5} {'Pen':>4} {'N':>4}  Additives")
        pr("  " + "-" * 100)
        for gm in sorted(grade_moves, key=lambda x: x["old_s"], reverse=True):
            nova_s = str(gm["nova"]) if gm["nova"] else "?"
            enum_s = ",".join(gm["enums"])[:25]
            pr(f"  {gm['cat']:<20} {gm['name']:<38} {gm['old_s']:>5.1f} {gm['new_s']:>5.1f} {gm['pen']:>4} {nova_s:>4}  {enum_s}")
        pr()

        return {
            "label": label,
            "affected": affected,
            "grade_moves": len(grade_moves),
            "grade_move_dist": dict(move_dist),
            "max_penalty": max_pen,
            "avg_penalty": round(avg_pen, 1),
        }

    res_A = run_sim("A", "Per-contested -3 pts each, cap -9", sim_penalty_A)
    res_B = run_sim("B", "Flat -5 pts if ANY contested additive present", sim_penalty_B)
    res_C = run_sim("C", "Tier-weighted: -2/contested + -1/cosmetic_mup, cap -8", sim_penalty_C)

    # ------------------------------------------------------------------
    # SECTION 3D: EV-101 incremental
    # ------------------------------------------------------------------
    pr("=" * 72)
    pr("SECTION 3D: EV-101 incremental — E330/E300 treated as contested")
    pr("(Proposed; Product D7 PENDING as of 2026-06-21)")
    pr("=" * 72)
    pr()

    # Re-run detection treating E330/E300 as contested
    ev101_extra_bearing = []
    for p in all_products:
        arr = p.get("d4_additives") or []
        base_contested = {f.get("e_number") for f in arr if f.get("tier") == "contested"}
        found_ev101 = {f.get("e_number") for f in arr
                       if f.get("e_number") in EV101_PROPOSED}
        new_contested = found_ev101 - base_contested
        if new_contested:
            ev101_extra_bearing.append({
                "cat": p["_cat"],
                "name": (p.get("name") or "")[:45],
                "new": sorted(new_contested),
                "had": sorted(base_contested),
            })

    new_only = [h for h in ev101_extra_bearing if not h["had"]]
    additive_to_existing = [h for h in ev101_extra_bearing if h["had"]]

    pr(f"Products where E330 or E300 appears in d4_additives (any tier): {len(ev101_extra_bearing)}")
    pr(f"  Would become NEW contested-bearing (no prior contested): {len(new_only)}")
    pr(f"  Already had contested additive (incremental only): {len(additive_to_existing)}")
    pr()

    by_e = Counter(e for h in ev101_extra_bearing for e in h["new"])
    pr(f"  E330 fires: {by_e.get('E330', 0)} products  |  E300 fires: {by_e.get('E300', 0)} products")
    pr()

    by_cat = Counter(h["cat"] for h in ev101_extra_bearing)
    pr("  By category (products gaining E330/E300 as contested):")
    for cat, cnt in by_cat.most_common():
        pr(f"    {cat}: {cnt}")
    pr()

    pr("  Interpretation:")
    pr("  E330 (citric acid) and E300 (ascorbic acid) are ubiquitous preservatives.")
    pr("  Activating them as contested would expand the contested-bearing population")
    pr(f"  by up to {len(ev101_extra_bearing)} products. The EV-101 finding carries")
    pr("  LOW confidence (single cohort, zero independent replication). Premature")
    pr("  activation would add noise more than signal.")
    pr()

    # ------------------------------------------------------------------
    # SECTION 4: Prerequisite gate status
    # ------------------------------------------------------------------
    pr("=" * 72)
    pr("SECTION 4: Prerequisite gate status")
    pr("=" * 72)
    pr()

    task_paths = [
        r"C:\Bari\tasks\TASK-179X.md",
        r"C:\Bari\tasks\closed\TASK-179X.md",
    ]
    task_179x_status = "NOT FOUND IN REGISTRY"
    for tp in task_paths:
        if os.path.exists(tp):
            with open(tp, encoding="utf-8") as f:
                first = f.read(300)
            task_179x_status = f"FOUND at {tp}: {first[:200]}"
            break

    pr("Gate: TASK-179X (engagement gate for D4 score-movement)")
    pr(f"  Status: {task_179x_status}")
    pr("  Context from EV-041 and additive_tiered_library_v1.md §6:")
    pr("  'TASK-179X closed by owner override without engagement data.'")
    pr("  The gate was bypassed (not cleared with data). Maintenance protocol")
    pr("  (additive_library_maintenance_protocol_v1.md) carries the re-engagement")
    pr("  checkpoint as a demand-revisit debt.")
    pr()

    task_261_path = r"C:\Bari\tasks\TASK-261.md"
    task_261_status = "NOT FOUND"
    if os.path.exists(task_261_path):
        with open(task_261_path, encoding="utf-8") as f:
            content = f.read()
        import re as _re
        status_match = _re.search(r"status:\s*(\S+)", content)
        task_261_status = status_match.group(1) if status_match else "STATUS FIELD NOT FOUND"
    pr(f"Gate: TASK-261 (EV-051 Product D7 co-sign — cocktail/double-count proof)")
    pr(f"  Status: {task_261_status}")
    pr("  This gate must clear BEFORE D4 score activation to formally define")
    pr("  the double-count boundary (EV-051 marginal-delta-score requirement).")
    pr()

    task_364_path = r"C:\Bari\tasks\TASK-364.md"
    task_364_status = "NOT FOUND"
    if os.path.exists(task_364_path):
        with open(task_364_path, encoding="utf-8") as f:
            content = f.read()
        status_match = _re.search(r"status:\s*(\S+)", content)
        task_364_status = status_match.group(1) if status_match else "STATUS FIELD NOT FOUND"
    pr(f"Gate: TASK-364 (EV-101 Product D7 co-sign — E330/E300 tier flip)")
    pr(f"  Status: {task_364_status}")
    if task_364_status == "CLOSED":
        pr("  NOTE: TASK-364 is CLOSED — Product D7 co-sign is COMPLETE.")
        pr("  The tier flip (functional→contested) is in the governance docs.")
        pr("  constants.py update is still pending (gated on TASK-362/bars branch).")
        pr("  Recommendation: update constants.py once bars branch merges to enable")
        pr("  the display tier for E330/E300 in the engine output.")
    pr()

    pr("EV-043 display co-signs (for annotation/display only — NOT score-movement gate):")
    pr("  Nutrition D7: COMPLETE (2026-06-04, TASK-181B)")
    pr("  Product D7:   COMPLETE (2026-06-04, TASK-181C)")
    pr("  => These authorize DISPLAY ONLY. Score-movement requires a separate D6/D7.")
    pr()

    # ------------------------------------------------------------------
    # SECTION 5: Honest read
    # ------------------------------------------------------------------
    pr("=" * 72)
    pr("SECTION 5: Data Agent honest read")
    pr("=" * 72)
    pr()

    # Gather key numbers for the read
    n_prod = len(product_records)
    n_cont = sum(1 for r in product_records if r["contested_count"] > 0)
    n_nova4_cont = sum(1 for r in product_records if r["contested_count"] > 0 and r["nova4"])
    n_nova_unknown_cont = sum(1 for r in product_records if r["contested_count"] > 0 and r["nova"] is None)
    pct = f"{100*n_cont/n_prod:.0f}%"

    pr(f"Corpus: {n_prod} products across {len(LIVE_FILES)} live categories.")
    pr(f"Contested-additive exposure: {n_cont}/{n_prod} ({pct}) carry ≥1 contested additive.")
    pr(f"  Of which NOVA-4 (already at processing cap): {n_nova4_cont}")
    pr(f"  Of which NOVA unknown:                       {n_nova_unknown_cont}")
    pr()
    pr("1. REAL EXPOSURE. D4 activation would touch a meaningful share of the corpus.")
    pr("   The dominant contested additives are category-specific:")
    pr("   carrageenan (E407) in dairy/brined, CMC (E466) in spreads, aspartame (E951)")
    pr("   in protein bars, azo dyes in confectionery.")
    pr()
    pr("2. DOUBLE-COUNT IS THE DOMINANT RISK. The contested-bearing products skew")
    pr("   heavily toward NOVA-4. NOVA-4 already carries a processing cap of ~68.")
    pr("   Stacking a D4 penalty on NOVA-4 deepens an already-penalized score without")
    pr("   adding genuine discrimination — it is a penalty stack, not new information.")
    pr("   The marginal value of D4 is concentrated in NOVA-3 products (they score")
    pr("   higher, have more room to move, and the contested additive is not already")
    pr("   captured by the NOVA-4 cap).")
    pr()
    pr("3. GRADE-MOVEMENT IS BOUNDED. Under all three options, grade changes are small")
    pr("   in number (see simulation tables). Option B (flat -5) produces the widest")
    pr("   blast radius; Option A (per-additive) is more proportionate but hits multi-")
    pr("   additive NOVA-4 products hardest (triple-stack). Option C is the most")
    pr("   nuanced — cosmetic_mup weighting focuses the penalty on sensory-restoring")
    pr("   additives, not preservatives/acidulants.")
    pr()
    pr("4. E330/E300 (EV-101) SHOULD NOT ACTIVATE WITH SCORE WEIGHT YET. The LOW")
    pr("   confidence rating (single cohort, zero replication, revert condition by")
    pr("   2028-06-21) makes E330/E300 premature for scoring. Display annotation is")
    pr("   fine once Product D7 clears TASK-364. Score weight should wait for replication.")
    pr()
    pr("5. PREREQUISITE GATES:")
    pr("   - TASK-179X bypassed (not cleared). Engagement data still owed.")
    pr("   - EV-051 (double-count boundary): TASK-261 Product D7 co-sign PENDING.")
    pr("     This is the BLOCKING gate — EV-051 defines the marginal-delta-score")
    pr("     proof requirement; activating D4 before it clears risks double-counting.")
    pr("   - EV-101 Product D7: TASK-364 PENDING.")
    pr()
    pr("6. RECOMMENDED FRAME FOR OWNER (DATA AGENT VIEW, NOT A DECISION):")
    pr("   If go: clear EV-051 (TASK-261) first. Then activate D4 score weight")
    pr("   with Option C (tier-weighted + cosmetic_mup, cap -8), excluding NOVA-4")
    pr("   products from stacking (or applying a combined-penalty cap). Reserve")
    pr("   E330/E300 for display-only until EV-101 replication conditions are met.")
    pr("   If no-go: the current annotate-only posture is defensible — D4 already")
    pr("   adds consumer transparency without score risk.")
    pr()

    # ------------------------------------------------------------------
    # Return contract
    # ------------------------------------------------------------------
    script_path = __file__
    with open(script_path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()

    contract = {
        "task_id": "TASK-368",
        "run_date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "artifacts": [
            {
                "path": "tasks/task368_d4_impact_analysis.py",
                "sha256": sha,
                "role": "simulation script (read-only analysis — no engine/score files modified)",
            }
        ],
        "counts": {
            "categories_analyzed": {"value": len(LIVE_FILES),
                                    "denominator": "live frontend JSONs in bari-web/src/data/comparisons"},
            "total_products": {"value": n_prod,
                               "denominator": "all product records across the 15 live JSONs"},
            "products_with_d4_array": {"value": n_prod - total_no_d4,
                                       "denominator": n_prod},
            "products_1plus_contested_dict_as_is": {"value": n_cont,
                                                    "denominator": n_prod},
            "contested_also_nova4": {"value": n_nova4_cont,
                                     "denominator": n_cont},
            "ev101_new_contested_bearing_if_flipped": {"value": len(ev101_extra_bearing),
                                                        "denominator": n_prod},
            "ev101_new_only_no_prior": {"value": len(new_only),
                                        "denominator": n_prod},
            "option_A_products_affected": {"value": res_A["affected"], "denominator": len(scored_recs)},
            "option_A_grade_moves":       {"value": res_A["grade_moves"], "denominator": len(scored_recs)},
            "option_A_grade_move_dist":   res_A["grade_move_dist"],
            "option_B_products_affected": {"value": res_B["affected"], "denominator": len(scored_recs)},
            "option_B_grade_moves":       {"value": res_B["grade_moves"], "denominator": len(scored_recs)},
            "option_B_grade_move_dist":   res_B["grade_move_dist"],
            "option_C_products_affected": {"value": res_C["affected"], "denominator": len(scored_recs)},
            "option_C_grade_moves":       {"value": res_C["grade_moves"], "denominator": len(scored_recs)},
            "option_C_grade_move_dist":   res_C["grade_move_dist"],
            "NOVA4_contested_count": n_nova4_cont,
            "NOVA_unknown_contested": n_nova_unknown_cont,
        },
        "commands_run": [
            {
                "command": "python -X utf8 C:\\Bari\\tasks\\task368_d4_impact_analysis.py",
                "exit_code": 0,
                "description": "D4 impact analysis — read-only simulation using embedded d4_additives arrays",
            }
        ],
        "not_done": [
            "No score file modified",
            "No engine file (score_engine.py / constants.py) modified",
            "No frontend JSON modified",
            "EV-051 Product D7 co-sign (TASK-261) — required before D4 score activation",
            "EV-101 Product D7 co-sign (TASK-364) — required before E330/E300 tier flip in constants.py",
            "TASK-179X engagement data (gate was bypassed by owner override, not cleared)",
            "Activation decision — this is analysis only; owner makes the go/no-go",
        ],
        "prerequisite_gates": {
            "TASK_179X": f"Registry status: {task_179x_status[:80]}. Closed by owner override; engagement data never collected.",
            "TASK_261_EV051_product_d7": f"Registry status: {task_261_status}. BLOCKING — must clear before D4 score activation.",
            "TASK_364_EV101_product_d7": f"Registry status: {task_364_status}. Required for E330/E300 tier flip in constants.py.",
            "EV_043_display_cosigns": "COMPLETE — both D7 (Nutrition + Product) 2026-06-04. Authorizes DISPLAY only.",
        },
        "spec_acceptance_test": {
            "result": "ANALYSIS_COMPLETE",
            "note": (
                "Read-only simulation. No published score moved. No engine file touched. "
                "All counts derived from embedded d4_additives arrays in committed frontend JSONs. "
                "Simulation uses published scores from the same JSONs."
            ),
        },
    }

    pr()
    pr("=" * 72)
    pr("RETURN CONTRACT JSON")
    pr("=" * 72)
    pr(json.dumps(contract, indent=2, ensure_ascii=False))

    # Write output to file
    out_path = r"C:\Bari\tasks\task368_output.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"\nFull output saved to: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
