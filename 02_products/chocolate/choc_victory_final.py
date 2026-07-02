"""
Final targeted Victory scrape for TASK-366 Pass 2.

Architecture confirmed:
1. /api/products/{barcode} → identity (id, imageId, filename)
2. CDN image URL includes barcode OR filename — need to confirm
3. Branch API requires browser session (403 without it)
4. All 8 targets are on Victory (confirmed via /api/products/{barcode})

Strategy:
- Use Playwright with response interception
- For each target, search by label keywords + try barcode search
- Intercept ALL branch API responses to find our targets by productId
- Also try clicking the product once found in search results
- Use Victory's angular $state params — product modal may be opened via URL hash
"""
import sys, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
import pathlib, datetime

VICTORY_BASE = "https://www.victoryonline.co.il"
RETAILER_ID = 1470
BRANCH_ID = 2930

# All confirmed-on-Victory target products
TARGETS = {
    "4820005195848": {"api_id": 415280,  "label": "Millennium 80%",          "imageId": 1801293},
    "3046920023443": {"api_id": 7872576, "label": "Lindt Excellence dark",    "imageId": None},
    "3046920023429": {"api_id": 7872575, "label": "Lindt caramel milk",       "imageId": None},
    "3046920023368": {"api_id": 7872574, "label": "Lindt Excellence milk",    "imageId": None},
    "3046920028004": {"api_id": 6181,    "label": "Lindt 70%",               "imageId": None},
    "4820005198597": {"api_id": 324953,  "label": "Millennium 74%",           "imageId": None},
    "5941021001261": {"api_id": 817732,  "label": "75% dark",                 "imageId": None},
    "7290119500482": {"api_id": 7630501, "label": "62% dark",                 "imageId": None},
}

target_pids = {v["api_id"] for v in TARGETS.values()}
bc_by_pid = {v["api_id"]: bc for bc, v in TARGETS.items()}
label_by_pid = {v["api_id"]: v["label"] for v in TARGETS.values()}

# ── Parsers ────────────────────────────────────────────────────────────────────
LABEL_MAP = [
    (["טראנס", "trans"], "trans_fat"),
    (["רווי", "saturated"], "saturated_fat"),
    (["סוכר", "sugar"], "sugar"),
    (["פחמימ", "carbohydrate"], "carbs"),
    (["סיב", "fiber"], "fiber"),
    (["חלבונ", "protein"], "protein"),
    (["נתרן", "sodium"], "sodium"),
    (["אנרגי", "קלורי", "kcal", "energy", "calorie"], "energy"),
    (["שומנ", "fat"], "fat"),
]

def parse_nutrition_table(html: str) -> dict:
    from bs4 import BeautifulSoup as BS
    soup = BS(html, "html.parser")
    # Victory modal: <section class="nutrition-values"><table>
    section = soup.find("section", class_=re.compile("nutrition", re.I))
    table = (section.find("table") if section else None) or soup.find("table")
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
        ll = label.lower()
        for tokens, canon in LABEL_MAP:
            if canon in seen:
                continue
            if any(t in label or t in ll for t in tokens):
                # Skip sub-rows ("מתוכ")
                if canon in ("fat", "carbs") and any(x in label for x in ["מתוכ", "מהם"]):
                    continue
                result[canon] = val
                seen.add(canon)
                break
    return result

def parse_nutrition_json(nv: dict) -> dict:
    """Parse nutritionValues JSON from the branch API response."""
    if not isinstance(nv, dict):
        return {}
    sizes = nv.get("sizes") or []
    values = nv.get("values") or []
    # Find per-100g column
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
                if canon in ("fat", "carbs") and any(x in (label or "") for x in ["מתוכ", "מהם"]):
                    continue
                result[canon] = val
                seen.add(canon)
                break
    return result

def parse_ingredients_from_html(html: str) -> str:
    from bs4 import BeautifulSoup as BS
    soup = BS(html, "html.parser")
    txt = soup.get_text(separator=" ", strip=True)
    m = re.search(r"רכיב[ים:]*\s*[:]?\s*(.*)", txt, re.DOTALL | re.UNICODE)
    if m:
        ingr = m.group(1).strip()[:1400]
        return ingr
    return ""

def is_boilerplate(s: str) -> bool:
    if not s:
        return True
    kw = any(w in s for w in ["קקאו", "סוכר", "חלב", "לציטין", "שומן", "שקדים"])
    if kw:
        return False
    # The boilerplate is "כפי שרשום על גבי האריזה עלול להכיל"
    if "כפי שרשום" in s or ("עלול להכיל" in s and not kw):
        return True
    return False

# ── XHR capture ────────────────────────────────────────────────────────────────
found_products: dict[int, dict] = {}  # api_id -> full product from XHR

def handle_response(response):
    url = response.url
    if "victoryonline" not in url:
        return
    if "branches" not in url and "products" not in url:
        return
    try:
        ct = response.headers.get("content-type", "")
        if "json" not in ct:
            return
        body = response.body()
        if len(body) < 500:
            return
        text = body.decode("utf-8", errors="replace")
        if '"products"' not in text:
            return
        data = json.loads(text)
        prods = data.get("products") or []
        for p in prods:
            pid = p.get("productId")
            if pid in target_pids and pid not in found_products:
                # Save this product
                found_products[pid] = p
                label = label_by_pid.get(pid, "")
                nv = p.get("nutritionValues") or {}
                nv_vals = (nv.get("values") or []) if isinstance(nv, dict) else []
                d = p.get("data") or {}
                l1 = d.get("1") or d.get(1) or {}
                ingr = (l1.get("ingredients") or "") if isinstance(l1, dict) else ""
                print(f"  [XHR] CAPTURED: pid={pid} {label} | nutr_rows={len(nv_vals)} | ingr={len(ingr)} chars", flush=True)
    except Exception:
        pass

# ── Main Playwright session ────────────────────────────────────────────────────
print("=== Victory targeted Playwright scrape ===", flush=True)

# Session-scraped results (modal HTML)
modal_results: dict[str, dict] = {}  # barcode -> {nutrition, ingredients, ...}

SEARCHES = [
    # broad chocolate searches that should return many products
    ("שוקולד מריר 80%",   "80%"),
    ("שוקולד לינדט",      "lindt"),
    ("לינדט שוקולד מריר", "lindt dark"),
    ("שוקולד מריר 74",    "74%"),
    ("שוקולד מריר 75",    "75%"),
    ("שוקולד מריר 62",    "62%"),
    ("שוקולד מריר",        "generic dark"),
    # barcode-based searches (Victory might support direct barcode search)
    ("4820005195848",     "bc millennium 80"),
    ("3046920023443",     "bc lindt dark"),
    ("3046920023368",     "bc lindt milk"),
    ("3046920023429",     "bc lindt caramel"),
]

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1600, "height": 900},
        locale="he-IL",
        extra_http_headers={"Accept-Language": "he-IL,he;q=0.9,en;q=0.8"},
        permissions=[],
    )
    page = context.new_page()
    page.on("response", handle_response)

    def dismiss():
        for sel in ['button:has-text("אישור")', 'button:has-text("מסכים")', 'button:has-text("הבנתי")',
                    '[aria-label="סגור"]', '[data-test="dialog-close"]', 'button.close']:
            try:
                b = page.locator(sel).first
                if b.is_visible(timeout=300):
                    b.click(force=True)
                    page.wait_for_timeout(300)
            except Exception:
                pass

    # ── Phase 1: Intercept XHR across multiple search pages ──
    print("\nPhase 1: XHR interception across search queries...", flush=True)
    for q, desc in SEARCHES:
        if len(found_products) == len(TARGETS):
            print(f"  All targets found via XHR!", flush=True)
            break
        from urllib.parse import quote as _q
        url = f"{VICTORY_BASE}/category?search={_q(q)}"
        print(f"  [{desc}] {url[:80]}", flush=True)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(6000)
            dismiss()
        except Exception as e:
            print(f"    GOTO error: {e}", flush=True)
            continue

        # Scroll to trigger lazy-load of more XHR calls
        for scroll_i in range(80):
            page.mouse.wheel(0, 1000)
            page.wait_for_timeout(400)

        print(f"    Found so far: {len(found_products)}/{len(TARGETS)}", flush=True)

    # ── Phase 2: For remaining targets, try clicking product cards ──
    remaining = [bc for bc, info in TARGETS.items() if info["api_id"] not in found_products]
    print(f"\nPhase 2: {len(remaining)} targets still missing — trying click-and-modal...", flush=True)

    for bc in remaining:
        info = TARGETS[bc]
        api_id = info["api_id"]
        label = info["label"]
        print(f"\n  {bc} | {label}", flush=True)

        # Try searching in a way that might surface this product
        search_options = [bc, label.split()[0] if " " in label else label]
        for q in search_options:
            from urllib.parse import quote as _q
            url = f"{VICTORY_BASE}/category?search={_q(q)}"
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=40000)
                page.wait_for_timeout(5000)
                dismiss()
            except Exception:
                continue

            # Try to find product by barcode in CDN image URL
            found = False
            for scroll_i in range(150):
                # Check by barcode in img src
                try:
                    bc_locator = page.locator(f'img[src*="{bc}"]').first
                    if bc_locator.count() > 0:
                        print(f"    Found barcode in img! scroll={scroll_i}", flush=True)
                        bc_locator.scroll_into_view_if_needed(timeout=2000)
                        page.wait_for_timeout(700)
                        bc_locator.click(force=True)
                        page.wait_for_timeout(5000)
                        found = True
                        break
                except Exception:
                    pass

                # Check by imageId in img src (for Millennium 80%)
                img_id = info.get("imageId")
                if img_id:
                    try:
                        id_locator = page.locator(f'img[src*="{img_id}"]').first
                        if id_locator.count() > 0:
                            print(f"    Found by imageId={img_id}! scroll={scroll_i}", flush=True)
                            id_locator.scroll_into_view_if_needed(timeout=2000)
                            page.wait_for_timeout(700)
                            id_locator.click(force=True)
                            page.wait_for_timeout(5000)
                            found = True
                            break
                    except Exception:
                        pass

                page.mouse.wheel(0, 800)
                page.wait_for_timeout(300)

            if found:
                # Extract modal content
                dialog = page.locator('[role="dialog"]').first
                if dialog.count() == 0:
                    # Maybe the click opened inline product view
                    product_view = page.locator('[ng-controller*="product"], [ng-controller*="Product"]').first
                    if product_view.count() > 0:
                        dialog = product_view

                if dialog.count() > 0:
                    # Get product name
                    prod_name = ""
                    try:
                        h_el = dialog.locator("h1, h2, [class*='name'], [class*='title']").first
                        prod_name = h_el.inner_text(timeout=1000).strip()
                    except Exception:
                        pass

                    # Click ingredients tab
                    ingr = ""
                    try:
                        ingr_tab = dialog.get_by_role("tab", name="רכיבים").first
                        if ingr_tab.count() > 0:
                            ingr_tab.click(force=True)
                            page.wait_for_timeout(2000)
                            ingr_html = dialog.inner_html(timeout=2000)
                            ingr = parse_ingredients_from_html(ingr_html)
                    except Exception:
                        pass

                    # Click nutrition tab
                    nutr = {}
                    try:
                        nutr_tab = dialog.get_by_role("tab", name="ערכים תזונתיים").first
                        if nutr_tab.count() > 0:
                            nutr_tab.click(force=True)
                            page.wait_for_timeout(2500)
                            nutr_html = dialog.inner_html(timeout=2000)
                            nutr = parse_nutrition_table(nutr_html)
                    except Exception:
                        pass

                    modal_results[bc] = {
                        "product_name_victory": prod_name,
                        "nutrition": nutr,
                        "ingredients": ingr or None,
                    }
                    print(f"    Modal scraped: name={prod_name!r} | nutr={nutr} | ingr={ingr[:80]}", flush=True)
                    break

                page.keyboard.press("Escape")
                page.wait_for_timeout(500)

    print(f"\nXHR found: {len(found_products)}/{len(TARGETS)} | Modal scraped: {len(modal_results)}", flush=True)

    context.close()
    browser.close()

# ── Assemble results ───────────────────────────────────────────────────────────
print("\n=== Assembling final results ===", flush=True)

results = {}
for bc, info in TARGETS.items():
    api_id = info["api_id"]
    label = info["label"]

    if api_id in found_products:
        p = found_products[api_id]
        nutr = parse_nutrition_json(p.get("nutritionValues") or {})
        d = p.get("data") or {}
        l1 = d.get("1") or d.get(1) or {}
        ingr = (l1.get("ingredients") or "") if isinstance(l1, dict) else ""

        bplate = is_boilerplate(ingr)
        ingr_status = (
            "REAL_INGREDIENTS" if ingr and not bplate else
            "BOILERPLATE" if ingr else "NULL"
        )
        results[bc] = {
            "barcode": bc,
            "label": label,
            "status": "SCRAPED_VIA_XHR",
            "source": "victory",
            "source_method": "branch_api_xhr",
            "product_name_victory": p.get("localName", ""),
            "nutrition": nutr,
            "ingredients": ingr or None,
            "ingredients_status": ingr_status,
            "has_full_nutrition": bool(nutr.get("energy") and nutr.get("fat") and nutr.get("carbs")),
            "plausibility_gate": "PENDING",
        }
        print(f"  {bc}: XHR | nutr={nutr} | ingr_status={ingr_status}", flush=True)

    elif bc in modal_results:
        md = modal_results[bc]
        nutr = md["nutrition"]
        ingr = md["ingredients"] or ""
        bplate = is_boilerplate(ingr)
        ingr_status = (
            "REAL_INGREDIENTS" if ingr and not bplate else
            "BOILERPLATE" if ingr else "NULL"
        )
        results[bc] = {
            "barcode": bc,
            "label": label,
            "status": "SCRAPED_VIA_MODAL",
            "source": "victory",
            "source_method": "playwright_modal",
            "product_name_victory": md["product_name_victory"],
            "nutrition": nutr,
            "ingredients": ingr or None,
            "ingredients_status": ingr_status,
            "has_full_nutrition": bool(nutr.get("energy") and nutr.get("fat") and nutr.get("carbs")),
            "plausibility_gate": "PENDING",
        }
        print(f"  {bc}: MODAL | nutr={nutr} | ingr_status={ingr_status}", flush=True)

    else:
        results[bc] = {
            "barcode": bc,
            "label": label,
            "status": "NOT_FOUND_ON_VICTORY",
            "source": "victory",
            "source_method": "playwright_search",
            "product_name_victory": None,
            "nutrition": None,
            "ingredients": None,
            "ingredients_status": "NULL",
            "has_full_nutrition": False,
            "plausibility_gate": "NOT_APPLICABLE",
        }
        print(f"  {bc}: NOT_FOUND", flush=True)

# ── Run plausibility gate ──────────────────────────────────────────────────────
print("\n=== Running plausibility gate ===", flush=True)
import importlib.util, os, sys as _sys

NUTR_KEYS_NEEDED = {"energy", "fat", "carbs", "protein"}

def quick_plausibility(nutr: dict) -> tuple[bool, str]:
    if not nutr or not NUTR_KEYS_NEEDED.issubset(nutr):
        return False, "INCOMPLETE_PANEL"
    e = nutr.get("energy", 0)
    f = nutr.get("fat", 0)
    c = nutr.get("carbs", 0)
    p = nutr.get("protein", 0)
    s = nutr.get("sugar", 0)
    so = nutr.get("saturated_fat", 0)
    na = nutr.get("sodium", 0)
    # Chocolate per-100g plausibility
    if not (400 <= e <= 700):
        return False, f"ENERGY_OOB ({e} kcal/100g)"
    if not (20 <= f <= 65):
        return False, f"FAT_OOB ({f}g)"
    if not (0 <= c <= 65):
        return False, f"CARBS_OOB ({c}g)"
    macro_sum = f + c + p
    if not (60 <= macro_sum <= 105):
        return False, f"MACRO_SUM_OOB ({macro_sum}g)"
    if s > c + 2:
        return False, f"SUGAR_EXCEEDS_CARBS ({s}>{c})"
    if so > f + 0.5:
        return False, f"SATFAT_EXCEEDS_FAT ({so}>{f})"
    if na > 5000:
        return False, f"SODIUM_OOB ({na})"
    return True, "PASS"

for bc, r in results.items():
    if r["status"] in ("NOT_FOUND_ON_VICTORY",) or not r["nutrition"]:
        r["plausibility_gate"] = "NOT_APPLICABLE" if not r["nutrition"] else "SKIP"
        continue
    ok, reason = quick_plausibility(r["nutrition"])
    r["plausibility_gate"] = "PASS" if ok else f"FAIL:{reason}"
    print(f"  {bc}: plausibility = {r['plausibility_gate']}", flush=True)

# ── Score via existing chocolate lens ─────────────────────────────────────────
print("\n=== Scoring scoreable products ===", flush=True)
try:
    _sys.path.insert(0, str(pathlib.Path(r"C:\Bari\02_products\chocolate")))
    import run_task360_phase3 as P3
    SCORER_AVAILABLE = True
    print("  Scorer loaded OK", flush=True)
except ImportError as e:
    SCORER_AVAILABLE = False
    print(f"  Scorer not available: {e}", flush=True)

for bc, r in results.items():
    if not r["nutrition"] or r["plausibility_gate"] not in ("PASS", "PENDING"):
        r["score"] = None
        r["grade"] = None
        continue
    if not SCORER_AVAILABLE:
        r["score"] = None
        r["grade"] = None
        continue
    try:
        n = r["nutrition"]
        bsip1 = P3.build_bsip1(
            barcode=bc,
            name=r.get("product_name_victory") or bc,
            nutrition=n,
            ingredients=r.get("ingredients") or "",
            source="victory_pass2",
        )
        scored = P3.run_bsip2(bsip1)
        r["score"] = scored.get("score")
        r["grade"] = scored.get("grade")
        print(f"  {bc}: score={r['score']} grade={r['grade']}", flush=True)
    except Exception as e:
        r["score"] = None
        r["grade"] = None
        print(f"  {bc}: scoring error — {e}", flush=True)

# ── OFF check ─────────────────────────────────────────────────────────────────
off_fields = []
for bc, r in results.items():
    for k, v in r.items():
        if isinstance(v, str) and ("openfoodfacts" in v.lower() or "off_" in v.lower()):
            off_fields.append(f"{bc}.{k}")
off_status = "PASS" if not off_fields else f"FAIL: {off_fields}"

# ── Write output ───────────────────────────────────────────────────────────────
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
out_path = pathlib.Path(r"C:\Bari\02_products\chocolate") / f"choc_tablets_fix_task366b_{ts}.json"

output = {
    "task": "TASK-366 Pass 2 Victory probe",
    "run_ts": ts,
    "retailer": "victory",
    "branch_id": BRANCH_ID,
    "off_check": off_status,
    "targets_attempted": len(TARGETS),
    "targets_with_nutrition": sum(1 for r in results.values() if r.get("has_full_nutrition")),
    "targets_with_real_ingredients": sum(1 for r in results.values() if r.get("ingredients_status") == "REAL_INGREDIENTS"),
    "plausibility_pass": sum(1 for r in results.values() if r.get("plausibility_gate") == "PASS"),
    "results": results,
}
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nOutput: {out_path}", flush=True)

print("\n=== FINAL SUMMARY ===", flush=True)
for bc, r in results.items():
    print(
        f"  {bc} | {r['label']}: {r['status']} | "
        f"plaus={r.get('plausibility_gate')} | "
        f"score={r.get('score')} | ingr={r.get('ingredients_status')}",
        flush=True
    )
print(f"\nOFF check: {off_status}", flush=True)
print(f"Output path: {out_path}", flush=True)
