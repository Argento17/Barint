# GATE-EXCL-1 + passes_with_flag_split_rule_v2 — Product Agent D7 Co-Sign (TASK-504)

**Task:** D7 co-sign of Nutrition's mechanism implementing the owner's "rank on what varies"
ruling (Product's earlier recommendation, `creatine_guide_thirdparty_scope_cosign_v1.md`).
**Reviewer:** Product Agent. **Date:** 2026-07-04.
**Verified against:** `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`
(sha256 `7161410bdf30a9cb171abb539b7b5ba14f483215c52539c087b22a2c9f307171` — confirmed via
`sha256sum` against the file on disk, matches the coordinator's cited hash exactly), sections
`band_gating_exclusion_rule` (lines 592–692), `passes_with_flag_split_rule_v2` (lines
862–950). Read in full before ruling, not taken on the coordinator's summary alone.

---

## Q1 — GATE-EXCL-1 and split_rule_v2, as authored: GRANT, one binding condition

**Both mechanisms co-signed as authored.** They implement exactly what was recommended:

- **GATE-EXCL-1's trigger** ("no product resolves PASS for this bar, AND no product resolves
  FAIL for this bar," a two-ANDed-existential-negation test) is precisely the narrower
  condition my prior report called for instead of silently reusing
  `display_suppression_rule`'s CANNOT-VERIFY-only trigger. It is kept structurally distinct
  (`bandExcludedBars`, never merged into `suppressedBars`), inherits
  `guardrail_never_hides_a_fail` by construction (condition (b) makes it structurally
  incapable of excluding a bar with a real FAIL anywhere in the pool), and its anti-drift
  check is sound: two existential quantifiers, no cardinality, no ratio — the same category
  of test the v1 split rule was already validated on, not a new kind of computation.
- **Keeping the bar displayed, excluded only from gating** is the correct call and matches
  what I required in the prior report: hiding 9 real, differentiated manufacturer claims
  (Informed Sport / Informed Choice / HPLC / iTested) to make a ranking mechanism cleaner
  would delete real information for no honesty gain. Correct to keep visible.
- **`passes_with_flag_split_rule_v2`** closes exactly the empty-caveat-set inversion flagged
  in my prior report, and does it as a strict generalization (subset test on a fixed
  two-element powerset, `∅` or `{dose_adequacy}`) rather than a new computation — verified
  this is not a cardinality test: `CAVEAT_SET ⊆ {dose_adequacy}` is a Boolean OR of two
  identity checks, same category as v1's equality test, not an arithmetic step up from it.
- **`ordering_within_recommended`** (empty-caveat-set products lead, dose-only below,
  catalog-order tie-break within each group) is a stable categorical partition, not a score —
  every gating bar stays independently visible on the card, so nothing is being smuggled into
  an implicit rank a reader can't see for themselves. Co-signed.

**Binding condition on the grant (Q3 folds into this — see below):** before either mechanism
governs a live build, the implementation must attach a byte-diff regression check proving
magnesium's already-gated 18-product tier table (`magnesium_guide_tier_copy_v1.md` /
`supplement_guides_tier_mapping_cosign_v1.md` §2 table — 2×מומלץ, 3×טוב, 0/5/12/1 buckets)
is unchanged under v2. This is not a new task — it's a one-line assertion Frontend runs as
part of the same PR, and I've already done the manual version of it below (§ Q3) so there is
zero ambiguity about what the assertion should confirm.

---

## Q2 — Band A stays empty rather than redefined: AGREE, no conditions

Correct call, and it's the same principle I applied to the letter-relabel question in the
sibling report: a top-tier label must mean the identical thing everywhere it appears, or the
label itself becomes the next trust problem. Redefining "מומלץ מאוד"/A to mean "clears
everything checkable domestically" on one sub-guide while it means "literal 6-of-6" on the
benchmark band and every other guide creates exactly the kind of silent semantic drift a
shopper has no way to detect — worse than an honest empty tier, not better. The existing
`empty_state_handling` mechanism (unconditional header + one-line honest finding) is already
built, already shipped once on magnesium, and needs no new logic — reuse, don't rebuild.

---

## Q3 — magnesium re-check: IN SCOPE NOW, cheaply, not a tracked follow-up

Nutrition's own text confirms "not observed in magnesium's validated 18-product table" but
proposes deferring the re-check. **I already ran it** (independently, against the same table
I verified in my own §0 review of the original `dose_adequacy_sole_caveat` co-sign):

| Product | Raw caveat set (all 6 bars, pre-any-exclusion) | Displayed/gating set (3rd-party + price already suppressed for magnesium) | Empty under v2? |
|---|---|---|---|
| Altman Citrate 120 | `{dose_adequacy}` | `{dose_adequacy}` | No |
| Nutricare WELL | `{dose_adequacy}` | `{dose_adequacy}` | No |
| Supherb Citrate+B6 | `{dose_adequacy, safety}` | `{dose_adequacy, safety}` | No |
| Altman Bisglycinate | `{dose_adequacy, safety}` | `{dose_adequacy, safety}` | No |
| NT L.C. Anti Leg Cramps | `{dose_adequacy, form_absorption}` | `{dose_adequacy, form_absorption}` | No |

Zero of magnesium's 5 `passes_with_flag` members hit an empty caveat set. **v1 and v2
therefore compute byte-identical output on magnesium's current, already-two-gate-satisfied
table** — this is not a "wait and see," it's a already-checked "confirmed no-op," and there
is no reason to schedule it as separate future work when the answer is already known and
costs nothing to state now.

**Ruling: this closes today, not as a new task.** The binding condition in Q1 above is the
formal version of this check — Frontend runs the same comparison as an automated assertion
inside the PR that ships GATE-EXCL-1/v2 for creatine, since the code path is shared between
both guides. If that assertion ever fails (i.e., a future magnesium data update introduces an
empty-caveat product), it fails loudly in CI/build, not silently in production — which is a
stronger guarantee than a manually-tracked follow-up task that could get deprioritized. No
separate TASK-5xx needed for this.

---

## Return Contract

```json
{
  "task": "TASK-504-gate-excl-1-splitrulev2-product-d7-cosign",
  "agent": "Product Agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\product\\supplement_guides_gate_excl1_v2_cosign_v1.md",
      "sha256": "pending — compute post-write"
    }
  ],
  "counts": {
    "rubric_file_sha256_verified": "7161410bdf30a9cb171abb539b7b5ba14f483215c52539c087b22a2c9f307171",
    "sections_read_in_full_before_ruling": 2,
    "magnesium_passes_with_flag_products_rechecked": 5,
    "magnesium_products_hitting_empty_caveat_set": 0,
    "magnesium_v1_v2_output_divergence": 0,
    "resulting_domestic_creatine_distribution_as_relayed": {"A": 0, "B": 10, "C": 7, "D": 4, "cannot_assess": 2, "benchmark": 13}
  },
  "commands_run": [
    {"cmd": "sha256sum 01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml", "exit_code": 0},
    {"cmd": "Grep 'GATE-EXCL-1|bandExcludedBars|passes_with_flag_split_rule_v2' in rubric yaml", "exit_code": 0},
    {"cmd": "Read rubric yaml lines 592-1005 in full", "exit_code": 0}
  ],
  "not_done": [
    "Frontend's byte-diff regression assertion (magnesium v1-vs-v2 output) — recommended as a PR-embedded check here, not run in code",
    "Disclosure-line copy (disclosure_line_draft_gate1) — GATE-1 draft only per Nutrition's own entry; Content + Adversarial QA two-gate still required before it ships",
    "This does not close TASK-504 or any sub-task"
  ],
  "acceptance_test": {
    "spec": "Grant or withhold D7 co-sign on GATE-EXCL-1 and split_rule_v2 as authored, with any binding condition; confirm or reject the empty-Band-A ruling; rule whether the magnesium latent-defect re-check is in scope now or a tracked follow-up.",
    "result": "PASS — both mechanisms GRANTED with one binding condition (PR-embedded regression assertion, substance already verified manually here); Band-A-stays-empty AGREED with no conditions; magnesium re-check ruled IN SCOPE NOW and CLOSED in this same return (0/5 products affected, v1/v2 output byte-identical on the current table) rather than deferred to a new tracked task."
  }
}
```
