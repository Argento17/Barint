# Product Agent D7 Co-sign: `biscuit` Router Category (EV-058)

**Task:** TASK-275 (P74 — Product Agent D7 co-sign on routing architecture)
**Date:** 2026-06-13
**Author:** Product Agent
**Verdict: APPROVED-WITH-CONDITIONS**
**Status:** RETURNED — conditions must be met by implementing agent before any code ships

---

## Verdict

**APPROVED-WITH-CONDITIONS.**

The `biscuit` router category addition (EV-058) is a principled factory fix, not grade
inflation. It is approved to proceed to implementation once the four conditions in §4 are
satisfied. No code ships until all four conditions are met and documented.

---

## §1. Precedent / Special-Pleading Risk

**Finding: Principled factory fix. Not special pleading.**

The brined_food precedent (EV-052) established the correct test: does the router lack a home
for a real, coherent, commercially distinct shelf — or is this a post-hoc reroute designed
to make bad scores look better?

Coffee biscuits / plain sweet biscuits are a real shelf. They are bought as a distinct
consumer category (cookies near the coffee aisle). The router has no current home for them.
Without `biscuit`, products scatter to `snack_bar_granola` (20/61), `cracker` (27/61),
`bread` (7/61), and `default`/`cereal`/`dairy_protein` (7/61) — four different lenses for
the same product class. This is a genuine routing gap, not a marginal case.

The special-pleading test is: would a reasonable person, seeing the post-reroute distribution,
say grades improved because the reroute removed legitimate penalties? The answer here is no.
The Nutrition Agent ruling confirms the post-reroute ceiling stays at C. A moves to 0 (already
0). B goes to 3–5 products (up from 0) — those are digestives with genuinely lower sugar/fat.
The 7–8 products that move from E to D do so because the snack_bar_granola lens was applying
sub-rules calibrated for bar formats to plain biscuits. Removing an irrelevant sub-rule penalty
is a correction, not relief.

The category-agnostic caps — ISRAELI_RED_LABELS_2_PLUS (sugar >17.5g AND sat-fat >5g → floor
45), ISRAELI_RED_LABEL_1_SAT_FAT, ISRAELI_RED_LABEL_1_SUGAR — fire identically on the biscuit
path. 25/61 products remain capped at 45 after rerouting. The honest E-modal finding is
preserved.

**Special-pleading rejected. This is the same class of fix as brined_food.**

---

## §2. Keyword Scope Discipline

**Finding: Keyword list is tight. One term requires a condition.**

The 12 proposed hard anchors are evaluated against the live corpora:

| Keyword | Risk of live-corpus bleed | Assessment |
|---|---|---|
| ביסקוויט | MODERATE — generic term; appears as component word (e.g., "ציפוי ביסקוויט") | Exclusions proposed cover this; requires validation |
| פטי-בר / פטי בר | Low — brand-specific term | Clean |
| לוטוס | Low-moderate — brand name; appears in dessert/gelato contexts | Exclusions (בטעם, מילוי, ציפוי, גלידה) address it |
| ביסקוויט בלגי | Low — compound; sufficiently specific | Clean |
| ביסקוויט תה | Low — compound | Clean |
| מרי ביסקוויט / ביסקוויט מרי | Low — Marie biscuit specific | Clean |
| דייג'סטיב | Low-moderate — "digestive" appears in health/supplement contexts | Exclusions (חטיף, ציפוי) address it |
| ביסקוטי | Low | Clean |
| שורטברד | Low | Clean |
| עוגיות חמאה | MODERATE — "עוגיות" is a broad term | See condition C2 below |

The orchestrator's pre-check confirmed zero live-corpus keyword overlap across 14 published
comparison JSONs. That is necessary but not sufficient for the broad terms. The issue is not
current overlap but future pipeline contamination: if a snack-bar or cereal product with
"עוגיות" in its name enters a live corpus later, it would route to `biscuit` unless blocked.

**Condition C2** addresses this: `עוגיות חמאה` must carry explicit exclusions blocking חטיף,
גרנולה, and דגנים as component words. Additionally, the no-regression proof (condition C1)
must include a keyword-bleed simulation — run each of the 12 anchors against the current
registered corpus of all 7 live categories, verify zero hits.

The `ביסקוויט` exclusion list proposed by Nutrition (`מילוי, שכבת, ציפוי, קרם, טחינה, בטעם,
גבינה, שוקולד ביסקוויט`) is adequate. The `לוטוס` exclusions are adequate.

**The list is approvable. Conditions C1 and C2 make it safe to ship.**

---

## §3. Minimum Necessary Change

**Finding: Yes, this is the minimum necessary change.**

Three alternatives were considered and rejected:

**Alternative A: Do nothing, live with routing scatter.**
Rejected. A 35-percentage-point E-rate difference between `snack_bar_granola` and `cracker`
lenses on the same product class (75% vs 40% E) means the rank ordering within the category
is unreliable for 20 misrouted products. A comparison page built on unreliable rank ordering
is not shippable. The router gap must be fixed.

**Alternative B: Force all coffee biscuits to `cracker` without a new category.**
Rejected. `cracker` is the wrong archetype — it applies savoury-cracker signals and does not
capture the compositional profile of sweet biscuits. It would reduce the routing artifact (40%
E vs 75% E) but would not produce semantically correct rationale. This is a smaller fix that
still produces incoherent explainability.

**Alternative C: Add a `context_limited` flag with serving-size or sodium adjustment (EV-052
style).**
Rejected. Nutrition Agent confirmed: coffee biscuits do not require endemic relief. Sodium
is not the binding constraint. No serving-size re-weighting is warranted. Adding a
`context_limited` entry would be overbuilding — it adds complexity without user value.

EV-058 as proposed — vocabulary addition to `HARD_ANCHORS` and `ANCHOR_EXCLUSIONS`, new entry
in `CATEGORIES` and `ALL_SIGNALS` with empty signal list — is the minimum necessary change. It
fixes the routing gap without touching any cap, signal weight, or context flag.

---

## §4. Conditions Before Implementation is Accepted

Four conditions. All four must be met. None are waivable.

**C1 — No-regression proof (mandatory, blocks implementation).**
Before any code ships:
- Run `engine_invariants.py` 342-case suite. Must pass with zero new failures.
- Run golden-corpus byte-identity check on all 7 live categories (milk, yogurts, breads,
  salty_snacks, cereals, snack_bars, brined_cheeses). Every product's score and grade must be
  byte-identical to the pre-EV-058 baseline. Zero exceptions.
- Run each of the 12 proposed keywords against the full registered corpus of all 7 live
  categories. Zero hits. Document the result.
- STOP condition: any published-score movement = immediate rollback. Zero-movement is a
  non-negotiable requirement for this routing change. This is tripwire-1; it reaches the owner.

**C2 — עוגיות חמאה exclusion hardening.**
Add `חטיף`, `גרנולה`, `דגנים` to the `עוגיות חמאה` `ANCHOR_EXCLUSIONS` entry before
shipment. The currently proposed exclusions (ממולא, שוקולד, ציפוי, מצופה, חטיף) already
include `חטיף`, so only `גרנולה` and `דגנים` need to be added. Confirm the final exclusion
list in the implementation PR.

**C3 — run_cookies_002 post-reroute score run.**
After EV-058 is implemented, run the full 61-product corpus through the engine with the new
`biscuit` routing. Publish the resulting grade distribution in the task record. The Nutrition
Agent ruling predicts: E ~25–26, D ~20–22, C ~12–13, B ~3–5, A ~0. If the actual post-reroute
distribution shows B > 8 products or any A grades, STOP — escalate to Product Agent before
proceeding to frontend. The predicted ceiling (C category, B for best-in-class digestives)
must hold.

**C4 — EV-058 formal registration.**
EV-058 must be registered in `bsip2_evidence_registry_v1.md` before any frontend packaging
begins. The draft EV entry in `cookies_coffee_routing_ruling_v1.md` §5 is the template.
Registration requires citing this co-sign document and the Nutrition Agent ruling as the dual
approval basis.

---

## §5. Decision Log

| Field | Value |
|---|---|
| Options considered | (A) Do nothing; (B) Force-route to cracker; (C) Add context_limited flag; (D) Add dedicated biscuit category via HARD_ANCHORS |
| Chosen option | D — dedicated `biscuit` category via HARD_ANCHORS |
| Decisive reason | Only D produces semantically correct routing AND coherent explainability AND zero cap modification; B reduces but does not eliminate the artifact; A leaves 20/61 products on the wrong lens; C overbUILDS without user value |
| Reversal condition | Revisit if post-reroute run (C3) shows B > 8 or any A grades — that would suggest the routing change is lifting more than taxonomy correction warrants, and endemic relief or cap modification is somehow triggering; also revisit if C1 keyword-bleed simulation finds any live-corpus hit |

---

## §6. Guards Confirmation

| Guard | Status |
|---|---|
| No code / engine edits in this task | CONFIRMED — this is a co-sign decision document only |
| OFF ban absolute | CONFIRMED — no OFF data referenced; Nutrition ruling confirms 0/61 OFF products in run_cookies_001 |
| Frozen invariants untouchable | CONFIRMED — milk scores (run_005_headpin), snk-001 ceiling (70/B), and all other frozen invariants are unaffected |
| Caps INTACT | CONFIRMED — this approval does not authorize any cap modification, cap exemption, or endemic relief |
| No endemic relief | CONFIRMED — cookie sugar+fat is a formulation choice; EV-052 brined_food analogy does NOT extend to sodium re-weighting for cookies |
| Zero published-score movement required | CONFIRMED — condition C1 makes this non-negotiable; any live-score movement = rollback + tripwire-1 escalation |
| C3 strategic read followed | CONFIRMED — "add the category for taxonomy only, never to lift grades" is exactly what this approval authorizes |

---

```json
{
  "task": "P74",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/cookies_coffee/methodology/cookies_coffee_d7_cosign_v1.md",
      "sha256": "61d554a54f9b0383cf49a0851fc7f3dd077fa59837773950198a62fe4df53edb"
    }
  ],
  "counts": {
    "sections_in_cosign": 6,
    "conditions_required": 4,
    "conditions_waivable": 0,
    "keywords_reviewed": 12,
    "keywords_flagged_for_hardening": 1,
    "alternatives_considered_and_rejected": 3,
    "live_categories_in_regression_scope": 7
  },
  "verdict": "APPROVED-WITH-CONDITIONS",
  "conditions": [
    "C1: No-regression proof — 342-case invariants suite PASS + 7-category golden-corpus byte-identity + 12-keyword bleed simulation against all live corpora = zero hits; any published-score movement = STOP + rollback + tripwire-1",
    "C2: Add גרנולה and דגנים to עוגיות חמאה ANCHOR_EXCLUSIONS before shipment; confirm final exclusion list in implementation PR",
    "C3: Run run_cookies_002 post-reroute and verify predicted ceiling holds (B <= 8, A = 0); if ceiling is breached STOP and escalate to Product Agent",
    "C4: Register EV-058 in bsip2_evidence_registry_v1.md citing this co-sign + Nutrition ruling as dual approval basis before any frontend packaging begins"
  ],
  "not_done": [
    "EV-058 implementation — requires C1-CURSOR dispatch after both D7 approvals; this document is the Product Agent approval only",
    "No-regression proof run (C1) — not yet executed; mandatory before code ships",
    "עוגיות חמאה exclusion hardening (C2) — required in implementation PR",
    "run_cookies_002 post-reroute score run (C3) — blocked on implementation",
    "EV-058 formal registration in bsip2_evidence_registry_v1.md (C4) — blocked on this co-sign + orchestrator acceptance",
    "Frontend packaging (factory Stage 8 render_local_page) — blocked on C3 distribution verification",
    "Red-team gate (Stage 9) — blocked on render"
  ],
  "self_check": {
    "verdict_stated_first": true,
    "all_4_questions_answered": true,
    "special_pleading_test_applied": true,
    "keyword_bleed_risk_assessed_per_term": true,
    "minimum_necessary_change_verified": true,
    "conditions_are_non_waivable": true,
    "zero_published_movement_enforced": true,
    "off_ban_respected": true,
    "frozen_invariants_untouched": true,
    "caps_intact_confirmed": true,
    "no_endemic_relief_confirmed": true,
    "no_code_edits_in_this_task": true,
    "c3_strategic_read_cited": true,
    "decision_log_present": true,
    "proposed_status_returned_not_closed": true
  }
}
```
