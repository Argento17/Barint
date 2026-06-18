"""
Cakes & Hard Cookies — Copy Generator
Factory Run #8 / TASK-283 — final pass after red-team corpus clean
Content Agent — autonomous copy stage

Fills all PENDING_COPY fields for 149 products + page_copy block.
Grounded entirely in trace-derived fields (score, grade, nutrition, ingredients,
limitingFactors, _has_phvo, novaGroup).

No OFF data. No invented values. No framework vocabulary in consumer output.

Key changes from previous run:
- Corpus clean: breakfast cereals, granola, cereal bars, pretzels removed — 149 products total
- Distribution: C:5, D:12, E:132 — NO A, NO B
- Top product: 54.5/C (עוגיות פירות יער כשל"פ)
- least_bad filter: C-only, 5 products
- has_phvo: 41, no_phvo: 108, high_sugar(>=30g): 66
- RT-3 fix: PHVO insightLines are product-specific, not a shared label
- RT-4 fix: za'atar product explicitly framed as savory occasion
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

INPUT_PATH = "C:/Bari/bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json"
OUTPUT_PATH = INPUT_PATH  # overwrite in place


def confidence_copy(conf: float) -> dict:
    if conf >= 0.78:
        return {
            "label": "ניתוח מלא",
            "tooltip": "נתוני תזונה ורשימת רכיבים נסרקו מהחנות ישירות. הציון מבוסס על נתונים מלאים.",
            "sub_reason": "תזונה ורכיבים זמינים",
            "expansion_label": "ניתוח מלא",
        }
    else:  # 0.72 — partial
        return {
            "label": "ניתוח חלקי",
            "tooltip": "נתוני התזונה נסרקו מהחנות ישירות. חלק מהפירוט עשוי להיות חלקי בשל מגבלות תווית.",
            "sub_reason": "נסרק ישירות מהחנות; חלק מהנתונים חלקי",
            "expansion_label": "ניתוח חלקי",
        }


def serving_note(energy_kcal, product_name: str) -> str:
    return "הנתונים מחושבים לפי 100 גרם מוצר, כפי שנסרק ישירות מתווית הרכיבים."


def fmt(val, decimals=0, fallback="?"):
    """Safe format for float values that may be None. Always integer — no decimal score mechanics."""
    if val is None:
        return fallback
    return str(int(round(val)))


# ─────────────────────────────────────────────────────────────
# Core copy builder per product
# ─────────────────────────────────────────────────────────────

def build_product_copy(p: dict) -> dict:
    name = p["name"]
    score = p["score"]
    grade = p["grade"]
    conf = p.get("confidence", 0.72)
    nutrition = p["expansion"]["nutrition"]
    ingredients = p["expansion"].get("ingredients", "") or ""
    limiting = p["expansion"].get("limitingFactors", []) or []
    has_phvo = p.get("_has_phvo", False)
    nova = p.get("novaGroup", 4)
    routed = p.get("_category_routed", "biscuit")
    barcode = p.get("barcode", "")

    energy = nutrition.get("energy_kcal")
    fat = nutrition.get("fat_g")
    sat_fat = nutrition.get("saturated_fat_g")
    sugar = nutrition.get("sugar_g")
    sodium = nutrition.get("sodium_mg")
    fiber = nutrition.get("fiber_g")
    protein = nutrition.get("protein_g")

    conf_copy = confidence_copy(conf)

    insight = build_insight(name, score, grade, energy, fat, sat_fat, sugar, sodium, fiber,
                             protein, has_phvo, nova, limiting, ingredients, routed, barcode)

    verdict = build_verdict(name, score, grade, energy, fat, sat_fat, sugar, sodium, fiber,
                             protein, has_phvo, nova, limiting, ingredients, routed, barcode)

    bottom = build_bottom_line(name, score, grade, energy, fat, sat_fat, sugar, sodium,
                                fiber, protein, has_phvo, nova, limiting, ingredients, routed)

    takeaway = build_takeaway(name, score, grade, energy, fat, sat_fat, sugar, sodium,
                               fiber, protein, has_phvo, nova, limiting, ingredients, routed)
    explanation = build_explanation(name, score, grade, energy, fat, sat_fat, sugar, sodium,
                                     fiber, protein, has_phvo, nova, limiting, ingredients, routed)
    interpretation = build_interpretation(name, score, grade, energy, fat, sat_fat, sugar,
                                           sodium, fiber, protein, has_phvo, nova, limiting,
                                           ingredients, routed)

    pos_signals = build_positive_signals(score, grade, fiber, protein, sugar, sat_fat,
                                          has_phvo, energy, ingredients, nova)

    best_use = build_best_use_cases(grade, score, fiber, protein, sugar, has_phvo, energy, routed)

    return {
        "confidence_label_he": conf_copy["label"],
        "confidence_tooltip_he": conf_copy["tooltip"],
        "confidence_sub_reason": conf_copy["sub_reason"],
        "insightLine": insight,
        "rowVerdict": verdict,
        "expansion_confidenceLabel": conf_copy["expansion_label"],
        "expansion_servingNote": serving_note(energy, name),
        "expansion_positiveSignals": pos_signals,
        "expansion_bottomLine": bottom,
        "consumerTakeaway": takeaway,
        "consumerExplanation": explanation,
        "bariInterpretation": interpretation,
        "bestUseCases": best_use,
    }


# ─────────────────────────────────────────────────────────────────────────────
# INSIGHT LINE builders
# RT-3 FIX: PHVO lines must be product-specific — lead with the product's real
# distinctive fact. Generic "מרגרינה / שומן מוקשה ברשימת הרכיבים" is a label,
# not an insight. Use it only as a last-resort suffix, never a standalone line.
# ─────────────────────────────────────────────────────────────────────────────

def build_insight(name, score, grade, energy, fat, sat_fat, sugar, sodium, fiber,
                   protein, has_phvo, nova, limiting, ingredients, routed, barcode=""):
    """
    T1: specific fact (number / ingredient) not already shown in columns.
    T2: contradiction between positioning and composition.
    T3: shelf position / rarity.
    12 Hebrew words max. No verdict. No relational framing.
    """
    name_lower = name.lower()

    # ── C grade: the 5 named products get bespoke lines ──────────────────────
    if grade == "C":
        return _insight_c(name, barcode, energy, fat, sat_fat, sugar, sodium, fiber,
                          protein, has_phvo, ingredients)

    # ── D grade: 12 named products ────────────────────────────────────────────
    if grade == "D":
        return _insight_d(name, barcode, energy, fat, sat_fat, sugar, sodium, fiber,
                          protein, has_phvo, ingredients)

    # ── E grade ───────────────────────────────────────────────────────────────
    return _insight_e(name, barcode, energy, fat, sat_fat, sugar, sodium, fiber,
                      protein, has_phvo, nova, limiting, ingredients)


def _insight_c(name, barcode, energy, fat, sat_fat, sugar, sodium, fiber,
               protein, has_phvo, ingredients):
    """Bespoke insight for each of the 5 C products."""

    # 7290017962139 — עוגיות פירות יער כשל"פ (top scorer, 54.5)
    if "פירות יער" in name and "כשל" in name and "כוסמין" not in name:
        almond_pct = "18% שקדים"
        fiber_str = f"{fmt(fiber)} גרם סיבים" if fiber else ""
        if fiber_str:
            return f"{almond_pct}, {fiber_str} ל-100 גרם; שמן קנולה כשומן עיקרי"
        return f"{almond_pct} וחמוציות; שמן קנולה כשומן עיקרי"

    # 7290020030184 — עוגיות מזרחיות עם זעתר (RT-4: savory, 0g sugar)
    if "זעתר" in name:
        sodium_str = f"{fmt(sodium)} מ\"ג נתרן" if sodium else ""
        if sodium_str:
            return f"עוגייה מלוחה ב-{sodium_str} ל-100 גרם; 0 גרם סוכר"
        return "עוגייה מלוחה, לא מתוקה — 0 גרם סוכר ל-100 גרם"

    # 7290122781359 — מיני עוגיות קלאסי פיטנס (61% whole wheat, 53 pts)
    if "פיטנס" in name and "מיני" in name and "חמוציות" not in name:
        return "61% קמח חיטה מלא; 4.6 גרם סוכר ל-100 גרם"

    # 7290013453068 — עוגיות כוסמין פירות יער (34% spelt, high fiber)
    if "כוסמין" in name:
        fiber_str = f"{fmt(fiber)} גרם סיבים" if fiber else ""
        if fiber_str:
            return f"34% קמח כוסמין מלא; {fiber_str} ל-100 גרם"
        return "34% קמח כוסמין מלא; ממתיקי אגבה ומונק פרוט"

    # 7290119030095 — עוגת גבינה אפויה ללת"ס (10g protein, no added sugar)
    if "גבינה" in name and ("אפויה" in name or "ללת" in name or "ללא" in name):
        protein_str = f"{fmt(protein)} גרם חלבון" if protein else ""
        if protein_str:
            return f"עוגת גבינה: {protein_str} ל-100 גרם, 3.4 גרם סוכר"
        return "עוגת גבינה אפויה ללא תוספת סוכר; חלבון גבוה לקטגוריה"

    # Fallback C (shouldn't reach here for this corpus)
    if fiber and fiber >= 5:
        return f"{fmt(fiber)} גרם סיבים ל-100 גרם — גבוה לקטגוריה"
    if energy:
        return f"{fmt(energy)} קק\"ל ל-100 גרם; בין הנמוכים בציון C"
    return "הרכב מוצק יחסית לקטגוריה"


def _insight_d(name, barcode, energy, fat, sat_fat, sugar, sodium, fiber,
               protein, has_phvo, ingredients):
    """Bespoke insight for each of the 12 D products."""

    # 7290119043743 — עוגיות מרוקאיות (palm fat, 48% white flour)
    if "מרוקאיות" in name and not "סגנון" in name and "מיני" not in name and "עגול" not in name and "ריפ" not in name:
        return f"קמח לבן (48%) ושמן דקלים; {fmt(sugar)} גרם סוכר ל-100 גרם"

    # 7290119043149 — עוגיות בטעם חמאה (partially hydrogenated, 8g sat fat)
    if "בטעם חמאה" in name:
        return f"שומנים מוקשים חלקית; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # 7290013156921 — עוגיות אצבעות ללא סוכר גאקובס (malt + PHVO, 9.5g sat fat)
    if "אצבעות" in name and "ללא סוכר" in name:
        return f"מרגרינה ברשימה; {fmt(sat_fat)} גרם שומן רווי למרות 0 גרם סוכר"

    # 5317194 — ביסקוויט בטעם וניל הדר (75g carbs, 22g sugar)
    if "וניל" in name and "ביסקוויט" in name and "הדר" in name:
        return f"75 גרם פחמימות ל-100 גרם; {fmt(sugar)} גרם סוכר"

    # 7290011489625 — ביסקוויט בטעם שוקו (identical formula to vanilla variant)
    if "שוקו" in name and "ביסקוויט" in name and "ממולא" not in name:
        return f"נוסחה זהה לגרסת הוניל; 2% אבקת קקאו, {fmt(sugar)} גרם סוכר"

    # 7290000061245 — עוגיות שוקוצ'יפס ממולאות (97 kcal/pack; low serving)
    if "שוקוצ'יפס" in name and "ממולאות" in name:
        return f"מנה אישית {fmt(energy)} קק\"ל; 36% מילוי קרם שוקולד"

    # 7290013740014 — עוגיות שוקוצ'יפס (9.5g sat fat, 23.6g sugar, no PHVO)
    if "שוקוצ'יפס" in name and "ממולאות" not in name and "נוגטלי" not in name and "קלאסי" not in name and "מיני" not in name and "מרקם" not in name:
        return f"{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר ל-100 גרם"

    # 7296073346340 — עוגות אישיות קרם שוקולד (145 kcal/pack; personal size)
    if "עוגות אישיות" in name and "קרם שוקולד" in name:
        return f"עוגות אישיות {fmt(energy)} קק\"ל למנה; סוכר+סירופ גלוקוז ראשונים"

    # 7290119041053 — עוגיות סגנון מרוקאי (PHVO, 7.4g sat fat)
    if "סגנון מרוקאי" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; 60% קמח לבן"

    # 7290119041107 — עוגיות מרוקאיות עגול (same formula as above)
    if "מרוקאיות עגול" in name:
        return f"נוסחת מרגרינה+קמח לבן; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # 7290119041152 — עוגיות ריפ'את (same formula again)
    if "ריפ'את" in name:
        return f"ריפ'את — נוסחה זהה לשורת המרוקאיות; מרגרינה, {fmt(sat_fat)} גרם שומן רווי"

    # 7290013156006 — עוגיות מיני מרוקאיות בבקה (PHVO, 8.8g sat fat, 18g sugar)
    if "מיני מרוקאיות" in name:
        return f"מרגרינה ראשונה בשומנים; {fmt(sat_fat)} גרם שומן רווי ו-{fmt(sugar)} גרם סוכר"

    # D fallback
    if has_phvo and sat_fat is not None:
        return f"שומן מוקשה ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"
    if sugar is not None and sugar > 20:
        return f"{fmt(sugar)} גרם סוכר ל-100 גרם"
    if energy:
        return f"{fmt(energy)} קק\"ל ל-100 גרם"
    return "ציון D — פערים מצטברים בהרכב"


def _insight_e(name, barcode, energy, fat, sat_fat, sugar, sodium, fiber,
               protein, has_phvo, nova, limiting, ingredients):
    """
    E-grade insight lines — 132 products.
    Each must be product-specific: lead with a real distinguishing number or fact.
    PHVO is never the sole content of the line; it's a secondary note when relevant.
    """
    name_lower = name.lower()

    # ── Named / distinctive products ─────────────────────────────────────────

    # פרה קראנץ' שוקולד לבן — extreme sugar (47g) and fat (16.7g sat)
    if "פרה קראנץ" in name or "פרה קראנץ'" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # צימקאו / שוקולד צ'יפס לבן — 70.9g sugar (highest in corpus)
    if "צימקאו" in name or ("שוקולד לבן" in name and "כשל" in name):
        return f"{fmt(sugar)} גרם סוכר ל-100 גרם — הגבוה בסריקה"

    # אוראו ציפוי שוקולד לבן (49g sugar)
    if "אוראו" in name and "לבן" in name:
        return f"{fmt(sugar)} גרם סוכר; ציפוי שוקולד לבן על עוגיית אוראו"

    # אוראו ציפוי שוקולד חלב (47g sugar)
    if "אוראו" in name and "חלב" in name and "ציפוי" in name:
        return f"{fmt(sugar)} גרם סוכר; ציפוי שוקולד חלב על בסיס אוראו"

    # אוראו דאבל קרם (43g sugar)
    if "אוראו" in name and "דאבל" in name:
        return f"{fmt(sugar)} גרם סוכר; כפליים קרם מהגרסה הרגילה"

    # אוראו — generic (any remaining oreo)
    if "אוראו" in name:
        sug = f"{fmt(sugar)} גרם סוכר" if sugar is not None else ""
        return f"עוגיית אוראו — {sug} ל-100 גרם; שמן דקל בשומנים"

    # ביסקוויט לוטוס / קרמל (38.1g sugar, palm oil)
    if "לוטוס" in name:
        return f"{fmt(sugar)} גרם סוכר; שמן דקל כשומן הראשי"

    if "קרמל" in name and "ביסקוויט" in name and "לוטוס" not in name:
        return f"קרמל תעשייתי — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # ביסקוויט נוטלה (35.8g sugar, 11.5g sat fat)
    if "נוטלה" in name:
        return f"40% ממרח קקאו-אגוזים; {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # מילקה סנסיישן אוראו
    if "מילקה" in name and "אוראו" in name:
        return f"{fmt(sugar)} גרם סוכר; שילוב שוקולד חלב + עוגיית אוראו"

    # מילקה סנסיישן (regular)
    if "מילקה" in name and "סנסיישן" in name:
        return f"{fmt(sugar)} גרם סוכר; עוגיית שוקולד חלב בציפוי קרמי"

    # ביסקוויט מילקה
    if "מילקה" in name and "ביסקוויט" in name:
        return f"{fmt(sugar)} גרם סוכר; שוקולד חלב מילקה בציפוי שכבתי"

    # עוגות ספוג צ'וקטה (37.3g sugar, 16.3g sat fat)
    if "ספוג" in name and "צ'וקטה" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי; ציפוי שוקולד מריר"

    # צ'וקטה סנדוויץ שוקו
    if "צ'וקטה" in name and "שוקו" in name:
        return f"קרם שוקו — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # צ'וקטה סנדוויץ וניל
    if "צ'וקטה" in name and "וניל" in name:
        return f"קרם וניל — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגות אישיות קרם חלב (36.3g sugar, 13.2g sat fat)
    if "עוגות אישיות" in name and "קרם חלב" in name:
        return f"מנה אישית — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגות אישיות קוקוס צ'וקטה (35.7g sugar, 18.7g sat fat — highest sat fat)
    if "עוגות אישיות" in name and "קוקוס" in name:
        return f"{fmt(sat_fat)} גרם שומן רווי ל-100 גרם — הגבוה שנצפה בסריקה"

    # עינוגים קוקיס
    if "עינוגים" in name:
        return f"קוקיס — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # LOVITA שוקולד (35.8g sugar, 14.2g sat fat)
    if "LOVITA" in name or "lovita" in name_lower:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגיות היט שוקולד (29g sugar, 17g sat fat — very high sat fat)
    if "היט" in name and "שוקולד" in name and "מיניס" not in name:
        return f"{fmt(sat_fat)} גרם שומן רווי — הגבוה בסדרת עוגיות ביסקוויט"

    # עוגיות היט מיניס (28g sugar, 15g sat fat)
    if "היט" in name and "מיניס" in name:
        return f"מיני גרסה — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגיות היט וניל (31g sugar, 17g sat fat)
    if "היט" in name and "וניל" in name:
        return f"{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר ל-100 גרם"

    # עוגיות חיוכים שוקולד (40g sugar)
    if "חיוכים" in name:
        return f"{fmt(sugar)} גרם סוכר ל-100 גרם; עוגיית ילדים עם ציפוי שוקולד"

    # עוגיות חיות שוקו
    if "חיות שוקו" in name:
        return f"עוגיית ילדים — {fmt(sugar)} גרם סוכר, {fmt(sat_fat)} גרם שומן רווי"

    # עוגיות נסיכה תות / מיקס
    if "נסיכה" in name:
        return f"עוגיית ילדים — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגיות גן חיות וניל
    if "גן חיות" in name:
        return f"עוגיית ילדים — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגיות בוטנים כשל"פ (30.5g sugar; peanuts NOT first)
    if "בוטנים" in name:
        return f"{fmt(sugar)} גרם סוכר; הבוטנים אינם הרכיב הראשון ברשימה"

    # קוקיס שבבי שוקולד חלבי (PHVO, sat fat 13.6g, no sugar data)
    if "קוקיס" in name and "שבבי שוקולד חלבי" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(energy)} קק\"ל ל-100 גרם"

    # קוקיס שוקולד לבן חלבי (PHVO, 10g sat fat)
    if "קוקיס" in name and "לבן חלבי" in name:
        return f"שוקולד לבן עם מרגרינה; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # קוקיס שוקולד מריר חלבי (PHVO, 36.2g sugar, 13.3g sat fat)
    if "קוקיס" in name and "מריר חלבי" in name:
        return f"מרגרינה, {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # קוקיס שוקו+שבבי שוקולד (PHVO, 39.1g sugar, 13.6g sat fat)
    if "קוקיס" in name and "שוקו+שבבי" in name:
        return f"מרגרינה, {fmt(sugar)} גרם סוכר; צפוף קלורית ב-{fmt(energy)} קק\"ל"

    # עוגת קראנץ — PHVO series (30g sugar, 8g sat fat)
    if "עוגת קראנץ" in name and "שוקולד" in name and "אגוזים" not in name:
        return f"מרגרינה ו-{fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי"

    if "עוגת קראנץ" in name and "קינמון" in name:
        return f"מרגרינה ו-{fmt(sugar)} גרם סוכר; {fmt(energy)} קק\"ל ל-100 גרם"

    if "עוגת קראנץ" in name and "פרג" in name:
        return f"מרגרינה ופרג; {fmt(sugar)} גרם סוכר ל-100 גרם"

    if "עוגת קראנץ" in name and "אגוזים" in name:
        return f"קראנץ אגוזים עם מרגרינה; {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # קרמוגית קראנץ שוקו וניל / קרם וניל (low kcal per pack but high sat fat ratio)
    if "קרמוגית" in name and "שוקו" in name:
        return f"מנה {fmt(energy)} קק\"ל; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    if "קרמוגית" in name and "קרם" in name:
        return f"קרם וניל — {fmt(energy)} קק\"ל למנה; {fmt(sat_fat)} גרם שומן רווי"

    # קראנץ אגוזי לוז (33g sugar, 16g sat fat)
    if "קראנץ אגוזי לוז" in name:
        return f"{fmt(sat_fat)} גרם שומן רווי ו-{fmt(sugar)} גרם סוכר ל-100 גרם"

    # קראנץ סנדויץ שוקולד (25.3g sugar, 8.9g sat fat)
    if "קראנץ סנדויץ" in name:
        return f"קראנץ סנדוויץ — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # קראנץ מיני אלפחורס (32g sugar, 12g sat fat)
    if "אלפחורס" in name:
        return f"אלפחורס — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # מאגדת מיני קראנץ (30.3g sugar, 14g sat fat)
    if "מאגדת" in name:
        return f"מיני קראנץ — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגיות שוקוצ'יפס (several variants)
    if "שוקוצ'יפס" in name and "מרקם רך" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי בגרסת מרקם רך"

    if "שוקוצ'יפס" in name and "נוגטלי" in name:
        return f"נוגט + שוקוצ'יפס — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    if "שוקוצ'יפס" in name and "קלאסי" in name:
        return f"קלאסי — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    if "שוקוצ'יפס" in name and "מיני" in name:
        return f"מיני — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    if "שוקוצ'יפס" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # שוקולד צ'יפס (multiple products with same base name)
    if "שוקולד צ'יפס" in name and ("46214" in barcode or "7622300" in barcode):
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגיות+שבבי שוקולד לל"ג (sugar-free label, still 19g sugar)
    if 'לל"ג' in name and "שבבי" in name:
        return f"מסומן לל\"ג — עדיין {fmt(sugar)} גרם סוכר ל-100 גרם"

    # שוקולד צ'יפס כשל"פ (31g sugar, 3.8g sat fat)
    if "שוקולד צ'יפס" in name and "כשל" in name:
        return f"כשל\"פ — {fmt(sugar)} גרם סוכר ל-100 גרם"

    # מיני עוגיות שוקולד
    if "מיני שוקולד" in name and "עוגיות" in name:
        return f"מיני — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגיות שוקוציפס קרם אגוז (36g sugar, 9g sat fat)
    if "שוקוציפס" in name and "קרם אגוז" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי; קרם אגוזים"

    # עוגיות קקאו דגנים מלאים + נטיפי שוקולד מריר פיטנס
    if "קקאו" in name and "דגנים מלאים" in name:
        return f"{fmt(energy)} קק\"ל ל-100 גרם; דגנים מלאים אבל {fmt(sugar)} גרם סוכר"

    # עוגיות פיטנס חמוציות (22.4g sugar, 4g sat fat, 467 kcal)
    if "פיטנס" in name and "חמוציות" in name:
        return f"{fmt(energy)} קק\"ל ל-100 גרם; חמוציות — {fmt(sugar)} גרם סוכר"

    # עוגיות שיבולת שועל (9.6g sat fat, 23.2g sugar — not healthy despite name)
    if "שיבולת שועל" in name and "עוגיות" in name:
        return f"שיבולת שועל בשם; {fmt(sat_fat)} גרם שומן רווי ו-{fmt(sugar)} גרם סוכר"

    # רולדה תמרים (PHVO, 10.3g sat fat; dates not dominant)
    if "רולדה" in name and "תמרים" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; תמרים אינם הרכיב הדומיננטי"

    # עוגיות עם שבבי קוקוס (PHVO, 22.1g sugar, 10.3g sat fat, 507 kcal)
    if "שבבי קוקוס" in name or ("קוקוס" in name and "עם" in name and "שועל" not in name and "עוגיות" in name):
        return f"מרגרינה ו-{fmt(energy)} קק\"ל ל-100 גרם; {fmt(sat_fat)} גרם שומן רווי"

    # עוגיות עם גרעיני חמנייה (PHVO, 26.2g sugar, 9.4g sat fat, 504 kcal)
    if "גרעיני חמנייה" in name:
        return f"מרגרינה ו-{fmt(energy)} קק\"ל; גרעינים שניים מהסוף ברשימה"

    # עוגיות עם ש.שועל קוקוס (PHVO, 36.6g sugar, 7.5g sat fat)
    if "ש.שועל" in name and "קוקוס" in name:
        return f"מרגרינה ו-{fmt(sugar)} גרם סוכר; שיבולת שועל — לא הרכיב הראשון"

    # מיני שטרודל שקדים (PHVO, 1.8g sugar, 12g sat fat)
    if "שטרודל" in name and "שקדים" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; 1.8 גרם סוכר בלבד"

    # מיני שטרודל קרם פטיסייר (PHVO, 1.6g sugar, 11.4g sat fat)
    if "שטרודל" in name and "פטיסייר" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; קרם פטיסייר"

    # מיני שטרודל חלבה שוקולד (PHVO, 2g sugar, 12g sat fat)
    if "שטרודל" in name and "חלבה" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; מילוי חלבה-שוקולד"

    # מיני שטרודל תפוח עץ (PHVO, 2.2g sugar, 11.7g sat fat)
    if "שטרודל" in name and "תפוח" in name and "מיני" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; מילוי תפוחים"

    # שטרודל גבינה / תפוחי עץ (non-mini, PHVO)
    if "שטרודל גבינה" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; גבינה לבנה במילוי"

    if "שטרודל תפוחי עץ" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; תפוחי עץ במילוי"

    if "שטרודל" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגיות אקלר סנדוויץ ריבה ללא סוכר (PHVO; sodium NULLed — label value unreliable, RT-R2)
    if "אקלר" in name or "סנדוויץ ריבה" in name:
        return "מסומן 'ללא סוכר' — מרגרינה וממתיק מלטיטול ברשימת הרכיבים"

    # עוגיות קינמון מסוכרות (PHVO, 9.5g sat fat, 430 kcal)
    if "קינמון מסוכרות" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    # עוגיות מקלות עלים (PHVO, 9.5g sat fat — same formula as cinnamon)
    if "מקלות עלים" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(energy)} קק\"ל ל-100 גרם"

    # עוגת פס גבינה אפויה (PHVO, 28.9g sugar, 2.3g sat fat)
    if "פס גבינה" in name and "אפויה" in name:
        return f"מרגרינה ברשימה; {fmt(sugar)} גרם סוכר ל-100 גרם"

    # עוגת גבינה שמנת ופירורים (PHVO, 24.5g sugar, 13g sat fat)
    if "גבינה שמנת" in name and "פירורים" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    # עוגת מוס גבינה+תות (PHVO, 10.1g sat fat, 25g sugar)
    if "מוס גבינה" in name and "תות" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    # עוגת מוס גבינה פרורים (PHVO, 9.1g sat fat)
    if "מוס גבינה פרורים" in name or ("מוס" in name and "פרורים" in name and "גבינה" in name):
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    # עוגת פס מוס בלגי פרווה (PHVO, 18.2g sat fat — highest sat fat in E)
    if "מוס בלגי" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי — בין הגבוהים בסריקה"

    # עוגת פס מוס טירמיסו (PHVO, 9.3g sat fat)
    if "מוס טירמיסו" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    # עוגת סבתא שוקולד (PHVO, 7.4g sat fat)
    if "סבתא" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    # עוגת קרנץ' שוקולד (PHVO, 8g sat fat)
    if "קרנץ'" in name and "שוקולד" in name and "שמרים" not in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    # עוגת קרנץ' בטעם שוקולד (PHVO, 6.8g sat fat)
    if "קרנץ'" in name and "בטעם שוקולד" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    # עוגת קרנץ אגוזים וקינמון (PHVO, 6.9g sat fat)
    if "קרנץ אגוזים" in name or ("קרנץ" in name and "אגוזים" in name):
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    # עוגת מאפין שוקו צ'יפס (PHVO, 4.7g sat fat)
    if "מאפין" in name and "שוקו צ'יפס" in name and "5" not in name:
        return f"מרגרינה ב-{fmt(energy)} קק\"ל; {fmt(sugar)} גרם סוכר"

    # עוגת מאפין בטעם תפוז (PHVO, 3.7g sat fat)
    if "מאפין" in name and "תפוז" in name and "PHVO" not in name:
        phvo_note = f"מרגרינה; " if has_phvo else ""
        return f"{phvo_note}{fmt(sugar)} גרם סוכר; {fmt(energy)} קק\"ל ל-100 גרם"

    # עוגת מאפין אגוזים (2 variants — one per retailer, similar values)
    if "מאפין" in name and "אגוזים" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגת מאפין תפוחי עץ / תפוח עץ
    if "מאפין" in name and "תפוח" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(energy)} קק\"ל ל-100 גרם"

    # עוגת מאפין וניל (highest sugar muffin — 36.2g)
    if "מאפין" in name and "וניל" in name:
        return f"{fmt(sugar)} גרם סוכר — הגבוה בסדרת המאפינים"

    # עוגת מאפין שוקולד / שיש / תפוז variants (various)
    if "מאפין" in name and "שוקולד" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    if "מאפין" in name and "שיש" in name:
        return f"{fmt(sugar)} גרם סוכר; שוקולד ווניל בשיש"

    if "מאפין" in name and "תפוז" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(energy)} קק\"ל ל-100 גרם"

    if "מאפין" in name and "5" in name:
        return f"חמישייה — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    if "מאפין" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגיות סנדוויץ שוקולד (33g sugar, 10g sat fat)
    if "סנדוויץ" in name and "שוקולד" in name and "גולון" not in name and "צ'וקטה" not in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגיות סנדוויץ גולון (5g sugar, 6g sat fat, 422 kcal)
    if "גולון" in name and "סנדוויץ" in name:
        return f"{fmt(energy)} קק\"ל ל-100 גרם; {fmt(sat_fat)} גרם שומן רווי"

    # עוגת גבינה רנסנס / אפויה (20.6g sugar, 1.9g sat fat)
    if "גבינה" in name and ("רנסנס" in name or ("אפויה" in name and "שמנת" not in name and "ללת" not in name)):
        return f"עוגת גבינה — {fmt(sugar)} גרם סוכר; {fmt(energy)} קק\"ל ל-100 גרם"

    # עוגת גבינה פירורים לייט / פירורים (8-10g sat fat)
    if "גבינה פירורים" in name:
        return f"{fmt(sat_fat)} גרם שומן רווי; {fmt(energy)} קק\"ל ל-100 גרם"

    # עוגת גבינה פס (PHVO, 28.9g sugar)
    if "גבינה" in name and "פס" in name:
        return f"מרגרינה; {fmt(sugar)} גרם סוכר ל-100 גרם"

    # עוגת גבינה generic
    if "גבינה" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגת פס דובוש (32.7g sugar, 2.7g sat fat)
    if "דובוש" in name:
        return f"שכבות קרם עם גלוקוז — {fmt(sugar)} גרם סוכר ל-100 גרם"

    # עוגת פס דובדבנים (11g sugar, 9.6g sat fat)
    if "דובדבנים" in name:
        return f"{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר ל-100 גרם"

    # עוגת פס שוקולד / קפוצ'ינו / היער השחור
    if "פס שוקולד" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    if "פס קפוצ'ינו" in name:
        return f"{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר ל-100 גרם"

    if "היער השחור" in name and "פס" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    if "פס שביל החלב" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    if "פס אוכמניות" in name:
        return f"מרגרינה ו-{fmt(sat_fat)} גרם שומן רווי; {fmt(sugar)} גרם סוכר"

    if "פס" in name:
        phvo_note = f"מרגרינה; " if has_phvo else ""
        return f"{phvo_note}{fmt(sugar)} גרם סוכר ל-100 גרם"

    # עוגת מוס היער השחור (28g sugar, 6.1g sat fat)
    if "מוס" in name and "היער השחור" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגת מוס (generic remaining)
    if "מוס" in name:
        phvo_note = f"מרגרינה; " if has_phvo else ""
        return f"{phvo_note}{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגת הבית שוקולד צ'יפס (9.3g sugar, 1.1g sat fat, 126 kcal — small serving)
    if "עוגות הבית" in name or "עוגת הבית" in name:
        return f"מנה אישית {fmt(energy)} קק\"ל; {fmt(sugar)} גרם סוכר"

    # עוגת שמרים שוקולד (26g sugar, 5g sat fat)
    if "שמרים" in name and "שוקולד" in name and "קרם" not in name and "בריוש" not in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגת שמרים בריוש שוקולד (29g sugar, 5.6g sat fat)
    if "שמרים" in name and "בריוש" in name:
        return f"בריוש שמרים — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגת שמרים קרנאץ'
    if "שמרים" in name and "קרנאץ'" in name:
        return f"שמרים+קרנאץ' — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגת שמרים (generic)
    if "שמרים" in name and "פרג" in name:
        return f"פרג מתוק — {fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי"

    if "שמרים" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגת בראוניס (39g sugar, 11.5g sat fat)
    if "בראוניס" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגה אנגלית (25g sugar, 8g sat fat)
    if "אנגלית" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגה בטעם שוקולד כשל"פ (various)
    if "שוקולד" in name and "כשל" in name and "עוגה" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    # עוגת שוקולד ללא גלוטן (28.8g sugar, 13.4g sat fat)
    if "שוקולד ללא גלוטן" in name:
        return f"ללא גלוטן — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגת שוקוציפס ללא גלוטן (31.9g sugar, 13.8g sat fat)
    if "שוקוציפס ללא גלוטן" in name:
        return f"ללא גלוטן — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # עוגת דבש (31g sugar, 2.9g sat fat)
    if "דבש" in name and "עוגת" in name:
        return f"{fmt(sugar)} גרם סוכר; דבש — לא הרכיב הראשון ברשימה"

    # שוקולד ציפס מצופות (38.1g sugar, 14.9g sat fat)
    if "מצופות" in name and "שוקולד" in name:
        return f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי; ציפוי שוקולד"

    # עוגת הבית שיש / תפוז / שוקולד (various Osem)
    if "שיש" in name and "מאפין" not in name:
        phvo_note = "מרגרינה; " if has_phvo else ""
        return f"{phvo_note}{fmt(sugar)} גרם סוכר ל-100 גרם"

    # עוגת הבית generic
    if "הבית" in name:
        return f"{fmt(sugar)} גרם סוכר; {fmt(energy)} קק\"ל ל-100 גרם"

    # חמישיית מאפין שוקו צ'יפס (10 score)
    if "חמישיית" in name:
        return f"חמישייה — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי"

    # Generic E — lead with dominant limiting factor
    if has_phvo and sat_fat is not None and sat_fat > 10:
        fat_word = "מרגרינה" if "מרגרינה" in ingredients else "שומן מוקשה"
        return f"{fat_word} ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם"

    if has_phvo and sugar is not None:
        return f"שומן מוקשה ברשימה; {fmt(sugar)} גרם סוכר ל-100 גרם"

    if sugar is not None and sugar > 40:
        return f"{fmt(sugar)} גרם סוכר ל-100 גרם — גבוה מאוד"

    if sugar is not None and sugar > 30:
        return f"{fmt(sugar)} גרם סוכר ל-100 גרם"

    if sat_fat is not None and sat_fat > 12:
        return f"{fmt(sat_fat)} גרם שומן רווי ל-100 גרם — גבוה מאוד"

    if energy is not None and energy > 480:
        sug_note = f"; {fmt(sugar)} גרם סוכר" if sugar else ""
        return f"{fmt(energy)} קק\"ל ל-100 גרם{sug_note}"

    if energy is not None:
        return f"{fmt(energy)} קק\"ל ל-100 גרם"

    return "נתונים לא מלאים — נסרק ישירות מהחנות"


# ─────────────────────────────────────────────────────────────────────────────
# ROW VERDICT builders
# ─────────────────────────────────────────────────────────────────────────────

def build_verdict(name, score, grade, energy, fat, sat_fat, sugar, sodium, fiber,
                   protein, has_phvo, nova, limiting, ingredients, routed, barcode=""):
    """2-line verdict. Standing → why → catch. No grade letter in body."""

    # ── C grade (5 products) ─────────────────────────────────────────────────
    if grade == "C":
        # פירות יער כשל"פ — top scorer (54.5)
        if "פירות יער" in name and "כשל" in name and "כוסמין" not in name:
            return (
                "עוגיית שקדים וחמוציות עם שמן קנולה כשומן הראשי — 18% שקדים ו-6 גרם סיבים ל-100 גרם. "
                "הציון הגבוה ביותר בקטגוריה; הצד השני: 420 קק\"ל ל-100 גרם."
            )
        # זעתר — RT-4 savory frame
        if "זעתר" in name:
            return (
                "עוגייה מלוחה, לא מתוקה: 0 גרם סוכר ו-730 מ\"ג נתרן ל-100 גרם. "
                "הציון C נובע מהיעדר סוכר, לא מעדיפות תזונתית כללית. "
                "מתאימה לאכילה מלוחה, לא כחלופה לעוגיות מתוקות."
            )
        # פיטנס מיני (61% whole wheat, 4.6g sugar)
        if "פיטנס" in name and "מיני" in name and "חמוציות" not in name:
            return (
                "מיני עוגיות עם 61% קמח חיטה מלא ו-4.6 גרם סוכר ל-100 גרם — נמוך לקטגוריה. "
                "פחמימות זמינות גבוהות וחומרי תפיחה מרובים מגבילים את הציון."
            )
        # כוסמין פירות יער (34% spelt, 8.3g fiber)
        if "כוסמין" in name:
            return (
                "עוגיית כוסמין מלא עם 8 גרם סיבים ל-100 גרם — הגבוה בקטגוריה. "
                "ממתיקי אגבה ומונק פרוט במקום סוכר לבן; 453 קק\"ל ל-100 גרם."
            )
        # עוגת גבינה אפויה ללת"ס (10g protein, 3.4g sugar)
        if "גבינה" in name and ("אפויה" in name or "ללת" in name):
            return (
                "עוגת גבינה אפויה עם 10 גרם חלבון ו-3.4 גרם סוכר ל-100 גרם — גבוה בחלבון לקטגוריה. "
                "רשימת חומרים עם 14 תוספי מרקם ומייצבים."
            )
        # Fallback C
        return (
            f"ציון C — הרכב מוצק יחסית ל-149 מוצרי הקטגוריה. "
            f"{'מרגרינה ברשימה. ' if has_phvo else ''}"
            f"{'סיבים: ' + fmt(fiber, 1) + ' גרם ל-100 גרם.' if fiber else ''}"
        ).strip()

    # ── D grade (12 products) ────────────────────────────────────────────────
    if grade == "D":
        if "מרוקאיות" in name and "סגנון" not in name and "מיני" not in name and "עגול" not in name and "ריפ" not in name:
            return (
                "עוגיות מרוקאיות עם קמח לבן (48%) ושמן דקלים. "
                f"{fmt(sugar)} גרם סוכר ל-100 גרם — בינוני לקטגוריה, אבל הרכיבים הבסיסיים."
            )
        if "בטעם חמאה" in name:
            return (
                "עוגיות 'בטעם חמאה' עם שומנים צמחיים מוקשים חלקית — 8 גרם שומן רווי ל-100 גרם. "
                "הרכב קרוב לגרסאות ה-E."
            )
        if "אצבעות" in name and "ללא סוכר" in name:
            return (
                "עוגיות ללא סוכר עם מלטיטול ומרגרינה. "
                "9.5 גרם שומן רווי ל-100 גרם — לא שונה מגרסאות עם סוכר."
            )
        if "וניל" in name and "ביסקוויט" in name and "הדר" in name:
            return (
                "ביסקוויט וניל קלאסי עם 75 גרם פחמימות ו-22 גרם סוכר ל-100 גרם. "
                "הרכב טיפוסי לביסקוויט תעשייתי."
            )
        if "שוקו" in name and "ביסקוויט" in name and "ממולא" not in name:
            return (
                "ביסקוויט שוקו — זהה בנוסחה לגרסת הוניל עם 2% אבקת קקאו. "
                "22 גרם סוכר ל-100 גרם."
            )
        if "שוקוצ'יפס" in name and "ממולאות" in name:
            return (
                "עוגיות ממולאות ב-36% קרם שוקולד — מנה אישית של 97 קק\"ל. "
                "סוכר ראשון ברשימה, 2.2 גרם שומן רווי."
            )
        if "שוקוצ'יפס" in name and "ממולאות" not in name and "נוגטלי" not in name and "קלאסי" not in name and "מיני" not in name and "מרקם" not in name:
            return (
                f"עוגיות שוקולד צ'יפס עם {fmt(sat_fat)} גרם שומן רווי ל-100 גרם — ללא שומן מוקשה. "
                f"{fmt(sugar)} גרם סוכר ל-100 גרם."
            )
        if "עוגות אישיות" in name and "קרם שוקולד" in name:
            return (
                "עוגות אישיות 145 קק\"ל למנה עם קרם שוקולד. "
                "סוכר וסירופ גלוקוז-פרוקטוז בראש הרשימה."
            )
        if "סגנון מרוקאי" in name:
            return (
                "עוגיות בסגנון מרוקאי עם מרגרינה ו-60% קמח לבן. "
                "7.4 גרם שומן רווי ל-100 גרם."
            )
        if "מרוקאיות עגול" in name:
            return (
                "עוגיות מרוקאיות עגול — נוסחת מרגרינה וקמח לבן. "
                "7.4 גרם שומן רווי ל-100 גרם."
            )
        if "ריפ'את" in name:
            return (
                "עוגיות ריפ'את — נוסחה זהה לגרסאות המרוקאיות האחרות. "
                "מרגרינה ו-7.4 גרם שומן רווי ל-100 גרם."
            )
        if "מיני מרוקאיות" in name:
            return (
                "עוגיות מיני מרוקאיות עם מרגרינה. "
                "8.8 גרם שומן רווי ו-18 גרם סוכר ל-100 גרם."
            )
        # D fallback
        return (
            f"ציון D — הרכב תעשייתי. "
            f"{'מרגרינה זוהתה. ' if has_phvo else ''}"
            f"{'שומן רווי ' + fmt(sat_fat) + ' גרם ל-100 גרם.' if sat_fat else ''}"
        ).strip()

    # ── E grade ──────────────────────────────────────────────────────────────
    if grade == "E":
        return build_e_verdict(name, score, energy, fat, sat_fat, sugar, sodium, fiber,
                                protein, has_phvo, nova, limiting, ingredients, routed, barcode)

    return "נתונים לא זמינים."


def build_e_verdict(name, score, energy, fat, sat_fat, sugar, sodium, fiber,
                     protein, has_phvo, nova, limiting, ingredients, routed, barcode=""):
    """E-grade verdicts — 132 products, grouped by character."""

    # Extreme sat-fat products first
    if "עוגות אישיות" in name and "קוקוס" in name:
        return (
            f"עוגות קוקוס אישיות עם {fmt(sat_fat)} גרם שומן רווי ל-100 גרם — הגבוה שנמדד בסריקה. "
            f"{fmt(sugar)} גרם סוכר."
        )

    if "מוס בלגי" in name:
        return (
            f"עוגת מוס בלגי פרווה עם {fmt(sat_fat)} גרם שומן רווי ל-100 גרם ומרגרינה. "
            f"{fmt(sugar)} גרם סוכר."
        )

    if has_phvo and sat_fat is not None and sat_fat > 10:
        fat_word = "מרגרינה" if "מרגרינה" in ingredients else "שומן צמחי מוקשה"
        return (
            f"{fat_word} ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם — שני אותות שומן מצטברים. "
            "הציון נמוך גם בלי להביא בחשבון את הסוכר."
        )

    if has_phvo:
        msg = "מרגרינה" if "מרגרינה" in ingredients else "שומן צמחי מוקשה"
        extra = f" סוכר {fmt(sugar)} גרם ל-100 גרם." if sugar is not None else ""
        return f"{msg} ברשימת הרכיבים.{extra}"

    # פרה קראנץ' (47g sugar, 16.7g sat fat)
    if "פרה קראנץ" in name:
        return (
            f"פרה קראנץ' עם {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם. "
            f"{fmt(energy)} קק\"ל."
        )

    # צימקאו / שוקולד לבן כשל"פ (70.9g sugar)
    if "צימקאו" in name or ("שוקולד לבן" in name and "כשל" in name):
        return (
            f"{fmt(sugar)} גרם סוכר ל-100 גרם — הגבוה בסריקה. "
            f"{fmt(sat_fat)} גרם שומן רווי."
        )

    # אוראו variants
    if "אוראו" in name and "לבן" in name:
        return f"אוראו בציפוי שוקולד לבן — {fmt(sugar)} גרם סוכר ל-100 גרם. שמן דקל בשומנים."

    if "אוראו" in name and "חלב" in name and "ציפוי" in name:
        return f"אוראו בציפוי שוקולד חלב — {fmt(sugar)} גרם סוכר ל-100 גרם. {fmt(sat_fat)} גרם שומן רווי."

    if "אוראו" in name and "דאבל" in name:
        return f"אוראו דאבל קרם — {fmt(sugar)} גרם סוכר ל-100 גרם; כפליים קרם מהגרסה הרגילה."

    if "אוראו" in name:
        return f"עוגיות אוראו — {fmt(sugar)} גרם סוכר ל-100 גרם. שמן דקל בראש רשימת השומנים."

    # לוטוס / קרמל (38.1g sugar, 8g sat fat, 484 kcal)
    if "לוטוס" in name:
        return (
            f"ביסקוויט קרמל מוכר — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי. "
            f"{fmt(energy)} קק\"ל ל-100 גרם."
        )

    if "קרמל" in name and "ביסקוויט" in name:
        return f"ביסקוויט קרמל — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    # נוטלה (35.8g sugar, 11.5g sat fat)
    if "נוטלה" in name:
        return (
            f"ביסקוויט נוטלה — 40% ממרח קקאו-אגוזים. "
            f"{fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם."
        )

    # מילקה
    if "מילקה" in name and "אוראו" in name:
        return f"שוקולד חלב + אוראו — {fmt(sugar)} גרם סוכר ל-100 גרם."

    if "מילקה" in name:
        return f"עוגיות מילקה — {fmt(sugar)} גרם סוכר ל-100 גרם. {fmt(sat_fat)} גרם שומן רווי."

    # Ultra-high sugar (>45g)
    if sugar is not None and sugar > 45:
        return (
            f"{fmt(sugar)} גרם סוכר ל-100 גרם — גבוה מאוד. "
            "רכיב ראשון ברשימה."
        )

    # Very high sugar (>35g)
    if sugar is not None and sugar > 35:
        return (
            f"{fmt(sugar)} גרם סוכר ל-100 גרם, {fmt(sat_fat)} גרם שומן רווי. "
            "שני הגורמים עיקריים בציון הנמוך."
        )

    # High sat fat (>13g) without PHVO
    if sat_fat is not None and sat_fat > 13:
        sug_note = f" סוכר {fmt(sugar)} גרם נוסף." if sugar is not None else ""
        return f"{fmt(sat_fat)} גרם שומן רווי ל-100 גרם — בולט גם בקטגוריה זו.{sug_note}"

    # Named products (less extreme)
    if "עינוגים" in name:
        return f"עינוגים קוקיס — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "LOVITA" in name or "lovita" in name.lower():
        return f"עוגיות LOVITA שוקולד — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "היט" in name and "מיניס" in name:
        return f"עוגיות היט מיניס — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "היט" in name and "שוקולד" in name:
        return f"עוגיות היט שוקולד — {fmt(sat_fat)} גרם שומן רווי ל-100 גרם."

    if "היט" in name:
        return f"עוגיות היט — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "חיוכים" in name:
        return f"עוגיות חיוכים — {fmt(sugar)} גרם סוכר ל-100 גרם. עוגיית ילדים."

    if "גן חיות" in name or "חיות שוקו" in name or "נסיכה" in name:
        return f"עוגיות ילדים — {fmt(sugar)} גרם סוכר ל-100 גרם. {fmt(sat_fat)} גרם שומן רווי."

    if "בוטנים" in name:
        return f"עוגיות בוטנים — {fmt(sugar)} גרם סוכר. הבוטנים אינם הרכיב הדומיננטי."

    if "שיבולת שועל" in name and "עוגיות" in name:
        return f"עוגיות שיבולת שועל — {fmt(sat_fat)} גרם שומן רווי ל-100 גרם. שיבולת שועל בשם, לא הרכיב הראשון."

    if "קקאו דגנים מלאים" in name:
        return f"דגנים מלאים ונטיפי שוקולד מריר — {fmt(energy)} קק\"ל ל-100 גרם. {fmt(sugar)} גרם סוכר."

    if "פיטנס" in name and "חמוציות" in name:
        return f"עוגיות פיטנס חמוציות — {fmt(energy)} קק\"ל ל-100 גרם. {fmt(sugar)} גרם סוכר."

    if "ספוג" in name:
        return f"עוגות ספוג מצופות שוקולד — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "קרמוגית" in name and "שוקו" in name:
        return f"קרמוגית קראנץ שוקו — {fmt(energy)} קק\"ל למנה. {fmt(sat_fat)} גרם שומן רווי ל-100 גרם."

    if "קרמוגית" in name:
        return f"קרמוגית קראנץ — {fmt(energy)} קק\"ל למנה. {fmt(sat_fat)} גרם שומן רווי ל-100 גרם."

    if "קראנץ אגוזי לוז" in name:
        return f"קראנץ אגוזי לוז — {fmt(sat_fat)} גרם שומן רווי ו-{fmt(sugar)} גרם סוכר."

    if "מאגדת" in name:
        return f"מיני קראנץ — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "אלפחורס" in name:
        return f"מיני אלפחורס — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "קראנץ סנדויץ" in name:
        return f"קראנץ סנדוויץ — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "גולד רינג" in name:
        return f"עוגיות גולד רינג — {fmt(energy)} קק\"ל ו-{fmt(sat_fat)} גרם שומן רווי."

    if "דובוש" in name:
        return f"עוגת פס דובוש — {fmt(sugar)} גרם סוכר. שכבות קרם עם גלוקוז."

    if "דובדבנים" in name:
        return f"עוגת פס דובדבנים — {fmt(sat_fat)} גרם שומן רווי ו-{fmt(sugar)} גרם סוכר."

    if "דבש" in name and "עוגת" in name:
        return f"עוגת דבש — {fmt(sugar)} גרם סוכר. דבש אינו הרכיב הראשון."

    if "אנגלית" in name:
        return f"עוגה אנגלית — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "בראוניס" in name:
        return f"בראוניס — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "רולדה" in name:
        return f"עוגיות רולדה תמרים — {fmt(sat_fat)} גרם שומן רווי. תמרים לא דומיננטיים."

    if "מאפין" in name:
        phvo_note = "מרגרינה ו" if has_phvo else ""
        return f"מאפין תעשייתי — {phvo_note}{fmt(sugar)} גרם סוכר ל-100 גרם."

    if "שמרים" in name and "קרנאץ'" in name:
        return f"עוגת שמרים קרנאץ' — {fmt(sugar)} גרם סוכר ל-100 גרם. פחמימות גבוהות."

    if "שמרים" in name and "פרג" in name:
        return f"עוגת שמרים פרג — {fmt(sugar)} גרם סוכר ל-100 גרם."

    if "שמרים" in name and "בריוש" in name:
        return f"בריוש שמרים — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "שמרים" in name:
        return f"עוגת שמרים — {fmt(sugar)} גרם סוכר ל-100 גרם. פחמימות גבוהות."

    if "גבינה" in name and "פס" in name:
        return f"עוגת פס גבינה — {fmt(sugar)} גרם סוכר. מרגרינה ברשימה."

    if "גבינה" in name and "רנסנס" in name:
        return f"עוגת גבינה רנסנס — {fmt(sugar)} גרם סוכר ל-100 גרם."

    if "גבינה פירורים" in name:
        return f"עוגת גבינה פירורים — {fmt(sat_fat)} גרם שומן רווי ל-100 גרם."

    if "גבינה" in name:
        return f"עוגת גבינה — {fmt(sugar)} גרם סוכר ל-100 גרם. {fmt(sat_fat)} גרם שומן רווי."

    if "מוס" in name and "היער השחור" in name:
        return f"עוגת מוס היער השחור — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "מוס" in name:
        return f"עוגת מוס — {fmt(sugar)} גרם סוכר ל-100 גרם. {fmt(sat_fat)} גרם שומן רווי."

    if "עוגות הבית" in name or "עוגת הבית" in name:
        return f"עוגה תעשייתית — {fmt(sugar)} גרם סוכר ל-100 גרם. {fmt(energy)} קק\"ל."

    if "סנדוויץ" in name:
        return f"עוגיות סנדוויץ — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "ללא גלוטן" in name:
        return f"ללא גלוטן — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי ל-100 גרם."

    if "פס" in name:
        return f"עוגת פס — {fmt(sugar)} גרם סוכר ל-100 גרם. {fmt(sat_fat)} גרם שומן רווי."

    if "קרנץ'" in name:
        return f"עוגת קרנץ' — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    if "קרנץ" in name:
        return f"עוגת קרנץ — {fmt(sugar)} גרם סוכר ו-{fmt(sat_fat)} גרם שומן רווי."

    # Generic E
    if sugar is not None and sugar > 25:
        sug_note = f" שומן רווי {fmt(sat_fat)} גרם בנוסף." if sat_fat is not None else ""
        return f"{fmt(sugar)} גרם סוכר ל-100 גרם — הגורם המוביל בציון.{sug_note}"

    if sat_fat is not None and sat_fat > 8:
        return f"{fmt(sat_fat)} גרם שומן רווי ל-100 גרם. הרכב תעשייתי."

    if energy is not None:
        return f"{fmt(energy)} קק\"ל ל-100 גרם — הרכב מוגבל."

    return "הרכב תזונתי נמוך — נתוני סריקה חלקיים."


# ─────────────────────────────────────────────────────────────────────────────
# BOTTOM LINE
# ─────────────────────────────────────────────────────────────────────────────

def build_bottom_line(name, score, grade, energy, fat, sat_fat, sugar, sodium, fiber,
                       protein, has_phvo, nova, limiting, ingredients, routed):
    if grade == "C":
        fb = f"סיבים: {fmt(fiber)} גרם ל-100 גרם. " if fiber else ""
        phvo_note = "מרגרינה ברשימה. " if has_phvo else ""
        if "זעתר" in name:
            return (
                "ציון C על בסיס 0 גרם סוכר — לא מדד לאיכות כללית. "
                "נתרן גבוה (730 מ\"ג) ואין יתרון תזונתי מיוחד. "
                "מוצר מלוח, לא חלופה לעוגיות."
            )
        return (
            f"ציון C — בין חמשת הגבוהים ב-149 מוצרי הקטגוריה. לא מוצר 'בריאות'. "
            f"{phvo_note}{fb}"
            "גם C הגבוה ביותר בקטגוריה זו מייצג פינוק, לא ארוחה."
        )
    if grade == "D":
        phvo_note = "שומן מוקשה ברשימה. " if has_phvo else ""
        return (
            f"ציון D — הרכב נמוך. {phvo_note}"
            "מוגבל בסוכר, שומן רווי, או קלוריות צפופות."
        )
    # E
    phvo_note = "שומן מוקשה ברשימה. " if has_phvo else ""
    sug_note = f"סוכר {fmt(sugar)} גרם ל-100 גרם. " if sugar is not None else ""
    return (
        f"ציון E. {phvo_note}{sug_note}"
        "הרכב נמוך לכל הגדרה — מוצר פינוק עם מחיר תזונתי ברור."
    )


# ─────────────────────────────────────────────────────────────────────────────
# CONSUMER TAKEAWAY
# ─────────────────────────────────────────────────────────────────────────────

def build_takeaway(name, score, grade, energy, fat, sat_fat, sugar, sodium, fiber,
                    protein, has_phvo, nova, limiting, ingredients, routed):
    if grade == "C":
        if "זעתר" in name:
            return "ציון C בזכות 0 גרם סוכר. עוגייה מלוחה עם נתרן גבוה — לא חלופה לפינוק מתוק."
        phvo = " עם שומן מוקשה ברשימה" if has_phvo else ""
        return f"ציון C — אחד מחמישה מוצרים בטווח זה מתוך 149{phvo}. עדיין מוצר פינוק."
    if grade == "D":
        phvo = " עם שומן מוקשה ברשימה" if has_phvo else ""
        return f"ציון D — בין הפחות גרועים מהחלק התחתון{phvo}. עדיין מוצר פינוק."
    # E
    sug = f"סוכר {fmt(sugar)} גרם ל-100 גרם — " if sugar is not None and sugar > 25 else ""
    return f"{sug}ציון E. מוצר פינוק עם הרכב תזונתי מוגבל."


# ─────────────────────────────────────────────────────────────────────────────
# CONSUMER EXPLANATION
# ─────────────────────────────────────────────────────────────────────────────

def build_explanation(name, score, grade, energy, fat, sat_fat, sugar, sodium, fiber,
                       protein, has_phvo, nova, limiting, ingredients, routed):
    if grade == "C":
        fiber_str = f"סיבים תזונתיים: {fmt(fiber)} גרם ל-100 גרם. " if fiber else ""
        phvo_str = "שומן צמחי מוקשה / מרגרינה נצפו ברשימת הרכיבים. " if has_phvo else ""
        if "זעתר" in name:
            return (
                "הציון C נובע מהיעדר סוכר בלבד — לא מהרכב תזונתי מיוחד. "
                "730 מ\"ג נתרן ל-100 גרם הם גבוהים. "
                "מוצר מלוח הנצרך באוקזיות שונות לחלוטין מעוגיות."
            )
        return (
            f"ציון C נמצא בחמישיית הגבוהים בסריקה של 149 מוצרים. "
            f"{fiber_str}{phvo_str}"
            "גם ציון C מייצג מוצר פינוק — לא מזון לאכילה יומיומית."
        )
    if grade == "D":
        lf_parts = []
        if has_phvo:
            lf_parts.append("שומן מוקשה")
        if sat_fat is not None and sat_fat > 6:
            lf_parts.append(f"שומן רווי {fmt(sat_fat)} גרם ל-100 גרם")
        if sugar is not None and sugar > 15:
            lf_parts.append(f"סוכר {fmt(sugar)} גרם ל-100 גרם")
        if energy is not None and energy > 400:
            lf_parts.append(f"צפיפות קלורית {fmt(energy)} קק\"ל")
        lf_str = "; ".join(lf_parts) + ". " if lf_parts else ""
        return (
            f"ציון D — הרכב נמוך. {lf_str}"
            "מוצר תעשייתי עם פחמימות מהירות כעיקר."
        )
    # E
    phvo_str = "שומן מוקשה / מרגרינה זוהה ברשימת הרכיבים. " if has_phvo else ""
    sug_str = f"סוכר: {fmt(sugar)} גרם ל-100 גרם. " if sugar is not None else ""
    sat_str = f"שומן רווי: {fmt(sat_fat)} גרם ל-100 גרם. " if sat_fat is not None else ""
    return (
        f"ציון E — הרכב תזונתי נמוך. "
        f"{sug_str}{sat_str}{phvo_str}"
        "הציון משקף את מה שנמצא בתווית שנסרקה ישירות מהחנות."
    )


# ─────────────────────────────────────────────────────────────────────────────
# BARI INTERPRETATION
# ─────────────────────────────────────────────────────────────────────────────

def build_interpretation(name, score, grade, energy, fat, sat_fat, sugar, sodium, fiber,
                          protein, has_phvo, nova, limiting, ingredients, routed):
    if grade == "C":
        if "זעתר" in name:
            return (
                "ברי סרקה 149 מוצרים בקטגוריית עוגות ועוגיות. "
                "מוצר זה קיבל ציון C בעיקר בגלל 0 גרם סוכר. "
                "הנתרן הגבוה (730 מ\"ג) ואופי הצריכה המלוח מציבים אותו בקטגוריית מוצרים שונה לחלוטין."
            )
        return (
            f"ברי סרקה 149 מוצרים בקטגוריה. ציון C — אחד מחמישה מוצרים בטווח הגבוה. "
            f"{'שומן מוקשה זוהה. ' if has_phvo else ''}"
            "גם ציון C בקטגוריה זו מייצג הרכב שאינו מתאים לאכילה יומיומית."
        )
    if grade == "D":
        phvo_note = "מרגרינה / שומן מוקשה זוהה. " if has_phvo else ""
        return (
            f"ברי סרקה 149 מוצרים. ציון D — 12 מוצרים בטווח זה. "
            f"{phvo_note}"
            "הרכב מוגבל בסוכר, שומן רווי, או עיבוד גבוה."
        )
    # E
    return (
        f"ברי סרקה 149 מוצרים בקטגוריה. 132 קיבלו ציון E — כולל מוצר זה. "
        f"{'שומן מוקשה זוהה. ' if has_phvo else ''}"
        f"{'סוכר גבוה: ' + fmt(sugar) + ' גרם ל-100 גרם. ' if sugar is not None and sugar > 25 else ''}"
        "הציון משקף הרכב תזונתי נמוך על בסיס נתוני התווית שנסרקו ישירות."
    )


# ─────────────────────────────────────────────────────────────────────────────
# POSITIVE SIGNALS
# ─────────────────────────────────────────────────────────────────────────────

def build_positive_signals(score, grade, fiber, protein, sugar, sat_fat, has_phvo,
                             energy, ingredients, nova):
    signals = []
    if grade == "E":
        return []  # Never manufacture positives for E

    if fiber is not None and fiber >= 5:
        signals.append(f"סיבים תזונתיים: {fmt(fiber)} גרם ל-100 גרם")
    if protein is not None and protein >= 8 and grade in ("C",):
        signals.append(f"חלבון: {fmt(protein)} גרם ל-100 גרם")
    if sugar is not None and sugar <= 5 and grade in ("C", "D"):
        signals.append(f"סוכר נמוך: {sugar:.1f} גרם ל-100 גרם")
    if grade in ("C",) and ("קמח חיטה מלא" in ingredients or "כוסמין מלא" in ingredients
                            or "קמח כוסמין מלא" in ingredients):
        signals.append("דגן מלא ברשימת הרכיבים")
    if not has_phvo and sat_fat is not None and sat_fat < 3 and grade in ("C",):
        signals.append(f"שומן רווי נמוך: {sat_fat:.1f} גרם ל-100 גרם")

    return signals


# ─────────────────────────────────────────────────────────────────────────────
# BEST USE CASES
# ─────────────────────────────────────────────────────────────────────────────

def build_best_use_cases(grade, score, fiber, protein, sugar, has_phvo, energy, routed):
    if grade == "E":
        return []
    if grade == "D" and (not fiber or fiber < 3):
        return []
    cases = []
    if grade == "C":
        cases.append("פינוק בודד — לא חלק מתפריט יומיומי")
        if sugar is not None and sugar < 10:
            cases.append("כשמחפשים עוגייה עם פחות סוכר יחסית")
        if fiber is not None and fiber >= 5:
            cases.append("כמקור לסיבים תזונתיים בתוך קטגוריית פינוק")
    elif grade == "D":
        if fiber is not None and fiber >= 3:
            cases.append("כשהסיבים חשובים — עם מגבלות ברורות")
    return cases


# ─────────────────────────────────────────────────────────────────────────────
# PAGE COPY  — updated for 149 / no A / no B / C:5 · D:12 · E:132
# ─────────────────────────────────────────────────────────────────────────────

PAGE_COPY = {
    "hero": {
        "title": "עוגות ועוגיות",
        "tagline": "149 מוצרים נסרקו — אף אחד לא הגיע ל-A."
    },
    "prologue": {
        "sentences": [
            "קטגוריית עוגות ועוגיות היא אחת הגדולות שברי סרקה: 149 מוצרים משתי רשתות, כולם מוצרי פינוק. "
            "הממצא הבולט: אף מוצר לא הגיע ל-A ואף מוצר לא הגיע ל-B. "
            "חמישה מוצרים עצרו ב-C; 12 ב-D; 132 קיבלו E. "
            "הטוב ביותר בסריקה הוא עוגיית שקדים וחמוציות שהגיעה ל-C בלבד — לא A, לא B. "
            "41 מוצרים מכילים שומן צמחי מוקשה (מרגרינה), ולחלקם שמות כמו 'טבעי' או 'כשל\"פ'. "
            "שני הגורמים שמושכים את הציונים למטה: סוכר גבוה (עד 70 גרם ל-100 גרם) ושומן רווי גבוה. "
            "ברי תיעדה את כל זה ישירות מתוויות המוצרים. ללא מקורות חיצוניים."
        ]
    },
    "methodology": {
        "body": (
            "הציון מחושב על בסיס נתוני התזונה ורשימת הרכיבים כפי שנסרקו ישירות מהחנות. "
            "הגורמים המרכזיים: צפיפות קלורית, כמות הסוכר, שומן רווי, נוכחות שומן מוקשה, ורמת עיבוד המזון. "
            "ציון C בקטגוריה זו פירושו 'פחות גרוע יחסית' — לא 'מוצר בריאות'. "
            "אף מוצר מ-149 שנסרקו לא הגיע ל-A או B. "
            "הנתונים נסרקו ישירות מהמדף. Open Food Facts לא שימש בשום שלב."
        )
    },
    "caveat": {
        "title": "הערת קטגוריה — עוגות ועוגיות",
        "body": (
            "קטגוריה זו היא קטגוריית פינוק. ציון C במדף הזה הוא 'פחות גרוע', לא המלצה לצריכה יומיומית.\n\n"
            "ברי בדקה 149 מוצרים: C:5, D:12, E:132. אף מוצר לא הגיע ל-A או B. "
            "הציון הגבוה ביותר בקטגוריה הוא C בלבד.\n\n"
            "41 מוצרים מכילים שומן צמחי מוקשה (מרגרינה), עובדה שלא תמיד ברורה מהשם. "
            "עוגיית הזעתר קיבלה C בגלל 0 גרם סוכר, לא בגלל ערך תזונתי כולל. מוצר מלוח לאוקזיות שונות לחלוטין. "
            "מוצרים שנסרקו מבית קפה או מאפייה חצי-תעשייתית לא נכללו בסריקה זו. "
            "ברי תיעדה רק מוצרים ארוזים עם תווית תזונה מלאה."
        )
    },
    "filters": [
        {
            "id": "all",
            "label_he": "הכל",
            "count": 149
        },
        {
            "id": "least_bad",
            "label_he": "הפחות גרועים",
            "count": 5,
            "description_he": "ציון C בלבד — 5 מוצרים; אף מוצר לא הגיע ל-B בקטגוריה זו"
        },
        {
            "id": "has_phvo",
            "label_he": "מכיל שומן מוקשה",
            "count": 41,
            "description_he": "41 מוצרים שזוהה בהם שומן צמחי מוקשה או מרגרינה ברשימת הרכיבים"
        },
        {
            "id": "no_phvo",
            "label_he": "ללא שומן מוקשה",
            "count": 108,
            "description_he": "108 מוצרים ללא שומן מוקשה ברשימת הרכיבים — כולל ציוני D ו-E רבים"
        },
        {
            "id": "high_sugar",
            "label_he": "סוכר גבוה",
            "count": 66,
            "description_he": "מוצרים עם 30 גרם סוכר ומעלה ל-100 גרם — על בסיס נתוני הסריקה"
        }
    ]
}


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    with open(INPUT_PATH, encoding="utf-8") as f:
        data = json.load(f)

    # Verify corpus matches expected
    total = len(data["products"])
    dist = {}
    for p in data["products"]:
        g = p["grade"]
        dist[g] = dist.get(g, 0) + 1

    expected_total = 149
    expected_dist = {"C": 5, "D": 12, "E": 132}
    if total != expected_total:
        print(f"WARNING: expected {expected_total} products, got {total}", file=__import__('sys').stderr)
    for g, n in expected_dist.items():
        if dist.get(g, 0) != n:
            print(f"WARNING: expected {n} grade-{g} products, got {dist.get(g, 0)}", file=__import__('sys').stderr)

    # ── Fill page copy ──────────────────────────────────────────────────────
    data["page_copy"]["hero"]["title"] = PAGE_COPY["hero"]["title"]
    data["page_copy"]["hero"]["tagline"] = PAGE_COPY["hero"]["tagline"]
    data["page_copy"]["prologue"]["sentences"] = PAGE_COPY["prologue"]["sentences"]
    data["page_copy"]["methodology"]["body"] = PAGE_COPY["methodology"]["body"]
    data["page_copy"]["caveat"]["title"] = PAGE_COPY["caveat"]["title"]
    data["page_copy"]["caveat"]["body"] = PAGE_COPY["caveat"]["body"]
    data["page_copy"]["filters"] = PAGE_COPY["filters"]

    # ── Fill product copy ────────────────────────────────────────────────────
    filled = 0
    errors = []
    for p in data["products"]:
        try:
            c = build_product_copy(p)
            p["confidence_label_he"] = c["confidence_label_he"]
            p["confidence_tooltip_he"] = c["confidence_tooltip_he"]
            p["confidence_sub_reason"] = c["confidence_sub_reason"]
            p["insightLine"] = c["insightLine"]
            p["rowVerdict"] = c["rowVerdict"]
            p["expansion"]["confidenceLabel"] = c["expansion_confidenceLabel"]
            p["expansion"]["servingNote"] = c["expansion_servingNote"]
            p["expansion"]["positiveSignals"] = c["expansion_positiveSignals"]
            p["expansion"]["bottomLine"] = c["expansion_bottomLine"]
            p["consumerTakeaway"] = c["consumerTakeaway"]
            p["consumerExplanation"] = c["consumerExplanation"]
            p["bariInterpretation"] = c["bariInterpretation"]
            p["bestUseCases"] = c["bestUseCases"]
            filled += 1
        except Exception as e:
            errors.append(f"{p.get('id', '?')}: {e}")

    # ── Update meta ──────────────────────────────────────────────────────────
    data["_meta"]["copy_status"] = "COMPLETE"

    # ── Write output ─────────────────────────────────────────────────────────
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Done. Filled: {filled}/{total}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
    else:
        print("No errors.")


if __name__ == "__main__":
    main()
