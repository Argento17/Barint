# TASK-461 Phase-2 Fan-Out Audit — Copy Badness Across All Live Comparison Categories

**Scope:** read-only. Source of truth = `origin/master` (NOT local working tree — local category JSONs
are stale after recent merges). Every file below was extracted with
`git show origin/master:bari-web/src/data/comparisons/<file>` into the scratchpad and analyzed there.
Zero git writes, zero repo edits performed by this lane.

**Script:** `audit_copy.py` (scratchpad) — identical logic run over all 16 files.
**Raw output:** `fanout_audit_metrics.json` (scratchpad).

## Category set and exact file audited

16 live categories on `origin/master`. Two had version ambiguity (bread v3/v4, cheese v4/v5);
resolved by reading the actual page-data adapter import, not by filename-latest assumption.

| category key | file audited | blob sha (origin/master) | resolved via |
|---|---|---|---|
| bread_v4 | `bread_frontend_v4.json` | `b2fb0fd484503ea89b0241acfee32a1843579e37` | `bread-comparison-page-data.ts` imports `bread_frontend_v4.json` (bread-page-data.ts imports a different, unrelated `bread-retail-curated.json` used elsewhere) |
| brined_cheeses_v2 | `brined_cheeses_frontend_v2.json` | `ef1c8045cb97e1ca13f5cd718c11ec45b7664be7` | only version present |
| cakes_hard_cookies_v1 | `cakes_hard_cookies_frontend_v1.json` | `5a72a79e109f19fcbd88b7fb3ea5e7c47ac1118b` | only version present |
| cereals_v2 | `cereals_frontend_v2.json` | `30c0b0ec6637acb4b2c10f4e713a8b94bf3be1c5` | only version present |
| cheese_v5 | `cheese_frontend_v5.json` | `deec2e911cb369444f7bec796ff468220b75c37a` | `cheese-page-data.ts` imports `cheese_frontend_v5.json` (v4 is superseded/unused) |
| chocolate_bars_v1 | `chocolate_bars_frontend_v1.json` | `5c625b7b56508c1949312a6612f672ad1dde2038` | only version present |
| chocolate_tablets_v1 | `chocolate_tablets_frontend_v1.json` | `45c962fe990ca21be87320b3f65cbc4982803869` | only version present |
| cookies_coffee_v2 | `cookies_coffee_frontend_v2.json` | `675eac00510d2a7ba77ce17928639ade04275102` | only version present |
| crackers_v1 | `crackers_frontend_v1.json` | `784af2593a3c98d3cf08c9368c563239d8e7eb08` | only version present |
| granola_v2 | `granola_frontend_v2.json` | `2312442beb6a44a106b472c5751bfeb12f16a471` | only version present |
| hard_cheeses_v4 | `hard_cheeses_frontend_v4.json` | `a93efc84c0b600ba092b1c7f5a2e38595dd0c7d2` | only version present |
| hummus_v5 | `hummus_frontend_v5.json` | `2fbd70fdc8368b93333d01b34fa3726397b380ad` | only version present |
| juices_v3 | `juices_frontend_v3.json` | `95c42010dd40a3bada829e0e6efcd88c6d802f09` | only version present |
| milk_v1 | `milk_frontend_v1.json` | `ad3592b2741aa6f6465a3ebf41d81651479b9201` | only version present |
| protein_combined_v2 | `protein_combined_frontend_v2.json` | `4127b58965bebb689016ba58388eda39b312f9d7` | only version present |
| snacks_v5 | `snacks_frontend_v5.json` | `4febff7befeed04274ae00113ea3de6ba771506c` | only version present |

Note on scope: `hard_cheeses_v4` and `cheese_v5` are two distinct live pages (hard/yellow cheeses vs
the de-anchored general cheese page) — both audited separately, as instructed by the category list.

## Method notes (so the numbers are reproducible, not vibes)

- **Em dashes** — literal `—` count in `insightLine + rowVerdict` concatenated per product.
- **Raw-number recitation** — regex for `\d+ (גרם|מ"ג|קק"ל|%|אחוז)` or `N רכיבים` anywhere in the
  combined text. **Caveat (see cereals row below):** this regex cannot distinguish "number recited
  because it already appears in the pills/table" (bad) from "number IS the story" (fine, per the
  TASK-461 voice standard §2). Cereals scores 95% on this metric yet is the golden reference —
  its numbers are argument-bearing ("95% מהמוצר הוא חיטה. הדגן הוא הסיפור כולו"), not recited. Treat
  raw-number % as a **screening signal**, not a verdict; the qualitative read below is the tiebreaker.
- **Engine-mechanic vocabulary** — literal counts of חציון / חיסרון / מדד עיבוד / תקרת עיבוד /
  רמת אמון / פרמטרים / נקודות. Manually eyeballed 3 samples per nonzero category to screen false
  positives. Found one real false positive: crackers' single "נקודות" hit is idiomatic ("נותנים לו
  נקודות טובות" = colloquial "gives it good marks", not a score-points leak) — excluded from read
  but left in the raw count since it's a single occurrence and doesn't change the ranking.
  hard_cheeses' "נקודות" hit ("מתקבצת עם המקבץ הרחב של ה-67 נקודות") IS a real score-leak (67 is a
  literal score value) — genuine mechanic exposure despite the category's otherwise clean em-dash profile.
- **Template repetition** — top-5 most repeated first-2-word openings of insightLine; % of products
  sharing their first 3 words with ≥1 other product; top repeated 5-grams across
  insightLine+rowVerdict combined (only grams occurring >1 time surfaced).
- **"X, not Y" / negation** — approximate regex count of ` ולא ` / `אבל לא` / `לא X אלא` (X ≤15 chars)
  across combined text. Approximation flagged per the task's own instruction; true define-by-negation
  requires reading each hit, which was spot-checked but not exhaustively re-verified per hit.
- **OFF scan** — no Open Food Facts references found in any of the 16 files (see `off_references_found`
  in the JSON, empty array in all 16 categories).
- **Composite "badness" ranking** — `mechanic% × 3.0 + em_dash_gt1% × 1.0 + rawnum% × 0.5 +
  shared_opening3% × 0.5 + em_dash_mean × 10`. Weights reflect the owner's stated priorities in
  TASK-461: mechanic leakage is the worst offender (internal vocabulary exposed to consumers),
  em-dash overuse and opening-template repetition are the visible "robotic" tells, raw-number
  recitation is real but partially conflated with legitimate number-driven copy (see caveat above)
  so it's weighted lower. This is a **screening ranking**, not a substitute for the per-category
  qualitative read — cereals proves the metric alone misclassifies a golden-voice category as
  "number-heavy."

## Ranked table (worst → best by composite badness)

| rank | category | N | cov% | em Σ | em mean | em>1% | rawnum% | mech% | shared-open3% | neg(approx) | badness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **brined_cheeses_v2** (pilot, calibration row) | 36 | 100 | 74 | 2.06 | 69.4 | 100.0 | **69.4** | 22.2 | 7 | 359.3 |
| 2 | cheese_v5 | 47 | 100 | 94 | 2.00 | 93.6 | 100.0 | 0.0 | 23.4 | 1 | 175.3 |
| 3 | chocolate_tablets_v1 | 35 | 100 | 80 | 2.29 | 88.6 | 91.4 | 2.9 | 0.0 | 5 | 165.9 |
| 4 | juices_v3 | 17 | 100 | 38 | 2.24 | 82.4 | 94.1 | 0.0 | 11.8 | 2 | 157.8 |
| 5 | bread_v4 | 23 | 100 | 47 | 2.04 | 87.0 | 56.5 | 0.0 | 43.5 | 3 | 157.4 |
| 6 | snacks_v5 | 21 | 100 | 55 | 2.62 | 81.0 | 100.0 | 0.0 | 0.0 | 4 | 157.2 |
| 7 | protein_combined_v2 | 32 | 100 | 54 | 1.69 | 65.6 | 100.0 | 6.2 | 9.4 | 7 | 155.8 |
| 8 | granola_v2 | 22 | 100 | 52 | 2.36 | 81.8 | 77.3 | 0.0 | 9.1 | 2 | 148.6 |
| 9 | **cereals_v2 (GOLDEN REFERENCE)** | 20 | 100 | 38 | 1.90 | 70.0 | 95.0* | 0.0 | 10.0 | 0 | 141.5* |
| 10 | cookies_coffee_v2 | 117 | 100 | 242 | 2.07 | 82.9 | 54.7 | 0.9 | 12.0 | 5 | 139.7 |
| 11 | hummus_v5 | 57 | 100 | 97 | 1.70 | 50.9 | 100.0 | 5.3 | 10.5 | 6 | 139.1 |
| 12 | crackers_v1 | 19 | 100 | 34 | 1.79 | 68.4 | 52.6 | 5.3† | 0.0 | 0 | 128.5 |
| 13 | cakes_hard_cookies_v1 | 62 | 100 | 102 | 1.65 | 62.9 | 50.0 | 1.6 | 12.9 | 2 | 115.7 |
| 14 | chocolate_bars_v1 | 23 | 100 | 32 | 1.39 | 30.4 | 100.0 | 0.0 | 0.0 | 0 | 94.3 |
| 15 | hard_cheeses_v4 | 31 | 100 | 21 | 0.68 | 16.1 | 100.0 | 3.2‡ | 0.0 | 1 | 82.5 |
| 16 | milk_v1 | 18 | 100 | 18 | 1.00 | 27.8 | 50.0 | 0.0 | 11.1 | 5 | 68.3 |

\* Cereals' 95% raw-number rate is **not** recitation badness — see method caveat; qualitative read
below shows the numbers are argument-bearing. Its true rank on the *voice* axis (not the mechanical
metric) is #1 best, not #9. The composite score under-penalizes it for using numbers well; treat
the numeric rank as informational only for this row.

† Crackers' one mechanic-vocab hit is a confirmed false positive (idiomatic "נקודות טובות"), so its
true mechanic-leakage rate is 0/19, not 5.3%.

‡ Hard_cheeses' one mechanic-vocab hit is a confirmed TRUE positive (literal score value "67 נקודות"
leaked into rowVerdict) despite the category's otherwise-cleanest em-dash profile in the corpus.

## Qualitative read (3 sentences per category) + one representative insightLine

**brined_cheeses_v2 (calibration row, pilot in flight):** Recites data — "שלושה רכיבים / X מ"ג נתרן"
stamped across the shelf with internal scoring vocabulary (חציון/חיסרון/רמת אמון) leaking straight
into consumer copy. Reads as system output, not a verdict. Example: *"הנתרן (600 מ"ג) נמוך משמעותית
מחציון המדף — ולכן הגבינה הזו נמלטת מחיסרון פער הנתרן."*

**cheese_v5:** insightLine is terse tag-soup ("חלבון גבוה, קלוריות מינימליות, ללא תוספים") with no
verb, no opinion, just three nutrition-panel words back to back; rowVerdict then re-recites the exact
same numbers that already render in the table. No engine-mechanic leakage, but zero voice — purely
descriptive. Example: *"חלבון גבוה, קלוריות מינימליות, ללא תוספים"* (insightLine, קוטג 1%).

**chocolate_tablets_v1:** Heaviest em-dash use in the corpus (2.29 mean, 88.6% of products with >1)
stacked onto near-total raw-number recitation (91.4%); reads as a spec sheet chained together with
dashes rather than a verdict. Needs sampling to confirm whether any opinion survives under the dashes.
*(Representative line not hand-verified beyond the metric — flag for the fan-out executor to read
before scoping the rewrite.)*

**juices_v3:** Small category (17 products) but very high recitation (94.1%) and em-dash overuse
(82.4% >1); combined with 11.8% opening-template sharing, this reads as a template stamped with
numbers substituted per product rather than product-specific reasoning.

**bread_v4:** Worst opening-template repetition in the whole corpus (43.5% of products share their
first 3 words with another product) — the copy engine is visibly running one sentence template with
blanks filled in. Raw-number rate is moderate (56.5%) but the structural repetition is the dominant
defect here, distinct from brined-cheeses' recitation-first problem.

**snacks_v5:** 100% raw-number recitation, second-highest em-dash mean (2.62) in the corpus, and the
highest single em-dash-count product in the audit (max 4). No mechanic-vocab leakage and no template
sharing, so the defect is purely "numbers + dashes," not structural repetition.

**protein_combined_v2:** 100% raw-number recitation and moderate mechanic-vocab leakage (6.2%, second
worst after brined-cheeses) — some scoring vocabulary is bleeding through here too. 7 negation
constructions (tied-highest with brined-cheeses), suggesting "X not Y" antithesis is a live pattern
in this category's copy, not just brined-cheeses'.

**granola_v2:** High em-dash mean (2.36, third-worst) and 81.8% >1-em-dash rate, with 77.3% raw-number
recitation. No mechanic leakage. Reads mechanically dash-heavy but without the internal-vocabulary
problem — closer to a "too many dashes" fix than a full rewrite.

**cereals_v2 — GOLDEN REFERENCE:** Leads with a finding, lands an opinion, and only uses numbers when
they carry the argument — exactly the target voice. Zero mechanic-vocab leakage, zero negation
constructions, lowest opening-template overlap alongside chocolate_bars/hard_cheeses/milk/snacks.
Representative: *"95% מהמוצר הוא חיטה. הדגן הוא הסיפור כולו, ורשימת הרכיبים מסתיימת ב-4 פריטים וללא
תוספות מזון מיותרות."* — states the number once, in service of the point, then stops. This is the
bar every other category should be measured against, not the raw-number percentage.

**cookies_coffee_v2:** Largest category by far (117 products) with high em-dash overuse (82.9% >1)
and moderate recitation (54.7%); at this scale, even a moderate per-product defect rate compounds
into the largest absolute rework volume (242 em dashes total, most of any category).

**hummus_v5:** 100% raw-number recitation but the lowest em-dash->1 rate among the number-heavy
categories (50.9%) and only 5.3% mechanic leakage; the dominant defect here is recitation, not
dash-stacking or internal jargon.

**crackers_v1:** Cleanest mechanic profile (the one hit is a confirmed false positive) with moderate
em-dash and recitation rates; reads as a mid-tier "needs a polish pass" category rather than a
structural rewrite.

**cakes_hard_cookies_v1:** Second-largest category (62 products); moderate across all metrics with no
standout defect, similar profile to crackers but at 3x the volume — a bulk polish job.

**chocolate_bars_v1:** Lowest em-dash mean of the "high recitation" cluster (1.39) and zero
mechanic/template issues; 100% raw-number recitation is the single defect driving its score, worth
checking whether the numbers are argument-bearing (cereals-style) before assuming it needs a full rewrite.

**hard_cheeses_v4:** By far the cleanest em-dash profile in the corpus (0.68 mean, only 16.1% >1) and
the copy already leads with opinion in places ("ראש הטבלה, וברור למה") — closest structural cousin to
cereals despite 100% raw-number recitation, because (like cereals) many of those numbers are the
argument (protein/sodium comparisons that ARE the finding). One real score-leak needs fixing (see †).

**milk_v1:** Lowest badness score in the corpus — low em-dash mean (1.00), lowest max em-dash count
tied with hard_cheeses, moderate recitation (50.0%), zero mechanic leakage. Per existing memory
(`owner_milk_page_content_gold_standard`), milk is already the content quality bar — this audit is
consistent with that: mechanically it's the second-cleanest category after hard_cheeses.

## Recommended fan-out order (worst → best, with 1-line rationale)

Ranking blends composite badness with category size (rework volume) and known traffic prominence
where knowable from memory (`bari_canonical_reference_v1`: brined-cheeses = golden *structural*
reference and already the pilot; milk = content gold standard, deprioritize).

1. **brined_cheeses_v2** — already in flight as the Phase-1 pilot; worst composite score, validates
   the pilot choice was correct. No further action needed from this audit (tracked separately).
2. **cheese_v5** — second-worst composite (175.3), 100% recitation, near-total em-dash overuse (93.6%),
   AND the largest of the top-tier bad categories (47 products) — highest rework payoff after the pilot.
3. **cookies_coffee_v2** — mid-table composite but the largest category in the entire corpus (117
   products, 242 total em dashes) — fixing this alone removes more raw defect volume than any other
   single category; high implied traffic-prominence (cookies/coffee is a broad, high-search-volume shelf).
4. **chocolate_tablets_v1** — third-worst composite (165.9), heaviest em-dash mean in the corpus (2.29);
   needs a full read before scoping (representative line not hand-verified in this pass).
5. **hummus_v5** — large category (57 products), 100% recitation, tied-second-highest negation count;
   high implied traffic-prominence (hummus is a staple Israeli comparison shelf).
6. **snacks_v5** — 100% recitation + second-highest em-dash mean; per memory this category has had
   recent explanation-engine work (`bsip2_explanation_engine_v2`) so a copy pass completes that thread.
7. **juices_v3** — high recitation and em-dash overuse but smallest of the top-8 bad categories (17
   products) — lower absolute payoff, do after the bigger shelves above.
8. **bread_v4** — worst template-repetition in the corpus (43.5% shared openings) is a distinct defect
   pattern (structural, not just recitation) worth a dedicated look; moderate size (23 products).
9. **protein_combined_v2** — real mechanic-vocab leakage (6.2%, second only to the pilot) means some
   internal vocabulary needs deliberate scrubbing, not just a dash/recitation pass.
10. **granola_v2** — heavy em-dash use but otherwise clean (no mechanic leakage); smaller lift.
11. **cakes_hard_cookies_v1** — second-largest category (62 products) but no standout defect; bulk
    polish, schedule opportunistically alongside cookies_coffee_v2 (same rewrite pass, adjacent shelf).
12. **crackers_v1** — small, mid-table, no real mechanic leakage; low urgency.
13. **chocolate_bars_v1** — clean mechanically; verify whether its 100% recitation is cereals-style
    (numbers-as-argument) before assuming it needs work — may need only a light touch.
14. **cereals_v2 — GOLDEN REFERENCE, do not touch** except to confirm during QA that later categories
    are actually converging toward its voice; used as the sign-off bar for every other row.
15. **hard_cheeses_v4** — cleanest em-dash profile, opinion-first in places; only needs the single
    confirmed score-leak (†, "67 נקודות") scrubbed — smallest lift in the whole set besides milk.
16. **milk_v1** — lowest composite badness AND already the owner-designated content gold standard
    (`owner_milk_page_content_gold_standard`); skip or defer indefinitely, review only if the fan-out
    reaches the very end.

## OFF-ban compliance

No Open Food Facts references (`openfoodfacts`, `open food facts`, `off_`) found in any insightLine
or rowVerdict across all 16 categories. `off_references_found` is an empty array for every category
in `fanout_audit_metrics.json`.

## Caveats / known limitations of this audit

- The raw-number-recitation regex cannot distinguish argument-bearing numbers (cereals, and partly
  hard_cheeses) from recited-elsewhere numbers (brined-cheeses, cheese_v5). This is flagged wherever
  it materially changes the read (cereals, hard_cheeses, chocolate_bars).
- "X, not Y" negation counts are regex-approximate per the task's own instruction; not every hit was
  individually read for true antithesis vs benign "and not" phrasing.
- chocolate_tablets_v1's representative line was not hand-sampled in this pass (time-boxed); flagged
  explicitly above so the executor reads it before scoping.
- Traffic-prominence is inferred only from what's knowable in memory (golden/gold-standard
  designations, category type as broad staple vs niche); no actual analytics data was available to
  this lane.
