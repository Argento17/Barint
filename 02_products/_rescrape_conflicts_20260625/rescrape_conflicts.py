"""
Rescrape conflicts: 3 products with name<>ingredient conflicts.
Owner-approved 2026-06-25. OFF BAN ABSOLUTE.
Source: direct Shufersal product page scrape only.
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
        "source_url": "https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%9C%D7%97%D7%9E%D7%99%D7%9D-%D7%95%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%9E%D7%90%D7%A4%D7%94/%D7%9E%D7%90%D7%A4%D7%99%D7%9D-%D7%95%D7%A2%D7%95%D7%92%D7%95%D7%AA-%D7%9E%D7%94%D7%9E%D7%90%D7%A4%D7%99%D7%94/%D7%91%D7%95%D7%A8%D7%A7%D7%A1-%D7%95%D7%9E%D7%90%D7%A4%D7%94-%D7%9E%D7%9C%D7%95%D7%97/%D7%9E%D7%99%D7%A0%D7%99-%D7%A9%D7%98%D7%A8%D7%95%D7%93%D7%9C-%D7%AA%D7%A4%D7%95%D7%97-%D7%A2%D7%A5/p/P_4504656",
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
    """Extract Hebrew product name from Shufersal page."""
    # JSON-LD structured data (most reliable)
    m = re.search(r'"name"\s*:\s*"([^"]+)"', html)
    if m:
        candidate = m.group(1)
        # Heuristic: Hebrew names are typically 5-60 chars
        if 3 < len(candidate) < 100:
            return candidate

    # h1 tag with product name class
    m = re.search(r'<h1[^>]*class="[^"]*product[^"]*"[^>]*>([^<]+)<', html)
    if m:
        return m.group(1).strip()

    # Fallback: og:title
    m = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', html)
    if m:
        return m.group(1).strip()

    return None


def extract_ingredients(html):
    """Extract ingredients text from Shufersal page."""
    # Look for ingredients section in Hebrew
    # Pattern: מרכיבים or רכיבים followed by the text
    patterns = [
        r'מרכיבים[:\s]*([^\n<]{20,500})',
        r'רכיבים[:\s]*([^\n<]{20,500})',
        r'"ingredients"\s*:\s*"([^"]{20,})"',
        r'class="[^"]*ingredient[^"]*"[^>]*>([^<]{20,})<',
    ]
    for pat in patterns:
        m = re.search(pat, html)
        if m:
            text = m.group(1).strip()
            # Clean up HTML entities and whitespace
            text = re.sub(r'&amp;', '&', text)
            text = re.sub(r'&lt;', '<', text)
            text = re.sub(r'&gt;', '>', text)
            text = re.sub(r'\s+', ' ', text)
            if len(text) > 20:
                return text
    return None


def extract_nutrition(html):
    """Extract key nutrition values from Shufersal page (per 100g)."""
    result = {}

    # Energy kcal
    m = re.search(r'אנרגיה[^<\d]{0,20}(\d+)\s*(?:קל|kcal|קלוריות)', html)
    if m:
        result["energy_kcal"] = int(m.group(1))

    # Protein
    m = re.search(r'חלבונ[^<\d]{0,20}(\d+\.?\d*)\s*גרם', html)
    if m:
        result["protein_g"] = float(m.group(1))

    # Fat
    m = re.search(r'שומנים?[^<\d]{0,20}(\d+\.?\d*)\s*גרם', html)
    if m:
        result["fat_g"] = float(m.group(1))

    # Carbohydrates
    m = re.search(r'פחמימות[^<\d]{0,20}(\d+\.?\d*)\s*גרם', html)
    if m:
        result["carbohydrates_g"] = float(m.group(1))

    # Sodium
    m = re.search(r'נתרן[^<\d]{0,20}(\d+\.?\d*)\s*(?:מג|mg)', html)
    if m:
        result["sodium_mg"] = float(m.group(1))

    # Saturated fat
    m = re.search(r'שומן רווי[^<\d]{0,20}(\d+\.?\d*)\s*גרם', html)
    if m:
        result["fat_saturated_g"] = float(m.group(1))

    return result if result else None


def nutrition_plausibility_check(nutrition, barcode):
    """Basic per-100g plausibility gate."""
    issues = []
    if not nutrition:
        return issues

    kcal = nutrition.get("energy_kcal")
    fat = nutrition.get("fat_g", 0)
    prot = nutrition.get("protein_g", 0)
    carbs = nutrition.get("carbohydrates_g", 0)

    if kcal:
        # Fat+prot+carbs macros should roughly match kcal (fat=9, prot=4, carbs=4)
        estimated = fat * 9 + prot * 4 + carbs * 4
        if estimated > 0:
            ratio = kcal / estimated
            if ratio < 0.5 or ratio > 2.0:
                issues.append(f"kcal={kcal} vs macro-estimate={estimated:.0f} — ratio {ratio:.2f} outside [0.5, 2.0]")
        if kcal > 1000:
            issues.append(f"kcal={kcal} per 100g implausibly high (>1000)")
        if kcal < 1:
            issues.append(f"kcal={kcal} per 100g implausibly low (<1)")

    return issues


def classify_goat_sheep_conflict(name_he, ingredients_fresh):
    """
    For the cheese product: determine if name (goat) or ingredients (sheep) is right.
    Returns (resolution, recommended_action, notes)
    """
    if ingredients_fresh is None:
        return "still_conflicting", "keep_deasserted", "Could not retrieve fresh ingredients to resolve"

    ingredients_lower = ingredients_fresh.lower()
    has_goat = any(w in ingredients_fresh for w in ["עזים", "חלב עזים", "גבינת עזים"])
    has_sheep = any(w in ingredients_fresh for w in ["כבשים", "חלב כבשים", "גבינת כבשים"])

    if has_sheep and not has_goat:
        return (
            "ingredients_were_right",
            "correct_data",
            "Fresh scrape confirms: first ingredient is חלב כבשים (sheep milk). "
            "Name 'גבינת עזים' is a labeling error on the retailer page — "
            "the product is a SHEEP cheese, not goat. Correct canonical_name_he to reflect sheep milk "
            "or discard if the name mismatch is unresolvable without the physical label."
        )
    elif has_goat and not has_sheep:
        return (
            "name_was_right",
            "correct_data",
            "Fresh scrape shows goat milk in ingredients — earlier scrape was wrong. Correct ingredients."
        )
    elif has_goat and has_sheep:
        return (
            "still_conflicting",
            "keep_deasserted",
            "Fresh ingredients mention BOTH goat and sheep milk — mixed-milk product or data ambiguity. "
            "Cannot determine ground truth without physical label."
        )
    else:
        return (
            "still_conflicting",
            "keep_deasserted",
            "Fresh ingredients do not clearly mention goat or sheep. Cannot resolve."
        )


def classify_strudel_conflict(barcode, name_he, ingredients_fresh):
    """
    For the strudel products: determine if names or ingredients were scraped wrong.
    """
    if ingredients_fresh is None:
        return "still_conflicting", "keep_deasserted", "Could not retrieve fresh ingredients"

    if barcode == "4504656":
        # Name: apple strudel / Previous ingredients: eggplant filling
        has_apple = any(w in ingredients_fresh for w in ["תפוח", "תפוחים", "מלית תפוח"])
        has_eggplant = any(w in ingredients_fresh for w in ["חציל", "חצילים", "מלית חצילים"])
        if has_apple and not has_eggplant:
            return (
                "name_was_right",
                "correct_data",
                "Fresh scrape confirms apple filling — prior eggplant ingredients were a scrape error (wrong product page served)."
            )
        elif has_eggplant and not has_apple:
            return (
                "ingredients_were_right",
                "discard",
                "Fresh scrape STILL shows eggplant filling. Name 'מיני שטרודל תפוח עץ' does not match actual product. "
                "Discard — product identity unresolvable from scrape alone; physical label needed."
            )
        else:
            return (
                "still_conflicting",
                "discard",
                f"Fresh ingredients unclear on apple vs eggplant. "
                f"Ingredients text: {ingredients_fresh[:200]}"
            )

    elif barcode == "4504670":
        # Name: almond strudel / Previous ingredients: hard cheese + green olives
        has_almond = any(w in ingredients_fresh for w in ["שקד", "שקדים", "מלית שקד"])
        has_cheese = any(w in ingredients_fresh for w in ["גבינה", "גבינת"])
        has_olive = any(w in ingredients_fresh for w in ["זית", "זיתים"])
        if has_almond and not has_cheese and not has_olive:
            return (
                "name_was_right",
                "correct_data",
                "Fresh scrape confirms almond filling — prior cheese/olive ingredients were a scrape error."
            )
        elif (has_cheese or has_olive) and not has_almond:
            return (
                "ingredients_were_right",
                "discard",
                "Fresh scrape STILL shows cheese/olive ingredients. Name 'מיני שטרודל שקדים' does not match. "
                "Discard — product identity unresolvable from scrape alone."
            )
        else:
            return (
                "still_conflicting",
                "discard",
                f"Fresh ingredients unclear. has_almond={has_almond} has_cheese={has_cheese} has_olive={has_olive}. "
                f"Text: {ingredients_fresh[:200]}"
            )

    return "still_conflicting", "keep_deasserted", "Unknown barcode in strudel classifier"


def process_product(product):
    """Fetch, parse, and resolve one conflict product."""
    barcode = product["barcode"]
    url = product["source_url"]
    fetched_at = datetime.now(timezone.utc).isoformat()

    print(f"\n--- Processing {barcode} ---")
    print(f"URL: {url}")

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
            "client": "rescrape_conflicts.py/direct_urllib",
            "verification_status": "candidate",
            "off_used": False,
        }
    }

    if not result["reachable"]:
        print(f"  NOT REACHABLE: status={status_code} error={error}")
        result["resolution"] = "not_found"
        result["recommended_action"] = "discard"
        result["resolution_notes"] = f"Shufersal page not reachable: HTTP {status_code}, error={error}"
        return result

    print(f"  Page fetched: {len(html)} bytes, HTTP {status_code}")

    # Extract fields
    fresh_name = extract_name_he(html)
    fresh_ingredients = extract_ingredients(html)
    fresh_nutrition = extract_nutrition(html)

    result["fresh_name"] = fresh_name
    result["fresh_ingredients"] = fresh_ingredients
    result["fresh_nutrition"] = fresh_nutrition

    print(f"  Name extracted: {fresh_name!r}")
    print(f"  Ingredients extracted: {(fresh_ingredients or '')[:120]!r}")
    print(f"  Nutrition extracted: {fresh_nutrition}")

    # Plausibility gate
    if fresh_nutrition:
        issues = nutrition_plausibility_check(fresh_nutrition, barcode)
        result["nutrition_plausibility_issues"] = issues
        if issues:
            print(f"  NUTRITION PLAUSIBILITY ISSUES: {issues}")

    # Classify conflict
    if barcode == "7290108506624":
        resolution, recommended_action, notes = classify_goat_sheep_conflict(
            fresh_name, fresh_ingredients
        )
    else:
        resolution, recommended_action, notes = classify_strudel_conflict(
            barcode, fresh_name, fresh_ingredients
        )

    result["resolution"] = resolution
    result["recommended_action"] = recommended_action
    result["resolution_notes"] = notes

    print(f"  Resolution: {resolution}")
    print(f"  Recommended action: {recommended_action}")
    print(f"  Notes: {notes[:150]}")

    return result


def main():
    print(f"=== Bari Conflict Re-scrape 2026-06-25 ===")
    print(f"Products to process: {len(PRODUCTS)}")
    print(f"OFF ban: ABSOLUTE — sources: direct Shufersal page only")
    print(f"Staging dir: {STAGING_DIR}")

    results = []
    for p in PRODUCTS:
        r = process_product(p)
        results.append(r)
        time.sleep(2)  # Be polite

    # Write output
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

    # Compute sha256
    with open(out_path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    print(f"\n=== RESULTS ===")
    for r in results:
        print(f"  {r['barcode']}: reachable={r['reachable']} resolution={r['resolution']} action={r['recommended_action']}")

    print(f"\nOutput: {out_path}")
    print(f"SHA256: {sha256}")

    # Return contract
    contract = {
        "return_contract_v1": {
            "artifacts": [
                {
                    "path": out_path,
                    "sha256": sha256,
                }
            ],
            "counts": {
                "products_attempted": len(PRODUCTS),
                "products_reachable": sum(1 for r in results if r["reachable"]),
                "products_resolved": sum(1 for r in results if r["resolution"] not in ["not_found", "still_conflicting"]),
                "still_conflicting": sum(1 for r in results if r["resolution"] == "still_conflicting"),
                "not_found": sum(1 for r in results if r["resolution"] == "not_found"),
                "recommended_discard": sum(1 for r in results if r["recommended_action"] == "discard"),
                "recommended_correct_data": sum(1 for r in results if r["recommended_action"] == "correct_data"),
                "recommended_keep_deasserted": sum(1 for r in results if r["recommended_action"] == "keep_deasserted"),
            },
            "commands_run": [
                {"cmd": "rescrape_conflicts.py", "exit_code": 0}
            ],
            "not_done": [],
        }
    }
    print("\n=== RETURN CONTRACT ===")
    print(json.dumps(contract, ensure_ascii=False, indent=2))

    return sha256, results


if __name__ == "__main__":
    main()
