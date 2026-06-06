---
document: glass_box_technical_methodology_v1
task: TASK-181R
program: TASK-181 (Glass Box program-of-record) — Wave 5
status: CLEARED FOR DISTRIBUTION — citation corrections applied 2026-06-05 (Research Agent verification); EV-035–039 Product D7 co-signed 2026-06-05
audience: NDA partners, academic reviewers, institutional counterparts, nutrition researchers
distribution: NDA / on-request (not public website)
created_at: 2026-06-05
author: Nutrition Agent
---

# Bari Glass Box — Technical Methodology Packet (v1)

**Date:** 2026-06-05
**Author:** Nutrition Agent
**Task:** TASK-181R (Glass Box Wave 5 — NDA/partner technical documentation)
**Audience:** Nutritionists, dietitians, food-science researchers, academic reviewers

This document is the technical complement to the consumer-facing Glass Box methodology page. The consumer page is intentionally concise. This packet is the full evidence framework underneath it — the citable, internally defensible specification that a professional reviewer or institutional counterpart requires. The two documents describe the same engine, at different levels of resolution.

---

## 1. Overview

### 1.1 What Glass Box is

Glass Box is an evolution of Bari's BSIP2 food scoring engine into six explicitly separable, auditable dimensions. The strategic frame: the engine must be **decisive on the outside** (one grade a shopper can act on in seconds) and **fully inspectable underneath** (six dimensions a professional can audit). Same engine, two faces.

The name describes the epistemic posture: every inference the engine makes about a food product is visible, traceable, and attached to a stated confidence. Where the evidence is thin, the system does not fabricate certainty — it surfaces the gap and adjusts the confidence gate accordingly. "Glass box" is the opposition to black-box scoring, which hides how a grade is produced and therefore cannot be independently verified or challenged.

### 1.2 How Glass Box fits BSIP2

BSIP2 (Bari Structured Ingredient and Panel scoring system, version 2) is the existing engine used to score all live Bari categories. It currently operates over ten internal scoring dimensions, applying nutritional, processing, and additive signals drawn from the product's BSIP0 data layer (the raw scraped panel: ingredient list, nutrition panel, product metadata).

Glass Box does not replace BSIP2. It **relabels and extends** it. The ten internal dimensions are grouped and renamed into six public-facing dimensions (D1–D6), and three new capabilities are added: a transparent disclosure-gap detector (D5), an evidence-aware additive annotation layer (D4), and a formal confidence gate (D6). All changes are implemented behind environment flags with default OFF, meaning the live engine is byte-identical until the flags are activated by a co-signed decision.

### 1.3 The six-dimension architecture

| Dimension | Consumer name | Role in the grade |
|---|---|---|
| D1 | Nutritional quality | Primary driver — nutritional standing of the disclosed panel |
| D2 | Ingredient evidence | Modulator — quality and evidence status of named whole-food ingredients |
| D3 | Processing signal | Bounded modulator — population-level probabilistic formulation correlate |
| D4 | Additive annotation | Annotate-only — evidence-tiered additive panel (does NOT enter the grade) |
| D5 | Transparency | Disclosure profile — feeds D6, never moves the grade on its own axis |
| D6 | Confidence gate | Gate — can demote or withhold the grade; cannot promote |

**Composition rule:** D1 through D5 contribute to one composite 0–100 score. D6 then gates that composite: unconstrained (passes through), demote (applies a ceiling), or withhold (outputs null/"לא נוקד"). The shopper never sees six numbers — they see one decisive grade and, where D6 demotes or withholds, a confidence flag.

### 1.4 Annotate-only versus grade-moving

The annotate-only boundary is a hard architectural invariant.

D4 (additive annotation) does NOT enter the headline grade. The additive panel is a transparency and information layer, not a scoring signal. Whether D4 evidence tiers should eventually move grades is a separate future owner-gated decision, classified as a frozen-invariant tripwire (see Section 6). This is not a shortcoming of the current design — it is the current design, adopted deliberately. The annotate-only boundary prevents Bari from issuing quality verdicts on additives in advance of the demand data that would justify the maintenance cost of keeping those verdicts current.

D5 (transparency) also does not move the grade on its own axis. A disclosure gap — an ingredient class named generically, a compound ingredient without a breakdown, a missing red-label field — is a finding about the product's label, not a finding about the product's quality. D5 routes the disclosure gap to D6 (confidence), where it may cause a demotion, and annotates the professional surface with the specific finding. It does not deduct grade points. This preserves the principle that the grade reflects the disclosed data; opacity costs standing via confidence, not via a quality penalty.

### 1.5 "Who-pays is not who's-scored"

Bari is an independent scoring service. The scoring engine reads in-house BSIP0 data only. No manufacturer data submission, sponsorship, or commercial relationship can influence a product's score. Evidence sources used for calibration and rule governance (EFSA, JECFA, FDA, IARC/WHO, peer-reviewed cohort literature) are publicly accessible and cited per entry in the evidence registry. Score changes require a co-signed evidence-registry entry (EV-### + both Nutrition Agent and Product Agent D7 co-sign). No rule is deployed in a disputed state.

---

## 2. D3 — De-Moralized Processing Signal

### 2.1 The problem D3 corrects

The pre-Glass-Box engine mapped NOVA class directly to a fixed dimension score: NOVA 4 = 35, NOVA 3 = 65, NOVA 2 = 85, NOVA 1 = 95, unconditionally (`NOVA_PROCESSING_SCORES`, `constants.py`). A separate set of guardrail caps applied a hard overall-score ceiling of 68 to every NOVA 4 product regardless of its nutritional profile. HP (hyper-palatability) penalties were scaled by NOVA class rather than fired on direct observational criteria.

This approach makes three overstatements (documented in `d3_demoralization_spec_v1.md §1.3`):

- **O1 — Class-to-score determinism.** The mapping treats a population-level probabilistic correlate as if it were a per-product quality measurement. There is no such measurement.
- **O2 — Hard ceiling regardless of nutritional profile.** A clean-formula high-protein NOVA 4 product is capped at 68 on the basis of class assignment alone, not on any nutritional observation.
- **O3 — NOVA class as HP amplifier.** Scaling HP penalties by NOVA class compounds the NOVA assumption on top of direct HP observations. If the HP signals fire, they fire; their magnitude must not further depend on a population-level class assignment.

### 2.2 The evidence base and its correct interpretation

NOVA is an epidemiological food classification system. The evidence claim, stated precisely, is:

> **Populations whose diets contain a higher proportion of NOVA class 4 foods show, at the population level, associations with worse health outcomes including obesity, type 2 diabetes, cardiovascular disease, and all-cause mortality.**
> (Srour et al. 2019 [BMJ, NutriNet-Santé cohort]; Monteiro et al. 2019 [NOVA classification criteria, *Public Health Nutrition*])

Evidence strength: **Moderate**. The population-level dietary-pattern association is robust across multiple cohort geographies. The extrapolation to per-product quality verdicts is not supported by the evidence and constitutes the governance problem.

Specifically, the evidence does **not** claim that any single NOVA 4 product causes harm, that NOVA class reliably predicts the nutritional quality of an individual product, or that NOVA class is assignable with high confidence from an Israeli retail label (where generic additive terms, unnamed stabilizers, and missing proportions are structural norms).

### 2.3 The material / non-material uncertainty split (EV-042, revised 2026-06-04)

The Glass Box D3 reframe introduces a confidence-first rule. The core shift: D3 no longer claims "this product has processing quality 35." It claims "this product's formulation pattern is associated at population scale with [direction], with stated confidence."

**Confidence bands** reflect the engine's confidence in the NOVA assignment for the specific product, derived from ingredient-evidence quality — not from the NOVA class itself (the de-circularizing move):

- **High confidence** — all three: ingredient list present and not corrupted; NOVA class unambiguous from ingredient signals (named E-codes or specific additive names, not bare generic terms; processing pattern clear); no D5 severe disclosure band.
- **Medium confidence** — ingredient list present; some additives named; class plausible but not fully verifiable from the panel alone (typical for multi-ingredient NOVA 2–3 with partial disclosure).
- **Low confidence** — any of: no ingredient list; D5 disclosure band partial or severe with closable gaps that could materially affect NOVA assignment; class inferred primarily from product name/category heuristics with no corroborating ingredient evidence.

**The material / non-material split (TASK-181J revision to EV-042):** Not all medium-confidence products are equivalent. The revised rule splits the medium band by whether the unresolved/unknown element could change the processing verdict:

**Material uncertainty** — unknown could plausibly flip the NOVA class. Observable criteria (any one fires):
- M1: The NOVA-deciding additive is a bare-generic term (D5 G4 detector: unnamed "מייצב"/stabiliser, "מתחלב"/emulsifier) whose function class is itself the processed-vs-ultra-processed pivot.
- M2: D5 band = severe (a severely opaque panel cannot pin the NOVA read).
- M3: The unresolved fraction of the ingredient list exceeds 30%, or an unnamed compound ingredient ("תערובת") could carry NOVA-4 markers.
- M4: Worst-case NOVA-flip test — if the unresolved term is assumed to be a NOVA-4 marker, would the class assignment change? If yes, the gap is material by definition.

**Non-material uncertainty** — visible signals already pin the NOVA read; the unresolved term is peripheral (e.g. "תבלינים"/spices or a single named stabilizer on an otherwise legible whole-food list). The worst-case identity of the unknown term would NOT change the NOVA class given the rest of the list.

### 2.4 Score-modification formula

The D3 dimension score uses a pull-toward-neutral formula keyed to confidence and materiality. Base anchor values (`NOVA_PROCESSING_SCORES`) are retained as calibration constants:

```
base_score(nova_class) = NOVA_PROCESSING_SCORES[nova_class]  → 95 / 85 / 65 / 35

neutral = 50.0

confidence_scale:
  high                   → 1.0  (current-magnitude modifier; high certainty)
  medium + MATERIAL      → 0.70 (moderate pull toward neutral; uncertainty is real and could move the verdict)
  medium + NON-MATERIAL  → 1.00 (NO D3 score move; doubt routes to D6 confidence only)
  low                    → 0.40 (substantial pull toward neutral; low-confidence NOVA assignment contributes little)

modifier_score = 50.0 + (base_score − 50.0) × confidence_scale
```

Worked examples:
- NOVA 4, high confidence: `50 + (35−50) × 1.0 = 35.0` (identical to today)
- NOVA 4, medium-material: `50 + (35−50) × 0.70 = 39.5`
- NOVA 4, medium-non-material: `50 + (35−50) × 1.0 = 35.0` (D3 does not move — doubt goes to D6 −5)
- NOVA 4, low confidence: `50 + (35−50) × 0.40 = 44.0`
- NOVA 1, high confidence: `50 + (95−50) × 1.0 = 95.0` (identical to today)
- NOVA 1, medium-non-material: `50 + (95−50) × 1.0 = 95.0` (no move)
- NOVA 1, low confidence: `50 + (95−50) × 0.40 = 68.0`

**Guardrail cap scaling:** Processing caps (`NOVA_PROXY_4_ULTRA_PROCESSED` base 68; `NOVA_PROXY_3_PROCESSED` base 87) are relaxed proportionally using the same `confidence_scale`:

```
cap_effective = 100 − (100 − base_cap) × confidence_scale
```

For medium-non-material: `confidence_scale = 1.0` → cap unchanged (the non-material = no-move principle holds for caps as well as scores). For medium-material (0.70): NOVA-4 cap becomes `100 − 32 × 0.70 = 77.6`.

**Population-correlation reference values** (calibration anchors in the trace, not score inputs):

| NOVA class | `population_correlation` | Rationale |
|---|---|---|
| 1 | 0.05 | Near-zero; NOVA 1 is the reference group in the epidemiology |
| 2 | 0.15 | Small positive signal; culinary-processed staples |
| 3 | 0.40 | Moderate; heterogeneous group — central estimate |
| 4 | 0.75 | Strong tail driving the NOVA epidemiology; still a population correlate |

### 2.5 HP de-amplification

Hyper-palatability (HP) penalties in the existing engine were scaled by NOVA class (`NOVA_HP_WEIGHTS = {1:0.0, 2:0.0, 3:0.5, 4:1.0}`). Under Glass Box, this NOVA-class amplification is removed. HP detection signals (`HP_FAT_SUGAR_COMBO`, `HP_FAT_SODIUM_COMBO`, `HP_CRUNCH_SWEET_COMBO`) fire on their direct observational criteria at full weight, regardless of NOVA class.

**Rationale:** Applying a NOVA-class discount to an observed fat+sugar or fat+salt combination is invented certainty through the back door. If the macro combination is present in the disclosed panel, the HP signal should fire at full weight — the NOVA class is not additional information about the combination, it is a population-level class that does not change what is in the product. A NOVA discount on an observed HP pattern constitutes a health-halo effect: it gives a product a quality premium for belonging to a class, not for having a cleaner composition. The net effect on the real shelf is a 17-product downward grade shift and 3-product upward shift — directionally net-downward — which is the correct representation of the HP signal applied without NOVA amplification.

### 2.6 D6 routing for non-material and low-confidence products

When the gap is non-material (D3 score does not move), the engine emits a `d3_nonmaterial_gap` signal to D6 carrying a **−5 confidence deduction**. Magnitude justification: this is exactly half the D5 `partial`-band confidence reduction (−10), which is the governing anchor. A non-material gap is a smaller dent in certainty than a closable structural disclosure gap, by construction — it cannot change the processing verdict, so it must dent certainty strictly less than the closable-opacity term, while remaining non-zero.

When the confidence band is low (no panel, or class inferred from heuristics), D3 routes a **−10 confidence deduction** to D6 — equal to the D5 `partial` term, which reflects that a low-confidence NOVA read is at least as corrosive to certainty as a closable structural gap.

Both D3→D6 terms are max-combined with any D5 confidence term, never summed. No double-counting of the same unresolved token across D3 and D5.

### 2.7 Known limitations

**F1 — D5/D6-offline materiality degeneracy.** When `BARI_GLASSBOX_D5D6` is OFF, the M2 and M3 criteria (D5 band severity) cannot be evaluated. The two-signal fallback (ingredient list present/absent + NOVA classifier confidence band) is less precise. This is a logged architectural dependency, not fixed in W4.

**HP×WFI interaction watch-item.** The interaction between HP de-amplification and the whole-food-integrity (WFI) signal is an open watch-item. Under WFI, high-NOVA products receive a reduced WFI score. Under the HP reframe, the HP penalty fires at full weight on direct criteria. If a high-NOVA product also has a WFI penalty, the cumulative effect should be monitored to confirm no over-penalization of the same root signal.

**NOVA assignment on Israeli labels.** A non-trivial share of the real shelf (~40% of the bread corpus in `run_bread_retail_003`) involves low-confidence NOVA assignments due to partial ingredient disclosure. D3's confidence-scaling correctly reports this uncertainty rather than suppressing it, but it means that many products' D3 signals are confidence-reduced rather than decisive — an honest representation of what the label supports.

---

## 3. D4 — Evidence-Aware Additive Annotation

### 3.1 The annotate-only constraint

D4 does NOT enter the headline grade. This is the operative design as of Wave 3 (W3). It is a current design decision, not a shortcoming. Score-integration for D4 remains a separate future owner-gated decision classified under frozen-invariant tripwire #1 (see Section 6). Any future D4 score integration would require a new evidence-registry entry, both Nutrition Agent and Product Agent D7 co-sign, and separate go-live authorization.

What D4 does: it emits, per product, a per-additive tier assignment that populates the additive annotation panel on the professional surface and, on opt-in, the consumer drilldown. The tiers drive display copy only.

### 3.2 The six-tier evidence model (EV-041 / EV-043)

Tiers are assigned to additives based on the authoritative regulatory/scientific evidence at the time of the review. The tier model is frozen in EV-041 and must not be redefined without a new co-signed evidence-registry entry.

| Tier | Meaning | Governance anchor |
|---|---|---|
| `functional` | Well-characterised function; broad regulatory acceptance; no safety concern at typical food doses. EFSA "ADI not specified" or "no ADI necessary" / JECFA "not limited" / FDA GRAS. | EV-041, EV-043 |
| `likely-neutral` | Extensive history of use; no significant safety signal at typical doses; a minor unconfirmed signal may exist (e.g. one unconfirmed observational association). | EV-041, EV-043 |
| `dose-dependent` | Safe at typical food doses; a documented dose-response pathway exists at high or cumulative exposure (established ADI with a non-trivial exposure-to-ADI margin, or an EFSA over-exposure flag for a specific consumer subgroup). | EV-041, EV-043 |
| `contested` | Mixed or emerging evidence; a credible mechanistic or clinical signal (e.g. peer-reviewed pre-registered human RCT or IARC reclassification) without regulatory consensus. | EV-041, EV-043 |
| `disclosure-gap` | The label does not transmit the information needed to assign a tier (e.g. E150 caramel colour without the class, which determines whether 4-MEI is implicated). | EV-041, EV-043 |
| `confirmed-negative` | Credible weight-of-evidence harm at relevant exposure. **No additive on the current displayed Israeli shelf meets this bar** (industrial trans fat, which would qualify, is a separately handled veto trigger). | EV-041, EV-043 |
| `unclassified` | True fallback: the available evidence anchor does not permit a clean tier verdict (used once: E141 copper chlorophylls — group EFSA evaluation with copper-release caveat, no clean single numeric ADI). | EV-041, EV-043 |

The taxonomy is asymmetric by design. On the real displayed Israeli shelf, the observed distribution across 36 shelf-present additives is: functional 19 · likely-neutral 7 · dose-dependent 5 · contested 3 · disclosure-gap 1 · confirmed-negative 0 · unclassified 1. The dominant population of shelf additives is functional or likely-neutral technological aids. Only a small subset (the three contested additives: carrageenan E407, CMC E466, BHA E320) carry an active scientific discussion. No additive on the shelf is confirmed-negative. The taxonomy must reflect this shelf reality — not an alarmist presumption in either direction.

### 3.3 Evidence sources and the bulk-import model

The tiered library is assembled through a **bulk-curate, not live-per-product** model. For each of the 36 shelf-present additives:

1. **EFSA OpenFoodTox / EFSA re-evaluation programme** — the primary European hazard-characterisation source. For additives evaluated on the rolling pre-2009 re-evaluation programme, the opinion PDF is read directly. For additives with a group evaluation (e.g. modified starches, citrate salts), the group opinion is applied.
2. **JECFA (WHO/FAO Joint Expert Committee on Food Additives)** — international standard; where EFSA has not yet issued a discrete numeric ADI, JECFA "not limited" is the fallback anchor for `functional` tier assignments.
3. **FDA GRAS and 21 CFR regulations** — used as a corroborating anchor, particularly for additives (e.g. calcium citrate E333, calcium sulphate E516) where EFSA has a group evaluation without a single numeric figure.
4. **IARC Monographs** — for additives with carcinogenicity classifications (BHA E320 = Group 2B, caramel colour E150 Class III/IV 4-MEI context).
5. **Peer-reviewed primary literature** — for contested additives where a pre-registered human study or a mechanistic finding creates a credible regulatory-science gap (carrageenan E407: Bhattacharyya et al. NF-κB / gut-barrier work; CMC E466: Chassaing 2021, pre-registered randomized controlled-feeding study, exploratory design, n=16, *Gastroenterology*).

**The EFSA numeric-ADI wiring gap (EVIDENCE-GAP, logged TASK-181A):** EFSA numeric ADI values and JECFA ADI values have no free per-substance REST API. The library was assembled using per-substance opinion PDF web-scraping and cross-referencing. A one-time EFSA OpenFoodTox bulk import (a downloadable substance-level hazard/reference-point dataset) would close this gap for future re-verifications. This import is deferred until either (a) the demand-revisit checkpoint confirms consumer engagement with the additive panel, or (b) score integration is opened by the owner. Until then, the web-scrape + carried-forward protocol remains in use.

**Israel-vs-EFSA divergence:** No free authoritative source covers the divergence between Israeli MoH additive approvals and EFSA approvals. This is documented as a standing D5 disclosure-note candidate (a label-vs-jurisdiction fact) but is not a D4 tier driver. D4 tiers reflect evidence of harm/safety, not jurisdictional approval status.

### 3.4 Shelf-present scope

The library governs **shelf-present additives only** — additives actually observed on the displayed Israeli Shufersal shelf corpora (hummus + maadanim pilot corpora, supplemented by cross-category inference). New additives enter the library only when observed on a displayed shelf (the 181A-style corpus pass surfaces them), never speculatively. The current library covers 36 additives. The full E-number space has thousands of registered additives; that space is not the maintenance target.

### 3.5 Maintenance cadence and the go/no-go gate

The library is maintained under the protocol in `additive_library_maintenance_protocol_v1.md` (EV-043):

- **Annual full re-verify** (Nutrition executes, Product co-signs any delta): every additive's tier is re-confirmed against the current EFSA/JECFA/FDA position.
- **Quarterly light scan**: EFSA "Latest" re-evaluation feed + JECFA meeting reports + IARC monograph announcements, filtered to the 36 shelf-present additives. Hits are triaged by Nutrition.
- **Six trigger events** force an off-cycle review regardless of the calendar: a new EFSA re-evaluation opinion; a JECFA ADI change; an IARC reclassification; an FDA GRAS withdrawal or ban; a high-quality new primary study (pre-registered RCT or mechanism that materially changes a contested/likely-neutral call); a new additive appearing on the displayed shelf.

**The Product go/no-go gate** runs at every annual re-verify. The library is maintained (KEEP/SCALE) only if all three conditions hold: (1) correctness is sustainable (re-verify completed on cadence, stale count = 0); (2) the maintenance surface is still bounded to shelf-present additives; (3) demand is not disproven by engagement instrumentation. If any condition fails, the outcome is FREEZE — the library stops expanding, and a keep-or-retire decision routes to the owner. FREEZE is an expected governance outcome, not a failure mode.

**Staleness detection:** every additive entry carries a `last_verified` date. The staleness threshold is 15 months. Stale count is surfaced on the Command Center dashboard automatically (derived from the registry, never hand-edited). A stale-but-live library is itself a go/no-go input.

---

## 4. D5 — Label Transparency

### 4.1 What D5 assesses

D5 runs a deterministic detector over the raw BSIP0 ingredient panel (`ingredients_raw` string + disclosed nutrition block) for each product. It emits a structured **disclosure profile** — a list of which gap types fired — and a **disclosure-completeness band** (D5-band: full / minor / partial / severe).

Five disclosure gap types are detected:

- **G1 — Undisclosed proportions.** Multi-ingredient products where no `%` appears, or the lead ingredient's share is undisclosed. Single-ingredient products are explicitly protected: a panel with exactly one ingredient is classified as maximally transparent, G1 does not fire, and the product receives the `full` band regardless. This is critical — the engine must not flag a clean walnut or cooked-chickpea panel as incomplete.
- **G2 — Compound ingredient without internal breakdown.** A named compound food (e.g. chocolate coating, cream, syrup) that is not followed by a sub-ingredient itemization.
- **G3 — "Protein blend" / unspecified protein source.** Generic protein declarations (`תערובת חלבונים`, `חלבון צמחי`) without single specific source identification. Collagen/gelatin declarations are a special case: disclosed but low-quality protein source — routed to D2 as an ingredient-evidence signal, not treated as a D5 gap.
- **G4 — Generic additive class without E-code or name.** Bare class terms (`מייצב`, `מתחלב`, `צבע מאכל`, `חומרי שימור`, etc.) not followed immediately by a parenthetical specifying the E-code or name. Bare `חומרי טעם וריח` (flavorings) is classified as endemic — present in approximately 70% of panels in the maadanim corpus — and is therefore **excluded from band-raising**. Applying a band penalty for bare flavorings would push nearly the entire shelf into `partial`/`severe` and demote it via D6, a category-blind distortion comparable to the documented fiber-penalty distortion in the dairy category.
- **G5 — Missing nutrition fields.** Fields expected by the category that are absent from the disclosed panel (energy, protein, carbohydrates, fat, fiber, sodium, saturated fat, sugar where red-label regime applies). G5 names the specific missing fields in the disclosure profile; it does not re-apply the confidence deduction already applied by the existing `compute_confidence` machinery (no double-counting).

### 4.2 Severity split: structural vs closable

The gap taxonomy separates two severities that carry different governance weight:

**Structural gaps** — the format cannot close them. Ingredient proportions are not required by Israeli or EU labeling law (QUID disclosure applies only to emphasized or named ingredients). Missing panel fields often reflect label-format limits rather than manufacturer decisions. These are the market floor: they must not erode confidence, or the engine would systematically demote the entire shelf for a systemic regulatory gap.

**Closable gaps** — the manufacturer could have disclosed but did not. Bare generic additive terms (when a named E-code was available), compound ingredients without sub-itemization, omitted red-label-relevant fields (saturated fat, sugar on an otherwise complete panel). Closable gaps do erode confidence, because they represent a real information asymmetry that the manufacturer had the means to close.

### 4.3 The D5-band and its role

| D5-band | Condition |
|---|---|
| full | Single-ingredient product, or zero findings after endemic-flavoring and structural exclusions |
| minor | Only structural gaps fire — no closable gaps |
| partial | At least one closable gap fires |
| severe | Panel absent, or closable gaps across three or more distinct gap classes, or a generic protein blend co-occurring with two or more closable gaps |

The D5-band feeds D6 as a single named confidence reduction (see Section 5). It does not deduct grade points. A `severe` band does not lower the grade; it lowers confidence, which may lower the ceiling applied to the grade.

### 4.4 What D5 does NOT evaluate

D5 does not assess the following, and the consumer surface must not imply it does:

- **Intent.** D5 finds what is not disclosed. It does not claim the manufacturer deliberately omitted information. Consumer language uses "לא צוין" (not stated) and "לא ניתן לאמת מהנתונים הזמינים" (cannot be verified from available data); never "היצרן מסתיר" (the manufacturer is hiding).
- **Product quality on its own axis.** A product with a `partial` band is not a lower-quality product — it is a product whose quality is harder to assess. The distinction is preserved by routing disclosure gaps only through D6 (confidence), not through the quality composite.
- **Cross-market disclosure.** Whether a product's Israeli label omits information that the same product's US or EU label would include is a Wave 3 backlog candidate (Cross-Market Disclosure concept), not part of D5's current scope.

---

## 5. D6 — Confidence Gate

### 5.1 What D6 is and is not

D6 is the confidence axis of the engine. It is not a food-quality measure. High D6 confidence means the engine trusts its inputs — the panel is present, coherent, and reasonably complete. Low D6 confidence means the engine is working from thin or opaque data. D6 gates the composite grade accordingly.

### 5.2 Confidence score construction

The D6 confidence score starts at 100 and is reduced by the existing `compute_confidence` deductions plus the new D5-derived and D3-derived terms introduced under Glass Box:

**Existing deductions (unchanged):**
- Missing energy / protein / carbohydrates / fat: −10 each
- Missing fiber / sodium: −5 each
- Missing ingredient list entirely: −25
- Suspicious data patterns (e.g. sugar > total carbohydrates): −20
- Low NOVA confidence: up to −10 (scaled)
- Low category confidence: up to −15 (scaled)

**New Glass Box deductions (flag-gated):**

| Source | Condition | Reduction | Reasoning |
|---|---|---|---|
| D5 | band = partial (closable gaps) | −10 | Closable opacity erodes trust that the engine sees the real formulation |
| D5 | band = severe | −20 | Severe closable opacity — near-floor trust |
| D5 | band = minor or full | 0 | Structural gaps are the market floor; they must not bleed confidence |
| D3 | medium-confidence, non-material gap | −5 | Half the D5 partial deduction; a peripheral unknown that cannot move the verdict dents certainty less than a closable structural gap |
| D3 | low-confidence NOVA read | −10 | Equal to D5 partial; a low-confidence NOVA is at least as corrosive to certainty as a closable gap |

No double-counting rule: if the same unresolved ingredient token triggers both a D3 non-material deduction and a D5 partial deduction, D6 takes the **maximum** of the two, not the sum.

### 5.3 The three-state gate

After computing the D6 confidence score, the engine derives a gate state:

**Unconstrained** (d6 ≥ 60, High/Medium band): the D1–D5 composite passes through. Grade reflects the full composite.

**Demote** (d6 in the 30–59 range, or below 60 with a non-severe D5 band): a ceiling applies using the existing constants (`CONFIDENCE_LOW_CEILING = 75` for the 40–59 Low band; `CONFIDENCE_INSUFFICIENT_CEILING = 50` for the <40 Insufficient band). A visible `ניתוח חלקי` flag is surfaced to the consumer. This is the normal partial-disclosure / thin-data case: coverage over silence.

**Withhold → null** (floor-of-observability failure only): output `score: null`, grade label `לא נוקד`. This fires only when the panel is absent (no usable ingredient list) OR when d6 < 30 AND the D5 band is severe — both numerically thin AND structurally opaque simultaneously. This is the "reluctant-to-withhold" posture: below a genuine floor of observability, the engine declines to rank rather than displaying a capped middle number. A plain `<40 → null` rule would withhold a large chunk of the shelf on thin-data grounds alone, which violates the "buy coverage over silence" principle. The conjunction of `<30` and `severe` catches only genuine floor failures.

### 5.4 The F3 gate-guard (TASK-181M — hard architectural invariant)

A specific constraint was added in TASK-181M as a consequence of validation against real maadanim panels:

**The −5 non-material D3 confidence dent cannot independently trigger `insufficient_data` (the withhold state).** If the only reason a product would cross the `insufficient_data` boundary is the `d3_nonmaterial_gap` −5 term, the product does NOT enter `insufficient_data`. The −5 dent reduces displayed confidence within the graded band only.

This is a hard architectural invariant, not a calibration detail. The co-signed promise for non-material uncertainty was "confidence dent, never a grade cut." Without the F3 guard, three maadanim products crossed the insufficient_data boundary solely because of a peripheral unresolved ingredient term — a violation of the principle that a peripheral unknown routes to confidence, not to grade removal. The guard is precise: it rescues exactly those products where the non-material dent is the decisive term, without over-clamping products that are genuinely data-poor.

**Validation (TASK-181M):** 3 maadanim products that flipped under 181K (pre-guard) are restored to graded D with identical scores (42.0/41.8/46.2). Genuinely data-poor products (25 no-gap + 12 genuinely-low-confidence products) continue to reach `insufficient_data` correctly — the guard is not over-clamping.

### 5.5 Relationship between D3 routing and D6

D3 and D6 interact through two distinct signal paths, both flag-gated:

1. **Non-material medium uncertainty:** D3 score = unchanged (scale 1.0); D3 emits `d3_nonmaterial_gap` → D6 −5.
2. **Low-confidence NOVA read:** D3 score pulled toward neutral (scale 0.40); D3 emits `low_confidence_nova` → D6 −10.

Neither path is a quality signal — both act through confidence only. The F3 gate-guard applies to path 1 only (the −5 term). Path 2 (−10) has a higher magnitude and is more likely to combine with other existing confidence deductions to reach the demote threshold legitimately.

---

## 6. Frozen Invariants and What Does Not Change

The following are hard constraints on the Glass Box system. They are not revisited without explicit owner authorization (frozen-invariant tripwires 1 and 2 from the decision authority matrix).

### 6.1 Milk = run_005_headpin (engine tag engine-baseline-2026-06-04)

The milk category scores are frozen as of the `run_005_headpin` run (2026-06-04, TASK-180A). The top score is 85/A (whole 3.4% / natural 4% / goat dairy). This supersedes `run_004_recalibrated`. No Glass Box rule, including D3 or D6, moves any milk score.

The D3 reframe is structurally safe for milk: milk products are predominantly NOVA 1–2 with high-confidence NOVA assignments. High-confidence NOVA assignments use scale 1.0 — identical to the current engine. No milk score moves.

### 6.2 Snack bar ceiling = 70/B (snk-001)

No snack bar reaches grade A. This is a calibrated ceiling grounded in the category's structural sugar/calorie load, not a cap applied by D4 or D6. D6 can only demote or withhold, never promote. D3 confidence scaling for non-high-confidence medium-band products moves D3 toward neutral (bounded), which could raise the D3 sub-score contribution, but this is bounded and cannot breach the snack-bar ceiling logic independently of the nutritional guardrails (sugar, calorie caps) that enforce it.

### 6.3 Bread provenance = real_bread_retail_003_v1

Bread category scores derive from the `real_bread_retail_003_v1` corpus (Shufersal, 25–26 May 2026; 256 scanned, 81 scored, 31 curated). The "best ≠ excellent" framing applies: the best bread on the real Israeli retail shelf does not reach a standard that warrants an A grade under honest scoring. The D3 reframe for bread is directionally correct — many bread NOVA assignments are low-confidence on the real shelf (partial ingredient disclosure), and the confidence-scaling correctly reflects this uncertainty.

### 6.4 W4 is behind a flag with OFF = byte-identical

The Glass Box Wave 4 D3 reframe ships behind `BARI_GLASSBOX_W4` (default OFF). With the flag OFF, the engine is byte-identical to the pre-W4 baseline: `score_processing_quality` runs the current `NOVA_PROCESSING_SCORES` lookup verbatim, `NOVA_HP_WEIGHTS` scaling is unchanged, and no `d3_processing_signal` struct is emitted. Rollback = unset the flag. No code revert is required.

The same flag discipline applies to D5/D6 (`BARI_GLASSBOX_D5D6`, default OFF) and D4 (`BARI_GLASSBOX_W2`, default OFF). All golden/frozen runs must verify 0-diff with their respective flags OFF before any go-live.

### 6.5 D4 score-integration is owner-gated

Whether D4 evidence tiers should ever move the headline grade is explicitly not within the scope of any current rule. This decision is classified as a frozen-invariant tripwire #1 (touches scoring philosophy and published scores). It requires owner authorization, a new evidence-registry entry, Nutrition and Product D7 co-sign, and separate go-live authorization. The current annotate-only design does not pre-commit to this decision in either direction.

---

## 7. Evidence Registry Index

The following EV-registry entries are the governing authority for the rules described in this packet. All entries are in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (the BSIP2 packaged-food engine registry).

| EV-ID | Dimension | One-line description | Status |
|---|---|---|---|
| EV-035 | D5 | D5 disclosure-gap taxonomy (five types: G1–G5) over the raw BSIP0 panel; structural vs closable severity split | Active — co-signed Product D7 2026-06-05 |
| EV-036 | D5 | Endemic-flavoring exclusion: bare `חומרי טעם וריח` excluded from D5 band-raising and D6 to avoid category-blind distortion | Active — co-signed Product D7 2026-06-05 |
| EV-037 | D5/D6 | D5-band → D6 confidence reduction: full/minor 0 · partial −10 · severe −20 | Active — co-signed Product D7 2026-06-05 |
| EV-038 | D6 | D6 gate state machine + null-vs-cap floor (`NULL_FLOOR=30`, `DEMOTE_CEILING_BOUND=60`) | Active — co-signed Product D7 2026-06-05 |
| EV-039 | D5/D6 | `BARI_GLASSBOX_D5D6` flag + OFF = byte-identical guarantee | Active — co-signed Product D7 2026-06-05 |
| EV-041 | D4 | Six-tier additive evidence taxonomy (the tier model; W2 prototype 20-additive set; detector spec) | Both D7 co-signs complete |
| EV-042 | D3 | D3 de-moralization: confidence-scaled probabilistic processing signal; material/non-material medium-band split (revised TASK-181J); F3 gate-guard (TASK-181M) | Both D7 co-signs complete (revised); deployed behind BARI_GLASSBOX_W4 |
| EV-043 | D4 | D4 expanded additive library tier assignments (36 additives; annotate-only; W3) | Both D7 co-signs complete |

**Governance entries cited but not reproduced here:**
- BEV-001 — Bari analytical boundary ("ברי מתאר. לא ממליצה")
- BEV-003 — What Bari is not (anti-processing ideology, NOVA scorer, health certification body)
- BEV-018 — Confidence ceiling mechanism (the D6 demote state's substrate)
- BEV-019 — Confidence score construction — existing deduction amounts
- BEV-021 — NOVA classification system — accepted as primary processing signal
- BEV-029 — Hyper-palatability: four accepted patterns (HP signals fired by D3's direct-observation rule)
- BEV-052 — Hard cap inventory (the caps that D3 confidence-scaling now relaxes proportionally)

---

## Appendix A — Note on Evidence Gaps

The following evidence gaps are known and logged. They are disclosed here so reviewers understand where the current methodology reaches its limits.

**EVIDENCE-GAP 1 (EFSA numeric-ADI wiring, logged TASK-181A):** The D4 library was assembled using per-substance PDF web-scraping rather than a programmatic bulk import of the EFSA OpenFoodTox dataset. The tier assignments are accurate for the 36 current shelf-present additives, but the re-verification process requires manual effort. An EFSA OpenFoodTox bulk-import implementation is deferred until demand data justifies the maintenance infrastructure. This does not affect the correctness of the current tiers.

**EVIDENCE-GAP 2 (Israel-vs-EFSA divergence):** There is no free authoritative API for Israeli MoH additive approval status vs. EFSA status. Jurisdictional divergences (e.g. E141 copper chlorophylls: permitted in EU, not in FDA general use) are documented as D5 disclosure-note candidates but do not drive D4 tier assignments.

**EVIDENCE-GAP 3 (NOVA assignment confidence on Israeli labels):** A structural fraction of the Israeli retail shelf — observed at approximately 40% in the bread corpus — presents panels with sufficient disclosure ambiguity that NOVA class cannot be assigned with high confidence. D3's confidence-scaling correctly reflects this; it does not resolve it. Resolving it would require richer ingredient disclosure, which is a structural label-format limit, not an engine gap.

**EVIDENCE-GAP 4 (HP × WFI interaction at scale):** The interaction between the HP de-amplification change (HP signals fire without NOVA weighting) and the whole-food-integrity (WFI) scoring dimension under full-scale corpus conditions is a logged watch-item. The pilot data does not show an over-penalization issue, but the interaction has not been formally tested across all six live categories.

---

## Appendix B — Governance Boundaries

The following boundaries are stated explicitly to support institutional review:

1. The grade is a **within-shelf ranking over observable disclosed data** — not a health verdict, a dietary recommendation, or an absolute quality certification.
2. **No external database value enters the score engine directly.** External sources (EFSA, JECFA, FDA, USDA FDC) calibrate and justify rules via the evidence registry; the engine reads in-house BSIP0 labels only (EDPG firewall).
3. **Every scoring rule requires a co-signed evidence-registry entry** (Nutrition Agent D7 + Product Agent D7) before Data Agent implementation. Either agent can block. No disputed rule is deployed.
4. **D4 score integration is owner-gated** (frozen-invariant tripwire #1). Current D4 is annotate-only.
5. **Framework terms do not appear in consumer copy.** NOVA, BSIP, structural_class, cap, floor — none of these surface to consumers. The consumer sees one grade + optional drilldown findings in plain language.

---

*End of Glass Box Technical Methodology v1. Authored by Nutrition Agent (TASK-181R, 2026-06-05). For NDA/partner use. Not for public publication.*
