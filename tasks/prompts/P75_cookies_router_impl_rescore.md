# P75 — Implement `biscuit` router category (EV-058) + re-score (run_cookies_002) (route: C1-CURSOR)

**Task:** TASK-275. **Lane:** C1-CURSOR — spec-complete engine change (router only) + no-regression proof +
re-score. **PROVISIONAL:** output is not accepted until Product D7 co-sign (P74) lands AND zero published
movement is proven. Spec = the Nutrition ruling.

## Read first
- `02_products/cookies_coffee/methodology/cookies_coffee_routing_ruling_v1.md` (§2 = exact keywords +
  mechanism; the authoritative spec for this task).
- How `brined_food` / EV-052 was wired (the precedent to mirror): `router_v2.py` HARD_ANCHORS (line 50),
  ANCHOR_EXCLUSIONS (179), CATEGORIES (26), `_check_anchors` (248); `evaluation_scope.py` 39-68.

## Implement (router ONLY — no cap changes, no scoring rule, no context_flag)
1. Add `biscuit` to `CATEGORIES` in `router_v2.py`.
2. Add the ruling's 12 Hebrew keywords to `HARD_ANCHORS` as `(term, "biscuit", subtype, confidence)`,
   with `ANCHOR_EXCLUSIONS` entries to prevent over-capture (e.g. exclude ממרח/spread, וופל/wafer,
   filled/coated terms, and anything that could pull a snack-bar/cereal/bread/cracker product).
3. Register **EV-058** in `03_operations/bsip2/proto_v0/src/.../bsip2_evidence_registry_v1.md` (scope,
   keywords, rollback = remove the anchors, no-regression plan). Mirror the EV-052 entry format.
4. **Do NOT touch any cap, weight, NOVA rule, or context_flag.** Routing taxonomy only.

## NO-REGRESSION PROOF — HARD GATE (STOP on any failure; this is tripwire-1)
Before reporting success, prove ZERO published-score movement:
- `engine_invariants.py` → **342 cases, 6/6 PASS** (paste verdict).
- Re-score a representative product from EACH live category (milk/yogurt/bread/cereals/granola/snack-bars/
  cheese-spreads + any others) and **diff score+grade vs the committed published trace** → must be
  byte/score identical. If ANY live product's category, score, or grade changes → **STOP, do not re-score
  cookies, report the regression.** (The orchestrator pre-checked: no cookie keyword appears in live JSONs;
  confirm that holds at the engine level.)
- Confirm the 12 anchors do not fire on any live-category product (the exclusions hold).

## Re-score cookies → run_cookies_002 (only after the no-regression gate passes)
- Re-run BSIP1→BSIP2 on the 61 IN_SCORED with the new router, same flag config as run_cookies_001
  (RECAL_P0 off, all brined/grad-sodium/shelf-relative off). Output:
  `02_products/cookies_coffee/bsip2_outputs/run_cookies_002/`.
- Report: new grade distribution, **routing tally (expect biscuit≈61)**, grade-by-category, score
  min/max/median/stdev, OFF 0/61, brined_food 0/61.
- **Reroute experiment verdict (the whole point):** vs run_cookies_001 — did the snack_bar_granola-distorted
  biscuits rationalize (move from E toward D/C consistent with cracker-routed peers)? Did the 25 genuine
  2-red-label products STAY E/D (they must — caps intact)? Report the before/after grade migration.

## Guards
- OFF ban absolute. No fabricated numbers. The no-regression gate is non-negotiable — a failed live-score
  diff means STOP, not proceed.

## Return
End with the return contract: task=P75, proposed_status=RETURNED, artifacts (router_v2.py + EV registry +
run_cookies_002 run_record, all +sha256), counts (new dist + routing tally + invariants + live-diff result
+ before/after migration), commands_run (exit codes), not_done, self_check. Propose RETURNED — do NOT close.
The orchestrator independently re-runs invariants + the live-diff before accepting.
