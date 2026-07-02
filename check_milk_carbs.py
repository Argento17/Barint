import json, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

target_milk = {
    "7290000051352", "7290019790259", "7290102392094", "7290114313865",
    "7290116936116", "7290110324926", "7290014760141", "5411188124689",
    "7290110325619", "5411188112709",
}

# Use the most recent run: run_006_shelfrel_refreeze
trace_dir = r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_006_shelfrel_refreeze\products"

print("=== Milk BSIP2 traces (run_006_shelfrel_refreeze) ===")
print("Looking for:", target_milk)
print()

found = {}
for product_dir in os.listdir(trace_dir):
    # product_dir is like bsip1_7290000051352
    bc = product_dir.replace("bsip1_","")
    if bc not in target_milk:
        continue
    trace_file = os.path.join(trace_dir, product_dir, "bsip2_trace.json")
    if not os.path.isfile(trace_file):
        print(f"  BC={bc}: trace file missing at {trace_file}")
        continue
    with open(trace_file, encoding="utf-8") as f:
        t = json.load(f)
    l1 = t.get("L1_observed_signals", {})
    carbs = l1.get("carbohydrates_g")
    sugar = l1.get("sugars_g")
    name = t.get("input_reference", {}).get("product_name_he", "?")
    fires = carbs >= 5.0 if carbs is not None else None
    status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN")
    print(f"  BC={bc:<22} carbs={str(carbs):<8} sugars={str(sugar):<8} status={status}  {str(name)[:50]}")
    found[bc] = (carbs, sugar, fires, name)

for bc in target_milk:
    if bc not in found:
        print(f"  BC={bc:<22} NOT_FOUND in run_006 traces")

print()
print("=== SUMMARY ===")
activated = [(bc, d) for bc, d in found.items() if d[2] is True]
safe = [(bc, d) for bc, d in found.items() if d[2] is False]
unknown = [(bc, d) for bc, d in found.items() if d[2] is None]
print(f"FIRES (carbs>=5.0): {len(activated)}")
for bc, d in activated:
    print(f"  BC={bc}  carbs={d[0]}  name={str(d[3])[:50]}")
print(f"SAFE (carbs<5.0): {len(safe)}")
for bc, d in safe:
    print(f"  BC={bc}  carbs={d[0]}  name={str(d[3])[:50]}")
print(f"UNKNOWN: {len(unknown)}")
for bc, d in unknown:
    print(f"  BC={bc}  name={str(d[3])[:50]}")
