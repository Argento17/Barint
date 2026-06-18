"""
shufersal_stealth_retry.py — Bounded Shufersal stealth retry with fingerprint
randomization.

Runs Playwright with crawlee-style browser fingerprint randomization (NO proxies),
tries up to 5 Shufersal pages, and reports whether the captcha clears.

If it fails, Shufersal continuous crawl waits for a residential-proxy decision
(owner) or the owner's relocation to Israel (~Aug 2026).

Requirements: playwright (pip install playwright && playwright install chromium)
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUTPUT_DIR = Path(__file__).resolve().parent

# URLs to probe (mirroring the yogurt scraper's entry points)
PROBE_URLS = [
    ("search_yogurt", "https://www.shufersal.co.il/online/he/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98"),
    ("search_greek", "https://www.shufersal.co.il/online/he/search?q=%D7%99%D7%95%D7%92%D7%95%D7%A8%D7%98+%D7%99%D7%95%D7%95%D7%A0%D7%99"),
    ("category_A4001", "https://www.shufersal.co.il/online/he/c/A4001"),
    ("product_page", "https://www.shufersal.co.il/online/he/A7290008316037"),
    ("search_activia", "https://www.shufersal.co.il/online/he/search?q=%D7%90%D7%A7%D7%98%D7%99%D7%91%D7%99%D7%94"),
]

CAPTCHA_SIGNALS = [
    "recaptcha", "g-recaptcha", "hcaptcha", "cf-challenge",
    "captcha", "challenge-platform", "_cf_chl_opt",
    "verify you are human", "verify your identity",
]

MAINTENANCE_SIGNALS = ["maintenance", "\u05d0\u05ea\u05e8 \u05d1\u05ea\u05d7\u05d6\u05d5\u05e7\u05d4", "\u05d1\u05ea\u05d7\u05d6\u05d5\u05e7\u05d4"]


def _detect_captcha(page_text: str, page_source: str) -> list[str]:
    """Detect captcha/challenge signals in page text and HTML source."""
    signals_found: list[str] = []
    combined = page_text + " " + page_source
    low = combined.lower()
    for signal in CAPTCHA_SIGNALS:
        if signal in low:
            signals_found.append(signal)
    return signals_found


def _detect_maintenance(page_text: str) -> bool:
    low = page_text.lower()
    return any(s in low for s in MAINTENANCE_SIGNALS)


def _get_page_text(page) -> str:
    """Get visible text content from page."""
    try:
        return page.inner_text() or ""
    except Exception:
        try:
            return page.text_content() or ""
        except Exception:
            return ""


def _randomize_fingerprint(context) -> None:
    """Apply crawlee-style fingerprint randomization via CDP."""
    try:
        import random
        width = random.choice([1920, 1366, 1536, 1440, 1680])
        height = random.choice([1080, 768, 864, 900, 1050])
        context.add_init_script(f"""
        (() => {{
            Object.defineProperty(navigator, 'webdriver', {{ get: () => false }});
            Object.defineProperty(navigator, 'plugins', {{ get: () => [1, 2, 3, 4, 5] }});
            Object.defineProperty(navigator, 'languages', {{ get: () => ['he-IL', 'he', 'en-US', 'en'] }});
            Object.defineProperty(navigator, 'hardwareConcurrency', {{ get: () => {random.choice([4, 8, 12, 16])} }});
            Object.defineProperty(navigator, 'deviceMemory', {{ get: () => {random.choice([4, 8])} }});
            window.screen = {{ ...window.screen, width: {width}, height: {height} }};
        }})();
        """)
    except Exception as e:
        print(f"  [fingerprint warn] {e}", flush=True)


def run_stealth_probe() -> dict[str, Any]:
    """Run stealth probe: try up to 5 pages with fingerprint randomization."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "status": "SKIPPED",
            "reason": "playwright not installed. Install: pip install playwright && playwright install chromium",
            "results": [],
            "captcha_clears": None,
            "blocker": "missing_dependency",
        }

    results: list[dict] = []
    captcha_on_first: bool | None = None
    captcha_cleared: bool | None = None
    notes: list[str] = []

    def log(msg: str):
        print(msg, flush=True)
        notes.append(msg)

    log(f"=== Shufersal Stealth Retry ({datetime.now(timezone.utc).isoformat()}) ===")
    log("Probing up to 5 pages with Playwright + fingerprint randomization (NO proxies)")

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-features=IsolateOrigins,site-per-process",
                ],
            )
            context = browser.new_context(
                locale="he-IL",
                timezone_id="Asia/Jerusalem",
                viewport={"width": 1920, "height": 1080},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
            )

            # Randomize fingerprint
            _randomize_fingerprint(context)

            for label, url in PROBE_URLS[:5]:
                log(f"\n--- {label} ---")
                log(f"URL: {url}")

                page = context.new_page()
                probe_result: dict[str, Any] = {
                    "label": label,
                    "url": url,
                    "status": "unknown",
                    "captcha_signals": [],
                    "maintenance": False,
                    "product_cards": 0,
                    "text_length": 0,
                    "error": None,
                    "page_title": "",
                }

                try:
                    resp = page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    time.sleep(2.0)

                    status = resp.status if resp else 0
                    text = _get_page_text(page)[:5000]
                    source = page.content()[:20000]
                    title = page.title()

                    probe_result["status"] = status
                    probe_result["page_title"] = title
                    probe_result["text_length"] = len(text)

                    # Detect captcha
                    captcha = _detect_captcha(text, source)
                    probe_result["captcha_signals"] = captcha

                    # Detect maintenance
                    maint = _detect_maintenance(text)
                    probe_result["maintenance"] = maint

                    # Count product cards (li[data-product-name])
                    try:
                        cards = page.locator("li[data-product-name]").count()
                        probe_result["product_cards"] = cards
                    except Exception:
                        pass

                    if captcha:
                        log(f"  CAPTCHA DETECTED: {captcha}")
                        if captcha_on_first is None:
                            captcha_on_first = True
                    else:
                        log(f"  NO CAPTCHA (page loads OK)")
                        if captcha_on_first is None:
                            captcha_on_first = False
                        captcha_cleared = True

                    if maint:
                        log(f"  MAINTENANCE PAGE DETECTED")

                    log(f"  Status: {status}, Title: {title[:60]}")
                    log(f"  Text: {len(text)} chars, Cards: {probe_result['product_cards']}")

                except Exception as e:
                    probe_result["status"] = "error"
                    probe_result["error"] = str(e)[:200]
                    log(f"  ERROR: {e}")

                finally:
                    page.close()

                results.append(probe_result)
                time.sleep(2.0)

            browser.close()

            # Determine overall verdict
            any_clear = any(
                r and not r.get("captcha_signals") and r.get("status") == 200
                for r in results
            )
            all_blocked = all(
                r and r.get("captcha_signals") for r in results
            )

            if any_clear:
                captcha_cleared = True
                verdict = "PARTIALLY_CLEARED"
                summary = f"Captcha cleared on {sum(1 for r in results if r and not r.get('captcha_signals'))}/{len(results)} pages"
            elif all_blocked:
                captcha_cleared = False
                verdict = "BLOCKED"
                summary = "All pages returned captcha — Shufersal remains blocked"
            else:
                captcha_cleared = None
                verdict = "INCONCLUSIVE"
                summary = "Mixed results — some pages may have loaded"

            log(f"\n=== VERDICT: {verdict} ===")
            log(summary)

            report = {
                "run_ts": datetime.now(timezone.utc).isoformat(),
                "browser": "chromium",
                "fingerprint_randomization": True,
                "proxy": "none",
                "max_pages": len(PROBE_URLS),
                "captcha_on_first": captcha_on_first,
                "captcha_cleared": captcha_cleared,
                "verdict": verdict,
                "summary": summary,
                "results": results,
                "notes": notes,
            }

            # Write report
            report_path = OUTPUT_DIR / "shufersal_stealth_report.json"
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            log(f"\nReport: {report_path}")

            return report

    except Exception as e:
        error_report = {
            "run_ts": datetime.now(timezone.utc).isoformat(),
            "status": "ERROR",
            "error": str(e)[:500],
            "notes": notes,
            "bloker": "runtime_error",
        }
        report_path = OUTPUT_DIR / "shufersal_stealth_report.json"
        report_path.write_text(json.dumps(error_report, ensure_ascii=False, indent=2), encoding="utf-8")
        return error_report


def main():
    report = run_stealth_probe()
    print(f"\n{'='*60}")
    print(f"Shufersal Stealth Retry: {report.get('verdict', 'ERROR')}")
    print(f"{'='*60}")
    if report.get("captcha_cleared") is True:
        print("Captcha CLEARED on at least one page — Shufersal crawl may be possible.")
        print("Recommendation: Attempt full crawl with same fingerprint config.")
    elif report.get("captcha_cleared") is False:
        print("Captcha NOT cleared on any page — Shufersal remains blocked.")
        print("Next step: Wait for residential-proxy decision (owner) or relocation (~Aug 2026).")
    elif report.get("status") == "SKIPPED":
        print(f"Skipped: {report.get('reason', 'unknown')}")
    else:
        print("Inconclusive. See full report for details.")


if __name__ == "__main__":
    main()
