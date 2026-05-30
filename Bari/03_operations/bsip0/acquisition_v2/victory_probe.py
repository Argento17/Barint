"""
Victory (ויקטורי) probe — BSIP0 acquisition v2.

Victory is an AngularJS SPA — static HTTP returns only the 6716B JS shell.
Strategy:
1. Open browser, navigate to Victory, wait for networkidle
2. Confirm Angular rendered (look for ng-version on html element)
3. Navigate to bread/cracker category pages
4. Wait for product cards to appear in DOM
5. Extract product data from rendered DOM and any captured XHR calls
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

BASE_URL = "https://www.victory.co.il"

BREAD_CATEGORY_URLS = [
    f"{BASE_URL}/category/%D7%9C%D7%97%D7%9D",            # לחם
    f"{BASE_URL}/category/%D7%A7%D7%A8%D7%A7%D7%A8%D7%99%D7%9D",  # קרקרים
    f"{BASE_URL}/search?q=%D7%9C%D7%97%D7%9D",           # search: לחם
    f"{BASE_URL}/search?q=%D7%A7%D7%A8%D7%A7%D7%A8",     # search: קרקר
]

CAPTURE_PATTERNS = [
    "/api/products",
    "/api/search",
    "/api/category",
    "victory.co.il/api",
    "graphql",
]

PRODUCT_CARD_SELECTORS = [
    ".product-item",
    ".product-card",
    "[data-product-id]",
    "[data-item-id]",
    ".item-wrapper",
    "app-product",
    ".product",
]

JS_EXTRACT = """
() => {
    const results = [];
    const cards = document.querySelectorAll(
        '.product-item, .product-card, [data-product-id], [data-item-id], app-product'
    );
    cards.forEach(card => {
        const name = (
            card.querySelector('.product-name, .item-name, h2, h3, .name')?.innerText || ''
        ).trim();
        const price = (
            card.querySelector('.price, .product-price, .item-price')?.innerText || ''
        ).trim();
        const img = card.querySelector('img')?.src || '';
        const link = card.querySelector('a')?.href || '';
        const barcode = card.dataset?.productId || card.dataset?.itemId || '';
        if (name) results.push({ name, price, img, link, barcode });
    });
    return results;
}
"""

JS_CHECK_ANGULAR = """
() => {
    const html = document.documentElement;
    return html.getAttribute('ng-version') || html.getAttribute('ng-app') || null;
}
"""


class VictoryProbe(RetailSource):
    retailer_id = "victory"
    retailer_name = "ויקטורי"
    retailer_url = BASE_URL
    requires_browser = True
    capture_patterns = CAPTURE_PATTERNS

    def probe(self) -> RetailProbeResult:
        result = self._empty_result(access_method="playwright_browser")

        try:
            with BrowserSession(
                retailer_id="victory",
                headless=True,
                capture_patterns=CAPTURE_PATTERNS,
                slow_mo=200,
            ) as session:
                result = self._run(session, result)
        except Exception as exc:
            result.access_status = "failed"
            result.blocker_type = "browser_crash"
            result.blocker_detail = str(exc)
            result.probe_notes.append(f"Browser session crashed: {exc}")

        return result

    def _run(self, session: BrowserSession, result: RetailProbeResult) -> RetailProbeResult:
        # Navigate to homepage
        ok = session.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
        if not ok:
            result.access_status = "failed"
            result.blocker_type = "timeout"
            result.blocker_detail = "Browser timed out on homepage"
            path = session.screenshot("homepage_timeout")
            result.screenshots.append(str(path))
            return result

        session.wait_networkidle(timeout=20_000)
        dismissed = session.dismiss_popups()
        if dismissed:
            result.probe_notes.append(f"Dismissed popups: {dismissed}")

        # Check Angular rendered
        ng_version = session.eval_js(JS_CHECK_ANGULAR)
        if not ng_version:
            # Try waiting longer for Angular bootstrap
            session.page.wait_for_timeout(3000)
            ng_version = session.eval_js(JS_CHECK_ANGULAR)

        if ng_version:
            result.probe_notes.append(f"Angular detected: ng-version={ng_version}")
        else:
            result.probe_notes.append("Angular NOT detected — page may not be AngularJS or failed to render")
            if session.is_blocked():
                result.access_status = "blocked"
                result.blocker_type = "http_403"
                result.blocker_detail = "Page shows block indicators even in browser"
                path = session.screenshot("blocked")
                result.screenshots.append(str(path))
                return result

        # Take homepage screenshot as evidence
        path = session.screenshot("homepage_loaded")
        result.screenshots.append(str(path))

        all_products: list[RawProduct] = []
        seen_names: set[str] = set()

        for cat_url in BREAD_CATEGORY_URLS:
            session.goto(cat_url, wait_until="domcontentloaded", timeout=25_000)
            session.wait_networkidle(timeout=15_000)
            session.page.wait_for_timeout(2000)
            session.dismiss_popups()

            # Wait for product cards
            found_cards = False
            for sel in PRODUCT_CARD_SELECTORS:
                try:
                    session.page.wait_for_selector(sel, timeout=5000)
                    found_cards = True
                    result.probe_notes.append(f"{cat_url} → found cards with selector '{sel}'")
                    break
                except Exception:
                    continue

            if not found_cards:
                result.probe_notes.append(f"{cat_url} → no product cards found")
                path = session.screenshot(f"no_cards_{cat_url.split('/')[-1][:20]}")
                result.screenshots.append(str(path))
                continue

            # Extract via JS
            raw_items = session.eval_js(JS_EXTRACT) or []
            result.probe_notes.append(
                f"{cat_url} → extracted {len(raw_items)} items via DOM"
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
                    category_raw=cat_url.split("/")[-1],
                    image_urls=[item.get("img", "")] if item.get("img") else [],
                    barcode=item.get("barcode", ""),
                    extraction_method="dom_parse",
                    extraction_confidence="medium",
                    raw_source_json=item,
                )
                all_products.append(p)

        # Also check XHR captures for richer data
        for cr in session.captured:
            if cr.response_status == 200 and cr.response_body:
                try:
                    data = json.loads(cr.response_body)
                    items = data if isinstance(data, list) else data.get("products", data.get("items", []))
                    if isinstance(items, list) and items:
                        result.probe_notes.append(
                            f"XHR capture: {cr.url[:80]} → {len(items)} items"
                        )
                        for item in items:
                            if not isinstance(item, dict):
                                continue
                            name = item.get("name", item.get("title", "")).strip()
                            if not name or name in seen_names:
                                continue
                            seen_names.add(name)
                            p = self._product(
                                source_url=cr.url,
                                name_he=name,
                                barcode=str(item.get("sku", item.get("id", ""))),
                                extraction_method="xhr_capture",
                                extraction_confidence="high",
                                raw_source_json=item,
                            )
                            all_products.append(p)
                except Exception:
                    pass
            result.captured_api_calls.append(cr.to_dict())

        result.products = all_products

        if all_products:
            result.access_status = "accessible"
            result.probe_notes.append(f"Total unique products: {len(all_products)}")
        elif ng_version:
            result.access_status = "partial"
            result.blocker_type = "angularjs_spa"
            result.blocker_detail = (
                "Angular rendered but no products extracted from DOM. "
                "Category pages may require additional navigation or auth."
            )
        else:
            result.access_status = "blocked"
            result.blocker_type = "angularjs_spa"
            result.blocker_detail = "Angular SPA did not render product content"

        return result


if __name__ == "__main__":
    probe = VictoryProbe()
    res = probe.probe()
    print(f"Status: {res.access_status} | Blocker: {res.blocker_type}")
    print(f"Products: {res.n_products()}")
    for note in res.probe_notes:
        print(f"  {note}")
    for p in res.products[:3]:
        print(f"  - {p.name_he}")
