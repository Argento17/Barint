# Bari Snack Bar — Editorial Recovery v1
**Date:** 2026-05-28
**Type:** Editorial recovery + Cursor implementation guidance
**Replaces:** snack_bar_blog_v1.md *for UX philosophy and page architecture only*
**Preserves:** All analytical content in snack_bar_blog_v1.md (dataset constants, score drivers, comparison pairs, component data specs) — that data remains valid.

---

## What This Document Is

The snack bar implementation drifted from the Bari editorial standard. This document corrects the philosophy and page architecture. It does not rebuild the analysis — it rebuilds the *experience*.

The analytical content in `snack_bar_blog_v1.md` (scores, comparisons, BarCompositionBreakdown rows, product data) is still valid. What failed was everything above it: how the experience opens, how it paces itself, where comparisons live, how filters and maps are presented.

---

## Diagnosis — The Three Failures

### Failure 1: Blog and Comparison Engine were the same experience

The main architectural mistake. The blog attempted to be both a guided investigation and an exploration interface. The result was neither. Filters appeared before the user understood what they were filtering. Maps appeared before the user cared about the axes. Taxonomy appeared before the user had emotional context.

**Fix:** Two entirely separate experiences with one-way navigation. Blog first. Comparison engine second. The CTA at the end of the blog is the bridge.

---

### Failure 2: Maps and filters displaced product presence

The user's first visual encounter was with axes, clusters, and controls — not with bars. Snack bars are familiar, visually deceptive, packaging-driven objects. Without product imagery present early, the category collapsed into abstraction. A dot on a map is not a granola bar.

**Fix:** Products appear before maps. Packaging imagery is mandatory and large. Maps support the story — they do not open it.

---

### Failure 3: The comparison moments were buried

The comparisons in `snack_bar_blog_v1.md` are the editorial core — three chocolate bars with a 41-point spread, a protein bar vs. a 4-ingredient date bar with a 23-point gap, "granola" on two completely different compositions. These are the moments that should make a reader stop. Instead, they appeared below maps, below breakdowns, inside tables, after multiple scroll cycles.

**Fix:** Comparisons dominate the page. They are the largest visual moments. Everything before them is pacing toward them. Everything after them is synthesis.

---

## The Milk Standard — What Must Be Replicated

The milk investigation worked because of four things that snack bars lost:

| Milk did this | Snack must do this |
|---|---|
| Products felt physically real — large CDN images, recognizable packaging | Large packaging visuals on every comparison moment |
| Shelf tension in the first sentence — "whole milk wins, but why?" | Shelf tension in the first headline — a specific gap, a named paradox |
| Investigation unfolded gradually — story before data | Hero → Findings → Map → COMPARISONS → Synthesis |
| Comparisons were emotionally obvious — the visual difference was immediate | Each comparison: packaging side-by-side, score contrast, one-sentence driver |

The milk comparison engine was a grid of 6 products sorted by score. Simple. Product-first. No filter wall. That is the target.

---

---

# PART 1 — THE SNACK BLOG

## Philosophy

The reader should feel: *"These bars look similar. Why are they completely different?"*

The page should feel: visual, surprising, curated, calm, shelf-native.

The page should not feel: filterable, operational, system-driven, component-heavy.

The pacing model: hero creates tension → findings explain patterns → map contextualizes scale → comparisons are the emotional peak → synthesis closes → CTA opens exploration.

---

## New Blog Structure

```
1. Hero                         ← Shelf tension. Specific. Not generic.
2. Shelf intro                  ← Make the shelf feel real. Name the products.
3. Key findings (3 max)         ← Memorable. Concrete. Emotionally sticky.
4. ONE quiet editorial map      ← Context, not experience.
5. BIG comparison moments       ← This is the heart. Visually dominant.
6. Calm synthesis               ← Short. Human. Not reportese.
7. CTA → Comparison engine      ← Only here, only once.
```

---

## 1. Hero

### Philosophy

The hero creates immediate shelf tension. It names something specific that is surprising or counterintuitive. It does not describe the system. It does not announce the category. It announces a finding.

### Required: Two article heroes

**Article 1 — Everyday bars hero:**

Option A (recommended):
> שלושה חטיפי דגנים. 36 נקודות הפרש.
> *על אותו מדף — הרכב שונה לחלוטין.*

Option B:
> "גרנולה" על שני מוצרים שונים לחלוטין.
> *שניהם קראנצ'י. אחד 53/C — אחד 17/E.*

Option C:
> 58% מהחטיפים שסרקנו הם NOVA4.
> *כולם קיבלו D או E.*

**Article 2 — Wellness bars hero:**

Option A (recommended):
> בר פרוטאין: 47/D.
> חטיף תמרים עם 4 רכיבים: 70/B.
> *23 נקודות הפרש. אותה קטגוריה.*

Option B:
> המוצר עם הציון הגבוה ביותר בכל הנתונים לא נקרא "פרוטאין", לא "פיטנס", לא "אנרג'י".
> *הוא נקרא חטיף תמרים.*

### Visual of the hero

Large packaging image (or two side-by-side for contrast). Score chip prominently below the image. Headline above. No filters, no maps, no stat bars at this stage.

**Hero visual order:**
```
Headline (tension statement)
↓
Product imagery (large — one or two products)
↓
Score chips below the images
↓
Single subline: "מה שהפריד ביניהם — לא השם על האריזה."
```

### Do NOT put in the hero:
- ShelfStatBar (move it below the fold, after findings)
- InsightCards
- Any filter UI
- Category navigation
- Article menu

---

## 2. Shelf Intro (130–160 words)

This paragraph makes the shelf feel real before the investigation begins.

It must:
- Name the actual shelf segments (protein bars, granola bars, chocolate-coated bars, date bars, "fitness" bars, "energy" bars, kids bars)
- Create the sense that the reader knows this shelf
- Plant the question the investigation will answer

**Required feel:**
The reader should think: *"I know this shelf. I've bought from this shelf. I wonder what happened."*

**Tone:** Calm, shelf-first. Not analytical. Not introductory.

**Example opening:**
> "יוחננוף, מדף הקטגוריה. חטיפי פיטנס בצהוב-כחול. Nature Valley קלאסי. קורני ושוגי. חטיפי תמרים בחום. בשורה הבאה — חטיפי פרוטאין, ובצד: 'אנרג'י', 'סלים', 'Free'. אנחנו סרקנו 53 מוצרים מהמדף הזה. הציון הגבוה ביותר — 70/B — לא הלך לאף אחד מהשמות שהזכרנו."

**ShelfStatBar placement:** Directly below the intro paragraph. Not above it.

---

## 3. Key Findings (3 cards maximum)

### Philosophy

3 findings maximum. Not 4, not 5. Each finding is one thing that is surprising and specific. They are not a table of contents. They are not a system summary. They are the three moments that will stick in the reader's memory after they leave the page.

### Card format

```
[Type tag — Finding / Pattern / Gap]
Bold finding sentence.
One-sentence elaboration.
```

No icons. No color differentiation between cards. Same visual weight for all three.

### Article 1 — Three findings

**Finding 1:**
> **רק מוצר אחד מ-53 הגיע לדרגה B — חטיף עם 4 רכיבים.**
> כל השאר: C, D, או E.

**Finding 2:**
> **כל מוצר NOVA4 בנתונים קיבל D או E — ללא יוצא מן הכלל.**
> NOVA4 מכסה 58% מהמדף.

**Finding 3:**
> **"פיטנס" ו"אנרג'י" על האריזה — ציונים בטווח 17–46.**
> השמות לא ניבאו את הציון. ההרכב כן.

### Article 2 — Three findings

**Finding 1:**
> **חטיפי הפרוטאין קיבלו D. חטיף תמרים עם 4 רכיבים קיבל B.**
> הפרש: 23 נקודות. הגורם: עומק העיבוד, לא כמות הפרוטאין.

**Finding 2:**
> **"תמרים" על האריזה לא אמר את אותו הדבר בשני מוצרים שונים.**
> חטיף תמרים במילוי חמאת שקדים: 70/B. פרי מארז תמרים ואגוזי לוז: 43/D.

**Finding 3:**
> **NOVA4 הוא תקרת ציון — לא מדד "רע".**
> כשמוצר הוא NOVA4, הציון המקסימלי שיכול לקבל הוא D. המיצוב על האריזה לא שינה את זה.

---

## 4. ONE Quiet Editorial Map

### Philosophy

One map. Calm. Supporting the investigation — not leading it. The map comes *after* the findings, not before them. The reader already knows the story. The map shows where on the shelf each product landed.

### Map requirements

**What the map must have:**
- Two axes (as in snack_bar_blog_v1.md — one per article)
- Product dots with score on hover
- 2–3 annotated products (not cluster labels)
- A one-line caption below the map

**What the map must NOT have:**
- Filter controls on the map
- Cluster selection UI
- Dropdown overlays
- Multiple map options/views
- Interactive color toggles
- "Show/hide cluster" controls

**Map title format:**
Simple. Descriptive. Not analytical.

Article 1: "עומק עיבוד וסוכר — 53 חטיפים"
Article 2: "פשטות הרכיבים מול מיצוב — 53 חטיפים"

**Annotated products (mandatory):**
- The B-grade date bar (always labeled: "70/B — 4 רכיבים")
- The lowest-scoring product (always labeled: "13/E")
- One protein bar cluster (labeled: "חטיפי פרוטאין — 45–47/D")

**Map size:** Medium. Not dominant. The comparisons below it should feel larger.

**Mobile behavior:** Replace map with the top-3 annotated products in a list. Do not attempt to shrink the scatter plot for mobile.

---

## 5. BIG COMPARISON MOMENTS

### Philosophy

This is the heart of the snack bar investigation. Every design decision flows from making these moments as large, visually clear, and emotionally obvious as possible.

The reader should feel: *"These look similar. Why are they so different?"*

The comparison sections should be the largest, most visually dominant element on the page. Everything before them is pacing toward them. They are not inside tables. They are not text with inline scores. They are visual confrontations.

---

### Comparison visual structure (per comparison)

```
[COMPARISON TITLE — shelf tension statement]

[Product A packaging image] [Product B packaging image]
     [Score: 56/C]               [Score: 17/E]

[One-sentence driver: "שניהם שיבולת שועל. אחד NOVA3, אחד NOVA4 עם 14 רכיבים."]

[Expandable: more detail — ingredient count, NOVA, one observable difference]
```

Packaging images: full product front-of-pack. CDN URL from BSIP1 (already scraped for Yohananof products). Large. Not thumbnail size.

Score chips: below the image. Prominent. Grade letter is visually largest element of the chip.

Driver sentence: below both images. One sentence. Maximum 20 words. The single most observable difference.

No tables within the comparison card. No dimension breakdowns inside the comparison. The comparison is emotional first, analytical on expand.

---

### Article 1 — Three comparison moments

**Comparison 1: "אותה שיבולת שועל — הפרש של 36 נקודות"**
Products: קראנצ'י שיבולת שועל עם דבש (53/C) vs. פיטנס בר גרנולה שוקולד מריר (17/E)
Driver: "שניהם עם שיבולת שועל. אחד בסיס שיבולת שועל שלמה — אחד בסיס קמח וסירופ גלוקוז עם 14 רכיבים."
Tension: Same oats word. 36-point gap.

**Comparison 2: "פיטנס על האריזה — ציון D בפנים"**
Products: חטיף תמרים בציפוי שוקולד קקאו 100% (56/C) vs. חטיפי דגנים פיטנס קלאסי (46/D)
Driver: "שני חטיפים בציפוי שוקולד. אחד תמרים-ראשון, NOVA2. אחד קמח-וסירופ-ראשון, NOVA4."
Tension: "Fitness" branding on lower-scoring product.

**Comparison 3: "הציון הנמוך ביותר"** *(shorter — one product spotlight, not a pair)*
Product: שחור ולבן קורני שוקולד (13/E)
Driver: "הציון הנמוך ביותר בנתונים. שלושה מקורות סוכר. 5+ תוספות פונקציונליות. NOVA4."
Purpose: Anchors the bottom of the shelf before synthesis.

---

### Article 2 — Three comparison moments

**Comparison 1: "בר פרוטאין מול חטיף תמרים — 23 נקודות"** *(the article's central moment)*
Products: חטיף תמרים במילוי חמאת שקדים (70/B) vs. נייצ'ר וואלי פרוטאין בוטנים ושוקולד (47/D)
Driver: "4 רכיבים, NOVA2: 70/B. 15+ רכיבים, NOVA4: 47/D. הפרש הציון לא בא מהפרוטאין."
Tension: The counterintuitive result — the simpler product won.

**Comparison 2: "שלושה חטיפי שוקולד מריר — שלושה ציונים"** *(three-way contrast)*
Products: חטיף תמרים שוקולד קקאו (56/C) + סלים דליס שוקולד מריר (58/C) + פיטנס גרנולה שוקולד מריר (17/E)
Format: Three products in one comparison moment. Score chips large and visible. 41-point span labeled.
Driver: "שלושה חטיפים בציפוי שוקולד מריר. בסיס שונה — NOVA שונה — 41 נקודות הפרש."
Tension: Same shelf category, same visual register, massive divergence.

**Comparison 3: "תמרים — אבל לא אותו דבר"**
Products: חטיף תמרים במילוי חמאת שקדים (70/B) vs. פרי מארז תמרים ואגוזי לוז (43/D)
Driver: "שניהם 'תמרים'. אחד: תמרים ראשון ברשימה, NOVA2. אחד: NOVA4, סוכרים מוספים."
Tension: Same product category signal, 27-point gap.

---

### What makes a comparison feel large (visual specs)

- Minimum image height: 180px per product image on desktop
- Minimum image height: 140px per product image on mobile
- Score chip: Grade letter at 32px minimum, number at 18px minimum
- Driver sentence: 16px body text, centered below both images, maximum 25 words
- Section spacing: 48px above and below each comparison moment
- No borders between products in the pair — use whitespace only
- Section title: 22px heading, left-aligned (RTL: right-aligned)

**Do NOT:**
- Show both products in a table
- Use a score badge smaller than the product name
- Put the comparison inside an accordion
- Combine two comparison pairs in one visual unit
- Compress comparisons to allow more content above them

---

## 6. Calm Synthesis (Article 2 only)

Article 1 ends with the TakeawayList (as specified in snack_bar_blog_v1.md) — three factual bullets, no changes.

Article 2 ends with a synthesis paragraph before the CTA.

**Synthesis rules:**
- 80–120 words maximum
- Finding-first
- No "the data suggests," no "the conclusion from the dataset"
- No moral framing
- No recommendations

**Example:**
> "מה שהפריד את המוצרים בקטגוריה הזו היה מבנה הרכיבים ועומק העיבוד — לא השם. חטיפי פרוטאין, חטיפי פיטנס, ומוצרים עם 'תמרים' בשם שהם NOVA4 — כולם הגיעו לאותה תקרה. הציון הגבוה ביותר — 70/B — לא נשא שום תווית. 4 רכיבים, NOVA2."

---

## 7. CTA → Comparison Engine

Appears once. After synthesis. Short.

```
→ לכל 53 המוצרים, סוננים לפי ציון
[לטבלת ההשוואה המלאה]
```

This is the only place the comparison engine is surfaced from the blog. Not in the header. Not as a secondary nav. Not before the investigation finishes.

---

## Blog Sequencing — Visual Priority

```
Priority 1 — COMPARISON MOMENTS (largest visual footprint)
Priority 2 — HERO (immediate tension, large imagery)
Priority 3 — FINDINGS (3 cards, clear)
Priority 4 — MAP (medium, single, quiet)
Priority 5 — SYNTHESIS + CTA (text, restrained)
Priority 6 — ShelfStatBar, Glossary, Methodology (minimal)
```

The BarCompositionBreakdown (5 dimensions from snack_bar_blog_v1.md) is **removed from the blog** in this recovery. It belongs in the comparison engine as supporting detail, not in the investigation narrative. The blog's analytical core is the comparisons — not the dimension breakdown.

---

---

# PART 2 — THE COMPARISON ENGINE

## Philosophy

The comparison engine is where the reader goes *after* the investigation. They have context. They want to explore.

The engine should feel like: browsing a curated shelf intelligence system.

The engine should not feel like: operating software, a BI dashboard, or a nutrition analytics platform.

---

## Page Entry Frame

The comparison engine does not re-explain the investigation. The reader came from the blog. The entry is simple.

```
כל החטיפים — 53 מוצרים, יוחננוף, מאי 2026
[Search bar — one line, no additional controls above the fold]
[Product grid immediately below]
```

No hero. No InsightCards. No map. No filter wall. Products appear immediately.

---

## Above-the-fold: Products, Not Filters

**Current (failed) state:** Filters, pills, cluster selectors, search, map — all before any product appears.

**Corrected state:**
- Search bar (one line)
- Product grid (6 products visible above the fold on desktop, 4 on tablet, 2 on mobile)
- Filters: collapsed behind one "סינון" button

The user sees products first. Filters are available but dormant until requested.

---

## Product Card — Mandatory Visual Requirements

Each product card must show:

```
[Product packaging image — minimum 120px tall on desktop]
[Product name — Hebrew, 1–2 lines max]
[Score chip: number / grade — prominent]
[One-line shelf segment: "חטיף תמרים" / "חטיף גרנולה" / "חטיף פרוטאין"]
[NOVA tag: NOVA2 / NOVA3 / NOVA4 — small, below segment]
```

Packaging image is mandatory. Products without a resolvable image_url: show a category-appropriate placeholder (a flat bar silhouette in the shelf segment color — not a broken image icon).

**Card grid:** 3 columns desktop, 2 tablet, 1 mobile. Sorted by score descending by default.

**Card size:** Not small. Cards must be large enough that packaging imagery is recognizable. Minimum card width: 200px desktop, 160px tablet.

---

## Filter System — Secondary, Collapsed

**Available filters (if user opens them):**
1. דרגה (A–E) — grade filter
2. NOVA — NOVA2 / NOVA3 / NOVA4
3. קטגוריה — 6 shelf segments from snack_bar_blog_v1.md
4. ציון (range slider — 0 to 100)

**Filter presentation:**
- Hidden behind single "סינון" button
- When opened: a clean panel with 4 filter groups. No pills initially.
- Active filter chips appear in a single row below the search bar when filters are applied
- Max 3 active filter chips visible before "+ more" truncation

**Do NOT:**
- Show all filters expanded above the fold
- Use multi-select filter pills as a primary navigation element
- Show filter counts before the user has context (e.g., "NOVA4 (31)" as a visible option from the start)

---

## Map in the Comparison Engine

The comparison engine contains ONE map (not two). It appears in a separate "מפת המדף" section, below the product grid. Not above it.

**Map behavior in the engine:**
- Default: hidden
- Revealed on click: "להצגת מפת המדף ←"
- When revealed: same map as Article 1 (processing depth × sweetener architecture)
- Same specs as blog map (calm, annotated, no controls)

The map in the comparison engine is a discovery tool for users who want it. It is not the organizing principle of the experience.

---

## Comparison Engine — Product Detail

When a user clicks a product card, they see:

```
[Product packaging — large, left/right]
[Score: number/grade — large]
[Shelf segment label]
[NOVA tag]
---
[WhyThisLandedHere — 3-section explainability from explainability_v1.md]
  Section 1: מה שבלט (always shown)
  Section 2: מה שהגביל (if score <60)
  Section 3: מה שלא ניתן לאמת (if confidence=partial)
---
[BarCompositionBreakdown — the 5 dimensions from snack_bar_blog_v1.md]
  This lives here, not in the blog.
---
[Score Driver list — from snack_bar_blog_v1.md score driver table]
```

This is where the analytical detail lives. The blog is editorial. The engine is investigative.

---

## Comparison Engine — Preset Comparisons

Three comparison presets available from the engine:

```
[השוואות מוכנות]
• שיבולת שועל משני קצות המדף →
• בר פרוטאין מול חטיף תמרים →
• שלושה חטיפי שוקולד מריר →
```

When a preset is selected, it renders the same comparison visual format used in the blog (large imagery, score chips, driver sentence) — but within the engine's archive aesthetic.

Custom comparison (user selects two products manually): available from the engine's product grid via a "השווה" toggle on each card. Maximum 3 products in custom comparison.

---

## Dashboard Energy — What to Remove

The following elements belong to the failed state and must be removed or deprioritized:

| Element | Status | Corrected behavior |
|---|---|---|
| Filter wall above the fold | Remove | Filters behind single "סינון" button |
| Map as primary visual anchor | Remove | Map in collapsed "מפת המדף" section, below grid |
| Cluster selection UI | Remove | Not present in engine |
| Multiple simultaneous filter pills | Remove | Max 3 active chips visible |
| BI-style header statistics | Remove | ShelfStatBar moves to bottom of engine, below grid |
| Animation on filter change | Remove | Static transitions only |
| Score color encoding on card background | Remove | Score chip only — no card background color |
| "בחר קטגוריה" mega-menu | Remove | Simple dropdown within filter panel |

---

---

# VISUAL PACING RULES (Both Experiences)

## 1. Spacing

- Section spacing (between major sections): 64px desktop, 48px mobile
- Comparison moment internal padding: 48px desktop, 32px mobile
- Product card grid gap: 24px desktop, 16px mobile

## 2. Typography hierarchy

- Hero headline: 36–42px, bold, high contrast
- Finding headline: 20px, bold
- Comparison title: 22px, medium-weight
- Body text: 16px, regular
- Labels/tags (NOVA, shelf segment): 12px, uppercase, muted

## 3. Imagery

### Blog

Hero: one or two product images, full-width or half-width, minimum 240px tall.
Comparison: packaging images, centered, minimum 180px tall.

### Engine

Product cards: minimum 120px image height.
Product detail: large, minimum 240px tall.

### Source

`image_url` from BSIP1 for all Yohananof products. Add `loading="lazy"`. Fallback: flat bar silhouette in the shelf segment color.

## 4. Color

No score-based background color on cards (forbidden by score_presentation_v1.md).
NOVA tags: simple text tags, not color-coded. NOVA2 = no visual emphasis, NOVA3 = no visual emphasis, NOVA4 = no visual emphasis. The word carries the meaning.
Grade chip: grade letter colored by grade (A=dark green, B=light green, C=amber, D=orange, E=red) — chip background only, not card background.

## 5. Restrained interaction

- Hover: simple opacity shift on product cards (0.85)
- Click: opens detail — no modal animation beyond a simple slide
- Filter apply: instant, no loading spinner unless dataset >500 products
- Map hover: tooltip appears, nothing else moves

---

---

# EDITORIAL SEQUENCING RULES

## Rule 1: Investigation before exploration

The blog completes before the engine opens. No "browse" links from the blog navigation. The CTA at the bottom is the only path.

## Rule 2: Products before frameworks

Products appear before maps, before breakdowns, before dimension tables. This applies to both experiences.

## Rule 3: Tension before explanation

Each section creates a question before answering it. Hero creates tension. Findings name the patterns. Map contextualizes the scale. Comparisons deliver the emotional answer. Synthesis closes. This order is not optional.

## Rule 4: Comparisons are the largest visual units

No other element on the blog page should visually outweigh a comparison moment. Not the map. Not the findings grid. Not the stat bar.

## Rule 5: One map per page

One map per article in the blog. One map (collapsed by default) in the engine. The map is a support tool. Not a navigation tool.

## Rule 6: Framework vocabulary stays in the engine

The blog uses shelf vocabulary: "חטיף תמרים", "שיבולת שועל שלמה", "קמח ו-סירופ גלוקוז ראשונים". The engine can surface dimension names (מקור הבסיס, עומס התוספות) — but only in product detail, not in the grid view.

---

---

# NARRATIVE PACING RULES

## Blog pacing

| Position | Purpose | Max words |
|---|---|---|
| Hero | Tension — one specific gap | 25 |
| Intro | Shelf presence — names the products | 160 |
| Finding 1 | Pattern — the dominant driver | 30 |
| Finding 2 | Pattern — the shelf-wide fact | 30 |
| Finding 3 | Gap — the positioning misalignment | 30 |
| Map | Contextual — silent data visual | — |
| Comparison 1 | Emotional peak — visual + 1 sentence | 25 |
| Comparison 2 | Emotional peak — visual + 1 sentence | 25 |
| Comparison 3 | Emotional peak — visual + 1 sentence | 25 (Article 1: one product spotlight) |
| Synthesis | Closing — factual, not philosophical | 120 |
| TakeawayList | Synthesis bullets | 3 bullets × 25 words |
| CTA | Bridge to engine | 15 |

## Pacing anti-patterns

**Anti-pattern 1: Front-loading**
Putting all findings, the stat bar, and an InsightCards grid above the fold before the reader has emotional context. This kills curiosity before the investigation begins.

**Anti-pattern 2: Map dominance**
Making the map the largest visual unit on the page. Maps contextualize. They do not create shelf presence.

**Anti-pattern 3: Buried comparisons**
Placing comparison pairs after multi-section dimension breakdowns. The reader has lost momentum by the time they reach the emotional core.

**Anti-pattern 4: Symmetric weight**
Every section at the same visual weight. The comparison moments must be heavier than everything else on the page.

---

---

# MILK BENCHMARK RULES

Every design decision in the snack experience should pass this test:

**"Would this feel shelf-native in the milk investigation?"**

Specific benchmark requirements:

| Milk standard | Snack implementation required |
|---|---|
| Products are physically recognizable objects | Packaging imagery on every card, every comparison |
| First impression is a specific finding, not a category overview | Hero = specific gap, not "Snack Bar Intelligence" |
| Comparisons are the investigation's emotional core | Comparisons are visually largest elements |
| The shelf feels real before the analysis begins | Intro names actual products, not shelf types |
| Complexity reveals gradually | Engine starts with grid, filters dormant |
| The user is guided, not handed controls | CTA is the only navigation tool in the blog |
| Score is primary, dimensions are secondary | Score chip is the largest number on the card |
| One story per page | Blog = investigation, Engine = archive |

---

---

# BEFORE vs AFTER EXAMPLES

## Hero

**BEFORE (failed):**
```
"חטיפי חלבון, גרנולה ו'טבעי' — מה הנתונים הראו"
[ShelfStatBar: 53 נסרקו | 48 קיבלו ציון | 59% NOVA4 | 24 E | יוחננוף]
[InsightCard 1][InsightCard 2][InsightCard 3][InsightCard 4]
```
Reader sees: category overview, stats, analysis summary — before any product.

**AFTER (corrected):**
```
"בר פרוטאין: 47/D.
חטיף תמרים עם 4 רכיבים: 70/B."
[Product image: נייצ'ר וואלי פרוטאין]  [Product image: חטיף תמרים]
         47 / D                                    70 / B
"23 נקודות הפרש. אותה קטגוריה."
```
Reader sees: specific gap, two real products, immediate curiosity.

---

## Above-the-fold (Comparison Engine)

**BEFORE (failed):**
```
[Filter bar: דרגה | NOVA | קטגוריה | ציון | השוואה]
[Pill row: B C D E | NOVA2 NOVA3 NOVA4 | תמרים גרנולה פרוטאין...]
[SnackBarShelfMap — full-width scatter plot]
[Product grid — visible only after scrolling past the above]
```
Reader sees: controls, taxonomy, map — no products above the fold.

**AFTER (corrected):**
```
[Search bar — one line]
[Product Grid — 6 products visible]
  [Card: חטיף תמרים במילוי חמאת שקדים | 70/B | NOVA2]
  [Card: מרבה סלים דליס שוקולד מריר | 58/C | NOVA3]
  [Card: חמאת בוטנים אמריקאי | 55/C | NOVA3]
  [Card: קראנצ'י שיבולת שועל ודבש | 53/C | NOVA3]
  ...
[סינון ▼]  [מפת המדף ▼]  — both collapsed, below the grid header
```
Reader sees: products first. Filters available but dormant.

---

## Comparison moment

**BEFORE (failed):**
```
**Pair 2: "שיבולת שועל בשני קצות המדף"**
| מוצר | ציון | דרגה | NOVA | בסיס | הסיבה לפרש |
|------|------|------|------|------|------------|
| קראנצ'י שיבולת שועל עם דבש | 53 | C | 3 | שיבולת שועל שלמה | עיבוד בינוני |
| פיטנס בר גרנולה שוקולד מריר | 17 | E | 4 | קמח + סירופ | NOVA4 + מרובה תוספות |

"שניהם עם שיבולת שועל. שניהם קראנצ'י/גרנולה. הפרש ציון: 36 נקודות..."
```
Reader sees: a data table. Database energy.

**AFTER (corrected):**
```
"אותה שיבולת שועל — 36 נקודות הפרש"

[Image: קראנצ'י שיבולת שועל — 180px tall]    [Image: פיטנס גרנולה — 180px tall]
              53 / C                                        17 / E

"שניהם שיבולת שועל. אחד בסיס שלם NOVA3 — אחד קמח וסירופ גלוקוז NOVA4 עם 14 רכיבים."

[▸ פרטים נוספים]  ← collapsed detail
```
Reader sees: two real bars, a specific gap, one clear reason. Shelf presence.

---

## Map presentation

**BEFORE (failed):**
Map is the primary visual anchor. Full-width. Loaded before user understands the investigation. With cluster selection, filter overlays, multiple view modes.

**AFTER (corrected):**
Map appears after findings, at medium width (70% of content column), with 3 annotated points (70/B date bar, 13/E Corny, Nature Valley protein cluster), and a one-line caption. No interaction controls on the map itself. Hover for tooltip. That is all.

---

## Filter experience

**BEFORE (failed):**
Multiple filter rows visible above the fold. Product taxonomy exposed as navigation element. Cluster selection integrated with the map as primary interaction.

**AFTER (corrected):**
```
[Search bar]
[Product grid]
[סינון ▼]  ← single button

When "סינון" clicked:
  Panel appears from the right (desktop) / bottom sheet (mobile):
  ──────────────────────
  דרגה:  [B] [C] [D] [E]
  NOVA:  [2] [3] [4]
  קטגוריה: [dropdown]
  ציון: [slider 0–100]
  [החל]  [נקה]
  ──────────────────────
```
Filters are available but dormant. Products are not hidden behind filters.

---

---

# CURSOR IMPLEMENTATION GUIDANCE

## What changes from snack_bar_blog_v1.md

| Component in v1 | Status | New behavior |
|---|---|---|
| ShelfStatBar | Stays, but moved | Blog: below intro (not in hero). Engine: below product grid. |
| InsightCardsGrid (4 cards) | Reduced to 3 | Remove 4th card. 3-card grid maximum. |
| SnackBarShelfMap | Stays, but repositioned | Blog: after findings, medium width. Engine: collapsed section. |
| BarCompositionBreakdown (5 rows) | Moved to engine | Not on the blog. Lives in product detail within the engine. |
| ProductComparisonMatrix | Rebuilt | Was table + prose. Now: imagery + score chip + 1 sentence. See "Comparison moment" specs above. |
| TakeawayList | Stays | Article 1 only. Same 3 bullets as v1. |
| SynthesisParagraph | Stays | Article 2 only. 80–120 words. |
| GlossaryAccordion | Stays | Both articles. Same content as v1. |
| MethodologyNote | Stays | Both articles. Same content as v1. |

## New components required

### `ComparisonMoment`
Props: `{ title: string, products: [Product, Product?], driverSentence: string }`
Renders: packaging images (large), score chips, driver sentence, collapsed detail.
Note: `products` can be 2 (pair) or 3 (triple — Article 2 Comparison 2). Handles both cases.

### `ProductCardGrid`
Props: `{ products: Product[], defaultSort: "score" }`
Renders: grid with packaging imagery mandatory. Sort controls: score, grade, NOVA, name.
No filter UI within this component — filters handled by parent.

### `FilterPanel`
Props: `{ onApply, onClear, activeFilters }`
Renders: collapsible panel. Never visible above the fold by default.
Opens via single "סינון" button in the toolbar.

### `MapSection`
Props: `{ products: Product[], annotatedIds: string[], title: string, caption: string }`
Renders: the scatter plot at 70% content width. No controls on the map itself.
Blog: visible by default. Engine: collapsed behind "מפת המדף ▼".

## Data requirements (unchanged from v1)

All data requirements in `snack_bar_blog_v1.md` Section 11 remain valid. The `image_url` field from BSIP1 is now **mandatory** — not optional. No product appears without either a resolved image or a category placeholder.

## Pre-implementation checklist (unchanged from v1)

The checklist in `snack_bar_blog_v1.md` (BSIP2 re-run, granola routing, frontend dataset JSON) remains fully required. This document adds one item:

- [ ] `image_url` verified and resolvable for the following products: חטיף תמרים במילוי חמאת שקדים, נייצ'ר וואלי פרוטאין, קראנצ'י שיבולת שועל ודבש, פיטנס בר גרנולה שוקולד מריר, שחור ולבן קורני שוקולד, פרי מארז תמרים ואגוזי לוז. These 6 products appear in comparison moments and must have real imagery.

## Build order

```
1. ComparisonMoment — build and validate against 3 pairs before building any other component
2. ProductCardGrid — with mandatory image handling and fallback placeholder
3. Blog hero — imagery + score chip + tension headline
4. Blog findings — 3-card grid
5. MapSection — medium width, 3 annotations
6. FilterPanel — collapsed by default, single-button trigger
7. Blog synthesis + CTA
8. Engine: ProductCardGrid integration + FilterPanel + collapsed MapSection
9. Engine: product detail with WhyThisLandedHere + BarCompositionBreakdown
```

## Likely failure modes

- Returning BarCompositionBreakdown to the blog (it belongs in engine product detail only)
- Building InsightCards as 4 cards (3 maximum)
- Opening the engine with filters or map above the fold
- Rendering comparison pairs as data tables
- Using small product images (thumbnail size) on comparison moments
- Surfacing ScoreDriverTable as a section on the blog
- Adding "recommended" or endorsement language to the 70/B date bar
- Applying card background color based on grade (forbidden — grade chip only)

---

*Document generated 2026-05-28 by Claude Code (Bari internal toolchain)*
*Analytical data reference: snack_bar_blog_v1.md (unchanged)*
*Governance reference: bari_governance_v1.md, explainability_v1.md, score_presentation_v1.md*
