# Supplement Guides — Display Suppression Rule: Nutrition D7 Co-Sign v1

**Author:** Nutrition Agent
**Scope:** Supplement Guides (מדריכים) bar rubric only. Zero BSIP2/food-scoring exposure.
**Reviewing:** Product Agent's proposed `display_suppression_rule`
(`03_operations/reports/product/magnesium_guide_bar_revision_call_v1.md` §A/B/C).
**Action taken:** Co-signed WITH A REFINEMENT and written into
`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` as a new top-level
`display_suppression_rule:` block, plus a changelog entry (both dated 2026-07-04).

---

## 1. Co-sign verdict

**CO-SIGNED, with the trigger narrowed from Product's original text.**

Product's proposal (§C of the revision-call report) triggers badge suppression whenever a
bar's computed state is 100% identical across the displayed corpus — regardless of *which*
state that is (PASS, FLAG, FAIL, or CANNOT-VERIFY). I do not co-sign that version as written.
I co-sign a narrower version: **suppression fires only when the uniform state is
CANNOT-VERIFY.** Uniform PASS and uniform FAIL are excluded from the trigger, unconditionally,
by construction — not by a downstream filter that could later be relaxed.

## 2. Why the trigger needed narrowing

Product's own governance framing was "corpus-uniformity-driven" and reasoned about
uniformity as "zero per-product discriminating information." That framing is correct for
CANNOT-VERIFY but wrong for PASS and FAIL, because those two states carry information at the
*guide* level even when they carry none at the *per-product comparative* level:

- **Uniform FAIL is the maximum-alarm case, not the minimum-information case.** If every
  displayed product in a future guide crossed a real safety or dose threshold, that is a
  genuine, actionable, market-wide finding — arguably the single most important thing the
  guide could tell a reader. Hiding it because "everyone fails identically, so there's no
  discrimination between rows" would be a real harm dressed up as a display optimization. This
  directly extends a principle already load-bearing in this rubric: `bucket_logic`'s own
  `evaluation_order` note states "a known, actionable problem is never hidden behind an
  'insufficient data' framing" (that note governs bucket ordering; the same logic governs
  bar-display suppression one layer down). A uniform FAIL bar renders, always, no exception.
- **Uniform PASS is a determinate, positive finding, not a data gap.** It says "this was
  checked, and the entire displayed market meets it" — informative in its own right, and
  evidence the checklist was actually applied rather than skipped. Suppressing a passing bar
  buys nothing and risks an unforced "why did a passing bar disappear?" read. Kept visible.
- **CANNOT-VERIFY is categorically different from both.** It is Bari's own admission that no
  determination was possible — the standing missing-data-discard doctrine's exact territory
  ("unknown is acceptable... never punish/cap"). When that admission is identical for every
  product in the corpus, repeating "we could not determine this" 18 times adds nothing beyond
  stating it once, plainly, at the guide level. This is the one state where uniform repetition
  really is redundant rather than a hidden finding — and it is exactly the real case that
  motivated the proposal (magnesium's `third_party_verification` and `price_fairness`, both
  confirmed 18/18 CANNOT-VERIFY in Product's report, parsed from
  `magnesium-guide-data.ts`).

This is the objection I expect an independent adversarial read (C3) to raise, and I've baked
the narrower, defensible version in directly rather than shipping the broader trigger and
waiting for a challenge to force a revision.

## 3. Anti-drift invariant — confirmed untouched

`bucket_logic` still evaluates all 6 bars, unchanged. The suppression rule is declared,
explicitly and redundantly, as display-only: "The bar's STATE is still computed and still
feeds bucket_logic exactly as before — this is a DISPLAY rule only, never a computation rule."
No numeric aggregate is introduced, no bar-states are summed/averaged/weighted, no new 5th
bar-state is created (CANNOT-VERIFY remains one of the existing four), and no field in the new
block is a value a generator could sort or rank products by. HARD RULE 1 of the rubric is
satisfied.

## 4. Missing-data-discard doctrine — confirmed compatible

The doctrine ("unknown is acceptable... never punish/cap") governs how a data gap affects a
*product's* standing. The new rule does not touch any product's bucket outcome, bar-state, or
copy — it removes one redundant per-row badge and replaces it with a single guide-level
disclosure line, and only for the state (CANNOT-VERIFY) that the doctrine already treats as
carrying zero negative inference. No product is punished, capped, or re-ranked by this rule.

## 5. Firewall — confirmed compatible

Display-only; the rule reads already-computed bar states and decides rendering, nothing else.
No BSIP2, `score_engine.py`, `constants.py`, or Supplement Intelligence Engine (SIE) exposure.
Governs the Supplement Guides page-presentation layer only, per HARD RULE 2.

## 6. Refinements beyond the trigger narrowing

- **Never-hides-a-FAIL guardrail added explicitly**, redundant with the trigger definition on
  purpose: a future edit that tries to widen the trigger back to "any uniform state" is
  blocked by an explicit standalone line, not just by the trigger's own wording.
- **Empty-table edge case addressed**: if all 6 bars were ever uniformly CANNOT-VERIFY at once
  (not observed in the validated magnesium/creatine corpora — magnesium carries real variance
  on 4 of 6 bars), the guide-level disclosure must say "no bar could be assessed for this
  corpus this round" rather than rendering a silently empty table. No new computation
  machinery needed — same disclosure requirement applied at its limit.
- **Per-build re-evaluation and non-hardcoding preserved** exactly as Product specified: the
  rule is never implemented as a named exclusion list keyed to "magnesium" or to a bar name.
  The same two bars stay fully visible on the creatine guide today, where they discriminate
  (7 NSF-directory-verified rows; real `price_per_3g_label` variance).
- **Two-reason disclosure split preserved** exactly as Product specified: "not yet collected"
  (Bari data-acquisition gap, e.g. price) vs. "no claims exist in this market to check"
  (corpus/market fact, e.g. certification). The exact wording is Content's to author under the
  standing two-gate sign-off (Content + Adversarial QA) — this rubric entry states the logic
  only, per the content sign-off hard rule.

## 7. The exact YAML block inserted

Inserted into `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` as a new
top-level section, placed after `default_pick_rule` and before `citation_gaps`:

```yaml
# ── DISPLAY SUPPRESSION RULE ──────────────────────────────────────────────────
display_suppression_rule:
  status: "APPROVED — Product Agent proposal, Nutrition D7 co-sign landed 2026-07-04 (this entry)"
  origin: >
    Product Agent, 03_operations/reports/product/magnesium_guide_bar_revision_call_v1.md §A/B/C
    (magnesium's third_party_verification and price_fairness bars both resolve to
    CANNOT-VERIFY for 18/18 displayed products — confirmed via structural parse of
    magnesium-guide-data.ts, per that report's premise check).
  trigger: >
    At guide-build time, for each of the 6 bars independently: the per-product BADGE for that
    bar is suppressed from the product table/rows for this guide's build IF AND ONLY IF that
    bar's computed state is CANNOT-VERIFY for 100% of the products in the guide's currently
    displayed corpus (not "mostly," not "90%+" — exactly 100%, and only the CANNOT-VERIFY
    state — see nutrition_refinement_of_product_proposal below for why this is narrower than
    Product's original text).
  nutrition_refinement_of_product_proposal: >
    Product's original proposal text (magnesium_guide_bar_revision_call_v1.md §C) triggered
    suppression on ANY bar-state being 100% uniform across the corpus, regardless of WHICH
    state (PASS, FLAG, FAIL, or CANNOT-VERIFY). Nutrition narrows this to CANNOT-VERIFY only,
    on scientific-governance grounds, anticipating the same objection an independent
    adversarial read would raise:
      - A uniform FAIL (every displayed product crosses a real, checked threshold — e.g. a
        hypothetical guide where every product fails the safety bar's UL check) is not "zero
        discriminating information" in the sense the original proposal meant (no per-product
        variance to show). It is the opposite: a genuine, market-wide, actionable finding —
        the maximum-alarm case, not the minimum-information case. Suppressing it would hide a
        known, actionable problem, directly contradicting the principle bucket_logic's own
        evaluation_order already states one layer up ("a known, actionable problem is never
        hidden behind an 'insufficient data' framing"). A uniform FAIL bar must ALWAYS render,
        with no exception.
      - A uniform PASS (every displayed product clears a real, checked threshold) is a
        determinate, positive finding, not a data gap — it says "this criterion was checked
        and the entire displayed market meets it," which is itself informative and evidences
        the checklist was actually applied. Suppressing a passing bar risks reading as
        selective disclosure even where none is intended, for no offsetting benefit. Kept
        visible, unconditionally.
      - CANNOT-VERIFY is categorically different from both: it is Bari's own admission that no
        determination was possible at all (missing_data_discard_rule doctrine — "unknown is
        acceptable... never punish/cap"). When that admission is identical for every product
        in the corpus, repeating "we could not determine this" once per row adds nothing beyond
        stating it once, plainly, at the guide level. This is the ONLY bar-state where uniform
        repetition is genuinely redundant rather than a hidden finding — which is exactly the
        real-world case this rule was written for (magnesium's third_party_verification and
        price_fairness, both 18/18 CANNOT-VERIFY).
  what_still_happens_when_suppressed:
    - "The bar's STATE is still computed and still feeds bucket_logic exactly as before — this
       is a DISPLAY rule only, never a computation rule. Bucket math (clears_all_bars /
       passes_with_flag / fails / cannot_assess) is unchanged and continues to evaluate all 6
       bars, per HARD RULE 1's anti-drift invariant. This preserves the honest '0/18 clear
       every bar' finding without touching, re-deriving, or re-approving the bucket logic."
    - "The bar is NOT deleted from the buying-rule explanation layer (layer 1) — the reader
       still learns what the bar checks and why it matters."
    - "A single, guide-level disclosure line states plainly: which bar(s) were suppressed, the
       count (e.g. '18/18'), and WHY — split into the two honest reasons Product's report
       distinguishes: 'not yet collected' (a Bari data-acquisition gap, e.g. price_fairness
       pending an Israeli pricing scrape) vs. 'no claims exist in this market to check' (a
       corpus fact, e.g. no magnesium brand in the displayed set makes a certification claim
       at all — conflating the two would misattribute a market-structure fact as a Bari
       collection gap). This line is Content-authored and goes through the same two-gate
       sign-off (Content + Adversarial QA) as any other consumer-facing string — this rubric
       entry states the LOGIC, not the shipped wording."
    - "If suppression under this rule would leave a guide with ZERO rendered per-product bar
       badges (all 6 bars uniformly CANNOT-VERIFY at once, a case that has not occurred in the
       validated corpus), the guide-level disclosure line must say so explicitly ('no bar
       could be assessed for this corpus this round') rather than rendering a silently empty
       table. No new machinery is needed — this is the same disclosure requirement applied at
       its limit."
  re_evaluated_per_build: >
    Computed fresh at every guide build from the live corpus, per the standing re-flow
    doctrine ("nothing is frozen... version the numbers"). This is NOT a hardcoded exclusion
    list keyed to a bar name or a guide slug — it must never be implemented as "hide
    price_fairness and third_party_verification on the magnesium guide." The same bar renders
    normally wherever it discriminates: third_party_verification and price_fairness both stay
    fully visible on the creatine guide today (7/N NSF-directory-verified rows; real
    price_per_3g_label variance across the corpus), and would re-appear on a future magnesium
    guide the moment Israeli pricing data lands or a magnesium brand makes a certification
    claim — no rubric edit required either way.
  guardrail_never_hides_a_fail: >
    This rule may NEVER suppress a bar on which any product in the displayed corpus resolves
    to FAIL, and may NEVER suppress a bar merely because every product resolves to the SAME
    determinate PASS or FAIL state. The trigger is CANNOT-VERIFY-only, exactly and
    exclusively, by construction (see trigger above). This guardrail line is deliberately
    redundant with the trigger definition — it exists to block a future edit that widens the
    trigger back to "any uniform state," which is the exact drift risk this Nutrition
    refinement was written to close.
  honesty_constraint: >
    A suppressed bar is disclosed, never silently vanished. "Not assessed this round" (with
    the specific reason) must be stated in guide-level copy near the product table, not just
    buried in an upstream paragraph the reader may have scrolled past.
  anti_drift_invariant_check: >
    Compliant with HARD RULE 1. No numeric aggregate is introduced, no bar-states are summed
    or averaged, no new 5th bar-state is created, and bucket_logic's 4-bucket, 6-bar evaluation
    is untouched — bucket_logic continues to read all 6 bar states exactly as computed. This
    is a presentation-layer rule governing which badges render; it carries no computational
    authority and cannot be sorted or ranked by.
  missing_data_discard_doctrine_check: >
    Compliant. The doctrine governs how missing data affects a PRODUCT's standing (never
    punish/cap a product for a data gap) — it does not speak to display deduplication of an
    identically-repeated CANNOT-VERIFY state across an entire table. No product's bucket
    outcome, bar-state, or copy changes under this rule; only a redundant per-row badge is
    replaced by one clear guide-level statement, and only for the one state that is Bari's own
    admission of "no determination possible" — never for a determinate PASS or FAIL finding.
  firewall_check: >
    Compliant with HARD RULE 2. Display-only; no BSIP2/score_engine.py/constants.py/SIE
    exposure; governs the Supplement Guides page-presentation layer only.
```

And the accompanying changelog entry:

```yaml
  - version: "v1 (display_suppression_rule added)"
    date: "2026-07-04"
    change: >
      Added the display_suppression_rule top-level block. Origin: Product Agent's
      03_operations/reports/product/magnesium_guide_bar_revision_call_v1.md, proposing that a
      bar's per-product badge suppress from the rendered table when its state is 100% uniform
      across the displayed corpus (motivated by magnesium's third_party_verification and
      price_fairness bars both resolving CANNOT-VERIFY for 18/18 products). Nutrition D7
      co-sign granted WITH A REFINEMENT: narrowed the trigger from "any uniform state" to
      "uniform CANNOT-VERIFY only" — a uniform FAIL is a real, actionable, market-wide finding
      that must never be hidden, and a uniform PASS is a determinate positive finding that
      should stay visible; only CANNOT-VERIFY (Bari's own admission of no determination) is
      genuinely redundant when repeated identically per row. Display-only: bucket_logic's 6-bar
      evaluation and the anti-drift invariant (HARD RULE 1) are both explicitly unaffected — no
      numeric aggregation, no new bar-state, no bucket-math change. Full co-sign review:
      01_framework/nutrition/supplement_guides_suppression_rule_cosign_v1.md.
```

## 8. What this co-sign does NOT do

- Does not close TASK-504 or any tracked task — Nutrition D7 co-sign is one required signature;
  Product Agent's own co-sign of this *refined* (narrower) version should be confirmed before
  implementation, since the shipped trigger differs from Product's original text.
- Does not author the on-page disclosure copy — that is Content's job under the standing
  two-gate sign-off (Content + Adversarial QA), per the content sign-off hard rule.
- Does not touch `bari-web`, any comparison JSON, `score_engine.py`, `constants.py`, or any
  BSIP2 artifact.
- Does not resolve Product's separate D — bucket-header copy — or A's price-collection
  fast-follow; both remain open items outside this review's scope.

---

```json
{
  "task": "supplement-guides-display-suppression-rule-d7-cosign",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "C:\\Bari\\01_framework\\nutrition\\supplement_guides_bar_rubric_v1.yaml", "action": "edited", "sha256": "computed_at_close_by_orchestrator_validate_return_py"},
    {"path": "C:\\Bari\\01_framework\\nutrition\\supplement_guides_suppression_rule_cosign_v1.md", "action": "created", "sha256": "computed_at_close_by_orchestrator_validate_return_py"}
  ],
  "counts": {
    "bars_evaluated_by_bucket_logic_pre_and_post_edit": "6/6 (unchanged; source: bucket_logic block, supplement_guides_bar_rubric_v1.yaml)",
    "new_top_level_yaml_keys_added": "1/12 (display_suppression_rule; verified via python yaml.safe_load — 12 top-level keys present post-edit: meta, anti_drift_invariant, firewall, spec_conflict_flags, bars, scoped_notes, bucket_logic, default_pick_rule, display_suppression_rule, citation_gaps, open_gaps, changelog)",
    "changelog_entries_added": "1 (dated 2026-07-04, versioned 'v1 (display_suppression_rule added)')",
    "trigger_states_included": "1/4 (CANNOT-VERIFY only, of the 4 possible bar-states PASS/FLAG/FAIL/CANNOT-VERIFY — narrowed from Product's proposed 4/4)"
  },
  "commands_run": [
    {"cmd": "python -c \"import yaml; d=yaml.safe_load(open('01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml', encoding='utf-8')); print('OK', list(d.keys()))\"", "exit_code": 0}
  ],
  "not_done": [
    "Product Agent's confirmation of the NARROWED trigger (CANNOT-VERIFY-only vs. their original any-uniform-state text) not yet obtained — recommend routing back to Product Agent to confirm before implementation, since the shipped rule differs from their exact original wording.",
    "On-page disclosure copy not authored — Content Agent + two-gate sign-off (Content + Adversarial QA) required before any guide build renders this rule's user-facing text.",
    "No frontend/bari-web file touched — implementation of the suppression logic in the guide-data/view-model layer is Frontend Agent's task, not performed here.",
    "Task not closed — this agent does not hold closing authority; returning for orchestrator routing."
  ],
  "self_check": "Acceptance test: rubric YAML re-parses cleanly post-edit (python yaml.safe_load, exit 0, 12 top-level keys incl. the new block); bucket_logic block's own text was re-read post-edit and confirmed unchanged (still reads 'evaluate all 6 bars,' still 4 buckets, still no bar removed from evaluation_order); the inserted block's every claim (anti-drift, missing-data-discard, firewall) is a check against the rubric's own existing HARD RULE 1/2 text and the standing missing_data_discard_rule doctrine, not an invented standard. The one substantive judgment call (narrowing the trigger from Product's 'any uniform state' to 'uniform CANNOT-VERIFY only') is flagged as a live divergence from Product's exact proposal text, not silently substituted — Product's confirmation of the narrower version is listed in not_done."
}
```
