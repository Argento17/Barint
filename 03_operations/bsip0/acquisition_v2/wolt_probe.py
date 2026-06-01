"""
Wolt Market probe — BSIP0 acquisition v2.

Known from bread_retail_002 investigation:
- Consumer API front page: accessible (698KB JSON)
- Venue SSR page: accessible (1.6MB HTML with React Query dehydrated state)
- SSR products: only 24 promoted items (vegetables/dairy) — no bread
- Category product API: returns 404/410 without auth

Strategy:
1. Open browser, navigate to Wolt venue page
2. Handle any cookie/consent popups
3. Click bread category links (menucategory-32, menucategory-26, menucategory-218)
4. Capture all XHR calls triggered by category clicks
5. Extract product data from XHR responses (product API)
6. Parse any SSR JSON for additional product data
7. If auth required: document and stop — do NOT attempt login unless user provides session
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from browser_session import BrowserSession
from retailer_base import RawProduct, RetailProbeResult, RetailSource

VENUE_SLUG = "wolt-market-ben-yehuda"
VENUE_ID = "64048ba88782694efcd34892"
BASE_WOLT = "https://wolt.com"
VENUE_URL = f"{BASE_WOLT}/he/isr/tel-aviv/restaurant/{VENUE_SLUG}"

BREAD_CATEGORY_IDS = [
    "menucategory-32",   # לחם פרוס ושלם
    "menucategory-26",   # מאפייה
    "menucategory-218",  # קרקרים
    "menucategory-217",  # פריכיות
    "menucategory-212",  # חטיפים וקרקרים
    "menucategory-33",   # פיתות, לחמניות וטורטיות
]

CAPTURE_PATTERNS = [
    "consumer-api.wolt.com",
    "restaurant-api.wolt.com",
    "wolt.com/api",
    "/menu",
    "/items",
    "/products",
    "/categories",
]

JS_CHECK_AUTH = """
() => {
    const body = document.body?.innerText?.toLowerCase() || '';
    const url = window.location.href.toLowerCase();
    return (
        body.includes('התחבר') || body.includes('כניסה') ||
        body.includes('log in') || body.includes('sign in') ||
        url.includes('/login') || url.includes('/signup')
    );
}
"""

JS_EXTRACT_MENU_ITEMS = """
() => {
    const results = [];
    // Wolt product cards
    const cards = document.querySelectorAll(
        '[data-test-id="horizontal-item-card"], ' +
        '[class*="ItemCard"], [class*="product-card"], ' +
        'li[class*="item"]'
    );
    cards.forEach(card => {
        const name = (
            card.querySelector('[class*="name"], h3, h4, [class*="title"]')?.innerText || ''
        ).trim();
        const price = (card.querySelector('[class*="price"]')?.innerText || '').trim();
        const img = card.querySelector('img')?.src || '';
        const link = card.querySelector('a')?.href || '';
        if (name) results.push({ name, price, img, link });
    });
    return results;
}
"""

JS_FIND_CATEGORY_LINKS = """
() => {
    const links = [];
    document.querySelectorAll('a[href*="menucategory"]').forEach(a => {
        links.push({ href: a.href, text: a.innerText.trim() });
    });
    // Also check buttons with category IDs in data attributes
    document.querySelectorAll('[data-category-id], [data-id*="menucategory"]').forEach(el => {
        links.push({
            href: el.getAttribute('data-category-id') || el.getAttribute('data-id') || '',
            text: el.innerText.trim(),
            isButton: true
        });
    });
    return links;
}
"""


def _parse_wolt_item(item: dict, source_url: str) -> RawProduct | None:
    name = (
        item.get("name", {})
        if isinstance(item.get("name"), dict)
        else {"he": item.get("name", ""), "en": item.get("name", "")}
    )
    name_he = name.get("he", "") if isinstance(name, dict) else str(name)
    name_en = name.get("en", "") if isinstance(name, dict) else ""

    if not name_he and not name_en:
        return None

    barcode = item.get("barcode_gtin", item.get("barcode", item.get("id", "")))
    images = item.get("image_blurhash", item.get("images", []))
    img_urls = []
    if isinstance(images, list):
        img_urls = [i.get("url", i) if isinstance(i, dict) else i for i in images[:3]]

    desc = item.get("description", {})
    if isinstance(desc, dict):
        desc = desc.get("he", desc.get("en", ""))
    elif not isinstance(desc, str):
        desc = ""

    p = RawProduct(
        retailer_id="wolt_market",
        retailer_name="וולט מרקט",
        source_url=source_url,
        scraped_at="",
        name_he=name_he,
        name_en=name_en,
        barcode=str(barcode) if barcode else "",
        image_urls=[u for u in img_urls if u],
        extraction_method="xhr_capture",
        extraction_confidence="high",
        raw_source_json=item,
    )

    # Wolt sometimes embeds nutrition in the item (not always populated)
    nutr = item.get("nutrition_info", item.get("nutritional_info", {})) or {}
    if isinstance(nutr, dict) and nutr:
        p.energy_kcal_raw = str(nutr.get("energy_kcal", nutr.get("calories", "")) or "")
        p.protein_raw = str(nutr.get("protein", "") or "")
        p.carbs_raw = str(nutr.get("carbohydrates", "") or "")
        p.fat_raw = str(nutr.get("fat", "") or "")
        p.fiber_raw = str(nutr.get("fiber", "") or "")

    ingredients = item.get("ingredients", "") or ""
    if isinstance(ingredients, dict):
        ingredients = ingredients.get("he", ingredients.get("en", ""))
    if ingredients:
        p.ingredients_raw = str(ingredients)
        p.ingredients_language = "he" if any("א" <= c <= "ת" for c in str(ingredients)) else "en"

    return p


class WoltProbe(RetailSource):
    retailer_id = "wolt_market"
    retailer_name = "וולט מרקט"
    retailer_url = VENUE_URL
    requires_browser = True
    capture_patterns = CAPTURE_PATTERNS

    def probe(self) -> RetailProbeResult:
        result = self._empty_result(access_method="playwright_browser")
        try:
            with BrowserSession(
                retailer_id="wolt_market",
                headless=True,
                capture_patterns=CAPTURE_PATTERNS,
                slow_mo=300,
            ) as session:
                result = self._run(session, result)
        except Exception as exc:
            result.access_status = "failed"
            result.blocker_type = "browser_crash"
            result.blocker_detail = str(exc)
            result.probe_notes.append(f"Browser session crashed: {exc}")
        return result

    def _run(self, session: BrowserSession, result: RetailProbeResult) -> RetailProbeResult:
        ok = session.goto(VENUE_URL, wait_until="domcontentloaded", timeout=35_000)
        if not ok:
            result.access_status = "failed"
            result.blocker_type = "timeout"
            result.blocker_detail = "Browser timed out loading Wolt venue page"
            path = session.screenshot("venue_timeout")
            result.screenshots.append(str(path))
            return result

        session.wait_networkidle(timeout=20_000)
        dismissed = session.dismiss_popups()
        if dismissed:
            result.probe_notes.append(f"Dismissed popups: {dismissed}")

        # Check auth wall
        is_auth = session.eval_js(JS_CHECK_AUTH)
        if is_auth:
            result.access_status = "partial"
            result.blocker_type = "auth_required"
            result.blocker_detail = "Wolt requires login to view product catalog"
            result.requires_manual_action = True
            result.manual_action_description = (
                "Wolt shows a login prompt. To unlock: "
                "1) Log in to wolt.com in a regular browser, "
                "2) Export cookies from the wolt.com domain, "
                "3) Import them into the sessions/wolt_market/ directory. "
                "Do NOT provide Wolt account credentials here."
            )
            path = session.screenshot("auth_wall")
            result.screenshots.append(str(path))
            return result

        path = session.screenshot("venue_homepage")
        result.screenshots.append(str(path))
        result.probe_notes.append(f"Wolt venue loaded: {session.title()}")

        # Find category links in the rendered DOM
        cat_links = session.eval_js(JS_FIND_CATEGORY_LINKS) or []
        result.probe_notes.append(f"Category links found in DOM: {len(cat_links)}")
        for link in cat_links[:10]:
            result.probe_notes.append(f"  cat link: {link.get('text', '')} → {link.get('href', '')[:60]}")

        all_products: list[RawProduct] = []
        seen_ids: set[str] = set()

        # Click bread categories
        for cat_id in BREAD_CATEGORY_IDS:
            # Try to find and click the category link
            category_url = f"{VENUE_URL}?category={cat_id}"
            session.goto(category_url, wait_until="domcontentloaded", timeout=25_000)
            session.wait_networkidle(timeout=15_000)
            session.page.wait_for_timeout(2000)
            session.dismiss_popups()

            # Extract from DOM
            dom_items = session.eval_js(JS_EXTRACT_MENU_ITEMS) or []
            if dom_items:
                result.probe_notes.append(
                    f"{cat_id} → {len(dom_items)} DOM items"
                )
                for item in dom_items:
                    name = item.get("name", "").strip()
                    if not name or name in seen_ids:
                        continue
                    seen_ids.add(name)
                    p = self._product(
                        source_url=item.get("link", category_url) or category_url,
                        name_he=name,
                        category_raw=cat_id,
                        image_urls=[item.get("img", "")] if item.get("img") else [],
                        extraction_method="dom_parse",
                        extraction_confidence="medium",
                        raw_source_json=item,
                    )
                    all_products.append(p)
            else:
                result.probe_notes.append(f"{cat_id} → no DOM items")

            path = session.screenshot(f"cat_{cat_id}")
            result.screenshots.append(str(path))

        # Process XHR captures
        for cr in session.captured:
            result.captured_api_calls.append(cr.to_dict())
            if cr.response_status != 200 or not cr.response_body:
                continue
            try:
                data = json.loads(cr.response_body)

                # Wolt menu structure: {"sections": [{"items": [...]}]}
                sections = data.get("sections", [])
                for section in sections:
                    for item in section.get("items", []):
                        if not isinstance(item, dict):
                            continue
                        item_id = str(item.get("id", ""))
                        if item_id in seen_ids:
                            continue
                        p = _parse_wolt_item(item, cr.url)
                        if p:
                            seen_ids.add(item_id or p.name_he)
                            p.scraped_at = self._timestamp()
                            all_products.append(p)

                # Direct items array
                items = data.get("items", [])
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    item_id = str(item.get("id", ""))
                    if item_id in seen_ids:
                        continue
                    p = _parse_wolt_item(item, cr.url)
                    if p:
                        seen_ids.add(item_id or p.name_he)
                        p.scraped_at = self._timestamp()
                        all_products.append(p)

                if sections or items:
                    result.probe_notes.append(
                        f"XHR {cr.url[:70]} → {len(sections)} sections, {len(items)} direct items"
                    )
            except Exception:
                pass

        result.products = all_products

        if all_products:
            result.access_status = "accessible"
            result.probe_notes.append(f"Total products extracted: {len(all_products)}")
        else:
            result.access_status = "partial"
            result.blocker_type = "auth_required"
            result.blocker_detail = (
                "Wolt venue page loaded in browser but category product API "
                "returned no items. Product listings require authenticated session "
                "or Wolt-specific session token."
            )
            result.requires_manual_action = True
            result.manual_action_description = (
                "No products retrieved from Wolt Market via browser. "
                "The category product API calls may require a Wolt session cookie. "
                "Options: (1) provide Wolt session cookies for import, "
                "(2) navigate categories manually and identify which API endpoints "
                "return product JSON, (3) contact Wolt Israel for data partnership."
            )

        return result


if __name__ == "__main__":
    probe = WoltProbe()
    res = probe.probe()
    print(f"Status: {res.access_status} | Blocker: {res.blocker_type}")
    print(f"Products: {res.n_products()}")
    if res.requires_manual_action:
        print(f"MANUAL ACTION: {res.manual_action_description}")
    for note in res.probe_notes:
        print(f"  {note}")
    for p in res.products[:5]:
        print(f"  - {p.name_he} | {p.barcode}")
