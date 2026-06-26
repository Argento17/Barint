# -*- coding: utf-8 -*-
import sys, json, glob, os
WT = r"C:\Bari\.claude\worktrees\task409"
sys.path.insert(0, os.path.join(WT, "03_operations", "bsip2", "proto_v0", "src"))
from signal_extractor import sanitize_ingredient_list

ROOT = os.path.join(WT, "03_operations", "bsip1")
dirs = sorted(set(os.path.dirname(p) for p in glob.glob(os.path.join(ROOT, "*", "output", "bsip1_*.json"))))

distinct = {}
total_files = 0
for d in dirs:
    files = glob.glob(os.path.join(d, "bsip1_*.json"))
    for f in files:
        total_files += 1
        try:
            j = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        lst = j.get("ingredients_list") or []
        txt = (j.get("ingredients_text_he") or "").strip()
        bc = os.path.basename(f).replace("bsip1_", "").replace(".json", "")
        has_text = bool(txt) or bool(lst)
        san = sanitize_ingredient_list([str(x) for x in lst]) if lst else None
        polluted = bool(san and san["clean_count"] != san["raw_count"])
        rec = distinct.setdefault(bc, {"text": False, "polluted": False})
        if has_text: rec["text"] = True
        if polluted: rec["polluted"] = True

dt = sum(1 for v in distinct.values() if v["text"])
dp = sum(1 for v in distinct.values() if v["polluted"])
rate = round(100*dp/dt, 1) if dt else 0
out = {"total_files": total_files, "distinct_barcodes": len(distinct),
       "distinct_with_text": dt, "distinct_polluted": dp, "pollution_rate_pct": rate}
outf = os.path.join(WT, "_task405_detect_post.json")
json.dump(out, open(outf, "w", encoding="utf-8"), indent=1)
print(f"POST-CLEAN: files={total_files} distinct={len(distinct)} with_text={dt} polluted={dp} ({rate}%)")
