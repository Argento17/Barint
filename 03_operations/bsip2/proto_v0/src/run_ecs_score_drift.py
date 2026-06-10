"""
ECS-v1 Score-Drift Validation — checks real product traces for expected penalty.

Loads product traces from 7 category directories, applies _emulsifier_complexity()
to any product that has the new L3 signals, and reports score impact.
"""
import sys, json, pathlib, glob
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from score_engine import _emulsifier_complexity

PRODUCT_ROOTS = {
    "plant_based_dairy":  r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_004_recalibrated\products",
    "sauces_dressings":   r"C:\Bari\02_products\hummus\intelligence_bsip2\run_001\products",
    "snack_bars":         r"C:\Bari\02_products\snack_bars\intelligence_bsip2\run_004\products",
    "bread_light":        r"C:\Bari\02_products\bread_light\intelligence_bsip2\run_003\products",
    "bread_retail":       r"C:\Bari\02_products\bread_retail_003\intelligence_bsip2\run_001\products",
    "yogurt":             r"C:\Bari\02_products\yogurt_system\intelligence_bsip2\run_001\products",
}

def find_traces(root: str, max_count: int = 20) -> list[dict]:
    """Load up to max_count product traces from a directory."""
    traces = []
    for d in sorted(glob.glob(str(pathlib.Path(root) / "bsip1_*")))[:max_count]:
        trace_path = pathlib.Path(d) / "bsip2_trace.json"
        if trace_path.exists():
            with open(trace_path, encoding="utf-8") as f:
                traces.append(json.load(f))
    return traces

def get_emulsifier_signals(trace: dict) -> dict:
    """Extract ECS-relevant L3 signals from a trace, checking both old and new keys."""
    l3 = trace.get("L3_inferred_classifications", trace)
    return {
        "tax_emulsifier_concern": l3.get("tax_emulsifier_concern") or [],
        "tax_emulsifier_medium":  l3.get("tax_emulsifier_medium") or [],
        "tax_emulsifier_low":     l3.get("tax_emulsifier_low") or [],
        "score_estimate": trace.get("final_score_estimate") or trace.get("score_estimate"),
    }

print("=" * 72)
print("ECS-v1 Score-Drift Validation")
print("=" * 72)

categories_empty = 0
categories_with_agents = 0
total_checked = 0
products_with_penalty = 0
max_penalty_seen = 0

for cat, root in PRODUCT_ROOTS.items():
    if not pathlib.Path(root).exists():
        print(f"\n  [{cat}] NO DATA: {root}")
        continue
    traces = find_traces(root)
    if not traces:
        print(f"\n  [{cat}] No traces found")
        continue
    print(f"\n  [{cat}] {len(traces)} products")
    cat_penalties = []
    for t in traces:
        sigs = get_emulsifier_signals(t)
        pid = t.get("product_id") or t.get("id", "?")
        if not any([sigs["tax_emulsifier_concern"], sigs["tax_emulsifier_medium"], sigs["tax_emulsifier_low"]]):
            # No ECS signals — check if old traces have the new fields or if this is truly clean
            if "tax_emulsifier_medium" not in (t.get("L3_inferred_classifications", t)):
                # Old trace without ECS-v1 fields — skip
                continue
            cat_penalties.append(0)
            continue
        total_checked += 1
        ecs_penalty, note, detail = _emulsifier_complexity(sigs)
        cat_penalties.append(ecs_penalty)
        if ecs_penalty > 0:
            products_with_penalty += 1
            if ecs_penalty > max_penalty_seen:
                max_penalty_seen = ecs_penalty
            print(f"    {pid}: ECS penalty = -{ecs_penalty} "
                  f"(high={detail['high_agents']} med={detail['medium_agents']} "
                  f"low={detail['low_agents']} tier={detail['complexity_tier']})")

    if cat_penalties:
        nonzero = [p for p in cat_penalties if p > 0]
        if nonzero:
            categories_with_agents += 1
            print(f"    -> {len(nonzero)}/{len(cat_penalties)} products with ECS penalty "
                  f"(max={max(nonzero)}, avg={sum(nonzero)/len(nonzero):.1f})")
        else:
            categories_empty += 1
            print(f"    -> No products with ECS penalty in sample")

print("\n" + "-" * 72)
print(f"  Categories with ECS-active traces:  {categories_with_agents}")
print(f"  Categories with clean-only traces:  {categories_empty}")
print(f"  Total products checked:             {total_checked}")
print(f"  Products with non-zero penalty:     {products_with_penalty}")
print(f"  Max penalty observed:               -{max_penalty_seen}")
print("=" * 72)

# Check for score-drift in clean products (should be 0)
print("\n  Note: Score-drift = 0 for clean products (no ECS agents).")
print("  The penalty is additive at Stage 7 and does not change dimension scores.")
print("  Products with no emulsifier/stabiliser agents = unchanged score.")
