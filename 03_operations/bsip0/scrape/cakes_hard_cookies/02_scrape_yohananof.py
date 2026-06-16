"""
BSIP0 Yochananof — Cakes + Hard Cookies (Retailer #2, run_cakes_001 / TASK-283).

Streamlined headless Playwright scrape of yochananof.co.il storefront product modals.
OFF BAN: absolute — nutrition + ingredients come ONLY from the storefront tabs
(רכיבים / ערכים תזונתיים). No OFF import, no OFF fallback. Empty tab -> NULL field.

Outputs the SAME BSIP0 record schema as 01_scrape_shufersal.py so 03_merge.py can
dedup+merge the two retailers into one corpus.
Output: 02_products/cakes_hard_cookies/bsip0_outputs/cakes_yohananof_bsip0_raw_{ts}.json
"""
from __future__ import annotations
import json, re, sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT_DIR = Path(r"C:\Bari\02_products\cakes_hard_cookies\bsip0_outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = ["עוגיות שוקולד צ׳יפס", "עוגיות", "קוקיס", "עוגת שוקולד", "עוגה",
           "עוגת שמרים", "עוגיות מילוי", "עוגת גבינה", "ביסקוויט", "קראנץ"]
MAX_PRODUCTS = 70
BLEED = ["הנתונים המדויקים", "יתכנו טעויות", "התמונות והתאריכים", "יש לקרוא"]
INCLUDE = ["עוג", "קוקיס", "ביסקוויט", "שבבי", "קראנץ", "שטרודל", "מאפין", "צ׳יפס", "צ'יפס"]
EXCLUDE = ["לחם", "פיתה", "חלה", "קרקר", "פריכ", "וופל", "ופל", "במבה", "ביסלי",
           "צ'יפס תפו", "קמח", "אבקת", "תבנית", "נרות", "סוכריות", "גלידה"]


def clean(t): return re.sub(r"\s+", " ", str(t or "")).strip()


def _num(pattern, text):
    m = re.search(pattern, text)
    if not m:
        return ""
    return m.group(1)


def parse_nutrition(text):
    t = clean(text)
    return {
        "energy_kcal_raw": _num(r"אנרגיה\s*\(?קלוריות\)?\s*([\d.]+)", t),
        "protein_raw": _num(r"חלבונים?\s*\(גרם\)\s*([\d.]+)", t),
        "carbs_raw": _num(r"(?:סך ה)?פחמימות\s*\(גרם\)\s*([\d.]+)", t),
        "sugar_raw": _num(r"סוכרים?\s*(?:מתוך פחמימות\s*)?\(גרם\)\s*([\d.]+)", t),
        "fat_raw": _num(r"שומנים?\s*\(גרם\)\s*([\d.]+)", t),
        "saturated_fat_raw": _num(r"רוויות?\s*\(גרם\)\s*([\d.]+)", t),
        "sodium_raw": _num(r"נתרן\s*\(מ[\"׳']?ג\)\s*([\d.]+)", t),
        "fiber_raw": _num(r"סיבים\s*תזונתיים\s*\(גרם\)\s*([\d.]+)", t),
    }


def parse_ingredients(text):
    t = clean(text)
    # The real ingredient list follows the tab-bar (…רכיבים ערכים תזונתיים מידע אלרגני);
    # take everything after the LAST 'מידע אלרגני', then cut at the first bleed marker.
    idx = t.rfind("מידע אלרגני")
    if idx != -1:
        ing = t[idx + len("מידע אלרגני"):]
    else:
        m = re.search(r"רכיבים\s*[:]?\s*(.+)", t)
        ing = m.group(1) if m else t
    for b in BLEED:
        i = ing.find(b)
        if i != -1:
            ing = ing[:i]
    return clean(ing)[:1200]


def capture_tab(pg, tab_name):
    try:
        tab = pg.get_by_role("tab", name=tab_name).first
        if tab.count() == 0:
            return ""
        tab.click(force=True)
        pg.wait_for_timeout(1800)
        return pg.locator('[role="dialog"]').first.inner_text(timeout=4000)
    except Exception:
        return ""


def looks_target(name):
    nl = name
    return any(s in nl for s in INCLUDE) and not any(s in nl for s in EXCLUDE)


def run():
    products, seen = [], set()
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        pg = b.new_page(viewport={"width": 1400, "height": 1000})
        for q in QUERIES:
            if len(products) >= MAX_PRODUCTS:
                break
            try:
                pg.goto(f"https://yochananof.co.il/category?search={quote(q)}",
                        wait_until="domcontentloaded", timeout=60000)
                pg.wait_for_timeout(3500)
            except PWTimeout:
                continue
            for t in ["אישור", "מסכים", "הבנתי", "קבל"]:
                try:
                    x = pg.get_by_text(t, exact=False).first
                    if x.is_visible(timeout=500):
                        x.click(force=True); pg.wait_for_timeout(400); break
                except Exception:
                    pass
            for _ in range(6):
                pg.mouse.wheel(0, 1000); pg.wait_for_timeout(600)
            cards = pg.evaluate("""()=>{const o=[];const s=new Set();
              for(const img of document.querySelectorAll('img')){let el=img,bt=null,bs=0;
                for(let d=0;d<10&&el;d++){const tx=(el.innerText||'').trim();let sc=0;
                  if(tx.includes('₪'))sc+=3;if(tx.includes('גרם'))sc+=2;
                  if(el.querySelector('img'))sc+=3;if(tx.length>12&&tx.length<800)sc+=1;
                  if(sc>bs){bs=sc;bt=el;}el=el.parentElement;}
                if(!bt||bs<5||s.has(bt))continue;s.add(bt);
                const ie=bt.querySelector('img');const src=ie?(ie.currentSrc||ie.src||''):'';
                o.push({text:(bt.innerText||'').trim(),src:src});}return o;}""")
            print(f"[{q}] {len(cards)} cards", flush=True)
            for c in cards:
                if len(products) >= MAX_PRODUCTS:
                    break
                txt = clean(c["text"])
                bcm = re.search(r"(729\d{10}|\d{13})", txt + " " + c["src"])
                barcode = bcm.group(1) if bcm else ""
                name = next((l for l in txt.split("\n") if len(clean(l)) > 5
                             and "₪" not in l), txt[:60])
                name = clean(name)
                if not barcode or barcode in seen or not looks_target(name):
                    continue
                seen.add(barcode)
                # open modal via barcode image, else by name text
                try:
                    loc = pg.locator(f'img[src*="{barcode}"]').first
                    if loc.count() == 0:
                        loc = pg.get_by_text(name[:25], exact=False).first
                    loc.scroll_into_view_if_needed(timeout=4000); pg.wait_for_timeout(400)
                    loc.click(force=True); pg.wait_for_timeout(3000)
                    if pg.locator('[role="dialog"]').first.count() == 0:
                        continue
                except Exception:
                    continue
                ing_txt = capture_tab(pg, "רכיבים")
                nut_txt = capture_tab(pg, "ערכים תזונתיים")
                full = clean(ing_txt + " " + nut_txt)
                real_bc = (re.search(r"ברקוד:\s*(\d{8,13})", full) or [None, barcode])[1]
                brand = clean((re.search(r"מותג/יצרן:\s*(.+?)\s+(?:ארץ|מדינת|כשרות|ברקוד)", full) or [None, ""])[1])
                size = (re.search(r"מידה:\s*([\d.]+)\s*גרם", full) or [None, None])[1]
                nutrition = parse_nutrition(nut_txt)
                ingredients = parse_ingredients(ing_txt)
                imgs = [c["src"]] if c["src"].startswith("http") else []
                products.append({
                    "retailer_id": "yohananof", "retailer_name": "יוחננוף",
                    "source_url": f"https://yochananof.co.il/category?search={quote(q)}",
                    "scraped_at": datetime.utcnow().isoformat(),
                    "name_he": name, "name_en": "", "brand": brand, "barcode": real_bc,
                    "category_raw": "", "subcategory_raw": "cakes_hard_cookies",
                    "serving_size_g_hint": None, "nutrition": nutrition,
                    "nutrition_raw_source": {"tab_text": clean(nut_txt)[:1500]},
                    "ingredients_raw": ingredients,
                    "ingredients_language": "he" if ingredients and any("א" <= ch <= "ת" for ch in ingredients) else "",
                    "image_urls": imgs, "extraction_method": "playwright_modal",
                    "extraction_confidence": "high" if (nutrition["energy_kcal_raw"] and ingredients) else ("medium" if nutrition["energy_kcal_raw"] else "low"),
                    "price": "", "weight_g": float(size) if size else None, "price_per_100g": None,
                    "acquisition_query": q, "acquisition_tier": "yohananof",
                })
                if len(products) % 10 == 0:
                    print(f"  ...{len(products)} captured", flush=True)
                try:
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(700)
                except Exception:
                    pass
        b.close()
    return products


if __name__ == "__main__":
    ps = run()
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out = OUT_DIR / f"cakes_yohananof_bsip0_raw_{ts}.json"
    nut = sum(1 for p in ps if p["nutrition"]["energy_kcal_raw"])
    ing = sum(1 for p in ps if p["ingredients_raw"])
    out.write_text(json.dumps({
        "meta": {"retailer_id": "yohananof", "category": "cakes_hard_cookies",
                 "scraped_at": ts, "count": len(ps), "off_used": False,
                 "nutrition": nut, "ingredients": ing,
                 "source": "yochananof.co.il storefront modal tabs (OFF banned)"},
        "products": ps,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWROTE {out}  ({len(ps)} products, {nut} nutrition, {ing} ingredients)")
