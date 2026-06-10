"""
Parse Baby Bell re-scraped HTML tabs to extract ingredients, nutrition, allergens.
Outputs parsed_baby_bell.json in yohananof_scrape/.
"""
from pathlib import Path
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
SCRAPE_DIR = BASE_DIR / "yohananof_scrape" / "3073781199918"

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


def clean(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def extract_text_from_html(html_path):
    if not html_path.exists():
        return None, "file_missing"
    html = html_path.read_text(encoding="utf-8")
    if not html.strip():
        return None, "empty"
    if BS4_AVAILABLE:
        soup = BeautifulSoup(html, "html.parser")
        text = clean(soup.get_text(separator=" "))
    else:
        # Fallback: strip tags with regex
        text = clean(re.sub(r"<[^>]+>", " ", html))
    return text, "ok"


def parse_nutrition_from_text(text):
    """
    Extract key nutrition values from the visible text of the nutrition tab.
    Yohananof nutrition tables look like:
      ערך אנרגטי XXX קק"ל
      שומן X גרם
      מתוכם רווי X גרם
      פחמימות X גרם
      מתוכם סוכרים X גרם
      חלבון X גרם
      מלח X גרם   (or נתרן)
    """
    nutrition = {}

    patterns = [
        ("energy_kcal", r"ערך אנרגטי[\s\S]{0,30}?([\d\.]+)\s*(?:קק\"ל|kcal|קילוקלוריות|קלוריות)"),
        ("energy_kcal", r"([\d\.]+)\s*(?:קק\"ל|kcal)\b"),
        ("fat_g", r"שומן\s+([\d\.]+)\s*גרם"),
        ("fat_saturated_g", r"(?:מתוכם\s+)?(?:שומן\s+)?רווי\s+([\d\.]+)\s*גרם"),
        ("carbohydrates_g", r"פחמימות\s+([\d\.]+)\s*גרם"),
        ("sugars_g", r"(?:מתוכם\s+)?סוכרים\s+([\d\.]+)\s*גרם"),
        ("protein_g", r"חלבון\s+([\d\.]+)\s*גרם"),
        ("sodium_mg_from_salt", r"מלח\s+([\d\.]+)\s*גרם"),  # salt → sodium: salt_g * 400
        ("sodium_mg", r"נתרן\s+([\d\.]+)\s*(?:מ\"ג|mg)"),
        ("fiber_g", r"סיבים\s+(?:תזונתיים\s+)?([\d\.]+)\s*גרם"),
    ]

    for key, pattern in patterns:
        if key in nutrition:
            continue
        m = re.search(pattern, text)
        if m:
            val = float(m.group(1))
            if key == "sodium_mg_from_salt":
                # Convert salt (g/100g) to sodium (mg/100g): Na = salt * 0.4 * 1000
                nutrition["sodium_mg"] = round(val * 400, 1)
            else:
                nutrition[key] = val

    return nutrition


def parse_ingredients_from_text(text):
    """
    In Yohananof dialog, ingredients appear after a tab click.
    The text typically contains the product name followed by ingredients.
    Try to extract the ingredients block.
    """
    # Look for a block starting after common prefixes
    prefixes = ["רכיבים:", "מרכיבים:", "הרכב:"]
    for prefix in prefixes:
        idx = text.find(prefix)
        if idx >= 0:
            raw = text[idx + len(prefix):idx + 800].strip()
            # Cut at disclaimer boilerplate
            for stopper in ["הנתונים המדויקים", "אין להסתמך", "יתכנו טעויות"]:
                s = raw.find(stopper)
                if s >= 0:
                    raw = raw[:s].strip()
            return clean(raw)

    # Fallback: find Hebrew ingredient-like block (starts after product name + price)
    # Look for a sequence that looks like ingredient list (חלב, מלח, ...)
    m = re.search(r'(חלב[^<\n]{10,400})', text)
    if m:
        raw = m.group(1).strip()
        for stopper in ["הנתונים המדויקים", "אין להסתמך", "ברקוד"]:
            s = raw.find(stopper)
            if s >= 0:
                raw = raw[:s].strip()
        return clean(raw)

    return None


def main():
    ing_html = SCRAPE_DIR / "ingredients.html"
    nut_html = SCRAPE_DIR / "nutrition.html"
    alg_html = SCRAPE_DIR / "allergens.html"

    ing_text, ing_status = extract_text_from_html(ing_html)
    nut_text, nut_status = extract_text_from_html(nut_html)
    alg_text, alg_status = extract_text_from_html(alg_html)

    print("=== INGREDIENTS RAW TEXT (first 600 chars) ===")
    print((ing_text or "")[:600])
    print("\n=== NUTRITION RAW TEXT (first 600 chars) ===")
    print((nut_text or "")[:600])
    print("\n=== ALLERGENS RAW TEXT (first 400 chars) ===")
    print((alg_text or "")[:400])

    ingredients_parsed = parse_ingredients_from_text(ing_text or "")
    nutrition_parsed = parse_nutrition_from_text(nut_text or "")

    print("\n=== PARSED INGREDIENTS ===")
    print(ingredients_parsed)
    print("\n=== PARSED NUTRITION ===")
    print(json.dumps(nutrition_parsed, ensure_ascii=False, indent=2))

    result = {
        "barcode": "3073781199918",
        "canonical_name_he": "גבינה חצי קשה 24% בייבי בל 5*20 גרם",
        "ingredients_text_parsed": ingredients_parsed,
        "nutrition_parsed": nutrition_parsed,
        "ingredients_raw_text": (ing_text or "")[:1500],
        "nutrition_raw_text": (nut_text or "")[:1500],
        "allergens_raw_text": (alg_text or "")[:800],
        "parse_notes": {
            "ingredients_status": ing_status,
            "nutrition_status": nut_status,
            "allergens_status": alg_status,
            "bs4_available": BS4_AVAILABLE,
        }
    }

    out_path = SCRAPE_DIR.parent / "parsed_baby_bell.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
