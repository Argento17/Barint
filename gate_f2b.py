import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Bari')
from integrations.clients.naturalness_gate import analyze

drafts = {
    # jc-021 — recast closer to avoid "X, לא מיץ"; keep the opinionated take
    "jc-021": "ארבעים אחוז פרי — יותר מנקטר המנגו של ספרינג, אך עדיין: המים הם הרכיב הראשון, הסוכר הלבן הרביעי, והפרי כולו מרוכז. עם 9.4 גרם סוכר ל-100 מ\"ל — שווה לנקטר תות-בננה ולא נמוך — אחוז הפרי הגבוה לא מציל אותו: זהו הנמוך בציון מבין שלושת נקטרי ספרינג בסקירה. הפרי הנדיב יותר כאן עדיין יושב בתוך נקטר מים-וסוכר, ולכן הוא בתחתית השלישייה.",

    # jc-026 — recast closer to avoid "— לא במיץ ענבים"
    "jc-026": "9% פרי בסך הכל — תפוח וענבים, שניהם מרוכזים. המים ראשון, הסוכר הלבן שני, הפרי שלישי ורביעי, וצבע קרמל יוצר את מראה הענבים. כשהסוכר הלבן קודם לפרי וצבע מאכל אחראי על הגוון, מדובר במשקה בטעם ענבים שכמעט ואין בו ענבים. מי שקונה לפי השם על האריזה מקבל בעיקר מים, סוכר וצבע.",
}

print("=== F2-LIFT ROUND 2 ===\n")
th = tm = 0
for label, text in drafts.items():
    r = analyze(text)
    highs = r.high_flags
    meds = [f for f in r.flags if f.severity == 'MEDIUM']
    f2 = r.f2_signal
    status = "HIGH" if highs else ("MED" if meds else "OK")
    print(f"[{status}] {label}  (f2_risk={f2.get('f2_risk')}, verdict_marker={f2.get('has_verdict_marker')})")
    for f in r.flags:
        print(f"    [{f.severity}]-{f.tell}: {f.match!r}")
    th += len(highs); tm += len(meds)
print(f"\nTotal HIGH: {th} | MED: {tm}")
