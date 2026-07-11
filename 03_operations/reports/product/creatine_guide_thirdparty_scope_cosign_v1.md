# Creatine Guide — Third-Party Bar Suppression Scope: Product Agent Ruling (TASK-504)

**Task:** Mid-task co-sign request from the orchestrator (2026-07-04), triggered by the
`wb-*` benchmark split (this report's sibling,
`supplement_guides_abcd_relabel_cosign_v1.md`, §4) re-opening whether the domestic creatine
shelf differentiates at all once benchmark products leave the ranked bands.
**Reviewer:** Product Agent. Nutrition recomputing the distribution under domestic-scope in
parallel per the coordinator's note; this ruling was reached independently against the live
data file, not against Nutrition's parallel output.

---

## 0. Premise check (Hard Rule 10) — the handed-in premise is close but not exact

The routed question stated the mechanism as "a bar that is uniformly cannot-verify... gets
suppressed" and "no Israeli-shelf creatine carries independent third-party verification."
Verified directly against `C:\bari_wt_t504\bari-web\src\lib\guides\creatine-guide-data.ts`
(all 18 Israeli-shelf `buildProduct()` calls, third element of each `states` tuple = third-
party bar, per the file's own `bars(d,f,t,p,s,l)` key order):

| State | Count (of 18) | Products |
|---|---|---|
| `pass` (directory-confirmed) | **0** | none |
| `flag` (manufacturer-stated, unchecked) | **9** | ABE, MyProtein Impact, Optimum Nutrition, Thorne (IL/iHerb), California Gold (capsules), MyProtein Elite (IL), MyProtein Creapure (IL), Kaged HCl, Con-Cret HCl |
| `fail` (checked, not found) | **0** | none |
| `cannot_verify` (no claim at all) | **9** | NOW Foods, MuscleTech, All In, MyProtein Gummies, MyProtein Creapure Capsules, Super Effect ×2, Sport GS, MyProtein Tablets |

**Correction to the premise:** the second half — "0/18 achieve independent/registry-
confirmed verification" — is exactly right, and it is the part that matters for this
decision. The first half is imprecise: the bar is **not** uniformly `cannot_verify` under
either full-corpus or domestic-only scope (it's a 9/9 `flag`/`cannot_verify` split
domestically). This means the *existing* `display_suppression_rule` in
`supplement_guides_bar_rubric_v1.yaml` — trigger is "CANNOT-VERIFY, exactly and
exclusively, by construction" — does **not**, as literally written today, fire under either
scope. Whatever ships here is a **new, narrower rule**, not a reuse of the magnesium
precedent's exact trigger. I'm flagging this precisely so it isn't silently wired through
under the existing rule's authority — that would be the same class of quiet rule-widening
Nutrition already caught and rejected once this session (the count-threshold ruling). See §3.

---

## 1. Q1 — which scope, and does it avoid manufactured differentiation

**Recommendation: domestic-scope exclusion of the third-party bar from the domestic
B/C split**, not full-corpus inclusion. Single best option, no menu.

**Why domestic-scope is right, not a re-creation of the retired ranking problem:** the
"ranking supplements doesn't work" finding was about *manufacturing* differentiation among
products the engine itself says are substantively equivalent (monohydrate is monohydrate).
This is the opposite situation: dose adequacy, price, form (monohydrate vs. HCl), and label
completeness are **already-real, already-checked, categorical facts** for these 18
products, sitting unused because one uniformly-absent bar (third-party) was flattening all
of them into the same middle tier. Excluding a bar that provides **zero** discriminating
information across the entire domestic pool (0/18 PASS, 0/18 FAIL — nothing to
differentiate on) and *letting the bars that do carry real information determine the band*
is the same principle as the magnesium suppression rule (`missing_data_discard_doctrine`:
"unknown is acceptable... never punish/cap a product for a data gap") — not a new one.

**Why full-corpus scope is the worse choice, not just the more conservative one:** with
`wb-*` items providing real PASS/FAIL variance, the bar stays "live" and blocks every
domestic product from ever exceeding "טוב"/C — but it does this **indiscriminately**,
collapsing a ₪0.52/3g well-labeled 4.2g monohydrate (NOW Foods) and a ₪5.38/3g
undisclosed-ratio HCl product into visually adjacent territory (the HCl products still fall
to D on their own dose FAIL, but everything else compresses into one C-band mush). That is
not "more honest" — it is a resolution loss that actively hides the real signal a shopper
needs (price spread, dose-floor vs. comfortable margin, real vs. fairy-dust labeling) behind
a caveat that is uniformly true of the entire market and therefore uniformly uninformative
for a *domestic* buying decision. Full-corpus scope answers "how does Israel compare to the
world" (a real, useful, separate question — that's what the BENCHMARK section is for);
domestic-scope answers "which of the things I can actually buy here is the better pick" (the
guide's actual job). Conflating the two into one band computation is the mistake, not
whichever scope is chosen — which is exactly why the two need separating.

---

## 2. Q2 — is domestic banding on dose/form/price/label honest signal or noise

**Honest signal**, verified against the same 18-row table, not asserted:

- **Price**: real, large, non-cosmetic spread — ₪0.52 to ₪5.38 per 3 g-equivalent across
  the 18 rows (a >10x range). This is exactly the kind of number the guide's own
  `price_fairness` bar and `default_pick_rule` already exist to surface; it is not invented
  precision layered on equivalent products.
- **Dose**: binary categorical (PASS ≥3g / FLAG 1.5–3g / FAIL <1.5g), not a fabricated
  points scale — 5 of 18 already resolve to FAIL or CANNOT-VERIFY on real disclosure/floor
  facts (Kaged, Con-Cret: 0.75g HCl; Super Effect ×2, Sport GS, MyProtein Tablets: zero gram
  disclosure at all — a real labeling-honesty finding, not noise).
- **Form**: monohydrate vs. HCl is a real compound-identity fact already governed by the
  rubric's existing FLAG (not FAIL) treatment for HCl — "evidence-orphaned for a premium
  claim," per the standing creatine evidence co-sign, so this correctly avoids overstating
  the case against HCl while still surfacing it.
- **Label transparency**: PASS/FAIL here is literally "does the label state a gram figure at
  all" — the Super Effect/Sport GS/MyProtein Tablets zero-disclosure finding is real, not
  manufactured.

None of this introduces a new composite: bands are still pure categorical bar-state lookups
(`bucket_logic` + `dose_adequacy_sole_caveat`, unchanged), and `tier_ordering_no_within_tier_sort`
already forbids using price (or anything else) to rank *within* a band. The risk the original
ruling was written to prevent — small, real differences inflated into a false precision
ordinal — does not recur here because nothing within a band gets sub-ranked; the band
boundaries themselves are drawn from real pass/fail facts, several of which (price spread,
zero-disclosure labeling) are large and unambiguous, not marginal.

**The frame the task proposed — "most standard monohydrate on the Israeli shelf is fine;
avoid the HCl-novelty and undisclosed-dose ones; order abroad for lab-verified" — is honest
and useful**, provided it ships with the mandatory disclosure in §4 attached to the top
domestic band, not as a free-floating claim that domestic monohydrate is "as good as"
anything.

---

## 3. Mechanical gap this scope choice creates — route to Nutrition, do not let Frontend invent it

Excluding the third-party bar from the **displayed-bars set** the `dose_adequacy_sole_caveat`
predicate runs over produces an unhandled case the current rubric text does not define. Four
products — ABE, MyProtein Impact, Optimum Nutrition, Thorne (IL/iHerb) — have `flag` on
third-party and `pass` on every other bar (dose, form, price, safety, label all PASS). With
third-party excluded from the displayed set, their caveat set among the remaining 5 bars is
**empty**, which fits neither of the predicate's two defined branches (`exactly
{dose_adequacy}` → B; `contains a non-dose bar` → C).

**Recommended resolution (for Nutrition to formally rule, not for this report to decide
unilaterally):** an empty displayed-caveat set is a strictly *cleaner* result than a
dose-only caveat, so it belongs in the same tier as `{dose_adequacy}` — i.e., extend the
predicate's first branch to "empty set OR exactly `{dose_adequacy}` → מומלץ/B." This is
still a pure set-membership test (is the set a subset of `{dose_adequacy}`), introduces no
cardinality comparison, and does not touch `bucket_logic` (which still correctly keeps these
4 products in `passes_with_flag`, never `clears_all_bars`, since their real third-party state
is `flag`, not `pass`). Flagging this explicitly so it lands as a scoped rubric amendment
with its own one-line rationale, the same discipline Nutrition applied to the count-threshold
rejection — not something Frontend quietly resolves during implementation.

**Consequence to confirm, not treat as a surprise:** Band A (`clears_all_bars`, "A" per the
sibling report's relabel) stays **empty for domestic creatine even under domestic-scope**
suppression, because bucket assignment is computed off the real, unsuppressed 6-bar state
(third-party is genuinely never PASS domestically) — this is unaffected by display-layer
exclusion, per the rubric's own "display rule only, never a computation rule" carve-out. The
practical effect of domestic-scope is repopulating Band **B**, not Band A: the four
empty-caveat products above move from what would otherwise be a uniform C into B, and the
remaining domestic pool (Creapure Capsules, real price-fairness gaps, etc.) stays in C. This
mirrors, rather than undoes, magnesium's honest empty-top-tier precedent.

---

## 4. Q3 — honest framing for the domestic top band

**Required, non-collapsible caption attached to every domestic Band B product** (Content to
author exact wording, two-gate as usual; this is the substance requirement, not the copy):

States three facts, in this order, every time: (1) this is the best a domestic-shelf product
can show on what Bari can check locally; (2) it has **not** passed an independent
registry check — Israel's creatine shelf carries zero registry-confirmed products today, a
market fact, not a knock on this specific brand; (3) the BENCHMARK section on the same page
shows what registry-confirmed monohydrate looks like and how to get it. This keeps Band B
an honest "best of what's checkable here" claim rather than letting a shopper read it as "as
rigorously verified as the benchmark" — the exact confusion the benchmark/ranked split in
the sibling report exists to prevent. The caption must sit with the badge itself (same
"visible, not buried" rule the safety bar's `rendering_rule` already establishes for FAIL
states) — never only in the page's intro paragraph.

---

## Return Contract

```json
{
  "task": "TASK-504-creatine-thirdparty-suppression-scope-product-ruling",
  "agent": "Product Agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\product\\creatine_guide_thirdparty_scope_cosign_v1.md",
      "sha256": "pending — compute post-write"
    }
  ],
  "counts": {
    "domestic_creatine_products_reviewed": 18,
    "domestic_third_party_pass": 0,
    "domestic_third_party_flag": 9,
    "domestic_third_party_fail": 0,
    "domestic_third_party_cannot_verify": 9,
    "products_hitting_empty_caveat_set_under_domestic_scope": 4,
    "empty_caveat_set_products": ["ABE Creatine Monohydrate Micronized", "MyProtein Impact Creatine (250g)", "Optimum Nutrition Micronized Creatine Powder", "Thorne (IL/iHerb) Creatine"],
    "domestic_price_range_ils_per_3g": "0.52 to 5.38",
    "source": "C:\\bari_wt_t504\\bari-web\\src\\lib\\guides\\creatine-guide-data.ts, Israeli-shelf block, lines 254-512, all 18 buildProduct() states tuples read directly"
  },
  "commands_run": [
    {"cmd": "Read creatine-guide-data.ts lines 254-513 (full Israeli-shelf block)", "exit_code": 0}
  ],
  "not_done": [
    "Nutrition's parallel domestic-scope recompute — this ruling reached independently, needs merge per coordinator's note",
    "Formal rubric amendment text for the empty-caveat-set extension (recommended here, not authored as a rubric edit — Nutrition-owned file)",
    "Exact Hebrew caption copy for the Band B disclosure — Content + two-gate, substance requirement only given here",
    "Does not close TASK-504 or any sub-task"
  ],
  "acceptance_test": {
    "spec": "Recommend one scope (no menu) for the third-party suppression fork with reasoning tied to the anti-manufactured-differentiation principle; answer whether domestic dose/form/price/label banding is honest signal citing real data; give required framing for a domestic top band; verify the handed-in premise against source before ruling.",
    "result": "PASS — premise corrected against direct source read (9/9 flag/cannot_verify split, not uniform cannot_verify, under either scope); domestic-scope recommended with reasoning distinguishing real-signal exclusion from manufactured differentiation; Q2 answered with cited price/dose/label variance; Q3 answered with a 3-part mandatory disclosure requirement; flagged one unhandled mechanical edge case (empty displayed-caveat set, 4 named products) for Nutrition to formally resolve rather than leaving it for Frontend to guess during implementation."
  }
}
```
