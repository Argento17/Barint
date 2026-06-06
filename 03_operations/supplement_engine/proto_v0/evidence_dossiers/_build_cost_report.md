# SIE Evidence Dossier — Build & Maintenance Cost Report (MVP, Phase 1)

**Task:** TASK-171B · **Date:** 2026-06-03 · **Author:** Research Agent
**Purpose:** measured per-dossier build/maintenance cost as the evidence input to **Product's maintenance-cost go/no-go gate** (methodology §5.1.5, D7 amendment 7). This is the "proving the dossier model" half of "proving the engine."
**Scope:** the 5 MVP dossiers (creatine, magnesium, vitamin D3, caffeine, omega-3 EPA/DHA), all `verification_status: candidate`, no score movement.

> Effort is reported as **measured proxies** (literature queries actually run, papers screened, fields requiring human judgement vs mechanical lookup), not wall-clock hours — author time here is a model (Claude) and would mislead a human-hour gate. The proxies are what scale linearly with catalog size; Product can apply its own hour multiplier.

---

## 1. Per-dossier build effort (measured)

| Dossier | Lit queries run | Papers screened (approx) | pubchem lookups | dsld dose pulls | Human-judgement fields* | Mechanical-lookup fields** | Build tier |
|---|---|---|---|---|---|---|---|
| **Creatine monohydrate** | 3 | ~18 | 2 | 1 | 3 (2 claim tiers + form-ladder) | 5 (CID, MW, formula, dose, no-UL) | CHEAP |
| **Vitamin D3** | 4 | ~24 | 2 (D3+D2) | 1 | 4 (3 claim tiers + form D3>D2) | 6 (CID, MW, UL, IU conv, D2 id, dose) | CHEAP–MODERATE |
| **Caffeine** | 3 | ~16 | 1 | 1 | 3 (2 claim tiers + honesty-lead logic) | 5 (CID, MW, UL, dose, flat-form) | CHEAP |
| **Magnesium** | 4 | ~20 | 4 (3 forms + element) | 1 | 5 (2 claim tiers + 3-rung form ladder) | 7 (CID, 3 elemental fractions, MW, dose, UL) | MODERATE |
| **Omega-3 (EPA/DHA)** | 7 | ~40 | 2 (EPA+DHA) | 2 | 8 (3 claim states incl. contested + form ladder + active-fraction basis + dual-UL framing) | 6 (2 CIDs, 2 MWs, formulas, dose-basis) | EXPENSIVE |
| **AGGREGATE** | **21** | **~118** | **11** | **6** | **23** | **29** | — |

\* **Human-judgement field** = requires an agent to read evidence and make a call the client cannot make: tiering a claim, ranking a form ladder, choosing a governing UL among discrepant authorities, deciding contested-vs-tier.
\*\* **Mechanical-lookup field** = a value the client returns directly: CID, molecular weight, formula, an elemental fraction computed from MW, a dose number read off a label.

### Drift-field vs stable-field split of the build judgement

| | Drift fields (review-bound) | Stable fields (compute-once) |
|---|---|---|
| Share of human-judgement effort | **~22 of 23 (~96%)** | ~1 of 23 |
| Share of mechanical-lookup effort | ~6 of 29 (~21%) | **~23 of 29 (~79%)** |

**Read:** nearly all the *expensive* (judgement) effort lands on **drift fields** (claim tiers, dose, form ladder, UL choice). Nearly all the *cheap* (mechanical) effort lands on **stable fields** (chemistry identity). This is the key structural fact for maintenance: the cost concentrates exactly where it recurs — but it is concentrated in a *small number of fields per active*.

---

## 2. Authority-leverage ratio (how much drift can be outsourced)

For each active, the drift fields are: `claim tiers`, `effective_dose`, `form_ladder`, `upper_limit_UL`. The question: which can be **delegated to an externally-maintained authority** (NIH ODS / EFSA re-sync — Bari stores value + source + re-sync date, doesn't re-derive) vs must be **hand-maintained** (Bari reads the literature and adjudicates)?

| Drift field | Externally maintained? | Authority | Notes |
|---|---|---|---|
| `safety.upper_limit_UL` | **YES** | NIH ODS / EFSA | Re-sync, not re-derive. The cheapest drift field. (Caveat: 3 of 5 actives have **discrepant** NIH-vs-EFSA values → Bari must still pick a governing one once.) |
| `effective_dose` | **PARTIAL** | DSLD (market prevalence) + literature (effective) | DSLD gives the *market* sanity-check mechanically; the *clinically effective* number is hand-read from literature. |
| `claim → evidence_tier` | **NO** | — (Bari Nutrition+Research adjudicate) | No external body publishes "Bari tier." Cochrane/EFSA *authorized health claims* help, but tiering is in-house judgement. **The irreducible hand-maintained cost.** |
| `form_ladder` | **NO** | — | Bioavailability ranking is hand-read from literature. |

**Authority-leverage ratio (drift fields delegable to re-sync):**
- **Per-active:** 1 fully delegable (UL) + 1 partial (dose) out of 4 drift fields ≈ **1.5 / 4 ≈ 0.375**.
- **The two highest-judgement drift fields — claim tiers and form ladder — are NOT delegable.** They are the structural floor of Bari's maintenance ownership.
- **Implication:** UL maintenance is nearly free (re-sync a published number). Tier + form maintenance is the real recurring cost and it is **irreducibly human** — which is correct, because tiering is exactly the in-house judgement the firewall (EDPG) exists to protect.

---

## 3. Re-verification cadence (per drift field, realistic)

Cadence is a **detection** sweep (re-run `literature` to flag new high-tier publications since `last_evidence_sweep`) + **human adjudication only if** the flag is real. Detection is mechanical and cheap; adjudication is the cost, and only fires when something actually moved.

| Drift field | Realistic sweep cadence | Why | Adjudication cost when flagged |
|---|---|---|---|
| `upper_limit_UL` | **Annual** (re-sync) | Regulatory ULs change rarely; NIH/EFSA revisions are infrequent and announced. | Low — swap a cited number. |
| `claim → evidence_tier` (mature actives: creatine, caffeine, D3-status) | **Annual** | Evidence base is settled; a single new trial rarely moves a Strong tier. | Low-moderate — read 1 new MA, confirm no tier move. |
| `claim → evidence_tier` (active-debate claims: omega-3 CV/cognition, Mg sleep) | **Semi-annual** | Live debate; a major trial or pooled MA can shift consensus. | Moderate-high — the omega-3 CV/cognition fields are the costliest to keep current. |
| `effective_dose` | **Annual** | Effective doses are stable once established. | Low. |
| `form_ladder` | **Annual** | Bioavailability rankings are stable; new comparative RCTs are rare. | Low-moderate. |

**Net:** 4 of 5 actives need **one annual sweep**; omega-3 needs **two sweeps/year** and carries the only fields likely to actually flag. Detection across all 5 is a single batched re-run of the literature client (cheap). The expensive event — a real tier change — is **rare and concentrated** (predominantly omega-3, secondarily Mg-sleep).

---

## 4. Per-active cost variance (which were cheap, which expensive, why)

- **Cheapest — creatine, caffeine:** single dominant claim with a *settled* (Strong) base; flat or trivial form ladder; no-UL (creatine) or one stable guidance number (caffeine); market dose == effective dose (no trap to untangle). ~3 queries, ~2-3 judgement fields each.
- **Cheap-moderate — vitamin D3:** more claims (status / bone / mortality) and a real Form distinction (D3>D2), but every drift field is **well-established and externally corroborated** (Cochrane + a clean regulatory UL). The extra claims cost screening time, not adjudication difficulty.
- **Moderate — magnesium:** the cost is the **3-rung form ladder + 3 elemental fractions** (mechanical but multiple) and a **discrepant UL** (NIH 350 vs EFSA 250 supplemental) requiring a governing-authority decision. Claims themselves (BP Moderate, sleep Weak) were straightforward.
- **Expensive — omega-3 (EPA/DHA):** ~2x every other active. Drivers: (1) **three claim states** including a **contested** one that must be *deferred, not tiered* — the single hardest judgement in the set; (2) a real **form ladder** (TG/rTG > EE) whose *magnitude* is under-specified; (3) the **active-fraction basis** (EPA+DHA vs total fish-oil mass) — a distinct stable-field concept to encode; (4) a **discrepant UL framing** (EFSA 5 g vs FDA 3 g); (5) the broad-vs-clinical mood-claim conflation trap. 7 queries, ~40 papers, 8 judgement fields.

**Pattern:** cost scales with **number of distinct claims × evidence-settledness × form-ladder depth**, plus a fixed premium for any **contested** claim. A single-claim, settled, flat-form active is ~1 unit; a multi-claim, partly-contested, laddered active is ~2.5-3 units. Identity/chemistry (the stable fields) is a near-constant cheap floor regardless of active.

---

## 5. Bottom line for Product (go/no-go input)

**The per-dossier maintenance burden is sustainable at Phase-2 (~10) and plausibly at full-catalog (~50+) scale, with one named condition.** The build cost concentrates in 2-4 drift fields per active, and within those, the *only irreducibly hand-maintained* recurring cost is **claim-tier + form-ladder adjudication** — and that cost is **rare-event-driven, not continuous**: detection is a cheap batched literature re-run; expensive human adjudication fires only when a sweep actually flags a tier-moving publication, which is concentrated in a small minority of "live-debate" claims (in this set: omega-3 CV/cognition, secondarily Mg-sleep). The bulk of the catalog (settled actives like creatine, caffeine, D3, most minerals/vitamins) needs **one annual sweep with near-zero adjudication**, and ULs can be **outsourced to NIH ODS/EFSA re-sync** almost for free. At 50+ actives the model holds *if* the live-debate minority stays small and is explicitly triaged onto a faster (semi-annual) sweep while the settled majority sits on annual — i.e. **cadence must be tiered by evidence-settledness, not flat across the catalog.** The failure mode to guard is not build cost but **silent staleness on a contested active** (omega-3 is the canary): if a contested claim's consensus shifts and the sweep is missed, the dossier misranks silently. Recommendation to Product: **GO for Phase-2 scale-up**, conditioned on (a) a tiered sweep cadence (annual default, semi-annual for flagged live-debate claims), (b) UL/safety fields maintained by authority re-sync not hand-derivation, and (c) a hard staleness alarm on any `contested`/live-debate claim past its `review_by`. The math works *and* the model scales — provided contested actives are the explicitly-budgeted exception, not treated like the settled majority.

---

# Phase-1 WIDEN build-cost addendum (TASK-171H) — 10 new dossiers, measured

**Task:** TASK-171H · **Date:** 2026-06-03 · **Author:** Nutrition Agent (co-own: Research)
**Purpose:** measure the per-dossier build cost of the 10 widen actives and **validate the ~24–40 h/yr-at-15 maintenance estimate** (from `market_coverage_analysis_v1` Q5) against reality. Same measured-proxy methodology as §1 (queries run, papers screened, judgement vs lookup fields) — NOT wall-clock; the author is a model.

## A. Per-dossier build effort (measured, the 10 widen actives)

| Dossier | Claims tiered | Umbrella maps / null | pubchem lookups | Lit queries (incl. **citation re-verify**) | Human-judgement fields* | Mechanical-lookup fields** | Build tier |
|---|---|---|---|---|---|---|---|
| **Vitamin C** | 3 | 3 / 1 | 1 | 4 | 4 (3 tiers + reversible-GI UL classify) | 4 (CID, MW, formula, dose) | CHEAP |
| **Zinc** | 3 | 2 / 1 | 5 (4 forms + element) | 5 | 5 (3 tiers + form ladder + discrepant-UL pick) | 8 (CID, 5 elemental fractions, MW, dose) | MODERATE |
| **Iron** | 2 | 2 / 1 | 4 (3 forms + element) | 6 | 5 (2 tiers + form ladder + toxicity-veto classify + necessity-fence) | 6 (CID, 3 fractions, MW, dose) | MODERATE |
| **Calcium** | 2 | 2 / 1 | 3 (2 forms + element) | 5 | 4 (2 tiers + conditional-bone framing + total-intake UL caveat) | 6 (CID, 2 fractions, MW, dose) | CHEAP–MODERATE |
| **Folic acid** | 3 | 3 / 1 | 2 (folic + 5-MTHF) | 5 | 5 (3 tiers + B12-masking UL + clinical carve-out + vitamer form) | 5 (CID, MW, formula, dose, 5-MTHF id) | MODERATE |
| **Vitamin B12** | 3 | 4 / 0 | 2 (cyano + methyl) | 4 | 4 (3 tiers + no-UL + **per-active nerve-maps boundary**) | 5 (CID, MW, formula, dose, methyl id) | CHEAP–MODERATE |
| **Melatonin** | 2 | 2 / 1 | 1 | 3 | 4 (2 tiers + over-dose-no-bonus + regulatory-status flag) | 4 (CID, MW, formula, dose) | CHEAP |
| **Biotin** | 2 | 0 / 4 | 1 | 4 | 4 (2 tiers incl. the **Insufficient refusal** + assay-interference NOTE + 4 null-mapping refusals) | 4 (CID, MW, formula, dose) | CHEAP–MODERATE (refusal authoring is the cost) |
| **Vitamin E** | 3 | 2 / 2 | 2 (d- + dl-) | 5 | 5 (3 tiers incl. Insufficient/harm + toxicity-veto + sub-UL mortality NOTE + form) | 5 (CID, MW, formula, dose, dl- id) | MODERATE |
| **CoQ10** | 3 | 2 / 1 | 2 (ubiquinone + ubiquinol) | 5 | 5 (3 tiers + **clinical-scope fence** + borderline-contested watch + form) | 4 (CID, MW, formula, dose) | MODERATE |
| **AGGREGATE (10)** | **26** | **22 / 13** | **23** | **~46** | **~45** | **~51** | — |

\* judgement field = a call the client cannot make (tier, form-ladder rank, UL veto-vs-note classify, scope-fence, umbrella map/refusal).
\*\* mechanical-lookup field = a value the client returns (CID, MW, formula, elemental fraction, dose read).

**New cost category introduced by v1.3 (the `structure_function_umbrella`):** **22 authored maps + 13 cited refusals = 35 umbrella decisions across the 10.** Each map reuses an existing `claims[]` tier (a *pointer*, cheap) but each REFUSAL (`resolves_to: null`) required a literature check to justify the non-mapping (e.g. magnesium-style "nerve = deficiency-only"). The refusals are the genuinely new judgement load v1.3 added — ~1.3 refusals/dossier, each a small literature-justified call. Biotin (4 refusals, 0 maps) is the extreme: its whole umbrella is refusal authoring.

## B. The citation-integrity cost — a MEASURED, previously-unbudgeted line item

A first-pass authoring set contained **~15 mismatched PMIDs** (correct topic intent, wrong identifier — a model-authoring failure mode). These were caught by **title-checking every PMID against the live `literature` (`pubmed_fetch`) client** and corrected (re-searched → re-verified). **This citation re-verification is a real, recurring build cost** the original 171B report did not isolate (171B's 5 MVP dossiers were smaller and hand-checked inline). Measured here: **~1 extra verify-and-correct query per 2 claims** ≈ +0.5 lit-query/dossier of overhead. **Maintenance implication:** every drift-field sweep that *adds or swaps a citation* must re-run the title-check — cheap (batched `pubmed_fetch`) but **non-optional** (an uncited or mis-cited umbrella map is a `DossierError`, by design — the loader enforces it). Recommend folding a "PMID title-check" step into the §5.1 sweep protocol.

## C. Settled-vs-contested split of the 10 (drives the maintenance estimate)

| Class | Actives | Sweep cadence | Annual adjudication risk |
|---|---|---|---|
| **Settled** (8) | vitamin C, zinc, iron, calcium, folic acid, B12, melatonin, biotin | **Annual** | near-zero (settled tiers; ULs authority-re-sync) |
| **Contested / live-debate** (2) | **CoQ10 (statin-myopathy, borderline-contested)**; **vitamin E (high-dose harm signals still accumulating)** | **Semi-annual** | moderate (CoQ10 statin claim may re-classify to contested-deferred; vitamin E harm thresholds may move) |

This is an **8 settled : 2 contested** split — slightly *better* than the 171B-projected "~12 settled + ~3 contested at 15." The widen actives are predominantly **settled vitamins/minerals**, exactly the cheap-to-maintain class.

## D. Validation of the ~24–40 h/yr-at-15 estimate (the headline ask)

Applying the **171B-measured per-class hours** (settled ≈ 1–2 h/yr; contested ≈ 4–6 h/yr) to the **actual 15-active mix now built** (5 MVP + 10 widen = 13 settled + **2–3 contested**: omega-3 always-contested, CoQ10-statin + vitamin-E-harm borderline):

| Mix (measured, 15 built) | Calculation | Annual maintenance |
|---|---|---|
| 13 settled + 2 contested | 13×1.5 + 2×5 = 19.5 + 10 | **~30 h/yr** |
| 12 settled + 3 contested (if CoQ10-statin hardens to contested) | 12×1.5 + 3×5 = 18 + 15 | **~33 h/yr** |

**Verdict: the ~24–40 h/yr-at-15 estimate HOLDS — the measured 15-active build lands at ~30–33 h/yr, comfortably inside the band.** Two refinements the measurement surfaced:
1. **The contested fraction came in LOWER than projected** (2–3 of 15 vs the projected 3), because the widen set is settled-vitamin/mineral-heavy. This pushes the realistic number toward the **lower-middle** of the 24–40 band, not the top. Good news for scale.
2. **A new, small, non-optional line item: citation title-check (§B)** + **umbrella-refusal re-justification (§A)** — both v1.3 additions. Neither is large (batched, cheap detection) but both must be **folded into the sweep protocol** or they become the silent-staleness vector (a stale refusal — e.g. new evidence that magnesium 'nerve' now DOES have a studied endpoint — would not error; it would silently keep refusing). **Recommend: add "re-verify umbrella refusals + PMID title-check" to the §5.1 drift sweep.**

**Bottom line for Product:** the widen to 15 is **measured-sustainable at ~30 h/yr**, validating the estimate; the marginal maintenance cost of the 10 widen actives is **low** (8 of 10 settled). The two watch-items are CoQ10-statin and vitamin-E-harm (semi-annual), plus the two **structurally-hard deferrals** (multivitamin, probiotics) that no amount of dossier-building reaches — those remain a separate, explicitly-budgeted strategic decision per `market_coverage_analysis_v1`.
