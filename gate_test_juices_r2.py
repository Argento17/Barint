import sys, io
# Force UTF-8 output so Hebrew in flag.match / flag.note prints cleanly
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\Bari')
from integrations.clients.naturalness_gate import analyze

proposed_r2 = {
    # jc-019 — fix: the closer "לא בגלל פחות מתיקות, אלא בגלל הממתיק" is T1-closer; also fix mid "הסוכר הלבן הוחלף" framing + resolve closer in prose
    "jc-019 rowVerdict R2": "גרסת הדיאט: אותם 25% חמוציות מרוכזות כמו הגרסה הרגילה. ההבדל: הסוכר הלבן הוחלף בשילוב של פרוקטוז (סוכר פירות — עדיין סוכר), סוכרלוז (ממתיק ללא קלוריות) ומסמיך. הציון D נובע מאחוז הפרי הנמוך. הסוכר הכולל יורד בזכות הממתיק — הפרי האמיתי בבקבוק נשאר 25%.",

    # jc-026 — fix: closer needs to avoid X, לא Y; recast as plain declarative
    "jc-026 rowVerdict R2": "9% פרי בסך הכל — תפוח וענבים, שניהם מרוכזים. המים ראשון, הסוכר הלבן שני — הפרי שלישי ורביעי. צבע קרמל נוסף ליצירת מראה הענבים. עם 9.5 גרם סוכר ל-100 מ\"ל ורוב המתיקות מהסוכר הלבן, זה ציון E.",

    # jc-017 rowVerdict — also fix the MED mid-text T1: "נוסף, לא הגיע מהפרי"
    "jc-017 rowVerdict R2": "רכז חמוציות מרוכז ברבע הבקבוק; המים ראשון, הסוכר הלבן שלישי. מרבית הסוכר כאן נוסף — מהסוכר הלבן, לא מהפרי המרוכז. שם המוצר הוא \"מיץ חמוציות\"; מה שבפנים הוא משקה פרי בסיסי עם תוספת סוכר. הציון D הגבוה ביותר בקטגוריה — הרשימה הקצרה (שלושה רכיבים) היא הסיבה.",

    # jc-023 rowVerdict — also fix MED mid-text: "נמוך בגלל הממתיק, לא בגלל פחות מתיקות"
    "jc-023 rowVerdict R2": "11% אשכולית (6% מיץ + 5% רכיבי אשכולית), כולה מרוכזת. השאר: מים, שני סוגי סוכר, ממתיק ללא קלוריות (סוכרלוז), חומר משמר וחמישה מייצבים. הסוכר בכוס נמוך בזכות הממתיק — לא בגלל פחות פרי. עם 11% פרי ורשימת תוספי מזון ארוכה — זה ציון E.",
}

print("=== NATURALNESS GATE — ROUND 2 ===\n")
total_high = 0
total_med = 0
for label, text in proposed_r2.items():
    r = analyze(text)
    highs = r.high_flags
    meds = [f for f in r.flags if f.severity == 'MEDIUM']
    status = "HIGH" if highs else ("MED" if meds else "OK")
    if highs or meds:
        print(f"[{status}] {label}")
        for f in r.flags:
            print(f"  [{f.severity}]-{f.tell}: {f.match!r} — {f.note[:100]}")
    else:
        print(f"[{status}] {label}")
    total_high += len(highs)
    total_med += len(meds)

print(f"\nTotal HIGH flags: {total_high}")
print(f"Total MED flags: {total_med}")
