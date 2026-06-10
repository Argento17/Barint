"""TASK-233C consumer-copy patch for FROZEN generators (snacks, cereals, bread).

These three categories ship from frozen generators (run_snackbars_007_headpin / bread),
so we do NOT re-run them. We surgically edit ONLY consumer-copy STRING fields in the
shipped frontend JSON, per the grade-literal ruling:

  Decision 1 — ban the `NN/X` grade-mechanic literal in prose (the chip is its only home).
  Decision 2 — remove cereals rescore-history narration unconditionally.

HARD CONSTRAINTS:
  * Touch ONLY consumer-copy strings (bottomLine, comparisonContext, rowVerdict,
    limitingFactors, positiveSignals, insightLine). Never score/grade/confidence/image.
  * Keep composition facts (nutrition gram values like "24.7 גרם סוכר" are NOT score
    mechanics and stay — the ruling says keep the composition facts).
  * Only strip the slashed `NN/X` token (digits + '/' + grade letter). Bare decimal
    nutrition values are left intact.
"""
import sys, io, json, re, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = pathlib.Path(r'C:\Bari')
COMP = BASE / 'bari-web' / 'src' / 'data' / 'comparisons'

sys.path.insert(0, str(BASE / 'integrations' / 'clients'))
import hebrew_readability as HR

# --- the slashed grade-mechanic literal: 1-3 digits / single grade letter (A-E or heb) ---
SLASH = re.compile(r'\d{1,3}\s*/\s*[A-Eא-ה]')
# bottomLine prefix form: "NN/X: rest"  ->  "rest"
PREFIX = re.compile(r'^\s*\d{1,3}\s*/\s*[A-Eא-ה]\s*:\s*')
# inline parenthetical reference form: " (NN/X)" -> ""
PAREN = re.compile(r'\s*\(\s*\d{1,3}\s*/\s*[A-Eא-ה]\s*\)')


def strip_slash_literal(s: str) -> str:
    """Remove the NN/X mechanic from prose, leaving the sentence intact."""
    if not s:
        return s
    out = PREFIX.sub('', s)          # drop a leading "NN/X: "
    out = PAREN.sub('', out)         # drop inline "(NN/X)" references
    # any residual bare "NN/X" not in the above forms -> drop the token, tidy spaces
    out = SLASH.sub('', out)
    out = re.sub(r'\s{2,}', ' ', out).strip()
    # tidy an orphaned leading punctuation left by a stripped prefix
    out = re.sub(r'^[—\-–:,.\s]+', '', out).strip()
    return out


# --- cereals: hand-authored re-write (rescore narration removed; grade letter == chip) ---
# Grades verified against live JSON: 5010029000061 = 75/B; the other two = 55/C.
CEREALS_REWRITE = {
    'bsip1_cereal_5010029000061':
        '95% חיטה, הרכב פשוט, 12 גרם חלבון ו-10 גרם סיבים ל-100 גרם, הגבוהים בקטגוריה. '
        'הפער מוויטביקס המוביל ניכר. '
        'עוצר ב-B כי מועשר בוויטמינים (לא ספונטני) ו-342 קלוריות ל-100 גרם.',
    'bsip1_cereal_5900020036407':
        'ליון: דגני שוקולד וקרמל עם 24.7 גרם סוכר ו-6.2 גרם שומן ל-100 גרם. '
        '8.5 גרם חלבון ו-6.5 גרם סיבים, אך גלוקוז גבוה וארכיטקטורת שומן בינונית עוצרים אותו ב-C.',
    'bsip1_cereal_5900020012814':
        'נסקוויק: חיטה מלאה ראשונה ברשימה, 8.9 גרם חלבון ו-8 גרם סיבים, אבל 24.7 גרם סוכר ל-100 גרם. '
        'עוצר ב-C כי הסוכר הגבוה מגביל את ההרכב.',
}

# consumer-copy string fields we are allowed to touch
TOP_FIELDS = ['insightLine', 'rowVerdict']
EXP_STR_FIELDS = ['bottomLine', 'comparisonContext', 'rowVerdict']
EXP_LIST_FIELDS = ['positiveSignals', 'limitingFactors']


def patch_file(fn, mode):
    path = COMP / fn
    d = json.loads(path.read_text(encoding='utf-8'))
    prods = d.get('products', [])
    changes = []

    for pr in prods:
        pid = pr.get('id') or pr.get('barcode')

        # cereals rowVerdict: full hand-authored rewrite for the 3 rescore-narration products
        if mode == 'cereals' and pid in CEREALS_REWRITE:
            old = pr.get('rowVerdict')
            new = CEREALS_REWRITE[pid]
            if old != new:
                pr['rowVerdict'] = new
                changes.append((pid, 'rowVerdict', old, new))
            continue  # these are fully re-authored; no mechanical pass needed

        # mechanical NN/X strip for snacks/bread (and any other cereals row with a slash literal)
        for f in TOP_FIELDS:
            v = pr.get(f)
            if isinstance(v, str) and SLASH.search(v):
                nv = strip_slash_literal(v)
                if nv != v:
                    pr[f] = nv
                    changes.append((pid, f, v, nv))
        ex = pr.get('expansion') or {}
        for f in EXP_STR_FIELDS:
            v = ex.get(f)
            if isinstance(v, str) and SLASH.search(v):
                nv = strip_slash_literal(v)
                if nv != v:
                    ex[f] = nv
                    changes.append((pid, f, v, nv))
        for f in EXP_LIST_FIELDS:
            lst = ex.get(f)
            if isinstance(lst, list):
                for i, v in enumerate(lst):
                    if isinstance(v, str) and SLASH.search(v):
                        nv = strip_slash_literal(v)
                        if nv != v:
                            lst[i] = nv
                            changes.append((pid, f, v, nv))

    path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    return changes


def report_clean(fn):
    d = json.loads((COMP / fn).read_text(encoding='utf-8'))
    prods = d.get('products', [])
    tot = clean = 0
    slash_hits = 0
    dec_only = []  # strings clean except for a bare nutrition decimal
    def chk(pid, f, v):
        nonlocal tot, clean, slash_hits
        if not isinstance(v, str) or not v:
            return
        tot += 1
        r = HR.analyze(v)
        if r.is_clean:
            clean += 1
        else:
            kinds = [(l.kind, l.term) for l in r.leaks if l.kind != 'english']
            if SLASH.search(v):
                slash_hits += 1
            else:
                dec_only.append((pid, f, kinds))
    for pr in prods:
        pid = pr.get('id') or pr.get('barcode')
        for f in TOP_FIELDS:
            chk(pid, f, pr.get(f))
        ex = pr.get('expansion') or {}
        for f in EXP_STR_FIELDS:
            chk(pid, f, ex.get(f))
        for f in EXP_LIST_FIELDS:
            for v in (ex.get(f) or []):
                chk(pid, f, v)
    return tot, clean, slash_hits, dec_only


if __name__ == '__main__':
    plan = [('snacks_frontend_v2.json', 'snacks'),
            ('cereals_frontend_v2.json', 'cereals'),
            ('bread_frontend_v2.json', 'bread')]
    for fn, mode in plan:
        changes = patch_file(fn, mode)
        tot, clean, slash_hits, dec_only = report_clean(fn)
        print(f'\n===== {fn} ({mode}) =====')
        print(f'  string fields changed: {len(changes)}')
        print(f'  is_clean: {clean}/{tot}  | residual NN/X (slash) hits: {slash_hits}')
        print(f'  residual non-slash (nutrition-decimal) gate hits: {len(dec_only)}')
        # show first 2 before/after for evidence
        for pid, f, old, new in changes[:2]:
            print(f'  [{pid}.{f}]')
            print(f'    BEFORE: {old}')
            print(f'    AFTER : {new}')
