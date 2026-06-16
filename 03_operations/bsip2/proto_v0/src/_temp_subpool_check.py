import json, pathlib

# Check milk products for bsip_cheese_subpool
milk_dir = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output")
print("=== MILK ===")
for f in sorted(milk_dir.glob("*.json"))[:5]:
    d = json.loads(f.read_text(encoding="utf-8"))
    nn = d.get("normalized_nutrition_per_100g", {})
    print(f"  {f.name}: subpool={d.get('bsip_cheese_subpool')} fat={nn.get('fat_g')} sat_fat={nn.get('fat_saturated_g')}")

# Check HC products
hc_dir = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip1_outputs")
print("\n=== HC ===")
for f in sorted(hc_dir.glob("*.json"))[:5]:
    d = json.loads(f.read_text(encoding="utf-8"))
    nn = d.get("normalized_nutrition_per_100g", {})
    print(f"  {f.name}: subpool={d.get('bsip_cheese_subpool')} fat={nn.get('fat_g')} sat_fat={nn.get('fat_saturated_g')}")

# Check the two named HC products
for bc_name in ["bsip1_hardcheese_7290108502725.json", "bsip1_hardcheese_7290019635192.json"]:
    f = hc_dir / bc_name
    if f.exists():
        d = json.loads(f.read_text(encoding="utf-8"))
        nn = d.get("normalized_nutrition_per_100g", {})
        print(f"  TARGET {bc_name}: subpool={d.get('bsip_cheese_subpool')} fat={nn.get('fat_g')} sat_fat={nn.get('fat_saturated_g')}")
