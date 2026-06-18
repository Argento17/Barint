# Factory Run #8 — Lessons Learned + Process Fixes
**2026-06-16. Companion to `factory_run8_audit_v2.md`.** The audit measures the run; this captures the durable lessons and the standing process changes so the same failures don't recur. Owner consequence this run: **the week's metered Sonnet budget was exhausted** — these fixes exist to prevent that.

---

## Lessons learned (the "why" behind the fixes)

1. **The tool you pick *is* the routing decision.** Reaching for native Agent-tool subagents silently pinned every C1 dispatch to `model: sonnet` and defeated the "Sonnet+Gemini+Grok, pick-per-piece, no default builder" law. Mechanism = policy. *Decompose and choose the lane consciously before dispatching — never let convenience pick the model.*

2. **A copy gate is not a correctness gate.** The cakes copy passed C3, yet the page still rendered a structurally broken additive panel (RT-1 CRITICAL). Quality gates are orthogonal — passing one certifies nothing about another. *"Copy passed" ≠ "page is correct."*

3. **Stale-hardcode is the dominant defect class after a rescore.** 8 of 10 red-team findings were literals (scores, counts, tags, schema) that didn't track the data when it moved. *Literals are debt; derive from data. A hardcoded number on a page that has the data is a future defect.*

4. **Push checks left — C0 beats the red-team for deterministic faults.** A 120K-token adversarial agent spent most of its run doing arithmetic a free validator should do at stage 4–5. *Reserve the red-team for genuine adversarial reasoning; let deterministic validators catch drift and schema.*

5. **Sample before you generate.** The biscuit copy failed C3 on a pattern (E-codes / number-recital) visible in a 5-product sample — after 166K tokens of full generation. *Gate a small sample first, then generate the batch once.*

6. **Pixel review belongs *before* "done," not at re-gate.** The 3/10 batch was **owner-caught (detection lag ∞)** — the cardinal failure. The orchestrator should see the rendered page before handing it over. *Owner is never the first line of QA.*

7. **Measure at return-time, not by reconstruction.** W1–W2 telemetry had to be reconstructed (gap F-0). *You can't manage what you didn't capture.*

8. **Rework is the real cost.** ~35% of ~1M tokens was avoidable rework, driven by late catches (lessons 4–6) and single-model spend (lesson 1). *Efficiency is won by catching early and routing right, not by working faster.*

---

## Process fixes (standing changes)

### Routing / budget discipline
- **P-1 Pre-dispatch decomposition is mandatory.** Before any C1 work: split into pieces → assign a lane *per piece* → **mechanical/spec-complete work (re-exports, stale-string edits, bulk JSON/renames) goes to flat-rate Grok/Gemini via the router CLI**; reserve Sonnet for reasoning, Hebrew copy, and red-team. A run that used only one C1 model is a flagged violation. *(Memory: `native_subagent_pins_sonnet_trap`; audit C-10.)*
- **P-2 Budget-preservation default.** Metered Sonnet is opt-in, not reflexive. Flat-rate lanes carry the default load; the orchestrator (Opus) runs lean — no inline verification theater, no speculative dispatches.

### Validators (push-left)
- **P-3 Add a C0 schema-conformance validator** — every `d4_additives` entry must match `AdditiveEntry` (5 keys, valid tier) at export. *(audit C-1)*
- **P-4 Add a C0 data-display-drift validator** — fail the build if a hardcoded literal in a card/SEO/page-data string drifts from the data stat it represents. *(audit C-2)*
- **P-5 Add a C0 filter-contract check** — every filter id implemented in a component must have a matching `page_copy.filters` entry, or the build fails. *(audit C-4)*

### Pipeline hardening
- **P-6 Generate, don't hand-edit, derived artifacts** — SEO/FAQ schema regenerates from the corpus keyed to version; additive VM-conversion + name-normalization live at the export step, not post-hoc. *(audit C-3, C-5)*
- **P-7 Single export entrypoint / clobber guard** — kill the `gen_frontend_json` ↔ `task283_restructure` same-file hazard (65↔149 silent regression). *(audit C-6)*

### Gate ordering & QA
- **P-8 C3 sample-gate before full copy generation.** *(audit C-7)*
- **P-9 Pixel review is a pre-handoff step**, run before declaring any page "done" — not only at the Stage-9 re-gate. *(audit C-8)*
- **P-10 Capture `tokens/tools/wall/outcome` into the ledger at every agent return.** *(audit C-9)*

---

## Pipeline & data-integrity lessons (the product bugs — not just orchestration)

The orchestrator lessons above are only half of it. The run had **real data bugs at every stage**, and almost all of them were born at the **scrape (BSIP0) / enrichment (BSIP1)** and survived undetected to the **stage-9 red-team** — because there is **no integrity or red-team review right after the scrape.** Evidence from this run:

| bug | origin stage | what it was | how far it traveled |
|-----|--------------|-------------|---------------------|
| Misclassified product scored & graded | 0–1 scrape/filter | a Nestlé **breakfast cereal** ("קראנץ שוקולד", 7613038451954) sat in the cakes/cookies corpus and scored **65/B** | nearly published as a B-grade |
| Marketing text as ingredients | 2 BSIP1 | ingredients populated from `bsip1_text_fallback` (ad copy), not a real ingredient list | corrupts scoring **and** risks the no-invent rule |
| Unphysical nutrition value | 0 scrape | **sodium 7000 mg** parsed and scored on | only caught manually; nulled to 23/E |
| Retailer price/promo text in names | 0 scrape | "…\| 80 גרם 5.90 ₪ 7.38" rendered verbatim | RT-10, detection **lag 9** (the longest) |
| Additive schema wrong | 4 export | `{term,category}` instead of the VM `AdditiveEntry` | RT-1 **CRITICAL**, lag 5 |

**The lesson (your point):** garbage enters at the scrape and the pipeline has no early tripwire, so a 120K stage-9 red-team ends up doing data-cleaning that a gate right after the scrape should do for free. Defects born at stage 0 caught at stage 9 cost everything built in between.

### Pipeline lessons
- **L-9 The scrape is the dirtiest stage and the least gated.** Name pollution, junk values, misclassification, and fake-ingredient fallbacks all originate here and currently have *no* review until stage 9.
- **L-10 A silent fallback that fills a field with non-data is worse than a null.** `bsip1_text_fallback` writing ad copy into `ingredients` is a fabrication vector — "unknown is acceptable, invented is not."
- **L-11 Misclassified products must never reach scoring.** Corpus-filter membership is too permissive; an off-category item that gets a grade is a published-score risk.
- **L-12 Unphysical values must be rejected at parse time, not discovered downstream.**

### Pipeline process fixes
- **G-0.5 — Post-scrape integrity + red-team gate (NEW, highest leverage).** Immediately after BSIP0/BSIP1, before scoring, run a review that asserts: (a) names clean — no price/promo/unit strings; (b) every product is genuinely **in-category** (no misclassified shelf items); (c) nutrition values within **physical plausibility bounds** (per-nutrient min/max per 100 g); (d) ingredients are a **real list**, not `text_fallback` ad copy — flag any product whose ingredients came from fallback; (e) images resolve or are honestly null. Fail-closed: a flagged product is **discarded or held**, never scored. This is the "red-team after the scrape" gate — it moves the RT-10 / cereal / 7000 mg / fallback-ingredient classes from lag-9 to lag-0.
- **P-11 `bsip1_text_fallback` must null the field, not populate it** — and emit a low-confidence flag the integrity gate reads.
- **P-12 Category-membership validation at corpus-filter (stage 1)** — a product the shelf-mapper can't confidently place in-category is excluded before BSIP, not after.
- **P-13 Physical-plausibility bounds validator at BSIP0/BSIP1** — out-of-bounds nutrient → null + flag, never scored.
- **P-14 Name-normalization at the scrape/export boundary** (strip promo tails once, centrally) — not patched per page (which is how RT-10 reached stage 9).

These join the orchestrator/validator fixes (P-1…P-10) — but **G-0.5 is the one that would have prevented the most damage this run**, because it attacks the defects at their origin instead of at the most expensive gate.

## Promotion note
P-1/P-2 (routing + budget) → fold into `bari_router_v4_2.md` and `orchestrator_operating_protocol.md`. P-3/P-4/P-5 + P-11/P-12/P-13 are new C0 validators to build. P-8/P-9/P-10 are orchestrator-protocol amendments. **G-0.5 (post-scrape integrity + red-team gate) is a new pipeline stage** — fold into the bari-category-factory skill as a mandatory gate between BSIP1 and BSIP2. None are built yet — they are the backlog this run earned, and G-0.5 is the highest-leverage of them.
