# Supplement Intelligence Engine (SIE) — Methodology v1.4

**Classification:** Internal — Scoring Intelligence (sibling to BSIP2, NOT BSIP2.1)
**Version:** 1.4 (Phase 0/2 — methodology / scoring philosophy) — *banked; Phase-2 amendments applied while banked (TASK-195, 2026-06-06): speciation-aware Form dimension, EFSA TUL as named Safety ceiling, strain-resolved probiotics (Phase 3+ scope). No engine code touched. No score moved.*
**Date:** 2026-06-03 (v1.0) · 2026-06-03 (v1.1) · 2026-06-03 (v1.2) · 2026-06-03 (v1.3 amendment) · 2026-06-06 (v1.4 banked amendments)
**Owner:** Nutrition Agent
**Parent task:** TASK-171 · **This task:** TASK-171E (v1.3); TASK-171A (v1.0–1.2); TASK-195 (v1.4)
**Status:** v1.2 is CO-SIGNED (Nutrition + Product). **v1.3 adds the claim-resolution rule** — vague structure/function claims resolve to studied endpoints via an authored, cited dossier umbrella-map (moderate "fair but skeptical" posture, owner-approved; approach ruled by Product TASK-171E). **This amendment MOVES A REAL GRADE** (the magnesium PoC E/34 → expected B/A once implemented), so unlike v1.1/v1.2 it is a **scoring-rule change requiring Product D7 co-sign before it can ship.** v1.3 is **D6-authored, pending (a) Product D7 co-sign and (b) Data engine implementation** (§11). Everything stays `verification_status: candidate` / `should_affect_score_now: false`; **nothing ships.** The 5-dimension model, grade bands, tiers, weights, and calibration-pending numbers are otherwise **unchanged**.

## Changelog

- **v1.4 (2026-06-06)** — **Banked Phase-2 amendments (TASK-195).** Three methodology amendments applied while the SIE is banked, sourced from "Clinical and Pharmacological Assessment of Dietary Supplementation" (New Batch, 2026-06-06). No engine code touched; no corpus touched; no score changed. All amendments are pre-revival; they activate when TASK-171 revival_gate opens (manufacturer/importer data feed):
  1. **Amendment A — Form dimension: speciation-aware and graded (§2.3).** Added a "speciation tier" sub-table covering magnesium (oxide ~4% / citrate ~25–30% / glycinate ~31%), folate (folic acid with DHFR bottleneck vs 5-MTHF bypassing MTHFR), and B12 (cyanocobalamin / methylcobalamin / adenosylcobalamin). Graded scoring within the Form tier where absorption differential ≥2× and label-observable. `SUPP-EV-017` added.
  2. **Amendment B — Safety dimension: EFSA Tolerable Upper Limit as named hard ceiling (§2.5).** Formalized EFSA TUL as the primary Safety reference (previously "tolerable upper limit" without naming the table). Added tiered penalty: dose > EFSA TUL → Safety VETO (grade cap E); dose 80–100% EFSA TUL → Safety FLAG (annotate only, no grade cap); dose < 80% EFSA TUL → no Safety action on dose grounds. `SUPP-EV-018` added.
  3. **Amendment C — Probiotics: strain-resolved (Advanced/Phase 3+ scope) (§7).** Added probiotics sub-section to Advanced scope. Probiotics require strain-resolved Evidence Dossiers; each named strain gets its own dossier entry; un-named strains ("probiotic blend") → Insufficient evidence tier regardless of CFU count. Does not affect MVP or Phase 2 scope. `SUPP-EV-019` added.
- **v1.3 (2026-06-03)** — **Claim-resolution rule (TASK-171E)** — D6-authored by Nutrition, moderate posture owner-approved, **PENDING Product D7 co-sign + Data engine implementation.** A *scoring-rule change* (moves the magnesium PoC off a wrongful E), not a design refinement. Three coordinated edits:
  1. **§2.1 — claim-resolution procedure replaces the "vague claim → Insufficient" default.** Supplements are legally restricted to vague structure/function language, so literal-wording Evidence matching wrongly floored honest products. Now: a vague claim **resolves** to the active's studied endpoint(s) via the **authored, cited `structure_function_umbrella`** (NOT free-association, NOT live inference); Evidence scores the **best plausibly-mapped endpoint's tier**; the §3 cap-1 Insufficient ceiling fires **only when no studied endpoint plausibly maps.** The **"plausibly maps" boundary (moderate posture)** is defined precisely: an endpoint maps iff it is a **recognized physiological correlate** of the claim term, **pre-authored + cited** in the dossier — narrower than "any-loosely-related" (rejected broad), wider than "exact studied endpoint verbatim" (rejected narrow). Deterministic for Data: engine does an exact key-lookup against the umbrella; "recognized" is the *authoring* test, not an engine inference.
  2. **§5 — `structure_function_umbrella` schema added.** Per active: a map from compliant vague phrases ("bone health", "heart health", …) → studied endpoint(s) with tier + citation + `SUPP-EV-###`. The firewall membrane — pre-authored + cited, never inferred; `resolves_to: null` records a *deliberate* non-mapping.
  3. **§2.4 — over-promise catch confirmed (resolution is not a loophole).** An **over-specific** claim asserting an unsupported tier ("clinically proven", "cures", a named disease) fires the **claim-vs-substance gap** (Honesty debit / potential cap-3) **and** resolves Evidence to the endpoint's *real* (often Weak) tier. Honest vagueness resolves and is scored on its real tier; a confident lie resolves to the same real tier **and** eats an Honesty debit.
  - **Populated:** magnesium `structure_function_umbrella` authored against live `literature` evidence — **heart→BP=Moderate** (maps, best), **bone→BMD=Weak** (maps, observational), **muscle→sarcopenia=Weak** (maps, observational; cramp-null logged), **nerve→does NOT map** (deficiency-state only, no recognized cited correlate). PoC resolves to **Moderate** → expected **B/A**, off E. `SUPP-EV-006` added.
  - **Specified (Data to build):** three §13.4 golden fixtures — R1 vague/evidenced→B/A (binding=blend, NOT cap-1), R2 vague/snake-oil→E (binding=cap-1), R3 over-specific-false→D (binding=cap-3 honesty / Weak tier). Prove the rule is fair, not a loophole.
- **v1.2 (2026-06-03)** — Phase-2 specification additions (design refinements, no scoring-logic or number changes), **RE-RATIFIED by Product 2026-06-03** (§11). Surfaced by two owner challenges pressure-testing the engine's *attribution* (can it tell failure modes apart, and explain them):
  1. **Dose short-circuit rule (§2.2 + §3).** If Evidence tier = **Insufficient**, Dose Adequacy is **N/A — it contributes NO positive credit.** "Effective dose" is *defined by the evidence*; with no evidence there is no effective dose, so a no-evidence active must never read "well-dosed" off `market_range_dsld` (market prevalence). Keeps *attribution* honest — the explanation can never praise the dose of a useless product. Interacts with the §3 Insufficient-Evidence ceiling (the ceiling caps the grade; this rule additionally neutralizes the Dose sub-score so the trace reads `Evidence LOW · Dose N/A · delivery dims as-is`).
  2. **Failure attribution & the explanation layer (new §12).** The engine must emit a **machine-readable "why it failed"** — the **binding constraint** (the cap/veto that actually bound the grade under §3 most-restrictive-wins), NOT merely the lowest sub-score. Specifies the binding-constraint attribution rule, a structured trace contract (5 sub-scores + firing caps/vetoes + binding constraint + dossier facts used), inheritance of BSIP2 explanation discipline (grounded-in-real-trace, dominant-driver/anti-attribution, banned-phrase list) + the No-Necessity firewall + Hard Rule 5. **Phase split:** machine-readable "why" = **Phase 2**; consumer-facing Hebrew prose = **Phase 4**.
  3. **Golden corpus: the attribution axis (new §13).** Beyond §6's per-dimension anchors, the corpus gains **three named failure archetypes** the engine must both *distinguish* (by sub-score signature) and *explain* (by binding constraint): good-active/wasted (**D**), bad-active/excellent-product (**E**, evidence ceiling), good-active/dangerous (**E**, safety floor). Decisive test: **the bottom two are both E with inverted signatures** — validation must confirm the explanation attributes them differently ("no reliable evidence" vs "unsafe dose") and never confuses them. Constructed engineering fixtures (per §11 D7 ruling 5), not published claims.
- **v1.1 (2026-06-03)** — post-D7 amendment; **RE-RATIFIED by Product 2026-06-03**, now supersedes v1.0 as the co-signed artifact. Two owner-approved scope refinements, both *tightening* the MVP (no change to the 5-dimension model or any scoring logic):
  1. **MVP Evidence probe swapped ashwagandha → omega-3 (EPA/DHA).** Ashwagandha's core difficulty (contested botanical evidence + extract standardization) is the very machinery the MVP defers, making it an incoherent Evidence probe. Omega-3 isolates Evidence better — *same molecule/form, Strong for triglyceride lowering and Weak/Insufficient for "brain & mood"* (claim is the variable, form held constant) — and adds high-value Dose/Form/Honesty secondary coverage (the "1,000 mg fish oil" mass trap). The omega-3 CV-events claim is *deliberately not* an anchor (genuinely contested → deferred). Ashwagandha + the botanical/standardization subsystem moved to Phase 2; KSM-66 insight preserved as a deferred note (§7, §8 SUPP-EV-005).
  2. **Dossier lifecycle / maintenance model added (§5.1 + schema fields).** Names the dominant operational risk — dossiers are a living liability whose failure mode is *silent misranking* from a stale, non-erroring dossier. Adds stable-vs-drift fields, staleness *detection* (not auto-update), change-control (D7 + `SUPP-EV-###` bump + golden-corpus re-validation), leaning on externally-maintained authorities (NIH ODS/EFSA), and an MVP maintenance-cost go/no-go metric.
- **v1.0 (2026-06-03)** — initial Phase-0 methodology; CO-SIGNED (Nutrition + Product), Phase 1 authorized.

> **Governance gate.** This document is the scoring *philosophy* for the SIE MVP. Per the BSIP2 governance model, no scoring rule named here is "approved" until it carries both Nutrition and Product D7 co-sign and a `SUPP-EV-###` registry entry where it leans on an external source. Phase 1 builds the dossiers; Phase 2 calibrates the numbers; nothing in this doc ships a score.

> **Firewall (EDPG) — binding.** The integrations layer (`dsld`, `literature`, `pubchem`, `il_gov_data`, `open_food_facts`) is a *fetch* capability, never an *admission* capability. External data is born `verification_status: candidate`. It may **calibrate or justify** a rule (with a `SUPP-EV-###` citation) but the engine **reads in-house BSIP0-S labels only** — never an external value directly. See §9.

---

## Invariants

**SIE Invariant 1 — No-Necessity Rule.** The SIE never scores, ranks, or copy-implies whether a person needs an active; necessity/contraindication text is reader context only and may never feed a sub-score, cap, veto, or grade. This is the firewall that keeps Bari out of medical-advice territory (it operationalizes Hard Rule 5). Every necessity mention elsewhere in this doc (§1 Non-goals, §2.4, §4, §5 dossier `necessity_context`/`contraindication_notes`, §7 out-of-scope item 5, §10 Q3) is downstream of this invariant and points back to it.

---

## 0. Relationship to BSIP2 — what is shared, what is forked

| Concern | BSIP2 (food) | SIE (supplement) |
|---|---|---|
| Object of analysis | A matrix eaten for calories/macros | An `(active, dose, form, evidence)` tuple delivered as a dose |
| Unit | per-100g nutrition panel + ingredient list | per-serving active rows + label claims |
| Question | "Is the nutritional architecture of this food sound?" | "Is this worth taking, as sold?" |
| Dimensions | 10 (NOVA, matrix integrity, glycemic, fat, hyper-palatability…) | 5 (Evidence, Dose, Form, Honesty, Safety) — **none transfer** |
| Constants / golden corpus | frozen food invariants | **separate** `proto_v0/` — food invariants structurally untouchable |
| Plumbing | BSIP0 scrape → BSIP1 enrich → BSIP2 score | **shared** BSIP0-S/BSIP1-S acquisition; **forked** scoring brain |
| Grade scale meaning | architecture of a food (see scoring.md) | "worth taking" semantics — **redefined** in §4, NOT reused |

**Why a sibling engine, not BSIP2.1:** sharing constants or the golden corpus would put the frozen food invariants (milk run_004, snk-001 ceiling, bread provenance) at risk and invite scoring-logic bleed. The decision (TASK-171) is **shared acquisition plumbing, forked scoring brain.** SIE has its own `constants.py`, its own grade thresholds, its own evidence registry (`SUPP-EV-###`), and its own golden corpus.

Placement (sibling tree):
- `01_framework/supplement_framework/` — this methodology, dimensions, grade semantics, scope (Phase 0)
- `02_products/supplements/` — corpus, category-first (Phase 3)
- `03_operations/supplement_engine/proto_v0/` — own constants + scorer + dossier loader; `evidence_dossiers/` (Phase 2+)

---

## 1. Scoring object & the question it answers

**The SIE scores a supplement SKU against the question: "Is this product worth taking, as sold?"**

"As sold" is load-bearing. The SIE does not score an *active* in the abstract (creatine is well-evidenced); it scores **this product's delivery of that active** — the dose in *this* serving, the chemical form on *this* label, the honesty of *this* panel, the safety of *this* daily intake. Two products with the same active can score A and E.

This differs structurally from a food score in four ways:

1. **No per-100g panel.** A supplement is not eaten for its macro composition. Scoring "energy density" or "saturated fat per 100g" of a creatine tub is a category error. The analytical unit is the **active row**: `(active name, per-serving quantity, unit, chemical form)`.
2. **Evidence is a first-class dimension, not a guardrail.** For food, "does protein build muscle?" is settled background. For a supplement, *whether the active does what the product implies* is the central uncertain question and the leading dimension.
3. **Dose is the product, not a serving suggestion.** A food at half-portion is still that food. A supplement at one-third of the clinically effective dose is a *different, non-functional* product — "fairy-dusting." Dose adequacy is scored, not assumed.
4. **The label is an adversary.** Proprietary blends, claim-vs-substance gaps, and form-substitution (oxide sold as "high elemental magnesium") are deliberate label strategies. Formulation Honesty has no food analogue of comparable centrality.

**Non-goals (hard).** The SIE does not give health or medical advice, does not tell a user whether they *need* a supplement, and does not diagnose deficiency. It scores whether *this product*, *if* a person has chosen to supplement this active, is a sound delivery of it. Necessity/contraindication notes live in the dossier as *context surfaced to the reader*, never as a health directive. This is governed by **SIE Invariant 1 — No-Necessity Rule** (see Invariants block above). (Mirrors Bari Hard Rule 5: Bari scores architecture, not health outcomes.)

---

## 2. The five dimensions

Each dimension is scored 0–100, then combined (§3). For each: **what it measures · sub-score logic · which source(s) feed it and how · PASS vs FAIL behavior · edge cases.** All numbers are **calibration-pending** (Phase 2).

Every dimension obeys the firewall: the engine reads the **in-house BSIP0-S label** (the scanned/curated active rows + claims). The external clients (`dsld`, `literature`, `pubchem`, `il_gov_data`) feed the **Evidence Dossier** (§5) and **calibration**, not the live score path.

---

### 2.1 Evidence Strength — *does the active do what the product implies?*

**Measures:** the strength of the published evidence that this active, at a dose in the effective range, produces the benefit the product's **claim** implies. This is the gate dimension — a perfectly-dosed, perfectly-formed active for a claim with no evidence is not worth taking.

**Sub-score logic (calibration-pending):** read from the Evidence Dossier's tier for the `(active → claim)` pair, using the **existing Nutrition evidence-tier ladder** (do not invent a new one):

| Dossier tier | Evidence sub-score band (pending) | Meaning |
|---|---|---|
| **Strong** | 85–100 | Multiple RCTs / meta-analyses / Cochrane / EFSA-authorized health relationship for the claimed effect at the studied dose |
| **Moderate** | 60–84 | Consistent RCT evidence with limitations (heterogeneity, smaller n, surrogate endpoints) |
| **Weak** | 35–59 | Sparse, mechanistic, or animal/observational only; or evidence exists but not at the dose/form sold |
| **Insufficient** | 0–34 | No credible human evidence for the claimed effect, or claim untethered from any studied endpoint |

The relevant tier is **claim-specific**, not active-specific. Creatine for strength = Strong; the *same creatine* marketed for "fat burning" is scored against the fat-loss claim's tier (Weak/Insufficient). The dossier stores tiers per studied claim; the SKU's actual on-label claim selects which one applies.

**Claim-resolution procedure (v1.3 — replaces the prior "vague claim → Insufficient default").** Supplements are legally restricted to vague structure/function language ("supports bone health", "supports muscle function"), so most real labels never state a studied clinical endpoint. Reading Evidence off the *literal label wording* therefore wrongly floors honest products: a good-form, honest, safe magnesium that says "supports bone, heart, nerve and muscle health" matches no studied endpoint and collapses to Insufficient → E, even though magnesium *does* have a studied cardiovascular endpoint. The fix is **claim resolution**, not literal matching:

1. **Resolve, don't literal-match.** A vague structure/function claim **resolves** to the active's studied endpoint(s) under that claim's umbrella, via an **authored, cited claim-map** in the dossier (the `structure_function_umbrella`, §5) — **NOT** free-association and **NOT** live inference. The resolution membrane is pre-authored, cited, and frozen, exactly like a tier (firewall: the engine reads the dossier map, never reasons about the claim itself).
2. **Score the best plausibly-mapped endpoint's tier.** Evidence scores against the **highest tier among the endpoints that plausibly map** under the umbrella. (Most-favourable-mapped, since a structure/function umbrella is a disjunction — "supports bone, heart, nerve & muscle" asserts the active is good for *at least one* of these; the engine credits the best one that genuinely maps, then Honesty (§2.4) independently polices any over-promise.)
3. **Insufficient ceiling applies only when nothing maps.** The §3 cap-1 Insufficient-Evidence ceiling fires **only when no studied endpoint plausibly maps** under the claim umbrella — i.e. a true snake-oil claim with no recognized cited correlate. A vague-but-resolvable claim is **no longer** auto-Insufficient.
4. **The "plausibly maps" boundary (moderate posture — owner-set "fair but skeptical").**

   > **An endpoint "plausibly maps" to a structure/function claim term if and only if it is a *recognized physiological correlate* of that claim term AND that correlate is *pre-authored and cited* in the active's `structure_function_umbrella` (§5) with a tier and a `SUPP-EV-###`.** A claim term with **no** recognized cited correlate **does not map** (→ contributes nothing; if *no* term on the label maps, cap-1 Insufficient fires). "Recognized physiological correlate" means the claim term names a body system/function for which the active has a *studied endpoint* in the published literature — not a marketing adjacency, not a mechanism-only hand-wave, not a deficiency-state finding generalized to a benefit claim in replete users.

   This boundary is deliberately the **middle** of three:
   - **Narrow / "tight-exact" (rejected):** an endpoint maps only if the label states the exact studied endpoint verbatim ("lowers triglycerides"). Rejected — it re-floors every legally-compliant structure/function label, which is the bug.
   - **Broad / "any-loosely-related" (rejected):** any endpoint the claim term *could* be associated with maps. Rejected — it lets "supports wellness" inherit any tier the active earned anywhere, a free-association loophole.
   - **Moderate / "recognized + pre-authored + cited" (adopted):** the correlate must be both physiologically *recognized for that term* **and** written into the dossier with a citation before it can map. Skeptical (an unwritten or uncited correlate does not map; the burden is on the dossier author to cite it) but fair (a legally-vague claim still resolves to the real endpoint the active genuinely has). The skepticism lives in *authoring discipline* (cite or it doesn't map), not in floor-everything literalism.

   Deterministic-implementation note for Data: the engine does **not** judge "recognized." It performs an exact lookup of each label claim term against the keys of the active's `structure_function_umbrella`; a term maps iff a key matches and that entry carries a non-null tier + citation + `SUPP-EV-###`. "Recognized physiological correlate" is the **authoring** test (Nutrition, at dossier-build time, decides what earns a key); the **engine** test is a frozen dictionary lookup. No NLP, no inference, no live literature call on the score path.

**Worked resolution (magnesium PoC):** label claim "supports bone, heart, nerve and muscle health" → the umbrella resolves: **heart → blood-pressure endpoint = Moderate** (cited); **bone → BMD endpoint = Weak** (observational, cited); **muscle → sarcopenia/strength endpoint = Weak** (observational, cited); **nerve → does NOT map** (no recognized cited supplementation endpoint in replete adults — see §5 magnesium map). Best plausibly-mapped tier = **Moderate** (heart/BP) → Evidence is no longer Insufficient, cap-1 does **not** fire, and the PoC moves off E. (Resolved grade: §6/§13 — expected **B/A**, not E.)

**Source feed:** `literature` (PubMed + Europe PMC + OpenAlex + ClinicalTrials) gathers the evidence base; **the Nutrition + Research Agents assign the tier** (the client never tiers — see its docstring). The tier is frozen into the dossier with citations and a `SUPP-EV-###` entry. The engine reads the dossier tier, not the live literature query.

**PASS anchor:** Omega-3 (EPA/DHA) marketed for **triglyceride lowering** → well-established RCT/meta-analytic base → Strong → high sub-score.
**FAIL anchor:** the *same* omega-3 (same molecule, same form) sold for a broad **"brain & mood"** claim → thin/heterogeneous evidence base → Weak/Insufficient → low sub-score.

Omega-3 is the MVP's Evidence probe because it isolates this dimension cleanly: **the claim is the variable, the form is held constant.** The identical EPA/DHA molecule earns Strong for one claim (TG lowering) and Weak/Insufficient for another (brain/mood) — proving the tier attaches to the `(active → claim)` pair, not the active. (A food analogue would be impossible; for food the benefit is settled.)

> **Why TG + cognition, not cardiovascular events.** The omega-3 **CV-events** claim is *deliberately avoided as an anchor*: it is genuinely **contested** (REDUCE-IT positive vs STRENGTH null), which trips the MVP's deferred contested-evidence rule (§7). Using it would force a tier on a conflict the MVP refuses to adjudicate. The TG claim (Strong) and the brain/mood claim (Weak/Insufficient) are *uncontested at their respective tiers*, so they isolate the dimension without invoking deferred machinery. CV-events is recorded in the dossier as `contested` (§8 SUPP-EV-005), not scored.

**Edge cases:**
- **Evidence exists but not at this dose/form.** Downgrade toward Weak — the *claim* is studied but *this delivery* is not the studied one. This is the seam where Evidence and Dose interact; resolve by scoring the claim at the tier of the *evidence that matches the sold dose/form*.
- **Contested evidence** (genuine high-quality conflict — e.g. the omega-3 CV-events claim) is **out of scope for MVP** (§7) — flag as `contested`, do not force a tier.
- **Generic vs branded-extract evidence** (botanical standardization — KSM-66 evidence doesn't transfer to raw root) moves to **Phase 2** context (§7) because it depends on the deferred contested/standardization machinery; the concept is retained there, not deleted.

---

### 2.2 Dose Adequacy — *is there enough active in a serving to work?*

**Measures:** whether the per-serving dose sits at or above the clinically effective dose for the claimed effect — vs underdosed / "fairy-dusted."

**Sub-score logic (calibration-pending):** compare the **in-house label's per-serving quantity** for the active against the dossier's `effective_dose_range = [min_effective, typical, upper_studied]`:

| Condition | Dose sub-score band (pending) |
|---|---|
| dose ≥ `min_effective` and ≤ `upper_studied` | 85–100 (in-range) |
| `0.5 × min_effective` ≤ dose < `min_effective` | 50–84 (sub-therapeutic, graded by proximity) |
| dose < `0.5 × min_effective` | 0–34 ("fairy-dusting" — present for the label, not for effect) |
| dose > `upper_studied` (but below UL) | 60–84 (over the studied range; not more effective; hands off to Safety §2.5) |

**Dose short-circuit rule (Evidence-gated; v1.2).** **If the active's Evidence tier (§2.1) for the on-label claim = Insufficient, Dose Adequacy is N/A and contributes NO positive credit.** "Effective dose" is *defined by the evidence*: `effective_dose_range` only has meaning relative to a studied effect. With no credible evidence for the claim there is no effective dose to be at or above, so the engine must **never** read a dose as "adequate" off `market_range_dsld` (which is market *prevalence*, not efficacy — DSLD shows what is *typically sold*, never what *works*; firewall: it is a sanity check, never a score input). Concretely, when Evidence tier = Insufficient: the engine **sets the Dose sub-score to N/A** (records `dose: N/A`, not a number, not 0-as-a-low-score) so it neither adds positive points in the §3 weighted blend nor is reported as "well-dosed" in the trace. This is an **attribution** rule first: it prevents the explanation layer (§12) from praising the dose of a product whose active has no evidence behind it. (It is *narrower* than the §3 Insufficient-Evidence ceiling — see §3 for how the two interact: the ceiling caps the **grade**; this rule neutralizes the **Dose sub-score** so the trace reads correctly.)

**Fairy-dusting detection** is explicit: an active present at a token fraction of `min_effective` is treated as a *label-decoration ingredient*, not a functional dose. The signal is `dose < fairy_dust_fraction × min_effective` (`fairy_dust_fraction` pending, candidate 0.5). When the active is buried in a proprietary blend so the per-active dose is *unknowable*, Dose Adequacy cannot be computed → it is scored as **fairy-dust-suspected** and the gap is handed to Formulation Honesty (§2.4), which caps the product (you cannot earn dose credit for a dose you refuse to disclose).

**Source feed:** `dsld` supplies the **reference dose ranges** observed across many US labels (e.g. creatine ~1.5–5 g/serving) → seeds the dossier's `effective_dose_range` *candidate*; `literature` supplies the **clinically effective** dose from trials → the authoritative `min_effective`. DSLD shows what's *typically sold*; literature shows what *works* — the dossier stores the literature-derived effective dose and uses DSLD only as a market-prevalence sanity check. The engine reads the **in-house label dose**, compares to the dossier — never queries DSLD live.

**PASS anchor:** creatine monohydrate 5 g/serving → in-range → high.
**FAIL anchor:** creatine HCl 1 g/serving → below `0.5 × min_effective` (5 g) → fairy-dust band.

**Edge cases:**
- **Elemental vs compound mass.** Magnesium "500 mg magnesium oxide" delivers ~300 mg *elemental* Mg; "500 mg magnesium glycinate" delivers far less elemental Mg. Dose Adequacy must compare **elemental** content, derived from the molecular weight ratio (`pubchem` formula/weight → elemental fraction, stored in the dossier per form). Comparing compound mass directly is a known label trap and is forbidden. (Interacts with §2.3.)
- **EPA/DHA vs total fish-oil mass.** A "1,000 mg fish oil" softgel commonly delivers only ~120–300 mg of *actual* EPA+DHA — the rest is other fatty acids and glyceride backbone. Dose Adequacy must compare the **active EPA+DHA mg** against `effective_dose_range`, never the total fish-oil mass on the front label. This is *structurally symmetric* with the minerals' elemental-vs-compound trap: in both cases the headline mass overstates the active. The dossier stores the active-fraction basis (per-form, Phase-1 verify); comparing total fish-oil mg directly is forbidden. (The misleading-mass framing is also penalized by Honesty, §2.4.)
- **Per-serving vs per-day.** Effective doses are sometimes daily and split across servings. The dossier stores the basis; the engine normalizes the label's serving-count to a daily dose before comparison.
- **Dose-by-weight actives** (e.g. mg/kg protocols) are flagged as `dose_basis: bodyweight` and scored against the standard-adult assumption with a confidence note; per-kg precision is Phase 2+.

---

### 2.3 Form & Bioavailability — *is the active in an absorbable form?*

**Measures:** whether the chemical form of the active is a well-absorbed / studied form vs a cheap, poorly-absorbed, or evidence-orphaned form.

**Sub-score logic (calibration-pending):** the dossier stores, per active, a `form_ladder`: `preferred_forms` (studied, well-absorbed), `acceptable_forms`, and `poor_forms` (cheap / low-bioavailability / unstudied). The label's stated form is resolved to identity via `pubchem` (at dossier-build time) and matched to the ladder:

| Form match | Form sub-score band (pending) |
|---|---|
| preferred form (the form the evidence was generated on) | 85–100 |
| acceptable form (absorbed, but weaker/less-studied) | 60–84 |
| poor form sold *as if* premium | 0–34 |
| poor form, honestly the cheap option | 35–59 |

**How form quality is graded** (not from chemistry alone): a form is "good" when **(a)** `pubchem` confirms its identity and **(b)** the *evidence* (§2.1) was generated on that form, or human bioavailability data favors it. Chemistry identity without evidence is necessary but not sufficient — bioavailability is an *evidentiary* claim, not a structural-formula deduction. The dossier records the rationale + citation; a form's placement on the ladder is a `SUPP-EV-###` rule.

**Speciation tier sub-table (v1.4 — Amendment A, TASK-195).** Where absorption data clearly differentiates forms by ≥2× and the form is label-observable (identifiable from the ingredient name on the supplement label), graded within-form scoring applies rather than a binary good/poor split. The following actives are covered at minimum; the dossier is the authoritative source — this table is a reference, not the engine input:

| Active | Form | Absorption / Bioavailability | Tier placement | Notes |
|---|---|---|---|---|
| **Magnesium** | Oxide (MgO) | ~4% fractional absorption (virtually insoluble; gastric acid only partially dissociates) | `poor` | High in elemental Mg per compound mass — the dose trap (§2.2 elemental-fraction correction required). Clinically indicated as antacid/laxative, not repletion. |
| **Magnesium** | Citrate (Mg citrate) | ~25–30% absorption; high solubility, does not reprecipitate in alkaline environments | `preferred` | Confirmed by post-load urinary Mg excretion (25 mmol load: 0.22 mg/mg creatinine vs 0.006 for oxide, p<0.05). |
| **Magnesium** | Glycinate / bisglycinate | ~31% absorption; uses active amino-acid transport; gentle on bowel, low osmotic-laxation risk | `preferred` | Glycine moiety shields Mg from dietary inhibitors. Preferred for GI-sensitive individuals. |
| **Magnesium** | L-threonate | Crosses blood-brain barrier; raises CSF Mg levels | `preferred (specialized)` | Use case: cognitive/anxiety applications. Elemental Mg per compound mass is lower than oxide. |
| **Folate** | Folic acid (synthetic) | 85–100% bioavailability (monoglutamate, highly stable); BUT requires rate-limiting hepatic DHFR → THF → 5-MTHF conversion | `acceptable` | DHFR saturation at ≥200–400 mcg/day causes circulating Unmetabolized Folic Acid (UMFA). MTHFR polymorphisms (C677T, A1298C; ~10–15% population) severely impair conversion. EFSA TUL: 1,000 mcg/day (B12-masking). NTD-prevention evidence base is specific to folic acid form. |
| **Folate** | 5-MTHF / L-methylfolate (levomefolate) | Directly absorbed across intestinal mucosa; bypasses DHFR and MTHFR entirely; immediately enters one-carbon cycle | `preferred` | Does not generate UMFA. Effective in MTHFR-variant individuals. Does not mask B12 deficiency. Clinical NTD-prevention guidelines still cite folic acid (the studied form for NTD trials); 5-MTHF is preferred for MTHFR-variant supplementation outside pregnancy contexts. |
| **B12** | Cyanocobalamin | Standard crystalline form; requires renal conversion to active cobalamins; stable, cheap, well-studied | `acceptable` | High-dose oral (1,000 mcg/day) utilizes passive diffusion (~1%), effective even in achlorhydric states (atrophic gastritis). Requires conversion. |
| **B12** | Methylcobalamin | Active coenzyme form; directly participates in methyl transfer; no conversion required | `preferred` | Label-observable by name. Superiority claims over cyanocobalamin at equivalent doses are contested in the literature — dossier records this as a watch item. |
| **B12** | Adenosylcobalamin | Mitochondrial coenzyme form; complementary to methylcobalamin for full metabolic coverage | `preferred (specialized)` | Label-observable. Less common in Israeli market; included for completeness. |

**Grading rule (Amendment A):** Where absorption differential between the best and worst form for the same active is ≥2× and both forms are label-observable, the Form sub-score is graded (not binary). Specifically: the existing `poor_form` / `acceptable_form` / `preferred_form` ladder applies within each active; the speciation tier table above defines which form occupies which rung. Engine reads the dossier's `form_ladder` (unchanged schema); the speciation data is what populates those rungs. `SUPP-EV-017` covers the speciation evidence for Mg, folate, and B12.

**Source feed:** `pubchem` resolves the named form to a canonical compound (CID, formula, weight, synonyms) — disambiguates "magnesium bisglycinate" = "magnesium glycinate", separates D3 (cholecalciferol) from D2 (ergocalciferol). `literature` supplies the bioavailability/efficacy evidence that *ranks* the forms. Engine reads the in-house label's form string, matched to the dossier ladder built from these sources.

**PASS anchor:** magnesium glycinate / citrate → preferred → high.
**FAIL anchor:** magnesium **oxide** marketed as "high elemental magnesium" → poor absorption form sold as premium → low (and the "high elemental" claim is *technically true but misleading*, which §2.4 also penalizes; the elemental-vs-absorbed split is the trap).

**Edge cases:**
- **The oxide paradox.** Oxide *is* high in elemental Mg per mg of compound but poorly absorbed — high on the §2.2 elemental axis, low here. This is intentional: Dose measures *how much elemental*, Form measures *how much is absorbed*. Both fire; they are not double-counting because they measure different failures. Concern-coordination (§3) ensures the *honesty* angle isn't triple-counted across Form + Honesty.
- **Standardized botanical extracts.** For botanicals, "form" = standardization (KSM-66's withanolide %). A named studied extract is `preferred`; raw/unstandardized root is `poor` *for an evidence-backed claim*. This ties Form to Evidence (§2.1).
- **D2 vs D3.** D3 (cholecalciferol) raises serum 25(OH)D more effectively than D2 (ergocalciferol); D2 on a "vitamin D" product is an acceptable-but-weaker form. (`SUPP-EV-003`.)
- **Omega-3 form ladder.** triglyceride (TG) / re-esterified triglyceride (rTG) = `preferred` (better/faster bioavailability per evidence); ethyl ester (EE) = `acceptable` (absorbed, but lower/slower bioavailability). The exact ladder ranking (TG/rTG > EE, and the magnitude of the EE bioavailability gap) is **Phase-1 Research-verify** — stored as a working value, cited, `SUPP-EV-005`. (Ties to §2.2: the form also bears on how the active EPA/DHA fraction is read.)
- **Mixed/multiple forms** (e.g. "magnesium oxide + glycinate" blend): score the *weighted* form quality if the split is disclosed; if not disclosed → hand to §2.4 (you can't grade a form blend you won't itemize).

---

### 2.4 Formulation Honesty — *is the label telling the truth about what you get?*

**Measures:** the gap between what the label *implies* and what the product *delivers* — proprietary blends that hide per-active doses, claim-vs-substance mismatch, misleading-but-true form/elemental framing, and filler/additive burden that crowds out actives.

**Sub-score logic (calibration-pending):** Honesty starts at 100 and is debited by detected deceptions:

| Deception signal | Effect (pending) |
|---|---|
| **Proprietary/"blend" hiding per-active dose** | hard cap (see §3) — caps the *whole product*, because Dose (§2.2) cannot be verified |
| **Claim-vs-substance gap** (front-label claim not supported by the actual active/dose/form inside) | major debit, scaled by gap severity |
| **Misleading-but-true framing** ("high elemental Mg" on oxide; "1,000 mg fish oil" front label hiding only ~120 mg EPA/DHA; "contains clinically studied X" at a sub-clinical dose) | moderate debit |
| **Filler / bulking-agent dominance** (actives are a minority of the capsule by mass; excessive flow agents, dyes) | minor–moderate debit |
| **Pixie-dust roster** (long list of trendy actives each at fairy-dust dose to pad the label) | moderate debit + interacts with §2.2 |

**Core vs secondary active (definition — drives the C-vs-D cap split, §3 cap 3).** A **core active** is an active named in the product's **primary on-label claim** — the thing the SKU is sold to do (the front-of-pack/lead claim). Every other named active is **secondary/ancillary**. This is **objective and label-observable**: read it off the primary claim text, not assigned at calibration time. A hidden dose on a **core** active caps the product at **D-band**; a hidden dose on a **secondary/ancillary** active caps at **C-band**. (Example: a "sleep" product hiding its melatonin dose → core active hidden → D-band; the same product disclosing melatonin but hiding an ancillary "calm blend" L-theanine dose → secondary hidden → C-band.)

**How "fairy-dusting" / blend-hiding is detected:** the in-house label exposes either (a) a per-active quantity, or (b) a **proprietary-blend total** with named actives but no per-active split. Case (b) is the hiding signal: the SIE cannot confirm any single active reaches `min_effective`, so it *withholds* Dose credit and applies the Honesty cap (C- or D-band per the core/secondary split above). The reader-facing logic is: "a product that hides its doses is asking to be trusted on faith; the SIE does not extend that trust."

**Source feed:** primarily the **in-house label structure itself** (blend flag, per-active presence, claim text) — this dimension is largely *intrinsic* and label-observable, the most BSIP0-S-native of the five. `dsld` calibrates what a "normal" disclosed panel looks like (prevalence of proprietary blends per category) so the cap threshold is grounded, not arbitrary. `il_gov_data` can corroborate importer/registration legitimacy (a non-registered importer is a separate honesty/legitimacy signal) — **candidate, calibration-only**, never a live engine read.

**PASS anchor:** caffeine labeled "200 mg" explicitly → fully disclosed → high.
**FAIL anchor:** caffeine hidden inside a "proprietary energy blend 1,200 mg" with no per-active dose → blend-hiding cap fires; Dose Adequacy for caffeine is unknowable → withheld.

**Edge cases:**
- **Legitimate blends.** Some blends are honest (full per-active disclosure under a "blend" header). The signal is *hidden dose*, not the word "blend." Disclosure, not nomenclature, is scored. (Mirrors the food-side "raw vs prepared is decided by composition not the word סלט" memory.)
- **Necessary excipients.** A binder/flow agent at functional minimum is not dishonesty; only *dominance* or *deceptive padding* is. Don't penalize a capsule for being a capsule.
- **"Clinically studied" halo.** "Contains clinically studied [active]" is honest *only if* the dose matches the studied dose; "studied ingredient at unstudied dose" is a claim-substance gap → debit.
- **Over-specific over-promise — the claim-resolution backstop (v1.3).** Claim resolution (§2.1) makes vague structure/function claims *resolvable*, which could be read as a loophole — "just say something vague and inherit the active's best tier." It is **not** a loophole, because the over-promise catch lives **here, in Honesty.** Resolution applies only to **compliant vague** structure/function language. An **over-specific claim** that asserts a tier the evidence does not support — "**clinically proven**", "**cures**" / "**treats**", or a **specific disease/condition** ("cures insomnia", "reverses osteoporosis", "fixes nerve damage") — fires the **claim-vs-substance gap** (major Honesty debit, scaled by gap severity; up to the §3 cap-3 Honesty cap when the over-claim is on the core active). The two mechanisms act **together**, not in competition: (a) Evidence still resolves the *underlying* endpoint to its **real** tier — "clinically proven to cure insomnia" resolves to magnesium's **sleep endpoint = Weak**, not to a free A; and (b) Honesty **debits the over-promise** because the label asserted certainty ("proven", "cure") that a Weak endpoint cannot bear. So a specific lie is marked down twice over — a real-but-Weak underlying tier *plus* an Honesty claim-gap — and never earns the grade the vague version would. **Rule of thumb:** vague-but-true resolves and is scored on its real tier; specific-but-false resolves to the same real tier **and** eats an Honesty debit. Resolution rewards honest vagueness; it never rewards a confident lie.
- **Headline-mass framing.** "1,000 mg fish oil" stated where the active is the EPA+DHA fraction (~120 mg) is *technically true but misleading* — the buyer reads the big number as the active dose. Debit the claim-substance gap; the dose comparison itself is corrected in §2.2 against active EPA/DHA, not total mass.

---

### 2.5 Safety Ceiling — *is the daily intake safe?*

**Measures:** whether the product, at its labeled serving (and plausible daily use), exceeds the tolerable upper intake level (UL), uses a risky/banned active, or pushes unjustified mega-dosing with no added benefit.

**Sub-score logic (calibration-pending):** this dimension is a **veto/cap**, not a smooth contributor — most products are "safe" and should not be *rewarded* for it; unsafe ones must be *floored*:

| Condition | Effect (pending) |
|---|---|
| labeled daily dose within all thresholds, no risky active | neutral (does not lift score; absence of harm isn't a virtue) |
| daily dose between a **reversible-tolerance threshold** and the toxicity-relevant UL | **Safety NOTE** → graded soft penalty, **NOT a veto** (e.g. magnesium 250–350 mg: EFSA's 250 is reversible GI/osmotic tolerance, not toxicity) |
| labeled daily dose **exceeds the toxicity-relevant UL** | **Safety veto** → hard score floor (analogous to BSIP2 trans-fat veto) |
| risky/banned/regulatory-flagged active present | Safety veto → floor |
| mega-dose above `upper_studied` but below UL | no Safety penalty, but **no Dose bonus** (§2.2) — "more is not better" |

**Source feed:** the dossier stores `upper_limit_UL` and `risky_active` flags, sourced from **NIH ODS / EFSA** UL values (tiered, cited, `SUPP-EV-###`). `literature` + `il_gov_data` (banned/restricted substances, importer legitimacy) corroborate. The engine reads the in-house label's daily dose vs the dossier UL. UL comparison must use the **same basis** as the dossier (elemental, daily, adult).

**Veto-vs-note classification rule (standing meta-rule — Nutrition+Product D7, 2026-06-03, FLAG-2; supersedes the prior "most-conservative-tolerance governs the veto").** The hard Safety **veto is reserved for toxicity/harm ceilings** (systemic-toxicity UL, banned/risky actives). A **reversible, self-limiting tolerance threshold** (e.g. GI/osmotic, like magnesium's EFSA 250 mg or vitamin C's diarrhea threshold) **does not trigger a veto** — it sets a graded **Safety NOTE** band (soft penalty), and the hard veto rests on the higher *toxicity-relevant* bound (e.g. magnesium's NIH/IOM 350 mg). Rationale: a rule that vetoes a reversible GI effect would auto-fail an *adequately-dosed* product (magnesium `min_effective` ≈ 300 mg > EFSA 250) — punishing efficacy, not harm. **Guardrail:** the reversible-vs-toxicity classification is a **dossier-level, evidence-tiered, Nutrition-owned, cited (`SUPP-EV-###`) judgement** — the engine reads the already-classified `upper_limit_UL` (veto) and `ul_note_threshold` (note); it **never infers reversibility itself.** Most-restrictive-wins is unchanged for harm thresholds.

**EFSA Tolerable Upper Limit as named primary Safety ceiling (v1.4 — Amendment B, TASK-195).** Previously, the Safety dimension referenced "tolerable upper limit" without naming the authoritative table. This amendment formalizes EFSA's Tolerable Upper Intake Levels (TULs) — established under Directive 2002/46/EC and assessed by EFSA's Panel on Nutrition, Novel Foods and Food Allergens (NDA) through systematic toxicological evaluation — as the primary Safety ceiling reference for the SIE. Israel has no equivalent standalone TUL table; EFSA TULs are the most defensible European reference and are already partially captured in individual dossiers (SUPP-EV-002, 003, 004, etc.).

**Tiered Safety penalty structure (Amendment B):**

| Dose vs. EFSA TUL | Safety effect | Grade impact |
|---|---|---|
| Dose > EFSA TUL | **Safety VETO** — hard score floor (grade cap = E). Existing behavior, now explicitly citing EFSA TUL as the reference. | Overrides all positive dimensions. Analogue: BSIP2 trans-fat veto. |
| Dose 80–100% EFSA TUL | **Safety FLAG** — annotate only; note appears in the explanation trace; no grade cap applies. The product is approaching the ceiling but has not crossed it. | No grade cap; trace records `safety_flag: approaching_tul`. Consumer-facing explanation surfaces the proximity. |
| Dose < 80% EFSA TUL | **No Safety action on dose grounds.** | Safety dimension is neutral for dose (existing behavior). |

**Scope and authority:** EFSA TUL values are stored in dossiers as `upper_limit_UL` (the toxicity veto ceiling) sourced from the EFSA NDA Panel's published opinions and the Directive 2002/46/EC harmonized positive list. Where EFSA and NIH/IOM values differ, the governing-UL choice is documented per dossier (existing per-dossier D7 ruling convention, e.g. SUPP-EV-002 for magnesium). The 80% FLAG threshold is a fixed engine constant (`TUL_FLAG_FRACTION = 0.80`), not a per-active dossier value. `SUPP-EV-018` added. Example EFSA TULs already in dossiers: Vitamin B6 12.5 mg/day (reduced from 30 mg/day following sensory neuropathy data); Folate (folic acid) 1,000 mcg/day (B12 masking); Selenium 255 mcg/day; Iron 40 mg/day; Manganese 8 mg/day.

**PASS anchor:** vitamin D3 1,000–2,000 IU/day → well within UL (UL = 4,000 IU/day for adults, NIH ODS — *Strong/regulatory, Phase-1 verify*) → no penalty.
**FAIL anchor:** vitamin D3 50,000 IU/day labeled for daily use → exceeds UL by an order of magnitude → Safety veto floors the score, regardless of how well-evidenced or well-formed D3 is. (Creatine doubles as the Safety **PASS control**: a well-evidenced active with no UL concern at its effective dose — proves the dimension doesn't punish a clean active.)

**Edge cases:**
- **Therapeutic megadose under supervision** (e.g. a 50,000 IU D3 *weekly* repletion product, clinician-directed): the SIE scores the *product as sold to a consumer*. A clearly-labeled weekly clinical-repletion SKU is flagged `clinical_use` and may be exempted from the consumer-daily veto **with a Safety note** — but a 50,000 IU product labeled for *daily* use is vetoed. The discriminator is the **labeled regimen**, read from the in-house label.
- **Stacking/cumulative UL** (same active across multiple products) is **out of MVP scope** — the SIE scores one SKU. Note the limitation.
- **No established UL** (e.g. creatine has no UL): absence of a UL is *not* a safety pass for arbitrarily high doses — fall back to `upper_studied` + a Weak-evidence safety note. Creatine at its 5 g effective dose = clean.

---

## 3. Dimension combination → final score & grade

The five sub-scores combine into a 0–100 product score, then map to a grade (§4). **All values calibration-pending (Phase 2).**

### 3.1 Combination model (candidate)

Evidence and Dose are **gating** (a product that fails either is not "worth taking" regardless of the rest); Form, Honesty, Safety modulate. The candidate model is a **weighted blend with gates and vetoes**, mirroring BSIP2's "weighted dimensions + caps + vetoes" structure but with supplement-appropriate weights:

| Dimension | Candidate weight (pending) | Role |
|---|---|---|
| Evidence Strength | 30% | gate + weight |
| Dose Adequacy | 25% | gate + weight |
| Form & Bioavailability | 20% | weight |
| Formulation Honesty | 15% | weight + cap source |
| Safety Ceiling | 10% | veto/cap (rarely additive) |

Rationale for the shape (not the exact numbers): a supplement's worth is dominated by *does the active work* (Evidence) and *is there enough of it* (Dose). Form refines delivery. Honesty and Safety are primarily **cap/veto** mechanisms — they rarely *add* points; they *withhold* them.

**N/A sub-scores in the blend (v1.2).** A dimension can resolve to **N/A** (currently only Dose Adequacy, via the §2.2 dose short-circuit when Evidence = Insufficient). An N/A dimension is **excluded from the weighted blend entirely** — it is *not* treated as 0 (which would be a low score, i.e. a number) and *not* re-weighted to inflate the remaining dimensions. Operationally: drop the N/A dimension's weight from the denominator and blend the remaining dimensions on their original relative weights. The N/A is recorded verbatim in the trace (`dose: N/A`) so the binding-constraint attribution (§12) reads the failure as "no evidence," never "underdosed." Because the §3 cap 1 Insufficient-Evidence ceiling is the binding constraint in exactly this case, the blended number is moot for the grade — but the N/A still matters so the **trace and the explanation are honest** about *why*.

### 3.2 Caps, floors, vetoes (analogous to BSIP2 guardrails) — all pending

1. **Insufficient-Evidence ceiling.** If Evidence tier = Insufficient, the final score is **capped** (candidate ceiling 34 → cannot exceed grade E). You cannot earn a good grade for delivering, in a perfect form at a perfect dose, an active with no evidence for the claim. (Analogue: BSIP2 `CONFIDENCE_INSUFFICIENT_CEILING`.) **Pairs with the §2.2 dose short-circuit (v1.2):** the ceiling caps the *grade*; the short-circuit additionally sets *Dose = N/A* so no "well-dosed" credit accrues and the trace attributes the failure to evidence, not dose. Two distinct mechanisms — one bounds the grade (cap 1), one neutralizes a sub-score (§2.2) — so the explanation (§12) names the **evidence ceiling** as the binding constraint and never reports a dose verdict for a claim with no studied effect.
2. **Fairy-dust / hidden-dose cap.** If Dose is in the fairy-dust band *or* the per-active dose is hidden in a proprietary blend, the final score is **capped** (candidate ceiling ~ D-band). A non-functional or unverifiable dose cannot pass.
3. **Formulation-Honesty cap.** A proprietary blend that hides per-active doses caps the whole product, because Dose cannot be verified. The cap is on the *product*, not just the Honesty sub-score. The ceiling depends on **which** active is hidden, per the **core vs secondary active** definition in §2.4: a hidden **core active** (named in the product's primary on-label claim) → **D-band** cap; a hidden **secondary/ancillary** active → **C-band** cap. The split is label-observable, not a calibration-time judgement call.
4. **Safety veto.** Daily labeled dose > UL, or a banned/risky active → hard **floor** (candidate floor ~ E-band), overriding all positive dimensions. (Analogue: BSIP2 trans-fat veto → floor 20.)
5. **Form-evidence coupling floor.** A `poor_form` sold for an evidence-backed claim where the evidence was generated on a *different* form cannot score above the form-honesty band (you're selling the halo of evidence the product's form didn't earn).
6. **Concern coordination** (mirrors BSIP2 Stage 5): the *same* underlying deception must not be charged in three places. The "oxide sold as premium magnesium" failure expresses as low Form (poor absorption) + an Honesty debit (misleading framing). These are **distinct failures** (one absorption, one disclosure) and both stand; but a single "hidden dose" must not *also* be re-charged as a separate filler debit and a separate claim-gap debit — the primary signal holds full weight, secondaries demote.

**Most-restrictive-wins:** when multiple caps apply, the lowest ceiling wins (BSIP2 convention).

---

## 4. Supplement grade semantics (A–E / S) — redefined, NOT the food scale

The SIE reuses the **letter shape** (S/A/B/C/D/E) for reader familiarity but **redefines every grade's meaning** for a supplement. A food B and a supplement B are different claims. Score→grade band thresholds are **calibration-pending**; the candidate bands mirror BSIP2's (S 90+, A 80–89, B 65–79, C 50–64, D 35–49, E 0–34) but may move in Phase 2.

| Grade | Supplement meaning (NOT food meaning) |
|---|---|
| **S** | Exemplary delivery: Strong evidence for the claim, dose at the studied effective range, preferred/studied form, fully disclosed, comfortably within safety. The product to point to. |
| **A** | Worth taking as sold: strong/moderate evidence, adequate dose, good form, honest label, safe. Minor refinements possible. |
| **B** | Sound but compromised on one axis: e.g. effective active + good dose but an acceptable-not-ideal form, or a modest disclosure gap. Functional. |
| **C** | Works only partially / asks for trust: under-the-ideal dose, weaker form, or a disclosure/claim gap that the buyer should know about. Not clearly worth the money. |
| **D** | Likely not worth taking as sold: fairy-dusted dose, poor form sold as premium, or a meaningful claim-substance gap. The active may be fine; *this delivery* is not. |
| **E** | Should not be relied on: no credible evidence for the claim, a hidden-dose blend that can't be verified, or a safety-ceiling breach. Includes the Insufficient-evidence ceiling and the Safety veto. |

**Key divergence from food:** for food, a high grade means *nutritional architecture is sound*. For a supplement, a high grade means *this is a trustworthy, effective, honest delivery of an active you've chosen to take*. A supplement E is not "unhealthy" — it is "not worth taking as sold" (no evidence, hidden dose, or unsafe). The SIE never implies a person *should* or *should not* take a supplement (Hard Rule 5).

---

## 5. Evidence Dossier schema — the Phase-1 backbone asset

The **Evidence Dossier** is the reusable, per-active reference record built **once** and reused by every SKU containing that active. It is where all external-source reasoning is frozen into in-house, cited, tiered facts (firewall-compliant: the engine reads the dossier, an in-house artifact, not the live APIs). Built in Phase 1 (Nutrition + Research).

```yaml
# evidence_dossiers/<active_slug>.yaml   (schema v1 — Phase 1 fills values)
active:
  canonical_name: "creatine monohydrate"
  pubchem_cid: 586              # from pubchem (identity)
  synonyms: ["creatine", "N-carbamimidoyl-N-methylglycine"]
  category: "performance"      # performance | mineral | vitamin | stimulant | botanical

claims:                         # tier is CLAIM-specific (see §2.1)
  - claim: "strength / lean mass with resistance training"
    evidence_tier: "Strong"     # Strong | Moderate | Weak | Insufficient  (existing ladder)
    citations: ["PMID:xxxxxxx", "PMID:xxxxxxx"]   # from literature client
    notes: "meta-analytic; well-replicated"
  - claim: "fat loss"
    evidence_tier: "Insufficient"
    citations: []

effective_dose:
  basis: "per_day"              # per_day | per_serving | bodyweight
  min_effective: 3.0            # literature-derived (authoritative)
  typical: 5.0
  upper_studied: 5.0
  unit: "g"
  market_range_dsld: [1.5, 5.0] # dsld prevalence — SANITY CHECK ONLY, candidate
  elemental_fraction: null      # for minerals: elemental/compound (from pubchem MW)

forms:
  preferred: ["monohydrate"]    # form the evidence was generated on
  acceptable: []
  poor: ["HCl (sold premium, no superiority evidence)"]
  rationale: "monohydrate is the studied form; alternatives lack superiority data"
  citations: ["PMID:xxxxxxx"]

safety:
  upper_limit_UL: null          # NIH ODS / EFSA — null = no established UL
  ul_basis: "n/a"
  ul_source: "NIH ODS"
  risky_flags: []               # banned/restricted/regulatory
  notes: "no UL; well-tolerated at effective dose"

label_claims_common: ["builds muscle", "strength", "recovery"]   # for claim-matching

structure_function_umbrella:    # v1.3 — the claim-resolution membrane (§2.1). Pre-authored + cited, NEVER inferred.
  # Maps compliant VAGUE structure/function phrases → the studied endpoint(s) they resolve to.
  # Each phrase is a KEY; the engine does an EXACT lookup (no NLP). A phrase maps iff it has a
  # non-null resolved_tier + citation + supp_ev. A phrase with resolves_to: null does NOT map
  # (documents the deliberate non-mapping). The "best plausibly-mapped tier" across all label
  # phrases drives Evidence (§2.1 step 2).  Engine reads `mappings[]`; `umbrella_resolution_summary`
  # is human-readable provenance only (not read by the engine).
  mappings:
    - phrase: "muscle health"      # example shape (per-active values authored at build time)
      resolves_to: "strength / lean mass with resistance training"  # an existing claims[] endpoint
      resolved_tier: "Strong"
      citations: ["PMID:xxxxxxx"]
      supp_ev: "SUPP-EV-001"
      verification_status: "candidate"
      should_affect_score_now: false
    - phrase: "energy"
      resolves_to: null            # no recognized cited correlate for THIS active → does NOT map
      resolved_tier: null
      note: "creatine 'energy' is mechanistic/ATP hand-wave, not a studied consumer 'energy' endpoint → does not map"
  umbrella_resolution_summary: "human-readable note: which phrases mapped, best tier, expected grade effect"

necessity_context: "not a dietary necessity; ergogenic aid"      # surfaced, never a directive
contraindication_notes: ""                                        # context only, not health advice

provenance:
  built_by: ["nutrition-agent", "research-agent"]
  built_at: "2026-06-..."
  supp_ev_refs: ["SUPP-EV-001", "SUPP-EV-007"]
  verification_status: "candidate"   # until QA/D7 promotes

lifecycle:                            # §5.1 — maintenance / staleness control
  last_evidence_sweep: "2026-06-..."  # date the literature client last detected-checked drift fields
  review_by: "2027-06-..."            # date OR cadence (e.g. "annual") for the next drift-field sweep
  field_stability:                    # which fields drift vs are compute-once (review cadence = drift only)
    stable: ["pubchem_cid", "elemental_fraction", "molecular_weight", "synonyms"]
    drift:  ["claims.*.evidence_tier", "effective_dose", "safety.upper_limit_UL", "forms.form_ladder"]
  externally_maintained:             # drift fields preferred as reference + re-sync, not hand-maintained
    - field: "safety.upper_limit_UL"
      authority: "NIH ODS / EFSA"
      last_resync: "2026-06-..."
  change_log: []                      # [{date, field, old, new, evidence, adjudicated_by, supp_ev}]  — drift-field changes; score-moving ones require D7 + SUPP-EV bump + golden-corpus re-validation
```

Notes:
- **`verification_status: candidate`** until it clears the SIE admission gate — honors EDPG. No dossier value reaches a published score on the strength of "the API returned it."
- Tiers use the **existing** ladder; `Contested` is recorded only as a flag for deferred actives (§7), not used as a scoring tier in MVP.
- Every field that leans on an external source carries a citation + a `SUPP-EV-###` ref.
- **`structure_function_umbrella` (v1.3) is the firewall membrane for claim resolution (§2.1).** It is pre-authored + cited, never inferred: a vague structure/function phrase resolves to a studied endpoint **only** through a key written here by Nutrition at dossier-build time. A phrase with `resolves_to: null` is the *deliberate non-mapping* record (it documents that the author considered the phrase and found no recognized cited correlate — so "nerve health" not mapping is an explicit authored decision, not a silent omission). Adding/changing an umbrella key that *moves a score* is a drift-field change → D7 co-sign + `SUPP-EV-###` bump + golden-corpus re-validation (§5.1). Each mapped key reuses the active's existing `claims[]` tier + citations (no new evidence; resolution is a *pointer*, not a new tier).

---

### 5.1 Dossier lifecycle & maintenance — the dominant operational risk

**The engine is built roughly once; the dossiers are a living liability.** A scorer, once validated, is stable. A dossier encodes *the current state of the science* for an active — and science drifts. The failure mode is the dangerous kind: a stale dossier **does not error**. It silently encodes a drifted state of evidence and keeps scoring confidently, producing **silent misranking**. This is the single largest operational risk in the SIE and is treated as first-class.

**1. Stable vs drift fields.** Dossier fields split into two classes, and review cadence applies to the drift class **only**:

| Class | Fields | Behavior |
|---|---|---|
| **Stable (compute-once)** | molecular weight, `pubchem_cid`, elemental fraction, EPA/DHA active-fraction basis, canonical name/synonyms | Computed once from chemistry/identity. Do not drift with the science; no review cadence. |
| **Drift (review-bound)** | `evidence_tier` (per claim), `effective_dose`, `upper_limit_UL`, the claim→tier map, the `form_ladder` | Track the moving state of evidence/regulation. Carry a review cadence and a staleness flag. |

**2. Staleness detection, not auto-update.** The `literature` client is **re-runnable to *detect*** new high-tier publications since a dossier's `last_evidence_sweep` date. A detected new meta-analysis / RCT / regulatory revision **raises a review flag** — it does **not** move any number. A human (Nutrition + Research) adjudicates whether the new evidence actually changes a drift field. The pipeline **never auto-moves a score**; detection is mechanical, adjudication is human.

**3. Change-control.** Any drift-field change that *would move a score* is a **scoring change**, not a data refresh. It therefore requires: **D7 co-sign** (Nutrition + Product), a **`SUPP-EV-###` bump** (new/superseding entry), and **re-validation against the golden corpus** (the 12-anchor set must still behave). The change is recorded in a per-dossier **`change_log`** (what changed, old→new, evidence, who adjudicated, `SUPP-EV-###`, date). A drift-field edit that does *not* move any score is logged but does not require corpus re-validation.

**4. Lean on externally-maintained authorities.** For drift fields that *someone else already maintains rigorously* — ULs and safety/banned-substance flags via **NIH ODS / EFSA** — prefer **reference + periodic re-sync** over independent hand-maintenance. This shrinks the surface area Bari owns: Bari stores the value, its source, and a re-sync date, rather than re-deriving it. Firewall-clean throughout: the re-synced value is still born `candidate`, still cited, still admitted only through the dossier (never a live external read on the score path).

**5. MVP success metric (Product go/no-go input).** Proving the engine is **not** the same as proving the model is sustainable. The MVP must therefore **measure the real per-dossier build + maintenance cost** — author-hours to build a dossier *and* the re-verification cadence (how often drift fields realistically need a sweep + adjudication) — and surface it as an explicit **Product go/no-go input before any scale-up (D1/D10).** If a dossier costs more to keep current than the category can bear, the honest answer is "the math works but the model doesn't scale," and that must be visible *before* committing to a shelf, not discovered after. Proving the engine includes proving the dossier model.

---

## 6. MVP 5-active stress matrix — every dimension gets both poles

Restated from TASK-171, with PASS/FAIL anchors and the pole each provides. Each active **leads** one dimension; together they span the full evidence spectrum.

| Active | Leads | PASS anchor | FAIL anchor |
|---|---|---|---|
| **Creatine monohydrate** | Dose Adequacy | 5 g monohydrate (in-range) | 1 g creatine HCl (sub-dose, fairy-dust band) |
| **Magnesium** | Form & Bioavailability | glycinate / citrate (preferred) | oxide marketed "high elemental Mg" (poor form, misleading) |
| **Vitamin D3** | Safety Ceiling | 1,000–2,000 IU D3 (within UL) | 50,000 IU/day daily (UL breach) **or** D2 (weaker form) |
| **Caffeine** | Formulation Honesty | labeled 200 mg (disclosed) | hidden in "proprietary energy blend" (dose unknowable) |
| **Omega-3 (EPA/DHA)** | Evidence Strength | EPA/DHA for triglyceride lowering (well-established → Strong) | same omega-3 sold for a broad "brain & mood" claim (thin base → Weak/Insufficient) |

**Pole coverage check — every dimension has a PASS and a FAIL anchor:**

| Dimension | PASS anchor | FAIL anchor |
|---|---|---|
| Evidence Strength | EPA/DHA for TG lowering (Strong) | omega-3 broad "brain & mood" claim (Weak/Insufficient) |
| Dose Adequacy | creatine 5 g | creatine HCl 1 g |
| Form & Bioavailability | Mg glycinate/citrate; D3 | Mg oxide; D2 |
| Formulation Honesty | caffeine 200 mg labeled | caffeine in proprietary blend |
| Safety Ceiling | creatine 5 g (PASS control) + D3 1–2k IU | D3 50,000 IU/day |

Every dimension is exercised at both poles. **Creatine is deliberately dual-use** (Dose lead + Safety PASS control — a clean, no-UL active that proves Safety doesn't punish a good product). **Omega-3 also gives strong secondary coverage** beyond its Evidence lead: Dose (active EPA/DHA mg vs total fish-oil mass), Form (TG/rTG vs ethyl ester ladder), and Honesty (the "1,000 mg fish oil" misleading-mass trap) — so the Evidence probe is not single-purpose. The 5-active floor is justified: dropping to 4 would remove either the omega-3 claim-specific-tiering subsystem (Evidence isolated with form held constant + its Dose/Form/Honesty secondaries) or the proprietary-blend machinery (caffeine → Honesty) — both load-bearing.

**MVP inputs:** 5 dossiers + a ~12-product golden corpus (~2–3 constructed SKUs per active = the PASS/FAIL anchors). **Zero Israeli scrape required** — the engine is validated entirely on the live reference layer + constructed anchors (Phase 2). The constructed anchors are *engineering test fixtures*, not invented product claims published to consumers.

---

## 7. Scope boundaries

Mirrors TASK-171.

**MVP (this engine):** creatine · magnesium · vitamin D3 · caffeine · **omega-3 (EPA/DHA)**. Five dimensions, dossier backbone, 12-anchor golden corpus, live reference layer only.

**Phase 2 (harden + common shelf):** **ashwagandha (KSM-66) + the botanical / standardization subsystem** (branded-extract evidence does not transfer to the raw herb), iron (necessity/contraindication — the angle MVP under-tests — + toxicity), zinc, B12 (form depth), calcium, vitamin C, whey (amino-spiking), melatonin (~10× over-dosing), collagen, curcumin/turmeric. These exercise machinery MVP only stubs (necessity gating, amino-spiking detection, over-dose-as-norm).

> **Why ashwagandha / standardized botanicals are Phase 2, not MVP.** The botanical subsystem's core difficulty is *contested botanical evidence + extract standardization* — i.e. it depends on the **contested-evidence machinery the MVP deliberately defers** (out-of-scope item 3 below). An active whose central question is "does this branded-extract evidence even transfer, and is the underlying evidence settled?" is an *incoherent Evidence probe* for an MVP that refuses to adjudicate contested evidence. Omega-3 replaces it as the MVP Evidence probe because it isolates Evidence with uncontested per-claim tiers (form held constant). The KSM-66 insight (extract-specific evidence doesn't transfer to raw root) is preserved as a deferred note in §8.

> **Scope fence (anti-pull-forward).** The Phase 2 named actives above (iron, melatonin, whey, etc.) and their machinery (necessity gating, amino-spiking detection, over-dose-as-norm) are **listed for scope-fencing only and are NOT authorized work under TASK-171.** They enumerate what the MVP deliberately does *not* build — they are not a commitment to build them. No Phase-2 active or its machinery may be implemented under the TASK-171 / TASK-171A authorization; each is a separate, later authorization.

**Advanced (deferred — each needs machinery MVP lacks):**
- Full pre-workouts / sports stacks → **blend-level dose attribution** (splitting a blend total across named actives) — explicitly **out of MVP**.
- Probiotics → see sub-section below (v1.4 — Amendment C).
- Greens/detox powders, mushroom/adaptogen/nootropic blends.
- Hormone-adjacent & weight-loss → safety + regulatory-risk handling.

#### Probiotics: strain-resolved Evidence Dossiers (v1.4 — Amendment C, TASK-195 — Advanced / Phase 3+ scope)

Probiotics are defined as live microorganisms that, when administered in adequate amounts, confer a health benefit on the host. The clinical evidence base establishes that therapeutic benefits are **highly strain-specific and disease-specific**: pooling different taxonomic strains in evaluation leads to inaccurate conclusions regarding efficacy. A systematic review of 228 clinical trials demonstrated that different strains within the same species exhibit highly variable gastric-acid survival rates, mucosal adherence, and immunomodulatory properties. In screening of over 127 different *Lactobacillus* strains, only 3% met probiotic criteria for bile and acid resistance.

This evidence base establishes that **probiotics cannot be scored at the active level** (i.e., "probiotics" as a class, or even *Lactobacillus* as a genus) — efficacy evidence attaches to specific named strains. The SIE's `(active, dose, form, evidence)` unit must therefore resolve to the individual strain, not the organism type or genus.

**Probiotics scoring rules (Phase 3+ only — does NOT affect MVP or Phase 2 scope):**

1. **Strain-resolved Evidence Dossiers required.** Each named probiotic strain receives its own Evidence Dossier entry, not a shared active-level entry. Evidence tier is assigned per strain per studied indication. Pooling strains under a single tier is prohibited.

2. **Named strain = scorable; un-named strain = Insufficient.** A label that declares a specific strain (e.g., *Lactobacillus rhamnosus* GG, *Saccharomyces boulardii* CNCM I-745) is scorable against that strain's dossier. A label that declares only "probiotic blend," a genus without strain identifier, or a CFU count without strain name → Evidence tier = **Insufficient** regardless of CFU count. CFU quantity has no evidential meaning without strain identity.

3. **CFU viability at end-of-shelf-life is a separate gate.** The scored dose must represent live organisms at end-of-shelf-life, not at manufacture. The current SIE acquisition plumbing cannot verify this from a label; Phase 3+ requires either manufacturer-certified end-of-shelf-life data or a third-party stability assay. Until this gate is met, CFU dose adequacy cannot be scored (§2.2 Dose Adequacy remains unresolvable for probiotics).

4. **Strain-specificity applies to indication.** A dossier for *L. rhamnosus* GG covers antibiotic-associated diarrhea prevention (robust evidence — a named Cochrane indication) but does NOT cover "immune support" in general unless that specific strain has studied that endpoint. The claim-resolution rule (§2.1) applies: the on-label claim resolves to the strain's studied indication via the umbrella, not to any studied endpoint of "probiotics."

5. **This sub-section does NOT reopen MVP or Phase 2 scope.** Probiotics were explicitly deferred in v1.0 as "out of MVP" (§7 item 2: CFU/probiotic viability). This amendment adds the strain-resolution requirement so it is codified for Phase 3+ — not to authorize probiotic scoring under any current task. The deferred-to-hard-gate note in the SUPP-EV registry is updated (SUPP-EV-019 added).

**Source:** "Clinical and Pharmacological Assessment of Dietary Supplementation" (New Batch, 2026-06-06) — systematic review of 228 probiotic clinical trials; *L. rhamnosus* GG and *S. boulardii* CNCM I-745 strain-specific efficacy for AAD prevention; 3% viability rate among 127 *Lactobacillus* strains screened; meta-analysis of 63 depression and 49 anxiety RCTs showing strain-pooled but significant SMD improvements (noting high heterogeneity — the heterogeneity itself is evidence that strain pooling is masking differential effects).

**Explicitly out-of-scope machinery for MVP (named so Phase 2 doesn't assume it exists):**
1. **Blend-level dose attribution** — MVP treats a hidden blend as an Honesty cap, it does *not* try to estimate per-active doses inside a blend.
2. **CFU / probiotic viability** — no live-count or shelf-stability model.
3. **Contested-evidence handling** — genuine high-quality evidentiary conflict is flagged `contested` and the active is deferred, not force-tiered. (Mirrors Hard Rule 7: flag ambiguous, don't force a ruling.)
4. **Cross-product cumulative UL / stacking** — one SKU at a time.
5. **Necessity/deficiency gating as a score input** — necessity is dossier *context surfaced to the reader*, never a scored dimension in MVP (avoids health-advice drift). Binding under **SIE Invariant 1 — No-Necessity Rule** (Invariants block).

---

## 8. Evidence registry — `SUPP-EV-###` convention

Mirrors BSIP2's `EV-###` registry (`03_operations/bsip2/evidence_registry/`). The SIE keeps its **own** registry — `03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.{md,json}` — so food and supplement evidence never cross. **Any scoring rule that leans on an external source needs a `SUPP-EV-###` entry** with: concept, scientific rationale, evidence tier, source + citation, dimension affected, `should_affect_score_now`, risk-of-misuse, and Nutrition+Product D7 status.

**Seed entries** (facts asserted below that *inform a rule* — each flagged for **Phase-1 Research Agent verification** before it can move a score; numbers stated here are working values, not yet authoritative):

### SUPP-EV-001 — Creatine effective dose & no-UL
| Field | Value |
|---|---|
| concept | Creatine monohydrate effective dose ≈ 3–5 g/day maintenance; no established UL |
| dimension | Dose Adequacy (§2.2), Safety Ceiling (§2.5 PASS control) |
| evidence_tier | **Strong** (well-replicated, meta-analytic) |
| source | `literature` (PubMed meta-analyses); ISSN position stand — *verify exact citations Phase 1* |
| should_affect_score_now | false — pending dossier build + D7 |
| risk_of_misuse | treating no-UL as license for arbitrary mega-dose; use `upper_studied` fallback |
| d7_status | pending |

### SUPP-EV-002 — Magnesium oxide low bioavailability vs glycinate/citrate
| Field | Value |
|---|---|
| concept | Mg oxide has low fractional absorption; glycinate/citrate better absorbed; oxide high in *elemental* Mg per compound mass (the trap) |
| dimension | Form & Bioavailability (§2.3), Dose elemental basis (§2.2) |
| evidence_tier | **Moderate** (bioavailability studies; some heterogeneity) — *verify Phase 1* |
| source | `literature` + `pubchem` (MW → elemental fraction) |
| should_affect_score_now | false — pending |
| risk_of_misuse | conflating elemental content with absorbed dose; penalizing oxide twice (Form + Honesty must coordinate, §3) |
| d7_status | pending |

### SUPP-EV-003 — Vitamin D3 (cholecalciferol) > D2 for raising serum 25(OH)D; adult UL
| Field | Value |
|---|---|
| concept | D3 raises/maintains serum 25(OH)D more effectively than D2; adult UL = 4,000 IU/day (NIH ODS) |
| dimension | Form (§2.3, D3>D2), Safety Ceiling (§2.5, UL veto) |
| evidence_tier | **Strong/regulatory** (form: Moderate–Strong; UL: regulatory) — *verify UL value + age basis Phase 1* |
| source | NIH ODS Vitamin D fact sheet; `literature` (D2-vs-D3 RCTs) |
| should_affect_score_now | false — pending |
| risk_of_misuse | applying adult UL to a children's product; treating a clinician-directed weekly repletion SKU as a daily-use veto |
| d7_status | pending |

### SUPP-EV-004 — Caffeine effective dose & proprietary-blend hiding
| Field | Value |
|---|---|
| concept | Caffeine effective acute dose ≈ 3–6 mg/kg (≈200 mg adult); proprietary blends commonly hide per-active caffeine dose |
| dimension | Formulation Honesty (§2.4), Dose (§2.2), Safety (§2.5 high-dose/total caffeine) |
| evidence_tier | **Strong** (ergogenic); blend-hiding = label-practice observation |
| source | `literature`; `dsld` (blend-prevalence calibration) |
| should_affect_score_now | false — pending |
| risk_of_misuse | scoring "blend" by name vs hidden-dose by disclosure (penalize disclosure failure, not the word) |
| d7_status | pending |

### SUPP-EV-005 — Omega-3 (EPA/DHA): claim-specific tiers, dose basis, form ladder, mass-honesty trap
| Field | Value |
|---|---|
| concept | Same EPA/DHA molecule is tiered **per claim**: triglyceride lowering = **Strong**; broad "brain & mood" = **Weak/Insufficient**; cardiovascular-events = **contested/deferred** (REDUCE-IT vs STRENGTH — not tiered in MVP, §7). Effective EPA/DHA dose for TG lowering ≈ *working value, Phase-1 verify* (commonly cited ~2–4 g/day EPA+DHA). Form ladder: triglyceride / re-esterified triglyceride (preferred) > ethyl ester (acceptable, lower/slower bioavailability). Honesty trap: "1,000 mg fish oil" front label hides ~120–300 mg actual EPA+DHA — Dose must compare *active* EPA+DHA, not total fish-oil mass |
| dimension | Evidence Strength (§2.1, lead), Dose Adequacy (§2.2, active-fraction basis), Form & Bioavailability (§2.3, TG/rTG vs ethyl ester), Formulation Honesty (§2.4, misleading-mass) |
| evidence_tier | TG-lowering: **Strong** (RCT/meta-analytic); brain/mood: **Weak/Insufficient**; CV-events: **contested (deferred)** — *verify exact per-claim tiers + effective dose + form-ladder ranking Phase 1* |
| source | `literature` (per-claim RCTs/meta-analyses; REDUCE-IT/STRENGTH for the contested CV claim); `pubchem` (EPA/DHA + ester-form identity); `dsld` (EPA/DHA-vs-total-mass prevalence calibration) |
| should_affect_score_now | false — pending dossier build + D7 |
| risk_of_misuse | tiering the contested CV-events claim instead of deferring it; comparing total fish-oil mass instead of active EPA+DHA; treating ethyl ester as equivalent to TG/rTG without verifying the bioavailability gap |
| d7_status | pending |

> **Deferred Phase-2 note (ashwagandha / standardized botanicals).** Preserved so the KSM-66 insight is not lost: *stress/anxiety evidence is on standardized extracts (e.g. KSM-66 ~300–600 mg) and does **not** transfer to unstandardized raw root or unstudied doses; over-tiering a small/heterogeneous trial base is a risk.* This belongs to the **Phase 2** botanical/standardization subsystem because it depends on the contested-evidence machinery the MVP defers (§7). **Not** a live `SUPP-EV` in MVP — it gets its own `SUPP-EV-###` when the Phase-2 botanical subsystem is authorized.

*(Registry seeded; Phase 1 expands per active + per rule. `should_affect_score_now: false` on all until dossiers built and D7 co-signed.)*

---

## 9. EDPG firewall + D7 governance note

**Firewall (binding).** The integrations clients are a *fetch* capability. In the SIE:
- External sources (`dsld`, `literature`, `pubchem`, `il_gov_data`, `open_food_facts`) **calibrate or justify** a rule — they populate the Evidence Dossier and seed `SUPP-EV-###` entries, *with citations*.
- The **engine reads in-house BSIP0-S labels and the in-house dossier only** — never a live external value on the score path. The dossier is the firewall membrane: external facts are frozen, cited, tiered, and `verification_status: candidate` until promoted by the SIE admission gate (BSIP0-S + QA pass), exactly as a scrape would be.
- "LIVE-VERIFIED" for a client means *it reached the source*, not *the datum is true*. A DSLD dose or a PubChem identity does not become a scored fact until it clears the gate and carries a `SUPP-EV-###` + D7 co-sign.

**D7 governance.** Every SIE scoring rule requires **Nutrition + Product D7 co-sign** (either can block; disputed rules don't deploy — joint review). This methodology is the Phase-0 artifact for that co-sign; **D7 is now CO-SIGNED (Nutrition + Product)** — see §11 — authorizing Phase 1 only. The SIE keeps its own registry, its own constants, its own grade thresholds; the **frozen food invariants are structurally untouchable** because the engine is a separate tree (no shared `constants.py`, no shared golden corpus). `roadmap_impact: true` → the CC close-readiness gate applies before TASK-171A can close.

**Consumer-language note.** This internal doc uses technical terms freely. Consumer-facing SIE copy (Phase 4) inherits Bari's rules: no "NOVA / cap / floor / BSIP / structural_class" language, no health claims, evidence-tiered uncertainty where relevant. Phase 4 defines a *separate verdict model* from the food comparison pages (a supplement verdict is "worth taking?", not "best on the shelf").

---

## 10. Open questions for Product (D7 review)

1. **Grade bands.** Adopt BSIP2's band thresholds (S90/A80/B65/C50/D35/E0) for reader consistency, or set supplement-specific bands in Phase 2? (Recommend: start aligned, allow Phase-2 drift.)
2. **Honesty cap severity.** Should a hidden-dose proprietary blend cap at C-band (still "works partially, asks for trust") or D-band (treat unverifiable dose as presumptively failing)? Calibration-pending; Nutrition leans C-band unless a *core* active is hidden, then D.
3. **Necessity surfacing.** Confirm necessity/contraindication stays **reader context only**, never a scored input in MVP (avoids health-advice drift). Nutrition recommends yes. *(Resolved D7 — now codified as SIE Invariant 1; see §11.)*
4. **Clinical-megadose exemption.** Accept the "labeled regimen decides" rule for the 50,000 IU weekly-vs-daily D3 split, or veto all megadoses in MVP for simplicity? (Recommend: keep the regimen discriminator; it's the honest read.)
5. **Constructed golden corpus.** Confirm constructed PASS/FAIL SKUs are acceptable as engineering fixtures (they are not published consumer claims) for Phase-2 validation, deferring real Israeli SKUs to Phase 3.

*(All five resolved at D7 — see §11.)*

---

## 11. D7 decisions (resolved)

The Product Agent's D7 co-sign resolved the five §10 open questions. Recorded here so they do **not** reopen in Phase 2.

1. **Grade bands — RATIFIED.** Start aligned with BSIP2 bands (S 90 / A 80 / B 65 / C 50 / D 35 / E 0); any supplement-specific drift must be *earned* with Phase-2 calibration data, not assumed. (Resolves §10 Q1; bands in §4 remain calibration-pending pending Phase-2 evidence.)
2. **Honesty cap severity — RATIFIED with C1.** C-band cap by default; **D-band** when a *core active* (per the §2.4 core-vs-secondary definition) is the hidden one. (Resolves §10 Q2; reflected in §2.4 and §3 cap 3.)
3. **Necessity surfacing — RATIFIED.** Reader-context-only, never scored — now codified as **SIE Invariant 1 — No-Necessity Rule** (Invariants block). (Resolves §10 Q3.)
4. **Clinical-megadose exemption — RATIFIED.** "Labeled regimen decides": a clearly-labeled weekly clinical-repletion D3 SKU is exempt from the consumer-daily veto (flagged `clinical_use` + Safety note); a 50,000 IU product labeled for *daily* use is vetoed. (Resolves §10 Q4; reflected in §2.5 edge cases.)
5. **Constructed golden corpus — RATIFIED.** Constructed PASS/FAIL fixtures are accepted for Phase-2 validation as engineering test fixtures (not published consumer claims); real Israeli SKUs deferred to Phase 3. (Resolves §10 Q5.)

**D7 status = CO-SIGNED (Nutrition + Product)** once these edits land. This co-sign authorizes **Phase 1 (dossier build) only.** A supplement category go-live remains a separate **D10 / D1** decision; numeric weights, thresholds, and grade bands stay **calibration-pending** until Phase 2 and carry `SUPP-EV-###` + D7 co-sign before any value can move a published score.

---

### v1.1 amendment decisions (post-D7 scope refinements)

Two owner-approved refinements applied in v1.1. Both **tighten** the MVP; neither changes the 5-dimension model, scoring logic, grade semantics, or the calibration-pending numbers. Recorded here for re-ratification.

6. **(D6) MVP Evidence probe = omega-3 (EPA/DHA); ashwagandha → Phase 2.** Ashwagandha is an incoherent Evidence probe for an MVP that *defers* contested-evidence machinery — its core difficulty (contested botanical evidence + branded-extract standardization) is exactly that deferred machinery. Omega-3 isolates the Evidence dimension better (same molecule/form: Strong for TG lowering, Weak/Insufficient for "brain & mood" — claim held as the variable) and adds Dose/Form/Honesty secondary coverage. The omega-3 CV-events claim is deliberately excluded as an anchor (genuinely contested → deferred). Ashwagandha + the botanical/standardization subsystem move to Phase 2; the KSM-66 non-transfer insight is preserved as a deferred note (§7, §8 SUPP-EV-005). **Status: v1.1 amendment — RE-RATIFIED (Product, 2026-06-03).**
7. **(D7) Dossier lifecycle / maintenance model adopted, incl. maintenance-cost go/no-go gate.** The dossiers (not the engine) are the dominant operational risk; their failure mode is *silent misranking* from a stale, non-erroring dossier. v1.1 makes this first-class (§5.1 + schema): stable-vs-drift field split, staleness *detection* via re-runnable `literature` (raises a human review flag, never auto-moves a score), change-control (any score-moving drift-field change = D7 + `SUPP-EV-###` bump + golden-corpus re-validation, logged in `change_log`), preference for externally-maintained authorities (NIH ODS/EFSA UL re-sync over hand-maintenance), and an **MVP success metric that measures real per-dossier build + maintenance cost and surfaces it as a Product go/no-go input before any scale-up.** **Status: v1.1 amendment — RE-RATIFIED (Product, 2026-06-03); Product owns the maintenance-cost go/no-go gate (evidence required: per-dossier author-hours drift-vs-stable, re-verification cadence + adjudication-hours per staleness flag, authority-leverage ratio, per-active cost variance).**

> **Re-ratification note.** v1.0's D7 co-sign stands for the unchanged core. The v1.1 delta (one MVP active swapped; one operational gate added) was **re-ratified by Product 2026-06-03** — v1.1 now *is* the co-signed artifact of record (D7 CO-SIGNED, Nutrition + Product). Numbers remain calibration-pending; no score ships; a supplement category go-live is a separate D10/D1 decision Product has not made.

---

### v1.2 amendment decisions (Phase-2 specification additions — RE-RATIFIED by Product 2026-06-03)

Three Phase-2 specification additions applied in v1.2, surfaced by two owner challenges pressure-testing the engine's *attribution* (does it tell failure modes apart, and explain them). All three are **design refinements**: they make the existing model implementable and honest in its trace. **Neither the 5-dimension model, the grade bands, the tiers, nor any calibration-pending number changes.** Recorded here for Product re-ratification.

8. **(D6/D7) Dose short-circuit rule — Evidence-gated Dose.** If Evidence tier = Insufficient, **Dose Adequacy is N/A and contributes no positive credit** (§2.2). "Effective dose" is defined by the evidence; with no evidence there is no effective dose, so a no-evidence active must never read "well-dosed" off `market_range_dsld` (market prevalence ≠ efficacy). Interacts with the §3 Insufficient-Evidence ceiling (cap 1): the ceiling caps the grade, the short-circuit neutralizes the Dose sub-score (→ N/A, excluded from the blend, not 0) so the trace and explanation attribute the failure to evidence, not dose. **Status: v1.2 amendment — RE-RATIFIED (Product, 2026-06-03).**
9. **(D6/D7) Failure attribution & the explanation layer (§12).** The engine emits a machine-readable "why" = the **binding constraint** (the cap/veto that actually bound the grade under §3 most-restrictive-wins), not merely the lowest sub-score. Structured trace contract (5 sub-scores + firing caps/vetoes + binding constraint + dossier facts used) makes the "why" deterministically regenerable. Inherits BSIP2 explanation discipline (grounded-in-real-trace, dominant-driver/anti-attribution, banned-phrase list — *BSIP2 Explanation Engine v2 + Explainability System v1*) + the No-Necessity firewall (SIE Invariant 1) + Hard Rule 5. **Phase split codified:** machine-readable "why" = Phase 2; consumer-facing Hebrew prose = Phase 4. **Status: v1.2 amendment — RE-RATIFIED (Product, 2026-06-03).**
10. **(D6/D7) Golden corpus gains the attribution axis (§13).** Beyond §6's per-dimension PASS/FAIL anchors, the corpus adds **three named failure archetypes** the engine must both *distinguish* (sub-score signature) and *explain* (binding constraint): good-active/wasted → **D**; bad-active/excellent-product → **E** (evidence ceiling); good-active/dangerous → **E** (safety floor). The decisive test: the **bottom two are both E with inverted signatures** — Phase-2 validation must confirm the explanation attributes them differently ("no reliable evidence" vs "unsafe dose") and never confuses them. Constructed engineering fixtures (per §11 D7 ruling 5), not published consumer claims. **Status: v1.2 amendment — RE-RATIFIED (Product, 2026-06-03).**

11. **(D6/D7) Safety veto-vs-note classification — standing meta-rule (FLAG-2, Phase-2 build).** The hard Safety veto is reserved for **toxicity/harm ceilings**; a **reversible self-limiting tolerance threshold** (e.g. GI/osmotic) sets a graded **Safety NOTE** band, not a veto, with the veto resting on the higher toxicity-relevant bound. Applied to magnesium: hard veto → NIH/IOM **350 mg** supplemental; EFSA **250 mg** (reversible GI) → Safety NOTE. **This supersedes the earlier "EFSA 250 governs the veto / most-conservative-tolerance governs" ruling** (SUPP-EV-002). Reversible-vs-toxicity classification is a dossier-level, Nutrition-owned, cited judgement; the engine never infers it. **Status: CO-SIGNED (Nutrition D6/D8 + Product D7, 2026-06-03); candidate / no score-movement.** Validated: effective 300 mg Mg → A/Safety-note, 423 mg → E/veto; 14/14 golden fixtures green.

> **v1.2 ratification status.** v1.1 stands as the co-signed artifact for the unchanged core. The v1.2 delta (dose short-circuit; failure-attribution/explanation layer; golden-corpus attribution axis) is **RE-RATIFIED by Product 2026-06-03** (D7) and is now part of the co-signed artifact of record. It changes no number, no dimension weight, no tier, no grade band — it specifies *attribution and trace honesty* for the Phase-2 build. **Product D7 re-ratification GRANTED; TASK-171C (Phase 2) cleared to build against this addendum.** Numbers remain calibration-pending; a supplement category go-live remains a separate D10/D1 decision.

---

### v1.3 amendment decision (claim-resolution rule — D6-AUTHORED, PENDING Product D7 co-sign)

One owner-approved scoring-rule change applied in v1.3. **Unlike v1.1/v1.2, this is NOT a design refinement — it moves a real grade** (the magnesium PoC E/34 → expected B/A once Data implements it), so it is a scoring-rule change that **requires Product D7 co-sign before it can ship** (per the SIE governance gate, §9, and Bari Hard Rule 8 — both Nutrition and Product must co-sign; either can block).

12. **(D6) Claim-resolution via an authored, cited dossier umbrella-map — moderate posture.** The engine read Evidence off the *literal label wording*; because supplements are legally restricted to vague structure/function claims, this wrongly floored honest products (the magnesium PoC: preferred form, honest, safe → **E** because "supports bone, heart, nerve & muscle health" matched no studied endpoint). v1.3 replaces the §2.1 "vague claim → Insufficient" default with a **claim-resolution procedure**: a vague claim resolves to the active's studied endpoint(s) via the **pre-authored, cited `structure_function_umbrella`** (§5); Evidence scores the **best plausibly-mapped tier**; cap-1 Insufficient fires **only when nothing maps.** The **"plausibly maps" boundary** is the **moderate "fair but skeptical"** middle (owner-approved): an endpoint maps iff it is a **recognized physiological correlate** of the claim term **and** is pre-authored + cited — rejecting both the *narrow* "exact-endpoint-verbatim" posture (re-floors compliant labels) and the *broad* "any-loosely-related" posture (free-association loophole). The over-promise catch (§2.4) keeps it honest: an over-specific lie ("clinically proven to cure X") resolves to the *real* (often Weak) tier **and** eats an Honesty debit. **Approach ruled by Product (TASK-171E); scientific authoring + the "plausibly maps" boundary owned by Nutrition.**
    - **Magnesium umbrella authored** against live `literature` evidence: heart→BP=**Moderate** (maps, best); bone→BMD=**Weak**; muscle→sarcopenia=**Weak**; nerve→**does NOT map**. PoC resolves to **Moderate** → expected **B/A**. `SUPP-EV-006` added.
    - **Three golden fixtures specified** (§13.4) for Data to build (vague/evidenced→B/A; vague/snake-oil→E; over-specific-false→D).
    - **Status: v1.3 amendment — D6-AUTHORED (Nutrition, 2026-06-03), moderate posture owner-approved. PENDING (a) Product D7 co-sign and (b) Data engine implementation.** Everything `candidate` / `should_affect_score_now: false`; **nothing ships** until D7 co-sign + implementation + golden-corpus validation.

> **v1.3 ratification status.** v1.2 stands as the co-signed artifact of record for the unchanged core. The v1.3 delta (claim-resolution rule + magnesium umbrella + 3 fixtures) is **D6-authored by Nutrition and pending Product D7 co-sign + Data implementation.** Because it **moves a published-equivalent grade** (`roadmap_impact`-relevant), it must not be treated as ratified on Nutrition's authoring alone — Product D7 co-sign is required (Hard Rule 8). The magnesium PoC stays **E/34** in the artifact until Data implements the rule and the engine re-scores it under co-signed logic; the B/A is the **expected** result, not a shipped one.

---

## 12. Failure attribution & the explanation layer (Phase-2 deliverable)

A grade alone is not enough. A supplement that scores **E** can be E for very different reasons — no evidence behind the active, a dose hidden in a blend, or a dose that is unsafe — and a consumer (and our own QA) must be able to tell *which*. The engine must therefore emit a **machine-readable "why it failed,"** not just a number and a letter. This section specifies that "why" as a Phase-2 deliverable. **Scope fence:** the **machine-readable attribution logic here = Phase 2**; the **consumer-facing Hebrew prose that renders it = Phase 4** (§9 consumer-language note, separate verdict model). This section builds the former and is silent on the latter's wording.

### 12.1 Binding-constraint attribution rule

> **Binding-constraint attribution rule (v1.2).** The explanation names the **binding constraint** — the single cap, veto, or gate that *actually determined the grade* under §3 most-restrictive-wins — **not** merely the lowest sub-score. The engine identifies the binding constraint as follows: it evaluates the weighted blend and every applicable cap/floor/veto (§3.2), takes the **most-restrictive outcome** (the lowest effective ceiling, or the veto floor, that the final grade rests on), and records *that mechanism* as `binding_constraint`. If no cap/floor/veto fired and the grade came from the weighted blend itself, the binding constraint is the **dominant limiting dimension** of the blend (the lowest-weighted-contribution dimension that, if lifted, would raise the grade band). The lowest *raw sub-score* is reported only as supporting detail; it is **never** asserted as the cause unless it *is* the binding constraint. (This is the anti-attribution discipline of *Bari Explainability System v1*, ported: the dominant driver is the constraint that bound the outcome, not whichever number is smallest.)

Why this matters concretely: a product can have its lowest sub-score in Form (say 40) yet be graded E by the **Insufficient-Evidence ceiling** (cap 1). Naming "weak form" as the reason would be wrong — Form did not bind the grade; the evidence ceiling did. The binding-constraint rule forces the explanation to say "no reliable evidence for this claim," which is the truthful cause.

**Recording in the trace.** The engine writes, per score: the firing mechanism (`cap_1_insufficient_evidence` | `cap_2_fairy_dust_hidden_dose` | `cap_3_honesty_core` / `cap_3_honesty_secondary` | `veto_safety` | `floor_form_evidence_coupling` | `blend_dominant_limit`), the ceiling/floor value it imposed, and a one-line machine reason keyed to that mechanism. When multiple caps fire, the **most-restrictive wins** and *that* is the binding constraint; the others are recorded as `also_fired` (supporting, not causal).

### 12.2 Structured trace contract

Every score emits a structured trace sufficient to **regenerate the "why" deterministically** — no second pass over the dossier or the literature, no recomputation that could drift. The trace is the contract between the scorer (Phase 2) and the explanation renderer (Phase 4):

```yaml
# emitted per scored SKU (Phase 2)
trace:
  sku_id: "<in-house BSIP0-S id>"
  active: "<canonical_name>"           # resolved active(s)
  on_label_claim: "<claim text read off the label>"   # selects the dossier tier
  sub_scores:                          # all five, N/A allowed (see §2.2/§3)
    evidence: { value: 22, tier: "Insufficient" }
    dose:     { value: "N/A", reason: "evidence_insufficient_dose_short_circuit" }
    form:     { value: 88 }
    honesty:  { value: 95 }
    safety:   { value: "neutral" }
  caps_vetoes_fired:                   # every guardrail that triggered, with its ceiling/floor
    - { mechanism: "cap_1_insufficient_evidence", ceiling: 34 }
  binding_constraint:                  # the ONE that bound the grade (§12.1)
    mechanism: "cap_1_insufficient_evidence"
    machine_reason: "no_reliable_evidence_for_claim"
  also_fired: []                       # other caps/vetoes, supporting not causal
  dossier_facts_used:                  # exact in-house facts the verdict rests on (firewall: dossier, not live API)
    - { field: "claims[on_label_claim].evidence_tier", value: "Insufficient", supp_ev: "SUPP-EV-###" }
  final: { score: 22, grade: "E" }
```

Contract guarantees: (a) every sub-score is present (N/A explicit, never silently dropped); (b) every firing cap/veto is listed; (c) exactly one `binding_constraint` is named; (d) the `dossier_facts_used` are the *in-house dossier* facts (never a live external value — EDPG firewall, §9), each carrying its `SUPP-EV-###`. Given this trace, the "why" is regenerable with no access to anything but the trace itself.

### 12.3 Inherited explanation discipline (reuse, do not reinvent)

The SIE explanation layer **inherits the BSIP2 explanation discipline** rather than inventing a parallel one. Specifically reuse:

- **Grounded-in-real-trace (no fabricated reasons).** Every clause of the "why" must trace to a value in §12.2 — a sub-score, a fired mechanism, or a `dossier_facts_used` entry. No reason may be asserted that is not in the trace. (*BSIP2 Explanation Engine v2*: explanations rebuilt from real trace data; no invented drivers.)
- **Dominant-driver / anti-attribution rules.** Attribute the failure to the **binding constraint** (§12.1), not the smallest number; do not stack multiple "reasons" when one mechanism bound the grade. (*Bari Explainability System v1*: anti-attribution dominant-driver rules; Tier-4 internals never surface as the named cause.)
- **Banned-phrase list.** Port and extend the BSIP2 banned-phrase list (the 9 banned phrases of *Explanation Engine v2*) with SIE-specific bans: no "well-dosed" / "clinically dosed" when Dose = N/A; no "proven" / "guaranteed" efficacy language; no necessity/should-take phrasing (Invariant 1). The full SIE banned-phrase list is authored in Phase 4 (consumer prose) but the **machine reasons** in §12.2 must already avoid efficacy-overclaim and necessity tokens.
- **No-Necessity firewall (SIE Invariant 1).** The "why" never states or implies the reader needs (or does not need) the active. A binding-constraint reason describes the *product's delivery* ("no reliable evidence for this claim," "dose hidden in a blend," "dose exceeds the safe ceiling"), never the reader's *need*.
- **Hard Rule 5 (no health claims).** The explanation describes scoring architecture — evidence, dose, form, honesty, safety — never a diet or health outcome for the reader.

### 12.4 Phase split (scope fence)

| Layer | Phase | What it is |
|---|---|---|
| Machine-readable attribution logic (binding-constraint rule, structured trace, machine reasons) | **Phase 2** (TASK-171C) | This section. Deterministic, language-free, validated against §13. |
| Consumer-facing Hebrew prose (the verdict a reader reads) | **Phase 4** | Separate verdict model (§9); renders the Phase-2 trace into Hebrew under Bari consumer-language rules. Not specified here. |

State explicitly: **Phase 2 must not author consumer prose, and Phase 4 must not invent attribution logic** — Phase 4 may only render what the Phase-2 trace already determined. This fence prevents the explanation from drifting away from the score.

---

## 13. Golden corpus: the attribution axis (Phase-2 validation spec)

The §6 golden corpus exercises each **dimension** at both poles (PASS/FAIL anchors). v1.2 adds an orthogonal **attribution axis**: a small set of **named failure archetypes** the Phase-2 engine must both (a) **distinguish** — produce the right sub-score *signature* — and (b) **explain** — name the right *binding constraint* (§12.1). Distinguishing without explaining is insufficient: two products can land on the same grade for opposite reasons, and the engine must not confuse them.

### 13.1 The three failure archetypes

| Archetype | Expected grade | Required sub-score signature | Required machine "why" (binding constraint) |
|---|---|---|---|
| **Good active / wasted** (e.g. 1 g fairy-dust creatine) | **D** | Evidence **HIGH** · Dose **LOW** (fairy-dust band) · Form/Honesty/Safety ok | "underdosed — a sound active at roughly one-fifth of the studied dose" (binding = `cap_2_fairy_dust_hidden_dose`) |
| **Bad active / excellent product** (no-evidence active, impeccably made) | **E** (evidence ceiling) | Evidence **LOW** (Insufficient) · Dose **N/A** · Form **HIGH** · Honesty **HIGH** · Safety ok | "no reliable evidence for this claim" (binding = `cap_1_insufficient_evidence`) |
| **Good active / dangerous** (e.g. 50,000 IU D3 daily) | **E** (safety floor) | Evidence **HIGH** · Safety **VETO** · Dose/Form may be ok | "dose exceeds the safe ceiling" (binding = `veto_safety`) |

### 13.2 The decisive test — inverted-signature E pair

> **Decisive validation test (v1.2).** The **bottom two archetypes are both graded E**, but for **opposite reasons and with inverted sub-score signatures**: the bad-active/excellent-product is `Evidence LOW · Safety ok` (capped by the evidence ceiling), while the good-active/dangerous is `Evidence HIGH · Safety VETO` (floored by safety). Phase-2 validation **must confirm the explanation layer attributes these two differently** — one says *"no reliable evidence"* (nothing behind it), the other says *"unsafe dose"* (the active is sound, the dose is not) — and **never confuses them.** A scorer that returns "E" for both but cannot tell them apart in the `binding_constraint` has failed this test even if both grades are numerically correct. This is the single most important attribution check in the SIE.

The first archetype (good-active/wasted → **D**) is the *distinguishing-by-grade* control: a sound active at a sub-therapeutic dose should land a band above the evidence-ceiling/safety-floor E's, attributed to `cap_2` (fairy-dust), never to "no evidence" (the evidence is HIGH) and never to safety (the dose is too *low*, not unsafe). It guards against the engine collapsing all three failures into one undifferentiated "bad supplement."

### 13.3 Construction & governance

These archetypes are **constructed engineering fixtures**, not published consumer claims — consistent with the **§11 D7 ruling 5** (constructed PASS/FAIL SKUs accepted for Phase-2 validation; real Israeli SKUs deferred to Phase 3). Each fixture is a synthetic `(active, dose, form, label-claim)` tuple chosen to force a specific signature and binding constraint; none is attributed to a real brand or shipped to a consumer. They live with the §6 12-anchor corpus in `03_operations/supplement_engine/proto_v0/` (Phase 2) and are versioned with the golden corpus — any change to an archetype's expected signature/binding constraint is a golden-corpus change and triggers the §5.1 re-validation discipline. The fixtures reuse the MVP actives (creatine for wasted-dose, an Insufficient-claim active for the evidence-ceiling E, D3 50,000 IU for the safety-floor E) so no new dossier is required to validate the attribution axis.

### 13.4 Claim-resolution fixtures (v1.3 — proves the rule is fair, not a loophole)

The v1.3 claim-resolution rule (§2.1) adds **three golden fixtures** that prove resolution *helps honest products without opening a loophole*. They are constructed `(active, dose, form, label-claim)` tuples (per §13.3 governance — no real brand, not shipped) for Data to build in Phase 2. The decisive property: **fixture R1 must NOT be reachable by fixture R2** (a vague claim resolves only when the active genuinely has a mapped endpoint), and **fixture R3 must NOT earn R1's grade** (a specific lie resolves to the real low tier AND eats an Honesty debit).

| # | Fixture | Construction (active · dose · form · label claim) | Expected resolution | Expected grade | Binding constraint | What it proves |
|---|---|---|---|---|---|---|
| **R1** | **vague-claim / active-has-evidence** | magnesium · 200 mg elemental · bisglycinate (preferred) · **"supports bone & muscle health"** (compliant vague) | umbrella resolves: bone→BMD=Weak, muscle→sarcopenia=Weak, (heart not on this label) → **best mapped = Weak**; *(the real PoC, which also says "heart", resolves heart→BP=**Moderate**)* | **B/A** (NOT E). The PoC variant with "heart" → **Moderate** → solidly B/A; a bone+muscle-only variant → **Weak** → still off the cap-1 floor (C/B, not E) | **blend** (`blend_dominant_limit`), **NOT** `cap_1_insufficient_evidence` — cap-1 must **not** fire because an endpoint mapped | Resolution lifts an honest, well-formed, safe product off a wrongful E. cap-1 fires **only** when nothing maps. |
| **R2** | **vague-claim / snake-oil** | a constructed active whose `structure_function_umbrella` has **every** label phrase → `resolves_to: null` (no recognized cited correlate for any term on the label) · any dose · any form · **"supports wellness & vitality"** | umbrella resolves: **nothing maps** (all keys null) | **E** | **`cap_1_insufficient_evidence`** (ceiling 34); Dose = **N/A** (dose short-circuit, §2.2) | The skeptic half of the moderate posture: resolution is **not** a free pass. An active with no mapped endpoint still floors at E exactly as before. R2 is the control that R1 cannot reach by saying something vague. |
| **R3** | **over-specific false claim** | magnesium · 200 mg elemental · bisglycinate · **"clinically proven to cure insomnia"** (over-specific over-promise) | sleep phrase resolves to magnesium's **sleep endpoint = Weak** (real tier, §2.1 step 2); "clinically proven" + "cure" + named condition → **Honesty claim-vs-substance gap fires** (§2.4, up to cap-3 on the core active) | **D** (or worse) — marked down, **NOT** a free A | **`cap_3_honesty_core`** (core-active over-claim) *and* a Weak Evidence sub-score; the more-restrictive of (cap-3 ceiling, Weak-tier blend) binds | Resolution is **not** a loophole: a confident lie resolves to the *real* (Weak) tier **and** eats an Honesty debit. Honest vagueness (R1) outscores a confident lie (R3) on the *same active*. |

**Cross-fixture invariants Phase-2 validation must assert:**
- **R1 ≠ R2 by mapping, not by grade luck:** R1's `binding_constraint` must be `blend_dominant_limit` (cap-1 did not fire); R2's must be `cap_1_insufficient_evidence` (cap-1 fired). If R1 ever shows `cap_1`, resolution failed to fire and the rule is broken.
- **R3 < R1 on the same active (magnesium):** the over-specific lie must grade **below** the honest-vague version, with `cap_3_honesty_core` (or the Weak tier) binding. If R3 ever reaches R1's band, the over-promise catch (§2.4) failed and resolution became a loophole.
- **No invented tiers:** every mapped endpoint in R1/R3 traces to a cited `structure_function_umbrella` key (firewall: dossier, not live API). R2's null mappings are the *absence* of a cited correlate, recorded explicitly.

These fixtures reuse the MVP magnesium dossier (R1, R3) plus one constructed all-null umbrella active (R2) — no new evidence dossier is required, consistent with §13.3.
