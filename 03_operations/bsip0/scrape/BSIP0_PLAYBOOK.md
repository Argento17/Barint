# BSIP0 Acquisition Playbook — the canonical runbook for C1 lanes

**Owner-mandated (2026-06-20, TASK-362).** Read this BEFORE any category scrape.
BSIP0 kept failing not because the code couldn't scrape, but because the *process*
wasn't written down: lanes single-sourced, admitted wrong-category products, dropped
real ones on id technicalities, and shipped physically-impossible nutrition. This
playbook is the fix. Every step here is backed by working code in this directory.

> **Golden rule:** *"Unknown is acceptable; OFF is not, and wrong-category is not."*
> Never use Open Food Facts for any field, ever. Never fabricate. If data isn't
> found one-shot from a reachable Israeli retailer, the field is NULL and the
> product may be discarded — never back-filled from a banned or guessed source.

---

## The 6 mandatory stages (in order)

```
1. PROBE all 4 retailers      -> source_selection (never default to one; don't stop if one is blocked)
2. ACQUIRE from reachable     -> proven Shufersal 3-phase engine (reference scraper)
3. SCOPE TEST (Hebrew)        -> hebrew_scope_test.py  — IS this product in the category?  [NEW]
4. PLAUSIBILITY GATE          -> plausibility_gate.py  — is the per-100g panel physically possible?
5. CROSS-CHECK + DEDUP        -> by barcode across sources; prefer plausibility-passing value
6. COMPOSITION GATE           -> >=30 products, >=90% nutrition, >=90% ingredients, else STOP+report
```

A product enters the corpus **iff** it passes stages 3 *and* 4. Membership has
exactly one authority (the scope test) — never an id list, never a curator's memory.

---

## Stage 1 — Source selection (probe all four)

Policy: `retailer_capabilities/SOURCE_SELECTION_POLICY.md`. **Probe every run** —
reachability is per-environment. Measured 2026-06-20 (Claude Code sandbox + owner box):

| Retailer | Path that works | Reachability (2026-06-20) |
|---|---|---|
| **Shufersal** (primary) | `requests` → HTML search + product pages | ✅ reachable |
| **Victory** | `requests` (cookie-wall on some nutrition) | ✅ home; ⚠️ nutrition gated |
| **Yochananof** | **Playwright + cookie-dismiss** (NOT `requests`) | ⚠️ blocked via requests (TLS/403); works via browser — see below |
| **Rami-Levy** | price-transparency portal | ❌ connection refused from our envs |

**Rules:** attempt all four in priority order; use every reachable one; **do not abort
because one is blocked** — record which were blocked and proceed with the rest. If
*all four* fail, STOP and report (never fabricate).

### Yochananof workaround (the "block" is a tooling choice)
`requests`/the JSON API hits a TLS `ERR_CERT_COMMON_NAME_INVALID` + 403 bot-wall.
The **browser path works** and already exists:
`02_products/hard_cheeses/scrape_cheeses_yohananof.py` drives it with Playwright +
`close_cookie_popup()` (dismisses the Hebrew consent modal — `אישור / מסכים / קבל /
הבנתי`) then opens per-product nutrition modals. For yochananof: **use Playwright,
dismiss the cookie/consent popup, open the product modal — never the requests/API.**

---

## Stage 2 — Acquire (the proven Shufersal engine)

**Reference scrapers (copy one, retarget queries+filters):**
`shufersal_cereals/01_scrape_cereals.py` and `shufersal_snack_bars/01_scrape_snack_bars.py`
(TASK-362). Both are the same 3-phase engine:

1. **Search (list):** `GET /online/he/search?q=<urlenc>&pageSize=48&currentPage=N`
   → HTML. Parse `<li data-product-name … data-product-code … data-food … data-product-price>`.
   **GOTCHA:** the JSON endpoint `/online/he/search/results?q=…:relevance` returns the
   list too, but **nutrition fields (calories/fats/sodium/sugar) are NULL there.** Do
   not trust search-level nutrition. Nutrition lives on the product page only.
2. **Product page:** `GET /online/he/p/<code>` (code like `P_<sku>`) → HTML.
   - Name / barcode / brand / images: `<script type="application/ld+json">` `@type:Product`
     → `name`, `gtin13` (the real barcode), `brand.name`, `image[]`.
   - **Nutrition:** `_shared/bsip0_nutrition.py::parse_nutrition_list(soup)` — reads
     TOTAL macros, captures saturated separately, never lets an "of which" sub-row
     overwrite a total (EV-026/EV-029). Also persist `extract_nutrition_raw(soup)` so a
     future parser fix replays offline (no re-scrape).
   - **Ingredients:** regex around the `רכיב` label. (Known minor leak: marketing text
     can precede the list; BSIP1 trims it.)
3. **Throttle** ~0.55s between product pages. Cap via `BARS_MAX` env / `MAX_PRODUCTS`.

Output → `02_products/<category>/bsip0_outputs/<cat>_bsip0_raw_<ts>.json` (+ log).
Schema per product: `retailer_id, source_url, scraped_at, name_he, brand, barcode,
nutrition{…_raw}, nutrition_raw_source, ingredients_raw, image_urls,
extraction_confidence, price, weight_g, acquisition_query`.

---

## Stage 3 — Hebrew Scope Test  *(the NEW thing — Orchestrator-defined)*

`_shared/hebrew_scope_test.py`. **The Orchestrator (Opus) defines each category's
scope ONCE, in Hebrew, as a `ScopeDefinition`.** Every stage (scraper filter, BSIP1
curation, conformance) calls this same test. This is what stops Pesek Zman leaking in
and real bars being dropped — there is one authority for "what is in the category."

```python
from hebrew_scope_test import scope_test, BAR_SHELF, Scope
r = scope_test(name_he, ingredients_he, BAR_SHELF)
# r.verdict ∈ {IN_SCOPE, OUT_OF_SCOPE, AMBIGUOUS}
```

A `ScopeDefinition` has three Hebrew token sets:
- **required_markers** — at least one must appear to be in-scope (e.g. `חטיף`, `חלבון`, `מאגדת`).
- **disqualifiers** — any hit forces OUT_OF_SCOPE *even if a marker matched*. This is
  how an adjacent category is excluded: chocolate candy (`פסק זמן`, `קיט קט`, `טבלת שוקולד`),
  salty (`ביסלי`, `במבה`), crackers/cookies/wafers, drinks/dairy, raw commodity (`קוואקר 500`).
- **supporting_markers** — weak signals; presence without a required marker → AMBIGUOUS.

Verdicts: **OUT_OF_SCOPE** never admitted; **IN_SCOPE** admitted; **AMBIGUOUS**
(no marker, no disqualifier) routed to the Orchestrator — **never silently admitted or
dropped.** Disqualifier always beats marker (Pesek Zman contains `חטיף` but is candy).

> To add a category: author a new `ScopeDefinition` in `hebrew_scope_test.py`, add a
> self-test case, get the Orchestrator's sign-off. Do **not** hardcode include/exclude
> strings inside a scraper anymore — point the scraper at the ScopeDefinition.

---

## Stage 4 — Plausibility gate (mandatory, moisture-aware)

`_shared/plausibility_gate.py::check_panel(nutr_per_100g, food_class, ingredients_text)`.
Runs on **every** panel regardless of source. Catches the snacks bug (white-chocolate
bar "99 kcal / 0g sugar" → rank #1). Checks:
- **accounted_mass = carbs+fat+protein** ≥ a **moisture-aware floor** (dry bar 70g,
  dry-dense 80g, moist baked 30g, spread 18g, beverage 2g, dairy-solid 20g). *Do not
  apply the dry floor to moist foods* — cheesecake is legitimately ~45g (false-positive
  source in the first cut).
- **kcal bounds** per food class; **kcal vs Atwater** (4/4/9) within 30%.
- **sugar==0 against a sugar-bearing ingredient** (`סוכר/סירופ/שוקולד/תמרים/…`) → impossible.

Failing panel → **quarantine + report**, never score, never carry forward.
Bar split (after the gate): `classify_bar(name_he, protein_per_100g)` → `protein_bar`
iff name marks `חלבון/פרוטאין/protein` or protein ≥ 20 g/100g; else `snack_bar`.

---

## Stages 5–6 — Cross-check, dedup, composition gate

- **Dedup by barcode** (gtin13). When a barcode appears at ≥2 retailers, compare panels;
  prefer the plausibility-passing value; flag material disagreement.
- **Composition gate (hard):** ≥30 products, ≥90% with nutrition, ≥90% with ingredients.
  Below → STOP and report; do not ship a thin/holey corpus.

---

## Failure-mode catalogue (what bit us, and which gate now prevents it)

| What happened | Root cause | Prevented by |
|---|---|---|
| White-choc bar "99 kcal/0 sugar" ranked #1 | single-source yochananof, no sanity check | Stage 1 multi-source + Stage 4 plausibility |
| Pesek Zman / chocolate candy in "snacks" | ad-hoc include strings, no scope authority | Stage 3 scope test (disqualifier beats marker) |
| Real bars dropped "on a technicality" | curation pinned display to hardcoded snk-NNN ids in a stale module | Stage 3 scope test = sole membership authority (no id lists) |
| Raw oats / loose granola admitted | name "שיבולת שועל" matched, no commodity DQ | Stage 3 disqualifiers (`קוואקר 500`, `גריסים`) |
| "official food source" copy / OFF residue | banned source crept in as fallback | OFF ban (golden rule) — Israeli retailers only |
| Agent reported coverage it didn't have | self-reported counts, no trace | Stage 6 gate prints trace-derived counts |

## C1 lane runbook (copy-paste order)
1. `python … probe all 4` (or reuse SOURCE_SELECTION_POLICY table) — record reachability.
2. Copy `shufersal_snack_bars/01_scrape_snack_bars.py`; retarget `QUERY_PLAN` + point its
   filter at a `ScopeDefinition`; set output dir.
3. Run; confirm the **composition gate** line (≥30 / ≥90% / ≥90%).
4. Run `plausibility_gate.check_panel` over every product; quarantine failures.
5. Hand BSIP0 raw to BSIP1; the scope test + gate travel with it (same authority downstream).
6. Report **trace-derived** counts only (command + numbers), never self-reported.
```
