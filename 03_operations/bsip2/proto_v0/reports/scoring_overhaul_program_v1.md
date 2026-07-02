# Bari Scoring-System Overhaul — Program Plan v1 (TASK-395)

**Owner manifesto (2026-06-25):** "Our system is strong enough to avoid relying on simplistic methods such as NOVA."
**Re-planned by 4 lanes:** Nutrition (target architecture) · Data (engineering/reproducibility) · Adversarial QA/Red-Team (trust bar) · C3 (independent). All four converged.
**Status:** plan ratified by the four lanes; execution not started beyond the flag-gated, default-OFF surgical work already built (reversible). No published score changed. Deploy is owner-gated.

---

## The reframe
This is not "remove NOVA." It is a scoring-system rebuild whose **first blocker is reproducibility, not NOVA**. Verified by Data + Red Team independently:
- **8 of 12 live categories cannot be regenerated** by today's engine; **4 live frontend files have NULL run_id** (~127 consumer-facing products with no traceable provenance).
- Root causes (per-category, Data): wrong BSIP1 corpus pinned at scoring time; flags that built a baseline missing from its `configs/*.json` (hard_cheeses: HC_DAIRY_SATFAT_V1/HC002_NOVA1; granola: GRAN_SUGAR_25G_V1); 80+ `batch_run_*.py` scripts each setting their own flag vector outside the canonical spine path.
- **Consequence:** any de-chain drift table measured against an unreproducible baseline is half real-change, half untracked drift — uninterpretable. Reproducibility is *measurement hygiene*, not over-caution (C3).

**C3's governing principle:** *"Do not confuse 'remove chains' with 'remove judgment.' The chains are bad because they are brittle, opaque, and over-dominant — not because Bari can avoid normative choices. The rewrite must make those choices explicit, evidence-backed, observable, testable, and reversible."* This is the operational form of the owner manifesto.

## Method (all 4 lanes agree)
**Whole-system overhaul, incremental-refactor behind versioned flags, with a parallel SHADOW-RUN per category** (old engine and candidate engine run side-by-side, no public change, compared) — **not** a big-bang rewrite (loses institutional invariants) and **not** continued patching (preserves the disease, creates hidden interactions). Public outputs require auditability, tested rollback, and category-by-category sign-off.

---

## Phased plan (consolidated; in-house Phase 0–N merged with C3's 0–6)

### Phase 0 — Reproducible baseline (NON-NEGOTIABLE, first)
For every category: version-pin the exact product set + scraped label payloads + parser/engine/config versions + activation scope; regenerate and match committed scores within a declared tolerance (Red Team: ≤0.05, round-trip not just file-hash). Classify every mismatch (data / parser / engine / config / unknown). **Unknown drift blocks scoring changes for that category**; a category that cannot be reproduced is explicitly **quarantined**, not silently accepted.
- Exit: 12/12 regenerate-to-hash OR are explicitly quarantined.
- Owner looks at: the drift ledger + unreproducible causes (this reveals we currently publish ~127 products we can't regenerate).
- Catastrophe to avoid: "accepting" drift to move faster.

### Phase 1 — Chain inventory + trust instruments
- Map every cap/lookup/floor → signal, evidence, affected products, disposition (kill/keep/convert). (~40 chains; Nutrition's D6 inventory is the seed.)
- Build the machine-checkable trust bar (Red Team's invariants): **G9 dominance run cross-category** (not just cookies); **monotonicity** (adding sugar/additives never raises a score; removing data never raises it) — does not exist yet; **reproducibility-to-hash**; **no-new-inversions**; **grade-distribution sanity** (hard threshold; today's G7 PARITY is hard-coded PASS and cannot gate); **copy-trace consistency** (kills the granola/"canola" fabrication class); **confidence integrity** (no confident score on missing data).
- Consolidate to **one engine, one path**: every flag declared in `configs/*.json`; retire direct engine-attribute mutation and the 80+ batch_run scripts.
- Exit: kill/keep/convert table complete + all invariant gates runnable.

### Phase 2 — Target model spec + fix the root cause
- Nutrition north-star: mostly-continuous evidence-backed dimensions; replace the rigid NOVA step-lookup with a **label-derivable "reassembly/matrix" signal** (refined-starch-no-whole-food); **category-calibrated weights, not global blunt caps**.
- Retain only ~7 principled guards: trans-fat veto (=0), confidence ceilings, whole-food floors (FL-1..4), sweetener caps, the dominance guardrail.
- **Fix the verified root cause first:** `whole_food_integrity` is not confidence-scaled while `processing_quality` is — scale it toward the **worse** class (never reward obfuscation), BEFORE any cap is removed.
- Calibration discipline: category-relative anchoring + committed reference product pairs; every threshold cited to evidence or honestly labeled "corpus-fit" — never "invent the numbers."
- Exit: dimension list + weights + observability + retained vetoes + monotonic rules + tested rollback, owner-reviewed for philosophy.

### Phase 3 — Shadow implementation behind flags
- Old + candidate engines run side-by-side across all ~847 products; no public change.
- Exit: per-category movement reports (rank/grade/score deltas, top risers & fallers) generated; implementation matches spec; reads only in-house labels (firewall).

### Phase 4 — Red-team + inversion gate
- All 7 invariants green on the full corpus; adversarial fixtures pass: cookie/biscuit, low-sugar UPF, clean-label junk, high-protein candy, additive-heavy "healthy" bar, sodium bomb, palm-oil product.
- Owner looks at: the worst surprises and the top-20 movements **per category**, not averages. No unexplained large movements.
- Catastrophe to avoid: aggregate metrics hiding embarrassing examples.

### Phase 5 — Category-by-category owner-gated cutover
- One category at a time: signed approval, deploy window, **tested rollback** (old scores restorable exactly), full copy re-audit (+C3) on every grade-mover before publish.
- Catastrophe to avoid: all categories reflow at once and trust is lost.

### Phase 6 — Post-deploy monitoring
- No severe regressions after publication; audit artifacts archived. Catastrophe to avoid: declaring victory at launch.

---

## Acceptance bar (what proves the manifesto true)
Not a prettier formula — **proof** that the new engine produces fewer inversions, fewer arbitrary cliffs, explainable rises/falls, and **no category where obvious junk moves up because a cap disappeared**. 12/12 reproducible before any change; shadow old-vs-new for all 847; movement tables; invariants green; owner reviews top-20 movers/category; adversarial fixtures pass; evidence registry per dimension with documented label-observability; rollback tested.

## Governance
Every score-moving change: D6 (Nutrition) + D7 (Product) co-sign → conformance + shadow drift + full verdict re-audit (+C3) → owner pre-look → owner-gated deploy. Phase 0/1 are infrastructure (no score change). The full reflow (Phase 5) is the frozen-invariant + consumer-facing tripwire — owner-gated by construction.

## Honest scale
Multi-week program. Phase 0 alone is several days of corpus archaeology (snacks and cakes the messiest). This is a genuine scoring-system rebuild, correctly sized to the manifesto.
