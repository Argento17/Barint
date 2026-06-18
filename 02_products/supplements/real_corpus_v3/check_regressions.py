"""Check grade regressions between v1 and v2 corpus runs."""
import json, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = pathlib.Path(r"C:\Bari\02_products\supplements\real_corpus_v3")
v1 = json.loads((HERE / "_corpus_run_full.json").read_text(encoding="utf-8"))
v2 = json.loads((HERE / "_corpus_run_full_v2.json").read_text(encoding="utf-8"))

v1_map = {}
for r in v1["results"]:
    if r.get("outcome") == "scored":
        v1_map[str(r["barcode"])] = r

tier_order = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "E": 0}

regressions = []
for r in v2["results"]:
    if r.get("outcome") == "scored":
        bc = str(r["barcode"])
        prev = v1_map.get(bc)
        if prev:
            prev_g = prev["engine_output"]["grade"]
            new_g = r["engine_output"]["grade"]
            if tier_order.get(prev_g, 0) > tier_order.get(new_g, 0):
                regressions.append({
                    "bc": bc,
                    "name": r["name_he"][:40],
                    "active": r["engine_active"],
                    "prev_grade": prev_g,
                    "new_grade": new_g,
                    "prev_claim_fed": prev.get("bsip0s_label", {}).get("primary_claim_fed", "?")[:60],
                    "prev_claim_note": prev.get("claim_note", "?")[:60],
                    "prev_matched": str(prev["engine_output"].get("claim_matched", "?"))[:60],
                    "new_claim_fed": r.get("bsip0s_label", {}).get("primary_claim_fed", "?")[:60],
                    "new_bind": str(r["engine_output"].get("binding_constraint", {}).get("mechanism", "?"))
                })

print(f"REGRESSIONS (grade went DOWN): {len(regressions)}")
for rr in regressions:
    print(f"  {rr['bc']} {rr['prev_grade']}->{rr['new_grade']} [{rr['active']}] {rr['name']}")
    print(f"    prev_claim_fed: {rr['prev_claim_fed']}")
    print(f"    prev_note:      {rr['prev_claim_note']}")
    print(f"    prev_matched:   {rr['prev_matched']}")
    print(f"    new_claim_fed:  {rr['new_claim_fed']}")
    print(f"    new_bind:       {rr['new_bind']}")
    print()
