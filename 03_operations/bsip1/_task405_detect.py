# -*- coding: utf-8 -*-
"""TASK-405 detection sweep (READ-ONLY). Reuse the proven sanitize_ingredient_list to
find where nutrition-panel/disclaimer bleed pollutes stored BSIP1 ingredient fields.
No writes. Reports per-run-dir pollution + a distinct-barcode dedup to compare to 47/311."""
import sys, json, glob, os, re
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")
from signal_extractor import sanitize_ingredient_list

ROOT = r"C:\Bari\03_operations\bsip1"
dirs = sorted(set(os.path.dirname(p) for p in glob.glob(os.path.join(ROOT, "*", "output", "bsip1_*.json"))))

per_dir = {}
distinct = {}        # barcode -> {"text": bool, "polluted": bool, "raw": int, "clean": int}
total_files = 0
for d in dirs:
    files = glob.glob(os.path.join(d, "bsip1_*.json"))
    n_text = 0; n_poll = 0
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
        if has_text:
            n_text += 1
        san = sanitize_ingredient_list([str(x) for x in lst]) if lst else None
        polluted = bool(san and san["clean_count"] != san["raw_count"])
        if polluted:
            n_poll += 1
        rec = distinct.setdefault(bc, {"text": False, "polluted": False, "raw": 0, "clean": 0})
        if has_text:
            rec["text"] = True
        if polluted:
            rec["polluted"] = True
            rec["raw"] = san["raw_count"]; rec["clean"] = san["clean_count"]
    per_dir[os.path.relpath(d, r"C:\Bari")] = {"files": len(files), "with_text": n_text, "polluted": n_poll}

dt = sum(1 for v in distinct.values() if v["text"])
dp = sum(1 for v in distinct.values() if v["polluted"])
summary = {
    "total_files_scanned": total_files,
    "run_dirs": len(dirs),
    "distinct_barcodes": len(distinct),
    "distinct_with_text": dt,
    "distinct_polluted": dp,
    "distinct_pollution_rate_pct": round(100*dp/dt, 1) if dt else 0,
    "per_dir_polluted_nonzero": {k: v for k, v in sorted(per_dir.items(), key=lambda x:-x[1]["polluted"]) if v["polluted"] > 0},
}
# 8 verification barcodes
checks = ["7290014758681","4127077","4127329","4127336","41445","41452","2824183","2824640"]
summary["verify_8"] = {bc: distinct.get(bc, "NOT FOUND") for bc in checks}
json.dump(summary, open(r"C:\Bari\_task405_detect.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("files", total_files, "| distinct", len(distinct), "| with_text", dt, "| polluted", dp, f"({summary['distinct_pollution_rate_pct']}%)")
print("dirs with pollution:", len(summary["per_dir_polluted_nonzero"]))
