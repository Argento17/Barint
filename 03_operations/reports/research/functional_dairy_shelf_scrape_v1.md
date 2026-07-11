# Functional / High-Protein Dairy Drink Shelf Scrape — v1 (TASK-492B / TASK-492C)

**Status: RETURNED — acquisition ran successfully. Evidence table produced.**
**Date of this run:** 2026-07-03, ~14:53–14:58 UTC (re-run after the earlier 2026-07-03
14:37–14:44 UTC attempt, logged below as superseded — Shufersal was under site-wide
maintenance then; the owner confirmed it fixed and this re-run confirms it live)
**Governing document:** `01_framework/nutrition/functional_dose_ingredient_ruling_v1.md`
(§3.1 field list, §3.2 dose-honesty bands)
**Named trigger product:** Tnuva GO (טנובה גו) — see Section 3, important finding: the
live shelf does not show a creatine SKU under this brand today.

---

## 1. Source-selection compliance (Shufersal → Victory → Yochananof → Rami-Levy)

| Retailer | Result this run |
|---|---|
| **Shufersal** (primary) | **LIVE. Confirmed via direct probe** (200 status, 205,621-byte real page, not the 444-byte maintenance stub seen in the prior blocked attempt) before running the full scraper. Full 3-phase scrape completed clean: 9 queries, 53 unique product codes found, 53/53 product pages fetched successfully (0 failures). |
| **Victory** | Re-checked (`https://www.victoryonline.co.il/`): still **403** (bot wall), unchanged from the prior run. Not usable this run either. |
| **Yochananof** | Re-checked (`https://yochananof.co.il/`): **now returns 200** (was 403 in the prior run) — but a follow-up search-endpoint probe hit a 404, meaning the storefront is reachable but its search URL path differs from what the existing playbook assumes. Per the missing-data discard rule's "don't over-invest re-sourcing a missing datum" instruction, reverse-engineering a second retailer's search API was not pursued further once Shufersal (the policy-first retailer) had already produced a full, clean 53-product scrape — this is a single evidence table, not a category corpus build, so a second full corroborating retailer scrape was judged not worth the additional time. Flagged honestly here rather than silently skipped. |
| **Rami-Levy** | Not attempted — Shufersal (primary, policy-first) succeeded and yielded sufficient coverage; per policy, cross-check retailers are pursued when the primary is blocked or thin, not required unconditionally when the primary succeeds cleanly. |
| **Open Food Facts** | Not used. Never used. Project-wide ban held. |

**Conclusion: Shufersal, the policy-first retailer, is live and was scraped successfully.
This satisfies the source-selection policy** (primary succeeded; Victory remains
genuinely blocked; Yochananof is reachable but not scraped this run for the reason
above — noted as a real gap, not hidden).

---

## 2. Corpus scoping — what counts as "functional / high-protein dairy drink"

The scraper's 9-query plan returned 53 unique product codes. Before building the
evidence table, the raw pull was filtered to the actual shelf scope (milk-based
protein/functional **drinks** — not yogurt cups, not cottage, not snack bars/noodles,
not standalone supplement powders that only surfaced because "קריאטין משקה" is a
broad-match query on Shufersal's search):

| Filter step | Count |
|---|---|
| Raw unique products returned by the 9-query plan | 53 |
| Excluded — creatine-monohydrate **supplement powder tubs** (סופר אפקט, אולאין, ספורט GS — 4 SKUs; these are gym-supplement products that matched the "קריאטין משקה" query on keyword overlap, not dairy drinks) | −4 |
| Excluded — non-drink protein snacks that matched "יוטבתה חלבון"/"תרו חלבון" on keyword overlap (protein noodles ×4, a protein pretzel snack ×1) | −5 |
| **Functional/high-protein dairy drink corpus (N)** | **44** |

This filtering is corpus-scoping, not scoring — no product was down-ranked or annotated,
these 9 items were simply outside the shelf this task defines (drinks). Full names and
exclusion reasons are in the raw scrape output (Section 6).

---

## 3. Evidence table — creatine (and functional-dose) declarations

Of the 44 dairy drinks, the creatine-detector (page text + ingredients scan for
"קריאטין"/"creatine", per ruling §3.1) flagged **2 products**. Both are **Yoplait GO
(יופלה גו)** SKUs — not Tnuva GO.

**Important finding on the named trigger:** Tnuva's own "GO" line (brand field on
Shufersal reads `GO תנובה`) has exactly one SKU on the live shelf today —
**"משקה GO קולגן אייס קפה" (GO Collagen Iced Coffee)**, barcode `7290116935607`.
Its ingredients list and page text contain **no mention of creatine** — its functional
ingredient is **collagen** (hydrolyzed collagen, 1.48%), not creatine. No other
Tnuva-branded GO SKU was found on Shufersal in this run (cross-checked with 4 query
variants: "תנובה GO", "GO תנובה", "טנובה גו קריאטין", "תנובה גו קריאטין" — none
surfaced a Tnuva-branded creatine product; the "קריאטין" hits under those queries were
all the Yoplait GO or supplement-powder products, matched on keyword overlap, not
brand). **This scrape does not find a creatine-declaring Tnuva GO product** — the
task brief's premise (Tnuva GO = the creatine trigger) does not hold on today's
Shufersal shelf. Tnuva's functional-dairy claim there is collagen, not creatine.
Flagging this rather than silently substituting the two Yoplait products under the
"Tnuva GO" label, which would misattribute brand.

### 3a. Products with a functional ingredient declared on-label

| # | Name (He) | Brand | Barcode | Serving size | Ingredient | Declared amount | Form | Named vs. blend | Daily dose (computed) | §3.2 Band |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | משקה GO קריאטin שוקולד (GO Creatine Chocolate) | יופלה גו (Yoplait GO) | 7290116936482 | **Undisclosed** — no serving-size or "מנה" instruction found on the product page (only a per-100g nutrition panel) | Creatine monohydrate ("תוסף תזונה (קריאטין מונוהידראט)") | **0.6%** of formulation (ingredients list only — no mg/serving figure anywhere on the page) | Monohydrate (disclosed) | **Named, quantified as a % only** — not a per-serving mg figure | **Cannot be computed** — 0.6% of an undisclosed serving volume cannot be converted to mg/day without assuming a bottle size, which the missing-data discard rule forbids | **Amount not disclosed** (no per-serving/day mg figure exists to band; the 0.6% figure is real but not convertible without a serving size) |
| 2 | משקה GO קריאטin קפה (GO Creatine Coffee) | יופלה גו (Yoplait GO) | 7290116936178 | **Undisclosed** — same as above | Creatine (mentioned by name in the product title/description) | **Not disclosed** in ingredients text or page body — no % figure, no mg figure | Not disclosed | **Named on-label (product name itself), no dose disclosure anywhere on the page** | **Cannot be computed** — no figure of any kind | **Amount not disclosed** |
| — | משקה GO קולגן אייס קפה (GO Collagen Iced Coffee) — **Tnuva-branded, the named trigger's actual GO SKU** | GO תנובה (Tnuva GO) | 7290116935607 | Not applicable — no creatine | **Collagen** (hydrolyzed, 1.48%), not creatine | 1.48% (collagen, different functional ingredient) | N/A (collagen) | N/A | N/A — out of scope for this ruling (creatine-specific; collagen dossier not yet built per ruling §4.2) | **Not applicable — different ingredient, no creatine present** |

### 3b. Headline count

**Of 44 functional-dairy-drink products scraped from Shufersal, 2 advertise a
functional ingredient (creatine) on-label. 0 deliver a dose that could be verified
as meaningful, partial, or decorative — both are undisclosed-dose cases (one shows
only a formulation percentage with no serving size to convert it, one shows no
dose figure at all).**

No product in this corpus crosses into the "meaningful" (≥3 g/day), "partial"
(1.5–3 g/day), or "decorative" (<1.5 g/day) bands, because none discloses the
information (mg/serving or a servable %+volume pair) required to compute a daily
dose. Per the ruling's own §3.1 discipline, this is reported as **"amount not
disclosed"** for both — a transparency-gap finding, not a downgraded or assumed-low
dose. This is itself the honest headline: the shelf's on-label creatine claims are
currently **not dose-verifiable from the product page**, for either SKU found.

---

## 4. What this means for 492B (blog) and 492C (comparison page)

- **492B (blog):** The defensible consumer-facing headline this evidence supports is
  about **disclosure**, not about a specific dose verdict: "2 of 44 functional dairy
  drinks on Shufersal's shelf name creatine on the label; neither discloses a
  per-serving dose you could evaluate." This is a stronger, more honest story than
  the assumed premise (Tnuva GO has a verifiable dose) — and it corrects a factual
  error in the task brief (Tnuva's actual GO functional ingredient found on-shelf is
  collagen, not creatine). Any blog copy must go through the mandatory two-gate
  sign-off (Content Agent + Adversarial QA/Red-Team) before reaching the owner —
  this report supplies evidence only, no consumer copy is drafted here.
- **492C (comparison page):** Same correction applies — a "Tnuva GO creatine" framing
  is not supportable from this scrape. If a comparison page proceeds, it should be
  framed around the two Yoplait GO creatine SKUs (with the transparency-gap finding
  as the actual story) and/or broadened to include the Tnuva GO collagen SKU under a
  separate collagen framing once that dossier exists (ruling §4.2 — not yet built).
  **Recommend Product Agent re-confirm scope before 492C proceeds** — this is a
  scope-conflict flag per this agent's Spec-Conflict Duty, not a unilateral redirect.

---

## 5. Constraints compliance

- **Missing-data discard rule**: held throughout. Neither creatine dose was assumed,
  backfilled, or hedged into a band — both render as "amount not disclosed."
  Serving size was left NULL for every one of the 44 products (Shufersal's product
  pages for this shelf do not carry a "מנה" instruction in the scraped HTML;
  the regex-based serving-size extractor found zero matches across the whole
  corpus, not just the creatine SKUs — noted as a shelf-wide data gap, not a
  parser bug specific to these two products).
- **OFF**: not used, not considered, at any point.
- **No score computed, no BSIP2 run** — this remains annotation/evidence-only scope.
- **No subagents spawned** — all scraping, filtering, and cross-checks run directly
  by this agent via Bash/Python.
- **No invented data** — every figure in Section 3 traces to a specific scraped
  field; the 0.6% figure is a direct ingredients-list quote, not a derived number.

---

## 6. Raw artifacts

- Scraper (unchanged, re-run as-is): `C:\Bari\03_operations\bsip0\scrape\shufersal_functional_dairy\01_scrape_functional_dairy.py`
- **New raw scrape output (this run, 53 products, live data):**
  `C:\Bari\03_operations\bsip0\scrape\shufersal_functional_dairy\functional_dairy_bsip0_raw_20260703T145405.json`
- Scrape log: `C:\Bari\03_operations\bsip0\scrape\shufersal_functional_dairy\functional_dairy_bsip0_log_20260703T145405.txt`
- Prior blocked-run artifacts (superseded, kept for the record):
  `functional_dairy_bsip0_raw_20260703T143700.json` (0 products, honest empty stub)

---

## Return Contract

```json
{
  "task": "TASK-492B / TASK-492C data step",
  "deliverable": "functional_dairy_shelf_scrape_v1 (re-run)",
  "status_proposed": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\research\\functional_dairy_shelf_scrape_v1.md",
      "sha256": "8014b905c870a980176ed9775a1752e9be92b757f09f918326a798a773998321 (of the version prior to this final edit -- report content unchanged below this line, only this block filled in)"
    },
    {
      "path": "C:\\Bari\\03_operations\\bsip0\\scrape\\shufersal_functional_dairy\\functional_dairy_bsip0_raw_20260703T145405.json",
      "sha256": "f7386ece1c8d96070553ef6a9724519371a854138d714d63e594a29f16ef9986"
    },
    {
      "path": "C:\\Bari\\03_operations\\bsip0\\scrape\\shufersal_functional_dairy\\functional_dairy_bsip0_log_20260703T145405.txt",
      "sha256": "5db3c45cb46d11018307c80adb1d810bef67c7af311f10e2a3e1d10f80d0f8fe"
    }
  ],
  "counts": {
    "retailers_attempted": {"value": 3, "denominator": "4 in source-selection policy order (Shufersal, Victory, Yochananof attempted; Rami-Levy skipped -- primary succeeded)"},
    "retailers_yielding_usable_scrape": {"value": 1, "denominator": "3 attempted (Shufersal live+scraped; Victory still 403; Yochananof reachable but search endpoint not mapped this run)"},
    "raw_products_returned_by_query_plan": {"value": 53, "denominator": "9 queries, MAX_PRODUCTS cap 80 (not hit)"},
    "product_pages_fetched_ok": {"value": 53, "denominator": "53 unique codes found (0 failures)"},
    "functional_dairy_drink_corpus_after_scope_filter": {"value": 44, "denominator": "53 raw -- 4 supplement-powder SKUs -- 5 non-drink protein snacks excluded"},
    "products_declaring_creatine_on_label": {"value": 2, "denominator": "44 functional-dairy-drink corpus"},
    "products_with_computable_daily_dose": {"value": 0, "denominator": "2 creatine-declaring products -- both undisclosed (one % w/o serving size, one no figure at all)"},
    "tnuva_go_creatine_skus_found": {"value": 0, "denominator": "1 Tnuva-branded GO SKU found on shelf (collagen, not creatine) -- named trigger's premise does not hold on live data"},
    "products_with_nutrition_data": {"value": 44, "denominator": "53 raw scrape (coverage stat from scraper log: 44/53 nutrition, 48/53 ingredients)"},
    "off_usages": {"value": 0, "denominator": "0 -- banned source, never invoked"}
  },
  "commands_run": [
    {"cmd": "python -c \"requests.get shufersal search probe\"", "exit_code": 0, "note": "confirmed 200 status, 205621 bytes, real page -- not maintenance stub -- before running full scraper"},
    {"cmd": "python 03_operations/bsip0/scrape/shufersal_functional_dairy/01_scrape_functional_dairy.py", "exit_code": 0, "note": "full run: 53 products, 53/53 pages OK, 0 failures, 6 raw creatine-token hits before scope filtering"},
    {"cmd": "python -c \"requests.get victoryonline.co.il\"", "exit_code": 0, "note": "confirmed still 403, unchanged from prior run"},
    {"cmd": "python -c \"requests.get yochananof.co.il\"", "exit_code": 0, "note": "confirmed now 200 (was 403 prior run) -- reachability improved but search endpoint not mapped this run"},
    {"cmd": "python -c \"requests.get yochananof.co.il/catalogsearch/result\"", "exit_code": 0, "note": "404 -- guessed search path wrong, not pursued further per missing-data discard rule (don't over-invest re-sourcing)"},
    {"cmd": "python -c \"4x tnuva-GO query variants against shufersal search\"", "exit_code": 0, "note": "confirmed 0 Tnuva-branded creatine SKUs; only Tnuva GO SKU found is collagen"},
    {"cmd": "python -c \"corpus scope filter: exclude supplement powders + non-drink snacks\"", "exit_code": 0, "note": "53 raw -> 44 scoped dairy-drink corpus"}
  ],
  "not_done": [
    "Yochananof not fully cross-checked -- reachable (200) but search endpoint path not mapped in this run; flagged as a real gap, not required given Shufersal's clean full result",
    "Rami-Levy not attempted -- policy allows skipping cross-check retailers when the primary yields a clean full result",
    "No creatine daily dose computed for either declaring product -- both genuinely undisclosed per the scraped data, not a scraper limitation",
    "No blog or comparison-page copy drafted -- out of this agent's lane and requires two-gate sign-off",
    "Scope-conflict flagged to Product Agent: the task brief's premise (Tnuva GO = creatine trigger) does not match live shelf data (Tnuva GO's actual SKU is collagen); recommend Product re-confirm 492C's framing before that page proceeds"
  ],
  "acceptance_test": {
    "spec_requirement": "Re-run the functional-dairy shelf scrape now that Shufersal is fixed, capture S3.1 fields for creatine-declaring products including Tnuva GO and peers, compute S3.2 dose bands, produce evidence table + headline count, no OFF, no invented data, no subagents, discard missing fields rather than assume",
    "result": "PASS, with one material scope-conflict flag",
    "evidence": "Shufersal confirmed live via direct probe (200, full page) then scraped clean: 53 products, 0 fetch failures. Corpus scoped to 44 genuine functional-dairy-drinks after excluding 9 out-of-shelf matches (supplement powders, protein noodles/snacks) that surfaced only via keyword-overlap search matching. 2 of 44 declare creatine on-label; both computed as 'amount not disclosed' per S3.2 because neither a per-serving mg figure nor a serving-size+percentage pair exists on the scraped page -- held to the missing-data discard rule rather than assuming a serving size to force a dose figure. Headline count delivered in Section 3b. Material finding: the named trigger 'Tnuva GO' has no creatine SKU on the live Shufersal shelf today -- its one GO product is a collagen drink, not creatine; the two creatine-declaring products found are a different brand (Yoplait GO). This is flagged in Section 4 as a scope-conflict for Product Agent re-confirmation before 492C proceeds, per this agent's Spec-Conflict Duty -- not silently substituted or hidden. OFF never used. No subagents spawned. No dose figures invented -- the 0.6% figure is a direct ingredients-list quote."
  }
}
```
