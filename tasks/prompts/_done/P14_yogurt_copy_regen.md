P14 / TASK-256 — Yogurts full copy regeneration (Content Agent). This is the
launch copy for Bari's FIRST S-tier category. Produce a DRAFT json (not written
into the live data) that the orchestrator then runs through the claim gate.

=== WHY THIS IS A REGEN, NOT A TWEAK ===
The page was rebuilt as `yogurts_frontend_v4.json` (17 products, Shufersal-only,
run_yogurt_006_shipcfg2). ALL string fields are PENDING_P14 — carry over NOTHING
from the old v3 strings. CRITICAL: the OLD page copy declared "אף אחד לא מגיע
ל-S / 'הכי טוב' הוא A — אבל לא S". That is now FALSE — TWO products scored S.
The page-level copy must be rewritten to lead with the S story.

=== SOURCES (read before writing) ===
- Data + nutrition + ingredients per product: `bari-web/src/data/comparisons/yogurts_frontend_v4.json`
  (every product's `expansion.nutrition` + `expansion.ingredients` are the ONLY
  numeric source — quote nothing not present there; missing = omit, never invent, no OFF).
- Real grade driver per product: each product's shipcfg2 trace
  `02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg2/products/products/bsip1_yogurt_<barcode>/bsip2_trace.json`
  (`explanation_drivers`, `binding_cap`, `caps_applied`). Driver spine below.
- The two S explanations + the shared S caveat: `02_products/yogurt_system/s_grade_explanations_v1.md`
  — Nutrition-APPROVED. Use the Hebrew insight lines + S paragraphs VERBATIM; do NOT re-author them.
- Editorial law (memories): `bari_editorial_intelligence_v1` (insight-first, framework
  invisible), `bari_assertive_writing_v1` (finding-first, no-apology), `bari_insight_line_spec_v1`,
  `comparison_row_verdict_model`, `verdict_calories_sodium_standard`, `bari_score_presentation_v1`,
  `bari_category_caveat_standard`.

=== FIELDS TO AUTHOR (per product, 17×) ===
`insightLine` · `expansion.confidenceLabel` · `expansion.positiveSignals[]` ·
`expansion.limitingFactors[]` · `confidence_label_he` · `confidence_tooltip_he` ·
`confidence_sub_reason`. (Yogurts have NO rowVerdict field.)

=== PAGE-LEVEL STRINGS (regenerate, S-aware) ===
`hero_eyebrow` · `hero_title` · `prologue_1..4` · `methodology_1..4` · `category_note`.
- Lead the prologue with S=2 (the two דנונה PRO plain), then the A tier, then the
  fall through B/C/D as flavor/additives/crunch get added.
- `category_note` MUST include three blocks: (a) the "same label, two ends" caveat
  (protein number on front ≠ the score); (b) the shared S caveat — paste VERBATIM
  from s_grade_explanations_v1.md §"SHARED METHODOLOGY NOTE"; (c) the fiber caveat
  (dairy rarely lists dietary fiber, so it's excluded from this category's analysis).

=== DRIVER SPINE (name the REAL driver; ground every grade claim here) ===
S 92.6  7290112336712 דנונה פרו 21 חלבון 0% — no cap; S = clean across all dims. USE VERBATIM S copy.
S 90.6  7290110565527 דנונה PRO 20 גרם חלבון — no cap; S, 1.5g fat / 10g protein vs the 21. USE VERBATIM S copy.
A 89.9  7290110321031 יופלה GO מועשר בחלבון — no cap; held just under S by protein_quality (63.8 lowest dim).
A 84.8  7290114311069 מולר אקטיב לבן 0% 25 חלבון — no cap; processing_quality (64) is the lowest dim.
B 79.7  7290014758100 יוגורט ביו תנובה 3% — no cap; near-A, limited by protein_quality (31.7 lowest dim).
B 78.4  7290014758117 יוגורט ביו תנובה 1.5% — *** cap=94.8 but score 78.4 BELOW cap → cap did NOT bind. Do NOT say "capped". Real limiter = dimensions (lean base, moderate protein). ***
B 77.8  7290110328221 יוגורט נטול לקטוז 3% — *** same: cap 94.8 did NOT bind. Name the dimension story, not a cap. ***
B 76.6  7290107936309 יוגורט בסגנון יווני 6.5% — no cap; nutrient_density (38.8 lowest) — fat-rich but protein/density modest.
B 75.5  7290014890589 יוגורט יווני 8% — no cap; nutrient_density (42.5). High fat does NOT raise the score.
B 75.3  7290012645297 יוגורט עיזים ביו — no cap; nutrient_density (24.5 lowest) — lower protein is why it trails the plain cow bases.
B 72   7290112330352 דנונה PRO 20 וניל 0% — cap=72 BINDS (ADDITIVE_MARKERS_3_PLUS + NOVA3). Story: same brand as the S plain, but the vanilla version's additives are the whole gap.
C 64   7290116934402 יוגורט אוורירי GO מנגו — cap=68 BINDS (NOVA4 ultra-processed + additives).
C 62   7290110328764 יוגורט GO קרמי תות — cap=68 BINDS (NOVA4 + additives).
C 57.7 7290110321680 יופלה GO תות — cap=68 BINDS (NOVA4 + additives) + penalty LONG_INGREDIENT_LIST.
C 55   7290102394081 מולר מיקס קורנפלקס מצופה — cap=68 BINDS (NOVA4 + additives); cornflake topping = ultra-processed.
D 49.9 7290102399819 מולר פרוטאין יוגורט פירות יער — cap=68 BINDS + penalties MULTIPLE_ADDED_SUGAR_MARKERS, LONG_INGREDIENT_LIST.
D 36.3 7290010471669 יוגורט קראנצ תות קורנפלקס — cap=60 BINDS (NOVA4 + ADDITIVE_MARKERS_5_PLUS) + sugar/long-list penalties. The most processed on the page.

=== HARD CLAIM-GATE CONSTRAINTS (the draft must pass these) ===
1. Grade letter in any prose = the product's badge grade exactly (ב/ג/ד = B/C/D).
2. Sodium is a DISPLAYED FACT only — never a grade cause. Same for "high fat": fat
   does not lower these scores; never imply it does (Greek 8% is B on density, not a fat penalty).
3. No prior-run / "הציון הקודם" / version references (T4 banned).
4. Per `verdict_calories_sodium_standard`: where relevant name calorie density + the
   REAL fired driver. For capped products the driver = the binding cap's rule family
   (ultra-processing / additives / added-sugar). For uncapped, the lowest dimension.
5. Where binding_cap > score (the two flagged B's) the cap did NOT bind — do not claim it did.
6. Every number traces to v4 `expansion.nutrition`/`ingredients`. No invented figures. No OFF.
7. Honest-S framing: S is a structural finding (2 of 87), never "a ceiling we allowed."
8. The two S products use the Nutrition-approved Hebrew verbatim — do not paraphrase.

=== OUTPUT ===
Write `02_products/yogurt_system/yogurts_copy_regen_draft_v1.json` in the same shape
as the cereals remediation draft (per-product: barcode, name, badge{score,grade},
the authored string fields, and a `trace_drivers_cited` list naming the real driver).
Plus a `page_strings` block. Do NOT edit yogurts_frontend_v4.json or any live file.

RETURN BLOCK: draft path; confirm 17 products + page_strings authored; confirm the
2 S products use verbatim approved copy; confirm the 2 cap-didn't-bind B's avoid
cap language; list any product where the real driver was unclear. Propose RETURNED.
(Orchestrator then repoints the claims builder to v4 and runs the claim gate.)

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and put an `x` in the
P14 line under 📬 Signals.
