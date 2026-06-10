# Recent Evidence Coverage Audit v1

**Purpose:** Audit 11 recent scientific/market findings against existing BSIP2 methodology before creating any new scoring rules.

**Core principle:** Do not add a new scoring layer until confirming it does not duplicate, contradict, or demolish existing Bari logic.

**Date:** 2026-06-10  
**Status:** Complete — no new scoring spec required  
**Owner:** Scoring Governance Lead  

---

## 1. Food Matrix Collapse

### Existing BSIP2 coverage

| Layer | How it captures matrix collapse | Weight/impact |
|-------|--------------------------------|---------------|
| NOVA proxy | NOVA 4 → processing_quality=35 overall score, extrusion signal (EV-043) directly detects puffed/extruded forms | NOVA 4 cap at 68 |
| Fragmentation spectrum | intact → mechanical → fractional → reconstructed (4 levels assigned to 28+ ingredient categories) | Drives fragmentation profile, feeds _score_processing_quality |
| Matrix Integrity Engine (standalone) | Degradation scores per ingredient (80-92 for reconstructed forms), assembly drag, HP reconstruction combos, protein engineering scores | NOT wired into composite score (research-only) |
| Extrusion signal (EV-043/TASK-216) | "מורחב" marker + puff subpool → NOVA 4 directly | Bypasses standard NOVA inference |
| Reconstitution detection | Milk powder, reconstituted dairy → EV-018 marker | NOVA 3 read for dairy |
| Whole Food Integrity dimension | NOVA-based WFI score + ingredient count + fermentation | 4% weight |
| Glycemic quality | Sugar penalty + fiber bonus + whole grain bonus | 12% weight (does not measure matrix directly) |
| Hyper-palatability patterns | Fat-sugar, fat-sodium, crunch-sweet combos penalize engineered formulations | HP family budget 12 |

### Gap classification: **Already covered**

Matrix collapse is already the single most-covered concept in BSIP2. Four separate layers address it: NOVA (processing level), fragmentation (structural form), extrusion (direct detection), and HP (engineered palatability). The Matrix Integrity Engine exists as a standalone research tool but is intentionally unwired.

### Demolition risk

- **High double-count risk.** Adding a "matrix collapse" score now would penalize the same products through NOVA, fragmentation, extruded detection AND the new score. A single product (e.g., puffed cereal bar with modified starch) could face: NOVA 4 cap (-32 on processing), reconstructed fragmentation penalty, extruded signal, HP pattern penalty, AND a new matrix collapse penalty — all for the same underlying mechanism.
- **Contradiction risk with fragmentation levels.** The existing fragmentation spectrum already defines a severity hierarchy. A new "matrix collapse" score using different thresholds would create internal contradictions about which matrix state is worse.

### Recommendation: **No action**

The mechanism is comprehensively covered. The fragmentation system + NOVA proxy + extrusion signal form a complete processing severity chain. If the Matrix Integrity Engine is ever wired into scoring, it should REPLACE (not stack on top of) the simpler NOVA-based processing score in a future architecture version (BSIP3 candidate).

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| `golden_products_suite.md` | Entire suite tests matrix integrity across all processing levels | All — rice cakes (ex14), instant noodles (ex15), vegan meat (ex20) are the canonical matrix-collapse products |
| `emulsifier_complexity_regression_v1.md` | Multi-agent products are also matrix-collapse products | Ex6, Ex13, Ex15, Ex18 |
| `run_regression_check.py` | Frozen batch-runs lock processing scores | bread_retail_003, milk_004, snacks run_001 |

---

## 2. Emulsifier Differentiation and Complexity

### Existing BSIP2 coverage

| Layer | How it covers emulsifiers | Weight/impact |
|-------|--------------------------|---------------|
| F1 identity deltas (TASK-222A, active) | carrageenan/CMC/P80 = −3 each (cap −6), lecithin = +2 relief | Up to −6 on additive_quality |
| Additive marker detection | emulsifier, stabilizer, thickener categories detected via regex | Feeds additive_marker_count → NOVA and caps |
| NON_LECITHIN_EMULSIFIER_RE (signal_extractor.py:337-339) | Matches E471, E472, E476, E481, DATEM, mono/diglycerides | Used for retired sprint1 correction (zeroed) |
| EV-003 (evidence registry) | CMC/P80 gut barrier disruption; carrageenan moderate-strong; lecithin benign | Grounds identity split |
| D4 additive tier library (glass box) | 36 additives with evidence tiers: carrageenan/CMC/BHA = contested; mono/diglycerides/DATEM/SSL = likely-neutral | Presentation only, no score movement |
| **ECS-v1 (NOT IMPLEMENTED)** | Three-tier complexity score: high −5, medium −3, low −1 + complexity adjustment | Max budget 8 pts |

### Gap classification: **Covered but under-specified**

Emulsifier differentiation exists (F1 identity deltas) for the top 3 concern agents. The full three-tier system (ECS-v1) is designed and went through QA but is NOT yet implemented. Gap is in implementation status, not methodology.

### Demolition risk

- **Double-count with F1.** A new emulsifier scoring rule that also penalizes carrageenan/CMC/P80 would double-stack on the existing −3 each identity deltas. The ECS-v1 design already addresses this by using different per-agent weights (−5 for ECS vs −3 for F1) and targeting a different dimension signal.
- **Double-count with additive_marker_count.** All emulsifiers already count as additive markers (emulsifier, stabilizer, thickener categories). Adding a new score that counts them again would be double-counting.
- **Regression risk.** Any new rule that changes emulsifier scoring could shift snack_bar scores (highest emulsifier density), bread_light scores (multi-agent systems), and dairy_protein scores.

### Recommendation: **Amend existing spec — implement ECS-v1**

Do NOT create a new emulsifier methodology. ECS-v1 already exists and passed QA. The next step is implementation (taxonomy extension, signal extractor extension, engine scoring function, constants).

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| `emulsifier_complexity_regression_v1.md` | 22 examples covering all tiers and complexity levels | Ex6 (ice cream), Ex10 (bread light), Ex13 (snack bar), Ex15 (pudding), Ex18 (gum) |
| `golden_products_suite.md` | Hummus (guar+xanthan), protein pudding (multi-additive), flavored yogurt | Medium-tier products |
| Frozen invariants | Milk 85/A must be unchanged, snk-001 70/B must be unchanged | Milk (0 emulsifiers), snack bar ceiling |

---

## 3. Fermentation and Phytate Bioavailability

### Existing BSIP2 coverage

| Layer | How it covers fermentation | Weight/impact |
|-------|---------------------------|---------------|
| Fermentation detection (signal_extractor.py:210-236) | 21+ Hebrew terms including retail vocabulary fix (EV-022) | Drives has_fermentation flag |
| Fermentation direct bonus (PROCESSING_PENALTIES) | +8 pre-cap, NOVA 1-3 only | PROCESSING_LOAD family |
| WFI dimension bonus | +5 when fermentation detected | whole_food_integrity dimension |
| Matrix integrity fermentation credit | 14-38 pts per marker, cap 42, max factor 0.40 | Standalone MI engine |
| R7 v1.1 culture bonus (RECAL_P0) | Path A = declared culture, Path B = yogurt/cultured cheese subtype | RECAL_P0 gated |
| EV-015 (evidence registry) | Fermentation degrades phytate, improves mineral bioaccessibility | Grounds the bonus |
| EV-022/024 (vocabulary fixes) | Mirrored BSIP1 culture detection into BSIP2 scorer | Repaired 0% → 49/86 detection |

### Gap classification: **Already covered**

The fermentation bonus is active, justified by phytate degradation (EV-015), and restored to correct detection levels by EV-022/024. The +8 bonus on NOVA 1-3 products with live culture is the score expression. No gap exists — the mechanism (phytate degradation → mineral bioaccessibility) is explicitly cited in EV-015 as the scientific rationale.

### Demolition risk

- **Double-count if expanded.** If the current +8 bonus were supplemented with a separate "phytate bioavailability" credit, the same mechanism would be credited twice. Fermentation has already received special treatment (separate from standard NOVA) and additional vocabulary-fix tasks.
- **Regression risk.** Any change to fermentation scoring would shift yogurt, bread (sourdough), and potentially fermented dairy scores. The yogurt D-score distribution (0 A, 29 B, 32 C at post-EV-024) would change.

### Recommendation: **No action**

The fermentation bonus exists, is grounded, and functions correctly post-EV-022/024. The phytate mechanism is the scientific justification already on file. No new rule or spec needed.

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| `run_yogurt_003` | Yogurt fermentation detection AND bonus | Plain yogurt, flavored yogurt, drinkable yogurt |
| `batch_run_bread_retail_003` | Sourdough fermentation detection | Sourdough breads |
| Golden products suite | Plain Greek yogurt (fermented, should score high) | Fermented dairy |
| Frozen invariants (milk_004) | Milk has no fermentation — must be unchanged | All non-fermented categories |

---

## 4. DIAAS / Protein Quality Refinement

### Existing BSIP2 coverage

| Layer | How it covers protein quality | Weight/impact |
|-------|------------------------------|---------------|
| R1 category-relative protein scales | 7 archetype-specific curves (dairy, bread, snack_bar, milk, yogurt, sauce_spread, default) | protein_quality base |
| Source factors | whole_food=1.0, dairy=1.0, mixed=0.85, isolate=0.70, unknown=0.80 | Multiplies base score |
| F2 matrix discount (TASK-222B, active) | reconstructed=0.80 (bar-format capped), collagen=0.55 (all categories) | Discounts protein quality contribution |
| Dairy source typing (TASK-144 Fix 3) | Whole dried dairy → factor 1.0 (not isolate haircut) | Preserves dairy identity |
| DIAAS W1.5 (glass box, default OFF) | Rule A: complete-protein whitelist → +3 D2 credit. Rule B: generic protein → D5 annotation | Gated, presentation-only |
| Protein quality dimension weight | 10% of composite score | Moderate weight |

### Gap classification: **Already covered**

The protein quality system is one of the most refined in BSIP2. Category-relative scales, source factors, matrix-form discounts, and dairy-identity preservation form a multi-layer system. DIAAS W1.5 (glass box) adds an additional +3 credit for complete-protein sources when activated. The existing source factors (whole_food=1.0, dairy=1.0, isolate=0.70) function as a DIAAS proxy where precise AA profile data is unavailable.

### Demolition risk

- **Triple-count risk.** Protein quality is already scored through: (1) R1 base scale, (2) source factor, (3) matrix discount. Adding a fourth layer (e.g., a separate DIAAS score) would overweight protein vs other dimensions.
- **F2 discount is already DIAAS-grounded.** The 0.80 reconstructed discount is explicitly pegged to the 47-81% DIAAS range (TASK-222B constants.py:310-313). Adding another DIAAS layer on top would be circular.
- **Regression risk.** Snack_bar scores (reconstructed protein, F2 discount active), dairy scores (isolate haircut now preserved by dairy typing), collagen products.

### Recommendation: **No action**

The protein quality system already uses DIAAS-equivalent reasoning (source factors = DIAAS proxy, F2 matrix discount = DIAAS-grounded). DIAAS W1.5 exists in glass box for future activation. No new methodology needed.

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| `run_regression_check.py` | Golden structural regression (11 tests) covers protein dimension | Protein shakes, snack bars, dairy |
| Frozen milk invariant | Dairy protein quality curve is frozen | Milk 85/A |
| Snack bar ceiling (snk-001 70/B) | F2 discount active for bar-format | All snack bars |

---

## 5. Fiber Functionality (Viscous vs Non-Viscous)

### Existing BSIP2 coverage

| Layer | How it covers fiber | Weight/impact |
|-------|--------------------|---------------|
| Fiber scoring curve | (0,0) to (12,95) — all fibers equal | Scales nutrient_density (35% of dimension) |
| Fiber-not-applicable override (EV-027) | Categories where fiber=0 is natural | nutrient_density scored on protein alone |
| Fortification discount | has_fortification → score × 0.80 | Discounts isolated fiber additives |
| Whole-grain detection | 12 markers, glycemic bonus +5 | Glycemic quality |
| EV-006 (evidence registry) | Viscous vs non-viscous fiber documented, `should_affect_score_now: false` | Requires vocabulary dictionary |

### Gap classification: **Covered but under-specified**

EV-006 explicitly identifies this gap: viscous fibers (psyllium, β-glucan) reduce glycemic response via gel formation; non-viscous fibers (inulin, polydextrose) do not. The evidence entry exists but is gated on a viscous-fiber vocabulary dictionary. Current scoring treats all fibers as equal, which is known to over-credit inulin-fortified products.

### Demolition risk

- **Low demolition risk.** Fiber is a single dimension (nutrient_density, 35% of a 15%-weight dimension = 5.25% of total score). Changing fiber differentiation is low-impact.
- **No contradiction.** Current system does not differentiate — a viscous/non-viscous split would be additive, not contradictory.
- **Regression risk.** Cereal scores (oat β-glucan vs inulin-fortified cereals), snack bars with added inulin (over-credited currently).

### Recommendation: **Amend existing spec — implement EV-006 vocabulary**

The gap is identified and documented. What's needed is the Hebrew vocabulary for viscous vs non-viscous fibers, then a score differentiation within the existing fiber curve. No new methodology spec — amend the fiber scoring in constants.py.

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| `golden_products_suite.md` | Oat milk (fiber-fortified), breakfast cereal (fortified, over-credited) | Cereal scores, fiber-fortified snack bars |
| Bread retail_003 | Fiber sources in bread (some inulin-added, some intrinsic) | Bread scores |
| Existing batch runs | Any cereal or snack product with declared fiber | All categories with fiber |

---

## 6. Sweetener Differentiation

### Existing BSIP2 coverage

| Layer | How it covers sweeteners | Weight/impact |
|-------|--------------------------|---------------|
| 3-tier sweetener system | A (stevia/monkfruit): −8, cap 75; B (polyols): −10, cap 73; C (synthetic): −15, cap 70 | Active, outside CONCERNS graph |
| Sweetener detection (signal_extractor.py:70-113) | 3 tier lists (A, B, C) with 20+ Hebrew/English terms | Worst tier dominates |
| Allulose relief (EV-004, active) | Sugar penalty reduced by 30% | Glycemic quality |
| Polyol penalty (EV-005, active) | 1 = −4, 2+ = −10, keto = −15 | additive_quality dimension |
| EV-017 (evidence registry) | Sucralose/saccharin gut dysbiosis documented as `should_affect_score_now: false` | Flag-only recommended |
| Polyol type map (signal_extractor.py:326-334) | 7 polyols mapped with Hebrew terms | Polyol detection |

### Gap classification: **Already covered**

Sweeteners are the most differentiated domain in all of BSIP2. Three tiers with tier-specific penalties and caps, allulose relief, polyol-specific penalties, humectant-group exclusion, keto overdrive, and a separate sweetener cap outside the CONCERNS coordination graph (so it cannot be weakened by other family budgets). EV-017 recommends flag-only for saccharin/sucralose above current scoring.

### Demolition risk

- **High double-count risk.** Every sweetener-related finding would double-penalize through the existing sweetener cap + sweetener penalty + whatever new rule is proposed. The tier system already differentiates by risk (A/B/C).
- **Regression risk.** Any sweetener change affects over 40% of all scored products (beverages, snack bars, yogurts, protein shakes, desserts).

### Recommendation: **No action**

The sweetener system is mature. EV-017 (further saccharin/sucralose differentiation) is already documented as flag-only — consistent with current tier C treatment. No new rule needed.

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| `golden_products_suite.md` | Coke Zero (ex15), protein pudding (ex16), sugary granola bar (ex17) | All sweetened products |
| Frozen invariants | No invariant has sweeteners (milk=85/A, bread retail_003, snk-001) | Unaffected — but every batch run would be |
| `emulsifier_complexity_regression_v1.md` | Several examples with sweeteners + emulsifiers (Ex7, Ex13, Ex18) | Diet products, gum |

---

## 7. FDA GRAS / Regulatory Watch

### Existing BSIP2 coverage

| Layer | How it covers regulatory watch | Weight/impact |
|-------|-------------------------------|---------------|
| Named-additive system (F1/F4) | BHA = −5 (FDA reassessment active), BHT = 0 (explicitly excluded) | additive_quality dimension |
| EV-003 evidence | References EFSA/IARC regulatory status for emulsifiers | Grounds tier assignments |
| D4 tier library | `contested` tier = regulatory-science gap (carrageenan, CMC, BHA) | Presentation only |
| D4 maintenance protocol | Periodic re-review of additive tiers | Architecture doc, no schedule |

### Gap classification: **Backlog / monitoring only**

BSIP2 has ad-hoc named-additive rules for additives under active regulatory review, but no systematic regulatory watch infrastructure. The D4 tier library maintenance protocol envisions periodic review but has no defined schedule.

### Demolition risk

- **Low.** Adding regulatory watch tracking would add data (new flagged additives) but not necessarily new scoring rules. Each additive would need its own evidence entry before scoring.
- **No regression risk** if implemented as monitoring-only (no score impact).
- **Risk of premature scoring.** If a regulatory review is ongoing (not concluded), adding a penalty would be penalizing uncertainty, not demonstrated harm.

### Recommendation: **Add registry mapping only**

Do NOT create new scoring rules. Add an EV entry noting the need for a regulatory watch list as input to the D4 tier library maintenance process. Implementation: add a `regulatory_watch.md` reference doc listing additives under active FDA/EFSA/IARC review, linked from the D4 maintenance protocol. No score impact.

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| (none) | No score change — monitoring only | None |

---

## 8. Microplastics / PFAS / Contamination Vectors

### Existing BSIP2 coverage

**None.** BSIP2 evaluates packaged food labels. Microplastics, PFAS, heavy metals, and environmental contaminants are:
- NOT declared on Israeli retail labels
- NOT detectable from ingredient text
- NOT inferable from nutrition panel
- NOT a packaged-food-label signal

### Gap classification: **Not implementable from labels**

Complete gap, but fundamentally outside BSIP2's scope. Israeli labels contain no information about packaging migration, environmental contamination, or processing-equipment shedding.

### Demolition risk

- **Zero demolition risk** — cannot be implemented from current data sources.
- **Risk of misleading scoring.** If proxy signals were used (e.g., "processed food → microplastics risk"), this would be a statistical inference, not a label signal, and would violate BSIP2's label-observability principle (EV-001 core constraint).

### Recommendation: **No action — monitoring only**

Create a monitoring backlog entry. Flag as "outside current data scope" — not actionable until:
1. Israeli retail labels declare contamination test results, OR
2. A third-party database with per-batch testing data is integrated

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| (none) | No score change — not implementable | None |

---

## 9. Clean-Label Marketing Risk

### Existing BSIP2 coverage

| Layer | How it covers clean-label risk | Impact |
|-------|-------------------------------|--------|
| D5 disclosure gap detector (glass box) | Detects bare generic terms (מייצבים, מתחלב, חומר משמר) without E-number breakdown | Presentation layer (severe band = disclosure gap) |
| Ingredient sanitization (TASK-144 Fix 1) | Removes marketing/health-claim bleed from ingredient text | Feeds sanitized_ingredient_count → NOVA |
| D4 additive tier library | Evidence-based tier labels per additive | Presentation only |
| Known failure modes (known_failure_modes.md:12) | Explicitly flags "clean-label" halo risk | Documentation |

### Gap classification: **Already covered**

The "clean-label" phenomenon (marketing a product as natural/clean while it contains significant additives) is already addressed by BSIP2's architecture:
1. The D5 disclosure gap detector catches products that use generic terms without E-numbers (e.g., "מייצבים" without listing which stabilizers)
2. The ingredient sanitization prevents marketing language from inflating ingredient counts
3. The D4 library provides evidence-based tier labels for individual additives

BSIP2 evaluates actual composition, not marketing claims. A product marketed as "clean-label" with 4 additives still gets additive_marker_count=4, the appropriate additive caps, and D5 disclosure annotations.

### Demolition risk

- **Medium.** Creating a "clean-label penalty" would penalize products for marketing language, not composition. This risks: (a) false positives (actually clean products with natural marketing), (b) false negatives (highly engineered products without explicit "clean" claims), (c) gaming (removing the word "natural" from packaging to avoid the penalty).
- **Regression risk.** Bread products with "no preservatives" claims would shift, snack bars with "natural" positioning, yogurt with "clean ingredients" language.

### Recommendation: **No action**

The system already penalizes the actual composition. D5 disclosure gaps add a presentation-layer flag when labels hide behind generic terms without disclosure. A marketing-claims-based penalty would be analytically unsound.

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| `batch_run_bread_retail_003` | Bread products with "no preservatives" marketing | Bread scores |
| `golden_products_suite.md` | Sugary granola bar (canonical health-halo product) | Snack bars |

---

## 10. HPP / PEF Non-Thermal Processing

### Existing BSIP2 coverage

**None.** HPP (high-pressure processing) and PEF (pulsed electric field) are not detectable from standard Israeli retail labels.

- HPP is sometimes mentioned on premium product labels ("HPP", "פסטור בקור") but is not a required declaration
- PEF is never declared on Israeli retail labels
- Neither signal is in the current signal extractor

### Gap classification: **Not implementable from labels**

Cannot be detected reliably from label data. Voluntary front-label claims (e.g., "cold-pressed," "HPP") could be detected but:
- Coverage would be near-zero
- Would create perverse incentive (products NOT declaring HPP would score better)
- Would reward marketing language rather than actual processing method

### Demolition risk

- **Low demolition risk** (cannot be implemented).
- **Potential for bad rule.** If we treated "no thermal processing" as a positive signal: (a) low coverage, (b) marketing-gaming risk, (c) HPP products can still be ultra-processed (additives, isolates, flavorings are independent of pasteurization method).

### Recommendation: **No action — monitoring only**

Not implementable from current labels. If Israeli labels ever require processing-method declaration, revisit. For now, flagged as a monitoring backlog item.

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| (none) | No score change — not implementable | None |

---

## 11. Supply-Chain Verification

### Existing BSIP2 coverage

**None.** BSIP2 evaluates the final packaged product label. Supply chain attributes are not available:
- No origin declarations on Israeli retail labels (beyond "product of X" which is too coarse)
- No animal welfare data
- No sustainable sourcing claims verified
- No batch-level traceability data

### Gap classification: **Not implementable from labels**

Completely outside BSIP2's scope. Would require:
- Full supply-chain API integration
- Third-party certification database access
- Per-batch testing data feeds

### Demolition risk

- **Zero demolition risk** — outside scope.
- **High reputational risk** if BSIP2 attempted supply-chain scoring without data. Would violate label-observability principle and potentially mislead consumers.

### Recommendation: **No action — monitoring only**

Architecture boundary decision: BSIP2 is a label-based packaged food scoring system. Supply-chain verification is a separate capability (future program, possibly "Bari Trust" or "Bari Verify"). Do NOT add supply-chain signals to BSIP2.

### Regression protection

| Regression file | Why it covers this | Products at risk |
|----------------|-------------------|------------------|
| (none) | No score change — outside scope | None |

---

## Coverage Mapping Table

| Finding | Existing coverage | Gap class | Demolition risk | Recommendation |
|---------|-----------------|-----------|----------------|---------------|
| Food matrix collapse | NOVA, fragmentation, extrusion signal, MI engine, HP patterns, WFI | Already covered | HIGH — would quadruple-penalize same mechanism | No action |
| Emulsifier differentiation/complexity | F1 identity deltas (active), ECS-v1 (designed, not impl) | Covered but under-specified | HIGH — double-count with F1 + additive_marker_count | Amend existing spec — implement ECS-v1 |
| Fermentation/phytate | +8 bonus, +5 WFI, MI credit, all active | Already covered | MEDIUM — double-count if expanded | No action |
| DIAAS/protein quality | R1 scales, source factors, F2 discounts, DIAAS W1.5 (gated) | Already covered | HIGH — triple-count through R1 + source + matrix | No action |
| Fiber functionality | All fibers equal (EV-006 registered, not implemented) | Covered but under-specified | LOW — small dimension weight | Amend existing spec — implement EV-006 vocabulary |
| Sweetener differentiation | 3 tiers + caps + polyol + allulose (all active) | Already covered | HIGH — double-count through cap + penalty | No action |
| FDA GRAS/regulatory watch | Named-additive system (BHA), D4 tiers, no systematic tracking | Backlog / monitoring | LOW — monitoring has no score impact | Add registry mapping only |
| Microplastics/PFAS | None | Not implementable | ZERO — outside scope | No action — monitoring |
| Clean-label marketing | D5 disclosure gaps, ingredient sanitization, known failure modes | Already covered | MEDIUM — marketing claims != composition | No action |
| HPP/PEF non-thermal | None | Not implementable | ZERO — outside scope | No action — monitoring |
| Supply-chain verification | None | Not implementable | ZERO — outside scope | No action — monitoring |

**Summary:**
- **7 findings** → No action (already covered or not implementable)
- **2 findings** → Amend existing spec (ECS-v1 implementation, EV-006 vocabulary)
- **1 finding** → Add registry mapping only (regulatory watch)
- **1 finding** → Already covered but ECS-v1 is designed and not yet implemented

---

## No-Demolition Checklist for Future BSIP2 Methodology Tasks

Any new scoring rule proposal MUST pass all checks before acceptance:

### Check 1 — Dimensional uniqueness
- Does a dimension already score this mechanism? (check processing_quality, additive_quality, protein_quality, fat_quality, glycemic_quality, nutrient_density, satiety_support, regulatory_quality, whole_food_integrity)
- If yes: the new rule targets a DIFFERENT dimension signal OR replaces the existing approach (not stacks on top)

### Check 2 — Penalty family check
- Does a penalty family already cover this concern? (check SUGAR_LOAD, CALORIE_LOAD, PROCESSING_LOAD, SODIUM_LOAD, FAT_QUALITY, additives, ingredient_complexity, hyper_palatability, general)
- If yes: new rule must be folded into the existing family budget, not create a new parallel family

### Check 3 — Fragmentation spectrum check
- Is the new rule about structural food form (matrix integrity, processing disruption)?
- If yes: check if fragmentation spectrum (intact/mechanical/fractional/reconstructed) already covers it
- Check: does extrusion signal (EV-043) already detect it? Does NOVA proxy already classify it?

### Check 4 — Additive identity check
- Is the new rule about a specific additive or additive class?
- If yes: check if it appears in ingredient_taxonomy._ADDITIVES
- Check: is it already in EV-003 (emulsifier tiering), F1 identity deltas, or ECS-v1?
- Check: is it in the D4 additive library with an evidence tier?

### Check 5 — Evidence registry check
- Does an EV entry already exist for this mechanism?
- If yes: what does `should_affect_score_now` say? If false, the evidence supports monitoring/research, not scoring

### Check 6 — Label observability check
- Is the signal detectable from Israeli retail labels (ingredient list, nutrition panel, product name)?
- If no: BLOCKED — cannot score what cannot be observed

### Check 7 — Regression protection check
- List all regression files that would be affected
- Which frozen invariants could shift?
- Run a corpus diff before:after the change

### Check 8 — Anti-accumulation check
- Calculate: what is the MAX total penalty a single product could receive under the new rule + all existing rules that address the same mechanism?
- If the total exceeds the family budget + coordination cap: FAIL — the system would over-penalize

### Check 9 — Rollback plan
- Can the previous state be restored with a single git revert?
- Are all changed files listed?
- Who must be notified?

---

## Recommended Next Task

Based on this audit, the next task should be **implementation, not new methodology:**

### TASK-NEXT: Implement ECS-v1 (emulsifier_complexity_score)

The audit confirmed that ECS-v1 methodology:
- Does NOT duplicate existing rules (F1 identity deltas target additive_quality dimension, ECS targets a new emulsifier_complexity signal)
- Does NOT contradict any existing rule (additive_marker_count counts functional categories, ECS counts canonical agents)
- Has regression protection (22 examples in emulsifier_complexity_regression_v1.md)
- Has demolition risk assessment (low — the 8-pt max budget is within the concern coordination framework)
- Has a design spec through QA (PASS WITH FIXES, all applied)

Implementation steps (from ECS-v1 §8):
1. Extend `ingredient_taxonomy._ADDITIVES` with 13 new Identity entries (6 medium, 7 low)
2. Add `tax_emulsifier_medium` and `tax_emulsifier_low` signals to `signal_extractor.py`
3. Add `EMULSIFIER_COMPLEXITY` constants block to `constants.py`
4. Add `_emulsifier_complexity()` scoring function to `score_engine.py`
5. Update concern coordination contract with the new family
6. Run regression: 22 ECS examples + golden structural regression + frozen invariants
7. Corpus diff gate on snack_bar, dairy_protein, sauce_spread, and bread_light corpora

**No new methodology spec is needed.** ECS-v1 is ready for implementation.

### Secondary: Register EV-NNN for viscous fiber vocabulary (EV-006 gating)

EV-006 is registered but gated on vocabulary development. The next step is a research task to compile Hebrew viscous-fiber terms (psyllium, β-glucan, guar gum as fiber) vs non-viscous (inulin, polydextrose, FOS, resistant dextrin) from the Israeli shelf. This is a data task, not a scoring rule task.
