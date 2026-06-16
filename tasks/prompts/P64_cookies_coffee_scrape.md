# P64 — Cookies-near-coffee: broad BSIP0 scrape (route: C1-CURSOR)

**Task:** TASK-275 (factory run #7, `cookies-coffee`). Read `C:\Bari\tasks\TASK-275.md`.
**Repo:** `C:\Bari`. **Lane:** C1-CURSOR (spec-complete code; the template carries all context).

## Objective
Write **and run** a Shufersal BSIP0 scraper for a **BROAD cookie/biscuit radius** (we narrow to the
"coffee cookie" subcategory later, at corpus-filter). One-shot, deterministic, OFF-banned.

## Exact method — MIRROR the proven template
Copy the structure of `03_operations/bsip0/scrape/shufersal_brined_cheeses/01_scrape_brined_cheeses.py`
**exactly** (same imports, `store_page` raw-store banking, ld+json parse, `parse_nutrition_list` /
`extract_nutrition_raw`, `composition_nutrition_report`, the `off_source_used=False` sentinel and the
OFF-ban audit that raises on any violation). Change ONLY the category params below.

New file: `03_operations/bsip0/scrape/shufersal_cookies_coffee/01_scrape_cookies_coffee.py`
- `RETAILER = "shufersal"`, `CATEGORY = "cookies_coffee"`
- `MAX_PRODUCTS = 300` (broad; no pre-trimming — narrowing happens downstream)
- Output: BSIP0 JSON → `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_<ts>.json`
  + log `..._log_<ts>.txt`; raw HTML → `raw_store/shufersal/cookies_coffee/<code>/<ts>.html` + manifest.

### QUERY_PLAN (broad — sweet biscuits/cookies; mainstream first)
mainstream: `עוגיות`, `ביסקוויט`, `ביסקוויטים`, `פתי בר`, `פטיבר`, `מארי`, `לוטוס`, `עוגיות חמאה`,
`עוגיות שוקולד צ'יפס`, `שורטברד`, `דייג'סטיב`, `ביסקוטי`
specialty: `lotus`, `biscoff`, `speculoos`, `עוגיות קפה`, `עוגיות תה`, `עוגיות מקמח מלא`,
`קנטוצ'יני`, `עוגיות שקדים`, `מקרון`, `עוגיות טבעוניות`, `עוגיות אורגניות`, `שופרסל עוגיות`
Also browse the broad cookies/biscuits aisle category URLs best-effort (graceful on 404), same as the
template's `CATEGORY_URLS` pattern — pick the Shufersal sweet-biscuit aisle codes; name-filter still gates.

### INCLUDE_SIGNALS (broad — match ≥1 to be a candidate cookie)
`עוגי`, `עוגיות`, `ביסקוויט`, `biscuit`, `פתי בר`, `פטיבר`, `petit`, `מארי`, `marie`, `לוטוס`, `lotus`,
`biscoff`, `speculoos`, `שורטברד`, `shortbread`, `דייג'סטיב`, `digestive`, `ביסקוטי`, `biscotti`,
`קנטוצ'יני`, `cookie`, `cookies`

### EXCLUDE_SIGNALS (clearly NOT a coffee-biscuit — keep the radius clean of non-cookies)
crackers/savory: `קרקר`, `cracker`, `מצות`, `מצה`, `פריכיות`, `אורז` (rice cakes), `מלוח`, `קרוטון`, `בייגלה`, `במבה`, `ביסלי`, `צ'יפס`, `chips`, `מקלות`
cakes/pastry: `עוגה`, `עוגת`, `cake`, `מאפה`, `מאפים`, `רוגלך`, `קרואסון`, `croissant`, `בורקס`, `שטרודל`, `טארט`, `פאי`, `מאפין`, `muffin`, `דונאט`, `donut`
confection/bars: `חטיף`, `חטיפים`, `bar`, `שוקולד` (chocolate bars — but allow "עוגיות שוקולד"), `ופל`, `wafer` (wafers = separate shelf), `מרשמלו`, `סוכריות`, `גלידה`, `ice cream`
other: `דגני בוקר`, `cereal`, `גרנולה`, `granola`, `תינוק`, `baby`, `כלב`, `חתול` (pet)
NOTE on `שוקולד`: exclude only when the name is a chocolate **bar/snack**, not a chocolate-chip
**cookie**. Implement as: exclude if `שוקולד`/`chocolate` present AND no INCLUDE cookie term present.
(Keep this the ONLY conditional; everything else is plain substring exclude like the template.)

## Guards (hard)
- **OFF BAN (TASK-238, absolute):** only the direct Shufersal scrape. No Open Food Facts, any field,
  ever. `off_source_used=False` on every record; the OFF-ban audit must run and pass (raise on >0).
  Missing field = NULL, never filled.
- Do not touch any other category, the score engine, or any frontend file. New files only.
- Polite crawl (keep the template's `PRODUCT_PAGE_DELAY`).

## Definition of done
1. New scraper file created, mirroring the template (only category params differ).
2. **Run it.** Report the BSIP0 composition gate block verbatim: product count, nutrition %,
   ingredients %, images, high/low-confidence, plausibility, **OFF ban check (= 0)**, raw-store banked.
3. Report the raw JSON path + a 5-row sample (name_he, brand, barcode, has-nutrition, has-ingredients).
4. If the scrape environment blocks network, say so explicitly in `not_done` (do NOT fabricate
   coverage numbers) — the orchestrator will run it.

## Return format
End with the machine-readable return contract (`01_framework/operations/return_contract_v1.md`):
```json
{"task":"P64","proposed_status":"RETURNED","artifacts":[{"path":"...","action":"created","sha256":"..."}],
 "counts":{"products_scraped":"N","nutrition_pct":"...","ingredients_pct":"...","off_used":"0"},
 "commands_run":[{"cmd":"python 01_scrape_cookies_coffee.py","exit_code":0}],
 "not_done":[],"self_check":"..."}
```
Do NOT close — propose RETURNED. The orchestrator verifies every claim against artifacts.
