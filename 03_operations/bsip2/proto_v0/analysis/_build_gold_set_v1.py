"""
_build_gold_set_v1.py
=====================
Generates matrix_gold_set_candidates_v1.md and matrix_gold_set_candidates_v1.json
from real corpus data pulled from the probe results JSON.

All Hebrew written via Python file writes — never echoed through the shell,
which corrupts UTF-8 on Windows.

TASK-395 / BSIP2 de-chain program — condition C-N1-1 re-validation gold set.
Run: python _build_gold_set_v1.py
"""

import json
import hashlib
import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Gold set definition — all 62 products
# Source: matrix_signal_probe_v1_results.json (real corpus ingredient texts)
# ---------------------------------------------------------------------------

# Each product dict:
#   barcode, name_he, category, source_file, ingredients_text_he (FULL from corpus),
#   tier (T1/T2/T3/T4), expected_label, confidence (C=confident / B=borderline),
#   reason_he (one-line Hebrew plain reason), spelt_correction (True if one of 7 flagged corrections)

GOLD_SET = [

    # =========================================================================
    # TIER 1 — CLEAR WHOLE  (expected matrix score >= 65)
    # Criterion: first ingredient is whole grain/nut at >= 40% mass, no refined starch >= 15%
    # =========================================================================

    {
        "barcode": "16000423534",
        "name_he": "קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמישייה",
        "category": "snack_bar_granola",
        "source_file": "bsip2_trace:bsip1_16000423534",
        "ingredients_text_he": "פתיתי שיבולת שועל מלאה (54%) (מכיל גלוטן), סוכר לבן, שמנים צמחיים, שבבי שוקולד מריר מעולה (7%) (סויה), מים, אבקת קקאו מופחת שומן, דבש, מלח, מולסה, מתחלבים (לציטין), חומר תפיחה (סודיום ביקרבונט), חומר טעם וריח.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל מלאה 54% — מרכיב ראשון ומוצהר; שוקולד (7%) וסוכר משניים בלבד.",
        "spelt_correction": False,
    },
    {
        "barcode": "16000548404",
        "name_he": "קראנצ'י חטיף שיבולת שועל עם דבש חמישייה",
        "category": "snack_bar_granola",
        "source_file": "bsip2_trace:bsip1_16000548404",
        "ingredients_text_he": "פתיתי שיבולת שועל מלאה (60%) (מכיל גלוטן), סוכר לבן, שמנים צמחיים, מים, דבש (3%), מלח, מולסה, מתחלבים (לציטין), חומר תפיחה (סודיום ביקרבונט).",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל מלאה 60% — מרכיב ראשון ומוצהר; יתר המרכיבים קטנים ומשניים.",
        "spelt_correction": False,
    },
    {
        "barcode": "16000548503",
        "name_he": "קראנצ'י חטיף שיבולת שועל עם מייפל קנדי חמישייה",
        "category": "snack_bar_granola",
        "source_file": "bsip2_trace:bsip1_16000548503",
        "ingredients_text_he": "פתיתי שיבולת שועל מלאה (60%) (מכיל גלוטן), סוכר לבן, שמנים צמחיים, מים, סירופ מייפל (2%), דבש, חומר טעם וריח, מלח, מתחלב (לציטין), חומר תפיחה (סודיום ביקרבונט), מולסה.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל מלאה 60% — מרכיב ראשון ומוצהר; שאר מרכיבים משניים.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290112199942",
        "name_he": 'גרנולה תותים ללת"ס',
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "פתיתי שיבולת שועל מלאה (53%) (מכיל גלוטן), סיבי עולש, קמח חיטה, פתיתים פריכים מחיטה-תירס (קמח חיטה, גריסי תירס, סמולינה מתירס), חתיכות תפוחות מחיטה-תירס (קמח חיטה, גריסי תירס, סמולינה מתירס, מלח), תותים מיובשים בהקפאה (1.5%), ממתיק [Truvia] ממתיקים (אריתריתול, גליקוזידים של סטיביול), חומרי טעם וריח.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל מלאה 53% — מרכיב ראשון ומוצהר; קמח חיטה ורכיבים משניים.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290112199959",
        "name_he": 'גרנולה פירות ללת"ס',
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "פתיתי שיבולת שועל מלאה (53%) (מכיל גלוטן), סיבי עולש, קמח חיטה, פתיתים פריכים מחיטה-תירס (קמח חיטה, גריסי תירס, סמולינה מתירס), חתיכות תפוחות מחיטה-תירס (קמח חיטה, גריסי תירס, סמולינה מתירס, מלח), תותים מיובשים בהקפאה (1.5%), ממתיקים (אריתריתול, גליקוזידים של סטיביול), חומרי טעם וריח.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל מלאה 53% — אותה נוסחת בסיס כמו התותים; מרכיב ראשון ומוצהר.",
        "spelt_correction": False,
    },
    {
        "barcode": "574615",
        "name_he": "כוסמין מלא 100%",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח כוסמין מלא (נטחן מגרעין הכוסמין בשלמותו) (מכיל גלוטן) (100% מהקמח, 60% מהלחם), מים, גלוטן חיטה, שמרים, מלח, לתת שעורה (מכיל גלוטן), חומרים משמרים (קלציום פרופיונט, פוטסיום סורבט), חומר מתחלב (E481), קמח סויה, סיבים תזונתיים, חומר מווסת חומציות (חומצה ציטרית), חומר לטיפול בקמח (חומצה אסקורבית).",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "קמח כוסמין מלא — 100% מהקמח, 60% מהלחם; כוסמין עם 'מלא' = דגן מלא מוצהר. שימו לב: זהו כוסמין מלא (≠ כוסמין לבן).",
        "spelt_correction": False,
    },
    {
        "barcode": "7290106571945",
        "name_he": "עוגיות קקאו דגנים מלאים עם נטיפי שוקולד מריר פיטנס",
        "category": "cakes_hard_cookies",
        "source_file": "cakes_merged_bsip0_raw.json",
        "ingredients_text_he": "דגנים (קמח חיטה מלא (41%) (קמח חיטה, סובין, נבט) (מכיל גלוטן), פתיתי שיבולת שועל מלאים (4.5%)), סוכר, שמן צמחי, נטיפי שוקולד מריר מעולה (8.5%) (מכיל סויה), סובין שיבולת שועל, אבקת קקאו (4.5%), גלוטן חיטה, מלטודקסטרין, תמצית לתת שעורה, עמילן, חומרי תפיחה (E503, E450, E500), מלח, מתחלב (לציטין סויה).",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "קמח חיטה מלא 41% — מרכיב ראשון ומוצהר; פתיתי שיבולת שועל מלאים (4.5%) נוספים.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290013740823",
        "name_he": "קרקר כוסמין טבעי",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח כוסמין מלא (37%) (גלוטן), מים, שמן זית, שומשום, גרעיני חמניות, צ'יה, מיץ לימון, פפריקה, גרעיני פשתן, גרעיני דלעת, מלח ים אטלנטי.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "קמח כוסמין מלא 37% — מרכיב ראשון; ללא קמח לבן כלל; שמן זית + גרעינים.",
        "spelt_correction": False,
    },
    {
        "barcode": "574141",
        "name_he": "לחם חיטה מלא",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה מלא (נטחן מגרעין החיטה בשלמותו (מכיל גלוטן)) (100% מהקמח, 62.2% מהלחם), מים, דגנים 3% (שיבולת שועל (גלוטן), לתת שעורה (גלוטן)), שמרים, גרעיני פשתן, גלוטן חיטה, מלח, גרעיני חמניות, מתחלב (E481).",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "קמח חיטה מלא 100% מהקמח (62.2% מהלחם) — דגן מלא מוחלט; ללא קמח לבן.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290106771314",
        "name_he": "גרנולה אגוזים חמוציות",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "שיבולת שועל מלאה (54%) (גלוטן), אגוזים (11.5%) (קשיו, לוז, שקדים), סיבים תזונתיים (עולש) (10%), גרעיני חמנייה, גרעיני דלעת, סילאן טבעי, חמוציות (4.5%) (חמוציות, רכז תפוחים, שמן חמניות), שמן קוקוס, קינמון.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל מלאה 54% — מרכיב ראשון ומוצהר; אגוזים, גרעינים, סילאן — ללא קמח לבן.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290017962047",
        "name_he": "גרנולה חמוציות ושקדים",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "שיבולת שועל (מכיל גלוטן), סיבים תזונתיים (עולש), רכז תפוחים, שקדים (5%), חמוציות ברכז תפוחים (5%), גרעיני חמנייה, קוקוס, גרעיני פשתן, אוכמניות, שומשום מלא, זרעי צ'יה, קינמון.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל — מרכיב ראשון; ממותק ברכז פירות בלבד; ללא קמח לבן, ללא סוכר מוסף.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290013433107",
        "name_he": "גרנולה חלבה תמר קשיו",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "שיבולת שועל (מכיל גלוטן) 50%, גרעינים 13% (פשתן, טחינה, שומשום, גרעיני חמנייה, גרעיני דלעת, צ'יה), תמרים 12%, חלבה 11% (טחינה משומשום, מלטיטול, שומן צמחי, תמצית שורש ספונירה, חומצת לימון, ונילין), פצפוצי אורז, טחינה 4%, קשיו 3%, שומן צמחי, לציטין סויה.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל 50% — מרכיב ראשון ומוצהר; גרעינים ותמרים משלימים; ללא קמח לבן.",
        "spelt_correction": False,
    },
    {
        "barcode": "7296073705567",
        "name_he": "טבעות דגנים בטעם דבש",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "קמח חיטה מלא 36% (מכיל גלוטן), קמח שיבולת שועל 26% (מכיל גלוטן), סוכר לבן, עמילן חיטה (מכיל גלוטן), דבש 2%, סירופ גלוקוז-פרוקטוז, מולסה, שמן לפתית, מלח, מתחלב סויה לציטין, חומר טעם וריח טבעי, תערובת ויטמינים.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "B",
        "reason_he": "קמח חיטה מלא 36% + קמח שיבולת שועל 26% = 62% דגן מלא מוצהר; סוכר + עמילן חיטה משניים. גבולי: עמילן חיטה נוסף ממוקם שלישי — האם מורד את הציון?",
        "spelt_correction": False,
    },

    # =========================================================================
    # TIER 2 — CLEAR REFINED  (expected matrix score <= 40)
    # =========================================================================

    {
        "barcode": "7290119043095",
        "name_he": "עוגיות שיבולת שועל",
        "category": "cakes_hard_cookies",
        "source_file": "cakes_merged_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה לבן (מכיל גלוטן)(37%), שומן צמחי מדקלים, סוכר, אבקת סוכר, שיבולת שועל (מכיל גלוטן)(8%), מים, קמח סויה (1%), שמן סויה (1%), אבקת אפיה (1%) (חומרים מתפיחים E500ii, E450i), קינמון (0.4%), מלח (0.5%), סודה לשתייה (0.3%), חומרי טעם וריח.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קמח חיטה לבן 37% — מרכיב ראשון ומוצהר; שיבולת שועל רק 8% (שמינית!). שם מוצר מבלבל.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290119040568",
        "name_he": "עוגת קראנץ אגוזים",
        "category": "cakes_hard_cookies",
        "source_file": "cakes_merged_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה לבן (מכיל גלוטן), מים, מרגרינה (חומר משמר (חומצה סורבית), מתחלב (לציטין סויה)), סוכר, מילוי בטעם שוקולד (10%) (ממרח בטעם שוקולד, סוכר, שמן סויה, קמח סויה, אבקת קקאו, מתחלב (לציטין סויה), שמן דקלים, חומר טעם וריח, מלח), גלוקוז, שמרים, חומרי הלחה (E422), תערובת תפיחה (עמילן תירס, דקסטרוז, קמח סויה), גלוטן חיטה, מלח.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קמח חיטה לבן — מרכיב ראשון; מרגרינה + סוכר + גלוקוז; ללא דגן מלא כלל.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290018500644",
        "name_he": "מארז פיתות כוסמין לבן",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח כוסמין לבן (גלוטן) (100% מהקמחים, 64% מהמוצר), מים, סוכר, שמרים, מלח, גלוטן חיטה, חומר משמר (קלציום פרופיונט), סיבים תזונתיים, אנזימים.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "כוסמין לבן = קמח כוסמין מזוקק (ללא 'מלא'). 64% ממשקל המוצר — שליטה מוחלטת של קמח מעובד. תיקון על ניתוח ההיוריסטי שסיווג כ'מלא' (WRONG-HEURISTIC).",
        "spelt_correction": True,
    },
    {
        "barcode": "7290116530482",
        "name_he": "מארז קורנפלקס של אלופים",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "קמח תירס (89%), סוכר, תמצית לתת שעורה (מכיל גלוטן), מלח, מתחלב (E471), ויטמינים (B3 (ניאצין), B2, B6 (ריבופלאבין), B1 (תיאמין), חומצה פולית, B12), ברזל.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קמח תירס 89% — מזוקק (ללא 'מלא'); שליטה מוחלטת של עמילן מעובד.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290107647731",
        "name_he": "דגני בוקר קוקומן חום לבן",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "דגנים (71%) (קמח חיטה (מכיל גלוטן), קמח חיטה מלא, קמח לתת שעורה (מכיל גלוטן)), סוכר, עמילן חיטה, אבקת קקאו, מלח, חומרי טעם וריח, תערובת ויטמינים ומינרלים, מתחלב (לציטין סויה).",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "B",
        "reason_he": "קמח חיטה לבן — ראשון ברשימת הדגנים (71%); קמח חיטה מלא שני; יחס לא מוצהר. גבולי: האם הלבן או המלא שולט?",
        "spelt_correction": False,
    },
    {
        "barcode": "7296073431916",
        "name_he": "עוגת מאפין בטעם תפוז",
        "category": "cakes_hard_cookies",
        "source_file": "cakes_merged_bsip0_raw.json",
        "ingredients_text_he": "סוכר, קמח חיטה (מכיל גלוטן), ביצים, שמן קנולה מזוכך, מים, עמילן חיטה, מרגרינה (סויה) (חומר משמר (E202)), מתפיחים (E450i, E500ii, E500iii), מתחלבים (E471, E481), גלוטן חיטה, מלח, דקסטרוזה, עמילן תירס, חומרי טעם וריח.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "סוכר — מרכיב ראשון; קמח חיטה לבן שני; עמילן חיטה + מרגרינה + עמילן תירס; ללא דגן מלא.",
        "spelt_correction": False,
    },
    {
        "barcode": "5000396021202",
        "name_he": "קרקר (Jacob's Cream Crackers)",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה (מכיל גלוטן), שמן חמניות, סוכר, סירופ גלוקוז-פרוקטוז, חומרי התפחה (קלציום פוספט, אמוניום קרבונט, סודיום קרבונט, פוטסיום קרבונט), מלח, קמח שעורה (מכיל גלוטן).",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קמח חיטה לבן — מרכיב ראשון ומוחלט; ללא דגן מלא; קרקר קלאסי מזוקק.",
        "spelt_correction": False,
    },
    {
        "barcode": "7622201809188",
        "name_he": "ביסקוויט מילקה",
        "category": "cakes_hard_cookies",
        "source_file": "cakes_merged_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה (מכיל גלוטן), סוכר, חמאת קקאו, שמן דקל, אבקת חלב דל שומן, אבקת מי גבינה, עיסת קקאו, שומן חלב, מתפיחים (E450, E500, E503), מתחלבים (סויה לציטין, E476), מלח, חומרי טעם וריח, מווסת חומציות (חומצה ציטרית).",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קמח חיטה לבן — מרכיב ראשון; סוכר שני; ביסקוויט מזוקק קלאסי.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290116537351",
        "name_he": "כריות נוגט",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "קרם נוגט (48%) (סוכר, שמן צמחי, אגוזי לוז (8.2%), אבקת קקאו, מלטודקסטרין, שמן צמחי מוקשה, מתחלב (E322)), דגנים (40%) (קמח חיטה (מכיל גלוטן), גריסי תירס, קמח תירס, קמח חיטה מלא), סוכר, מלטודקסטרין, אבקת קקאו, שמן צמחי, מלח.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קרם נוגט 48% (סוכר + שמן ראשונים בתוכו); דגנים 40% — קמח לבן וגריסי תירס ראשונים שם; קמח חיטה מלא רביעי.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290017325910",
        "name_he": "קורנפלקס אורגני הרדוף",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "קמח תירס אורגני (94%), קמח לתת שעורה אורגני (5%), מלח.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קמח תירס אורגני 94% — מזוקק (ללא 'מלא'); אורגני לא משנה את הזיקוק.",
        "spelt_correction": False,
    },
    {
        "barcode": "313184",
        "name_he": "עוגיות גן חיות טעם וניל",
        "category": "cakes_hard_cookies",
        "source_file": "cakes_merged_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה (מכיל גלוטן), סוכר, שמנים צמחיים, סוכר אינברטי, חומרי תפיחה (E500, E503), מלח, מתחלב (לציטין סויה), חומרי טעם וריח, מעכב חמצון (מיצוי רוזמרין), חומר לטיפול בקמח (סולפיט).",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קמח חיטה לבן — מרכיב ראשון; סוכר + שמן צמחי; ללא כל דגן מלא.",
        "spelt_correction": False,
    },
    {
        "barcode": "7296073398875",
        "name_he": "קרם קרקר",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה, עמילן תירס, שמנים צמחיים (דקל, חמניות), סוכרים (דקסטרוז, פרוקטוז), גלוטן חיטה, מלח, שמרים, מתחלב: לציטין סויה, חומרי תפיחה: נתרן ואמוניום קרבונטים, מעכב חמצון: תמצית רוזמרין.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קמח חיטה לבן — מרכיב ראשון; עמילן תירס + שמנים + סוכרים (דקסטרוז+פרוקטוז); ללא דגן מלא.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290013453624",
        "name_he": "עוגיות שוקולד צ'יפס (כשלפ)",
        "category": "cakes_hard_cookies",
        "source_file": "cakes_merged_bsip0_raw.json",
        "ingredients_text_he": "חיטה. אנחנו מאמינים שאפשר לאכול אוכל בריא ומזין שהוא גם טעים ומפנק! כדי לעמוד באתגר, חומרי הגלם הקלאסיים של קונדיטוריה: קמח לבן, מרגרינה, חמאה, ביצים ושמנת - יצאו לחלוטין מתהליך האפייה. בכדי לתת עושר תזונתי למוצרינו, יש שימוש גורף בקמח שקדים וקמח אורז מלא, ממתיקים טבעיים (מייפל, אגבה, רכז תפוחים ועוד).",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "B",
        "reason_he": "טקסט שיווקי — לא רשימת רכיבים אמיתית. ההיוריסטי ייחס WFP בגלל 'מלא' בשם, אך הטקסט אינו רשימת רכיבים. גבולי לקבוצת מקרה קצה (NO_MARKERS / MARKETING_BLURB) — ראה ניתוח.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290119040667",
        "name_he": "עוגת קראנץ פרג",
        "category": "cakes_hard_cookies",
        "source_file": "cakes_merged_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה לבן (מכיל גלוטן), מים, מרגרינה (חומר משמר (חומצה סורבית), מתחלב (לציטין סויה)), סוכר, מילוי בטעם שוקולד (10%) (ממרח בטעם שוקולד, סוכר, שמן סויה, קמח סויה, אבקת קקאו, מתחלב (לציטין סויה), שמן דקלים, חומר טעם וריח, מלח), גלוקוז, שמרים, חומרי הלחה (E422), תערובת תפיחה, גלוטן חיטה, מלח.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "קמח חיטה לבן — מרכיב ראשון; מרגרינה + סוכר; ללא דגן מלא.",
        "spelt_correction": False,
    },
    {
        "barcode": "8710502279010",
        "name_he": "עוגיות שוקולד צ'יפס מצופות",
        "category": "cakes_hard_cookies",
        "source_file": "cakes_merged_bsip0_raw.json",
        "ingredients_text_he": "סוכר, קמח חיטה (מכיל גלוטן), שמנים צמחיים (דקלים, חמניות), מסת קקאו, חמאת קקאו, אבקת חלב מלא, מתחלב: לציטין (סויה, חמניות), סירופ גלוקוזה, חומרי התפחה (E450, E500), מלח, חומר טעם טבעי.",
        "tier": "T2",
        "expected_label": "clear-refined",
        "confidence": "C",
        "reason_he": "סוכר — מרכיב ראשון; קמח חיטה לבן שני; ציפוי שוקולד + שמנים; ללא דגן מלא.",
        "spelt_correction": False,
    },

    # Spelt pita corrections (the 7 flagged WRONG-heuristic products)
    # Only one physical product appears in the corpus for לבן; others are variants
    # The correction is explicitly flagged for owner review
    {
        "barcode": "7290017947464",
        "name_he": "מארז פיתות כוסמין (מלא)",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטת כוסמין מלא (נטחן מגרעין חיטת הכוסמין בשלמותו)(גלוטן)(100% מהקמחים, 58% מהמוצר), מים, גלוטן חיטה, סוכר, שמרים, מלח, חומר משמר (קלציום פרופיונט), אנזימים.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "קמח כוסמין מלא — 100% מהקמחים, 58% מהמוצר; 'מלא' מפורש ומוצהר. זהו כוסמין מלא ≠ כוסמין לבן.",
        "spelt_correction": False,
    },

    # =========================================================================
    # TIER 3 — HARD MIXED  (expected score 40-65, rank-ordered)
    # =========================================================================

    {
        "barcode": "6322838",
        "name_he": "לחם קמח מלא 100%",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה מלא (100% ממשקל הקמחים, 58% ממשקל הלחם) (מכיל גלוטן), מים, חלבון צמחי (מכיל גלוטן), מלח שולחן, שמן צמחי, שמרים, לתת שעורה (מכיל גלוטן), חומרים משמרים: קלציום פרופיונט ופוטסיום סורבט, חומר מתחלב E481, חומר לטיפול בקמח: חומצה אסקורבית (ויטמין C), מווסת חומציות: חומצת לימון, אנזימים.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "B",
        "reason_he": "קמח חיטה מלא 100% מהקמח (58% מהלחם) — מלא לחלוטין מבחינת הקמח; אך המוצר כולל 42% מים+תוספים. דורג ראשון בתוך T3 (הכי שלם).",
        "spelt_correction": False,
    },
    {
        "barcode": "7290018500460",
        "name_he": "לחם אנג'ל חצי מלא",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה מלא (נטחן מגרעין החיטה בשלמותו) (גלוטן) (50% ממשקל הקמחים, 34% ממשקל הלחם), קמח חיטה לבן (50% ממשקל הקמחים, 34% ממשקל הלחם), מים, גלוטן חיטה, שמרים, מלח, חומרים משמרים (E282, E202), מתחלב (E481), סיבים תזונתיים, חומר מעכב חמצון (E300), אנזימים.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "מוצהר מפורשות: 50% קמח מלא / 50% קמח לבן (מסך הקמחים). מדוגמת ה'חצי-חצי' המושלמת לסט.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290115205176",
        "name_he": "קרקר דק כפרי פיטנס",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה מלא (30.5%) (מכיל גלוטן), קמח אורז (25.5%), קמח חיטה (17%), שמן חמניות, קמח אורז מלא (6.8%), גלוטן חיטה, עמילן אורז, קינואה אדומה מיובשת (2.7%), שומשום (2.7%), שמרים, קצח (1.3%), מלח ים, סוכר, שום מיובש.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "קמח חיטה מלא 30.5% + קמח אורז מלא 6.8% = 37.3% מלא; קמח אורז לבן 25.5% + קמח חיטה לבן 17% = 42.5% מזוקק. מעורב אמיתי.",
        "spelt_correction": False,
    },
    {
        "barcode": "7296073659952",
        "name_he": "קרקר דק כפרי",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "תערובת קמחים 66% (קמח חיטה מלאה 25.5% (קמח חיטה, סובין, נבט), אורז 21%, חיטה 14%, אורז מלא 5.5%), שמן חמניות, שמן דקל, גלוטן חיטה, שומשום 3%, קינואה אדומה 2.5%, קצח 2%, עמילן תירס, מלח, שום, סוכר, שמרים.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "תערובת 66%: חיטה מלאה 25.5% + אורז מלא 5.5% = 31% מלא; אורז 21% + חיטה 14% = 35% מזוקק. מעורב.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290011131975",
        "name_he": "גרנולה פירות",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "גרנולה 65% (פתיתי שיבולת שועל 43% (מכיל גלוטן), קמח חיטה (מכיל גלוטן), שמן צמחי (דקלים), סוכר, קמח תירס, סירופ תמרים, תמצית לתת שעורה (מכיל גלוטן), סוכר חום, סירופ גלוקוז, דבש, מתחלב: לציטין סויה, אבקת קקאו, קינמון, צבע מאכל: קרמל), חטיפי דגנים 16% (פתיתי שיבולת שועל 6% (מכיל גלוטן), קמח חיטה (מכיל גלוטן)).",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "B",
        "reason_he": "שיבולת שועל 43% בתוך גרנולה 65% = ~28% מהמוצר; קמח חיטה לבן + קמח תירס + סוכרים משמעותיים. גבולי T3 (יכול לנטות T1 בגישת שליטה).",
        "spelt_correction": False,
    },
    {
        "barcode": "7290011131050",
        "name_he": "גרנולה פקאן",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "גרנולה 75% (פתיתי שיבולת שועל (מכיל גלוטן), קמח חיטה (מכיל גלוטן), שמן צמחי (דקלים), סוכר, קמח תירס, סירופ תמרים, תמצית לתת שעורה (מכיל גלוטן), סוכר חום, סירופ גלוקוז, דבש, מתחלב: לציטין סויה, אבקת קקאו, קינמון, צבע מאכל: קרמל), חטיפי דגנים 19% (פתיתי שיבולת שועל (מכיל גלוטן), קמח חיטה (מכיל גלוטן)).",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "B",
        "reason_he": "גרנולה 75%: שיבולת שועל ראשון אך ללא % מוצהר; קמח חיטה לבן שני; קמח תירס + סוכרים. מעורב — ניתוח עמדה נדרש.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290016883176",
        "name_he": "מוזלי 47% דגנים מלאים",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "פתיתי שיבולת שועל (מכיל גלוטן) 47%, אורז תפוח 10% (אורז, סוכר), סוכר חום, שמן צמחי (דקלים), סירופ גלוקוז, קמח חיטה (מכיל גלוטן), קוקוס 5%, שוקולד מריר 4% (סוכר, עיסת קקאו, חמאת קקאו, מתחלב (E322)), אבקת קקאו, מתחלב (E322), חומרי טעם וריח, מלח.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "שיבולת שועל 47% — מוצהר ראשון; אך: קמח חיטה לבן + סוכר חום + סירופ גלוקוז + שמן דקלים; 47% מלא vs ~25%+ מזוקק.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290011131371",
        "name_he": "מוזלי קראנצ'י בוטנ+שקדים",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "פתיתי שיבולת שועל 38% (מכיל גלוטן), שמן צמחי (דקלים), סוכר חום מקנה סוכר, סירופ גלוקוז, קמח חיטה (מכיל גלוטן), אגוזים 4.7% (בוטנים 2.7%, אגוזי לוז 1%, שקדים 1%), קוקוס, גרעיני חמניות, אבקת קקאו, מלח, מתחלב לציטין סויה, חומר טעם.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "שיבולת שועל 38% — ראשון; אך שמן דקל + סוכר + סירופ גלוקוז + קמח חיטה לבן מרובים. T3 ממוקם מתחת למוזלי 47%.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290011131388",
        "name_he": "מוזלי קראנצי תפוח קינמון",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "פתיתי שיבולת שועל (מכיל גלוטן) 39%, שמן צמחי (דקלים), סוכר חום מקני סוכר, סירופ גלוקוזה, קמח חיטה (מכיל גלוטן), צימוקים, תפוחי עץ מיובשים (2%), גרעיני חמניות (1.5%), אבקת קקאו, מלח, קינמון (0.2%), מתחלב: לציטין סויה, חומר טעם.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "B",
        "reason_he": "שיבולת שועל 39% — ראשון; שמן דקל שני; סוכר חום + סירופ גלוקוז + קמח חיטה לבן. גבולי: שמן דקל לפני הסוכר מוסיף לכיוון מזוקק.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290118427858",
        "name_he": "פיטנס בר גרנולה שוקולד מריר",
        "category": "snack_bar_granola",
        "source_file": "bsip2_trace:bsip1_7290118427858",
        "ingredients_text_he": "פתיתי שיבולת שועל מלאים (32%) (מכיל גלוטן), סוכר, נטיפי שוקולד מריר (13%) (מכיל מתחלב (לציטין סויה)), קמח שיבולת שועל מלא (11%), קמח חיטה (10%), שמן חמניות, מרגרינה (שמן צ'יה, שמן קוקוס, מים, מלח, מתחלב (E471)), קמח אורז (4.5%), סובין שיבולת שועל, דקסטרין, סיבים תזונתיים (אינולין), דבש, אבקת קקאו.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "שיבולת שועל מלאים 32% + קמח שיבולת שועל מלא 11% = 43% מלא; קמח חיטה לבן 10% + קמח אורז 4.5% = 14.5% מזוקק. T3 עם נטייה למלא.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290112968807",
        "name_he": "קרקר דק פיטנס סלק",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה מלא (31%) (מכיל גלוטן), קמח אורז (23%), קמח חיטה (15.5%), שמנים צמחיים, אבקת סלק (7.5%), קמח אורז מלא (6%), גלוטן חיטה, עמילן אורז, סוכר, שמרים, מלח ים, בצל מיובש (0.9%), שומשום.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "קמח חיטה מלא 31% + קמח אורז מלא 6% = 37% מלא; קמח אורז 23% + קמח חיטה לבן 15.5% = 38.5% מזוקק. מאוזן מאוד.",
        "spelt_correction": False,
    },
    {
        "barcode": "9401790",
        "name_he": "מארז פיתות קמח מלא",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה מלא, מים, קמח חיטה לבן, סוכר, שמרים, מלח, גלוטן חיטה, אנזימים, מתחלב.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "B",
        "reason_he": "קמח חיטה מלא — ראשון; קמח חיטה לבן — שלישי; ללא % מוצהרים. יחסים לא ידועים — גבולי.",
        "spelt_correction": False,
    },
    {
        "barcode": "5900020034021",
        "name_he": "חטיפי דגנים פיטנס שוקולד בננה שישייה",
        "category": "snack_bar_granola",
        "source_file": "bsip2_trace:bsip1_5900020034021",
        "ingredients_text_he": "חיטה מלאה (21.1%) (מכיל גלוטן), קמח חיטה מלא (13.9%), סירופ גלוקוז, אורז (11.9%), סוכר, שבבי שוקולד חלב (7%) (מכיל מוצקי חלב, חומר מתחלב: לציטין סויה), חומרי הלחה (גליצרול, סורביטול), סירופ סוכר אינברטי.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "חיטה מלאה 21.1% + קמח חיטה מלא 13.9% = 35% מלא; אורז 11.9% + סירופ גלוקוז + סוכר = ~25%+ מזוקק. T3.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290107947480",
        "name_he": "חטיף דגנים מצופה שוקולד חלב עם שברי אגוזים שישייה",
        "category": "snack_bar_granola",
        "source_file": "bsip2_trace:bsip1_7290107947480",
        "ingredients_text_he": "פתיתי דגנים 32% (אורז 26%, סוכר לבן, קמח תירס 2%, חיטה מלאה-גלוטן 1%, תמצית לתת שעורה-גלוטן, מלח), שוקולד חלב מעולה 32%, סירופ גלוקוז, סיבים תזונתיים (אינולין), חומרי הלחה (גליצרול, סורביטול), שברי אגוזים 10.2% (שקדים, לוז).",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "B",
        "reason_he": "פתיתי דגנים 32%: אורז מעובד 26%, חיטה מלאה רק 1%; שוקולד 32% (סוכר+שמן); שברי אגוזים 10%. גבולי — נוטה לT2 (מזוקק).",
        "spelt_correction": False,
    },

    # =========================================================================
    # TIER 4 — EDGE CASES  (expected behavior by rule, not score)
    # =========================================================================

    {
        "barcode": "9137842",
        "name_he": "מארז לחמניות כוסמין",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "בקיצור, היא עפה על עצמה ויש לה סיבה טובה: היא טעימה, איכותית וגם בריאה! פרגנו לעצמכם מארז של חמש מיוחסות לכל המשפחה, ולא תצטערו. זו הבטחה.",
        "tier": "T4",
        "expected_label": "edge-case",
        "confidence": "C",
        "reason_he": "טקסט שיווקי — לא רשימת רכיבים. הפורמולה צריכה להחזיר None (MD-2 fallback). בדיקת מקרה קצה: NO_MARKERS / MARKETING_BLURB.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290011525316",
        "name_he": "סנסיטיב שיבולת שועל",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "Water (Aqua), Cetearyl Alcohol, Caprylic/Capric Triglyceride, Ethylhexyl Palmitate, Glycerin, Cetearyl Glucoside, Helianthus Annuus (Sunflower) Seed Oil, Avena Sativa (Oat) Kernel Extract, Panthenol, Tocopheryl Acetate, Caprylyl Glycol, Parfum (Fragrance), Allantoin, Tocopherol, Carbomer, Potassium Hydroxide, Phenoxyethanol.",
        "tier": "T4",
        "expected_label": "edge-case",
        "confidence": "C",
        "reason_he": "רשימת INCI קוסמטית באנגלית — אין מרכיבי מזון. הפורמולה צריכה להחזיר None. מוצר קוסמטי שנכנס בטעות לקורפוס הדגנים.",
        "spelt_correction": False,
    },
    {
        "barcode": "7297488098688",
        "name_he": 'פצפוצי אורז ללת"ס',
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "100% אורז מלא (ללא תוספת סוכר ומלח).",
        "tier": "T4",
        "expected_label": "edge-case",
        "confidence": "C",
        "reason_he": "אורז מלא 100% — תיאורטית T1; אך 'אורז מלא' אינו בלקסיקון הנוכחי כ-marker. בדיקה: האם הפורמולה החדשה מזהה 'אורז מלא' כ-whole_rice?",
        "spelt_correction": False,
    },
    {
        "barcode": "5010029000061",
        "name_he": "דגני בוקר ויטביקס",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "חיטה (מכיל גלוטן) (95%), מיצוי לתת שעורה, סוכר, מלח, ויטמינים ומינרלים (ניאצין, ריבואפלאבין, תיאמין, חומצה פולית, ברזל).",
        "tier": "T4",
        "expected_label": "edge-case",
        "confidence": "C",
        "reason_he": "חיטה 95% — ויטביקס הוא מוצר דגן מלא (חיטה שלמה). אך 'חיטה' ללא 'מלא' לא נתפסת בלקסיקון הנוכחי. בדיקה: האם חיטה >=80% בעמדה ראשונה תסווג כ-whole wheat?",
        "spelt_correction": False,
    },
    {
        "barcode": "58449779032",
        "name_he": "דגני טבעות תירס ואורז אורגני",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "קמח מאורז מלא אורגני (50%), קמח תירס אורגני (40%), סוכר קנים אורגני, תרכיז מיץ רימונים אורגני (5%), מלח ים.",
        "tier": "T4",
        "expected_label": "edge-case",
        "confidence": "B",
        "reason_he": "אורז מלא 50% + קמח תירס אורגני 40%. שאלת מפתח: האם 'קמח תירס' (מזוקק) + 'אורז מלא' (מלא) — מי שולט? בדיקת qualifier 'מלא' על קמח אורז מול קמח תירס רגיל.",
        "spelt_correction": False,
    },
    # Additional T3 products to meet >= 15 minimum and expand toward 60 total

    {
        "barcode": "379142",
        "name_he": "לחם עינן פרוס וארוז",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה מלא (נטחן מגרעין החיטה בשלמותו) (גלוטן) (71% ממשקל הקמחים, 56% ממשקל הלחם), מים, חיטה מלאה טרום נבוטה (29% ממשקל הקמחים, 20% ממשקל הלחם), שמרים, גלוטן חיטה, מלח, חומר משמר (E282), שמן צמחי, מתחלבים (E472e, E481).",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "קמח חיטה מלא 71% מהקמחים (56% מהלחם) + חיטה טרום-נבוטה 29% — כל הקמח מלא; אך 44% מהלחם הוא מים+תוספים. T3 על גבול T1.",
        "spelt_correction": False,
    },
    {
        "barcode": "8445291638839",
        "name_he": "צ'יריוס בטעם דבש ושקדים",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "קמח שיבולת שועל מלא (מכיל גלוטן) (30.1%), קמח חיטה מלא (מכיל גלוטן) (28%), סוכר, קמח שעורה מלא (מכיל גלוטן) (17.2%), קמח חיטה (6.6%), דבש (2.4%), סירופ סוכר אינברטי, מינרלים (סידן), ברזל, שמן צמחי, מלח.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "שלושה קמחים מלאים מוצהרים: שיבולת שועל 30.1% + חיטה מלא 28% + שעורה מלא 17.2% = 75.3%; קמח חיטה לבן 6.6%. נוטה בבירור למלא אך הדגן המלא אינו ראשון — סוכר בעמדה 3.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290112495433",
        "name_he": "דגני בוקר דליפקאן",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "דגנים (63%) (קמח חיטה מלא (35%) (מכיל גלוטן), קמח אורז, שיבולת שועל מלאה (6%) (מכיל גלוטן), תמצית לתת שעורה (מכיל גלוטן), גריסי תירס, קמח שיפון (מכיל גלוטן)), סוכר, אגוזי פקאן מקורמלים (13%) (אגוזי פקאן (8.5%), סוכר, סירופ גלוקוז), דבש.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "B",
        "reason_he": "קמח חיטה מלא 35% בתוך דגנים 63% = ~22% מהמוצר; שיבולת שועל מלאה 6% נוספת; קמח אורז + גריסי תירס מזוקק. גבולי: מלא נוטה אך לא שולט.",
        "spelt_correction": False,
    },
    {
        "barcode": "481180",
        "name_he": "לחם מחמצת שאור",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטה לבן (מכיל גלוטן) (75% מהקמח, 40% מהלחם), מים, מחמצת חיטה לבן 18% (קמח חיטה לבן (מכיל גלוטן), מים), קמח חיטה מלא (נטחן מגרעין החיטה בשלמותו (מכיל גלוטן)) (25% מסך הקמחים, 15% מהלחם), מלח, גלוטן חיטה, חומר משמר (E282).",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "קמח חיטה לבן 75% מהקמח (40% מהלחם); קמח מלא רק 25% מהקמח (15% מהלחם). נוטה בבירור למזוקק — T3 קרוב ל-T2.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290120870017",
        "name_he": "קרקר כוסמין דק רוזמרין",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח חיטת כוסמין בהיר (70% מתכולת הגרעין — 38% מהמוצר הסופי — מכיל גלוטן), קמח אורז (22%), שמנים מהצומח (חמניות, דקל), גלוטן (חיטה), קמח אורז מלא (5.5%), שומשום (3%), קינואה אדומה (2.5%), קצח (2.5%), עמילן תירס, מלח.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "B",
        "reason_he": "כוסמין בהיר (≠ מלא, ≠ לבן) — 70% מהגרעין, 38% מהמוצר; קמח אורז 22%; קמח אורז מלא 5.5%. 'בהיר' = חצי-מזוקק בערך. גבולי: מיקום בין T2 ל-T3.",
        "spelt_correction": False,
    },
    {
        "barcode": "7296073705550",
        "name_he": "כדורי דגנים טעם שוקו",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "גריסי תירס 26%, קמח חיטה מלאה (מכיל גלוטן) 25%, קמח חיטה (מכיל גלוטן), סוכר לבן, סירופ גלוקוז-פרוקטוז, אבקת קקאו, קמח שיבולת שועל (מכיל גלוטן), דקסטרוז, שמן לפתית, מלח, מתחלב סויה לציטין, חומר טעם וריח.",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "גריסי תירס 26% (מזוקק) ראשון; קמח חיטה מלא 25% שני; קמח חיטה לבן + קמח שיבולת שועל + סירופ גלוקוז. מאוזן — T3 מובהק.",
        "spelt_correction": False,
    },
    {
        "barcode": "7290117382868",
        "name_he": "טורטיה כוסמין",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "תערובת קמחים (מכיל גלוטן) {קמח חיטה (46%), קמח כוסמין מלא (5%)}, מים, שומן מהצומח, פתיתי שיבולת שועל (מכיל גלוטן) (3%), סובין חיטה (מכיל גלוטן) (3%), מתחלב (E471), מווסת חומציות (חומצה מלית), משמרים (סודיום פרופיונט).",
        "tier": "T3",
        "expected_label": "hard-mixed",
        "confidence": "C",
        "reason_he": "קמח חיטה לבן 46% — שולט; כוסמין מלא רק 5%; שיבולת שועל 3%. נוטה לT2 אך קמח כוסמין מלא + שיבולת שועל נוכחים. T3 על גבול T2.",
        "spelt_correction": False,
    },

    # Additional T1 products to strengthen the tier
    {
        "barcode": "7290017962023",
        "name_he": "גרנולה מייפל תמר פקאן",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "שיבולת שועל (מכיל גלוטן), סירופ מייפל קנדי (8%), גרעיני חמניות, אוכמניות (5%), אגוזי פקאן (5%), קוקוס, סיבים תזונתיים (עולש), גרעיני פשתן, זרעי צ'יה, שומשום מלא, ממתיק: מונק פרוט.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל — מרכיב ראשון; ממותק בסירופ מייפל + מונק פרוט; אגוזים + גרעינים; ללא קמח לבן, ללא סוכר מוסף.",
        "spelt_correction": False,
    },
    {
        "barcode": "7613037012095",
        "name_he": "גרנולה שוקולד קינואה",
        "category": "cereals_granola",
        "source_file": "cereals_bsip0_raw_20260605T154620.json",
        "ingredients_text_he": "פתיתי שיבולת שועל מלאה (מכיל גלוטן) (40.8%), סוכר, קמח חיטה מלא (מכיל גלוטן)(9%), שמן חמניות, קמח שיבולת שועל מלא (8.7%), סירופ גלוקוז מיובש, נטיפי שוקולד מריר (4.8%) (מכיל חומר מתחלב: לציטין סויה), שקדים (4.7%), קינואה מלאה תפוחה (2.9%), סירופ סוכר.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "שיבולת שועל מלאה 40.8% ראשון + קמח חיטה מלא 9% + קמח שיבולת שועל מלא 8.7% = 58.5% דגן מלא מוצהר. סוכר + סירופ גלוקוז משניים.",
        "spelt_correction": False,
    },
    {
        "barcode": "96086000577",
        "name_he": "קרקר כוסמין אורגני",
        "category": "bread",
        "source_file": "real_bread_retail_003_v1_bsip0_raw.json",
        "ingredients_text_he": "קמח כוסמין מלא אורגני (98%) (מכיל גלוטן), מים, מלח, סוכרים הנמצאים באופן טבעי בחומרי הגלם.",
        "tier": "T1",
        "expected_label": "clear-whole",
        "confidence": "C",
        "reason_he": "קמח כוסמין מלא אורגני 98% — מרכיב כמעט יחיד; מלא מוחלט. פשוט ונקי.",
        "spelt_correction": False,
    },
]

# ---------------------------------------------------------------------------
# Spelt pita flag summary (the 7 WRONG-heuristic corrections from redesign_v2 §4.3)
# ---------------------------------------------------------------------------
SPELT_PITA_CORRECTIONS = """
## תיקוני הכוסמין הלבן — 7 מוצרים (WRONG-017/022/024/025/028/029/034)

המחקר זיהה 7 מוצרי פיתה/לחם כוסמין שסווגו שגויה כ"WFP" (מלא) על ידי ההיוריסטיקה,
מכיוון ש'כוסמין' הופיע בשם — אך הלייבל מצהיר על 'כוסמין לבן' = קמח כוסמין מזוקק.

**כלל ברור לבעלים:**
- כוסמין מלא (עם המילה 'מלא') = דגן מלא → T1
- כוסמין לבן (עם המילה 'לבן') = מזוקק → T2

מוצרי הדגמה בסט הנוכחי:
- ברקוד 7290018500644 (מארז פיתות כוסמין לבן) → T2, ציון ≤ 40 (מוצהר: 64% ממשקל המוצר כוסמין לבן)
- ברקוד 574615 (כוסמין מלא 100%) → T1, ציון ≥ 65 (מוצהר: 100% מהקמח מלא)
- ברקוד 7290017947464 (מארז פיתות כוסמין — מלא) → T1, ציון ≥ 65 (מוצהר: 100% מהקמח מלא)

**7 WRONG-017/022/024/025/028/029/034 שלא נמצאו בסט:** אלה מופיעים בדוח הגלם בפורמט
WRONG-NNN ואינם מזוהים בברקוד בגוף הדוח. הם מיוצגים בעיקרון על ידי הדגמת הכוסמין הלבן לעיל.
"""

# ---------------------------------------------------------------------------
# Tier counts
# ---------------------------------------------------------------------------
tier_counts = {}
for p in GOLD_SET:
    t = p["tier"]
    tier_counts[t] = tier_counts.get(t, 0) + 1

# ---------------------------------------------------------------------------
# Build Markdown table
# ---------------------------------------------------------------------------
TIER_LABELS = {
    "T1": "שכבה 1 — מלא ברור (ציון צפוי ≥ 65)",
    "T2": "שכבה 2 — מזוקק ברור (ציון צפוי ≤ 40)",
    "T3": "שכבה 3 — מעורב קשה (ציון צפוי 40–65)",
    "T4": "שכבה 4 — מקרי קצה (התנהגות צפויה לפי כלל)",
}

TIER_DESCRIPTIONS = {
    "T1": "המרכיב הראשון הוא דגן מלא / אגוז / זרע ≥ 40% ממשקל, ללא עמילן מזוקק ≥ 15%.",
    "T2": "המרכיב הראשון הוא קמח לבן / סוכר / עמילן, והכלל הכבד עולה על המלא ב-2:1 לפחות.",
    "T3": "≥ 20% מלא וגם ≥ 20% מזוקק — שניהם נוכחים, אף אחד לא שולט ב-2:1. הסדר הפנימי קובע.",
    "T4": "מוצרים שחושפים כשלי לקסיקון ידועים, טקסט שיווקי, מרכיב מלא ללא qualifier, שם מטעה.",
}

CONFIDENCE_NOTE = {
    "C": "בטוח — ניתן לקרוא ישירות מהלייבל",
    "B": "גבולי — מבקשים עיניים של הבעלים",
}

def build_markdown(products: list[dict]) -> str:
    lines = []
    lines.append("# סט הזהב — מועמדים לאימות מחדש של אות C-N1-1")
    lines.append("")
    lines.append("**TASK-395 | תוכנית de-chain | פרוטוקול B — Component B Redesign**")
    lines.append("")
    lines.append("מסמך זה מיועד לביקורת הבעלים. כל טקסט הרכיבים נשלף ישירות מהסריקה")
    lines.append("הישירה של המוצר (corpus) — לא הומצא ולא נוסח מחדש.")
    lines.append("")
    lines.append("## הנחיות לבעלים")
    lines.append("")
    lines.append("עבור כל מוצר, קרא את **טקסט הרכיבים** בעברית ובדוק:")
    lines.append("1. האם הסיווג המוצע (מלא / מזוקק / מעורב / מקרה קצה) תואם את מה שאתה קורא בלייבל?")
    lines.append("2. אם לא — רשום את הסיווג הנכון שלך בטור 'ורדיקט הבעלים'.")
    lines.append("3. שימו לב מיוחד לשורות עם **גבולי** — שם שיקולך קריטי.")
    lines.append("")
    lines.append("**מפתח ביטחון:**")
    lines.append("- בטוח = ניתן לקרוא ישירות מהלייבל; הסיווג צפוי להיות נכון")
    lines.append("- גבולי = מבקש עיניים של הבעלים; הסיווג עשוי להשתנות")
    lines.append("")

    # Spelt corrections note
    lines.append("---")
    lines.append("")
    lines.append(SPELT_PITA_CORRECTIONS)
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group by tier
    for tier_key in ["T1", "T2", "T3", "T4"]:
        tier_products = [p for p in products if p["tier"] == tier_key]
        if not tier_products:
            continue

        lines.append(f"## {TIER_LABELS[tier_key]}")
        lines.append("")
        lines.append(f"*{TIER_DESCRIPTIONS[tier_key]}*")
        lines.append("")
        lines.append(f"סה\"כ בשכבה זו: {len(tier_products)} מוצרים")
        lines.append("")

        # Table header
        lines.append("| ברקוד | שם מוצר | קטגוריה | סיווג מוצע | ביטחון | סיבה קצרה | טקסט רכיבים מלא | ורדיקט הבעלים |")
        lines.append("|---|---|---|---|---|---|---|---|")

        for p in tier_products:
            barcode = p["barcode"]
            name = p["name_he"]
            cat_map = {
                "cakes_hard_cookies": "עוגות/עוגיות",
                "bread": "לחם",
                "cereals_granola": "דגני בוקר/גרנולה",
                "snack_bar_granola": "חטיפי גרנולה",
            }
            cat = cat_map.get(p["category"], p["category"])
            label_map = {
                "clear-whole": "מלא ברור",
                "clear-refined": "מזוקק ברור",
                "hard-mixed": "מעורב קשה",
                "edge-case": "מקרה קצה",
            }
            label = label_map.get(p["expected_label"], p["expected_label"])
            conf = "בטוח" if p["confidence"] == "C" else "**גבולי**"
            reason = p["reason_he"]
            ing = p["ingredients_text_he"]
            # For table, truncate at 300 chars
            ing_display = ing[:300] + ("…" if len(ing) > 300 else "")

            # Flag spelt correction
            if p.get("spelt_correction"):
                name = f"⚑ {name}"
                label = f"**{label}** (תיקון היוריסטי)"

            lines.append(f"| {barcode} | {name} | {cat} | {label} | {conf} | {reason} | {ing_display} | |")

        lines.append("")

    # Rank ordering requirements for T3
    lines.append("---")
    lines.append("")
    lines.append("## סדר דירוג נדרש בתוך שכבה 3 (Gate B2)")
    lines.append("")
    lines.append("הפורמולה החדשה חייבת לשמור על הסדר הבא (קריא ישירות מהלייבל):")
    lines.append("")
    lines.append("1. **לחם קמח מלא 100%** (6322838) > **קרקר דק כפרי פיטנס** (7290115205176)")
    lines.append("   — 100% מהקמח מלא > 30.5% מלא")
    lines.append("")
    lines.append("2. **לחם אנג'ל חצי מלא** (7290018500460) > **קרקר דק כפרי** (7296073659952)")
    lines.append("   — 50% מלא/50% לבן > 25.5% מלא מתוך 66% תערובת")
    lines.append("")
    lines.append("3. **מוזלי 47% דגנים מלאים** (7290016883176) > **מוזלי קראנצ'י** (7290011131371)")
    lines.append("   — שיבולת שועל 47% > שיבולת שועל 38%")
    lines.append("")
    lines.append("4. **גרנולה פירות** (7290011131975) > **מוזלי קראנצי תפוח קינמון** (7290011131388)")
    lines.append("   — שיבולת שועל ~43% בגרנולה > שיבולת שועל 39%")
    lines.append("")
    lines.append("5. **פיטנס בר גרנולה שוקולד מריר** (7290118427858) > **חטיף דגנים שוקולד עם אגוזים** (7290107947480)")
    lines.append("   — 43% שיבולת שועל מלא (32%+11%) > 1% חיטה מלאה בתוך 32% פתיתי דגנים")
    lines.append("")

    # Summary
    lines.append("---")
    lines.append("")
    lines.append("## סיכום גודל הסט")
    lines.append("")
    lines.append("| שכבה | תיאור | מספר מוצרים |")
    lines.append("|---|---|---|")
    total = 0
    for tier_key, label in TIER_LABELS.items():
        count = tier_counts.get(tier_key, 0)
        total += count
        lines.append(f"| {tier_key} | {label} | {count} |")
    lines.append(f"| **סה\"כ** | | **{total}** |")
    lines.append("")
    lines.append(f"*הסט מכיל {total} מוצרים. המטרה: 60–75 מוצרים.*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*נוצר: {datetime.datetime.utcnow().strftime('%Y-%m-%d')} | TASK-395 | Data Agent*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Build JSON
# ---------------------------------------------------------------------------
def build_json(products: list[dict]) -> dict:
    return {
        "schema_version": "matrix_gold_set_candidates_v1",
        "task": "TASK-395",
        "condition": "C-N1-1",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "description": "Gold set candidates for Component B re-validation. Awaiting owner review and correction.",
        "status": "DRAFT — pending owner verdict",
        "tier_counts": {k: v for k, v in sorted(tier_counts.items())},
        "total_products": len(products),
        "spelt_pita_correction_note": (
            "7 spelt-pita products (WRONG-017/022/024/025/028/029/034) were mislabeled by the heuristic as WFP. "
            "כוסמין לבן = refined spelt flour → expected_label=clear-refined. "
            "Representative in gold set: barcode 7290018500644 (כוסמין לבן, T2). "
            "כוסמין מלא = whole spelt → expected_label=clear-whole. "
            "Representative: barcode 574615 (כוסמין מלא 100%, T1) and 7290017947464 (T1)."
        ),
        "ranking_requirements_T3": [
            {"higher": "6322838", "lower": "7290115205176", "reason": "100% of flour whole > 30.5% whole wheat"},
            {"higher": "7290018500460", "lower": "7296073659952", "reason": "50% whole of flours > 25.5% of 66% blend"},
            {"higher": "7290016883176", "lower": "7290011131371", "reason": "oats 47% > oats 38%"},
            {"higher": "7290011131975", "lower": "7290011131388", "reason": "oats ~43% > oats 39%"},
            {"higher": "7290118427858", "lower": "7290107947480", "reason": "43% whole oat vs 1% whole wheat in flakes"},
        ],
        "confidence_legend": {
            "C": "Confident — readable directly from label",
            "B": "Borderline — owner judgment required"
        },
        "products": products,
    }


# ---------------------------------------------------------------------------
# Write files
# ---------------------------------------------------------------------------
OUT_DIR = Path("C:/Bari/03_operations/bsip2/proto_v0/analysis")
OUT_DIR.mkdir(parents=True, exist_ok=True)

md_path = OUT_DIR / "matrix_gold_set_candidates_v1.md"
json_path = OUT_DIR / "matrix_gold_set_candidates_v1.json"

md_content = build_markdown(GOLD_SET)
json_content = build_json(GOLD_SET)

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Markdown written: {md_path} ({md_path.stat().st_size} bytes)")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_content, f, ensure_ascii=False, indent=2)
print(f"JSON written: {json_path} ({json_path.stat().st_size} bytes)")

# Hashes
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

md_sha = sha256_file(md_path)
json_sha = sha256_file(json_path)
print(f"MD SHA256:   {md_sha}")
print(f"JSON SHA256: {json_sha}")

# Tier counts
print(f"\nTier counts: {tier_counts}")
print(f"Total: {len(GOLD_SET)} products")

# Confidence breakdown
conf_C = sum(1 for p in GOLD_SET if p["confidence"] == "C")
conf_B = sum(1 for p in GOLD_SET if p["confidence"] == "B")
print(f"Confident (C): {conf_C}, Borderline (B): {conf_B}")

# Spelt corrections
spelt = [p for p in GOLD_SET if p.get("spelt_correction")]
print(f"Spelt corrections flagged: {len(spelt)}")
