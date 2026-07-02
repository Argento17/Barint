import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path("C:/Bari/03_operations/supplement_engine/proto_v0/src").resolve()))

with open(r"C:\Bari\02_products\supplements\real_corpus_v3\_corpus_run_full_v8.json", encoding="utf-8") as f:
    data = json.load(f)

results = data["results"]

target_barcodes = {
    "7290018365359": "Tink Zinc 50mg (name_derived)",
    "0033984037250": "Solgar Zinc Picolinate 22mg",
    "7290006437563": "Altman Zinc Picolinate 25mg",
    "7290015429245": "Amorphicure Mg Carbonate 160mg",
    "7290118814061": "SupHerb Iron 30mg bisglycinate",
    "783495578741": "liposomal iron 27mg",
    "7290012056741": "Tink Iron 36mg bisglycinate",
}

print("=== Key Product Full Engine Outputs ===")
found = set()
for r in results:
    bc = r.get("barcode", "")
    if bc in target_barcodes:
        found.add(bc)
        print(f"\n--- [{bc}] {target_barcodes[bc]} ---")
        print(f"  outcome: {r.get('outcome')}")
        print(f"  acquisition_method: {r.get('acquisition_method')}")
        eo = r.get("engine_output", {})
        print(f"  grade: {eo.get('grade')}  score: {eo.get('score')}")
        print(f"  binding_constraint: {json.dumps(eo.get('binding_constraint', {}))}")
        ss = eo.get("sub_scores", {})
        print(f"  sub_scores: {json.dumps(ss, ensure_ascii=False, indent=4)}")

missing = set(target_barcodes.keys()) - found
if missing:
    print(f"\nNOT FOUND in results (searching all outcomes): {missing}")
    for r in results:
        bc = r.get("barcode", "")
        if bc in missing:
            eo = r.get("engine_output", {})
            print(f"  {bc}: outcome={r.get('outcome')} grade={eo.get('grade')} score={eo.get('score')}")
