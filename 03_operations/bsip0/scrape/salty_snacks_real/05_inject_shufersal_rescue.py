"""
TASK-241 — Inject the 4 verified Shufersal rescue panels into the salty-snacks BSIP0.

The rescue scraper (04) recovered REAL per-100g Shufersal panels + Hebrew ingredients for
the basis-error drops it could identity-confirm (JSON-LD gtin13 == full target barcode).
This step writes those panels back into the BSIP0 retailer raw, OVERRIDING only the bad
per-serving Yochananof panel + ingredients for those EANs. Identity + image are UNTOUCHED
(they came from the real Yochananof catalog). The overridden products are stamped
panel_source = shufersal_product_page so provenance is honest and the BSIP1 builder will
no longer trip basis_error() on them (real kcal ~390-458/100g, not the per-serving 47-132).

Idempotent: re-running re-applies the same override from the rescue file. A timestamped
backup of the BSIP0 is written before the first mutation.
"""
import sys, json, re, pathlib, shutil
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BSIP0 = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip0_outputs\bsip0_salty_snacks_retailer_raw.json")
RESCUE = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip0_outputs\shufersal_rescue_panels.json")


def clean_ingredients(text):
    """Strip raw-scrape artifacts from a Hebrew ingredient string while preserving meaning:
    literal CR/LF tokens ('rn'/'\\r\\n'), a doubled leading letter ('קקמח'->'קמח'),
    intra-word spaces left by line wraps ('לציטי ן'->'לציטין'), and collapse whitespace.
    No ingredient is added or removed."""
    if not text:
        return text
    t = text.replace("\r", " ").replace("\n", " ")
    t = re.sub(r"\brn\b", " ", t)            # literal 'rn' wrap artifact
    t = re.sub(r"^(.)\1", r"\1", t.strip())  # de-duplicate a doubled leading char
    # rejoin a final-form letter split off its word by a wrap (e.g. "לציטי ן" -> "לציטין")
    t = re.sub(r"([א-ת])\s+([ןםךףץ])\b", r"\1\2", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def main():
    rescue = json.loads(RESCUE.read_text(encoding="utf-8"))
    recovered = rescue["recovered"]
    if not recovered:
        print("No recovered panels to inject.")
        return

    bsip0 = json.loads(BSIP0.read_text(encoding="utf-8"))

    # one-time backup
    bak = BSIP0.with_suffix(".pre_task241.json")
    if not bak.exists():
        shutil.copy2(BSIP0, bak)
        print(f"Backup written: {bak}")

    by_ean = {p["barcode"]: p for p in bsip0["products"]}
    applied = []
    for ean, rr in recovered.items():
        p = by_ean.get(ean)
        if p is None:
            print(f"  WARN {ean} not in BSIP0 — skipped")
            continue
        nn = rr["normalized_nutrition_per_100g"]
        ing = clean_ingredients(rr.get("ingredients_text_he"))
        # OVERRIDE panel + ingredients only. Identity (name, sub_pool) + image untouched.
        p["normalized_nutrition_per_100g"] = nn
        p["ingredients_text_he"] = ing
        p["panel_source"] = "shufersal_product_page"
        p["retailer"] = "shufersal"
        p["identity_source"] = "yochananof_catalog"  # identity/image stay Yochananof
        p["nutrition_provenance"] = {
            "panel_source": "shufersal_product_page",
            "shufersal_product_code": rr.get("shufersal_product_code"),
            "shufersal_product_url": rr.get("shufersal_product_url"),
            "shufersal_matched_name": rr.get("shufersal_matched_name"),
            "identity_match": "gtin13_exact (shufersal json-ld gtin13 == target barcode)",
            "verified_per_100g": True,
            "selected_basis": rr.get("selected_basis"),
            "raw_rows": rr.get("raw_rows"),
            "task": "TASK-241",
            "threshold_declared": {},
        }
        p["capture"] = {"basis_per_100g": True, "rescued_from": "shufersal", "task": "TASK-241"}
        applied.append((ean, nn["energy_kcal"], rr["name_he"]))

    bsip0.setdefault("task241_rescue", {})
    bsip0["task241_rescue"] = {
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "recovered_eans": list(recovered.keys()),
        "panel_source": "shufersal_product_page",
        "still_dropped_eans": [d["barcode"] for d in rescue.get("still_dropped", [])],
    }
    BSIP0.write_text(json.dumps(bsip0, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Injected {len(applied)} Shufersal rescue panels into {BSIP0.name}")
    for ean, kcal, name in applied:
        print(f"  + {ean}  kcal={kcal}  {name}")


if __name__ == "__main__":
    main()
