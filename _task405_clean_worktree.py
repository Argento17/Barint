# -*- coding: utf-8 -*-
"""Wrapper: run TASK-405 clean in worktree, remapping C:\Bari -> worktree root."""
import sys, json, glob, os, re, datetime
WT = r"C:\Bari\.claude\worktrees\task409"
sys.path.insert(0, os.path.join(WT, "03_operations", "bsip2", "proto_v0", "src"))
from signal_extractor import sanitize_ingredient_list

ROOT = os.path.join(WT, "03_operations", "bsip1")
REPORT_OUT = os.path.join(WT, "_task405_clean_report.json")
EXCLUDE = ("maadanim", "yogurt")
DRY = "--apply" not in sys.argv
PCT_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*%")
NOW = datetime.datetime.now().isoformat(timespec="seconds")

dirs = sorted(set(os.path.dirname(p) for p in glob.glob(os.path.join(ROOT, "*", "output", "bsip1_*.json"))))
dirs = [d for d in dirs if not any(x in d.lower() for x in EXCLUDE)]

cleaned, flagged, per_dir = [], [], {}
for d in dirs:
    rel = os.path.relpath(d, WT)
    nclean = 0
    for f in glob.glob(os.path.join(d, "bsip1_*.json")):
        try:
            j = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            flagged.append({"file": f, "reason": f"unreadable: {e}"}); continue
        lst = [str(x) for x in (j.get("ingredients_list") or [])]
        if not lst:
            continue
        san = sanitize_ingredient_list(lst)
        if san["clean_count"] == san["raw_count"]:
            continue
        clean = san["clean"]
        if not clean:
            flagged.append({"file": os.path.relpath(f, WT),
                            "reason": "clean_count==0", "raw": san["raw_count"]}); continue
        bc = os.path.basename(f).replace("bsip1_", "").replace(".json", "")
        new_text = ", ".join(clean)
        new_order = []
        for i, it in enumerate(clean, 1):
            m = PCT_RE.search(it)
            new_order.append({"position": i, "text": it,
                              "percentage_declared": float(m.group(1).replace(",", ".")) if m else None,
                              "has_subgroup": "(" in it})
        if not DRY:
            j["_task405_clean"] = {
                "ts": NOW, "task": "TASK-405 ingredient-pollution clean (de-chain F1)",
                "raw_count": san["raw_count"], "clean_count": san["clean_count"],
                "dropped": san["dropped"], "truncated": san["truncated"],
                "original_ingredients_text_he": j.get("ingredients_text_he"),
                "original_ingredients_list": j.get("ingredients_list"),
            }
            j["ingredients_list"] = clean
            j["ingredients_text_he"] = new_text
            j["ingredients_raw"] = new_text
            j["ingredient_order"] = new_order
            json.dump(j, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        nclean += 1
        cleaned.append({"file": rel + "/" + os.path.basename(f), "barcode": bc,
                        "raw": san["raw_count"], "clean": san["clean_count"]})
    if nclean:
        per_dir[rel] = nclean

out = {"mode": "DRY-RUN" if DRY else "APPLIED", "ts": NOW,
       "dirs_processed": len(dirs), "files_cleaned": len(cleaned),
       "files_flagged": len(flagged), "per_dir": per_dir,
       "flagged": flagged}
json.dump(out, open(REPORT_OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out["mode"], "| cleaned", len(cleaned), "| flagged", len(flagged), "| dirs", len(per_dir))
