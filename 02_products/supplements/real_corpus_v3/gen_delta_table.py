"""Generate before/after delta table for TASK-277 return contract."""
import json, pathlib, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = pathlib.Path(r"C:\Bari\02_products\supplements\real_corpus_v3")

v2 = json.loads((HERE / "_corpus_run_full_v2.json").read_text(encoding="utf-8"))
v1 = json.loads((HERE / "_corpus_run_full.json").read_text(encoding="utf-8"))

# Build lookup by barcode for v1
v1_map = {}
for r in v1["results"]:
    if r.get("outcome") == "scored":
        v1_map[str(r["barcode"])] = r["engine_output"]

print("barcode         | name_he (trunc)             | active        | score | grade | binding_constraint           | delta")
print("-" * 140)
scored = [r for r in v2["results"] if r.get("outcome") == "scored"]
for r in sorted(scored, key=lambda x: (x.get("engine_output", {}).get("score", 0) or 0), reverse=True):
    e = r["engine_output"]
    bc = str(r["barcode"])
    prev = v1_map.get(bc)
    delta = ""
    if prev:
        if prev["grade"] != e["grade"]:
            delta = f"{prev['grade']}->{e['grade']}"
        elif str(prev.get("binding_constraint")) != str(e.get("binding_constraint")):
            delta = "bind-changed"
    else:
        delta = "not-in-v1"
    name_trunc = r["name_he"][:28].ljust(28)
    bind_mech = e["binding_constraint"].get("mechanism", str(e["binding_constraint"]))[:29]
    print(f"{bc:<16}| {name_trunc}| {r['engine_active']:<13} | {e['score']:<5} | {e['grade']:<5} | {bind_mech:<29}| {delta}")

print()
print("UNSCOREABLE RESIDUE:")
for r in v2["results"]:
    if r.get("outcome") != "scored":
        prev_outcome = None
        for pr in v1["results"]:
            if str(pr["barcode"]) == str(r["barcode"]):
                prev_outcome = pr.get("outcome")
                break
        delta = ""
        if prev_outcome and prev_outcome != r["outcome"]:
            delta = f"was:{prev_outcome}"
        print(f"  {r['outcome']:<28} | {r['engine_active']:<13} | {r['name_he'][:35]}  {delta}")
