"""
Targeted Playwright scrape — navigate to specific product modal using Victory's
deep link pattern, capture the branch API response.

From earlier testing:
- /category/item/{id} opens a cookie dialog (not product)
- The correct pattern needs a branch selection + product route

Strategy:
1. Accept cookies/select a branch
2. Navigate to chocolate search
3. Scroll until Millennium 80% (4820005195848) or Lindt products appear in the page
4. Click product and capture modal HTML
5. Parse nutritionValues from modal

Key fix from previous failure: the scrolling found 200 images but never found our specific
products. Victory may sort search results differently (e.g. by relevance/popularity) and
our products may appear deeper in the scroll. We need to scroll much more aggressively,
and also try different search terms.
"""
import sys, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright, TimeoutError as PW_Timeout

VICTORY_BASE = "https://www.victoryonline.co.il"

# Map barcode -> internal product ID (from /api/products/{barcode})
TARGET_PRODUCTS = {
    "4820005195848": {"api_id": 415280, "label": "Millennium 80%", "search_terms": ["שוקולד מריר 80", "80% קקאו", "מיליניום 80"]},
    "3046920023443": {"api_id": 7872576, "label": "Lindt Excellence dark", "search_terms": ["שוקולד קרמי מריר לינדט", "לינדט מריר", "lindt dark"]},
    "3046920023429": {"api_id": 7872575, "label": "Lindt caramel milk", "search_terms": ["לינדט קרמל", "שוקולד חלב קרמל לינדט", "caramel lindt"]},
    "3046920023368": {"api_id": 7872574, "label": "Lindt Excellence milk", "search_terms": ["לינדט חלב", "שוקולד חלב לינדט", "אקסטרה קרימי לינדט"]},
}

def _dismiss_popups(page):
    for sel in ['button:has-text("אישור")', 'button:has-text("מסכים")', 'button:has-text("הבנתי")',
                '[aria-label="סגור"]', '.cookie-wall button', '[data-test="dialog-close"]']:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass

def parse_nutrition_from_html(dialog_html: str) -> dict:
    """Parse nutrition from the dialog HTML (same Victory structure as fixture)."""
    from bs4 import BeautifulSoup as BS
    soup = BS(dialog_html, "html.parser")
    section = soup.find("section", class_="nutrition-values")
    table = section.find("table") if section else soup.find("table")
    if not table:
        return {}

    result = {}
    seen = set()
    LABEL_MAP = [
        (["טראנס", "trans"], "trans_fat"),
        (["רווי", "saturated"], "saturated_fat"),
        (["סוכר", "sugar"], "sugar"),
        (["פחמימ", "carb"], "carbs"),
        (["סיב", "fiber"], "fiber"),
        (["חלבונ", "protein"], "protein"),
        (["נתרן", "sodium"], "sodium"),
        (["אנרגי", "קלורי", "kcal", "energy"], "energy"),
        (["שומנ", "fat"], "fat"),
    ]
    for row in table.find_all("tr"):
        th = row.find("th")
        td = row.find("td")
        if not th or not td:
            continue
        label = th.get_text(strip=True)
        val_text = td.get_text(strip=True)
        m = re.search(r"([\d,.]+)", val_text)
        if not m:
            continue
        try:
            val = float(m.group(1).replace(",", "."))
        except ValueError:
            continue
        ll = label.lower()
        for tokens, canon in LABEL_MAP:
            if canon in seen:
                continue
            if any(t in label or t in ll for t in tokens):
                if canon in ("fat", "carbs") and any(x in label for x in ["מתוכ"]):
                    continue
                result[canon] = val
                seen.add(canon)
                break
    return result


def parse_ingredients_from_html(dialog_html: str) -> str:
    from bs4 import BeautifulSoup as BS
    soup = BS(dialog_html, "html.parser")
    full_text = soup.get_text(separator=" ", strip=True)
    m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
    if m:
        return m.group(1).strip()[:1400]
    if any(w in full_text for w in ["קקאו", "סוכר", "חלב", "לציטין", "שומן"]):
        return full_text[:1400]
    return ""


captured_responses_by_product = {}  # api_id -> {nutrition, ingredients}

def handle_response(response, target_api_id):
    url = response.url
    if "victoryonline" not in url:
        return
    if "branches" not in url or "products" not in url:
        return
    try:
        ct = response.headers.get("content-type", "")
        if "json" not in ct:
            return
        body = response.body()
        if b"nutritionValues" not in body:
            return
        text = body.decode("utf-8", errors="replace")
        data = json.loads(text)
        prods = data.get("products", [])
        for p in prods:
            pid = p.get("productId")
            if pid == target_api_id:
                nv = p.get("nutritionValues") or {}
                values = nv.get("values") or []
                data_obj = p.get("data") or {}
                lang1 = data_obj.get("1") or data_obj.get(1) or {}
                ingr = (lang1.get("ingredients") or "") if isinstance(lang1, dict) else ""
                if values or ingr:
                    captured_responses_by_product[pid] = {
                        "nutritionValues": nv,
                        "ingredients": ingr,
                        "localName": p.get("localName", ""),
                    }
                    print(f"  CAPTURED via XHR: pid={pid} nutr_rows={len(values)} ingr_len={len(ingr)}", flush=True)
    except Exception:
        pass


results = {}

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)

    for bc, info in TARGET_PRODUCTS.items():
        api_id = info["api_id"]
        label = info["label"]
        search_terms = info["search_terms"]

        print(f"\n{'='*60}", flush=True)
        print(f"{bc} | {label}", flush=True)

        # Create a fresh context per product for clean state
        context = browser.new_context(
            viewport={"width": 1500, "height": 900},
            locale="he-IL",
            extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()

        # Set up response handler for this product's API id
        page.on("response", lambda resp, aid=api_id: handle_response(resp, aid))

        for search_term in search_terms:
            from urllib.parse import quote as _q
            url = f"{VICTORY_BASE}/category?search={_q(search_term)}"
            print(f"  Search: {search_term!r}", flush=True)
            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(8000)
                _dismiss_popups(page)
                page.wait_for_timeout(800)
                _dismiss_popups(page)
            except Exception as e:
                print(f"  GOTO error: {e}", flush=True)
                continue

            # Aggressive scroll to find the product
            bc_found = False
            for scroll_i in range(1, 150):
                # Check for our barcode in image src
                try:
                    bc_img = page.locator(f'img[src*="{bc}"], img[ng-src*="{bc}"]').first
                    if bc_img.count() > 0:
                        print(f"  Found by barcode in img src! scroll={scroll_i}", flush=True)
                        bc_img.scroll_into_view_if_needed(timeout=3000)
                        page.wait_for_timeout(700)
                        bc_img.click(force=True)
                        page.wait_for_timeout(5000)
                        bc_found = True
                        break
                except Exception:
                    pass

                # Also check for product ID (internal api_id) in img path
                try:
                    id_img = page.locator(f'img[src*="/{api_id}/"], img[ng-src*="/{api_id}/"]').first
                    if id_img.count() > 0:
                        print(f"  Found by api_id in img src! scroll={scroll_i}", flush=True)
                        id_img.scroll_into_view_if_needed(timeout=3000)
                        page.wait_for_timeout(700)
                        id_img.click(force=True)
                        page.wait_for_timeout(5000)
                        bc_found = True
                        break
                except Exception:
                    pass

                page.mouse.wheel(0, 1200)
                page.wait_for_timeout(700)

                if scroll_i % 30 == 0:
                    print(f"  Scrolling... {scroll_i}/150", flush=True)

            if bc_found:
                # Try to get modal content
                dialog = page.locator('[role="dialog"]').first
                if dialog.count() > 0:
                    # Click nutrition tab
                    try:
                        nutr_tab = page.get_by_role("tab", name="ערכים תזונתיים").first
                        if nutr_tab.count() > 0:
                            nutr_tab.click(force=True)
                            page.wait_for_timeout(2500)
                    except Exception:
                        pass

                    # Capture HTML
                    nutr_html = dialog.inner_html(timeout=3000)
                    nutr = parse_nutrition_from_html(nutr_html)

                    # Click ingredients tab
                    try:
                        ingr_tab = page.get_by_role("tab", name="רכיבים").first
                        if ingr_tab.count() > 0:
                            ingr_tab.click(force=True)
                            page.wait_for_timeout(2000)
                            ingr_html = dialog.inner_html(timeout=3000)
                            ingr = parse_ingredients_from_html(ingr_html)
                        else:
                            ingr = ""
                    except Exception:
                        ingr = ""

                    # Product name from dialog
                    prod_name = ""
                    try:
                        h_el = dialog.locator("h1, h2, .product-name, .title").first
                        if h_el.count() > 0:
                            prod_name = h_el.inner_text(timeout=1500).strip()
                    except Exception:
                        pass

                    results[bc] = {
                        "barcode": bc,
                        "label": label,
                        "status": "FOUND_AND_SCRAPED",
                        "source": "victory",
                        "search_term_used": search_term,
                        "product_name_on_victory": prod_name,
                        "nutrition": nutr,
                        "ingredients": ingr or None,
                        "ingredients_status": (
                            "REAL_INGREDIENTS" if ingr and any(w in ingr for w in ["קקאו","סוכר","חלב","שומן","לציטין"]) else
                            "BOILERPLATE" if "עלול להכיל" in (ingr or "") and "קקאו" not in (ingr or "") else
                            "TEXT" if ingr else "NULL"
                        ),
                        "has_full_nutrition": bool(nutr.get("energy") and nutr.get("fat") and nutr.get("carbs")),
                    }
                    print(f"  Scraped: nutr={nutr} | ingr={ingr[:100]}", flush=True)
                    break
                else:
                    print(f"  Clicked product but no dialog found", flush=True)
            else:
                print(f"  Product NOT FOUND on scroll for {search_term!r}", flush=True)

            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

        if bc not in results:
            results[bc] = {
                "barcode": bc,
                "label": label,
                "status": "NOT_FOUND_ON_VICTORY",
                "source": "victory",
                "nutrition": None,
                "ingredients": None,
                "has_full_nutrition": False,
            }

        context.close()

    browser.close()

# Also include any XHR-captured data
for api_id, data in captured_responses_by_product.items():
    print(f"\nXHR captured: pid={api_id} | {data}", flush=True)

print(f"\n=== FINAL RESULTS ===", flush=True)
for bc, r in results.items():
    print(f"  {bc}: {r['status']} | nutr={bool(r.get('nutrition'))} | ingr={bool(r.get('ingredients'))}", flush=True)

import json, pathlib, datetime
out_path = pathlib.Path(r"C:\Bari\02_products\chocolate\victory_targeted_scrape.json")
out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved: {out_path}", flush=True)
