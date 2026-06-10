"""
BARI_REDLABEL_V1 Cross-Shelf Before/After Survey (v2)
Runs flag OFF and flag ON for representative products from 4 shelves.
Uses proper BSIP1 source files for cereals, snacks, cheese.
Uses normalize_to_bsip1 for bread (no separate bsip1 files).
"""
import sys, json, pathlib, os, glob
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from input_loader import load_product
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from trace_writer import assemble_trace
import score_engine
import constants as C


def patch_flag(on: bool):
    score_engine.BARI_REDLABEL_V1 = on
    C.BARI_REDLABEL_V1 = on


def run_once(product: dict, flag_on: bool) -> dict:
    patch_flag(flag_on)
    prod = {k: v for k, v in product.items() if not k.startswith("_")}
    signals = extract_signals(prod)
    cat = classify_category(prod)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(prod, l3)
    scope = assign_evaluation_scope(prod, cat["category"])
    score = score_engine.score_product(prod, signals, cat, nova, scope)
    trace = assemble_trace(prod, signals, cat, nova, scope, score)
    return trace


def extract_row(trace_off: dict, trace_on: dict, shelf: str, pid: str) -> dict:
    def _fields(trace):
        score = trace.get('final_score_estimate') or trace.get('score_after_floors', 50)
        grade = trace.get('grade_estimate', '?')
        nn = trace.get('L1_observed_signals', {})
        sugar = nn.get('sugars_g') or 0
        sodium = nn.get('sodium_mg') or 0
        sat_fat = nn.get('fat_saturated_g') or 0
        dim = trace.get('dimension_scores', {})
        reg_q = dim.get('regulatory_quality', 0)
        guardrails = trace.get('guardrail_evaluation', {})
        caps = [c.get('rule') for c in (guardrails.get('caps_applied') or [])]
        pens = [p.get('rule') for p in (guardrails.get('penalties_applied') or [])]
        return {
            'score': round(float(score), 1),
            'grade': grade,
            'sugar': round(float(sugar), 1),
            'sodium': round(float(sodium), 0),
            'sat_fat': round(float(sat_fat), 2),
            'reg_quality': round(float(reg_q), 1),
            'caps': caps,
            'pens': pens,
            'after_cap': round(float(trace.get('score_after_cap', score)), 1),
            'after_pen': round(float(trace.get('score_after_penalty', score)), 1),
        }

    f_off = _fields(trace_off)
    f_on  = _fields(trace_on)
    delta = round(f_on['score'] - f_off['score'], 1)

    # Identify mechanism change
    caps_removed = set(f_off['caps']) - set(f_on['caps'])
    caps_added   = set(f_on['caps']) - set(f_off['caps'])
    pens_removed = set(f_off['pens']) - set(f_on['pens'])
    pens_added   = set(f_on['pens']) - set(f_off['pens'])
    reg_change   = f_on['reg_quality'] != f_off['reg_quality']

    mech_parts = []
    if caps_removed:
        mech_parts.append(f"cap removed: {', '.join(sorted(caps_removed))}")
    if caps_added:
        mech_parts.append(f"cap added: {', '.join(sorted(caps_added))}")
    if pens_removed:
        mech_parts.append(f"pen removed: {', '.join(sorted(pens_removed))}")
    if pens_added:
        mech_parts.append(f"pen added: {', '.join(sorted(pens_added))}")
    if reg_change:
        mech_parts.append(f"reg_quality: {f_off['reg_quality']} -> {f_on['reg_quality']}")
    mechanism = '; '.join(mech_parts) if mech_parts else 'no rule change'

    name = (trace_off.get('input_reference', {}).get('product_name_he')
            or trace_off.get('input_reference', {}).get('product_name')
            or pid)

    return {
        'shelf': shelf,
        'pid': pid,
        'product': name,
        'score_off': f_off['score'],
        'grade_off': f_off['grade'],
        'score_on': f_on['score'],
        'grade_on': f_on['grade'],
        'delta': delta,
        'mechanism': mechanism,
        'sodium_mg': f_off['sodium'],
        'sugar_g': f_off['sugar'],
        'sat_fat_g': f_off['sat_fat'],
        'reg_q_off': f_off['reg_quality'],
        'reg_q_on': f_on['reg_quality'],
        'after_cap_off': f_off['after_cap'],
        'after_cap_on': f_on['after_cap'],
        'after_pen_off': f_off['after_pen'],
        'after_pen_on': f_on['after_pen'],
    }


def score_product_pair(product: dict, shelf: str, pid: str) -> dict | None:
    try:
        trace_off = run_once(product, flag_on=False)
        trace_on  = run_once(product, flag_on=True)
        row = extract_row(trace_off, trace_on, shelf, pid)
        return row
    except Exception as e:
        print(f"  ERROR {shelf}/{pid}: {e}")
        return None


# ---------------------------------------------------------------------------
# BREAD: load from normalize_to_bsip1 (extracted inline here)
# ---------------------------------------------------------------------------
import re

def _parse_num(raw):
    if not raw:
        return None
    s = str(raw).strip()
    m = re.match(r"(?:פחות מ|<)\s*([\d.]+)", s, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1)) / 2
        except:
            return None
    m2 = re.match(r"([\d.]+)", s.replace(",", "."))
    if m2:
        try:
            return float(m2.group(1))
        except:
            return None
    return None


def normalize_bread_to_bsip1(raw: dict) -> dict:
    name_he  = (raw.get("name_he") or "").strip()
    barcode  = str(raw.get("barcode") or "")
    brand    = raw.get("brand") or ""
    nutr_raw = raw.get("nutrition", {})

    def _n(k): return _parse_num(nutr_raw.get(k))

    # Try both 'raw' suffixed and direct keys
    energy  = _n("energy_kcal_raw") or _n("energy_kcal") or _parse_num(nutr_raw.get("energy_kcal_raw", ""))
    protein = _n("protein_raw") or _n("protein_g")
    carbs   = _n("carbs_raw") or _n("carbohydrates_g")
    fat     = _n("fat_raw") or _n("fat_g")
    fiber   = _n("fiber_raw") or _n("dietary_fiber_g")
    sodium  = _n("sodium_raw") or _n("sodium_mg")
    sugar   = _n("sugar_raw") or _n("sugars_g")
    sat_fat = _n("sat_fat_raw") or _n("fat_saturated_g")

    rid = raw.get("retailer_id", "shufersal")
    pid = f"bsip1_bread_{rid}_{barcode or name_he[:20]}"

    return {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": name_he,
        "brand": brand,
        "source_retailers": [rid],
        "normalized_nutrition_per_100g": {
            "energy_kcal": energy,
            "fat_g": fat,
            "fat_saturated_g": sat_fat,
            "fat_trans_g": None,
            "sodium_mg": sodium,
            "carbohydrates_g": carbs,
            "sugars_g": sugar,
            "dietary_fiber_g": fiber,
            "protein_g": protein,
        },
        "ingredients_list": [],
        "ingredients_text_he": raw.get("ingredients_raw") or "",
        "ingredient_count": 0,
        "nova_proxy": None,
        "nova_confidence": 0.0,
        "allergens_contains": [],
        "allergens_may_contain": [],
        "confidence": {"overall": 0.6},
        "conflicts_summary": [],
        "missing_fields": [],
        "inferred_fields": [],
        "audit_ref": None,
    }


def main():
    results = []
    errors = []

    # -----------------------------------------------------------------------
    # SHELF 1: Breakfast Cereals (use BSIP1 source files)
    # -----------------------------------------------------------------------
    cereal_bsip1_dir = pathlib.Path(r'C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\output')
    cereal_targets = [
        # (barcode, reason)
        ('42400108153',   'sugar=42.9g, sodium=454mg'),
        ('7290116537962', 'sugar=38.5g, score=28.6'),
        ('4005528115218', 'sugar=30.0g'),
        ('884912102102',  'sugar=27.2g'),
        ('7613032045753', 'sugar=20.0g, sodium=1272mg (very high Na)'),
    ]
    print("\n[CEREALS] Loading from:", cereal_bsip1_dir)
    for barcode, reason in cereal_targets:
        bsip1_path = cereal_bsip1_dir / f'bsip1_{barcode}.json'
        if not bsip1_path.exists():
            errors.append(f'cereals/{barcode}: bsip1 file not found at {bsip1_path}')
            print(f'  SKIP cereals/{barcode}: file not found')
            continue
        product = load_product(bsip1_path)
        pid = product.get('canonical_product_id', barcode)
        row = score_product_pair(product, 'cereals', pid)
        if row:
            row['reason'] = reason
            results.append(row)
            print(f"  {pid}: OFF={row['score_off']}/{row['grade_off']}  ON={row['score_on']}/{row['grade_on']}  delta={row['delta']:+.1f}  |{reason}")

    # -----------------------------------------------------------------------
    # SHELF 2: Bread (normalize from bsip0 raw JSON)
    # -----------------------------------------------------------------------
    bread_raw_path = pathlib.Path(r'C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_20260525T194532_bsip0_raw.json')
    # Real bread products (filtered to exclude cheese/deli/crackers)
    # 9401912=pretzels(688mg), 4685157=rye100%(631mg), 4170479=rustic baguette(580mg),
    # 4033569=lchm parne(571mg), 7290013121028=gluten-free white(537mg)
    bread_targets_barcodes = {'9401912', '4685157', '4170479', '4033569', '7290013121028'}
    # Also search by retailer_id for shufersal products
    bread_targets_ids = {f'shufersal_{b}' for b in bread_targets_barcodes} | bread_targets_barcodes
    print("\n[BREAD] Loading from:", bread_raw_path)
    bread_raw = json.load(open(bread_raw_path, encoding='utf-8'))

    # Build a lookup by barcode and retailer product id
    found_bread = {}
    for raw_p in bread_raw:
        bc = str(raw_p.get('barcode') or '')
        rid = str(raw_p.get('retailer_id') or '')
        # The bsip2 output uses the internal id as key
        # Try to match by barcode
        for target in bread_targets_barcodes:
            if bc == target or bc.endswith(target):
                key = f'shufersal_{target}'
                if key not in found_bread:
                    found_bread[key] = raw_p
    print(f"  Found {len(found_bread)} of {len(bread_targets_barcodes)} bread targets")

    # Also map shufersal product IDs (used in bsip2 outputs) back to raw products
    # The bsip2 product_id = f"shufersal_{internal_id}" where internal_id is from URL
    # Check bsip2 output for the product ID to barcode mapping
    bread_bsip2_dir = pathlib.Path(r'C:\Bari\02_products\bread_retail_003\bsip2')
    if not found_bread:
        # Try matching via bsip2 output files
        for target_raw_id in ['8606646', '7290115251227', '318363', '7290011489595', '4685157']:
            bsip2_file = bread_bsip2_dir / f'bsip2_shufersal_{target_raw_id}.json'
            if bsip2_file.exists():
                bsip2_data = json.load(open(bsip2_file, encoding='utf-8'))
                barcode = bsip2_data.get('barcode', '')
                # Find raw product with this barcode
                for raw_p in bread_raw:
                    if str(raw_p.get('barcode') or '') == str(barcode):
                        found_bread[f'shufersal_{target_raw_id}'] = raw_p
                        break

    print(f"  After bsip2 lookup: found {len(found_bread)} targets")

    # If still empty, fall back to using bsip2 output data directly with nutrition
    for target_raw_id in ['9401912', '4685157', '4170479', '4033569', '7290013121028']:
        pid = f'shufersal_{target_raw_id}'
        if pid in found_bread:
            product = normalize_bread_to_bsip1(found_bread[pid])
            row = score_product_pair(product, 'bread', pid)
            if row:
                results.append(row)
                print(f"  {pid}: OFF={row['score_off']}/{row['grade_off']}  ON={row['score_on']}/{row['grade_on']}  delta={row['delta']:+.1f}")
        else:
            # Use the bsip2 output nutrition directly
            bsip2_file = bread_bsip2_dir / f'bsip2_shufersal_{target_raw_id}.json'
            if bsip2_file.exists():
                bsip2_data = json.load(open(bsip2_file, encoding='utf-8'))
                n = bsip2_data.get('nutrition', {})
                # Build a synthetic raw product
                raw_synth = {
                    'name_he': bsip2_data.get('name_he', pid),
                    'barcode': bsip2_data.get('barcode', ''),
                    'brand': bsip2_data.get('brand', ''),
                    'retailer_id': 'shufersal',
                    'nutrition': {
                        'energy_kcal': n.get('energy_kcal'),
                        'fat_g': n.get('fat_g'),
                        'fat_saturated_g': n.get('fat_saturated_g'),
                        'sodium_mg': n.get('sodium_mg'),
                        'sugars_g': n.get('sugars_g'),
                        'dietary_fiber_g': n.get('dietary_fiber_g'),
                        'protein_g': n.get('protein_g'),
                        'carbohydrates_g': n.get('carbohydrates_g'),
                    }
                }
                product = normalize_bread_to_bsip1(raw_synth)
                # Patch the nutrition directly since _parse_num may fail on already-parsed floats
                product['normalized_nutrition_per_100g'] = {
                    'energy_kcal': n.get('energy_kcal'),
                    'fat_g': n.get('fat_g'),
                    'fat_saturated_g': n.get('fat_saturated_g'),
                    'fat_trans_g': n.get('fat_trans_g'),
                    'sodium_mg': n.get('sodium_mg'),
                    'carbohydrates_g': n.get('carbohydrates_g'),
                    'sugars_g': n.get('sugars_g'),
                    'dietary_fiber_g': n.get('dietary_fiber_g'),
                    'protein_g': n.get('protein_g'),
                }
                row = score_product_pair(product, 'bread', pid)
                if row:
                    results.append(row)
                    print(f"  {pid} (from bsip2): OFF={row['score_off']}/{row['grade_off']}  ON={row['score_on']}/{row['grade_on']}  delta={row['delta']:+.1f}")
            else:
                errors.append(f"bread/{pid}: no source found")
                print(f"  SKIP bread/{pid}: no source found")

    # -----------------------------------------------------------------------
    # SHELF 3: Salty Snacks (BSIP1 source from bsip1_outputs)
    # -----------------------------------------------------------------------
    snack_bsip1_dir = pathlib.Path(r'C:\Bari\02_products\salty_snacks\bsip1_outputs')
    snack_targets = [
        ('bsip1_snack_7290011350002', 'sodium=920mg'),
        ('bsip1_snack_3560071050009', 'sodium=880mg'),
        ('bsip1_snack_3560071056000', 'sodium=840mg'),
        ('bsip1_snack_7290004702001', 'sodium=750mg, sat_fat=5.0g'),
        ('bsip1_snack_7290000055014', 'sodium=580mg, score=51.9 (near-threshold)'),
    ]
    print("\n[SALTY SNACKS] Loading from:", snack_bsip1_dir)
    for pid, reason in snack_targets:
        bsip1_path = snack_bsip1_dir / f'{pid}.json'
        if not bsip1_path.exists():
            errors.append(f'snacks/{pid}: bsip1 file not found')
            print(f'  SKIP snacks/{pid}: not found')
            continue
        product = load_product(bsip1_path)
        row = score_product_pair(product, 'salty_snacks', pid)
        if row:
            row['reason'] = reason
            results.append(row)
            print(f"  {pid}: OFF={row['score_off']}/{row['grade_off']}  ON={row['score_on']}/{row['grade_on']}  delta={row['delta']:+.1f}  |{reason}")

    # -----------------------------------------------------------------------
    # SHELF 4: Cheese Spreads (BSIP1 from bsip2 trace reconstructed)
    # Use the cheese spread traces which already have L1 signals
    # -----------------------------------------------------------------------
    cheese_targets = [
        ('bsip1_cheese_7290108506624', 'sodium=720mg, sat_fat=22g, score=42 (multi RL)'),
        ('bsip1_cheese_3075553',       'sodium=610mg'),
        ('bsip1_cheese_3075850',       'sodium=558mg, sat_fat=8.8g'),
        ('bsip1_cheese_7290014762831', 'sodium=481mg'),
        ('bsip1_cheese_7290019048015', 'sodium ~400mg range'),
    ]
    cheese_trace_dirs = [
        pathlib.Path(r'C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_001\products'),
        pathlib.Path(r'C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_002\products'),
        pathlib.Path(r'C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_003\products'),
        pathlib.Path(r'C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_004\products'),
    ]
    # Also check if there's a direct bsip1_outputs dir
    cheese_bsip1_dir = pathlib.Path(r'C:\Bari\02_products\cheese_spreads\bsip1_outputs')

    print("\n[CHEESE SPREADS] Searching in trace dirs and bsip1 outputs")
    for pid, reason in cheese_targets:
        barcode = pid.replace('bsip1_cheese_', '')
        product = None

        # Try bsip1_outputs
        if cheese_bsip1_dir.exists():
            for fname in [f'{pid}.json', f'bsip1_{barcode}.json']:
                candidate = cheese_bsip1_dir / fname
                if candidate.exists():
                    product = load_product(candidate)
                    break

        # Fall back to trace reconstruction
        if product is None:
            for tdir in cheese_trace_dirs:
                tpath = tdir / pid / 'bsip2_trace.json'
                if tpath.exists():
                    trace = json.load(open(tpath, encoding='utf-8'))
                    nn = trace.get('L1_observed_signals', {})
                    product = {
                        'schema_version': 'bsip1_v0_1',
                        'file_type': 'product',
                        'canonical_product_id': pid,
                        'barcode': barcode,
                        'canonical_name_he': trace.get('input_reference', {}).get('product_name_he', pid),
                        'brand': trace.get('input_reference', {}).get('brand', ''),
                        'source_retailers': trace.get('input_reference', {}).get('source_retailers', []),
                        'normalized_nutrition_per_100g': {
                            'energy_kcal': nn.get('energy_kcal'),
                            'fat_g': nn.get('fat_g'),
                            'fat_saturated_g': nn.get('fat_saturated_g'),
                            'fat_trans_g': nn.get('fat_trans_g'),
                            'sodium_mg': nn.get('sodium_mg'),
                            'carbohydrates_g': nn.get('carbohydrates_g'),
                            'sugars_g': nn.get('sugars_g'),
                            'dietary_fiber_g': nn.get('dietary_fiber_g'),
                            'protein_g': nn.get('protein_g'),
                        },
                        'ingredients_list': nn.get('ingredient_list', []),
                        'ingredient_count': nn.get('ingredient_count', 0),
                        'nova_proxy': trace.get('nova_proxy'),
                        'nova_confidence': 0.5,
                        'allergens_contains': [],
                        'allergens_may_contain': [],
                        'confidence': {'overall': 0.7},
                        'conflicts_summary': [],
                        'missing_fields': [],
                        'inferred_fields': [],
                        'audit_ref': None,
                    }
                    break

        if product is None:
            errors.append(f'cheese/{pid}: no source found')
            print(f'  SKIP cheese/{pid}: not found')
            continue

        row = score_product_pair(product, 'cheese_spreads', pid)
        if row:
            row['reason'] = reason
            results.append(row)
            print(f"  {pid}: OFF={row['score_off']}/{row['grade_off']}  ON={row['score_on']}/{row['grade_on']}  delta={row['delta']:+.1f}  |{reason}")

    # -----------------------------------------------------------------------
    # PRINT RESULTS TABLE
    # -----------------------------------------------------------------------
    print()
    print("=" * 115)
    print("BARI_REDLABEL_V1 CROSS-SHELF SURVEY -- RESULTS")
    print("=" * 115)

    shelf_order = ['cereals', 'bread', 'salty_snacks', 'cheese_spreads']
    shelf_labels = {
        'cereals': 'SHELF 1: BREAKFAST CEREALS',
        'bread': 'SHELF 2: BREAD',
        'salty_snacks': 'SHELF 3: SALTY SNACKS',
        'cheese_spreads': 'SHELF 4: CHEESE SPREADS',
    }

    for shelf in shelf_order:
        rows = [r for r in results if r['shelf'] == shelf]
        if not rows:
            print(f"\n{shelf_labels[shelf]} -- no results")
            continue
        print(f"\n{shelf_labels[shelf]}")
        print("-" * 115)
        hdr = f"{'Product':<38} {'OFF':>5} {'ON':>5} {'Delta':>6}  {'Mechanism':<45}  {'Na mg':>6}  {'Sug g':>5}  {'Sat g':>5}"
        print(hdr)
        print("-" * 115)
        for r in rows:
            name = str(r['product'])[:36]
            mech = str(r['mechanism'])[:43]
            delta_str = f"{r['delta']:+.1f}"
            print(f"{name:<38} {r['score_off']:>5} {r['score_on']:>5} {delta_str:>6}  {mech:<45}  {r['sodium_mg']:>6.0f}  {r['sugar_g']:>5.1f}  {r['sat_fat_g']:>5.2f}")

    if errors:
        print(f"\nSKIPPED / ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")

    # Save full results
    out_path = pathlib.Path(r'C:\Bari\03_operations\bsip2\proto_v0\src\redlabel_v1_survey_results.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'results': results, 'errors': errors}, f, indent=2, ensure_ascii=False)
    print(f"\nFull results -> {out_path}")

    return results, errors


if __name__ == '__main__':
    main()
