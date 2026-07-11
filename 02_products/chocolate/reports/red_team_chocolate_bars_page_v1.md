# Red-Team Challenge Report — Chocolate Bars (`/hashvaot/chocolate-bars`)

Date: 2026-07-03
Scope: 23 products, `/hashvaot/chocolate-bars`
Challenger: adversarial-qa-agent (Bari)
Task: TASK-474 (P1 item 9a / launch finding F2)
Ground truth ref: `origin/master` (fetched fresh this run) — all file reads below via `git show origin/master:<path>` unless stated otherwise.
Status: **COMPLETE.**

**Category-identity note (read first):** there are TWO chocolate categories sharing one corpus root
(`02_products/chocolate/`) and one BSIP0/BSIP1/BSIP2 run (`fresh_rescore_task391_20260624_113405`,
121 scored = 29 chocolate_bar + 92 chocolate_tablet). This report covers **chocolate-bars only**
(route `/hashvaot/chocolate-bars`, JSON `bari-web/src/data/comparisons/chocolate_bars_frontend_v1.json`,
config `03_operations/page_generator/configs/chocolate_bars.json`). Chocolate-tablets is a separate
task/report (`02_products/chocolate/reports/red_team_tablets_2026-07-03.md`, already on origin/master
for a different scope — a copy-overhaul QA, not this launch gate). Do not conflate the two.

Per `chocolate_bars.json` comment: 29 chocolate_bar records were scored; the live page displays only
**23/29** — 6 are `CORPUS_NOT_DISPLAYED` (barcodes: 5000159561945, 5000159560498, 7290112494221,
7290116532028, 5000159557689, 5000159559461). This narrowing needs a documented reason (G3) — checked
below.

---

## Provenance note

Route: `bari-web/src/app/hashvaot/chocolate-bars/page.tsx` → imports from
`@/lib/comparisons/chocolate-bars-comparison-page-data.ts`, which wraps
`bari-web/src/data/comparisons/chocolate_bars_frontend_v1.json` (23 products, confirmed by reading the
route + loader source — NOT taking a builder's word for it).

Live JSON `_meta`:
- `run_id = task409_rederive_chocolate_bars_20260626`
- `corpus_dirs = C:\Bari\03_operations\bsip1\fresh_rescore_task391_20260624_113405\output`
- `engine_sha = 5f2e611db7417d1e31e9ae548afde041d5a148a9`
- `corpus_records = 23`, `scored = 23`, `product_count = 23`, `failed_barcodes = []`
- `reflow` block: TASK-455 "chocolate correctness (classifier fix + endemic carve-out)",
  `BARI_REDLABEL_CONTINUOUS_V1=on`, date 2026-07-02, "chocolate re-classified from snack_bar_granola to
  chocolate (router_v2 Rule 4) + EV-REDLABEL-013 endemic sat-fat carve-out; all moves upward"
- `deanchor_meta_regenerated = 2026-07-02`
- All 23 live products carry grade **E** (grade_dist = {E: 23}).

Committed BSIP2 trace directory: `02_products/chocolate/bsip2_outputs/fresh_rescore_task391_20260624_113405/products/` —
generated 2026-06-24, i.e. **before** the TASK-455 re-flow (2026-07-02) and de-anchor sweep baked into
today's live numbers. Same F-V1 traceability-gap pattern as bread/cakes is suspected — verified below.

---

## Opening Finding

No data-absent scoring found: all 23 products carry populated core nutrition (sugar/sat-fat/sodium/
protein/kcal/ingredients) and `confidence: "verified"` uniformly — null `fat_trans_g`/`cholesterol_mg`
(23/23) and null `dietary_fiber_g` (19/23) are standard Israeli-label absences, not data gaps driving a
score, so Hard Rule 12 does not fire as a CRITICAL here.

The opening structural problem is instead the **same F-V1 traceability-gap pattern already found on
bread/cakes**: no committed BSIP2 trace file on disk reproduces the current live chocolate-bars score for
any sampled product. Unlike cakes, this is fully and precisely explained here — the committed trace
(`fresh_rescore_task391_20260624_113405`) was generated 2026-06-24 under the **wrong category**
(`category: "snack_bar_granola"` in every one of the 8 sampled traces) before TASK-455 (commit `f026f2dd`,
2026-07-02) fixed the router classification to `chocolate` and applied an endemic sat-fat carve-out
(EV-REDLABEL-013) + continuous red-label de-anchor. All 8/8 sampled products show live score strictly
above trace `final_score_estimate` (deltas +0.9 to +4.6), consistent with the commit message's own claim
("chocolate_bars: 23/23 score-moves, all up, 0 grade flips"). See F-V1 (HIGH, not CRITICAL — the movement
direction and magnitude are independently explained by a named, two-gate-signed commit, but no single
committed artifact reproduces today's number).

A second, more consumer-visible structural finding: the hero title — the single largest, most prominent
string on the page, above every product row — contains the owner-banned "X, not Y" antithesis
construction stacked with an em-dash: **"חטיפי השוקולד האלה הם חטיפי ממתק, לא חטיפי ביניים — וכולם יודעים
את זה"** ("these chocolate bars are candy bars, not snack bars — and everyone knows it"). This single
string carries both of the two phrasing violations this report was asked to check, on the page's most
visible element. See F-C2 (HIGH).

---

## Track V — Verification

### V1. Score/trace fidelity (G5) — 8 products sampled across the score range

All 23 live products carry grade **E** (no cross-grade sampling possible — `_meta` grade_dist =
`{E: 23}`, confirmed programmatically). Sampled across the full score range instead (top, bottom, and
5 spread points). Trace = `02_products/chocolate/bsip2_outputs/fresh_rescore_task391_20260624_113405/products/bsip1_{barcode}/bsip2_trace.json`
(only committed trace directory; generated 2026-06-24, i.e. pre-TASK-455).

| # | Barcode | Live score | Live grade | Trace `final_score_estimate` | Trace `grade_estimate` | Delta (live-trace) | Grade-cross? | Trace `category` (debug) |
|---|---|---|---|---|---|---|---|---|
| 1 | 5000159560511 | 25.5 | E | 20.9 | E | +4.6 | no | **snack_bar_granola** |
| 2 | 7290116536781 | 21.3 | E | 17.6 | E | +3.7 | no | **snack_bar_granola** |
| 3 | 5900951310379 | 19.3 | E | 16.8 | E | +2.5 | no | **snack_bar_granola** |
| 4 | 7290116537375 | 17.6 | E | 15.0 | E | +2.6 | no | **snack_bar_granola** |
| 5 | 3800020401552 | 17.2 | E | 15.7 | E | +1.5 | no | **snack_bar_granola** |
| 6 | 72917367 | 16.0 | E | 14.4 | E | +1.6 | no | **snack_bar_granola** |
| 7 | 7290116534442 | 13.8 | E | 12.9 | E | +0.9 | no | **snack_bar_granola** |
| 8 | 34000250103 | 12.3 | E | 10.0 | E | +2.3 | no | **snack_bar_granola** |

**Summary: 0/8 grade-crosses (all stay E, matching the commit message's "0 grade flips" claim exactly).
8/8 sampled products show a positive delta (+0.9 to +4.6), all live-above-trace, matching the commit
message's "all 58 products move UP" claim exactly.** Every trace's `category` field reads
`snack_bar_granola` — direct confirmation that the committed trace predates the TASK-455 router fix
(chocolate was scored against granola-bar calorie/cap tables, not the new dedicated "chocolate" calorie
regime). No committed BSIP2 trace file on disk currently reproduces a post-TASK-455 chocolate-bars score
for any product — this is the same F-V1 pattern found on bread/cakes, but here the direction and rough
magnitude of every single sampled delta is fully consistent with, and named in, one specific two-gate-
signed commit (`f026f2dd`), which is a stronger reproducibility floor than cakes had (cakes needed two
separately-dated commits chained together). See F-V1 (HIGH).

Live `grade` was independently re-derived from `frontendGradeFromScore()` (`bari-web/src/lib/comparisons/corpus.ts`,
`E` if `score < 35`) for all 8 sampled products — matches the stored `grade` field in all 8/8 cases.

### V2. Ingredient-handoff (TASK-475/476 bug class) — 5 products sampled

Source: `03_operations/bsip1/fresh_rescore_task391_20260624_113405/output/bsip1_{barcode}.json`
`ingredient_order` length vs BSIP2 trace `L1_observed_signals.ingredient_count`.

| # | Barcode | BSIP1 `ingredient_order` len | BSIP1 `ingredients_text_he` len | BSIP2 `ingredient_count` | Verdict |
|---|---|---|---|---|---|
| 1 | 5000159560511 | 14 | 178 chars | 14 | Clean (exact match) |
| 2 | 7290116536781 | 30 | 464 chars | 33 | OK — populated both sides, minor count divergence (BSIP2 counts 3 more than BSIP1's parsed order list; not a zero/handoff-loss case) |
| 3 | 5900951310379 | 19 | 256 chars | 34 | OK — same divergence pattern, larger gap (19 vs 34); populated both sides, not a zero-bug |
| 4 | 3800020401552 | 16 | 274 chars | 18 | OK — minor divergence |
| 5 | 34000250103 | 23 | 325 chars | 36 | OK — same pattern, largest gap (23 vs 36) |

**5/5 clean of the REAL_LOSS-57 handoff-zero bug class** (BSIP1 populated + BSIP2 `ingredient_count=0`
never occurs in this sample — BSIP2 count is always >0 and always ≥ BSIP1's order-list length). Worth a
MEDIUM note: in 3/5 sampled products, BSIP2's `ingredient_count` is meaningfully higher than BSIP1's
parsed `ingredient_order` length (e.g. 19 vs 34, 23 vs 36) — this is a counting-methodology divergence
(BSIP2 likely tokenizes sub-ingredients inside parenthetical/compound entries that BSIP1's order list
treats as one item), not a data-loss bug, but it means `ingredient_count` and `ingredient_order` are not
interchangeable and a future consumer of either field should not assume they agree. See F-V2 (MEDIUM).

### V3. Data integrity

- **Product count vs `_meta`:** `_meta.product_count = 23`; actual `products` array length = 23.
  **MATCH.**
- **Dropped/excluded documented (G3):** config `03_operations/page_generator/configs/chocolate_bars.json`
  states 29 chocolate_bar records were scored (per the shared `fresh_rescore_task391_20260624_113405`
  manifest, `chocolate_bar` list len=29) but only 23 are displayed; `exclusions: []` (empty array) in the
  config's structured field, with the only explanation living in a free-text `_comment`: "the 6
  non-displayed are `CORPUS_NOT_DISPLAYED`" (barcodes 5000159561945, 5000159560498, 7290112494221,
  7290116532028, 5000159557689, 5000159559461) — a bucket label, not a reason. Independently checked all
  6: all carry `evaluation_status: standard` and normal, plausible scores (14.5-17.1) in their committed
  traces — nothing distinguishes them as data-quality failures. Cross-checked their names against the
  displayed 23: all 6 are **multi-pack or seasonal/kosher-for-Passover variants of products already shown
  as single-serving bars** (e.g. "סניקרס מיני"/"חטיפי סניקרס" [Snickers multi-pack] vs displayed "סניקרס
  חטיף בודד" [Snickers single bar]; "טוויקס מיני"/"חטיפי טוויקס" vs displayed "טוויקס חטיף בודד"; "קליק
  ביסקוויט"/"קליק נוגט כשל\"פ" vs displayed regular Click variants). This is a plausible, defensible
  editorial rule (one card per single-serving SKU, no multi-packs/seasonal duplicates) but **it is stated
  nowhere in the config or `_meta`** — only inferable by manual name comparison, exactly the same class of
  gap as the cakes report's circular `"not_in_live_curation"` finding. See F-V3 (MEDIUM).
- **Rank monotonicity:** `rank` field equals array index+1 for all 23 (0 mismatches, verified
  programmatically); `score` values strictly non-increasing down the array (0 inversions). **PASS.**
- **Duplicate IDs / barcodes:** 0 duplicate `id` values, 0 duplicate `barcode` values across 23 products.
  **PASS.**
- **`categoryTotal` consistency:** single distinct value `23` across all 23 products, matches array length
  and `_meta.product_count`. **PASS.**
- **`_scoring_trace.category` debug mirror:** all 23 products show `chocolate` (not the pre-fix
  `snack_bar_granola`) — confirms the commit message's claim that this debug field was refreshed on all
  58 products (both bars + tablets). **PASS** (internal-consistency confirmation of the TASK-455 reflow).

### V4. OFF ban (hard gate)

- Grepped the live frontend JSON (`chocolate_bars_frontend_v1.json`) and all 8 sampled BSIP2 trace files
  plus all 5 sampled BSIP1 files for `openfoodfacts` / "open food facts" / `off_source`: **0 matches.**
- **Gap vs cakes precedent:** unlike the cakes live JSON (which carries `_meta.off_used = false` as an
  explicit machine-checkable enforcement flag), the chocolate-bars live JSON's `_meta` has **no `off_used`
  key at all** — the only OFF-clean assertion is prose in the page-generator config's free-text
  `_comment` field ("OFF check = PASS (all Shufersal direct scrape)"), which is not machine-checkable
  against the served JSON itself. No actual OFF dependency was found in this sampled scope, so this is not
  a CRITICAL launch-blocker under the hard rule's own carve-out language, but it is a documentation/
  consistency gap relative to how other categories record the same enforcement. See F-V4 (MEDIUM).
- **Verdict: PASS** (no OFF dependency found) in sampled scope — not exhaustive across all 23 products'
  full traces.

---

## Track C — Challenge

### C5. Consumer strings defensibility (incl. filter-chip/caveat count check vs actual corpus)

**Category identity/count claims — all verified TRUE:**
- `chocolateBarsMetadataLine` is built as a template literal off `chocolateBarsProducts.length`
  (`${chocolateBarsProducts.length} חטיפי שוקולד בדף...`, in
  `bari-web/src/lib/comparisons/chocolate-bars-comparison-page-data.ts`) — **not a hardcoded number.** It
  will always equal the live array length (23). This is architecturally immune to the exact stale-count
  bug class that produced the cakes CRITICAL (F-C1 there was a static `page_copy.filters[].count` baked
  into JSON at generation time and never recomputed).
- Prologue sugar-range claim: "27 עד 60 גרם סוכר ל-100 גרם" (27 to 60g sugar/100g) — actual corpus range
  is **27.0-59.6g**, verified programmatically across all 23. **TRUE** (59.6 rounds to 60 in prose; not a
  fabrication).
- Prologue majority claim: "וברוב המדף מעל 45" (and most of the shelf above 45) — actual: **19/23 (83%)**
  have sugar > 45g. **TRUE.**

**Filter-chip architecture — GOOD, structurally different from the cakes bug class:**
`bari-web/src/lib/comparisons/chocolate-bars-shelf-filters.ts` computes all three filter chips
(`sugar-low` ≤50g, `sugar-high` >50g, `has-real-food` name-keyword match) **live against
`product.expansion.nutrition.sugar` / `product.name`** at click-time — no chip bakes in a static count
string in its `label` the way cakes did ("(20)", "(45)"). Verified `expansion.nutrition.sugar` matches
`nutrition_per_100g.sugars_g` exactly for the sampled product. **This page cannot reproduce the cakes
CRITICAL by construction.**

**However, a real defect found in the `has-real-food` filter's underlying logic (not a stale-count bug,
a keyword-matching gap):**
The filter matches only if `product.name` (the brand-stripped generic name, e.g. "חטיף בודד" for
Snickers/Twix/Bounty alike) contains one of `["בוטן","אגוז","שקד","פיסטוק","קשיו"]`. Computed against the
live 23-product array: **only 1/23 products match** (barcode 72917329, "חטיף שוקולד אגוזי"). But the
page's own row copy repeatedly names peanuts/almonds/hazelnuts as the central scoring driver for at least
5 more products that do NOT match the filter: Snickers (5000159560511) — insightLine: "הבוטנים שבפנים...
מובילים את המדף הזה" (peanuts inside lead the shelf); Snickers Creamy (5900951310379) — "בוטנים פותחים את
הרשימה... החלבון הגבוה במדף" (peanuts open the list, highest protein); Click Nougat ×3 variants
(7290116536774, 7290116532011, 7290100249086) — all explicitly discuss 8.4%-14.1% almonds/hazelnuts in
the filling; the peanut bar (34000250103) — "בוטנים טחונים אמיתיים כאן, 22%" (real ground peanuts, 22%).
A consumer who reads Snickers' own row (which leads with "the peanuts inside") and clicks the "אגוזים /
בוטנים" (Nuts/Peanuts) filter chip to find similar products gets a near-empty result set that **excludes
Snickers itself** — the exact product whose copy motivated the click. This is a real, reproducible
UX/data-accuracy defect, distinct from (and arguably subtler than) the cakes stale-count bug: the chip
doesn't lie about a count, but it silently fails to surface products the page's own editorial voice
identifies as belonging to that filter. See F-C1 (HIGH).

**insightLine / rowVerdict spot-check (8 products, overlapping with V1 sample plus superlative sample):**
all checked strings trace to real nutrition/ingredient fields — no fabricated numbers found in this
sample (see C6 below for the superlative-specific rank-checks).

### C6. Superlatives rank-checked vs the full 23-product corpus

| Barcode | Claim | Scope | Verified rank | Verdict |
|---|---|---|---|---|
| 5000159560511 (Snickers) | "leads this shelf" (score 25.5) | all 23 | #1 of 23 (25.5; next 23.7) | **Verified correct** |
| 7290110571405 (mini Time Out) | "lowest sugar on the shelf" (27g) | all 23 | #1 lowest of 23 (27.0g; next 39.0g — real gap) | **Verified correct** |
| 5900951310379 (Snickers Creamy) | "highest protein on the shelf" (10.1g) AND "second-highest sodium" (227.5mg) | all 23 | protein #1 of 23 (10.1 vs #2 9.6); sodium #2 of 23 (227.5, behind 304.0) | **Both verified correct** |
| 5000159561976 (Bounty) | "holds three records simultaneously: highest sugar, highest sat fat, lowest protein" | all 23 | sugar #1 (59.6 vs #2 56.5); sat fat #1 (21.2 vs #2 17.5); protein lowest #1 (3.7 vs #2 4.5) | **All 3 verified correct** |
| 34000250103 (peanut bar) | "highest sodium on the whole shelf" (304mg) | all 23 | #1 of 23 (304 vs #2 227.5 — real gap) | **Verified correct** |
| 7290105362377 (Kif Kef) | "highest sat fat among wafer bars" | wafer subgroup (KitKat Chunky Funky 15.2, Kif Kef 17.5, Twist 15.0), n=3 | #1 of 3 (17.5) | **Verified correct** |
| 5000159559485 (Twix) | "protein almost the lowest on the shelf" (4.5g, hedged not claimed #1) | all 23 | #2 lowest of 23 (4.5, only 0.8g behind Bounty's 3.7) | **Verified correct, correctly hedged (not overclaimed as #1)** |
| 72991008 / 7290106651265 (Time Out twins) | "identical product, only the pack calls it 'Megadim'" | n/a (identity claim) | nutrition_per_100g byte-identical (sugar 46.0, satfat 16.4, sodium 62.0, all fields) AND ingredients string byte-identical | **Verified correct — genuine data twin, not a fabricated claim** |

**8/8 rank-checked superlative and identity claims hold up exactly against the real 23-product corpus (or
the correctly identified named subgroup, e.g. wafer bars n=3).** No fabricated or unverifiable
"highest/lowest/only" claim found in this sample — genuinely clean result, listed in Clean below.

### C7. Phrasing (owner rules: em-dash, "X not Y" antithesis, grade-letter-as-crutch)

Swept: `insightLine`, `rowVerdict`, `expansion.comparisonContext`, `expansion.positiveSignals[]`,
`expansion.limitingFactors[]` for all 23 products, plus page-level `hero.title`, all 3
`prologueSentences`, all 3 `categoryNote` paragraphs, both `methodologyLines`, and the SEO
`metaDescription`.

- **Em-dash ("—") count: 40 total** — 32 in product-level `expansion` fields (mostly the
  "number — context" template pattern in `positiveSignals`/`limitingFactors`, e.g. "51.8 גרם סוכר ל-100
  גרם — בין הגבוהים במדף"), **8 in page-level copy** (hero title; prologue sentences 1 and 2 [2 dashes in
  sentence 2]; categoryNote paragraph 2; both methodology lines; the SEO metaDescription), plus a further
  **9 in `d4_additives.function_he`** disclosure strings (e.g. "חומר תחליב — מרכך לחם ומייצב שומן") — this
  last group is the pre-flagged **known systemic RT-480-3 class** (site-wide templated additive-disclosure
  em-dashes), noted here for completeness but NOT counted as a new per-page finding per the task's own
  framing. The 40 product/page-level dashes ARE new-to-this-page findings. Volume is high relative to the
  "minimize" guidance; routes to `content-agent`. See F-C4 (MEDIUM — volume, not a hard ban).
- **"X, not Y" antithesis pattern (regex `,\s*ו?לא\s` or literal `אלא`): 6 hits, all real:**
  1. **`hero.title` (the single most prominent string on the page):** *"חטיפי השוקולד האלה הם חטיפי ממתק,
     **לא** חטיפי ביניים — וכולם יודעים את זה"* ("these chocolate bars are candy bars, not snack bars —
     and everyone knows it"). Textbook banned construction, stacked with an em-dash, on the hero.
  2. SEO `metaDescription`: *"...מידע, **לא** המלצה"* ("information, not a recommendation").
  3. Product 5000159560511 (Snickers) `expansion.comparisonContext`: *"יש בו אוכל אמיתי אחד, בוטנים,
     **ולא** רק סוכר ושמן מתחת לציפוי"* ("it has one real food ingredient, peanuts, and not just sugar
     and oil under the coating").
  4. Product 5000159560511 `expansion.limitingFactors[1]`: *"490 קלוריות ל-100 גרם — צפיפות קלורית של
     ממתק, **לא** של חטיף ביניים"* ("calorie density of candy, not of a snack bar").
  5. Product 72991008 (Time Out) `expansion.comparisonContext`: *"...**לא** בזכות משהו שיש בו, **אלא**
     בזכות מה שאין בו"* ("not because of something it has, but rather because of what it lacks") — the
     full "לא X אלא Y" define-by-negation form the owner explicitly banned.
  6. Product 7290110571405 (mini Time Out) `expansion.comparisonContext`: *"...נובע מהחלפת סוכר בשומן
     וקמח, **לא** מהפיכתו לחטיף ביניים אמיתי"* ("comes from swapping sugar for fat and flour, not from it
     becoming an actual snack bar").
  See F-C2 (HIGH — explicit, named, standing owner ruling; 2 of the 6 hits are on the page's single most
  visible strings — the hero title and the SEO meta description — not buried in row-level detail).
- **Grade-letter-as-crutch** (regex for "ציון [A-E]" inside insightLine/rowVerdict/comparisonContext):
  **0 hits** in product-level copy. **1 hit at the category-note level** — `categoryNote` paragraph 1
  explicitly states "כל מוצר במדף הזה מקבל ציון E" (every product on this shelf gets grade E) — this is
  arguably NOT a "crutch" in the banned sense (it's disclosing the structural fact that the whole category
  clusters at one grade, which is itself an editorial finding worth stating, not leaning on the letter to
  avoid explaining a score) but is flagged for awareness since it is a literal grade-letter mention. Judged
  Clean/non-violating given context, but noted.

### C8. Confidence honesty / proportionality

- All 23/23 products carry `confidence: "verified"`, with populated `confidence_sub_reason` ("נתוני תזונה
  ורכיבים ישירות מדף המוצר בשופרסל" — nutrition data and ingredients directly from the Shufersal product
  page) uniformly.
- `confidence_tooltip_he` text: "הציון מבוסס על פאנל התזונה ורשימת הרכיבים שפורסמו למוצר" ("the score is
  based on the nutrition panel and ingredient list published for the product") — this is **modest,
  accurate phrasing** that does NOT claim "all data" or "complete data" the way the cakes tooltip did
  ("כל הנתונים התזונתיים... נסרקו" — flagged there as an overclaim given 82% null fiber). Here, despite
  19/23 (83%) products also having null `dietary_fiber_g`, the tooltip never claims completeness — it
  only claims the score is based on what was published. **No confidence-honesty violation found; this is
  cleaner phrasing than the cakes precedent.** Listed in Clean below.
- No INSUFFICIENT-confidence products found in the live 23 (consistent with "verified" being the only
  value present) — nothing to check for correct-discard in this category.
- Proportionality: spot-checked adjacent-rank score gaps across the full sorted list (25.5, 23.7, 23.7,
  21.3, 19.5, 19.3, 18.3, 17.9, 17.9, 17.6, 17.4, 17.3, 17.2, 17.0, 16.5, 16.3, 16.0, 15.9, 15.8, 15.1,
  13.8, 13.2, 12.3) — largest adjacent gap is 2.4 points (21.3→19.5); most gaps are ≤1.0. No unexplained
  double-digit gap between adjacent products found in the full ranked list (not just a sample — the full
  23-product list was checked here since it's short enough to review exhaustively). **Clean.**

---

## Product-by-Product Assessment (sampled products only — not full 23)

| Barcode | Product | Score | Grade | RT Assessment | Confidence | Critical Notes |
|---|---|---|---|---|---|---|
| 5000159560511 | סניקרס חטיף בודד (Snickers) | 25.5 | E | Justified — score movement fully explained by TASK-455 (trace 20.9, snack_bar_granola misclassification); superlative "leads shelf" verified #1/23; but comparisonContext + limitingFactors both carry antithesis violations | verified | F-C2 (×2 antithesis hits on this product); has-real-food filter excludes it despite copy naming peanuts as the driver (F-C1) |
| 72991008 | שוקולד פסק זמן קלאסי (Time Out) | 23.7 | E | Justified — trace-explained; twin-identity claim with 7290106651265 verified byte-identical; but comparisonContext carries the full "לא X אלא Y" banned construction | verified | F-C2 |
| 7290106651265 | פסק זמן קלאסי מגדים (Time Out multipack) | 23.7 | E | Justified — confirmed genuine data twin of 72991008 (nutrition + ingredients byte-identical) | verified | none |
| 7290116536781 | קליק אין קרם חלבי | 21.3 | E | Justified — trace-explained (delta +3.7) | verified | none |
| 5900951310379 | סניקרס קרימי חטיף בודד (Snickers Creamy) | 19.3 | E | Justified — both superlative claims (highest protein, 2nd-highest sodium) verified TRUE | verified | has-real-food filter excludes it despite peanut-led copy (F-C1) |
| 7290116537375 | קליק כריות | 17.6 | E | Justified — trace-explained (delta +2.6) | verified | none |
| 7290110571405 | מיני פינוקיות פסק זמן (mini Time Out) | 17.9 | E | Justified — "lowest sugar" superlative verified #1/23 (27.0g); comparisonContext carries antithesis violation | verified | F-C2 |
| 3800020401552 | קיט קט צ'אנקי פאנקי (KitKat) | 17.2 | E | Justified — trace-explained (delta +1.5); ingredient-handoff clean | verified | none |
| 7290105362377 | כיף כף מגדים (Kif Kef) | 16.3 | E | Justified — "highest sat fat among wafer bars" superlative verified #1/3 of correctly-scoped subgroup | verified | none |
| 72917367 | חטיף שוקולד טעמי | 16.0 | E | Justified — trace-explained (delta +1.6) | verified | none |
| 5000159561976 | באונטי חטיף בודד (Bounty) | 15.9 | E | Justified — all 3 simultaneous-record claims (sugar/satfat/protein) verified TRUE against full corpus | verified | none |
| 5000159559485 | טוויקס חטיף בודד (Twix) | 16.5 | E | Justified — "almost lowest protein" correctly hedged as #2, not overclaimed as #1 | verified | none |
| 7290116534442 | חטיף שוקולד קרם חלבי | 13.8 | E | Justified — trace-explained (delta +0.9, smallest in sample) | verified | none |
| 34000250103 | חטיף שוקולד ממולא בוטנים (peanut bar) | 12.3 | E | Justified — "highest sodium on shelf" superlative verified #1/23 (304mg); ingredient-handoff clean | verified | has-real-food filter excludes it despite copy naming ground peanuts as 22% of product (F-C1) |

---

## Clean (verified) list

- **Metadata line architecture:** `chocolateBarsMetadataLine` is computed live off `.length` (not
  hardcoded) — structurally immune to the cakes stale-count bug class.
- **Filter-chip computation:** all 3 chips (`sugar-low`, `sugar-high`, `has-real-food`) recompute live
  against real product fields at click-time, no baked-in count strings in labels.
- **Rank/order/dedup (V3):** rank field = index+1 for all 23 (0 mismatches); scores strictly
  non-increasing (0 inversions); 0 duplicate ids/barcodes; `categoryTotal` uniformly 23.
- **Product count vs `_meta.product_count`:** exact match (23 = 23).
- **`_scoring_trace.category` debug mirror:** correctly refreshed to `chocolate` on all 23 (was
  `snack_bar_granola` pre-TASK-455) — confirms the reflow was applied uniformly, not partially.
- **Grade re-derivation:** independently recomputed `frontendGradeFromScore()` matches stored `grade` on
  all 8 V1-sampled products.
- **Superlatives (C6):** 8/8 rank-checked "highest/lowest/only/identical-twin" claims verified TRUE
  against the real 23-product corpus or the correctly-scoped named subgroup (wafer bars n=3). No
  fabricated or unverifiable superlative found — includes a genuinely-verified byte-identical product-twin
  claim (Time Out vs Time Out Megadim).
- **Ingredient-handoff (V2):** 5/5 sampled products show BSIP1 `ingredient_order` populated and BSIP2
  `ingredient_count` > 0 — no REAL_LOSS-57-class handoff-zero bug found.
- **OFF ban (V4):** 0 OFF references in the live JSON or 13 sampled trace/BSIP1 files.
- **Confidence tooltip honesty (C8):** phrasing is modest and accurate ("score based on published panel")
  — does not overclaim "all data" the way the cakes precedent did, despite a comparable null-fiber rate
  (83% here vs 82% there).
- **Proportionality (C8):** full 23-product adjacent-gap scan (not just a sample) found no unexplained
  double-digit gap; largest gap is 2.4 points.
- **Grade-letter-as-crutch (C7):** 0 hits in product-level copy (the 1 category-note-level mention is
  contextually a disclosure of genuine category clustering, not an explanatory shortcut).

---

## Findings by Severity

**No CRITICAL findings.** All findings below are HIGH or MEDIUM.

### HIGH — should resolve before launch

**F-C2: Two "X, not Y" antithesis-pattern violations on the page's two single most prominent strings
(hero title, SEO meta description), plus 4 more in product-level copy — 6 total.**
- Evidence: `hero.title` (`bari-web/src/lib/comparisons/chocolate-bars-comparison-page-data.ts:43`):
  *"חטיפי השוקולד האלה הם חטיפי ממתק, **לא** חטיפי ביניים — וכולם יודעים את זה."* SEO `metaDescription`
  (line 68): *"...מידע, **לא** המלצה."* Product-level: 5000159560511 `comparisonContext` + `limitingFactors[1]`
  (2 hits), 72991008 `comparisonContext` (full "לא X אלא Y" form), 7290110571405 `comparisonContext`.
- Implication: the standing owner ruling bans this construction project-wide with no stated exception for
  hero titles or meta descriptions — and unlike the cakes precedent (where the 2 hits were in a caveat box
  and one row), here one hit is literally the largest text on the page (the H1-equivalent hero) and
  another is the `<meta description>` tag search engines and social shares surface before a user even
  clicks through.
- Repro: `git show origin/master:bari-web/src/lib/comparisons/chocolate-bars-comparison-page-data.ts` lines
  43, 68; regex `,\s*ו?לא\s` or literal `אלא` over all 23 products' `expansion.comparisonContext` and
  `expansion.limitingFactors[]`.
- Routes to: `content-agent`.

**F-V1: No committed BSIP2 trace file on disk reproduces the current live score for any sampled
chocolate-bars product — but the gap is fully explained by one named, two-gate-signed commit.**
- Evidence: the only committed trace directory (`fresh_rescore_task391_20260624_113405`, generated
  2026-06-24) scores every sampled product under `category: "snack_bar_granola"`. TASK-455
  (`f026f2dd`, 2026-07-02) fixed the router to classify chocolate as `category: "chocolate"` with its own
  calorie regime + endemic sat-fat carve-out, re-scoring both chocolate shelves. 8/8 sampled products show
  live score strictly above trace `final_score_estimate` (deltas +0.9 to +4.6), matching the commit
  message's own claim ("chocolate_bars: 23/23 score-moves, all up, 0 grade flips") exactly in direction,
  count, and grade-stability.
- Implication: an outside reviewer cannot point at one committed file and get today's exact chocolate-bars
  score for any product — reproduction requires knowing to apply the TASK-455 delta on top of the stale
  trace. This is a process gap, not evidence of a wrong score (the movement is fully named and two-gate
  signed), and it is a **cleaner** version of the same finding on bread/cakes (single commit fully
  explains it here, vs. two chained commits needed for cakes).
- Repro: `git show origin/master:02_products/chocolate/bsip2_outputs/fresh_rescore_task391_20260624_113405/products/bsip1_5000159560511/bsip2_trace.json`
  → `final_score_estimate=20.9`, `category="snack_bar_granola"` vs live `score=25.5`, delta +4.6.
- Routes to: `data-agent` (regenerate and commit a current BSIP2 trace snapshot for chocolate reflecting
  TASK-455, so V1 reproduces cleanly against a single artifact going forward).

**F-C1: The `has-real-food` (אגוזים / בוטנים / "Nuts/Peanuts") filter chip matches only 1 of 23 products,
silently excluding at least 5 products whose own row copy names peanuts/nuts as the central scoring
driver — including the #1-ranked product.**
- Evidence: `bari-web/src/lib/comparisons/chocolate-bars-shelf-filters.ts` matches `product.name` (the
  brand-stripped generic name, e.g. "חטיף בודד" for Snickers/Twix/Bounty alike) against keywords
  `["בוטן","אגוז","שקד","פיסטוק","קשיו"]`. Computed live against the 23-product corpus: only barcode
  72917329 matches. But Snickers (5000159560511, rank #1, score 25.5) — whose own `insightLine` reads "the
  peanuts inside... lead this shelf" — does not match; nor does Snickers Creamy (5900951310379, "highest
  protein on the shelf" from peanuts), nor 3 Click Nougat variants (7290116536774/7290116532011/
  7290100249086, each discussing 8.4-14.1% almonds/hazelnuts), nor the peanut bar (34000250103, "22%
  ground peanuts").
- Implication: a consumer who reads the #1 product's own copy (which leads with "the peanuts inside") and
  clicks the filter chip meant to surface products like it gets a near-empty result that excludes that
  exact product. This is a functional navigation defect, not a data-fabrication issue — the underlying
  nutrition/ingredient data is correct, only the filter's keyword-matching field/list is too narrow.
- Repro: `bari-web/src/lib/comparisons/chocolate-bars-shelf-filters.ts` `REAL_FOOD_KEYWORDS` matched
  against `.name` field of all 23 live products (both `name` and `name_he` give the same 1/23 result,
  since brand-stripped generic names rarely contain the ingredient keyword even when the row copy does).
- Routes to: `frontend-agent` (the filter needs either a broader keyword list matched against a field that
  actually carries the ingredient signal, or a dedicated `_has_real_food` boolean computed at generation
  time from the parsed ingredient list, mirroring how `has_phvo` works on the cakes page).

### MEDIUM — should document or monitor

**F-V2: BSIP2 `ingredient_count` diverges from BSIP1 `ingredient_order` length in 3 of 5 sampled
products (populated on both sides, not a zero/loss bug, but not interchangeable).**
- Evidence: 7290116536781 (30 vs 33), 5900951310379 (19 vs 34), 34000250103 (23 vs 36) — BSIP2 count is
  meaningfully higher than BSIP1's parsed order-list length in each case; the other 2/5 sampled products
  matched exactly (5000159560511: 14=14; 3800020401552: 16 vs 18, a small gap).
- Implication: not the REAL_LOSS-57 handoff-zero class (no product showed populated BSIP1 + zero BSIP2),
  but the two fields are clearly using different counting methodologies (likely sub-tokenization of
  parenthetical/compound ingredient entries) and should not be treated as interchangeable by any future
  consumer of either field.
- Routes to: `data-agent` (confirm intended counting methodology; document the expected divergence or fix
  the discrepancy).

**F-V3: The 6 chocolate-bar products excluded from the live 23-product page (of 29 scored) carry only a
bucket label (`CORPUS_NOT_DISPLAYED`) as their documented reason, not an actual cause.**
- Evidence: `03_operations/page_generator/configs/chocolate_bars.json` `exclusions: []` (empty structured
  field); the only explanation is prose in the config's `_comment`. Independently verified all 6 excluded
  barcodes carry `evaluation_status: standard` with plausible scores (14.5-17.1) — nothing distinguishes
  them as data-quality failures. Name comparison against the displayed 23 strongly suggests a real,
  defensible editorial rule (one card per single-serving SKU; multi-packs and Passover-kosher seasonal
  variants of already-displayed products excluded) — but this inference had to be reconstructed by this
  report, it is not stated as a rule anywhere in the config or `_meta`.
- Implication: G3 ("dropped/excluded documented") is only nominally satisfied — a bucket name exists, but
  the actual selection rule is not written down, so it cannot be verified as applied consistently without
  manual reconstruction (as done here).
- Routes to: `data-agent` (add the actual selection rule — e.g. "one card per single-serving SKU;
  multi-pack/seasonal-variant duplicates of a displayed SKU excluded" — as a structured, verifiable
  `exclusions[]` entry per barcode, replacing the bucket label).

**F-V4: No machine-checkable `_meta.off_used` flag on the chocolate-bars live JSON (unlike the cakes
precedent, which carries one).**
- Evidence: `chocolate_bars_frontend_v1.json` `_meta` keys checked — no `off_used` or equivalent field.
  The only OFF-clean assertion is prose in the page-generator config's `_comment` ("OFF check = PASS").
  No actual OFF dependency was found in this report's sampled scope (0/8 traces, 0/5 BSIP1 files, 0 in live
  JSON).
- Implication: not a launch blocker (no dependency found), but a documentation-consistency gap — a future
  automated OFF-ban gate check against `_meta` fields across categories would silently skip this category.
- Routes to: `data-agent` (add `_meta.off_used = false` to the served JSON for parity with other
  categories' machine-checkable enforcement record).

**F-C3 (minor): 40 em-dash occurrences across product/page-level copy (32 product-level, 8 page-level),
plus 9 more in the pre-flagged systemic `d4_additives.function_he` class (not counted as new).**
- Evidence: see C7 above for full breakdown by field/product.
- Implication: within the "minimize, don't ban" owner guidance, not a hard violation, but the volume
  (40 new-to-this-page occurrences) is high, concentrated in a repeating "number — context" template
  pattern across `positiveSignals`/`limitingFactors`.
- Routes to: `content-agent`.

**F-C4 (minor): `categoryNote` explicitly states "כל מוצר במדף הזה מקבל ציון E" (every product on this
shelf gets grade E) — a literal grade-letter mention at the category-caveat level.**
- Evidence: `chocolateBarsCategoryNote` paragraph 1.
- Implication: judged NOT a "grade-letter-as-crutch" violation in the banned sense (it discloses a genuine
  structural finding — the whole category clusters at E — rather than substituting the letter for an
  explanation; the same paragraph immediately explains why: "זו קטגוריה אחת של ממתקים"). Flagged for
  awareness only, not routed as an action item.

---

## Verdict

**GO-WITH-FINDINGS.**

**0 CRITICAL.** 2 HIGH (F-C2 antithesis on the hero title + SEO meta description; F-C1 the nuts/peanuts
filter chip silently excludes the products its own copy names as nut-driven, including the #1-ranked
product). 4 MEDIUM (F-V2 ingredient-count methodology divergence; F-V3 undocumented exclusion rule for 6
of 29 scored bars; F-V4 missing `_meta.off_used` parity flag; F-C3 em-dash volume). 1 minor note (F-C4
category-note grade mention, judged non-violating).

Per this agent's own Hard Rule 10, neither open HIGH finding blocks launch by the letter of the rule
("HIGH requires acknowledgment, not necessarily resolution") — and per the unified D10 gate definition,
launch is blocked only on open CRITICAL. **There are zero CRITICAL findings in this report**, which is a
meaningfully cleaner result than the cakes report (1 CRITICAL) reviewed for template/depth comparison.

That said, both HIGH findings are genuinely worth prompt attention before this page is put in front of the
owner or a consumer, because of where they sit: F-C2's worst instance is the hero title — the single
largest, first-read string on the page — and F-C1 is a functional defect a consumer can trigger in one
click on the page's own #1-ranked product. Neither requires touching a scoring number or a frozen
invariant; both are copy/frontend-logic fixes.

**Summary assessment:** Justified. The scoring engine's output for chocolate-bars holds up cleanly under
adversarial reproduction pressure — every one of 8 sampled score deltas is fully and precisely explained
by one named, two-gate-signed commit (TASK-455/`f026f2dd`), matching that commit's own claims exactly
(23/23 up-moves, 0 grade-flips); 8/8 rank-checked superlative and product-identity claims verified TRUE
against the real 23-product corpus; the metadata line and filter-chip counts are architecturally immune to
the stale-count bug class that produced the cakes CRITICAL; confidence-tooltip phrasing is honest and
does not overclaim completeness despite a comparable null-fiber rate to cakes. The two HIGH findings are
real but narrowly scoped (a phrasing-rule violation on 2 prominent strings + 4 product-level instances;
a filter-matching gap on 1 UI control) — they do not implicate the underlying scores, ingredient data, or
category identity.

**Recommendation for Product Agent's go/no-go:** no tripwire is implicated (no frozen invariant, no
scoring-philosophy change, nothing irreversible at stake — both open HIGH findings are reversible
copy/logic fixes). This agent takes no position on timeline; it reports that F-C1 and F-C2 are open and
that F-V1 (trace-reproducibility) should be closed promptly given it will compound on the next re-flow,
same caution as raised for bread/cakes.

**Scope reminder:** this report covers chocolate-**bars** only (`/hashvaot/chocolate-bars`, 23 products).
Chocolate-**tablets** (`/hashvaot/chocolate-tablets`, separate frontend JSON, separate route) is the next
task and is NOT covered by this report, despite sharing the same corpus root, BSIP0/BSIP1/BSIP2 run, and
TASK-455 commit.
