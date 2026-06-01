# Bari Comparison Template — v1 (Stable)

**Status:** Canonical — applies to all Bari product categories  
**Date:** 2026-05-28  
**Replaces:** Per-category architectural improvisation  

---

## Core Principle

The user should feel:  
**"Someone carefully investigated this supermarket shelf for me."**

Not:  
"I am using food analytics software."

Everything in this document serves that distinction.

---

## 1. Page Structure

Four sections. In order. No additions.

```
[1] HERO
[2] PROLOGUE
[3] PRODUCT TABLE
[4] METHODOLOGY
```

No maps. No dashboards. No cluster visualizations. No insight systems. No decomposition panels. No glossary sections.

The product table is the main experience. Everything else is support.

---

## 2. Hero

**Purpose:** Create a moment of recognition. Connect the user to something they know from the shelf. Transition quickly into products.

**Rules:**

- One sentence. Maximum 12 words in Hebrew.
- The sentence names a real product and a real observation. It does not explain anything.
- Hero image: product packaging only. Clean background. Label visible. No food styling.
- Score visible immediately on load. No delayed reveal. No animation.
- Hero height: compact. Not full-screen. The table should be visible or nearly visible without scrolling.
- One product image maximum in the hero. Not a collage.

**What the hero is not:**

Not a thesis statement. Not a summary of findings. Not an invitation to a journey. Not a hook. It is a moment of orientation — "you are about to see products from this shelf."

**Example form (Hebrew):**

> "ב-95 מוצרים ממדף המעדנים של שופרסל, הגביע הכי מוכר מקבל את הציון הכי נמוך."

That is the entire hero text. Nothing more follows before the prologue.

---

## 3. Prologue

**Purpose:** Brief observational framing. Not education. Not philosophy. Not methodology.

**Rules:**

- 3–5 sentences. Hard limit.
- Calm declarative tone.
- Every sentence is a shelf observation that is verifiable from the data.
- No nutrition lecture. No framework language. No "here is how we score."
- No bullet points. No subheadings. Continuous prose only.
- Does not repeat the hero sentence.
- Does not preview the findings. It names what is on the shelf, not what to think about it.

**What the prologue is not:**

Not a summary of the category analysis. Not a list of contradictions. Not an editorial argument. It sets the room — quietly.

**Example form:**

> "מדף המעדנים של שופרסל כולל מוצרי חלב קלאסיים, אלטרנטיבות חלבון, ומוצרים שמציגים תוויות 'דיאט' ו'ללא סוכר'. בדקנו 95 מוצרים. לא כל מוצר שמרגיש בריא יותר מקבל ציון גבוה יותר."

That is a complete prologue. Two sentences is enough. Five sentences is the maximum.

---

## 4. Product Table

The product table is the page.

### 4a. Row — Collapsed State

Each row contains exactly:

| Element | Spec |
|---|---|
| Packaging image | 56px square, clean crop, label visible |
| Product name | Primary text, full Hebrew name |
| Score + grade | Single chip: "69 / B" — no color encoding |
| One-line insight | ≤12 Hebrew words, observational, no framework terms |
| Expand toggle | Chevron, right-aligned |

Nothing else in the collapsed row.

The one-line insight is not a score explanation. It is an observation about the product's position. Examples:

- "חלבון גבוה, רשימת רכיבים קצרה"
- "מוצר הדיאט עם יותר תוספים מהגרסה הרגילה"
- "הגביע המוכר ביותר בקטגוריה"

Do not write: "הציון נמוך בגלל עיבוד גבוה." Do not explain the score. Name what is observable.

### 4b. Row — Expanded State

Expanded on tap/click. Contains:

1. Nutrition facts — 5 fields only: calories / protein / sugar / fat / sodium (per 100g)
2. Ingredient list — verbatim from label, Hebrew, scrollable if long
3. Data note — one line: "נתונים נלקחו מ[שם קמעונאי]. ייתכנו שינויים בין מוצרים מאריזות שונות."
4. Confidence indicator — two states only: "נתונים מלאים" / "נתונים חלקיים"

Nothing else in the expanded state.

Do not show: dimension scores, cap information, NOVA level by name, routing category, framework terms of any kind.

### 4c. Row Rhythm

- Rows alternate white / very light gray (no borders between rows)
- Vertical padding: 14px top/bottom per row
- Score chip: 40px wide, neutral background, high-contrast text, no color gradient
- Grade letter: same chip as score, separated by " / "
- Image: consistent crop, consistent background color across all rows in the table
- Insight line: secondary text weight, slightly muted — present but not competing

### 4d. Default Sort

Score descending. The highest-scoring product appears first.

This is the natural order. The user sees the best product at the top and can scroll toward lower-scoring products. This creates natural discovery without any explicit "ranking" framing.

### 4e. Optional Highlighted Pair

One optional comparison pair may be highlighted within the table.

If used:
- Two adjacent rows are visually grouped with a thin bracket or subtle background difference
- A single line appears between them: the driver line (≤15 Hebrew words)
- No separate narrative scene. No side-by-side layout. No ComparisonMoment component.
- This is a table annotation, not a story beat.

If the data does not surface a single clearly strongest pair, omit this element entirely. Absence is better than a forced comparison.

**Maximum: one highlighted pair per page.** If there is pressure to add a second, resist it.

---

## 5. Filters

Collapsed by default. Triggered by a single "סינון" button above the table (right-aligned).

**Maximum: 3 filter dimensions.** Fewer is better.

Each filter dimension is:
- Single-select (radio behavior)
- Category-specific values (no generic framework values)
- Hebrew display names

Filter dimensions by category type:

| Category | Filter 1 | Filter 2 | Filter 3 |
|---|---|---|---|
| מעדנים | סוג מוצר | ציון | — |
| לחם | סוג לחם | ציון | — |
| חטיפים | סוג חטיף | ציון | — |

"סוג מוצר / לחם / חטיף" values must be Hebrew consumer language, not internal cluster names. Examples:
- Not: `milky_style` → Yes: `"מילקי ודומיהם"`
- Not: `whole_grain_sourdough` → Yes: `"לחם שאור"`
- Not: `protein_bar` → Yes: `"חטיף חלבון"`

"ציון" filter: grade values only (B / C / D / E). Never numeric ranges. Never "good / average / poor" labels.

No "clear all" button if only 1 active filter. Show "clear all" only when 2+ filters are active.

No nested filters. No "advanced" filter expansion. No filter count badges.

---

## 6. Methodology

**Purpose:** Quiet trust infrastructure. Not explanation. Not education.

**Rules:**

- 2–4 sentences. Hard limit.
- Footer position or near-footer. Low visual weight.
- Small type size.
- No heading that reads "מתודולוגיה" in large text — that signals "you need to understand this system."
- Acceptable heading: "על הנתונים" or simply no heading.

**What to include:**
- Products reviewed from Israeli retail shelves
- Ingredients, nutrition, and processing context were considered — not only calories or macronutrients
- Scores are relative to the category, not universal rankings
- Full methodology available at [link] — one linked line

**What not to include:**
- Score mechanics
- NOVA explanation
- Cap or floor logic
- Dimension names or weights
- Framework architecture
- Confidence computation

**Example form:**

> "בדקנו 95 מוצרים ממדף המעדנים בשופרסל. הציון מבוסס על רכיבים, ערכי תזונה ורמת עיבוד — לא רק על קלוריות. הציונים יחסיים לקטגוריה. [המתודולוגיה המלאה →]"

That is the complete methodology section.

---

## 7. Mobile

Mobile is the primary design target. The desktop layout adapts from mobile, not the reverse.

### Collapsed row (mobile)

```
[Image 48px] [Product name — truncated to 2 lines]
             [Score chip]
             [Insight line — 1 line, truncated if needed]
```

Tap anywhere on the row to expand. Chevron indicates expandability.

No score explanation on collapsed mobile row. No sub-chips. No badges beyond the single score/grade chip.

### Expanded row (mobile)

Full-width expansion below the row:
- Nutrition 5-field grid (2-column layout)
- Ingredient list (scrollable, 4 lines visible before "show more")
- Data note (1 line)
- Confidence indicator

No horizontal scroll on mobile. No multi-column tables in expanded state.

### Filter panel (mobile)

Full-screen modal triggered by "סינון" button. Apply button at bottom. 3 filter dimensions stacked vertically with radio groups.

### Hero (mobile)

Image: 240px height max. Sentence below image. Score chip below sentence. Table begins within one scroll.

No parallax. No sticky header with score. No overlay text on image.

### Highlighted pair (mobile)

If used: both rows highlighted, driver line appears between them as a subtle annotation. Does not reformat into side-by-side layout on mobile.

---

## 8. Public Language Rules

These rules apply to all public-facing text: hero, prologue, row insights, methodology, filter labels, and any UI microcopy.

### Approved terms

| Concept | Public language |
|---|---|
| Score | ציון (number + grade letter only) |
| High processing | "רמת עיבוד גבוהה" or "מוצר מעובד" |
| Additives | "תוספים" or "תוספים מזוניים" |
| Short ingredient list | "רשימת רכיבים קצרה" |
| Protein | "חלבון" (g amount, not quality classification) |
| Sugar | "סוכר" (g amount from label) |
| Confidence | "נתונים מלאים" / "נתונים חלקיים" |

### Forbidden terms (never appear publicly)

- BSIP, BSIP0, BSIP1, BSIP2
- NOVA (by name or number)
- Cap, binding cap, floor
- Routing, category routing
- Dimension (processing_quality, glycemic_quality, etc.)
- Structural class
- Anchor, hard anchor
- Confidence band, confidence score (numeric)
- Framework, pipeline, ontology
- "Score mechanics" or any explanation of how scores are computed

### Score display rules

Primary display: `69 / B` — no suffix, no label, no color.

Do not say: "ציון גבוה" / "ציון בינוני" / "ציון נמוך." The number and grade speak without interpretation.

Do not map grades to adjectives: no "טוב", "בינוני", "חלש." Grades are A through E. Let them stand.

### Insight line rules

The insight line is an observation, not a verdict.

Approved forms:
- "רשימת רכיבים קצרה מ-5 מרכיבים"
- "10 גרם חלבון ל-100 גרם"
- "מוצר הדיאט עם יותר תוספים מהגרסה הרגילה"
- "המוצר הנמכר ביותר בקטגוריה"

Forbidden forms:
- "מוצר לא בריא"
- "כדאי להימנע"
- "עדיף על"
- "הציון נמוך כי..."
- Any causal explanation of the score

---

## 9. Ontology Leakage Prevention

A leakage event occurs when the internal framework becomes visible to the user through any surface: a filter label, a tooltip, a row annotation, a data note.

**Detection checklist — run before every category launch:**

- [ ] Does any filter label contain a framework term?
- [ ] Does any row insight explain the score mechanism?
- [ ] Does the methodology section name any framework dimension?
- [ ] Does the hero or prologue contain NOVA, cap, or routing language?
- [ ] Does the expanded row show anything other than nutrition, ingredients, data note, confidence?
- [ ] Does the highlighted pair driver line reference framework logic?

If any checkbox is YES: fix before launch.

---

## 10. Dashboard Drift Prevention

A drift event occurs when the page starts feeling like analytics software rather than shelf exploration.

**Drift warning signs:**

- A chart or visualization appears above the first product row
- The user must make a choice (filter, select, configure) before seeing any product
- A summary statistic ("67% of products are NOVA4") appears before product rows
- Color-coding encodes score (red = bad, green = good)
- Multiple filter dimensions are visible and open by default
- Comparison moments multiply beyond one
- An aggregate view (brand ranking, category average) is surfaced as primary content
- Score appears with a verbal interpretation alongside it

**Response to drift pressure:** Do not add the element. If a stakeholder requests one of the above, the answer is: methodology page or framework documentation, not the product table.

---

## 11. Category Portability

The template is category-independent. What changes per category:

| Element | Change |
|---|---|
| Hero product | Identified from data (most surprising score gap) |
| Hero sentence | Written from data observation |
| Prologue | 3–5 sentences from category-specific data |
| Filter dimension 1 | Category product subtypes (Hebrew consumer terms) |
| Highlighted pair | Most structurally clear gap in the category (or omitted) |
| Methodology retailer reference | Current data source |

What does not change:
- Page structure (hero → prologue → table → methodology)
- Row anatomy (image, name, score, insight, expand)
- Expanded row content (nutrition 5-field, ingredients, data note, confidence)
- Filter behavior (collapsed, max 3, single-select)
- Methodology length (2–4 sentences)
- All public-language rules
- All drift-prevention rules

---

## 12. Content-Generation Workflow

For each new category:

**Step 1 — Data prerequisites**
- BSIP2 run complete
- Batch summary reviewed
- Editorial scope filtered (false positives removed)
- Minimum scored products: 30

**Step 2 — Hero identification**
From scored data, identify the single most surprising product:
- Known brand with unexpected low score, OR
- "Healthy" positioned product with score below category average

Write one Hebrew sentence naming the product and the observation. Nothing else.

**Step 3 — Prologue writing**
Three questions to answer in 3–5 sentences total:
1. What products are on this shelf?
2. What did we look at?
3. What is not obvious from the front of the package?

No answer should require more than one sentence. Write those sentences. That is the prologue.

**Step 4 — Highlighted pair identification (optional)**
Identify the single clearest score gap between two comparable products (similar positioning, similar shelf location, significant score difference).

Write one driver line: ≤15 Hebrew words, observational, no framework language.

If no pair is clearly strongest: omit the pair. Do not force one.

**Step 5 — Row insight writing**
For each product in editorial scope, write one insight line (≤12 Hebrew words). Sources: ingredient count, dominant ingredient, notable claim vs. score, protein amount, additive presence.

Do not write an insight that requires knowing the score to interpret. The insight should be independently observable.

**Step 6 — Filter configuration**
Name the 2–3 filter dimensions for this category. Write Hebrew consumer labels for each value. Confirm none of the labels expose framework terms.

**Step 7 — Methodology line**
Write 2–4 sentences using the methodology template. Confirm no framework terms appear.

**Step 8 — Leakage + drift checklist**
Run both checklists (sections 9 and 10). Fix any failures before launch.

---

## 13. UX Principles

These are the governing principles. Every design decision is evaluated against them, in order.

**1. Products first.**  
The user's first visual interaction is with a product, not a system. No filter wall, chart, or summary box appears before the first product row.

**2. Calm by default.**  
Nothing on the page moves, pulses, or competes for attention. Interactions are quiet: expand/collapse, filter toggle. No hover state changes the layout.

**3. One discovery at a time.**  
The table is sorted by score. Contradictions emerge through scrolling, not through annotation. The user does not need a map to find the contradiction — they find it by reading.

**4. Invisible scaffolding.**  
The system that produced the scores does not appear. The user sees products, scores, and observations. They do not see the pipeline.

**5. Mobile is not a reduction.**  
The mobile experience is complete. Collapsed rows contain everything a browsing user needs. Expanded rows contain everything an investigating user needs. Nothing essential is desktop-only.

**6. Restraint is the feature.**  
When in doubt, remove. A page with fewer elements at higher quality is better than a page with more elements at lower quality. The absence of a comparison moment is not a loss — it is a decision to let the table speak.

---

## Appendix — What This Template Deliberately Excludes

The following were considered and excluded. They are not in scope for the standard template. They require explicit re-approval to introduce.

| Excluded element | Reason |
|---|---|
| Score distribution chart | Analytics register, no consumer utility |
| Brand performance table | Too strong an editorial claim at category level |
| Interactive cluster map | Displaces products, requires user orientation work |
| Multi-comparison narrative scenes | Theatrical, over-structured, hard to scale |
| "Understanding the score" modal | Framework exposure risk |
| Animated score reveal | Cinematic, disconnected from shelf-native feeling |
| Color-coded score chips | Creates good/bad framing the score number doesn't need |
| Filter count badges | Analytics UI pattern |
| "Recommended" or "best" labels | Editorial claim too strong for observational frame |
| Radar / spider charts per product | Exposes dimension architecture |
| Category average benchmarks | Requires explanation of how average was computed |
