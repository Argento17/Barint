# Magnesium Guide 4-Tier Recommendation Mapping — Nutrition D7 Co-Sign Review

**Task:** TASK-504 follow-on. **Reviewer:** Nutrition Agent (rubric owner,
`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`, HARD RULE 1 anti-drift
invariant). **Date:** 2026-07-04. **Reviewing:** Product Agent's proposal at
`03_operations/reports/product/magnesium_guide_recommendation_tiers_v1.md`.
**Status:** Nutrition D7 delivered here — WITH AMENDMENT to the מומלץ/טוב split predicate.
Product Agent D7 co-sign on the amended predicate specifically is still outstanding before
this governs live copy (Hard Rule 8 dual-key). A parallel C3 challenge on the same question
is running independently; this ruling was reached without reference to it.

Scope discipline observed: this review touches only
`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` (recorded the endorsed rule as a
new `recommendation_tier_mapping` block + changelog entry) and this report. No code, no
`magnesium-guide-data.ts`, no `bucket_logic`, no bar states were edited.

---

## 1. The load-bearing ruling: does the 1-vs-2+ count threshold violate Hard Rule 1?

**Yes.** Product's proposed מומלץ/טוב split — count the number of non-PASS bars among the 4
displayed bars (`dose_adequacy`, `form_absorption`, `safety`, `label_transparency`), then
route exactly-1 to מומלץ and 2-or-more to טוב — is a violation of the anti-drift invariant
as written, and is not co-signed.

**Reasoning.** Counting non-PASS bars is arithmetically identical to assigning an implicit
point value of 1 to every FLAG/CANNOT-VERIFY bar and 0 to every PASS bar, summing those
points, and comparing the sum against a cutoff (1 vs ≥2). That is exactly the "point value
per bar-state" language and the "no numeric field... a generator could sort by" language
Hard Rule 1 uses verbatim. Two aspects of Product's own defense do not change this:

- **"It's never stored or shown as a number."** Hard Rule 1 bans the *computation* ("no
  implementation of it may compute... any composite or weighted numeric score"), not merely
  its storage or display. An intermediate count that only ever feeds a binary gate is still
  a computed composite — the rule does not carve out an exception for aggregates that are
  immediately discarded after one comparison.
- **"bucket_logic itself already uses threshold language, so this isn't new in kind."** This
  conflates two different logical operations. `bucket_logic`'s own rules — "if ANY bar =
  FAIL," "if any bar in {FLAG, CANNOT-VERIFY}" — are **existential quantifiers**: does at
  least one bar match a state, yes or no. An existential test needs no intermediate numeric
  variable; it short-circuits on the first match. Asking "are there ≥2 non-PASS bars"
  requires computing a cardinality, |{non-PASS bars}|, as a number *before* the comparison
  can happen. That intermediate number is the composite the invariant forbids. Existence-
  testing and counting are different operations in kind, not degree, and `bucket_logic`
  provides precedent for the former, not the latter.

This is also precisely the risk the rubric's own `anti_drift_invariant.why` and
`supplement_guides_science_cosign_v1.md` §6 tripwire 2 named in advance: "a real future
temptation to bolt a composite number back on top of the bars." A binary-thresholded count
is a small, reasonable-looking version of exactly that temptation — rule-accretion risk does
not shrink because the threshold is 1-vs-2 and the output has only two labels. Product
flagged this exact concern for independent review rather than asserting it unilaterally
cleared the invariant (§6 of their proposal); this ruling confirms their instinct to flag it
was correct.

---

## 2. The endorsed qualitative replacement: `dose_adequacy_sole_caveat`

**Rule.** Among the 4 displayed bars, compute the *set* of bars whose state is not PASS —
never a count, a set-membership test:

- Set is **exactly `{dose_adequacy}`** (form, safety, label all PASS) → **מומלץ**.
- Set is non-empty and **contains any bar other than `dose_adequacy`** (form_absorption,
  safety, or label_transparency — whether or not dose_adequacy is also present) → **טוב**.

No cardinality of the set is ever computed. The predicate asks *which* bar(s) are in the
caveat set, never *how many*.

**Why this is nutritionally grounded, not an arbitrary re-carving of the same line.** A
dose-only caveat means the product's chemical form, safety profile, and label honesty are
all clean — the sole open question is a quantity shortfall against the full
literature-effective range (still ≥ 0.5× `min_effective`, i.e. not fairy-dust, per the
`dose_adequacy` bar's own FLAG definition), and it is correctable simply by the consumer
taking a larger daily amount or stacking with another source. It is not a finding about
product quality. A `form_absorption`, `safety`, or `label_transparency` caveat is
categorically different: it says something about the compound's absorption tier, a
GI-tolerance soft-note, or the clarity of the label itself — a property of the product a
consumer cannot fix by taking more of it. That is why a product with a single *non-dose*
caveat sits in טוב, not מומלץ, even though it would show the same "1 flag" surface profile
Product's count rule would have called מומלץ. The distinction is drawn directly from the
bars' own `measures` definitions already in the rubric, not a new judgment invented for this
proposal.

**Proof this is a genuine replacement, not the same rule relabeled.** On the current corpus,
every `passes_with_flag` member happens to carry `dose_adequacy = FLAG`, so this rule and
Product's count rule produce the identical split today. They diverge on a hypothetical future
product with a single *non-dose* caveat and a clean dose bar (e.g., full dose, moderate-tier
form): Product's count rule would place it in מומלץ (1 non-PASS bar); this rule places it in
טוב (the caveat set ≠ `{dose_adequacy}`). That divergence is the evidence the two rules are
different in kind, not just in wording.

### Per-product result, the 5 `passes_with_flag` members (2026-07-04, verified against `buildProduct()` calls in `magnesium-guide-data.ts` lines 206–260)

| Product | dose | form | safety | label | Caveat set | Tier |
|---|---|---|---|---|---|---|
| Altman Citrate 120 (200mg citrate) | FLAG | PASS | PASS | PASS | `{dose_adequacy}` | **מומלץ** |
| Nutricare WELL (168mg bisglycinate) | FLAG | PASS | PASS | PASS | `{dose_adequacy}` | **מומלץ** |
| Supherb Citrate+B6 (250mg citrate) | FLAG | PASS | FLAG | PASS | `{dose_adequacy, safety}` | **טוב** |
| Altman Bisglycinate (250mg bisglycinate) | FLAG | PASS | FLAG | PASS | `{dose_adequacy, safety}` | **טוב** |
| NT L.C. Anti Leg Cramps (190mg hydroxide) | FLAG | FLAG | PASS | PASS | `{dose_adequacy, form_absorption}` | **טוב** |

Result matches Product's proposed split exactly (2× מומלץ, 3× טוב) — the mechanism changed,
today's visible tier assignment did not.

---

## 3. Rest of the mapping — co-signed

| Element | Ruling |
|---|---|
| `clears_all_bars` → מומלץ מאוד | **CO-SIGNED.** Unchanged `bucket_logic` definition (all 6 bars PASS); no new computation. |
| Empty מומלץ מאוד tier rendered unconditionally with an honest empty-state line | **CO-SIGNED.** 0/18 today is the guide's own headline finding, not a bug to hide; omitting the tier would misrepresent the tier structure as 3-tier and require rebuilding the moment a product clears all 6 bars. |
| Any FAIL → לא מומלץ | **CO-SIGNED.** Unchanged `bucket_logic` definition; no new computation. |
| `cannot_assess` (TRIOMAG) → separate "לא ניתן להעריך" section, outside the 4 ranked tiers | **CO-SIGNED.** TRIOMAG's own bar-state row is all-CANNOT-VERIFY because the form itself is an undisclosed 3-way blend — a genuine data gap, not an actionable negative finding. Folding it into לא מומלץ would violate the missing-data-discard doctrine ("unknown is acceptable... never punish/cap") and collapse `bucket_logic`'s own deliberate distinction between Tink Oxide-520 (known-bad form → fails) and TRIOMAG (genuinely unknowable → cannot_assess). |
| Ordered tier display (מומלץ מאוד → מומלץ → טוב → לא מומלץ), no within-tier sort | **CO-SIGNED.** Tier *names* are ordered; products within a tier stay in stable catalog/scrape order, never re-sorted by a derived value. No score, percentile, or "N/6" ever accompanies a tier name. |

None of these five elements required amendment — each is either a direct restatement of
`bucket_logic`'s existing categorical definitions or an honesty-preserving display choice
with no computation attached.

---

## 4. Final anti-drift confirmation

Confirmed for the rule set actually endorsed (Product's four unchanged mappings +
`dose_adequacy_sole_caveat` in place of the count threshold):

- No numeric field is created, stored, or computed per product.
- No sum, average, weighting, percentage, or cardinality comparison is introduced anywhere.
- `bucket_logic`'s existing 4-bucket, 6-bar computation is untouched.
- The one place a count *was* about to be introduced (the מומלץ/טוב split) has been replaced
  with a set-membership predicate that cannot be generalized into a sortable score — it has
  exactly two output states, keyed to *which* bar is in the caveat set, not a magnitude.
- Tier membership remains a categorical grouping, never a rank, consistent with Hard Rule
  1's closing statement that "the four buckets are unordered as a set."

---

## 5. Recorded in the rubric

The endorsed mapping is now recorded at
`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` as a new top-level
`recommendation_tier_mapping` block (inserted after `display_suppression_rule`, before
`citation_gaps`), containing: the 5 tier definitions (including the outside-tiers
`cannot_assess` placement), the full `dose_adequacy_sole_caveat` predicate with its
nutritional grounding and the 5-product validation table above, the `anti_drift_ruling`
block reproducing §1's reasoning, the `rest_of_mapping_cosign` block reproducing §3, and a
`final_no_numeric_field_confirmation` line. A corresponding changelog entry
(`v1 (recommendation_tier_mapping added)`, dated 2026-07-04) was appended to the rubric's
existing `changelog` list. No other file was touched.

The block's `status` field states plainly that Product Agent's D7 co-sign on the *amended*
split predicate specifically is still outstanding — Product signed off on a different
mechanism (the count threshold), not this one — so this rule does not yet carry full D7
dual-key authority per Hard Rule 8. Frontend must not build against this until Product
confirms.

---

## Return Contract

```json
{
  "task": "TASK-504-magnesium-4tier-recommendation-nutrition-d7",
  "agent": "Nutrition Agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\01_framework\\nutrition\\supplement_guides_tier_mapping_cosign_v1.md",
      "sha256": "self-referential — hash of this file's content prior to this JSON block finalizing cannot embed its own final hash; last computed pre-edit value was 0d6cee87a4804a05a432ca88a998685d46deae067e53abbfd84c5cc0b7eff26b, recompute after save for the exact stored value"
    },
    {
      "path": "C:\\Bari\\01_framework\\nutrition\\supplement_guides_bar_rubric_v1.yaml",
      "sha256": "d8ae4089ed52c0496c86f475c67599e162b1d71359c57b5829692e6928dc6628",
      "change": "Added recommendation_tier_mapping block + one changelog entry. No other content changed."
    }
  ],
  "counts": {
    "passes_with_flag_products_reviewed": 5,
    "passes_with_flag_products_total_denominator": 5,
    "tier_split_result": {
      "מומלץ": 2,
      "טוב": 3
    },
    "elements_of_product_mapping_reviewed": 5,
    "elements_amended": 1,
    "elements_cosigned_unchanged": 4,
    "source": "C:\\bari_wt_t504\\bari-web\\src\\lib\\guides\\magnesium-guide-data.ts (buildProduct() calls, lines 206-410, read in full); C:\\Bari\\01_framework\\nutrition\\supplement_guides_bar_rubric_v1.yaml (bucket_logic, anti_drift_invariant, display_suppression_rule)"
  },
  "commands_run": [
    {"cmd": "Get-FileHash 01_framework\\nutrition\\supplement_guides_bar_rubric_v1.yaml -Algorithm SHA256", "exit_code": 0}
  ],
  "not_done": [
    "Product Agent D7 co-sign on the amended dose_adequacy_sole_caveat split predicate specifically — not yet requested/received; the rubric block's status field flags this explicitly",
    "This review does not close TASK-504 or any sub-task — proposal-and-ruling only, per instruction",
    "Exact Hebrew copy for tier labels/sub-captions/empty-state line remains Content Agent + two-gate territory, not addressed here",
    "headlineFinding.body[2]'s retired phrase ('זו הרשימה המעשית להתחיל ממנה') still needs a matching content edit once tier copy lands — flagged by Product, not resolved by either doc"
  ],
  "acceptance_test": {
    "spec": "Rule directly on whether the count-threshold split violates the anti-drift invariant (yes/no + reasoning); if it violates, define a qualitative, non-counting split rule grounded in bar semantics with per-product results for all 5 passes_with_flag products; co-sign or amend the remaining 4 mapping elements; confirm no numeric field/percentage/sortable score is introduced; record the endorsed rule in the rubric yaml only if co-signing.",
    "result": "PASS — ruled the count threshold a Hard Rule 1 violation with explicit reasoning (existential vs. cardinality distinction); defined dose_adequacy_sole_caveat as the qualitative replacement with nutritional grounding and full 5-product table verified against the live data file; co-signed all 4 remaining mapping elements with reasoning; confirmed zero numeric/sortable fields in the final endorsed rule; recorded the rule as a new recommendation_tier_mapping block + changelog entry in the rubric yaml, and nowhere else."
  }
}
```
