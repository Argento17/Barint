"""
Hazi Hinam Angular SPA exploration using raw Playwright.

Goal: find the correct category URL for juices, confirm product cards load
via JS, open a product modal, and check for nutrition tab.

shop.hazi-hinam.co.il is CLEAR (no WAF). Angular SPA on own CDN
(cdn.hazi-hinam.co.il). Category URL: /catalog/{id}/{slug}.
Search does NOT work via static URL — Angular client-side routing only.

Run from C:\Bari:  python 03_operations/bsip0/scrape/hazi_hinam/test_hazi_hinam_explore.py
"""
import asyncio
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

HOMEPAGE = "https://shop.hazi-hinam.co.il/"
# Dairy category — confirmed in navigation links (cat 78)
DAIRY_CATALOG_URL = "https://shop.hazi-hinam.co.il/catalog/78/מוצרי-חלב-וביצים"
# Cheese deli — confirmed in navigation links (cat 41)
CHEESE_CATALOG_URL = "https://shop.hazi-hinam.co.il/catalog/41/מעדניית-גבינות"

COOKIE_SELECTORS = [
    'button:has-text("סגור")',
    'button:has-text("אישור")',
    'button:has-text("הבנתי")',
    '[class*="cookie"] button',
    '[class*="consent"] button',
]


async def dismiss_popups(page) -> None:
    for sel in COOKIE_SELECTORS:
        try:
            btn = page.locator(sel).first
            if await btn.is_visible(timeout=800):
                await btn.click(force=True)
                await page.wait_for_timeout(500)
        except Exception:
            pass


async def main() -> None:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1500, "height": 900},
            locale="he-IL",
            timezone_id="Asia/Jerusalem",
            extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = await context.new_page()

        # --- Step 1: load homepage, dismiss any popups ---
        print("Step 1: Loading homepage...")
        await page.goto(HOMEPAGE, wait_until="domcontentloaded", timeout=30_000)
        await page.wait_for_timeout(4000)
        await dismiss_popups(page)
        title = await page.title()
        print(f"  Title: {title}")

        # --- Step 2: navigate to dairy category (cat 78) ---
        print(f"\nStep 2: Loading dairy catalog (cat 78)...")
        await page.goto(DAIRY_CATALOG_URL, wait_until="domcontentloaded", timeout=30_000)
        await page.wait_for_timeout(5000)
        await dismiss_popups(page)
        content = await page.content()
        print(f"  Final URL: {page.url}")
        print(f"  Content length: {len(content):,}")

        product_card_selectors = [
            "[class*='product-item']",
            "[class*='product-card']",
            "[class*='product_card']",
            "[class*='catalog-item']",
            "app-product-card",
        ]
        found_sel = None
        for sel in product_card_selectors:
            count = await page.locator(sel).count()
            if count > 0:
                print(f"  Found {count} product cards: {sel}")
                found_sel = sel
                break
        else:
            print("  No product cards found")

        # Inspect first few product card links/hrefs to understand URL pattern
        if found_sel:
            print("\n  Inspecting product card links...")
            cards = page.locator(found_sel)
            for i in range(min(3, await cards.count())):
                card = cards.nth(i)
                # Get href if it's an anchor, or inner anchor
                href = await card.get_attribute("href")
                if not href:
                    inner_link = card.locator("a").first
                    if await inner_link.count() > 0:
                        href = await inner_link.get_attribute("href")
                name_text = (await card.inner_text()).strip()[:80].replace("\n", " ")
                print(f"  card[{i}] href={href}  text={name_text!r}")

            # Navigate to the first product's URL directly
            first_card = cards.first
            href = await first_card.get_attribute("href")
            if not href:
                inner_link = first_card.locator("a").first
                if await inner_link.count() > 0:
                    href = await inner_link.get_attribute("href")
            # Cards have no href — click triggers Angular JS navigation
            print("\n  Clicking first product card (JS navigation)...")
            url_before = page.url
            await cards.first.click()
            await page.wait_for_timeout(3000)
            url_after = page.url
            print(f"  URL before: {url_before}")
            print(f"  URL after:  {url_after}")
            prod_content = await page.content()
            print(f"  Content after click: {len(prod_content):,} chars")
            nutrition_signals = ["ערכים תזונתיים", "רכיבים", "מידע אלרגני"]
            found_nutrition = [sig for sig in nutrition_signals if sig in prod_content]
            if found_nutrition:
                for sig in found_nutrition:
                    print(f"  Found nutrition signal: '{sig}'")
            else:
                print("  No nutrition signals found after click")
                # Dump overlay text if visible
                overlay = page.locator("[class*='overlay']").first
                try:
                    if await overlay.is_visible(timeout=1000):
                        import re
                        overlay_text = re.sub(r"<[^>]+>", " ", await overlay.inner_html())
                        overlay_text = re.sub(r"\s+", " ", overlay_text).strip()
                        print(f"  Overlay text: {overlay_text[:400]}")
                except Exception:
                    pass

        # --- Step 3: get full category tree ---
        print("\nStep 3: Full category tree from navigation...")
        nav_links = await page.locator("a[href*='/catalog/']").all()
        catalog_links = []
        for link in nav_links[:60]:
            href = await link.get_attribute("href")
            text = (await link.inner_text()).strip()
            if href and text and len(text) > 1:
                catalog_links.append((href, text))
        seen = set()
        print(f"  Found {len(catalog_links)} catalog links:")
        for href, text in catalog_links:
            key = href
            if key not in seen:
                seen.add(key)
                print(f"    {href}  →  {text}")

        await context.close()
        await browser.close()
        print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
