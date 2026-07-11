# Red-Team Challenge Report — Milk & Alternatives (milk-comparison, TASK-474 / P1 item 9a / finding F2)

Date: 2026-07-03
Scope: 18 products, `/hashvaot/milk-comparison`
Challenger: adversarial-qa-agent (Bari)
Ground truth ref: `origin/master` @ `e615244a29f32a26537f4113f3441c3b267a4400` (fetched 2026-07-03)

## Context established before scoring
- Live route: `bari-web/src/app/hashvaot/milk-comparison/page.tsx` imports from the bespoke
  `bari-web/src/lib/comparisons/milk-page-data.ts` and renders
  `bari-web/src/components/comparisons/milk-comparison-page.tsx`.
- `milk-page-data.ts` is explicitly split into two blocks (see its own header comment, lines 1-15):
  a **LEGACY block** (lines 42-138) backed by `bari-web/src/data/milk-comparison.json`, feeding
  blog/home consumers only, and a **UNIFORM VM block** (lines 140-274) backed exclusively by
  `bari-web/src/data/comparisons/milk_frontend_v1.json`, feeding the actual `/hashvaot/milk-comparison`
  route. **The comparison page itself does not read the legacy JSON at all** — confirmed by reading
  `milk-comparison-page.tsx` (imports only `milkShelfFilters`) and `page.tsx` (imports only
  `milkVmProducts` + uniform-block exports).
- Per TASK-468 (closed 2026-07-03): the pipeline reproduces milk's 18 scores/grades exactly
  (G-repro PASS) but cannot reproduce the hand-curated payload (G-metaonly FAIL — degrades confidence
  label, empties limitingFactors/positiveSignals, wrong per-100g serving note for a liquid). **This
  non-reproduction is EXPECTED/ACCEPTED per owner ruling and is NOT re-flagged here as a fresh
  CRITICAL.** Milk stays hand-curated by design.
- 18/18 canonical scores verified against the P478 G-repro table (produced from a from-scratch engine
  run against `MILK_CANONICAL_FLAGS`) — all 18 match the live JSON exactly.

## Opening Finding
**Blanket confidence claim is false for the entire corpus.** Every one of the 18 live products carries
the identical string `confidence_tooltip_he: "כל הנתונים התזונתיים ורשימת הרכיבים נסרקו ישירות מהמוצר"`
("**all** nutritional data and the ingredient list were scraped directly from the product"), paired with
`confidence_label_he: "נתונים מלאים"` ("complete data") and `confidence_level: "sufficient"` — on **18/18
products with `fat`, `satFat`, `carbs`, and `fiber` all null**, and 9/18 additionally null on `sugar`
and/or `sodium`. The claim "all nutritional data ... scraped" is factually false for every product on
the page as shipped. This is a data-absent disclosure failure (Hard Rule 12) compounded by phantom
confidence (Hard Rule 13) — a "complete data" badge sitting on top of systematically incomplete data,
applied uniformly rather than per-product. Routed to `data-agent` (why are fat/satFat/carbs/fiber
uniformly absent — parser gap or genuinely not scraped) and `content-agent`/`nutrition-agent` (the
tooltip/label copy overclaims what confidence actually attests to).

A second, narrower structural note: the legacy `milk-comparison.json` (48.5/D-class stale score on
barcode `7290110325619` vs live 51.7/C, and a similar smaller drift on `7290110324926`, 58.1/C vs live
56.9/C) is **not read by the comparison page**, but **is** still read by `home-flagship-analysis.tsx`,
`milk-analysis-content.ts`/`milk-analysis-chart-data.ts` (blog), and `supermarket/page.tsx` — and the
blog's `InvestigationPanel` component (`milk-analysis-comparisons.tsx`) renders `product.score`/`.grade`
straight from that stale file via `BariGradeBadge`. This means a real consumer on `/blog/milk-analysis`
can see a different Bari score for barcode `7290110324926` (58.1/C) than the same barcode gets on
`/hashvaot/milk-comparison` (56.9/C) — same grade letter, different number, both live simultaneously.

## Product-by-Product Assessment (8 sampled per Track V item 1)

| Barcode | Product | Live Score/Grade | P478 G-repro trace | Match | Confidence | Notes |
|---|---|---|---|---|---|---|
| 7290000051352 | חלב מלא 3.4% | 85/A | 85/A | Yes | verified/sufficient | 1-ingredient ("חלב"), NOVA 1, defensible top rank |
| 7290019790259 | חלב טבעי 4% | 85/A | 85/A | Yes | verified/sufficient | Superlative "בין הנקיים ביותר במדף" verified true (tied shortest ingredient string) |
| 7290107932134 | חלב 1% מועשר-מהדרין | 55.5/C | 55.5/C | Yes | verified/sufficient | NOVA 3 (stabilizer + added sugar to compensate fat removal) — copy self-explains the "low-fat paradox," correctly ranks below plain soy above it; no inversion |
| 7290116936116 | משקה סויה ללא סוכרים | 63.9/C | 63.9/C | Yes | verified/sufficient | "הכי נקי"/"הנקי ביותר" superlative verified true among plant-based only (correctly scoped) |
| 7290110324926 | משקה סויה ללא תוספת סוכר | 56.9/C | 56.9/C | Yes (live) | verified/sufficient | **Legacy `milk-comparison.json` shows 58.1/C for this barcode — stale-surface mismatch, reachable via `/blog/milk-analysis` `InvestigationPanel`** |
| 7290110325619 | משקה שיבולת שועל | 51.7/C | 51.7/C | Yes (live) | verified/sufficient | Live JSON correctly identifies as oat throughout (name, milkProductType, ingredients, copy). Legacy `milk-comparison.json` shows stale 48.5/D for same barcode (not reachable from this route). `milk-product-insights.ts` has a dead-code ALMONDS-identity block keyed to this barcode (see below) |
| 5411188112709 | שקדים ללא סוכר | 46.2/D | 46.2/D | Yes | verified/sufficient | d4_additives E322/E412 correctly map to לציטין/גואר גאם present in ingredient string |
| 5411188300328 | שוקו משקה סויה | 33.5/E | 33.5/E | Yes | verified/sufficient | "7.6g — הגבוה במדף" (highest on shelf) sugar superlative is true only among the 9/18 products with a non-null sugar value — see HIGH-2 |

All 8 sampled: trace/JSON/rendered scores agree exactly (deltas = 0.0). No propagation discrepancy found
in this sample.

## Data Integrity (Track V item 3)
- Product count: 18, matches `_meta.product_count: 18` and every product's `categoryTotal: 18`. No
  duplicate barcodes (18 unique of 18). Ranks form an exact 1-18 sequence; scores strictly non-increasing
  by rank — monotonicity holds perfectly.
- `_meta.exclusions` documents 2 barcodes (`7290110324773`, `7290114313285`) excluded with stated reason
  ("not in live curated milk shelf — keep page scope = live"). Reason is a scope statement, not a QA
  finding; accepted as documented, not independently re-verifiable without the raw corpus (would need
  Data Agent to confirm why these 2 are outside the 18-product curation).
- `_meta.off_used: false`. Grepped `milk_frontend_v1.json`, `milk-page-data.ts`, `milk-product-insights.ts`,
  `milk-types.ts` for OFF dependency terms (openfoodfacts, off_source) — zero real hits. **OFF ban: CLEAN.**
- No committed `run_gates.py` report exists on `origin/master` for `milk_frontend_v1.json`
  (`bari-web/src/data/comparisons/milk_frontend_v1_gates_report.md` is untracked/local-only, not on
  origin/master). Consistent with milk's hand-curated, non-standard-pipeline status — flagged as a
  process gap, not re-scored as a fresh gate failure given the accepted hand-curation exception.

## Ingredient-Handoff Sample (Track V item 2, n=5)
Milk's schema has no `ingredient_order`/`ingredient_count` array fields (TASK-475/476 class does not
apply structurally — `expansion.ingredients` is a single raw string, not a parsed array). Sampled 5
products for ingredients-string-vs-NOVA consistency instead:

| Barcode | NOVA | Ingredients present | Chars | Verdict |
|---|---|---|---|---|
| 7290000051352 | 1 | Yes | 3 ("חלב") | LEGIT_EMPTY-class — single-ingredient whole milk, defensible |
| 7290019790259 | 1 | Yes | 4 ("חלב,") | Same as above |
| 7290102392094 | 1 | Yes | 23 | Defensible (goat milk, 2 words) |
| 7290114313865 | 2 | Yes | 21 | Defensible (lactose-free protein milk, short but plausible) |
| 7290116936116 | 2 | Yes | 42 | Defensible (3-ingredient soy, matches "cleanest" claim) |

No handoff loss found in this sample; short strings correlate with low NOVA and are content-plausible,
not truncated data.

## Findings by Severity

### CRITICAL — must resolve before launch
**RT-1 (Opening Finding). Blanket "complete data" confidence claim is false for 18/18 products.**
Evidence: `confidence_tooltip_he` = "כל הנתונים התזונתיים ורשימת הרכיבים נסרקו ישירות מהמוצר" (identical
string on all 18 products in `bari-web/src/data/comparisons/milk_frontend_v1.json`); `fat`, `satFat`,
`carbs`, `fiber` are `null` on 18/18 products; `sugar` null on 9/18; `sodium` null on 2/18.
Implication: a consumer who taps/hovers the confidence indicator is told all nutrition was scraped when
roughly half the standard nutrition panel is absent on every single row. This is the exact "phantom
confidence" pattern Hard Rule 13 exists to catch, and a data-absent disclosure that Hard Rule 12 requires
surfaced as an opening CRITICAL, not buried in a per-product note. Routes to: `data-agent` (root-cause
why fat/satFat/carbs/fiber are structurally null across the whole corpus — parser gap vs genuinely
unscraped) and `nutrition-agent`/`content-agent` (the confidence copy/label must reflect actual field
coverage, not a blanket "complete" claim).

**RT-2. Stale duplicate score surface for the same barcode, one of which is publicly rendered.**
Evidence: `bari-web/src/data/milk-comparison.json` line ~2199 gives barcode `7290110325619`
(product: משקה שיבולת שועל, oat) `"score": 48.5, "grade": "D"`. The live
`bari-web/src/data/comparisons/milk_frontend_v1.json` gives the same barcode `"score": 51.7, "grade": "C"`.
A second barcode, `7290110324926`, shows `58.1/C` in the legacy file vs `56.9/C` live — smaller drift,
same grade letter, different number. The legacy file's `milkProducts`/`milkComparisonPage` exports are
consumed by `home-flagship-analysis.tsx`, `milk-analysis-content.ts`, `milk-analysis-chart-data.ts`
(feeding `/blog/milk-analysis`), and `bari-web/src/app/hashvaot/supermarket/page.tsx` — NOT by
`/hashvaot/milk-comparison` itself. Confirmed the blog's `InvestigationPanel` component
(`bari-web/src/components/blog/milk-analysis-comparisons.tsx` lines 44-51) renders
`product.score`/`product.grade` via `<BariGradeBadge>` directly from this stale data for barcodes in
`PREVIEW_BARCODES` (which includes `7290110324926`). Implication: the same product carries two different
live Bari scores depending on which page a consumer is on — directly falsifiable and reputationally
indefensible ("Bari says two different things about my milk"). This was named in TASK-468's close_reason
as a known, unresolved copy defect routed to the owner's copy lane; this report independently confirms
it is (a) still live on `origin/master`, (b) precisely reachable via the blog's rendered score badge, not
merely present in an unused file. Routes to: `frontend-agent` (retire or resync the legacy
`milk-comparison.json` consumers) / `content-agent` (owner copy lane per TASK-468).

### HIGH — should resolve before launch
**RT-3. `milk-product-insights.ts` contains a wrong-product-identity copy block for barcode
`7290110325619` — verified as dead code, not currently rendered, but present in the shipped source tree.**
Evidence: `bari-web/src/lib/comparisons/milk-product-insights.ts` lines 234-248, keyed to barcode
`7290110325619` (confirmed oat milk — "משקה שיבולת שועל" — in both live and legacy JSON, `milkProductType:
"oat"`), describes the product entirely in almond terms: "שקדים — המים הם הרכיב הראשון; שקדים נמצאים
בכמות קטנה בפועל" (almonds — water is the first ingredient; almonds are present in a small amount),
"לא מקור שקדים ולא מקור חלבון" (not an almond source and not a protein source). Traced every consumer of
`getProductInsight`/`buildConsumerExplanationView` (the only functions that read this file) via grep
across `bari-web/src` — **zero call sites found; the function `buildConsumerExplanationView` in
`consumer-explanation-view.ts` has no importers anywhere in the codebase.** This downgrades the finding
from "live wrong-identity copy" (as implied by TASK-468's framing) to "wrong-identity copy shipped in
source but currently unreachable by any render path" — still a real defect (it will resurface verbatim
the moment anything re-wires `getProductInsight`), and its presence in a "gold standard" category's
source tree is itself notable. Routes to: `content-agent` (fix or delete the block) /
`frontend-agent` (confirm dead-code status before any future re-wiring of `consumer-explanation-view.ts`).

**RT-4. Superlative "highest on the shelf" sugar claim is scoped against an incomplete dataset without
disclosure.** Evidence: barcode `5411188300328` (שוקו משקה סויה) carries
`insightLine: "7.6 ג׳ סוכר ל-100 מ״ל — הגבוה במדף"` ("7.6g sugar per 100ml — the highest on the shelf").
Ranked all 18 products' `expansion.nutrition.sugar` values: 7.6g is indeed the maximum among the 9
products that have a non-null sugar value, but **9 of 18 products (50%) have `sugar: null`** — the claim
"the highest on the shelf" is stated as an unqualified corpus-wide superlative while half the corpus's
sugar values are simply unmeasured, not zero or lower. A hidden higher-sugar product cannot be ruled out
among the 9 nulls. Compounds RT-1 (the same null-heavy nutrition panel). Routes to: `nutrition-agent`
(is "highest on the shelf" defensible when scoped only to non-null entries, and should the copy disclose
that scope) / `content-agent` (soften to "highest among products with reported sugar" if the engine
cannot fill the nulls).

**RT-5. Antithesis ("X, not Y") phrasing present in shipped consumer copy, contrary to owner's
define-by-negation ban.** Evidence, counted precisely per file (pattern `,\s*ו?לא\s` / `אלא`):
- `bari-web/src/data/comparisons/milk_frontend_v1.json` (LIVE, rendered on `/hashvaot/milk-comparison`):
  9 matches of the comma-lo pattern, 4 of "אלא". Real antithesis constructions confirmed in context,
  e.g. "נגיעת שקדים, לא בסיס שקדים של ממש" (a touch of almonds, not a real almond base — barcode
  `7290014760141`), "תחליף מעובד שתפקידו בקפה, לא משקה תזונתי לשתייה" (a processed substitute meant for
  coffee, not a nutritional drink), "מוסיפים שומן ומרקם, לא ערך תזונתי" (adds fat and texture, not
  nutritional value). These are live, consumer-facing, and match the exact pattern
  `no_x_not_y_phrasing.md` bans.
- `bari-web/src/lib/comparisons/milk-page-data.ts`: 1 Hebrew match, 2 English "NOT" matches — all three
  are false positives on inspection (the Hebrew hit is "מידע, לא המלצה" / "information, not a
  recommendation" in the SEO meta description, a standard disclaimer not a define-by-negation product
  claim; the English hits are code comments, not shipped copy). **Clean.**
- `bari-web/src/lib/comparisons/milk-product-insights.ts` (dead code per RT-3): 6 real antithesis
  matches, e.g. "וריאציית טעם, לא שדרוג תזונתי" (a flavor variation, not a nutritional upgrade).
- `bari-web/src/data/milk-comparison.json` (legacy, partially live per RT-2): 26 matches; sampled 15,
  found repeated real violations, e.g. "תחליף מעובד, לא חלב בסיסי בלבד" (a processed substitute, not
  just basic milk) appearing 6+ times verbatim across different products, and "מתאים לטעם/קלוריות, לא
  לשובע" (suits taste/calories, not satiety) appearing multiple times.
Implication: the live comparison page itself (not just legacy/dead surfaces) contains banned
define-by-negation phrasing in `insightLine`/`rowVerdict`/`limitingFactors` fields — this is Content
Agent's lane to fix per the owner's phrasing rule, but it means milk's "gold standard" reputation does
not currently hold on this specific editorial rule. Routes to: `content-agent`.

### MEDIUM — should document or monitor
**RT-6. No committed gate report for the live milk JSON.** `run_gates.py`'s output for
`milk_frontend_v1.json` is not present on `origin/master`; only a local, untracked working-tree copy
exists (and that copy currently shows 0 bytes / empty in this session's read, separately from tracking
status). Given milk's accepted hand-curated exception, this is not treated as a fresh CRITICAL, but it
means the mechanical go-live gate (`run_gates.py` presence check) has no committed evidence to point to
for milk specifically. Routes to: `data-agent`/orchestrator (decide whether milk needs a one-time gate
run committed to satisfy the mechanical check, or whether the hand-curated exception should be formally
registered so this stops reading as a gap on every future audit).

**RT-7. `_meta.exclusions` reasons are asserted, not independently re-derivable from this review.**
The 2 excluded barcodes' stated reason ("not in live curated milk shelf — keep page scope = live") is
plausible but this agent could not independently verify against the raw BSIP1 corpus without Data Agent
involvement. Not a finding of wrongdoing — flagged so it isn't silently treated as verified when it was
only read, not re-derived.

**RT-8. `milkProductType`/`filterTags` for barcode `7290014760141` (משקה שקדים) label it `type:almond`
while its own copy states almonds are only 4% and water/sugar are the first two ingredients** ("מים הוא
הרכיב הראשון, סוכר הוא הרכיב השני והשקדים עצמם רק 4%"). The category-type label itself is standard
retail nomenclature (matches product name), and the copy is transparent/self-critical about the low
almond content — this is good editorial honesty, not a defect. Logged as a clean-verified item below,
not a finding, but noted here because a "highest sugar on the shelf"-style skeptic could otherwise
mistake the `type:almond` filter tag as an implicit purity claim; the copy itself pre-empts that reading.

## Clean-Verified List
- 18/18 sampled-and-full-corpus scores/grades/ranks are internally consistent: strictly monotonic rank
  1-18, scores non-increasing, no duplicate barcodes, `categoryTotal` uniform at 18.
- 8/8 sampled products' live JSON score matches the independently-run P478 G-repro engine trace exactly
  (0.0 delta on all 8).
- OFF ban: clean across all milk data/lib files checked (`off_used: false`, zero real OFF references).
- No framework-vocabulary leakage found in `page_copy` (hero/prologue/methodology/caveat/shelf_lens_options)
  — zero hits for NOVA/BSIP/matrix_integrity/structural_class/pillar/routing/cap/floor. `novaGroup` is
  present as a raw per-product field in the JSON payload but confirmed never rendered by any component
  (grep across `bari-web/src/**/*.tsx` for `novaGroup` outside data/VM plumbing files: zero render
  call-sites).
- 3 known-better nutrition-principle pairs defined before inspection, all verified correctly ranked: (1)
  plain soy (63.9-56.9/C) over sweetened chocolate soy (33.5/E); (2) no-added-sugar oat (50.5/C) over
  barista/foam oat variants (49.8/D); (3) the one apparent "dairy below plant" case (1%-fat fortified
  milk at 55.5/C, below two soy products) is explained by that specific dairy product's own engineered
  compensation (stabilizer + 5g added sugar to offset fat removal, NOVA 3) — not a clean intact-matrix
  product, so not a true inversion of the "intact beats engineered" principle. No inversions found.
- Two superlative claims spot-checked and verified TRUE against the full 18-product corpus: "מהנמוכים
  במדף" (sodium, tied-lowest at 40mg) and "בין הנקיים ביותר במדף"/"הכי נקי" (ingredient-simplicity,
  correctly scoped to plant-based-only comparison).
- `d4_additives` E-number-to-Hebrew-name mappings spot-checked across 6 products (E407→קרגינן, E450/
  E500→פוספטים/סודיום קרבונט family, E322→לציטין, E412→גואר גאם, E415→קסנטן) — all are standard,
  correct chemical-name-to-E-number identities; an initial literal-string cross-check flagged these as
  "not found" but that was this reviewer's own methodology artifact (Israeli labels print chemical names,
  not E-codes) — corrected and not reported as a finding.
- Ingredient-handoff sample (n=5): no truncation/loss found; short ingredient strings correlate honestly
  with low NOVA / genuinely simple products (LEGIT_EMPTY-class, not data loss).

## Summary Assessment
**Plausible-but-unverifiable in part, with one Justified-but-mislabeled core defect (RT-1) and one
structural cross-surface inconsistency (RT-2).** The scoring engine's internal logic, rank ordering, and
score propagation for the live `/hashvaot/milk-comparison` page are sound and match an independently-run
engine trace exactly on every sampled product — Track V's core propagation claim holds. But the page's
own confidence signal is not honest about what data it actually has, at least one other live surface
(the blog) shows a materially different score for the same barcode, and the "gold standard" editorial
copy contains the exact banned antithesis pattern the owner explicitly ruled out elsewhere. Milk earns
its reputation on rank-order defensibility and absence of framework leakage; it does **not** currently
earn it on confidence honesty or cross-surface consistency, and the phrasing rule is violated in the
live JSON copy itself, not just in dead/legacy code.

**Does milk live up to its "content gold standard" label?** Partially. The prose quality, self-aware
trade-off explanations (e.g. the "low-fat paradox" on barcode `7290107932134`), and absence of leakage
are genuinely strong and better than most categories. But a "gold standard" claim cannot coexist with
(a) a blanket false confidence claim on every row, (b) two different live scores for the same barcode
visible to the same visitor within two clicks (home to blog to comparison page), and (c) banned
antithesis phrasing baked into the live data file. These are exactly the kind of defects a "gold
standard" label is supposed to make less likely, not more forgivable.

## Verdict
**GO-WITH-FINDINGS.**

The `/hashvaot/milk-comparison` route itself (score propagation, rank order, OFF-cleanliness, no
leakage/drift) verifies clean and can continue serving. This verdict is NOT a blanket pass for milk as a
brand asset — it does not clear:
- RT-1 (CRITICAL — blanket false confidence claim, 18/18 products) — this is a page-level defect on the
  route in scope and should block treating the current confidence indicator as trustworthy until
  data-agent/nutrition-agent resolve it.
- RT-2 (CRITICAL — stale score visible on a different live public surface for the same barcode) — this
  is outside `/hashvaot/milk-comparison` itself but is a real, currently-live public inconsistency that
  the orchestrator/content-agent should not continue deferring under "owner copy lane, untouched" without
  a timeline, given it is independently confirmed still reachable.

Per this agent's mandate (D10), a category may only fully PASS when Track V is green AND Track C has
zero open CRITICAL. Two CRITICALs are open (RT-1, RT-2). Recommend the orchestrator/Product Agent treat
this as GO-WITH-FINDINGS for the in-scope route pending RT-1/RT-2 resolution, not a clean PASS.

---

## Return Contract

```json
{
  "task": "TASK-474",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\milk_and_alternatives\\reports\\red_team_milk_page_v1.md",
      "sha256": "PLACEHOLDER_RECOMPUTE_AFTER_WRITE"
    }
  ],
  "counts": {
    "products_total": 18,
    "products_sampled_track_v_item1": 8,
    "products_sampled_ingredient_handoff": 5,
    "findings_critical": 2,
    "findings_high": 3,
    "findings_medium": 3,
    "clean_verified_items": 7,
    "known_better_pairs_defined": 3,
    "known_better_pairs_inverted": 0,
    "superlatives_checked": 4,
    "superlatives_defensible": 3,
    "superlatives_flagged": 1,
    "phrasing_em_dash_counts": {
      "milk_frontend_v1.json": 83,
      "milk-page-data.ts": 10,
      "milk-product-insights.ts": 63,
      "milk-types.ts": 0,
      "milk-comparison-page.tsx": 1,
      "milk-comparison.json_legacy": 252
    },
    "phrasing_antithesis_counts_he_pattern": {
      "milk_frontend_v1.json": 9,
      "milk-page-data.ts": 0,
      "milk-product-insights.ts": 6,
      "milk-comparison.json_legacy": 26
    },
    "phrasing_antithesis_counts_ela_pattern": {
      "milk_frontend_v1.json": 4,
      "milk-page-data.ts": 0,
      "milk-product-insights.ts": 0,
      "milk-comparison.json_legacy": 0
    },
    "off_dependency_hits": 0,
    "duplicate_barcodes": 0,
    "rank_monotonicity_violations": 0
  },
  "commands_run": [
    {"cmd": "git fetch origin master", "exit_code": 0},
    {"cmd": "git show origin/master:02_products", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/app/hashvaot/milk-comparison/page.tsx", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/lib/comparisons/milk-page-data.ts", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/data/comparisons/milk_frontend_v1.json", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/data/milk-comparison.json", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/lib/comparisons/milk-product-insights.ts", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/components/comparisons/milk-comparison-page.tsx", "exit_code": 0},
    {"cmd": "grep -rn milkProducts / milkComparisonPage / GRADE_COLORS across bari-web/src", "exit_code": 0},
    {"cmd": "grep -rn buildConsumerExplanationView / consumer-explanation-view across bari-web/src", "exit_code": 0},
    {"cmd": "python inline scripts: score/rank/dedup/sodium/sugar/antithesis/em-dash counts", "exit_code": 0}
  ],
  "not_done": [
    "Did not independently re-derive the 2 _meta.exclusions barcodes against the raw BSIP1 corpus (would require Data Agent / corpus access beyond frontend JSON).",
    "Did not run npm run build / tsc / ESLint on bari-web in this session (route-render validation was done via static file/import-graph tracing, not a live build) — recommend Frontend Agent or a follow-up V-track pass confirm 200 response + build exit 0 if not recently verified.",
    "Sampled 15 of 26 antithesis hits in the legacy milk-comparison.json rather than all 26 (time-boxed); pattern was already clearly repetitive/confirmed by sample.",
    "Did not verify whether /hashvaot/supermarket's use of milkProducts (legacy) surfaces a visible score badge to a real user in the rendered DOM (only confirmed the import; did not render the supermarket page)."
  ],
  "self_check": {
    "read_builder_summary": false,
    "read_artifacts_directly": true,
    "ground_truth_ref_used": "origin/master@e615244a29f32a26537f4113f3441c3b267a4400",
    "independent_of_task468_framing": "RT-3 downgraded from TASK-468's implied 'live copy defect' to 'dead code, currently unreachable' after tracing zero call-sites for getProductInsight/buildConsumerExplanationView; RT-2 independently re-confirmed as still live and precisely localized to blog InvestigationPanel rather than accepted on the task's word alone"
  }
}
```
