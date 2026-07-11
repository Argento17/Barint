"""
Apply the dose-honesty classification (creatine_evidence_cosign_v1.md S4) to the raw
scraped creatine-supplement shelf and produce headline counts for the evidence report.

Classification (co-sign S4, arithmetic against the dossier's own ratified 3.0 g/day
min_effective -- no new number invented):
  - honest:      named form + exact g/serving disclosed + >= 3.0 g/day (at labeled use)
  - subtherapeutic: named + quantified but < 3.0 g/day (not concealed, just below floor)
  - fairy_dust:  blend-hidden / % with no serving size / zero quantification anywhere
  - undisclosed: creatine named on-label but no per-serving figure found on the scraped page
"""
from __future__ import annotations

import json
from pathlib import Path

RAW_PATH = Path(r"C:\Bari\03_operations\bsip0\scrape\creatine_supplement_shelf\creatine_supplement_shelf_bsip0_raw_v1.json")

products = json.loads(RAW_PATH.read_text(encoding="utf-8"))


def classify(p: dict) -> str:
    """Co-sign S4 draws the honest/fairy-dust line on CONCEALMENT (named+quantified vs.
    blend-hidden/%-only/zero-quantification), not on the raw gram number alone. A named,
    exactly-quantified per-serving dose that happens to fall under the 3g/1.5g reference
    bands (which are calibrated to monohydrate's studied effective range) is a real
    per-serving-math finding worth reporting, but calling it "fairy dust" -- a term the
    co-sign reserves for concealment -- would overstate what the label actually does.
    HCl's 750mg figure in particular reflects a different-form nominal dose (marketed,
    not independently verified here, as more concentrated per gram than monohydrate) and
    single-capsule servings (California Gold) are a labeling convention, not concealment.
    So: dose bands are reported, but the "fairy dust" word is reserved for the true
    concealment cases (blend-hidden / %-only-no-serving / zero quantification anywhere)."""
    dose = p["creatine_g_per_serving"]
    basis = p["named_vs_blend"]
    if basis == "blend_no_split":
        return "fairy_dust_blend_hidden"
    if dose is None or basis == "named_no_dose":
        return "undisclosed"
    if dose >= 3.0:
        return "honest_meaningful_dose"
    if dose >= 1.5:
        return "disclosed_partial_dose"  # named+quantified, below floor, NOT concealment
    return "disclosed_below_floor"  # named+quantified, well below floor (e.g. single-capsule HCl/monohydrate servings), NOT concealment -- co-sign reserves "fairy dust" for concealment cases


for p in products:
    p["dose_honesty_class"] = classify(p)

RAW_PATH.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")

# ── Headline counts ──────────────────────────────────────────────────────────
from collections import Counter

n = len(products)
by_retailer = Counter(p["retailer_id"] for p in products)
by_form = Counter(p["form"].split(" ")[0].split("(")[0].strip() for p in products)
by_class = Counter(p["dose_honesty_class"] for p in products)
by_cert = sum(1 for p in products if p["third_party_cert"])
prices = [p["price_ils"] for p in products if p["price_ils"] is not None]
standalone = sum(1 for p in products if p["standalone_or_blend"] == "standalone")

print("=== HEADLINE COUNTS ===")
print(f"Total products captured: {n}")
print(f"By retailer/channel: {dict(by_retailer)}")
print(f"By form (raw split): {dict(by_form)}")
print(f"By dose-honesty class: {dict(by_class)}")
print(f"With a stated third-party certification: {by_cert}/{n}")
print(f"Standalone (not blend/pre-workout): {standalone}/{n}")
print(f"Price range (ILS): {min(prices):.2f} - {max(prices):.2f} (n={len(prices)}/{n} priced)")
