# Red-Team Challenge Report — Crackers Category (53-Product Corpus)

**Category:** crackers (includes ricecakes/פריכיות pool, TASK-516/517)
**Corpus version:** 54 scored / 53 displayed (up from 19 displayed pre-TASK-516)
**Trigger:** corpus growth +179% (19→53, ≫20% threshold) + scoring-table change (EV-104)
**Date:** 2026-07-05
**Reviewer:** Adversarial QA Agent (multiple independent passes, consolidated below)
**Verdict: 0 open CRITICAL.**

This report consolidates the substantive adversarial verification performed across
this corpus expansion, in place of a single end-of-run pass, because the work was
gated incrementally (data pipeline → content → scoring) with an independent
Adversarial QA review at each gate rather than one pass at the end. Each section
below was a genuinely independent review — not a summary accepted at face value —
with its own re-derivation from raw artifacts.

---

## 1. Brand-fix data integrity (TASK-516)

**Claim under review:** 17/19 products' `brand` field changed from null to a real
value via a live re-fetch of Shufersal's structured `Product.brand` ld+json field.

**Independent verification performed:**
- Live re-fetch of 5 of the 17 changed barcodes using an independently-written
  fetcher (not the implementer's code) — all 5 matched the shipped value
  byte-for-byte, confirmed attached to the specific product page (not a shelf/category
  tag).
- Merchandising-label sanity check on the ambiguous case (`פיטנס`) — confirmed it is
  a genuine manufacturer brand line (recurs across a barcode-prefix cluster), not a
  mis-captured diet/merchandising tag.
- Barcode-keyed field diff, working tree vs. `origin/master`: 0 non-brand field
  diffs, 0 score/grade/rank diffs across all 19 products — confirms the patch is
  brand-only.
- Reconciled against a prior closed audit (TASK-486) that had concluded brand was
  unrecoverable — confirmed non-contradictory: that audit checked a different
  (already-empty) data field; this fix used a different, valid source (live
  ld+json) the prior audit never attempted.

**Finding:** GO. One MEDIUM, non-blocking: barcode `8434165658523` ships as `"KRIT"`
(uppercase) vs. the evidence artifact's literal lowercase `"krit"` — same brand,
retailer-attested, a casing-normalization documentation gap only. Routed to
data-agent as a fast-follow, does not affect displayed correctness.

---

## 2. Content authoring (TASK-517) — two-gate cycle

**Claim under review:** insight-first Hebrew copy authored for all 53 products (19
rewritten, 34 new), self-gated clean by the authoring pass.

**Independent verification performed (first pass — SIGN-OFF WITH CONDITIONS):**
- Fact-checked claims against real BSIP1/BSIP2 data for a full sweep of the 34 new
  products and a sample of the 19 rewritten ones.
- Independently recomputed superlative rankings (min/max/quartile position) across
  the full 53-product corpus to verify the "re-based to n=53, not the old n=19"
  claim — confirmed true for 10 spot-checked single-extremum claims.
- Found 4 HIGH-severity issues on first pass: (1) one garbled number in prose
  (potato+starch % arithmetic error), (2) sugar superlatives asserted despite the
  sugar field being null for 18/53 products (13 of which have sugar in their
  ingredient list) — not defensible as "highest of 53," (3) six instances of rounded
  gram values contradicting the exact decimals shown in the same product's nutrition
  panel, (4) one relational/cross-product reference violating the standalone-value
  rule plus an overstated "almost double" claim, (5) incorrect flour-blend
  percentage math (confused % of total product vs. % of flour blend). 0 CRITICAL.

**Second pass (post-fix, SIGN-OFF):**
- Re-verified all 6 fixes against trace/nutrition data at the exact flagged
  locations — all corrected accurately.
- Independently re-derived the rescoped sugar-superlative claims against the
  35-product declared-sugar subset — confirmed the claims hold over that subset
  (e.g., the top sugar claim is genuinely the max of the 35 that declare sugar).
- Re-ran the leakage/pattern scan on all 329 strings — 0 relational-reference or
  antithesis violations remaining, 0 real leakage (5 flagged decimals were
  false-positives on the readability tool's score-mechanic regex, adjudicated
  clean since the same decimal precision is already precedented on the live page).

**Finding:** GO. 0 open findings after the fix cycle.

---

## 3. EV-104 protein-scale calibration — scoring change

**Claim under review:** adding `PROTEIN_SCALE_TABLES["cracker"]` (anchored on the
real 53-product protein distribution) moves 13/53 products one letter grade
(8×B→A, 3×C→B, 2×D→C), 0 double jumps, with no unintended side effects.

**Independent verification performed:**
- Re-derived the interpolated protein-mass score by hand for representative
  crossers against the proposed breakpoint table — matched the pilot's claims
  exactly (e.g. 16.0g→95.0, 9.0g→58.0, both exact anchor points).
- Re-ran the actual scoring engine (not a linear back-calculation) against the
  live 54-product corpus with the new table active, in isolation (constants.py on
  disk untouched during the pilot phase) — reproduced the exact 13-crosser list
  and settled a real discrepancy between two independent human/agent estimates
  (7×B→A claimed by one analyst, 8×B→A by another; the engine run confirmed 8 was
  correct).
- Checked all 54 products for double-grade jumps (0 found) and downward movers (0
  found — the change is monotonic-upward over the observed protein range, as
  expected from a corrected curve replacing an under-crediting one).
- Found and independently verified one cap-interaction case (barcode
  `7290011489595`): a sodium-cap (`HIGH_SODIUM_700MG_PLUS`, cap=60) newly binds
  post-patch because the corrected protein dimension score rises above the cap.
  Re-derived both the pre-patch (59.42, non-binding) and post-patch (61.72,
  binding, clipped to 60) values independently — confirmed this is the safety cap
  functioning exactly as designed (absorbing a genuine dimension-accuracy
  improvement on a high-sodium product), not a defect. Grade unchanged (C→C).
- Anti-immunity check: confirmed all 13 crossers have measured protein ≥7.3g/100g
  from direct label data — no plausible gaming path (protein content cannot be
  fabricated without a genuine formulation change).
- Cross-category isolation: scored 306 products across 5 OTHER live categories
  (bread, brined_cheeses, cereals, hummus, snacks) with the patched table active —
  confirmed 0 products outside `category="cracker"` moved at all, proving the
  change cannot leak into any other category's published scores. Structural proof
  independently confirmed (`PROTEIN_SCALE_TABLES.get(category, ...)` is a single
  dict-keyed lookup with no fuzzy matching).
- Verified the anchoring methodology against the precedent it extends (EV-030):
  median→58 (within EV-030's stated 55-60 target band) and max→95 (matching
  EV-030's "top-of-shelf reaches ~95" target) — no daylight from precedent.
- Confirmed via Product Agent's D7 review that the resulting 8 B→A movers are
  defensible on the full picture, not just protein: checked processing_quality,
  additive_quality, sodium, red-label status, and NOVA classification for each —
  none shows a masked quality problem; all 8 are genuine high-protein,
  otherwise-clean products.

**Finding:** GO. Product Agent's D7 conditions (crosser-count reconciliation,
cap-clip review, ship-corpus confirmation, isolated commit, this QA sign-off) are
all closed as of this report.

---

## 4. Data-repair exception (barcode 4267230)

**Claim under review:** a bracket-reversal corruption in one product's ingredient
text is a genuine, reproducible, isolated source-side bug (not fabrication), fixed
via a narrow signature-gated repair rather than invented content.

**Independent verification performed:**
- Confirmed the corruption exists in Shufersal's own raw HTML (not introduced by
  any Bari-side scraping/parsing step).
- Confirmed the position-preserving bracket-swap hypothesis by manually
  unscrambling multiple bracket pairs in the raw string and checking each resolves
  to coherent, plausible Hebrew ingredient text.
- Independently re-ran a stack-based reverse-nesting scan across all 54 BSIP1
  records feeding this page — confirmed the signature fires on exactly 1 product,
  not systemically.
- Confirmed score/grade are byte-identical before and after the repair (41.2/D) —
  the fix changes only displayed text, not any scored signal.

**Finding:** GO. Logged as EXCEPTION-003 in the governance exception registry
(renumbered from EXCEPTION-004 on the source development branch to the correct
next-available number on `origin/master`; body content verified identical).

---

## 5. Merge-reconciliation verification (this document's own gate)

Because this corpus was built independently in parallel on two branches
(`task506` and `origin/master`, diverging before crackers existed on either), the
merge itself required verification distinct from the underlying feature work:

- Confirmed `constants.py`'s merge added exactly one dict entry
  (`PROTEIN_SCALE_TABLES["cracker"]`) with zero disturbance to `origin/master`'s
  independently-added `chocolate` calorie-density table and fermentation flag.
- Confirmed the evidence registry append (EV-104) introduced no cross-contamination
  from unrelated, concurrent in-progress work on the source branch (a yogurt
  scoring entry, EV-105, unrelated to crackers) — verified by grep, 0 hits.
- Re-ran the scoring engine against the merge worktree's own checked-out
  `constants.py` (not trusting the source branch's traces) — 54/54 products
  reproduced their committed scores byte-exactly, confirming the merged file is
  live-correct, not just superficially copied.
- Confirmed zero cross-contamination from unrelated source-branch work (newsletter
  changes, Hebrew health scan, other categories) — diff scope is crackers/ricecakes
  plus exactly 3 shared infrastructure files (constants.py, two evidence
  registries) plus one unrelated one-line agent-registration bugfix
  (`content-agent.md` BOM strip).
- Confirmed all 53 products' `imageUrl` values resolve to self-hosted files (0
  hotlinked), per the project's same-origin image policy.
- Confirmed 0 Open Food Facts usage anywhere in the corpus (`off_used: false`
  throughout; raw store is direct Shufersal HTML only).

**Findings requiring correction before this report was finalized (self-caught, not
external):** the exception-registry entry's first draft during reconciliation
dropped two sections (scoring-impact proof, multiplication-prevention constraints)
present in the source — corrected to restore the full verbatim body. The gate
config (`configs/crackers.json`) was stale (still described the pre-expansion
20-record, PENDING_COPY state) — refreshed to describe the actual 54-scored/
53-displayed, fully-authored corpus.

---

## Summary

| Area | Verdict | Open findings |
|---|---|---|
| Brand data (TASK-516) | GO | 1 MEDIUM (casing doc nit, non-blocking) |
| Content authoring (TASK-517) | GO | 0 |
| Scoring calibration (EV-104) | GO | 0 (all D7 conditions closed) |
| Data repair (EXCEPTION-003) | GO | 0 |
| Merge reconciliation | GO | 0 (2 issues found and fixed during this review) |

**Overall: 0 open CRITICAL, 1 open MEDIUM (non-blocking, routed to data-agent).**
This corpus is cleared for the `run_gates.py` / `validate_comparison_page.py`
mechanical gates and, contingent on those passing, for go-live.
