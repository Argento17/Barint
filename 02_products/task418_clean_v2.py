# -*- coding: utf-8 -*-
"""
TASK-418 — Corrected cleaning script v2 for HC (bsip1_task412) and Juices (bsip1_outputs).

Fixes the TRUNCATE-FIRST bug in v1: entries with real content before a nutrition-panel
boundary were being dropped (is_disclaimer fired first). Correct logic:
  1. Find nutrition-panel boundary in entry
  2. If found and head (text before boundary) is non-empty and not a pure disclaimer -> TRUNCATE
  3. Only if no boundary found, OR head is a pure disclaimer -> check if pure disclaimer -> DROP

Usage:
  python task418_clean_v2.py          # dry-run (no writes)
  python task418_clean_v2.py --apply  # write cleaned files
  python task418_clean_v2.py --restore-and-apply  # restore already-cleaned from original + re-clean
"""

import argparse
import json
import pathlib
import datetime
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HC_DIR    = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip1_task412")
JUICE_DIR = pathlib.Path(r"C:\Bari\02_products\juices\bsip1_outputs")

# 3 juice barcodes with entire list as a single fused string — DO NOT TOUCH
EXCLUDED_JUICE_BARCODES = {
    "7290013153395",   # "ערכים תזונתיים ערכים תזונתיים מיץ רימונים"
    "7290110114886",   # "ערכים תזונתיים ערכים תזונתיים מיץ קלמנטינות"
    "7290003009640",   # "ערכים תזונתיים ערכים תזונתיים מיץ תפוזים"
}

# Juice 7290019056355 first entry special-case
SPECIAL_JUICE_BARCODE = "7290019056355"


# These phrases indicate the START of retailer disclaimer text
DISCLAIMER_MARKERS = [
    "אין להסתמך על הפירוט המופיע באתר",
    "יתכנו טעויות",
    "יש לקרוא את המופיע על גבי אריזת המוצר",
    "הנתונים המדויקים מופיעים על גבי המוצר",
    "התמונות והתאריכים המופיעים הינם להמחשה בלבד",
    "אין להסתמך עליהם",
]

# These phrases mark the boundary where the nutrition panel begins in a fused entry
NUTRITION_BOUNDARY_MARKERS = [
    "ערכים תזונתיים",
    "מכיל חלב ערכים",
    "מכיל חלב עיזים ערכים",
    "עלול להכיל חלב ערכים",
    "עלול להכיל חלב עיזים ערכים",
    " קל אנרגיה",
    " גרם חלבונים",
    " גרם פחמימות",
    " גרם שומנים",
    " מג נתרן",
    " גרם שומן רווי",
]

# Pure nutrition panel start markers (entry is ONLY a nutrition panel bleed)
NUTRITION_PRIMARY_MARKERS = [
    "קל אנרגיה",
    "גרם חלבונים",
    "גרם פחמימות",
    "גרם שומנים",
    "מג נתרן",
    "גרם שומן רווי",
    "גרם חומצות שומן",
]


def is_disclaimer_text(text):
    """True if text contains a retailer disclaimer phrase."""
    for marker in DISCLAIMER_MARKERS:
        if marker in text:
            return True
    return False


def is_pure_nutrition_panel(entry):
    """True if entry is solely a nutrition panel bleed (starts with nutrition marker)."""
    stripped = entry.strip()
    for marker in NUTRITION_PRIMARY_MARKERS:
        if stripped.startswith(marker):
            return True
    return False


def is_pure_disclaimer(entry):
    """True if entry is solely a disclaimer (starts with disclaimer phrase)."""
    stripped = entry.strip()
    for marker in DISCLAIMER_MARKERS:
        if stripped.startswith(marker):
            return True
    return False


def find_nutrition_boundary(entry):
    """Return index of earliest nutrition-panel boundary in entry, or -1 if none found."""
    min_idx = -1
    for marker in NUTRITION_BOUNDARY_MARKERS:
        idx = entry.find(marker)
        if idx >= 0 and (min_idx < 0 or idx < min_idx):
            min_idx = idx
    return min_idx


def clean_entry_v2(entry):
    """
    TRUNCATE-FIRST logic (corrects v1 bug).
    Returns ('keep', entry) | ('truncate', head) | ('drop', entry)
    """
    # Step 1: Pure nutrition panel bleed (starts with nutrition data) -> DROP
    if is_pure_nutrition_panel(entry):
        return "drop", entry

    # Step 2: Pure disclaimer (starts with disclaimer phrase) -> DROP
    if is_pure_disclaimer(entry):
        return "drop", entry

    # Step 3: Find nutrition-panel boundary
    boundary = find_nutrition_boundary(entry)
    if boundary > 0:
        head = entry[:boundary].rstrip(" ,.")
        if len(head) >= 2 and not is_pure_disclaimer(head):
            # Real content before boundary -> TRUNCATE to head
            return "truncate", head
        else:
            # Head is empty or itself a disclaimer -> DROP entire entry
            return "drop", entry

    # Step 4: No boundary found but entry contains a disclaimer -> it IS a disclaimer entry -> DROP
    if is_disclaimer_text(entry):
        return "drop", entry

    # Step 5: No issues -> KEEP
    return "keep", entry


def clean_ingredient_list_v2(entries, barcode=None):
    result_entries = []
    dropped = []
    truncated_entries = []

    for i, entry in enumerate(entries):
        # Special handling: juice 7290019056355 first entry embedded-ingredient
        if barcode == SPECIAL_JUICE_BARCODE and i == 0 and entry.startswith("ערכים תזונתיים ערכים תזונתיים "):
            real_ingredient = entry.replace("ערכים תזונתיים ערכים תזונתיים ", "").strip()
            if real_ingredient:
                truncated_entries.append({"original": entry, "cleaned": real_ingredient})
                result_entries.append(real_ingredient)
            else:
                dropped.append(entry)
            continue

        action, cleaned = clean_entry_v2(entry)
        if action == "drop":
            dropped.append(entry)
        elif action == "truncate":
            truncated_entries.append({"original": entry, "cleaned": cleaned})
            result_entries.append(cleaned)
        else:
            result_entries.append(entry)

    return {
        "clean": result_entries,
        "dropped": dropped,
        "truncated": truncated_entries,
        "raw_count": len(entries),
        "clean_count": len(result_entries),
    }


def process_file(p, apply=False, label="", restore_first=False):
    """Process one BSIP1 file. Returns dict with result info."""
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return {"path": str(p), "status": "error", "error": str(e)}

    barcode = str(doc.get("barcode", ""))

    # Skip excluded juice barcodes
    if barcode in EXCLUDED_JUICE_BARCODES:
        return {"path": str(p), "status": "excluded", "barcode": barcode}

    # If restore_first and already has _task418_clean, restore from original
    if restore_first and "_task418_clean" in doc:
        orig = doc["_task418_clean"].get("original_ingredients_list")
        orig_text = doc["_task418_clean"].get("original_ingredients_text_he")
        if orig is not None:
            doc["ingredients_list"] = list(orig)
            if orig_text is not None:
                doc["ingredients_text_he"] = orig_text
            doc["ingredient_count"] = len(orig)
            del doc["_task418_clean"]

    ingr_list = doc.get("ingredients_list")
    if not isinstance(ingr_list, list) or len(ingr_list) == 0:
        return {"path": str(p), "status": "skip_no_list", "barcode": barcode}

    result = clean_ingredient_list_v2(ingr_list, barcode=barcode)

    if result["dropped"] == [] and result["truncated"] == []:
        return {"path": str(p), "status": "clean", "barcode": barcode}

    # Check: would cleaning empty the list?
    if result["clean_count"] == 0:
        print(f"  FLAG (would-empty): {p.name} — cannot clean without emptying list")
        return {"path": str(p), "status": "flagged_would_empty", "barcode": barcode,
                "dropped": result["dropped"], "truncated": result["truncated"]}

    if apply:
        # Audit block
        audit = {
            "_task418_clean": {
                "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "task": "TASK-418",
                "version": "v2",
                "raw_count": result["raw_count"],
                "clean_count": result["clean_count"],
                "dropped": result["dropped"],
                "truncated": result["truncated"],
                "original_ingredients_list": list(ingr_list),
                "original_ingredients_text_he": doc.get("ingredients_text_he", ""),
            }
        }
        doc.update(audit)
        doc["ingredients_list"] = result["clean"]
        doc["ingredients_text_he"] = ", ".join(result["clean"])
        doc["ingredient_count"] = result["clean_count"]

        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  CLEANED [{label}]: {p.name}  raw={result['raw_count']} -> clean={result['clean_count']}  "
              f"dropped={len(result['dropped'])} truncated={len(result['truncated'])}")
    else:
        print(f"  WOULD-CLEAN [{label}]: {p.name}  raw={result['raw_count']} -> clean={result['clean_count']}  "
              f"dropped={len(result['dropped'])} truncated={len(result['truncated'])}")

    return {
        "path": str(p),
        "status": "cleaned",
        "barcode": barcode,
        "raw_count": result["raw_count"],
        "clean_count": result["clean_count"],
        "dropped": result["dropped"],
        "truncated": result["truncated"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Actually write cleaned files")
    ap.add_argument("--restore-and-apply", action="store_true",
                    help="Restore already-cleaned files from original_ingredients_list then re-clean")
    args = ap.parse_args()

    apply = args.apply or args.restore_and_apply
    restore_first = args.restore_and_apply
    mode = "RESTORE+APPLY" if restore_first else ("APPLY" if apply else "DRY-RUN")
    print(f"=== TASK-418 Ingredient Cleaning v2 [{mode}] ===")
    print()

    results = {"hc": [], "juices": []}

    # --- HC files ---
    hc_files = sorted(HC_DIR.glob("bsip1_hardcheese_*.json"))
    print(f"[HC] Scanning {len(hc_files)} files in {HC_DIR}")
    for p in hc_files:
        r = process_file(p, apply=apply, label="HC", restore_first=restore_first)
        results["hc"].append(r)

    # --- Juice files ---
    juice_files = sorted(JUICE_DIR.glob("bsip1_juice_*.json"))
    print(f"\n[JUICES] Scanning {len(juice_files)} files in {JUICE_DIR}")
    for p in juice_files:
        r = process_file(p, apply=apply, label="JUICE", restore_first=restore_first)
        results["juices"].append(r)

    # --- Summary ---
    print()
    print("=== SUMMARY ===")
    for corpus, label in [("hc", "HC"), ("juices", "JUICES")]:
        rs = results[corpus]
        scanned = len(rs)
        cleaned = sum(1 for r in rs if r["status"] == "cleaned")
        clean = sum(1 for r in rs if r["status"] == "clean")
        excluded = sum(1 for r in rs if r["status"] == "excluded")
        flagged = sum(1 for r in rs if r["status"] == "flagged_would_empty")
        skip = sum(1 for r in rs if r["status"] == "skip_no_list")
        errors = sum(1 for r in rs if r["status"] == "error")
        print(f"[{label}] scanned={scanned}  cleaned={cleaned}  already-clean={clean}  "
              f"excluded={excluded}  flagged={flagged}  skip-no-list={skip}  errors={errors}")
        if cleaned > 0:
            print(f"  Barcodes cleaned:")
            for r in rs:
                if r["status"] == "cleaned":
                    print(f"    {r['barcode']}  dropped={len(r.get('dropped',[]))}  "
                          f"truncated={len(r.get('truncated',[]))}")

    print()
    if not apply:
        print("NOTE: Dry-run only. Pass --apply or --restore-and-apply to write files.")
    else:
        print("Files have been written.")


if __name__ == "__main__":
    main()
