---
id: TASK-142A
title: "BSIP0 nutrition-parse data-integrity bug: trans-fat row captured as total fat (fat_g=0.5) + nutrition-panel bleed — root-cause, fix, blast-radius"
owner: data-agent
status: CLOSED
priority: CRITICAL
created_at: 2026-06-01
completed_at: 2026-06-02
depends_on: []
blocks: [TASK-142]
parent: TASK-142
category_id: cheese_spreads
summary: >
  The cheese Nutrition review (2026-06-01) found the Shufersal BSIP0 scraper records the TRANS-FAT row
  ("שומן טראנס פחות מ-0.5") as TOTAL fat -> fat_g=0.5 on 62/116 raw cheese products (incl. 18% cream cheese,
  5% white cheese). Fat feeds the score engine, so run_cheese_001/002 grades are INVALID. The scraper also
  BLEEDS the nutrition panel into ingredients_text_he ("...ערכים תזונתיים 100 גרם...גרם שומנים..."), which
  produces false sweetener / added-sugar / 'light' flags (EV-026 class). Root-cause, fix, and assess blast
  radius across categories that share the same nutrition parser before re-running cheese (run_cheese_003).
---

# TASK-142A — BSIP0 nutrition-parse data-integrity bug

CRITICAL. Spun off TASK-142 (blocks it). Discovered by the Nutrition Agent grade-publication review.

## The defect (confirmed)
- `03_operations/bsip0/scrape/shufersal_cheese/01_scrape_cheese.py` parses the `nutritionList` / `nutritionItem`
  divs and maps Hebrew labels via `NUTR_LABEL_MAP`. The map sends both `שומנים` and `שומן` -> `fat`, and a
  `שומן טראנס`/`מתוכו ... שומן` row also contains the substring `שומן` -> overwrites `fat` with the trans value
  `"פחות מ 0.5"` -> `fat_g = 0.5`. Confirmed: `fat_raw == "פחות מ 0.5"` on **62/116** raw products.
- Ingredient extraction bleeds the nutrition block into `ingredients_text_he`
  (e.g. `חלב, מלח מכיל חלב ערכים תזונתיים 100 גרם 98 קל ... 5 גרם שומנים ...`), so the enricher sees panel text
  and the `סוכר`/`כפיות סוכר` tokens fire false `extracted_sweeteners` (-> false A-ceiling C1 fail) and the
  trans `פחות מ-0.5` corrupts `light` math (`light_supported` nonsense; EV-026 class).

## Required work
1. **Root-cause** the nutritionList parse: why the trans/saturated sub-rows win over the total-fat row, and why
   the panel text bleeds into ingredients. Confirm whether the reliable source is the structured
   `ערכים תזונתיים ...` text block (`(\d+(?:\.\d+)?)\s*גרם\s*שומנים`) vs the div selector.
2. **Fix the parser** (in the shared scrape path): read TOTAL fat (`שומנים` / total-fat row), order label
   matching most-specific-first so `שומן טראנס` / `שומן רווי` never overwrite total fat, and isolate the
   nutrition block from `ingredients_text_he` (stop the bleed). Verify all macros (energy/protein/carbs/fat/
   sat-fat/sugar/sodium/fiber) parse correctly on a sample.
3. **Blast-radius assessment (do not skip):** the SAME `nutritionList`/`NUTR_LABEL_MAP` pattern is used by
   `shufersal_cereals/01_scrape_cereals.py` and the yogurt scraper. Audit run_cereals_002 and run_yogurt_003
   BSIP1 for `fat_g == 0.5` / trans-row capture and panel bleed. Report how many products/categories are
   affected and whether any frozen/live score is implicated (milk/bread/snacks used different/earlier paths —
   confirm). This determines whether the fix is cheese-only or a shared-scraper correction.
4. **QA guard:** add an implausibility sanity-check to the QA gate / BSIP0 composition gate (e.g. a cheese/
   dairy product with fat_g <= 0.5 but energy >= 120 kcal is implausible; trans-as-total detection), so this
   class of error fails the gate instead of passing "coverage >= 90%" (which counts presence, not correctness).
5. **Evidence registry:** log the fix + blast-radius under the EV-026 family (or a new EV) with rollback.

## Exit / DoD
Root cause documented; parser fixed and verified on a re-scraped sample (fat sane across pools); blast-radius
report delivered (cheese + cereals/yogurt audited, frozen/live status confirmed); QA implausibility guard added.
Hand back to TASK-142 for the cheese re-scrape -> re-build -> re-score (run_cheese_003) -> re-validate. Then
propose RETURNED (CC records CLOSED).

---

## RETURN BLOCK — proposed RETURNED (2026-06-02, data-agent)

**Root cause (confirmed).** The shared Shufersal `div.nutritionList` parser used `NUTR_LABEL_MAP`
with substring matching + break-on-first. It mapped BOTH `שומנים` (total fat) and `שומן` (a substring
of every "of which" sub-row — `שומן טראנס`, `חומצות שומן רוויות`) to `fat`. The panel lists total fat
first, then indented `מתוכו…` sub-rows; each sub-row label contains `שומן`, re-matched `שומן→fat`, and
**overwrote** total fat. The last fat-bearing row (trans, `פחות מ 0.5`) won → `fat_g=0.5`. Saturated fat
was **never** captured (generic `שומן→fat` preceded the specific `שומן רווי→saturated_fat` in dict order;
loop broke first) → 0% saturated capture in every nutritionList corpus (the universal signature). The
**Hebrew final-letter trap** (`שומן` final-ן ⊄ `שומנים` regular-נ) is why the legacy map carried both
forms and why a naive stem fix fails — the new parser normalizes final-forms. The reliable source is the
`div.nutritionList` selector (not the textblock regex); it was the *label matching*, not the source, that
was wrong.

**Fix (data-ingestion only; no scoring logic touched).** New single-source parser
`03_operations/bsip0/scrape/_shared/bsip0_nutrition.py` — `classify_nutr_label()` normalizes final-forms,
classifies most-specific-first (trans→saturated→…→generic fat LAST), and never lets an `מתוכו/מהם`
sub-row map to total fat; `parse_nutrition_list()` keeps first-per-field. All 5 Shufersal nutritionList
scrapers (cheese, cereals, yogurt, maadanim, hummus) now import it — closing the gap that let TASK-039's
hummus audit fail to stop re-propagation. Verified on **live re-scrape** (2026-06-02): גבינת עזים 32%
0.5→32 (sat 22); קוטג' 9% 0.5→9 (sat 5.4); שמנת לבישול 15% 0.5→15 (sat 9); גבינת שמנת 18% 0.5→22 (sat 14.3).
Unit tests + corpus-gate tests pass.

**Blast radius.**
| Category | Path | Raw fat=0.5 | Sat captured | Status |
|---|---|---|---|---|
| cheese run_cheese_001/002 | nutritionList | 62/116 | 0% | NON-AUTHORITATIVE (NO-GO) — invalid, re-scrape |
| cereals run_cereals_002 | nutritionList | 75/113 | 0% | NON-AUTHORITATIVE (NO-GO) — fat_quality 92/92 dead |
| yogurt run_yogurt_003 | nutritionList | 47/97 (scored 45/88) | 0% | **AFFECTED — see TASK-143 verdict** |
| **maadanim (LIVE)** | nutritionList | 88/200 | 0% | **LIVE & AFFECTED** — needs re-scrape+re-score (separate task) |
| **hummus (LIVE)** | nutritionList | 59/69 (TASK-039) | n/a | **LIVE & AFFECTED** — max fat 5.9g; needs re-scrape+re-score |
| milk (frozen run_004) | Playwright tab-capture | — | — | **NOT affected** (different path) ✓ |
| bread (frozen retail_003) | proto_v0 scrape | — | no sat field | **NOT affected** (different path) ✓ |
| snacks | separate path | — | — | **NOT affected** ✓ |

Propagation into scoring confirmed: across affected runs `fat_quality` is **uniformly neutralized to 50**
("sat_fat absent → neutral 50") — the dimension is dead, suppressing real signal (weight 0.08; also feeds
`fat_pct_of_kcal`, `hp_fat_*`).

**TASK-143 verdict (explicit).** **run_yogurt_003 is AFFECTED, NOT clean.** The yogurt LIVE swap must wait
for a clean re-scrape (run_yogurt_004) + re-score. **TASK-143 stays BLOCKED on TASK-142A's downstream
re-score, not on the parser fix itself** (parser is now fixed).

**QA guard added.** `COV-006 Nutrition plausibility` in `03_operations/qa/run_qa.py` (hard-fail ≥5%
implausible) + scraper `main()` composition-gate Plausibility line (fail ≥5%) + shared
`nutrition_implausible()` / `composition_nutrition_report()`. Catches `saturated_fat>fat` and `fat≤0.5`
with energy ≥50 kcal above macro-implied energy; legit low-fat high-carb foods (cereal flakes) pass.
Verified: old broken cheese corpus 31.9% → FAIL; corrected sample → PASS.

**Evidence registry.** Logged as **EV-029** (EV-026 data-hygiene family) in
`03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`, with mechanism, propagation,
frozen/live status, TASK-143 verdict, QA guard, and rollback.

**Hand-back to TASK-142.** Parser is fixed and verified. TASK-142 can now run cheese re-scrape → re-build
→ re-score (run_cheese_003) on corrected fat/saturated data.

**Recommended follow-ups (NOT done here — separate tasks, owner sign-off needed):**
1. TASK-142 → run_cheese_003 on corrected data.
2. **New task: re-scrape + re-score LIVE maadanim** (88/200 fat collapsed; latent grade impact) — Product sign-off.
3. **New task: re-scrape + re-score LIVE hummus** (59/69; max fat 5.9g) — Product sign-off.
4. TASK-143: gate the yogurt swap on run_yogurt_004 (clean re-scrape).

**Proposed state: RETURNED.** Central Controller to record CLOSED.

**Files changed:** `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py` (new);
`shufersal_cheese/01_scrape_cheese.py`, `shufersal_cereals/01_scrape_cereals.py`,
`shufersal_yogurt/01_scrape_yogurt.py`, `shufersal_maadanim/01_scrape_maadanim.py`,
`shufersal_hummus/02_scrape_hummus_shufersal.py` (wired to shared parser); `03_operations/qa/run_qa.py`
(COV-006); evidence registry (EV-029). No scoring logic, no published scores, no frozen data modified.
