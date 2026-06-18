"""
BSIP0 — Salty snacks REAL retailer-panel re-source (TASK-237).

REPLACES 01_bsip0_off_panels.py. NO Open Food Facts anywhere.

For each of the 38 salty-snacks EANs (identity already real from Yochananof catalog),
open the Yochananof storefront product modal and capture the REAL Hebrew nutrition panel
+ ingredient list from the retailer product page. Yochananof primary.

Output: 02_products/salty_snacks/bsip0_outputs/bsip0_salty_snacks_retailer_raw.json
  panel_source = retailer_product_page (yochananof)
Per product: real per-100g nutrition + real Hebrew ingredients, or honest panel-only/missing.
"""
import sys, json, re, pathlib, time
from datetime import datetime, timezone
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from bs4 import BeautifulSoup

HERE = pathlib.Path(__file__).parent
FRONTEND = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\salty_snacks_frontend_v4.json")
CATALOG = pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\shufersal_frozen_vegetables\rescraper\yoh_named_catalog.json")
OUT_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip0_outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "bsip0_salty_snacks_retailer_raw.json"
RAW_DIR = HERE / "yoh_product_html"
RAW_DIR.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# label -> canonical per-100g key (parser pulls from #simple-tabpanel-1 list)
LABEL_MAP = [
    ("חומצות שומן רוויות", "fat_saturated_g"),
    ("חומצות שומן טראנס", "fat_trans_g"),
    ("סך הפחמימות", "carbohydrates_g"),
    ("סוכרים מתוך פחמימות", "sugars_g"),
    ("סיבים תזונתיים", "dietary_fiber_g"),
    ("חלבונים", "protein_g"),
    ("שומנים", "fat_g"),
    ("נתרן", "sodium_mg"),
    ("אנרגיה", "energy_kcal"),
]


def clean(t):
    if t is None:
        return ""
    return re.sub(r"\s+", " ", str(t).replace("\xa0", " ").replace("‎", "")).strip()


def parse_number(text):
    """Return (value, is_threshold). 'L 0.5' / 'פחות מ 0.5' => (0.5, True)."""
    if text is None:
        return None, False
    t = clean(text).replace(",", ".")
    is_thr = bool(re.search(r"(^|\s)L\s|פחות\s*מ|<", t))
    t = re.sub(r"(^|\s)L(\s|$)", " ", t)
    t = t.replace("<", "").replace("פחות מ", "")
    m = re.search(r"(\d+(?:\.\d+)?)", t)
    return (float(m.group(1)) if m else None), is_thr


def load_targets():
    fe = json.loads(FRONTEND.read_text(encoding="utf-8"))
    targets = []
    for p in fe["products"]:
        targets.append({"ean": str(p["barcode"]), "name": p["name"], "sub_pool": p["subPool"]})
    # map EAN -> real image url from catalog
    cat = json.loads(CATALOG.read_text(encoding="utf-8"))
    img_by_ean = {}
    for item in cat:
        m = re.search(r"_(\d{8,14})_", item.get("url", ""))
        if m:
            img_by_ean.setdefault(m.group(1), item["url"])
    for t in targets:
        t["image_url"] = img_by_ean.get(t["ean"], "")
    return targets


def close_popup(page):
    for t in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK", "סגור"]:
        try:
            b = page.get_by_text(t, exact=False).first
            if b.is_visible(timeout=400):
                b.click(force=True); page.wait_for_timeout(300); return
        except Exception:
            pass


def open_modal(page, ean, name):
    page.goto(f"https://yochananof.co.il/category?search={ean}",
              wait_until="domcontentloaded", timeout=60000)
    try:
        page.wait_for_selector('img[src*="catalog/product"]', timeout=18000)
    except Exception:
        pass
    page.wait_for_timeout(2000)
    close_popup(page)
    for sel in [f'img[src*="{ean}"]', 'img[src*="catalog/product"]']:
        try:
            loc = page.locator(sel).first
            if loc.count() > 0:
                loc.scroll_into_view_if_needed(timeout=4000)
                page.wait_for_timeout(300)
                loc.click(force=True)
                page.wait_for_timeout(3500)
                # confirm a dialog opened
                if page.locator('[role=dialog]').first.count() > 0:
                    return True
        except Exception:
            continue
    return False


def capture_tab(page, label):
    try:
        tab = page.get_by_role("tab", name=label).first
        if tab.count() == 0:
            return None
        tab.click(force=True)
        page.wait_for_timeout(1600)
        dlg = page.locator('[role=dialog]').first
        if dlg.count() == 0:
            return None
        return dlg.inner_html()
    except Exception:
        return None


def parse_nutrition(html):
    if not html:
        return {}, {}
    s = BeautifulSoup(html, "lxml")
    nut = {}
    raw = {}
    thr = {}
    # tabpanel-1 list rows: "<label> (unit) <value>"
    panel = s.select_one("#simple-tabpanel-1")
    rows = panel.select("li") if panel else []
    if not rows and panel:
        # fallback: split lines
        rows = []
    for row in rows:
        full = clean(row.get_text(" ", strip=True))
        if not full:
            continue
        # strip trailing number to get label part
        for heb, key in LABEL_MAP:
            if heb in full and key not in nut:
                val_part = full.split(heb, 1)[1]
                val, is_thr = parse_number(val_part)
                if val is not None:
                    if key == "sodium_mg":
                        nut[key] = round(val)
                    elif key == "energy_kcal":
                        nut[key] = round(val)
                    else:
                        nut[key] = val
                    raw[key] = full
                    if is_thr:
                        thr[key] = True
                break
    return nut, {"raw_rows": raw, "threshold_declared": thr}


def parse_ingredients(html):
    if not html:
        return None
    s = BeautifulSoup(html, "lxml")
    panel = s.select_one("#simple-tabpanel-0")
    if not panel:
        return None
    txt = clean(panel.get_text(" ", strip=True))
    return txt or None


def basis_is_per_100g(html):
    if not html:
        return False
    t = clean(BeautifulSoup(html, "lxml").get_text(" ", strip=True))
    return ("ל100 גרם" in t.replace("-", "").replace(" ", "") or "100 גרם" in t or "ל-100 גרם" in t)


def main():
    targets = load_targets()
    print(f"Targets: {len(targets)}")
    results = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True)
        pg = br.new_page(viewport={"width": 1400, "height": 1100}, user_agent=UA)
        for i, t in enumerate(targets, 1):
            ean, name = t["ean"], t["name"]
            rec = {
                "barcode": ean, "name_he": name, "sub_pool": t["sub_pool"],
                "image_url": t["image_url"], "identity_source": "yochananof_catalog_harvest",
                "panel_source": "retailer_product_page",
                "retailer": "yochananof",
                "normalized_nutrition_per_100g": {}, "ingredients_text_he": None,
                "nutrition_provenance": {}, "capture": {},
            }
            try:
                opened = open_modal(pg, ean, name)
                rec["capture"]["modal_opened"] = opened
                if opened:
                    n_html = capture_tab(pg, "ערכים תזונתיים")
                    i_html = capture_tab(pg, "רכיבים")
                    nut, prov = parse_nutrition(n_html)
                    ingr = parse_ingredients(i_html)
                    per100 = basis_is_per_100g(n_html)
                    rec["normalized_nutrition_per_100g"] = nut
                    rec["ingredients_text_he"] = ingr
                    rec["nutrition_provenance"] = prov
                    rec["capture"]["basis_per_100g"] = per100
                    rec["capture"]["nutrition_rows"] = len(nut)
                    rec["capture"]["has_ingredients"] = bool(ingr)
                    # persist raw html
                    if n_html:
                        (RAW_DIR / f"{ean}_nutrition.html").write_text(n_html, encoding="utf-8")
                    if i_html:
                        (RAW_DIR / f"{ean}_ingredients.html").write_text(i_html, encoding="utf-8")
                    # close modal
                    try:
                        pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
                    except Exception:
                        pass
                print(f"  [{i}/{len(targets)}] {ean} opened={opened} "
                      f"nut={len(rec['normalized_nutrition_per_100g'])} "
                      f"ingr={'Y' if rec['ingredients_text_he'] else 'N'}")
            except Exception as e:
                rec["capture"]["error"] = str(e)[:200]
                print(f"  [{i}/{len(targets)}] {ean} ERROR {str(e)[:120]}")
            results.append(rec)
            time.sleep(0.4)
        br.close()

    with_nut = sum(1 for r in results if len(r["normalized_nutrition_per_100g"]) >= 4)
    with_ingr = sum(1 for r in results if r["ingredients_text_he"])
    bsip0 = {
        "schema_version": "bsip0_v1",
        "run_id": "salty_snacks_retailer_001",
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "category": "salty_snacks",
        "retailer": "yochananof",
        "acquisition_method": "yochananof_storefront_product_modal (playwright)",
        "scrape_date": datetime.now().strftime("%Y-%m-%d"),
        "identity_source": "yochananof storefront catalog (real EAN + real image URL)",
        "panel_source": "retailer_product_page",
        "product_count": len(results),
        "completeness": {
            "with_nutrition_4plus": with_nut,
            "with_real_ingredients": with_ingr,
            "modal_opened": sum(1 for r in results if r["capture"].get("modal_opened")),
        },
        "provenance": {
            "identity": "yochananof_catalog_harvest",
            "panel": "yochananof_product_modal_html (real Hebrew panel + ingredients)",
            "no_off": "Open Food Facts NOT used (TASK-237)",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        },
        "products": results,
    }
    OUT.write_text(json.dumps(bsip0, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nBSIP0 written: {OUT}")
    print(f"with nutrition(>=4): {with_nut}/{len(results)} | with real ingredients: {with_ingr}/{len(results)}")


if __name__ == "__main__":
    main()
