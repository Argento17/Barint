---
name: bari-explainability-v1
description: "Universal Explainability System v1 — cross-category interpretability infrastructure; 4-tier signal hierarchy; dominant driver anti-attribution rules; category-native translation for bread/snack bars/milk; 4 uncertainty types; 6 Cursor components; mobile 4-level disclosure; approved/forbidden wording libraries; governance checklist"
metadata:
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Built 2026-05-27. Master document at `C:\Bari\01_framework\frontend\explainability_v1.md`.
Applies cross-category to: milk, bread, snack bars, all future categories.

**Why:** Scores were perceived as mysterious/black-boxed; users attributed score causation to single ingredients; framework vocabulary (GSS, FQC, cap, structural class) was leaking into consumer copy; category vocabulary was crossing between unrelated categories.

**How to apply:** This governs every consumer-facing explanation written for any Bari category. All Cursor explainability components must implement these rules. The governance checklist (13 items) must pass before publication.

## Core Distinction

NOT explaining: "How the algorithm calculated 61."
IS explaining: "What materially separated this product on the shelf."

## 3 Core Principles

1. **Shape over mechanics** — describe the compositional pattern, not how it scored
2. **Pattern over ingredient** — no single ingredient caused the score; patterns caused it
3. **Calibrated density** — surface only signals that genuinely separated the product; suppress noise

## 4-Tier Signal Hierarchy

| Tier | What | Consumer-visible? |
|---|---|---|
| 1 | Shelf-level (NOVA, grade, confidence) | Always |
| 2 | Composition (dominant pattern driving score) | When dominant |
| 3 | Supporting (secondary nuance) | Expanded views only |
| 4 | System signals (GSS, FQC, cap names, BSIP, structural class, field names) | **NEVER** |

80/20 rule: Tier 1+2 signals account for 80%+ of consumer comprehension. Convergent signals: when 3+ signals point same direction, consolidate into one pattern statement.

## Dominant Driver Framework (Anti-Attribution)

4 rules:
1. **No single-ingredient causation** — "ingredient X caused score Y" is forbidden
2. **Direction before ingredient** — "עיבוד עמוק" before "18 תוספים"
3. **Process over presence** — "עיבוד תעשייתי" before "מכיל X"
4. **Max 2 dominant drivers** — if more qualify, consolidate into pattern

Template: "מה שבלט כאן היה [pattern], לא [single item]."

Per-grade patterns:
- B: whole food base, minimal processing, 1-2 ingredient sources
- C: mixed base, moderate processing, some additives but bounded
- D: engineered base OR multiple additive systems OR ultra-processing
- E: all three converge (engineered + ultra-processed + dense additives)

## "Why This Landed Here" — 3 Sections

| Section | Hebrew | When shown | Max words |
|---|---|---|---|
| 1 | מה שבלט | Always | 25 |
| 2 | מה שהגביל | When score <60 or confidence=partial | 20 |
| 3 | מה שלא ניתן לאמת | When confidence=partial/insufficient | 15 |

Display rules by context:
- Card view: Section 1 only
- Product page: Sections 1+2
- Full detail view: All 3 sections

## Category-Native Translation

**Bread** — vocabulary: מנה של שיפון/חיטה מלאה, מה שמתפיח, כמות הסיבים בדגן; tone: shelf decoding
**Snack bars** — vocabulary: בסיס שלם vs. מהונדס, ריכוז ממתיקים, עומס תוספות; tone: investigative contrast
**Milk** — vocabulary: רמת עיבוד, מייצבים/מתחלבים, תוספת שומן/סוכר; tone: processing interpretation

Vocabulary MUST NOT cross categories. Bread fermentation language never appears in snack bar copy.

## 4 Uncertainty Types

| Type | Phrase | Forbidden |
|---|---|---|
| Unverifiable claim | "לא ניתן לאמת מרשימת הרכיבים" | "ייתכן ש..." |
| Missing data | "לא היה זמין לציבור" | "נתונים חסרים" |
| Conflicting signals | "אינדיקטורים סותרים" (internal only) → "ההרכב לא עקבי" | "ייתכן בגלל ש..." |
| Structural limitation | describe limitation → "ברי מבוססת על רשימת הרכיבים בלבד" | "ניתוח שמרני" |

## Explainability Density Rules

Max signals by context: Card=1, Product page=2, Comparison=2 per product (4 total), Full detail=3, Mobile=1 (expandable to 2).

Progressive disclosure: Level 0 = score only → Level 1 = 1 dominant pattern → Level 2 = pattern + boundary condition → Level 3 = full WhyThisLandedHere.

## Comparison Explainability — 3 Patterns

1. Same category, different processing depth (NOVA gap) — lead with processing contrast
2. Same presentation, different compositional base — lead with base contrast
3. Same claim, different composition — lead with claim/reality gap
Multi-factor rule: gaps >10 points require ≥2 dimensions named. Single-factor attribution forbidden for large gaps.

## Mobile Strategy — 4 Disclosure Levels

- Level 0: score chip only (default collapsed)
- Level 1: one-line dominant signal (tap to expand)
- Level 2: WhyThisLandedHere Section 1+2 (in-card)
- Level 3: full detail view (separate screen, 80 words max)

Mobile forbidden: inline tables, multi-column comparisons, footnoted signals, >3 signals at once.

## 6 Cursor Components

1. `ExplainabilityPill` — inline score chip + 1 dominant signal
2. `WhyThisLandedHere` — 3-section disclosure component
3. `ComparisonExplainer` — 2-product contrast with pattern labels
4. `UncertaintyBadge` — confidence state display (verified/partial/insufficient)
5. `ExpandableInsight` — progressive disclosure container
6. `SignalSummary` — Tier 1+2 signals summary strip

## Forbidden Wording (Key Categories)

**Framework internals (never consumer-facing):** מנגנון, מטריצה, ארכיטקטורה, GSS, FQC, NOVA (as explanation mechanism), cap/floor (as explanation), structural class, hyper-palatable, fiber laundering, field names (ingredients_raw, nova_score, confidence_level)

**Analytical tone:** "הנגזרת מ...", "אינדיקטור", "בהתאם לפרמטרים", "מוצר זה הציג"

**Apologetic tone:** "לצערנו", "מוגבל ל...", "רק מבוסס על"

## Governance Checklist (13 items)

Pre-publication verification: No Tier 4 signals in copy; no single-ingredient causation; ≤2 dominant drivers; uncertainty stated as scope limit not apology; category vocabulary not crossed; no recommendations masked as observations; all uncertainty types use approved phrases; mobile shows ≤2 signals before expand; comparison gap >10 uses ≥2 dimensions; WhyThisLandedHere Section 3 only when confidence=partial/insufficient; no framework terms in any consumer-facing string; score explanation references pattern not algorithm; forbidden phrases library checked.

[[bari-editorial-intelligence-v1]]
[[bari-governance-v1]]
[[bari-assertive-writing-v1]]
[[bari-bread-blog-v3]]
[[bari-snack-bar-blog-v1]]
