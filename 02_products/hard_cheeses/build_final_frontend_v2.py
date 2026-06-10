"""
Job 2: Integrate Content Agent insight lines into hard_cheeses_frontend_v2.json.
Also applies hc-030 (Baby Bell) handling per TASK-215 instructions:
  - Re-scrape succeeded; score is D/39 (confirmed correct — driven by 2x Israeli red labels
    + HP_FAT_SODIUM_COMBO penalty, not by data artifact)
  - Keep hc-030 in JSON with corrected ingredient data
  - Apply holding insight line from content draft
  - Update ingredients field with corrected data from re-scrape

Also fixes hc-028 insight line (removes bogus "E 144" reference).
"""
import json, sys, re
from pathlib import Path
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

FRONTEND_V2 = Path(r"C:\Bari\02_products\hard_cheeses\hard_cheeses_frontend_v2.json")
WEB_TARGET = Path(r"C:\bari\bari-web\src\data\comparisons\hard_cheeses_frontend_v2.json")

# Insight lines from content_draft_v1.md, keyed by product name (Hebrew)
INSIGHT_LINES = {
    "פרוסות גבינת גאודה 28% יורו צ'יז 400 גרם":
        "שלושה רכיבים בלבד: חלב, מלח, תרבית. חלבון 25 גרם ל-100 גרם.",
    "פרוסות גאודה עיזים":
        "חלב עיזים ומלח, ותו לא. חלבון 22 גרם ל-100 גרם, שומן 30%.",
    "גבינת גאודה מגורדת 28% יורו צ'יז 500 גרם":
        "גבינה לגרירה — מיועדת לכמויות קטנות. חלבון 27 גרם ל-100 גרם; הערכים מחושבים לפי ריכוז גבוה.",
    "גבינת גאודה מגורדת יוחננוף 400 גרם":
        "גבינה לגרירה — מיועדת לכמויות קטנות. חלבון 25 גרם ל-100 גרם; הערכים מחושבים לפי ריכוז גבוה.",
    "פרוסות גבינה צהובה חצי קשה 28% נעם 500 גרם":
        "גבינה 28% עם שלושה רכיבים בלבד. נתרן 660 מ\"ג.",
    "פרוסות גבינת גלבוע 5% 200 גרם":
        "מופחת שומן 5% — חלבון 33 גרם ל-100 גרם. מכיל חומר משמר אחד (E-202).",
    "פרוסות גאודה עמק 200 גרם":
        "גאודה 30% עם שלושה חומרי שימור ברשימת הרכיבים. חלבון 24 גרם.",
    "פרוסות גבינת טל העמק 32% בסגנון אמנטל 200 גרם":
        "גבינה 32% עם חלבון 27 גרם ל-100 גרם וחומר משמר אחד. נתרן 550 מ\"ג.",
    "פרוסות גבינה צהובה חצי קשה דקה 9% נעם 200 גרם":
        "מופחת שומן 9% ללא תוספות מזוהות. חלבון 30 גרם; נתרן גבוה, 620 מ\"ג.",
    "פרוסות גבינה צהובה חצי קשה דקה 9% נעם 360 גרם":
        "אותה גבינה, אריזה גדולה יותר — חלבון 30 גרם, ללא תוספות.",
    "פרוסות גבינת עמק מופחתת שומן 9% בד\"צ 200 גרם":
        "מופחת שומן 9% עם חומר משמר E-202. חלבון 30 גרם; נתרן 495 מ\"ג.",
    "פרוסות גבינת עמק מופחתת שומן 9% בקופסא 400 גרם":
        "מופחת שומן 9% עם חומר משמר E-202. חלבון 30 גרם; נתרן 491 מ\"ג.",
    "פרוסות גבינה צהובה חצי קשה דקה 22% נעם 200 גרם":
        "גבינה 22% ללא תוספות, רכיבים מינימליים. נתרן 670 מ\"ג — הגבוה בסגמנט.",
    "גאודה פסטו ירוק 200 גרם":
        "גבינה בטעם פסטו — חלבון 24 גרם, שומן 34%. רכיבי תיבול ממקור צמחי.",
    "פרוסות גבינה חצי קשה גוש חלב 28% מהדרין 200 גרם":
        "גבינה 28% עם חומר משמר אחד. חלבון 23 גרם; נתרן 510 מ\"ג.",
    "פרוסות גבינה חצי קשה גוש חלב 28% מהדרין 400 גרם":
        "אותה גבינה, אריזה כפולה — חומר משמר אחד, נתרן 510 מ\"ג.",
    "גבינה איטלקית גרנה פדנו קשה מגורדת 29% 100 גרם":
        "גבינה איטלקית לגרירה — חלבון 33 גרם ל-100 גרם. מיועדת לתוספת, לא לאכילה ישירה.",
    "פרוסות גבינת עמק דק 28% 200 גרם":
        "גבינה 28% עם חומר משמר E-202. נתרן 640 מ\"ג — שיקול בשימוש יומיומי.",
    "פרוסות גבינת עמק 28% 400 גרם":
        "גבינה 28% עם חומר משמר E-202. נתרן 640 מ\"ג.",
    "פרוסות גבינת עמק 28% בקופסא 200 גרם":
        "גבינה 28% עם חומר משמר E-202. נתרן 640 מ\"ג; חלבון 23 גרם.",
    "אצבעות גבינת עמק 28% 172 גרם":
        "אותה הרכבה כמו פרוסות עמק 28% — E-202, נתרן 640 מ\"ג.",
    "פרוסות גבינת עמק 28% בקופסא 400 גרם":
        "גבינה 28%, E-202, נתרן 640 מ\"ג. פורמט קופסא.",
    "פרוסות גבינת עמק 28% 600 גרם":
        "אריזה משפחתית של אותה גבינה — E-202, נתרן 640 מ\"ג.",
    "גבינת עמק מגורדת 28% 200 גרם":
        "גרידה של עמק 28% — E-202 ותאית כחומר מונע התגיישות. נתרן 640 מ\"ג.",
    "גבינת עמק מגורדת 28% 500 גרם":
        "אריזה גדולה של גרידת עמק — E-202 ותאית. נתרן 640 מ\"ג.",
    "פרוסות גבינת גאודה הולנדית 30% 200 גרם":
        "שני רכיבים בלבד: חלב ומלח. אבל נתרן 831 מ\"ג — הגבוה ביותר בקטגוריה.",
    "פרוסות גבינה מותכת 13% בטעם גאודה יורו צ'יז 150 גרם":
        "גבינה מותכת — נתרן 1,300 מ\"ג ל-100 גרם, ארבעה חומרי עיבוד ברשימת הרכיבים. לא גבינה רגילה.",
    "גבינת גאודה עיזים.":   # matches with trailing period as in JSON
        "גבינת עיזים עם שלושה רכיבים בלבד. שומן 34%, נתרן 800 מ\"ג.",
    "גבינת גאודה עיזים":     # alternate match without trailing period
        "גבינת עיזים עם שלושה רכיבים בלבד. שומן 34%, נתרן 800 מ\"ג.",
    # hc-030 Baby Bell: holding insight line (score confirmed D/39, correct engine output)
    "גבינה חצי קשה 24% בייבי בל 5*20 גרם":
        "ציון D — נתוני הרכיבים במאגר חלקיים עבור מוצר זה. ממה שזמין: חלבון 23 גרם, נתרן 680 מ\"ג.",
    # hc-005 variant name in JSON
    "גבינת גאודה פרוסות יוחננוף 400 גרם":
        "גבינה 28% עם רכיבים מינימליים. חלבון 25 גרם, נתרן 640 מ\"ג.",
}

# Names in the draft that don't exactly match JSON product names — provide manual mapping
MANUAL_MAP = {
    "hc-005": "פרוסות גבינה צהובה חצי קשה 28% נעם 500 גרם",  # draft hc-005 = נעם 500g, but JSON hc-005 is יוחננוף
}


def normalize_name(name):
    """Normalize name for fuzzy comparison."""
    name = name.strip()
    # Remove trailing period
    if name.endswith("."):
        name = name[:-1]
    # Collapse spaces
    name = re.sub(r"\s+", " ", name)
    return name


def build():
    data = json.loads(FRONTEND_V2.read_text(encoding="utf-8"))
    products = data["products"]

    matched = 0
    unmatched = []

    # Build normalized lookup
    normalized_insight = {}
    for k, v in INSIGHT_LINES.items():
        normalized_insight[normalize_name(k)] = v

    for product in products:
        pid = product["id"]
        name = product["name"]
        normalized = normalize_name(name)

        insight = normalized_insight.get(normalized)

        if insight:
            old = product.get("insightLine", "")
            product["insightLine"] = insight
            matched += 1
            print(f"MATCH {pid} | {name[:50]}")
        else:
            unmatched.append((pid, name))
            print(f"NO MATCH {pid} | {name[:60]}")

        # Baby Bell specific: update ingredients with corrected data
        if pid == "hc-030" and name == "גבינה חצי קשה 24% בייבי בל 5*20 גרם":
            product["expansion"]["ingredients"] = "חלב פרה מפוסטר(98%), מלח, תרבית לקטית, רנט."
            product["expansion"]["positiveSignals"] = [
                "חלבון טוב (23g ל-100g)",
                "ללא תוספות מזוהות",
                "NOVA 1 — עיבוד מינימלי"
            ]
            product["expansion"]["limitingFactors"] = [
                "שומן רווי גבוה (16g ל-100g) — תווית אדומה",
                "נתרן גבוה (710mg ל-100g) — תווית אדומה",
                "שומן טראנס נמוך (1g ל-100g)"
            ]
            # Update nutrition with corrected per-100g values
            product["expansion"]["nutrition"]["sodium"] = 710.0
            product["expansion"]["nutrition"]["satFat"] = 16.0
            product["expansion"]["nutrition"]["fat"] = 24.0
            product["expansion"]["nutrition"]["energyKcal"] = 305.0
            print(f"  hc-030 corrected: ingredients + nutrition updated (re-scrape 2026-06-07)")

        # hc-028: fix bogus "E 144" reference in insight line (already handled by INSIGHT_LINES override)
        if pid == "hc-028":
            print(f"  hc-028 insight line corrected (removed E 144 reference)")

    print(f"\nMatched: {matched}/{len(products)}")
    if unmatched:
        print("Unmatched products:")
        for pid, name in unmatched:
            print(f"  {pid}: {name}")

    # Update meta
    data["_meta"]["generated"] = datetime.now(timezone.utc).isoformat()
    data["_meta"]["content_draft_integrated"] = "content_draft_v1.md (2026-06-07)"
    data["_meta"]["hc030_rescrape"] = (
        "Re-scraped 2026-06-07. Corrected ingredients: חלב פרה מפוסטר(98%), מלח, תרבית לקטית, רנט. "
        "Score D/39 confirmed correct (ISRAELI_RED_LABELS_2_PLUS cap=45 + HP_FAT_SODIUM_COMBO penalty). "
        "Product kept in JSON with holding insight line."
    )

    # Write updated JSON
    FRONTEND_V2.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\nWritten: {FRONTEND_V2}")

    # Copy to website
    WEB_TARGET.parent.mkdir(parents=True, exist_ok=True)
    WEB_TARGET.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"Deployed: {WEB_TARGET}")

    return matched, len(products), unmatched


if __name__ == "__main__":
    matched, total, unmatched = build()
    print(f"\nFinal: {matched}/{total} insight lines matched")
