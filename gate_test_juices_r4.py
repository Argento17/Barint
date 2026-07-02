import sys
sys.path.insert(0, r'C:\Bari')
from integrations.clients.naturalness_gate import analyze

r4_strings = {
    "jc-002 comparisonContext NEW": "בתוך שישת המוצרים עם ציון A — כולם מיצים סחוטים של פרי יחיד — הגרסה הזאת זהה להרכב של מיץ תפוזים סחוט ליטר: מיץ תפוזים בלי שום דבר נוסף. ההבדלים הקטנים בנתוני תזונה (43 קלוריות לעומת 47) הם טבע הפרי — הרכב שניהם זהה.",
    "jc-003 comparisonContext NEW": "אחד משלושה מיצי תפוזים סחוטים עם ציון A בסקירה. ההבדל בין השלושה הוא זן הפרי בלבד — כולם רכיב אחד, ללא ריכוז. בתוך קטגוריית המיצים כולה, ולנסיה מייצג את הפינה הנקייה ביותר שיש.",
    "jc-017 limitingFactor_0 NEW": "רק 25% חמוציות — מדובר במשקה פרי בסיסי",
    "jc-017 limitingFactor_1 NEW": "11.4 גרם סוכר ל-100 מ\"ל — רוב הסוכר הוא מהסוכר הלבן המוסף",
    "jc-017 limitingFactor_2 NEW": "עשוי מרכז",
    "jc-018 limitingFactor_2 NEW": "הסוכר הנמוך נשמר בעזרת ממתיק — הממתיק עושה את העבודה",
    "jc-019 comparisonContext NEW": "אחד ממעט המוצרים בסקירה ללא סוכר לבן. ציון D נובע בעיקר מ-25% פרי בלבד. הסוכר הנמוך (1.2 גרם) הוא יתרון מוגבל — מקורו בממתיק, והפרי בבקבוק נשאר 25%.",
    "jc-023 limitingFactor_2 NEW": "הממתיק מוריד את הסוכר — המתיקות בכוס נשמרת",
    "jc-024 limitingFactor_2 NEW": "המנגו עשוי מרכז",
    "jc-027 limitingFactor_1 NEW": "9.3 גרם סוכר ל-100 מ\"ל — רוב הסוכר הוא מהסוכר המוסף",
}

print("=== NATURALNESS GATE — ROUND 4 (limitingFactors + comparisonContexts) ===\n")
total_high = 0
total_med = 0
for label, text in r4_strings.items():
    r = analyze(text)
    highs = r.high_flags
    meds = [f for f in r.flags if f.severity == 'MEDIUM']
    if highs:
        print(f"[HIGH] {label}")
        for f in highs:
            print(f"  HIGH-{f.tell}: {f.match!r}")
        total_high += len(highs)
    elif meds:
        print(f"[MED]  {label}")
        for f in meds:
            print(f"  MED-{f.tell}: {f.match!r} — {f.note[:80]}")
        total_med += len(meds)
    else:
        print(f"[OK]   {label}")

print(f"\nTotal HIGH: {total_high}  |  Total MED: {total_med}")
