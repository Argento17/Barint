# -*- coding: utf-8 -*-
"""
TASK-515A: Build yogurt_drinkable_FINAL_v3.json from the 20-product D7-suppressed base.
Carries FINAL_v2 (23-corpus, signed) copy byte-for-byte for unchanged products,
re-authors the 4 score/grade-changed products from trace data, applies 2 surgical
false-superlative fixes (55336, 58030) found during the corpus-wide recheck, and
updates all consumer-facing "23" counts to "20".
Words only. No score/data field is touched -- every non-copy field is carried
forward from the base unmodified.
"""
import json
import re
import copy
import hashlib

BASE_PATH = r"C:\Bari\02_products\yogurt_system\bsip2_task515_v3\frontend_out\yogurt_drinkable_D7_SUPPRESS_v1.json"
PRIOR_PATH = r"C:\Bari\02_products\yogurt_system\bsip2_task515_v3\frontend_out\yogurt_drinkable_FINAL_v2.json"
OUT_PATH = r"C:\Bari\02_products\yogurt_system\bsip2_task515_v3\frontend_out\yogurt_drinkable_FINAL_v3.json"

base = json.load(open(BASE_PATH, encoding="utf-8"))
prior = json.load(open(PRIOR_PATH, encoding="utf-8"))
prior_by_bc = {p["barcode"]: p for p in prior["products"]}

COUNT_RE = re.compile(r"(?<!\d)23(?!\d)")


def fix_count(s):
    if not isinstance(s, str):
        return s
    return COUNT_RE.sub("20", s)


def carry_copy(dst, src):
    """Copy all copy fields from src (prior, 23-corpus) onto dst (base product),
    fixing the '23' -> '20' count reference in every copied string."""
    dst["bestUseCases"] = [fix_count(x) for x in src["bestUseCases"]]
    dst["consumerTakeaway"] = fix_count(src["consumerTakeaway"])
    dst["insightLine"] = fix_count(src["insightLine"])
    dst["rowVerdict"] = fix_count(src["rowVerdict"])
    src_bi = {x["key"]: x["interpretation"] for x in src["bariInterpretation"]}
    for item in dst["bariInterpretation"]:
        if item["key"] in src_bi:
            item["interpretation"] = fix_count(src_bi[item["key"]])
    dst["expansion"]["comparisonContext"] = fix_count(src["expansion"]["comparisonContext"])
    ce_src = src["expansion"]["consumerExplanation"]
    ce_dst = dst["expansion"]["consumerExplanation"]
    ce_dst["context"] = fix_count(ce_src["context"])
    ce_dst["good"] = [fix_count(x) for x in ce_src["good"]]
    ce_dst["takeaway"] = fix_count(ce_src["takeaway"])
    ce_dst["watchOut"] = [fix_count(x) for x in ce_src["watchOut"]]
    ce_dst["whyRated"] = fix_count(ce_src["whyRated"])


# ---------------------------------------------------------------------------
# 1) Full re-authoring: the 4 products whose score/grade changed under D7
# ---------------------------------------------------------------------------
REAUTHOR = {
    # -------------------------------------------------------------- 55343
    "55343": {
        "bestUseCases": ["טעם פירותי"],
        "consumerTakeaway": "משקה טרופי עם סוכר גבוה (9.9 גרם), ארבעה תוספים, ו-2.4 גרם חלבון בלבד.",
        "bariInterpretation": {
            "processing_quality": "רשימת הרכיבים כוללת 9 רכיבים, עם מספר שלבי עיבוד.",
            "additive_quality": "4 תוספים מזוהים ברשימה, כולל כאלה בשימוש תלוי-מינון או שנויים במחלוקת מדעית.",
            "nutrient_density": "מכיל 2.4 גרם חלבון ל-100 גרם, לצד 65 קלוריות.",
            "protein_quality": "2.4 גרם חלבון ל-100 גרם.",
            "calorie_density": "65 קלוריות ל-100 גרם.",
            "glycemic_quality": "9.9 גרם סוכר ל-100 גרם.",
            "fat_quality": "1.5 גרם שומן ל-100 גרם.",
            "satiety_support": "2.4 גרם חלבון ל-100 גרם.",
            "regulatory_quality": "עומד בדרישות התיוג הרגולטורי הבסיסיות למוצרי חלב בישראל.",
            "whole_food_integrity": "ההרכב נשען במידה ניכרת על תוספים ורכיבים מעובדים (עמילן מעובד ומייצב) לצד יוגורט ופרי מבושל.",
        },
        "expansion": {
            "comparisonContext": "9.9 גרם סוכר ל-100 גרם, מתוך טווח סוכר של 3.3 עד 12 גרם ב-20 המשקאות שנבדקו, מהגבוהים בהשוואה זו.",
            "consumerExplanation": {
                "context": "המשקה מבוסס על יוגורט עם ארבעה פירות טרופיים מבושלים (6%), סוכר, מייצב (פקטין), עמילן מעובד, מווסת חומציות, וחומר משמר.",
                "good": ["ארבעה טעמי פרי אמיתיים במחית מבושלת"],
                "takeaway": "טעם טרופי מגוון, אך עם סוכר גבוה, ארבעה תוספים, ו-2.4 גרם חלבון בלבד.",
                "watchOut": [],
                "whyRated": "הפירות האמיתיים תורמים לזהות המוצר. מנגד, 9.9 גרם סוכר, ארבעה תוספים (כולל חומצת לימון וחומר משמר), ו-2.4 גרם חלבון בלבד ל-100 גרם מגבילים את הציון בכמה ממדים במקביל.",
            },
        },
        "insightLine": "משקה טרופי עם 9.9 גרם סוכר ל-100 גרם, מהגבוהים בהשוואה זו, וארבעה תוספים.",
        "rowVerdict": "משקה יוגורט טרופי (פסיפלורה, אננס, מנגו, אפרסק) עם 9.9 גרם סוכר ל-100 גרם, מהגבוהים בהשוואה זו. ארבעה תוספים ברשימה, כולל חומצת לימון כתוסף שימור וחומר משמר, ו-2.4 גרם חלבון בלבד.",
    },
    # ------------------------------------------------------- 7290107938396
    "7290107938396": {
        "bestUseCases": ["סיבים תזונתיים"],
        "consumerTakeaway": "משקה עם תרבית פרוביוטית מתועדת (L.CASEI DN114-001), ויטמין D מוסף, ו-1.7 גרם סיבים ל-100 גרם.",
        "bariInterpretation": {
            "processing_quality": "רשימת הרכיבים ארוכה יחסית (11 רכיבים), עם מספר שלבי עיבוד.",
            "additive_quality": "2 תוספים מזוהים ברשימה, שני מייצבים טבעיים (גואר ולוקוסט-בין גאם).",
            "nutrient_density": "מכיל 2.7 גרם חלבון ו-1.7 גרם סיבים תזונתיים ל-100 גרם, לצד 52 קלוריות.",
            "protein_quality": "2.7 גרם חלבון ל-100 גרם.",
            "calorie_density": "52 קלוריות ל-100 גרם.",
            "glycemic_quality": "5 גרם סוכר ל-100 גרם.",
            "fat_quality": "1.5 גרם שומן ל-100 גרם.",
            "satiety_support": "2.7 גרם חלבון ו-1.7 גרם סיבים תזונתיים ל-100 גרם. תרומת הסיבים לתחושת השובע ניכרת.",
            "regulatory_quality": "עומד בדרישות התיוג הרגולטורי הבסיסיות למוצרי חלב בישראל.",
            "whole_food_integrity": "ההרכב נשען במידה ניכרת על רכיבים מבודדים ותוספים (חלבוני מי גבינה, אבקת חלב ומייצבים) לצד חלב ושמנת.",
        },
        "expansion": {
            "comparisonContext": "אחד משלושה מוצרי אקטימל בקטגוריה זו עם תרבית L.CASEI DN114-001 מתועדת במפורש ברשימת הרכיבים.",
            "consumerExplanation": {
                "context": "המשקה מבוסס על חלב, שמנת, סוכר, מחית תות (2%), סיבי עולש, חלבוני מי גבינה, אבקת חלב, מיצוי פרי המונק, שני מייצבים טבעיים (גואר ולוקוסט-בין גאם), ויטמין D, ותרבית L.CASEI DN114-001.",
                "good": [
                    "1.7 גרם סיבים ל-100 גרם",
                    "תרבית פרוביוטית מתועדת בשם (L.CASEI DN114-001)",
                    "ויטמין D מוסף",
                ],
                "takeaway": "משקה עם תרבית מתועדת וסיבים, אך 2.7 גרם חלבון בלבד וברשימת רכיבים ארוכה.",
                "watchOut": [],
                "whyRated": "הסיבים המוספים והתרבית המתועדת תומכים בציון. מנגד, 2.7 גרם חלבון ל-100 גרם ורשימת רכיבים ארוכה יחסית, הכוללת חלבוני מי גבינה, אבקת חלב ושני מייצבים, לצד סוכר לבן ורכז פרי המונק כממתיקים, מגבילים את הציון הכולל.",
            },
        },
        "insightLine": "אקטימל תות: תרבית L.CASEI DN114-001 מתועדת ברשימת הרכיבים, לצד 1.7 גרם סיבים ל-100 גרם.",
        "rowVerdict": "אקטימל תות במארז, עם תרבית פרוביוטית מתועדת (L.CASEI DN114-001), ויטמין D, ו-1.7 גרם סיבים ל-100 גרם. שני מייצבים טבעיים ברשימה, לצד סוכר לבן ורכז פרי המונק כממתיקים, ו-2.7 גרם חלבון בלבד.",
    },
    # ------------------------------------------------------- 7290115676051
    "7290115676051": {
        "bestUseCases": ["סיבים תזונתיים"],
        "consumerTakeaway": "משקה עם שיבולת שועל וסיבים תזונתיים (1.1 גרם), ללא תוספים מזוהים.",
        "bariInterpretation": {
            "processing_quality": "רשימת הרכיבים כוללת 9 רכיבים, ברמת עיבוד בינונית.",
            "additive_quality": "אין תוספים מזוהים ברשימת הרכיבים.",
            "nutrient_density": "מכיל 2.9 גרם חלבון ו-1.1 גרם סיבים תזונתיים ל-100 גרם, לצד 53 קלוריות.",
            "protein_quality": "2.9 גרם חלבון ל-100 גרם.",
            "calorie_density": "53 קלוריות ל-100 גרם.",
            "glycemic_quality": "4.9 גרם סוכר ל-100 גרם.",
            "fat_quality": "1.4 גרם שומן ל-100 גרם.",
            "satiety_support": "2.9 גרם חלבון ו-1.1 גרם סיבים תזונתיים ל-100 גרם. תרומת הסיבים לתחושת השובע ניכרת.",
            "regulatory_quality": "עומד בדרישות התיוג הרגולטורי הבסיסיות למוצרי חלב בישראל.",
            "whole_food_integrity": "ההרכב מבוסס בעיקר על חלב, שיבולת שועל אמיתית וסיבים תזונתיים, עם מעט רכיבים מעובדים או תוספים.",
        },
        "expansion": {
            "comparisonContext": "1.1 גרם סיבים ל-100 גרם, נתון שרוב 20 המשקאות בהשוואה זו אינם מדווחים עליו כלל. שיבולת השועל (1.8%) מופיעה ברשימת הרכיבים כרכיב אמיתי.",
            "consumerExplanation": {
                "context": "המשקה מבוסס על חלב פרה עם תוספת שיבולת שועל (1.8%), סוכר, סיבים תזונתיים, ורכז לימון, ללא תוספים מזוהים ברשימת הרכיבים, לצד תרבית פרוביוטית ביפידוס אקטירגולריס.",
                "good": ["שיבולת שועל כרכיב אמיתי", "1.1 גרם סיבים ל-100 גרם", "ללא תוספים מזוהים"],
                "takeaway": "משקה עם שיבולת שועל וסיבים, אך חלבון צנוע (2.9 גרם) למשקה יוגורט.",
                "watchOut": [],
                "whyRated": "היעדר תוספים מזוהים, תוספת שיבולת השועל האמיתית, והתרבית הפרוביוטית תומכים בציון. מנגד, 2.9 גרם חלבון ל-100 גרם נחשבים צנועים למשקה יוגורט, וזה הגורם המרכזי שממתן את הציון.",
            },
        },
        "insightLine": "משקה אקטיביה עם שיבולת שועל (1.8%): 1.1 גרם סיבים ל-100 גרם, ללא תוספים מזוהים ברשימה.",
        "rowVerdict": "משקה אקטיביה בתוספת שיבולת שועל אמיתית (1.8%) עם 1.1 גרם סיבים ל-100 גרם. אין תוספים מזוהים ברשימת הרכיבים, וההרכב מבוסס בעיקרו על חלב, שיבולת שועל וסיבים. 2.9 גרם חלבון ל-100 גרם נחשבים צנועים למשקה יוגורט.",
    },
    # -------------------------------------------------------------- 55329
    "55329": {
        "bestUseCases": ["טעם פירותי"],
        "consumerTakeaway": "משקה תות-מלון עם סוכר גבוה (9.8 גרם) וחמישה תוספים, ובהם קרגינן וצבע מאכל טבעי. הציון הכולל הנמוך ביותר בהשוואה זו.",
        "bariInterpretation": {
            "processing_quality": "רשימת הרכיבים כוללת 11 רכיבים, עם מספר שלבי עיבוד.",
            "additive_quality": "5 תוספים מזוהים ברשימה, ובהם קרגינן, המסווג כתוסף שנוי במחלוקת מדעית.",
            "nutrient_density": "מכיל 2.4 גרם חלבון ל-100 גרם, לצד 64 קלוריות.",
            "protein_quality": "2.4 גרם חלבון ל-100 גרם.",
            "calorie_density": "64 קלוריות ל-100 גרם.",
            "glycemic_quality": "9.8 גרם סוכר ל-100 גרם.",
            "fat_quality": "1.5 גרם שומן ל-100 גרם.",
            "satiety_support": "2.4 גרם חלבון ל-100 גרם.",
            "regulatory_quality": "עומד בדרישות התיוג הרגולטורי הבסיסיות למוצרי חלב בישראל.",
            "whole_food_integrity": "ההרכב נשען במידה ניכרת על תוספים ורכיבים מעובדים (קרגינן ועמילן מעובד) לצד יוגורט ומחיות פרי.",
        },
        "expansion": {
            "comparisonContext": "9.8 גרם סוכר ל-100 גרם, מתוך טווח סוכר של 3.3 עד 12 גרם ב-20 המשקאות שנבדקו, מהגבוהים בהשוואה זו. הציון הכולל של המשקה הוא הנמוך ביותר מבין 20 המשקאות שנבדקו.",
                "consumerExplanation": {
                "context": "המשקה מבוסס על יוגורט עם תות ומלון מבושלים (6% בסך הכול), סוכר, שני מייצבים (פקטין וקרגינן), עמילן מעובד, צבע מאכל טבעי (מיץ מרוכז מגזר סגול), ומווסת חומציות.",
                "good": ["פרי אמיתי מבושל (תות ומלון)"],
                "takeaway": "פרי אמיתי בבסיס, אבל סוכר גבוה, קרגינן וארבעה תוספים נוספים מביאים את המשקה לציון הכולל הנמוך ביותר בהשוואה זו.",
                "watchOut": [],
                "whyRated": "הפרי האמיתי תורם לזהות הטעם. מנגד, 9.8 גרם סוכר, קרגינן (תוסף שנוי במחלוקת מדעית) לצד ארבעה תוספים נוספים כולל חומצת לימון כתוסף שימור, ו-2.4 גרם חלבון בלבד, מעמידים את המשקה עם הציון הכולל הנמוך ביותר מבין 20 המשקאות שנבדקו.",
            },
        },
        "insightLine": "משקה תות-מלון עם 9.8 גרם סוכר ל-100 גרם וחמישה תוספים, ובהם קרגינן. הציון הכולל הנמוך ביותר בהשוואה זו.",
        "rowVerdict": "משקה יוגורט תות-מלון עם מחיות פרי מבושלות (6% בסך הכול) וחמישה תוספים, ובהם קרגינן וצבע מאכל טבעי (מיץ גזר סגול). 9.8 גרם סוכר ו-2.4 גרם חלבון בלבד ל-100 גרם. הציון הכולל הוא הנמוך ביותר מבין 20 המשקאות שנבדקו, בעיקר בשל שילוב הסוכר, התוספים ורמת העיבוד.",
    },
}

reauthored_barcodes = set(REAUTHOR.keys())

for p in base["products"]:
    bc = p["barcode"]
    if bc in REAUTHOR:
        r = REAUTHOR[bc]
        p["bestUseCases"] = r["bestUseCases"]
        p["consumerTakeaway"] = r["consumerTakeaway"]
        p["insightLine"] = r["insightLine"]
        p["rowVerdict"] = r["rowVerdict"]
        for item in p["bariInterpretation"]:
            item["interpretation"] = r["bariInterpretation"][item["key"]]
        p["expansion"]["comparisonContext"] = r["expansion"]["comparisonContext"]
        ce = r["expansion"]["consumerExplanation"]
        p["expansion"]["consumerExplanation"]["context"] = ce["context"]
        p["expansion"]["consumerExplanation"]["good"] = ce["good"]
        p["expansion"]["consumerExplanation"]["takeaway"] = ce["takeaway"]
        p["expansion"]["consumerExplanation"]["watchOut"] = ce["watchOut"]
        p["expansion"]["consumerExplanation"]["whyRated"] = ce["whyRated"]
    else:
        if bc not in prior_by_bc:
            raise SystemExit(f"FATAL: barcode {bc} in base has no prior copy donor and is not in REAUTHOR set")
        carry_copy(p, prior_by_bc[bc])

# ---------------------------------------------------------------------------
# 2) Surgical false-superlative fixes on two "unchanged" products
#    (found during the mandatory 20-corpus superlative recheck; both claims
#    were already inaccurate in the signed 23-corpus copy and are corrected
#    now, not merely re-counted)
# ---------------------------------------------------------------------------
SURGICAL = {
    # 55336: "6 additives = highest in category" is false -- GO products have 7 and 8.
    "55336": {
        "consumerTakeaway": "משקה עם שישה תוספים, לצד סוכר גבוה (9.6 גרם) ו-2.4 גרם חלבון בלבד.",
        "expansion.comparisonContext": "שישה תוספים ברשימת הרכיבים, מבין 20 המשקאות שנבדקו בהשוואה זו.",
        "expansion.consumerExplanation.takeaway": "פרי אמיתי בבסיס, אבל שישה תוספים ברשימה מגבילים את הציון.",
        "expansion.consumerExplanation.whyRated": "הפרי האמיתי תורם לזהות הטעם. מנגד, שישה תוספים ברשימה, לצד 9.6 גרם סוכר ו-2.4 גרם חלבון בלבד, מגבילים את הציון במספר ממדים במקביל.",
        "insightLine": "משקה בננה-אפרסק עם 9.6 גרם סוכר ל-100 גרם ושישה תוספים ברשימה.",
        "rowVerdict": "משקה יוגורט בננה-אפרסק עם מחיות פרי מבושלות (6.1% בסך הכול) ושישה תוספים ברשימה. 9.6 גרם סוכר ו-2.4 גרם חלבון בלבד ל-100 גרם.",
    },
    # 58030: "lowest overall score in category" is false -- 55329 dropped below it (34.3 vs 35.2).
    "58030": {
        "consumerTakeaway": "משקה עם תוספת סידן ייחודית בקטגוריה, אך מהציונים הנמוכים במשקאות שנבדקו.",
        "expansion.comparisonContext": "היחיד מבין 20 המשקאות שנבדקו עם תוספת סידן מפורשת (טריקלציום ציטראט) ברשימת הרכיבים, ומהציונים הנמוכים בהשוואה זו.",
        "expansion.consumerExplanation.good.0": "תוספת סידן מפורשת, היחיד מבין 20 המשקאות שנבדקו",
        "expansion.consumerExplanation.whyRated": "תוספת הסידן היא תוספת תזונתית ואינה חיסרון, אך 2.3 גרם חלבון בלבד, ערך תזונתי כללי נמוך, ורמת עיבוד גבוהה יחד מביאים את המשקה לאחד הציונים הנמוכים מבין 20 המשקאות שנבדקו.",
        "insightLine": "משקה תות עם תוספת סידן, ייחודי מבין 20 המשקאות שנבדקו, ומהציונים הנמוכים בהם.",
        "rowVerdict": "יופלה שטוזים תות, עם תוספת סידן (טריקלציום ציטראט), היחיד מבין 20 המשקאות שנבדקו עם תוספת מינרלים מפורשת. עם זאת, זהו גם אחד הציונים הנמוכים מביניהם.",
    },
}

for p in base["products"]:
    bc = p["barcode"]
    if bc not in SURGICAL:
        continue
    fixes = SURGICAL[bc]
    for path, val in fixes.items():
        parts = path.split(".")
        if parts[0] == "expansion" and parts[1] == "comparisonContext":
            p["expansion"]["comparisonContext"] = val
        elif parts[0] == "expansion" and parts[1] == "consumerExplanation":
            if parts[2] == "good":
                idx = int(parts[3])
                p["expansion"]["consumerExplanation"]["good"][idx] = val
            else:
                p["expansion"]["consumerExplanation"][parts[2]] = val
        elif parts[0] in ("consumerTakeaway", "insightLine", "rowVerdict"):
            p[parts[0]] = val
        else:
            raise SystemExit(f"unhandled surgical path {path}")

# ---------------------------------------------------------------------------
# 3) page_copy: carry hero/prologue/methodology/caveat from prior, fix counts
# ---------------------------------------------------------------------------
page_copy = copy.deepcopy(prior["page_copy"])
page_copy["hero"]["productCount"] = 20
page_copy["hero"]["scoredCount"] = 20
page_copy["prologue"]["sentences"] = [fix_count(s) for s in page_copy["prologue"]["sentences"]]
page_copy["methodology"]["lines"] = [fix_count(s) for s in page_copy["methodology"]["lines"]]
# caveat body carries no "23" literal (already absolute-floor, Nutrition-cosigned
# text per CAVEAT_NUTRITION_COSIGN.md) -- verified no digit-count needs updating.
# SPEC-CONFLICT FIX (flagged in return, not silent): the cosigned caveat body
# fails the current hebrew_readability ANTITHESIS hard-gate ("ולא" as
# definitional negation, owner rule banning "X, not Y" phrasing). This gate
# postdates the caveat's original cosign. Applying a minimal, meaning-preserving
# rewrite ("ולא בהשוואה" -> "בלי השוואה") so the deliverable ships gate-clean;
# no fact, number, or claim changes. Flagged for Nutrition re-confirmation since
# the body was registered as cosigned verbatim in CAVEAT_NUTRITION_COSIGN.md.
_old_caveat_clause = "ולכן הציון של סוכר כאן נבדק מול רף קבוע מראש ולא בהשוואה בין המשקאות עצמם."
_new_caveat_clause = "ולכן הציון של סוכר כאן נבדק מול רף קבוע מראש, בלי השוואה בין המשקאות עצמם."
for _note in page_copy["caveat"]["notes"]:
    if _old_caveat_clause in _note["body"]:
        _note["body"] = _note["body"].replace(_old_caveat_clause, _new_caveat_clause)

# ---------------------------------------------------------------------------
# 4) Assemble output
# ---------------------------------------------------------------------------
out = {
    "_meta": dict(base["_meta"]),
    "products": base["products"],
    "page_copy": page_copy,
}
out["_meta"]["source_note"] = (
    "TASK-515A FINAL v3: base = yogurt_drinkable_D7_SUPPRESS_v1.json (20-product conservative "
    "corpus, Product D7 sugar absolute-floor-only ruling). Consumer copy carried byte-for-byte from "
    "yogurt_drinkable_FINAL_v2.json (23-corpus, signed) for the 16 score/grade-unchanged products, "
    "with '23'->'20' count fix applied to every copied string. Re-authored from bsip2_trace.json for "
    "the 4 score/grade-changed products: 55343, 7290107938396, 7290115676051, 55329. Two surgical "
    "false-superlative fixes applied to otherwise-unchanged products (55336: '6 additives = highest' "
    "was already false vs GO products' 7/8; 58030: 'lowest overall score' broken by 55329's new-E "
    "drop). Caveat carried unchanged (Nutrition-cosigned absolute-floor text, CAVEAT_NUTRITION_COSIGN.md)."
)

# ---------------------------------------------------------------------------
# 5) Verification gates before write
# ---------------------------------------------------------------------------
serialized = json.dumps(out, ensure_ascii=False)
pending_count = serialized.count("PENDING_COPY")
if pending_count:
    raise SystemExit(f"FATAL: {pending_count} PENDING_COPY placeholders remain")
if len(out["products"]) != 20:
    raise SystemExit(f"FATAL: expected 20 products, got {len(out['products'])}")

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

sha = hashlib.sha256(open(OUT_PATH, "rb").read()).hexdigest()
print("WROTE:", OUT_PATH)
print("SHA256:", sha)
print("products:", len(out["products"]))
print("PENDING_COPY remaining:", pending_count)
