"""
Scrape approved Victory juice candidates — BSIP0 Victory corpus expansion.

Mirrors scrape_juices_yohananof.py structure, adapted for victoryonline.co.il.
Reads approved_candidates.json from victory_scrape/, opens product modals via
Playwright, captures nutrition / ingredients / allergens HTML per barcode.
Also attempts OFF fallback for products where the modal panel is empty.

Per-product output structure (mirrors yohananof_scrape/<barcode>/):
  discovery.json       — identity record (barcode, name, brand, query, retailer)
  discovery.txt        — text summary for quick review
  nutrition.html       — raw modal HTML (ערכים תזונתיים tab)
  ingredients.html     — raw modal HTML (רכיבים tab)
  allergens.html       — raw modal HTML (מידע אלרגני tab)
  capture_status.json  — per-tab status codes

Top-level artifacts:
  victory_scrape/run_report.json       — full scrape run record
  victory_scrape/bsip0_summary.json    — summary with provenance envelope

Run after discover_juices_victory.py:
    python scrape_juices_victory.py [--headless]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlparse, parse_qs

import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, r"C:\Bari")

from integrations.clients import open_food_facts as off

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "victory_scrape"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RETAILER = "victory"
RETAILER_NAME = "ויקטורי"
BASE_URL = "https://www.victoryonline.co.il"
SEARCH_URL = BASE_URL + "/category?search={query}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean(text) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_approved() -> list[dict]:
    path = OUTPUT_DIR / "approved_candidates.json"
    if not path.exists():
        raise FileNotFoundError(
            f"approved_candidates.json not found: {path}\n"
            "Run discover_juices_victory.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Image helpers (Victory CDN pattern — same as Yohananof)
# ---------------------------------------------------------------------------

def normalize_image_url(raw_url: str | None) -> str | None:
    if not raw_url:
        return None
    first = raw_url.split(" ")[0]
    if "/_next/image" in first and "url=" in first:
        parsed = urlparse(first)
        qs = parse_qs(parsed.query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return first


def save_product_image(product: dict, product_dir: Path) -> dict:
    image_url = normalize_image_url(product.get("image_url_raw"))
    if not image_url:
        return {
            "source_image_url": None,
            "local_image_file": None,
            "image_download_error": "missing_image_url",
        }
    try:
        response = requests.get(image_url, timeout=20)
        response.raise_for_status()
        lower = image_url.lower()
        suffix = ".jpg"
        if ".png" in lower:
            suffix = ".png"
        elif ".webp" in lower:
            suffix = ".webp"
        elif ".jpeg" in lower:
            suffix = ".jpeg"
        image_path = product_dir / f"product_image{suffix}"
        image_path.write_bytes(response.content)
        return {"source_image_url": image_url, "local_image_file": image_path.name}
    except Exception as e:
        return {
            "source_image_url": image_url,
            "local_image_file": None,
            "image_download_error": str(e)[:200],
        }


# ---------------------------------------------------------------------------
# Playwright helpers (ported from 01_acquire_victory.py)
# ---------------------------------------------------------------------------

def dismiss_all_popups(page) -> None:
    """Dismiss Victory's MaxCard modal and cookie/consent dialogs."""
    for selector in [
        'button:has-text("אישור")',
        'button:has-text("מסכים")',
        'button:has-text("הבנתי")',
        '[data-aria-desc="dialog_cookies_accept"]',
        '[role="dialog"] button',
    ]:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=600):
                btn.click(force=True)
                page.wait_for_timeout(700)
        except Exception:
            pass
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            btn = page.get_by_text(text, exact=True).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass


def open_product_modal(page, barcode: str, name: str, query: str) -> bool:
    """
    Navigate to search page, scroll to find product, click to open modal.
    Returns True if product was found and modal opened.
    Victory uses AngularJS — check both src and ng-src for barcode in CDN URL.
    """
    url = SEARCH_URL.format(query=quote(query))
    print(f"  Search page: {url}")
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(8000)   # AngularJS digest needs extra time
    dismiss_all_popups(page)
    page.wait_for_timeout(1000)
    dismiss_all_popups(page)      # second pass: MaxCard sometimes fires after first dismiss

    barcode_locator = page.locator(
        f'img[src*="{barcode}"], img[srcset*="{barcode}"], img[ng-src*="{barcode}"]'
    ).first
    name_locator = page.get_by_text(name, exact=False).first

    for i in range(1, 121):
        if i % 10 == 0:
            print(f"  Searching... attempt {i}/120 | {barcode} | {name[:40]}")

        try:
            if barcode_locator.count() > 0:
                barcode_locator.scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(700)
                barcode_locator.click(force=True)
                page.wait_for_timeout(4500)
                return True
        except Exception:
            pass

        try:
            if name_locator.count() > 0:
                name_locator.scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(700)
                name_locator.click(force=True)
                page.wait_for_timeout(4500)
                return True
        except Exception:
            pass

        page.mouse.wheel(0, 900)
        page.wait_for_timeout(850)

    return False


def capture_current_dialog(page, output_path: Path) -> str:
    try:
        dialog = page.locator('[role="dialog"]').first
        if dialog.count() == 0:
            output_path.write_text("", encoding="utf-8")
            return "dialog_missing"
        html = dialog.inner_html(timeout=5000)
        output_path.write_text(html, encoding="utf-8")
        return "success" if len(html.strip()) >= 50 else "captured_but_nearly_empty"
    except Exception as e:
        output_path.write_text("", encoding="utf-8")
        return f"dialog_capture_failed:{str(e)[:120]}"


def capture_tab(page, tab_name: str, output_path: Path, retries: int = 2) -> str:
    for attempt in range(1, retries + 1):
        try:
            if page.locator('[role="tab"]').count() == 0:
                return capture_current_dialog(page, output_path)
            tab = page.get_by_role("tab", name=tab_name).first
            if tab.count() == 0:
                output_path.write_text("", encoding="utf-8")
                return "tab_missing"
            tab.click(force=True)
            page.wait_for_timeout(2200)
            return capture_current_dialog(page, output_path)
        except PlaywrightTimeoutError:
            if attempt == retries:
                output_path.write_text("", encoding="utf-8")
                return "timeout"
            page.wait_for_timeout(1200)
        except Exception as e:
            if attempt == retries:
                output_path.write_text("", encoding="utf-8")
                return f"failed:{str(e)[:120]}"
            page.wait_for_timeout(1200)
    output_path.write_text("", encoding="utf-8")
    return "unknown_failure"


def close_dialog(page) -> None:
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Per-product scrape
# ---------------------------------------------------------------------------

def scrape_one(page, product: dict) -> dict:
    barcode = clean(product.get("barcode"))
    name = clean(product.get("name"))
    query = clean(product.get("query") or name[:40])

    if not barcode:
        raise RuntimeError(f"Missing barcode for product: {name}")

    product_dir = OUTPUT_DIR / barcode
    product_dir.mkdir(parents=True, exist_ok=True)

    image_info = save_product_image(product, product_dir)

    discovery = {
        "barcode": barcode,
        "name": name,
        "brand": clean(product.get("brand") or product.get("manufacturer") or ""),
        "query": query,
        "subpool": product.get("subpool", "unknown"),
        "captured_at": now_iso(),
        "retailer": RETAILER,
        "image": image_info,
        "image_url_raw": product.get("image_url_raw"),
        "identity_source": product.get("identity_source", "unknown"),
        "provenance": {
            "source": "victory_storefront",
            "source_id": barcode,
            "source_url": SEARCH_URL.format(query=quote(query)),
            "fetched_at": now_iso(),
            "client_version": "juices_victory_v1",
            "verification_status": "candidate",
        },
    }
    save_json(product_dir / "discovery.json", discovery)
    (product_dir / "discovery.txt").write_text(
        "\n".join([
            f"barcode={barcode}",
            f"name={name}",
            f"brand={discovery.get('brand') or ''}",
            f"query={query}",
            f"subpool={discovery.get('subpool') or ''}",
            f"captured_at={discovery['captured_at']}",
            f"retailer={RETAILER}",
            f"image_file={(image_info or {}).get('local_image_file') or ''}",
            f"image_source_url={(image_info or {}).get('source_image_url') or ''}",
        ]),
        encoding="utf-8",
    )

    found = open_product_modal(page, barcode, name, query)
    if not found:
        close_dialog(page)
        capture_status = {
            "ingredients": "not_found",
            "nutrition": "not_found",
            "allergens": "not_found",
        }
        save_json(product_dir / "capture_status.json", capture_status)
        # Write empty HTML files so downstream parsers don't trip on missing files
        for tab_file in ["ingredients.html", "nutrition.html", "allergens.html"]:
            (product_dir / tab_file).write_text("", encoding="utf-8")
        return {
            "barcode": barcode,
            "name": name,
            "status": "not_found",
            "ingredients": "not_found",
            "nutrition": "not_found",
            "allergens": "not_found",
            "provenance": discovery["provenance"],
        }

    capture_status = {
        "ingredients": capture_tab(page, "רכיבים",           product_dir / "ingredients.html"),
        "nutrition":   capture_tab(page, "ערכים תזונתיים",   product_dir / "nutrition.html"),
        "allergens":   capture_tab(page, "מידע אלרגני",      product_dir / "allergens.html"),
    }
    save_json(product_dir / "capture_status.json", capture_status)
    close_dialog(page)

    return {
        "barcode": barcode,
        "name": name,
        "brand": discovery["brand"],
        "query": query,
        "subpool": discovery["subpool"],
        "status": "scraped",
        "ingredients": capture_status["ingredients"],
        "nutrition": capture_status["nutrition"],
        "allergens": capture_status["allergens"],
        "provenance": discovery["provenance"],
    }


# ---------------------------------------------------------------------------
# OFF fallback
# ---------------------------------------------------------------------------

def run_off_fallback(run_report: list[dict]) -> None:
    """
    For scraped products where the nutrition panel is empty/missing,
    attempt to retrieve it from Open Food Facts by barcode.
    """
    nutrition_empty = [
        r for r in run_report
        if r.get("status") == "scraped"
        and r.get("nutrition") in ("tab_missing", "dialog_missing", "not_found",
                                   "captured_but_nearly_empty")
    ]
    print(f"\nOFF fallback: {len(nutrition_empty)} products with empty nutrition panel")

    for r in nutrition_empty:
        try:
            p = off.get_product(r["barcode"])
            r["off_panel"] = {
                "found": p.found,
                "has_panel": p.has_panel,
                "name": p.name,
                "nutriments": p.nutriments if p.found else {},
                "ingredients_text": p.ingredients_text if p.found else "",
            }
            if p.found and p.has_panel:
                r.setdefault("provenance", {})
                r["provenance"]["nutrition_source"] = "off_api"
                r["provenance"]["ingredients_source"] = "off_api"
                print(f"  OFF hit: {r['barcode']} | {r.get('name', '')[:40]}")
            else:
                print(f"  OFF miss: {r['barcode']}")
        except Exception as e:
            r["off_panel"] = {"found": False, "error": str(e)[:100]}
            print(f"  OFF error: {r['barcode']} — {e}")
        time.sleep(0.3)


# ---------------------------------------------------------------------------
# Summary writer
# ---------------------------------------------------------------------------

def write_summary(run_report: list[dict], ts: str) -> None:
    scraped_ok = [r for r in run_report if r.get("status") == "scraped"]
    not_found  = [r for r in run_report if r.get("status") == "not_found"]
    failed     = [r for r in run_report if r.get("status") == "failed"]

    # Nutrition panel coverage
    nutrition_ok = [
        r for r in scraped_ok
        if r.get("nutrition") in ("success", "captured_but_nearly_empty")
        or (r.get("off_panel") or {}).get("has_panel")
    ]

    summary = {
        "schema_version": "bsip0_v1",
        "retailer_id": RETAILER,
        "retailer_name": RETAILER_NAME,
        "category": "juices",
        "run_ts": ts,
        "candidates_total": len(run_report),
        "scraped_ok": len(scraped_ok),
        "not_found": len(not_found),
        "failed": len(failed),
        "nutrition_panel_coverage": len(nutrition_ok),
        "provenance": {
            "source": "victory_storefront",
            "fetched_at": ts,
            "client_version": "juices_victory_v1",
            "verification_status": "candidate",
            "note": "External values remain candidates until promoted by BSIP0/QA pass (EDPG)",
        },
        "products": run_report,
    }
    summary_path = OUTPUT_DIR / f"bsip0_summary_{ts}.json"
    save_json(summary_path, summary)
    print(f"\nBSIP0 summary: {summary_path}")
    return summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(headless: bool = False) -> None:
    approved = load_approved()
    if not approved:
        print("approved_candidates.json is empty — nothing to scrape.")
        return

    print("\n==============================")
    print(f"Victory juice products to scrape: {len(approved)}")
    subpool_counts = {}
    for a in approved:
        sp = a.get("subpool", "unknown")
        subpool_counts[sp] = subpool_counts.get(sp, 0) + 1
    for sp, cnt in sorted(subpool_counts.items()):
        print(f"  {sp}: {cnt}")
    print("==============================\n")

    run_report: list[dict] = []
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1500, "height": 1000},
            locale="he-IL",
            timezone_id="Asia/Jerusalem",
            extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],   # silently deny geolocation
        )
        page = context.new_page()

        for product in approved:
            barcode = clean(product.get("barcode"))
            name = clean(product.get("name"))
            print(f"\nScraping: {barcode} | {name[:60]}")

            try:
                result = scrape_one(page, product)
                run_report.append(result)
                print(f"  Status: {result['status']} | "
                      f"nutrition={result.get('nutrition')} | "
                      f"ingredients={result.get('ingredients')}")
            except Exception as e:
                close_dialog(page)
                run_report.append({
                    "barcode": barcode,
                    "name": name,
                    "status": "failed",
                    "error": str(e)[:300],
                    "provenance": {
                        "source": "victory_storefront",
                        "source_id": barcode,
                        "fetched_at": now_iso(),
                        "client_version": "juices_victory_v1",
                        "verification_status": "candidate",
                    },
                })
                print(f"  FAILED: {e}")

            # Checkpoint after each product
            save_json(OUTPUT_DIR / "run_report.json", run_report)

        context.close()
        browser.close()

    # OFF fallback for empty-panel products
    run_off_fallback(run_report)

    # Final checkpoint
    save_json(OUTPUT_DIR / "run_report.json", run_report)

    # Summary
    write_summary(run_report, ts)

    print("\n==============================")
    print(f"Scrape complete.")
    print(f"  Attempted:      {len(run_report)}")
    print(f"  Scraped OK:     {sum(1 for r in run_report if r.get('status') == 'scraped')}")
    print(f"  Not found:      {sum(1 for r in run_report if r.get('status') == 'not_found')}")
    print(f"  Failed:         {sum(1 for r in run_report if r.get('status') == 'failed')}")
    print(f"Run report:  {OUTPUT_DIR / 'run_report.json'}")
    print("==============================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Victory juice products")
    parser.add_argument("--headless", action="store_true", help="Run browser headless")
    args = parser.parse_args()
    main(headless=args.headless)
