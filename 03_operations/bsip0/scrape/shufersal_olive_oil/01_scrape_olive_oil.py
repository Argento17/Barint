"""
BSIP0 Shufersal — Olive Oil scraper (TASK-197 Phase 2).

Purpose: acquire the Shufersal Israeli olive oil corpus with Hebrew product names,
  ingredient panels, nutrition panels, and olive-oil-specific label signals
  (origin country, harvest date, PDO/PGI claims, processing grade).

Category scope:
  - Extra virgin olive oil (שמן זית כתית מעולה)
  - Virgin olive oil (שמן זית כתית)
  - Olive oil blends (שמן זית / תערובת)
  - PDO/PGI-labelled olive oils (ares/kalamata/cretan etc.)
  - Imported + Israeli-produced

Excluded at scrape time:
  - Pomace oil (שמן פסולת זיתים) — processed byproduct, not olive oil
  - Canola / sunflower / mixed vegetable oils without olive content
  - Truffle/flavoured oils that are NOT olive-oil base
  - Olive-based cosmetics / soap / non-food

Architecture mirrors shufersal_cereals/01_scrape_cereals.py (proven Shufersal path).

OLIVE OIL-SPECIFIC label signals captured:
  - origin_country_raw   — named country of harvest (e.g. "יוון", "ספרד", "ישראל")
  - origin_multi_country — True if "מיזוג" / multiple countries mentioned
  - harvest_date_raw     — any harvest year or model year on the label
  - grade_claim_raw      — "כתית מעולה" / "extra virgin" / "כתית" / "virgin" etc.
  - pdo_pgi_claim_raw    — any PDO/PGI/DOP/IGP/ΠΟΠ/ΠΓΕ designation text
  - certification_raw    — other certifications (כשר / אורגני / organic etc.)
  - acidity_claim_raw    — declared acidity % if stated ("חומציות עד 0.8%")
  - dilution_flags       — non-olive oil ingredients found in the ingredient panel
                           (seed oils, palm oil, sunflower, canola, soya, rapeseed)

FRAUD ANNOTATION PREP (label-detectable signals per TASK-197):
  These fields are CAPTURED here, NOT annotated or scored. Annotation layer =
  Phase 3 (Nutrition Agent D5/D6 fence design). No scoring here.

Output: C:\\Bari\\02_products\\olive_oil\\bsip0_raw\\olive_oil_bsip0_raw_{ts}.json + log
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = "https://www.shufersal.co.il"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

PAGE_SIZE = 48
MAX_PRODUCTS = 150
MAX_PAGES_MAINSTREAM = 5
MAX_PAGES_SPECIALTY = 3
PRODUCT_PAGE_DELAY = 0.7

# Shared BSIP0 nutrition parser — mandatory, COV-007 enforced.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw, nutrition_implausible  # noqa: E402

# ── Query plan — olive-oil-targeted ─────────────────────────────────────────────
QUERY_PLAN: list[tuple[str, str]] = [
    ("שמן זית",               "mainstream"),
    ("שמן זית כתית מעולה",   "mainstream"),
    ("extra virgin olive oil", "mainstream"),
    ("שמן זית כתית",          "mainstream"),
    ("שמן זית אורגני",        "specialty"),
    ("שמן זית ישראלי",        "specialty"),
    ("שמן זית יווני",         "specialty"),
    ("שמן זית ספרדי",         "specialty"),
    ("שמן זית איטלקי",        "specialty"),
    ("שמן זית קלמטה",         "specialty"),
    ("שמן זית PDO",            "specialty"),
    ("שמן זית DOP",            "specialty"),
    ("שמן זית כתית מובחר",    "specialty"),
    ("olive oil",              "specialty"),
]

# Shufersal category code for oils / condiments (best-effort; graceful 404)
# A13 = "שמנים, חומץ ותבלינים" (oils, vinegar, spices) — checked from shelf mapping
CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A1301?pageSize={PAGE_SIZE}", "A1301_oils"),
    (f"{BASE}/online/he/c/A13?pageSize={PAGE_SIZE}",   "A13_condiments"),
]

# EXCLUDE: clearly not olive oil
EXCLUDE_SIGNALS = [
    # pomace / industrial
    "פסולת זיתים", "pomace", "עכורים",
    # other pure oils (when NOT combined with olive)
    "שמן קנולה", "שמן חמניות", "שמן סויה", "שמן דקלים", "שמן תירס",
    "שמן שומשום", "שמן בוטנים", "שמן אגוזים", "שמן אבוקדו",
    "canola oil", "sunflower oil", "palm oil", "soybean oil", "rapeseed oil",
    # non-food / cosmetic
    "קרם", "סבון", "לוסיון", "שמן גוף", "cream", "soap",
    # other food categories
    "חומץ", "חרדל", "רוטב", "מיונז", "חמוצים", "כבוש", "pickles",
    # baby food
    "תינוק", "מטרנה", "סימילק",
    # truffle/flavoured that are NOT olive-based
    "שמן טרופל בסיס חמניות", "שמן ארומטי",
]

# INCLUDE: must look like an olive oil product
INCLUDE_SIGNALS = [
    "שמן זית", "olive oil", "extra virgin", "כתית מעולה", "כתית",
    "PDO", "DOP", "IGP", "ΠΟΠ", "ΠΓΕ", "קלמטה", "kalamata",
    "זיתים כבושים",  # sometimes appears in olive category browse but should be excluded below
]

MAINTENANCE_SIGNALS = ["maintenance", "אתר בתחזוקה", "בתחזוקה"]

# ── Olive oil fraud-signal patterns ──────────────────────────────────────────────

# Seed/non-olive oils that should NOT appear in a pure olive oil ingredient panel.
# Finding any of these = dilution contamination flag.
DILUTION_OIL_SIGNALS = [
    "שמן חמניות", "sunflower oil", "שמן קנולה", "canola", "rapeseed",
    "שמן סויה", "soybean", "שמן תירס", "corn oil",
    "שמן דקלים", "palm oil", "שמן דקל", "palm kernel",
    "שמן כותנה", "cottonseed", "שמן בוטנים", "groundnut", "peanut oil",
    "שמן שומשום", "sesame oil",  # permitted in blends but flags origin question
]

# Origin countries (Hebrew and transliteration variants)
ORIGIN_COUNTRY_TOKENS = {
    "ישראל": "Israel", "israel": "Israel",
    "יוון": "Greece", "greece": "Greece", "greek": "Greece",
    "ספרד": "Spain", "spain": "Spain", "spanish": "Spain",
    "איטליה": "Italy", "italy": "Italy", "italian": "Italy",
    "תוניסיה": "Tunisia", "tunisia": "Tunisia",
    "מרוקו": "Morocco", "morocco": "Morocco",
    "טורקיה": "Turkey", "turkey": "Turkey",
    "פורטוגל": "Portugal", "portugal": "Portugal",
    "ירדן": "Jordan", "jordan": "Jordan",
    "קרואטיה": "Croatia", "croatia": "Croatia",
    "אלג'יריה": "Algeria", "algeria": "Algeria",
    "סוריה": "Syria", "syria": "Syria",
    "לבנון": "Lebanon", "lebanon": "Lebanon",
    "ארה\"ב": "USA", "usa": "USA", "california": "USA",
    "אוסטרליה": "Australia", "australia": "Australia",
    "ארגנטינה": "Argentina", "argentina": "Argentina",
    "צ'ילה": "Chile", "chile": "Chile",
}

# Multi-country blending markers
MULTI_COUNTRY_MARKERS = [
    "מיזוג", "מיובא מ", "ממדינות", "ממקורות מרובים", "ממספר ארצות",
    "blend of", "mixture of", "origin: eu", "אירופה", "אחת ממדינות",
    "ממדינות האיחוד", "ממדינות הים התיכון",
]

# Grade/quality claim patterns
# IMPORTANT: more-specific tokens must be checked BEFORE shorter substrings.
# "כתית מעולה" (extra virgin) must appear before bare "כתית" (virgin) — "כתית" is
# a substring of "כתית מעולה", so matching shorter first causes a false-positive:
# "כתית מעולה" products would be misclassified as "כתית" (Signal 6 false positive).
# "כתית פרימיום" ("premium" = marketing synonym for "מעולה") is also extra_virgin —
# its back-label ingredient text declares "שמן זית כתית מעולה", confirming EVOO identity.
# Bug fixed 2026-06-06 per TASK-197 Phase 4 Return Block (B5 extractor bug).
GRADE_TOKENS = [
    ("extra_virgin", ["כתית מעולה", "כתית פרימיום", "extra virgin",
                      "ekstra negdje", "ekstra sjeverni"]),
    ("virgin",       ["כתית",       " virgin ",     "virgen"]),
    ("refined",      ["מזוקק",      "refined",       "מעורב", "blend", "light"]),
    ("lampante",     ["lampante"]),
    ("pomace",       ["פסולת",      "pomace",        "orujo"]),
]

# PDO/PGI/DOP/IGP markers
PDO_PGI_MARKERS = [
    "PDO", "DOP", "AOP", "ΠΟΠ", "IGP", "PGI", "ΠΓΕ", "IGT",
    "מוצר מוגן", "הגנת מקור", "מוגן גיאוגרפי",
    "kalamata", "קלמטה",   # Kalamata is a registered PDO
    "priego de córdoba", "sierra de cazorla", "les baux de provence",
    "terra di bari", "toscano", "tuscan", "ligurian", "sicilian",
    "cretan", "crete", "kreta",
]

# Harvest date patterns (year-based)
HARVEST_YEAR_PATTERNS = [
    re.compile(r"עונ[ה]?\s*(\d{4})[/\-](\d{2,4})", re.IGNORECASE),  # עונה 2023/24
    re.compile(r"קציר\s*(\d{4})", re.IGNORECASE),                    # קציר 2024
    re.compile(r"harvest\s+(\d{4})", re.IGNORECASE),                  # harvest 2024
    re.compile(r"(?:campaign|crop)\s+(\d{4})[/\-](\d{2,4})", re.IGNORECASE),
    re.compile(r"(\d{4})[/\-](\d{4})\s*(?:olive|זית|שמן)", re.IGNORECASE),
    re.compile(r"best before.*?(\d{4})", re.IGNORECASE),              # fallback: best-before year
]

# Acidity claim
ACIDITY_PATTERN = re.compile(
    r"(?:חומציות|acidity|acid(?:ity)?)[:\s]*(?:עד|max\.?|<|פחות מ)?\s*([\d.,]+)\s*%",
    re.IGNORECASE
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    return len(text) < 5000 and any(s in text.lower() for s in MAINTENANCE_SIGNALS)


def _get(url: str, timeout: int = 25) -> requests.Response | None:
    try:
        return requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


def _extract_volume_ml(name: str) -> float | None:
    """Extract container size from product name (ml / L / litre)."""
    patterns = [
        re.compile(r"(\d[\d,.]*)\s*ל(?:יטר|\'|\")?(?:\b|$)", re.IGNORECASE),  # 1 ליטר / 1 ל'
        re.compile(r"(\d[\d,.]*)\s*(?:ml|מ\"ל|מל)\b", re.IGNORECASE),
        re.compile(r"(\d[\d,.]*)\s*(?:liter|litre|l)\b", re.IGNORECASE),
    ]
    for pat in patterns:
        m = pat.search(name)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ל" in m.group(0) and val <= 5:  # litres
                    val *= 1000
                if 50 < val <= 5000:
                    return val
            except ValueError:
                pass
    return None


def _price_per_100ml(price_str: str, volume_ml: float | None) -> float | None:
    if not price_str or not volume_ml:
        return None
    try:
        price = float(price_str.replace(",", "."))
        return round(price * 100 / volume_ml, 2)
    except (ValueError, ZeroDivisionError):
        return None


def _price_per_liter(price_str: str, volume_ml: float | None) -> float | None:
    """Compute price per liter (ILS/L) for Signal 4 internal price-anomaly gate.

    Internal use only — NOT consumer-facing. Gate for triggering Signal 5 checks.
    """
    if not price_str or not volume_ml:
        return None
    try:
        price = float(price_str.replace(",", "."))
        return round(price * 1000 / volume_ml, 2)
    except (ValueError, ZeroDivisionError):
        return None


def _is_excluded(name: str) -> bool:
    nl = " " + name.lower() + " "
    return any(sig.lower() in nl for sig in EXCLUDE_SIGNALS)


def _looks_like_olive_oil(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in INCLUDE_SIGNALS)


# ── Olive-oil-specific signal extractors ──────────────────────────────────────

def _extract_origin_country(text: str) -> tuple[str, list[str]]:
    """Return (primary_country_or_empty, [all_countries_found])."""
    tl = text.lower()
    found = []
    for token, country in ORIGIN_COUNTRY_TOKENS.items():
        if token.lower() in tl and country not in found:
            found.append(country)
    return (found[0] if len(found) == 1 else ""), found


def _extract_origin_text(text: str) -> str:
    """Extract the raw origin/country-of-origin text as printed on the label.

    Looks for common Hebrew / English origin disclosure patterns and returns
    a snippet of up to 120 chars around the first match (Signal 1 — origin opacity).
    """
    patterns = [
        re.compile(
            r"(?:ארץ מוצא|מקום מוצא|country of origin|origin)[:\s]*([\s\S]{0,120}?)(?:\.|,|;|\n|$)",
            re.IGNORECASE
        ),
        re.compile(
            r"(?:מיובא מ|מיוצר ב|יוצא מ|imported from|produced in|מקור)[:\s]*([\s\S]{0,120}?)(?:\.|,|;|\n|$)",
            re.IGNORECASE
        ),
    ]
    for pat in patterns:
        m = pat.search(text)
        if m:
            return m.group(0).strip()[:150]
    return ""


def _is_multi_country(text: str) -> bool:
    tl = text.lower()
    if any(m.lower() in tl for m in MULTI_COUNTRY_MARKERS):
        return True
    # Multiple origin countries in text also signals blending
    _, countries = _extract_origin_country(text)
    return len(countries) >= 2


def _extract_blend_text(text: str) -> str:
    """Return the actual blending-language snippet found, or empty string.

    Signal 3 — multi-country blending language (e.g. 'מיזוג שמנים ממדינות האיחוד').
    """
    tl = text.lower()
    for marker in MULTI_COUNTRY_MARKERS:
        idx = tl.find(marker.lower())
        if idx >= 0:
            snippet = text[max(0, idx - 10):idx + 100].strip()
            return snippet[:150]
    # Also flag if two or more countries found side-by-side
    _, countries = _extract_origin_country(text)
    if len(countries) >= 2:
        return f"multiple origins detected: {', '.join(countries)}"
    return ""


def _extract_grade_claim(text: str) -> str:
    """Return the highest/first matched olive oil grade claim."""
    tl = text.lower()
    for grade, tokens in GRADE_TOKENS:
        if any(tok.lower() in tl for tok in tokens):
            return grade
    return ""


def _extract_grade_front(name: str) -> str:
    """Extract grade claim from the product name / front-label text.

    The product name on Shufersal is derived from the front-label designation
    (e.g. "שמן זית כתית מעולה 750 מל"). This is `olive_grade_front`.
    """
    return _extract_grade_claim(name)


def _extract_grade_back(ingredients_or_back: str) -> str:
    """Extract grade claim from the back-label / ingredient section text.

    This is `olive_grade_back`. A mismatch between front and back grades is
    Signal 6 (processing-state inconsistency).
    """
    return _extract_grade_claim(ingredients_or_back)


def _extract_pdo_pgi(text: str) -> tuple[bool, str]:
    """Return (has_pdo_pgi_claim, claim_text_snippet).

    Signal 5 — PDO/PGI logo or claim presence. `has_pdo_pgi_claim` is True
    when any recognised PDO/PGI/DOP/IGP marker is found. `claim_text` is the
    raw snippet (up to 3 matches joined), or "" if absent.
    """
    tl = text.lower()
    hits = []
    for marker in PDO_PGI_MARKERS:
        if marker.lower() in tl:
            # Grab a 60-char window around the match
            idx = tl.find(marker.lower())
            snippet = text[max(0, idx - 10):idx + 50].strip()
            hits.append(snippet)
    claim_text = "; ".join(hits[:3]) if hits else ""
    return bool(hits), claim_text


def _extract_harvest_date(text: str) -> tuple[bool, str]:
    """Return (has_harvest_date, harvest_date_text) from label text.

    `has_harvest_date` = True when a harvest year/season is found.
    `harvest_date_text` = the raw matched text, or "" if absent.
    Also checks for Hebrew patterns: שנת קציר, בציר.
    """
    # Additional Hebrew harvest-year patterns not in HARVEST_YEAR_PATTERNS
    extra_patterns = [
        re.compile(r"שנת\s*קציר\s*(\d{4})", re.IGNORECASE),
        re.compile(r"בציר\s*(\d{4})", re.IGNORECASE),
    ]
    all_patterns = extra_patterns + HARVEST_YEAR_PATTERNS
    for pat in all_patterns:
        m = pat.search(text)
        if m:
            return True, m.group(0).strip()
    return False, ""


def _extract_acidity(text: str) -> str:
    """Return acidity claim string (e.g. '0.8%') or empty."""
    m = ACIDITY_PATTERN.search(text)
    return m.group(0).strip()[:50] if m else ""


def _detect_dilution_flags(ingredients: str) -> list[str]:
    """Return list of non-olive oils found in the ingredient panel."""
    if not ingredients:
        return []
    il = ingredients.lower()
    flags = []
    for sig in DILUTION_OIL_SIGNALS:
        if sig.lower() in il:
            flags.append(sig)
    return flags


# ── Page parsing ──────────────────────────────────────────────────────────────

def _parse_product_list_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", attrs={"data-product-name": True})
    results = []
    for li in items:
        d = li.attrs
        name = d.get("data-product-name", "").strip()
        code = d.get("data-product-code", "").strip()
        if not name or not code:
            continue
        if d.get("data-food", "false").lower() != "true":
            continue
        if _is_excluded(name):
            continue
        if not _looks_like_olive_oil(name):
            continue
        price = d.get("data-product-price", "")
        volume_ml = _extract_volume_ml(name)
        results.append({
            "name": name,
            "code": code,
            "categories": d.get("data-all-categories", ""),
            "price": price,
            "volume_ml": volume_ml,
            "price_per_100ml": _price_per_100ml(price, volume_ml),
        })
    return results


def _search_query(query: str, page: int = 0) -> list[dict]:
    url = (
        f"{BASE}/online/he/search?q={requests.utils.quote(query)}"
        f"&pageSize={PAGE_SIZE}&currentPage={page}"
    )
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)


def _category_page(base_url: str, page: int = 0) -> list[dict]:
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}currentPage={page}" if page > 0 else base_url
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)


# ── Product page ──────────────────────────────────────────────────────────────

def _parse_product_page(code: str, meta: dict) -> dict | None:
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=25)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    product_url = r.url

    ld_name, ld_sku, ld_gtin, ld_images, ld_brand = "", "", "", [], ""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_sku = ld.get("sku", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                brand = ld.get("brand", "")
                ld_brand = brand.get("name", "") if isinstance(brand, dict) else (brand or "")
                ld_images = ld.get("image", [])
                if isinstance(ld_images, str):
                    ld_images = [ld_images]
                break
        except Exception:
            pass

    # Nutrition — shared parser (COV-007 mandate)
    nutr_raw = parse_nutrition_list(soup)
    nutr_src = extract_nutrition_raw(soup)

    # Full page text for label-signal extraction
    page_text = soup.get_text(separator=" ", strip=True)

    # Ingredients
    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:2000]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{30,})", text)
            if m:
                ingredients_raw = m.group(1)[:2000]
                break

    # ── Olive-oil-specific label signals ────────────────────────────────────────
    # Search in both the full page text and ingredients (ingredients are most reliable)
    combined_text = ingredients_raw + " " + page_text[:3000]

    origin_primary, origin_all = _extract_origin_country(combined_text)
    origin_text = _extract_origin_text(combined_text)
    is_multi = _is_multi_country(combined_text)
    blend_text = _extract_blend_text(combined_text)

    # Grade split: front = product name (front-label designation), back = ingredients/back text
    name_for_grade = ld_name or meta.get("name", "")
    olive_grade_front = _extract_grade_front(name_for_grade)
    olive_grade_back  = _extract_grade_back(ingredients_raw + " " + page_text[2000:4000])

    has_pdo_pgi, pdo_pgi_text = _extract_pdo_pgi(combined_text)
    has_harvest_date, harvest_date_text = _extract_harvest_date(combined_text)
    acidity_claim = _extract_acidity(combined_text)
    dilution_flags = _detect_dilution_flags(ingredients_raw)

    # Certifications (kosher, organic, etc.)
    cert_tokens = []
    if any(kw in combined_text for kw in ["כשר", "kosher", "כשרות"]):
        cert_tokens.append("kosher")
    if any(kw in combined_text for kw in ["אורגני", "organic", "bio"]):
        cert_tokens.append("organic")
    if any(kw in combined_text.lower() for kw in ["vegan", "טבעוני"]):
        cert_tokens.append("vegan")
    if any(kw in combined_text.lower() for kw in ["gluten free", "ללא גלוטן"]):
        cert_tokens.append("gluten_free")

    # Net weight / volume (label-declared, separate from URL extraction)
    net_weight_raw = ""
    nw_m = re.search(
        r"(?:נטו|משקל נטו|נפח נטו|net weight|content)[:\s]*([\d.,]+\s*(?:ל\'|ליטר|מ\"ל|מל|ml|g|גרם|kg))",
        combined_text, re.IGNORECASE
    )
    if nw_m:
        net_weight_raw = nw_m.group(1).strip()

    # Country of manufacture / bottling (may differ from country of harvest)
    country_manufacture_raw = ""
    cm_m = re.search(
        r"(?:יוצר|מיוצר ב|מוצר בארץ|bottled in|packaged in|filled in)[:\s]*([^\n,;.]{5,40})",
        combined_text, re.IGNORECASE
    )
    if cm_m:
        country_manufacture_raw = cm_m.group(1).strip()[:80]

    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "")
    volume_ml = meta.get("volume_ml") or _extract_volume_ml(name)

    return {
        "retailer_id": "shufersal",
        "retailer_name": "שופרסל",
        "source_url": product_url,
        "scraped_at": datetime.utcnow().isoformat(),
        "name_he": name,
        "name_en": "",
        "brand": ld_brand,
        "barcode": barcode,
        "category_raw": meta.get("categories", ""),
        "subcategory_raw": "olive_oil",

        # ── Nutrition panel (per 100g/100ml) ────────────────────────────────
        "nutrition": {
            "energy_kcal_raw": nutr_raw.get("energy", ""),
            "protein_raw":     nutr_raw.get("protein", ""),
            "carbs_raw":       nutr_raw.get("carbs", ""),
            "fat_raw":         nutr_raw.get("fat", ""),
            "fiber_raw":       nutr_raw.get("fiber", ""),
            "sodium_raw":      nutr_raw.get("sodium", ""),
            "sugar_raw":       nutr_raw.get("sugar", ""),
            "saturated_fat_raw": nutr_raw.get("saturated_fat", ""),
        },
        "nutrition_raw_source": nutr_src,
        "ingredients_raw": ingredients_raw,
        "ingredients_language": (
            "he" if ingredients_raw and any("א" <= c <= "ת" for c in ingredients_raw) else ""
        ),

        # ── Olive-oil fraud-signal fields (label-detectable) ─────────────────
        # These are captured here. Annotation layer = Phase 3 (Nutrition Agent D5/D6).
        # NEVER used for scoring at this stage.
        "olive_signals": {
            # Signal: grade front/back split (Signal 6 — processing-state inconsistency)
            "olive_grade_front":       olive_grade_front,   # from product name / front label
            "olive_grade_back":        olive_grade_back,    # from ingredient section / back label

            # Signal 1 — origin opacity
            "origin_text":             origin_text,         # full raw origin text as printed
            "origin_country_primary":  origin_primary,      # parsed primary country (single-origin)
            "origin_countries_all":    origin_all,          # all parsed countries

            # Signal 3 — multi-country blending
            "origin_multi_country":    is_multi,            # boolean
            "blend_text":              blend_text,          # actual blending language found

            # Harvest date (internal freshness signal)
            "has_harvest_date":        has_harvest_date,    # boolean
            "harvest_date_text":       harvest_date_text,   # raw text (שנת קציר / season string)

            # Signal 5 — PDO/PGI claim (manual check gate)
            "has_pdo_pgi_claim":       has_pdo_pgi,         # boolean
            "pdo_pgi_claim_text":      pdo_pgi_text,        # raw claim snippet

            "acidity_claim_raw":       acidity_claim,
            "certification_raw":       cert_tokens,
            "dilution_flags":          dilution_flags,
            "net_weight_raw":          net_weight_raw,
            "country_manufacture_raw": country_manufacture_raw,
        },

        # ── Pricing ──────────────────────────────────────────────────────────
        # price_per_liter = Signal 4 internal gate (NOT consumer-facing).
        # Triggers Signal 5 check when price anomaly detected.
        "price": meta.get("price", ""),
        "volume_ml": volume_ml,
        "price_per_100ml":  _price_per_100ml(meta.get("price", ""), volume_ml),
        "price_per_liter":  _price_per_liter(meta.get("price", ""), volume_ml),

        # ── Acquisition metadata ──────────────────────────────────────────────
        "image_urls": [u for u in ld_images[:3] if u],
        "extraction_method": "html_parse",
        "extraction_confidence": (
            "high"   if (nutr_raw and ingredients_raw) else
            "medium" if nutr_raw else
            "low"
        ),
        "acquisition_query": meta.get("query", ""),
        "acquisition_tier": meta.get("tier", ""),
    }


# ── Main acquisition ──────────────────────────────────────────────────────────

def run_acquisition(verbose: bool = True) -> tuple[list[dict], list[str]]:
    notes: list[str] = []
    seen_codes: set[str] = set()
    code_meta: dict[str, dict] = {}

    def log(msg: str) -> None:
        if verbose:
            print(msg, flush=True)
        notes.append(msg)

    log("=== Phase 1: Search queries ===")
    for query, tier in QUERY_PLAN:
        if len(seen_codes) >= MAX_PRODUCTS:
            log(f"  Cap {MAX_PRODUCTS} reached — skipping remaining queries")
            break
        max_pages = MAX_PAGES_MAINSTREAM if tier == "mainstream" else MAX_PAGES_SPECIALTY
        new_total = 0
        for page in range(max_pages):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _search_query(query, page)
            if not items:
                log(f"  '{query}' page {page}: no results — stopping")
                break
            new_page = 0
            for item in items:
                c = item["code"]
                if c and c not in seen_codes:
                    seen_codes.add(c)
                    code_meta[c] = {**item, "query": query, "tier": tier}
                    new_page += 1
            new_total += new_page
            log(f"  '{query}' page {page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            sleep(0.3)
        log(f"  '{query}' total new: {new_total}")

    log(f"\n=== Phase 2: Category browsing ({len(seen_codes)} so far) ===")
    for base_url, cat_id in CATEGORY_URLS:
        if len(seen_codes) >= MAX_PRODUCTS:
            break
        cat_new = 0
        for page in range(MAX_PAGES_MAINSTREAM):
            if len(seen_codes) >= MAX_PRODUCTS:
                break
            items = _category_page(base_url, page)
            if not items:
                log(f"  {cat_id} page {page}: no results — stopping")
                break
            new_page = 0
            for item in items:
                c = item["code"]
                if c and c not in seen_codes:
                    seen_codes.add(c)
                    code_meta[c] = {**item, "query": f"category:{cat_id}", "tier": "category"}
                    new_page += 1
            cat_new += new_page
            log(f"  {cat_id} page {page}: {len(items)} items, {new_page} new (total {len(seen_codes)})")
            if new_page == 0:
                break
            sleep(0.3)
        log(f"  {cat_id} total new: {cat_new}")

    log(f"\nTotal unique product codes: {len(seen_codes)}")

    log("\n=== Phase 3: Product page fetching ===")
    products: list[dict] = []
    failed = 0
    codes_to_fetch = list(seen_codes)[:MAX_PRODUCTS]
    for i, code in enumerate(codes_to_fetch):
        p = _parse_product_page(code, code_meta.get(code, {}))
        if p:
            products.append(p)
            if verbose and i % 10 == 0 and i > 0:
                print(f"  [{i}/{len(codes_to_fetch)}] fetched {len(products)} OK", flush=True)
        else:
            failed += 1
        sleep(PRODUCT_PAGE_DELAY)

    log(f"\nProduct pages: {len(products)} OK, {failed} failed")

    # Coverage stats
    n_nutr        = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["fat_raw"])
    n_ingr        = sum(1 for p in products if p["ingredients_raw"])
    n_img         = sum(1 for p in products if p["image_urls"])
    n_high        = sum(1 for p in products if p["extraction_confidence"] == "high")
    n_grade_front = sum(1 for p in products if p["olive_signals"]["olive_grade_front"])
    n_grade_back  = sum(1 for p in products if p["olive_signals"]["olive_grade_back"])
    n_grade_mismatch = sum(
        1 for p in products
        if p["olive_signals"]["olive_grade_front"]
        and p["olive_signals"]["olive_grade_back"]
        and p["olive_signals"]["olive_grade_front"] != p["olive_signals"]["olive_grade_back"]
    )
    n_orig        = sum(1 for p in products if p["olive_signals"]["origin_country_primary"])
    n_origin_text = sum(1 for p in products if p["olive_signals"]["origin_text"])
    n_harv        = sum(1 for p in products if p["olive_signals"]["has_harvest_date"])
    n_pdo         = sum(1 for p in products if p["olive_signals"]["has_pdo_pgi_claim"])
    n_blend       = sum(1 for p in products if p["olive_signals"]["blend_text"])
    n_dil         = sum(1 for p in products if p["olive_signals"]["dilution_flags"])
    n_ppl         = sum(1 for p in products if p.get("price_per_liter"))

    log(f"Coverage: {n_nutr}/{len(products)} nutrition, {n_ingr}/{len(products)} ingredients, "
        f"{n_img}/{len(products)} images, {n_high}/{len(products)} high-confidence")
    log(f"Olive signals: grade_front={n_grade_front}, grade_back={n_grade_back}, "
        f"grade_mismatch(Sig6)={n_grade_mismatch}")
    log(f"  origin_text={n_origin_text}(Sig1), blend_text={n_blend}(Sig3), "
        f"price_per_liter={n_ppl}(Sig4-gate), PDO/PGI={n_pdo}(Sig5), "
        f"harvest_date={n_harv}, dilution_flags={n_dil}")

    return products, notes


def main():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_dir = Path(r"C:\Bari\02_products\olive_oil\bsip0_raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"olive_oil_bsip0_raw_{ts}.json"
    log_path = out_dir / f"olive_oil_bsip0_log_{ts}.txt"

    products, notes = run_acquisition(verbose=True)
    raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path.write_text("\n".join(notes), encoding="utf-8")

    print("\n=== DONE ===")
    print(f"Products scraped: {len(products)}")
    print(f"Raw JSON: {raw_path}")
    print(f"Log:      {log_path}")

    n_nutr     = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["fat_raw"])
    n_ingr     = sum(1 for p in products if p["ingredients_raw"])
    n_dil      = sum(1 for p in products if p["olive_signals"]["dilution_flags"])
    n_orig     = sum(1 for p in products if p["olive_signals"]["origin_country_primary"])
    n_harv     = sum(1 for p in products if p["olive_signals"]["has_harvest_date"])
    n_pdo      = sum(1 for p in products if p["olive_signals"]["has_pdo_pgi_claim"])
    n_blend    = sum(1 for p in products if p["olive_signals"]["blend_text"])
    n_ppl      = sum(1 for p in products if p.get("price_per_liter"))
    n_mismatch = sum(
        1 for p in products
        if p["olive_signals"]["olive_grade_front"]
        and p["olive_signals"]["olive_grade_back"]
        and p["olive_signals"]["olive_grade_front"] != p["olive_signals"]["olive_grade_back"]
    )

    print("\n--- BSIP0 Composition Gate ---")
    print(f"Products:         {len(products)} [need >=30 before scoring]")
    print(f"Nutrition panels: {n_nutr}/{len(products)} ({100*n_nutr//max(len(products),1)}%) [target >=80%]")
    print(f"Ingredient lists: {n_ingr}/{len(products)} ({100*n_ingr//max(len(products),1)}%) [target >=80%]")
    print(f"Origin named:     {n_orig}/{len(products)}")
    print(f"Dilution flags:   {n_dil}/{len(products)}")
    print("\n--- Fraud-Signal Field Coverage ---")
    print(f"Signal 1 (origin opacity):        origin_text present = {n_orig}/{len(products)}")
    print(f"Signal 3 (multi-country blending): blend_text present = {n_blend}/{len(products)}")
    print(f"Signal 4 (price gate, internal):  price_per_liter    = {n_ppl}/{len(products)}")
    print(f"Signal 5 (PDO/PGI, manual gate):  has_pdo_pgi_claim  = {n_pdo}/{len(products)}")
    print(f"Signal 6 (grade inconsistency):   grade mismatch F/B = {n_mismatch}/{len(products)}")
    print(f"Harvest date:                     has_harvest_date   = {n_harv}/{len(products)}")
    print("\nNOTE: BSIP2 scoring HALTED. First-batch owner consult required before any scoring.")
    return products


if __name__ == "__main__":
    main()
