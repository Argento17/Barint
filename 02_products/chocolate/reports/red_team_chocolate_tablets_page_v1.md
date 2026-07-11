# Red-Team Challenge Report — Chocolate Tablets (`/hashvaot/chocolate-tablets`)

Date: 2026-07-03
Scope: ~92 scored chocolate_tablet products, `/hashvaot/chocolate-tablets`
Challenger: adversarial-qa-agent (Bari)
Task: TASK-474 (P1 item 9a / launch finding F2)
Ground truth ref: `origin/master` @ `e615244a29f32a26537f4113f3441c3b267a4400` (fetched fresh this run) —
all file reads below via `git show origin/master:<path>` unless stated otherwise.
Status: **COMPLETE.**

**Category-identity note (read first):** there are TWO chocolate categories sharing one corpus root
(`02_products/chocolate/`) and one BSIP0/BSIP1/BSIP2 run. This report covers **chocolate-tablets only**
(route `/hashvaot/chocolate-tablets`). The chocolate-bars report
(`02_products/chocolate/reports/red_team_chocolate_bars_page_v1.md`) is complete and NOT repeated here.
A prior tablets-scoped file may exist at `red_team_tablets_2026-07-03.md` (per the bars report's own
note) — if found, it is treated as a DIFFERENT, narrower QA (copy-overhaul), not a substitute for this
launch-gate report.

---

## Provenance note

Route: `bari-web/src/app/hashvaot/chocolate-tablets/page.tsx` → imports from
`@/lib/comparisons/chocolate-tablets-comparison-page-data.ts`, which wraps
`bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json` (35 products, confirmed by reading
the route + loader source directly — not taking a builder's word for it). Shelf filters:
`bari-web/src/lib/comparisons/chocolate-tablets-shelf-filters.ts`.

Live JSON `_meta`:
- `run_id = task409_rederive_chocolate_tablets_20260626`
- `corpus_dirs = C:\Bari\03_operations\bsip1\fresh_rescore_task391_20260624_113405\output`
- `engine_sha = 5f2e611db7417d1e31e9ae548afde041d5a148a9`
- `corpus_records = 33`, `scored = 33`, **`product_count = 35`** — internally inconsistent, see F-V3.
- `reflow` block: TASK-455 "chocolate correctness (classifier fix + endemic carve-out)",
  `BARI_REDLABEL_CONTINUOUS_V1=on`, date 2026-07-02, `grade_movers` = 7 barcodes (2× C→B, 2× D→C,
  3× E→D), `grade_flip_count = 7`, note "chocolate re-classified from snack_bar_granola to chocolate
  (router_v2 Rule 4) + EV-REDLABEL-013 endemic sat-fat carve-out; all moves upward"
- `deanchor_meta_regenerated = 2026-07-02`
- Live grade distribution (independently computed): `{B: 2, C: 6, D: 10, E: 17}`, N=35. Score range
  12.8–65.8.
- No `off_used` key present (same gap class as bars).

Committed BSIP2 trace directory: `02_products/chocolate/bsip2_outputs/fresh_rescore_task391_20260624_113405/products/` —
generated 2026-06-24, i.e. **before** the TASK-455 re-flow (2026-07-02). Same F-V1 traceability-gap
pattern as bread/cakes/chocolate-bars — verified below.

Config file `03_operations/page_generator/configs/chocolate_tablets.json` is **stale relative to the
live JSON**: its `scoring.flags.BARI_REDLABEL_V1 = "off"` while the live JSON's `reflow` block shows
`BARI_REDLABEL_CONTINUOUS_V1=on` (a different, newer flag name/state applied after this config was last
written, 2026-06-26, six days before the 2026-07-02 reflow). The config was not regenerated post-TASK-455.

---

## Opening Finding

No data-absent scoring found: all 35 products carry populated core nutrition and `confidence: "verified"`
uniformly (11/35 null `dietary_fiber_g` is a standard Israeli-label absence pattern, not a data gap
driving a score — consistent with bars). Hard Rule 12 does not fire as CRITICAL here.

The opening structural problem is the **same F-V1 traceability-gap pattern found on bread/cakes/
chocolate-bars**: no committed BSIP2 trace file reproduces the current live tablets score for any
sampled product — the only committed trace directory was generated 2026-06-24 under
`category: "snack_bar_granola"`, before TASK-455 (2026-07-02) fixed the classifier and applied the
endemic sat-fat carve-out. 8/8 sampled products show live score strictly above trace, and 2/8 grade-cross
(matching the `grade_movers` list exactly). This is the identical pattern and identical root cause as the
bars report — same commit, same explanation quality. See F-V1 (HIGH, not CRITICAL).

A second, independently significant structural finding, **specific to tablets and not present on bars**:
the live JSON's own `_meta` block is internally inconsistent about how many products this run scored.
`_meta.corpus_records = 33` and `_meta.scored = 33`, but the `products` array holds **35** and
`_meta.product_count = 35` correctly reflects that. The `33` figure is a carry-over from an earlier
TASK-409 rederive step (`_task409_rederive_v2_result.json`: `chocolate_tablets → corpus_records: 33,
scored: 33`) that predates 2 products being added into the live set by another mechanism. Worse, the
category's own config file (`chocolate_tablets.json`) claims "Live page displays 35/92 tablets — the 57
non-displayed are ... all E-grade products curated out by editorial curation" — a claim this report
**checked and found false**: 3 of the 59 actually-non-displayed products (not 57 — the config's own
arithmetic is off too) carry grade **C** in the shared run's manifest, not E, at exactly the C/D boundary
score of 50. See F-V3 (CRITICAL — a documented, machine-readable data-provenance claim that a downstream
reviewer would reasonably trust is factually wrong on inspection, and the actual product_count math in
`_meta` does not internally reconcile).

A third finding: the tablets shelf-filter chips offer only grade-C/D/E — **no grade-B option exists**,
despite TASK-455 having just created 2 live B-grade products (the page's #1 and #2 ranked products,
per the prior copy-overhaul report's "co-leaders" framing). A consumer cannot filter to see the two
highest-ranked, most-prominently-discussed products on the page. See F-C1 (HIGH).

---

## Track V — Verification

### V1. Score/trace fidelity (G5) — 8 products sampled across grades

Sampled across the full live score range (top, bottom, 6 spread points), covering all 4 live grades
(B/C/D/E). Trace = `02_products/chocolate/bsip2_outputs/fresh_rescore_task391_20260624_113405/products/bsip1_{barcode}/bsip2_trace.json`
(only committed trace directory; generated 2026-06-24, pre-TASK-455).

| # | Barcode | Live score | Live grade | Trace `final_score_estimate` | Trace `grade_estimate` | Delta (live-trace) | Grade-cross? | Trace `category` (debug) |
|---|---|---|---|---|---|---|---|---|
| 1 | 7290112197467 | 65.8 | B | 55.0 | C | +10.8 | **yes, C→B** | snack_bar_granola |
| 2 | 4000539280740 | 53.7 | C | 50.0 | C | +3.7 | no | snack_bar_granola |
| 3 | 7290018893609 | 47.5 | D | 44.7 | D | +2.8 | no | snack_bar_granola |
| 4 | 7296073747802 | 41.3 | D | 32.0 | E | +9.3 | **yes, E→D** | snack_bar_granola |
| 5 | 3046920023047 | 33.9 | E | 29.9 | E | +4.0 | no | snack_bar_granola |
| 6 | 3046920028752 | 28.7 | E | 23.0 | E | +5.7 | no | snack_bar_granola |
| 7 | 7290110579463 | 20.6 | E | 16.6 | E | +4.0 | no | snack_bar_granola |
| 8 | 7290112348548 | 12.8 | E | 12.2 | E | +0.6 | no | snack_bar_granola |

**Summary: 2/8 grade-crosses (7290112197467 C→B, 7296073747802 E→D), both of which appear verbatim in
the live JSON's own `reflow.grade_movers` list** — internally consistent with the commit's own claim.
**8/8 sampled products show a positive delta (+0.6 to +10.8), all live-above-trace**, matching "all moves
upward." Every trace's `category` field reads `snack_bar_granola` — direct confirmation the committed
trace predates the TASK-455 router fix. No committed BSIP2 trace file on disk reproduces a
post-TASK-455 tablets score for any product — the same F-V1 pattern as bread/cakes/chocolate-bars, with
the same single-commit explanation quality as bars (cleaner than cakes, which needed two chained
commits). See F-V1 (HIGH).

Live `grade` was independently re-derived from `frontendGradeFromScore()` (`bari-web/src/lib/comparisons/corpus.ts`
lines 51-57: A≥80, B≥65, C≥50, D≥35, else E) for all 8 sampled products — matches stored `grade` in
8/8 cases.

### V2. Ingredient-handoff (TASK-475/476 bug class) — 5 products sampled

Source: `03_operations/bsip1/fresh_rescore_task391_20260624_113405/output/bsip1_{barcode}.json`
`ingredient_order` length vs BSIP2 trace `ingredient_count` (deep-searched in trace JSON).

| # | Barcode | BSIP1 `ingredient_order` len | BSIP1 `ingredients_text_he` len | BSIP2 `ingredient_count` | Verdict |
|---|---|---|---|---|---|
| 1 | 7290112197467 | 11 | 242 chars | 11 | Clean (exact match) |
| 2 | 4000539280740 | 7 | 140 chars | 7 | Clean (exact match) |
| 3 | 7290018893609 | 8 | 144 chars | 8 | Clean (exact match) |
| 4 | 3046920023047 | 12 | 157 chars | 12 | Clean (exact match) |
| 5 | 7290110579463 | 10 | 121 chars | 10 | Clean (exact match) |

**5/5 clean of the REAL_LOSS-57 handoff-zero bug class, and 5/5 exact-match (no divergence at all)** —
cleaner result than chocolate-bars, which had 3/5 sampled products showing a counting-methodology
divergence between the two fields. No finding here.

### V3. Data integrity

- **Product count vs `_meta`:** `_meta.product_count = 35`; actual `products` array length = 35.
  **MATCH.** However `_meta.corpus_records = 33` and `_meta.scored = 33` **do not match** either the
  displayed count (35) or the shared run's full tablet manifest count (92). Traced to origin: the
  staging file `_task409_staging/chocolate_tablets_frontend_staged.json` already carries the same
  33/33 alongside a 35-length products array — meaning the discrepancy was baked in when the staging
  file was assembled (35 products placed in the array, but `corpus_records`/`scored` fields never
  recalculated from the older TASK-409 rederive step, which itself operated on only 33 tablets per
  `_task409_rederive_v2_result.json`: `chocolate_tablets → corpus_records: 33, scored: 33`). **FAIL** —
  `_meta`'s own count fields do not describe what's actually being served. See F-V3 (CRITICAL).
- **Dropped/excluded documented (G3) — claim checked and found FALSE:** config's `_comment` states "Live
  page displays 35/92 tablets — the 57 non-displayed are CORPUS_NOT_DISPLAYED in the diff (all E-grade
  products curated out by editorial curation)." Independently computed against the shared run's manifest
  (`02_products/chocolate/fresh_rescore_task391_20260624_113405_manifest.json`, `chocolate_tablet` array,
  len=92): manifest barcodes minus live-displayed barcodes = **59** products, not 57 as the config states,
  and their manifest-recorded grade distribution is **{C: 3, E: 56}**, not "all E-grade" as claimed. The
  3 non-displayed C-grade products (3046920023429, 3046920023368, 3046920023443 — all correctly
  classified `category: chocolate_tablet`) each score exactly 50 (the C/D boundary) in the manifest.
  Because these are pre-TASK-455 manifest grades and TASK-455's moves are all upward, these products
  cannot have been E-grade pre-reflow and become "curated as E" post-hoc — the claim is checkably false
  in the direction that matters (they were never E). Additionally, 2 live-displayed barcodes
  (7296073726562, 7290119500482) are **not present at all** in this manifest's `chocolate_tablet` list —
  though both do have committed BSIP2 traces in the same run directory, so they are not fabricated, just
  outside the manifest's own bookkeeping. **FAIL** — the documented exclusion reason is factually
  incorrect on inspection, not merely vague (which was the bars-report finding; this is a stronger
  defect). See F-V3 (CRITICAL, folded into the same finding as the count mismatch above — both stem from
  the same underlying `_meta`/manifest bookkeeping failure).
- **Rank monotonicity:** `rank` field equals array index+1 for all 35 (0 mismatches, verified
  programmatically); `score` values strictly non-increasing down the array (0 inversions). **PASS.**
- **Duplicate IDs / barcodes:** 0 duplicate `id` values, 0 duplicate `barcode` values across 35 products.
  **PASS.**
- **`categoryTotal` consistency:** single distinct value `35` across all 35 products, matches array
  length and `_meta.product_count`. **PASS.**
- **Proportionality (full-list scan):** largest adjacent gap 9.8 (B→C boundary, disclosed in
  `categoryNote` as a genuine category-cluster finding — "only two tablets reach B, then a ten-point gap"
  — verified TRUE, see C5), second-largest 6.0 (between two D-grade products, 7296073747802→4000417025005)
  and 4.1 (between two E-grade products) — neither of the smaller two gaps is explicitly named as a gap
  in any copy, though both stay within-grade. Not escalated to a finding on its own (Hard Rule 11 is most
  concerned with unexplained *cross-grade* gaps; the one cross-grade gap of size is the disclosed B→C
  gap), but noted for awareness.

### V4. OFF ban (hard gate)

- Grepped the live frontend JSON (`chocolate_tablets_frontend_v1.json`) and all 8 sampled BSIP2 trace
  files plus all 5 sampled BSIP1 files for `openfoodfacts` / "open food facts" / `off_source`: **0
  matches.**
- No `_meta.off_used` key present (same documentation-gap class as bars — not a launch blocker since no
  actual dependency was found, but a consistency gap). See F-V4 (MEDIUM).
- **Verdict: PASS** (no OFF dependency found) in sampled scope — not exhaustive across all 35 products'
  full traces.

### V2. Ingredient-handoff (TASK-475/476 bug class) — 5 products sampled

TBD

### V3. Data integrity

TBD

### V4. OFF ban (hard gate)

TBD

---

## Track C — Challenge

### C5. Consumer strings defensibility (filter-chip/caveat counts vs actual corpus; name-only filter check)

**Category identity/count claims in prologue and categoryNote — checked against the live 35-product
corpus, all TRUE:**
- `chocolateTabletsMetadataLine` is built as a template literal off `chocolateTabletsProducts.length`
  (`bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts` line 38) — **not hardcoded.**
  Architecturally immune to the stale-count bug class (cakes CRITICAL), same as bars.
- CategoryNote paragraph 1: "רק שתי טבלאות במדף הזה מגיעות ל-B, ואחריהן פער של עשר נקודות עד הבאה בתור"
  ("only two tablets on this shelf reach B, then a ten-point gap to the next") — actual: **2 B-grade
  products (65.8, 65.1), next is 55.3 (a 9.8-point gap)**. **TRUE** (9.8 rounds to "ten" in prose, not a
  fabrication).
- CategoryNote paragraph 4 (white chocolate): "אין בו מוצקי קקאו כלל" (no cocoa solids at all) — a
  category-level factual claim about white chocolate's definition, not corpus-specific; accepted as
  food-science fact per the bars/copy-overhaul precedent, not independently falsifiable against this
  dataset's fields.

**Filter-chip architecture: grade-only (C/D/E), no name-only keyword filter exists on this page** — the
specific bars-report bug class (a keyword filter matching product NAME only, under-selecting products
whose ingredients/copy actually discuss the trait) **does not reproduce here** because tablets has no
such filter at all; `chocolate-tablets-shelf-filters.ts` implements exactly 3 grade-equality checks
(`product.grade === "C"` / `"D"` / `"E"`), nothing name- or keyword-based. **This specific defect class is
absent — confirmed by reading the filter source directly, not inferred.**

**However, a different, analogous defect found in the filter *set's coverage* of the live grade
distribution:** the 3 available chips (grade-C, grade-D, grade-E) do not include a grade-B option, yet
the live corpus has 2 B-grade products — precisely the 2 highest-ranked products on the entire page
(rank #1 7290112197467 score 65.8, rank #2 7296073382416 score 65.1), which the page's own row copy
describes as "co-leaders" ("אחת משתי הטבלות שחולקות את ראש הדירוג"). A consumer using the filter UI to
narrow the shelf has no way to isolate or view only the top-ranked products via any chip — the filter
option set was not updated when TASK-455's reflow created a B grade on this page for the first time
(the shelf-filters.ts file's own code comment says "Grade-based (C/D/E spread exists on this corpus)" —
accurate before TASK-455, stale now). This is a real, reproducible navigation-completeness gap: both B
products still render normally in the main list, but they are unreachable via any filter chip, on the
exact page where a consumer would most plausibly want to filter to "the best ones." See F-C1 (HIGH).

**insightLine / rowVerdict spot-check (8 V1-sampled products plus the C6 superlative sample):** all
checked strings trace to real nutrition/ingredient fields — no fabricated numbers found in this sample.
One recurring template phrase noted: "X, לא טבלת קקאו" ("X, not a cocoa tablet") appears in
`expansion.comparisonContext` for at least 8 different products as a near-verbatim closing formula — see
C7 for the phrasing-rule implications and F-C3 for the template-repetition angle.

### C6. Superlatives rank-checked vs the full 35-product corpus

| Barcode | Claim | Scope | Verified rank | Verdict |
|---|---|---|---|---|
| 3046920029759 (Lindt 90%) | "the fattest tablet on the shelf" (55g fat) | all 35 | #1 of 35 (55.0 vs #2 53.0) | **Verified correct** |
| 7290119500437 | "lowest sugar on the whole shelf" (0.2g/100g) | all 35 | #1 lowest of 35 (0.2 vs #2 0.3 — real, if narrow, gap) | **Verified correct** |
| 7622202265648 (white chocolate) | "sweetest tablet on the shelf" (65g sugar) | all 35 | #1 of 35 (65.0 vs #2 60.0 — real gap) | **Verified correct** |
| 7290112914699 | "sodium record, and by a huge margin" (357mg) | all 35 | #1 of 35 (357.0 vs #2 215.0 — gap of 142mg, genuinely large) | **Verified correct** |
| 3046920028363 (Lindt 85%) | "richest protein on the shelf" (12.5g) AND "only one sweetened with demerara sugar" | all 35 | protein #1 of 35 (12.5 vs #2 11.0); demerara mention count = 1/35 (unique) | **Both verified correct** |
| 7290112197467 / 7296073382416 | "co-leaders, sharing the top of the ranking" | all 35 | #1 (65.8) and #2 (65.1) — gap 0.7, next product (#3) is 9.8 away | **Verified correct — genuine tie, no 3rd product within reach** |

**6/6 rank-checked superlative claims hold up exactly against the real 35-product corpus.** No fabricated
or unverifiable "highest/lowest/only" claim found in this sample — consistent with the prior copy-overhaul
report's own independent rank-table appendix (which checked additional hotspots not re-verified here to
avoid duplicating that report's work; this report independently re-derived these 6 from the current live
JSON rather than relying on that report's numbers).

### C7. Phrasing (antithesis, em-dash) — JSON vs page-data.ts split

Swept `insightLine`, `rowVerdict`, `expansion.comparisonContext`, `expansion.positiveSignals[]`,
`expansion.limitingFactors[]`, `d4_additives[].function_he` for all 35 products, plus page-level
`hero.title`, all 3 `prologueSentences`, all 4 `categoryNote` paragraphs, both `methodologyLines`
(4 lines total), and the SEO `metaDescription`, in `chocolate-tablets-comparison-page-data.ts`.

**Antithesis ("X, not Y" / "X — not Y" / "X; not Y" pattern, regex `[,—;]\s*ו?לא\s`, plus literal
`אלא`):**
- **JSON (product-level): 12 hits, all in `expansion.comparisonContext` or `positiveSignals`** —
  7290112197467, 7296073382416, 5941021001674, 3046920028363, 4000417025005, 3046920023047,
  3046920029674, 7610008641001, 7290112331984, 7290110579463, 7622202257506, 7290112348548. Several use
  the exact repeating template close "X, **לא** טבלת קקאו" ("X, not a cocoa tablet") — a stamped phrase
  in addition to being a banned construction (see F-C3 for the repetition angle).
- **`chocolate-tablets-comparison-page-data.ts` (page-level): 3 hits** — `chocolateTabletsMethodologyLines[2]`
  (line 62): *"הציון נשען על אחוז הקקאו, כמות הסוכר, סוג השומן ורמת העיבוד — **לא** על כמות השוקולד
  בלבד"* ("the score rests on cocoa%, sugar, fat type, and processing — not just chocolate quantity");
  the SEO `metaDescription` (line 69): *"...מידע, **לא** המלצה"* ("information, not a recommendation" —
  the identical construction found on the bars page's SEO description, word for word); and
  `chocolateTabletsCategoryNote[0]` (line 53): *"ה-B הוא הצד הנכון של מדף הממתקים; **לא** מוצר בריאות"*
  ("B is the right side of the candy shelf; not a health product" — a semicolon-separated instance of
  the same rhetorical pattern).
- `אלא` (the reinforced "not X but rather Y" form): **0 hits** anywhere (JSON or page-data.ts) — cleaner
  than bars, which had 1.
- The hero title (line 43, "שוקולד מריר **לא** הופך לבריא בגלל השם — הציון מפריד...") uses a bare "לא"
  without a preceding comma/dash/semicolon separator — a direct negation clause ("dark chocolate does not
  become healthy because of the name"), not the "X [separator] not Y" antithesis form the owner ruling
  targets. Judged a **different, milder construction**, not counted in the antithesis tally, but flagged
  for awareness since it is the single most prominent string on the page and leads with a negation.
- **Total antithesis-pattern hits: 12 JSON + 3 page-data.ts = 15.** See F-C2 (HIGH — same standing owner
  ruling as bars; here the SEO metaDescription repeats the identical violating phrase found on the bars
  page verbatim, suggesting a shared, un-swept template string rather than two independent authoring
  choices).

**Em-dash ("—") count:**
- **47 in JSON product-level fields**: 19 in `expansion.comparisonContext`, 22 across
  `positiveSignals[0-2]`, 6 in `d4_additives[].function_he` (the pre-flagged systemic RT-480-3 class,
  noted but not counted as new-to-this-page per the task's framing).
- **9 total in page-data.ts, 8 consumer-facing** (excluding 1 in a code comment, line 25): hero title
  (line 43), 2 in prologue sentence 3 (line 49), 1 each in categoryNote paragraphs 2 and 4 (lines 54,
  56), methodology lines 1 and 3 (lines 60, 62), and the SEO metaDescription (line 69).
- **Total new-to-this-page em-dashes: 41 JSON (47 minus the 6 d4_additives) + 8 page-level = 49.** Higher
  volume than bars (40), concentrated in the same "number — context" template pattern. See F-C3
  (MEDIUM — volume, not a hard ban, same framing as bars).

**Grade-letter-as-crutch** (regex for "ציון [A-E]" / "דירוג [A-E]" inside insightLine/rowVerdict/
comparisonContext): **0 hits** in product-level copy (JSON). **2 hits at the categoryNote level** — "רק
שתי טבלאות במדף הזה מגיעות ל-B" (paragraph 1) and "יכולה להגיע גם ל-B... יורדת ל-D ואף ל-E" (paragraph
2) — both disclose genuine structural findings (the B-cluster size, the sugar-substitute grade-swing
mechanism) rather than substituting a letter for an explanation; judged **Clean/non-violating**, same
disposition as the single bars-page hit, but flagged for awareness (2 mentions here vs 1 on bars).

### C8. Confidence honesty / proportionality

- All 35/35 products carry `confidence: "verified"`, with a single distinct `confidence_tooltip_he` text:
  "הציון מבוסס על פאנל התזונה ורשימת הרכיבים שפורסמו למוצר" ("the score is based on the nutrition panel
  and ingredient list published for the product") — modest, accurate phrasing that does not claim "all
  data" or "complete data." Despite 11/35 (31%) products having null `dietary_fiber_g`, the tooltip never
  overclaims completeness. **No confidence-honesty violation found — same clean disposition as bars.**
  Listed in Clean below.
- No INSUFFICIENT-confidence products found in the live 35 — nothing to check for correct-discard.
- Proportionality: see V3 above (full 35-product adjacent-gap scan) — largest gap (9.8, B→C) is
  explicitly disclosed in categoryNote and verified true; no *unexplained* cross-grade gap found. Two
  smaller within-grade gaps (6.0, 4.1) are not individually named in copy but do not cross a grade
  boundary. **Clean**, with a minor observation (not a new finding) that within-grade gaps aren't
  individually narrated — consistent with how a 35-product shelf is normally presented.

---

## Product-by-Product Assessment (sampled products only — not full 35)

| Barcode | Product | Score | Grade | RT Assessment | Confidence | Critical Notes |
|---|---|---|---|---|---|---|
| 7290112197467 | שוקולד מריר | 65.8 | B | Justified — score movement fully explained by TASK-455 (trace 55.0/C, snack_bar_granola misclassification), C→B grade-cross matches `grade_movers` list; "co-leader" claim verified TRUE | verified | Unreachable via any filter chip (F-C1); comparisonContext carries antithesis (F-C2) |
| 7296073382416 | שוקולד מריר 90% | 65.1 | B | Justified — "co-leader" claim verified TRUE (gap to #1 only 0.7, gap to #3 is 9.8) | verified | Unreachable via any filter chip (F-C1); positiveSignals[2] carries antithesis (F-C2) |
| 4000539280740 | שוקולד מריר 78% | 53.7 | C | Justified — trace-explained (delta +3.7, no grade-cross) | verified | none |
| 7290018893609 | שוקולד מריר 85% | 47.5 | D | Justified — trace-explained (delta +2.8); ingredient-handoff clean (8=8) | verified | none |
| 7296073747802 | שוקולד מריר פרימיום 75% | 41.3 | D | Justified — trace-explained, E→D grade-cross matches `grade_movers` list exactly (delta +9.3) | verified | none |
| 3046920023047 | אקסלנס פיסטוק | 33.9 | E | Justified — trace-explained (delta +4.0); ingredient-handoff clean (12=12) | verified | comparisonContext carries antithesis (F-C2) |
| 3046920028363 | שוקולד מריר 85% (Lindt) | 44.8 | D | Justified — both superlative claims (highest protein 12.5g, unique demerara) verified TRUE against full 35-product corpus | verified | comparisonContext carries antithesis (F-C2) |
| 3046920029759 | שוקולד מריר 90% (Lindt) | 53.0 | C | Justified — "fattest tablet" superlative verified #1/35 (55.0g) | verified | none checked in phrasing sample |
| 3046920028752 | שוקולד מריר מנטה | 28.7 | E | Justified — trace-explained (delta +5.7); ingredient-handoff not sampled here | verified | none |
| 7290110579463 | חלב שברי אגוז | 20.6 | E | Justified — trace-explained (delta +4.0); ingredient-handoff clean (10=10) | verified | comparisonContext carries antithesis (F-C2) |
| 7622202265648 | שוקולד לבן (Milka) | 16.3 | E | Justified — "sweetest tablet" superlative verified #1/35 (65.0g, real gap to #2 at 60.0) | verified | none checked in phrasing sample |
| 7290112914699 | שוקולד חלב וקרמל מלוח | 15.1 | E | Justified — "sodium record, huge margin" superlative verified #1/35 (357mg vs #2 215mg, 142mg gap) | verified | none checked in phrasing sample |
| 7290112348548 | לבן | 12.8 | E | Justified — trace-explained (delta +0.6, smallest in sample) | verified | comparisonContext carries antithesis (F-C2) |
| 7290119500437 | שוקולד מריר | 54.1 | C | Justified — "lowest sugar on whole shelf" superlative verified #1/35 (0.2g) | verified | none checked in phrasing sample |

---

## Clean (verified) list

- **Metadata line architecture:** `chocolateTabletsMetadataLine` computed live off `.length` (not
  hardcoded) — structurally immune to the cakes stale-count bug class.
- **Filter-chip name-only-keyword defect class (bars F-C1 bug):** confirmed ABSENT — tablets filters are
  grade-equality only, no keyword/name matching logic exists to under-select.
- **Rank/order/dedup (V3):** rank field = index+1 for all 35 (0 mismatches); scores strictly
  non-increasing (0 inversions); 0 duplicate ids/barcodes; `categoryTotal` uniformly 35.
- **Product count vs `_meta.product_count`:** exact match (35 = 35) — though see F-V3 for the
  `corpus_records`/`scored` sub-fields, which do NOT match.
- **Grade re-derivation:** independently recomputed `frontendGradeFromScore()` matches stored `grade` on
  all 8 V1-sampled products.
- **Ingredient-handoff (V2):** 5/5 sampled products show exact match between BSIP1 `ingredient_order`
  length and BSIP2 `ingredient_count` — cleaner than bars (which had a 3/5 divergence pattern); no
  REAL_LOSS-57-class handoff-zero bug found.
- **Superlatives (C6):** 6/6 rank-checked "highest/lowest/only/co-leader" claims verified TRUE against
  the real 35-product corpus. No fabricated or unverifiable superlative found.
- **OFF ban (V4):** 0 OFF references in the live JSON or 13 sampled trace/BSIP1 files.
- **Confidence tooltip honesty (C8):** phrasing is modest and accurate ("score based on published
  panel") — does not overclaim "all data" despite 31% null fiber.
- **B-grade cluster claim (C5):** "only two tablets reach B, then a ten-point gap" verified TRUE (9.8pt
  actual gap).
- **`אלא` antithesis (reinforced form):** 0 hits anywhere — cleaner than bars (1 hit).
- **Grade-letter-as-crutch (C7):** 0 hits in product-level copy; the 2 categoryNote-level mentions are
  contextually genuine structural disclosures, not explanatory shortcuts.

---

## Clean (verified) list

TBD

---

## Findings by Severity

### CRITICAL — must resolve before launch

**F-V3: The live JSON's own `_meta` count fields are internally inconsistent, AND the config's
documented exclusion reason for the 59 non-displayed tablets is checkably false.**
- Evidence (count inconsistency): `_meta.corpus_records = 33` and `_meta.scored = 33` in
  `chocolate_tablets_frontend_v1.json`, while the `products` array holds 35 and `_meta.product_count =
  35` is correct. Traced to `_task409_staging/chocolate_tablets_frontend_staged.json`, which already
  carries the same 33/33 alongside a 35-length array — the count fields were never recalculated after
  2 products were added on top of the TASK-409 rederive step's 33-product output
  (`_task409_rederive_v2_result.json`: `chocolate_tablets → corpus_records: 33, scored: 33`).
- Evidence (false exclusion reason): `03_operations/page_generator/configs/chocolate_tablets.json`
  `_comment` states "Live page displays 35/92 tablets — the 57 non-displayed are CORPUS_NOT_DISPLAYED...
  all E-grade products curated out by editorial curation." Independently computed against
  `02_products/chocolate/fresh_rescore_task391_20260624_113405_manifest.json`'s `chocolate_tablet` array
  (92 entries, each carrying its own `grade` field): manifest-minus-live = **59** products (not 57), with
  grade distribution **{C: 3, E: 56}** (not "all E"). The 3 non-displayed C-grade products
  (3046920023429, 3046920023368, 3046920023443) are correctly classified `chocolate_tablet` and each
  score exactly 50 (the C/D boundary) — pre-TASK-455 manifest grades, and TASK-455's moves are all
  upward, so these products cannot have been E-grade and later "curated as E." Separately, 2
  live-displayed barcodes (7296073726562, 7290119500482) do not appear in this manifest's tablet list at
  all (though both have legitimate committed BSIP2 traces in the same run directory — not fabricated,
  just outside this manifest's bookkeeping).
- Implication: this is not a vague-documentation gap (the bars-report finding) — it is a specific,
  checkable factual claim in a governance artifact that turns out to be wrong in the direction that
  matters (real C-grade products silently excluded under a false "all-E" justification), plus a `_meta`
  block whose own scored-count fields do not describe what is actually being served. An outside reviewer
  or auditor who trusts the config's stated reason, or trusts `_meta.scored` as the denominator for this
  category, is being told something false. This directly implicates whether the displayed 35 is a fair,
  documented sample of the scored 92, or a set of unknown, undocumented selection criteria — which is
  exactly the kind of category-identity question a competitor or journalist would ask first.
- Repro: `git show origin/master:02_products/chocolate/fresh_rescore_task391_20260624_113405_manifest.json`
  → `chocolate_tablet` array, filter by barcode not in live JSON's `products[].barcode` set, group by
  `grade`. `git show origin/master:_task409_rederive_v2_result.json` → `results.chocolate_tablets`.
- Routes to: `data-agent` (recompute `_meta.corpus_records`/`_meta.scored` to match reality; correct or
  retract the "all E-grade" claim in the config comment; if the true selection rule is something else
  — e.g. one-card-per-SKU dedup, as bars had — state it explicitly and verify it against all 59, not
  just infer it).

### HIGH — should resolve before launch

**F-C1: The live grade distribution includes 2 B-grade products (the page's #1 and #2 ranked
"co-leaders") that are unreachable via any shelf-filter chip, because the filter set was not updated
when TASK-455 created a B grade on this page for the first time.**
- Evidence: `bari-web/src/lib/comparisons/chocolate-tablets-shelf-filters.ts` offers exactly 3 chips —
  `grade-C`, `grade-D`, `grade-E` — with a code comment stating "Grade-based (C/D/E spread exists on
  this corpus)." The live JSON's grade distribution (independently computed) is `{B: 2, C: 6, D: 10, E:
  17}` — a B/C/D/E spread, not C/D/E. The 2 B-grade products (7290112197467, 7296073382416) are ranked
  #1 and #2 of 35 and are described in their own row copy as sharing "the top of the ranking."
- Implication: a consumer who wants to filter to the best-scoring tablets has no chip that surfaces
  either of the two top-ranked products — the filter UI's own option set silently excludes the page's
  best-scoring content. This is a functional navigation defect introduced by the TASK-455 reflow (the
  filter file was not touched when the reflow created new grade values), analogous in kind (though not
  identical in mechanism) to the bars report's F-C1 keyword-filter gap.
- Repro: `bari-web/src/lib/comparisons/chocolate-tablets-shelf-filters.ts`
  `CHOCOLATE_TABLETS_SHELF_LENS_OPTIONS` (3 entries, no `grade-B`) vs live JSON grade distribution
  (`{B: 2, C: 6, D: 10, E: 17}`, computed from `chocolate_tablets_frontend_v1.json`).
- Routes to: `frontend-agent` (add a `grade-B` chip, or make the filter option set derive from the
  actual live grade distribution rather than being hand-authored per category).

**F-V1: No committed BSIP2 trace file on disk reproduces the current live score for any sampled
chocolate-tablets product — but the gap is fully explained by one named, two-gate-signed commit.**
- Evidence: the only committed trace directory (`fresh_rescore_task391_20260624_113405`, generated
  2026-06-24) scores every sampled product under `category: "snack_bar_granola"`. TASK-455 (`f026f2dd`,
  2026-07-02) fixed the router to classify chocolate as `category: "chocolate"` with its own calorie
  regime + endemic sat-fat carve-out. 8/8 sampled products show live score strictly above trace
  `final_score_estimate` (deltas +0.6 to +10.8); 2/8 grade-cross (C→B, E→D), both appearing verbatim in
  the live JSON's own `reflow.grade_movers` list.
- Implication: an outside reviewer cannot point at one committed file and get today's exact
  chocolate-tablets score for any product — reproduction requires knowing to apply the TASK-455 delta on
  top of the stale trace. Same process gap as bread/cakes/chocolate-bars; not evidence of a wrong score
  (the movement is fully named and internally self-consistent with the commit's own claims).
- Repro: `git show origin/master:02_products/chocolate/bsip2_outputs/fresh_rescore_task391_20260624_113405/products/bsip1_7290112197467/bsip2_trace.json`
  → `final_score_estimate=55.0`, `grade_estimate="C"`, `category="snack_bar_granola"` vs live
  `score=65.8`, `grade="B"`, delta +10.8.
- Routes to: `data-agent` (regenerate and commit a current BSIP2 trace snapshot for chocolate tablets
  reflecting TASK-455, matching the same recommendation already routed for chocolate-bars).

**F-C2: 15 total "X, not Y"-pattern antithesis violations (12 in product-level JSON, 3 in page-level
`chocolate-tablets-comparison-page-data.ts`), including one that repeats an existing bars-page violation
verbatim.**
- Evidence: JSON hits in `expansion.comparisonContext`/`positiveSignals` for 12 barcodes (listed in C7
  above), several using a repeating template close "X, לא טבלת קקאו." Page-level: `methodologyLines[2]`
  (line 62, "...לא על כמות השוקולד בלבד"), SEO `metaDescription` (line 69, "...מידע, לא המלצה" — **word-
  for-word identical** to the phrase already flagged as a HIGH finding on the chocolate-bars page's SEO
  description), and `categoryNote[0]` (line 53, semicolon form, "...לא מוצר בריאות").
- Implication: the standing owner ruling bans this construction project-wide with no stated hero/SEO
  exception. The SEO metaDescription repeating the exact same violating phrase as bars strongly suggests
  a shared, un-swept template fragment used across both chocolate pages (and potentially others) rather
  than two independently-authored instances — worth checking whether other categories share the same
  boilerplate SEO line.
- Repro: `git show origin/master:bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts`
  lines 53, 62, 69; regex `[,—;]\s*ו?לא\s` over all 35 products' `expansion.comparisonContext` and
  `positiveSignals[]`.
- Routes to: `content-agent`.

### MEDIUM — should document or monitor

**F-C3: 49 em-dash occurrences across product/page-level copy (41 product-level, 8 page-level), plus 6
more in the pre-flagged systemic `d4_additives.function_he` class (not counted as new); a repeating
"X, לא טבלת קקאו" template phrase found in at least 8 of the 12 antithesis hits.**
- Evidence: see C7 above for the full em-dash breakdown by field. The "not a cocoa tablet" template close
  appears in `expansion.comparisonContext` for 8 different products (4000417025005, 3046920023047,
  3046920029674, 7610008641001, 7290112331984, 7290110579463, 7622202257506, 7290112348548) — nearly
  verbatim each time, which is both an antithesis violation (already counted in F-C2) and a stamped-
  phrase repetition concern in its own right (the prior tablets copy-QA's own hygiene gate explicitly
  checks for >2× phrase repeats).
- Implication: within "minimize, don't ban" guidance this is not a hard violation on em-dash volume
  alone, but the repeated template phrase is a distinct hygiene concern the prior copy-overhaul report's
  own 5-gram/4-gram repeat-check would likely have flagged had it covered `comparisonContext` (that
  report explicitly noted `expansion` was untouched by its own candidate and out of scope — see M3 in the
  prior report — so this repetition was never actually checked by that gate).
- Routes to: `content-agent`.

**F-V4: No machine-checkable `_meta.off_used` flag on the chocolate-tablets live JSON (same gap as
bars).**
- Evidence: `chocolate_tablets_frontend_v1.json` `_meta` keys checked — no `off_used` or equivalent
  field. No actual OFF dependency was found in this report's sampled scope (0/8 traces, 0/5 BSIP1 files,
  0 in live JSON).
- Implication: not a launch blocker, but a documentation-consistency gap shared with chocolate-bars — a
  future automated OFF-ban gate check against `_meta` fields would silently skip both chocolate
  categories.
- Routes to: `data-agent` (add `_meta.off_used = false` to the served JSON for parity).

**F-V5: Config file (`chocolate_tablets.json`) is stale relative to the live JSON's actual scoring flags.**
- Evidence: config's `scoring.flags.BARI_REDLABEL_V1 = "off"` (last written 2026-06-26); live JSON's
  `_meta.reflow.flag = "BARI_REDLABEL_CONTINUOUS_V1=on"` (applied 2026-07-02) — a different flag name and
  state, applied after the config was last regenerated.
- Implication: the config is not a reliable record of what scoring configuration actually produced the
  live page; anyone consulting it for an audit would get a wrong answer about which red-label flag regime
  is active.
- Routes to: `data-agent` (regenerate config alongside any reflow, or stop treating the config as a
  source of truth once a reflow has occurred without regenerating it).

---

## Verdict

**GO-WITH-FINDINGS — 1 open CRITICAL (F-V3).**

**1 CRITICAL.** 3 HIGH (F-C1 missing grade-B filter chip; F-V1 trace-reproducibility gap, same class as
bread/cakes/bars; F-C2 antithesis, 15 hits including one verbatim-repeated bars violation in the shared
SEO template). 3 MEDIUM (F-C3 em-dash volume + a repeated template phrase; F-V4 missing `_meta.off_used`
parity flag; F-V5 stale config file).

Per this agent's own Hard Rule 10 and the unified D10 gate definition, **the open CRITICAL (F-V3) blocks
launch by the letter of the rule** — a category may PASS only when Track C has zero open CRITICAL
findings. Unlike chocolate-bars (0 CRITICAL, cleaner exclusion documentation), tablets' exclusion
documentation was checked and found factually wrong: 3 of the 59 non-displayed products are C-grade, not
E-grade as the config claims, and the `_meta` count fields (`corpus_records`/`scored` = 33) do not match
either the displayed count (35) or the shared run's true scored count (92 tablets). This is a data-
provenance integrity failure, not a scoring-philosophy or frozen-invariant issue — it does not require
touching a published score, only correcting bookkeeping and the exclusion-reason claim.

**Summary assessment:** Justified-with-a-provenance-gap. The scoring engine's output for chocolate-
tablets holds up cleanly under adversarial reproduction pressure at the per-product level — every one of
8 sampled score deltas is fully and precisely explained by the same named, two-gate-signed TASK-455
commit that explains chocolate-bars, and both sampled grade-crosses (C→B, E→D) match the commit's own
`grade_movers` list exactly; 6/6 rank-checked superlative and co-leader claims verified TRUE against the
real 35-product corpus; ingredient-handoff is cleaner than bars (5/5 exact match, no divergence);
confidence-tooltip phrasing is honest. But the category-level bookkeeping — which products were
excluded and why, and how many were actually scored — does not hold up: the stated exclusion reason is
checkably false, and the `_meta` scored-count does not reconcile with either the served count or the
shared run's manifest. This is a narrower, more precisely diagnosable defect than "undocumented" (the
bars-report finding) — it is actively mis-documented.

**Recommendation for Product Agent's go/no-go:** no tripwire is implicated (no frozen invariant, no
scoring-philosophy change, nothing irreversible at stake — F-V3 is a bookkeeping/documentation correction,
not a re-score). This agent takes no position on timeline; it reports that F-V3 is open and, per Hard
Rule 10, blocks the unified D10 gate until resolved — Product Agent's go/no-go should treat this report as
**not yet clearing the gate** on its current findings, distinct from the chocolate-bars report which
cleared with 0 CRITICAL. F-C1 (missing grade-B chip) is a quick, low-risk frontend fix worth bundling with
whatever data-agent pass resolves F-V3, since both surfaced from the same TASK-455 reflow event without a
full downstream artifact refresh.

**Scope reminder:** this report covers chocolate-**tablets** only (`/hashvaot/chocolate-tablets`, 35
displayed of 92 scored products). Chocolate-**bars** (`/hashvaot/chocolate-bars`, separate frontend JSON,
separate route, GO-WITH-FINDINGS/0-CRITICAL) is covered by the companion report
`02_products/chocolate/reports/red_team_chocolate_bars_page_v1.md` and is not re-verified here. A prior,
narrower tablets report (`02_products/chocolate/reports/red_team_tablets_2026-07-03.md`) covered a
TASK-461 Phase-2 copy-overhaul candidate (insightLine/rowVerdict field isolation only, GO, 0/0/0 open) —
that report predates and does not cover the TASK-455 reflow's downstream `_meta`/config/filter
consequences found here, and is a different scope (copy-QA vs full launch gate), not a substitute.
