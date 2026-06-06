"""TASK-171 thin-live-proof — step 0: re-derive the global-brand addressable SKUs.

The addressable_corpus_mapping_v1.md gives only AGGREGATE counts (23 global-brand,
115 addressable) — it does NOT enumerate the SKUs. So we re-derive from the LIVE
Super-Pharm catalog via il_prices.fetch_super_pharm_supplements():

  1. read the live oral-supplement shelf (identity + price; NO panel — guardrail),
  2. keep SKUs whose Hebrew name maps to ONE of the 15 engine actives (precision-first),
  3. keep only GLOBAL brands (Solgar-led) whose panels are iHerb-gettable today.

Output: global_brand_skus.json — the candidate SKU list the proof pipeline will run.
EDPG: every PriceItem is provenance candidate; identity+price only; nothing scored here.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, r"C:\Bari")
from integrations.clients.il_prices import fetch_super_pharm_supplements

OUT = pathlib.Path(__file__).resolve().parent

# ---- the 15 engine actives, keyed by Hebrew name signals on the Super-Pharm label ----
# precision-first: a miss is "not found", never invented. Multi-active combos are NOT
# force-mapped (left out -> deferred blend, per the mapping doc).
ACTIVE_HE = {
    "magnesium":  [r"מגנזיום", r"magnesium"],
    "vitamin_d3": [r"ויטמין\s*d\s*3", r"ויטמין\s*די", r"vitamin\s*d3?", r"\bd3\b", r"d-3"],
    "omega3":     [r"אומגה", r"omega", r"fish\s*oil"],
    "vitamin_c":  [r"ויטמין\s*c", r"vitamin\s*c", r"\bc\b.*ויטמין"],
    "zinc":       [r"אבץ", r"zinc"],
    "iron":       [r"ברזל", r"iron"],
    "calcium":    [r"סידן", r"calcium"],
    "folic_acid": [r"חומצה\s*פולית", r"folic"],
    "vitamin_b12":[r"b\s*-?\s*12", r"קובלמין", r"cobalamin"],
    "caffeine":   [r"קפאין", r"caffeine"],
    "biotin":     [r"ביוטין", r"biotin"],
    "vitamin_e":  [r"ויטמין\s*e", r"vitamin\s*e"],
    "creatine":   [r"קריאטין", r"creatine"],
    "coq10":      [r"קואנזים", r"coq", r"q10", r"קו-?אנזים"],
    "melatonin":  [r"מלטונין", r"melatonin"],
}

# multi-active combo markers -> NOT a single-active corpus member (deferred blend)
COMBO_MARKERS = [r"מולטי", r"multi", r"\+", r" ו[סבמ]", r"קומפלקס", r"complex", r"b-?קומפלקס"]

# ---- global brands (iHerb-gettable). Hebrew + Latin spellings. Solgar-led. ----
# CRITICAL: brand is detected from the product NAME, NOT the manufacturer/importer field.
# The Super-Pharm importer field is the Israeli DISTRIBUTOR ("אמברוזיה/סולגר" = Ambrosia/
# Solgar) which distributes BOTH the genuine global Solgar line AND the LOCAL SupHerb
# ("סופהרב") house brand. The mapping doc lists SupHerb as LOCAL-ONLY / not iHerb-gettable.
# So we match on the NAME prefix and HARD-EXCLUDE local house brands sharing the importer.
GLOBAL_BRANDS = {
    "solgar":      [r"סולגאר", r"סולגר", r"solgar"],
    "now":         [r"נאו\b", r"now\s*foods", r"\bnow\b"],
    "centrum":     [r"סנטרום", r"centrum"],
    "nature_made": [r"nature'?s?\s*made", r"נייצ'ר\s*מייד"],
    "natures_bounty":[r"nature'?s?\s*bounty", r"באונטי"],
    "doctors_best":[r"doctor'?s?\s*best", r"דוקטורס\s*בست"],
    "jarrow":      [r"jarrow", r"ג'ארו"],
    "california_gold":[r"california\s*gold", r"קליפורניה\s*גולד"],
    "country_life":[r"country\s*life", r"קאנטרי\s*לייף"],
    "biogaia":     [r"biogaia", r"ביוגאיה"],
    "allmax":      [r"allmax", r"אולמקס", r"אלמקס"],
}

# Local house brands that ride the SAME importer as a global brand — hard exclude so the
# importer field can never promote them to "global". (SupHerb shares Ambrosia/Solgar.)
LOCAL_BRAND_EXCLUDE = [r"סופהרב", r"סאפ\s*הרב", r"supherb"]


def match_active(name: str):
    low = name.lower()
    hits = [a for a, pats in ACTIVE_HE.items()
            if any(re.search(p, name) or re.search(p, low) for p in pats)]
    return hits


def is_combo(name: str) -> bool:
    low = name.lower()
    return any(re.search(p, name) or re.search(p, low) for p in COMBO_MARKERS)


def match_brand(name: str, manufacturer: str | None):
    # Match on the product NAME only (not the shared importer field), and reject local
    # house brands first so the importer can never promote a local SKU to "global".
    low_name = name.lower()
    if any(re.search(p, name) or re.search(p, low_name) for p in LOCAL_BRAND_EXCLUDE):
        return None
    for brand, pats in GLOBAL_BRANDS.items():
        if any(re.search(p, name) or re.search(p, low_name) for p in pats):
            return brand
    return None


def run():
    catalog = fetch_super_pharm_supplements()
    print(f"[0] live Super-Pharm oral-supplement SKUs: {len(catalog)}")

    addressable, global_brand = [], []
    for it in catalog:
        actives = match_active(it.name)
        combo = is_combo(it.name)
        # single-active corpus membership: exactly one active and not a combo
        single = (len(actives) == 1) and not combo
        if not actives:
            continue
        addressable.append(it)
        brand = match_brand(it.name, it.manufacturer)
        if brand and single:
            global_brand.append((it, actives[0], brand))

    print(f"[0] addressable (>=1 of 15 actives): {len(addressable)}")
    print(f"[0] GLOBAL-BRAND single-active SKUs: {len(global_brand)}")

    recs = []
    for it, active, brand in global_brand:
        recs.append({
            "barcode": it.barcode,
            "name_he": it.name,
            "manufacturer": it.manufacturer,
            "price_ils": it.price,
            "active_slug": active,
            "global_brand": brand,
            "provenance": it.provenance.as_dict() if it.provenance else None,
        })

    out = {
        "task": "TASK-171 thin-live-proof / step0 derive",
        "verification_status": "candidate",
        "source": "Super-Pharm PriceFull (live) via il_prices.fetch_super_pharm_supplements",
        "live_supplement_skus": len(catalog),
        "addressable_skus": len(addressable),
        "global_brand_single_active_skus": len(global_brand),
        "skus": recs,
    }
    (OUT / "global_brand_skus.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[0] wrote {OUT / 'global_brand_skus.json'} ({len(recs)} SKUs)")
    # print a compact table
    for r in recs:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(f"  {r['barcode']:<15}{r['global_brand']:<16}{r['active_slug']:<12}"
              f"{(r['name_he'] or '')[:48]}")
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    run()
