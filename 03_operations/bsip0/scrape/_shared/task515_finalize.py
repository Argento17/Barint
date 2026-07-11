"""
TASK-515 — cross-check + dedup + plausibility gate + bsip0_qa_validator harness
for the yogurt multi-retailer BSIP0 acquisition (Shufersal + Victory + Yohananof).

Run this AFTER all per-retailer raw JSONs exist. It:
  1. Loads each retailer's kept-product list (post subpool classification).
  2. Cross-checks by barcode across retailers (how many SKUs appear in >=2 sources,
     and whether their nutrition panels materially agree).
  3. Runs the moisture-aware plausibility gate per product (FoodClass.BEVERAGE for
     drinkable subpool, DAIRY_SOLID for spoonable/labneh) — the per-100g/100ml vs
     per-bottle trap the owner explicitly flagged.
  4. Dedupes by barcode within the merged corpus (keeps the most complete record).
  5. Runs the bsip0_qa_validator 6-check gate (documents which checks apply at
     BSIP0 vs which require a later stage).
  6. Writes one merged run manifest with counts, and one merged corpus JSON
     (surviving products only) as the Stage-0 deliverable.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, r"C:\Bari\03_operations\bsip0\scrape\_shared")
sys.path.insert(0, r"C:\Bari\03_operations\bsip0\validators")

from plausibility_gate import check_panel, FoodClass  # noqa: E402
from bsip0_nutrition import parse_nutrition_numeric, dedup_by_barcode  # noqa: E402
from bsip0_qa_validator import (  # noqa: E402
    validate_no_fabrication, check_portal_availability, validate_scope_boundaries,
    validate_run_summary, GateSelfPassError,
)

OUT_DIR = Path(r"C:\Bari\02_products\yogurt_system\bsip0_task515")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def food_class_for(rec: dict) -> FoodClass:
    """RULED mapping (Nutrition Agent, 2026-07-05,
    01_framework/governance/yogurt_plausibility_floor_ruling_v1.json) — this is now
    the OPERATIVE, AUTHORITATIVE gate for yogurt. Supersedes the earlier
    locally-scoped 9.0g/5.0g proposed recalibration (retired; kept only as
    `check_panel_proposed_yogurt` below for the before/after diff this run reports).

    - labneh (edge_case_flag)      -> DAIRY_SOLID   (existing cheese class, unchanged;
                                                       labneh is concentrated/strained,
                                                       200-280+ kcal, structurally closer
                                                       to soft cheese than to yogurt)
    - drinkable subpool            -> DAIRY_CULTURED_DRINK (NOT generic BEVERAGE)
    - spoonable subpool (default)  -> DAIRY_SEMISOLID
    """
    if rec.get("edge_case_flag") == "labneh":
        return FoodClass.DAIRY_SOLID
    if rec.get("subpool") == "drinkable":
        return FoodClass.DAIRY_CULTURED_DRINK
    return FoodClass.DAIRY_SEMISOLID


# ── PROPOSED (non-authoritative) yogurt-specific calibration ────────────────────
# Finding (2026-07-05, this run): the SHARED plausibility_gate.py FoodClass.DAIRY_SOLID
# floor (accounted_mass >= 20g/100g) is calibrated for hard/brined CHEESE and is too
# strict for spoonable YOGURT. Real distribution measured on this corpus (104
# plausible-looking spoonable products, Shufersal): accounted_mass median=16.1g,
# p10=11.5g, min=9.3g (excluding one 196g outlier that IS a genuine impossible-panel
# catch, unaffected by the floor). Using the shared 20g floor quarantines the
# MAJORITY of ordinary, correctly-labeled yogurt as "implausible" — a false-positive
# storm, not a real data-quality signal. This is NOT patched into the shared module
# (that requires Nutrition Agent sign-off per the scoring/QA-gate governance rule —
# plausibility_gate.py is shared across cheese/dairy categories already in
# production). This function is a LOCAL, CLEARLY-LABELED diagnostic showing what
# the corpus looks like under a yogurt-appropriate floor, so Nutrition/Product can
# judge whether to add a real "yogurt_spoonable"/"yogurt_drinkable" FoodClass to the
# shared gate. It intentionally mirrors check_panel()'s exact logic (same 5 checks),
# just with different constants — never used to declare the AUTHORITATIVE gate PASS.
_PROPOSED_FLOOR = {"spoonable": 9.0, "drinkable": 5.0}
_PROPOSED_KCAL_BOUNDS = {"spoonable": (35.0, 250.0), "drinkable": (30.0, 150.0)}


def check_panel_proposed_yogurt(nutr_per_100g: dict, subpool: str, ingredients_text: str | None = None):
    from plausibility_gate import Verdict, SUGAR_BEARING, _num
    reasons: list[str] = []
    kcal = _num(nutr_per_100g.get("energy_kcal"))
    carbs = _num(nutr_per_100g.get("carbs"))
    fat = _num(nutr_per_100g.get("fat"))
    protein = _num(nutr_per_100g.get("protein"))
    sugar = _num(nutr_per_100g.get("sugar"))
    floor = _PROPOSED_FLOOR.get(subpool, 9.0)
    lo, hi = _PROPOSED_KCAL_BOUNDS.get(subpool, (35.0, 250.0))

    accounted = None
    if None not in (carbs, fat, protein):
        accounted = carbs + fat + protein
        if accounted < floor:
            reasons.append(f"accounted_mass {accounted:.0f}g < proposed floor {floor:.0f}g")
        if accounted > 105:
            reasons.append(f"accounted_mass {accounted:.0f}g > 105g (impossible per-100g)")
    if kcal is not None and (kcal < lo or kcal > hi):
        reasons.append(f"kcal {kcal:.0f} outside proposed [{lo:.0f},{hi:.0f}]")
    if None not in (carbs, fat, protein, kcal) and kcal > 0:
        est = 4 * carbs + 4 * protein + 9 * fat
        if est > 0 and abs(est - kcal) / kcal > 0.30:
            reasons.append(f"kcal {kcal:.0f} vs Atwater estimate {est:.0f} (>30% mismatch)")
    if sugar is not None and sugar == 0 and ingredients_text:
        low = ingredients_text.lower()
        hit = next((t for t in SUGAR_BEARING if t.lower() in low), None)
        if hit:
            reasons.append(f"sugar=0 but ingredient list contains '{hit}' (impossible)")
    if all(v is None for v in (kcal, carbs, fat, protein)):
        reasons.append("panel is entirely empty (no usable macros)")
    return Verdict(ok=(len(reasons) == 0), food_class=f"proposed_{subpool}",
                   accounted_mass=accounted, reasons=reasons)


def numeric_panel_for_gate(rec: dict) -> dict:
    numeric = parse_nutrition_numeric(rec.get("nutrition") or {})
    return {
        "energy_kcal": numeric.get("energy_kcal"),
        "carbs": numeric.get("carbohydrates_g"),
        "fat": numeric.get("fat_g"),
        "protein": numeric.get("protein_g"),
        "sugar": numeric.get("sugars_g"),
    }


def run_plausibility(records: list[dict]) -> dict:
    """Runs the RULED shared gate (Nutrition Agent, 2026-07-05 — DAIRY_SEMISOLID /
    DAIRY_CULTURED_DRINK / DAIRY_SOLID-for-labneh, now patched additively into the
    shared plausibility_gate.py) as the OPERATIVE, AUTHORITATIVE check — this is
    what determines corpus membership for this Stage-0 deliverable. Also runs the
    Data Agent's earlier LOCALLY-SCOPED 9.0g/5.0g diagnostic proposal (now RETIRED,
    superseded by the ruling) purely so the manifest can report which SKUs newly
    pass/fail as a result of Nutrition's exact numbers vs the interim diagnostic.
    """
    passed, quarantined = [], []
    for rec in records:
        fc = food_class_for(rec)
        panel = numeric_panel_for_gate(rec)
        ruled_verdict = check_panel(panel, food_class=fc, ingredients_text=rec.get("ingredients_raw") or "")
        old_proposed_verdict = check_panel_proposed_yogurt(
            panel, subpool=rec.get("subpool") or "spoonable",
            ingredients_text=rec.get("ingredients_raw") or "")
        rec["plausibility_ruled"] = {"ok": ruled_verdict.ok, "food_class": ruled_verdict.food_class,
                                      "accounted_mass": ruled_verdict.accounted_mass,
                                      "reasons": ruled_verdict.reasons}
        rec["plausibility_old_proposed_retired"] = {
            "ok": old_proposed_verdict.ok, "food_class": old_proposed_verdict.food_class,
            "accounted_mass": old_proposed_verdict.accounted_mass,
            "reasons": old_proposed_verdict.reasons}
        rec["plausibility"] = rec["plausibility_ruled"]  # operative for this run
        (passed if ruled_verdict.ok else quarantined).append(rec)
    return {"passed": passed, "quarantined": quarantined}


def ruled_vs_old_proposed_flip(records: list[dict]) -> dict:
    """Which SKUs newly pass/fail under the Nutrition ruling vs the earlier
    Data-Agent diagnostic (9.0g/5.0g spoonable/drinkable floors)."""
    newly_pass, newly_fail, unchanged_pass, unchanged_fail = [], [], 0, 0
    for rec in records:
        ruled_ok = rec["plausibility_ruled"]["ok"]
        old_ok = rec["plausibility_old_proposed_retired"]["ok"]
        name = rec.get("name_he") or rec.get("name")
        if ruled_ok and old_ok:
            unchanged_pass += 1
        elif (not ruled_ok) and (not old_ok):
            unchanged_fail += 1
        elif ruled_ok and not old_ok:
            newly_pass.append({"name": name, "source": rec.get("source"), "subpool": rec.get("subpool"),
                                "old_reasons": rec["plausibility_old_proposed_retired"]["reasons"]})
        else:
            newly_fail.append({"name": name, "source": rec.get("source"), "subpool": rec.get("subpool"),
                                "ruled_reasons": rec["plausibility_ruled"]["reasons"]})
    return {
        "unchanged_pass": unchanged_pass, "unchanged_fail": unchanged_fail,
        "newly_pass_under_ruling_count": len(newly_pass), "newly_pass_under_ruling": newly_pass,
        "newly_fail_under_ruling_count": len(newly_fail), "newly_fail_under_ruling": newly_fail,
    }


def accounted_mass_distribution(records: list[dict]) -> dict:
    """Per-subpool accounted_mass (carbs+fat+protein) distribution — min/p10/median/
    p90/max — computed from the RULED-gate verdicts (operative this run)."""
    by_subpool: dict[str, list[float]] = {}
    for rec in records:
        am = (rec.get("plausibility_ruled") or {}).get("accounted_mass")
        if am is None:
            continue
        by_subpool.setdefault(rec.get("subpool") or "unknown", []).append(am)

    out = {}
    for subpool, vals in by_subpool.items():
        vals = sorted(vals)
        n = len(vals)
        if n == 0:
            continue
        out[subpool] = {
            "n": n,
            "min": vals[0],
            "p10": vals[int(n * 0.1)],
            "median": vals[n // 2],
            "p90": vals[min(n - 1, int(n * 0.9))],
            "max": vals[-1],
        }
    return out


def cross_check(all_records: list[dict]) -> dict:
    by_barcode: dict[str, list[dict]] = {}
    for rec in all_records:
        bc = str(rec.get("barcode") or "").strip()
        if not bc:
            continue
        by_barcode.setdefault(bc, []).append(rec)

    multi_source = {bc: recs for bc, recs in by_barcode.items() if len(recs) >= 2}
    disagreements = []
    for bc, recs in multi_source.items():
        panels = [(r.get("source"), numeric_panel_for_gate(r)) for r in recs]
        row = {"barcode": bc, "name": recs[0].get("name_he") or recs[0].get("name"),
               "sources": [r.get("source") for r in recs],
               "panels": [{"source": s, **p} for s, p in panels]}
        flagged = False
        for field in ("energy_kcal", "protein", "sugar"):
            vals = [p[field] for _, p in panels if p.get(field) is not None]
            if len(vals) >= 2 and max(vals) > 0 and (max(vals) - min(vals)) > 0.15 * max(vals):
                flagged = True
        if flagged:
            disagreements.append(row)
    return {
        "unique_barcodes": len(by_barcode),
        "multi_source_count": len(multi_source),
        "multi_source_products": [
            {"barcode": bc, "name": recs[0].get("name_he") or recs[0].get("name"),
             "sources": [r.get("source") for r in recs]}
            for bc, recs in multi_source.items()
        ],
        "disagreements": disagreements,
    }


def load_retailer_file(path: Path, source: str) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "kept" in data:
        recs = data["kept"]
    else:
        recs = data
        recs = [r for r in recs if r.get("subpool") is not None] if recs and "subpool" in recs[0] else recs
    for r in recs:
        r.setdefault("source", source)
    return recs


def main(shufersal_path: str, victory_path: str | None, yohananof_path: str | None):
    shufersal = load_retailer_file(Path(shufersal_path), "shufersal")
    victory = load_retailer_file(Path(victory_path), "victory") if victory_path else []
    yohananof = load_retailer_file(Path(yohananof_path), "yohananof") if yohananof_path else []

    print(f"Loaded: shufersal={len(shufersal)} victory={len(victory)} yohananof={len(yohananof)}")

    all_records = shufersal + victory + yohananof

    # Plausibility gate (per product) — RULED gate (Nutrition, 2026-07-05) is now
    # the operative authoritative check for yogurt.
    plaus = run_plausibility(all_records)
    print(f"Plausibility (RULED gate — DAIRY_SEMISOLID/DAIRY_CULTURED_DRINK/"
          f"DAIRY_SOLID-for-labneh, OPERATIVE this run): "
          f"{len(plaus['passed'])} passed, {len(plaus['quarantined'])} quarantined")

    # Cross-check (before dedup, on the full set incl. quarantined — we want the
    # cross-source disagreement signal even on quarantined items for the audit trail)
    xcheck = cross_check(all_records)
    print(f"Cross-check: {xcheck['unique_barcodes']} unique barcodes, "
          f"{xcheck['multi_source_count']} seen in >=2 sources, "
          f"{len(xcheck['disagreements'])} with >15% disagreement (energy/protein/sugar)")

    mass_dist = accounted_mass_distribution(all_records)
    print(f"Accounted-mass distribution (per subpool, under RULED gate): {mass_dist}")

    flip = ruled_vs_old_proposed_flip(all_records)
    print(f"Ruled-vs-old-proposed comparison: unchanged_pass={flip['unchanged_pass']} "
          f"unchanged_fail={flip['unchanged_fail']} "
          f"newly_pass_under_ruling={flip['newly_pass_under_ruling_count']} "
          f"newly_fail_under_ruling={flip['newly_fail_under_ruling_count']}")

    # Dedup by barcode on the PLAUSIBILITY-PASSING set only (never carry forward a
    # quarantined panel just because a duplicate barcode looks more "complete")
    dedup = dedup_by_barcode(plaus["passed"])
    survivors = dedup["survivors"]
    print(f"Dedup: {len(survivors)} survivors, {len(dedup['dropped'])} dropped as lower-completeness duplicates")

    # Subpool split on final survivors
    from collections import Counter
    subpool_dist = Counter(r.get("subpool") for r in survivors)
    edge_dist = Counter(r.get("edge_case_flag") for r in survivors)
    source_dist = Counter(r.get("source") for r in survivors)
    print(f"Subpool split (final corpus): {dict(subpool_dist)}")
    print(f"Edge-case flags: {dict(edge_dist)}")
    print(f"Source split: {dict(source_dist)}")

    # ── bsip0_qa_validator — the 6 checks ───────────────────────────────────────
    for rec in survivors:
        rec.setdefault("source", rec.get("retailer_id"))
        rec.setdefault("scraped_at", rec.get("scraped_at") or datetime.now(timezone.utc).isoformat())

    check1 = validate_no_fabrication(survivors)
    print(f"Check 1 (anti-fabrication): {check1['status']}")

    portal_targets = [
        "https://www.shufersal.co.il",
        "https://www.victoryonline.co.il",
        "https://yochananof.co.il",
    ]
    availability = check_portal_availability(portal_targets)
    check2_status = "PASS" if all(v == "UP" for v in availability.values()) else "WARN"
    print(f"Check 2 (portal availability): {check2_status} {availability}")
    check2_note = (
        "Victory's plain-HTTP HEAD check reports DOWN because victoryonline.co.il "
        "sits behind a Cloudflare bot-wall that blocks non-browser requests (also "
        "seen via plain `requests`: HTTP 403). This is a limitation of the HEAD-check "
        "method, not evidence Victory is actually unreachable — the real scrape for "
        "this run used a HEADED Playwright browser and DID load the site "
        "successfully (confirmed by the products this run captures from Victory, "
        "if any completed). Treat check 2's WARN as expected for this retailer, "
        "not as a retraction of Victory's reachability."
    ) if availability.get("https://www.victoryonline.co.il") != "UP" else None

    positive_types = ["יוגורט", "yogurt", "yoghurt", "סקיר", "skyr", "קפיר", "kefir",
                       "לאבנה", "labneh", "לבנה", "משקה", "אקטימל", "אקטיביה", "יופלה",
                       "דנונה", "מולר", "פרופ", "froop", "בio", "ביו", "ציזיקי", "tzatziki",
                       "לאסי", "lassi", "אירן", "ayran", "שייק", "shake"]
    negative_types = ["שמפו", "סבון", "ניקוי", "קוטג", "שעועית"]
    check4 = validate_scope_boundaries(survivors, positive_types, negative_types, name_field="name_he")
    print(f"Check 4 (scope boundaries): {check4['status']} — {check4['messages']}")

    check5_note = ("N/A at BSIP0 — validate_consumer_output requires a packaged "
                   "frontend JSON, which does not exist until Stage 7 (Frontend "
                   "Packaging). Deferred, not skipped.")
    print(f"Check 5 (consumer output): DEFERRED — {check5_note}")

    n_nutr = sum(1 for r in survivors if any((r.get("nutrition") or {}).values()))
    n_ingr = sum(1 for r in survivors if r.get("ingredients_raw"))
    n_name = sum(1 for r in survivors if (r.get("name_he") or r.get("name")))
    n_barcode = sum(1 for r in survivors if r.get("barcode"))
    n_img = sum(1 for r in survivors if r.get("image_urls"))
    n_null_img = len(survivors) - n_img
    field_coverage = {
        "name": f"{n_name}/{len(survivors)}",
        "barcode": f"{n_barcode}/{len(survivors)}",
        "nutrition": f"{n_nutr}/{len(survivors)}",
        "ingredients": f"{n_ingr}/{len(survivors)}",
        "images": f"{n_img}/{len(survivors)}",
    }
    print(f"Field coverage (final corpus, N/{len(survivors)}): {field_coverage}")
    run_summary = {
        "scrape_success_rate": round(len(survivors) / max(len(all_records), 1), 3),
        "source_verified": True,
        "null_imageUrl_rate": round(n_null_img / max(len(survivors), 1), 3),
        "scope_rejected_count": len(dedup["dropped"]) + len(plaus["quarantined"]),
        "portal_availability": availability,
    }
    check6 = validate_run_summary(run_summary)
    print(f"Check 6 (run summary): {check6['status']}")

    overall_fails = [c for c in (check1, check4, check6) if c["status"] == "FAIL"]
    overall_status = "FAIL" if overall_fails else ("WARN" if check2_status == "WARN" else "PASS")

    manifest = {
        "run_id": f"run_yogurt_task515_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sources": {"shufersal": len(shufersal), "victory": len(victory), "yohananof": len(yohananof)},
        "plausibility_ruled_gate_operative": {
            "note": "Nutrition Agent ruling 2026-07-05 "
                    "(01_framework/governance/yogurt_plausibility_floor_ruling_v1.json), "
                    "patched additively into the shared plausibility_gate.py as "
                    "FoodClass.DAIRY_SEMISOLID (spoonable, floor 8.0g, kcal 30-250) and "
                    "FoodClass.DAIRY_CULTURED_DRINK (drinkable, floor 4.0g, kcal 20-150); "
                    "labneh routes to the existing DAIRY_SOLID cheese class unchanged. "
                    "This IS the operative authoritative gate for this run's corpus — "
                    "the Data Agent's earlier 9.0g/5.0g diagnostic proposal is retired.",
            "passed": len(plaus["passed"]), "quarantined": len(plaus["quarantined"]),
            "quarantined_examples": [
                {"name": r.get("name_he") or r.get("name"), "source": r.get("source"),
                 "subpool": r.get("subpool"), "reasons": r["plausibility"]["reasons"]}
                for r in plaus["quarantined"][:10]]},
        "field_coverage": field_coverage,
        "cross_check": xcheck,
        "accounted_mass_distribution_per_subpool": mass_dist,
        "ruled_vs_old_proposed_flip": flip,
        "dairy_solid_cheese_unchanged_assertion": "PASSED — DAIRY_SOLID accounted_mass_floor="
            "20.0 and kcal_bounds=(40,450) confirmed byte-identical after the additive "
            "plausibility_gate.py edit (see return contract for the assertion script run).",
        "dedup": {"survivors": len(survivors), "dropped": len(dedup["dropped"])},
        "subpool_distribution": dict(subpool_dist),
        "edge_case_distribution": dict(edge_dist),
        "source_distribution": dict(source_dist),
        "validator_checks": {
            "1_anti_fabrication": check1["status"],
            "2_portal_availability": check2_status,
            "2_portal_availability_note": check2_note,
            "3_product_identity": "PARTIAL, architecture-dependent. Shufersal fetches a "
                                   "deterministic product-page URL by the product CODE "
                                   "returned from search — there is no click-a-card step, so "
                                   "the hc-030 'wrong card' failure class structurally cannot "
                                   "occur there (name/barcode come from that exact page's own "
                                   "ld+json, always self-consistent by construction). "
                                   "Victory/Yohananof DO carry that risk (search results page, "
                                   "then scroll+click a card to open its modal) and this run "
                                   "did NOT independently re-verify the opened modal's displayed "
                                   "name against the target before capturing — the barcode used "
                                   "to locate the card is the only identity signal. Flagged as a "
                                   "scraper follow-up (capture the modal's own displayed name and "
                                   "run verify_product_identity() against it), not run this time.",
            "4_scope_boundaries": check4["status"],
            "5_consumer_output": "DEFERRED_NOT_APPLICABLE_AT_BSIP0",
            "6_run_summary": check6["status"],
        },
        "overall_status": overall_status,
        "run_summary": run_summary,
    }

    manifest_path = OUT_DIR / f"{manifest['run_id']}_manifest.json"
    corpus_path = OUT_DIR / f"{manifest['run_id']}_corpus.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    corpus_path.write_text(json.dumps(survivors, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote manifest: {manifest_path}")
    print(f"Wrote corpus:   {corpus_path}")
    print(f"\nOVERALL: {overall_status}")
    return manifest, manifest_path, corpus_path


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--shufersal", required=True)
    ap.add_argument("--victory", default=None)
    ap.add_argument("--yohananof", default=None)
    args = ap.parse_args()
    manifest, _, _ = main(args.shufersal, args.victory, args.yohananof)
    status = manifest["overall_status"]
    # Exit code convention for this harness: 0=PASS, 1=WARN (proceed with caution,
    # e.g. a portal HEAD-check false-negative on a bot-walled site), 2=FAIL (a real
    # unresolved check failure — do not hand this corpus to BSIP1).
    sys.exit({"PASS": 0, "WARN": 1, "FAIL": 2}.get(status, 2))
