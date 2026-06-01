# Cross-Category Drift Audit — v1

**Date:** 2026-05-28  
**Categories audited:** חלב (milk), מעדנים, לחם (bread)  
**Template reference:** comparison_template_v1.md  

---

## Audit Scope

This audit checks each category's current editorial state against the frozen template standard. The goal is to identify where Bari's three active categories diverge from the canonical architecture — and to flag risks before they reach the product.

Severity scale:
- **PASS** — conforms to template
- **WATCH** — minor drift, no immediate action needed
- **FIX** — active deviation requiring correction
- **GAP** — template element not yet built

---

## Category Status Summary

| Dimension | חלב | מעדנים | לחם |
|---|---|---|---|
| Tone consistency | PASS | PASS | WATCH |
| Ontology leakage | PASS | PASS | WATCH |
| Dashboard drift | PASS | PASS | FIX |
| Editorial drift | PASS | WATCH | FIX |
| Metadata creep | PASS | PASS | WATCH |
| Row density | PASS | GAP | GAP |
| Hero spec | PASS | GAP | GAP |
| Prologue spec | PASS | PASS | PASS |
| Methodology spec | PASS | PASS | WATCH |

---

## Category Assessments

---

### חלב (Milk) — Gold Standard

**Overall status: PASS**

Milk is the reference implementation. It established the core Bari pattern before the template was formalized. Its current state is used as the benchmark for all drift detection.

**What it does well:**
- Products arrive before any system element
- No dashboard, map, or analytics layer in the primary experience
- Comparisons are emotionally legible — similar packaging, visible score gap, one sentence
- Score chip is minimal: number and grade, no color
- Methodology is footer-weight, 2–3 sentences

**Residual risks to monitor:**
- If additional products are added to the milk shelf, ensure the filter remains single-select with no new analytical dimensions
- The milk comparison set is small (6 products). If a redesign tempts adding a "full comparison table" to expand coverage, resist — the constrained set is a feature, not a limitation

**Ontology:** No framework terms in current consumer-facing text. PASS.

**Recommendation:** Treat milk as the benchmark. Do not alter it during the operationalization phase.

---

### מעדנים — Recently Built

**Overall status: PASS with implementation gaps**

The מעדנים editorial architecture (maadanim_editorial_v1.md) was designed to the frozen template spec. The content is correct. The gaps are in implementation artifacts not yet built.

**Tone: PASS**
The editorial document and insight lines are restrained but fearless. The icon paradox finding (מילקי scores E) is named directly without moralizing. Type 2 contradiction lines are in place for the key products.

**Ontology: PASS**
The editorial doc explicitly lists forbidden terms. The insight lines do not expose BSIP terminology, cap logic, or dimension names. NOVA is rendered as composition observations (additive count, ingredient lists) not as a numbered system.

**Dashboard drift: PASS**
The editorial doc explicitly prohibits cluster maps, distribution charts, brand ranking tables, and score summary boxes before products. These prohibitions are in the right place. Risk is low if the Cursor implementation follows the spec.

**Editorial drift: WATCH**
The editorial document includes a "Category Architecture Notes" section (Part 2) that explains the six cluster system by name (milky_style, protein_forward, etc.). This is internal framework language. It should not appear in the consumer product. The risk: a developer reading the editorial doc might build cluster labels directly from the internal names.

*Fix:* The cluster display names in the filter spec are already the consumer-facing versions ("מילקי ודומיהם", "מוצרי חלבון"). Confirm these are what gets built — not the internal slugs.

**Metadata creep: PASS**
Expanded row spec is clearly bounded (nutrition 5-field, ingredients, data note, confidence state). No structural class, no dimension scores, no cap information in the spec.

**Row density: GAP**
The insight lines are written (maadanim_insight_lines_v1.md). The visual row spec (image size, padding, chip dimensions) is in comparison_template_v1.md section 4c. This has not been applied to a Figma or component spec for מעדנים. Implementation risk: developers use default dense table styling.

*Action:* When building the מעדנים component, reference comparison_template_v1.md section 4c directly for row rhythm. Do not derive row density from the editorial doc.

**Hero: GAP**
The hero product for מעדנים is identified (מילקי בטעם שוקולד, 40.3/D). The hero sentence is drafted in maadanim_editorial_v1.md Part 8. Implementation spec is in comparison_template_v1.md section 2. Not yet connected in a single Cursor-ready component spec.

*Action:* When briefing Cursor on the מעדנים hero, combine: comparison_template_v1.md §2 (structural rules) + maadanim_editorial_v1.md §Part 8 §section 1 (copy).

**Highlighted pair: PASS**
One pair designated: מילקי 40/D vs. יופלה GO 70/B. Driver line written. Maximum one pair rule satisfied.

---

### לחם (Bread) — Multiple Iterations, Active Risk

**Overall status: WATCH/FIX**

Bread has the longest editorial history (bread_retail_001 → 002_frontend → 003) and the highest drift risk because multiple documents exist with different architectural generations.

**Tone: WATCH**

The bread editorial documents span multiple iterations. Early iterations (bread_retail_001 analysis, blog_v1/v3) used an investigative journalism register that is heavier than the current standard. This tone may re-enter through historical document references.

Specific risk: the bread blog documents (bari_bread_blog_v3.md, bari_bread_refinement_v1.md) include multi-section article architecture with InsightCards, ScoreDriverTables, and "12-section architecture" elements that are explicitly not part of the frozen template.

*Fix:* The bread_template_application_v1.md (this sprint) supersedes the bread blog documents for page architecture. Mark bread_blog_v3.md and bread_refinement_v1.md as DEPRECATED for page architecture; retain for analytical content (scores, comparisons, product data) only.

**Ontology: WATCH**

The bread dataset introduced "fermentation_detected" as a signal that has real consumer-facing value. The "תסיסה" filter dimension in the bread template application exposes this signal in consumer language. This is an approved exception — "מחמצת" is already printed on bread packaging.

Risk: the filter label "ללא מחמצת מזוהה" may prompt UI designers to add explanatory tooltips that over-explain the signal detection process. Keep any tooltip to one sentence: "רשימת הרכיבים לא כללה סמנים של תסיסת מחמצת."

**Dashboard drift: FIX**

The bread operational history includes:
- A "frontend JSON" (bread_retail_002_frontend) with a 248KB schema containing aggregate metrics, comparison tables, and category averages
- Reports (13 total from retail_003) that include segment comparisons (commodity avg 50.7 vs. wellness avg 60.0)
- A batch summary report format that surfaces score distributions

These are analytical artifacts for internal use. None should appear in the consumer product. The risk is that when building the bread page, a developer reaches for these reports as source material and surfaces aggregate data (segment averages, distribution charts) that belongs in internal documentation only.

*Fix:* The bread consumer page uses only: per-product BSIP2 traces. Not the batch summary. Not the mass_market_anchors report. Not any aggregate metric. The only numbers that appear publicly are product-level numbers: score, grade, nutrition fields per 100g, ingredient list.

**Editorial drift: FIX**

The most serious bread drift risk: the bread blog v3 architecture includes "12-section article structure" with components (InsightCard, ScoreDriverTable, fermentation explanation sections, wellness-halo glossary). These are all explicitly excluded from the frozen template.

The bread category currently has two conflicting architectural visions:
1. **The old bread blog architecture** — investigative journalism, 12 sections, heavy editorial structure
2. **The frozen comparison template** — hero, prologue, table, methodology

These cannot coexist. The frozen template wins. The bread blog documents are deprecated as architecture references.

*What survives from old bread documents:*
- Specific product names and scores (factual, still valid)
- Comparison pair identification (the sourdough gap)
- Fiber laundering finding (editorial finding, still valid)

*What is retired:*
- InsightCard component
- ScoreDriverTable component
- 12-section article structure
- Fermentation explanation sections
- Any sidebar, glossary, or framework explanation element

**Metadata creep: WATCH**

The bread BSIP2 traces include fermentation markers, fiber laundering flags, and GSS (germination/sourdough/sprouted) signals that are not in the standard expanded row spec. These signals are editorially valuable but must remain in BSIP2 traces — not surface in expanded rows unless rendered as consumer-facing observations.

Permissible expanded row addition for bread:
- "תסיסה מזוהה ✓" / "לא נמצאו סמני תסיסה" — one line, under data note

Not permissible:
- "GSS score: 0.8"
- "fermentation_detected: true"
- Fiber laundering flags by name

**Methodology: WATCH**

The bread batch summary includes a 13-report suite with analytical detail. This creates a risk that someone drafts a bread methodology section citing the analytical reports or explaining the fermentation detection algorithm.

The bread methodology should match the template exactly:

> "בדקנו מעל 80 מוצרי לחם ממדף שופרסל. הציון מבוסס על רכיבים, ערכי תזונה ורמת עיבוד — לא רק על קלוריות. הציונים יחסיים לקטגוריית הלחם. [המתודולוגיה המלאה →]"

No mention of fermentation signal methodology. No mention of report count. No mention of aggregate statistics.

---

## Cross-Category Consistency Risks

These risks span all three categories and apply to future categories as well.

### Risk 1: Score chip color

No category currently uses color-coded score chips. Monitor during implementation. If any developer proposes a red/yellow/green score chip: decline. Reference comparison_template_v1.md §4c.

### Risk 2: The "what this means" instinct

Every category has a finding that creates pressure to explain it. "מילקי scores E — here's why." "Sourdough labels aren't what they seem — here's the mechanism." The insight line handles this. Nothing else should. Any content that begins with "here's why" is methodology and belongs on the methodology page only.

### Risk 3: Historical document drift

Each category has multiple historical documents. Developers or editors reaching for context may use older documents that predate the frozen template. All major category documents should have a header note indicating whether they are ACTIVE or DEPRECATED for architectural use.

| Document | Status |
|---|---|
| comparison_template_v1.md | ACTIVE — canonical |
| insight_line_spec_v1.md | ACTIVE — canonical |
| maadanim_editorial_v1.md | ACTIVE — category analysis |
| maadanim_insight_lines_v1.md | ACTIVE — production ready |
| bread_template_application_v1.md | ACTIVE — use for implementation |
| bari_bread_blog_v3.md | DEPRECATED for architecture — retain for product data only |
| bari_bread_refinement_v1.md | DEPRECATED for architecture — retain for product data only |
| snack_bar_editorial_recovery_v1.md | ACTIVE — snack bar philosophy |
| snack_bar_blog_v1.md | DEPRECATED for architecture — retain for product data only |

### Risk 4: "One more comparison" pressure

Each category currently has zero or one highlighted comparison pair. Pressure will arise to add a second (and third). The rule is one maximum. Every additional pair is an editorial architecture expansion that should be declined.

---

## Summary Recommendations

| Action | Priority | Category |
|---|---|---|
| Deprecate bread blog architecture docs | HIGH | לחם |
| Confirm cluster display names (not slugs) in מעדנים filter | MEDIUM | מעדנים |
| Write bread insight lines for 81 products using spec | MEDIUM | לחם |
| Confirm bread hero product from data (score D, recognized brand, sourdough label) | MEDIUM | לחם |
| Enforce expanded row boundary — no GSS/fermentation flags by internal name | MEDIUM | לחם |
| Apply row rhythm spec (comparison_template_v1.md §4c) to all three categories | MEDIUM | All |
| Do not color-code score chips during implementation | LOW | All |
| Monthly drift check: run leakage + drift checklists on published pages | ONGOING | All |

---

## Tone Reference

The gold standard is this sentence from the מילקי insight line:

> "הגביע הכי מוכר בקטגוריה, הציון הנמוך בה."

Fourteen characters. No verdict. Two facts that produce a sharp, uncomfortable observation. The reader does the rest.

Every piece of editorial content in every Bari category is trying to reach that level of restraint — and that level of fearlessness. They are not opposites. They are the same thing.
