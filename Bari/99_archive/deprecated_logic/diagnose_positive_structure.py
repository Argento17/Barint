"""
Diagnostic: Why does positive structure have weak upward expressiveness?
Investigates 5 specific mechanisms across all 53 traces.
"""
import json, pathlib, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

TRACE_ROOT = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\outputs\products")
WEIGHTS = {
    "processing_quality":   0.15,
    "nutrient_density":     0.15,
    "calorie_density":      0.15,
    "glycemic_quality":     0.12,
    "protein_quality":      0.10,
    "additive_quality":     0.10,
    "satiety_support":      0.06,
    "fat_quality":          0.08,
    "regulatory_quality":   0.05,
    "whole_food_integrity": 0.04,
}

traces = []
for p in sorted(TRACE_ROOT.glob("*/bsip2_trace.json")):
    with open(p, encoding="utf-8") as f:
        traces.append(json.load(f))

sufficient = [t for t in traces if t.get("data_sufficiency") == "sufficient"]
print(f"Total traces: {len(traces)}, sufficient-data: {len(sufficient)}")
print()

# ── 1. Weight audit: what fraction of the ceiling can positive dims actually contribute? ──
print("=" * 70)
print("1. WEIGHT CEILINGS — Maximum weighted contribution per dimension")
print("   (Score=100 × weight = contribution if fully maximized)")
print("=" * 70)
for dim, w in sorted(WEIGHTS.items(), key=lambda x: -x[1]):
    print(f"  {dim:<25}  weight={w:.2f}  max_contribution={w*100:.1f} pts")

positive_structural = ["satiety_support", "whole_food_integrity"]
positive_structure_ceiling = sum(WEIGHTS[d] for d in positive_structural) * 100
print(f"\n  satiety_support + whole_food_integrity ceiling = {positive_structure_ceiling:.1f} pts "
      f"(combined weight = {sum(WEIGHTS[d] for d in positive_structural):.2f})")
print()

# ── 2. Actual dimension scores observed across sufficient products ──
print("=" * 70)
print("2. ACTUAL DIMENSION SCORE RANGES ACROSS 48 SUFFICIENT PRODUCTS")
print("=" * 70)
dims = list(WEIGHTS.keys())
for dim in sorted(dims, key=lambda d: -WEIGHTS[d]):
    vals = [t["dimension_scores"].get(dim, 0) for t in sufficient if t.get("dimension_scores")]
    if not vals:
        continue
    mn, mx, avg = min(vals), max(vals), sum(vals)/len(vals)
    w = WEIGHTS[dim]
    contrib_avg = avg * w
    contrib_max = mx * w
    print(f"  {dim:<25}  w={w:.2f}  min={mn:5.1f}  avg={avg:5.1f}  max={mx:5.1f}  "
          f"avg_contrib={contrib_avg:.2f}  max_contrib={contrib_max:.2f}")
print()

# ── 3. Cap bite analysis: how many pts does cap shave vs what positive dims add? ──
print("=" * 70)
print("3. CAP BITE vs POSITIVE DIMENSION HEADROOM")
print("   For each product: weighted_dim_score vs score_after_cap vs final")
print("=" * 70)
cap_bites = []
for t in sufficient:
    ds = t.get("dimension_scores", {})
    wds = t.get("weighted_dimension_score")
    sac = t.get("score_after_cap")
    final = t.get("final_score_estimate")
    binding = t.get("binding_cap")
    if wds is None or sac is None:
        continue
    bite = round(wds - sac, 2)
    penalty = round(sac - (t.get("score_after_penalty") or sac), 2)
    name = (t.get("input_reference") or {}).get("product_name_he", "?")[:40]
    cap_bites.append((bite, penalty, wds, sac, final, binding,
                      ds.get("satiety_support",0), ds.get("whole_food_integrity",0), name))

cap_bites.sort(key=lambda x: -x[0])
print(f"  {'Product':<42} WDS    Cap  Bite  Pen  Final  Saty  WFI")
for b, pen, wds, sac, fin, cap, ss, wfi, name in cap_bites[:20]:
    print(f"  {name:<42} {wds:5.1f}  {str(cap) if cap else '---':>4}  {b:4.1f}  {pen:4.1f}  {fin:5.1f}  "
          f"{ss:4.1f}  {wfi:4.1f}")
print(f"\n  Average cap bite across all sufficient products: "
      f"{sum(x[0] for x in cap_bites)/len(cap_bites):.1f} pts")
print(f"  Products where cap bites > 0: {sum(1 for x in cap_bites if x[0] > 0)}/{len(cap_bites)}")
print(f"  Products where cap bites > 10: {sum(1 for x in cap_bites if x[0] > 10)}/{len(cap_bites)}")
print()

# ── 4. Satiety support vs score: does it correlate? ──
print("=" * 70)
print("4. SATIETY_SUPPORT SCORE DIAGNOSTIC")
print("   Weight = 0.06. Max weighted contribution = 6 pts.")
print("=" * 70)
ss_vals = [(t["dimension_scores"].get("satiety_support",0),
            t.get("final_score_estimate"),
            (t.get("input_reference") or {}).get("product_name_he","?")[:40])
           for t in sufficient if t.get("dimension_scores")]
ss_vals.sort(key=lambda x: -x[0])
print(f"  {'Satiety Score':<14} {'Final Score':<13} Product")
for ss, fin, name in ss_vals[:12]:
    print(f"  {ss:<14.1f} {fin:<13} {name}")
print(f"\n  Best satiety_support = {ss_vals[0][0]:.1f} (weighted = {ss_vals[0][0]*0.06:.2f} pts contribution)")
print(f"  Average satiety_support = {sum(x[0] for x in ss_vals)/len(ss_vals):.1f}")
print()

# ── 5. Whole food integrity diagnostic ──
print("=" * 70)
print("5. WHOLE_FOOD_INTEGRITY SCORE DIAGNOSTIC")
print("   Weight = 0.04. Max weighted contribution = 4 pts.")
print("=" * 70)
wfi_vals = [(t["dimension_scores"].get("whole_food_integrity",0),
             t.get("nova_proxy"),
             t.get("final_score_estimate"),
             (t.get("input_reference") or {}).get("product_name_he","?")[:40])
            for t in sufficient if t.get("dimension_scores")]
wfi_vals.sort(key=lambda x: -x[0])
print(f"  {'WFI Score':<10} {'NOVA':<6} {'Final':<8} Product")
for wfi, nova, fin, name in wfi_vals[:10]:
    print(f"  {wfi:<10.1f} {nova:<6} {fin:<8} {name}")
print(f"\n  Best WFI score = {wfi_vals[0][0]:.1f} (weighted = {wfi_vals[0][0]*0.04:.2f} pts contribution)")
print()

# ── 6. Weighted dimension score vs final score: compression analysis ──
print("=" * 70)
print("6. COMPRESSION ANALYSIS: WDS → Final")
print("   Shows how much the pipeline compresses scores downward")
print("=" * 70)
for t in sorted(sufficient, key=lambda x: -(x.get("final_score_estimate") or 0)):
    wds = t.get("weighted_dimension_score", 0)
    final = t.get("final_score_estimate", 0)
    cap = t.get("binding_cap")
    pen = t.get("total_penalty_after_scaling", 0)
    grade = t.get("grade_estimate","?")
    name = (t.get("input_reference") or {}).get("product_name_he","?")[:38]
    compression = round(wds - final, 1)
    print(f"  {name:<40} WDS={wds:5.1f}  cap={str(cap) if cap else '---':>4}  "
          f"pen={pen:4.1f}  final={final:5.1f} ({grade})  compression={compression:+.1f}")
print()

# ── 7. Ingredient fragmentation — additive_quality ceiling ──
print("=" * 70)
print("7. ADDITIVE_QUALITY and NUTRIENT_DENSITY — actual score distribution")
print("   These two together = 0.25 weight (25 pts max)")
print("=" * 70)
aq_nd = [(t["dimension_scores"].get("additive_quality",0),
          t["dimension_scores"].get("nutrient_density",0),
          t["dimension_scores"].get("protein_quality",0),
          t.get("final_score_estimate"),
          t.get("category","?"))
         for t in sufficient if t.get("dimension_scores")]
aq_nd.sort(key=lambda x: -(x[0]+x[1]))
print(f"  {'AQ':>6}  {'ND':>6}  {'PQ':>6}  {'AQ+ND+PQ wt contrib':>20}  {'Final':>6}  Cat")
for aq, nd, pq, fin, cat in aq_nd[:15]:
    contrib = aq*0.10 + nd*0.15 + pq*0.10
    print(f"  {aq:6.1f}  {nd:6.1f}  {pq:6.1f}  {contrib:20.2f}  {fin:6.1f}  {cat}")
print()

# ── 8. The structural signal problem — what would happen if we raised weights ──
print("=" * 70)
print("8. COUNTERFACTUAL: if satiety_support weight → 0.10 and WFI → 0.07")
print("   (moved from penalty budget, not inflating total)")
print("   Only showing top 10 by score to test upper-middle expressiveness")
print("=" * 70)
ALT_WEIGHTS = {**WEIGHTS, "satiety_support": 0.10, "whole_food_integrity": 0.07,
               "glycemic_quality": 0.10, "additive_quality": 0.08}
# Glycemic and additive reduced to compensate; total must still = 1.0
total_alt = sum(ALT_WEIGHTS.values())
print(f"  Alt weight total = {total_alt:.2f} (must be 1.00)")
for t in sorted(sufficient, key=lambda x: -(x.get("final_score_estimate") or 0))[:10]:
    ds = t.get("dimension_scores", {})
    wds_orig = t.get("weighted_dimension_score", 0)
    wds_alt = sum(ds.get(k,0) * ALT_WEIGHTS.get(k, WEIGHTS[k]) for k in WEIGHTS)
    cap = t.get("binding_cap")
    final_orig = t.get("final_score_estimate", 0)
    sac_alt = min(wds_alt, cap) if cap else wds_alt
    pen = t.get("total_penalty_after_scaling", 0)
    final_alt = round(max(10, sac_alt - pen), 1)
    name = (t.get("input_reference") or {}).get("product_name_he","?")[:38]
    print(f"  {name:<40} orig_WDS={wds_orig:5.1f} alt_WDS={wds_alt:5.1f}  "
          f"final_orig={final_orig:5.1f} final_alt={final_alt:5.1f}  delta={final_alt-final_orig:+.1f}")
print()

# ── 9. Check: does same counterfactual inflate bottom products? ──
print("=" * 70)
print("9. COUNTERFACTUAL bottom-10: does alt weight lift highly engineered products?")
print("=" * 70)
for t in sorted(sufficient, key=lambda x: x.get("final_score_estimate") or 999)[:10]:
    ds = t.get("dimension_scores", {})
    wds_orig = t.get("weighted_dimension_score", 0)
    wds_alt = sum(ds.get(k,0) * ALT_WEIGHTS.get(k, WEIGHTS[k]) for k in WEIGHTS)
    cap = t.get("binding_cap")
    final_orig = t.get("final_score_estimate", 0)
    sac_alt = min(wds_alt, cap) if cap else wds_alt
    pen = t.get("total_penalty_after_scaling", 0)
    final_alt = round(max(10, sac_alt - pen), 1)
    name = (t.get("input_reference") or {}).get("product_name_he","?")[:38]
    nova = t.get("nova_proxy","?")
    print(f"  {name:<40} NOVA={nova}  "
          f"final_orig={final_orig:5.1f} final_alt={final_alt:5.1f}  delta={final_alt-final_orig:+.1f}")
