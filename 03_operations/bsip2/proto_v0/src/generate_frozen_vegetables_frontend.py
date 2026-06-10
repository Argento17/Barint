"""Generate frozen_vegetables_frontend_v1.json from BSIP2 traces."""
import sys, io, json, pathlib, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = pathlib.Path(r'C:\Bari')
TRACES_DIR = BASE / '02_products' / 'frozen_vegetables' / 'bsip2_outputs' / 'run_frozen_vegetables_001' / 'products'
OUTPUT = BASE / 'bari-web' / 'src' / 'data' / 'comparisons' / 'frozen_vegetables_frontend_v1.json'

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

def get_nutrition(dim_scores: dict) -> dict:
    """Extract nutrition from dimension_scores sub-dict."""
    nut = dim_scores.get('nutrition_score', {})
    components = nut.get('nutrition_components', {})
    raw = nut.get('nutrition_raw', {})
    nn = {}
    # Try components first (calculated), fall back to raw
    for key, bkey in [('energy_kcal', 'energyKcal'), ('protein_g', 'protein'),
                       ('sugars_g', 'sugar'), ('fat_g', 'fat'),
                       ('fat_saturated_g', 'satFat'), ('fiber_g', 'fiber'),
                       ('sodium_mg', 'sodium')]:
        val = components.get(key) or raw.get(key)
        nn[bkey] = round(val, 1) if val is not None else None
    return nn

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
    """Identify data gaps."""
    dims = trace.get('dimension_scores', {})
    nut = dims.get('nutrition_score', {})
    raw = nut.get('nutrition_raw', {})
    gaps = []
    if raw.get('fiber_g') is None:
        gaps.append('ערך הסיבים התזונתיים לא צוין על התווית')
    if raw.get('fat_saturated_g') is None:
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
    """One-liner insight for collapsed row."""
    grade = trace.get('grade_estimate', '')
    score = trace.get('final_score_estimate', 0)
    scope = trace.get('bsip0_scope_class', '')
    nova = trace.get('nova_proxy', 0)
    note = trace.get('bsip1_note', '') or ''
    
    if note:
        return (f'תערובת ירקות ופסטה — {int(round(score))}/{grade}. '
                f'75% מהמוצר הוא ירקות, הפסטה והרוטב הם מרכיב משני. '
                f'הציון משקף את ההרכב המלא.')
    
    if nova == 1:
        if 'frozen_legume' in scope:
            return (f'קטניה קפואה טבעית — {int(round(score))}/{grade}. '
                    f'רכיב בודד ללא תוספות, ציון מלא לקטגוריה.')
        return (f'ירק קפוא טבעי — {int(round(score))}/{grade}. '
                f'רכיב בודד, בלי תוספות. ציון מלא לקטגוריה.')
    
    if nova == 2:
        return (f'תערובת ירקות — {int(round(score))}/{grade}. '
                f'ציון טוב לקטגוריה. יורד במעט מירקות בודדים בשל התוספת.')
    
    if nova == 3:
        if scope == 'frozen_herb_or_seasoning':
            return (f'תבלין/ירק קפוא מעובד — {int(round(score))}/{grade}. '
                    f'מכיל מייצבים ותוספות להארכת חיי המדף, לא ירק טבעי.')
        return (f'ירק קפוא בתוספת רכיבים קולינריים — {int(round(score))}/{grade}. '
                f'מכיל שמן/מייצבים/תבלינים, לא ירק נקי.')
    
    return f'ציון {int(round(score))}/{grade}'

def build_confidence(score: float | None, trace: dict) -> str:
    if score is None:
        return 'insufficient'
    conf = trace.get('confidence_band', 'medium')
    if conf == 'high':
        return 'verified'
    if conf == 'medium':
        return 'verified'
    return 'partial'

def build_confidence_label(conf: str) -> str:
    if conf == 'verified':
        return 'מבוסס על לוח התזונה'
    if conf == 'partial':
        return 'מבוסס על נתונים חלקיים'
    return 'מידע חלקי'

def build_confidence_tooltip(conf: str) -> str:
    # NOTE: ingredient lists are not captured for this category (ingredients=None),
    # and the source is a retailer scrape — never claim "official source" or that
    # all ingredient data was available. Copy must stay honest about what backs the score.
    if conf == 'verified':
        return 'הציון מבוסס על לוח התזונה של המוצר. רשימת רכיבים מלאה לא הייתה זמינה.'
    if conf == 'partial':
        return 'חלק מנתוני התזונה לא היו זמינים — הציון מבוסס על הנתונים שכן היו זמינים.'
    return 'חלק מנתוני התזונה או הרכיבים לא היו זמינים.'

def build_confidence_sub_reason(unknowns: list[str]) -> str | None:
    if unknowns:
        return 'partial_field'
    return None

traces = load_traces()
# Sort by score descending
traces.sort(key=lambda t: -(t.get('final_score_estimate') or -1))

products = []
for idx, t in enumerate(traces):
    ref = t.get('input_reference', {}) or {}
    score = t.get('final_score_estimate')
    grade = t.get('grade_estimate')
    score_int = int(round(score)) if score is not None else None
    name = ref.get('product_name_he', '')
    barcode = ref.get('barcode', '')
    image_url = f'https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/MNH68_Z_P_{barcode}_1.png'
    # Normalize barcode for ID
    prod_id = f'frozen-veg-{idx+1:02d}'
    
    nn = get_nutrition(t.get('dimension_scores', {}))
    cluster = build_cluster(t)
    positive = build_positive_signals(t)
    limiting = build_limiting_factors(t)
    unknowns = build_unknowns(t)
    caveats = build_caveats(t)
    insight = build_insight_line(t)
    bottom = build_bottom_line(t)
    conf = build_confidence(score, t)
    
    prod = {
        'id': prod_id,
        'name': name,
        'imageUrl': image_url,
        'score': score_int,
        'grade': grade,
        'confidence': conf,
        'insightLine': insight,
        '_cluster': cluster,
        'expansion': {
            'nutrition': nn,
            'ingredients': None,
            'confidenceLabel': build_confidence_label(conf),
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
        'source_traceability_status': 'resolved',
        'confidence_label_he': build_confidence_label(conf),
        'confidence_tooltip_he': build_confidence_tooltip(conf),
        'confidence_sub_reason': build_confidence_sub_reason(unknowns),
    }
    products.append(prod)

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
        'retailer_breakdown': {'shufersal': len([p for p in products if p['retailer'] == 'shufersal'])},
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
