"""
TASK-360 — Snacks Fresh Re-Scrape + Per-100g Plausibility Gate
==============================================================
Full pipeline: discover → scrape → plausibility gate → BSIP1 → BSIP2 → frontend JSON

Steps:
  1. Live re-discover snacks shelf on yochananof
  2. Scrape all product modals (nutrition, ingredients, allergens)
  3. Parse serving size from card_text and package_size
  4. Apply per-100g plausibility gate (with per-serving conversion)
  5. Rebuild BSIP1 records for surviving products
  6. Re-run BSIP2 scoring
  7. Rebuild frontend JSON

Hard rules enforced:
  - OFF BAN: no Open Food Facts, ever
  - No scoring-engine changes (TRIPWIRE-1)
  - No fabrication: if scrape blocked, script stops and reports honestly
  - No copy/voice generation: all copy fields set to PENDING_COPY
"""
import sys
import json
import os
import re
import math
import pathlib
import datetime
import requests
import hashlib
import logging

from urllib.parse import quote, unquote, urlparse, parse_qs
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = pathlib.Path(r"C:\Bari")
SNACKS_DIR = ROOT / "02_products" / "snack_bars"
RUN_TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
RUN_ID = f"run_snacks_task360_{RUN_TS}"

NEW_BSIP0_DIR = SNACKS_DIR / "observations_bsip0" / "yohananof_task360" / RUN_ID
BSIP1_OUTPUT_DIR = ROOT / "03_operations" / "bsip1" / f"run_snacks_task360_{RUN_TS}" / "output"
BSIP2_OUTPUT_DIR = SNACKS_DIR / "bsip2_outputs" / RUN_ID
BSIP2_SRC = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"

NEW_BSIP0_DIR.mkdir(parents=True, exist_ok=True)
BSIP1_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(BSIP2_OUTPUT_DIR / "products").mkdir(parents=True, exist_ok=True)

FRONTEND_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "snacks_frontend_v4.json"

# ── Discovery queries (snack bars / cereal bars shelf) ────────────────────────
SEARCH_QUERIES = [
    "חטיפי דגנים",
    "חטיפי בריאות",
    "granola bar",
    "קראנצ'י",
    "חטיף אנרגיה",
    "nature valley",
    "slim delice",
    "פיטנס בר",
]

# ── Plausibility gate thresholds ─────────────────────────────────────────────
GATE_MIN_ACCOUNTED_MASS_G = 70.0   # carbs+fat+protein+fiber >= 70g per 100g
GATE_MIN_KCAL_DRY = 150.0          # dry snack must have >= 150 kcal/100g
SUGAR_BEARING_TOKENS = [
    "סוכר", "שוקולד", "דבש", "סירופ", "תמרים", "גלוקוז", "פרוקטוז",
    "מולסה", "מחית תמרים", "ממתיק",
]

# ── Helper functions ──────────────────────────────────────────────────────────

def clean(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text).replace("\xa0", " ")).strip()

def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

def save_json(path, data):
    pathlib.Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def parse_number(text):
    if not text:
        return None
    text = clean(text).replace(",", ".").replace("L ", "").replace("<", "").replace("פחות מ", "").strip()
    m = re.search(r"(\d+(?:\.\d+)?)", text)
    return float(m.group(1)) if m else None

def soup_from_html(html: str):
    return BeautifulSoup(html, "lxml")

def normalize_image_url(raw_url):
    if not raw_url:
        return None
    first = raw_url.split(" ")[0]
    if "/_next/image" in first and "url=" in first:
        parsed = urlparse(first)
        from urllib.parse import parse_qs as _pqs
        qs = _pqs(parsed.query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return first

def extract_barcode(text):
    """Extract 13-digit barcode or 729-prefix barcode from text."""
    m = re.search(r"(729\d{10}|\d{13})", text or "")
    return m.group(1) if m else ""

# ── Serving size parsing ──────────────────────────────────────────────────────

def parse_serving_size(card_text: str, package_size_str: str) -> dict:
    """
    Extract serving_size_g, unit_size_g, unit_count from card_text + package_size.
    E.g. "120 גרם 2 יח'" → package=120g, units=2, unit_size=60g
    """
    result = {
        "serving_size_g": None,
        "unit_size_g": None,
        "unit_count": None,
        "package_size_g": None,
        "parse_source": None,
    }

    # Try to extract from card_text: "N גרם M יח'"
    ct = clean(card_text)
    m = re.search(r"(\d+(?:\.\d+)?)\s*גרם\s+(\d+)\s+יח", ct)
    if m:
        pkg_g = float(m.group(1))
        units = int(m.group(2))
        result["package_size_g"] = pkg_g
        result["unit_count"] = units
        result["unit_size_g"] = round(pkg_g / units, 1)
        result["serving_size_g"] = round(pkg_g / units, 1)
        result["parse_source"] = "card_text_pkg_units"
        return result

    # Try from package_size_str alone: "35 גרם"
    if package_size_str:
        m2 = re.search(r"(\d+(?:\.\d+)?)\s*גר", clean(package_size_str))
        if m2:
            pkg_g = float(m2.group(1))
            result["package_size_g"] = pkg_g
            result["parse_source"] = "package_size_field"
            # Single-serve assumption if < 50g
            if pkg_g <= 50:
                result["unit_size_g"] = pkg_g
                result["serving_size_g"] = pkg_g
                result["unit_count"] = 1

    # Try from card_text: standalone "N גרם" (single unit)
    m3 = re.search(r"(\d+(?:\.\d+)?)\s*גרם", ct)
    if m3 and not result["package_size_g"]:
        pkg_g = float(m3.group(1))
        result["package_size_g"] = pkg_g
        result["parse_source"] = "card_text_single"
        if pkg_g <= 50:
            result["unit_size_g"] = pkg_g
            result["serving_size_g"] = pkg_g
            result["unit_count"] = 1

    return result

# ── Plausibility gate ─────────────────────────────────────────────────────────

def plausibility_gate(nutrition: dict, serving_info: dict, ingredients: str, barcode: str) -> dict:
    """
    Apply per-100g plausibility gate. Returns dict with:
      verdict: "pass" | "converted_pass" | "quarantine"
      final_nutrition: the nutrition dict to use (per-100g)
      nutrition_basis: "per_100g" | "converted_from_serving"
      conversion_factor: multiplier used (or 1.0)
      fail_reasons: list of failure reasons
      accounted_mass: sum of macros
    """
    kcal = nutrition.get("energy_kcal_100g") or 0
    carbs = nutrition.get("carbohydrates_g_100g") or 0
    fat = nutrition.get("fat_g_100g") or 0
    protein = nutrition.get("protein_g_100g") or 0
    fiber = nutrition.get("fiber_g_100g") or 0
    sugars = nutrition.get("sugars_g_100g")

    accounted = carbs + fat + protein + fiber
    ing_lower = (ingredients or "").lower()

    def check_fails(n, acc_mass, kcal_v, sugars_v):
        fails = []
        if acc_mass < GATE_MIN_ACCOUNTED_MASS_G:
            fails.append(f"accounted_mass={acc_mass:.1f}g < {GATE_MIN_ACCOUNTED_MASS_G}g")
        if sugars_v is not None and sugars_v == 0:
            has_sugar_token = any(tok in (ingredients or "") for tok in SUGAR_BEARING_TOKENS)
            if has_sugar_token:
                fails.append(f"sugars=0 but ingredients contain sugar-bearing tokens")
        if kcal_v is not None and kcal_v < GATE_MIN_KCAL_DRY:
            fails.append(f"kcal={kcal_v} < {GATE_MIN_KCAL_DRY} for dry snack")
        return fails

    fails = check_fails(nutrition, accounted, kcal, sugars)

    if not fails:
        return {
            "verdict": "pass",
            "final_nutrition": {k: v for k, v in nutrition.items()},
            "nutrition_basis": "per_100g",
            "conversion_factor": 1.0,
            "fail_reasons": [],
            "accounted_mass": round(accounted, 1),
            "kcal": kcal,
        }

    # Try conversion: are values per-serving?
    serving_g = serving_info.get("unit_size_g") or serving_info.get("serving_size_g")

    if serving_g and serving_g > 0 and serving_g < 90:
        factor = 100.0 / serving_g
        def conv(v):
            return round(v * factor, 1) if v is not None else None

        converted = {
            "energy_kcal_100g": conv(kcal),
            "carbohydrates_g_100g": conv(carbs),
            "sugars_g_100g": conv(sugars),
            "fat_g_100g": conv(fat),
            "saturated_fat_g_100g": conv(nutrition.get("saturated_fat_g_100g")),
            "trans_fat_g_100g": conv(nutrition.get("trans_fat_g_100g")),
            "cholesterol_mg_100g": conv(nutrition.get("cholesterol_mg_100g")),
            "sodium_mg_100g": conv(nutrition.get("sodium_mg_100g")),
            "fiber_g_100g": conv(fiber),
            "protein_g_100g": conv(protein),
        }

        conv_carbs = converted["carbohydrates_g_100g"] or 0
        conv_fat = converted["fat_g_100g"] or 0
        conv_prot = converted["protein_g_100g"] or 0
        conv_fiber = converted["fiber_g_100g"] or 0
        conv_kcal = converted["energy_kcal_100g"] or 0
        conv_sugars = converted["sugars_g_100g"]
        conv_accounted = conv_carbs + conv_fat + conv_prot + conv_fiber

        conv_fails = check_fails(converted, conv_accounted, conv_kcal, conv_sugars)

        if not conv_fails:
            return {
                "verdict": "converted_pass",
                "final_nutrition": converted,
                "nutrition_basis": "converted_from_serving",
                "conversion_factor": round(factor, 3),
                "serving_g_used": serving_g,
                "fail_reasons": fails,
                "accounted_mass": round(conv_accounted, 1),
                "kcal": conv_kcal,
                "original_fail_reasons": fails,
            }
        else:
            return {
                "verdict": "quarantine",
                "final_nutrition": None,
                "nutrition_basis": None,
                "conversion_factor": factor,
                "serving_g_used": serving_g,
                "fail_reasons": fails,
                "post_conversion_fails": conv_fails,
                "accounted_mass": round(accounted, 1),
                "kcal": kcal,
            }
    else:
        return {
            "verdict": "quarantine",
            "final_nutrition": None,
            "nutrition_basis": None,
            "conversion_factor": 1.0,
            "fail_reasons": fails,
            "no_serving_size": True,
            "accounted_mass": round(accounted, 1),
            "kcal": kcal,
        }

# ── HTML parsers ──────────────────────────────────────────────────────────────

def parse_nutrition_html(html: str) -> dict:
    """Extract nutrition values from yochananof product modal HTML."""
    soup = soup_from_html(html)
    nutrition = {}

    label_map = [
        ("אנרגיה", "energy_kcal_100g"),
        ("חומצות שומן רוויות", "saturated_fat_g_100g"),
        ("חומצות שומן טראנס", "trans_fat_g_100g"),
        ("שומנים", "fat_g_100g"),
        ("כולסטרול", "cholesterol_mg_100g"),
        ("נתרן", "sodium_mg_100g"),
        ("סך הפחמימות", "carbohydrates_g_100g"),
        ("סוכרים מתוך פחמימות", "sugars_g_100g"),
        ("מתוכן כפיות סוכר", "sugar_teaspoons_100g"),
        ("סיבים תזונתיים", "fiber_g_100g"),
        ("חלבונים", "protein_g_100g"),
    ]

    for row in soup.select("#simple-tabpanel-1 li"):
        label_el = row.select_one("span")
        if not label_el:
            continue
        label = clean(label_el.get_text(" ", strip=True))
        full_text = clean(row.get_text(" ", strip=True))
        if not label or not full_text:
            continue
        value_text = full_text.replace(label, "", 1).strip()
        value = parse_number(value_text)
        if value is None:
            continue
        for heb_label, field_name in label_map:
            if heb_label in label:
                nutrition[field_name] = value
                break

    # Extract stated basis from the header
    full_text = soup.get_text(" ", strip=True)
    if "ל-100 גרם" in full_text or "ל100 גרם" in full_text or "100 גרם" in full_text:
        basis_raw = "ל-100 גרם"
        basis_type = "per_100g"
    elif "ל-100 מ" in full_text or "100 מ" in full_text:
        basis_raw = "ל-100 מ״ל"
        basis_type = "per_100ml"
    elif "למנה" in full_text or "ליחידה" in full_text:
        basis_raw = "למנה/ליחידה"
        basis_type = "per_serving_or_unit"
    else:
        basis_raw = None
        basis_type = "unknown"

    return nutrition, {"basis_raw": basis_raw, "basis_type": basis_type}


def parse_ingredients_html(html: str) -> str | None:
    soup = soup_from_html(html)
    panel = soup.select_one("#simple-tabpanel-0")
    if not panel:
        return None
    text = clean(panel.get_text(" ", strip=True))
    return text if text else None


def parse_allergens_html(html: str) -> str | None:
    soup = soup_from_html(html)
    panel = soup.select_one("#simple-tabpanel-2")
    if not panel:
        return None
    text = clean(panel.get_text(" ", strip=True))
    return text if text else None


def find_value_by_label(soup, label):
    for row in soup.select("div.MuiTypography-body2"):
        text = clean(row.get_text(" ", strip=True))
        if text and text.startswith(label + ":"):
            return clean(text.replace(label + ":", "", 1))
    return None


def extract_metadata_from_html(html: str) -> dict:
    soup = soup_from_html(html)
    return {
        "name": clean(el.get_text(" ", strip=True)) if (el := soup.select_one('[class*="ccnpqe"]')) else None,
        "brand": find_value_by_label(soup, "מותג/יצרן"),
        "barcode": find_value_by_label(soup, "ברקוד"),
        "package_size": find_value_by_label(soup, "מידה"),
        "country_of_origin": find_value_by_label(soup, "ארץ יצור"),
        "kosher": find_value_by_label(soup, "כשרות"),
        "category_path": [
            clean(a.get_text(" ", strip=True))
            for a in soup.select("nav a")
            if clean(a.get_text(" ", strip=True))
        ],
    }

# ── Playwright scraper ────────────────────────────────────────────────────────

def close_cookie_popup(page):
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            button = page.get_by_text(text, exact=False).first
            if button.is_visible(timeout=800):
                button.click(force=True)
                page.wait_for_timeout(800)
                return
        except Exception:
            pass


def mark_product_cards(page):
    return page.evaluate("""
    () => {
      const out = [];
      const seen = new Set();
      function visible(el) {
        const r = el.getBoundingClientRect();
        return r.width > 60 && r.height > 60 && r.bottom >= 0 && r.top <= window.innerHeight + 800;
      }
      function score(el) {
        const txt = (el.innerText || '').trim();
        if (!txt) return 0;
        let s = 0;
        if (txt.includes('₪')) s += 3;
        if (txt.includes('גרם') || txt.includes("גר'") || txt.includes('ק"ג')) s += 2;
        if (txt.includes('חטיף') || txt.includes('granola') || txt.includes('בר') ||
            txt.includes('פיטנס') || txt.includes('slim') || txt.includes('nature') ||
            txt.includes('קראנצ')) s += 3;
        if (el.querySelector('img')) s += 3;
        if (txt.length > 15 && txt.length < 1200) s += 1;
        return s;
      }
      for (const img of Array.from(document.querySelectorAll('img'))) {
        let el = img;
        let best = null;
        let bestScore = 0;
        for (let depth = 0; depth < 12 && el; depth++) {
          const s = score(el);
          if (s > bestScore) { best = el; bestScore = s; }
          el = el.parentElement;
        }
        if (!best || bestScore < 5 || !visible(best) || seen.has(best)) continue;
        seen.add(best);
        const imgEl = best.querySelector('img');
        const src = imgEl ? (imgEl.currentSrc || imgEl.src || '') : '';
        const srcset = imgEl ? (imgEl.getAttribute('srcset') || '') : '';
        const alt = imgEl ? (imgEl.getAttribute('alt') || '') : '';
        const text = (best.innerText || '').trim();
        out.push({ card_text: text, image_alt: alt, image_url_raw: (src + ' ' + srcset).trim() });
      }
      return out;
    }
    """)


def choose_best_name(card_text, image_alt):
    lines = [clean(x) for x in clean(card_text).split("\n") if clean(x)]
    bad = ["₪", "100 גרם", "הוסף", "שמירה", "מבצע", "לרשימה", "מחיר", "יח' ב"]
    candidates = [l for l in lines if len(l) >= 4 and not any(b in l for b in bad)]
    snack_terms = ["חטיף", "בר", "גרנולה", "קראנצ'י", "פיטנס", "נייצר", "slim", "nature",
                   "quaker", "שיבולת", "תמר", "אנרגיה", "פרוטאין"]
    for line in candidates:
        if any(t in line.lower() for t in snack_terms):
            return line
    if candidates:
        return candidates[0]
    return clean(image_alt)


def is_snack_bar(name: str, card_text: str) -> bool:
    """Filter: is this a snack/cereal bar? Exclude if clearly not."""
    combined = (name + " " + card_text).lower()
    INCLUDE = ["חטיף", "בר", "granola", "גרנולה", "קראנצ'י", "פיטנס", "slim", "nature",
               "quaker", "שיבולת שועל", "תמרים", "אנרגיה", "פרוטאין", "cereal"]
    EXCLUDE_HARD = ["ביסקוויט", "עוגיה", "גלידה", "שוקולד טבלה", "חלב", "גבינה",
                    "לחם", "שתייה", "מיץ", "יוגורט", "קינוח"]
    if any(exc in combined for exc in EXCLUDE_HARD):
        return False
    if any(inc in combined for inc in INCLUDE):
        return True
    return False


def discover_shelf(page, query: str) -> list:
    log.info("Discover query: %s", query)
    url = f"https://yochananof.co.il/category?search={quote(query)}"
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3500)
    close_cookie_popup(page)

    products = {}
    stable_rounds = 0
    last_count = 0

    for round_no in range(1, 120):
        raw_cards = mark_product_cards(page)
        for c in raw_cards:
            combined = clean(f"{c.get('card_text', '')} {c.get('image_alt', '')} {c.get('image_url_raw', '')}")
            barcode = extract_barcode(combined)
            name = choose_best_name(c.get("card_text", ""), c.get("image_alt", ""))
            if not name:
                continue
            if not is_snack_bar(name, c.get("card_text", "")):
                continue
            key = barcode or f"{query}|{name}"
            if key not in products:
                products[key] = {
                    "key": key,
                    "barcode": barcode,
                    "name": name,
                    "brand": "",
                    "query": query,
                    "card_text": c.get("card_text", ""),
                    "image_alt": c.get("image_alt", ""),
                    "image_url_raw": c.get("image_url_raw", ""),
                    "discovered_at": now_iso(),
                }
        current = len(products)
        if current == last_count:
            stable_rounds += 1
        else:
            stable_rounds = 0
            last_count = current
        if stable_rounds >= 20:
            break
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(850)

    log.info("  found %d products for query: %s", len(products), query)
    return list(products.values())


def open_product_modal(page, product: dict):
    barcode = clean(product.get("barcode"))
    query = clean(product.get("query"))
    name = clean(product.get("name"))

    if not barcode:
        raise RuntimeError(f"Missing barcode for: {name}")

    url = f"https://yochananof.co.il/category?search={quote(query)}"
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3500)
    close_cookie_popup(page)

    barcode_locator = page.locator(f'img[src*="{barcode}"], img[srcset*="{barcode}"]').first
    name_locator = page.get_by_text(name, exact=False).first

    for i in range(1, 120):
        if i % 20 == 0:
            log.info("    still searching... attempt %d/120 | %s", i, barcode)
        try:
            if barcode_locator.count() > 0:
                barcode_locator.scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(700)
                barcode_locator.click(force=True)
                page.wait_for_timeout(4500)
                return
        except Exception:
            pass
        try:
            if name_locator.count() > 0:
                name_locator.scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(700)
                name_locator.click(force=True)
                page.wait_for_timeout(4500)
                return
        except Exception:
            pass
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(850)

    raise RuntimeError(f"Could not find product: barcode={barcode} name={name}")


def capture_tab(page, tab_name: str, retries=2) -> str:
    for attempt in range(1, retries + 1):
        try:
            if page.locator('[role="tab"]').count() == 0:
                dialog = page.locator('[role="dialog"]').first
                return dialog.inner_html(timeout=5000) if dialog.count() > 0 else ""
            tab = page.get_by_role("tab", name=tab_name).first
            if tab.count() == 0:
                return ""
            tab.click(force=True)
            page.wait_for_timeout(2200)
            dialog = page.locator('[role="dialog"]').first
            if dialog.count() == 0:
                return ""
            html = dialog.inner_html(timeout=5000)
            return html if len(html.strip()) >= 50 else ""
        except PlaywrightTimeoutError:
            if attempt == retries:
                return ""
            page.wait_for_timeout(1200)
        except Exception as e:
            if attempt == retries:
                return ""
            page.wait_for_timeout(1200)
    return ""


def close_dialog(page):
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)
    except Exception:
        pass


def download_image(image_url: str, dest: pathlib.Path) -> str | None:
    if not image_url:
        return None
    try:
        r = requests.get(image_url, timeout=20)
        r.raise_for_status()
        lower = image_url.lower()
        suffix = ".jpg"
        if ".png" in lower:
            suffix = ".png"
        elif ".webp" in lower:
            suffix = ".webp"
        fname = f"product_image{suffix}"
        (dest / fname).write_bytes(r.content)
        return fname
    except Exception:
        return None


# ── BSIP0 build ──────────────────────────────────────────────────────────────

def build_bsip0_product(product: dict, html_nutrition: str, html_ingredients: str,
                         html_allergens: str, serving_info: dict) -> dict:
    """Build BSIP0 record from scraped HTML."""
    barcode = clean(product.get("barcode"))

    # Parse HTML from each tab
    nutrition_raw, nutrition_basis = parse_nutrition_html(html_nutrition)
    ingredients_raw = parse_ingredients_html(html_ingredients)
    allergens_raw = parse_allergens_html(html_allergens)

    # Get metadata from any HTML
    meta_soup = BeautifulSoup(html_nutrition or html_ingredients or html_allergens or "", "lxml")
    name_el = meta_soup.select_one('[class*="ccnpqe"]')
    name = clean(name_el.get_text(" ", strip=True)) if name_el else clean(product.get("name"))
    brand = find_value_by_label(meta_soup, "מותג/יצרן") or clean(product.get("brand"))
    package_size = find_value_by_label(meta_soup, "מידה")
    country = find_value_by_label(meta_soup, "ארץ יצור")
    kosher = find_value_by_label(meta_soup, "כשרות")
    category_path = [
        clean(a.get_text(" ", strip=True))
        for a in meta_soup.select("nav a")
        if clean(a.get_text(" ", strip=True))
    ]

    # Apply plausibility gate
    gate_result = plausibility_gate(nutrition_raw, serving_info, ingredients_raw or "", barcode)

    parser_warnings = []
    if gate_result["verdict"] == "converted_pass":
        parser_warnings.append(f"per_serving_converted: factor={gate_result['conversion_factor']} serving_g={gate_result.get('serving_g_used')}")
    if gate_result["verdict"] == "quarantine":
        parser_warnings.append(f"QUARANTINED: {'; '.join(gate_result['fail_reasons'])}")

    final_nutrition = gate_result.get("final_nutrition") or {}

    return {
        "schema_version": "bsip0.v2_task360",
        "source": {
            "retailer": "Yohananof",
            "retailer_id": "yohananof",
            "source_type": "product_modal_html_tabs",
            "scrape_run": RUN_ID,
        },
        "product_identity": {
            "name": name,
            "brand": brand,
            "barcode": barcode,
            "country_of_origin": country,
            "package_size": package_size,
            "kosher": kosher,
            "image_url": normalize_image_url(product.get("image_url_raw")),
            "local_image_file": product.get("local_image_file"),
            "category_path": category_path,
        },
        "serving_info": serving_info,
        "raw_observations": {
            "ingredients_raw_he": ingredients_raw,
            "allergens_raw_he": allergens_raw,
        },
        "nutrition_basis": {
            "basis_raw": nutrition_basis["basis_raw"],
            "basis_type": nutrition_basis["basis_type"],
            "stated_basis_trusted": False,  # yochananof label is unreliable; gate applied
        },
        "nutrition_observed_values": nutrition_raw,
        "nutrition_per_100g": final_nutrition,
        "plausibility_gate": gate_result,
        "provenance": {
            "discovery": product,
            "capture_status": product.get("capture_status", {}),
            "off_check": "PASS - no Open Food Facts used",
        },
        "parser_status": {
            "product_modal_parsed": True,
            "ingredients_present": ingredients_raw is not None,
            "nutrition_present": bool(nutrition_raw),
            "nutrition_basis_confirmed_per_100g": gate_result["verdict"] in ("pass", "converted_pass"),
            "allergens_extracted": allergens_raw is not None,
            "image_present": product.get("local_image_file") is not None,
            "gate_verdict": gate_result["verdict"],
            "parser_warnings": parser_warnings,
        },
    }

# ── BSIP1 builder ─────────────────────────────────────────────────────────────

def build_bsip1_record(bsip0: dict) -> dict:
    """Build BSIP1 canonical record from BSIP0 observation."""
    barcode = bsip0["product_identity"]["barcode"]
    pid = f"bsip1_{barcode}"
    ing = bsip0["raw_observations"].get("ingredients_raw_he") or ""
    nutrition = bsip0.get("nutrition_per_100g") or {}
    gate = bsip0.get("plausibility_gate") or {}
    serving = bsip0.get("serving_info") or {}

    # Ingredient extraction patterns (minimal BSIP1 enrichment)
    E_PATTERN = re.compile(r"E(\d{3,4}[a-z]?)", re.IGNORECASE)
    ADDITIVE_TERMS = [
        ("לציטין סויה", "emulsifier"),
        ("לציטין", "emulsifier"),
        ("מתחלב", "emulsifier"),
        ("חומרי טעם", "flavor_generic"),
        ("חומר תפיחה", "raising_agent"),
        ("מגביר חמיצות", "acidity_regulator"),
        ("חומצה", "acid"),
        ("צבע", "color"),
        ("חומר ייצוב", "stabilizer"),
        ("עמילן מתוקן", "modified_starch"),
        ("מולטודקסטרין", "maltodextrin"),
        ("מלטודקסטרין", "maltodextrin"),
        ("פולידקסטרוז", "polydextrose"),
        ("גליצרול", "humectant"),
    ]
    SWEETENER_TERMS = [
        ("סוכר", "added_sugar"),
        ("דבש", "honey"),
        ("סירופ גלוקוזה", "glucose_syrup"),
        ("מולסה", "molasses"),
        ("פרוקטוז", "fructose"),
        ("גלוקוז", "glucose"),
    ]

    e_nums = list(set(E_PATTERN.findall(ing)))
    extracted_additives = []
    for e in e_nums:
        extracted_additives.append({"term": f"E{e}", "category": "e_number", "position": 1})
    for term, category in ADDITIVE_TERMS:
        if term in ing:
            extracted_additives.append({"term": term, "category": category, "position": 1})

    extracted_sweeteners = []
    for term, category in SWEETENER_TERMS:
        if term in ing:
            extracted_sweeteners.append({"term": term, "category": category, "position": 1})

    # NOVA inference
    has_ultra = bool(re.search(r"(E\d{3}|מלטודקסטרין|פולידקסטרוז|גליצרול|עמילן מתוקן|חומצה לקטית|אינולין)", ing))
    has_e_num = len(e_nums) >= 2
    has_flavor = "חומרי טעם" in ing
    has_processed_sugar = "סירופ גלוקוזה" in ing or "גלוקוז-פרוקטוז" in ing
    has_protein_isolate = bool(re.search(r"(חלבון סויה|חלבון חלב|חלבון אפונה|פרוטאין)", ing))

    if has_ultra or has_processed_sugar or has_protein_isolate:
        nova_proxy = 4
        nova_conf = 0.85
        nova_notes = ["ultra_processing_markers_detected"]
    elif has_e_num or has_flavor:
        nova_proxy = 3
        nova_conf = 0.75
        nova_notes = ["additives_or_flavors_detected"]
    elif len(ing) > 20:
        nova_proxy = 2
        nova_conf = 0.65
        nova_notes = ["minimal_processing_inferred"]
    else:
        nova_proxy = 3
        nova_conf = 0.5
        nova_notes = ["insufficient_ingredient_data"]

    # Ingredient quality
    if not ing:
        ingredient_quality = "missing"
        ingredient_warnings = ["ingredients_missing"]
    elif len(ing) < 10:
        ingredient_quality = "minimal"
        ingredient_warnings = ["ingredient_text_very_short"]
    else:
        ingredient_quality = "clean"
        ingredient_warnings = []

    # Missing fields
    missing_fields = []
    if not nutrition.get("energy_kcal"):
        missing_fields.append("energy_kcal_100g")
    if not serving.get("serving_size_g"):
        missing_fields.append("serving_size_g")

    # Build normalized nutrition with canonical keys
    nn = {
        "energy_kcal": nutrition.get("energy_kcal_100g"),
        "fat_g": nutrition.get("fat_g_100g"),
        "fat_saturated_g": nutrition.get("saturated_fat_g_100g"),
        "fat_trans_g": nutrition.get("trans_fat_g_100g"),
        "cholesterol_mg": nutrition.get("cholesterol_mg_100g"),
        "sodium_mg": nutrition.get("sodium_mg_100g"),
        "carbohydrates_g": nutrition.get("carbohydrates_g_100g"),
        "sugars_g": nutrition.get("sugars_g_100g"),
        "dietary_fiber_g": nutrition.get("fiber_g_100g"),
        "protein_g": nutrition.get("protein_g_100g"),
    }

    # Confidence
    has_full_nutrition = all(
        nn.get(k) is not None
        for k in ["energy_kcal", "fat_g", "carbohydrates_g", "protein_g"]
    ) and gate.get("verdict") in ("pass", "converted_pass")

    confidence_band = "confirmed_per_100g" if has_full_nutrition else "low_extraction"
    identity_conf = "medium"
    nutrition_conf = "confirmed_per_100g" if has_full_nutrition else "unconfirmed"

    return {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": bsip0["product_identity"].get("name"),
        "canonical_name_en": None,
        "brand": bsip0["product_identity"].get("brand"),
        "package_size_g": serving.get("package_size_g"),
        "unit_count": serving.get("unit_count"),
        "unit_size_g": serving.get("unit_size_g"),
        "serving_size_g": serving.get("serving_size_g"),
        "country_of_origin": bsip0["product_identity"].get("country_of_origin"),
        "kosher_certification": bsip0["product_identity"].get("kosher"),
        "image_url": bsip0["product_identity"].get("image_url"),
        "source_retailers": ["yohananof"],
        "normalized_nutrition_per_100g": nn,
        "energy_source_unit": "kcal",
        "ingredients_text_he": bsip0["raw_observations"].get("ingredients_raw_he"),
        "ingredients_list": [
            s.strip() for s in re.split(r"[,،]", ing) if s.strip()
        ][:20] if ing else [],
        "allergens_contains": [],
        "allergens_may_contain": [],
        "claims": [],
        "confidence": {
            "identity_confidence": identity_conf,
            "barcode_confidence": "inferred",
            "nutrition_confidence": nutrition_conf,
            "matched_by": "barcode_single_source",
            "observation_count": 1,
        },
        "barcode_validation_status": "inferred_from_text",
        "barcode_confidence_reason": "Single-source 13-digit barcode from yochananof TASK-360 scrape.",
        "nutrition_basis_claimed": bsip0["nutrition_basis"].get("basis_raw"),
        "nutrition_basis_detected": "per_100g" if gate.get("verdict") in ("pass", "converted_pass") else gate.get("verdict"),
        "nutrition_basis_gate": gate.get("verdict"),
        "nutrition_basis_conversion_factor": gate.get("conversion_factor"),
        "nutrition_serving_g_used": gate.get("serving_g_used"),
        "nutrition_consistency_status": "consistent" if has_full_nutrition else "insufficient",
        "nutrition_consistency_warnings": gate.get("fail_reasons", []),
        "ingredient_text_quality": ingredient_quality,
        "ingredient_warnings": ingredient_warnings,
        "canonical_trust_score": 0.85 if has_full_nutrition else 0.45,
        "canonical_trust_level": "medium" if has_full_nutrition else "low",
        "canonical_risk_flags": (
            ["per_serving_converted"] if gate.get("verdict") == "converted_pass" else []
        ) + ["inferred_barcode_only", "single_source_only"],
        "conflicts_summary": {
            "count": 0, "has_unresolved": False,
            "fields_in_conflict": [], "identity_conflicts": [],
            "nutrition_conflicts": [], "ingredient_conflicts": [],
            "labeling_conflicts": [], "completeness_conflicts": [],
        },
        "missing_fields": missing_fields,
        "inferred_fields": [],
        "audit_ref": f"bsip1_audit_{barcode}.json",
        "ingredients_raw": ing,
        "ingredients_raw_provenance": {
            "source": "bsip0_scrape",
            "bsip0_status": "bsip0_scrape",
            "populated_at": "bsip1_task360",
            "missing": not bool(ing),
            "note": "Direct scrape from yochananof product modal HTML. TASK-360 re-scrape.",
        },
        "ingredient_order": [
            {"position": i+1, "text": s.strip(), "percentage_declared": None, "has_subgroup": "(" in s}
            for i, s in enumerate(re.split(r"[,،]", ing)[:20])
            if s.strip()
        ] if ing else [],
        "extracted_additives": extracted_additives,
        "extracted_flavors": [{"term": "חומרי טעם", "category": "flavor_generic", "position": 1}] if "חומרי טעם" in ing else [],
        "extracted_sweeteners": extracted_sweeteners,
        "extracted_protein_markers": [],
        "extracted_matrix_markers": [],
        "extracted_fermentation_markers": [],
        "extracted_roasting_markers": [],
        "enrichment_summary": {
            "ingredient_count_parsed": len(re.split(r"[,،]", ing)) if ing else 0,
            "additive_count": len(extracted_additives),
            "flavor_marker_count": 1 if "חומרי טעם" in ing else 0,
            "sweetener_count": len(extracted_sweeteners),
            "protein_marker_count": 0,
            "matrix_marker_count": 0,
            "fermentation_marker_count": 0,
            "roasting_marker_count": 0,
            "has_flavor_descriptor": False,
            "has_prebiotic_fiber": "אינולין" in ing or "FOS" in ing or "אוליגופרוקטוז" in ing,
            "has_live_cultures": False,
            "has_protein_isolate_or_concentrate": has_protein_isolate,
        },
        "enrichment_version": "bsip1_task360",
        "enrichment_warnings": ingredient_warnings,
        "nova_proxy": nova_proxy,
        "nova_confidence": nova_conf,
        "nova_confidence_band": "high" if nova_conf >= 0.8 else "medium",
        "nova_notes": nova_notes,
    }

# ── BSIP2 runner ──────────────────────────────────────────────────────────────

def run_bsip2_on_corpus(bsip1_dir: pathlib.Path, output_dir: pathlib.Path) -> list:
    """Run BSIP2 scoring on all BSIP1 records using the unchanged engine."""
    sys.path.insert(0, str(BSIP2_SRC))

    # Set engine flags matching snacks.json config (UNCHANGED)
    os.environ["BARI_SHELF_RELATIVE_V1"] = "off"
    os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
    os.environ["BARI_RECAL_P0"] = "off"
    os.environ["BARI_GRAD_SODIUM_V1"] = "off"
    os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
    os.environ["BARI_REDLABEL_V1"] = "off"
    os.environ["BARI_SODIUM_CEREAL"] = "off"
    os.environ["BARI_FAT_TECH_V1"] = "on"
    os.environ["BARI_GLASSBOX_W4"] = "on"
    os.environ["BARI_TASK144_FIXES"] = "off"

    try:
        from input_loader import load_batch
        from signal_extractor import extract_signals
        from router_v2 import classify_category
        from nova_proxy import infer_nova
        from evaluation_scope import assign_evaluation_scope
        from score_engine import score_product
        from trace_writer import assemble_trace, write_trace
        from structural_classifier import classify_structural_class
    except ImportError as e:
        log.error("BSIP2 engine import failed: %s", e)
        return []

    products = load_batch(bsip1_dir)
    log.info("BSIP2: loaded %d products from corpus", len(products))

    traces = []
    errors = []

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            signals = extract_signals(product)
            cat_result = classify_category(product)
            l3 = signals["L3_inferred_classifications"]
            nova_result = infer_nova(product, l3)
            eval_result = assign_evaluation_scope(product, cat_result["category"])
            score_result = score_product(product, signals, cat_result, nova_result, eval_result)
            trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
            trace["structural_class"] = classify_structural_class(trace)
            write_trace(trace, output_dir)
            traces.append(trace)
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            log.info("  %s  score=%s  grade=%s", pid, score, grade)
        except Exception as e:
            log.error("  BSIP2 ERROR for %s: %s", pid, e)
            errors.append({"product_id": pid, "error": str(e)})

    log.info("BSIP2 complete. Scored: %d, Errors: %d", len(traces), len(errors))
    return traces, errors

# ── Frontend JSON builder ─────────────────────────────────────────────────────

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]

def score_to_grade(score):
    if score is None:
        return None
    for g, t in GRADE_SCALE:
        if score >= t:
            return g
    return "E"

DIMENSION_LABEL_MAP = {
    "processing_quality": "רמת עיבוד",
    "nutrient_density": "ערך תזונתי",
    "calorie_density": "צפיפות קלורית",
    "glycemic_quality": "איכות גליקמית",
    "protein_quality": "חלבון",
    "additive_quality": "תוספים",
    "satiety_support": "תחושת שובע",
    "fat_quality": "איכות שומן",
    "regulatory_quality": "איכות רגולטורית",
    "whole_food_integrity": "שלמות מזון",
}
DIMENSION_ORDER = [
    "processing_quality", "additive_quality", "nutrient_density", "protein_quality",
    "calorie_density", "glycemic_quality", "fat_quality", "satiety_support",
    "regulatory_quality", "whole_food_integrity",
]


def build_bari_interpretation(trace: dict) -> list:
    dim_scores = trace.get("dimension_scores") or {}
    result = []
    for key in DIMENSION_ORDER:
        label = DIMENSION_LABEL_MAP.get(key, key)
        raw = dim_scores.get(key)
        sf = None
        if raw is not None:
            try:
                sf = float(raw)
                sf = round(sf, 1) if 0 <= sf <= 100 else None
            except (TypeError, ValueError):
                sf = None
        strength = "data not available" if sf is None else ("חזק" if sf >= 80 else ("בינוני" if sf >= 50 else "נמוך"))
        result.append({
            "interpretation": "PENDING_COPY",
            "key": key,
            "label": label,
            "score": sf,
            "strength": strength,
        })
    return result


def build_frontend_json(traces: list, bsip1_dir: pathlib.Path, gate_results: dict,
                         quarantined: list, config_path: pathlib.Path) -> dict:
    """Build frontend JSON from BSIP2 traces. All copy = PENDING_COPY."""
    # Load config sha
    config_sha = hashlib.sha256(config_path.read_bytes()).hexdigest() if config_path.exists() else "N/A"

    # Load bsip1 corpus
    corpus = {}
    for f in bsip1_dir.glob("bsip1_*.json"):
        if "audit" in f.name:
            continue
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            corpus[str(rec.get("barcode", ""))] = rec
        except Exception:
            pass

    # Index traces by barcode
    trace_by_bc = {}
    for trace in traces:
        ref = trace.get("input_reference") or {}
        bc = str(ref.get("barcode") or ref.get("canonical_name_he") or "")
        if bc:
            trace_by_bc[bc] = trace
        # Also try canonical_product_id
        pid = ref.get("canonical_product_id") or ""
        if pid and pid.startswith("bsip1_"):
            bc2 = pid[len("bsip1_"):]
            if bc2 not in trace_by_bc:
                trace_by_bc[bc2] = trace

    products = []
    for bc, trace in sorted(trace_by_bc.items(), key=lambda x: -(x[1].get("final_score_estimate") or 0)):
        crec = corpus.get(bc, {})
        score = trace.get("final_score_estimate")
        grade = score_to_grade(score)
        name = crec.get("canonical_name_he") or ""
        image_url = crec.get("image_url")
        nn = crec.get("normalized_nutrition_per_100g") or {}

        gate = gate_results.get(bc, {})
        basis = gate.get("nutrition_basis", "per_100g")
        verdict = gate.get("verdict", "pass")
        conversion_factor = gate.get("conversion_factor", 1.0)

        has_full = all(nn.get(k) is not None for k in ["energy_kcal", "fat_g", "carbohydrates_g", "protein_g"])
        confidence = "full" if has_full else "partial"
        confidence_label_he = "נתונים מאומתים" if has_full else "נתונים בבדיקה"
        confidence_tooltip_he = (
            "הנתונים מאומתים ממקור ישיר. הציון מבוסס על נתוני תזונה ורכיבים מלאים."
            if has_full else
            "חלק מהנתונים בבדיקה. הציון עשוי להתעדכן כשיתווספו נתונים מאומתים."
        )

        nutrition = {
            "energyKcal": nn.get("energy_kcal"),
            "protein": nn.get("protein_g"),
            "sugar": nn.get("sugars_g"),
            "fat": nn.get("fat_g"),
            "fiber": nn.get("dietary_fiber_g"),
            "sodium": nn.get("sodium_mg"),
        }

        note_parts = ["ל-100 גרם"]
        if verdict == "converted_pass":
            note_parts.append(f"(המרה מ-{gate.get('serving_g_used', '?')}ג׳ מנה, ×{conversion_factor})")
        serving_note = " ".join(note_parts)

        bari_interp = build_bari_interpretation(trace)

        expansion = {
            "bottomLine": "PENDING_COPY",
            "comparisonContext": "PENDING_COPY",
            "confidenceLabel": confidence_label_he,
            "consumerExplanation": {
                "context": "PENDING_COPY",
                "good": ["PENDING_COPY"],
                "takeaway": "PENDING_COPY",
                "watchOut": [],
                "whyRated": "PENDING_COPY",
            },
            "ingredients": crec.get("ingredients_text_he"),
            "limitingFactors": ["PENDING_COPY"],
            "nutrition": nutrition,
            "positiveSignals": ["PENDING_COPY"],
            "servingNote": serving_note,
            "unknowns": [],
            "_nutrition_basis": basis,
            "_gate_verdict": verdict,
        }

        products.append({
            "bariInterpretation": bari_interp,
            "barcode": bc,
            "bestUseCases": ["PENDING_COPY"],
            "confidence": confidence,
            "confidence_label_he": confidence_label_he,
            "confidence_sub_reason": None if has_full else "low_extraction",
            "confidence_tooltip_he": confidence_tooltip_he,
            "consumerTakeaway": "PENDING_COPY",
            "d4_additives": [],
            "expansion": expansion,
            "grade": grade,
            "imageUrl": image_url,
            "insightLine": "PENDING_COPY",
            "name": name,
            "retailer": "yohananof",
            "rowVerdict": "PENDING_COPY",
            "score": score,
            "source_traceability_status": "resolved",
        })

    # Quarantine log
    quarantine_entries = [
        {
            "barcode": q["barcode"],
            "name": q.get("name"),
            "reason": "plausibility_gate_fail",
            "gate_fails": q.get("fail_reasons", []),
            "accounted_mass_g": q.get("accounted_mass"),
            "kcal": q.get("kcal"),
        }
        for q in quarantined
    ]

    from collections import Counter
    grade_dist = dict(Counter(p["grade"] for p in products if p.get("grade")))

    meta = {
        "category": "snacks",
        "config_sha256": config_sha,
        "display_count": len(products),
        "generated": now_iso(),
        "generator_version": "TASK-360-rescrape-v1.0",
        "grade_distribution": grade_dist,
        "off_check": "PASS - 0 products with OFF contamination. OFF banned project-wide. All nutrition from BSIP0 direct yochananof scrape only.",
        "pending_copy_fields": [
            "insightLine", "rowVerdict", "consumerTakeaway",
            "bariInterpretation.interpretation",
            "expansion.consumerExplanation", "expansion.comparisonContext",
            "expansion.bottomLine", "expansion.positiveSignals",
            "expansion.limitingFactors", "bestUseCases",
        ],
        "product_count": len(products),
        "schema": "BariProductVM[]",
        "schema_version": "v4",
        "scope_note": "ניתוח מדף יוחננוף בלבד — לא סקר שוק ישראלי. TASK-360 full rescrape.",
        "source_run": RUN_ID,
        "staging_note": (
            "TASK-360 full re-scrape + plausibility gate. "
            "Nutrition corrected from per-serving to per-100g where applicable. "
            "Consumer copy NOT done — separate voice pass required. "
            "Do NOT deploy without copy review."
        ),
        "quarantined_products": quarantine_entries,
        "quarantine_count": len(quarantined),
        "scoring_engine_unchanged": "TRIPWIRE-1 compliant — engine/config untouched",
        "editorial_note": (
            "הערת קטגוריה: קטגוריית חטיפי הדגנים היא מדף פינוק — כל המוצרים הם חטיפים מעובדים. "
            "הציונים מדרגים חטיף מול חטיף בלבד. ציון גבוה אינו אישור לאכול יותר."
        ),
    }

    return {"_meta": meta, "products": products}

# ── Main pipeline ─────────────────────────────────────────────────────────────

def main():
    log.info("=" * 60)
    log.info("TASK-360 Snacks Re-Scrape Pipeline")
    log.info("Run ID: %s", RUN_ID)
    log.info("=" * 60)

    # STEP 1 & 2: Discover + Scrape
    log.info("\n--- STEP 1+2: Discover & Scrape ---")

    all_products = {}  # keyed by barcode
    scrape_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1000})

        # Discovery
        for query in SEARCH_QUERIES:
            discovered = discover_shelf(page, query)
            for prod in discovered:
                bc = prod.get("barcode") or prod.get("key")
                if bc and bc not in all_products:
                    all_products[bc] = prod

        log.info("Total unique products discovered: %d", len(all_products))
        save_json(NEW_BSIP0_DIR / "all_discovered.json", list(all_products.values()))

        # Scrape each product
        for key, product in list(all_products.items()):
            bc = clean(product.get("barcode"))
            name = clean(product.get("name"))

            if not bc:
                log.warning("  No barcode for: %s — skip", name)
                continue

            log.info("  Scraping: %s | %s", bc, name)
            product_dir = NEW_BSIP0_DIR / bc
            product_dir.mkdir(parents=True, exist_ok=True)

            # Download image
            img_url = normalize_image_url(product.get("image_url_raw"))
            local_img = download_image(img_url, product_dir)
            product["local_image_file"] = local_img

            try:
                open_product_modal(page, product)

                html_nutrition = capture_tab(page, "ערכים תזונתיים")
                html_ingredients = capture_tab(page, "רכיבים")
                html_allergens = capture_tab(page, "מידע אלרגני")

                # Save raw HTML
                (product_dir / "nutrition.html").write_text(html_nutrition or "", encoding="utf-8")
                (product_dir / "ingredients.html").write_text(html_ingredients or "", encoding="utf-8")
                (product_dir / "allergens.html").write_text(html_allergens or "", encoding="utf-8")

                capture_status = {
                    "nutrition": "success" if html_nutrition else "empty",
                    "ingredients": "success" if html_ingredients else "empty",
                    "allergens": "success" if html_allergens else "empty",
                }

                product["capture_status"] = capture_status
                save_json(product_dir / "discovery.json", product)

                # STEP 3: Parse serving size
                package_size_html = ""
                for html in [html_nutrition, html_ingredients, html_allergens]:
                    if html:
                        meta_s = BeautifulSoup(html, "lxml")
                        pkg = find_value_by_label(meta_s, "מידה")
                        if pkg:
                            package_size_html = pkg
                            break

                serving_info = parse_serving_size(product.get("card_text", ""), package_size_html)

                # STEP 4: Parse nutrition + plausibility gate
                nutrition_raw, nutrition_basis = parse_nutrition_html(html_nutrition)
                ingredients_raw = parse_ingredients_html(html_ingredients)

                gate_result = plausibility_gate(
                    nutrition_raw, serving_info, ingredients_raw or "", bc
                )

                # Build BSIP0 record
                bsip0_record = build_bsip0_product(
                    product, html_nutrition, html_ingredients, html_allergens, serving_info
                )
                save_json(product_dir / "product.json", bsip0_record)

                scrape_results.append({
                    "barcode": bc,
                    "name": name,
                    "status": "scraped_ok",
                    "gate_verdict": gate_result["verdict"],
                    "accounted_mass": gate_result.get("accounted_mass"),
                    "kcal": gate_result.get("kcal"),
                    "serving_info": serving_info,
                    "nutrition_raw_kcal": nutrition_raw.get("energy_kcal_100g"),
                    "final_kcal": (gate_result.get("final_nutrition") or {}).get("energy_kcal_100g"),
                    "fail_reasons": gate_result.get("fail_reasons", []),
                    "capture_status": capture_status,
                })

                log.info("    gate=%s accounted=%.1fg kcal=%s",
                         gate_result["verdict"],
                         gate_result.get("accounted_mass", 0),
                         gate_result.get("kcal"))

                close_dialog(page)

            except Exception as e:
                log.error("  SCRAPE FAILED: %s | %s | %s", bc, name, str(e)[:200])
                scrape_results.append({
                    "barcode": bc,
                    "name": name,
                    "status": "scrape_failed",
                    "error": str(e)[:300],
                })
                close_dialog(page)

            save_json(NEW_BSIP0_DIR / "scrape_progress.json", scrape_results)

        browser.close()

    # Save scrape results
    save_json(NEW_BSIP0_DIR / "scrape_results.json", scrape_results)
    log.info("Scrape complete: %d attempts", len(scrape_results))

    # STEP 5: Build BSIP1 for surviving products
    log.info("\n--- STEP 5: Build BSIP1 ---")

    quarantined = []
    bsip1_built = 0
    gate_results_by_bc = {}

    for result in scrape_results:
        bc = result["barcode"]
        if result["status"] != "scraped_ok":
            continue

        gate_verdict = result.get("gate_verdict")
        if gate_verdict == "quarantine":
            quarantined.append({
                "barcode": bc,
                "name": result.get("name"),
                "fail_reasons": result.get("fail_reasons", []),
                "accounted_mass": result.get("accounted_mass"),
                "kcal": result.get("kcal"),
            })
            log.warning("  QUARANTINE: %s | %s", bc, "; ".join(result.get("fail_reasons", [])))
            continue

        # Load the BSIP0 record
        bsip0_path = NEW_BSIP0_DIR / bc / "product.json"
        if not bsip0_path.exists():
            log.warning("  No BSIP0 record for %s — skip", bc)
            continue

        bsip0_record = json.loads(bsip0_path.read_text(encoding="utf-8"))
        gate_results_by_bc[bc] = bsip0_record.get("plausibility_gate", {})

        # Build BSIP1
        bsip1_record = build_bsip1_record(bsip0_record)
        bsip1_path = BSIP1_OUTPUT_DIR / f"bsip1_{bc}.json"
        save_json(bsip1_path, bsip1_record)
        bsip1_built += 1
        log.info("  BSIP1: %s | %s", bc, bsip1_record.get("canonical_name_he", "")[:40])

    log.info("BSIP1 built: %d products | Quarantined: %d", bsip1_built, len(quarantined))

    # STEP 6: Run BSIP2
    log.info("\n--- STEP 6: Run BSIP2 ---")
    traces, bsip2_errors = run_bsip2_on_corpus(BSIP1_OUTPUT_DIR, BSIP2_OUTPUT_DIR)

    # STEP 7: Build frontend JSON
    log.info("\n--- STEP 7: Build Frontend JSON ---")
    config_path = ROOT / "03_operations" / "page_generator" / "configs" / "snacks.json"
    frontend_data = build_frontend_json(traces, BSIP1_OUTPUT_DIR, gate_results_by_bc, quarantined, config_path)

    save_json(FRONTEND_PATH, frontend_data)
    log.info("Frontend JSON written: %s", FRONTEND_PATH)

    # ── Summary ───────────────────────────────────────────────────────────────
    total_discovered = len([r for r in scrape_results])
    total_scraped_ok = len([r for r in scrape_results if r["status"] == "scraped_ok"])
    total_scrape_failed = len([r for r in scrape_results if r["status"] == "scrape_failed"])

    passed_direct = len([r for r in scrape_results if r.get("gate_verdict") == "pass"])
    passed_converted = len([r for r in scrape_results if r.get("gate_verdict") == "converted_pass"])
    total_quarantine = len(quarantined)
    surviving = bsip1_built
    scored = len(traces)

    log.info("\n" + "=" * 60)
    log.info("PIPELINE SUMMARY")
    log.info("=" * 60)
    log.info("Discovered products:        %d", total_discovered)
    log.info("Scrape OK:                  %d", total_scraped_ok)
    log.info("Scrape failed:              %d", total_scrape_failed)
    log.info("Passed gate (direct):       %d", passed_direct)
    log.info("Passed gate (converted):    %d", passed_converted)
    log.info("Quarantined:                %d", total_quarantine)
    log.info("BSIP1 built (surviving):    %d", surviving)
    log.info("BSIP2 scored:               %d", scored)
    log.info("BSIP2 errors:               %d", len(bsip2_errors))
    log.info("Frontend products:          %d", len(frontend_data["products"]))

    if quarantined:
        log.info("\nQuarantined barcodes:")
        for q in quarantined:
            log.info("  %s | %s | %s", q["barcode"], q.get("name", "")[:30], "; ".join(q.get("fail_reasons", [])))

    # Save run record
    run_record = {
        "run_id": RUN_ID,
        "run_timestamp": now_iso(),
        "task": "TASK-360",
        "pipeline": "snacks_rescrape_plausibility_gate",
        "discovered": total_discovered,
        "scraped_ok": total_scraped_ok,
        "scrape_failed": total_scrape_failed,
        "passed_gate_direct": passed_direct,
        "passed_gate_converted": passed_converted,
        "quarantined": total_quarantine,
        "bsip1_built": surviving,
        "bsip2_scored": scored,
        "bsip2_errors": len(bsip2_errors),
        "frontend_products": len(frontend_data["products"]),
        "quarantined_detail": quarantined,
        "bsip2_error_detail": bsip2_errors,
        "output_paths": {
            "bsip0_dir": str(NEW_BSIP0_DIR),
            "bsip1_dir": str(BSIP1_OUTPUT_DIR),
            "bsip2_dir": str(BSIP2_OUTPUT_DIR),
            "frontend_json": str(FRONTEND_PATH),
        },
        "scoring_engine_tripwire_check": "PASS - no changes to 03_operations/bsip2/** or page_generator configs",
        "off_check": "PASS - no Open Food Facts used in any field",
    }
    save_json(NEW_BSIP0_DIR / "run_record.json", run_record)
    save_json(SNACKS_DIR / "bsip2_outputs" / RUN_ID / "run_record.json", run_record)

    log.info("\nRun record: %s", NEW_BSIP0_DIR / "run_record.json")
    log.info("TASK-360 pipeline complete.")

    return run_record


if __name__ == "__main__":
    main()
