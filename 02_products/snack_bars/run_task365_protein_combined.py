"""
TASK-365 — Protein Combined Corpus: Bars + Cookies + Bites (Expanded Re-Scrape)
=================================================================================
Owner-approved 2026-06-21.

Scope: ONE combined protein shelf = protein BARS + protein COOKIES + protein BITES.
       Protein cookies are IN scope (previously excluded by HARD_EXCLUDE "עוגיה").
       Protein bites/cases (פניניה, ביס חלבון) are IN scope.

Stage: RAW CORPUS ONLY — no scoring, no BSIP2, no frontend JSON.
       Outputs: protein_combined_corpus_task365_<timestamp>.json + manifest.

Changes vs TASK-360:
  1. Brand-led + format-led queries added (WIN, All In, PRO20, Max Protein, etc.)
  2. Page cap raised to 6 for all queries (was 3 for specialty)
  3. עוגיה / עוגיות LIFTED from HARD_EXCLUDE — but requires protein signal
  4. Protein signal gate: name contains חלבון/protein OR ingredients contain protein isolate/concentrate
  5. Output is RAW corpus JSON (no BSIP1/BSIP2/frontend packaging)
  6. Full ingredient text captured (required by new scoring lens)

Hard rules enforced:
  - OFF BAN: no Open Food Facts, ever
  - No fabrication: if Shufersal unreachable, script stops and reports
  - Missing data discard: fields that cannot be parsed are NULL (not invented)
  - Per-100g plausibility gate: discards implausible panels
"""
from __future__ import annotations

import datetime
import json
import logging
import pathlib
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Shared BSIP0 nutrition parser ─────────────────────────────────────────────
_SHARED = pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\_shared")
sys.path.insert(0, str(_SHARED))
from bsip0_nutrition import (  # noqa: E402
    parse_nutrition_list,
    extract_nutrition_raw,
    parse_nutrition_numeric,
)

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = pathlib.Path(r"C:\Bari")
SNACKS_DIR = ROOT / "02_products" / "snack_bars"
RUN_TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
RUN_ID = f"run_protein_combined_task365_{RUN_TS}"

CORPUS_PATH = SNACKS_DIR / f"protein_combined_corpus_task365_{RUN_TS}.json"
MANIFEST_PATH = SNACKS_DIR / f"protein_combined_manifest_task365_{RUN_TS}.json"

# Existing live barcodes (TASK-362 frontend) — used for new-vs-existing diff
EXISTING_BARCODES = {
    "7290017516295", "7290121166850", "7290117384589", "7290121161886",
    "7290117384596", "7290119383153", "7290121161916", "7290121160582",
    "7290121161930", "7290119371112", "7290119383160", "8410076610386",
    "8410076610379", "7290112913487", "7290112915351", "7290112915382",
}

# ── Shufersal HTTP config ─────────────────────────────────────────────────────
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
MAX_PAGES = 6          # raised from 3 for specialty queries
PRODUCT_DELAY = 0.8

# ── TASK-365: Protein-focused search queries ──────────────────────────────────
# Generic protein-bar queries (original + extended).
# Query strings were tested against the live Shufersal search endpoint before
# inclusion — only queries that return food items are listed.
PROTEIN_QUERIES: list[str] = [
    # Generic protein-bar searches
    "חטיף חלבון",
    "חטיפי חלבון",
    "פרוטאין בר",
    # Brand-led: אול אין (All In)
    "אול אין חלבון",
    # Brand-led: WIN bars
    "win חטיף",           # returns WIN protein bars
    "חלבון WIN",
    # Brand-led: TODAY (טודיי)
    "טודיי",               # returns 12 food items including TODAY protein bars
    # Brand-led: Nature Valley Protein (נייטשר ואלי פרוטאין)
    "נייטשר ואלי פרוטאין",
    # Brand-led: Max Protein / מאקס פרוטאין
    "מאקס פרוטאין",
    # Brand-led: Pangaea / פנגיאה
    "פנגיאה חטיף",
    # Protein cookies
    "עוגיות חלבון",
    "עוגיית חלבון",
    # Protein bites / cases
    "ביס חלבון",
    "protein bites",
    # Additional coverage
    "חלבון בר",
]

# Category URLs for Shufersal protein/fitness shelf
CATEGORY_URLS: list[tuple[str, str]] = [
    (f"{BASE}/online/he/c/A13413?pageSize={PAGE_SIZE}", "A13413_snack_bars"),
    (f"{BASE}/online/he/c/A13414?pageSize={PAGE_SIZE}", "A13414_granola_bars"),
]

# ── Inclusion/exclusion logic ──────────────────────────────────────────────────
#
# TASK-365 CHANGE vs TASK-360:
#   עוגיה / עוגיות are LIFTED from HARD_EXCLUDE.
#   Instead we require a PROTEIN SIGNAL before accepting any cookie.
#
# Protein signal: name contains חלבון/protein, OR ingredients contain isolate/concentrate.
# We check the name signal at discovery time; ingredient check happens after scrape.

# Hard-exclude: clearly non-protein / non-bar categories (NOT cookies any more)
#
# CRITICAL: these are checked as exact-word or multi-word matches — NOT bare substrings.
# "חלב" must NOT match inside "חלבון" (protein).  We use a dedicated word-boundary
# check (_hard_exclude below) that wraps single short tokens in space/start/end anchors.
HARD_EXCLUDE_TASK365 = [
    # Wafers, crackers — not protein format
    "ביסקוויט", "וופל",
    "קרקר", "פריכית", "פריכיות",
    # Chocolate tablets (not bars) — use multi-word to avoid false positives
    "שוקולד טבלה", "שוקולד מריר", "שוקולד חלב",
    # Ice cream
    "גלידה", "ארטיק",
    # Drinks and spreads — "חלב" is a standalone word not a substring of "חלבון"
    "משקה", "מיץ", "יוגורט",
    "ממרח", "ריבה", "נוטלה",
    # Supplements (capsules, pills)
    "קפסול", "כמוסה", "תרופה",
    # Cereal box
    "דגני בוקר קופסה", "קורנפלקס", "מוזלי",
    # Pasta / noodles — protein noodles (נודלס) are out of scope
    "פתיתים", "פסטה", "אטריות", "נודלס",
    # Salty snacks
    "ביסלי", "אסנס", "פרינגלס", "צ'יפס",
    "בייגלה", "קרוטונים",
    # Bread, buns
    "לחם", "לחמנייה", "פיתה",
    # Dairy (bare "חלב" excluded only as standalone word below)
    "גבינה", "קוטג",
    # Protein powder (אבקת חלבון) — out of scope; bars only
    "אבקת חלבון",
    # Dried ingredient (חלבון סויה מיובש) — out of scope
    "מיובש",
    # Protein-enriched dairy drink (מעדן, דנונה פרו) — dairy drinks not bars
    # NOTE: "מעדן" alone would be too broad; use more specific patterns handled below
]

# Additional post-discovery format exclusions — checked AFTER the name passes HARD_EXCLUDE.
# These match partial names that indicate an out-of-scope product format.
FORMAT_EXCLUDE_PATTERNS = [
    "אבקת חלבון",          # protein powder
    "חלבון מיובש",          # dried protein ingredient
    "נודלס חלבון",          # protein noodles
    "דנונה פרו",            # Danone PRO dairy drink
    "מעדן חלבון",           # protein pudding/dairy product
    "מולר פרוטאין יוגור",   # Müller protein yogurt
    "שייקר",                # protein shaker drink/tool
    "חלב מועשר",            # protein-enriched milk
]

# Tokens that need word-boundary checking (to avoid false substring matches like
# "חלב" inside "חלבון").  Each item is (token, must_be_standalone).
_WORD_BOUNDARY_EXCLUDES = [
    "חלב",   # "milk" — standalone only; NOT "חלבון" (protein)
]

# Protein signal tokens — a product must contain at least one of these in its name
# to be accepted as a protein product at discovery time.
PROTEIN_NAME_SIGNALS = [
    "חלבון", "protein", "פרוטאין", "pro20", "pro ", " pro",
    "win ", " win", "all in", "אול אין",
]

# Protein signal in ingredients (checked post-scrape for cookies/bites)
PROTEIN_INGREDIENT_SIGNALS = [
    "חלבון מי גבינה", "חלבון חלב", "חלבון סויה", "חלבון אפונה",
    "חלבון ביצה", "מי גבינה", "whey", "isolate", "concentrate",
    "פרוטאין", "חלבון מרוכז", "חלבון מבודד",
    "casein", "קזאין",
]

# Plausibility gate thresholds
GATE_MIN_ACCOUNTED_G = 70.0
GATE_MIN_KCAL_DRY = 150.0

SUGAR_BEARING_TOKENS = [
    "סוכר", "שוקולד", "דבש", "סירופ", "תמרים", "גלוקוז", "פרוקטוז",
    "מולסה", "מחית תמרים", "ממתיק", "גלוקוז-פרוקטוז",
]


# ──────────────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def save_json(path: pathlib.Path | str, data) -> None:
    pathlib.Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _get(url: str, timeout: int = 30) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return r
    except Exception as exc:
        log.warning("GET error %s: %s", url, exc)
        return None


_WEIGHT_PATTERNS = [
    re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*g\b", re.IGNORECASE),
]

def _extract_weight_g(name: str) -> float | None:
    for pat in _WEIGHT_PATTERNS:
        m = pat.search(name)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    val *= 1000
                if 5 < val < 2000:
                    return val
            except ValueError:
                pass
    return None


def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    return len(text) < 5000 and ("maintenance" in text.lower() or "בתחזוקה" in text)


def _hard_exclude(name: str) -> tuple[bool, str]:
    nl = name.lower()

    # If the name contains a strong protein signal (חלבון / פרוטאין / protein),
    # the standalone-milk ("חלב") boundary check is suppressed — "קרם חלב" is a
    # flavor descriptor, not a dairy product.  Multi-word hard-excludes like
    # "שוקולד חלב" still apply because they are unambiguous category signals.
    has_protein_in_name = any(
        sig in nl for sig in ("חלבון", "פרוטאין", "protein")
    )

    # Standard substring check for multi-word / unambiguous tokens
    for term in HARD_EXCLUDE_TASK365:
        if term.lower() in nl:
            return True, f"hard_exclude:{term}"

    # Format-level exclusions (protein powder, dairy drinks, noodles, etc.)
    for pattern in FORMAT_EXCLUDE_PATTERNS:
        if pattern.lower() in nl:
            return True, f"format_exclude:{pattern}"

    # Word-boundary check for short tokens that are substrings of valid protein terms.
    # Skipped when the name already has a protein signal (avoids "קרם חלב" exclusion
    # on WIN protein bars).
    if not has_protein_in_name:
        import re as _re
        for token in _WORD_BOUNDARY_EXCLUDES:
            pattern = r"(?<![א-ת])" + _re.escape(token.lower()) + r"(?![א-ת])"
            if _re.search(pattern, nl):
                return True, f"hard_exclude_wordbound:{token}"

    return False, ""


def _has_protein_name_signal(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in PROTEIN_NAME_SIGNALS)


def _has_protein_ingredient_signal(ingredients: str) -> bool:
    il = ingredients.lower()
    return any(sig.lower() in il for sig in PROTEIN_INGREDIENT_SIGNALS)


def _infer_format(name: str) -> str:
    """Classify product as bar / cookie / bite based on name."""
    nl = name.lower()
    if any(t in nl for t in ["עוגי", "cookie", "cookies"]):
        return "cookie"
    if any(t in nl for t in ["ביס ", "bites", "bite", "פניני"]):
        return "bite"
    return "bar"


# Brand prefix mapping (ordered — first match wins)
_BRAND_PREFIXES: list[tuple[str, str]] = [
    ("WIN ",        "WIN"),
    ("win ",        "WIN"),
    ("אול אין",     "אול אין"),
    ("אול איןחלבון", "אול אין"),
    ("נייטשר פרוטאין", "Nature Valley"),
    ("נייטשר ואלי",  "Nature Valley"),
    ("גרנולה פרוטאין", "פנגיאה"),
    ("חטיפי חלבון",  "פנגיאה"),   # multipack Pangaea
    ("חט.חלבון",    "WIN"),       # WIN abbreviated
    ("חטיף פרוטאין", "Max Protein"),
    ("עוגיית חלבון", "אול אין"),   # אול אין cookie line
]

# Barcode-to-brand overrides derived from known SKU prefixes
_BARCODE_BRAND: dict[str, str] = {
    "7290017516": "פנגיאה",       # Pangaea single bars (barcode prefix)
    "7290112913": "פנגיאה",
    "7290112915": "פנגיאה",
    "7290112497": "פנגיאה",
    "7290121": "TODAY",           # TODAY bars
    "7290117384": "TODAY",        # TODAY bars
    "7290119371": "TODAY",
    "7290119383": "TODAY",
    "7290118": "TODAY",
    "8410076": "Nature Valley",
    "7290015130": "WIN",
    "7290018703": "אול אין",
    "7290018043": "אול אין",
    "7290019766": "אול אין",
    "7290019310": "Max Protein",
    "7290019401": "Max Protein",
}


def _infer_brand(name: str, barcode: str) -> str:
    """Infer brand from product name and barcode prefix."""
    nl = name.lower()
    # Name prefix
    for prefix, brand in _BRAND_PREFIXES:
        if nl.startswith(prefix.lower()) or prefix.lower() in nl[:20]:
            return brand
    # Barcode prefix (longest match wins)
    best_brand = ""
    best_len = 0
    for bc_prefix, brand in _BARCODE_BRAND.items():
        if barcode.startswith(bc_prefix) and len(bc_prefix) > best_len:
            best_brand = brand
            best_len = len(bc_prefix)
    return best_brand


# ──────────────────────────────────────────────────────────────────────────────
# Discovery
# ──────────────────────────────────────────────────────────────────────────────

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
        is_food = d.get("data-food", "false").lower() == "true"
        if not is_food:
            continue
        results.append({
            "name": name,
            "code": code,
            "categories": d.get("data-all-categories", ""),
            "price": d.get("data-product-price", ""),
            "weight_g": _extract_weight_g(name),
            "brand": d.get("data-product-brand", ""),
        })
    return results


def _search_shufersal(query: str, page: int = 0) -> list[dict]:
    url = (
        f"{BASE}/online/he/search"
        f"?q={requests.utils.quote(query)}"
        f"&pageSize={PAGE_SIZE}"
        f"&currentPage={page}"
    )
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)


def _category_shufersal(base_url: str, page: int = 0) -> list[dict]:
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}currentPage={page}" if page > 0 else base_url
    r = _get(url)
    if not r or r.status_code != 200 or _is_maintenance(r.content):
        return []
    return _parse_product_list_page(r.text)


def discover_protein_products() -> dict[str, dict]:
    """
    Run category + protein-query discovery.
    Returns {code: product_meta} deduped.

    Acceptance criteria at discovery time:
      - NOT in HARD_EXCLUDE_TASK365
      - Has a protein name signal (חלבון/protein/brand tokens)
      Note: cookies without a protein name signal are held as 'cookie_candidate'
            and get a second chance if their scraped ingredients show a protein isolate.
    """
    seen: dict[str, dict] = {}
    cookie_candidates: dict[str, dict] = {}  # cookies without protein name signal

    log.info("=== Phase 1: Shufersal category traversal ===")
    for base_url, cat_id in CATEGORY_URLS:
        for page in range(MAX_PAGES):
            items = _category_shufersal(base_url, page)
            if not items:
                break
            new_this_page = 0
            for item in items:
                code = item["code"]
                if not code or code in seen:
                    continue
                excl, reason = _hard_exclude(item["name"])
                if excl:
                    continue
                if _has_protein_name_signal(item["name"]):
                    seen[code] = {**item, "source": cat_id, "source_type": "category",
                                  "name_protein_signal": True}
                    new_this_page += 1
                elif any(t in item["name"].lower() for t in ["עוגי", "cookie"]):
                    cookie_candidates[code] = {**item, "source": cat_id, "source_type": "category",
                                               "name_protein_signal": False,
                                               "cookie_candidate": True}
            log.info("  [%s] page %d: %d new protein items (total %d)", cat_id, page, new_this_page, len(seen))
            if new_this_page == 0 and page > 0:
                break
            time.sleep(0.3)

    log.info("=== Phase 2: Protein search queries ===")
    for query in PROTEIN_QUERIES:
        for page in range(MAX_PAGES):
            items = _search_shufersal(query, page)
            if not items:
                break
            new_this_page = 0
            for item in items:
                code = item["code"]
                if not code or code in seen:
                    continue
                excl, _ = _hard_exclude(item["name"])
                if excl:
                    continue
                if _has_protein_name_signal(item["name"]):
                    seen[code] = {**item, "source": f"search:{query}", "source_type": "search",
                                  "name_protein_signal": True}
                    new_this_page += 1
                elif any(t in item["name"].lower() for t in ["עוגי", "cookie"]):
                    # cookie without protein name — keep as candidate for ingredient check
                    if code not in cookie_candidates:
                        cookie_candidates[code] = {
                            **item, "source": f"search:{query}", "source_type": "search",
                            "name_protein_signal": False, "cookie_candidate": True
                        }
            log.info("  [%s] p%d: %d new (total %d)", query[:30], page, new_this_page, len(seen))
            if new_this_page == 0 and page > 1:
                break
            time.sleep(0.3)

    log.info("Discovery phase 1+2 complete: %d protein candidates, %d cookie candidates",
             len(seen), len(cookie_candidates))

    # Merge cookie candidates into seen for scraping (we'll filter post-scrape on ingredients)
    for code, meta in cookie_candidates.items():
        if code not in seen:
            seen[code] = meta

    log.info("Total discovery pool (protein + cookie candidates): %d", len(seen))
    return seen


# ──────────────────────────────────────────────────────────────────────────────
# Product page scraping
# ──────────────────────────────────────────────────────────────────────────────

_INGR_PATTERNS = [
    re.compile(r"רכיב[ים:]*\s*:?\s*(.*)", re.DOTALL),
    re.compile(r"מרכיב[ים:]*\s*:?\s*(.*)", re.DOTALL),
]


def _extract_ingredients(soup: BeautifulSoup) -> str:
    """
    Extract ingredient list from Shufersal product page.

    Shufersal structure (observed 2026-06-21):
      <div class="title"><div class="mainInfo">רכיבים</div></div>
      <div class="info"><div class="componentsText">רכיבים: ...</div></div>

    The label ("רכיבים") and content are SIBLINGS, not parent-child.
    So we look for the componentsText div directly first, then fall back to
    the old parent-search approach.
    """
    # Strategy 1: Shufersal componentsText div (most reliable for this category)
    for div in soup.find_all("div", class_="componentsText"):
        text = div.get_text(separator=" ", strip=True)
        if "רכיב" in text and len(text) > 30:
            for pat in _INGR_PATTERNS:
                m = pat.search(text)
                if m and len(m.group(1).strip()) > 10:
                    return m.group(1).strip()[:3000]
            # If no pattern matched, return full text (may start with "רכיבים:")
            return text[:3000]

    # Strategy 2: div class="info" containing ingredient label
    for div in soup.find_all("div", class_="info"):
        text = div.get_text(separator=" ", strip=True)
        if "רכיב" in text and len(text) > 30:
            for pat in _INGR_PATTERNS:
                m = pat.search(text)
                if m and len(m.group(1).strip()) > 10:
                    return m.group(1).strip()[:3000]

    # Strategy 3: Label-then-parent search (original approach, kept as fallback)
    for label_text in ("רכיבים", "מרכיבים", "רכיב"):
        node = soup.find(string=re.compile(label_text))
        if node:
            parent = node.find_parent()
            container = parent.find_parent() if parent else None
            if container:
                full = container.get_text(separator=" ", strip=True)
                for pat in _INGR_PATTERNS:
                    m = pat.search(full)
                    if m and len(m.group(1).strip()) > 10:
                        return m.group(1).strip()[:3000]

    # Strategy 4: Scan all li elements
    for li in soup.find_all("li"):
        text = li.get_text(separator=" ", strip=True)
        for pat in _INGR_PATTERNS:
            m = pat.search(text)
            if m and len(m.group(1).strip()) > 20:
                return m.group(1).strip()[:3000]

    return ""


def _parse_serving_size_g(name: str, weight_g: float | None) -> dict:
    result: dict = {
        "package_size_g": weight_g,
        "unit_size_g": None,
        "unit_count": None,
        "serving_size_g": None,
        "parse_source": None,
    }
    if not weight_g:
        return result

    m = re.search(r"(\d+)\s*[x\*x]\s*(\d+(?:\.\d+)?)\s*(?:g|גר)", name or "", re.IGNORECASE)
    if m:
        unit_count = int(m.group(1))
        unit_g = float(m.group(2))
        result["unit_count"] = unit_count
        result["unit_size_g"] = unit_g
        result["serving_size_g"] = unit_g
        result["parse_source"] = "name_multipack_pattern"
        return result

    m2 = re.search(r"(\d+)\s*יח", name or "")
    if m2:
        unit_count = int(m2.group(1))
        result["unit_count"] = unit_count
        result["unit_size_g"] = round(weight_g / unit_count, 1)
        result["serving_size_g"] = round(weight_g / unit_count, 1)
        result["parse_source"] = "name_unit_count"
        return result

    result["parse_source"] = "package_only"
    return result


def scrape_shufersal_product(code: str, meta: dict) -> dict | None:
    """Scrape a single Shufersal product page. Returns raw record or None on failure."""
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=30)
    if not r or r.status_code != 200:
        log.warning("  HTTP %s for %s", r.status_code if r else "ERR", code)
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    source_url = r.url

    # LD+JSON for identity
    ld_name = ld_sku = ld_gtin = ""
    ld_images: list[str] = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string or "{}")
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_sku = ld.get("sku", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                imgs = ld.get("image", [])
                ld_images = [imgs] if isinstance(imgs, str) else imgs[:3]
                break
        except Exception:
            pass

    brand = ""
    # Primary: itemprop brand (present on some pages)
    brand_span = soup.find("span", itemprop="brand")
    if brand_span:
        brand = brand_span.get_text(strip=True)
    # Fallback: LD+JSON brand field
    if not brand:
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                ld = json.loads(script.string or "{}")
                if ld.get("@type") == "Product":
                    b = ld.get("brand", {})
                    if isinstance(b, dict):
                        brand = b.get("name", "")
                    elif isinstance(b, str):
                        brand = b
                    if brand:
                        break
            except Exception:
                pass
    # Fallback: use discovery metadata brand (from data-product-brand attribute)
    if not brand:
        brand = meta.get("brand", "")

    # Nutrition via shared parser
    nutr_parsed = parse_nutrition_list(soup)
    nutr_raw_src = extract_nutrition_raw(soup)

    nutr_numeric_dict = {
        "energy_kcal_raw":    nutr_parsed.get("energy", ""),
        "fat_raw":            nutr_parsed.get("fat", ""),
        "saturated_fat_raw":  nutr_parsed.get("saturated_fat", ""),
        "carbs_raw":          nutr_parsed.get("carbs", ""),
        "sugar_raw":          nutr_parsed.get("sugar", ""),
        "fiber_raw":          nutr_parsed.get("fiber", ""),
        "protein_raw":        nutr_parsed.get("protein", ""),
        "sodium_raw":         nutr_parsed.get("sodium", ""),
    }
    nutr_numeric = parse_nutrition_numeric(nutr_numeric_dict)

    ingredients_raw = _extract_ingredients(soup)

    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "").replace("p_", "")
    weight_g = meta.get("weight_g") or _extract_weight_g(name)
    serving_info = _parse_serving_size_g(name, weight_g)

    return {
        "schema_version": "task365_raw_corpus_v1",
        "source": {
            "retailer": "Shufersal",
            "retailer_id": "shufersal",
            "source_url": source_url,
            "scrape_run": RUN_ID,
            "scraped_at": now_iso(),
        },
        "product_identity": {
            "name": name,
            "brand": brand or meta.get("brand", ""),
            "barcode": barcode,
            "shufersal_code": code,
            "image_url": (ld_images or [None])[0],
            "image_urls": [u for u in ld_images if u],
        },
        "serving_info": serving_info,
        "nutrition_raw": {
            "parsed_strings": nutr_parsed,
            "raw_source": nutr_raw_src,
            "basis": nutr_raw_src.get("selection", {}).get("selected_basis", "unknown"),
            "basis_header": nutr_raw_src.get("selection", {}).get("selected_table_header", ""),
        },
        "nutrition_numeric_per_100g": nutr_numeric,
        "ingredients_raw": ingredients_raw,
        "price": meta.get("price", ""),
        "weight_g": weight_g,
        "discovery_meta": {
            "name_protein_signal": meta.get("name_protein_signal", False),
            "cookie_candidate": meta.get("cookie_candidate", False),
            "discovery_source": meta.get("source", ""),
        },
        "provenance": {
            "source": "shufersal_direct_scrape",
            "source_url": source_url,
            "fetched_at": now_iso(),
            "client_version": "task365_v1",
            "verification_status": "candidate",
            "off_check": "PASS - no Open Food Facts",
        },
    }


# ──────────────────────────────────────────────────────────────────────────────
# Plausibility gate
# ──────────────────────────────────────────────────────────────────────────────

def plausibility_gate(nutr_numeric: dict, serving_info: dict, ingredients: str) -> dict:
    """
    Per-100g plausibility gate (same logic as TASK-360).
    Returns verdict: pass | converted_pass | quarantine
    """
    kcal = nutr_numeric.get("energy_kcal") or 0.0
    carbs = nutr_numeric.get("carbohydrates_g") or 0.0
    fat = nutr_numeric.get("fat_g") or 0.0
    protein = nutr_numeric.get("protein_g") or 0.0
    fiber = nutr_numeric.get("dietary_fiber_g") or 0.0
    sugars = nutr_numeric.get("sugars_g")

    accounted = carbs + fat + protein + fiber

    def _check(n100_kcal, n100_acc, n100_sugars) -> list[str]:
        fails = []
        if n100_acc < GATE_MIN_ACCOUNTED_G:
            fails.append(f"accounted_mass={n100_acc:.1f}g < {GATE_MIN_ACCOUNTED_G}g per 100g")
        if n100_sugars is not None and n100_sugars == 0:
            if any(tok in (ingredients or "") for tok in SUGAR_BEARING_TOKENS):
                fails.append("sugars=0 but ingredients contain sugar-bearing tokens")
        if n100_kcal is not None and n100_kcal < GATE_MIN_KCAL_DRY:
            fails.append(f"kcal={n100_kcal:.0f} < {GATE_MIN_KCAL_DRY} for dry snack")
        return fails

    fails = _check(kcal, accounted, sugars)

    if not fails:
        return {
            "verdict": "pass",
            "final_nutrition": {k: v for k, v in nutr_numeric.items() if not k.startswith("_")},
            "nutrition_basis": "per_100g",
            "conversion_factor": 1.0,
            "fail_reasons": [],
            "accounted_mass": round(accounted, 1),
            "kcal": kcal,
        }

    # Try per-serving conversion
    serving_g = (
        serving_info.get("unit_size_g")
        or serving_info.get("serving_size_g")
        or serving_info.get("package_size_g")
    )

    if serving_g and 5.0 < serving_g < 120.0:
        factor = 100.0 / serving_g

        def _conv(v):
            return round(v * factor, 1) if v is not None else None

        converted = {
            "energy_kcal":     _conv(kcal),
            "fat_g":           _conv(fat),
            "fat_saturated_g": _conv(nutr_numeric.get("fat_saturated_g")),
            "sodium_mg":       _conv(nutr_numeric.get("sodium_mg")),
            "carbohydrates_g": _conv(carbs),
            "sugars_g":        _conv(sugars),
            "dietary_fiber_g": _conv(fiber),
            "protein_g":       _conv(protein),
        }

        conv_acc = (converted.get("carbohydrates_g") or 0.0) + \
                   (converted.get("fat_g") or 0.0) + \
                   (converted.get("protein_g") or 0.0) + \
                   (converted.get("dietary_fiber_g") or 0.0)
        conv_kcal = converted.get("energy_kcal") or 0.0
        conv_sugars = converted.get("sugars_g")

        conv_fails = _check(conv_kcal, conv_acc, conv_sugars)

        if not conv_fails:
            return {
                "verdict": "converted_pass",
                "final_nutrition": converted,
                "nutrition_basis": "converted_from_serving",
                "conversion_factor": round(factor, 3),
                "serving_g_used": serving_g,
                "fail_reasons": fails,
                "original_fail_reasons": fails,
                "accounted_mass": round(conv_acc, 1),
                "kcal": conv_kcal,
            }

    return {
        "verdict": "quarantine",
        "final_nutrition": None,
        "nutrition_basis": None,
        "fail_reasons": fails,
        "accounted_mass": round(accounted, 1),
        "kcal": kcal,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Main pipeline
# ──────────────────────────────────────────────────────────────────────────────

def main():
    log.info("=" * 70)
    log.info("TASK-365 Protein Combined Corpus — Bars + Cookies + Bites")
    log.info("Run ID: %s", RUN_ID)
    log.info("=" * 70)

    # Reachability check
    log.info("\n--- REACHABILITY CHECK ---")
    probe = _get(f"{BASE}/online/he/", timeout=20)
    if not probe or probe.status_code >= 400:
        print(
            f"\nFATAL: Shufersal unreachable (status={getattr(probe, 'status_code', 'ERR')}). "
            "Cannot proceed — hard rule: stop and report if primary blocked.",
            file=sys.stderr,
        )
        sys.exit(2)
    log.info("Shufersal: reachable (HTTP %d, %.1f KB)", probe.status_code, len(probe.content) / 1024)

    # ── STEP 1: Discovery ──────────────────────────────────────────────────────
    log.info("\n--- STEP 1: Discovery ---")
    candidates = discover_protein_products()
    log.info("Discovery pool: %d candidates", len(candidates))

    if not candidates:
        print("FATAL: 0 protein candidates discovered from Shufersal.", file=sys.stderr)
        sys.exit(2)

    # ── STEP 2: Scrape + plausibility gate ────────────────────────────────────
    log.info("\n--- STEP 2: Scrape + Plausibility Gate ---")

    survived: list[dict] = []          # passed gate
    discards: list[dict] = []          # quarantined by gate
    cookie_rejected: list[dict] = []   # cookie_candidates rejected at ingredient check
    scrape_failed: list[dict] = []     # HTTP failure

    seen_barcodes: set[str] = set()    # dedup by barcode

    for code, meta in candidates.items():
        name_preview = meta.get("name", "")[:60]
        log.info("  Scraping: %s | %s", code, name_preview)

        raw = scrape_shufersal_product(code, meta)
        if raw is None:
            log.warning("  FAILED: %s | %s", code, name_preview)
            scrape_failed.append({"code": code, "name": name_preview, "reason": "scrape_http_fail"})
            time.sleep(PRODUCT_DELAY)
            continue

        barcode = raw["product_identity"]["barcode"]
        name = raw["product_identity"]["name"]
        ingredients = raw.get("ingredients_raw", "")

        # Cookie post-scrape protein check
        is_cookie_candidate = meta.get("cookie_candidate", False)
        if is_cookie_candidate and not meta.get("name_protein_signal", False):
            # Must have protein ingredient signal
            if not _has_protein_ingredient_signal(ingredients):
                log.info("  COOKIE REJECTED (no protein ingredient): %s | %s", barcode, name[:50])
                cookie_rejected.append({
                    "barcode": barcode,
                    "name": name,
                    "reason": "cookie_no_protein_ingredient_signal",
                    "ingredients_preview": ingredients[:200],
                })
                time.sleep(PRODUCT_DELAY)
                continue

        # Barcode dedup
        if barcode and barcode in seen_barcodes:
            log.info("  DEDUP: %s | %s", barcode, name[:50])
            time.sleep(PRODUCT_DELAY)
            continue
        if barcode:
            seen_barcodes.add(barcode)

        # Plausibility gate
        gate = plausibility_gate(
            raw["nutrition_numeric_per_100g"],
            raw["serving_info"],
            ingredients,
        )

        raw["plausibility_gate"] = gate

        if gate["verdict"] == "quarantine":
            log.warning("  QUARANTINE: %s | %s | %s",
                        barcode, name[:40], "; ".join(gate.get("fail_reasons", [])))
            discards.append({
                "barcode": barcode,
                "name": name,
                "shufersal_code": code,
                "reason": "plausibility_gate_fail",
                "fail_reasons": gate.get("fail_reasons", []),
                "accounted_mass_g": gate.get("accounted_mass"),
                "kcal": gate.get("kcal"),
            })
            time.sleep(PRODUCT_DELAY)
            continue

        # Build the canonical corpus record
        nn = gate["final_nutrition"] or {}
        scraped_brand = raw["product_identity"].get("brand", "")
        inferred_brand = _infer_brand(name, barcode) if not scraped_brand else scraped_brand

        corpus_record = {
            "barcode": barcode,
            "shufersal_code": code,
            "name": name,
            "brand": inferred_brand or scraped_brand,
            "brand_source": "scraped" if scraped_brand else "inferred_from_name_barcode",
            "image_url": raw["product_identity"].get("image_url"),
            "format": _infer_format(name),
            "weight_g": raw.get("weight_g"),
            "serving_info": raw["serving_info"],
            "nutrition_per_100g": {
                "energy_kcal":     nn.get("energy_kcal"),
                "fat_g":           nn.get("fat_g"),
                "fat_saturated_g": nn.get("fat_saturated_g"),
                "sodium_mg":       nn.get("sodium_mg"),
                "carbohydrates_g": nn.get("carbohydrates_g"),
                "sugars_g":        nn.get("sugars_g"),
                "dietary_fiber_g": nn.get("dietary_fiber_g"),
                "protein_g":       nn.get("protein_g"),
            },
            "ingredients_full": ingredients,
            "nutrition_basis": gate.get("nutrition_basis"),
            "gate_verdict": gate.get("verdict"),
            "conversion_factor": gate.get("conversion_factor", 1.0),
            "is_new_vs_existing": barcode not in EXISTING_BARCODES,
            "was_in_existing": barcode in EXISTING_BARCODES,
            "discovery_source": meta.get("source", ""),
            "name_protein_signal": meta.get("name_protein_signal", True),
            "provenance": raw["provenance"],
        }

        survived.append(corpus_record)
        log.info("  PASS [%s]: %s | %s | protein=%.1fg | acc=%.1fg",
                 gate["verdict"], barcode, name[:40],
                 nn.get("protein_g") or 0,
                 gate.get("accounted_mass", 0))

        time.sleep(PRODUCT_DELAY)

    # ── STEP 3: Build output JSON ──────────────────────────────────────────────
    log.info("\n--- STEP 3: Build corpus JSON ---")

    # Brand distribution
    from collections import Counter
    brand_counts = Counter(r["brand"] for r in survived)
    format_counts = Counter(r["format"] for r in survived)
    new_count = sum(1 for r in survived if r["is_new_vs_existing"])
    existing_count = sum(1 for r in survived if r["was_in_existing"])

    corpus_out = {
        "schema_version": "protein_combined_corpus_task365_v1",
        "run_id": RUN_ID,
        "generated_at": now_iso(),
        "task": "TASK-365",
        "scope": "protein bars + protein cookies + protein bites (ONE combined shelf)",
        "off_check": "PASS — no Open Food Facts used in any field",
        "staging_note": (
            "RAW CORPUS ONLY — no scoring, no BSIP2, no frontend JSON. "
            "Ready for new protein scoring lens. "
            "Do NOT deploy without scoring approval + adversarial QA."
        ),
        "products": survived,
    }

    save_json(CORPUS_PATH, corpus_out)
    log.info("Corpus JSON saved: %s (%d products)", CORPUS_PATH, len(survived))

    # Manifest
    manifest = {
        "run_id": RUN_ID,
        "generated_at": now_iso(),
        "task": "TASK-365",
        "corpus_file": str(CORPUS_PATH),
        "counts": {
            "discovery_pool": len(candidates),
            "scrape_failed": len(scrape_failed),
            "cookie_rejected_no_protein": len(cookie_rejected),
            "quarantine_plausibility_fail": len(discards),
            "survived_corpus": len(survived),
            "new_vs_existing_16": new_count,
            "carried_from_existing_16": existing_count,
        },
        "brand_distribution": dict(brand_counts.most_common()),
        "format_distribution": dict(format_counts),
        "discards": {
            "scrape_failed": scrape_failed,
            "cookie_rejected": cookie_rejected,
            "quarantined": discards,
        },
        "existing_barcodes_baseline": sorted(EXISTING_BARCODES),
        "new_barcodes": sorted(
            r["barcode"] for r in survived if r["is_new_vs_existing"]
        ),
        "carried_barcodes": sorted(
            r["barcode"] for r in survived if r["was_in_existing"]
        ),
    }

    save_json(MANIFEST_PATH, manifest)
    log.info("Manifest JSON saved: %s", MANIFEST_PATH)

    # ── Self-verify: reload and count ─────────────────────────────────────────
    log.info("\n--- SELF-VERIFY: reload corpus and count ---")
    reloaded = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    verified_count = len(reloaded["products"])
    log.info("Self-verify corpus count (from file): %d", verified_count)

    # Summary
    log.info("\n" + "=" * 70)
    log.info("TASK-365 PIPELINE SUMMARY")
    log.info("=" * 70)
    log.info("Discovery pool:              %d", len(candidates))
    log.info("Scrape failed:               %d", len(scrape_failed))
    log.info("Cookie rejected (no prot.):  %d", len(cookie_rejected))
    log.info("Quarantined (gate fail):     %d", len(discards))
    log.info("SURVIVED corpus:             %d", len(survived))
    log.info("  Verified count (from file):%d", verified_count)
    log.info("  New vs existing 16:        %d", new_count)
    log.info("  Carried from existing 16:  %d", existing_count)
    log.info("Brand distribution:")
    for brand, cnt in brand_counts.most_common():
        log.info("  %-30s %d", brand or "(no brand)", cnt)
    log.info("Format distribution:")
    for fmt, cnt in format_counts.items():
        log.info("  %-10s %d", fmt, cnt)
    if discards:
        log.info("\nDiscards (plausibility gate):")
        for d in discards:
            log.info("  %s | %s | %s", d["barcode"], (d.get("name") or "")[:35],
                     "; ".join(d.get("fail_reasons", [])))
    if cookie_rejected:
        log.info("\nCookie candidates rejected (no protein ingredient):")
        for c in cookie_rejected:
            log.info("  %s | %s", c["barcode"], (c.get("name") or "")[:40])

    return {
        "corpus_file": str(CORPUS_PATH),
        "manifest_file": str(MANIFEST_PATH),
        "verified_count": verified_count,
        "brand_distribution": dict(brand_counts.most_common()),
        "format_distribution": dict(format_counts),
        "new_count": new_count,
        "existing_count": existing_count,
        "discards": len(discards),
        "cookie_rejected": len(cookie_rejected),
        "scrape_failed": len(scrape_failed),
    }


if __name__ == "__main__":
    main()
