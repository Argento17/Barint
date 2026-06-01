"""Merge BSIP2 + BSIP1 + matrix integrity into consumer-facing page JSON."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BSIP2_SRC = Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(BSIP2_SRC))
from matrix_integrity import compute_matrix_integrity  # noqa: E402

BSIP2_BASE = Path(
    r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_004_recalibrated\products"
)
BSIP1_BASE = Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output")
OUT_PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "milk-comparison.json"

# Barcodes removed from the public comparison (e.g. duplicates, bad data, or editorial choice).
EXCLUDED_FROM_COMPARISON: frozenset[str] = frozenset(
    {
        "7290114313285",  # was display rank 13
        "7290110324773",  # was display rank 19
    }
)

GRADE_LABELS = {"A": "מצוין", "B": "טוב", "C": "בינוני", "D": "חלש", "E": "בעייתי"}

PRODUCT_TYPE_LABELS = {
    "dairy": "חלב פרה",
    "oat": "שיבולת שועל",
    "soy": "סויה",
    "almond": "שקדים",
    "rice": "אורז",
    "coconut": "קוקוס",
    "protein_drink": "משקה חלבון",
    "other_plant": "צמחי אחר",
}

# Consumer-facing wording (avoid "צפיפות תזונתית")
NUTRIENT_VALUE_LABEL = "ערך תזונתי"  # tables / short labels
NUTRIENT_VALUE_PHRASE = "ערך תזונתי ביחס למוצר"  # prose / explanations

USE_CASE_LABELS = {
    "coffee": "קפה",
    "kids": "ילדים",
    "protein": "חלבון",
    "low_sugar": "פחות סוכר",
    "simple": "רכיבים פשוטים",
    "daily": "שתייה יומיומית",
    "occasional": "חלופה מדי פעם",
}


def detect_product_type(name: str, ingredients: str, category: str) -> str:
    text = f"{name} {ingredients}".lower()
    if any(x in text for x in ("חלבון", "go milk", "גו מילק", "27g", "מועשר חלבון")):
        return "protein_drink"
    if "שיבולת" in text or "oat" in text:
        return "oat"
    if "סויה" in text or "soy" in text:
        return "soy"
    if "שקד" in text or "almond" in text:
        return "almond"
    if "אורז" in text or "rice" in text:
        return "rice"
    if "קוקוס" in text or "coconut" in text:
        return "coconut"
    if category in ("dairy_protein", "dairy_milk", "dairy_milk_engineered") or "חלב" in name:
        return "dairy"
    return "other_plant"


def main_ingredient(ingredients: str, product_type: str) -> str:
    if not ingredients:
        return "—"
    first = ingredients.split(",")[0].strip()
    if len(first) > 42:
        return first[:40] + "…"
    if product_type == "dairy" and "חלב" in ingredients:
        return "חלב"
    return first


def additives_label(bsip1: dict, trace: dict) -> str:
    enrich = bsip1.get("enrichment_summary") or {}
    count = enrich.get("additive_count", 0)
    l3 = trace.get("L3_inferred_classifications") or {}
    marker_count = l3.get("additive_marker_count", 0)
    sweetener = l3.get("sweetener_detected", False)
    additives = bsip1.get("extracted_additives") or []

    if count == 0 and marker_count == 0 and not sweetener:
        return "ללא תוספים מזוהים"
    if count <= 1 and marker_count <= 1:
        return "מעט תוספים"
    names = [a.get("term", "") for a in additives[:2] if isinstance(a, dict)]
    if names:
        return "תוספים: " + ", ".join(names)
    if sweetener:
        return "ממתיק / תוספים"
    return "תוספים ומייצבים"


def infer_use_cases(
    product_type: str, name: str, protein: float | None, sugar: float | None, trace: dict, bsip1: dict
) -> list[str]:
    cases: list[str] = []
    enrich = bsip1.get("enrichment_summary") or {}
    ing_count = enrich.get("ingredient_count_parsed", 99)
    nova = trace.get("nova_proxy", 4)
    text = name.lower()

    if "בריסטה" in name or "barista" in text or product_type == "oat":
        cases.append("coffee")
    if protein is not None and protein >= 3.0:
        cases.append("protein")
    elif product_type in ("almond", "rice"):
        cases.append("occasional")
    if sugar is not None and sugar <= 3.5 or "ללא סוכר" in name or "unsweetened" in text:
        cases.append("low_sugar")
    if ing_count <= 2 and enrich.get("additive_count", 1) == 0:
        cases.append("simple")
    if product_type == "dairy" and nova <= 2:
        cases.append("kids")
        cases.append("daily")
    if product_type == "protein_drink":
        cases.append("protein")
    if not cases:
        cases.append("occasional")
    return list(dict.fromkeys(cases))[:3]


def build_filter_tags(product_type: str, use_cases: list[str], additives: str, score: float, protein, sugar) -> list[str]:
    tags = [f"type:{product_type}"]
    if "ללא תוספים" in additives:
        tags.append("no_additives")
    if protein is not None and protein >= 3.0:
        tags.append("high_protein")
    if "low_sugar" in use_cases:
        tags.append("low_sugar")
    if "coffee" in use_cases:
        tags.append("coffee")
    if score is not None and score >= 65:
        tags.append("high_score")
    return tags


def _truncate(text: str, max_len: int = 56) -> str:
    text = (text or "").strip()
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def product_identity(brand: str, name_he: str) -> dict[str, str | None]:
    """Avoid duplicating brand in title + subtitle."""
    brand_clean = (brand or "").replace("חלב ", "").strip()
    name = (name_he or "").strip()
    if brand_clean and brand_clean in name:
        return {"displayTitle": _truncate(name), "brandLine": None}
    if brand_clean:
        return {"displayTitle": _truncate(name), "brandLine": brand_clean}
    return {"displayTitle": _truncate(name), "brandLine": None}


def _strength(score: float) -> str:
    if score >= 75:
        return "חזק"
    if score >= 50:
        return "בינוני"
    if score >= 30:
        return "חלש"
    return "נמוך"


def build_good_observations(
    trace: dict,
    bsip1: dict,
    product_type: str,
    additives: str,
    type_avg_protein: float | None,
) -> list[str]:
    dim = trace.get("dimension_scores") or {}
    nut = bsip1.get("normalized_nutrition_per_100g") or {}
    protein = nut.get("protein_g")
    sugar = nut.get("sugars_g")
    nova = trace.get("nova_proxy", 0)
    enrich = bsip1.get("enrichment_summary") or {}
    ing = bsip1.get("ingredients_raw") or bsip1.get("ingredients_text_he") or ""
    l3 = trace.get("L3_inferred_classifications") or {}
    good: list[str] = []

    if dim.get("additive_quality", 0) >= 90:
        good.append("רשימת רכיבים יחסית פשוטה — מעט תוספים או מייצבים חזקים")
    if dim.get("whole_food_integrity", 0) >= 85:
        good.append("הרכב המוצר קרוב יותר למזון בסיסי — פחות רכיבים תפקודיים ארוכים")

    if protein is not None and protein >= 3.0:
        rel = ""
        if type_avg_protein and protein >= type_avg_protein * 1.15:
            rel = f" — מעל ממוצע {PRODUCT_TYPE_LABELS.get(product_type, 'הקטגוריה')}"
        good.append(f"חלבון בכמות טובה ביחס לקטגוריה{rel} ({protein} ג׳ ל־100 מ״ל)")
    elif protein is not None and protein >= 2.0 and product_type == "soy":
        good.append(f"חלבון צמחי בולט לעומת שקדים או שיבולת ({protein} ג׳ ל־100 מ״ל)")

    if sugar is not None and sugar <= 3.0:
        good.append(f"פחות סוכר ביחס למוצרים דומים ({sugar} ג׳ ל־100 מ״ל)")
    if "ללא סוכר" in ing or "unsweetened" in ing.lower():
        good.append("לפי התווית: בלי סוכר מוסף")

    if nova <= 2:
        good.append("רמת עיבוד יחסית מתונה — בסיס ברור ברשימת הרכיבים")
    if product_type == "dairy" and ing.strip() in ("חלב", "חלב."):
        good.append("חלב פרה בסיסי — חלבון טבעי בלי תוספות מיותרות")

    if "בריסטה" in ing or "barista" in ing.lower():
        good.append("מרקם וטעם שמושגים בלי עומס גבוה של רכיבים — מתאים לקפה")
    if dim.get("glycemic_quality", 0) >= 80 and sugar is not None:
        good.append("רמת סוכר נמוכה יחסית לעומת משקאות ממותקים דומים")

    if enrich.get("has_protein_isolate_or_concentrate") and protein and protein >= 4:
        good.append("חלבון מודגש בתווית — מתאים למי שמחפש שובע חלבוני")

    if l3.get("red_label_count", 0) == 0:
        good.append("אין תווית אדומה ישראלית בבדיקה לפי 100 גרם")

    return list(dict.fromkeys(good))[:5]


def build_watch_observations(
    trace: dict,
    bsip1: dict,
    product_type: str,
    additives: str,
    mi: dict,
    type_avg_protein: float | None,
    category_rank_pct: float,
) -> list[str]:
    dim = trace.get("dimension_scores") or {}
    nut = bsip1.get("normalized_nutrition_per_100g") or {}
    protein = nut.get("protein_g")
    sugar = nut.get("sugars_g")
    nova = trace.get("nova_proxy", 0)
    enrich = bsip1.get("enrichment_summary") or {}
    ing = bsip1.get("ingredients_raw") or bsip1.get("ingredients_text_he") or ""
    l3 = trace.get("L3_inferred_classifications") or {}
    sweeteners = bsip1.get("extracted_sweeteners") or []
    watch: list[str] = []

    if dim.get("nutrient_density", 100) < 25:
        watch.append(
            f"{NUTRIENT_VALUE_PHRASE} נמוך — חלבון וסיבים פחות בולטים לעומת מוצרים דומים"
        )
    if protein is not None and protein < 1.5:
        watch.append(
            "כמות חלבון נמוכה מאוד — בעיקר משקה, לא מקור חלבון משמעותי"
        )
    elif type_avg_protein and protein is not None and protein < type_avg_protein * 0.6:
        watch.append(
            f"חלבון נמוך מול ממוצע {PRODUCT_TYPE_LABELS.get(product_type, 'הקטגוריה')} — לשקול אם חשוב לכם חלבון"
        )

    if sugar is not None and sugar > 5:
        watch.append(f"רמת סוכר גבוהה יחסית ({sugar} ג׳) — כדאי להשוות למוצרים דומים בתווית")
    elif sugar is not None and 3.5 < sugar <= 5:
        watch.append(f"סוכר בינוני ({sugar} ג׳) — לא בהכרח «ללא סוכר» למרות מוצר צמחי")

    if nova >= 4:
        watch.append("רמת עיבוד גבוהה — רשימת רכיבים ארוכה יותר ורכיבים תפקודיים")
    elif nova == 3:
        watch.append("עיבוד בינוני-גבוה — תחליף מעובד, לא חלב בסיסי בלבד")

    if enrich.get("additive_count", 0) >= 3 or l3.get("additive_marker_count", 0) >= 3:
        watch.append("יש כמה תוספים ומייצבים — טריידאוף למרקם ויציבות")
    elif additives.startswith("תוספים") or "מייצב" in additives:
        watch.append(f"{additives} — שווה לבדוק אם חשוב לכם מה נכנס למרקם והטעם")

    if sweeteners or l3.get("sweetener_detected"):
        watch.append("מזוהים ממתיקים או סוכר מוסף — משפיעים על טעם ורמת מתיקות")

    if "שמן" in ing and product_type in ("oat", "almond", "rice"):
        watch.append("יש שמן צמחי ברשימה — עוזר במרקם והקצפה, מוסיף שומן למנה")

    if enrich.get("has_protein_isolate_or_concentrate") and product_type == "protein_drink":
        watch.append(
            "חלבון גבוה כרגיל במשקי חלבון — לרוב לצד רכיבים נוספים לטעם ויציבות"
        )

    if mi.get("structural_degradation_level") in ("high", "severe", "extreme"):
        watch.append("הרכב המוצר רחוק יותר ממזון בסיסי — יותר שלבים בתעשייה")

    if category_rank_pct < 0.35:
        watch.append("המיקום בציון נמוך יחסית לשאר המדף — כדאי לבחור לפי עדיפות אישית (חלבון מול פשטות)")

    if l3.get("red_label_count", 0) >= 1:
        labels = l3.get("red_labels") or []
        watch.append(f"תווית אדומה ישראלית ({', '.join(labels)}) בבסיס 100 גרם")

    if dim.get("fat_quality", 100) < 60 and nut.get("fat_saturated_g"):
        watch.append("שומן רווי גבוה יחסית בתווית — רלוונטי אם שותים הרבה ביום")

    if "אורגני" in ing or "organic" in ing.lower():
        watch.append("«אורגני» לא אומר רשימת רכיבים קצרה — כדאי לקרוא את הרשימה עצמה")

    return list(dict.fromkeys(watch))[:6]


def build_tradeoff_context(product_type: str, trace: dict, bsip1: dict) -> str:
    dim = trace.get("dimension_scores") or {}
    if product_type == "protein_drink":
        return "מוצר שמחזק חלבון אך לרוב בטריידאוף של רשימת רכיבים ועיבוד — לא אותו דבר כמו חלב בסיסי."
    if product_type == "almond":
        return "קליל ודל קלוריות, אך חלבון נמוך — טוב כתחליף טעם, פחות כמקור חלבון."
    if product_type == "oat" and dim.get("glycemic_quality", 0) < 85:
        return "נעים לשתייה ולקפה, אך לעיתים יותר סוכר/פחמימה מאשר נדמה."
    if dim.get("whole_food_integrity", 0) >= 85 and dim.get("nutrient_density", 0) < 30:
        return f"פשוט ברכיבים, אך {NUTRIENT_VALUE_PHRASE} לא בהכרח גבוה — תלוי מה אתם מחפשים."
    return "אין «מנצח» אחד — יש טריידאוף בין חלבון, פשטות, טעם ועיבוד."


def build_bari_interpretation(trace: dict, bsip1: dict, additives: str) -> list[dict]:
    dim = trace.get("dimension_scores") or {}
    nut = bsip1.get("normalized_nutrition_per_100g") or {}
    protein = nut.get("protein_g")
    sugar = nut.get("sugars_g")
    nova = trace.get("nova_proxy", 0)
    ing_count = (bsip1.get("enrichment_summary") or {}).get("ingredient_count_parsed", 99)

    def pillar(key: str, label: str, score: float, interp: str) -> dict:
        return {
            "key": key,
            "label": label,
            "score": round(score),
            "strength": _strength(score),
            "interpretation": interp,
        }

    ing_score = (dim.get("whole_food_integrity", 50) + dim.get("additive_quality", 50)) / 2
    if ing_count <= 2 and dim.get("additive_quality", 0) >= 90:
        ing_interp = "רשימת רכיבים קצרה — מרכיב בסיס מוכר"
    elif dim.get("additive_quality", 0) >= 75:
        ing_interp = "רכיבים מוכרים יחסית, עם מעט תוספים"
    else:
        ing_interp = "רשימה ארוכה יותר — יותר מייצבים, העשרה וטעמים"

    proc_score = dim.get("processing_quality", 50)
    if nova <= 1:
        proc_interp = "עיבוד מינימלי — קרוב למוצר בסיסי"
    elif nova <= 2:
        proc_interp = "עיבוד נמוך-בינוני — שינוי מתון מהמקור"
    elif nova == 3:
        proc_interp = "מעובד בינוני — תהליך תעשייתי ברור"
    else:
        proc_interp = "מעובד מאוד — הרבה רכיבים תפקודיים"

    dens_score = dim.get("nutrient_density", 50)
    if dens_score >= 50:
        dens_interp = f"{NUTRIENT_VALUE_PHRASE} סביר — בקו עם מה שמקובל בקטגוריה"
    elif protein and protein >= 2.5:
        dens_interp = "חלבון בולט, אך סיבים ומינרלים פחות מובילים בפרופיל"
    else:
        dens_interp = "דל יחסית בחלבון וסיבים — יותר כמו משקה מאשר כמקור תזונה מלא"

    add_score = dim.get("additive_quality", 50)
    add_interp = additives
    if "ללא" in additives:
        add_interp = "ללא תוספים מזוהים — פחות שינוי מרכיבי בסיס"
    elif "מעט" in additives:
        add_interp = "מעט תוספים — טריידאוף קטן למען יציבות"

    sugar_score = dim.get("glycemic_quality", 50)
    if sugar is None:
        sugar_interp = "נתון סוכר לא מוצהר במלואו — בדקו תווית"
    elif sugar <= 3:
        sugar_interp = f"סוכר נמוך ({sugar} ג׳) — פרופיל מתון"
    elif sugar <= 5:
        sugar_interp = f"סוכר בינוני ({sugar} ג׳) — לא דל-סוכר קיצוני"
    else:
        sugar_interp = f"סוכר גבוה יותר ({sugar} ג׳) — משפיע על טעם מתוק"

    prot_score = dim.get("protein_quality", 50)
    if protein is None:
        prot_interp = "חלבון לא מוצהר — לא ניתן להשוות בביטחון"
    elif protein >= 3:
        prot_interp = f"חלבון גבוה ({protein} ג׳) — בולט לעומת רוב המשקאות ברשימה"
    elif protein >= 1.5:
        prot_interp = f"חלבון בינוני ({protein} ג׳) — לא מקור חלבון עיקרי"
    else:
        prot_interp = f"חלבון נמוך ({protein} ג׳) — מתאים לטעם/קלוריות, לא לשובע"

    return [
        pillar("ingredients", "איכות רכיבים", ing_score, ing_interp),
        pillar("processing", "רמת עיבוד", proc_score, proc_interp),
        pillar("density", NUTRIENT_VALUE_LABEL, dens_score, dens_interp),
        pillar("additives", "תוספים", add_score, add_interp),
        pillar("sugar", "סוכר", sugar_score, sugar_interp),
        pillar("protein", "חלבון", prot_score, prot_interp),
    ]


def build_consumer_copy(
    trace: dict,
    bsip1: dict,
    product_type: str,
    use_cases: list[str],
    additives: str,
    mi: dict,
    type_avg_protein: float | None,
    category_rank_pct: float,
) -> dict:
    grade = trace.get("grade_estimate", "C")
    grade_label = GRADE_LABELS.get(grade, grade)
    score = trace.get("final_score_estimate", 0)
    dim = trace.get("dimension_scores") or {}

    good = build_good_observations(trace, bsip1, product_type, additives, type_avg_protein)
    watch = build_watch_observations(
        trace, bsip1, product_type, additives, mi, type_avg_protein, category_rank_pct
    )

    takeaway_parts = []
    if score >= 70:
        takeaway_parts.append("ציון גבוה ביחס למדף")
    elif score < 45:
        takeaway_parts.append("ציון נמוך יחסית בקטגוריה")
    if dim.get("nutrient_density", 0) < 25 and product_type != "protein_drink":
        takeaway_parts.append(f"{NUTRIENT_VALUE_LABEL} נמוך יחסית")
    if dim.get("additive_quality", 0) >= 90:
        takeaway_parts.append("רכיבים פשוטים יחסית")

    takeaway = " · ".join(takeaway_parts[:2]) if takeaway_parts else f"ציון {grade} ({grade_label})"

    why_parts = [f"ציון Bari ‏{int(score)} ({grade_label})"]
    if dim.get("whole_food_integrity", 0) >= 85:
        why_parts.append("בין השאר בזכות רשימת רכיבים פשוטה יחסית")
    if dim.get("nutrient_density", 0) < 30:
        why_parts.append(f"במקביל, {NUTRIENT_VALUE_LABEL} נמוך יחסית מוריד את הציון הכולל")
    if trace.get("nova_proxy", 0) >= 4:
        why_parts.append("רמת עיבוד גבוהה גם מורידה את הציון הכולל")
    why = " — ".join(why_parts) + "."

    return {
        "whyRated": why,
        "good": good if good else ["ההשוואה נשענת על רכיבים, ערכים וקטגוריה — בלי דגש אחד בולט במוצר הזה"],
        "watchOut": watch
        if watch
        else ["לא זוהה כאן דפוס נוסף מעבר לשורות למעלה — התאימו את הבחירה לשימוש שלכם"],
        "context": build_tradeoff_context(product_type, trace, bsip1),
        "takeaway": takeaway,
    }


def short_display_name(brand: str, name_he: str) -> str:
    return product_identity(brand, name_he)["displayTitle"]


def discover_barcodes() -> list[str]:
    barcodes = []
    for d in sorted(BSIP2_BASE.iterdir()):
        if not d.is_dir() or not d.name.startswith("bsip1_"):
            continue
        bc = d.name.replace("bsip1_", "")
        if bc in EXCLUDED_FROM_COMPARISON:
            continue
        if (BSIP1_BASE / f"bsip1_{bc}.json").exists():
            barcodes.append(bc)
    return barcodes


def _type_protein_averages(rows: list[dict]) -> dict[str, float]:
    by_type: dict[str, list[float]] = {}
    for row in rows:
        p = row.get("protein")
        if p is None:
            continue
        by_type.setdefault(row["product_type"], []).append(p)
    return {t: sum(vals) / len(vals) for t, vals in by_type.items() if vals}


def main() -> None:
    raw_rows: list[dict] = []
    for bc in discover_barcodes():
        trace_path = BSIP2_BASE / f"bsip1_{bc}" / "bsip2_trace.json"
        bsip1_path = BSIP1_BASE / f"bsip1_{bc}.json"
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        bsip1 = json.loads(bsip1_path.read_text(encoding="utf-8"))
        name_he = bsip1.get("canonical_name_he") or trace["input_reference"].get("product_name_he", "")
        ingredients = bsip1.get("ingredients_raw") or bsip1.get("ingredients_text_he") or ""
        category = trace.get("category", "")
        product_type = detect_product_type(name_he, ingredients, category)
        nut = bsip1.get("normalized_nutrition_per_100g") or {}
        raw_rows.append(
            {
                "bc": bc,
                "trace": trace,
                "bsip1": bsip1,
                "product_type": product_type,
                "protein": nut.get("protein_g"),
                "score": trace.get("final_score_estimate") or 0,
            }
        )

    type_avg_protein = _type_protein_averages(raw_rows)
    scores_sorted = sorted(r["score"] for r in raw_rows)
    n_scores = len(scores_sorted)

    def rank_pct(score: float) -> float:
        if n_scores <= 1:
            return 0.5
        below = sum(1 for s in scores_sorted if s < score)
        return below / (n_scores - 1)

    products = []
    for row in raw_rows:
        bc = row["bc"]
        trace = row["trace"]
        bsip1 = row["bsip1"]
        mi = compute_matrix_integrity(bsip1)

        name_he = bsip1.get("canonical_name_he") or trace["input_reference"].get("product_name_he", "")
        brand = (bsip1.get("brand") or trace["input_reference"].get("brand", "")).strip()
        ingredients = bsip1.get("ingredients_raw") or bsip1.get("ingredients_text_he") or ""
        product_type = row["product_type"]
        nut = bsip1.get("normalized_nutrition_per_100g") or {}
        protein = nut.get("protein_g")
        sugar = nut.get("sugars_g")
        additives = additives_label(bsip1, trace)
        use_cases = infer_use_cases(product_type, name_he, protein, sugar, trace, bsip1)
        score = row["score"]
        grade = trace.get("grade_estimate", "C")
        identity = product_identity(brand, name_he)
        consumer = build_consumer_copy(
            trace,
            bsip1,
            product_type,
            use_cases,
            additives,
            mi,
            type_avg_protein.get(product_type),
            rank_pct(score),
        )
        bari_interp = build_bari_interpretation(trace, bsip1, additives)

        l3 = trace.get("L3_inferred_classifications") or {}
        dim_scores = trace.get("dimension_scores") or {}

        products.append(
            {
                "barcode": bc,
                "shortName": identity["displayTitle"],
                "displayTitle": identity["displayTitle"],
                "brandLine": identity["brandLine"],
                "name_he": name_he,
                "brand": brand,
                "productType": product_type,
                "productTypeLabel": PRODUCT_TYPE_LABELS.get(product_type, product_type),
                "image_url": bsip1.get("image_url"),
                "score": score,
                "grade": grade,
                "grade_label": GRADE_LABELS.get(grade, grade),
                "proteinPer100ml": protein,
                "sugarPer100ml": sugar,
                "additivesLabel": additives,
                "mainIngredient": main_ingredient(ingredients, product_type),
                "bestUseCases": [USE_CASE_LABELS[u] for u in use_cases],
                "consumerTakeaway": consumer["takeaway"],
                "consumerExplanation": consumer,
                "bariInterpretation": bari_interp,
                "filterTags": build_filter_tags(
                    product_type, use_cases, additives, score, protein, sugar
                ),
                "nova_proxy": trace.get("nova_proxy"),
                "red_labels": l3.get("red_labels", []),
                "ingredients_display": ingredients,
                "energy_kcal": nut.get("energy_kcal"),
                "dimensions": {
                    k: {"score": round(v, 1), "display_name": k}
                    for k, v in dim_scores.items()
                },
                "matrix_integrity": {
                    "matrix_integrity_score": mi.get("matrix_integrity_score"),
                    "reconstruction_depth": mi.get("reconstruction_depth"),
                    "structural_degradation_level": mi.get("structural_degradation_level"),
                    "engineering_intensity": mi.get("engineering_intensity"),
                    "dominant_matrix_signals": mi.get("dominant_matrix_signals", []),
                    "integrity_summary": mi.get("integrity_summary", ""),
                },
                "explanation_drivers": trace.get("explanation_drivers", []),
            }
        )

    products.sort(key=lambda p: p["score"] or 0, reverse=True)

    page = {
        "generated_at": "2026-05-20",
        "data_source": "BSIP2 run_004 + BSIP1 run_milk_002 · כל המוצרים בקטגוריה",
        "comparison_title": "השוואת חלב ותחליפי חלב",
        "story_headline": (
            f"השווינו {len(products)} מוצרי חלב ומשקאות חלב פופולריים בישראל וניתחנו אותם באמצעות מנוע הפרשנות של Bari."
        ),
        "story_teaser": (
            "ההשוואה מתבססת על רכיבים, ערכים תזונתיים, רמת עיבוד, תוספים והקשר קטגוריאלי — ולא רק על פרמטר בודד."
        ),
        "philosophy_note": (
            "המידע נועד לספק הקשר והשוואה בין מוצרים, ולא מהווה המלצה רפואית או תזונתית."
        ),
        "products": products,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(page, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(products)} products)")


if __name__ == "__main__":
    main()
