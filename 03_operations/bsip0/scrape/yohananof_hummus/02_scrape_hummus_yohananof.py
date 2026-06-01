"""
Yohananof BSIP0 scraper — Hummus and Savory Dips.

Reads approved candidates from candidate_review.csv and opens each product
on the Yohananof website to capture the ingredient, nutrition, and allergen tabs.

Usage:
    cd C:\\Bari\\03_operations\\bsip0\\scrape\\yohananof_hummus
    python 02_scrape_hummus_yohananof.py

Prerequisites:
    playwright install chromium
    01_discover_hummus_yohananof.py has run.
    candidate_review.csv exists.
    approved_for_scrape is set to YES for net-new products.

Output:
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\yohananof\\{barcode}\\discovery.json
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\yohananof\\{barcode}\\ingredients.html
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\yohananof\\{barcode}\\nutrition.html
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\yohananof\\{barcode}\\allergens.html
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\yohananof\\{barcode}\\capture_status.json
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\yohananof\\run_report.json

Next:
    Run 03_audit_bsip0_hummus.py to check BSIP0 gate criteria.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, unquote, urlparse, parse_qs

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ──────────────────────────────────────────────────────────────────────
REVIEW_CSV = Path(r"C:\Bari\02_products\hummus\observations_bsip0\yohananof\candidate_review.csv")
OUT_DIR    = Path(r"C:\Bari\02_products\hummus\observations_bsip0\yohananof")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ── Utilities ──────────────────────────────────────────────────────────────────

def clean(text) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def repair_barcode(row: dict) -> str:
    """Recover a barcode from row fields if the barcode cell was corrupted (e.g. scientific notation)."""
    barcode = clean(row.get("barcode", ""))
    if barcode and "E+" not in barcode.upper() and "." not in barcode and len(barcode) >= 8:
        return barcode
    combined = " ".join([
        row.get("image_url_raw", ""),
        row.get("card_text", ""),
        row.get("image_alt", ""),
    ])
    match = re.search(r"(729\d{10}|\d{13}|\d{12})", combined)
    return match.group(1) if match else ""


def normalize_image_url(raw_url: str) -> str | None:
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
    raw_url = product.get("image_url_raw", "")
    image_url = normalize_image_url(raw_url)
    if not image_url:
        return {"source_image_url": None, "local_image_file": None, "image_download_error": "missing_url"}
    try:
        response = requests.get(image_url, timeout=20)
        response.raise_for_status()
        lower = image_url.lower()
        suffix = ".jpg"
        if ".png" in lower:
            suffix = ".png"
        elif ".webp" in lower:
            suffix = ".webp"
        image_path = product_dir / f"product_image{suffix}"
        image_path.write_bytes(response.content)
        return {"source_image_url": image_url, "local_image_file": image_path.name}
    except Exception as e:
        return {"source_image_url": image_url, "local_image_file": None, "image_download_error": str(e)[:200]}


# ── Playwright helpers ─────────────────────────────────────────────────────────

def close_cookie_popup(page) -> None:
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            button = page.get_by_text(text, exact=False).first
            if button.is_visible(timeout=800):
                button.click(force=True)
                page.wait_for_timeout(800)
                return
        except Exception:
            pass


def close_dialog(page) -> None:
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)
    except Exception:
        pass


def open_product_modal(page, product: dict) -> None:
    barcode = clean(product.get("barcode"))
    query   = clean(product.get("query"))
    name    = clean(product.get("name"))

    if not barcode:
        raise RuntimeError(f"Missing barcode for product: {name!r}")

    url = f"https://yochananof.co.il/category?search={quote(query)}"
    print(f"  Search URL: {url}")
    page.goto(url, wait_until="networkidle", timeout=60_000)
    page.wait_for_timeout(3_500)
    close_cookie_popup(page)

    barcode_locator = page.locator(f'img[src*="{barcode}"], img[srcset*="{barcode}"]').first
    name_locator    = page.get_by_text(name, exact=False).first

    for i in range(1, 121):
        if i % 20 == 0:
            print(f"  Still searching... attempt {i}/120 | {barcode}")
        try:
            if barcode_locator.count() > 0:
                barcode_locator.scroll_into_view_if_needed(timeout=5_000)
                page.wait_for_timeout(700)
                barcode_locator.click(force=True)
                page.wait_for_timeout(4_500)
                return
        except Exception:
            pass
        try:
            if name_locator.count() > 0:
                name_locator.scroll_into_view_if_needed(timeout=5_000)
                page.wait_for_timeout(700)
                name_locator.click(force=True)
                page.wait_for_timeout(4_500)
                return
        except Exception:
            pass
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(850)

    raise RuntimeError(f"Product not found after 120 scroll attempts: {barcode} | {name}")


def capture_current_dialog(page, output_path: Path) -> str:
    try:
        dialog = page.locator('[role="dialog"]').first
        if dialog.count() == 0:
            output_path.write_text("", encoding="utf-8")
            return "dialog_missing"
        html = dialog.inner_html(timeout=5_000)
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
            page.wait_for_timeout(2_200)
            return capture_current_dialog(page, output_path)
        except PlaywrightTimeoutError:
            if attempt == retries:
                output_path.write_text("", encoding="utf-8")
                return "timeout"
            page.wait_for_timeout(1_200)
        except Exception as e:
            if attempt == retries:
                output_path.write_text("", encoding="utf-8")
                return f"failed:{str(e)[:120]}"
            page.wait_for_timeout(1_200)
    output_path.write_text("", encoding="utf-8")
    return "unknown_failure"


# ── Scrape one product ─────────────────────────────────────────────────────────

def scrape_one(page, product: dict) -> dict:
    barcode     = clean(product.get("barcode"))
    name        = clean(product.get("name"))
    product_dir = OUT_DIR / barcode
    product_dir.mkdir(parents=True, exist_ok=True)

    image_info = save_product_image(product, product_dir)

    discovery = {
        "barcode":       barcode,
        "name":          name,
        "query":         clean(product.get("query")),
        "captured_at":   now_iso(),
        "retailer":      "yohananof",
        "image":         image_info,
        "image_url_raw": product.get("image_url_raw"),
        "card_text":     product.get("card_text"),
        "image_alt":     product.get("image_alt"),
    }
    save_json(product_dir / "discovery.json", discovery)

    open_product_modal(page, product)

    capture_status = {
        "ingredients": capture_tab(page, "רכיבים",          product_dir / "ingredients.html"),
        "nutrition":   capture_tab(page, "ערכים תזונתיים",  product_dir / "nutrition.html"),
        "allergens":   capture_tab(page, "מידע אלרגני",     product_dir / "allergens.html"),
    }
    save_json(product_dir / "capture_status.json", capture_status)
    close_dialog(page)

    return {
        "barcode": barcode,
        "name":    name,
        "status":  "scraped",
        **capture_status,
    }


# ── Load approved candidates ───────────────────────────────────────────────────

def load_approved() -> list[dict]:
    if not REVIEW_CSV.exists():
        print(f"ERROR: candidate_review.csv not found at {REVIEW_CSV}")
        print("Run 01_discover_hummus_yohananof.py first.")
        sys.exit(1)

    approved = []
    skipped  = []

    with REVIEW_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            flag = clean(row.get("approved_for_scrape", "")).upper()
            if flag != "YES":
                continue
            barcode = repair_barcode(row)
            name    = clean(row.get("name", ""))
            if not barcode:
                skipped.append(name)
                print(f"  SKIP (no barcode): {name}")
                continue
            approved.append({
                "barcode":         barcode,
                "name":            name,
                "query":           clean(row.get("query", "")),
                "card_text":       clean(row.get("card_text", "")),
                "image_alt":       clean(row.get("image_alt", "")),
                "image_url_raw":   clean(row.get("image_url_raw", "")),
                "decision_status": clean(row.get("suggested_decision", "")),
            })

    print(f"Approved candidates: {len(approved)}")
    if skipped:
        print(f"Skipped (no barcode): {len(skipped)}")
    return approved


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    approved = load_approved()
    if not approved:
        print("No approved candidates. Set approved_for_scrape = YES in candidate_review.csv")
        sys.exit(1)

    print(f"\nScraping {len(approved)} approved hummus products from Yohananof\n")
    run_report: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page(viewport={"width": 1500, "height": 1000})

        for i, product in enumerate(approved, 1):
            barcode = clean(product.get("barcode"))
            name    = clean(product.get("name"))
            print(f"\n[{i}/{len(approved)}] {barcode} | {name[:60]}")

            try:
                result = scrape_one(page, product)
                run_report.append(result)
                print(
                    f"  OK — ingredients={result['ingredients']} "
                    f"nutrition={result['nutrition']} "
                    f"allergens={result['allergens']}"
                )
            except Exception as e:
                close_dialog(page)
                run_report.append({
                    "barcode": barcode,
                    "name":    name,
                    "status":  "failed",
                    "error":   str(e)[:300],
                })
                print(f"  FAILED: {e}")

            # Save progress after each product so a mid-run abort is recoverable
            save_json(OUT_DIR / "run_report.json", run_report)

        browser.close()

    save_json(OUT_DIR / "run_report.json", run_report)

    ok   = sum(1 for r in run_report if r.get("status") == "scraped")
    fail = sum(1 for r in run_report if r.get("status") == "failed")
    print(f"\n{'='*50}")
    print(f"Yohananof hummus scrape complete")
    print(f"  Scraped : {ok}")
    print(f"  Failed  : {fail}")
    print(f"  Total   : {len(run_report)}")
    print(f"\nNext: python 03_audit_bsip0_hummus.py (from shufersal_hummus dir)")
    print(f"  (or re-attempt failed products individually)")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
