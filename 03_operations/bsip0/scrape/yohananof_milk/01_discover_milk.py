"""
BSIP0 — Yohananof Milk & Alternatives Discovery
Searches yochananof.co.il for liquid milk and plant-based beverages.
Outputs: outputs/yohananof_milk/candidate_review.csv (set approved_for_scrape=YES then run 03)
"""
from pathlib import Path
from urllib.parse import quote
from datetime import datetime
import csv
import json
import re

from playwright.sync_api import sync_playwright

import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
RETAILER = "yohananof_milk"
RETAILER_DIR = OUTPUT_DIR / RETAILER
RETAILER_DIR.mkdir(parents=True, exist_ok=True)

SEARCH_QUERIES = [
    "חלב מלא",
    "חלב 3%",
    "חלב 1%",
    "חלב דל שומן",
    "חלב חצי שמן",
    "חלב שוקולד",
    "חלב עשיר בחלבון",
    "חלב ללא לקטוז",
    "חלב עז",
    "משקה סויה",
    "משקה שיבולת שועל",
    "משקה שקדים",
    "משקה קוקוס",
    "משקה אורז",
    "Alpro",
    "Oatly",
    "משקה צמחי חלב",
]

HARD_EXCLUDE = [
    "גבינה", "גבינות", "קוטג'", "שמנת", "יוגורט", "לבן",
    "חמאה", "ריקוטה", "מסקרפונה", "בולגרית", "פטה",
    "אבקת חלב", "קרם חלב",
    "גלידה", "פודינג", "קינוח חלבי",
    "חטיף", "פצפוץ", "ביסקוויט", "עוגיות",
    "כלב", "חתול", "חיות מחמד",
    "שוקו אבקה", "קפה",
    "סויה טחונה", "טופו",
    "גרנולה", "דגני",
]

POSITIVE_TYPES = [
    "חלב",
    "משקה סויה",
    "משקה שיבולת",
    "משקה שקדים",
    "משקה קוקוס",
    "משקה אורז",
    "משקה צמחי",
    "משקה עשיר",
    "חלב צמחי",
]

LIQUID_SIGNALS = [
    'מ"ל', "מ'ל", "מל ", "1000 מ", "500 מ", "200 מ",
    "ליטר", "1L", "1 ל", "1.5L",
    "בקבוק", "קרטון",
]

KNOWN_BRANDS = [
    "תנובה", "שטראוס", "גלי", "טרה",
    "Alpro", "אלפרו",
    "Oatly", "אוטלי",
    "Silk",
    "Wlog",
    "נוגת",
    "ריינה",
    "פרי גן",
]


def clean(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def has_any(text, terms):
    text = clean(text)
    return any(term in text for term in terms)


def extract_barcode(text):
    match = re.search(r"(729\d{10}|\d{13})", text or "")
    return match.group(1) if match else ""


def candidate_decision(product):
    combined = clean(
        f"{product.get('name','')} {product.get('card_text','')} {product.get('image_alt','')}"
    )

    if not combined:
        return "REJECT", "empty"

    for term in HARD_EXCLUDE:
        if term in combined:
            return "REJECT", f"hard_exclude:{term}"

    is_liquid = has_any(combined, LIQUID_SIGNALS)
    is_positive_type = has_any(combined, POSITIVE_TYPES)
    is_known_brand = has_any(combined, KNOWN_BRANDS)

    if is_positive_type and is_liquid:
        return "YES", "milk_or_beverage_with_liquid_signal"

    if is_positive_type:
        return "REVIEW", "milk_type_missing_liquid_signal"

    if is_known_brand and "חלב" in combined:
        return "YES", "known_brand_with_milk_keyword"

    if is_known_brand:
        return "REVIEW", "known_brand_needs_review"

    if "חלב" in combined:
        return "REVIEW", "milk_keyword_present_needs_review"

    return "REJECT", "not_milk_or_beverage"


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


def mark_product_cards(page):
    return page.evaluate("""
    () => {
      const out = [];
      const seen = new Set();

      function visible(el) {
        const r = el.getBoundingClientRect();
        return r.width > 80 && r.height > 80 && r.bottom >= 0 && r.top <= window.innerHeight + 600;
      }

      function score(el) {
        const txt = (el.innerText || '').trim();
        if (!txt) return 0;

        let s = 0;
        if (txt.includes('₪')) s += 3;
        if (txt.includes('מ"ל') || txt.includes("ליטר") || txt.includes('מל')) s += 3;
        if (txt.includes('חלב') || txt.includes('משקה')) s += 3;
        if (el.querySelector('img')) s += 3;
        if (txt.length > 15 && txt.length < 1200) s += 1;
        return s;
      }

      for (const img of Array.from(document.querySelectorAll('img'))) {
        let el = img;
        let best = null;
        let bestScore = 0;

        for (let depth = 0; depth < 12 && el; depth++) {
          const s = score(el);
          if (s > bestScore) {
            best = el;
            bestScore = s;
          }
          el = el.parentElement;
        }

        if (!best || bestScore < 5 || !visible(best) || seen.has(best)) continue;
        seen.add(best);

        const imgEl = best.querySelector('img');
        const src = imgEl ? (imgEl.currentSrc || imgEl.src || '') : '';
        const srcset = imgEl ? (imgEl.getAttribute('srcset') || '') : '';
        const alt = imgEl ? (imgEl.getAttribute('alt') || '') : '';
        const text = (best.innerText || '').trim();

        out.push({
          card_text: text,
          image_alt: alt,
          image_url_raw: (src + ' ' + srcset).trim()
        });
      }

      return out;
    }
    """)


def choose_best_name(card_text, image_alt):
    lines = [clean(x) for x in clean(card_text).split("\n") if clean(x)]
    bad = ["₪", "הוסף", "שמירה", "מבצע", "לרשימה", "מחיר", "יח' ב", "100 מ"]

    candidates = [
        line for line in lines
        if len(line) >= 4 and not any(b in line for b in bad)
    ]

    for line in candidates:
        if any(kw in line for kw in ["חלב", "משקה", "Alpro", "Oatly", "Silk"]):
            return line

    if candidates:
        return candidates[0]

    return clean(image_alt)


def discover_query(page, query):
    print(f"\nDiscovering: {query}")
    url = f"https://yochananof.co.il/category?search={quote(query)}"

    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3500)
    close_cookie_popup(page)

    products = {}
    stable_rounds = 0
    last_count = 0

    for round_no in range(1, 100):
        raw_cards = mark_product_cards(page)

        for c in raw_cards:
            combined = clean(f"{c.get('card_text','')} {c.get('image_alt','')} {c.get('image_url_raw','')}")
            barcode = extract_barcode(combined)
            name = choose_best_name(c.get("card_text", ""), c.get("image_alt", ""))

            if not name:
                continue

            key = barcode or f"{query}|{name}"

            product = {
                "key": key,
                "barcode": barcode,
                "name": name,
                "brand": "",
                "query": query,
                "card_text": c.get("card_text", ""),
                "image_alt": c.get("image_alt", ""),
                "image_url_raw": c.get("image_url_raw", ""),
                "discovered_at": now_iso(),
            }

            if key not in products:
                products[key] = product

        current_count = len(products)
        print(f"  Round {round_no}: {current_count} products")

        if current_count == last_count:
            stable_rounds += 1
        else:
            stable_rounds = 0
            last_count = current_count

        if stable_rounds >= 15:
            break

        page.mouse.wheel(0, 900)
        page.wait_for_timeout(900)

    return list(products.values())


def write_outputs(all_products):
    deduped = {}
    for p in all_products:
        key = p.get("barcode") or p.get("key")
        if key and key not in deduped:
            decision, reason = candidate_decision(p)
            p["suggested_decision"] = decision
            p["decision_reason"] = reason
            p["approved_for_scrape"] = "YES" if decision == "YES" else "NO"
            deduped[key] = p

    rows = list(deduped.values())
    save_json(RETAILER_DIR / "all_discovered_raw.json", rows)

    csv_path = RETAILER_DIR / "candidate_review.csv"
    fields = [
        "approved_for_scrape", "suggested_decision", "decision_reason",
        "barcode", "name", "brand", "query", "card_text", "image_alt", "image_url_raw",
    ]
    rows_sorted = sorted(
        rows,
        key=lambda x: {"YES": 0, "REVIEW": 1, "REJECT": 2}.get(x.get("suggested_decision"), 9)
    )
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows_sorted:
            writer.writerow(row)

    yes_count = sum(1 for r in rows if r.get("suggested_decision") == "YES")
    review_count = sum(1 for r in rows if r.get("suggested_decision") == "REVIEW")
    reject_count = sum(1 for r in rows if r.get("suggested_decision") == "REJECT")

    print(f"\n{'='*40}")
    print(f"Discovery complete: {len(rows)} unique products")
    print(f"  YES (auto-approved): {yes_count}")
    print(f"  REVIEW (manual):     {review_count}")
    print(f"  REJECT:              {reject_count}")
    print(f"Review CSV: {csv_path}")
    print(f"{'='*40}")
    print("Next: python 03_scrape_milk.py")


def main():
    all_products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1500, "height": 900})

        for query in SEARCH_QUERIES:
            try:
                results = discover_query(page, query)
                all_products.extend(results)
                print(f"  → {len(results)} candidates from '{query}'")
            except Exception as e:
                print(f"  ERROR on query '{query}': {e}")

        browser.close()

    write_outputs(all_products)


if __name__ == "__main__":
    main()
