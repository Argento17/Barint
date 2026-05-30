# Bari Exception Registry — v1

**Status:** Active  
**Date:** 2026-05-28  
**Scope:** All deliberate deviations from frozen architecture rules across all Bari categories  
**Authority:** Any addition to this registry requires explicit approval. Undocumented exceptions are architecture violations.

---

## Purpose

The Bari comparison template architecture is frozen. Exceptions are not improvements — they are acknowledged risks that have been evaluated and approved on specific grounds. This registry documents every exception, its justification, and the constraints that prevent it from becoming a template for further drift.

A registered exception is not an invitation to repeat. It is a named deviation with defined boundaries.

---

## How to Use This Registry

**Before adding a UI element that violates a template rule:**

1. Identify which rule is being violated (cite section and item from `comparison_template_v1.md` or `mobile_geometry_checklist_v1.md`)
2. State the consumer need that cannot be met without the exception
3. State why no in-template solution exists
4. Define the exact constraints that prevent the exception from multiplying
5. Submit for registry approval before shipping

If you cannot answer all four questions, the exception is not ready. Build the in-template solution instead.

---

## Active Exceptions

### EXCEPTION-001 — Bread Fermentation Filter Tooltip

**Status:** Approved  
**Category:** לחם (Bread)  
**Date approved:** 2026-05-28  
**Rule violated:** UI Stabilization Sprint 1 — "no tooltips on any UI element except EXCEPTION-001" (which this entry defines)

---

**What it is:**

A ⓘ info icon placed beside the filter option "ללא מחמצת מזוהה" in the bread category filter panel. When tapped, it displays a brief explanation (1–2 sentences maximum) of what "ללא מחמצת מזוהה" means in plain language.

It does not appear on any product row, any ingredient list, any score chip, or any other UI element. It appears only on one specific filter label.

---

**Why it is allowed:**

The filter label "ללא מחמצת מזוהה" uses the word "מחמצת," which is printed on bread packaging by manufacturers as a consumer-facing claim. It is not internal framework vocabulary. The tooltip clarifies a filter option whose words are already in use on product labels — the consumer who buys bread has already seen this word.

The need arises because a consumer may tap the filter and not understand why a bread with "שאור" in its name appears in the "ללא מחמצת מזוהה" filter. The tooltip explains that the filter reflects what was detectable in the ingredient list — not the packaging claim. This is a verification statement, not a framework disclosure.

---

**Why it does not violate the ontology-leakage policy:**

The ontology-leakage policy prohibits surfacing internal framework concepts in consumer language. The concepts at risk are: NOVA, BSIP, cap values, routing logic, structural classes, and analytical methodology.

This tooltip explains none of those. It explains the gap between a label claim and an ingredient-list signal, using words the consumer already knows: מחמצת (from packaging), שמרים (from packaging), רשימת הרכיבים (universally understood). No internal scoring variable, weight constant, or framework class is mentioned or implied.

Test: A consumer reading this tooltip learns that some breads say "שאור" on the front but use industrial yeast in the ingredients. That is a shelf observation, not a framework disclosure.

---

**Constraints preventing multiplication:**

1. **This is the only tooltip in the product.** No other filter option, score chip, ingredient item, product name, or UI element may carry a tooltip. A second tooltip anywhere in the product — regardless of category — constitutes a drift event requiring registry review and explicit re-approval.

2. **The tooltip text is fixed and reviewed.** It may not be updated without editorial review. It is not dynamically generated.

3. **Scope is bread only.** This exception was approved because מחמצת is a consumer-visible claim specific to the bread category. Other categories may not use this exception as a precedent. If מעדנים or חלב requires a tooltip, a new registry entry must be written and approved — it cannot inherit this approval.

4. **Filter context only.** The tooltip is permitted only on the filter label. If any developer or designer places a ⓘ icon on a product row, score chip, or ingredient text, it is an unauthorized exception regardless of content.

---

**Approved text (Hebrew):**

> "מחמצת לא זוהתה ברשימת הרכיבים. המוצר עשוי לציין שאור על האריזה."

Maximum 2 sentences. No additional explanation.

---

## Rejected Exception Requests

*None yet. This section will log exception requests that were reviewed and denied, with rationale, so future contributors understand the boundaries.*

---

## Governance

### Approval process

1. Write a proposed entry following the format above
2. Answer all four required questions (rule violated, consumer need, no in-template solution, multiplication constraints)
3. Present for editorial review — approved additions are merged into this registry and the relevant UI spec is updated to reference EXCEPTION-[N]
4. Unapproved exceptions shipped to production are architecture violations, not judgment calls

### Registry maintenance

- Exceptions are reviewed at each major category launch
- If an exception's consumer need disappears (e.g., bread changes its filter label), the exception is retired and the tooltip removed
- Retired exceptions remain in this document under a "Retired" section for historical reference

### The drift test

Before adding an exception, ask: if ten other teams in ten other categories saw this exception, would it spread into something that mutates the architecture? If yes, the exception is not narrow enough. Tighten the constraints or abandon the exception.

---

*This registry is governed by the same editorial authority as `comparison_template_v1.md`. Architecture rules in the template take precedence over any exception not documented here.*
