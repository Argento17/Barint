"""
Carrefour Israel probe — BSIP0 acquisition v2.

Raw HTTP returns 403. Strategy:
1. Open browser with persistent cookie context
2. Navigate Carrefour homepage — handle consent/cookie/location popups
3. Navigate to bread category pages
4. Capture XHR product API calls during navigation
5. Extract products from DOM + captured API calls
6. If login wall encountered: document, take screenshot, set requires_manual_action
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

BASE_URL = "https://www.carrefour.co.il"

BREAD_URLS = [
    f"{BASE_URL}/cat/לחם",
    f"{BASE_URL}/cat/מאפים",
    f"{BASE_URL}/search?q=לחם",
    f"{BASE_URL}/search?q=קרקר",
    f"{BASE_URL}/categories/bread",
    f"{BASE_URL}/categories/bakery",
]

CAPTURE_PATTERNS = [
    "carrefour.co.il/api",
    "/products",
    "/search",
    "/catalog",
    "algolia",
    "elasticpath",
    "boclips",
]

# Extra consent/popup selectors specific to Carrefour
CARREFOUR_CONSENT_SELECTORS = [
    "#onetrust-accept-btn-handler",
    ".onetrust-accept-btn-handler",
    "button[id='accept-all']",
    "button[class*='consent']",
    ".gdpr-accept",
    "button:has-text('אני מסכים')",
    "button:has-text('קבל')",
    "button:has-text('OK')",
    "[data-testid='cookie-consent-accept']",
]

LOCATION_SELECTORS = [
    "button:has-text('אישור')",
    "button:has-text('המשך')",
    ".location-modal button",
    "[data-testid='delivery-area-confirm']",
    "button[aria-label*='close']",
]

PRODUCT_SELECTORS = [
    ".product-item",
    ".product-card",
    "[data-product]",
    ".item",
    "article.product",
    ".product-list-item",
]

JS_EXTRACT = """
() => {
    const results = [];
    const selectors = [
        '.product-item', '.product-card', '[data-product]',
        '.item', 'article.product', '.product-list-item'
    ];
    let cards = [];
    for (const sel of selectors) {
        cards = document.querySelectorAll(sel);
        if (cards.length > 0) break;
    }
    cards.forEach(card => {
        const name = (
            card.querySelector('.product-name, .name, h2, h3, .title')?.innerText || ''
        ).trim();
        const price = (card.querySelector('.price')?.innerText || '').trim();
        const img = card.querySelector('img')?.src || '';
        const link = card.querySelector('a')?.href || '';
        const barcode = card.dataset?.product || card.dataset?.sku || '';
        if (name) results.push({ name, price, img, link, barcode });
    });
    return results;
}
"""

JS_CHECK_BLOCKED = """
() => {
    const body = document.body?.innerText?.toLowerCase() || '';
    return body.includes('403') || body.includes('forbidden') || body.includes('access denied');
}
"""

JS_CHECK_LOGIN_WALL = """
() => {
    const body = document.body?.innerText?.toLowerCase() || '';
    const url = window.location.href.toLowerCase();
    return (
        body.includes('התחבר') || body.includes('הרשמה') ||
        body.includes('login') || body.includes('sign in') ||
        url.includes('login') || url.includes('signin')
    ) && !document.querySelector('.product-item, .product-card');
}
"""


def _parse_api_product(item: dict, source_url: str) -> RawProduct | None:
    name = (
        item.get("name", "")
        or item.get("title", "")
        or item.get("he_name", "")
        or ""
    ).strip()
    if not name:
        return None

    sku = str(item.get("sku", item.get("id", item.get("barcode", ""))))
    brand = item.get("brand", item.get("manufacturer", ""))
    if isinstance(brand, dict):
        brand = brand.get("name", "")

    img_raw = item.get("image", item.get("thumbnail", item.get("images", "")))
    img_urls = []
    if isinstance(img_raw, str) and img_raw:
        img_urls = [img_raw]
    elif isinstance(img_raw, list):
        img_urls = [i for i in img_raw if isinstance(i, str)][:3]

    nutr = item.get("nutrition", item.get("nutritionFacts", {})) or {}
    p = RawProduct(
        retailer_id="carrefour",
        retailer_name="קרפור ישראל",
        source_url=source_url,
        scraped_at="",
        name_he=name,
        brand=brand if isinstance(brand, str) else "",
        barcode=sku,
        image_urls=img_urls,
        extraction_method="xhr_capture",
        extraction_confidence="high",
        raw_source_json=item,
    )
    if isinstance(nutr, dict) and nutr:
        p.energy_kcal_raw = str(nutr.get("energy_kcal", nutr.get("calories", "")) or "")
        p.protein_raw = str(nutr.get("protein", "") or "")
        p.carbs_raw = str(nutr.get("carbohydrates", nutr.get("carbs", "")) or "")
        p.fat_raw = str(nutr.get("fat", nutr.get("total_fat", "")) or "")
        p.fiber_raw = str(nutr.get("fiber", nutr.get("dietary_fiber", "")) or "")
    ingredients = item.get("ingredients", item.get("ingredients_text", "")) or ""
    if isinstance(ingredients, str) and ingredients:
        p.ingredients_raw = ingredients
        p.ingredients_language = "he" if any(
            "א" <= c <= "ת" for c in ingredients
        ) else "en"
    return p


class CarrefourProbe(RetailSource):
    retailer_id = "carrefour"
    retailer_name = "קרפור ישראל"
    retailer_url = BASE_URL
    requires_browser = True
    capture_patterns = CAPTURE_PATTERNS

    def probe(self) -> RetailProbeResult:
        result = self._empty_result(access_method="playwright_browser")
        try:
            with BrowserSession(
                retailer_id="carrefour",
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
        ok = session.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
        if not ok:
            result.access_status = "failed"
            result.blocker_type = "timeout"
            result.blocker_detail = "Browser timed out on Carrefour homepage"
            path = session.screenshot("homepage_timeout")
            result.screenshots.append(str(path))
            return result

        session.wait_networkidle(timeout=20_000)

        # Handle Carrefour-specific consent buttons first
        for sel in CARREFOUR_CONSENT_SELECTORS:
            try:
                loc = session.page.locator(sel).first
                if loc.is_visible(timeout=600):
                    loc.click(timeout=800)
                    session.page.wait_for_timeout(600)
                    result.probe_notes.append(f"Clicked consent: {sel}")
                    break
            except Exception:
                continue

        # Generic popup dismissal
        dismissed = session.dismiss_popups()
        if dismissed:
            result.probe_notes.append(f"Dismissed generic popups: {dismissed}")

        # Handle location prompts
        for sel in LOCATION_SELECTORS:
            try:
                loc = session.page.locator(sel).first
                if loc.is_visible(timeout=500):
                    loc.click(timeout=700)
                    session.page.wait_for_timeout(500)
                    result.probe_notes.append(f"Dismissed location prompt: {sel}")
                    break
            except Exception:
                continue

        # Check for hard block
        is_blocked = session.eval_js(JS_CHECK_BLOCKED)
        if is_blocked or session.is_blocked():
            result.access_status = "blocked"
            result.blocker_type = "http_403"
            result.blocker_detail = "Browser also receives block response from Carrefour"
            path = session.screenshot("blocked_homepage")
            result.screenshots.append(str(path))
            result.probe_notes.append("IP/fingerprint block confirmed in browser")
            return result

        path = session.screenshot("homepage_loaded")
        result.screenshots.append(str(path))
        result.probe_notes.append(f"Homepage loaded: {session.title()}")

        # Check login wall
        is_login = session.eval_js(JS_CHECK_LOGIN_WALL)
        if is_login:
            result.access_status = "partial"
            result.blocker_type = "auth_required"
            result.blocker_detail = "Login wall detected on Carrefour homepage"
            result.requires_manual_action = True
            result.manual_action_description = (
                "Carrefour requires login to browse products. "
                "Manual step: open a browser, log in to carrefour.co.il, "
                "then export the session cookies so the probe can reuse them. "
                "Alternatively: browse to a product category manually and document the URL structure."
            )
            path = session.screenshot("login_wall")
            result.screenshots.append(str(path))
            return result

        # Navigate category pages
        all_products: list[RawProduct] = []
        seen_names: set[str] = set()

        for cat_url in BREAD_URLS:
            session.goto(cat_url, wait_until="domcontentloaded", timeout=25_000)
            session.wait_networkidle(timeout=15_000)
            session.page.wait_for_timeout(1500)
            session.dismiss_popups()

            # Wait for product cards
            found_cards = False
            for sel in PRODUCT_SELECTORS:
                try:
                    session.page.wait_for_selector(sel, timeout=5000)
                    found_cards = True
                    result.probe_notes.append(f"{cat_url} → found cards: '{sel}'")
                    break
                except Exception:
                    continue

            path = session.screenshot(f"cat_{cat_url.split('/')[-1][:20]}")
            result.screenshots.append(str(path))

            if not found_cards:
                result.probe_notes.append(f"{cat_url} → no product cards")
                continue

            raw_items = session.eval_js(JS_EXTRACT) or []
            result.probe_notes.append(
                f"{cat_url} → {len(raw_items)} DOM items"
            )
            for item in raw_items:
                name = item.get("name", "").strip()
                if not name or name in seen_names:
                    continue
                seen_names.add(name)
                link = item.get("link", "")
                if not link.startswith("http"):
                    link = BASE_URL + link if link.startswith("/") else BASE_URL
                p = self._product(
                    source_url=link or cat_url,
                    name_he=name,
                    category_raw="bread",
                    image_urls=[item.get("img", "")] if item.get("img") else [],
                    barcode=item.get("barcode", ""),
                    extraction_method="dom_parse",
                    extraction_confidence="medium",
                    raw_source_json=item,
                )
                all_products.append(p)

        # Parse XHR captures
        for cr in session.captured:
            result.captured_api_calls.append(cr.to_dict())
            if cr.response_status != 200 or not cr.response_body:
                continue
            try:
                data = json.loads(cr.response_body)
                items = (
                    data if isinstance(data, list)
                    else data.get("products", data.get("items", data.get("hits", [])))
                )
                if not isinstance(items, list) or not items:
                    continue
                result.probe_notes.append(
                    f"XHR {cr.url[:70]} → {len(items)} items"
                )
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    p = _parse_api_product(item, cr.url)
                    if p:
                        if p.name_he in seen_names:
                            continue
                        seen_names.add(p.name_he)
                        p.scraped_at = self._timestamp()
                        all_products.append(p)
            except Exception:
                pass

        result.products = all_products

        if all_products:
            result.access_status = "accessible"
        else:
            result.access_status = "blocked"
            result.blocker_type = "http_403"
            result.blocker_detail = (
                "Browser could load pages but no product data extracted. "
                "Carrefour Israel may require logged-in session to browse catalog."
            )
            result.requires_manual_action = True
            result.manual_action_description = (
                "No products extracted even with browser. "
                "Verify manually: does the Carrefour Israel website show product listings "
                "without login? If not, a logged-in session cookie is required."
            )

        return result


if __name__ == "__main__":
    probe = CarrefourProbe()
    res = probe.probe()
    print(f"Status: {res.access_status} | Blocker: {res.blocker_type}")
    print(f"Products: {res.n_products()}")
    if res.requires_manual_action:
        print(f"MANUAL ACTION REQUIRED: {res.manual_action_description}")
    for note in res.probe_notes:
        print(f"  {note}")
    for p in res.products[:3]:
        print(f"  - {p.name_he}")
