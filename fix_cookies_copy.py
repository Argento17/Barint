import json, sys, re, copy

sys.stdout.reconfigure(encoding='utf-8')

INPUT_FILE = r'C:\Bari\02_products\cookies_coffee\staging\task393_rescore\cookies_coffee_task393_staged.json'

with open(INPUT_FILE, encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

# Track changes
changes = []
original_data = copy.deepcopy(data)

def fix_product(barcode, field, new_value, reason):
    for p in products:
        if p['barcode'] == barcode:
            old = p.get(field, '')
            if old != new_value:
                p[field] = new_value
                changes.append({'barcode': barcode, 'field': field, 'old': old[:100], 'new': new_value[:100], 'reason': reason})
            return
    print(f'WARNING: barcode {barcode} not found')

# FIX 1: Grade mover 7290018893845 (D→E)
fix_product('7290018893845', 'rowVerdict',
    'פתי בר בטעם חמאה של צ\'וקטה הוא ביסקוויט ששמנו שמן חמניות — אין חמאה ברשימה. השומן הרווי נמוך מאוד לקטגוריה, ובכל זאת הציון נחת על E. הסיבה: גופרית דו-חמצנית ברשימה — תוסף מזון שנוי במחלוקת שמשפיע על הציון הכולל. הסוכר חוצה את הסף, וסירופ גלוקוז-פרוקטוז ברשימה. סיבי אפונה הם נגיעה חיובית שלא מספיקה לשנות את התמונה.',
    'grade-mover D→E: removed "מחזיק אותו ב-D", added E224 explanation')
fix_product('7290018893845', 'insightLine',
    'שמן חמניות בלבד — שומן רווי נמוך, אך גופרית דו-חמצנית ברשימה מורידה ל-E.',
    'grade-mover D→E: insightLine updated to E')

# FIX 2: Grade mover 313184 (D→E)
fix_product('313184', 'rowVerdict',
    'עוגיות גן חיות בצורות חיות הן ביסקוויט ילדים פשוט. הסוכר יושב בדיוק על סף התווית האדומה, והשומן הרווי נמוך לקטגוריה — שני אלה לא מספיקים. גופרית דו-חמצנית ברשימה — תוסף מזון שנוי במחלוקת — שקל את הכף ל-E. שמנים צמחיים כלליים ברשימה ללא פירוט.',
    'grade-mover D→E: removed D reference, added E224 explanation')
fix_product('313184', 'insightLine',
    'עוגיות ילדים — סוכר על הסף וגופרית דו-חמצנית ברשימה מביאים ל-E.',
    'grade-mover D→E: insightLine updated to E')
fix_product('313184', 'consumerTakeaway',
    'עוגיות ילדים עם סוכר על הסף וגופרית דו-חמצנית ברשימה — שני אלה ביחד מחזיקים אותן ב-E.',
    'grade-mover D→E: consumerTakeaway updated to E')

# FIX 6: Grade consistency — 7290013156006 (D): T1 contrastive closer + wrong grade C
fix_product('7290013156006', 'rowVerdict',
    'עוגיות המיני מרוקאיות של בבקה מגיעות ל-D. מרגרינה מופיעה לפני הביצים ברשימה. גם סוכר וגם שומן רווי חוצים את הסף — שני מגבילים פועלים יחד, ולכן D ולא פחות מזה.',
    'grade-consistency: removed "ל-D ולא ל-C" T1 contrastive closer naming wrong grade')

# FIX 7: Grade consistency — 7290118426615 (E): mentions C
fix_product('7290118426615', 'rowVerdict',
    'עוגיות המיני שוקולד האלה מגיעות ל-E. 56% קמח מלא ושוקולד מריר אמיתי — שני מאפיינים שלא נפוצים במדף הזה. הבעיה: סוכר גבוה שחוצה את הסף, גלוטן מוסף ורשימת חומרי עיבוד ארוכה שמגיעה ל-E על אף הבסיס הטוב.',
    'grade-consistency: removed "C היה דורש פחות סוכר" which named wrong grade')

# FIX 8: Grade consistency — 7296073529019 (E): mentions D
fix_product('7296073529019', 'rowVerdict',
    'קוקיס שוקולד מריר מגיע ל-E. שוקולד מריר 19% הוא יתרון אמיתי לקטגוריה. חמאה ומרגרינה מופיעות יחד — מקורות שומן שונים, האחד איכותי, השני תעשייתי. ה\'מריר\' מוסיף עומק בטעם; הסוכר הגבוה והשומן הרווי מכריעים את הציון.',
    'grade-consistency: removed "לא מחזיר את הציון ל-D" which named wrong grade')

# FIX 9: Panel-recitation fixes in consumerTakeaway
fix_product('7290119043149', 'consumerTakeaway',
    'עוגיות עם פרופיל נקי ושמן מוקשה כמגביל הבלעדי — שומן הרווי הוא הסיפור כאן, לא הסוכר.',
    'panel-recitation: removed "416 קלוריות ו-8 גרם שומן רווי ל-100 גרם"')

fix_product('80083764', 'consumerTakeaway',
    'עוגיית דגנים עם שיבולת שועל כרכיב ראשון — בסיס דגן שלם שנדיר בקטגוריה הזאת.',
    'panel-recitation: removed "8.7 גרם חלבון. 471 קלוריות ל-100 גרם"')

fix_product('8410376075915', 'consumerTakeaway',
    'ללא גלוטן לא מסמל פרופיל בריא — סוכר גבוה ועיבוד מוגבר הם הסיפור האמיתי.',
    'panel-recitation: removed "19 גרם סוכר"')

fix_product('7290018893036', 'consumerTakeaway',
    'שמן דקל, סירופ גלוקוז-פרוקטוז, ממתיק המלטודקסטרין — סוכר גבוה מאוד ועיבוד כבד. E.',
    'panel-recitation: removed "33 גרם סוכר"')

fix_product('7296073529026', 'consumerTakeaway',
    'קקאו לא שינה את הנוסחה — חמאה ומרגרינה יחד, וסוכר גבוה מאוד מכריעים את התמונה.',
    'panel-recitation: removed "39 גרם סוכר"')

fix_product('7622300356767', 'consumerTakeaway',
    'ביצים ואבקת חלב מלא בצד שמן דקל — נגיעות איכות שלא מספיקות מול סוכר גבוה.',
    'panel-recitation: removed "34 גרם סוכר במוצר"')

fix_product('8710502470028', 'consumerTakeaway',
    'חמאה ואגוזי מלך אמיתיים ברשימה — אבל שמן צמחי קודם ברשימה והסוכר גבוה מאוד.',
    'panel-recitation: removed "40 גרם סוכר"')

fix_product('7290101111986', 'consumerTakeaway',
    'ביסקוויט בקרם עם שמן קוקוס מוקשה — שומן רווי גבוה מאוד וסוכר גבוה מכריעים את הציון.',
    'panel-recitation: removed "25 גרם סוכר"')

# Verify no numeric/grade/score fields changed
numeric_fields = ['score', 'grade', 'rank', '_binding_cap', '_d4_score_penalty', '_nova_proxy']
for i, (orig_p, new_p) in enumerate(zip(original_data['products'], products)):
    for f in numeric_fields:
        if orig_p.get(f) != new_p.get(f):
            print(f'ERROR: numeric field changed at index {i}, barcode={new_p["barcode"]}, field={f}: {orig_p.get(f)} → {new_p.get(f)}')

# Save the file
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\n=== CHANGES MADE: {len(changes)} ===')
for c in changes:
    print(f'  [{c["barcode"]}] {c["field"]}: {c["reason"]}')
    print(f'    OLD: {c["old"]}')
    print(f'    NEW: {c["new"]}')
    print()

print('\n=== NATURALNESS GATE SCAN ===')
import sys
sys.path.insert(0, r'C:\\Bari')
try:
    from integrations.clients.naturalness_gate import analyze

    changed_strings = [c for c in changes]
    high_flag_count = 0
    for c in changes:
        text = c['new']
        r = analyze(text)
        if r.high_flags:
            high_flag_count += len(r.high_flags)
            print(f'  HIGH FLAGS [{c["barcode"]}] {c["field"]}:')
            for flag in r.high_flags:
                print(f'    {flag.tell} ({flag.severity}): {flag.match} — {flag.note}')

    print(f'\nTotal HIGH flags: {high_flag_count}')
    print('GATE: PASS' if high_flag_count == 0 else 'GATE: FAIL — iterate before returning')
except ImportError as e:
    print(f'naturalness_gate not importable: {e}')
    print('Skipping gate scan — manual review required.')
