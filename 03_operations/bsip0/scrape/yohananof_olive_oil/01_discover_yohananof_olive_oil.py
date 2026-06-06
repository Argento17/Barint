"""
BSIP0 Yochananof — Olive Oil discovery (adapted from snack-bar pattern).

Phase 1 of 3: discover + candidate list.
Phase 2: auto-approval (products named שמן זית are obvious — no manual CSV step needed).
Phase 3: scrape approved candidates (03_scrape_yohananof_olive_oil.py).

Outputs:
  02_products/olive_oil/bsip0_raw/yohananof/all_discovered_raw.json
  02_products/olive_oil/bsip0_raw/yohananof/approved_candidates.json
"""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_URL = "https://yochananof.co.il"
OUTPUT_DIR = Path(r"C:\Bari\02_products\olive_oil\bsip0_raw\yohananof")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SEARCH_QUERIES = [
    "שמן זית",
    "שמן זית כתית מעולה",
    "שמן זית ישראלי",
    "שמן זית כתית",
    "שמן זית אורגני",
    "סבא חביב שמן",
    "יד מרדכי שמן",
    "זיתא שמן",
    "ג'השאן שמן",
    "שמן זית יווני",
    "שמן זית ספרדי",
    "שמן זית PDO",
]

# These indicate it's clearly NOT an olive oil product
HARD_EXCLUDE = [
    "שמן חמניות", "שמן קנולה", "שמן תירס", "שמן סויה",
    "שמן דקלים", "שמן שומשום", "שמן אבוקדו",
    "שמן קוקוס", "שמן פשתן", "שמן ענבים", "שמן שקדים",
    "שמן גוף", "קרם", "סבון", "לוסיון",
    "חומץ", "רוטב", "מיונז",
    "זיתים כבושים", "זיתי שולחן",
    "תינוק", "מטרנה",
    "ביסלי", "במבה", "קרקר",
    "canola", "sunflower", " משחת שיניים",
    "פסולת", "pomace", "orujo",
]

# Signals that confirm it's olive oil
POSITIVE_SIGNALS = [
    "שמן זית",
    "olive oil",
    "כתית מעולה",
    "extra virgin",
    "כתית",
    "EVOO",
    "PDO",
    "DOP",
    "קלמטה",
]

# Known Israeli olive oil brands (for brand extraction)
KNOWN_BRANDS = [
    ("סבא חביב", "סבא חביב"),
    ("יד מרדכי", "יד מרדכי"),
    ("זיתא", "זיתא"),
    ("ג'השאן", "ג'השאן"),
    ("נריה", "נריה"),
    ("אליעד", "אליעד"),
    ("גרין", "גרין"),
    ("גרין אורגניק", "גרין"),
    ("אם הדרך", "אם הדרך"),
    ("שקדיה", "שקדיה"),
    ("BORGES", "BORGES"),
    ("MATTEO", "MATTEO"),
    ("FERNANDO", "FERNANDO"),
    ("GOYA", "GOYA"),
    ("COSTA D'ORO", "COSTA D'ORO"),
    ("Carapelli", "Carapelli"),
    ("Bertolli", "Bertolli"),
    ("Filippo Berio", "Filippo Berio"),
    ("Colavita", "Colavita"),
    ("עץ הזית", "עץ הזית"),
    ("פאם", "פאם"),
    ("כרמי", "כרמי"),
    ("כרמל", "כרמל"),
    ("זיתים ישראלים", "ישראלי"),
]


def clean(text: str | None) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def save_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_barcode(text: str) -> str:
    m = re.search(r"(729\d{10}|\d{13})", text or "")
    return m.group(1) if m else ""


def infer_brand(text: str) -> str:
    text = clean(text)
    for marker, brand in KNOWN_BRANDS:
        if marker in text:
            return brand
    return ""


def is_excluded(text: str) -> bool:
    t = clean(text).lower()
    return any(sig.lower() in t for sig in HARD_EXCLUDE)


def looks_like_olive_oil(text: str) -> bool:
    t = clean(text).lower()
    return any(sig.lower() in t for sig in POSITIVE_SIGNALS)


def candidate_decision(product: dict) -> tuple[str, str]:
    combined = clean(
        f"{product.get('name','')} {product.get('card_text','')} {product.get('image_alt','')}"
    )

    if not combined:
        return "REJECT", "empty"

    if is_excluded(combined):
        return "REJECT", "excluded_category"

    if looks_like_olive_oil(combined):
        return "YES", "olive_oil_signal_match"

    return "REJECT", "no_olive_oil_signal"


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


def extract_product_cards(page) -> list[dict]:
    return page.evaluate("""
    () => {
      const out = [];
      const seen = new Set();

      function visible(el) {
        const r = el.getBoundingClientRect();
        return r.width > 60 && r.height > 60 && r.bottom >= 0 && r.top <= window.innerHeight + 800;
      }

      function score(el) {
        const txt = (el.innerText || '').trim();
        if (!txt) return 0;
        let s = 0;
        if (txt.includes('₪') || txt.includes('ש"ח')) s += 3;
        if (txt.includes('שמן זית') || txt.includes('olive')) s += 4;
        if (txt.includes('מ"ל') || txt.includes('ליטר') || txt.includes('ml')) s += 2;
        if (txt.includes('כתית') || txt.includes('extra virgin')) s += 2;
        if (el.querySelector('img')) s += 2;
        if (txt.length > 10 && txt.length < 1500) s += 1;
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
        const alt = imgEl ? (imgEl.getAttribute('alt') || '') : '';
        const text = (best.innerText || '').trim();

        // Try to get product URL
        let href = '';
        const aTag = best.querySelector('a') || best.closest('a');
        if (aTag) href = aTag.getAttribute('href') || '';

        out.push({
          card_text: text,
          image_alt: alt,
          image_url_raw: src,
          product_href: href,
        });
      }
      return out;
    }
    """)


def choose_best_name(card_text: str, image_alt: str) -> str:
    lines = [clean(x) for x in clean(card_text).split("\n") if clean(x)]
    bad_tokens = ["₪", 'ש"ח', "הוסף", "לרשימה", "מבצע", "מחיר", "קנה", "100 מ"]

    candidates = [
        line for line in lines
        if len(line) >= 4 and not any(b in line for b in bad_tokens)
    ]

    # Prefer lines that include olive oil signals
    for line in candidates:
        if any(sig in line for sig in ["שמן זית", "olive oil", "כתית"]):
            return line

    if candidates:
        return candidates[0]

    return clean(image_alt)


def discover_query(page, query: str) -> list[dict]:
    print(f"\n--- Query: {query} ---")
    url = f"{BASE_URL}/category?search={quote(query)}"
    page.goto(url, wait_until="networkidle", timeout=60_000)
    page.wait_for_timeout(3_000)
    close_cookie_popup(page)

    products: dict[str, dict] = {}
    stable_rounds = 0
    last_count = 0

    for round_no in range(1, 100):
        raw_cards = extract_product_cards(page)

        for c in raw_cards:
            combined = clean(
                f"{c.get('card_text','')} {c.get('image_alt','')} {c.get('image_url_raw','')}"
            )
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
                    "brand": infer_brand(combined),
                    "query": query,
                    "card_text": c.get("card_text", ""),
                    "image_alt": c.get("image_alt", ""),
                    "image_url_raw": c.get("image_url_raw", ""),
                    "product_href": c.get("product_href", ""),
                    "discovered_at": now_iso(),
                }

        current_count = len(products)
        print(f"  Round {round_no}: {current_count} products")

        if current_count == last_count:
            stable_rounds += 1
        else:
            stable_rounds = 0
            last_count = current_count

        if stable_rounds >= 15:
            print(f"  Stable for {stable_rounds} rounds — done")
            break

        page.mouse.wheel(0, 900)
        page.wait_for_timeout(800)

    print(f"  Query '{query}': found {len(products)} candidates")
    return list(products.values())


def write_outputs(all_products: list[dict]) -> None:
    # Deduplicate by barcode or key
    deduped: dict[str, dict] = {}
    for p in all_products:
        key = p.get("barcode") or p.get("key")
        if key and key not in deduped:
            decision, reason = candidate_decision(p)
            p["suggested_decision"] = decision
            p["decision_reason"] = reason
            deduped[key] = p

    rows = list(deduped.values())
    approved = [r for r in rows if r["suggested_decision"] == "YES"]

    save_json(OUTPUT_DIR / "all_discovered_raw.json", rows)
    save_json(OUTPUT_DIR / "approved_candidates.json", approved)

    # Also write CSV for manual review
    csv_path = OUTPUT_DIR / "candidate_review.csv"
    fields = [
        "suggested_decision", "decision_reason", "barcode", "name",
        "brand", "query", "card_text", "image_alt", "product_href",
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

    print("\n" + "=" * 60)
    print(f"Discovery complete.")
    print(f"  Total unique candidates: {len(rows)}")
    print(f"  Auto-approved (olive oil): {len(approved)}")
    print(f"  Raw JSON:   {OUTPUT_DIR / 'all_discovered_raw.json'}")
    print(f"  Approved:   {OUTPUT_DIR / 'approved_candidates.json'}")
    print(f"  CSV review: {csv_path}")
    print("=" * 60)
    print("\nNext step: run 02_scrape_yohananof_olive_oil.py")


def main() -> None:
    all_products: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        for query in SEARCH_QUERIES:
            all_products.extend(discover_query(page, query))

        browser.close()

    write_outputs(all_products)


if __name__ == "__main__":
    main()
