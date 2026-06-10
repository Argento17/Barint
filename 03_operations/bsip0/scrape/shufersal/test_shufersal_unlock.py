"""
Shufersal TLS-fingerprint unlock test using crawlee's DefaultFingerprintGenerator.

The block: BLOCKED_TLS_FINGERPRINT_FAKE_200
Server fingerprints headless Chromium at the TLS layer (JA3/JA4 hash).
Returns HTTP 200 with static Maintenance1.jpg — no real content.

Fix attempt: crawlee's DefaultFingerprintGenerator injects realistic Chrome
browser fingerprints (navigator.*, screen, WebGL, canvas, TLS JA3) that
match a real desktop Chrome session.

Run from C:\Bari:  python 03_operations/bsip0/scrape/shufersal/test_shufersal_unlock.py
"""
import asyncio
import sys
sys.stdout.reconfigure(encoding="utf-8")
from datetime import timedelta

from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.fingerprint_suite import (
    DefaultFingerprintGenerator,
    HeaderGeneratorOptions,
    ScreenOptions,
)

# Homepage to confirm unlock; product page to confirm nutrition panel
TEST_URL = "https://www.shufersal.co.il/online/he/A7290000066233"  # Tnuva whole milk 3%

BLOCK_SIGNALS = ["Maintenance1.jpg", "s3-eu-west-1.amazonaws.com/www.shufersal.co.il"]
SUCCESS_SIGNALS = ["ערכים תזונתיים", "מרכיבים", "הוסף לסל", "שופרסל", "nutrition", "shufersal"]


async def main() -> None:
    fp_gen = DefaultFingerprintGenerator(
        header_options=HeaderGeneratorOptions(browsers=["chrome"]),
        screen_options=ScreenOptions(min_width=1280, min_height=720),
    )

    crawler = PlaywrightCrawler(
        fingerprint_generator=fp_gen,
        headless=True,
        browser_type="chromium",
        browser_new_context_options={
            "locale": "he-IL",
            "timezone_id": "Asia/Jerusalem",
            "extra_http_headers": {"Accept-Language": "he-IL,he;q=0.9,en-US;q=0.7"},
        },
        navigation_timeout=timedelta(seconds=30),
        max_requests_per_crawl=1,
    )

    @crawler.router.default_handler
    async def handler(context: PlaywrightCrawlingContext) -> None:
        page = context.page
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(4000)
        content = await page.content()
        final_url = page.url

        print(f"\n--- Shufersal unlock test ---")
        print(f"URL loaded: {final_url}")
        print(f"Content length: {len(content):,} chars")

        blocked = any(sig in content for sig in BLOCK_SIGNALS)
        success = any(sig in content for sig in SUCCESS_SIGNALS)

        if blocked:
            print("RESULT: BLOCKED — Maintenance1.jpg fake-200 still firing")
            print("  → fingerprint injection did not bypass TLS filter")
            print("  → next step: add residential proxy")
        elif success:
            print("RESULT: SUCCESS — real Shufersal product page loaded")
            for sig in SUCCESS_SIGNALS:
                if sig in content:
                    print(f"  ✓ found signal: '{sig}'")
        else:
            print("RESULT: UNKNOWN — neither blocked nor confirmed real")
            print(f"  → title: {await page.title()}")
            print(f"  → first 600 chars of content:")
            # Strip HTML tags roughly
            import re
            text = re.sub(r"<[^>]+>", " ", content)
            text = re.sub(r"\s+", " ", text).strip()
            print(f"  {text[:600]}")

    await crawler.run([TEST_URL])
    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
