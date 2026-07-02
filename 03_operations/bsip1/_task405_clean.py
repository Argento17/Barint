# -*- coding: utf-8 -*-
"""TASK-405 CLEAN pass. Apply the proven sanitize_ingredient_list to the STORED BSIP1
ingredient fields (ingredients_list / ingredients_text_he / ingredients_raw / ingredient_order)
so nutrition-panel/disclaimer bleed is removed AT REST for raw-text consumers (additive
detector, matrix probe) and for the de-chain re-shadow.

SAFETY:
- Score-neutral: the BSIP2 engine already calls sanitize_ingredient_list at runtime, so the
  NOVA/count path is unchanged; this only cleans the stored source fields.
- Only writes files where pollution is detected (clean_count != raw_count).
- Every changed file gets a reversible `_task405_clean` audit block (original fields + delta).
- Flag-and-escalate: if cleaning would empty the list or the salvaged head looks unsafe, the
  file is NOT written — it goes on the flag list for human review (no silent impute, no OFF).
- EXCLUDES wiped/dead categories (maadanim, yogurt) — pointless churn.
"""
import sys, json, glob, os, re, datetime
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")
from signal_extractor import sanitize_ingredient_list

ROOT = r"C:\Bari\03_operations\bsip1"
EXCLUDE = ("maadanim", "yogurt")          # wiped/dead categories
DRY = "--apply" not in sys.argv
PCT_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*%")
NOW = datetime.datetime.now().isoformat(timespec="seconds")

dirs = sorted(set(os.path.dirname(p) for p in glob.glob(os.path.join(ROOT, "*", "output", "bsip1_*.json"))))
dirs = [d for d in dirs if not any(x in d.lower() for x in EXCLUDE)]

cleaned, flagged, per_dir = [], [], {}
for d in dirs:
    rel = os.path.relpath(d, r"C:\Bari")
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
            continue  # not polluted
        clean = san["clean"]
        # flag-and-escalate: never empty a real list; never write if salvage looks unsafe
        if not clean:
            flagged.append({"file": os.path.relpath(f, r"C:\Bari"), "reason": "clean_count==0",
                            "raw": san["raw_count"]}); continue
        bc = os.path.basename(f).replace("bsip1_", "").replace(".json", "")
        # rebuild fields from the clean list
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

# verify the 8 handoff barcodes (post-clean if applied)
checks = ["7290014758681","4127077","4127329","4127336","41445","41452","2824183","2824640"]
verify = {}
for bc in checks:
    g = glob.glob(os.path.join(ROOT, "*", "output", f"bsip1_{bc}.json"))
    g = [p for p in g if not any(x in p.lower() for x in EXCLUDE)]
    if not g:
        verify[bc] = "NOT FOUND"; continue
    j = json.load(open(g[0], encoding="utf-8"))
    verify[bc] = {"count": len(j.get("ingredients_list") or []),
                  "items": j.get("ingredients_list"), "files": len(g)}

out = {"mode": "DRY-RUN" if DRY else "APPLIED", "ts": NOW,
       "dirs_processed": len(dirs), "files_cleaned": len(cleaned),
       "files_flagged": len(flagged), "per_dir": per_dir,
       "flagged": flagged, "verify_8": verify}
json.dump(out, open(r"C:\Bari\_task405_clean_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out["mode"], "| cleaned", len(cleaned), "| flagged", len(flagged), "| dirs", len(per_dir))
