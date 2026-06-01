"""
Yohananof BSIP0 discovery — Hummus and Savory Dips (supplementary).

Discovers hummus and savory dip products from Yohananof via Playwright
browser search. Run AFTER the Shufersal scrape to capture brands and
products not present on Shufersal.

Usage:
    cd C:\\Bari\\03_operations\\bsip0\\scrape\\yohananof_hummus
    python 01_discover_hummus_yohananof.py

Prerequisites:
    playwright install chromium

Output:
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\yohananof\\all_discovered_raw.json
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\yohananof\\candidate_review.csv

Next:
    Open candidate_review.csv.
    Set approved_for_scrape = YES for net-new products not already
    captured from Shufersal.
    Run: python 02_scrape_hummus_yohananof.py
"""

from pathlib import Path
from urllib.parse import quote
from datetime import datetime
import csv
import json
import re

from playwright.sync_api import sync_playwright

# ── Paths ──────────────────────────────────────────────────────────────────────
OUT_DIR = Path(r"C:\Bari\02_products\hummus\observations_bsip0\yohananof")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Search queries (Hebrew) ────────────────────────────────────────────────────
SEARCH_QUERIES = [
    "חומוס",
    "ממרח חומוס",
    "חומוס אורגני",
    "חומוס ביו",
    "חומוס שום",
    "חומוס חריף",
    "חומוס דל שומן",
    "חומוס 0%",
    "חומוס קל",
    "ממרח חצילים",
    "חציליות",
    "מטבוחה",
    "ממרח פלפל",
    "חומוס עם תוספות",
    "חומוס חלבון",
    "ממרח ירקות",
    "תבסיל",
]

# ── Hard exclude (TASK-018 + TASK-025 + TASK-026) ─────────────────────────────
HARD_EXCLUDE = [
    # Ready-to-eat tahini dip — defer to Tahini category (TASK-026)
    "סלט טחינה", "טחינה מוכנה", "ממרח טחינה", "טחינה ביתית",
    # Raw tahini
    "טחינה", "טחינה גולמית",
    # Schug and harissa
    "סחוג", "זחוג", "אריסה", "ארוסה", "חריסה",
    # Sweet spreads
    "ממרח שוקולד", "נוטלה", "ריבה", "ממרח תמרים", "דבש", "ממרח קרמל",
    # Dairy spreads
    "גבינה לבנה", "לאבנה", "גבינת שמנת", "קוטג", "ממרח גבינה",
    # Fish/meat
    "ממרח דגים", "דג מעושן", "ממרח טונה", "פטה",
    # European condiments
    "פסטו", "טפנד", "ממרח זיתים", "ארטישוק", "חזרת",
    # Pasta sauces and condiments
    "רוטב פסטה", "קטשופ", "חרדל", "מיונז",
    # Pickles
    "חמוצים", "כבוש", "זיתים",
    # Vegetable salads
    "קולסלאו", "כרוב לבן", "כרוב סגול", "גזר מרוקאי", "גזר קוריאני",
    "סלק", "תפוח אדמה", "בולגרי",
    # Wrong format
    "צ'יפס חומוס", "חומוסיות",
]

# ── Positive type signals ──────────────────────────────────────────────────────
POSITIVE_TYPES = [
    "חומוס",
    "ממרח חומוס",
    "ממרח חצילים",
    "חציליות",
    "מטבוחה",
    "ממרח פלפל",
    "פלפל צ'ומה",
    "ממרח ירקות",
    "תבסיל",
]

# ── Pack/multi-pack signals (exclude) ─────────────────────────────────────────
PACK_SIGNALS = ["שישייה", "רביעייה", "מארז", "מאגדת", "5+1", "*5", "*6", "5 יח", "6 יח"]


# ──────────────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────────────

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


def has_pack_signal(text):
    text = clean(text)
    return (
        has_any(text, PACK_SIGNALS)
        or re.search(r"\b\d+\s*[*xX]\s*\d+\b", text) is not None
        or re.search(r"\b\d+\s*\+\s*\d+\b", text) is not None
    )


def candidate_decision(product):
    combined = clean(
        f"{product.get('name','')} {product.get('card_text','')} {product.get('image_alt','')}"
    )

    if not combined:
        return "REJECT", "empty"

    for term in HARD_EXCLUDE:
        if term in combined:
            return "REJECT", f"hard_exclude:{term}"

    if has_pack_signal(combined):
        return "REJECT", "multi_pack"

    for term in POSITIVE_TYPES:
        if term in combined:
            return "YES", f"positive_type:{term}"

    if "חומוס" in combined or "ממרח" in combined or "מטבוחה" in combined:
        return "REVIEW", "possible_target"

    return "REJECT", "not_target_product_type"


# ──────────────────────────────────────────────────────────────────────────────
# Browser helpers
# ──────────────────────────────────────────────────────────────────────────────

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
        if (txt.includes('גרם') || txt.includes("גר'")) s += 2;
        if (txt.includes('חומוס') || txt.includes('ממרח') || txt.includes('מטבוחה')) s += 3;
        if (el.querySelector('img')) s += 3;
        if (txt.length > 10 && txt.length < 1200) s += 1;
        return s;
      }

      for (const img of Array.from(document.querySelectorAll('img'))) {
        let el = img;
        let best = null;
        let bestScore = 0;
        for (let depth = 0; depth < 12 && el; depth++) {
          const s = score(el);
          if (s > bestScore) { best = el; bestScore = s; }
          el = el.parentElement;
        }
        if (!best || bestScore < 5 || !visible(best) || seen.has(best)) continue;
        seen.add(best);
        const imgEl = best.querySelector('img');
        const src = imgEl ? (imgEl.currentSrc || imgEl.src || '') : '';
        const srcset = imgEl ? (imgEl.getAttribute('srcset') || '') : '';
        const alt = imgEl ? (imgEl.getAttribute('alt') || '') : '';
        out.push({
          card_text: (best.innerText || '').trim(),
          image_alt: alt,
          image_url_raw: (src + ' ' + srcset).trim()
        });
      }
      return out;
    }
    """)


def choose_best_name(card_text, image_alt):
    lines = [clean(x) for x in clean(card_text).split("\n") if clean(x)]
    bad = ["₪", "100 גרם", "הוסף", "שמירה", "מבצע", "לרשימה", "מחיר", "יח' ב"]
    candidates = [l for l in lines if len(l) >= 4 and not any(b in l for b in bad)]
    for line in candidates:
        if any(term in line for term in ["חומוס", "ממרח", "מטבוחה", "חצילים"]):
            return line
    if candidates:
        return candidates[0]
    return clean(image_alt)


def discover_query(page, query):
    print(f"\nDiscovering query: {query}")
    url = f"https://yochananof.co.il/category?search={quote(query)}"
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3500)
    close_cookie_popup(page)

    products = {}
    stable_rounds = 0
    last_count = 0

    for round_no in range(1, 80):
        raw_cards = mark_product_cards(page)
        for c in raw_cards:
            combined = clean(f"{c.get('card_text','')} {c.get('image_alt','')} {c.get('image_url_raw','')}")
            barcode = extract_barcode(combined)
            name = choose_best_name(c.get("card_text", ""), c.get("image_alt", ""))
            if not name:
                continue
            key = barcode or f"{query}|{name}"
            if key not in products:
                products[key] = {
                    "key": key,
                    "barcode": barcode,
                    "name": name,
                    "query": query,
                    "card_text": c.get("card_text", ""),
                    "image_alt": c.get("image_alt", ""),
                    "image_url_raw": c.get("image_url_raw", ""),
                    "discovered_at": now_iso(),
                }

        current_count = len(products)
        print(f"  Round {round_no}: discovered={current_count}")

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
            p["approved_for_scrape"] = "NO"
            deduped[key] = p

    rows = list(deduped.values())
    save_json(OUT_DIR / "all_discovered_raw.json", rows)

    csv_path = OUT_DIR / "candidate_review.csv"
    fields = [
        "approved_for_scrape", "suggested_decision", "decision_reason",
        "barcode", "name", "query", "card_text", "image_alt", "image_url_raw",
    ]
    rows_sorted = sorted(
        rows,
        key=lambda x: {"YES": 0, "REVIEW": 1, "REJECT": 2}.get(x.get("suggested_decision"), 9),
    )
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows_sorted:
            writer.writerow(row)

    yes = sum(1 for r in rows if r["suggested_decision"] == "YES")
    review = sum(1 for r in rows if r["suggested_decision"] == "REVIEW")
    reject = sum(1 for r in rows if r["suggested_decision"] == "REJECT")

    print(f"\n==============================")
    print(f"Discovery complete: {len(rows)} unique products")
    print(f"  YES    : {yes}")
    print(f"  REVIEW : {review}")
    print(f"  REJECT : {reject}")
    print(f"\nReview file: {csv_path}")
    print(f"Set approved_for_scrape = YES for net-new products")
    print(f"(Products already captured from Shufersal can be rejected to avoid duplication)")
    print(f"Then run: python 02_scrape_hummus_yohananof.py")
    print(f"==============================")


def main():
    all_products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1500, "height": 1000})
        for query in SEARCH_QUERIES:
            all_products.extend(discover_query(page, query))
        browser.close()
    write_outputs(all_products)


if __name__ == "__main__":
    main()
