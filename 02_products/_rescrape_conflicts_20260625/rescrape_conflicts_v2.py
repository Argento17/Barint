"""
Rescrape conflicts v2: 3 products with name<>ingredient conflicts.
Owner-approved 2026-06-25. OFF BAN ABSOLUTE.
Source: direct Shufersal product page scrape only.
Uses correct extraction patterns from page structure analysis.
Output: rescrape_conflicts_results.json in same directory.
"""

import json
import re
import hashlib
import sys
import os
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))

PRODUCTS = [
    {
        "barcode": "7290108506624",
        "category": "cheese_spreads",
        "conflict_description": "name=גבינת עזים 32% שומן (GOAT) but scraped ingredients=חלב כבשים מפוסטר (SHEEP)",
        "source_url": "https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%97%D7%9C%D7%91-%D7%95%D7%91%D7%99%D7%A6%D7%99%D7%9D/%D7%92%D7%91%D7%99%D7%A0%D7%95%D7%AA-%D7%9E%D7%A2%D7%93%D7%A0%D7%99%D7%99%D7%94/%D7%92%D7%91%D7%99%D7%A0%D7%95%D7%AA-%D7%91%D7%A7%D7%A8-%D7%95%D7%A6%D7%90%D7%9F-%D7%9E%D7%99%D7%95%D7%97%D7%93%D7%95%D7%AA/%D7%92%D7%91%D7%99%D7%A0%D7%AA-%D7%A2%D7%96%D7%99%D7%9D-32%25-%D7%A9%D7%95%D7%9E%D7%9F/p/P_7290108506624",
    },
    {
        "barcode": "4504656",
        "category": "cakes_hard_cookies",
        "conflict_description": "name=מיני שטרודל תפוח עץ (APPLE) but scraped ingredients=מלית חצילים (24%) (EGGPLANT filling)",
        "source_url": "https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%9C%D7%97%D7%9E%D7%99%D7%9D-%D7%95%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%9E%D7%90%D7%A4%D7%94/%D7%9E%D7%90%D7%A4%D7%99%D7%9D-%D7%95%D7%A2%D7%95%D7%92%D7%95%D7%AA-%D7%9E%D7%94%D7%9E%D7%90%D7%A4%D7%94/%D7%91%D7%95%D7%A8%D7%A7%D7%A1-%D7%95%D7%9E%D7%90%D7%A4%D7%94-%D7%9E%D7%9C%D7%95%D7%97/%D7%9E%D7%99%D7%A0%D7%99-%D7%A9%D7%98%D7%A8%D7%95%D7%93%D7%9C-%D7%AA%D7%A4%D7%95%D7%97-%D7%A2%D7%A5/p/P_4504656",
    },
    {
        "barcode": "4504670",
        "category": "cakes_hard_cookies",
        "conflict_description": "name=מיני שטרודל שקדים (ALMOND) but scraped ingredients=גבינה קשה כחושה (12%) + זיתים ירוקים (CHEESE/OLIVE)",
        "source_url": "https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%9C%D7%97%D7%9E%D7%99%D7%9D-%D7%95%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%9E%D7%90%D7%A4%D7%94/%D7%9E%D7%90%D7%A4%D7%99%D7%9D-%D7%95%D7%A2%D7%95%D7%92%D7%95%D7%AA-%D7%9E%D7%94%D7%9E%D7%90%D7%A4%D7%94/%D7%91%D7%95%D7%A8%D7%A7%D7%A1-%D7%95%D7%9E%D7%90%D7%A4%D7%94-%D7%9E%D7%9C%D7%95%D7%97/%D7%9E%D7%99%D7%A0%D7%99-%D7%A9%D7%98%D7%A8%D7%95%D7%93%D7%9C-%D7%91%D7%9E%D7%99%D7%9C%D7%95%D7%99-%D7%A9%D7%A7%D7%93%D7%99%D7%9D/p/P_4504670",
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
}


def fetch_page(url, timeout=20):
    """Fetch a Shufersal product page. Returns (html_str, status_code, error)."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            return html, resp.status, None
    except urllib.error.HTTPError as e:
        return None, e.code, str(e)
    except urllib.error.URLError as e:
        return None, None, str(e)
    except Exception as e:
        return None, None, str(e)


def extract_name_he(html):
    """Extract Hebrew product name from Shufersal page JSON-LD."""
    # JSON-LD is most reliable
    jsonld_matches = re.findall(
        r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
        html, re.DOTALL
    )
    for block in jsonld_matches:
        try:
            data = json.loads(block)
            if data.get("@type") == "Product" and data.get("name"):
                return data["name"]
        except Exception:
            pass

    # Fallback: og:title
    m = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', html)
    if m:
        return m.group(1).strip()

    return None


def extract_ingredients(html):
    """
    Extract ingredients text from Shufersal page.
    The page uses <div class="componentsText"> to hold ingredient text.
    The text is inside nested whitespace. Extract and clean it.
    """
    # Primary pattern: componentsText div
    m = re.search(
        r'<div\s+class="componentsText"[^>]*>(.*?)</div>',
        html, re.DOTALL
    )
    if m:
        raw = m.group(1)
        # Strip HTML tags
        text = re.sub(r'<[^>]+>', '', raw)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 5:
            return text

    # Fallback: look for רכיבים header followed by content
    m = re.search(
        r'רכיבים.*?<div[^>]*>(.*?)</div>',
        html, re.DOTALL
    )
    if m:
        raw = m.group(1)
        text = re.sub(r'<[^>]+>', '', raw)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 5:
            return text

    return None


def extract_nutrition(html):
    """
    Extract nutrition values from Shufersal page.
    The page uses <div class="nutritionList"> with <div class="nutritionItem"> children.
    Each item: <div class="number">VALUE</div><div class="name">UNIT</div><div class="text">LABEL</div>
    """
    result = {}

    # Find the nutritionList block
    m = re.search(
        r'<div[^>]+class="nutritionList"[^>]*>(.*?)</div>\s*</div>\s*</li>',
        html, re.DOTALL
    )
    if not m:
        # Try a broader capture
        m = re.search(
            r'class="nutritionList"[^>]*>(.*?)</div>\s*</div>',
            html, re.DOTALL
        )

    if m:
        nutrition_block = m.group(1)
        # Extract all nutritionItem blocks
        items = re.findall(
            r'<div[^>]+class="nutritionItem"[^>]*>(.*?)</div>\s*</div>',
            nutrition_block, re.DOTALL
        )
        for item in items:
            # Extract number/value
            val_m = re.search(r'class="number[^"]*"[^>]*>\s*([^<\s][^<]*?)\s*<', item)
            # Extract unit
            unit_m = re.search(r'class="name"[^>]*>\s*([^<]+?)\s*<', item)
            # Extract label
            label_m = re.search(r'class="text"[^>]*>\s*([^<]+?)\s*<', item)

            if val_m and label_m:
                val = val_m.group(1).strip()
                label = label_m.group(1).strip()
                unit = unit_m.group(1).strip() if unit_m else ""

                try:
                    num_val = float(val.replace(",", "."))
                    # Map label to standard fields
                    if "אנרגיה" in label:
                        result["energy_kcal"] = num_val
                    elif "חלבונ" in label:
                        result["protein_g"] = num_val
                    elif "פחמימות" in label and "סוכרים" not in label and "סוכר" not in label:
                        result["carbohydrates_g"] = num_val
                    elif "סוכרים" in label or "סוכר" in label:
                        result["sugars_g"] = num_val
                    elif "שומן רווי" in label or "מתוכן שומן רווי" in label or "מתוכם שומן רווי" in label:
                        result["fat_saturated_g"] = num_val
                    elif "שומנ" in label and "רווי" not in label and "טרנס" not in label:
                        result["fat_g"] = num_val
                    elif "נתרן" in label:
                        result["sodium_mg"] = num_val
                    elif "סיבים" in label:
                        result["dietary_fiber_g"] = num_val
                except ValueError:
                    pass  # Non-numeric values like "פחות מ 0.5"

    return result if result else None


def nutrition_plausibility_check(nutrition, barcode):
    """Basic per-100g plausibility gate."""
    issues = []
    if not nutrition:
        return issues

    kcal = nutrition.get("energy_kcal")
    fat = nutrition.get("fat_g", 0) or 0
    prot = nutrition.get("protein_g", 0) or 0
    carbs = nutrition.get("carbohydrates_g", 0) or 0

    if kcal:
        estimated = fat * 9 + prot * 4 + carbs * 4
        if estimated > 0:
            ratio = kcal / estimated
            if ratio < 0.5 or ratio > 2.0:
                issues.append(
                    f"kcal={kcal} vs macro-estimate={estimated:.0f} — ratio {ratio:.2f} outside [0.5, 2.0]"
                )
        if kcal > 1000:
            issues.append(f"kcal={kcal} per 100g implausibly high (>1000)")
        if kcal < 1:
            issues.append(f"kcal={kcal} per 100g implausibly low (<1)")

    return issues


def classify_goat_sheep_conflict(name_he, fresh_name, ingredients_fresh):
    """
    For the cheese product 7290108506624: determine if name (goat) or ingredients (sheep) is right.
    """
    if ingredients_fresh is None:
        return "still_conflicting", "keep_deasserted", "Could not retrieve fresh ingredients from Shufersal page"

    has_goat_ingredients = any(w in ingredients_fresh for w in ["עזים", "חלב עזים"])
    has_sheep_ingredients = any(w in ingredients_fresh for w in ["כבשים", "חלב כבשים"])

    # Also check fresh name for animal type
    fresh_name_goat = fresh_name and "עזים" in fresh_name
    fresh_name_sheep = fresh_name and "כבשים" in fresh_name

    if has_sheep_ingredients and not has_goat_ingredients:
        if fresh_name_goat:
            # Name says goat, ingredients say sheep — CONFIRMED conflict. Ingredients are the label.
            return (
                "ingredients_were_right",
                "correct_data",
                "CONFIRMED CONFLICT: Fresh Shufersal page STILL shows name='גבינת עזים' (goat) "
                "but ingredients_text first item='חלב כבשים מפוסטר' (pasteurised sheep milk). "
                "The product is a SHEEP cheese sold under a GOAT label — this is a real mislabeling "
                "issue on the Shufersal page. Ingredients are ground truth (the label declares sheep milk). "
                "Action: correct canonical_name_he to remove 'עזים' claim, OR mark as 'goat_label_sheep_milk' "
                "and flag. The name conflict is CONFIRMED from the direct scrape — it is not a scrape error."
            )
        elif fresh_name_sheep:
            return (
                "ingredients_were_right",
                "correct_data",
                "Fresh page shows sheep in both name and ingredients — prior name was wrong in our data."
            )
        else:
            return (
                "ingredients_were_right",
                "correct_data",
                f"Fresh ingredients confirm sheep milk; fresh name: {fresh_name!r}. "
                "Ingredients are correct; name field needs verification."
            )
    elif has_goat_ingredients and not has_sheep_ingredients:
        return (
            "name_was_right",
            "correct_data",
            "Fresh scrape shows goat milk in ingredients — prior scraped ingredients were wrong. "
            "Name is correct; correct the ingredients field."
        )
    elif has_goat_ingredients and has_sheep_ingredients:
        return (
            "still_conflicting",
            "keep_deasserted",
            "Fresh ingredients mention BOTH goat and sheep milk — mixed-milk product or ambiguous data. "
            "Cannot determine ground truth without physical label."
        )
    else:
        return (
            "still_conflicting",
            "keep_deasserted",
            f"Fresh ingredients do not clearly mention goat or sheep. "
            f"Text (first 200): {ingredients_fresh[:200]!r}"
        )


def classify_strudel_conflict(barcode, name_he, fresh_name, ingredients_fresh):
    """
    For the strudel products: determine if names or ingredients were scraped wrong.
    """
    if ingredients_fresh is None:
        return "still_conflicting", "keep_deasserted", "Could not retrieve fresh ingredients from Shufersal page"

    if barcode == "4504656":
        # Name: apple strudel / Previous ingredients: eggplant filling (24%)
        has_apple = any(w in ingredients_fresh for w in ["תפוח", "תפוחים", "מלית תפוח"])
        has_eggplant = any(w in ingredients_fresh for w in ["חציל", "חצילים", "מלית חצילים"])

        # Also check fresh name
        fresh_says_apple = fresh_name and "תפוח" in fresh_name
        fresh_says_eggplant = fresh_name and "חציל" in fresh_name

        if has_apple and not has_eggplant:
            return (
                "name_was_right",
                "correct_data",
                "RESOLVED: Fresh Shufersal page confirms APPLE filling in ingredients. "
                "Prior eggplant (חצילים) ingredients were a scrape error — likely the wrong product "
                "page was served to the scraper (Shufersal URL routing glitch or caching). "
                f"Fresh name='{fresh_name}' is consistent. The name was always correct; "
                "prior ingredients_raw must be replaced with fresh apple-strudel ingredients."
            )
        elif has_eggplant and not has_apple:
            return (
                "ingredients_were_right",
                "discard",
                "DISCARD: Fresh Shufersal page STILL shows eggplant filling. "
                "Name 'מיני שטרודל תפוח עץ' does not match. Product identity unresolvable from the "
                "retail page alone; physical label would be needed. Missing-data rule applies — discard."
            )
        else:
            # Both or neither
            return (
                "still_conflicting",
                "discard",
                f"Fresh page ambiguous — has_apple={has_apple}, has_eggplant={has_eggplant}. "
                f"Fresh name='{fresh_name}'. "
                f"Ingredients (first 250): {ingredients_fresh[:250]!r}. "
                "Discard — cannot confirm without physical label."
            )

    elif barcode == "4504670":
        # Name: almond strudel (שקדים) / Previous ingredients: hard lean cheese (12%) + green olives
        has_almond = any(w in ingredients_fresh for w in ["שקד", "שקדים", "מלית שקד"])
        has_cheese = any(w in ingredients_fresh for w in ["גבינה", "גבינת"])
        has_olive = any(w in ingredients_fresh for w in ["זית", "זיתים"])

        if has_almond and not has_cheese and not has_olive:
            return (
                "name_was_right",
                "correct_data",
                "RESOLVED: Fresh Shufersal page confirms ALMOND filling. "
                "Prior cheese+olive ingredients were a scrape error (wrong product data returned). "
                f"Fresh name='{fresh_name}' confirms almond strudel. "
                "Replace prior ingredients with fresh almond-strudel ingredients."
            )
        elif (has_cheese or has_olive) and not has_almond:
            return (
                "ingredients_were_right",
                "discard",
                "DISCARD: Fresh page STILL shows cheese/olive ingredients for this barcode. "
                f"has_cheese={has_cheese}, has_olive={has_olive}. "
                "Product identity unresolvable from Shufersal data. Discard per missing-data rule."
            )
        elif has_almond and (has_cheese or has_olive):
            return (
                "still_conflicting",
                "discard",
                f"Fresh page shows almond AND cheese/olive — ambiguous. "
                f"has_almond={has_almond}, has_cheese={has_cheese}, has_olive={has_olive}. "
                "Discard — cannot confirm without physical label."
            )
        else:
            return (
                "still_conflicting",
                "discard",
                f"Fresh ingredients unclear. has_almond={has_almond}, has_cheese={has_cheese}, "
                f"has_olive={has_olive}. Fresh name='{fresh_name}'. "
                f"Ingredients (first 250): {ingredients_fresh[:250]!r}. Discard."
            )

    return "still_conflicting", "keep_deasserted", "Unknown barcode in strudel classifier"


def process_product(product):
    """Fetch, parse, and resolve one conflict product."""
    barcode = product["barcode"]
    url = product["source_url"]
    fetched_at = datetime.now(timezone.utc).isoformat()

    print(f"\n--- Processing {barcode} ---")
    print(f"  Conflict: {product['conflict_description']}")

    html, status_code, error = fetch_page(url)

    result = {
        "barcode": barcode,
        "category": product["category"],
        "conflict_description": product["conflict_description"],
        "retailer": "shufersal",
        "source_url": url,
        "fetched_at": fetched_at,
        "http_status": status_code,
        "reachable": html is not None and status_code == 200,
        "fetch_error": error,
        "fresh_name": None,
        "fresh_ingredients": None,
        "fresh_nutrition": None,
        "nutrition_plausibility_issues": [],
        "resolution": None,
        "resolution_notes": None,
        "recommended_action": None,
        "provenance": {
            "source": "shufersal_direct_scrape",
            "source_url": url,
            "fetched_at": fetched_at,
            "client": "rescrape_conflicts_v2.py/direct_urllib",
            "verification_status": "candidate",
            "off_used": False,
        }
    }

    if not result["reachable"]:
        print(f"  NOT REACHABLE: status={status_code} error={error}")
        result["resolution"] = "not_found"
        result["recommended_action"] = "discard"
        result["resolution_notes"] = (
            f"Shufersal page not reachable: HTTP {status_code}, error={error}. "
            "Missing-data rule: discard."
        )
        return result

    print(f"  Fetched: {len(html):,} bytes, HTTP {status_code}")

    # Extract fields
    fresh_name = extract_name_he(html)
    fresh_ingredients = extract_ingredients(html)
    fresh_nutrition = extract_nutrition(html)

    result["fresh_name"] = fresh_name
    result["fresh_ingredients"] = fresh_ingredients
    result["fresh_nutrition"] = fresh_nutrition

    print(f"  Fresh name: {fresh_name!r}")
    if fresh_ingredients:
        print(f"  Fresh ingredients ({len(fresh_ingredients)} chars): {fresh_ingredients[:150]!r}")
    else:
        print(f"  Fresh ingredients: NONE EXTRACTED")
    print(f"  Fresh nutrition: {fresh_nutrition}")

    # Plausibility gate
    if fresh_nutrition:
        issues = nutrition_plausibility_check(fresh_nutrition, barcode)
        result["nutrition_plausibility_issues"] = issues
        if issues:
            print(f"  NUTRITION ISSUES: {issues}")

    # Classify conflict
    if barcode == "7290108506624":
        resolution, recommended_action, notes = classify_goat_sheep_conflict(
            product["conflict_description"], fresh_name, fresh_ingredients
        )
    else:
        resolution, recommended_action, notes = classify_strudel_conflict(
            barcode, product["conflict_description"], fresh_name, fresh_ingredients
        )

    result["resolution"] = resolution
    result["recommended_action"] = recommended_action
    result["resolution_notes"] = notes

    print(f"  Resolution: {resolution} | Action: {recommended_action}")
    print(f"  Notes: {notes[:200]}")

    return result


def main():
    print("=== Bari Conflict Re-scrape v2 2026-06-25 ===")
    print(f"Products to process: {len(PRODUCTS)}")
    print("OFF ban: ABSOLUTE — source: direct Shufersal page only")
    print(f"Staging dir: {STAGING_DIR}")

    results = []
    for p in PRODUCTS:
        r = process_product(p)
        results.append(r)
        time.sleep(2)  # Polite delay

    # Build output
    output = {
        "run_id": "rescrape_conflicts_20260625",
        "run_date": datetime.now(timezone.utc).isoformat(),
        "off_used": False,
        "source": "shufersal_direct_scrape",
        "products": results,
    }

    out_path = os.path.join(STAGING_DIR, "rescrape_conflicts_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # sha256 of output
    with open(out_path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    print("\n=== SUMMARY ===")
    for r in results:
        print(
            f"  {r['barcode']}: reachable={r['reachable']} "
            f"resolution={r['resolution']} action={r['recommended_action']}"
        )

    print(f"\nOutput: {out_path}")
    print(f"SHA256: {sha256}")

    return sha256, results


if __name__ == "__main__":
    main()
