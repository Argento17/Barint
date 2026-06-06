**Task:** TASK-179H

# QA Verdict — Glass Box D5/D6 Engine Build (TASK-179G, Wave 1)

**Date:** 2026-06-04 · **Author:** QA Agent (Bari) · **Flag:** `BARI_GLASSBOX_D5D6` (default OFF)
**Scope:** Independent go-live-gate verification of the D5 disclosure-gap detector + D6 confidence
gate. Verification only — no code changed; flag stays default OFF. Build self-proofs were NOT
trusted; every claim was re-run/re-derived independently.

---

## VERDICT: **PASS (CONDITIONAL — flag-ON go-live)**

- **Flag OFF is byte-identical** to the pristine pre-edit engine (git HEAD) across all 342
  products — **independently confirmed**, not via the build's own baseline. Frozen invariants hold.
- **Flag ON is zero-promotion** — independently confirmed (0 score-up, 0 grade-up across both
  pilots). Every delta is a demote or a null.
- **No hard fails.** Two **WARN**s (one documentation error in Proof B, one go-live blast-radius
  point) and one **PASS-with-recommendation** on the P3 deviation.
- The PASS is **conditional on the existing gate**: the −10/−20/30/60 thresholds remain PROPOSALS
  pending Product **D7 co-sign**, and flag-ON go-live is a separate Product/owner decision. Nothing
  ships from this task.

---

## PROOF A — Flag OFF = byte-identical (the hard gate)

**Method (anti-trivial).** I did not trust the build's `_off_baseline.json` (it is untracked and
could have been snapshotted post-edit, making `check` circular). Instead I reconstructed the
**pristine pre-edit engine from git HEAD** (`score_engine.py` + `constants.py`, 0 GLASSBOX refs),
scored all four corpora through both the pristine and the current edited engine with the flag OFF,
and diffed the full `score_product` result dicts.

```
golden_milk  n=20   DIFFS=0
snack_bars   n=53   DIFFS=0
hummus       n=69   DIFFS=0
maadanim     n=200  DIFFS=0
INDEPENDENT OFF (pristine-HEAD vs current-edited, flag OFF): PASS 0-diff   (342 products)
```

The build's own harness (`verify_glassbox_off_identical.py check`) also returns 0-diff (342),
consistent with the independent result.

**Flag gates real, behavior-changing code (not a no-op):** with the flag toggled on the maadanim
corpus, OFF emits **0** Glass Box keys, ON emits keys on **all 200** products and changes **37**
products (5 demote + 32 withhold). The `glassbox_*` keys are absent from the OFF result dict
(confirmed in code at score_engine.py L1636–1639, guarded by `GLASSBOX_D5D6_ON`). So OFF-identity
is real isolation, not the flag doing nothing.

**Frozen invariants under OFF (re-derived):**
- Milk top = **85/A** (`חלב עיזים בקרטון 1 ליטר`). PASS.
- Snack-bar ceiling = **70/B** (`חטיף תמרים במילוי חמאת שקדים`, the snk-001 ceiling product). PASS.
  (The literal key `snk-001` is absent in this BSIP1 corpus, which uses different IDs; the ceiling
  *value* 70/B is the invariant and it holds.)

**Anchoring nuance — RESOLVED, build reasoning is VALID.** The build anchored byte-identity on a
current-engine self-baseline rather than the published frozen traces, because the published traces
were generated under different flags. I verified this reasoning directly on milk:
- RECAL=on vs off (Glass Box off) changes **9** milk products → the milk OFF-vs-published deltas
  are **RECAL**, not Glass Box.
- Under RECAL=on (the published `run_004_recalibrated` lineage), Glass Box ON changes **0** milk
  products → Glass Box is a no-op on the frozen milk corpus regardless of RECAL state.
- Milk top = 85/A in all three configs (RECAL off/GB off, RECAL on/GB off, RECAL on/GB on).

**"OFF changes nothing vs the current engine" is TRUE** (independently confirmed). The
published-trace divergence is a pre-existing RECAL/sprint artifact, correctly isolated from
Glass Box.

**PROOF A: PASS.**

---

## PROOF B — Flag ON pilot (hummus + maadanim)

**Counts re-run fresh** (`run_glassbox_pilot_diff.py`), reproduce the build exactly:

| Corpus | n | demote | withhold→null | unchanged | endemic flavoring | promotions |
|---|---|---|---|---|---|---|
| hummus | 69 | 0 | 4 | 65 | 3 | **0** |
| maadanim | 200 | 5 | 32 | 163 | 130 | **0** |

**Zero promotions — independently confirmed** with my own grade-rank table reading the raw
on/off JSONs (not the harness's self-guard): 0 score-up, 0 grade-up across all 269 pilot products.

**Endemic-flavoring exclusion (EV-036) is load-bearing and working.** Bare `חומרי טעם וריח`
detected in **130/200** maadanim (~65%, matches spec's 129/184). Because it is excluded from
band-raising, only 5 demote + 32 withhold and **163 unchanged**; without the exclusion ~65% of the
shelf would demote (a category-blind distortion). Confirmed.

**Spot-checks (OFF → ON), re-derived:**
- `ג'לי בטעם ענבים` 34.5/E conf45 → 34.5/insufficient_data conf35. Band=partial → −10 conf crosses
  the legacy <40 gate. **demote** (score unchanged, grade removed). Valid.
- `סוכריות …לל"ס` (4 SKUs) 41–46/D-E → insufficient_data. Band=partial → −10 conf. **demote.** Valid.
- `בולגרית מעודנת 24%` 45/D conf? → **null / לא נוקד**, band=severe, panel_present=False. Genuine
  floor failure (severe + absent panel). **withhold.** Valid.
- `פרוביוטיק פמינה` 50/insufficient_data → null. `no_nutrition_data` context (cultures-only panel)
  → panel_absent floor failure; was already non-graded, relabelled. Valid.
- `חומוס מוקפא`, `חומוס לבן ענק שופרסל` (clean single-ingredient) → **full** band → **unchanged
  85/A**. Single-ingredient protection working. Valid.

**Withhold composition (re-derived):**
- **maadanim:** 31 were **already non-graded** under OFF (`insufficient_data`/cap-50) → pure relabel
  to `לא נוקד` (spec §2.3); **1 genuinely new null** from a graded state (`בולגרית 24%` 45/D, severe
  + panel absent).
- **hummus:** **4 genuinely new nulls** from a graded state — `חומוס` / `חומוס ענק` SKUs that were
  **72.1/B and 75/B under OFF**, all band=severe, panel_present=False (`ingredients_raw` absent).

All withholds are floor-of-observability failures (panel/nutrition absent, or severe+thin). No
product was withheld for being merely thin. **PROOF B: PASS (zero-promotion confirmed).**

---

## Assessment of the three build deviations

### 1. P3 token-aware refinement — **PASS (recommend formal Nutrition sign-off at post-pilot co-sign)**
The literal spec (§1.1 P3) says "panel absent if <15 non-space chars after P1" → would set
`panel_present=False` → severe → **withhold**. That directly contradicts the spec's own
single-ingredient protection (§1.2 G1) and sanity-check #1 (§5): a clean single-ingredient whole
food (`אגוזי מלך` = 8 chars, `שקדים` = 5 chars) would be wrongly withheld. The build deviated to:
absent only when sub-threshold **AND** lacking any coherent ≥2-letter token.

Re-derived behavior confirms intent: `אגוזי מלך`/`שקדים`/`גרגרי חומוס מבושלים` → present,
single_ingredient, **full** band (kept); empty/whitespace/garbage → still **absent/severe**;
2-ingredient panel → present/minor. The deviation is **sound and faithful to spec INTENT**, and is
the *more conservative* choice (avoids a perverse withhold of a clean whole food; honors Q1 "buy
coverage over silence"). It is verification-clean.

**Recommendation:** because it changes a written threshold rule (even if intent-preserving), it
should get an **explicit one-line Nutrition Agent sign-off at the post-pilot D6/D7 co-sign**, and
the spec §1.1 P3 text should be amended to the token-aware rule so the doc and the engine agree.
This is a documentation/governance tidy-up, **not** a blocker.

### 2. Self-baseline byte-identity anchoring — **PASS (valid)**
Covered in Proof A. Anchoring on the current-engine self-baseline is correct given the published
traces were generated under different flags; I independently confirmed OFF-identity against the
pristine git-HEAD engine (not the self-baseline), and confirmed the milk published-trace deltas are
RECAL, not Glass Box. Valid.

### 3. `no_nutrition_data` relabeling — **PASS (consistent with spec §2.3)**
31/32 maadanim withholds were **already** `insufficient_data` (cap-50, non-graded) under OFF;
Glass Box only relabels them `insufficient_data → לא נוקד`. This is exactly the spec §2.3 intent
("tightens today's `insufficient_data` to `לא נוקד` for the genuinely panel-less") and is **not**
new aggressive withholding — those products were never carrying a real grade. Consistent.

---

## Hard fails
**None.**

## Warnings (do not block; condition the flag-ON go-live)

- **WARN-1 (documentation defect in Proof B §3).** Proof B's example table names
  `חומוס לבן ענק שופרסל` as a panel-absent **withhold**, but in a fresh run that SKU is **full
  band / unchanged 85/A** (it is NOT withheld). The actual 4 hummus withholds are different plain
  `חומוס` / `חומוס ענק` SKUs (`bsip1_1990261`, `bsip1_3643714`, `bsip1_7296073733317`,
  `bsip1_7296073733348`), all OFF **72.1/B or 75/B** → null. The counts (4 withholds, 0 promotions)
  are correct; only the named example is wrong. Proof B should correct the example row. No effect
  on the engine or the verdict.

- **WARN-2 (flag-ON blast radius — for the Product/owner go-live gate, not this task).** Flag ON
  removes a published-equivalent grade from real products: **4 hummus SKUs lose 72–75/B → null**
  and **1 maadanim SKU loses 45/D → null** (plus 5 maadanim demotes E/D → insufficient_data). These
  are correct per spec (panel-absent / severe+thin), but they are *consumer-facing grade removals*.
  Before any flag-ON go-live, Product should confirm the desired posture (withhold vs. keep-capped)
  for panel-absent products that today carry a B — this is the spec's §2.3 "tighten to לא נוקד"
  call and is exactly the kind of demotion the gate is designed to produce, but it crosses a
  consumer-facing line and is a D7/owner decision. **This task ships nothing**, so it is a
  forward-looking note, not a blocker.

---

## Recommendation

1. **Adopt the build OFF.** Flag-OFF byte-identity is independently proven (pristine git-HEAD diff,
   0/342) and the frozen invariants (milk 85/A, snack ceiling 70/B) hold. The flag correctly gates
   real, behavior-changing code. This is safe to merge behind the default-OFF flag today.
2. **Flag-ON adoption stays gated** on Product **D7 co-sign** of the −10/−20/30/60 PROPOSALS and a
   separate go-live decision that accepts WARN-2's grade-removal blast radius.
3. **P3 deviation:** approve, but require an explicit Nutrition Agent line-item sign-off at the
   post-pilot co-sign and amend spec §1.1 P3 to the token-aware rule (doc-vs-engine reconciliation).
4. **Fix WARN-1** (Proof B §3 example) before the proof is cited in any go-live packet.

**No QA baseline is frozen by this report** (none was requested, and frozen-baseline authority is
not exercised over a pending-co-sign flag). Flag-ON go-live readiness = **CONDITIONAL PASS**,
blockers named above (all governance/co-sign, none engineering).
