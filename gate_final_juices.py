import sys, json
sys.path.insert(0, r'C:\Bari')
from integrations.clients.naturalness_gate import analyze

with open(r'C:\Bari\bari-web\src\data\comparisons\juices_frontend_v3.json', encoding='utf-8') as f:
    data = json.load(f)

all_strings = {}
for p in data['products']:
    pid = p['id']
    if p.get('insightLine'):
        all_strings[f"{pid}.insightLine"] = p['insightLine']
    if p.get('rowVerdict'):
        all_strings[f"{pid}.rowVerdict"] = p['rowVerdict']
    exp = p.get('expansion', {})
    if exp:
        for i, s in enumerate(exp.get('positiveSignals', [])):
            all_strings[f"{pid}.pos[{i}]"] = s
        for i, s in enumerate(exp.get('limitingFactors', [])):
            all_strings[f"{pid}.lim[{i}]"] = s
        if exp.get('comparisonContext'):
            all_strings[f"{pid}.ctx"] = exp['comparisonContext']

# Also check .ts strings
ts_strings = {
    "hero.title": "קונים מיץ בסופרמרקט? הנה מה שאתם צריכים לדעת על מה שבבקבוק.",
    "prologue[0]": "המדף נראה אחיד: פרי על האריזה, צבעים טבעיים, שמות מרגיעים. בפועל, \"מיץ\", \"נקטר\" ו\"משקה פירות\" הם שלוש רמות שונות לגמרי של פרי, מים ותוספות.",
    "prologue[1]": "\"100% מיץ\" פירושו פרי בלבד — לא מים, לא סוכר, לא רכז. \"נקטר\" פירושו בין 25% ל-99% פרי, עם מים ולרוב גם סוכר לבן מוסף. \"משקה פירות\" יכול להכיל פחות מ-10% פרי — השאר מים, סוכר, רכז וחומרי טעם.",
    "prologue[2]": "גם מיץ 100% סחוט הוא לא ניטרלי: הוא מספק את כל הסוכר שהיה בפרי, בלי הסיבים שהיו מאיטים את ספיגתו. זה לא פגם — זו פשוט הגדרת הנוזל. הציון מבוסס על כמה פרי יש בפועל, האם נוסף סוכר, ורמת העיבוד.",
    "prologue[3]": "בארי שאלה: כמה פרי יש בבקבוק, ומה עוד יש שם?",
    "categoryNote": "הערת קטגוריה — גם מיץ 100% הוא סוכר נוזלי\n\nמיץ פרי סחוט 100% מכיל את כל הסוכר שהיה בפרי — ללא הסיבים שמאיטים את ספיגתו בפרי שלם. הסיבים נשארים בתפוז, לא עוברים לכוס. זה אופי הנוזל, לא פגם ביצרן. ציון Bari מבוסס על שלושה דברים: כמה פרי אמיתי בפועל, האם נוסף סוכר, ורמת העיבוד.\n\nטווח הפרי על המדף הזה: מ-100% פרי שלם (ציון A) ועד פחות מ-10% פרי עם חומרי טעם ורכז (ציון E). שלושת המינוחים — \"מיץ\", \"נקטר\", \"משקה פירות\" — יכולים לשבת על אותו מדף, באריזות בגודל זהה.",
}
all_strings.update(ts_strings)

total_high = 0
total_med = 0
high_list = []
med_list = []

for label, text in all_strings.items():
    r = analyze(text)
    highs = r.high_flags
    meds = [f for f in r.flags if f.severity == 'MEDIUM']
    if highs:
        high_list.append((label, highs))
        total_high += len(highs)
    if meds:
        med_list.append((label, meds))
        total_med += len(meds)

print(f"=== FINAL GATE SCAN: {len(all_strings)} strings total ===\n")
if high_list:
    print(f"HIGH FLAGS ({total_high}):")
    for label, flags in high_list:
        print(f"  [{label}]")
        for f in flags:
            print(f"    {f.tell}: {f.match!r}")
else:
    print("HIGH FLAGS: 0 — all strings HIGH-clean")

print()
if med_list:
    print(f"MED FLAGS ({total_med}):")
    for label, flags in med_list:
        print(f"  [{label}]")
        for f in flags:
            print(f"    {f.tell}: {f.match!r} — {f.note[:80]}")
else:
    print("MED FLAGS: 0")

print(f"\nSUMMARY: {len(all_strings)} strings, HIGH={total_high}, MED={total_med}")
