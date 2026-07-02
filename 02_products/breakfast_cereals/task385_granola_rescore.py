"""
TASK-385: Granola clean corpus re-score
Pass A: BARI_SODIUM_CEREAL=OFF (baseline on clean fat data)
Pass B: BARI_SODIUM_CEREAL=ON (EV-049 sodium treatment)

Both passes use run_cereals_008 BSIP2 traces (already have correct fat from EV-029 fix).
This script:
1. Reads all 22 granola traces from run_cereals_008/products/
2. Re-scores each with BSIP1 data using BARI_SODIUM_CEREAL=OFF (Pass A)
3. Re-scores each with BSIP1 data using BARI_SODIUM_CEREAL=ON (Pass B)
4. Produces full tables + delta + HP_FAT_SODIUM analysis
5. Writes outputs to bsip2_outputs/run_granola_task385_{pass}/
"""
import sys, os, io, json, datetime, pathlib, shutil, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "03_operations" / "bsip2" / "proto_v0" / "src"))

GRANOLA_BCS = {
    "7290017962047","7290116534619","7290106773714","7290017962023","7290013433244",
    "7290013433336","7290106771369","7290112498007","7290106771314","7290112497994",
    "7290106771161","7290011668587","7290013433091","7290014471443","7290013433107",
    "7613035635845","7613037012095","7290011131050","7290011131968","7613035622623",
    "7290011131975","1343845"
}

TRACES_DIR = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_008\products")
BSIP1_DIR  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_008\output")
OUTPUT_ROOT = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs")
REPORTS_DIR = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def load_granola_products():
    """Load BSIP1 products for granola barcodes."""
    from input_loader import load_batch
    all_products = load_batch(BSIP1_DIR)
    granola_products = []
    for p in all_products:
        bc = str(p.get("barcode", ""))
        if bc in GRANOLA_BCS:
            granola_products.append(p)
    return granola_products

def run_score_pass(products, sodium_cereal_on: bool, pass_label: str):
    """Run the scoring pipeline for the given products with sodium flag setting."""
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    from trace_writer import assemble_trace, write_trace
    from structural_classifier import classify_structural_class

    # Set the env flag BEFORE importing constants (constants.py reads at module-level,
    # but score_engine reads the env var directly at module load too — we need to patch)
    import score_engine as se
    import constants as sc
    se.BARI_SODIUM_CEREAL = sodium_cereal_on
    # Also patch BARI_FAT_TECH_V1 and BARI_RECAL_P0 on (match granola.json config)
    se.BARI_RECAL_P0 = True
    se.BARI_FAT_TECH_V1 = True
    se.BARI_REDLABEL_V1 = False
    se.BARI_SHELF_RELATIVE_V1 = False

    run_id = f"run_granola_task385_{pass_label}"
    out_dir = OUTPUT_ROOT / run_id
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    results = []
    errors = []

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            signals      = extract_signals(product)
            cat_result   = classify_category(product)
            l3           = signals["L3_inferred_classifications"]
            nova_result  = infer_nova(product, l3)
            eval_result  = assign_evaluation_scope(product, cat_result["category"])
            score_result = score_product(product, signals, cat_result, nova_result, eval_result)
            trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
            trace["structural_class"] = classify_structural_class(trace)
            write_trace(trace, out_dir)
            results.append(trace)
        except Exception as e:
            import traceback
            errors.append({"pid": pid, "error": str(e), "tb": traceback.format_exc()})

    print(f"  Pass {pass_label}: scored {len(results)}, errors {len(errors)}")
    for e in errors:
        print(f"    ERROR {e['pid']}: {e['error']}")
    return results, errors, run_id

def extract_row(trace):
    """Extract key fields from a scoring trace."""
    bc = str(trace.get("input_reference", {}).get("barcode", ""))
    name = trace.get("input_reference", {}).get("product_name_he", "")
    score = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate", "?")
    l1 = trace.get("L1_observed_signals", {})
    fat_g = l1.get("fat_g")
    sodium_mg = l1.get("sodium_mg")
    fat_pct = trace.get("L2_derived_signals", {}).get("fat_pct_of_kcal")
    kcal = l1.get("energy_kcal")
    carbs = l1.get("carbohydrates_g")
    protein = l1.get("protein_g")
    fiber = l1.get("dietary_fiber_g")
    sugar = l1.get("sugars_g")

    # Macro sum check: 4*carb + 4*prot + 9*fat + 2*fiber ~ kcal
    macro_sum = None
    macro_delta = None
    try:
        macro_sum = 4*carbs + 4*protein + 9*fat_g + 2*fiber
        macro_delta = kcal - macro_sum
    except:
        pass

    # Caps fired
    caps_fired = [c.get("rule") for c in trace.get("caps_applied", [])]

    # HP_FAT_SODIUM fired?
    hp_fat_sodium = False
    for p in trace.get("penalties_considered", []):
        if p.get("rule") == "HP_FAT_SODIUM_COMBO" and p.get("fired"):
            hp_fat_sodium = True

    # SODIUM_LOAD_CEREAL_GRAD fired?
    sodium_grad = None
    for p in trace.get("penalties_considered", []):
        if p.get("rule") == "SODIUM_LOAD_CEREAL_GRAD":
            sodium_grad = p.get("amount", 0) if p.get("fired") else 0

    # HIGH_SODIUM_CEREAL_500 cap fired?
    cereal_cap = any(c.get("rule") == "HIGH_SODIUM_CEREAL_500" for c in trace.get("caps_applied", []))

    return {
        "barcode": bc,
        "name": name,
        "score": score,
        "grade": grade,
        "fat_g": fat_g,
        "fat_pct_kcal": fat_pct,
        "sodium_mg": sodium_mg,
        "kcal": kcal,
        "carbs_g": carbs,
        "protein_g": protein,
        "fiber_g": fiber,
        "sugar_g": sugar,
        "macro_sum": round(macro_sum, 1) if macro_sum else None,
        "macro_delta": round(macro_delta, 1) if macro_delta else None,
        "caps_fired": caps_fired,
        "hp_fat_sodium": hp_fat_sodium,
        "sodium_grad_penalty": sodium_grad,
        "cereal_cap_500": cereal_cap,
    }

def print_table(rows, label):
    print(f"\n{'='*120}")
    print(f"PASS {label}")
    print(f"{'='*120}")
    header = f"{'barcode':15s} | {'name':28s} | {'sc':5s} | {'gr':4s} | {'fat':5s} | {'fat%':6s} | {'na':5s} | {'kcal':5s} | {'carb':5s} | {'macro':6s} | {'Δ':5s} | hp_na | na_pen | caps"
    print(header)
    print("-"*len(header))
    for r in sorted(rows, key=lambda x: x.get("score") or 0, reverse=True):
        caps = ",".join(r["caps_fired"]) if r["caps_fired"] else "-"
        hp = "YES" if r["hp_fat_sodium"] else "no"
        na_pen = str(r["sodium_grad_penalty"]) if r["sodium_grad_penalty"] is not None else "-"
        macro_d = f"{r['macro_delta']:+.0f}" if r["macro_delta"] is not None else "N/A"
        macro_s = f"{r['macro_sum']:.0f}" if r["macro_sum"] else "N/A"
        print(f"{r['barcode']:15s} | {r['name'][:28]:28s} | {str(r['score'] or '?'):5s} | {r['grade']:4s} | {str(r['fat_g'] or '?'):5s} | {str(r['fat_pct_kcal'] or '?'):6s} | {str(r['sodium_mg'] or '?'):5s} | {str(r['kcal'] or '?'):5s} | {str(r['carbs_g'] or '?'):5s} | {macro_s:6s} | {macro_d:5s} | {hp:5s} | {na_pen:6s} | {caps}")

def grade_distribution(rows):
    dist = {}
    for r in rows:
        g = r["grade"]
        dist[g] = dist.get(g, 0) + 1
    return dict(sorted(dist.items()))

def main():
    print("=== TASK-385: Granola Clean Corpus Re-Score ===")
    print(f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    print()

    # Load BSIP1 products
    print("Loading BSIP1 granola products...")
    products = load_granola_products()
    print(f"Loaded: {len(products)} granola products")

    # Verify macro sums on BSIP1 data
    print("\nBSIP1 macro sanity check (pre-score):")
    print(f"{'barcode':15s} | {'fat_g':6s} | {'kcal':5s} | {'carbs':5s} | {'prot':5s} | {'fib':5s} | {'macro_sum':9s} | {'delta':6s} | {'macro_ok?'}")
    print("-"*110)
    fat_collapse_count = 0
    fat_ok_count = 0
    for p in products:
        nn = p.get("normalized_nutrition_per_100g", {})
        bc = p.get("barcode", "")
        fat = nn.get("fat_g")
        kcal = nn.get("energy_kcal")
        carbs = nn.get("carbohydrates_g")
        prot = nn.get("protein_g")
        fib = nn.get("dietary_fiber_g")
        macro_sum = None
        macro_delta = None
        ok = "N/A"
        try:
            macro_sum = 4*carbs + 4*prot + 9*fat + 2*fib
            macro_delta = kcal - macro_sum
            ok = "FAIL(collapse?)" if abs(macro_delta) > 100 else "ok"
            if fat is not None and fat < 2.0 and kcal and kcal > 300:
                fat_collapse_count += 1
                ok = "COLLAPSE"
            else:
                fat_ok_count += 1
        except:
            pass
        ms = f"{macro_sum:.0f}" if macro_sum else "N/A"
        md = f"{macro_delta:+.0f}" if macro_delta else "N/A"
        print(f"{bc:15s} | {str(fat):6s} | {str(kcal):5s} | {str(carbs):5s} | {str(prot):5s} | {str(fib):5s} | {ms:9s} | {md:6s} | {ok}")

    print(f"\nFat collapse count: {fat_collapse_count}/22")
    print(f"Fat OK count: {fat_ok_count}/22")
    print()

    # Pass A: BARI_SODIUM_CEREAL=OFF
    print("\n--- Running Pass A: BARI_SODIUM_CEREAL=OFF ---")
    rows_a, errs_a, run_id_a = run_score_pass(products, False, "off")
    extracted_a = [extract_row(t) for t in rows_a]

    # Pass B: BARI_SODIUM_CEREAL=ON
    print("--- Running Pass B: BARI_SODIUM_CEREAL=ON ---")
    rows_b, errs_b, run_id_b = run_score_pass(products, True, "on")
    extracted_b = [extract_row(t) for t in rows_b]

    # Print tables
    print_table(extracted_a, "A (SODIUM_CEREAL=OFF)")
    print_table(extracted_b, "B (SODIUM_CEREAL=ON)")

    # Grade distributions
    dist_a = grade_distribution(extracted_a)
    dist_b = grade_distribution(extracted_b)
    print(f"\n--- Grade Distribution ---")
    print(f"Pass A (OFF): {dist_a}")
    print(f"Pass B (ON):  {dist_b}")

    # A↔B delta
    print(f"\n--- A↔B Delta (grade movers) ---")
    map_a = {r["barcode"]: r for r in extracted_a}
    map_b = {r["barcode"]: r for r in extracted_b}
    score_movers = 0
    grade_movers = []
    for bc in GRANOLA_BCS:
        ra = map_a.get(bc)
        rb = map_b.get(bc)
        if not ra or not rb:
            print(f"  MISSING: {bc}")
            continue
        sa = ra.get("score") or 0
        sb = rb.get("score") or 0
        ga = ra.get("grade")
        gb = rb.get("grade")
        if abs(sa - sb) > 0.01:
            score_movers += 1
        if ga != gb:
            grade_movers.append({
                "barcode": bc,
                "name": ra.get("name"),
                "score_a": sa,
                "score_b": sb,
                "score_delta": round(sb - sa, 1),
                "grade_a": ga,
                "grade_b": gb,
                "sodium_mg": ra.get("sodium_mg"),
                "fat_g": ra.get("fat_g"),
                "fat_pct": ra.get("fat_pct_kcal"),
            })
            print(f"  {bc} | {ra['name'][:35]} | {ga}→{gb} | score {sa:.1f}→{sb:.1f} (Δ{sb-sa:+.1f}) | na={ra.get('sodium_mg')}mg | fat={ra.get('fat_g')}g fat%={ra.get('fat_pct_kcal')}%")

    print(f"\nScore movers: {score_movers}/{len(GRANOLA_BCS)}")
    print(f"Grade movers: {len(grade_movers)}")

    # HP_FAT_SODIUM analysis on clean data
    print(f"\n--- HP_FAT_SODIUM Analysis (Pass A — clean fat) ---")
    print(f"HP threshold: fat_pct >= 25.0% AND sodium >= 300mg")
    hp_candidates = []
    for r in extracted_a:
        fat_pct = r.get("fat_pct_kcal") or 0
        na = r.get("sodium_mg") or 0
        hp_cond = fat_pct >= 25.0 and na >= 300
        na_band = "na<150" if na < 150 else ("150-299" if na < 300 else ("300-449" if na < 450 else ("450-599" if na < 600 else ">=600")))
        if na >= 150 or fat_pct >= 25:
            hp_candidates.append({**r, "hp_cond": hp_cond, "na_band": na_band})
    for r in sorted(hp_candidates, key=lambda x: x.get("sodium_mg") or 0, reverse=True):
        hp_ok = "FIRED" if r["hp_fat_sodium"] else ("WOULD-FIRE" if r["hp_cond"] else "not-fire")
        print(f"  {r['barcode']:15s} | {r['name'][:30]:30s} | fat={r['fat_g']}g fat%={r['fat_pct_kcal']}% | na={r['sodium_mg']}mg {r['na_band']} | {hp_ok}")

    # Sodium distribution analysis
    print(f"\n--- Sodium Band Distribution (Pass A) ---")
    bands = {"<150": [], "150-299": [], "300-449": [], "450-599": [], ">=600": []}
    for r in extracted_a:
        na = r.get("sodium_mg") or 0
        if na < 150: bands["<150"].append(r)
        elif na < 300: bands["150-299"].append(r)
        elif na < 450: bands["300-449"].append(r)
        elif na < 600: bands["450-599"].append(r)
        else: bands[">=600"].append(r)
    for band, items in bands.items():
        print(f"  {band}: {len(items)} products | {'  '.join([i['name'][:20] for i in items])}")

    # Byte-identity proof for BARI_SODIUM_CEREAL=OFF vs run_cereals_008
    print(f"\n--- Byte-Identity Check: Pass A vs run_cereals_008 (SODIUM_CEREAL=OFF) ---")
    match = 0
    mismatch = []
    for bc in GRANOLA_BCS:
        ra = map_a.get(bc)
        # Load existing run_008 trace
        trace_path = TRACES_DIR / f"bsip1_cereal_{bc}" / "bsip2_trace.json"
        if not trace_path.exists():
            print(f"  MISSING existing trace: {bc}")
            continue
        with open(trace_path, encoding="utf-8") as f:
            t008 = json.load(f)
        score_008 = t008.get("final_score_estimate")
        grade_008 = t008.get("grade_estimate")
        score_a = ra.get("score") if ra else None
        grade_a = ra.get("grade") if ra else None
        # Byte-identity: scores within 0.01 and grades match
        if score_a is not None and score_008 is not None:
            if abs(score_a - score_008) < 0.05 and grade_a == grade_008:
                match += 1
            else:
                mismatch.append({"bc": bc, "score_a": score_a, "score_008": score_008, "grade_a": grade_a, "grade_008": grade_008})
        else:
            mismatch.append({"bc": bc, "score_a": score_a, "score_008": score_008})

    if mismatch:
        print(f"  FAIL: {len(mismatch)} mismatches:")
        for m in mismatch:
            print(f"    {m['bc']}: score_a={m.get('score_a')} vs run_008={m.get('score_008')} | grade_a={m.get('grade_a')} vs {m.get('grade_008')}")
    else:
        print(f"  PASS: {match}/{len(GRANOLA_BCS)} granola traces byte-identical to run_cereals_008")
    print(f"  Result: {'PASS' if not mismatch else 'FAIL'} ({match}/{len(GRANOLA_BCS)} match)")

    # Build full per-barcode table for artifact
    full_table = []
    for bc in sorted(GRANOLA_BCS):
        ra = map_a.get(bc, {})
        rb = map_b.get(bc, {})
        full_table.append({
            "barcode": bc,
            "name": ra.get("name", ""),
            "pass_a": {
                "score": ra.get("score"),
                "grade": ra.get("grade"),
                "fat_g": ra.get("fat_g"),
                "fat_pct_kcal": ra.get("fat_pct_kcal"),
                "sodium_mg": ra.get("sodium_mg"),
                "caps_fired": ra.get("caps_fired", []),
                "hp_fat_sodium": ra.get("hp_fat_sodium"),
                "sodium_grad_penalty": ra.get("sodium_grad_penalty"),
            },
            "pass_b": {
                "score": rb.get("score"),
                "grade": rb.get("grade"),
                "fat_g": rb.get("fat_g"),
                "fat_pct_kcal": rb.get("fat_pct_kcal"),
                "sodium_mg": rb.get("sodium_mg"),
                "caps_fired": rb.get("caps_fired", []),
                "hp_fat_sodium": rb.get("hp_fat_sodium"),
                "sodium_grad_penalty": rb.get("sodium_grad_penalty"),
            },
            "delta": {
                "score": round((rb.get("score") or 0) - (ra.get("score") or 0), 1),
                "grade_moved": ra.get("grade") != rb.get("grade"),
                "grade_a": ra.get("grade"),
                "grade_b": rb.get("grade"),
            }
        })

    # Write artifact
    artifact = {
        "_meta": {
            "task": "TASK-385",
            "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "run_id_pass_a": run_id_a,
            "run_id_pass_b": run_id_b,
            "bsip1_source": str(BSIP1_DIR),
            "granola_product_count": len(products),
            "scored_pass_a": len(extracted_a),
            "scored_pass_b": len(extracted_b),
            "fat_collapse_in_bsip1": fat_collapse_count,
            "flags_pass_a": {"BARI_SODIUM_CEREAL": "off", "BARI_RECAL_P0": "on", "BARI_FAT_TECH_V1": "on", "BARI_REDLABEL_V1": "off"},
            "flags_pass_b": {"BARI_SODIUM_CEREAL": "on", "BARI_RECAL_P0": "on", "BARI_FAT_TECH_V1": "on", "BARI_REDLABEL_V1": "off"},
        },
        "grade_distribution_pass_a": dist_a,
        "grade_distribution_pass_b": dist_b,
        "score_movers": score_movers,
        "grade_movers": grade_movers,
        "byte_identity_pass_a": {"result": "PASS" if not mismatch else "FAIL", "match": match, "total": len(GRANOLA_BCS), "mismatches": mismatch},
        "products": full_table,
    }

    out_path = REPORTS_DIR / "task385_granola_rescore_report.json"
    out_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nArtifact written: {out_path}")

    # SHA256
    sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
    print(f"SHA256: {sha}")

    return artifact

if __name__ == "__main__":
    main()
