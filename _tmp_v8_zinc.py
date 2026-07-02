import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path("C:/Bari/03_operations/supplement_engine/proto_v0/src").resolve()))

with open(r"C:\Bari\02_products\supplements\real_corpus_v3\_corpus_run_full_v8.json", encoding="utf-8") as f:
    data = json.load(f)

results = data["results"]

# Check the v8 header edpg_note for stated grade delta
print("=== v8 edpg_note (stated deltas) ===")
print(data.get("edpg_note", "none"))
print()

# Check v8 header grade_distribution
print("=== v8 header grade_distribution ===")
print(data.get("grade_distribution", {}))
print()

zinc_barcodes = {
    "0033984037250": "Solgar Zinc Picolinate 22mg",
    "7290006437563": "Altman Zinc Picolinate 25mg",
    "7290018365359": "Tink Zinc 50mg (name_derived)",
}

print("=== Zinc Products - Full Engine Output ===")
for r in results:
    bc = r.get("barcode", "")
    if bc in zinc_barcodes:
        eo = r.get("engine_output", {})
        print(f"\n--- [{bc}] {zinc_barcodes[bc]} ---")
        print(f"  grade={eo.get('grade')} score={eo.get('score')}")
        print(f"  binding={eo.get('binding_constraint', {})}")
        print(f"  claim_matched={eo.get('claim_matched')}")
        print(f"  on_label_claim={eo.get('on_label_claim')}")
        print(f"  claim_resolution={json.dumps(eo.get('claim_resolution', {}), ensure_ascii=False, indent=4)}")
        print(f"  sub_scores={eo.get('sub_scores')}")
        print()

# Check 0033984037250 cache file for panel data
import os
cache_path = r"C:\Bari\03_operations\supplement_engine\proto_v0\cache"
for bc in zinc_barcodes:
    fn = os.path.join(cache_path, f"{bc}.json")
    if os.path.exists(fn):
        with open(fn, encoding="utf-8") as f2:
            cdata = json.load(f2)
        print(f"--- Cache {bc} ---")
        print(f"  url={cdata.get('url')}")
        print(f"  actives={json.dumps(cdata.get('actives', cdata.get('parsed_actives', [])), ensure_ascii=False)}")
        print(f"  claim={cdata.get('primary_claim', cdata.get('claim', ''))}")
        print()
    else:
        print(f"--- Cache {bc}: NOT FOUND ---")
