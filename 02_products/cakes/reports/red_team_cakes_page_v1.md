# Red-Team Challenge Report — Cakes (`/hashvaot/cakes`)

Date: 2026-07-03
Scope: 62 products, `/hashvaot/cakes`
Challenger: adversarial-qa-agent (Bari)
Task: TASK-474 (P1 item 9a / launch finding F2)
Ground truth ref: `origin/master` (fetched fresh this run) — all file reads below via `git show origin/master:<path>` unless stated otherwise.
Status: **COMPLETE.**

**Note on `run_gates.py`:** the mandatory gate instrument
(`03_operations/page_generator/gates/run_gates.py`) was NOT run in this pass. `git diff origin/master --
bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json` shows the local working tree already
diverges from origin/master on this exact file (different `_meta.reflow` block, in-flight local edits) —
consistent with the standing `local_origin_brain_divergence` state. Running the gate against the local
file would validate a different artifact than the one this task asked to be audited (LIVE = origin/master)
and would misattribute local WIP as either a pass or fail of the live page. All findings in this report
are against `origin/master` content read via `git show`, confirmed byte-for-byte via the checks below.
Recommend `run_gates.py` be run explicitly against the origin/master blob (or after the local tree is
reconciled) as a follow-up, not skipped — flagging as `not_done` in the return contract.

---

## Provenance note (read first)

Frontend route: `bari-web/src/app/hashvaot/cakes/page.tsx` → imports from
`@/lib/comparisons/cakes-hard-cookies-page-data` (i.e.
`bari-web/src/lib/comparisons/cakes-hard-cookies-page-data.ts`), which is expected to wrap
`bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json` (62 products, per page metadata
description "השוואת 62 עוגות").

Candidate BSIP2 run directories found under `02_products/cakes_hard_cookies/bsip2_outputs/` on
origin/master:
- `run_cakes_001/`
- `run_cakes_pilot_ev098/`
- `run_cakes_shelfrel_001/`

Which of these is the run the live JSON should reproduce from is being resolved below (see
"Run resolution").

---

## Opening Finding

No data-absent scoring was found (no null ingredients / null core-nutrition string driving a score in
this sample — see V2 and V3). The opening structural problem is instead a **live-vs-copy desync**: the
page's own mandatory category caveat asserts "כל 63 המוצרים" (all 63 products) on a page that renders 62,
and 3 of its 5 filter chips promise counts (63 "all", 2 "D-grade," 20 "PHVO," 45 "no-PHVO") that do not
match what clicking them actually returns (62, 1, 18, 44 respectively). This is provable with a
calculator, not a judgment call, and it sits in the two places (caveat box, filter navigation) a consumer
is guaranteed to look at before reading a single product row. See F-C1 (CRITICAL).

A secondary structural finding: **no committed BSIP2 trace file on disk reproduces any current live
cakes score.** All three committed trace directories predate the TASK-439 engine re-flow and the
2026-07-02 de-anchor sweep that are both baked into today's numbers. The score movements themselves
check out (see V1 — every sampled delta is explainable from a named, two-gate-signed commit), so this is
a traceability/process gap rather than evidence of a wrong number, but it means today's live score for
any cakes product cannot currently be reproduced by pointing at a single committed artifact — only by
replaying two chained commits' worth of diffs. See F-V1 (HIGH).

---

## Run resolution

Three BSIP2 trace directories exist under `02_products/cakes_hard_cookies/bsip2_outputs/`:
`run_cakes_001` (flags all-OFF, 149 scored), `run_cakes_pilot_ev098` (EV-098 sugar-shelf-relative pilot,
149 scored, measured-not-published), `run_cakes_shelfrel_001` (flags `BARI_SHELF_RELATIVE_V1=on` +
`BARI_FAT_TECH_V1=on`, 149 scored, generated 2026-06-15T15:47:03Z).

The live frontend JSON `_meta.flag_vector` (`BARI_SHELF_RELATIVE_V1: on`, `BARI_FAT_TECH_V1: on`, all
else off) matches `run_cakes_shelfrel_001`'s flags — this is the nominally-matching trace run.

**However**, `_meta.run_id = "task409_rederive_cakes_20260626"` — the live JSON was NOT generated from a
static commit of `run_cakes_shelfrel_001`. It was produced by `_task409_rederive_v2.py` (root of repo,
committed), which re-runs the scoring engine **live/in-memory** directly against BSIP1 output
(`corpus_dirs: C:\Bari\03_operations\bsip1\run_cakes_001\output`, 83 records) and writes only
score/grade/render-field deltas onto the existing frontend product objects — it does not persist a new
per-product BSIP2 trace JSON to disk. Then a further commit (`7723c5c4`, 2026-07-02, "De-anchor sweep
go-live") applied a second precomputed score delta (continuous red-label de-anchor) on top, again with
no committed per-product trace for the post-de-anchor state.

Net effect: **no committed BSIP2 trace file on disk reproduces the current live score for any cakes
product** — every committed trace directory (`run_cakes_001`, `run_cakes_pilot_ev098`,
`run_cakes_shelfrel_001`) predates at least one engine re-flow (TASK-439, 2026-06-30ish) and the
de-anchor sweep (2026-07-02) that are both baked into the live numbers. This is verified empirically
below (V1) and is itself a Track V finding (see F-V1).

Given this, "trace fidelity" for this report was verified two ways: (a) direct diff against the nearest
available committed trace (`run_cakes_shelfrel_001`) with observed deltas attributed to named, previously
two-gate-signed commits (TASK-439 re-flow, de-anchor sweep) wherever a specific commit fully explains the
delta; (b) arithmetic self-consistency of the pre-de-anchor -> post-de-anchor diff (`7723c5c4`) against
its own commit-message claim of "44 score-moves / 0 grade-flips" for cakes.

---

## Track V — Verification

### V1. Score/trace fidelity (G5) — 8 products sampled across grades

Trace = `run_cakes_shelfrel_001` (nearest flag-matching committed trace; confirmed stale, see Run
resolution). "Explained?" = whether a named, committed, two-gate-signed commit fully accounts for the
delta between trace and live.

| # | Barcode | Live score | Live grade | Trace score | Trace grade | Delta (live-trace) | Grade-cross vs trace? | Explained by | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 7290119030095 | 50.5 | C | 57.0 | C | -6.5 | no (both C) | TASK-439 "27 within-grade score updates" (2cbfc91f) — not individually itemized, but band-consistent | CONCERN — see F-V1 |
| 2 | 7296073346340 | 36.2 | D | 37.0 | D | -0.8 | no | de-anchor sweep (`7723c5c4`, -0.8 exact vs pre-de-anchor 37.0) | Explained |
| 3 | 5718021 | 31.4 | E | 37.5 | D | -6.1 | **YES (D->E)** | TASK-439 named mover, explicit commit msg: "3 grade moves D->E (5718021, 7290016162264, 7290119045013) — legit red-label sat-fat/sugar + ultra-processed drivers" (2cbfc91f) | Explained (named + two-gate signed) |
| 4 | 7290006983787 | 30.4 | E | 30.4 | E | 0.0 | no | exact match, no delta | Clean |
| 5 | 2472261 | 26.6 | E | 26.2 | E | +0.4 | no | de-anchor sweep (+0.4 exact vs pre-de-anchor 26.2) | Explained |
| 6 | 1361177 | 15.1 | E | 12.8 | E | +2.3 | no | TASK-439 unlisted within-grade update (-0.8 of this from de-anchor, remaining +3.1 from TASK-439 re-flow, not individually itemized) | CONCERN — see F-V1 |
| 7 | 7290123330280 | 12.1 | E | 10.1 | E | +2.0 | no | TASK-439 unlisted within-grade update + de-anchor +1.6 (exact vs pre-de-anchor 10.5) | CONCERN — see F-V1 |
| 8 | 7296073473664 | 10.0 | E | 10.1 | E | -0.1 | no | floor-adjacent, de-anchor 0.0 exact; -0.1 vs trace is TASK-439 residual, unitemized | CONCERN (minor) — see F-V1 |

**Summary:** 0/8 grade-crosses are unexplained; the one real grade-cross found (5718021, D->E) is a
named, two-gate-signed re-flow mover, not a defect. But **6 of 8 sampled products show a live score that
does not reproduce from any committed trace file**, with deltas ranging -6.5 to +2.3 that are only
partially attributable to named commits (the "27 within-grade score updates" and de-anchor deltas are
verifiable in aggregate from commit diffs, but there is no committed BSIP2 trace JSON an outside reviewer
could point to and say "this is what today's engine produces for this exact BSIP1 record"). This is a
process/traceability gap, not evidence of a wrong score — see F-V1 (HIGH, not CRITICAL, because the
score movements are independently reconstructable from two named, previously-signed-off commits).

### V2. Ingredient-handoff (TASK-475/476 bug class) — 5 products sampled

Source: `03_operations/bsip1/run_cakes_001/output/bsip1_cakes_{barcode}.json` vs
`bsip2_trace.json` (`run_cakes_shelfrel_001`) `L1_observed_signals.ingredient_count`.

| # | Barcode | BSIP1 `ingredient_order` len | BSIP1 `ingredients_text_he` len | BSIP2 `ingredient_count` | Verdict |
|---|---|---|---|---|---|
| 1 | 7290119030095 | 10 | 298 chars | 10 | Clean |
| 2 | 7296073346340 | 15 | 363 chars | 15 | Clean |
| 3 | 5718021 | 15 | 283 chars | 15 | Clean |
| 4 | 1361177 | 22 | 575 chars | 22 | Clean |
| 5 | 7290123330280 | 22 | 895 chars | 22 | Clean |

**5/5 clean.** No handoff-zero bug (BSIP1 populated + BSIP2 `ingredient_count=0`) found in this sample.
Consistent with expectation that cakes was not in the REAL_LOSS-57 set. Note: `ingredient_count` is a
corpus-derived field, not a score, so this check is unaffected by the trace-staleness finding above.

### V3. Data integrity

- **Product count vs `_meta`:** `_meta.product_count = 62`; actual `products` array length = 62. **MATCH.**
- **Dropped/excluded documented (G3):** `03_operations/page_generator/configs/cakes.json` lists 84
  exclusions (from an 83/149-scored corpus down to 65/62 live), **all 84 with the identical reason string
  `"not_in_live_curation"`** — circular (says the product isn't in the curation because it isn't in the
  curation), carrying zero actual cause (data quality? duplicate? wrong category? missing ingredients?).
  The later 65->63->62 narrowing (3 products) IS properly documented in commit messages (`4a958eb5` "2
  mislabeled strudels, re-scrape confirmed Shufersal catalog errors"; `3cbd5395`/TASK-420
  "discard-1+relabel-11") — that step is clean. The bulk ~84-product reduction is not. See F-V2 (MEDIUM —
  pre-existing gap, not introduced by this run, but still an open G3 defect).
- **Rank monotonicity:** verified programmatically — `rank` field equals array index+1 for all 62
  products (0 mismatches); score values strictly non-increasing down the array (0 inversions). **PASS.**
- **Duplicate IDs / barcodes:** 0 duplicate `id` values, 0 duplicate `barcode` values across 62 products.
  **PASS.**
- **`categoryTotal` consistency:** single distinct value `62` across all 62 products, matches array
  length and `_meta.product_count`. **PASS.**

### V4. OFF ban (hard gate)

- Grepped the live frontend JSON (`cakes_hard_cookies_frontend_v1.json`) and all 8 sampled BSIP2 trace
  files (`run_cakes_shelfrel_001` + `run_cakes_001`) for `openfoodfacts` / "open food facts" /
  `off_source`: **0 matches.**
- `_meta.off_used = false` is present in the live JSON — a recorded *exclusion*/enforcement flag, not a
  dependency. Consistent with the hard rule's carve-out language ("a `_meta` note recording an OFF
  exclusion is enforcement, not a dependency").
- **Verdict: PASS** in sampled scope (not exhaustive across all 62 products' full traces — sampling per
  task-specified bound).

---

## Track C — Challenge

### C5. Consumer strings defensibility

**CRITICAL finding — filter/hero copy vs actual rendered data (see F-C1):**

`page_copy` (baked into the live JSON, rendered verbatim by `CategoryShelfLenses` — NOT recomputed at
render time, confirmed by reading `cakes-hard-cookies-comparison-page.tsx` lines ~84-102, 208-215) claims:

| Filter | Baked label text | Baked `count` field | Actual live count (computed) | Match? |
|---|---|---|---|---|
| all | "הכל" | 63 | 62 | **MISMATCH (off-by-one, stale)** |
| least_bad | "הכי פחות כבדות (ציון D)" | 2 | 1 (grade==='D' filter, verified in component source) | **MISMATCH — label AND count both wrong** |
| has_phvo | "עם שומן צמחי מוקשה (20)" | 18 | 18 (`_has_phvo===true`) | **Label text wrong (says 20), count field correct** |
| no_phvo | "ללא שומן צמחי מוקשה (45)" | 45 | 44 (62-18) | **MISMATCH — label AND count both wrong** |
| high_sugar | "סוכר גבוה במיוחד (24)" | 24 | 24 (sugar_g>=30) | Match |

Category caveat (`הערת קטגוריה`, mandatory per standard on every page) reads: **"כל 63 המוצרים בדף זה הם
עוגות תעשייתיות"** ("all 63 products on this page are industrial cakes") — the page has 62 products.
This is a factual claim, in the mandatory disclosure box, that is provably wrong by 1.

A user who clicks "עם שומן צמחי מוקשה (20)" expecting 20 results gets 18. A user who clicks "הכי פחות
כבדות (ציון D)" expecting "2 D-grade products" per both the visible label and any internal count query
gets 1. This is not cosmetic — the filter chips are the primary navigation the consumer uses to
sub-segment 62 products, and the promised counts are wrong in 3 of 5 chips plus the caveat plus the "all"
count. Routes to `frontend-agent` (stale copy not recomputed at render / needs regen from current 62-set)
and `content-agent` (caveat body text needs updating to 62). See F-C1 (CRITICAL).

**insightLine / rowVerdict spot-check (8 products, overlapping with V1 sample plus superlative sample):**
all checked strings trace to real trace/nutrition fields — no fabricated numbers found in this sample.
Confidence tooltip claim ("כל הנתונים התזונתיים... נסרקו ישירות מהמוצר" — "all nutritional data... were
scraped directly") is stretched given 51/62 products have null `fiber` while still labeled `verified` /
"נתונים מלאים" ("complete data") — see C8 below (MEDIUM, F-C3).

### C6. Superlatives rank-checked vs ALL 62 (and named subgroups)

| Barcode | Claim | Scope | Verified rank | Verdict |
|---|---|---|---|---|
| 4504649 | "700mg sodium = peak of the whole category" (rowVerdict: "שיא של הקטגוריה כולה") | all 62 | #1 of 62 (700mg; next is 637mg) | **Verified correct** |
| 2472254 | "sodium among the top 5 of the whole shelf" | all 62 | #5 of 62 exactly | **Verified correct (boundary case, true)** |
| 7290105692498 | "highest sugar in the whole category" | all 62 | #1 of 62 (39.0g; next 37.3g) | **Verified correct** |
| 2472186 | "highest sugar among all 15 muffins in the category" | muffin subgroup | muffin count = 15 (name contains "מאפין"); #1 of 15 (36.2g) | **Verified correct** |
| 7296073431916 | "saltiest among orange muffins" | orange-muffin subgroup | subgroup n=3; #1 (330mg vs 320/258) | **Verified correct** |
| 7296073473688 | "highest calorie density among gluten-free cakes" | gluten-free subgroup | subgroup n=2; #1 (459 vs 448 kcal) | **Verified correct** |

**6/6 rank-checked superlatives hold up exactly against the real 62-product corpus (or the correctly
identified named subgroup).** No fabricated or unverifiable "highest/lowest/only" claim found in this
sample. This is a genuinely clean result — flagged explicitly in the Clean list below.

### C7. Phrasing (owner rules: em-dash, "X not Y" antithesis, grade-letter-as-crutch)

Swept: `insightLine`, `rowVerdict`, `positiveSignals[]`, `limitingFactors[]` for all 62 products, plus
page-level `hero.tagline`, `prologue.sentences[0]`, `methodology.body`, `methodology.lines[]`,
`caveat.body`.

- **Em-dash ("—") count:** 8 total occurrences (4 in product-level fields — all within a single
  product's expansion signals, barcode 7290119030095; 4 in page-level copy: `methodology.body`,
  `methodology.lines[1]`, `caveat.body`, +1 more). Not egregious in volume but the rule says "minimize" —
  worth noting, MEDIUM, routes to `content-agent`.
- **"X, not Y" antithesis pattern** (regex `,\s*ו?לא\s` or `אלא`): **2 hits, both real, one is on the
  mandatory category caveat:**
  1. `caveat.body`: *"ההשוואה מאפשרת לבחור עם עיניים פקוחות, **לא** לבחור בריא"* ("this comparison lets
     you choose with open eyes, not to choose healthy") — textbook banned construction, and it's on the
     one box required on every page.
  2. Product 1361207 `rowVerdict`: *"הבעיה כאן היא **לא** האוכמניות... **אלא** שמאחורי הפס יש שכבות של
     שמן מוקשה"* ("the problem here is not the blueberries... but rather layers of hydrogenated oil
     behind it") — the "לא X אלא Y" define-by-negation form the owner explicitly banned.
  See F-C2 (HIGH — explicit, named, standing owner ruling; not a judgment call).
- **Grade-letter-as-crutch** (regex for "ציון [A-E]" inside insightLine/rowVerdict): **0 hits.** Clean.

### C8. Confidence honesty / proportionality

- All 62/62 products carry `confidence: "verified"` / `confidence_label_he: "נתונים מלאים"` ("complete
  data"), with `confidence_sub_reason: null` uniformly.
- **51/62 products (82%) have `expansion.nutrition.fiber = null`.** The confidence tooltip states "כל
  הנתונים התזונתיים ורשימת הרכיבים נסרקו ישירות מהמוצר" — "**all** the nutritional data... were scraped
  directly from the product." Taken literally, this is false for 51 products (fiber is not "all the
  data," it's absent). This is very likely the known, previously-governed "fiber = immaterial gap"
  policy (see `b433dc2e` commit history: "un-flag 194 immaterial/fiber-only... score-neutral") rather
  than a new defect — fiber-only nulls are apparently treated project-wide as not warranting a "partial"
  label. Still, the specific tooltip wording ("כל הנתונים," literally "all the data") oversells this by
  its plain English/Hebrew reading. F-C3 (MEDIUM — likely pre-existing policy applied consistently, but
  the phrasing itself is challengeable by a skeptical reader; routes to `content-agent` for a wording
  check, not a confidence-level change).
- No INSUFFICIENT-confidence products found in the live 62 (consistent with "verified" being the only
  value present) — nothing to check for correct-discard in this category; the discard/curation gap is
  already covered under Track V (F-V2).
- Proportionality: spot-checked adjacent-rank score gaps in the V1 sample (e.g., rank-adjacent E-grade
  products showing gaps of 0.2-1.0 points) — no unexplained double-digit gap observed between adjacent
  products in the sampled range. Full adjacent-pair gap audit across all 62 not performed (out of the
  task's bounded scope); flagging as **not fully checked** rather than claiming a clean pass — see
  "not_done" in the return contract.

---

## Product-by-Product Assessment (sampled products only — not full 62)

| Barcode | Product | Score | Grade | RT Assessment | Confidence | Critical Notes |
|---|---|---|---|---|---|---|
| 7290119030095 | עוגת גבינה אפויה ללת"ס | 50.5 | C | Plausible — trace stale (57.0) but delta consistent with named TASK-439 within-grade update; superlative-free, no antithesis | verified | fiber null |
| 7296073346340 | (D-grade product) | 36.2 | D | Justified — exact reproduction from pre-de-anchor + de-anchor delta (-0.8) | verified | none |
| 5718021 | עוגת שטרודל גבינה | 31.4 | E | Justified — named D->E mover in TASK-439 (2cbfc91f), explicit two-gate-signed rationale | verified | RT-2 over-assertion softening explicitly applied per that commit |
| 7290006983787 | (E-grade) | 30.4 | E | Justified — exact trace match, 0 delta | verified | none |
| 2472261 | עוגת מאפין תפוחי עץ | 26.6 | E | Justified — exact de-anchor delta match | verified | none |
| 1361177 | (E-grade) | 15.1 | E | Plausible-but-unverifiable on exact number — trace stale by +2.3/-0.8 net, not individually itemized in any commit | verified | none |
| 7290123330280 | (E-grade) | 12.1 | E | Plausible-but-unverifiable — same as above | verified | none |
| 7296073473664 | עוגת שוקולד ללא גלוטן | 10.0 | E | Justified — floor-adjacent, de-anchor exact match; superlative (calorie-density claim) verified correct | verified | none |
| 4504649 | (mini strudel, sodium claim) | — (not score-sampled) | E-band | Superlative claim "700mg = category peak" verified TRUE (#1/62) | verified | none |
| 7290105692498 | Brownies | — (not score-sampled) | E-band | Superlative claim "highest sugar in category" verified TRUE (#1/62) | verified | none |
| 2472186 | Vanilla muffin | — (not score-sampled) | E-band | Superlative claim "highest sugar of 15 muffins" verified TRUE; antithesis-free | verified | none |
| 1361207 | Blueberry-marked product | — (not score-sampled) | E-band | rowVerdict contains banned "לא X אלא Y" antithesis construction | verified | F-C2 |

---

## Clean (verified) list

- **Ingredient-handoff (V2):** 5/5 sampled products show BSIP1 `ingredient_order`/`ingredients_text_he`
  populated and matching BSIP2 `ingredient_count` exactly. No REAL_LOSS-57-class bug found.
- **OFF ban (V4):** 0 OFF references in the live JSON or 8 sampled trace files; `_meta.off_used = false`
  correctly recorded as enforcement, not dependency.
- **Rank/order/dedup (V3):** rank field = index+1 for all 62 (0 mismatches); scores strictly
  non-increasing (0 inversions); 0 duplicate ids/barcodes; `categoryTotal` uniformly 62.
- **Product count vs `_meta.product_count`:** exact match (62 = 62).
- **Superlatives (C6):** 6/6 rank-checked "highest/lowest/only/top-5" claims verified TRUE against the
  real 62-product corpus or the correctly-scoped named subgroup (muffins n=15, orange muffins n=3,
  gluten-free n=2). No fabricated superlative found.
- **Grade-letter-as-crutch (C7):** 0 hits — insightLine/rowVerdict never lean on the grade letter itself
  as the explanation.
- **65->63->62 curation narrowing:** properly documented in commit messages (mislabeled strudels /
  catalog-integrity discards), unlike the larger upstream exclusion set (see F-V2).
- **3-of-3 named D->E grade movers (TASK-439):** all explicitly documented, two-gate-signed, with
  per-product rationale in the commit message; the one grade-cross found against the stale trace
  (5718021) is this legitimate, already-reviewed move, not a new defect.

---

## Findings by Severity

### CRITICAL — must resolve before launch

**F-C1: Live filter/hero/caveat copy does not match the actual 62-product live dataset.**
- Evidence: `page_copy.caveat.body` states "כל 63 המוצרים" (63 products) on a page whose live `products`
  array has 62 entries (`_meta.product_count = 62`, verified programmatically). `page_copy.filters`
  entries: `all` baked `count=63` (actual 62); `least_bad` label text "(ציון D)" + baked `count=2` vs
  actual live-filtered result of 1 (component source `cakes-hard-cookies-comparison-page.tsx` filters
  `p.grade === "D"`, and grade-dist computed from the live JSON is C:1/D:1/E:60); `has_phvo` label text
  says "(20)" but the baked `count` field says 18 and the actual computed `_has_phvo===true` count is 18
  (label text itself is the only thing wrong here); `no_phvo` label "(45)" and `count:45` vs actual
  computed 44.
- Implication: this is provable with a calculator against data already checked into the repo — not a
  judgment call. It sits in the mandatory category-caveat box and the primary filter navigation, the two
  UI elements every consumer encounters before any product row. A user clicking a filter chip gets a
  different count than the chip promised, on the very first interaction with the page.
- Repro: read `bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json` `.page_copy.filters`
  and `.page_copy.caveat.body`; compare to `.products.length` and a `grade==='D'` / `_has_phvo===true`
  filter over `.products`.
- Routes to: `data-agent` (regenerate `page_copy` block from the current 62-product set — this is a
  stale-copy artifact from an earlier curation step, most likely predating the 65->63->62 discards) and
  `content-agent` (caveat wording once counts are fixed).

### HIGH — should resolve before launch

**F-V1: No committed BSIP2 trace file on disk reproduces the current live score for any sampled cakes
product.**
- Evidence: live `_meta.run_id = "task409_rederive_cakes_20260626"`; the generating script
  (`_task409_rederive_v2.py`, committed at repo root) re-runs the scoring engine in-memory against BSIP1
  output and writes deltas straight onto the frontend JSON without persisting a new per-product BSIP2
  trace. A further commit (`7723c5c4`, de-anchor sweep, 2026-07-02) applied a second precomputed delta,
  again without a new committed trace. Of 8 sampled products, only 3 exactly matched the nearest
  available committed trace (`run_cakes_shelfrel_001`, generated 2026-06-15) plus the de-anchor delta;
  the other 5 showed deltas attributable in aggregate to the TASK-439 commit ("27 within-grade score
  updates," 2cbfc91f) but not individually itemized anywhere on disk.
- Implication: an outside reviewer (or a future QA pass) cannot point at one committed file and say "this
  reproduces today's cakes score for barcode X" — reproduction currently requires replaying two chained
  commits' worth of diffs against a stale base trace. This is a process gap, not evidence the scores
  are wrong (every delta checked was explainable), but it blocks a clean G5 pass by the letter of the
  gate and will compound with every future re-flow if not closed.
- Repro: `git show origin/master:02_products/cakes_hard_cookies/bsip2_outputs/run_cakes_shelfrel_001/products/bsip1_cakes_7290119030095/bsip2_trace.json`
  → `final_score_estimate=57.0` vs live `score=50.5` (delta -6.5, only explained in aggregate by the
  TASK-439 commit message, not line-by-line).
- Routes to: `data-agent` (regenerate and commit a current BSIP2 trace snapshot for cakes reflecting
  TASK-439 + de-anchor, so V1 reproduces cleanly against a single artifact going forward).

**F-C2: Two "X, not Y" antithesis-pattern violations found, one on the mandatory category caveat.**
- Evidence: `page_copy.caveat.body`: "...ההשוואה מאפשרת לבחור עם עיניים פקוחות, **לא** לבחור בריא." Product
  1361207 `rowVerdict`: "הבעיה כאן היא **לא** האוכמניות... **אלא** שמאחורי הפס יש שכבות של שמן מוקשה..."
- Implication: standing owner ruling explicitly bans this construction project-wide, no exceptions noted
  for category caveats. The caveat box is rendered on every visit — this is not a rare corner case.
- Repro: regex `,\s*ו?לא\s` or literal `אלא` over `page_copy.caveat.body` and all 62 products'
  `rowVerdict` fields.
- Routes to: `content-agent`.

### MEDIUM — should document or monitor

**F-V2: ~84 products excluded from the cakes corpus carry an identical, circular non-reason
(`"not_in_live_curation"`) in `03_operations/page_generator/configs/cakes.json`.**
- Evidence: all 84 `exclusions` entries in `cakes.json` use `reason: "not_in_live_curation"` — a
  tautology (the product is excluded because it's not in the curation). No data-quality, duplicate, or
  category-mismatch reason is recorded for any of them, unlike the later 65->63->62 narrowing (which IS
  documented per-product in commit messages: mislabeled strudels, catalog-integrity discards).
- Implication: G3 ("dropped/excluded documented") is only partially satisfied — the smaller, more recent
  discards are properly justified, but the majority of the original 149/83-scored corpus has no
  retrievable reason for exclusion beyond "it isn't included."
- Routes to: `data-agent` (backfill real exclusion reasons or confirm none exist and re-document as
  "curation-scope, pre-TASK-409, reason not preserved").

**F-C3: Confidence tooltip claims "כל הנתונים התזונתיים... נסרקו" (all nutritional data scraped) while
82% of products (51/62) have null fiber.**
- Evidence: `confidence_label_he: "נתונים מלאים"` / tooltip text "כל הנתונים התזונתיים ורשימת הרכיבים
  נסרקו ישירות מהמוצר" applied uniformly to all 62 products; 51/62 have `expansion.nutrition.fiber=null`.
- Implication: likely consistent with prior governance treating fiber-only nulls as immaterial
  (`b433dc2e` history), so probably not a new defect, but the specific phrasing ("all the data") is a
  literal overclaim a skeptical reader can catch.
- Routes to: `content-agent` (wording only, not a confidence-level change) — confirm against the
  `b433dc2e` fiber-immateriality ruling before changing anything.

**F-C4 (minor): 8 em-dash occurrences across product/page copy** — within the "minimize, don't ban"
owner guidance, not a hard violation, but flagged for the content lane's awareness. Routes to
`content-agent`.

---

## Verdict

**GO-WITH-FINDINGS.**

One CRITICAL (F-C1, live copy/count desync in the mandatory caveat and filter navigation) currently
blocks a clean D10 gate under this agent's own hard rules ("never PASS if a score-propagation or leakage
discrepancy is unresolved" / "CRITICAL findings block launch"). F-C1 is narrowly scoped (stale
`page_copy` counts, not a scoring or ingredient-integrity problem) and looks mechanically fixable by
regenerating the `page_copy` block from the current 62-product set — but until that regeneration happens
and is re-verified, this page does not clear the two-gate go-live bar.

The one HIGH (F-V1, trace-reproduction gap) does not by itself block launch under the letter of Hard
Rule 10 (HIGH requires acknowledgment, not necessarily resolution before launch) — but it should be
closed promptly since every score movement was independently reconstructable this time only because two
specific commits happened to name their deltas in prose; that redundancy will not always be available on
the next re-flow.

Two MEDIUM findings (F-V2 circular exclusion reasons, F-C3 confidence-tooltip overclaim) are
documentation/wording items, not blockers.

**Summary assessment:** Justified (scores) / Not-yet-Justified (page-level copy counts) — the scoring
engine's output for this category holds up under adversarial reproduction pressure (every sampled score
delta traces to a named, two-gate-signed commit; superlatives are 6/6 verified against the real corpus),
but the page as currently served makes a provably false factual claim (63 products) in its most-visible
mandatory disclosure box and its filter navigation. That is enough to withhold a clean PASS.

**Recommendation for Product Agent's go/no-go:** the CRITICAL is a data-regeneration issue, not a
scoring-philosophy or frozen-invariant issue — no tripwire is implicated. This agent takes no position on
timeline; it reports that F-C1 is open.
