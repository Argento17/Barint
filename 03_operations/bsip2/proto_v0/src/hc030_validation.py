"""One-shot hc-030 validation: before/after BARI_REDLABEL_V1 full decomposition."""
import sys, json, os
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")

BSIP1 = "c:/Bari/02_products/hard_cheeses/bsip1_outputs/bsip1_hardcheese_8711528211138.json"
WEIGHTS = {
    "processing_quality": 0.15, "nutrient_density": 0.15, "calorie_density": 0.15,
    "glycemic_quality": 0.12, "protein_quality": 0.10, "additive_quality": 0.10,
    "satiety_support": 0.06, "fat_quality": 0.08, "regulatory_quality": 0.05,
    "whole_food_integrity": 0.04,
}


def run_once(flag_on):
    os.environ["BARI_REDLABEL_V1"] = "on" if flag_on else "off"
    for m in ["signal_extractor", "score_engine", "nova_proxy", "evaluation_scope",
              "router_v2", "input_loader", "constants", "structural_classifier"]:
        sys.modules.pop(m, None)
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product

    product = json.load(open(BSIP1, encoding="utf-8"))
    sig  = extract_signals(product)
    cat  = classify_category(product)
    nova = infer_nova(product, sig["L3_inferred_classifications"])
    ev   = assign_evaluation_scope(product, cat["category"])
    r    = score_product(product, sig, cat, nova, ev)
    return r, nova, sig


print("=== hc-030 LIVE VALIDATION ===")
print("Product: barcode 8711528211138 / גבינת גאודה עיזים")
print("Nutrition: fat=34g, sat_fat=null, sodium=800mg, energy=397kcal, protein=24g")
print("Ingredients (4): goat milk 97.7%, salt, rennet, lactic culture")
print()

for flag in [False, True]:
    r, nova, sig = run_once(flag)
    ds   = r.get("dimension_scores") or {}
    pens = r.get("penalties_applied") or []
    caps = r.get("caps_fired") or []
    dnotes = r.get("dimension_notes") or {}
    l3 = sig["L3_inferred_classifications"]

    wds = sum(ds.get(k, 0) * v for k, v in WEIGHTS.items())
    total_pen = sum(p["amount"] for p in pens)
    cap_val   = r.get("binding_cap")

    tag = "BARI_REDLABEL_V1=ON " if flag else "BARI_REDLABEL_V1=OFF"
    print(f"--- {tag} ---")
    print(f"NOVA: {nova['nova_level']}  conf={nova['nova_confidence']:.2f}")
    print(f"red_labels: {l3.get('red_labels')}  count={l3.get('red_label_count')}")
    print()
    print("Dimension scores:")
    for k, w in WEIGHTS.items():
        v = ds.get(k, 0)
        print(f"  {k:<26} {v:>6.1f} x {w:.2f} = {v*w:>5.2f}")
    print(f"  {'WEIGHTED DIM SCORE':<26} {'':>6}        = {wds:>5.2f}")
    print()
    print(f"  binding_cap:     {cap_val}")
    after_cap = min(wds, cap_val) if cap_val else wds
    print(f"  after cap:       {after_cap:.2f}")
    print("  penalties:")
    for p in pens:
        print(f"    -{p['amount']}  {p['rule']}: {p.get('note','')}")
    print(f"  total penalties: -{total_pen}")
    print(f"  after penalties: {after_cap - total_pen:.2f}")
    print()
    print(f"  FINAL SCORE:  {r.get('final_score_estimate')}   GRADE: {r.get('grade_estimate')}")
    rq_note = dnotes.get("regulatory_quality", "")
    print(f"  reg_quality note: {rq_note}")
    print()
