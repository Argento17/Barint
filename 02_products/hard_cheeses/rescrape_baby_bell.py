"""
Targeted re-scrape of Baby Bell (3073781199918) from yochananof.co.il.
Searches for the product by barcode in image src, clicks the correct card,
then captures ingredients + nutrition tabs.

Run: python rescrape_baby_bell.py
"""
from pathlib import Path
from urllib.parse import quote
from datetime import datetime
import json, re, sys

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BARCODE = "3073781199918"
PRODUCT_NAME = "גבינה חצי קשה 24% בייבי בל 5*20 גרם"
SEARCH_QUERY = "בייבי בל"

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "yohananof_scrape" / BARCODE
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RESULT_PATH = BASE_DIR / "yohananof_scrape" / "rescrape_baby_bell_result.json"


def clean(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


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


def capture_dialog_html(page):
    try:
        dialog = page.locator('[role="dialog"]').first
        if dialog.count() == 0:
            return "", "dialog_missing"
        html = dialog.inner_html(timeout=8000)
        if len(html.strip()) >= 50:
            return html, "success"
        return html, "captured_but_nearly_empty"
    except Exception as e:
        return "", f"dialog_capture_failed:{str(e)[:120]}"


def click_tab_and_capture(page, tab_name, output_path):
    for attempt in range(1, 3):
        try:
            tabs = page.locator('[role="tab"]')
            if tabs.count() == 0:
                html, status = capture_dialog_html(page)
                output_path.write_text(html, encoding="utf-8")
                return status
            tab = page.get_by_role("tab", name=tab_name).first
            if tab.count() == 0:
                output_path.write_text("", encoding="utf-8")
                return "tab_missing"
            tab.click(force=True)
            page.wait_for_timeout(2500)
            html, status = capture_dialog_html(page)
            output_path.write_text(html, encoding="utf-8")
            return status
        except PlaywrightTimeoutError:
            if attempt == 2:
                output_path.write_text("", encoding="utf-8")
                return "timeout"
            page.wait_for_timeout(1500)
        except Exception as e:
            if attempt == 2:
                output_path.write_text("", encoding="utf-8")
                return f"failed:{str(e)[:120]}"
            page.wait_for_timeout(1500)
    output_path.write_text("", encoding="utf-8")
    return "unknown_failure"


def main():
    result = {
        "barcode": BARCODE,
        "name": PRODUCT_NAME,
        "scraped_at": now_iso(),
        "status": "failed",
        "ingredients_status": None,
        "nutrition_status": None,
        "allergens_status": None,
        "error": None,
        "found_by": None,
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1000})

        try:
            url = f"https://yochananof.co.il/category?search={quote(SEARCH_QUERY)}"
            print(f"Loading: {url}")
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(3500)
            close_cookie_popup(page)

            # Strategy 1: find by barcode in image src — most reliable
            found = False
            for attempt in range(1, 121):
                if attempt % 10 == 0:
                    print(f"Scrolling... attempt {attempt}/120")

                # Barcode in image src
                bc_locator = page.locator(
                    f'img[src*="{BARCODE}"], img[srcset*="{BARCODE}"]'
                ).first
                if bc_locator.count() > 0:
                    print(f"Found product by barcode in image src (attempt {attempt})")
                    bc_locator.scroll_into_view_if_needed(timeout=5000)
                    page.wait_for_timeout(700)
                    bc_locator.click(force=True)
                    page.wait_for_timeout(4500)
                    found = True
                    result["found_by"] = "barcode_in_image_src"
                    break

                page.mouse.wheel(0, 900)
                page.wait_for_timeout(850)

            if not found:
                raise RuntimeError(
                    f"Could not find product by barcode image src after 120 scroll attempts.\n"
                    f"barcode={BARCODE}, search={SEARCH_QUERY}"
                )

            # Verify dialog opened — check it's NOT the Kashkaval product
            dialog_html, _ = capture_dialog_html(page)
            if "2370284" in dialog_html or "קשקבל" in dialog_html:
                raise RuntimeError(
                    "Dialog opened wrong product (Kashkaval barcode 2370284 detected). "
                    "Barcode-image strategy found wrong card."
                )
            if BARCODE not in dialog_html and "בייבי בל" not in dialog_html:
                print(
                    f"WARNING: Dialog may not contain Baby Bell — barcode {BARCODE} not in dialog HTML. "
                    "Proceeding but flagging."
                )

            # Capture tabs
            result["ingredients_status"] = click_tab_and_capture(
                page, "רכיבים", OUTPUT_DIR / "ingredients.html"
            )
            result["nutrition_status"] = click_tab_and_capture(
                page, "ערכים תזונתיים", OUTPUT_DIR / "nutrition.html"
            )
            result["allergens_status"] = click_tab_and_capture(
                page, "מידע אלרגני", OUTPUT_DIR / "allergens.html"
            )

            result["status"] = "scraped"
            print(f"Ingredients: {result['ingredients_status']}")
            print(f"Nutrition:   {result['nutrition_status']}")
            print(f"Allergens:   {result['allergens_status']}")

        except Exception as e:
            result["error"] = str(e)[:400]
            print(f"FAILED: {e}")
        finally:
            browser.close()

    save_json(RESULT_PATH, result)
    print(f"\nResult saved: {RESULT_PATH}")
    return result


if __name__ == "__main__":
    main()
