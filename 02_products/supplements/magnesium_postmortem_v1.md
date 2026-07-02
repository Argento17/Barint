# Magnesium Post-Mortem — what went wrong, and how to get smarter for supplement work

**Date:** 2026-06-23 · **Author:** Orchestrator (C4) · **Scope:** the full magnesium cycle — published → pulled → rebuilt → re-published — and the lessons for the next supplement category.

---

## 1. The one-paragraph story

The magnesium page was published, then **pulled the same day** when an owner-supplied clinical assessment exposed a scoring-methodology bug. We rebuilt it from the data up on a corrected model, ran it through every gate, and **re-published it** — and in doing so the gates caught a *second*, deeper data error (the cheap oxide products were elemental megadoses over the safe limit, not what we had), plus 11 Hebrew translationese phrases, an unsourced claim, unverified ingredient lists, and a recurrence of the mobile-layout bug. The final page is the honest inverse of the buggy one: premium well-absorbed forms lead; the popular cheap oxide megadoses drop to D with a safety warning.

---

## 2. What actually went wrong (root causes, not symptoms)

**RC-1 — A scoring model that was clinically invalid, and no gate checked for that.** The v1 model multiplied elemental mg by a fixed absorption % to get "absorbed mg," then compared *that* to clinical-trial thresholds — but trial doses are *administered* mg, not absorbed. Apples-to-oranges; it systematically depressed every product and produced a false "nothing on the shelf is adequate" headline. **The deeper failure: every gate we had (consistency, leakage, copy, build, render) checked whether the page was internally coherent — none checked whether the scoring methodology was clinically *sound*.** A page can pass all structural gates while being built on a wrong model.

**RC-2 — Label data was wrong twice, in opposite directions, because we scored on inference instead of primary evidence.** First: organic-salt products' elemental declarations were treated as compound and shrunk ~6×, making good products look empty. Then, correcting that, the oxide products' "520 mg" was *inferred* to be compound mass (→314 mg) on a plausibility argument ("520 mg elemental would exceed the UL"). Both were resolved only when we read the **actual label images** — the NRV% on the Altman label proved 520 mg is elemental. The foundational supplement fact — *does the label number mean elemental or compound?* — was never pinned to a resolving primary source before scoring.

**RC-3 — We kept signing off on estimates instead of real engine output.** The v2 model spec *projected* oxide would land D; the real engine run gave oxide a B. We nearly acted on the projection. Estimates and hand-arithmetic repeatedly diverged from (or masked) what the engine actually did.

**RC-4 — The mobile-layout bug recurred, and the render gate that catches it was nearly skipped.** The original page was pulled partly for a mobile-geometry problem; the rebuild reproduced a sibling of it (a long intro burying the shelf on phones). The browser-visual red-team that catches this was blocked by an API outage at publish time — we published before it ran (owner-approved, with live review), and it found the defect post-publish. We got lucky that the owner reviews live.

---

## 3. What worked — and must be kept

- **The owner's instinct to red-team + C3 the rebuild before go-live caught the biggest error (RC-2).** Independent adversarial review is not theater; it found the foundational data fault that three internal passes had carried.
- **The two-gate content sign-off works.** The deterministic naturalness gate caught **11 translationese calques** the author missed *and mis-reported as absent*; the independent content red-team caught an unsourced claim, unverified ingredients, and two Hebrew errors. This is exactly the gauntlet that was missing when the snacks page failed.
- **Primary-source verification resolved the conflict.** When two agents disagreed on elemental-vs-compound, reading the actual label image (the authoritative artifact) settled it — not picking the more confident agent.
- **The citation gate** confirmed the one cited PMID resolves to the right paper (no fabrication).

---

## 4. How to get smarter for the NEXT supplement category (actionable)

1. **Add the missing gate: a clinical-model-validity check.** Before any supplement scoring is built, an independent clinical reviewer (Nutrition + a C3 challenge) must sign that the *methodology* is clinically defensible — administered-vs-absorbed, threshold basis, safety logic — **separate from** the consistency/leakage/copy gates. This is the gate whose absence caused the v1 pull. (See [[done_means_rendered_redteamed_not_gate_pass]].)

2. **Make elemental-vs-compound a hard pre-score gate with primary-source evidence.** For supplements, the single highest-risk fact is what the label number means. **No product gets a score until its elemental basis is confirmed from a resolving primary source** (a supplement-facts panel with an NRV%, or a label showing both compound and elemental). If it can't be resolved one-shot → no-score, never score-by-inference. (Extends [[missing_data_discard_rule]].)

3. **Never sign off on projected/estimated grades — run the real engine.** Any grade an agent reports as an estimate is unverified until the actual flag-gated engine produces it and the orchestrator reads it from the trace/CSV. (Reinforces [[feedback_return_self_verifying]].)

4. **Run the browser-visual render red-team BEFORE publish, with a non-Anthropic fallback.** The mobile-geometry class of bug only shows in a real browser render; it must clear *before* the push, not after. When the native render lane is down, have a fallback (Playwright driven by any available lane) rather than publishing on HTML-only evidence. Consider a standing Playwright geometry test (≥3 rows above fold @390px) in CI for every comparison page.

5. **Watch for long-copy categories breaking mobile geometry.** Supplements carry more explanatory copy (safety, bioavailability) than food categories; the shared comparison template needs the mobile-collapse treatment (now built, opt-in) wherever the intro + category note is long.

6. **Keep the discipline that worked:** owner-triggered adversarial round before go-live, the two-gate content sign-off, primary-source verification over agent confidence, and reading the trace/CSV/DOM directly rather than trusting return prose.

---

## 5. Process note (orchestration honesty)

During a sustained Claude API outage mid-cycle, the native content lane was hard-down. Two adaptations kept the work moving without lowering the bar: (a) routing the independent content gate to **C3 (a different API provider)**, and (b) when the lane was fully unavailable, the orchestrator applied **gate-mandated fixes directly** (deletions + the gate's *own* proposed wording) and then **re-verified through the independent gate** — so the copy stayed gate-approved, not orchestrator-approved. The principle: an outage is a reason to reroute or self-verify-then-re-gate, never a reason to skip a gate.

**Net:** the rebuild was slow and bumpy (a determination reversal, a wrong-model ruling caught mid-flight, an API outage, a post-publish critical), but every defect was caught *before it reached the owner as truth* — which is the system working. The fix list above turns this cycle's pain into a faster, safer next supplement.
