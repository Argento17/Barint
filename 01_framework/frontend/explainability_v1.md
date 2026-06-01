# Bari Universal Explainability System — v1
**Date:** 2026-05-27
**Status:** Canonical. Applies to all categories, all contexts, all consumer-facing outputs.
**Supersedes:** Any prior per-category explanation patterns.
**Does not supersede:** governance_v1.md (constitutional layer — always wins).

---

## What This Document Is

This is the interpretability infrastructure layer. It governs how Bari surfaces reasoning to consumers — what gets explained, in what order, at what density, in what language.

This document does NOT define scoring logic. It defines how to communicate what the scoring found, at the right level of abstraction, without exposing the system that computed it.

---

## The Core Distinction (Read This First)

**We are not explaining:** how the algorithm calculated 61.

**We are explaining:** what materially separated this product on the shelf.

These are not the same thing. The first is a system disclosure. The second is a shelf investigation.

Every explainability decision in this document flows from this distinction.

---

# PART 1 — PHILOSOPHY

---

## 1.1 What Explainability Is For

Consumers feel the score is mysterious when they cannot connect it to something they could have seen themselves in the product. The explanation system exists to bridge that gap — not by revealing algorithm logic, but by naming the observable composition pattern that drove the interpretation.

A good explanation makes the reader feel: "I could have noticed that if I knew what to look for."

A bad explanation makes the reader feel: "This score came from a calculation I don't understand."

---

## 1.2 What Explainability Is Not For

Explainability is NOT a vehicle for:
- Disclosing internal scoring weights
- Teaching nutrition science
- Making health recommendations
- Revealing algorithm architecture
- Attributing manufacturer intent
- Generating emotional response

If an explanation does any of these, it has left the explainability system and entered forbidden territory.

---

## 1.3 The Shelf Investigation Frame

Every explanation should feel like it comes from someone who looked at the shelf carefully, not from someone who ran a calculation. The framing is always:

> "What a careful reader of the ingredient list would have noticed."

Not:
> "What our system computed from the ingredients."

This is not dishonest — it is the correct level of abstraction. Bari's system is designed to formalize what careful shelf reading reveals. The explanation describes the shelf finding, not the formalization process.

---

## 1.4 The Three Explainability Principles

### Principle 1 — Shape Over Mechanics
Explain the SHAPE of the finding (what patterns emerged, how products diverged), not the MECHANICS of the score (which field had which weight, which rule fired).

### Principle 2 — Pattern Over Ingredient
Explain COMPOSITIONAL PATTERNS, not individual ingredients. An ingredient is evidence of a pattern. The pattern is the explanation.

- NOT: "Contains yeast."
- YES: "Fermentation signals were mixed — commercial yeast appeared before sourdough culture."

### Principle 3 — Calibrated Density
Explain as much as creates understanding, and no more. Explanations that say too much create cognitive overload, framework visibility, and implied precision that doesn't exist.

---

# PART 2 — SIGNAL HIERARCHY SYSTEM

---

## 2.1 Four-Tier Hierarchy

Not all signals deserve equal visibility. The hierarchy governs what surfaces where.

---

### Tier 1 — Shelf-Level Signals

**Definition:** Compositional patterns that separate product categories — the kind of finding a category map visualizes. These are the most consumer-readable signals.

**Rule:** Always surface Tier 1 when dominant. These appear in InsightCards, ShelfStatBar, and article headlines.

**Examples by category:**

| Category | Tier 1 Signals |
|----------|----------------|
| Bread | Grain verification status · Fermentation alignment · Ingredient transparency |
| Snack Bars | Processing depth (NOVA tier) · Structural base type · Sweetener source count |
| Milk | Processing depth · Stabilizer presence · Ingredient list length |

---

### Tier 2 — Composition Signals

**Definition:** Specific compositional observations that become visible when they materially shaped interpretation. These appear in CompositionBreakdown sections and product-level summaries.

**Rule:** Surface Tier 2 when it was a dominant driver OR meaningfully distinguishes two products. Do not surface Tier 2 signals that merely confirm what Tier 1 already established.

**Examples by category:**

| Category | Tier 2 Signals |
|----------|----------------|
| Bread | Fiber source (grain vs. added) · Ingredient list length · Whole grain qualifier presence |
| Snack Bars | Specific additive count · Sweetener architecture (stacking) · Base ingredient identity |
| Milk | Specific stabilizer count · Emulsifier type · Processing steps |

---

### Tier 3 — Supporting Signals

**Definition:** Signals that reinforce Tier 1/2 findings but do not stand alone as explanations. These appear in expanded views and product detail drawers.

**Rule:** Surface Tier 3 only in expanded views and only when they add information not already captured by Tier 1/2. Never use Tier 3 signals as primary explanations.

**Examples:**
- Specific ingredient names (e.g., "אינולין" as fiber source — supports Tier 2 fiber laundering signal)
- Ingredient count (supports Tier 1 simplicity signal)
- Individual cap trigger names (supports Tier 1 processing depth signal)

---

### Tier 4 — System Signals (Never Consumer-Facing)

**Definition:** Internal algorithm constructs that exist in the scoring system but have no consumer-readable meaning.

**Rule:** These NEVER appear in consumer-facing copy, tooltips, article text, or any visible product explanation.

**Forbidden Tier 4 exposures:**
- Score weight percentages (e.g., "this dimension is worth 15%")
- Field names (e.g., `whole_grain`, `fermentation_real`, `fiber_laundering`)
- Cap mechanism names (e.g., `SNACK_BAR_RED_SUGAR_LABEL`)
- GSS score values
- FQC values
- Structural class letter assignments (A/B/C/D/E/F)
- BSIP pipeline stage names
- Archetype names (e.g., "Mechanism Mismatch", "Halo Product")
- NOVA confidence values (e.g., "NOVA proxy: 0.73 confidence")

---

## 2.2 The 80/20 Visibility Rule

Only surface what explains 80% of the interpretation. The remaining 20% of signals — the marginal effects, the weak confirmers, the low-confidence patterns — do not appear in consumer-facing explanations.

If more than three signals are contributing to an explanation, group the convergent ones into a single pattern observation.

---

## 2.3 Convergent Signal Consolidation

When multiple signals point in the same direction, describe them as ONE pattern. Do not list them separately.

**Example:**
- `whole_grain=true` + `fiber_source=matrix` + `ingredient_position=1`

These three signals converge. The explanation is not three bullets. It is one sentence:
> "קמח שיפון מלא ראשון ברשימה — בסיס דגן מאומת עם סיבים מהדגן."

**Rule:** When signals converge, name the pattern. When signals diverge, name the tension.

---

# PART 3 — DOMINANT DRIVER FRAMEWORK

---

## 3.1 What Makes a Signal "Dominant"

A signal is dominant when it shaped the CATEGORY of interpretation (the grade tier), not merely the position within a grade tier.

**Test:** If removing this signal would change the grade (e.g., from C to D), it is dominant. If it would only shift the score by 3 points within the same grade, it is supporting.

---

## 3.2 The Anti-Attribution Rules

These are the most important rules in this framework.

**Rule 1 — No Single-Ingredient Causation**
Never frame an explanation as "ingredient X caused the score." Ingredients are evidence of patterns. Patterns are explanations.

| ✗ Wrong | ✓ Right |
|---------|---------|
| שמרים גרמו לציון נמוך | אות התסיסה היה מעורב — שמרים מופיעים לפני מחמצת |
| אינולין הוריד את הציון | הסיבים הגיעו ממקורות מוספים (אינולין) — לא מהדגן |
| קמח לבן גרם לציון D | בסיס המוצר הוא קמח לבן, לא דגן מלא |

**Rule 2 — Maximum Two Dominant Drivers**
More than two dominant drivers creates an enumeration, not an explanation. If three things matter equally, find the compositional pattern connecting them and name the pattern.

**Rule 3 — Direction Before Ingredient**
Always name the direction of the finding before naming the evidence.

| ✗ Wrong | ✓ Right |
|---------|---------|
| מכיל אינולין, שורש עולש | הסיבים מגיעים ממקורות מוספים — אינולין, שורש עולש |
| ציינו "מחמצת" בשם | שמרים תעשייתיים מופיעים ברשימה לפני המחמצת |

**Rule 4 — Process Over Presence**
For processing signals, name the process pattern, not the ingredient presence.

| ✗ Wrong | ✓ Right |
|---------|---------|
| מכיל מייצבים, מתחלבים, גלוטמט | מבנה הרכיבים כולל מייצבים ומתחלבים — רמת עיבוד גבוהה |
| NOVA4 | עיבוד תעשייתי גבוה — רכיבים שלא ניתן להכין בבית |

---

## 3.3 The Dominant Driver Template

When displaying a dominant driver in any consumer-facing context, use this structure:

```
[Compositional pattern observed] — [what this represents on the shelf]
```

**Examples:**
> "קמח שיפון מלא ראשון ברשימה — הבסיס הוא הדגן עצמו."
> "שמרים תעשייתיים לפני מחמצת — התסיסה לא ניתנת לאימות כעיקרית."
> "עיבוד תעשייתי גבוה — רכיבים שלא ניתן להכין בבית מופיעים ברשימה."
> "מרובה מקורות סוכר מוספים — שלושה סוגי סוכר מצוינים ברשימה."

---

## 3.4 Dominant Driver Per Grade Zone

Different grade zones have characteristic dominant patterns. These are not the only patterns, but they are the most common:

| Grade Zone | Most Common Dominant Pattern |
|------------|------------------------------|
| A | Multiple dimensions aligned — grain, transparency, composition |
| B | One strong dimension + minor limitations |
| C | Mixed signals — one dimension aligned, another less so |
| D | Recurring gap — processing or alignment limitations dominate |
| E | Multiple cap triggers — processing depth + sweetener architecture together |

---

# PART 4 — THE "WHY THIS LANDED HERE" SYSTEM

---

## 4.1 The Three-Section Pattern

This is Bari's core product-level explanation structure. It works at two disclosure levels:

**Short form** (always visible): Section 1 only — one sentence.
**Expanded form** (on tap/click): All three sections — 3–5 sentences total.

---

### Section 1 — מה שבלט

**Always present. One sentence maximum.**

The dominant compositional observation. Uses Tier 1 or Tier 2 signal language. States what stood out from the ingredient composition — the pattern that was most distinctive on this shelf.

**Template:** "[Observation] — [what this represents]."

**Bread examples:**
> "קמח שיפון מלא מצוין ראשון ברשימה — הבסיס הוא הדגן."
> "שמרים תעשייתיים מופיעים לפני המחמצת — התסיסה לא ניתנת לאימות כמנגנון הדומיננטי."
> "סיבים מגיעים מאינולין — לא מהדגן."

**Snack bar examples:**
> "תמרים הם הרכיב הראשון ברשימה — בסיס שלם, עיבוד מינימלי."
> "עיבוד תעשייתי גבוה — מרובה תוספות פונקציונליות ברשימה."
> "שלושה מקורות סוכר מוספים ברשימה."

**Milk examples:**
> "שלושה מייצבים ברשימת הרכיבים."
> "שני מרכיבים: חלב ותרבית חיידקים — רשימה קצרה מאוד."

---

### Section 2 — מה שהגביל

**Present only when a cap or limiting condition materially shaped interpretation. One to two sentences.**

What bounded or weakened the interpretation. This is NOT an apology for the score. It is a factual observation about a compositional limitation.

**Template:** "[Condition] — [why it shaped interpretation]."

**Examples:**
> "ריבוי מקורות סוכר מוספים הגביל את טווח הציון האפשרי."
> "הרכב כולל גם שמרים וגם מחמצת — לא ניתן לאמת מה דומיננטי."
> "סיבים גבוהים בלוח — אך מקורם ממוסף, לא מהדגן."

**Forbidden in Section 2:**
- Score numbers ("הציון הוגבל ל-55")
- Cap rule names ("RED_SUGAR_LABEL fired")
- Algorithm references ("הניקוד נחתך על ידי...")
- Apologetic framing ("לצערנו, המידע לא מספיק")

---

### Section 3 — מה שלא ניתן לאמת

**Present only when a meaningful data gap affected interpretation. One sentence.**

What Bari could not confirm from available data. Matter-of-fact. Not apologetic.

**Template:** "[What was unclear] — [what Bari couldn't confirm from the available data]."

**Examples:**
> "רשימת הרכיבים לא הייתה זמינה לציבור — הניתוח לא בוצע."
> "לוח התזונה לא היה זמין — הניתוח מבוסס על רשימת הרכיבים בלבד."
> "ה-[X] מצוין ברשימה ללא פירוט — לא ניתן לאמת את [Y]."

**Rules:**
- Section 3 appears only when the data gap affected the score or interpretation
- Section 3 never appears alongside a "completed" high-confidence analysis
- Section 3 is not an excuse for a low score — it documents a factual gap

---

## 4.2 The "Why This Landed Here" Display Rules

| Context | Sections Shown | Max Length |
|---------|---------------|------------|
| Product card (article) | Section 1 only | 1 sentence |
| Comparison table row | Section 1 only | 1 sentence |
| Product comparison explanation | Sections 1 + 2 | 2–3 sentences |
| Product detail drawer/page | All three sections | 3–5 sentences |
| Tooltip | Section 1 (shortened) | 8–12 words |
| InsightCard | Sections 1 + 2 | 2 sentences |
| Article prose (inline) | Woven naturally — not section structure | N/A |

---

# PART 5 — CATEGORY-NATIVE TRANSLATION SYSTEMS

---

## 5.1 Why Category-Native Translation Is Required

The same underlying data signal should produce different consumer-facing language depending on category context. A bread explanation sounds like bread shelf investigation. A snack bar explanation sounds like snack bar composition contrast.

Importing vocabulary across categories is a failure mode. "NOVA4" belongs in snack bar explanations. "מחמצת" belongs in bread explanations. Neither belongs in milk explanations.

---

## 5.2 Bread — Translation System

### Dominant Signal Language

| Data signal | Bread consumer language |
|-------------|------------------------|
| whole_grain=true + position 1 | "קמח [X] מלא מצוין ראשון ברשימה" |
| whole_grain=true + position >1 | "קמח מלא מופיע ברשימה — לא כרכיב ראשון" |
| whole_grain=false | "הקמח המלא לא מאומת כרכיב ראשון" |
| fermentation_real=true | "מחמצת מצוינת לפני השמרים ברשימה" |
| fermentation_mismatch=true | "שמרים תעשייתיים מופיעים לפני המחמצת ברשימה" |
| fermentation_mismatch=false, no claim | "ללא תביעת תסיסה — ברי לא בדקה מחמצת" |
| fiber_laundering=true | "הסיבים מגיעים ממקורות מוספים — לא מהדגן" |
| fiber_source=matrix | "הסיבים מגיעים מהדגן עצמו" |
| seed_halo=true | "הזרעים מופיעים על גבי בסיס מעובד" |
| confidence=insufficient | "רשימת הרכיבים לא הייתה זמינה לציבור" |
| confidence=partial | "הניתוח מבוסס על רשימת הרכיבים בלבד — לוח התזונה לא היה זמין" |

### Tone Target: Shelf Decoding

Bread explanations feel like someone examining label text on a supermarket shelf. They name ingredient positions, qualifiers, and order. They do not use processing language (that's snack bar language).

### Bread Forbidden Translations

| Wrong | Why wrong |
|-------|-----------|
| "מנגנון ההתפחה" | Framework term — "מה שמתפיח" is the consumer equivalent |
| "מטריצת הדגן" | Internal construct — "הדגן עצמו" |
| "fiber laundering" | English internal term — "סיבים ממקורות מוספים" |
| "GSS" | System signal — never surface |
| "ניתוח שמרני" | Reveals scoring conservatism — say what was found instead |

---

## 5.3 Snack Bars — Translation System

### Dominant Signal Language

| Data signal | Snack bar consumer language |
|-------------|---------------------------|
| nova_proxy=2 | "עיבוד מינימלי — רכיבים מזוהים" |
| nova_proxy=3 | "עיבוד בינוני — מרכיבים מוכרים, מספר תוספות" |
| nova_proxy=4 | "עיבוד תעשייתי גבוה — רכיבים שלא ניתן להכין בבית" |
| base=whole_food (dates/nuts) | "תמרים / אגוזים — בסיס שלם כרכיב ראשון" |
| base=refined_cereal | "בסיס קמח מעובד — [קמח/סירופ] ראשון ברשימה" |
| multiple_sweeteners=true | "מרובה מקורות סוכר מוספים — [N] סוגים ברשימה" |
| additive_count=low (0–2) | "רשימת רכיבים קצרה — מעט תוספות" |
| additive_count=high (5+) | "מספר גבוה של תוספות פונקציונליות" |
| protein_claim + nova4 | "תביעת פרוטאין — עיבוד תעשייתי גבוה מגביל את הטווח" |
| hyper_palatable=true | "הנדסת טעם מורכבת — מרובה ממתיקים ותוספות" |
| name_composition_gap=large | "הציון מבוסס על רשימת הרכיבים — לא על שם המוצר" |
| confidence=insufficient | "נתוני הרכיבים לא היו זמינים לניתוח" |

### Tone Target: Investigative Contrast

Snack bar explanations feel like a comparison between what the shelf promises and what the ingredient list reveals. They use processing language, structural language, and sweetener architecture language.

### Snack Bar Forbidden Translations

| Wrong | Why wrong |
|-------|-----------|
| "אולטרה-מעובד" | English-adjacent, slightly value-laden — "עיבוד תעשייתי גבוה" |
| "מזוקק" | Chemistry term — not shelf language |
| "ארכיטקטורה" | Framework visible — use "מבנה" or describe it |
| "whole food matrix" | English internal term |
| "NOVA" as an explanation | NOVA is a categorization, not an explanation — explain what NOVA4 means |

---

## 5.4 Milk — Translation System

### Dominant Signal Language

| Data signal | Milk consumer language |
|-------------|----------------------|
| stabilizer_count=0 | "ללא מייצבים ברשימת הרכיבים" |
| stabilizer_count=1–2 | "מייצב אחד-שניים ברשימה" |
| stabilizer_count=3+ | "שלושה מייצבים ומעלה ברשימה" |
| emulsifier_presence=true | "מכיל מתחלבים ברשימת הרכיבים" |
| processing_depth=minimal | "רשימה קצרה — מרכיבים בסיסיים" |
| processing_depth=high | "רשימה ארוכה — מרובה רכיבים תעשייתיים" |
| ingredient_count_low (≤3) | "שניים-שלושה רכיבים בלבד" |
| ingredient_count_high | "מרובה רכיבים — [N] ברשימה" |
| fat_source=natural | "שומן מהמוצר עצמו" |
| confidence=partial | "הניתוח מבוסס על רשימת הרכיבים — נתוני תזונה לא היו זמינים" |

### Tone Target: Processing Interpretation

Milk explanations feel like reading the ingredient list next to a standard expectation. They focus on what's added vs. what's native, and how many processing steps are visible in the list.

---

# PART 6 — UNCERTAINTY UX FRAMEWORK

---

## 6.1 The Uncertainty Principle

Uncertainty is information, not failure.

When Bari cannot verify something, that is a finding — about data availability, about label transparency, about what the product discloses to the public. It is not a malfunction.

The tone for all uncertainty is: calm, investigative, matter-of-fact.

The tone NEVER is: apologetic, error-like, timid.

---

## 6.2 The Four Uncertainty Types

---

### Type 1 — שקיפות חסרה (Data Unavailable)

**What happened:** The product's ingredient list was not publicly accessible. Bari did not score this product.

**Consumer display:** "לא נוקד — רשימת הרכיבים לא הייתה זמינה לציבור."

**Visual treatment:** Confidence badge: `ניתוח לא בוצע` (not a score)

**In article context:** "~46% מהמדף לא קיבלו ציון — הנתונים לא היו זמינים לציבור."

**Never:**
- "נתונים חסרים" (sounds like system error)
- "לא הצלחנו לנתח" (apologetic)
- "שגיאת נתונים" (wrong register)

---

### Type 2 — אימות מוגבל (Limited Verification)

**What happened:** Bari has partial data — ingredient list but not nutrition panel, or ingredient present but depth unconfirmable.

**Consumer display:** "ניתוח חלקי — מבוסס על רשימת הרכיבים בלבד."

**Visual treatment:** Confidence badge: `ניתוח חלקי`

**In product context:** "לוח התזונה לא היה זמין — הניתוח מבוסס על רשימת הרכיבים בלבד."

**Never:**
- "ניתוח חלקי בלבד" ("בלבד" = apologetic minimization)
- "קצת ניתחנו" (imprecise)
- "ניסינו אבל..." (failure framing)

---

### Type 3 — אות עמום (Ambiguous Signal)

**What happened:** A signal exists in the ingredient list but its interpretation is ambiguous. Example: "כוסמין" without "מלא" qualifier — Bari cannot verify whether it is whole grain.

**Consumer display:** Handle inline. No special badge.

**In product context:** "[X] מצוין ברשימה — ברי אינה יכולה לאמת [Y] בהיעדר [qualifier]."

**Template:** "ה-[X] מצוין ברשימה ללא קידומת 'מלא' — ברי לא מאמתת כוסמין מלא במקרה זה."

**Never:**
- "אולי יש כוסמין מלא" (speculation)
- "ייתכן ש..." (epistemic weakness)
- "אנחנו לא בטוחים" (first-person doubt)

---

### Type 4 — נתוני תזונה חסרים (Nutrition Panel Gap)

**What happened:** Ingredient list available, but nutrition panel was not — limiting full analysis.

**Consumer display:** "ניתוח חלקי — לוח התזונה לא היה זמין."

**Visual treatment:** Same badge as Type 2: `ניתוח חלקי`

**In article context:** "~36% מהמוצרים נותחו על בסיס רשימת הרכיבים בלבד — לוח התזונה לא היה זמין."

---

## 6.3 Universal Uncertainty Phrase Rules

**Always present:**
- "לא ניתן לאמת" — for ambiguous signals
- "לא היה זמין לציבור" — for missing public data
- "מבוסס על [X] בלבד" — for partial analysis

**Never use:**
- "ייתכן" / "אולי" (speculation)
- "נסינו" / "לא הצלחנו" (effort-apology)
- "חסר" alone without explanation of what's missing and why
- "לא ידוע" (vague and passive)
- "בגלל מגבלות" (sounds like a system excuse)

---

# PART 7 — EXPLAINABILITY DENSITY RULES

---

## 7.1 The Overload Test

An explanation fails the overload test if:
- It names more than three compositional signals
- It explains the score's calculation
- It surfaces Tier 4 system signals
- It requires the reader to understand a prior technical concept to parse it
- Reading it feels like reading a nutrition report

---

## 7.2 Maximum Signal Count by Context

| Context | Max signals in explanation |
|---------|--------------------------|
| Tooltip | 1 signal |
| Product card (article) | 1 signal |
| Comparison table row | 1 signal per product |
| InsightCard | 1–2 signals |
| Product comparison explanation | 2 signals |
| "Why This Landed Here" (expanded) | 3 signals total (across all three sections) |
| Product detail page | 5 signals max (across all sections) |

**Rule:** If you need more than 3 signals to explain a product, consolidate convergent signals into patterns.

---

## 7.3 Progressive Disclosure Architecture

This is the core UX pattern for managing density:

```
Level 1 — Always visible:
  Score + Grade + Single-line dominant driver

Level 2 — On tap/hover:
  "Why This Landed Here" Section 1 + 2 (if applicable)
  2–3 sentences

Level 3 — Dedicated detail view:
  Full "Why This Landed Here" (all sections)
  Supporting signal list
  Data transparency statement

Level 4 — Comparison drawer:
  Side-by-side signal comparison
  Divergence explanation
  Shared context statement
```

---

## 7.4 Context-Specific Density Rules

### In Articles (Editorial Context)

- Explanation is WOVEN INTO PROSE — not structured as "Section 1, Section 2"
- Products appear as evidence of patterns — their explanation is implicit in the article narrative
- Explicit "why" explanations appear only in comparison pairs and InsightCards
- Articles do not repeat product explanations that the map and CompositionBreakdown already established

### In Comparison Tables

- One signal per product per row — the explanation of WHY they differ goes in the comparison explanation paragraph below the table
- Never include explanation text inside the table cells

### In Product Pages

- Full three-section "Why This Landed Here"
- Supporting signal list (Tier 2–3 signals)
- Confidence badge
- Data source statement

### In Full Comparison Engine (all-products table)

- Score + Grade + single dominant signal tag only
- Hover reveals Level 2 explanation
- No inline prose explanations in the table rows

---

# PART 8 — COMPARISON EXPLAINABILITY SYSTEM

---

## 8.1 Core Philosophy

Comparison explanations explain THE STRUCTURE OF DIVERGENCE — not individual differences.

Users currently leave comparisons thinking "product A lost points because of yeast" when the correct understanding is "the products diverged in fermentation alignment, ingredient order, and fiber structure."

The explanation names the axis of difference, not the ingredient that represented it.

---

## 8.2 The Three Comparison Patterns

---

### Pattern A — Same Category, Different Depth

Both products look like they belong to the same shelf type but have different processing depth.

**Frame:** "שני [category type]. [Signal 1] שונה. [Signal 2] שונה. ציון: [gap]."

**Example:**
> "שני חטיפי שיבולת שועל. עיבוד: NOVA3 מול NOVA4. מספר תוספות: שניים מול שישה. הפרש: 36 נקודות."

---

### Pattern B — Same Presentation, Different Base

Both products present identically (same category claim, similar packaging theme) but have different structural bases.

**Frame:** "שניהם [presented as X]. הבסיס שונה: [Product A] — [base A]. [Product B] — [base B]. הפרש: [N] נקודות."

**Example:**
> "שניהם בציפוי שוקולד. הבסיס שונה: חטיף התמרים — תמרים, NOVA2. פיטנס גרנולה — קמח ו-סירופ, NOVA4. הפרש: 39 נקודות."

---

### Pattern C — Same Positioning Claim, Different Composition

Both products carry the same positioning signal (both claim sourdough, both claim whole grain, both claim "natural") but the ingredient list tells different stories.

**Frame:** "שניהם [claim]. אבל: [Product A] — [observation A]. [Product B] — [observation B]. הציון שיקף את רשימת הרכיבים."

**Example:**
> "שניהם עם 'מחמצת' בשם. אבל: לחם שיפון קל — מחמצת לפני שמרים ברשימה. לחם מחמצת שיפון — שמרים לפני מחמצת. הציון: 75 מול 74."

---

## 8.3 The Multi-Factor Rule

When explaining a score gap larger than 10 points, always name at least TWO compositional dimensions. A single-factor explanation for a large gap creates the illusion that one thing "caused" the score.

**Gap ≤5 points:** One factor is sufficient.
**Gap 6–15 points:** Two factors required.
**Gap >15 points:** Two factors + a connecting observation.

---

## 8.4 The Convergence Statement

For comparison pairs where signals align in the same direction across both products, add a convergence statement:

> "בשני המקרים, [X] והציון תואמים — הכיוון ברור."

For pairs where signals diverge:

> "הפרש הציון נובע מ-[dimension 1] ו-[dimension 2] — שניהם הלכו בכיוונים שונים."

---

## 8.5 Comparison Forbidden Patterns

| Wrong | Why wrong |
|-------|-----------|
| "[Ingredient] caused the score gap" | Attribution, not pattern |
| "Product A is better than Product B because..." | Recommendation framing |
| "The algorithm gave [N] points for [signal]" | Score mechanics disclosure |
| Listing 4+ differences | Cognitive overload |
| "Both are equivalent" (when they're not) | False symmetry |
| Comparing scores without explaining the dimension | Score-only is not explanation |

---

# PART 9 — MOBILE EXPLAINABILITY STRATEGY

---

## 9.1 Mobile Constraints

Mobile explainability must solve: small screen + limited attention + touch interaction.

The core mobile rule: **Progressive revelation over comprehensive display.**

On mobile, the user sees less by default and reveals more by choosing. No explanation should feel overwhelming on a 6-inch screen.

---

## 9.2 Mobile Disclosure Levels

| Level | Trigger | Content | Max words |
|-------|---------|---------|-----------|
| 0 — Score | Default | Score + Grade only | — |
| 1 — Pulse | Automatic on product view | Score + Grade + 1 dominant signal | 12 |
| 2 — Tap | User taps signal | "Why This Landed Here" Level 2 | 40 |
| 3 — Detail | User taps "full explanation" | All three sections | 80 |

---

## 9.3 Mobile Forbidden Patterns

- Side-by-side comparison tables (collapse to stacked rows)
- Lists longer than 3 items without progressive disclosure
- Inline technical terms without translation
- Explanation text inside table cells
- Score breakdowns showing per-dimension point values

---

## 9.4 Mobile Comparison Pattern

Desktop comparison: table + explanation paragraph.

Mobile comparison: stacked cards + swipe/tap to reveal explanation.

```
Card 1: [Product A] — Score + Grade + 1-line dominant signal
Card 2: [Product B] — Score + Grade + 1-line dominant signal
[Tap: "מה הפריד ביניהם?"]
→ 2-sentence comparison explanation
```

---

# PART 10 — APPROVED WORDING LIBRARY

---

## 10.1 Ingredient Position Language

```
מצוין ראשון ברשימה
מופיע ברשימה לפני [X]
מופיע ברשימה אחרי [X]
הרכיב הראשון הוא [X]
[X] כרכיב ראשון
[X] מצוין בין הרכיבים הראשונים
[X] מופיע מאוחר ברשימה
```

---

## 10.2 Processing Depth Language

```
עיבוד מינימלי — רכיבים מזוהים
עיבוד בינוני — מרכיבים מוכרים, מספר תוספות
עיבוד תעשייתי גבוה — רכיבים שלא ניתן להכין בבית
רשימה קצרה — [N] רכיבים עיקריים
רשימה ארוכה — מרובה רכיבים
מרובה תוספות פונקציונליות
```

---

## 10.3 Fermentation Language (Bread)

```
מחמצת מצוינת לפני השמרים ברשימה
שמרים תעשייתיים מופיעים לפני המחמצת ברשימה
לא ניתן לאמת שמחמצת היא מה שמתפיח את הלחם
מחמצת ברשימה — שמרים גם הם
ללא מחמצת ברשימת הרכיבים
```

---

## 10.4 Grain/Flour Language (Bread)

```
קמח [X] מלא מצוין ראשון ברשימה
"מלא" מצוין לצד שם הדגן
"מלא" אינו מצוין — ברי לא מאמתת
הקמח המלא מופיע אחרי קמח הלבן ברשימה
בסיס קמח לבן — קמח מלא מופיע לאחר מכן
```

---

## 10.5 Fiber Language

```
הסיבים מגיעים מהדגן עצמו
הסיבים מגיעים ממקורות מוספים ([X])
אינולין / שורש עולש / פסיליום מצוינים כמקור הסיבים
הסיבים לא מיוחסים לדגן ברשימה
```

---

## 10.6 Sweetener Language (Snack Bars)

```
[N] מקורות סוכר מוספים ברשימה
סירופ גלוקוז + סוכר + [X] — שלושה מקורות
מקור הסוכר הוא [תמרים / דבש / סירופ / סוכר]
ללא סוכר מוסף — [X] הוא מקור הסוכר
```

---

## 10.7 Uncertainty Language

```
לא ניתן לאמת [X]
ברי לא יכולה לאמת [X] כי [Y] אינו מצוין ברשימה
רשימת הרכיבים לא הייתה זמינה לציבור
הניתוח מבוסס על רשימת הרכיבים בלבד
לוח התזונה לא היה זמין
[X] מצוין ברשימה — ברי לא מאמתת [Y] בהיעדר [qualifier]
```

---

## 10.8 Comparison Language

```
שניהם [X] — הפרש: [N] נקודות
הבסיס שונה: [A] מול [B]
[Signal 1] ו-[Signal 2] הלכו בכיוונים שונים
הציון שיקף את [dimension], לא את [what the name implies]
שני [X] עם ציונים שונים — מה הפריד: [dimension]
```

---

# PART 11 — FORBIDDEN WORDING LIBRARY

---

## 11.1 Technical/Algorithmic Language (Never Use)

```
מנגנון
מטריצה
ארכיטקטורה (in consumer copy)
אינטגריטי
GSS / FQC / NOVA proxy (as explanation)
cap / floor (as explanation)
structural class
hyper-palatable
fiber laundering (English term)
fermentation_real / whole_grain / fiber_laundering (field names)
BSIP
```

---

## 11.2 Moral/Judgment Language (Never Use)

```
רעיל
מסוכן
לא בריא / בריא
נקי / מלוכלך
מזיק
טוב / רע (as a judgment about a product)
מרמה
לא אמיתי / אמיתי (when referring to manufacturer)
המוצר הטוב ביותר / הגרוע ביותר (recommendation framing)
```

---

## 11.3 Apologetic Language (Never Use)

```
לצערנו
לא הצלחנו
מגבלות הניתוח
ניסינו אבל...
המערכת לא יכולה
הנתונים לא מספיקים (apologetic framing — say what's missing instead)
בלבד (as a minimizer: "ניתוח חלקי בלבד" → "ניתוח חלקי")
```

---

## 11.4 Attributional Language (Never Use)

```
היצרן [action verb]
הם הוסיפו
מכוון
במטרה ל
כדי ל (when attributing intent to manufacturer)
הסתירו
```

---

## 11.5 Over-Precision Language (Never Use)

```
הציון נחתך ב-[X] נקודות בגלל [ingredient]
[ingredient] שווה [N] נקודות
מימד [X] הוריד ב-[Y]%
הציון חושב על פי [formula]
[N] נקודות ניתנו עבור [signal]
```

---

## 11.6 Framework-Visible Language (Never Use)

```
המסגרת האנליטית
מערכת הניקוד
שיטת הניתוח
הסכמה של ברי
כפי שברי מגדיר
על פי פרמטרי ברי
```

---

# PART 12 — CURSOR IMPLEMENTATION GUIDANCE

---

## 12.1 Component Library

The following components implement the explainability system. All new components. None exist in current system.

---

### `ExplainabilityPill`

**Purpose:** Single-line dominant signal. Always visible.
**Appears in:** Product cards (articles), comparison table rows, tooltip summary.

**Props:**
```typescript
{
  signal: string;           // Consumer-language signal text (Tier 1 or 2)
  category: "bread" | "snack_bars" | "milk" | "default";
  confidence: "verified" | "partial" | "insufficient";
}
```

**Rendering rules:**
- Max 12 words
- If confidence=insufficient: show "לא נוקד" pill instead, no signal text
- No score number inside this component — score lives in ScoreDisplay
- Font: small, secondary weight
- No border, no color coding

**Mobile:** Same component, no changes needed.

---

### `WhyThisLandedHere`

**Purpose:** The 3-section explanation block. Appears in product drawers and detail pages.

**Props:**
```typescript
{
  section1: string;          // Always present — dominant signal sentence
  section2?: string;         // Optional — limiting condition
  section3?: string;         // Optional — uncertainty statement
  category: Category;
  displayMode: "summary" | "full";
}
```

**Rendering rules:**
- `displayMode="summary"`: Section 1 only
- `displayMode="full"`: All present sections
- Each section: one paragraph, no section heading visible
- Sections are separated by line break, not headers
- Max 3 sentences per section (usually 1)
- If section2 and section3 are both null: render section1 only, no empty space

**Mobile:** Both modes available. Default to `summary` on mobile, `full` on detail view.

---

### `ComparisonExplainer`

**Purpose:** The WHY PRODUCTS DIVERGED explanation. Appears below comparison tables.

**Props:**
```typescript
{
  pattern: "same_category_different_depth" | "same_presentation_different_base" | "same_claim_different_composition";
  productA: {name: string; score: number; grade: string; signals: string[]};
  productB: {name: string; score: number; grade: string; signals: string[]};
  scoreDelta: number;
  explanationText: string;   // Hand-written by CE — not auto-generated
}
```

**Rendering rules:**
- Always prose paragraph — never a bullet list
- Never more than 3 sentences
- Score delta appears as `הפרש: [N] נקודות` not as judgment
- Both products are visually neutral — no winner/loser treatment
- `explanationText` is CE-authored, not computed from props

**Mobile:** Full display, same component. Collapses to shorter prose if scrolling is needed.

---

### `UncertaintyBadge`

**Purpose:** Confidence state indicator on any product that appears in any component.

**Props:**
```typescript
{
  type: "verified" | "partial" | "insufficient";
  label: string;   // "ניתוח מלא" | "ניתוח חלקי" | "ניתוח לא בוצע"
}
```

**Rendering rules:**
- Appears beside every product name in cards, tables, comparison pairs
- No color coding. Text only (or at most neutral gray border)
- `insufficient` type: show "לא נוקד" — suppress score display
- `partial` type: show "ניתוח חלקי" — show score with asterisk or note
- `verified` type: show "ניתוח מלא" — show score normally
- Never use green/amber/red color coding for confidence states

**Mobile:** Same component. Badge renders inline after product name.

---

### `ExpandableInsight`

**Purpose:** Progressive disclosure wrapper for any explanation content.

**Props:**
```typescript
{
  summary: string;           // Always visible — max 12 words
  expandedContent: ReactNode; // Hidden until expanded
  expandLabel: string;       // "מה הפריד" | "פרטים נוספים" | "ראה הסבר"
  collapseLabel: string;     // "סגור" | "הסתר"
  defaultExpanded?: boolean;
}
```

**Rendering rules:**
- Summary always visible — no toggle needed to see the top line
- Expand/collapse is for secondary content only
- Animation: simple fade/height, not dramatic
- Mobile: same behavior, touch-friendly tap area

---

### `SignalSummary`

**Purpose:** 2–3 factor summary block. Appears in InsightCards and product detail.

**Props:**
```typescript
{
  factors: Array<{
    label: string;     // Consumer-language signal label
    value: string;     // Observed value in consumer language
    tier: 1 | 2 | 3;  // Signal tier
  }>;
  maxFactors?: number;  // Default 3
}
```

**Rendering rules:**
- Renders only Tier 1 and Tier 2 signals
- Never more than 3 factors regardless of `factors` array length
- Each factor: one row, label and value side by side
- No per-factor score contribution numbers
- Mobile: single column, factors stack vertically

---

## 12.2 Data Feed Requirements

The following fields must be in the frontend dataset to feed the explainability components:

**All categories:**
```
name_he
score (when displayable)
grade (when displayable)
displayable: boolean
confidence_level: "verified" | "partial" | "insufficient"
confidence_label_he: string
short_summary_he: string       // Section 1 of WhyThisLandedHere — CE-authored
limiting_summary_he?: string   // Section 2 — CE-authored when applicable
uncertainty_summary_he?: string // Section 3 — CE-authored when applicable
dominant_signal_he: string     // ExplainabilityPill text — CE-authored
```

**Bread-specific:**
```
fermentation_real: boolean
fermentation_mismatch: boolean
whole_grain: boolean
fiber_laundering: boolean
ingredient_architecture_summary: string
```

**Snack bar-specific:**
```
nova_proxy: 1 | 2 | 3 | 4
structural_class: string
caps_applied: string[]
synth_score: number
```

**Milk-specific:**
```
stabilizer_count: number
emulsifier_presence: boolean
processing_depth: "minimal" | "moderate" | "high"
```

---

## 12.3 Article Integration Rules

**In article prose:** Explanation is woven into narrative. Do NOT use ExplainabilityPill or WhyThisLandedHere component tags inside article body text.

**In article InsightCards:** Use InsightCard component with `explanationText` prop. The card body doubles as an explanation — do NOT add a separate WhyThisLandedHere below each card.

**In article comparison pairs:** Use ComparisonExplainer below the comparison table. This is the ONLY place in articles where structured explanation appears.

**In article CompositionBreakdown / ThreeMisalignmentBreakdown:** These sections ARE the explanation layer — they serve the same function as WhyThisLandedHere but at category level. Do not add per-product explanation components inside these sections.

---

# PART 13 — BEFORE/AFTER EXAMPLES

---

## 13.1 Bread — Product-Level Explanation

**Before:**
> "הציון לא גבוה בגלל שמרים תעשייתיים שהם המחמיץ הראשי ברשימה."

**Problems:** "המחמיץ הראשי" is unusual construction, and the framing is negative causation (ingredient "caused" low score).

**After:**
> "שמרים תעשייתיים מופיעים ברשימה לפני המחמצת — התסיסה לא ניתנת לאימות כמה שמתפיח את הלחם בפועל."

---

## 13.2 Snack Bar — Comparison Explanation

**Before:**
> "לחמניות לס קיטו קיבלו ציון נמוך בגלל שמכילות אינולין."

**Problems:** Single ingredient causation. "בגלל ש-" = attribution frame.

**After:**
> "הסיבים מגיעים ממקורות מוספים — אינולין, לא מהדגן. לחם שיפון קל עם 12.4 גרם מהדגן עצמו קיבל ציון גבוה יותר ממוצר עם 17.4 גרם מאינולין. הציון שיקף את המקור, לא את המספר."

---

## 13.3 Uncertainty — Ingredient Not Available

**Before:**
> "לצערנו, לא הצלחנו לנתח מוצר זה כי הנתונים חסרים."

**Problems:** Apologetic, failure-framing, vague.

**After:**
> "לא נוקד — רשימת הרכיבים לא הייתה זמינה לציבור."

---

## 13.4 Score Mechanics — Forbidden Exposure

**Before:**
> "הציון חושב על פי חמישה ממדים: מיקום קמח (15%), מקור סיבים (20%), תסיסה (25%), שקיפות (20%), הרכב כללי (20%)."

**Problems:** Score mechanics disclosure. Consumer doesn't need weight percentages.

**After:**
> "קמח שיפון מלא ראשון ברשימה, מחמצת לפני שמרים, וסיבים מהדגן — הרכב עקבי בכמה ממדים."

---

## 13.5 Comparison — Multi-Factor

**Before:**
> "פיטנס קלאסי הוא NOVA4. לכן הציון נמוך."

**Problems:** Single factor (NOVA). "לכן" = causation. NOVA4 as an isolated explanation.

**After:**
> "פיטנס קלאסי: עיבוד תעשייתי גבוה, בסיס קמח מעובד, מרובה תוספות. חטיף התמרים: עיבוד מינימלי, 4 רכיבים, בסיס שלם. שני הגורמים — עומק עיבוד ומבנה הבסיס — הלכו בכיוונים שונים."

---

## 13.6 Dominant Driver — Before/After

**Before (too technical):**
> "הניתוח הצביע על fiber_laundering=true עם isolated fiber source."

**After:**
> "הסיבים מגיעים ממקורות מוספים — אינולין ושורש עולש — לא מהדגן."

---

# PART 14 — CROSS-CATEGORY UX PATTERNS

---

## 14.1 The ExplainabilityPill — Cross-Category Examples

| Category | Product type | Pill text |
|----------|-------------|-----------|
| Bread | Top scorer | "קמח שיפון מלא ראשון, מחמצת לפני שמרים" |
| Bread | Mismatch | "שמרים תעשייתיים לפני מחמצת" |
| Bread | Insufficient | "לא נוקד" |
| Snack Bars | Date bar | "תמרים ראשון ברשימה — עיבוד מינימלי" |
| Snack Bars | NOVA4 | "עיבוד תעשייתי גבוה — מרובה תוספות" |
| Snack Bars | Protein bar | "תביעת פרוטאין — עיבוד גבוה" |
| Milk | Minimal | "שני רכיבים — ללא מייצבים" |
| Milk | Processed | "שלושה מייצבים ברשימה" |

---

## 14.2 The WhyThisLandedHere — Cross-Category Examples

**Bread — High score:**
> **מה שבלט:** קמח שיפון מלא מצוין ראשון ברשימה — הבסיס הוא הדגן עצמו. מחמצת מצוינת לפני השמרים.
> **מה שהגביל:** —
> **מה שלא ניתן לאמת:** לוח התזונה לא היה זמין — הניתוח מבוסס על רשימת הרכיבים בלבד.

**Snack Bar — Date bar 70/B:**
> **מה שבלט:** תמרים הם הרכיב הראשון — בסיס שלם, ארבעה רכיבים, ללא סוכר מוסף.
> **מה שהגביל:** —
> **מה שלא ניתן לאמת:** —

**Snack Bar — Protein bar 47/D:**
> **מה שבלט:** עיבוד תעשייתי גבוה — מרובה רכיבים ותוספות פונקציונליות ברשימה.
> **מה שהגביל:** עיבוד תעשייתי גבוה הגביל את טווח הציון — תביעת הפרוטאין לא מקזזת.
> **מה שלא ניתן לאמת:** —

**Bread — Insufficient data:**
> **מה שבלט:** לא נוקד — רשימת הרכיבים לא הייתה זמינה לציבור.
> [Sections 2 and 3 suppressed — not applicable when product unscored]

---

## 14.3 The ComparisonExplainer — Cross-Category Examples

**Pattern A — Snack Bar:**
> "שני חטיפי שיבולת שועל. עיבוד שונה: Nature Valley Crunchy — NOVA3, שיבולת שועל שלמה כרכיב ראשון. פיטנס גרנולה — NOVA4, קמח ו-סירופ כרכיבים ראשונים. שני הגורמים — עומק העיבוד ומבנה הבסיס — הפרידו."

**Pattern B — Bread:**
> "שניהם לחמי שיפון. הפרש: 8 נקודות. שיפון קל: 12.4 גרם סיבים מהדגן + מחמצת ברשימה. שיפון עגול: 5.8 גרם + ללא מחמצת. כמות הסיבים והסיגנל התסיסה הלכו בכיוונים שונים."

**Pattern C — Bread fermentation:**
> "שניהם עם 'מחמצת' בשם. אבל: לחם שיפון קל — מחמצת לפני שמרים ברשימה. לחם מחמצת שיפון — שמרים לפני מחמצת. הציון: 75 מול 74. ההבדל — ביחס בין השם לרשימה, לא בציון."

---

# GOVERNANCE CHECKLIST — EXPLAINABILITY

Before publishing any consumer-facing explanation, verify:

- [ ] No Tier 4 signals exposed (field names, cap names, algorithm terms)
- [ ] No single-ingredient causation ("X caused the score")
- [ ] No manufacturer intent attribution
- [ ] No moral/judgment language
- [ ] No apologetic framing for uncertainty
- [ ] Max 3 signals in any single explanation block
- [ ] Multi-factor comparison rule: ≥2 dimensions for gaps >10 points
- [ ] Category-native language used (bread ≠ snack bar vocabulary)
- [ ] All uncertainty phrased as matter-of-fact information, not apology
- [ ] "Why This Landed Here" Section 1 present on all scored products
- [ ] Score mechanics not disclosed (no weight percentages, no point calculations)

---
