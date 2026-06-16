# P75b — Fix `biscuit` anchor coverage + C2 exclusions, re-score run_cookies_003 (route: C1-CURSOR)

**Task:** TASK-275. **Lane:** C1-CURSOR. This is the ONE in-lane retry of P75. P75 wired EV-058 but only
7/61 cookies matched the anchors (spelling + generic names) and missed Product condition C2. Fix the
coverage faithfully to the EXISTING Nutrition ruling §1.2 scope + Product P74 conditions. No scope change,
no cap change.

## Context (verified by orchestrator)
- EV-058 is no-regression-clean (engine_invariants 342 6/6 PASS; 0 bleed on live corpora; milk/cereals
  byte-identical). The cheese/brined/yogurt baseline drift is PRE-EXISTING branch state, NOT EV-058 — ignore it.
- Coverage bug: anchors used `פטי בר` (tet ט) but corpus uses **`פתי בר` (tav ת)**; 54 products are named
  generically `עוגיות …` with no matching anchor; the `בטעם` exclusion over-blocks legit flavored biscuits.

## Fixes to `router_v2.py` HARD_ANCHORS / ANCHOR_EXCLUSIONS (router only — no caps, no signals, no scoring)
1. **Spelling variants** — add both tav-spellings as biscuit anchors: `פתי בר` and `פתי-בר`
   (keep the existing tet `פטי בר`/`פטי-בר`). Also add `פתיבר`/`פטיבר` (no-space) variants.
2. **Generic cookies** — add bare **`עוגיות`** as a biscuit anchor (confidence ~0.85, AFTER the more
   specific anchors so subtypes win). This catches the 54 generically-named in-scope cookies. MUST carry
   robust `ANCHOR_EXCLUSIONS` to prevent global bleed:
   `["אורז","גרנולה","דגנים","מוזלי","מוסלי","חטיף","ברים","ממרח","וופל","קרקר","פריכיות","ציפוי","מילוי","קרם","שכבת","אנרגיה","חלבון"]`
   (block rice-cakes, granola/cereal, bars, spreads, wafers, crackers, filled/coated, protein/energy).
3. **C2 (Product condition, non-waivable)** — add `גרנולה` and `דגנים` to the `עוגיות חמאה` exclusion list.
4. **`בטעם` over-block** — REMOVE `בטעם` from the `ביסקוויט`/`לוטוס` exclusion lists (a flavored plain
   biscuit "ביסקוויט בטעם X" is in scope; keep `מילוי/ציפוי/קרם/שכבת/מצופה` which denote filling/coating).

## NO-REGRESSION GATE — HARD, non-waivable (Product C1; STOP on any failure)
- `engine_invariants.py` → 342, 6/6 PASS.
- **Bleed simulation (the critical one given bare `עוגיות`):** run the 13+ biscuit anchors against EVERY
  live category BSIP1 corpus (milk, yogurt, bread, cereals, granola, snack-bars, cheese-spreads, hard-
  cheeses, brined, hummus, salty-snacks, juices) — **must be 0 hits**. If bare `עוגיות` (or any term) fires
  on a live product → STOP, report the product, do NOT proceed (tripwire-1).
- Re-score one product per live category, diff score+grade+category vs committed baseline traces; the ONLY
  acceptable changes are zero. (Pre-existing branch drift is separate — diff against the SAME branch engine
  WITHOUT the biscuit anchors to isolate EV-058's delta = must be 0 for non-cookie products.)

## Re-score → run_cookies_003 (after the gate passes)
- Same flag config as run_cookies_001/002 (RECAL_P0 off, all brined/grad/shelf flags off).
  Output: `02_products/cookies_coffee/bsip2_outputs/run_cookies_003/`.
- Report: **routing tally (expect biscuit ≈ 55–61)**, grade distribution, score min/max/median/stdev,
  OFF 0/61, brined_food 0/61.
- **Product condition C3 (non-waivable): the distribution MUST show B ≤ 8 AND A = 0.** If breached → STOP + escalate.
- **Reroute verdict:** vs run_cookies_001 — how many products rationalized (snack_bar/cracker → biscuit),
  the grade migration, and confirm the 25 genuine 2-red-label products STAYED E/D (caps intact).

## Guards
- OFF ban absolute. No cap/weight/NOVA/flag changes — routing taxonomy only. No fabricated numbers.
- The bleed-sim is the tripwire-1 gate — a single live-product hit means STOP, not proceed.

## Return
End with the return contract: task=P75b, proposed_status=RETURNED, artifacts (router_v2.py + EV registry +
run_cookies_003 run_record + bleed-sim report, all +sha256), counts (routing tally, dist, invariants, bleed
hits [MUST be 0], B-count, A-count, reroute migration), commands_run (exit codes), not_done, self_check.
Propose RETURNED — do NOT close. Orchestrator independently re-runs invariants + bleed check + B≤8/A=0.
