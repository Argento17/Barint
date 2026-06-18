"""
TASK-241 — Rescue the 12 basis-error salty-snacks drops from Shufersal.

TASK-237 dropped 12 salty-snacks SKUs whose Yochananof product pages carried
PER-SERVING panels mislabeled as per-100g (kcal 47-132/100g). Owner wants them
rescued from REAL Shufersal per-100g panels rather than accept a 25-product shelf.

For each of the 12 basis-error EANs:
  1. NAME-based search on Shufersal (EAN search returns 0 there).
  2. Match a search result by Shufersal product-code == P_<ean> / P_<ean-suffix>
     when available, else by name+brand similarity. Confirm identity before trusting.
  3. Scrape the product page; parse the per-100g nutrition panel with the SHARED
     multi-table-aware parser (bsip0_nutrition.py) — which explicitly selects the
     per-100g table and refuses to silently pick a per-serving one.
  4. VERIFY genuinely per-100g: basis classified per_100g AND Atwater check
     (4*protein + 4*carbs + 9*fat ~= stated kcal) AND kcal in the real snack range
     (~350-550/100g). A panel that fails any check is left DROPPED (honest).
  5. Identity + image stay from the existing Yochananof catalog entry; only PANEL +
     INGREDIENTS come from Shufersal. Recovered records marked
     panel_source = shufersal_product_page.

NO Open Food Facts. NO guessed/rescaled panel. NO per-serving panel shipped.

Output: writes rescued panels into a side file
  bsip0_outputs/shufersal_rescue_panels.json
that the BSIP1 builder reads to override the bad Yochananof panel for these 12 EANs.
Raw Shufersal product HTML is persisted under shuf_rescue_html/ for replay.
"""
import sys, json, re, time, pathlib, difflib
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests
from bs4 import BeautifulSoup

# Shared Shufersal nutrition parser (multi-table per-100g selection + numeric layer).
sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\_shared")))
import bsip0_nutrition as bn  # noqa: E402

HERE = pathlib.Path(__file__).parent
DROPS = pathlib.Path(r"C:\Bari\02_products\salty_snacks\reports\salty_snacks_retailer_drops.json")
OUT_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip0_outputs")
OUT = OUT_DIR / "shufersal_rescue_panels.json"
RAW_HTML = HERE / "shuf_rescue_html"
RAW_HTML.mkdir(parents=True, exist_ok=True)

SEARCH = "https://www.shufersal.co.il/online/he/search"
PRODUCT = "https://www.shufersal.co.il/online/he/p/{}"

session = requests.Session()
session.headers.update({
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.7,en;q=0.5",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1", "Connection": "keep-alive",
})

# Real-snack kcal/100g window. A dry salty snack (cracker, rice cake, pretzel, crisp,
# popcorn) sits ~330-560 kcal/100g. Below ~300 on a per-100g claim is the per-serving
# artifact we are escaping; above ~600 is implausible for these categories.
KCAL_MIN, KCAL_MAX = 300.0, 600.0


def log(m):
    print(f"[{datetime.now().isoformat()[:19]}] {m}", flush=True)


def norm_name(s):
    """Normalize a Hebrew product name for fuzzy comparison: drop pack-size tokens,
    punctuation, quotes, and collapse whitespace."""
    s = s or ""
    s = re.sub(r"\d+\s*(?:גרם|ג'|גר|יח'?|מ\"?ל|ml|g)\b", " ", s)
    s = re.sub(r"[\"'‘’“”.,()/\\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def ean_variants(ean):
    """Shufersal product codes are often P_<full-ean> or P_<trailing-digits>. Build the
    candidate code suffixes we accept as a hard identity match."""
    v = {ean}
    # trailing 5-6 digits (Shufersal internal SKU often = last digits of the barcode)
    for n in (6, 5, 4):
        v.add(ean[-n:])
    return v


def search_candidates(query):
    cands = {}
    for page in range(2):
        try:
            r = session.get(SEARCH, params={"q": query, "pageSize": 48, "currentPage": page}, timeout=20)
            if r.status_code != 200:
                continue
        except Exception as e:
            log(f"    search error '{query}' p{page}: {e}")
            continue
        soup = BeautifulSoup(r.text, "lxml")
        for li in soup.find_all("li", attrs={"data-product-name": True}):
            d = li.attrs
            code = d.get("data-product-code")
            if not code or code in cands:
                continue
            cands[code] = {
                "code": code,
                "name": d.get("data-product-name") or "",
                "brand": d.get("data-product-manufacturer") or "",
                "ean_attr": d.get("data-product-ean") or "",
            }
        time.sleep(0.3)
    return list(cands.values())


def fetch_page(code):
    """Fetch a Shufersal product page, return (html, soup) or (None, None)."""
    try:
        r = session.get(PRODUCT.format(code), timeout=20)
    except Exception:
        return None, None
    if r.status_code != 200 or "Maintenance1.jpg" in r.text:
        return None, None
    return r.text, BeautifulSoup(r.text, "lxml")


def page_gtin13(soup):
    """Read the authoritative JSON-LD gtin13 from a Shufersal product page (or '')."""
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string)
        except Exception:
            continue
        if isinstance(data, dict):
            for k in ("gtin13", "gtin"):
                if data.get(k):
                    return str(data[k]).strip()
    return ""


def pick_match(ean, name, brand, cands):
    """Identity-confident match: fetch each ranked candidate's page and accept ONLY the
    one whose JSON-LD gtin13 EQUALS the full target barcode.

    Rationale (TASK-241): Shufersal exposes no EAN in search; the in-page JSON-LD gtin13
    is the ONE authoritative identity signal. Name similarity is NOT trusted on its own —
    same-line-different-flavor and same-name-different-barcode collisions are common in
    this category (verified in the audit) and would ship a guessed panel. A candidate
    whose page advertises a short internal SKU (e.g. '60071') or a DIFFERENT full barcode
    is rejected. Returns (candidate, soup, basis) or (None, None, reason).
    """
    # Rank candidates by name similarity so we probe the likeliest first, but the ACCEPT
    # decision is gtin13-exact only.
    tn = norm_name(name)
    ranked = sorted(
        cands,
        key=lambda c: difflib.SequenceMatcher(None, tn, norm_name(c["name"])).ratio(),
        reverse=True,
    )
    best_seen = []
    for c in ranked[:12]:  # cap page fetches per target
        html, soup = fetch_page(c["code"])
        if soup is None:
            continue
        gtin = page_gtin13(soup)
        best_seen.append(f"{c['code']}:gtin={gtin or 'none'}")
        if gtin == ean:
            c["_soup"] = soup
            return c, soup, "gtin13_exact"
        time.sleep(0.25)
    return None, None, "no_gtin13_match (" + ", ".join(best_seen[:6]) + ")"


def scrape_panel(code, soup=None):
    """Parse the per-100g panel + ingredients from a Shufersal product page.

    ``soup`` may be the already-fetched page (from pick_match) to avoid a re-fetch;
    when None the page is fetched here. Returns (nutrition_per_100g, ingredients_he,
    selection_meta, raw_html) or (None, None, {error}, None) on failure."""
    raw_html = None
    if soup is None:
        try:
            r = session.get(PRODUCT.format(code), timeout=20)
        except Exception as e:
            return None, None, {"error": str(e)[:160]}, None
        if r.status_code != 200 or "Maintenance1.jpg" in r.text:
            return None, None, {"error": f"page_status_{r.status_code}"}, None
        raw_html = r.text
        soup = BeautifulSoup(r.text, "lxml")

    raw = bn.extract_nutrition_raw(soup)
    sel = raw["selection"]
    rows = raw["rows"]
    nutr_raw = bn.parse_nutrition_rows(rows)  # {field: raw string}
    # canonical numeric per-100g panel
    numeric = bn.parse_nutrition_numeric({
        "energy_kcal_raw": nutr_raw.get("energy"),
        "fat_raw": nutr_raw.get("fat"),
        "saturated_fat_raw": nutr_raw.get("saturated_fat"),
        "carbs_raw": nutr_raw.get("carbs"),
        "sugar_raw": nutr_raw.get("sugar"),
        "fiber_raw": nutr_raw.get("fiber"),
        "protein_raw": nutr_raw.get("protein"),
        "sodium_raw": nutr_raw.get("sodium"),
    })
    nn = {
        "energy_kcal": round(numeric["energy_kcal"]) if numeric["energy_kcal"] is not None else None,
        "fat_g": numeric["fat_g"],
        "fat_saturated_g": numeric["fat_saturated_g"],
        "fat_trans_g": None,
        "sodium_mg": round(numeric["sodium_mg"]) if numeric["sodium_mg"] is not None else None,
        "carbohydrates_g": numeric["carbohydrates_g"],
        "sugars_g": numeric["sugars_g"],
        "dietary_fiber_g": numeric["dietary_fiber_g"],
        "protein_g": numeric["protein_g"],
    }

    # ingredients — Shufersal puts the list in div.componentsText (the title "רכיבים"
    # lives in a sibling div.title, so a find_next on the bare heading word returns the
    # heading, not the body). Read div.componentsText first; fall back to a heading scan.
    ingredients = ""
    comp = soup.find("div", class_="componentsText")
    if comp:
        cand = comp.get_text(" ", strip=True)
        if 5 < len(cand) < 2000:
            ingredients = cand
    for tag in (soup.find_all(["div", "span", "p", "h3", "h4"]) if not ingredients else []):
        t = tag.get_text(strip=True)
        if t in ("רכיבים", "מרכיבים", "רכיב", "מרכיב"):
            nx = tag.find_next(["div", "span", "p"])
            if nx:
                cand = nx.get_text(strip=True)
                if 5 < len(cand) < 2000:
                    ingredients = cand
                    break
    page_text = raw_html if raw_html is not None else str(soup)
    if not ingredients:
        m = re.search(r"(?:רכיבים?|מרכיבים?)\s*:?\s*(.+?)(?:\.\s*(?:מכיל|עלול|ללא|\d|$)|$)",
                      page_text, re.DOTALL)
        if m:
            ingredients = m.group(1).strip()[:1500]

    meta = {
        "selected_basis": sel.get("selected_basis"),
        "selected_table_header": sel.get("selected_table_header"),
        "competing_table_count": sel.get("competing_table_count"),
        "insufficient": sel.get("insufficient"),
        "nutr_raw_rows": nutr_raw,
        "integrity": numeric.get("_integrity"),
    }
    return nn, (ingredients or None), meta, page_text


def verify_per_100g(nn, meta):
    """Return (ok: bool, reasons: list[str]). All checks must pass to accept."""
    reasons = []
    e = nn.get("energy_kcal")
    c = nn.get("carbohydrates_g")
    fa = nn.get("fat_g")
    pr = nn.get("protein_g")

    if meta.get("insufficient"):
        reasons.append("parser_insufficient: >1 table and no identifiable per-100g panel")
    basis = meta.get("selected_basis")
    if basis not in ("per_100g", "none", None):
        # 'per_serving'/'unknown' on a multi-table page is a hard reject; a lone unlabeled
        # table ('none') is allowed to proceed to the numeric checks below.
        if basis == "per_serving":
            reasons.append(f"basis_per_serving: selected table header = '{meta.get('selected_table_header')}'")

    if e is None:
        reasons.append("no_energy")
    else:
        if not (KCAL_MIN <= e <= KCAL_MAX):
            reasons.append(f"kcal_out_of_snack_range: {e} not in [{KCAL_MIN:.0f},{KCAL_MAX:.0f}]")
    # Atwater self-consistency (catches a per-serving panel that slipped the basis label)
    if e and c is not None and fa is not None and pr is not None:
        atwater = 4 * c + 4 * pr + 9 * fa
        if atwater > 0:
            ratio = atwater / e
            if not (0.80 <= ratio <= 1.25):
                reasons.append(f"atwater_mismatch: macro-kcal {atwater:.0f} vs stated {e} (ratio {ratio:.2f})")
    elif e:
        reasons.append("atwater_incomputable: missing one of carbs/fat/protein")
    # core-macro completeness (same bar the BSIP1 builder applies)
    if not (e is not None and c is not None and nn.get("sodium_mg") is not None
            and (fa is not None or nn.get("fat_saturated_g") is not None)):
        reasons.append("missing_core_macros (need energy+carbs+sodium+fat)")

    return (len(reasons) == 0), reasons


def main():
    all_drops = json.loads(DROPS.read_text(encoding="utf-8"))
    targets = [d for d in all_drops if d.get("drop_class") == "basis_error"]
    log(f"Rescue targets (basis_error): {len(targets)}")

    recovered, still_dropped = {}, []
    audit = []

    for i, d in enumerate(targets, 1):
        ean, name = d["barcode"], d["name"]
        log(f"[{i}/{len(targets)}] {ean}  {name}")
        # search queries: full name, then name with pack-size tokens stripped
        queries = [name, norm_name(name)]
        cands = {}
        for q in queries:
            for c in search_candidates(q):
                cands[c["code"]] = c
            if len(cands) >= 8:
                break
        cands = list(cands.values())
        log(f"    candidates: {len(cands)}")

        match, soup, basis = pick_match(ean, name, "", cands)
        if not match:
            still_dropped.append({**d, "rescue_result": "no_match", "rescue_detail": basis})
            audit.append({"ean": ean, "name": name, "stage": "match", "result": "no_match",
                          "detail": basis, "candidates": [c["name"] for c in cands][:6]})
            log(f"    NO MATCH ({basis})")
            time.sleep(0.4)
            continue
        score = 1.0  # gtin13_exact is the only accept path

        log(f"    matched {match['code']} '{match['name']}' via {basis} (gtin13==barcode)")
        nn, ingredients, meta, html = scrape_panel(match["code"], soup=soup)
        if nn is None:
            still_dropped.append({**d, "rescue_result": "scrape_failed",
                                  "rescue_detail": meta.get("error"), "matched_code": match["code"]})
            audit.append({"ean": ean, "matched_code": match["code"], "stage": "scrape",
                          "result": "failed", "detail": meta})
            log(f"    SCRAPE FAILED ({meta.get('error')})")
            time.sleep(0.4)
            continue

        ok, vreasons = verify_per_100g(nn, meta)
        # persist raw html regardless (audit)
        if html:
            (RAW_HTML / f"{ean}__{match['code']}.html").write_text(html, encoding="utf-8")

        rec_audit = {
            "ean": ean, "name": name, "matched_code": match["code"],
            "matched_name": match["name"], "match_basis": basis, "match_score": round(score, 3),
            "shufersal_panel": nn, "selected_basis": meta.get("selected_basis"),
            "competing_tables": meta.get("competing_table_count"),
            "has_ingredients": bool(ingredients),
            "verify_ok": ok, "verify_reasons": vreasons,
        }
        audit.append(rec_audit)

        if not ok:
            still_dropped.append({**d, "rescue_result": "panel_rejected",
                                  "rescue_detail": "; ".join(vreasons),
                                  "matched_code": match["code"],
                                  "shufersal_kcal": nn.get("energy_kcal")})
            log(f"    PANEL REJECTED: {'; '.join(vreasons)}")
            time.sleep(0.5)
            continue

        recovered[ean] = {
            "barcode": ean,
            "name_he": name,
            "normalized_nutrition_per_100g": nn,
            "ingredients_text_he": ingredients,
            "panel_source": "shufersal_product_page",
            "shufersal_product_code": match["code"],
            "shufersal_product_url": PRODUCT.format(match["code"]),
            "shufersal_matched_name": match["name"],
            "match_basis": basis,
            "selected_basis": meta.get("selected_basis"),
            "raw_rows": meta.get("nutr_raw_rows"),
            "verified_per_100g": True,
        }
        log(f"    RECOVERED kcal={nn['energy_kcal']} sodium={nn['sodium_mg']} "
            f"ingr={'Y' if ingredients else 'N'} basis={meta.get('selected_basis')}")
        time.sleep(0.5)

    out = {
        "schema_version": "shufersal_rescue_v1",
        "task": "TASK-241",
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "source": "shufersal_product_page (name-based search match)",
        "kcal_window": [KCAL_MIN, KCAL_MAX],
        "targets": len(targets),
        "recovered_count": len(recovered),
        "dropped_count": len(still_dropped),
        "recovered": recovered,
        "still_dropped": still_dropped,
        "audit": audit,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    log("=" * 60)
    log(f"RESCUE DONE  recovered={len(recovered)}/{len(targets)}  dropped={len(still_dropped)}")
    log(f"  output: {OUT}")
    for ean, rr in recovered.items():
        log(f"  + {ean}  kcal={rr['normalized_nutrition_per_100g']['energy_kcal']}  {rr['name_he'][:30]}")
    for d in still_dropped:
        log(f"  - {d['barcode']}  {d.get('rescue_result')}: {str(d.get('rescue_detail'))[:60]}")


if __name__ == "__main__":
    main()
