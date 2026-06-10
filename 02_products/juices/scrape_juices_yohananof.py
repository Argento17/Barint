"""
Scrape approved juice candidates from yochananof.co.il — TASK-214 nutrition source fix.

Adapts 03_operations/bsip0/scrape/yohananof/03_scrape_yohananof.py for the
juices category. Reads approved_candidates.json from yohananof_scrape/,
opens product modals, captures nutrition / ingredients / allergens HTML per barcode.

Run after discover_juices_yohananof.py + auto_approve_juices.py:
    python scrape_juices_yohananof.py
"""
from pathlib import Path
from urllib.parse import quote, unquote, urlparse, parse_qs
from datetime import datetime
import json
import re
import requests

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "yohananof_scrape"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RETAILER = "yohananof"


def clean(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def save_json(path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_approved():
    path = OUTPUT_DIR / "approved_candidates.json"

    if not path.exists():
        raise FileNotFoundError(
            f"approved_candidates.json not found:\n{path}\n\n"
            "Run discover_juices_yohananof.py first, then run the auto-approve step."
        )

    return json.loads(path.read_text(encoding="utf-8"))


def close_cookie_popup(page):
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            button = page.get_by_text(text, exact=False).first
            if button.is_visible(timeout=800):
                button.click(force=True)
                page.wait_for_timeout(800)
                return
        except Exception:
            pass


def normalize_image_url(raw_url):
    if not raw_url:
        return None

    first = raw_url.split(" ")[0]

    if "/_next/image" in first and "url=" in first:
        parsed = urlparse(first)
        qs = parse_qs(parsed.query)

        if "url" in qs:
            return unquote(qs["url"][0])

    return first


def save_product_image(product, product_dir):
    image_url = normalize_image_url(product.get("image_url_raw"))

    if not image_url:
        return {
            "source_image_url": None,
            "local_image_file": None,
            "image_download_error": "missing_image_url"
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

        return {
            "source_image_url": image_url,
            "local_image_file": image_path.name
        }

    except Exception as e:
        return {
            "source_image_url": image_url,
            "local_image_file": None,
            "image_download_error": str(e)[:200]
        }


def open_product_modal(page, product):
    barcode = clean(product.get("barcode"))
    query = clean(product.get("query"))
    name = clean(product.get("name"))

    if not barcode:
        raise RuntimeError(f"Missing barcode for approved product: {name}")

    url = f"https://yochananof.co.il/category?search={quote(query)}"

    print(f"Opening search page: {query}")
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3500)
    close_cookie_popup(page)

    barcode_locator = page.locator(
        f'img[src*="{barcode}"], img[srcset*="{barcode}"]'
    ).first

    name_locator = page.get_by_text(name, exact=False).first

    for i in range(1, 121):
        if i % 10 == 0:
            print(f"Still looking for product... attempt {i}/120 | {barcode} | {name}")

        try:
            if barcode_locator.count() > 0:
                print("Found by barcode image.")
                barcode_locator.scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(700)
                barcode_locator.click(force=True)
                page.wait_for_timeout(4500)
                return
        except Exception:
            pass

        try:
            if name_locator.count() > 0:
                print("Found by visible product name.")
                name_locator.scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(700)
                name_locator.click(force=True)
                page.wait_for_timeout(4500)
                return
        except Exception:
            pass

        page.mouse.wheel(0, 900)
        page.wait_for_timeout(850)

    raise RuntimeError(
        f"Could not find product after scrolling:\n"
        f"barcode={barcode}\n"
        f"name={name}\n"
        f"query={query}"
    )


def capture_current_dialog(page, output_path):
    try:
        dialog = page.locator('[role="dialog"]').first

        if dialog.count() == 0:
            output_path.write_text("", encoding="utf-8")
            return "dialog_missing"

        html = dialog.inner_html(timeout=5000)

        output_path.write_text(html, encoding="utf-8")

        if len(html.strip()) >= 50:
            return "success"

        return "captured_but_nearly_empty"

    except Exception as e:
        output_path.write_text("", encoding="utf-8")

        return f"dialog_capture_failed:{str(e)[:120]}"


def capture_tab(page, tab_name, output_path, retries=2):

    for attempt in range(1, retries + 1):

        try:

            if page.locator('[role="tab"]').count() == 0:
                return capture_current_dialog(page, output_path)

            tab = page.get_by_role(
                "tab",
                name=tab_name
            ).first

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


def close_dialog(page):
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)
    except Exception:
        pass


def scrape_one(page, product):

    barcode = clean(product.get("barcode"))
    name = clean(product.get("name"))

    product_dir = OUTPUT_DIR / barcode

    product_dir.mkdir(parents=True, exist_ok=True)

    image_info = save_product_image(product, product_dir)

    discovery = {
        "barcode": barcode,
        "name": name,
        "brand": clean(product.get("brand")),
        "query": clean(product.get("query")),
        "captured_at": now_iso(),
        "retailer": RETAILER,
        "image": image_info,
        "image_url_raw": product.get("image_url_raw"),
        "card_text": product.get("card_text"),
        "image_alt": product.get("image_alt"),
    }

    save_json(product_dir / "discovery.json", discovery)

    (product_dir / "discovery.txt").write_text(
        "\n".join([
            f"barcode={barcode}",
            f"name={name}",
            f"brand={discovery.get('brand') or ''}",
            f"query={discovery.get('query') or ''}",
            f"captured_at={discovery.get('captured_at')}",
            f"image_file={(image_info or {}).get('local_image_file') or ''}",
            f"image_source_url={(image_info or {}).get('source_image_url') or ''}",
        ]),
        encoding="utf-8"
    )

    open_product_modal(page, product)

    status = {
        "ingredients": capture_tab(
            page,
            "רכיבים",
            product_dir / "ingredients.html"
        ),

        "nutrition": capture_tab(
            page,
            "ערכים תזונתיים",
            product_dir / "nutrition.html"
        ),

        "allergens": capture_tab(
            page,
            "מידע אלרגני",
            product_dir / "allergens.html"
        ),
    }

    save_json(product_dir / "capture_status.json", status)

    close_dialog(page)

    return {
        "barcode": barcode,
        "name": name,
        "brand": discovery.get("brand"),
        "query": discovery.get("query"),
        "status": "scraped",
        "ingredients": status["ingredients"],
        "nutrition": status["nutrition"],
        "allergens": status["allergens"],
    }


def main():

    approved = load_approved()

    if not approved:
        print("approved_candidates.json is empty.")
        return

    print("\n==============================")
    print(f"Approved juice products to scrape: {len(approved)}")
    print("==============================")

    run_report = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1500, "height": 1000}
        )

        for product in approved:

            barcode = clean(product.get("barcode"))
            name = clean(product.get("name"))

            print(f"\nScraping: {barcode} | {name}")

            try:

                result = scrape_one(page, product)

                run_report.append(result)

                print(f"Saved folder: {OUTPUT_DIR / barcode}")

                print(
                    f"Capture status: "
                    f"{{'ingredients': '{result['ingredients']}', "
                    f"'nutrition': '{result['nutrition']}', "
                    f"'allergens': '{result['allergens']}'}}"
                )

            except Exception as e:

                close_dialog(page)

                run_report.append({
                    "barcode": barcode,
                    "name": name,
                    "query": clean(product.get("query")),
                    "status": "failed",
                    "error": str(e)[:300],
                })

                print(f"FAILED: {barcode} | {name}")
                print(str(e)[:300])

            save_json(
                OUTPUT_DIR / "run_report.json",
                run_report
            )

        browser.close()

    save_json(
        OUTPUT_DIR / "run_report.json",
        run_report
    )

    print("\n==============================")
    print(f"Scrape attempts: {len(run_report)}")
    ok = sum(1 for r in run_report if r.get("status") == "scraped")
    print(f"Successful: {ok}")
    print(f"Saved: {OUTPUT_DIR / 'run_report.json'}")
    print("==============================")


if __name__ == "__main__":
    main()
