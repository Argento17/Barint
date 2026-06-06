"""
TASK-171D — Phase-3 End-to-End Proof-of-Concept runner
======================================================
Takes 5 REAL Israeli-market-available supplement SKUs whose Supplement Facts panels
were extracted (read-only) from iHerb via firecrawl 2026-06-03, maps each into the
in-house BSIP0-S label model (supplement_label.py), runs each through the REAL SIE
engine (score_engine.score_label), and writes the label + provenance + real engine
output (score / grade / binding_constraint / trace) to JSON.

EDPG: every SKU is verification_status=candidate. These scores are DEMONSTRATIONS of
acquisition->engine reachability, NOT authoritative and NOT admitted to any published
score. No engine changes. Any panel field that could not be extracted is marked missing
(None), never fabricated.
"""
import sys, json, pathlib, datetime

ENGINE = pathlib.Path(r"C:\Bari\03_operations\supplement_engine\proto_v0")
sys.path.insert(0, str(ENGINE / "src"))
sys.path.insert(0, str(ENGINE))

from supplement_label import SupplementLabel, LabelActive          # noqa: E402
from score_engine import score_label                                # noqa: E402
from dossier_loader import load_dossier                             # noqa: E402
from trace_writer import assemble_trace                             # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent
FETCHED_AT = "2026-06-03T09:27:00Z"
CLIENT = "firecrawl_scrape(json)/v2 + iHerb PDP"


def prov(source_id, url, notes=""):
    return {
        "source": "iherb.com",
        "source_id": source_id,
        "source_url": url,
        "fetched_at": FETCHED_AT,
        "client_version": CLIENT,
        "verification_status": "candidate",   # EDPG firewall — NOT admitted
        "admission_note": "candidate only; demonstrates acquisition->engine reach; "
                          "no BSIP0/QA pass; does NOT move any published score.",
        "extraction_notes": notes,
    }


# ---------------------------------------------------------------------------
# The 5 PoC SKUs: (real extracted panel) -> BSIP0-S label + dossier mapping + flags
# Each entry records the raw extraction and any lossy/ambiguous field.
# ---------------------------------------------------------------------------
POC = []

# 1) CREATINE — California Gold Nutrition Sport Pure Creatine Monohydrate 5 g
POC.append(dict(
    sku_id="POC-IL-CREATINE-CGN-149273",
    dossier_slug="creatine",
    provenance=prov("iherb:149273",
        "https://www.iherb.com/pr/california-gold-nutrition-sport-pure-creatine-monohydrate-unflavored-0-18-oz-5-g/149273",
        "form not in Supplement-Facts table; 'monohydrate' taken from product NAME (lossy but unambiguous: single-ingredient pure monohydrate)."),
    raw_panel={"brand": "California Gold Nutrition", "product_name": "Sport, Pure Creatine Monohydrate, 5 g",
               "primary_claim_on_label": "Exercise performance, Strength and power output, Lean muscle support",
               "barcode": "898220100187", "serving_size": "1 packet (5 g)", "proprietary_blend": False,
               "active": {"ingredient": "Creatine Monohydrate", "amount": 5, "unit": "g", "form": "monohydrate (from name)"}},
    label=SupplementLabel(
        sku_id="POC-IL-CREATINE-CGN-149273",
        product_name="California Gold Sport Pure Creatine Monohydrate 5 g",
        primary_claim="strength / lean mass with resistance training",  # maps to dossier Strong tier
        servings_per_day=1.0,
        actives=[LabelActive(active_slug="creatine", display_name="Creatine Monohydrate",
                             quantity=5, unit="g", form="monohydrate", is_core=True)]),
    flags={},
    missing_fields=["active.form (inferred from product name, not panel)"],
))

# 2) MAGNESIUM — California Gold Nutrition Magnesium Bisglycinate, 200 mg ELEMENTAL
#    Label states ELEMENTAL Mg directly -> pass elemental qty; form 'bisglycinate' matches the
#    form ladder (preferred) but is NOT a compound key in elemental_by_form, so the engine does
#    NOT re-apply the elemental fraction (correct: we already have elemental).
POC.append(dict(
    sku_id="POC-IL-MAGNESIUM-CGN-103273",
    dossier_slug="magnesium",
    provenance=prov("iherb:103273",
        "https://www.iherb.com/pr/california-gold-nutrition-magnesium-bisglycinate-chelate-albion-traacs-60-veggie-capsules-100-mg-per-capsule/103273",
        "Panel lists 200 mg ELEMENTAL magnesium (from bisglycinate + a minor oxide). Passed as elemental; "
        "form='bisglycinate' to hit the form ladder WITHOUT re-triggering elemental conversion. "
        "On-label claim is structure/function ('bone, heart, nerve, muscle'), NOT one of the dossier's studied "
        "endpoints (BP / sleep) -> mapped to 'blood pressure reduction' is NOT honest; left as a vague claim that "
        "will resolve Insufficient. This is the real 'untethered claim' case."),
    raw_panel={"brand": "California Gold Nutrition", "product_name": "Magnesium Bisglycinate Chelate (Albion TRAACS)",
               "primary_claim_on_label": "Supports bone, heart, nerve, and muscle health",
               "barcode": "898220019014", "serving_size": "2 capsules", "servings_per_day_label": 30,
               "proprietary_blend": False,
               "active": {"ingredient": "Magnesium", "amount": 200, "unit": "mg", "form": "bisglycinate",
                          "basis": "elemental (per label)"}},
    label=SupplementLabel(
        sku_id="POC-IL-MAGNESIUM-CGN-103273",
        product_name="California Gold Magnesium Bisglycinate 200 mg elemental",
        primary_claim="bone, heart, nerve and muscle health (structure/function)",  # untethered -> Insufficient
        servings_per_day=1.0,
        actives=[LabelActive(active_slug="magnesium", display_name="Magnesium (bisglycinate)",
                             quantity=200, unit="mg", form="bisglycinate", is_core=True)]),
    flags={},
    missing_fields=["on-label studied endpoint (label claim is structure/function, not a dossier claim tier)"],
))

# 3) VITAMIN D3 — Country Life Vitamin D3 5,000 IU
POC.append(dict(
    sku_id="POC-IL-VITD3-COUNTRYLIFE-141067",
    dossier_slug="vitamin_d3",
    provenance=prov("iherb:141067",
        "https://www.iherb.com/pr/country-life-vitamin-d3-125-mcg-5-000-lu-365-softgels/141067",
        "Clean panel: 5000 IU cholecalciferol, 1 softgel/day. 5000 IU exceeds the dossier UL (4000 IU) -> "
        "expect a safety mechanism to bind. Truthful test of the UL veto on a real, common retail dose."),
    raw_panel={"brand": "Country Life", "product_name": "Vitamin D3 125 mcg (5,000 IU)",
               "primary_claim_on_label": "bone, dental, immune health; aids calcium absorption",
               "barcode": "015794058120", "serving_size": "1 softgel", "servings_per_day_label": 1,
               "proprietary_blend": False,
               "active": {"ingredient": "Vitamin D3 (cholecalciferol)", "amount": 5000, "unit": "IU", "form": "cholecalciferol"}},
    label=SupplementLabel(
        sku_id="POC-IL-VITD3-COUNTRYLIFE-141067",
        product_name="Country Life Vitamin D3 5000 IU",
        primary_claim="correcting/maintaining vitamin D status (raising serum 25(OH)D)",
        servings_per_day=1.0, labeled_regimen="daily",
        actives=[LabelActive(active_slug="vitamin_d3", display_name="Vitamin D3",
                             quantity=5000, unit="IU", form="D3 (cholecalciferol)", is_core=True)]),
    flags={},
    missing_fields=[],
))

# 4) CAFFEINE — ALLMAX Essentials Caffeine 200 mg
POC.append(dict(
    sku_id="POC-IL-CAFFEINE-ALLMAX-67652",
    dossier_slug="caffeine",
    provenance=prov("iherb:67652",
        "https://www.iherb.com/pr/allmax-essentials-caffeine-200-mg-100-tablets/67652",
        "Clean single-active panel: 200 mg caffeine anhydrous, disclosed (no blend). On-label claim = mental "
        "alertness -> mapped to the dossier acute-alertness claim. Caffeine dose basis is per-kg in the dossier; "
        "engine normalizes against a ~70 kg adult (dossier note)."),
    raw_panel={"brand": "ALLMAX", "product_name": "Essentials Caffeine 200 mg",
               "primary_claim_on_label": "Restore mental alertness",
               "barcode": "665553126227", "serving_size": "1 tablet", "servings_per_day_label": "up to 5",
               "proprietary_blend": False,
               "active": {"ingredient": "Caffeine", "amount": 200, "unit": "mg", "form": "anhydrous"}},
    label=SupplementLabel(
        sku_id="POC-IL-CAFFEINE-ALLMAX-67652",
        product_name="ALLMAX Essentials Caffeine 200 mg",
        primary_claim="alertness / vigilance / cognitive performance (acute)",
        servings_per_day=1.0,
        actives=[LabelActive(active_slug="caffeine", display_name="Caffeine anhydrous",
                             quantity=200, unit="mg", form="caffeine anhydrous", is_core=True)]),
    flags={},
    missing_fields=[],
))

# 5) OMEGA-3 — NOW Foods Omega-3 Fish Oil, EPA 360 + DHA 240 = 600 mg EPA+DHA / 2 softgels
#    Dossier active = combined EPA+DHA. Panel gives them separately -> sum to the scored active.
#    Form TG/EE NOT on panel (only 'fish oil concentrate') -> form unknown (lossy, marked).
POC.append(dict(
    sku_id="POC-IL-OMEGA3-NOW-102333",
    dossier_slug="omega3",
    provenance=prov("iherb:102333",
        "https://www.iherb.com/pr/now-foods-omega-3-fish-oil-1-000-mg-180-epa-120-dha-100-softgels/102333",
        "EPA 360 + DHA 240 = 600 mg combined EPA+DHA per 2-softgel serving (the scored active). "
        "Chemical form (TG vs ethyl-ester) is NOT on the panel -> form=None (UNKNOWN, not fabricated). "
        "On-label claim = heart/cardiovascular -> nearest dossier claim is CV (deferred/insufficient) NOT the "
        "TG-lowering Strong claim; mapped to the broad CV claim truthfully."),
    raw_panel={"brand": "NOW Foods", "product_name": "Omega-3 Fish Oil 1000 mg (180 EPA/120 DHA)",
               "primary_claim_on_label": "Cardiovascular / heart health",
               "barcode": "733739016508", "serving_size": "2 softgels", "servings_per_day_label": 2,
               "proprietary_blend": False,
               "actives_raw": [{"EPA": 360, "DHA": 240, "unit": "mg"}],
               "scored_active": {"ingredient": "EPA+DHA (combined)", "amount": 600, "unit": "mg", "form": None}},
    label=SupplementLabel(
        sku_id="POC-IL-OMEGA3-NOW-102333",
        product_name="NOW Foods Omega-3 Fish Oil (EPA360/DHA240)",
        primary_claim="cardiovascular disease / CV events prevention",
        servings_per_day=1.0,
        actives=[LabelActive(active_slug="omega3", display_name="EPA+DHA combined",
                             quantity=600, unit="mg", form=None, is_core=True)]),  # form UNKNOWN (not on panel)
    flags={},
    missing_fields=["active.form (TG/EE not disclosed on panel -> form=None)"],
))


def run():
    out_records = []
    summary = []
    for sku in POC:
        dossier = load_dossier(sku["dossier_slug"])
        result = score_label(sku["label"], dossier, **sku["flags"])
        comb = result["combination"]
        cm = result["claim_matched"]
        facts = [{"field": f"claims['{cm}'].evidence_tier",
                  "value": result["sub_scores"]["evidence"]["tier"],
                  "supp_ev": result["supp_ev_refs"][0] if result["supp_ev_refs"] else None}]
        trace = assemble_trace(result, facts)
        rec = {
            "sku_id": sku["sku_id"],
            "dossier_active": result["active"],
            "provenance": sku["provenance"],
            "raw_extracted_panel": sku["raw_panel"],
            "missing_or_lossy_fields": sku["missing_fields"],
            "bsip0s_label": {
                "product_name": sku["label"].product_name,
                "primary_claim_fed": sku["label"].primary_claim,
                "actives": [vars(a) for a in sku["label"].actives],
                "servings_per_day": sku["label"].servings_per_day,
                "labeled_regimen": sku["label"].labeled_regimen,
            },
            "engine_output": {
                "claim_matched": cm,
                "score": comb["final_score"],
                "grade": comb["grade"],
                "blend": comb["blend"],
                "binding_constraint": comb["binding_constraint"],
                "sub_scores": {d: result["sub_scores"][d]["value"] for d in
                               ["evidence", "dose", "form", "honesty", "safety"]},
                "signature": trace["signature"],
                "caps_vetoes_fired": comb["caps_vetoes_fired"],
            },
            "trace": trace,
        }
        out_records.append(rec)
        path = OUT / f"{sku['sku_id']}.json"
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=2, ensure_ascii=False)
        summary.append((sku["sku_id"], result["active"], comb["final_score"], comb["grade"],
                        comb["binding_constraint"]["mechanism"], cm))

    # index file
    idx = {
        "task": "TASK-171D",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "verification_status": "candidate",
        "edpg_note": "All 5 SKUs are candidate; engine outputs are demonstrations of acquisition->engine "
                     "reachability, NOT authoritative, NOT admitted to any published score.",
        "engine": "03_operations/supplement_engine/proto_v0 (no changes)",
        "source": "iHerb PDPs via firecrawl_scrape(json) 2026-06-03; read-only",
        "skus": [r["sku_id"] for r in out_records],
    }
    with open(OUT / "_index.json", "w", encoding="utf-8") as fh:
        json.dump(idx, fh, indent=2, ensure_ascii=False)

    print("=" * 100)
    print("TASK-171D PoC — 5 REAL SKUs through the REAL SIE engine (ALL candidate / calibration-pending)")
    print("=" * 100)
    print(f"{'sku':<36}{'active':<22}{'score':>6}{'grd':>4}  {'binding_constraint':<30}")
    print("-" * 100)
    for sid, act, sc, gr, bind, cm in summary:
        print(f"{sid:<36}{act:<22}{sc:>6}{gr:>4}  {bind:<30}")
        print(f"{'':4}claim_matched={cm}")
    print("=" * 100)
    print(f"wrote {len(out_records)} SKU JSONs + _index.json to {OUT}")


if __name__ == "__main__":
    run()
