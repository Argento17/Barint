"""
Hard-cheese BARI_REDLABEL_V1 pilot — TASK-REDLABEL-001
Runs each product twice (flag OFF, flag ON with BARI_RECAL_P0=on).
QA deliverable: before/after table + corpus summary + recommendation.
"""
import sys
import json
import os
import glob

sys.stdout.reconfigure(encoding="utf-8")

BSIP1_DIR = "c:/Bari/02_products/hard_cheeses/bsip1_outputs/"

WEIGHTS = {
    "processing_quality": 0.15,
    "nutrient_density": 0.15,
    "calorie_density": 0.15,
    "glycemic_quality": 0.12,
    "protein_quality": 0.10,
    "additive_quality": 0.10,
    "satiety_support": 0.06,
    "fat_quality": 0.08,
    "regulatory_quality": 0.05,
    "whole_food_integrity": 0.04,
}

MODULES = [
    "signal_extractor", "score_engine", "nova_proxy", "evaluation_scope",
    "router_v2", "input_loader", "constants", "structural_classifier",
]


def run_once(bsip1_path, redlabel_on, recal_on):
    os.environ["BARI_REDLABEL_V1"] = "on" if redlabel_on else "off"
    os.environ["BARI_RECAL_P0"] = "on" if recal_on else "off"
    for m in MODULES:
        sys.modules.pop(m, None)

    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product

    product = json.load(open(bsip1_path, encoding="utf-8"))
    sig = extract_signals(product)
    cat = classify_category(product)
    nova = infer_nova(product, sig["L3_inferred_classifications"])
    ev = assign_evaluation_scope(product, cat["category"])
    r = score_product(product, sig, cat, nova, ev)
    return r, nova, sig, product, cat


def get_sodium_penalty_info(r):
    """Extract sodium penalty rule name + amount from penalties_applied."""
    penalties = r.get("penalties_applied") or []
    sodium_rules = [
        p for p in penalties
        if "SODIUM" in p.get("rule", "").upper()
    ]
    if sodium_rules:
        rule = sodium_rules[0]["rule"]
        amount = sodium_rules[0]["amount"]
        return f"{rule} -{amount}"
    return "none"


def get_binding_cap_info(r):
    """Return the binding cap rule name (the one that set the cap value)."""
    binding_cap = r.get("binding_cap")
    if binding_cap is None:
        return "none"
    caps = r.get("caps_applied") or []
    # find which cap rule has value == binding_cap
    for c in caps:
        if c.get("cap") == binding_cap:
            return f"{c['rule']}={binding_cap}"
    return f"cap={binding_cap}"


def cap_governed(r, cap_rule_substring):
    """Check if a specific cap rule governed (was the binding cap)."""
    binding_cap = r.get("binding_cap")
    if binding_cap is None:
        return False
    caps = r.get("caps_applied") or []
    for c in caps:
        if cap_rule_substring.upper() in c.get("rule", "").upper():
            if c.get("cap") == binding_cap:
                return True
    return False


def get_main_mechanism_changed(r_off, r_on):
    """Determine the primary mechanism change between OFF and ON runs."""
    mechanisms = []

    cap_off = r_off.get("binding_cap")
    cap_on = r_on.get("binding_cap")

    # Check for cap suppression
    caps_off_rules = {c["rule"] for c in (r_off.get("caps_applied") or [])}
    caps_on_rules = {c["rule"] for c in (r_on.get("caps_applied") or [])}

    suppressed = caps_off_rules - caps_on_rules
    added = caps_on_rules - caps_off_rules

    for rule in suppressed:
        mechanisms.append(f"cap_suppressed:{rule}")
    for rule in added:
        mechanisms.append(f"cap_added:{rule}")

    # Check for sodium penalty change
    sodium_off = get_sodium_penalty_info(r_off)
    sodium_on = get_sodium_penalty_info(r_on)
    if sodium_off != sodium_on:
        mechanisms.append(f"sodium:{sodium_off}→{sodium_on}")

    # Check for null sat_fat imputation
    dnotes_on = r_on.get("dimension_notes") or {}
    rq_note_on = dnotes_on.get("regulatory_quality", "")
    if "EV-REDLABEL-012" in rq_note_on:
        mechanisms.append("null_satfat_imputed")

    # Check for fermentation bonus
    dnotes_off = r_off.get("dimension_notes") or {}
    rq_note_off = dnotes_off.get("regulatory_quality", "")
    if "fermentation" in str(r_on.get("dimension_notes") or {}).lower():
        mechanisms.append("fermentation_bonus")

    return "; ".join(mechanisms) if mechanisms else "no_cap_change"


def get_reformulable_rl_count(r):
    gresult = r.get("guardrail_result") or {}
    return gresult.get("reformulable_rl_count", "n/a")


def sat_fat_handling(product, l3, redlabel_on):
    """Returns: 'disclosed' / 'null-imputed' / 'not_applicable'"""
    nn = product.get("normalized_nutrition_per_100g") or {}
    sat_f = nn.get("fat_saturated_g")
    fat_g = nn.get("fat_g") or 0
    if sat_f is not None:
        return "disclosed"
    # Check if imputation applies
    from constants import (
        REDLABEL_NULL_SATFAT_FAT_FLOOR,
        REDLABEL_ENDEMIC_SATFAT_CATEGORIES,
    )
    if redlabel_on and fat_g >= REDLABEL_NULL_SATFAT_FAT_FLOOR:
        cat = product.get("product_type_dairy", False)
        return "null-imputed"
    return "not_applicable"


def floor_fired(r):
    """Check if any floor rule fired."""
    notes = r.get("score_resolution_notes") or []
    floors = [n for n in notes if "floor" in str(n).lower()]
    return floors[0] if floors else "none"


def check_nova_mismatch(nova_result, product):
    """Compare engine NOVA vs BSIP1 nova_proxy."""
    engine_nova = nova_result.get("nova_level")
    bsip1_nova = product.get("nova_proxy_level") or product.get("nova_level")
    if bsip1_nova is None:
        # try nested
        nova_proxy_raw = product.get("nova_proxy")
    if isinstance(nova_proxy_raw, dict):
        bsip1_nova = nova_proxy_raw.get("nova_level")
    elif isinstance(nova_proxy_raw, int):
        bsip1_nova = nova_proxy_raw
    else:
        bsip1_nova = None
    if bsip1_nova is None:
        return "bsip1_nova_absent"
    if engine_nova != bsip1_nova:
        return f"MISMATCH engine={engine_nova} bsip1={bsip1_nova}"
    return "ok"


def get_product_name(product):
    name = (product.get("product_name")
            or product.get("name")
            or (str(product.get("brand") or "") + " " + str(product.get("product_type") or "")).strip())
    return (name or "unknown").strip()


def get_product_id(product, path):
    pid = product.get("barcode") or product.get("product_id")
    if not pid:
        # extract from filename
        fname = os.path.basename(path)
        pid = fname.replace("bsip1_hardcheese_", "").replace(".json", "")
    return str(pid)


def main():
    paths = sorted(glob.glob(os.path.join(BSIP1_DIR, "bsip1_hardcheese_*.json")))
    if not paths:
        print("ERROR: no BSIP1 files found in", BSIP1_DIR)
        sys.exit(1)

    print(f"Found {len(paths)} BSIP1 files. Running pilot...")
    print()

    results = []
    flags = []  # per-product diagnostic flags

    for path in paths:
        pid = os.path.basename(path).replace("bsip1_hardcheese_", "").replace(".json", "")
        try:
            r_off, nova_off, sig_off, product_off, cat_off = run_once(path, redlabel_on=False, recal_on=False)
            r_on, nova_on, sig_on, product_on, cat_on = run_once(path, redlabel_on=True, recal_on=True)
        except Exception as e:
            print(f"  ERROR {pid}: {e}")
            continue

        l3_off = sig_off["L3_inferred_classifications"]
        l3_on = sig_on["L3_inferred_classifications"]
        nn = product_off.get("normalized_nutrition_per_100g") or {}

        score_off = r_off.get("final_score_estimate")
        score_on = r_on.get("final_score_estimate")
        grade_off = r_off.get("grade_estimate")
        grade_on = r_on.get("grade_estimate")
        delta = round((score_on or 0) - (score_off or 0), 1) if (score_on is not None and score_off is not None) else None

        product_name = get_product_name(product_off)
        product_id = get_product_id(product_off, path)

        # Cap governance in OFF run
        rl2plus_governed_off = cap_governed(r_off, "ISRAELI_RED_LABELS_2_PLUS") or cap_governed(r_off, "REFORMULABLE_LABELS_2_PLUS")
        high_sodium_governed_off = cap_governed(r_off, "HIGH_SODIUM_700MG_PLUS")

        # reformulable_rl_count in ON run
        gresult_on = r_on.get("guardrail_result") or {}
        reformulable_count_on = gresult_on.get("reformulable_rl_count", "n/a")

        # sodium penalty ON
        sodium_pen_on = get_sodium_penalty_info(r_on)

        # sat_fat handling
        sat_f_val = nn.get("fat_saturated_g")
        fat_g_val = nn.get("fat_g") or 0
        if sat_f_val is not None:
            sat_fat_status = "disclosed"
        else:
            # Check if imputation note in regulatory_quality
            dnotes_on = r_on.get("dimension_notes") or {}
            rq_on = dnotes_on.get("regulatory_quality", "")
            if "EV-REDLABEL-012" in rq_on:
                sat_fat_status = "null-imputed"
            else:
                sat_fat_status = "not_applicable"

        # NOVA
        nova_level = nova_on.get("nova_level")
        nova_conf = nova_on.get("nova_confidence", nova_on.get("nova_confidence_score"))
        nova_conf_band = nova_on.get("nova_confidence_band")
        nova_mismatch = check_nova_mismatch(nova_on, product_on)

        # Floors
        floor_info = floor_fired(r_on)

        # Main mechanism changed
        mechanism = get_main_mechanism_changed(r_off, r_on)

        row = {
            "product_id": product_id,
            "product_name": product_name,
            "score_off": score_off,
            "score_on": score_on,
            "delta": delta,
            "grade_off": grade_off,
            "grade_on": grade_on,
            "mechanism": mechanism,
            "rl2plus_governed_off": rl2plus_governed_off,
            "high_sodium_governed_off": high_sodium_governed_off,
            "reformulable_rl_count_on": reformulable_count_on,
            "sodium_pen_on": sodium_pen_on,
            "sat_fat_status": sat_fat_status,
            "nova_level": nova_level,
            "nova_conf_band": nova_conf_band,
            "nova_mismatch": nova_mismatch,
            "floor_on": floor_info,
        }
        results.append(row)

        # Flag conditions
        row_flags = []
        if delta is not None and abs(delta) > 10:
            row_flags.append(f"FLAG: delta={delta} > 10pts")
        # routing confidence check
        cat_conf = cat_on.get("category_confidence", 1.0)
        if cat_conf is not None and cat_conf < 0.70:
            row_flags.append(f"FLAG: routing_conf={cat_conf:.2f} < 0.70")
        if nova_mismatch != "ok" and nova_mismatch != "bsip1_nova_absent":
            row_flags.append(f"FLAG: {nova_mismatch}")
        if row_flags:
            flags.append((product_id, product_name, row_flags))

    # -----------------------------------------------------------------------
    # OUTPUT
    # -----------------------------------------------------------------------

    print("=" * 110)
    print("HARD CHEESE BSIP_REDLABEL_V1 PILOT — BEFORE/AFTER TABLE")
    print(f"Corpus: {len(results)} products  |  flag OFF = baseline  |  flag ON = BARI_REDLABEL_V1=on + BARI_RECAL_P0=on")
    print("=" * 110)

    # Column headers
    hdr = (f"{'product_id':<20} {'name':<35} {'off':>5} {'on':>5} {'Δ':>5} "
           f"{'Goff':>4} {'Gon':>4}  {'mechanism':<55}")
    print(hdr)
    print("-" * 140)

    for row in results:
        name_trunc = row["product_name"][:34]
        delta_str = f"{row['delta']:+.0f}" if row['delta'] is not None else "ERR"
        print(f"{row['product_id']:<20} {name_trunc:<35} {str(row['score_off']):>5} "
              f"{str(row['score_on']):>5} {delta_str:>5} "
              f"{str(row['grade_off']):>4} {str(row['grade_on']):>4}  "
              f"{row['mechanism'][:54]}")

    print()
    print("=" * 110)
    print("PER-PRODUCT DETAIL (cap governance, sodium, sat_fat, NOVA)")
    print("=" * 110)
    print(f"{'product_id':<20} {'RL2+_cap_OFF':>12} {'HiNa_cap_OFF':>12} "
          f"{'reform_rl_ON':>12} {'sodium_pen_ON':<30} {'sat_fat':>12} "
          f"{'NOVA/conf':>10} {'floor':>12}")
    print("-" * 130)

    for row in results:
        nova_str = f"{row['nova_level']}/{row['nova_conf_band']}"
        floor_str = str(row['floor_on'])[:11]
        print(f"{row['product_id']:<20} "
              f"{'yes' if row['rl2plus_governed_off'] else 'no':>12} "
              f"{'yes' if row['high_sodium_governed_off'] else 'no':>12} "
              f"{str(row['reformulable_rl_count_on']):>12} "
              f"{row['sodium_pen_on']:<30} "
              f"{row['sat_fat_status']:>12} "
              f"{nova_str:>10} "
              f"{floor_str:>12}")

    print()
    print("=" * 110)
    print("FLAGGED PRODUCTS (delta > 10 | routing_conf < 0.70 | NOVA mismatch)")
    print("=" * 110)
    if flags:
        for pid, name, flist in flags:
            print(f"  {pid}  {name[:40]}")
            for f in flist:
                print(f"    {f}")
    else:
        print("  None.")

    # -----------------------------------------------------------------------
    # CORPUS SUMMARY
    # -----------------------------------------------------------------------
    print()
    print("=" * 110)
    print("CORPUS-LEVEL SUMMARY")
    print("=" * 110)

    grades = ["S", "A", "B", "C", "D", "E"]

    def grade_rank(g):
        return grades.index(g) if g in grades else 99

    improved = sum(1 for r in results
                   if r["grade_off"] and r["grade_on"]
                   and grade_rank(r["grade_on"]) < grade_rank(r["grade_off"]))
    unchanged = sum(1 for r in results
                    if r["grade_off"] and r["grade_on"]
                    and grade_rank(r["grade_on"]) == grade_rank(r["grade_off"]))
    degraded = sum(1 for r in results
                   if r["grade_off"] and r["grade_on"]
                   and grade_rank(r["grade_on"]) > grade_rank(r["grade_off"]))

    legacy_cap_governing = sum(1 for r in results
                                if r["rl2plus_governed_off"] or r["high_sodium_governed_off"])
    null_sat_fat_imputed = sum(1 for r in results if r["sat_fat_status"] == "null-imputed")
    large_delta = sum(1 for r in results if r["delta"] is not None and abs(r["delta"]) > 10)

    print(f"  Total products scored:             {len(results)}")
    print(f"  Grade IMPROVED (flag ON):          {improved}")
    print(f"  Grade UNCHANGED (flag ON):         {unchanged}")
    print(f"  Grade DEGRADED (flag ON):          {degraded}")
    print(f"  Products with legacy cap governing (OFF run):  {legacy_cap_governing}")
    print(f"    - ISRAELI_RED_LABELS_2_PLUS cap (binding):   {sum(1 for r in results if r['rl2plus_governed_off'])}")
    print(f"    - HIGH_SODIUM_700MG_PLUS cap (binding):      {sum(1 for r in results if r['high_sodium_governed_off'])}")
    print(f"  Null sat_fat imputation fired (ON run):        {null_sat_fat_imputed}")
    print(f"  Products with delta > 10pts (either dir):      {large_delta}")

    # Grade distribution shift
    print()
    print("  Grade distribution shift:")
    print(f"  {'Grade':<8}  {'OFF count':>10}  {'ON count':>10}")
    for g in grades:
        off_ct = sum(1 for r in results if r["grade_off"] == g)
        on_ct = sum(1 for r in results if r["grade_on"] == g)
        if off_ct or on_ct:
            print(f"  {g:<8}  {off_ct:>10}  {on_ct:>10}")

    # -----------------------------------------------------------------------
    # RECOMMENDATION
    # -----------------------------------------------------------------------
    print()
    print("=" * 110)
    print("QA RECOMMENDATION")
    print("=" * 110)

    # Evaluate
    hard_fails = []
    warnings = []

    if degraded > 0:
        warnings.append(f"{degraded} product(s) degraded grade under flag ON — verify intent")

    # Check for any score > 100 or < 0
    impossible = [r for r in results
                  if r["score_on"] is not None and (r["score_on"] > 100 or r["score_on"] < 0)]
    if impossible:
        hard_fails.append(f"{len(impossible)} product(s) with score outside 0-100: {[r['product_id'] for r in impossible]}")

    # Check for excessive delta that might indicate decomposition error
    very_large = [r for r in results if r["delta"] is not None and abs(r["delta"]) > 30]
    if very_large:
        hard_fails.append(f"{len(very_large)} product(s) with delta > 30: {[r['product_id'] for r in very_large]}")

    # Check flags
    nova_mismatches = [(pid, flist) for pid, name, flist in flags
                       if any("MISMATCH" in f for f in flist)]
    if nova_mismatches:
        warnings.append(f"{len(nova_mismatches)} NOVA mismatch(es) detected")

    if hard_fails:
        print("  VERDICT: FAIL")
        print("  Hard failures:")
        for hf in hard_fails:
            print(f"    - {hf}")
    elif warnings:
        print("  VERDICT: CONDITIONAL PASS")
        print("  Blockers requiring resolution before frontend score update:")
        for w in warnings:
            print(f"    - {w}")
    else:
        print("  VERDICT: APPROVE PILOT OUTPUT — proceed to frontend score update")

    print()
    print("  Notes:")
    print(f"  - Flag OFF run: BARI_REDLABEL_V1=off / BARI_RECAL_P0=off (baseline)")
    print(f"  - Flag ON run:  BARI_REDLABEL_V1=on  / BARI_RECAL_P0=on  (pilot)")
    print(f"  - Corpus: {len(paths)} BSIP1 files in {BSIP1_DIR}")
    print(f"  - Scored: {len(results)} / {len(paths)}")
    if len(results) < len(paths):
        print(f"  - {len(paths) - len(results)} file(s) errored — review above ERROR lines")


if __name__ == "__main__":
    main()
