# Magnesium Guide — 4-Tier Recommendation Model (Product decision doc)

**Task:** TASK-504 follow-on — owner directive to replace pass/flag bucket labels on the
magnesium buying guide with 4 named recommendation tiers, and remove the
"הרשימה המעשית להתחיל ממנה" header.
**Author:** Product Agent · **Date:** 2026-07-04
**Status:** AMENDED + CO-SIGNED 2026-07-04. Nutrition D7 (independently agreed by C3) ruled
that this doc's original §2 split rule (a count-threshold: 1 vs ≥2 non-PASS bars) violates
the anti-drift invariant — a count-then-compare-to-cutoff is a composite sum by
construction, regardless of whether the number is stored or shown. Nutrition replaced it
with a qualitative set-membership predicate, `dose_adequacy_sole_caveat`, recorded in
`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`
(`recommendation_tier_mapping` / `passes_with_flag_split_rule`) and detailed in
`01_framework/nutrition/supplement_guides_tier_mapping_cosign_v1.md`. Product verified both
documents directly and co-signs the amended predicate — see §2 (amended) below. It reaches
the identical result on today's 5 products through a materially different, compliant
mechanism (proof it's a real replacement, not a relabel). Everything else in this doc
(§§1, 3, 4, 5 [defensibility argument unaffected], 7) is unchanged and stands as
originally proposed. D7 is now dual-keyed (Nutrition + Product); still needs Content +
Adversarial QA two-gate on any consumer-facing string before Frontend ships copy.
**Scope:** Display-layer mapping only. Does **not** edit
`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`, does not edit
`bari-web/src/lib/guides/magnesium-guide-data.ts`, does not touch `bucket_logic`,
`bucket` field values, or any code. Proposal only.

---

## 0. Premise check (Hard Rule 10 — verify before ruling)

Re-derived directly from `C:\bari_wt_t504\bari-web\src\lib\guides\magnesium-guide-data.ts`
(18 `buildProduct()` calls, read in full) against
`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` `bucket_logic.evaluation_order`:

| Bucket | Count | Denominator | Match to brief |
|---|---|---|---|
| `clears_all_bars` | 0 | /18 | confirmed empty |
| `passes_with_flag` | 5 | /18 | confirmed |
| `fails` | 12 | /18 | confirmed |
| `cannot_assess` | 1 | /18 | confirmed (TRIOMAG) |

0+5+12+1 = 18/18. The brief's counts are correct against the artifact — proceeding on
verified numbers, not the brief's assertion alone.

Also confirmed from the rubric (lines 486–591): `third_party_verification` and
`price_fairness` are **suppressed from per-product display** for this guide build (both
100% CANNOT-VERIFY, 18/18) — they still feed `bucket_logic` computation but render no
per-row badge. This matters directly for the tier-split rule below: a suppressed bar
can never be the stated *reason* a product sits in one tier vs another, because the
consumer never sees that badge on that row.

---

## 1. The 4 tier definitions

| Tier (owner-final label) | Maps from | Definition |
|---|---|---|
| **מומלץ מאוד** | `clears_all_bars` | All 6 bars = PASS. Zero FLAG, zero FAIL, zero CANNOT-VERIFY. |
| **מומלץ** | `passes_with_flag`, split A | No FAIL anywhere; the non-PASS set is EXACTLY `{dose_adequacy}` (AMENDED §2). |
| **טוב** | `passes_with_flag`, split B | No FAIL anywhere; the non-PASS set contains a bar OTHER than `dose_adequacy` (AMENDED §2). |
| **לא מומלץ** | `fails` | At least one bar = FAIL (any of the 6). |
| *(outside the 4 tiers)* **לא ניתן להעריך** | `cannot_assess` | `dose_adequacy` = CANNOT-VERIFY and no bar = FAIL — see §3. |

"Displayed bar" = one of the 4 bars actually rendering a per-product badge on this guide
build: `dose_adequacy`, `form_absorption`, `safety`, `label_transparency`.
`third_party_verification` and `price_fairness` are excluded from the count because both
are suppressed 18/18 — they cannot be a stated, pointable reason for any tier placement.

---

## 2. The מומלץ / טוב split rule (exact, deterministic) — AMENDED, Nutrition D7 + Product co-sign

**Superseded rule (do not use):** the original version of this section counted the
number of non-PASS *displayed* bars among `passes_with_flag` members and thresholded at
1 (→ מומלץ) vs ≥2 (→ טוב). Nutrition D7 ruled this a violation of the anti-drift
invariant: computing a count and comparing it to a cutoff is a composite numeric
aggregate by construction — an implicit point-value-per-bar-state sum — regardless of
whether the count is ever stored or displayed. Product independently verified this
reasoning against `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` and
agrees the objection is correct; it was already flagged in this doc as "the one place
closest to the line."

**Current rule — `dose_adequacy_sole_caveat`** (set-membership / identity test, never a
count): compute the SET of *displayed* bars (`dose_adequacy`, `form_absorption`,
`safety`, `label_transparency`) whose state is NOT PASS.

- If that set is **exactly `{dose_adequacy}`** (dose is the only non-PASS bar; form,
  safety, and label are all PASS) → **מומלץ**.
- If that set **contains any bar other than `dose_adequacy`** (form_absorption, safety,
  or label_transparency is non-PASS, whether or not dose_adequacy also is) → **טוב**.

This is qualitative, not quantitative: it never computes a cardinality, stores no
per-product number, and is not sortable — it is a yes/no test of set identity. It also
carries real semantics distinct from a bare count: a dose_adequacy caveat is
consumer-correctable (take a larger daily amount / pair with another source), while a
form_absorption, safety, or label_transparency caveat is a property of the product
itself no consumer action fixes — which is a more defensible basis for "still generally
usable" vs "carries an independent product concern" than a raw tally ever was. It also
generalizes differently from the old count rule on future hypotheticals (e.g. a product
whose sole caveat is `form_absorption` alone: the old count rule would have called that
מומלץ at "1 non-PASS bar"; this rule correctly calls it טוב, since dose is not its sole
caveat) — proof this is a genuine qualitative replacement, not the same computation
wearing new words. Full ruling: `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`
`recommendation_tier_mapping.passes_with_flag_split_rule`;
`01_framework/nutrition/supplement_guides_tier_mapping_cosign_v1.md`.

### Applied to all 5 `passes_with_flag` products

| Product | dose | form | safety | label | Non-PASS displayed set | Is it exactly `{dose_adequacy}`? | Tier |
|---|---|---|---|---|---|---|---|
| Supherb Citrate+B6 (250mg) | FLAG | PASS | FLAG | PASS | {dose, safety} | No | **טוב** |
| Altman Bisglycinate (250mg) | FLAG | PASS | FLAG | PASS | {dose, safety} | No | **טוב** |
| Altman Citrate 120 (200mg) | FLAG | PASS | PASS | PASS | {dose} | Yes | **מומלץ** |
| Nutricare WELL (168mg) | FLAG | PASS | PASS | PASS | {dose} | Yes | **מומלץ** |
| NT L.C. Anti Leg Cramps (190mg, hydroxide) | FLAG | FLAG | PASS | PASS | {dose, form} | No | **טוב** |

Reasoning per row, pointing at bars (not a score):
- **Altman Citrate 120 / Nutricare WELL → מומלץ**: the only caution is that the dose
  sits below the 300mg full threshold (200mg / 168mg respectively) — form, safety, and
  label are all clean, so the non-PASS set is exactly `{dose_adequacy}`.
- **Supherb / Altman Bisglycinate → טוב**: the non-PASS set contains `safety` in addition
  to `dose_adequacy` — both sit at the 250mg point where the safety bar's soft
  GI-tolerance line also fires (per the rubric's own boundary treatment already baked
  into this data file, lines 215/226 — this is existing, previously gate-1-approved
  editorial framing, not a new interpretation I am introducing).
- **NT L.C. → טוב**: the non-PASS set contains `form_absorption` in addition to
  `dose_adequacy` — hydroxide is moderate-tier absorption, not the high tier
  citrate/bisglycinate sit in.

---

## 3. `cannot_assess` (TRIOMAG) — ruling: separate callout, OUTSIDE the 4 tiers

**Recommendation: a distinct "לא ניתן להעריך" section below the 4 ranked tiers — never
folded into לא מומלץ.**

Reasoning: TRIOMAG carries zero FAIL on any bar. Its own bar-state row is
`[cannot_verify, cannot_verify, cannot_verify, cannot_verify, cannot_verify,
cannot_verify]` — every bar is CANNOT-VERIFY because the form itself is an undisclosed
3-way blend (citrate/bisglycinate/taurate, no ratio published), not because anything was
checked and found wanting. Placing it in לא מומלץ would present a pure data gap as an
actual negative verdict — a direct violation of the missing-data-discard doctrine
("unknown is acceptable; never punish or cap a product for a data gap") and of
`bucket_logic`'s own stated principle that a genuine "insufficient data" case is
categorically different from an actionable negative finding.

The rubric's `bucketSubCaptions.cannot_assess` copy (already gate-1-drafted at
`magnesium-guide-data.ts:502-503`) already states this distinction correctly and should
be reused, not rewritten:
> "אצל המוצרים האלה אי אפשר לקבוע כמה מגנזיום יסודי מגיע בפועל, ולכן אי אפשר להעריך אף
> אחד מהספים האחרים."

Do not silently drop TRIOMAG from the page. It renders, labeled honestly, outside the
ranked spectrum.

---

## 4. Empty top tier (מומלץ מאוד) — ruling: show it, with an honest empty-state line

**Recommendation: render all 4 tier headers unconditionally, including מומלץ מאוד, with
an explicit one-line honest state when it is empty** (e.g. "אף מוצר לא עומד היום בכל
ששת ספי הבדיקה במלואם" — exact wording is Content's job, two-gate as always).

Reasoning: this is already the page's own headline finding
(`headlineFinding.title`: "אף מוצר מגנזיום במדף הישראלי לא עובר את כל ספי הקנייה") — an
empty top tier is not a display bug to hide, it *is* the guide's central finding.
Silently omitting the tier would look like the guide only ever had 3 tiers, which is
less transparent than stating plainly that zero products qualify today, and it breaks
the moment a future product (or the creatine guide, which uses the same bar rubric)
does clear all 6 bars — the tier structure should not need rebuilding when that happens.

---

## 5. Defensibility vs the owner's rejected composite score

The rejected model computed a single opaque weighted number (a composite/bioavailability
-adjusted figure) that consumers saw as one unexplained rank. This proposal computes
**zero** numbers: every tier assignment is a lookup over the 6 already-visible
PASS/FLAG/FAIL/CANNOT-VERIFY badges, using a stated if/then rule anyone can re-derive by
hand from the bars on the page. The tiers are 4 coarse, named buckets, not a fine-grained
scale (no 1–100, no percentile) — a consumer or red-teamer can falsify any placement by
pointing at a specific bar ("this is in טוב because its safety bar is flagged"), which is
exactly the auditability the old composite denied by hiding which input drove the number.
The מומלץ/טוב split (AMENDED §2, `dose_adequacy_sole_caveat`) is a set-identity test, not
a count — "is the non-PASS set exactly {dose_adequacy}, yes or no" — so it doesn't even
raise the "is a threshold secretly a sum" question the original count-based draft did.
That is categorically different from a composite score that ranks every product against
every other on a continuous scale.

---

## 6. Anti-drift confirmation (Hard Rule 1, `supplement_guides_bar_rubric_v1.yaml`)

- No new numeric field is created, stored, or computed per product.
- No sum, average, weighting, or percentage is introduced anywhere in this proposal.
- `bucket_logic`'s existing 4-bucket, 6-bar computation is untouched — this proposal is a
  **display relabeling** of `clears_all_bars`/`fails`/`cannot_assess` plus **one new
  display-only split predicate** applied only to members already computed as
  `passes_with_flag`. The rubric YAML, the `bucket` field values, and
  `magnesium-guide-data.ts` are not edited by this doc.
- The מומלץ/טוב split (AMENDED) is a set-membership/identity predicate over
  already-computed bar states — "is the non-PASS set exactly `{dose_adequacy}`" — not a
  count, sum, or threshold comparison, and it is consistent in kind with how
  `bucket_logic.evaluation_order` already uses set/existence language ("at least one bar
  is FLAG or CANNOT-VERIFY") rather than a cardinality comparison.
- **Nutrition D7 co-sign received 2026-07-04**, replacing Product's original
  count-threshold draft (which Nutrition correctly ruled a violation — a
  count-then-compare-to-cutoff is a composite sum by construction even if unstored) with
  `dose_adequacy_sole_caveat`. Product independently verified the ruling and the
  replacement against the live rubric YAML and co-signs it. See status banner at top of
  this doc and `01_framework/nutrition/supplement_guides_tier_mapping_cosign_v1.md`.

---

## 7. Tier ordering & display

**Ordered display (מומלץ מאוד → מומלץ → טוב → לא מומלץ) is acceptable**, with
לא ניתן להעריך shown separately below, not interleaved into the ordered spectrum. This
is not new precedent — the current live page already orders its 4 buckets top-to-bottom;
this proposal only renames and re-splits one of them. What keeps ordered tiers honest and
distinct from the rejected ranking: (1) there is no ordering *within* a tier — products in
the same tier display in a stable, non-scored order (catalog/scrape order), never
re-sorted by any derived value; (2) every tier boundary is a stated rule pointing at real
bars, not a magnitude; (3) the tier name itself is the entire signal shown — no score, no
percentile, no "N/6" ever accompanies it.

---

## 8. What this doc does NOT decide

- Exact Hebrew copy for the tier sub-captions, the מומלץ מאוד empty-state line, or the
  cannot_assess section heading — Content Agent drafts, both gates (Content +
  Adversarial QA) sign off, per the standing content sign-off hard rule. This doc gives
  the categorical logic only.
- Whether to also update `headlineFinding.body[2]`'s literal phrase
  "זו הרשימה המעשית להתחיל ממנה:" — that string uses the exact framing being retired and
  needs a matching content edit once the 4-tier copy lands. Flagging it here so it isn't
  missed; not resolving the wording myself.
- Implementation (new component, prop, or computed field) — Frontend Agent's call once
  scope is approved; Product approves scope only (D11).

---

## 9. Required sign-offs before Frontend builds

1. ~~**Nutrition D7 co-sign** (rubric owner)~~ — **RECEIVED 2026-07-04**, with the §2
   amendment (`dose_adequacy_sole_caveat` replaces the original count-threshold draft).
   Product independently verified and co-signs the amended predicate. D7 is closed,
   dual-keyed Nutrition + Product.
2. **C3 challenge** — per the coordinator, C3 independently agreed with Nutrition's
   anti-drift objection to the original count-threshold draft. Recommend one more C3 pass
   specifically on the amended `dose_adequacy_sole_caveat` predicate and on §5's
   defensibility argument, since C3's agreement so far is on record as directed at ruling
   out the *retired* mechanism, not yet as an affirmative sign-off on the *replacement*.
3. Content + Adversarial QA two-gate on all new consumer-facing strings once the above
   land (per `content_signoff_hard_rule` — orchestrator does not author these inline).
   Still fully outstanding — no tier-related consumer string has been drafted.

---

## Return Contract

```json
{
  "task": "TASK-504-magnesium-4tier-recommendation",
  "agent": "Product Agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\product\\magnesium_guide_recommendation_tiers_v1.md",
      "sha256": "98278365ac2a4b4e326d531ec852fbe37c980eb7843c40a7557d6402e4349f4d"
    }
  ],
  "counts": {
    "total_products_in_corpus": 18,
    "clears_all_bars_of_18": 0,
    "passes_with_flag_of_18": 5,
    "fails_of_18": 12,
    "cannot_assess_of_18": 1,
    "recommended_tier_split_of_18": {
      "מומלץ מאוד": 0,
      "מומלץ": 2,
      "טוב": 3,
      "לא מומלץ": 12,
      "לא ניתן להעריך (outside tiers)": 1
    },
    "source": "C:\\bari_wt_t504\\bari-web\\src\\lib\\guides\\magnesium-guide-data.ts (18 buildProduct() calls, read in full); cross-checked against 01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml bucket_logic.evaluation_order"
  },
  "commands_run": [],
  "amendment": {
    "date": "2026-07-04",
    "change": "passes_with_flag split rule replaced: count-threshold (1 vs >=2 non-PASS bars) -> dose_adequacy_sole_caveat (set-identity predicate)",
    "reason": "Nutrition D7 ruled (C3 independently agreed) the count-threshold is a composite sum by construction, violating supplement_guides_bar_rubric_v1.yaml anti_drift_invariant Hard Rule 1",
    "verified_against": [
      "01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml (recommendation_tier_mapping, passes_with_flag_split_rule)",
      "01_framework/nutrition/supplement_guides_tier_mapping_cosign_v1.md"
    ],
    "result_on_current_corpus": "identical — Altman Citrate 120 + Nutricare WELL -> מומלץ; Supherb Citrate+B6, Altman Bisglycinate, NT L.C. Anti Leg Cramps -> טוב",
    "product_action": "co-signed the amended predicate; this doc updated in place to record it, not re-litigated"
  },
  "not_done": [
    "Nutrition D7 co-sign — RECEIVED 2026-07-04 on the amended dose_adequacy_sole_caveat predicate; dual-keyed with Product",
    "C3 affirmative sign-off specifically on the REPLACEMENT predicate (dose_adequacy_sole_caveat) and on the defensibility argument — C3's agreement so far is on record against the retired count-threshold mechanism, not yet as approval of the replacement",
    "Exact Hebrew copy for new tier labels/sub-captions/empty-state line — Content Agent + two-gate, not drafted here",
    "headlineFinding.body[2] retains the retired 'הרשימה המעשית להתחיל ממנה' phrase inline — needs a matching content edit, not made here",
    "No code, rubric, or data file was edited by Product — this doc is proposal/record-of-decision only; the rubric YAML edit was made by Nutrition under its own D7 authority"
  ],
  "acceptance_test": {
    "spec": "Produce a decision doc mapping bar-states to 4 named tiers, honest and traceable to visible bars, with per-product assignment for all 18, cannot_assess ruling, empty-tier handling, defensibility argument, anti-drift confirmation, and sign-off flags.",
    "result": "PASS — all elements present in this doc; all counts and the amended rubric block verified against the live data file and rubric YAML before being stated (Hard Rules 9-10); zero numbers invented; the amendment itself was independently verified against source, not taken on the coordinator's assertion alone"
  }
}
```
