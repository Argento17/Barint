"""Generate frozen_vegetables_frontend_v1.json from BSIP2 traces."""
import sys, io, json, pathlib, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = pathlib.Path(r'C:\Bari')
TRACES_DIR = BASE / '02_products' / 'frozen_vegetables' / 'bsip2_outputs' / 'run_frozen_vegetables_001' / 'products'
BSIP1_DIR = BASE / '02_products' / 'frozen_vegetables' / 'bsip1_outputs'
OUTPUT = BASE / 'bari-web' / 'src' / 'data' / 'comparisons' / 'frozen_vegetables_frontend_v1.json'

# TASK-233B: grade/confidence/image/strip are now owned by the shared packaging core
# (frontend_core), which delegates confidence to confidence_annotation. Do NOT hand-roll
# confidence strings, grade, or image URLs here (a bespoke version once shipped a false
# "official food source" claim + a synthesized MNH68_ image prefix that 404s — TASK-233D).
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import confidence_annotation as CA
import frontend_core as FC

def load_traces():
    traces = []
    for d in sorted(TRACES_DIR.iterdir()):
        if not d.is_dir():
            continue
        p = d / 'bsip2_trace.json'
        if not p.exists():
            continue
        t = json.loads(p.read_text(encoding='utf-8'))
        traces.append(t)
    return traces

def get_nutrition(trace: dict) -> dict:
    """Extract the per-100g panel from L1_observed_signals — the engine's OBSERVED
    source of truth. The old source (dimension_scores.nutrition_score) is empty on all
    53 traces (QA: 0/53 populated), so reading it dropped 100% of the panel. Note the
    real L1 keys: dietary_fiber_g (not fiber_g) and sugars_g."""
    l1 = trace.get('L1_observed_signals', {}) or {}
    nn = {}
    for l1key, bkey in [('energy_kcal', 'energyKcal'), ('protein_g', 'protein'),
                        ('sugars_g', 'sugar'), ('fat_g', 'fat'),
                        ('fat_saturated_g', 'satFat'), ('dietary_fiber_g', 'fiber'),
                        ('sodium_mg', 'sodium')]:
        val = l1.get(l1key)
        nn[bkey] = round(val, 1) if isinstance(val, (int, float)) else None
    return nn


def get_ingredients(trace: dict):
    """Join the L1_observed_signals ingredient_list into the VM's `string | null`.
    The list is the engine's observed ingredient text (comma-split at scrape time);
    rejoining reconstructs the label string. Was hardcoded to None, dropping it on all 53."""
    l1 = trace.get('L1_observed_signals', {}) or {}
    il = l1.get('ingredient_list')
    if isinstance(il, (list, tuple)):
        parts = [str(x).strip() for x in il if str(x).strip()]
        return ', '.join(parts) if parts else None
    if isinstance(il, str) and il.strip():
        return il.strip()
    return None

def build_cluster(trace: dict) -> str:
    """Assign shelf-filter cluster based on BSIP0 scope + NOVA."""
    scope = trace.get('bsip0_scope_class', '')
    nova = trace.get('nova_proxy', 0)
    note = trace.get('bsip1_note', '') or ''
    
    if note:
        return 'pasta-blends'
    if scope == 'frozen_herb_or_seasoning':
        return 'herbs-seasonings'
    if scope == 'frozen_legume_sold_as_vegetable':
        return 'legumes'
    if nova == 1:
        return 'plain-veg'
    if nova == 2:
        return 'mixes'
    return 'processed'

def build_positive_signals(trace: dict) -> list[str]:
    """Build 1-2 positive signals in Hebrew."""
    scope = trace.get('bsip0_scope_class', '')
    nova = trace.get('nova_proxy', 0)
    dims = trace.get('dimension_scores', {})
    signals = []
    
    if nova == 1:
        signals.append('ירק קפוא נקי — רכיב אחד, ללא תוספות')
        if 'frozen_legume' in scope:
            signals.append('קטנייה — מקור טבעי לחלבון צמחי וסיבים')
    elif nova == 2:
        signals.append('תערובת ירקות — מגוון רכיבים מהצומח')
    elif nova == 3:
        signals.append('ירק קפוא בתוספת רכיבים קולינריים')
    
    note = trace.get('bsip1_note', '') or ''
    if note:
        signals.append('רוב המוצר הוא ירקות — הפסטה/הרוטב הם מרכיב משני')
    
    return signals[:2]

def build_limiting_factors(trace: dict) -> list[str]:
    """Build 0-2 limiting factors."""
    nova = trace.get('nova_proxy', 0)
    factors = []
    if nova >= 3:
        factors.append('מכיל מרכיבים מעובדים — מייצבים, חומרי טעם או תוספי מזון')
    if nova == 2:
        factors.append('ירקות מעורבים עם תוספת מינורית — ציון נמוך מירק נקי')
    note = trace.get('bsip1_note', '') or ''
    if note:
        factors.append('מכיל פסטה — המרכיב הפחמימתי מוריד את ציון הירקות הטהור')
    return factors[:2]

def build_unknowns(trace: dict) -> list[str]:
    """Identify GENUINE data gaps from L1_observed_signals (the real panel source).
    Reading dimension_scores.nutrition_score (empty on all 53) falsely reported every
    field as missing — e.g. 'fiber not on label' when fiber was actually present."""
    l1 = trace.get('L1_observed_signals', {}) or {}
    gaps = []
    if l1.get('dietary_fiber_g') is None:
        gaps.append('ערך הסיבים התזונתיים לא צוין על התווית')
    if l1.get('fat_saturated_g') is None:
        gaps.append('ערך השומן הרווי לא היה זמין לניתוח')
    return gaps

def build_caveats(trace: dict) -> list[str]:
    """Build product-level caveats."""
    caveats = []
    note = trace.get('bsip1_note', '') or ''
    if note:
        caveats.append(note)
    return caveats

def build_bottom_line(trace: dict) -> str:
    """Bottom-line editorial."""
    grade = trace.get('grade_estimate', '')
    scope = trace.get('bsip0_scope_class', '')
    if grade == 'A' and 'frozen_legume' in scope:
        return 'קטניות קפואות ברמה הגבוהה ביותר — רכיב טבעי, ללא תוספות. מוצר בסיסי ומצוין.'
    if grade == 'A':
        return 'ירק קפוא טבעי ברמה הגבוהה ביותר — רכיב בודד, נקי מתוספות. מוצר בסיסי במטבח.'
    if grade == 'B':
        return 'ירק קפוא טוב עם תוספת קלה — מתאים לשימוש יומיומי, ציון טוב לקטגוריה.'
    if grade == 'C':
        return 'ירק קפוא מעובד עם תוספות — מתאים לתיבול ובישול, אך רחוק מלהיות ירק טבעי.'
    if grade == 'D':
        return 'מוצר ירק קפוא מעובד מאוד — ממרח/תבלין עם בסיס ירק, לא ירק שלם.'
    return ''

def build_insight_line(trace: dict) -> str:
    """One-liner insight for collapsed row.

    TASK-233C: the `NN/X` score-mechanic literal is banned in prose (the chip is its
    only home — score_presentation_v1 Rule 1 + insight_line_spec anti-redundancy). Lines
    carry the driver and the qualitative standing, never the numeral.
    """
    scope = trace.get('bsip0_scope_class', '')
    nova = trace.get('nova_proxy', 0)
    note = trace.get('bsip1_note', '') or ''

    if note:
        return ('תערובת ירקות ופסטה. '
                '75% מהמוצר הוא ירקות, הפסטה והרוטב הם מרכיב משני. '
                'הציון משקף את ההרכב המלא.')

    if nova == 1:
        if 'frozen_legume' in scope:
            return ('קטניה קפואה, רכיב בודד ללא תוספות. '
                    'ציון מלא לקטגוריה.')
        return ('ירק קפוא, רכיב בודד בלי תוספות. '
                'ציון מלא לקטגוריה.')

    if nova == 2:
        return ('תערובת ירקות, ציון טוב לקטגוריה. '
                'יורד במעט מירקות בודדים בשל התוספת.')

    if nova == 3:
        if scope == 'frozen_herb_or_seasoning':
            return ('תבלין/ירק קפוא מעובד. '
                    'מכיל מייצבים ותוספות להארכת חיי המדף, לא ירק טבעי.')
        return ('ירק קפוא בתוספת רכיבים קולינריים. '
                'מכיל שמן/מייצבים/תבלינים, לא ירק נקי.')

    return 'ירק קפוא — פרטי ההרכב מופיעים בכרטיס.'

# Confidence (state + label + tooltip + sub_reason) is derived by the shared core /
# confidence_annotation from the BSIP2 trace. The bespoke build_confidence* functions
# that once mapped medium->verified and shipped a non-canonical "official source"-style
# tooltip have been deleted (TASK-233B DA-005/DA-007).

def load_bsip1_images() -> dict:
    """Map canonical_product_id -> real scraped Shufersal image URL from BSIP1.
    The trace carries no image_url; the bsip1 file does (real per-product prefix,
    e.g. WAC20_, not the synthesized MNH68_ guess that 404s — TASK-233D)."""
    images = {}
    if not BSIP1_DIR.exists():
        return images
    for f in BSIP1_DIR.glob('bsip1_*.json'):
        try:
            d = json.loads(f.read_text(encoding='utf-8'))
        except Exception:
            continue
        pid = d.get('canonical_product_id')
        if pid:
            images[pid] = FC.select_image_url(d)
    return images

traces = load_traces()
bsip1_images = load_bsip1_images()
# Sort by score descending
traces.sort(key=lambda t: -(t.get('final_score_estimate') or -1))

products = []
for idx, t in enumerate(traces):
    ref = t.get('input_reference', {}) or {}
    pid_canon = ref.get('canonical_product_id') or t.get('canonical_product_id')
    score = t.get('final_score_estimate')
    # Grade is a pure function of the rounded score via the shared core, byte-matching
    # corpus.ts so disk grade == runtime grade (kills DA-009 drift; the engine S folds to A).
    score_int = FC.round_score(score)
    grade = FC.grade_from_score(score_int)
    name = ref.get('product_name_he', '')
    barcode = ref.get('barcode', '')
    # Real scraped Shufersal image URL from BSIP1; never synthesize a Cloudinary prefix (DA-006).
    image_url = bsip1_images.get(pid_canon)
    # Normalize barcode for ID
    prod_id = f'frozen-veg-{idx+1:02d}'
    
    nn = get_nutrition(t)
    cluster = build_cluster(t)
    positive = build_positive_signals(t)
    limiting = build_limiting_factors(t)
    unknowns = build_unknowns(t)
    caveats = build_caveats(t)
    insight = build_insight_line(t)
    bottom = build_bottom_line(t)
    # Core-derived confidence: medium != verified; verified requires full panel +
    # ingredients. Products with `unknowns` (missing fiber/sat-fat) derive to partial,
    # never "full data" — fixes DA-005/DA-006. Canonical tooltip; never the overclaim.
    conf_fields = FC.confidence_from_trace(t)

    prod = {
        'id': prod_id,
        'name': name,
        'imageUrl': image_url,
        'score': score_int,
        'grade': grade,
        'confidence': conf_fields['confidence'],
        'insightLine': insight,
        '_cluster': cluster,  # internal shelf-filter hint; stripped at emission below
        'expansion': {
            'nutrition': nn,
            'ingredients': get_ingredients(t),
            'confidenceLabel': conf_fields['confidence_label_he'],
            'servingNote': 'ל-100 גרם',
            'positiveSignals': positive,
            'limitingFactors': limiting,
            'unknowns': unknowns,
            'caveats': caveats,
            'bottomLine': bottom,
            'comparisonContext': None,
        },
        'retailer': 'shufersal',
        'barcode': barcode if barcode else None,
        'source_traceability_status': 'resolved',  # stripped at emission (DA-012)
        'confidence_label_he': conf_fields['confidence_label_he'],
        'confidence_tooltip_he': conf_fields['confidence_tooltip_he'],
        'confidence_sub_reason': conf_fields['confidence_sub_reason'],
    }
    products.append(prod)

# Build the meta cluster/retailer reports BEFORE the emission strip (which removes the
# internal helper fields). `_cluster` is load-bearing for the frozen-veg shelf filters,
# which read it off the RAW JSON at module init — so it is the ONE `_`-internal field kept
# on emission; source_traceability_status and other non-VM keys are stripped (DA-012).
_clusters_report = {}
for p in products:
    cl = p.get('_cluster')
    _clusters_report[cl] = _clusters_report.get(cl, 0) + 1
_retailer_count = sum(1 for p in products if p.get('retailer') == 'shufersal')

# Emission strip: VM allowlist + the load-bearing `_cluster`. Drops retailer,
# source_traceability_status, and any other non-VM key.
products = [FC.strip_non_vm_fields(p, keep={'_cluster'}) for p in products]

# Grade distribution
grade_dist = {}
for p in products:
    g = p['grade']
    grade_dist[g] = grade_dist.get(g, 0) + 1

output = {
    '_meta': {
        'generated': '2026-06-10T13:06:19.488400+00:00',
        'category': 'frozen-vegetables',
        'product_count': len(products),
        'scored_count': len([p for p in products if p['score'] is not None]),
        'schema': 'BariProductVM[]',
        'version': 'v1',
        'source_run_id': 'run_frozen_vegetables_001',
        'provenance': 'Shufersal scrape (scope-clean v2_1). 53 products scored. Ginger nutrition corrected (scraper dual-table bug fix).',
        'retailer_breakdown': {'shufersal': _retailer_count},
        'grade_distribution': grade_dist,
        'scope_note': 'ניתוח מדף שופרסל בלבד — 53 ירקות קפואים, לא סקר שוק ישראלי מלא.',
    },
    'products': products,
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Written {len(products)} products to {OUTPUT}')
print(f'Grade distribution: {grade_dist}')
print(f'Clusters:')
clusters = {}
for p in products:
    cl = p['_cluster']
    clusters[cl] = clusters.get(cl, 0) + 1
for c, n in sorted(clusters.items()):
    print(f'  {c}: {n}')
