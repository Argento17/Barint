import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

additional_fixes = {
    '46214930207': {
        'rowVerdict': (
            "עוגיות שוקולד צ'יפס עם ציפוי צבעוני מגיעות ל-E. "
            "ציפוי הסוכר הצבעוני מוסיף שישה צבעי מאכל שונים וחומר הזגה לפרופיל שכבר הכיל "
            "שמן דקל וסוכר גבוה. מסת קקאו וחמאת קקאו נוכחות ולא מספיקות."
        ),
        'insightLine': "ציפוי סוכר צבעוני עם שישה צבעי מאכל — סוכר גבוה מאוד.",
    },
    '7622201809188': {
        'rowVerdict': (
            "ביסקוויט מילקה מגיע ל-E. שמן דקל כרכיב שני. חמאת קקאו ועיסת קקאו — קקאו אמיתי. "
            "מתחלב פוליגליצרול מצטרף לסוכר גבוה ולשומן רווי גבוה. הציון לא משתנה."
        ),
        'insightLine': "שמן דקל וסוכר גבוה — חמאת קקאו ועיסת קקאו נוכחות.",
    },
    '7290115206333': {
        'rowVerdict': (
            "עוגיות מיני שוקוציפס מגיעות ל-E. שוקולד מריר 22% עם מוצקי קקאו גבוהים — "
            "גבוה יחסית לקטגוריה. שמן צמחי לא מפורט, חומרי תפיחה ומתחלבים. "
            "סוכר גבוה ושומן רווי גבוה. הקקאו האיכותי לא מוציא מ-E."
        ),
        # insightLine is clean — no gram
    },
}

changes = []
for p in products:
    bc = str(p.get('barcode', ''))
    if bc in additional_fixes:
        fixes = additional_fixes[bc]
        if 'rowVerdict' in fixes:
            p['rowVerdict'] = fixes['rowVerdict']
            changes.append(('rowVerdict', bc))
        if 'insightLine' in fixes:
            p['insightLine'] = fixes['insightLine']
            changes.append(('insightLine', bc))

print('Additional changes:')
for c in changes:
    print(f'  {c[0]}: [{c[1]}]')

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('File written.')
