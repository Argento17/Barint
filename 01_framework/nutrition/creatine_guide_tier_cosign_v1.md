# Creatine Guide — Nutrition D7 Bar-State Accuracy Co-Sign (TASK-504 Wave 2)

**Task:** Nutrition D7 accuracy co-sign on Product's per-product bar-state assignments for
the creatine guide (31 products), per `03_operations/reports/product/creatine_guide_recommendation_tiers_v1.md`.
The 4-tier MECHANISM (`dose_adequacy_sole_caveat`, bucket_logic) is dual-keyed already from
the magnesium pass and is **not re-litigated here** — see
`01_framework/nutrition/supplement_guides_tier_mapping_cosign_v1.md` for that ruling.
**Author:** Nutrition Agent · **Date:** 2026-07-04
**Status:** CO-SIGNED WITH ONE DATA CORRECTION (California Gold Nutrition price_fairness
cascade — see §3). No tier outcome changes as a result.

---

## 0. What was checked

- Product's mapping doc in full (`creatine_guide_recommendation_tiers_v1.md`, all 31 rows,
  §1–§9).
- The rubric's creatine-specific bar rules (`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`
  — `bars`, `bucket_logic`, `recommendation_tier_mapping`, `display_suppression_rule`).
- The live data file: `git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts`
  at commit `9546878cf90f069fe12c1467d8d12966b40221cf` — independently re-pulled and read in
  full (997 lines, all 31 `mkBadge(...)` calls), not taken on Product's transcription.

Every one of the 31 rows was re-derived independently from the raw `mkBadge()` arguments
(form_label, dose_label, doseHonesty, certTier, cert_label, price_per_3g_label) against the
rubric's stated thresholds, rather than checked only against Product's table.

---

## 1. Per-product bar-state accuracy — verdict: ACCURATE, zero misassignments

All 31 rows in Product's §4 table match an independent re-derivation from the pulled data
file. Detail on the requested tier-boundary cases:

**The 3 מומלץ מאוד (Thorne, Momentous, BPN) — confirmed all-PASS.**
- Thorne (worldwide, `wb-thorne-creatine`): 5g honest (dose P), monohydrate (form P),
  `certTier: "directory_verified"`, NSF id 1204244 (3rd-party P), $0.27 ≤ $0.28125 pool-PASS
  ceiling (price P), no-UL (safety P, by construction), disclosed unambiguous 5g (label P).
  Six of six PASS.
- Momentous (`wb-momentous-creatine`): same pattern, NSF id 1285010, price range
  "~$0.19–0.26" midpoint = **$0.225** (independently recomputed, matches Product's figure),
  ≤ $0.28125 → PASS. Six of six PASS.
- BPN (`wb-bpn-creatine`): NSF id 1635096, price range "~$0.16–0.21" midpoint = **$0.185**
  (independently recomputed), PASS. Six of six PASS.

**The 1 מומלץ (BioSteel) — confirmed dose is genuinely the SOLE caveat.**
`wb-biosteel-creatine`: 2.5g stated per single measured serving. `dose_adequacy`: 1.5 ≤ 2.5 <
3.0 → FLAG (correct — this is the rubric's own FLAG band, not fairy-dust). Every other bar
independently re-checked and confirmed PASS: form = monohydrate (P), `certTier:
"directory_verified"` NSF id 1292599 (P), price range "~$0.17–0.24" midpoint = **$0.205**
(independently recomputed) ≤ $0.28125 (P), safety = PASS-by-construction, label = 2.5g stated
as a specific, unambiguous number (P). Caveat set = exactly `{dose_adequacy}` → מומלץ per the
`dose_adequacy_sole_caveat` predicate. This is the corpus's single clean demonstration of the
split rule's intended positive case, correctly identified.

**The 7 לא מומלץ.**
- **2 HCl dose fails (Kaged, Con-Cret):** both disclose 0.75g/dose. 0.75 < 0.5×3.0 = 1.5 →
  `dose_adequacy` = FAIL, correctly triggering `bucket_logic`'s `fails` (rule 1, checked
  before any CANNOT-VERIFY routing). Both also independently confirmed FAIL on `price_fairness`
  (₪4.75 and ₪5.38, both > ₪1.86 = 2.0× the ₪0.93 median) — a genuine double-fail, not a
  single-bar trigger. `form_absorption` on both correctly resolves to **FLAG, never FAIL**
  (see §4 below).
- **4 zero-quantification fails (Super Effect ×2, Sport GS, MyProtein Tablets):** all four
  name "קריאטין"/"Creatine" on-pack with **zero gram figure anywhere** in the pulled data
  (`dose_label: "לא מפורט"` in all four `mkBadge()` calls). This is exactly the rubric's
  `label_transparency` FAIL definition ("named active ingredient appears with ZERO
  quantification anywhere") — correctly distinguished from CANNOT-VERIFY, which requires an
  ambiguous-but-present number. `form_absorption` correctly resolves PASS on all four (the
  form itself — "מונוהידראט" — is named and known; only the gram figure is missing, which is
  the exact "Tink Oxide-520" pattern the rubric names: form-known/dose-unknown is not a blend
  and still resolves). `dose_adequacy` is independently CANNOT-VERIFY on all four (no daily
  figure to compare against 3.0g), but `bucket_logic`'s evaluation order checks FAIL before
  CANNOT-VERIFY, so all four correctly land in `fails` → לא מומלץ, not `cannot_assess`. Product's
  §5 discussion of this exact contrast is correct.
- **Naked Nutrition — the one `third_party_verification` FAIL:** independently confirmed
  against the pulled data (`wb-naked-creatine`) — the row's own `insightLine`/`rowVerdict`
  states the "NSF-certified" claim was checked and no matching registry entry was found
  ("לא אותר רישום תואם במאגר"). This is the rubric's FAIL sub-case (claim checked and
  contradicted), correctly distinguished from every FLAG row in the corpus (claim either
  unchecked, or checked-but-blocked/inconclusive — e.g. Applied Nutrition's Informed-Sport
  checker site refusing access on every attempt, correctly FLAG not FAIL). This distinction
  is scientifically load-bearing and Product applied it correctly. Note for the data model:
  the raw `certTier` field literally stores `"manufacturer_stated"` for this row — identical
  to every FLAG row — so the FAIL classification is correctly derived from the row's own
  prose (checked-and-not-found), not from the `certTier` enum value alone, which does not yet
  distinguish "unchecked" from "checked-and-contradicted." Recommend a future `certTier` enum
  value (e.g. `"checked_not_found"`) so this distinction is data-modeled rather than requiring
  a per-row prose read at every future rubric-application pass — a build hygiene note, not a
  tier-accuracy defect today.

**Thorne's IL-vs-worldwide split (same brand, different verification status per regional
SKU) — confirmed correct.** Thorne's US-market SKU (`wb-thorne-creatine`) is directory-verified
(PASS); Thorne's Israeli/iHerb-listed SKU (`693749006350`) is explicitly noted in its own
`rowVerdict` as not separately checked against the registry, and correctly resolves to FLAG.
This is the rubric's own `per_product_discipline` working as designed — a certification claim
is verified per SKU/listing, not per brand, and a brand's US NSF registration does not
transitively certify a different regional retail listing of the same nominal product.

---

## 2. Headline finding — confirmed exactly right

**0/18 Israeli products carry `third_party_verification` = PASS; 7/13 worldwide products
do.** Independently re-checked every `certTier` value in both raw arrays:

- Israeli (18): every row is either `null` (no claim — CANNOT-VERIFY) or
  `"manufacturer_stated"` (FLAG). Zero rows carry `"directory_verified"`.
- Worldwide (13): 7 rows carry `"directory_verified"` (Thorne, Momentous, Klean Athlete, BPN,
  MegaFood, Sports Research, BioSteel — matching the file's own header comment and the
  RT-1 red-team fix noted at the top of the file regarding Sports Research's primary SKU).

Because `third_party_verification` is therefore never PASS for any Israeli row, and the
`dose_adequacy_sole_caveat` split routes any caveat set containing a non-dose bar to **טוב**
(never מומלץ or מומלץ מאוד), the conclusion **"the Israeli shelf structurally cannot reach
מומלץ or מומלץ מאוד today"** is a mechanically correct, fully traced consequence of the
certification data — not an overstatement. Confirmed exactly as stated. This is the single
most consumer-relevant fact in this guide and it is accurately derived.

---

## 3. Premise Flag 1 — California Gold Nutrition price pool inclusion: RULING

**Ruling: the ₪0.97 figure must be excluded. `price_fairness` for California Gold Nutrition
must display as CANNOT-VERIFY, not a computed PASS/FLAG/FAIL band. This is a data correction
for the build, not a discretionary call.**

The rubric's own `price_fairness` state definition is unambiguous and non-optional on this
exact point: *"the daily effective dose itself is CANNOT-VERIFY (no denominator computable —
this state cascades from the `dose_adequacy` bar's own CANNOT-VERIFY, it is **not
independently re-derived**)."* California Gold Nutrition's `dose_adequacy` is CANNOT-VERIFY
(0.75g/capsule stated, daily capsule count undisclosed — the rubric's own verbatim worked
example for this state). The cascade instruction is explicit and admits no exception: whatever
arithmetic path produced "₪0.97 ל-3 גרם" in the live data (most likely a straight
price-per-gram-of-active-ingredient unit calculation — price ÷ 0.75g × 3g — which is
computable without knowing the daily serving count), it answers a **different question** than
the one `price_fairness` is defined to answer (price normalized to "one day's worth of the
effective dose," which requires the daily-dose denominator this product does not disclose).
Displaying a determinate ₪ figure here would silently answer a question the rubric says is
unanswerable for this product, which is exactly the failure mode the cascade rule exists to
block.

**Recomputed Israeli median, CGN excluded:** the remaining 9 price-disclosed rows are
0.52, 0.61, 0.65, 0.77, 0.89, 1.03, 1.20, 4.75, 5.38 → median (5th of 9) = **₪0.89**, not
₪0.93. Independently re-derived from the pulled data, matching Product's own computation in
§2 of the source doc.

**Does this recompute change any other product's tier? No — independently re-checked, not
just taken on Product's assertion.** New thresholds: PASS ≤ ₪1.1125, FLAG ₪1.1125–1.78, FAIL
> ₪1.78 (vs. old ₪1.1625 / ₪1.1625–1.86 / >₪1.86).
- MyProtein Impact Creatine (₪1.03): PASS under both old and new ceiling (1.03 ≤ 1.1125). No change.
- All In (₪1.20): FLAG under both (1.1125 < 1.20 ≤ 1.78 and 1.1625 < 1.20 ≤ 1.86). No change.
- Kaged (₪4.75) / Con-Cret (₪5.38): FAIL under both (both figures exceed both the old ₪1.86
  and new ₪1.78 FAIL ceiling by a wide margin). No change.
- Every other priced Israeli row sits well inside PASS under both medians.

**Does this change California Gold Nutrition's own tier? No.** `bucket_logic`'s evaluation
order resolves CGN via `dose_adequacy` = CANNOT-VERIFY at step 2 (no bar on this product is
FAIL — `label_transparency` is FLAG, not FAIL, per §5 of Product's doc, independently
confirmed correct: a real per-unit number is disclosed, so this is not the zero-quantification
FAIL pattern). `price_fairness`'s state does not enter `bucket_logic`'s evaluation at all for
a product already routed at the dose-CV step. CGN's tier remains **לא ניתן להעריך**, unchanged.

**Required build correction:** display CGN's price badge as "לא ניתן להעריך" (or the
guide's standard CANNOT-VERIFY price treatment), not "₪0.97 ל-3 גרם," and use ₪0.89 — not
₪0.93 — as the Israeli pool median in any guide-level copy or footnote that states the
median figure. **Flag for whoever next touches the rubric YAML:** the rubric's own cited
snapshot at `price_fairness.boundary_method.versioning_note` ("0.93 ₪/3g Israeli creatine
pool... dated 2026-07-04") should be corrected to ₪0.89 for consistency with this ruling —
not fixed here (out of this doc's scope; a rubric-file edit needs its own D6/D7 pass per the
standing governance discipline), but noted so the two artifacts do not silently disagree.

---

## 4. Premise Flag 2 — HCl form_absorption = FLAG, never FAIL: CONFIRMED, no correction

Independently re-checked against `creatine_evidence_cosign_v1.md §3.1` and the rubric's own
creatine `form_absorption.FLAG` definition: alternative forms (HCl, buffered/"alkaline,"
ethyl ester, citrate, malate) are "evidence-orphaned for a premium claim," **explicitly not
inferior or unsafe** — using FAIL here would misstate the evidence in the harsher direction,
which the standing evidence co-sign bans outright (§2.4's banned-claim list: no assertion that
alternative creatine forms are unsafe or lower-quality).

Both HCl rows in the live data (Kaged `850045966478`, Con-Cret `682676700646`) carry
`form_absorption` = FLAG in Product's table, matching this rule exactly. Their `לא מומלץ`
placement is driven entirely by their independently-confirmed `dose_adequacy` FAIL (0.75g <
1.5g floor) and `price_fairness` FAIL (₪4.75 / ₪5.38, both >2.0× median) — never by the form
bar. No inferiority/unsafety framing appears anywhere in either row's `insightLine`,
`rowVerdict`, or `limitingFactors` in the pulled data (both correctly frame the finding as
"no evidence of advantage that justifies the price," not "HCl is worse"). Confirmed clean.
No correction needed.

---

## 5. Confirmation: no tier outcome depends on an unverified bar-state

Every PASS/FLAG/FAIL/CANNOT-VERIFY call across all 6 bars × 31 products was re-derived from a
literal field in the pulled `mkBadge()` data (form_label, dose_label, doseHonesty, certTier,
price_per_3g_label) or a directly-quoted sentence in the row's own `insightLine`/`rowVerdict`
(the Naked Nutrition checked-not-found distinction, the Thorne IL-not-separately-checked
distinction). Nothing in the 31-row table rests on an inference not traceable to the source
file or the rubric's own stated threshold. The one correction identified (§3, CGN's
`price_fairness` cascade) is a **display-state fix that does not move CGN's own tier or any
other product's tier** — independently verified by re-running the classification against both
the old (₪0.93) and new (₪0.89) medians and finding zero divergence in outcome.

---

## 6. Sign-off

**Co-signed** (Nutrition D7, bar-state accuracy) with the one data correction in §3 above. The
mechanism itself (dual-keyed at the magnesium pass) is not touched. Recommend the standing C3
independent-challenge pass and the Content + Adversarial QA two-gate proceed as Product's §9
already scopes them — this co-sign does not substitute for either.

**Not decided here:** exact Hebrew copy for the CANNOT-VERIFY price treatment on the CGN row,
or whether/how the median correction is stated in consumer-facing copy — Content Agent drafts,
both gates sign off, per the standing content discipline. No rubric or data file was edited by
this doc.

---

## Return Contract

```json
{
  "task": "TASK-504-creatine-nutrition-d7-cosign",
  "agent": "Nutrition Agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\01_framework\\nutrition\\creatine_guide_tier_cosign_v1.md",
      "sha256": "0344760965d4ba4b904bcbd4cd47d2e918f4621ec2d1b9fce0381b9f9fe0e87c"
    }
  ],
  "counts": {
    "total_products_reviewed": 31,
    "israeli_of_31": 18,
    "worldwide_of_31": 13,
    "misassignments_found": 0,
    "data_corrections_required": 1,
    "tier_outcomes_changed_by_correction": 0,
    "third_party_directory_verified_of_31": 7,
    "third_party_directory_verified_israeli_of_18": 0,
    "third_party_fail_checked_not_found_of_31": 1,
    "price_pool_median_israeli_ils_per_3g_asfiled": 0.93,
    "price_pool_median_israeli_ils_per_3g_corrected": 0.89,
    "price_pool_median_worldwide_usd_per_3g": 0.225,
    "products_rechecked_against_recomputed_median_for_band_flip": 4,
    "products_that_flipped_band_under_recomputed_median": 0,
    "hcl_products_confirmed_form_flag_not_fail": 2,
    "zero_quantification_label_fails_confirmed": 4,
    "source": "git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts @ 9546878cf90f069fe12c1467d8d12966b40221cf (997 lines, read in full, independently re-pulled); cross-checked against 01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml and 03_operations/reports/product/creatine_guide_recommendation_tiers_v1.md"
  },
  "commands_run": [
    {"cmd": "git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts > scratchpad/creatine-page-data.ts", "exit_code": 0},
    {"cmd": "git log -1 --format=%H origin/master -- bari-web/src/lib/comparisons/creatine-page-data.ts", "exit_code": 0}
  ],
  "not_done": [
    "Rubric YAML's own cited median snapshot (0.93) not corrected to 0.89 in this doc — flagged for whoever next edits the rubric file under its own D6/D7 pass; not edited here",
    "certTier enum expansion recommendation (checked_not_found vs unchecked) not implemented — a build hygiene note, not a blocking defect",
    "CGN price badge display fix (CANNOT-VERIFY, not computed figure) not implemented in the data file — proposal only, per delegation scope",
    "C3 independent challenge pass, Content + Adversarial QA two-gate — outstanding, per Product's own §9 sequencing, not this doc's scope",
    "No code, rubric, or data file edited — proposal/decision-record only, per delegation instruction"
  ],
  "acceptance_test": {
    "spec": "Verify per-product bar-state accuracy for creatine's 31 products, confirm the 0/18 Israeli directory-verification headline, and rule on the 2 premise flags (CGN price cascade, HCl form FLAG-not-FAIL), stating any required data/threshold correction precisely for the build.",
    "result": "PASS — all 31 rows independently re-derived from the pulled data file and confirmed accurate; headline finding confirmed exact; premise flag 1 (CGN price cascade) ruled and resolved with a stated, precise correction (CANNOT-VERIFY display, median 0.93->0.89) that independently verifies to zero tier-outcome change; premise flag 2 (HCl form FLAG-not-FAIL) confirmed correct with no correction needed."
  }
}
```
