# Crackers Category Constitution v1

**Classification:** Governing Framework — Internal
**Issued:** 2026-07-01
**Author:** Nutrition Agent
**Status:** Active — gates TASK-433 (crackers split) BSIP0 scrape
**Governed by:** Comparison Governance Constitution v1 (`comparison_governance_v1.md`), Consumer Use-Case & Purpose Guardrails v2 (`consumer_usecase_guardrails_v2.md`), Cereals Gap Resolution v1 (`cereals_gap_resolution_v1.md`)
**Precondition satisfied:** This is a methodology/boundary document only. No scoring rule is changed. No published score is changed. One factual verification item is flagged for Data Agent (Section 2.3) — it is a check, not a proposal.

---

## 0. Standing precedent — this split was already anticipated

Cereals Gap Resolution v1, Meta-Finding 3 (bread section, line ~563), on file since 2026-05-29:

> "Crispbread / crackers occupy the same retail aisle as standard bread but are architecturally distinct (typically higher in fat, lower in water content, fundamentally different texture and serving role). The Rule 5 proxy indicators will identify these products as a distinct pool at BSIP2 run time."

This constitution is the execution of that standing prediction under **Comparison Governance Constitution v1, Article II, Rule 5 (Architectural Divergence Sub-Category Rule)**. Rule 5's proxy indicators (NOVA ≥3 vs. bread's typical NOVA 1–2 median; added sugar; added fat) are satisfied by at least 4 of the 6 current records (Swedish-style, rye-style, KRIT, Osem — all carry sugar + oils absent from typical bread median). Under Rule 5's conservative-inclusion clause, the whole 6-record cluster defaults into the separate pool rather than forcing a per-SKU split — consistent with how granola was separated from cereal.

**Conclusion: crackers is not a new invention — it is the governed, already-flagged execution of Rule 5.** No new governance mechanism is required; only the category-specific parameters this document supplies.

---

## 1. Category boundary — what IS and ISN'T a cracker

### 1.1 Rule for the Data Agent (apply at BSIP0 corpus filter)

**IN scope — scores as "cracker":**
A product is a cracker if it is a **flat, baked, dry snap/crisp product intended to be eaten as-is or as a topping base**, typically <15% moisture, shelf-stable without refrigeration, and marketed/shelved as a standalone snack or accompaniment (not as a bread substitute for sandwiches).

Concretely IN:
- קרקרים / crackers proper (all 6 current records)
- קראנצ'ים / crisp-style savory snap crackers, rice/corn snap crackers (אורז תפוח, פריכיות אורז) — same functional role (dry, snap, topping-base or standalone snack)
- water crackers, wafer-style crackers (wafer-thin, baked, dry)
- טוסטים / melba toast — functionally a twice-baked cracker, not bread

**OUT of scope — route elsewhere or exclude:**
- **מצות / matzah** — OUT. Distinct regulatory/cultural category (unleavened, Passover-driven purchase pattern, its own consumer decision frame per Comparison Governance Constitution Article II §2.1 primary-purpose test). Matzah is not chosen interchangeably with a cracker for the same eating occasion. If Bari ever scores matzah, it needs its own category, not a crackers sub-pool.
- **גריסיני / breadsticks** — OUT of crackers, stays IN bread (or its own future pool). Breadsticks are a leavened, higher-moisture baked product structurally closer to bread than to a dry snap cracker. Do not fold into crackers on the basis of shelf co-location alone (Comparison Governance Constitution Article II §2.4 Rule 1 — shelf proximity is not a comparison-eligibility criterion).
- **פריכיות אורז generic puffed rice cakes** at the very low-density end (Osem/Kitkarot-style pure puffed rice, ~380 kcal but near-zero fat, near-zero ingredient complexity) — FLAG, do not auto-include. These sit at the boundary between "cracker" and "puffed snack." Apply Rule 5 proxy check at BSIP1: if fat <2g/100g AND ingredient count ≤2 (essentially rice + salt), route as a **borderline sub-pool** or hold for a separate "rice cakes" ruling rather than silently merging into the 6-record cracker cluster, which currently has real fat/oil architecture in 4 of 6 records. This is a flag for Data Agent judgment at corpus-filter time, not a hard exclusion.
- **לחמניות קשות (hard rolls)** — OUT, stays bread. These are bread-format (leavened, higher moisture) regardless of "hard" texture in the name.

### 1.2 The crisp rule for the Data Agent

> **A product is IN the crackers corpus if and only if it is unleavened-or-minimally-leavened, flat, baked to <15% moisture, and consumed as a snap/crisp standalone or topping base — not as a sandwich-bread substitute, and not defined by a religious/cultural observance (matzah) or a puffed-extrusion process with near-zero fat and minimal ingredients (rice cakes, hold for separate ruling).**

Boundary cases default OUT of the initial 6-based cluster and into a flagged review list, per the conservative-inclusion principle already established for granola (Rule 5: "It is preferable to over-include in the distinct pool than to distort the parent category pool" — applied here in reverse, since crackers is the smaller/newer pool: don't dilute a clean 6-record founding cluster with ambiguous puffed-snack products sight-unseen).

---

## 2. Scoring framing — does the engine already handle crackers correctly?

### 2.1 Direct answer

**No scoring change is warranted for the calorie-density philosophy itself.** The category-relative architecture already exists and is designed exactly for this case. **But there is an open factual verification question (not a rule proposal) that Data Agent must confirm before the fresh BSIP2 run: which calorie-density table the 6 legacy records were actually scored under.**

### 2.2 What the engine already has (evidence, not inference)

`03_operations/bsip2/proto_v0/src/constants.py`, `CALORIE_DENSITY_TABLES`, already contains a **dedicated `"cracker"` archetype**, distinct from `"bread"` and from `"crispbread"`:

```python
# Bread: 200-330 kcal/100g is normal (whole-grain loaf ~240, white loaf ~270, enriched ~320)
"bread":       [(200,90),(280,80),(330,70),(400,55),(480,35),(1e9,20)],
# Cracker: 380-480 kcal/100g is normal (denser than bread, less water)
"cracker":     [(250,90),(350,80),(420,70),(480,55),(550,35),(1e9,20)],
# Crispbread: 300-380 kcal/100g (compressed grain, low moisture)
"crispbread":  [(200,90),(300,85),(380,70),(450,50),(520,30),(1e9,15)],
```

This is the correct engineering pattern — the same category-relative calibration approach already governed and shipped for protein bars (`PROTEIN_BAR_WEIGHTS`, TASK-365/EV-PBAR-005/008, D6/D7 co-signed 2026-06-21), where a structurally calorie-dense format got a calibrated table and a lowered `calorie_density` dimension weight (0.15→0.10) rather than a philosophy change. `score_calorie_density()` in `score_engine.py` (line 1586) takes `category` as a parameter and looks up the matching table — the mechanism is category-agnostic in the sense that it applies uniformly, but category-*aware* in the sense the "expected" curve is right for the food format. This is exactly the non-distorting design Article III of the Comparison Governance Constitution requires (composite score, not single-driver attribution) and exactly what the existing rowVerdicts already narrate correctly in prose ("קלוריות גבוהות — כצפוי מקרקר יבש ומרוכז" / "high calories — expected for a dry, concentrated cracker").

### 2.3 The one thing that must be verified, not assumed

I traced the numeric consequence of table selection. If a cracker at 418 kcal is scored under `"bread"` (ceiling steps at 400→55) it scores **35** on the calorie-density dimension. If scored under `"cracker"` (ceiling steps at 420→70) it scores **70** — a 35-point swing on that one raw dimension, which (after the dimension's fractional weight in the composite) can plausibly move the published 0–100 score by several points. Since `category` is a caller-supplied string (not derived automatically from `_website_cluster` or a record field, per my grep of `score_engine.py` and `build_bread_bsip1.py`), **I cannot confirm from static code alone whether the 6 legacy records shown in this task were scored under `"bread"` or `"cracker"`.**

**This is a factual trace-verification item, not a scoring-rule proposal.** I am flagging it for Data Agent to check during the TASK-433 fresh BSIP2 run: **re-score all 6 (plus any newly admitted crackers) explicitly passing `category="cracker"`**, and diff against the currently published bread-corpus numbers. Two possible outcomes:
- **If the legacy 6 were already scored under `"cracker"`** — the fresh run reproduces them (net of any corpus/data changes), and this section closes with a corroboration note. No rule action.
- **If the legacy 6 were scored under `"bread"`** — the fresh crackers run will show a genuine, mechanical, already-approved-architecture score increase for calorie-density-driven products (KRIT, Osem in particular, both at the high end of the delta). This is **not a scoring change** — it is applying an existing, uncalibrated-for-nothing-new table correctly for the first time. No D6/D7 needed because the `"cracker"` table already exists in production code (not a new invention); it is a category-routing correction, which is exactly what a category split is for. Flag it to Product Agent as an expected-and-desired score movement from the split, per the re-flow policy (nothing frozen, verify movement).

**Do NOT silently pick either interpretation.** State the actual routing outcome in the TASK-433 return block with the before/after calorie-density sub-score for each of the 6, sourced from the real trace — this is the standard "trace-derived counts w/ command" bar (see memory: `feedback_return_self_verifying`).

### 2.4 Distortion registry check (per Constitution Article VI, Section C, C1–C3)

No distortion in the existing registry (DISTORTION-002 through -010) covers "absolute calorie density of a structurally dry/dense food unfairly sinking a score." I checked the full registry — the closest adjacent entries are DISTORTION-006 (Low-Calorie Halo, the *inverse* problem: rewarding low-cal too much) and DISTORTION-010 (Macro Obsession). Neither applies here. **This confirms no distortion review gap exists for crackers on this axis** — the category-relative table mechanism is the correct, already-governed answer, not an unaddressed bias. **No new DISTORTION-0XX entry is warranted.**

---

## 3. Comparison lenses for crackers

Applying Consumer Use-Case & Purpose Guardrails v2, Section 3 (three lenses), Rule 3 (Lens 1 default; 2/3 require positive architectural evidence):

**LENS 1 — General Everyday Choice (default for all 6 current records).**
A consumer choosing between crackers for a snack/topping-base occasion. All 6 current records compare directly under this lens; no functional or restriction claim rises to Lens 2/3 threshold in this set.

**Honest comparison axes a consumer actually uses on this shelf (informs insight-line/rowVerdict content, not a new scored dimension):**

1. **Whole-grain density / flour dominance** — what % of the flour base is whole grain vs. refined + corn grits + starch fillers. This is the single largest real differentiator in the current 6 (82–98% spelt vs. 33–84% refined-flour-dominant). Already the primary driver Content is narrating correctly ("שלושים ושלושה אחוז קמח חיטה מלא בלבד").
2. **Clean-label / ingredient-count minimalism** — 3–5 ingredients (both כוסמין crackers) vs. 8–10+ (KRIT, Osem, with multiple sugar sources: sugar + glucose syrup + sometimes more). This maps directly to the existing Matrix Integrity / ingredient-integrity dimension already scored — surface it explicitly in copy, don't invent a new axis.
3. **Fiber-per-serving as a topping base** — 9–10g/100g (spelt crackers) vs. 3g/100g (KRIT). Relevant because crackers are frequently eaten as a base for cheese/spreads/hummus — a consumer comparing "what am I building my snack on" cares about fiber contribution more than absolute calorie count, since the topping (not the cracker) is often the bulk of the eating occasion.
4. **Calorie-for-topping-base** is a real but secondary axis — since crackers are rarely eaten to satiety alone, per-100g kcal matters less to this specific shelf's actual use-case than it does for bread (a meal-replacement carbohydrate). This is exactly why the `"cracker"` archetype table exists and should NOT be narrated as if it were a demerit; see Section 4.

None of these axes requires Lens 2/3 — no record in the current 6 carries an architecturally-supported functional claim (no "high protein" cracker, no keto/gluten-free claim present in the data given). If a future scrape admits a functional or restriction-claim cracker (e.g., "high-fiber," "keto," "gluten-free"), apply the existing Marketing Divergence Finding thresholds (Guardrails v2 §5.2.1) — the "high protein" general-food threshold (≥15g/100g solid) already covers the case if it arises (the sesame-spelt cracker's 16g/100g would, incidentally, pass that threshold honestly if it ever carried the claim — it currently doesn't per the data given, so no finding is triggered today).

---

## 4. Category caveat (הערת קטגוריה) — content direction

Grounded in the real engine behavior confirmed in Section 2: crackers are structurally calorie-dense **by format, not by formulation failure**, and the engine already accounts for this via a category-relative calibration (Section 2.2) — this is a fact to state plainly, not a limitation to apologize for, and not a distortion to disclose defensively.

**Endemic-prevalence check (Constitution Article VI §6.2 Section C, criterion C5):** all 6 current records exceed 370 kcal/100g — that is 100% of the founding corpus, which clears the ≥50% endemic threshold. This **does** require a category-level note per the Endemic Distortion Protocol (Article VI §6.4) — not because it's a distortion, but because "why is every cracker's kcal number high" is a real, recurring reader question the note should pre-empt (same logic as the bread fermentation caveat, EXCEPTION-001).

**Direction for Content Agent (draft framing, subject to two-gate sign-off — this is NOT approved consumer copy, per the content sign-off hard rule):**

- Open with the fact, not a defense: crackers are dry, low-moisture baked products — removing water concentrates calories per 100g compared to bread, independent of ingredient quality.
- State plainly that Bari's score already accounts for this: the comparison is against other crackers, not against bread's calorie profile.
- Redirect the reader to the axis that actually differentiates this shelf: flour composition (whole-grain vs. refined + starch fillers) and ingredient-list length/sugar-source count — because that is where the real 22-point score spread (81.6 → 59.6) actually comes from, not from calorie count.
- Do not use "קלוריה" as if it were the villain of the page — the rowVerdicts already get this right ("קלוריות גבוהות — כצפוי מקרקר יבש ומרוכז"); the category note should generalize that same honest framing to the whole shelf once, so it doesn't need repeating on every card.

**Do not claim** (per Hard Rule 4/5 and Marketing Divergence discipline): do not say a cracker "is not a health food" or moralize about snacking frequency — Bari scores architecture, not the eating occasion.

---

## 5. Category launch checklist cross-reference (Constitution Article VI)

This document satisfies, in advance of BSIP0 scrape:
- **B1** (category boundary defined) — Section 1
- **B2** (sub-category structure) — n/a, single pool, boundary cases flagged for Data Agent judgment
- **C1–C5** (distortion review, including endemic check) — Section 2.4, Section 4
- **D5** (purpose divergence pairs) — none identified; all Lens 1
- **D6** (claim threshold table) — no new claim types present in current 6; existing general "high protein" threshold (Guardrails v2 §5.2.1) sufficient if triggered later

Outstanding for Data Agent / Product Agent, not resolved by this document:
- **A1–A6** (dataset requirements — product count, traceability, coverage) — depends on fresh BSIP0 scrape scope, likely well above 6 once rice-cake-boundary and full retail shelf are scraped
- **Section 2.3 verification item** (calorie-density table routing) — must be resolved with a real trace, reported in TASK-433's return block

---

## 6. Escalation status

No tripwire fires. This is boundary/methodology work inside my lane (D5 enrichment-config-adjacent, D6 proposer role exercised only to flag a verification item, not a rule change). Routing:
- **Data Agent** — executes Section 1 boundary rule at corpus filter; runs Section 2.3 verification during BSIP1/BSIP2; reports the actual table-routing outcome with numbers.
- **Product Agent** — co-signs if Section 2.3 verification surfaces a genuine score movement for KRIT/Osem-type records (expected-and-desired per re-flow policy, not a tripwire, but Product should see the movement table before go-live).
- **Content Agent + Adversarial QA** — own the category-note and insight-line copy per Section 4 direction; nothing in Section 4 is approved consumer text until both gates sign off.

---

*Crackers Category Constitution v1*
*Nutrition Agent*
*2026-07-01*
*Governed by: Comparison Governance Constitution v1 (Article II Rule 5, Article VI), Consumer Use-Case & Purpose Guardrails v2, Cereals Gap Resolution v1 (Meta-Finding 3 standing precedent)*
*Gates: TASK-433 BSIP0 scrape*
