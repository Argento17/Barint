# P74 — Product D7 co-sign: `biscuit` router category (route: C1 / Product)

**Task:** TASK-275. **Lane:** C1 Product Agent — D7 co-sign on a ROUTING-ARCHITECTURE change (not a score
rule). Decide approve / reject / conditions. This gates ACCEPTANCE of the implementation (running in parallel).

## What you're co-signing
Add a dedicated `biscuit` category to the router (`router_v2.py` HARD_ANCHORS), so coffee biscuits stop
being mis-classified as snack-bars/crackers/bread. **Caps INTACT. No endemic relief. No scoring-rule change.
No context_flag.** The category only fixes semantically-wrong routing.

## The evidence (orchestrator-verified)
- run_cookies_001: A0 B0 C13 D15 E33 (E-modal). 25/61 genuinely bound by the category-agnostic 2-red-label
  cap (sugar>17.5 AND sat-fat>5) — honest. ~7–8 E grades are routing artifacts: snack_bar_granola-routed
  biscuits = 75% E vs cracker-routed = 40% E (same product class, wrong lens).
- Nutrition ruling: `02_products/cookies_coffee/methodology/cookies_coffee_routing_ruling_v1.md` (read it).
- C3 outside read (`tasks/returns/P72_return.md`): add the category for taxonomy ONLY, never to lift grades.
- Orchestrator pre-check: none of the 12 proposed keywords appear in any of the 14 live comparison JSONs
  (no published-product overlap).

## The questions for your D7
1. **Precedent / special-pleading risk:** is adding a `biscuit` router category a principled factory
   improvement (the router genuinely lacked a home for a real shelf — like brined_food was added for
   cheese), or grade-inflation special-pleading? Note caps stay intact and post-reroute ceiling is still C
   (no A, B only for 3–5 clean digestives) — scores are NOT being lifted into A/B wholesale.
2. **Scope discipline:** do the 12 keywords risk capturing products from OTHER categories (snack-bars,
   cereals, bread, crackers) and rerouting them — i.e. any published-score movement? (The hard gate is
   zero live movement; the pre-check is clean, but rule on the keyword breadth, esp. the broad `עוגיות`.)
3. **Is this the minimum necessary change?** Or is there a simpler fix than a new category?
4. **Conditions** you require before the implementation is accepted (e.g. specific exclusions, the exact
   no-regression proof, the rollback plan).

## Guards
- No code, no engine edits — this is a co-sign decision + EV-058 conditions. OFF ban. Frozen invariants
  untouchable (the zero-published-movement proof is mandatory regardless of your co-sign).

## Return
Deliverable: `02_products/cookies_coffee/methodology/cookies_coffee_d7_cosign_v1.md` (APPROVED / APPROVED-
WITH-CONDITIONS / REJECTED + reasons + conditions). End with the return contract: task=P74,
proposed_status=RETURNED, artifact (+sha256), the verdict, conditions list, not_done, self_check. Propose
RETURNED — do NOT close.
