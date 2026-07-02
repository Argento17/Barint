import sys
sys.path.insert(0, r'C:\Bari')
from integrations.clients.naturalness_gate import analyze

proposed_r3 = {
    # jc-017 R3 — eliminate ", לא מהפרי המרוכז" by asserting only what is true
    "jc-017 rowVerdict R3": "רכז חמוציות מרוכז ברבע הבקבוק; המים ראשון, הסוכר הלבן שלישי. מרבית הסוכר כאן מגיע מהסוכר הלבן המוסף. שם המוצר הוא \"מיץ חמוציות\"; מה שבפנים הוא משקה פרי בסיסי עם תוספת סוכר. הציון D הגבוה ביותר בקטגוריה — הרשימה הקצרה (שלושה רכיבים) היא הסיבה.",

    # jc-023 R3 — eliminate the "לא בגלל" contrastive; state positively
    "jc-023 rowVerdict R3": "11% אשכולית (6% מיץ + 5% רכיבי אשכולית), כולה מרוכזת. השאר: מים, שני סוגי סוכר, ממתיק ללא קלוריות (סוכרלוז), חומר משמר וחמישה מייצבים. הממתיק מוריד את הסוכר בכוס — הפרי עצמו נשאר 11%. עם אחוז פרי נמוך ורשימת תוספי מזון ארוכה — זה ציון E.",
}

print("=== NATURALNESS GATE — ROUND 3 ===\n")
total_high = 0
total_med = 0
for label, text in proposed_r3.items():
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
