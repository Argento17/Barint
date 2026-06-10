"""
BARI_REDLABEL_V1 Cross-Shelf Before/After Survey
Runs flag OFF and flag ON for representative products from 4 shelves:
  1. Breakfast cereals / granola
  2. Bread
  3. Salty snacks
  4. Cheese spreads (proxy for spreads/sauces shelf)

Products selected for high sugar (>12g), high sodium (>600mg), or high sat_fat (>5g).
"""
import sys, json, pathlib, os, copy, importlib, textwrap
sys.path.insert(0, str(pathlib.Path(__file__).parent))

def run_product_both_flags(product_data, bsip1_path_or_none=None):
    """
    Run score_product with flag OFF and flag ON.
    Returns (trace_off, trace_on).
    """
    import score_engine
    from input_loader import load_batch
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from trace_writer import assemble_trace

    def _run_once(product, flag_on):
        # Patch the module-level flag
        score_engine.BARI_REDLABEL_V1 = flag_on
        # Also patch constants module if imported separately
        try:
            import constants as C
            C.BARI_REDLABEL_V1 = flag_on
        except Exception:
            pass

        signals = extract_signals(product)
        cat = classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova = infer_nova(product, l3)
        scope = assign_evaluation_scope(product, cat["category"])
        score = score_engine.score_product(product, signals, cat, nova, scope)
        trace = assemble_trace(product, signals, cat, nova, scope, score)
        return trace

    trace_off = _run_once(product_data, flag_on=False)
    trace_on  = _run_once(product_data, flag_on=True)
    return trace_off, trace_on


def load_cereal_product(trace_path):
    """Load product from BSIP1 source given a bsip2_trace path."""
    import json, pathlib
    trace = json.load(open(trace_path, encoding='utf-8'))
    bsip1_path = trace.get('input_reference', {}).get('bsip1_source_path', '')
    if bsip1_path and pathlib.Path(bsip1_path).exists():
        return json.load(open(bsip1_path, encoding='utf-8'))
    return None


def load_bsip1_from_run(bsip1_dir, barcode_or_pid):
    """Try to load a bsip1 file by barcode or PID from a directory."""
    import glob
    patterns = [
        f"{bsip1_dir}/bsip1_{barcode_or_pid}.json",
        f"{bsip1_dir}/*{barcode_or_pid}*.json",
    ]
    for pat in patterns:
        files = glob.glob(pat)
        if files:
            return json.load(open(files[0], encoding='utf-8'))
    return None


def summarize(trace_off, trace_on, shelf, product_hint):
    """Extract before/after comparison row."""
    def _get(trace):
        score = trace.get('final_score_estimate') or trace.get('score_after_floors', 0)
        grade = trace.get('grade_estimate', '?')
        nn = trace.get('L1_observed_signals', {})
        sugar = nn.get('sugars_g') or 0
        sodium = nn.get('sodium_mg') or 0
        sat_fat = nn.get('fat_saturated_g') or 0

        # Find the binding mechanism that changed
        guardrails = trace.get('guardrail_evaluation', {})
        caps_fired = guardrails.get('caps_applied', [])
        pens_fired = guardrails.get('penalties_applied', [])
        fired = [c.get('rule') for c in caps_fired] + [p.get('rule') for p in pens_fired]

        # Reg quality
        dim = trace.get('dimension_scores', {})
        reg_q = dim.get('regulatory_quality', 0)

        return {
            'score': round(score, 1),
            'grade': grade,
            'sugar': round(sugar, 1),
            'sodium': round(sodium, 0),
            'sat_fat': round(sat_fat, 2),
            'fired_rules': fired,
            'reg_quality': round(reg_q, 1),
            'score_after_cap': round(trace.get('score_after_cap', score), 1),
            'score_after_penalty': round(trace.get('score_after_penalty', score), 1),
        }

    r_off = _get(trace_off)
    r_on  = _get(trace_on)
    name = (trace_off.get('input_reference', {}).get('product_name_he')
            or trace_off.get('input_reference', {}).get('product_name')
            or product_hint)
    delta = round(r_on['score'] - r_off['score'], 1)

    # What mechanism changed?
    rules_off = set(r_off['fired_rules'])
    rules_on  = set(r_on['fired_rules'])
    removed = rules_off - rules_on
    added = rules_on - rules_off

    mechanism = []
    if removed:
        mechanism.append(f"removed: {', '.join(sorted(removed))}")
    if added:
        mechanism.append(f"added: {', '.join(sorted(added))}")
    if r_off['reg_quality'] != r_on['reg_quality']:
        mechanism.append(f"reg_quality: {r_off['reg_quality']} → {r_on['reg_quality']}")

    return {
        'shelf': shelf,
        'product': name,
        'score_off': r_off['score'],
        'grade_off': r_off['grade'],
        'score_on': r_on['score'],
        'grade_on': r_on['grade'],
        'delta': delta,
        'mechanism': '; '.join(mechanism) if mechanism else 'no change in rules',
        'sodium_mg': r_off['sodium'],
        'sugar_g': r_off['sugar'],
        'sat_fat_g': r_off['sat_fat'],
        'after_cap_off': r_off['score_after_cap'],
        'after_cap_on': r_on['score_after_cap'],
        'after_pen_off': r_off['score_after_penalty'],
        'after_pen_on': r_on['score_after_penalty'],
    }


def main():
    import glob

    results = []
    errors = []

    # -----------------------------------------------------------------------
    # SHELF 1: Breakfast Cereals
    # Target PIDs (high sugar or high sodium from scan):
    #   bsip1_cereal_42400108153    sugar=42.9g, sodium=453.6mg, score=44.4
    #   bsip1_cereal_7290116537962  sugar=38.5g, sodium=258mg,   score=28.6
    #   bsip1_cereal_4005528115218  sugar=30.0g, sodium=200mg,   score=48.3
    #   bsip1_cereal_884912102102   sugar=27.2g, sodium=339mg,   score=51.0
    #   bsip1_cereal_7613032045753  sugar=20.0g, sodium=1272mg,  score=45.0
    # -----------------------------------------------------------------------
    cereal_pids = [
        'bsip1_cereal_42400108153',
        'bsip1_cereal_7290116537962',
        'bsip1_cereal_4005528115218',
        'bsip1_cereal_884912102102',
        'bsip1_cereal_7613032045753',
    ]
    cereal_bsip1_dir = r'C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\output'
    cereal_trace_root = r'C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_multiretailer_001\products'

    for pid in cereal_pids:
        trace_path = f'{cereal_trace_root}/{pid}/bsip2_trace.json'
        bsip1_path = f'{cereal_bsip1_dir}/bsip1_{pid.replace("bsip1_cereal_", "")}.json'
        try:
            product = json.load(open(bsip1_path, encoding='utf-8'))
            trace_off, trace_on = run_product_both_flags(product)
            row = summarize(trace_off, trace_on, 'cereals', pid)
            results.append(row)
            print(f"[cereals] {pid}: OFF={row['score_off']}/{row['grade_off']}  ON={row['score_on']}/{row['grade_on']}  delta={row['delta']:+.1f}")
        except Exception as e:
            errors.append(f"cereals/{pid}: {e}")
            print(f"  ERROR cereals/{pid}: {e}")

    # -----------------------------------------------------------------------
    # SHELF 2: Bread (high sodium, from bread_retail_003/bsip2)
    # Target products (by sodium, from scan):
    #   shufersal_8606646     score=40, sodium=920
    #   shufersal_7290115251227 score=60, sodium=910
    #   shufersal_318363      score=59.2, sodium=800
    #   shufersal_7290011489595 score=52.7, sodium=754
    #   shufersal_8606615     score=40, sodium=710
    # Bread uses a different input format — load from bsip2 trace and
    # reconstruct the product dict from the bsip2 file itself.
    # -----------------------------------------------------------------------
    bread_pids = [
        'shufersal_8606646',
        'shufersal_7290115251227',
        'shufersal_318363',
        'shufersal_7290011489595',
        'shufersal_4685157',   # score=70.3, sodium=631
    ]
    bread_bsip2_dir = r'C:\Bari\02_products\bread_retail_003\bsip2'
    bread_bsip1_dir = r'C:\Bari\03_operations\bsip1\run_bread_retail_003\output'

    for pid in bread_pids:
        bsip1_path = f'{bread_bsip1_dir}/bsip1_{pid}.json'
        bsip2_path = f'{bread_bsip2_dir}/bsip2_{pid}.json'
        product = None
        # Try bsip1 first
        if pathlib.Path(bsip1_path).exists():
            product = json.load(open(bsip1_path, encoding='utf-8'))
        elif pathlib.Path(bsip2_path).exists():
            # Reconstruct from bsip2 output — use nutrition fields directly
            bsip2 = json.load(open(bsip2_path, encoding='utf-8'))
            n = bsip2.get('nutrition', {})
            product = {
                'canonical_product_id': f'bsip1_bread_{pid}',
                'product_name': bsip2.get('name_he', pid),
                'brand': bsip2.get('brand', ''),
                'category_hint': 'bread',
                'energy_kcal': n.get('energy_kcal'),
                'fat_g': n.get('fat_g'),
                'fat_saturated_g': n.get('fat_saturated_g'),
                'fat_trans_g': n.get('fat_trans_g'),
                'sodium_mg': n.get('sodium_mg'),
                'carbohydrates_g': n.get('carbohydrates_g'),
                'sugars_g': n.get('sugars_g'),
                'dietary_fiber_g': n.get('dietary_fiber_g'),
                'protein_g': n.get('protein_g'),
                'ingredients': [],
                'nova_label': None,
            }

        if product is None:
            errors.append(f"bread/{pid}: no bsip1 or bsip2 file found")
            print(f"  SKIP bread/{pid}: no input file")
            continue

        try:
            trace_off, trace_on = run_product_both_flags(product)
            row = summarize(trace_off, trace_on, 'bread', pid)
            results.append(row)
            print(f"[bread]   {pid}: OFF={row['score_off']}/{row['grade_off']}  ON={row['score_on']}/{row['grade_on']}  delta={row['delta']:+.1f}")
        except Exception as e:
            errors.append(f"bread/{pid}: {e}")
            print(f"  ERROR bread/{pid}: {e}")

    # -----------------------------------------------------------------------
    # SHELF 3: Salty Snacks (high sodium, from salty_snacks bsip2_outputs)
    # Target products:
    #   bsip1_snack_7290011350002   sodium=920, score=57
    #   bsip1_snack_3560071050009   sodium=880, score=57
    #   bsip1_snack_7290011350019   sodium=880, score=57
    #   bsip1_snack_3560071056000   sodium=840, score=57
    #   bsip1_snack_7290004702001   sodium=750, sat_fat=5.0, score=47.5
    # -----------------------------------------------------------------------
    snack_pids = [
        'bsip1_snack_7290011350002',
        'bsip1_snack_3560071050009',
        'bsip1_snack_3560071056000',
        'bsip1_snack_7290004702001',
        'bsip1_snack_7290000055014',  # sodium=580, score=51.9
    ]
    snack_trace_dirs = [
        r'C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_001\products',
        r'C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002\products',
    ]
    snack_bsip1_dirs = [
        r'C:\Bari\03_operations\bsip1\run_salty_snacks_001\output',
        r'C:\Bari\03_operations\bsip1\run_salty_snacks_002\output',
    ]

    for pid in snack_pids:
        barcode = pid.replace('bsip1_snack_', '')
        product = None
        # Try bsip1 dirs
        for bsip1_dir in snack_bsip1_dirs:
            candidate = f'{bsip1_dir}/bsip1_{barcode}.json'
            if pathlib.Path(candidate).exists():
                product = json.load(open(candidate, encoding='utf-8'))
                break
            candidate2 = f'{bsip1_dir}/bsip1_{pid}.json'
            if pathlib.Path(candidate2).exists():
                product = json.load(open(candidate2, encoding='utf-8'))
                break

        # Fall back to reading the bsip2_trace and reconstructing
        if product is None:
            for tdir in snack_trace_dirs:
                tpath = f'{tdir}/{pid}/bsip2_trace.json'
                if pathlib.Path(tpath).exists():
                    trace = json.load(open(tpath, encoding='utf-8'))
                    nn = trace.get('L1_observed_signals', {})
                    product = {
                        'canonical_product_id': pid,
                        'product_name': trace.get('input_reference', {}).get('product_name_he', pid),
                        'brand': trace.get('input_reference', {}).get('brand', ''),
                        'category_hint': 'salty_snack',
                        'energy_kcal': nn.get('energy_kcal'),
                        'fat_g': nn.get('fat_g'),
                        'fat_saturated_g': nn.get('fat_saturated_g'),
                        'fat_trans_g': nn.get('fat_trans_g'),
                        'sodium_mg': nn.get('sodium_mg'),
                        'carbohydrates_g': nn.get('carbohydrates_g'),
                        'sugars_g': nn.get('sugars_g'),
                        'dietary_fiber_g': nn.get('dietary_fiber_g'),
                        'protein_g': nn.get('protein_g'),
                        'ingredients': [],
                        'nova_label': None,
                        'nova_proxy': trace.get('nova_proxy'),
                        'ingredient_count': nn.get('ingredient_count', 0),
                    }
                    break

        if product is None:
            errors.append(f"snacks/{pid}: no input found")
            print(f"  SKIP snacks/{pid}: no input file")
            continue

        try:
            trace_off, trace_on = run_product_both_flags(product)
            row = summarize(trace_off, trace_on, 'salty_snacks', pid)
            results.append(row)
            print(f"[snacks]  {pid}: OFF={row['score_off']}/{row['grade_off']}  ON={row['score_on']}/{row['grade_on']}  delta={row['delta']:+.1f}")
        except Exception as e:
            errors.append(f"snacks/{pid}: {e}")
            print(f"  ERROR snacks/{pid}: {e}")

    # -----------------------------------------------------------------------
    # SHELF 4: Cheese Spreads (proxy for spreads shelf)
    # Target products:
    #   bsip1_cheese_7290108506624  sodium=720, sat_fat=22, score=42
    #   bsip1_cheese_3075553        sodium=610, score=76.9
    #   bsip1_cheese_3075850        sodium=558, sat_fat=8.8, score=52
    #   bsip1_cheese_7290014762831  sodium=481, score=63
    # -----------------------------------------------------------------------
    cheese_pids = [
        'bsip1_cheese_7290108506624',
        'bsip1_cheese_3075553',
        'bsip1_cheese_3075850',
        'bsip1_cheese_7290014762831',
        'bsip1_cheese_7290014762824',
    ]
    cheese_trace_dirs = [
        r'C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_001\products',
        r'C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_002\products',
        r'C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_003\products',
        r'C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_004\products',
    ]
    cheese_bsip1_dirs = [
        r'C:\Bari\03_operations\bsip1\run_cheese_001\output',
        r'C:\Bari\03_operations\bsip1\run_cheese_002\output',
        r'C:\Bari\03_operations\bsip1\run_cheese_003\output',
        r'C:\Bari\03_operations\bsip1\run_cheese_004\output',
    ]

    for pid in cheese_pids:
        barcode = pid.replace('bsip1_cheese_', '')
        product = None
        for bsip1_dir in cheese_bsip1_dirs:
            for candidate in [f'{bsip1_dir}/bsip1_{barcode}.json', f'{bsip1_dir}/bsip1_{pid}.json']:
                if pathlib.Path(candidate).exists():
                    product = json.load(open(candidate, encoding='utf-8'))
                    break
            if product:
                break

        # Fall back to trace reconstruction
        if product is None:
            for tdir in cheese_trace_dirs:
                tpath = f'{tdir}/{pid}/bsip2_trace.json'
                if pathlib.Path(tpath).exists():
                    trace = json.load(open(tpath, encoding='utf-8'))
                    nn = trace.get('L1_observed_signals', {})
                    product = {
                        'canonical_product_id': pid,
                        'product_name': trace.get('input_reference', {}).get('product_name_he', pid),
                        'brand': trace.get('input_reference', {}).get('brand', ''),
                        'category_hint': 'cheese_spread',
                        'energy_kcal': nn.get('energy_kcal'),
                        'fat_g': nn.get('fat_g'),
                        'fat_saturated_g': nn.get('fat_saturated_g'),
                        'fat_trans_g': nn.get('fat_trans_g'),
                        'sodium_mg': nn.get('sodium_mg'),
                        'carbohydrates_g': nn.get('carbohydrates_g'),
                        'sugars_g': nn.get('sugars_g'),
                        'dietary_fiber_g': nn.get('dietary_fiber_g'),
                        'protein_g': nn.get('protein_g'),
                        'ingredients': [],
                        'nova_label': None,
                        'nova_proxy': trace.get('nova_proxy'),
                        'ingredient_count': nn.get('ingredient_count', 0),
                    }
                    break

        if product is None:
            errors.append(f"cheese/{pid}: no input found")
            print(f"  SKIP cheese/{pid}: no input file")
            continue

        try:
            trace_off, trace_on = run_product_both_flags(product)
            row = summarize(trace_off, trace_on, 'cheese_spreads', pid)
            results.append(row)
            print(f"[cheese]  {pid}: OFF={row['score_off']}/{row['grade_off']}  ON={row['score_on']}/{row['grade_on']}  delta={row['delta']:+.1f}")
        except Exception as e:
            errors.append(f"cheese/{pid}: {e}")
            print(f"  ERROR cheese/{pid}: {e}")

    # -----------------------------------------------------------------------
    # OUTPUT
    # -----------------------------------------------------------------------
    print("\n" + "="*100)
    print("BARI_REDLABEL_V1 CROSS-SHELF SURVEY — RESULTS")
    print("="*100)

    shelves_order = ['cereals', 'bread', 'salty_snacks', 'cheese_spreads']
    for shelf in shelves_order:
        shelf_rows = [r for r in results if r['shelf'] == shelf]
        if not shelf_rows:
            print(f"\n[{shelf.upper()}] — no results")
            continue
        print(f"\n{'='*100}")
        print(f"SHELF: {shelf.upper()}")
        print(f"{'='*100}")
        hdr = f"{'Product':<40} | {'OFF':>5} | {'ON':>5} | {'Delta':>6} | {'Mechanism':<55} | {'Na mg':>6} | {'Sug g':>6} | {'Sat g':>6}"
        print(hdr)
        print("-" * len(hdr))
        for r in shelf_rows:
            name = str(r['product'])[:38]
            mech = str(r['mechanism'])[:53]
            print(f"{name:<40} | {r['score_off']:>5} | {r['score_on']:>5} | {r['delta']:>+6.1f} | {mech:<55} | {r['sodium_mg']:>6} | {r['sugar_g']:>6} | {r['sat_fat_g']:>6}")

    if errors:
        print(f"\nERRORS / SKIPPED ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")

    # Save JSON results
    out_path = pathlib.Path(r'C:\Bari\03_operations\bsip2\proto_v0\src\redlabel_v1_survey_results.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'results': results, 'errors': errors}, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")

    return results, errors


if __name__ == '__main__':
    main()
