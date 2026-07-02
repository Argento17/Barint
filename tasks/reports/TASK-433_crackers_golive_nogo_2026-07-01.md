# TASK-433 — Crackers go-live (2026-07-01)

## ✅ RESOLVED → QA re-verify = GO (2026-07-01, after rework loop)
- **Set: 19 displayable** (was 20; 7290112968807 dropped as insufficient_data per discard rule + precedent).
- **Both gates green (orchestrator-independent + QA-independent):** run_gates.py Overall PASS; validate_comparison_page.py exit 0, 7/7 (ingredient-sanity + superlative rank_check now PASS).
- **Two-gate content rule satisfied:** Content (gate 1) + Adversarial QA re-verify GO (gate 2).
- **Data fixes at source (reproducible):** ingredient bleed (20→0), sodium thousands-separator parser bug (1.2→1200mg, now true ceiling), sugar extraction (2 real / 17 honest-null). Parser fix was in shared parse_num() → benefits other categories.
- **Copy fixes (10):** false sodium ceiling, KRIT glucose-syrup FABRICATION removed, row-1 false protein/fiber superlative, weakest-profile reframe, caveat calorie overstatement, Swedish-rye promise, intent-editorializing, scoring-causality, nameHe abbrev. Superlatives independently recomputed true (1200 ceiling / 754 2nd / protein tie@16 / fiber top@10.5 / energy ceiling@519). 74252 "3 sugar sources" verified GENUINE in scrape.
- **Remaining before actual launch:** (a) featured card on /hashvaot/supermarket + themes/crackers.jpg (OWNER ASSET); (b) optional Playwright/axe render pass. RT-7 stale comment fixed.
- **Owner call pending:** category go-live = tripwire #2.

---
## Original NO-GO record (below, for audit)

# TASK-433 — Crackers go-live: NO-GO consolidated findings (2026-07-01)

Orchestrator-driven build toward crackers consumer go-live (tripwire #2). Two independent gates + a mechanical sweep returned **NO-GO**. This file is the durable record of the verified findings + the rework routing. No tripwire fires (crackers NOT yet published — correcting not-yet-live data/scores is normal pipeline work).

## Gate results
- **C0 run_gates.py**: crackers Overall PASS (G1 schema fixed via nameHe/_hash_no_rank whitelist; G4 OFF, G6 copy-safety, G8 data-sanity PASS). bread_frontend_v4 Overall PASS incl. G7 PARITY (byte-identical 29→23).
- **C0 validate_comparison_page.py**: **FAIL 6/7** — ingredient-sanity fails on 19/20 (this is the second mandatory gate; run_gates alone is NOT sufficient — see [[run_both_page_gates]]).
- **C2 (DeepSeek) P453 leakage sweep**: CLEAN — 0 OFF, 0 framework-leak in consumer copy, 0 grade-tail, 0 token-leak. (13 "נמוך" instances = legitimate comparatives.)
- **Adversarial QA (native, Opus-independence)**: NO-GO.
- **C3 (gpt-5.5) P454 red-team**: NO-GO, corroborates + extends.

## Verified findings → rework routing
### DATA lane (regenerates JSON; dispatched a76ade8109b2f2d18)
- **RT-1 (CRIT)**: ingredient bleed/truncation 19/20 — root cause = BSIP1 `ingredients_text_he` attribute bleed cut mid-clause (orchestrator-traced: source-level, not display). Clean at source, reproducible rule, no invention.
- **RT-4 / C3-2 (HIGH)**: implausible sodium — 7290018790328 ("salted") = 1.2mg vs "מלח (3%)"; 7290112968807 = 86mg + implausible full nutrition. Verify source, fix unit/parse, re-score (may move grade/rank).
- **RT-2 extraction (CRIT enabler)**: sugar null 20/20 though present in raw text (≥ 5000396021202 8.5g). Extract to structured field where real; null where absent.

### CONTENT lane (after Data regen; will resume a49206ba42e85e6aa)
- **C3-1 (CRIT — fabrication)**: KRIT 8434165658523 copy claims "סירופ גלוקוזה"/"three sugar sources" NOT in ingredients (white sugar + barley-malt only). Remove invented source; verify ALL sugar-source claims vs scrape.
- **RT-3 / C3-4 (HIGH)**: row 1 96086000966 "protein+fiber higher than every other" FALSE (protein tied w/ 96086000577 @16g; fiber beaten by 7290013740823 @10.5 & 6). Also "הכי פשוט במדף" false. → "מהגבוהים"/"מהפשוטים".
- **RT-2 / C3-5 (HIGH)**: row 20 5000396021202 sugar superlative unsupported until extraction; "weakest nutritional profile" wrong (it's lowest OVERALL score, not weakest nutrient_density). Tie to overall score/rank.
- **C3-3 (HIGH)**: _meta.categoryCaveat overstates — says calories "אינן נזקפות לחובה" but calorie_density penalties exist (score 35 rows). Reframe: crackers-vs-crackers, calorie-density still a within-category signal.
- **C3-6 (HIGH)**: 7296073134459 "Swedish-style promises whole rye" not traceable → factual reframe.
- **C3-7 (MED)**: intent claims ("beet powder FOR color", "leans on color over grain") — factual ingredient placement, drop intent.
- **C3-8 (MED)**: 96086000577 "only because missing seeds" exposes scoring causality → factual comparison.
- **C3-9 / QA (MED)**: 7290013740083 nameHe expanded ללת"ס→ללא תוספת סוכר — document source or preserve abbreviation.
- Re-verify ALL superlatives vs regenerated corpus numbers.

## Sequence
Data (regen + stale-copy manifest + both gates) → Content (copy fixes on regen) → orchestrator re-run BOTH gates → Adversarial QA re-verify → owner go/no-go.

## Also open (non-blocking for the gate, needed for launch)
- Crackers **featured card** on /hashvaot/supermarket (Design spec + stats copy + themes/crackers.jpg stock image — likely owner-supplied asset). Category is registry-auto-onboarded to /catalog but NOT discoverable from the supermarket index without the card.
- bread↔crackers copy inconsistency: bread v4 rowVerdicts carry "ציון S." grade-letter tails (pre-existing live copy, preserved byte-identically); crackers strip tails. Not a crackers blocker; do not touch live bread copy without owner.
