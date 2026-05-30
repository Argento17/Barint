"""
Shufersal probe — BSIP0 acquisition v2.

Strategy:
1. Static HTTP maintenance check
2. Search via /online/he/search?q=<query> (server-rendered HTML, no JS required)
3. For each product: fetch individual product page for nutrition + ingredients
4. Nutrition from .nutritionList div; ingredients from tab section; JSON-LD for barcode/image

Product URL pattern: /online/he/p/p_<code_lowercase> → redirects to full path
Search URL: /online/he/search?q=<encoded>&pageSize=48
"""

from __future__ import annotations

import re
import sys
from time import sleep

import requests
from bs4 import BeautifulSoup

from retailer_base import RawProduct, RetailProbeResult, RetailSource

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))

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

SEARCH_QUERIES = ["לחם", "קרקר", "כוסמין", "שיפון", "פיתה", "לחמניה"]
PAGE_SIZE = 48
MAX_PRODUCTS = 120   # cap to avoid runaway fetches
PRODUCT_PAGE_DELAY = 0.8  # seconds between product page fetches

NUTR_LABEL_MAP = {
    "אנרגיה": "energy",
    "קל":     "energy",
    "kcal":   "energy",
    "חלבונים": "protein",
    "חלבון":   "protein",
    "פחמימות": "carbs",
    "שומנים":  "fat",
    "שומן":    "fat",
    "סיבים תזונתיים": "fiber",
    "סיבים":  "fiber",
    "נתרן":   "sodium",
    "סוכרים": "sugar",
}

MAINTENANCE_SIGNALS = ["maintenance", "אתר בתחזוקה", "בתחזוקה"]


def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    return len(text) < 5000 and any(s in text.lower() for s in MAINTENANCE_SIGNALS)


def _get(url: str, timeout: int = 20) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return r
    except Exception:
        return None


def _search(query: str) -> list[dict]:
    """Fetch search results page, extract product li elements."""
    url = f"{BASE}/online/he/search?q={requests.utils.quote(query)}&pageSize={PAGE_SIZE}"
    r = _get(url)
    if not r or r.status_code != 200:
        return []
    if _is_maintenance(r.content):
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.find_all("li", attrs={"data-product-name": True})
    products = []
    for li in items:
        d = li.attrs
        name = d.get("data-product-name", "").strip()
        code = d.get("data-product-code", "").strip()
        if not name or not code:
            continue
        is_food = d.get("data-food", "false").lower() == "true"
        cats = d.get("data-all-categories", "")
        price = d.get("data-product-price", "")
        img = li.find("img")
        img_url = img.get("src", "") if img else ""
        product_url = f"{BASE}/online/he/p/{code.lower()}"
        products.append({
            "name": name,
            "code": code,
            "is_food": is_food,
            "categories": cats,
            "price": price,
            "url": product_url,
            "img": img_url,
        })
    return products


def _parse_product_page(code: str, base_meta: dict) -> RawProduct | None:
    """Fetch product page, extract nutrition table and ingredients."""
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=20)
    if not r or r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    product_url = r.url  # use final redirected URL as canonical source

    # JSON-LD for barcode and image
    ld_name, ld_sku, ld_gtin, ld_images = "", "", "", []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            import json
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_sku = ld.get("sku", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                ld_images = ld.get("image", [])
                if isinstance(ld_images, str):
                    ld_images = [ld_images]
                break
        except Exception:
            pass

    # Nutrition table
    nutr_raw: dict[str, str] = {}
    nutr_div = soup.find("div", class_="nutritionList")
    if nutr_div:
        for item in nutr_div.find_all("div", class_="nutritionItem"):
            divs = item.find_all("div")
            parts = [d.get_text(strip=True) for d in divs if d.get_text(strip=True)]
            # Structure: [value, unit, label] or [value, label]
            if len(parts) >= 2:
                value = parts[0]
                label = parts[-1]
                for he_label, field in NUTR_LABEL_MAP.items():
                    if he_label in label:
                        nutr_raw[field] = value
                        break

    # Ingredients — in product tab section, after "רכיבים" label
    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        # Walk up to find container, then get subsequent text
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            # Find where "רכיב" starts and take everything after
            match = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if match:
                ingredients_raw = match.group(1).strip()[:800]

    # If not found via label, check the full product tab text
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{30,})", text)
            if m:
                ingredients_raw = m.group(1)[:800]
                break

    name = ld_name or base_meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "")

    p = RawProduct(
        retailer_id="shufersal",
        retailer_name="שופרסל",
        source_url=product_url,
        scraped_at="",
        name_he=name,
        barcode=barcode,
        category_raw=base_meta.get("categories", ""),
        image_urls=[u for u in ld_images[:3] if u],
        ingredients_raw=ingredients_raw,
        ingredients_language="he" if ingredients_raw and any("א" <= c <= "ת" for c in ingredients_raw) else "",
        extraction_method="html_parse",
        extraction_confidence="high" if nutr_raw else "medium",
        raw_source_json={
            "ld_json": {"sku": ld_sku, "gtin13": ld_gtin},
            "price": base_meta.get("price", ""),
        },
    )

    # Map nutrition fields
    p.energy_kcal_raw = nutr_raw.get("energy", "")
    p.protein_raw = nutr_raw.get("protein", "")
    p.carbs_raw = nutr_raw.get("carbs", "")
    p.fat_raw = nutr_raw.get("fat", "")
    p.fiber_raw = nutr_raw.get("fiber", "")
    p.sodium_raw = nutr_raw.get("sodium", "")
    p.sugar_raw = nutr_raw.get("sugar", "")

    return p


class ShufersalProbe(RetailSource):
    retailer_id = "shufersal"
    retailer_name = "שופרסל"
    retailer_url = BASE
    requires_browser = False
    capture_patterns = []

    def probe(self) -> RetailProbeResult:
        result = self._empty_result(access_method="http_static")

        # Step 1 — maintenance check
        r = _get(BASE)
        if not r:
            result.access_status = "failed"
            result.blocker_type = "timeout"
            result.blocker_detail = "Connection failed"
            return result

        result.http_status = r.status_code
        if _is_maintenance(r.content):
            result.access_status = "maintenance"
            result.blocker_type = "maintenance_mode"
            result.blocker_detail = f"HTTP {r.status_code}, {len(r.content)}B — maintenance placeholder"
            result.probe_notes.append("Site in maintenance mode — skipping search")
            return result

        result.probe_notes.append("Maintenance check passed — searching for bread/cracker products")

        # Step 2 — search and collect unique product codes
        seen_codes: set[str] = set()
        search_meta: dict[str, dict] = {}

        for query in SEARCH_QUERIES:
            items = _search(query)
            new = 0
            for item in items:
                code = item["code"]
                if code and code not in seen_codes and item["is_food"]:
                    seen_codes.add(code)
                    search_meta[code] = item
                    new += 1
            result.probe_notes.append(
                f"Search '{query}' → {len(items)} items, {new} new unique food products"
            )
            if len(seen_codes) >= MAX_PRODUCTS:
                break

        result.probe_notes.append(f"Total unique products to fetch: {len(seen_codes)}")

        if not seen_codes:
            result.access_status = "blocked"
            result.blocker_type = "api_no_products"
            result.blocker_detail = "Search returned no food products"
            return result

        # Step 3 — fetch each product page
        products: list[RawProduct] = []
        failed = 0
        for code in list(seen_codes)[:MAX_PRODUCTS]:
            p = _parse_product_page(code, search_meta.get(code, {}))
            if p:
                p.scraped_at = self._timestamp()
                products.append(p)
            else:
                failed += 1
            sleep(PRODUCT_PAGE_DELAY)

        result.products = products
        result.probe_notes.append(
            f"Product pages fetched: {len(products)} OK, {failed} failed"
        )

        if products:
            n_nutr = sum(1 for p in products if p.has_nutrition())
            n_ingr = sum(1 for p in products if p.has_ingredients())
            result.probe_notes.append(
                f"Coverage: {n_nutr}/{len(products)} nutrition, {n_ingr}/{len(products)} ingredients"
            )
            result.access_status = "accessible"
        else:
            result.access_status = "blocked"
            result.blocker_type = "api_no_products"
            result.blocker_detail = "Product pages returned no extractable data"

        return result


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    probe = ShufersalProbe()
    res = probe.probe()
    print(f"Status: {res.access_status}")
    print(f"Products: {res.n_products()}")
    for note in res.probe_notes:
        print(f"  {note}")
    for p in res.products[:5]:
        print(f"  - {p.name_he} | {p.barcode} | kcal={p.energy_kcal_raw} | fiber={p.fiber_raw} | ingr={bool(p.ingredients_raw)}")
