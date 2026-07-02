import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Bari\02_products\supplements\real_corpus_v3\_corpus_run_full_v8.json", encoding="utf-8") as f:
    data = json.load(f)

results = data["results"]

# Full Tink Zinc 50mg record
for r in results:
    if r.get("barcode") == "7290018365359":
        print("=== FULL TINK ZINC 50mg RECORD ===")
        # Print all fields except engine_output (already seen)
        for k, v in r.items():
            if k != "engine_output":
                print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
        print()
        print("  engine_output:")
        eo = r.get("engine_output", {})
        print(json.dumps(eo, ensure_ascii=False, indent=4))
        break

# Full Solgar Zinc Picolinate record
for r in results:
    if r.get("barcode") == "0033984037250":
        print("\n=== FULL SOLGAR ZINC PICOLINATE 22mg RECORD ===")
        for k, v in r.items():
            if k != "engine_output":
                print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
        print()
        print("  engine_output:")
        eo = r.get("engine_output", {})
        print(json.dumps(eo, ensure_ascii=False, indent=4))
        break

# Full Amorphicure Mg Carbonate record
for r in results:
    if r.get("barcode") == "7290015429245":
        print("\n=== FULL AMORPHICURE MG CARBONATE 160mg RECORD ===")
        for k, v in r.items():
            if k != "engine_output":
                print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
        print()
        print("  engine_output:")
        eo = r.get("engine_output", {})
        print(json.dumps(eo, ensure_ascii=False, indent=4))
        break
