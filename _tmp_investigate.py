import os, sys, importlib, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, "C:/Bari/03_operations/bsip2/proto_v0/src")
sys.path.insert(0, "C:/Bari/03_operations/page_generator")

# Load the rescore results
data = json.loads(Path("C:/Bari/_tmp_canonical_rescore.json").read_text(encoding="utf-8"))

# CEREALS: 12 movers with D4+SODIUM_CEREAL
# All DOWN -- check if they have additional flags active on the original run
cereals_movers = [x for x in data["results"]["cereals"] if not x["match"] and x.get("new_score") is not None]
print("CEREALS movers:")
for m in sorted(cereals_movers, key=lambda x: -(x.get("diff") or 0)):
    print(f"  {m['barcode']}: live={m['live_score']}/{m['live_grade']} new={m['new_score']}/{m['new_grade']} delta={m['delta']}")

# Check if the cereals live frontend has a _meta.scoring_flags or engine info
live = json.loads(Path("C:/Bari/bari-web/src/data/comparisons/cereals_frontend_v2.json").read_text(encoding="utf-8"))
meta = live.get("_meta", {})
print("\nCereals _meta keys:", list(meta.keys()))
sf = meta.get("scoring_flags", {})
print("scoring_flags:", sf)
print("engine_version:", meta.get("engine_version"))
print("run_id:", meta.get("run_id"))

# CHEESE: 9 movers all at 2.2 -- check what changed
cheese_movers = [x for x in data["results"]["cheese"] if not x["match"] and x.get("new_score") is not None]
print("\nCHEESE movers (all at 2.2):")
for m in cheese_movers[:5]:
    print(f"  {m['barcode']}: live={m['live_score']}/{m['live_grade']} new={m['new_score']}/{m['new_grade']} delta={m['delta']}")

live_cheese = json.loads(Path("C:/Bari/bari-web/src/data/comparisons/cheese_frontend_v4.json").read_text(encoding="utf-8"))
meta_ch = live_cheese.get("_meta", {})
print("Cheese _meta scoring_flags:", meta_ch.get("scoring_flags"))
