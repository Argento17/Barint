# D7 Co-Sign: C-N1-1 Metric Substitution — Dual Gate
**Reviewer:** Product Agent (D7 lane)
**Input spec:** `matrix_signal_redesign_v2.md` §3 and §3.3 (the dual gate proposal)
**Original condition:** C-N1-1 in `d7_cosign_dechain_v1.md`
**Probe evidence:** `matrix_signal_probe_v1_report.txt` (the binary test that failed at 72.3% combined / 62.4% high-confidence)
**Task:** TASK-395
**Date:** 2026-06-25
**Verdict: CO-SIGN WITH CONDITIONS**

---

## What This Ruling Does and Does Not Authorize

This ruling accepts the Nutrition Agent's proposed substitution of the binary 90%-accuracy gate with
a dual gate (B1 + B2 + B3) as the operative condition for C-N1-1. It does NOT authorize any engine
code change, any flag flip, or any NOVA lookup deactivation. The formula redesign in §2 of
`matrix_signal_redesign_v2.md` remains a D6 proposal — that co-sign is handled separately. This
ruling is limited to: does the metric substitution preserve the original activation intent, and are
the thresholds defensible?

---

## Question 1: Does the Dual Gate Preserve the Original Intent?

**Yes — with one important caveat addressed by the conditions below.**

The original C-N1-1 intent, quoted from `d7_cosign_dechain_v1.md`, was:

> "Component B (matrix signal) must be validated for label-derivability on a minimum 50-product
> sample from the live corpus before the NOVA lookup is deactivated. Accuracy floor: the
> refined-starch markers must fire on >= 90% of products where the ingredient list contains only
> refined-grain + fat + sugar combinations."

The intent had two components:
1. Coverage — does the signal fire at all on the relevant products? (B3 addresses this directly)
2. Directional accuracy — when it fires, does it correctly identify refined vs. whole? (B1+B2 address this)

The binary 90%-accuracy gate was a proxy for both. The Nutrition Agent's argument that it is the
wrong proxy for a continuous signal is correct, and the probe data confirms it: the 88-product
MIXED_MARKERS_WRONG_DIRECTION failure class (16.9% of corpus, source: `matrix_signal_probe_v1_report.txt`
line 75) is not a formula failure — it is a position-blindness failure that produces wrong
direction on mixed products regardless of how the threshold is set. A binary test penalizes a
formula for correctly scoring these products as mixed.

The 123 GENUINELY_MIXED products (23.5% of corpus, source: probe report line 74) confirm that
forcing binary classification on this corpus is structurally wrong: the right answer for many of
them IS near-50, not a classified WFP or RD. A dual gate that audits calibration anchors (B1)
and ranking fidelity (B2) on clear-class products, while counting mixed products via B3 coverage,
directly measures what matters.

The caveat: the dual gate must still hold the signal accountable on mixed products. It cannot be
a dodge. The ranking gate (B2) is what does this — it applies within Tier 3 (hard-mixed products)
and requires that among ranked pairs, the more-whole product scores higher. B2 with ≥95% pass rate
on ranked pairs within the hard-mixed tier IS accountability on the hard cases. The dual gate
does not let the signal fail silently on the 88-product class; B2 directly tests it.

**Intent preserved? Yes.** The substitution is a precision upgrade, not a goalpost move.

---

## Question 2: Are the Thresholds Defensible?

Reviewing each threshold individually:

### B1: ≥60 for whole-dominant (≥50% by stated label weight), ≤45 for refined-dominant

**Accepted.** The 60/45 split preserves a 15-point gap between the clear zones, which is wide
enough that a correctly calibrated formula does not straddle it by accident. The ≥80 sub-condition
for single-ingredient whole foods and ≤25 for classic refined (flour+sugar+fat, no whole food) are
the strictest anchors and appropriately so — these are products where no ambiguity exists and the
formula must be unambiguous.

One threshold I flag: the 90% pass rate on B1. This is the same number as the original binary
gate, but applied to a stricter, human-verifiable gold set (not the heuristic ground truth). On
a gold set of ~60–75 products correctly annotated by label inspection, 90% means ≤7 misses are
tolerated. This is tight and correct. Accept.

### B2: ≥95% on ordered pairs

**Accepted — this is the right gate and the harder one.** A 95% pair-accuracy requirement on
clearly-ordered product pairs means the formula can be wrong on roughly 1 in 20 ranking
judgments. For a signal that is a *continuous input* to a composite score (not a direct
consumer-facing grade), this is the correct bar. The Nutrition Agent is right that 95% pair
accuracy is harder than it sounds — it fails on any product where the formula reverses a
label-derivable rank. Accept.

### B3: ≥95% coverage on parseable Hebrew labels

**Accepted.** The probe reports 8/520 no-marker products (1.5%), source: probe report line 50.
The B3 condition requires ≥95% coverage, meaning ≤5% no-marker rate on parseable text. The
current 1.5% already clears this bar on the flat-count formula — the redesigned formula must
clear it too. B3 ensures the coverage requirement from the original C-N1-1 spirit is retained
as a hard check, not just assumed. Accept.

**No threshold is arbitrary. All three are defensible.**

---

## Question 3: Does the Dual Gate Still Hold the Signal Accountable on Mixed Products?

This is the crux and the question I spent the most time on.

The fear: that by excluding GENUINELY_MIXED products from the binary check, the gate creates a
loophole for the 88-product MIXED_MARKERS_WRONG_DIRECTION class — the products that broke the
first attempt. If these products are quietly moved into the "mixed" bucket and B1/B2 only run on
the clear-class products, then the gate is easier to pass without actually fixing the formula.

**The answer depends entirely on whether Tier 3 (hard-mixed) products are included in B2.**

The spec states B2 applies to "every ordered pair (P_whole, P_refined) in the gold set where
P_whole is clearly more whole-food-dominant than P_refined by label inspection." The Tier 3
definitions in §4.2 of the redesign spec include products from the hard-mixed failure class (the
fitness cracker, the granola variants, the mixed-flour breads). The spec's required rank ordering
within Tier 3 (§4.3) includes pairs like "גרנולה פירות (oats 43%) > מוזלי קראנצ'י (oats 38%)"
— these ARE the hard cases, and they ARE tested by B2.

**The condition I add:** The gold set must include Tier 3 products in the B2 pair set.
Specifically, the minimum pair set in §4.3 (3 pairs) is the floor, not the ceiling. The gold set
must generate at least 10 Tier 3 pairs to give B2 statistical meaning. With ~15 Tier 3 products
in a 60–75 product gold set, this is achievable.

If B2 is run only on Tier 1 vs Tier 2 cross-tier pairs (the easy case: oat granola vs. white
flour cookie), the 95% pass rate becomes trivial. That is not the gate I am co-signing. The gate
I am co-signing includes within-tier Tier 3 pairs as a required component of B2.

---

## Verdict: CO-SIGN WITH CONDITIONS

The metric substitution is accepted. The dual gate is the right structure. The conditions:

**MC-1 (Gold set Tier 3 inclusion):** The B2 pair set must include at minimum 10 within-Tier-3
or Tier-3-anchored pairs. Pure cross-tier (Tier 1 vs Tier 2 only) B2 does not constitute
passing this gate. The Data Agent must report the B2 pass rate separately for cross-tier pairs
and within-tier-3 pairs when submitting the re-validation results. Both must exceed 95%.

**MC-2 (Ground-truth correction traceability):** The gold set JSON must flag every product
where the expected class has been corrected from the heuristic ground truth (identified as "YES"
in the "Corrects heuristic?" column of §4.3). When Products Agent receives the re-validation
report, the B1/B2/B3 pass rates must be reported with and without these corrections applied, so
we can see exactly how much of the accuracy improvement is formula improvement vs.
ground-truth relabeling. This is not a blocking condition, but the Data Agent must produce both
numbers. A report showing only the post-correction accuracy is insufficient — the delta must be
visible.

**MC-3 (stated_pct field population audit):** Before the re-validation run counts as the
authoritative gate-clearing run, the Data Agent must confirm the stated_pct field population rate
in existing BSIP1 outputs. The redesign spec flags this as "not done" (item 7 of the Not Done
section). If stated_pct is populated in <30% of parseable labels, the percentage-override path
rarely fires and the formula effectively degrades to position-weighted only. That is still better
than the flat count, but the gate thresholds (B1: ≥60 for ≥50% stated-weight whole foods) assume
the formula is reading stated percentages where available. If the override path is rarely
exercised, the B1 threshold should be reviewed by the Nutrition Agent before the run is declared
authoritative.

**MC-4 (B3 denominator clarity):** B3 must be computed on "products with parseable Hebrew
ingredient text" as the denominator — not on the full corpus. The 8 no-marker products in the
probe include products with marketing copy, English INCI text, and nutritional-value-only text.
These are correctly excluded from B3's denominator (they cannot fire any marker regardless of
formula quality). The re-validation report must state the denominator explicitly (N parseable
products) and the no-marker count within that denominator.

---

## What the Dual Gate Does Not Change

The following conditions from the original C-N1-1 co-sign in `d7_cosign_dechain_v1.md` are
unchanged and remain in force:

- **C-N1-2** (adversarial fixture #1: refined white-flour cookie, zero additives, low sugar must
  score below 60/C in the shadow run) — unchanged. This is orthogonal to the metric
  substitution.
- **C-N1-3** (EV-NOVA-REPLACE-001 must be registered with the label-observability result
  attached) — unchanged.
- The minimum 50-product sample requirement is superseded by the gold set requirement (60–75
  products per §4.4) — the gold set is strictly more rigorous.

---

## On the Lexicon Extensions (§2.4)

The lexicon extensions in §2.4 of the redesign spec require a separate note because some affect
published scores: adding `גריסי תירס` (corn grits) as a refined marker, `אורז לבן` (white rice)
as a primary refined grain, and `קמח כוסמין לבן` (white spelt flour) will rescore products
containing those ingredients lower on Component B. Before any lexicon extension is implemented
in `signal_extractor.py`, the Data Agent must run a cross-corpus blast radius check: which
products in which live categories fire the new markers, and what is the expected score delta?
This is consistent with the return contract requirement (item 8 from `return_contract_v1.md`)
for keyword/routing changes.

This is not a condition on the metric substitution itself — it is a condition on the lexicon
implementation. Flagging here for the record; the lexicon co-sign is part of the broader D6
D7 handshake on the formula redesign, not this metric-only ruling.

---

## Decision Log

| Decision | Options considered | Chosen | Decisive reason | Reversal condition |
|---|---|---|---|---|
| Accept or withhold the metric substitution | (a) Accept dual gate, (b) Accept unconditionally, (c) Withhold pending empirical data | Accept with conditions (MC-1 through MC-4) | The binary gate is structurally wrong for a continuous signal on a corpus with 23.5% genuinely mixed products (source: probe report line 74); the dual gate directly measures what matters (anchor calibration + ranking fidelity + coverage); conditions prevent the gate from being trivially cleared on easy pairs only | Reversal to WITHHOLD if the gold set Tier 3 pair set cannot be assembled from the real corpus (fewer than 10 auditable Tier 3 pairs) — at that point, the B2 gate has no statistical power on the hard cases and cannot replace the binary gate |
| Tier 3 inclusion in B2 | (a) B2 cross-tier only, (b) B2 includes within-Tier-3 pairs | Require within-Tier-3 pairs (MC-1) | Cross-tier B2 is trivially clearable — a formula that correctly ranks oat granola above a flour cookie proves nothing about the 88-product mixed failure class that caused the first probe to fail at 62.4% | Reversal if Tier 3 gold set products turn out to be unauditable without food-science expertise (label not readable to a native Hebrew non-expert) — then those products move to Tier 4 and B2 is re-scoped |
| Ground-truth correction transparency (MC-2) | (a) Require split reporting, (b) Accept post-correction numbers only | Require split (MC-2) | The spelt-white-flour pita corrections alone recover ~5–6 percentage points of apparent accuracy; without the split, we cannot distinguish formula improvement from annotation correction | Reversal condition: none — this is an information requirement, not a threshold; always required |
| stated_pct audit (MC-3) | (a) Require before run, (b) Accept post-hoc | Require before authoritative run (MC-3) | The B1 threshold (≥60 for ≥50% whole-food products) is calibrated assuming the formula reads stated percentages; if the BSIP1 enricher rarely populates stated_pct, the formula degrades and the threshold may not hold | Reversal if BSIP1 stated_pct population rate is ≥50% — then the override path fires on the majority of labeled products and the risk is mitigated |

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/d7_cosign_metric_redesign_v1.md",
      "action": "created",
      "sha256": "9EA57FEFC4C7F50EB783267E803CB30A0978CAF6503F3D23DB11E71CC02372DB"
    }
  ],
  "counts": {
    "probe_corpus_total": "520 products (source: matrix_signal_probe_v1_report.txt line 9)",
    "genuinely_mixed_products": "123/520 = 23.5% (source: probe report line 74)",
    "mixed_markers_wrong_direction": "88/520 = 16.9% (source: probe report line 75)",
    "no_marker_products": "8/520 = 1.5% (source: probe report line 50)",
    "binary_gate_result": "62.4% high-confidence / 72.3% combined — FAIL vs 90% target (source: probe report lines 22-34)",
    "conditions_on_metric_substitution": "4 (MC-1 through MC-4; denominator: this ruling)",
    "original_c_n1_1_conditions_unchanged": "2 (C-N1-2 adversarial fixture, C-N1-3 EV registration; denominator: d7_cosign_dechain_v1.md)"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/matrix_signal_redesign_v2.md (full)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/d7_cosign_dechain_v1.md (full)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v1_report.txt (lines 1-80)", "exit_code": 0},
    {"cmd": "Read 01_framework/operations/return_contract_v1.md (full)", "exit_code": 0}
  ],
  "not_done": [
    "D6 co-sign on the formula redesign itself (§2 of matrix_signal_redesign_v2.md) — this ruling covers §3 metric substitution only; formula D6+D7 co-sign is a separate step",
    "Lexicon extension co-sign (§2.4) — blast radius check required before implementation; flagged in ruling but not co-signed here",
    "Gold set JSON creation (matrix_gold_set_v1.json) — Data Agent action, requires owner review per §4.4",
    "Re-validation probe rewrite for B1/B2/B3 — Data Agent action",
    "stated_pct field population audit — required by MC-3 before authoritative gate run"
  ],
  "self_check": "Acceptance test: the dual gate (B1 anchor calibration ≥90%, B2 ordinal ranking ≥95% including ≥10 Tier-3 pairs, B3 coverage ≥95% on parseable text) replaces the binary 90%-accuracy gate as the operative C-N1-1 condition. Observed result: co-sign rendered with 4 conditions (MC-1 through MC-4). The gate is not yet cleared — Data Agent must implement the formula, assemble the gold set, pass owner review, and run the re-validation probe before C-N1-1 is satisfied. This ruling authorizes the metric substitution; it does not clear the condition."
}
```
