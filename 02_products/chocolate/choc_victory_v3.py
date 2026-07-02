"""
Victory Playwright scrape v3 — final attempt.

KEY FIXES vs previous:
1. Image URL uses productId/imageId (NOT barcode) → fix locators
2. Shorter scroll timeout (200ms not 400ms)
3. Also try the CDN GS1 URL pattern with barcode (fallback, as some stores use it)
4. Directly target Victory product modal via AngularJS $state pattern

From /api/products/ we confirmed:
  - Millennium 80%: productId=415280, imageId=1801293
  - Lindt dark: productId=7872576, imageId=12115254
  - Lindt caramel: productId=7872575, imageId=12115260
  - Lindt milk: productId=7872574, imageId=12115258
  - Lindt 70%: productId=6181, imageId=943727
  - Millennium 74%: productId=324953, imageId=1801292
  - 75% dark: productId=817732, imageId=12517516
  - 62% dark: productId=7630501, imageId=11956111

Image URL = d226b0iufwcjmj.cloudfront.net/product-images/global/{productId}/{imageId}/large.png
"""
import sys, re, json, pathlib, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

VICTORY_BASE = "https://www.victoryonline.co.il"
RETAILER_ID = 1470
BRANCH_ID = 2930

TARGETS = {
    "4820005195848": {"api_id": 415280,  "imageId": 1801293,  "label": "Millennium 80%"},
    "3046920023443": {"api_id": 7872576, "imageId": 12115254, "label": "Lindt Excellence dark"},
    "3046920023429": {"api_id": 7872575, "imageId": 12115260, "label": "Lindt caramel milk"},
    "3046920023368": {"api_id": 7872574, "imageId": 12115258, "label": "Lindt Excellence milk"},
    "3046920028004": {"api_id": 6181,    "imageId": 943727,   "label": "Lindt 70%"},
    "4820005198597": {"api_id": 324953,  "imageId": 1801292,  "label": "Millennium 74%"},
    "5941021001261": {"api_id": 817732,  "imageId": 12517516, "label": "75% dark"},
    "7290119500482": {"api_id": 7630501, "imageId": 11956111, "label": "62% dark"},
}

target_pids  = {v["api_id"] for v in TARGETS.values()}
bc_by_pid    = {v["api_id"]: bc for bc, v in TARGETS.items()}
info_by_pid  = {v["api_id"]: v for v in TARGETS.values()}

LABEL_MAP = [
    (["טראנס", "trans"], "trans_fat"),
    (["רווי", "saturated"], "saturated_fat"),
    (["סוכר", "sugar"], "sugar"),
    (["פחמימ", "carb"], "carbs"),
    (["סיב", "fiber"], "fiber"),
    (["חלבונ", "protein"], "protein"),
    (["נתרן", "sodium"], "sodium"),
    (["אנרגי", "קלורי", "kcal", "energy", "calorie"], "energy"),
    (["שומנ", "fat"], "fat"),
]

def parse_nutr_table(html: str) -> dict:
    from bs4 import BeautifulSoup as BS
    soup = BS(html, "html.parser")
    table = soup.find("table")
    if not table:
        return {}
    result, seen = {}, set()
    for row in table.find_all("tr"):
        th, td = row.find("th"), row.find("td")
        if not th or not td:
            continue
        label = th.get_text(strip=True)
        m = re.search(r"([\d,.]+)", td.get_text(strip=True))
        if not m:
            continue
        try:
            val = float(m.group(1).replace(",", "."))
        except ValueError:
            continue
        for tokens, canon in LABEL_MAP:
            if canon in seen:
                continue
            if any(t in label or t in label.lower() for t in tokens):
                if canon in ("fat", "carbs") and "מתוכ" in label:
                    continue
                result[canon] = val
                seen.add(canon)
                break
    return result

def parse_nutr_json(nv: dict) -> dict:
    if not isinstance(nv, dict):
        return {}
    sizes = nv.get("sizes") or []
    values = nv.get("values") or []
    col_idx = 0
    for i, sz in enumerate(sizes):
        nm = sz.get("names") or {}
        sz_name = nm.get("1") or nm.get(1) or ""
        if isinstance(sz_name, dict):
            sz_name = sz_name.get("name", "")
        if "100" in (sz_name or ""):
            col_idx = i
            break
    result, seen = {}, set()
    for row in values:
        nm = row.get("names") or {}
        label = nm.get("1") or nm.get(1) or ""
        if isinstance(label, dict):
            label = label.get("name", "")
        sv_list = row.get("sizeValues") or []
        if col_idx >= len(sv_list):
            continue
        sv = sv_list[col_idx]
        val = sv.get("value") if isinstance(sv, dict) else sv
        try:
            val = float(str(val).replace(",", "."))
        except (ValueError, TypeError):
            continue
        ll = (label or "").lower()
        for tokens, canon in LABEL_MAP:
            if canon in seen:
                continue
            if any(t in (label or "") or t in ll for t in tokens):
                if canon in ("fat", "carbs") and "מתוכ" in (label or ""):
                    continue
                result[canon] = val
                seen.add(canon)
                break
    return result

def parse_ingr_html(html: str) -> str:
    from bs4 import BeautifulSoup as BS
    soup = BS(html, "html.parser")
    txt = soup.get_text(separator=" ", strip=True)
    m = re.search(r"רכיב[ים:]*\s*[:]?\s*(.*)", txt, re.DOTALL)
    if m:
        return m.group(1).strip()[:1400]
    return ""

def is_boilerplate(s: str) -> bool:
    if not s:
        return True
    if any(w in s for w in ["קקאו", "סוכר", "חלב", "לציטין", "שומן", "שקדים", "ריבה", "קמח"]):
        return False
    return True

# ── XHR capture ─────────────────────────────────────────────────────────────
found_products: dict[int, dict] = {}

def handle_response(response):
    url = response.url
    if "victoryonline" not in url:
        return
    if ("branches" not in url and "product" not in url.lower()):
        return
    try:
        ct = response.headers.get("content-type", "")
        if "json" not in ct:
            return
        body = response.body()
        if len(body) < 200:
            return
        text = body.decode("utf-8", errors="replace")
        if '"products"' not in text and "productId" not in text:
            return
        data = json.loads(text)
        prods = data.get("products") or []
        # Also check single-product responses
        if "productId" in data:
            prods.append(data)
        for p in prods:
            pid = p.get("productId") or p.get("id")
            if pid in target_pids and pid not in found_products:
                found_products[pid] = p
                label = info_by_pid[pid]["label"]
                nv = p.get("nutritionValues") or {}
                nv_vals = (nv.get("values") or []) if isinstance(nv, dict) else []
                d = p.get("data") or {}
                l1 = d.get("1") or d.get(1) or {}
                ingr = (l1.get("ingredients") or "") if isinstance(l1, dict) else ""
                print(f"  [XHR FOUND] pid={pid} {label} | nutr_rows={len(nv_vals)} | ingr={len(ingr)}ch", flush=True)
    except Exception:
        pass

# ── Helper: dismiss popups ───────────────────────────────────────────────────
def dismiss(page):
    for sel in ['button:has-text("אישור")', 'button:has-text("מסכים")', 'button:has-text("הבנתי")',
                '[aria-label="סגור"]', '.cookie-wall button']:
        try:
            b = page.locator(sel).first
            if b.is_visible(timeout=300):
                b.click(force=True)
                page.wait_for_timeout(200)
        except Exception:
            pass

# ── Main ─────────────────────────────────────────────────────────────────────
print("=== Victory scrape v3 ===", flush=True)
modal_scraped: dict[str, dict] = {}  # bc -> {nutrition, ingredients, name}

SEARCH_QUERIES = [
    "שוקולד מריר",        # broad — will yield many dark chocolates
    "שוקולד לינדט",       # lindt
    "לינדט",              # lindt (shorter)
    "שוקולד מריר 80",     # 80%
    "שוקולד מריר 75",     # 75%
    "שוקולד מריר 74",     # 74%
    "שוקולד מריר 62",     # 62%
]

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1600, "height": 900},
        locale="he-IL",
        extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    page.on("response", handle_response)

    # ── Phase 1: Broad XHR harvesting ─────────────────────────────────────────
    print("\nPhase 1: XHR harvesting", flush=True)
    for q in SEARCH_QUERIES:
        if len(found_products) >= len(TARGETS):
            break
        from urllib.parse import quote as _q
        url = f"{VICTORY_BASE}/category?search={_q(q)}"
        print(f"  Search: {q!r}", flush=True)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=40000)
            page.wait_for_timeout(5000)
            dismiss(page)
        except Exception as e:
            print(f"  ERROR goto: {e}", flush=True)
            continue

        # Scroll fast to load all products
        for _ in range(60):
            page.mouse.wheel(0, 1200)
            page.wait_for_timeout(200)

        print(f"  Found so far: {len(found_products)}/{len(TARGETS)}", flush=True)

    print(f"\nAfter Phase 1: {len(found_products)}/{len(TARGETS)} found via XHR", flush=True)

    # ── Phase 2: Click-and-modal for remaining targets ─────────────────────────
    remaining_bcs = [bc for bc, info in TARGETS.items() if info["api_id"] not in found_products]
    print(f"\nPhase 2: {len(remaining_bcs)} still needed — click-and-modal", flush=True)

    for bc in remaining_bcs:
        info = TARGETS[bc]
        api_id = info["api_id"]
        image_id = info["imageId"]
        label = info["label"]
        print(f"\n  Target: {bc} | {label}", flush=True)

        search_candidates = [
            bc,              # barcode search
            "שוקולד מריר",   # broad search
            label,
        ]
        found_in_phase2 = False

        for search_q in search_candidates:
            from urllib.parse import quote as _q
            url = f"{VICTORY_BASE}/category?search={_q(search_q)}"
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=40000)
                page.wait_for_timeout(5000)
                dismiss(page)
            except Exception:
                continue

            clicked = False
            for scroll_i in range(200):
                # Look by imageId in src (the CORRECT pattern for Victory)
                # URL = ...cloudfront.net/product-images/global/{productId}/{imageId}/large.png
                for img_frag in [str(image_id), str(api_id)]:
                    try:
                        loc = page.locator(f'img[src*="{img_frag}"]').first
                        if loc.count() > 0:
                            print(f"    Found via img frag [{img_frag}] at scroll={scroll_i}", flush=True)
                            loc.scroll_into_view_if_needed(timeout=2000)
                            page.wait_for_timeout(500)
                            loc.click(force=True)
                            page.wait_for_timeout(5000)
                            clicked = True
                            break
                    except Exception:
                        pass
                if clicked:
                    break

                page.mouse.wheel(0, 900)
                page.wait_for_timeout(200)

                if scroll_i % 50 == 49:
                    print(f"    Scroll {scroll_i+1}/200...", flush=True)

            if clicked:
                # Extract from modal
                dialog = page.locator('[role="dialog"]').first
                if dialog.count() > 0:
                    name = ""
                    try:
                        h = dialog.locator("h1, h2, [class*='name']").first
                        name = h.inner_text(timeout=1000).strip()
                    except Exception:
                        pass

                    ingr = ""
                    try:
                        tab = dialog.get_by_role("tab", name="רכיבים").first
                        if tab.count() > 0:
                            tab.click(force=True)
                            page.wait_for_timeout(2000)
                            ingr = parse_ingr_html(dialog.inner_html(timeout=2000))
                    except Exception:
                        pass

                    nutr = {}
                    try:
                        tab = dialog.get_by_role("tab", name="ערכים תזונתיים").first
                        if tab.count() > 0:
                            tab.click(force=True)
                            page.wait_for_timeout(2500)
                            nutr = parse_nutr_table(dialog.inner_html(timeout=2000))
                    except Exception:
                        pass

                    modal_scraped[bc] = {"name": name, "nutrition": nutr, "ingredients": ingr}
                    print(f"    Modal: name={name!r} nutr_keys={list(nutr.keys())} ingr={ingr[:80]!r}", flush=True)
                    found_in_phase2 = True
                    break

                page.keyboard.press("Escape")
                page.wait_for_timeout(500)

        if not found_in_phase2 and bc not in modal_scraped:
            print(f"    NOT FOUND after all search strategies", flush=True)

    context.close()
    browser.close()

# ── Assemble ─────────────────────────────────────────────────────────────────
print(f"\n=== Results: XHR={len(found_products)} modal={len(modal_scraped)} ===", flush=True)

results = {}
for bc, info in TARGETS.items():
    pid = info["api_id"]

    if pid in found_products:
        p = found_products[pid]
        nutr = parse_nutr_json(p.get("nutritionValues") or {})
        d = p.get("data") or {}
        l1 = d.get("1") or d.get(1) or {}
        ingr = (l1.get("ingredients") or "") if isinstance(l1, dict) else ""
        bplate = is_boilerplate(ingr)
        results[bc] = {
            "barcode": bc, "label": info["label"],
            "status": "SCRAPED_VIA_XHR", "source": "victory",
            "product_name_victory": p.get("localName", ""),
            "nutrition": nutr, "ingredients": ingr or None,
            "ingredients_status": "REAL_INGREDIENTS" if ingr and not bplate else ("BOILERPLATE" if ingr else "NULL"),
            "has_full_nutrition": bool(nutr.get("energy") and nutr.get("fat") and nutr.get("carbs")),
        }
    elif bc in modal_scraped:
        md = modal_scraped[bc]
        nutr, ingr = md["nutrition"], md.get("ingredients") or ""
        bplate = is_boilerplate(ingr)
        results[bc] = {
            "barcode": bc, "label": info["label"],
            "status": "SCRAPED_VIA_MODAL", "source": "victory",
            "product_name_victory": md.get("name", ""),
            "nutrition": nutr, "ingredients": ingr or None,
            "ingredients_status": "REAL_INGREDIENTS" if ingr and not bplate else ("BOILERPLATE" if ingr else "NULL"),
            "has_full_nutrition": bool(nutr.get("energy") and nutr.get("fat") and nutr.get("carbs")),
        }
    else:
        results[bc] = {
            "barcode": bc, "label": info["label"],
            "status": "NOT_FOUND_ON_VICTORY", "source": "victory",
            "product_name_victory": None,
            "nutrition": None, "ingredients": None,
            "ingredients_status": "NULL", "has_full_nutrition": False,
        }

# Plausibility
def plaus(n):
    if not n:
        return "NOT_APPLICABLE"
    e, f, c, p = n.get("energy",0), n.get("fat",0), n.get("carbs",0), n.get("protein",0)
    s, so = n.get("sugar",0), n.get("saturated_fat",0)
    if not (400 <= e <= 700):
        return f"FAIL:energy={e}"
    if not (20 <= f <= 65):
        return f"FAIL:fat={f}"
    if not (0 <= c <= 65):
        return f"FAIL:carbs={c}"
    ms = f + c + p
    if not (55 <= ms <= 110):
        return f"FAIL:macro_sum={ms}"
    if s > c + 2:
        return f"FAIL:sugar({s})>carbs({c})"
    if so > f + 0.5:
        return f"FAIL:satfat({so})>fat({f})"
    if not {"energy","fat","carbs"}.issubset(n):
        return "FAIL:incomplete_panel"
    return "PASS"

for r in results.values():
    r["plausibility_gate"] = plaus(r["nutrition"])

# Score
try:
    import sys as _sys
    _sys.path.insert(0, str(pathlib.Path(r"C:\Bari\02_products\chocolate")))
    import run_task360_phase3 as P3
    scorer_ok = True
    print("Scorer loaded", flush=True)
except ImportError as e:
    scorer_ok = False
    print(f"Scorer unavailable: {e}", flush=True)

for bc, r in results.items():
    if not r["nutrition"] or r["plausibility_gate"] not in ("PASS",) or not scorer_ok:
        r["score"] = None; r["grade"] = None
        continue
    try:
        bsip1 = P3.build_bsip1(
            barcode=bc,
            name=r.get("product_name_victory") or bc,
            nutrition=r["nutrition"],
            ingredients=r.get("ingredients") or "",
            source="victory_pass2",
        )
        scored = P3.run_bsip2(bsip1)
        r["score"] = scored.get("score")
        r["grade"] = scored.get("grade")
        print(f"  {bc}: score={r['score']} grade={r['grade']}", flush=True)
    except Exception as e:
        r["score"] = None; r["grade"] = None
        print(f"  {bc}: scoring error {e}", flush=True)

# OFF check
off_fields = [f"{bc}.{k}" for bc, r in results.items() for k, v in r.items()
              if isinstance(v, str) and "openfoodfacts" in v.lower()]
off_status = "PASS" if not off_fields else f"FAIL:{off_fields}"

# Write
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
out_path = pathlib.Path(r"C:\Bari\02_products\chocolate") / f"choc_tablets_fix_task366b_{ts}.json"
payload = {
    "task": "TASK-366 Pass 2 Victory probe",
    "run_ts": ts,
    "retailer": "victory",
    "branch_id": BRANCH_ID,
    "off_check": off_status,
    "targets_attempted": len(TARGETS),
    "targets_with_full_nutrition": sum(1 for r in results.values() if r.get("has_full_nutrition")),
    "targets_with_real_ingredients": sum(1 for r in results.values() if r.get("ingredients_status") == "REAL_INGREDIENTS"),
    "plausibility_pass": sum(1 for r in results.values() if r.get("plausibility_gate") == "PASS"),
    "results": results,
}
out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"\n{'='*60}", flush=True)
print("FINAL SUMMARY", flush=True)
print(f"{'='*60}", flush=True)
for bc, r in results.items():
    print(f"  {bc} | {r['label']}: {r['status']} | plaus={r.get('plausibility_gate')} | ingr={r.get('ingredients_status')} | score={r.get('score')}", flush=True)
print(f"\nOFF check: {off_status}", flush=True)
print(f"Output: {out_path}", flush=True)
