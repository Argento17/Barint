---
name: cereals_contamination_ev045_granola_split
description: TASK-140 cereals shipped ~26 non-cereals/bad-data (28% of batch) incl a pasta at
metadata: 
  node_type: memory
  type: project
  originSessionId: d29e433a-294b-4cb5-a1e5-440f50c7dac6
---

**Incident (owner QA, 2026-06-05):** the breakfast-cereals batch (run_cereals_004) that shipped live
was badly contaminated — a full shelf audit found **~26 of the original 92 displayable products were
non-cereals or bad data (≈28%)**. The corpus filter was a pure name-substring include with no
ingredient/semantic check, and contamination was misdiagnosed as a SCORING problem (EV-044/EV-010
lowered grades) instead of a corpus problem. Found in two QA passes:
- **Pass 1 (EV-045):** 10 Israeli **ptitim pasta** (`פתיתים אפויים [shape]` + organic spelt
  `פתיתים אורגנים כוסמין`, whitelisted to **A and ranked #1**) + 3 yeast **breads** (`כוסמין מלא 100%`,
  `חלה`, `פיטנס THIN`).
- **Pass 2 (EV-045b, after owner pushed back "QA was weak"):** 2 **pasta** (`פסטה...נודלס/פטוצ'יני`
  konjac), 1 **flour** (`קמח שיבולת שועל`), 6 **chocolate confections** (קליק×2, מיקס כרמית, ציפוי
  לבן, שוקולד+פצפוצי אורז, קראנץ' מיני), 1 **oat drink** (`שיבולת שועל וויט`, 59 kcal), 3
  **implausible-energy** items (110–139 kcal/100g for a dry cereal = per-serving parse error → withheld).
- Plus the original 12 `no_usable_nutrition`.

**Fix (`02_build_bsip1_cereals.py` curate + scraper):** multi-signal contaminant sweep — pasta tokens;
flour-as-product (name HEAD `קמח`); chocolate confection (choc as head/first-ingredient/≥50%/coating
/sugar+cocoa-butter, vs. legit choc-FLAVOURED grain cereal which lists grain first); drink tokens;
**dry-cereal energy floor 150 kcal/100g** (wet/parse-error gate); ptitim head-noun `פתיתים` vs.
construct `פתיתי X`; bread yeast/sourdough. **Hebrew word-boundary critical:** yeast `שמרים` ⊂
preservatives `משמרים` ("ללא חומרים משמרים"=NO preservatives) falsely dropped Nesquik/Cini Minis/Lion
(EV-029 substring-trap family).

**Re-run `run_cereals_005`** (engine byte-identical): 113 raw → **66 displayable**; **survivor score
drift = 0** (scoring is corpus-independent — fixed per-category PROTEIN_SCALE_TABLES + fixed grade
thresholds; proven empirically). Scripts `batch_run_cereals_005.py` + `split_cereals_005_frontend.py`
(idempotent; regression + GATE-2 + authored-copy asserts).

**Categories now (live, `next build` PASS):**
- **דגני בוקר** `/hashvaot/breakfast-cereals` — **31** products, **NO A** (top שיבולת שועל עבה 80/B),
  B9/C17/D5. `cereals_frontend_v1.json` v2.
- **גרנולה ומוזלי** `/hashvaot/granola` — NEW category, **35** (25 granola + 10 muesli/grain-mix; muesli
  folded in as same architectural family), top גרנולה ממותקת בסילאן 76/B, 35-pt span, B7/C16/D12.
  `granola_frontend_v1.json` v1 + full route/page-data/shelf-filters/featured-card/registry+types entry.
- All hand-authored Hebrew rowVerdict/insightLine **preserved** by PARTITIONING the authored corpus.

**3 hard gates** — `01_framework/operations/corpus_purity_gates_v1.md` (wired into `category_factory_v1.md`):
(1) **contamination ≠ calibration** — wrong-food product EXCLUDED at curation, never re-graded;
(2) **leaderboard integrity** — `nutrition_approved=false` never at/above an approved product or #1;
promotion ABORTS; (3) **first-batch owner consult** — first batch after any BSIP0/corpus-filter/calibration
change is owner-gated before live (consumer-facing-irreversible tripwire; see [[decision_authority_matrix]]).

**Meta-lessons:** (a) the CC close gate verified misroute/coverage/constructs (all true) but never asked
"are these products actually the category food?" — add a name+ingredient food-class check + an
energy-plausibility check to the close gate for any category launch. (b) Name-substring filters are
insufficient; require name-head + ingredient-dominance + nutrition-plausibility. Supersedes
[[bsip2_run_cereals_002]] live state.
