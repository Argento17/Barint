# Bari UI Stabilization Sprint 1

**Date:** 2026-05-28  
**Scope:** Row rhythm, mobile scroll, hero density, insight-line density, cross-category consistency  
**Status:** Canonical implementation reference  
**Not in scope:** Architecture changes, new sections, new systems

---

## Deliverable 1 — Row Rhythm Audit

### The core problem

The primary failure mode in product row design is the table/spreadsheet feel. It comes from three specific causes, any one of which is sufficient to break shelf-native rhythm:

1. Hard borders between rows
2. Type sizes that are too close together (no clear hierarchy)
3. Vertical padding that is too tight

All three create an environment where the eye treats the page as data, not as products. The fix is not soft — it is specific measurements applied consistently.

---

### Collapsed row specification

**Total row height:** 72px (mobile) / 80px (desktop)  
**Vertical padding:** 14px top / 14px bottom  
**Horizontal padding:** 16px left / 16px right

**Product image:**
- Size: 56px × 56px (square crop)
- Border radius: 6px
- Background: #F8F8F8 (used when packaging has whitespace or transparency)
- Object-fit: contain — never cover. The label must be fully visible.
- No border on the image itself
- Margin right: 12px

**Product name:**
- Font size: 15px
- Font weight: 500 (medium)
- Color: #1A1A1A
- Line clamp: 2 lines on mobile, 1 line on desktop
- Overflow: ellipsis
- Margin bottom (to insight line): 3px

**Score chip:**
- Width: auto (min 52px, max 68px)
- Height: 28px
- Border radius: 14px (fully rounded)
- Background: #F0F0F0
- Font size: 13px
- Font weight: 600
- Color: #1A1A1A
- Format: "69 / B"
- Padding: 0 10px
- Alignment: right-aligned in the row, vertically centered
- No color coding. No background change based on score value.

**Insight line:**
- Font size: 13px
- Font weight: 400
- Color: #666666 (muted — subordinate to product name)
- Line clamp: 1 line always
- Overflow: ellipsis
- No bold, no italic

**Expand chevron:**
- Size: 16px icon
- Touch target: 44px × 44px (full right edge of row)
- Color: #AAAAAA at rest, #666666 on hover/active
- Rotates 180° when row is expanded (transition: 200ms ease-out)

**Row separator:**
- NOT a border
- Alternating background: odd rows #FFFFFF, even rows #F9F9F9
- The color difference should be barely perceptible — the eye registers rhythm, not contrast

**Hover state (desktop):**
- Background: #F4F4F4
- Transition: 80ms
- No transform, no shadow, no color change on text

**Tap feedback (mobile):**
- Background: #EBEBEB
- Duration: 100ms, then release
- No ripple animation

---

### The hierarchy contract

The row has one visual hierarchy, and it must be maintained without exception:

```
Product name      — most visible (15px, 500 weight, near-black)
Insight line      — visible but subordinate (13px, 400 weight, gray)
Score chip        — legible at a glance (13px, 600 weight, contained)
Image             — present and recognizable (56px, contain crop)
Chevron           — suggests action, doesn't demand it (muted gray)
```

If any element competes with the product name for attention, fix it. The product name is always the first thing the eye reaches.

---

### Expanded row specification

**Animation:** max-height transition, 200ms ease-out. Do not use opacity fade — it reads as "content loading" rather than "content expanding."

**Inner padding:** 16px all sides, slightly more than collapsed padding (16px vs 14px) to signal a different mode

**Section separation within expanded row:** 12px vertical gap between sections. No dividers, no headings.

**Nutrition grid:**
- 5 fields only: קלוריות / חלבון / סוכר / שומן / נתרן
- 2-column layout on mobile: [label left] [value right]
- Label: 12px, #888888
- Value: 14px, 500 weight, #1A1A1A
- Units on the same line as value, same font, same weight
- Source: "ל-100 גרם" — appears once above the grid, not repeated per field

**Ingredient list:**
- Font size: 13px, #555555
- Line height: 1.6
- Max visible without interaction: 4 lines (~3 ingredients typically)
- "הצג הכל" link if ingredients > 4 lines (not a button — a text link, 12px, #888888)
- Verbatim from BSIP1 — no editing, no reformatting

**Data note:**
- Font size: 12px, #AAAAAA (very muted)
- 1 line, no overflow
- Example: "נתונים משופרסל. ייתכנו שינויים בין אריזות."

**Confidence indicator:**
- Text only: "נתונים מלאים" or "נתונים חלקיים"
- Font size: 12px
- Color: "מלאים" → #888888 / "חלקיים" → #B07000 (amber, no red)
- No icon, no badge

**Collapse behavior:** Tap anywhere in the expanded area to collapse. Chevron rotates back.

---

### What makes rows feel retail-native

Retail shelves present products with one clear hierarchy: the product name/brand is large, secondary info (price, weight) is smaller. Nothing competes with the product. Bari rows must recreate this at the information level.

The three specific behaviors that break shelf-native feel:
- Score chip larger than product name → fix: chip is always smaller
- Insight line bolder than product name → fix: insight line is always lighter weight
- Borders between rows → fix: alternating backgrounds only

---

## Deliverable 2 — Mobile Scroll Audit

### Scroll simulation: standard mobile (375px wide, 812px viewport)

A user opens the page. The experience unfolds in scroll stages:

**Stage 0 — Initial load (0px scroll)**  
The hero is visible. The product name and score chip appear without scrolling. The first row of the product table should be visible or partially visible. If the first product row is not visible at 0px scroll, the hero is too large.

**Target layout at 0px scroll:**
```
[0px]   Hero image start
[160px] Hero image end
[170px] Hero sentence (1–2 lines, ~40px)
[210px] Score chip
[240px] Hero bottom
[264px] Prologue start
[360px] Prologue end (3 sentences, ~96px)
[376px] TABLE HEADER (implicit) / first product row
[450px] First product row bottom
```

This means: the user sees part of the first product row before scrolling. That is the target.

**If hero + prologue > 400px total, products are invisible on load.** This is the key metric.

---

**Stage 1 — First scroll (200–400px scroll)**  
Products appear fully. User begins scanning. Score chips and insight lines are visible simultaneously. No interaction is required yet.

Scanning rhythm at this stage:
- The user's eye moves: image → product name → score chip → insight line, then down to next row
- This rhythm should be predictable and fast — 1–2 seconds per row
- If the insight line is long (wrapping) or heavy (too bold), it interrupts the scan rhythm

Risk at this stage: insight lines that don't fit in one line force the eye to pause longer than intended. This is why the 1-line clip is mandatory — the line must give up content before it breaks rhythm.

---

**Stage 2 — Mid scroll (400–1200px scroll)**  
The user is now scanning the full list. The filter button should be accessible without scrolling back to the top. Recommendation: make the filter button sticky on mobile (fixed position, bottom-right, appears after 300px scroll, disappears at methodology).

The filter button:
- "סינון" — 14px, #FFFFFF, #333333 background
- 44px height, 80px min-width
- 16px from right edge, 16px from bottom edge
- Appears on scroll, not on initial load (prevents competing with hero)
- Disappears when user reaches methodology section

---

**Stage 3 — Row expansion (any point during scroll)**  
The user taps a row. The row expands inline. The scroll position should not jump.

Risk: if the row expansion pushes content below the fold suddenly, the user feels disoriented. Mitigation: after expansion, scroll so that the top of the expanded row is 80px from the top of the viewport (smooth scroll, 200ms).

After expansion, "collapse" is tap anywhere in expanded area. The expanded row does not change visual position — it collapses in place.

---

**Stage 4 — Methodology (bottom of scroll)**  
Methodology should feel like it naturally ends the page — not like a section that demands reading. It should arrive quietly.

Risk: if methodology has a heading in large type, a box border, or an icon, it reads as a CTA or a new content section. The eye stops.

Required methodology treatment on mobile:
- No heading. No box. No border. No background color.
- Small type: 12px, #AAAAAA
- Top padding before methodology: 48px (generously separated from last product row)
- Methodology text is left-aligned, full-width, same margin as product rows

---

### Recommendations

| Issue | Fix |
|---|---|
| Products below fold on initial load | Hero total height ≤ 280px (mobile) |
| Scan rhythm interrupted | Insight line: 1 line, 13px, 400 weight always |
| User loses place after expansion | Auto-scroll to top of expanded row (200ms) |
| Filter inaccessible mid-scroll | Sticky "סינון" button: appears after 300px scroll |
| Methodology feels like a section | No heading, no box, 12px type, #AAAAAA |
| Ingredient list too long in expanded row | 4-line clip with "הצג הכל" text link |

---

## Deliverable 3 — Hero Density Audit

### Current risk

Heroes designed for desktop tend to overscale on mobile. Full-screen cinematic heroes create a problem specific to Bari: the product is the most important element on the page, but it doesn't appear until after the hero clears. Every pixel of hero height is a pixel of delay before products.

The hero must earn its height. It earns it by creating a moment of recognition — not by creating a cinematic experience.

---

### Recommended hero specification

**Mobile:**
```
Image container:     height: 180px, background: #F8F8F8, object-fit: contain
Vertical gap:        12px
Hero sentence:       font-size: 15px, line-height: 1.4, max 2 lines (~42px)
Vertical gap:        10px  
Score display:       font-size: 28px (number) / 22px (grade), weight: 600, color: #1A1A1A
Padding below score: 20px
Total hero height:   ~264px
```

**Desktop:**
```
Image container:     height: 240px (max), width: 200px, float or inline-block left
Hero sentence:       font-size: 17px, 1–2 lines
Score display:       font-size: 36px (number) / 28px (grade)
Total hero block:    max-height: 280px
```

---

### Score in hero vs. score in row

The hero score is the same data point as the row score chip. The difference is emphasis:

- **Hero score:** large (28–36px), standalone, communicates "this is the finding"
- **Row score chip:** small (13px), contained in chip, communicates "this is one data point among many"

These two contexts should NOT look identical. The hero score is large and unstyled (no chip container). The row chip is small and contained. If they look the same, neither has visual weight.

---

### Distance to first product: the critical measurement

The sequence is:
1. Hero image (180px mobile)
2. Hero sentence (~42px)
3. Score display (~40px)
4. Hero bottom padding (20px)
5. Prologue (~96px for 3 sentences)
6. Table gap (24px)
7. First product row top

Total: 402px. On a 812px viewport, the user sees the first product row at 402px from the top — approximately half the screen. This is acceptable.

If any element is added between the hero bottom and the first product row, it must be justified by the question: does this earn its height? Examples that do not earn their height:
- Section heading ("המוצרים" above the table) — remove
- Filter bar visible by default (collapsed filter button only)
- Category introduction text beyond 3 sentences — cut to 3 sentences

---

### Per-category hero adjustment

| Category | Image subject | Hero sentence type | Score context |
|---|---|---|---|
| חלב | Milk carton (recognizable brand) | Observation about the shelf | Most recognized product's score |
| מעדנים | מילקי cup (label-forward) | The icon paradox | 40/D — below expectations |
| לחם | Commercial שאור bread package | The fermentation gap | D-range score, recognizable brand |

In all three cases: the score creates surprise, not confirmation. If the hero product's score is expected (a health food brand with a B score), it is not the right hero. The hero earns attention through dissonance.

---

## Deliverable 4 — Insight-Line Density Audit

### The current problem

The מעדנים insight line set was written to demonstrate the full range of the spec. It succeeded as a demonstration but has too high a density of Type 2 (contradiction) lines to work as a production table.

When the user scrolls through a list where every third row contains a contradiction framed as "[claim], [counter-evidence]", the effect is:
1. The pattern becomes predictable — lines stop landing
2. The page starts reading as an accusatory list
3. The editorial energy becomes theatrical rather than calm

**The mix problem:** Too many contradiction lines at once create the feeling that every product is being caught doing something wrong. This is the opposite of calm shelf exploration — it is prosecutorial browsing.

---

### Required mix by proportion

Per every 10 visible product rows:

| Type | Target proportion | Notes |
|---|---|---|
| T1 — Composition fact | 50–60% | The default. Neutral, scannable, factual. |
| T2 — Contradiction | 20–30% | Reserved for the most structurally clear cases. |
| T3 — Position | 15–20% | Extremes and genuine rarities only. |

A page with 60 products should have approximately:
- ~33 T1 lines (composition facts)
- ~15 T2 lines (contradictions)
- ~12 T3 lines (position facts)

The current מעדנים set has approximately:
- ~25 T1 lines ✓
- ~25 T2 lines (too high — ~15 should be converted to T1)
- ~15 T3 lines ✓

---

### Lines to convert from T2 to T1

The following T2 lines in the current set rely on named comparisons to other products rather than standalone facts. They should be converted to T1 (specific composition observation).

| Current (T2) | Problem | Rewrite (T1 or T3) |
|---|---|---|
| "ציון נמוך ב-27 נקודות מ-GO" | Requires knowing GO | "תווית חלבון, 9 תוספים ברשימה" |
| "ציון קרוב למילקי הקלאסי" | Requires knowing מילקי's score | "שכבות שוקולד, הסוכר ברכיב השני" |
| "גרסת הגרסה הנמוכה ביותר בסדרה" | Redundant / vague | "הנמוכה בסדרת יופלה GO" (T3) |
| "ציון קרוב לממוצע הקטגוריה" | References internal statistic | "מעדן פרי קלאסי, ציון ממוצע" — or: drop the line and use just a composition fact |
| "קטגוריית ביניים" | Framework-adjacent, meaningless to consumer | Replace with specific composition fact |

---

### Strongest lines (retain as-is)

These lines represent the target. They are the reference points for the category.

| Line | Product | Type | Why it works |
|---|---|---|---|
| "26% פחות סוכר, 1.5 נקודות הפרש מהגרסה הרגילה" | מילקי עם 26% פחות סוכר | T2 | Two specific numbers. Contradiction without judgment. |
| "הגביע הכי מוכר בקטגוריה, הציון הנמוך בה" | מילקי בטעם שוקולד | T2 | Juxtaposes two verifiable facts. Reader does the work. |
| "10 גרם חלבון, 3 רכיבים עיקריים בלבד" | יופלה GO מועשר | T1 | Specific, short, positive — a rest from contradictions. |
| "להכנה ביתית — ציון גבוה ב-18 נקודות מהגביע המוכן" | פודינג אינסטנט | T2 | The paradox is complete in the line. |
| "ללא תוספים מזוניים מזוהים — נדיר בקטגוריה" | מעדן משמש | T3 | Names the rarity without calling other products bad. |
| "שלושה מייצבים, חומרי טעם וריח, עמילן מעובד" | מילקי טופ שוקולדה | T1 | Lists what is there. The density of the list is the finding. |

---

### Lines to rewrite

| Current line | Problem | Proposed rewrite |
|---|---|---|
| "מעדן פרי בלי תווית בריאות" | Vague, not verifiable | "מעדן תפוז — הסוכר ברכיב השלישי" |
| "פורמט נדיר בקטגוריה" (חצילים) | Position claim without number | "חציל כרכיב ראשון — יחיד בקטגוריה" |
| "קטגוריית ביניים" | Not consumer language | Replace with a specific T1 fact from the trace |
| "ציון קרוב לממוצע הקטגוריה" | Exposes aggregate data | Replace with ingredient observation |
| "גרסת הגרסה הנמוכה ביותר בסדרה" (GOדובדבן) | Clunky construction | "דובדבן — הנמוכה בסדרת GO" |
| "גביע קטן יותר, ציון זהה לגביע הגדול" (מיני מילקי) | Not useful observation | "מיני גרסה — אותו הרכב" |

---

### The quiet line principle

Not every product needs a striking line. Some products are editorially uninteresting — they score mid-range, have no strong contradiction, and have no position claim worth making. For these products, a quiet T1 line is the right answer.

Examples of acceptable quiet lines:
- "3% שומן, טעם מנגו" — (just what is stated)
- "הרכב דומה לגרסת הוניל"
- "5 גרם חלבון ל-100 גרם"

Quiet lines do not dilute the set. They provide rhythm. The contrast between a quiet T1 line and a sharp T2 line is what makes the T2 land. If every line is sharp, none of them are.

---

### Bread insight line density guidance

Bread has 81 products. The same mix rule applies: 50% T1, 25% T2, 20% T3.

The bread category's strongest T2 lines will cluster around:
1. The fermentation gap ("שאור בשם, שמרים תעשייתיים")
2. Fiber laundering ("'עשיר בסיבים' — אינולין מוסף")
3. Whole wheat naming ("'מלא' בשם — קמח לבן ברכיב הראשון")

There are approximately 10–15 products with genuine fermentation gap contradictions in the data. Use T2 for those. The remaining ~66 products get T1 (fiber content, ingredient simplicity, grain type) or T3 (category position facts).

---

## Deliverable 5 — Cross-Category Visual Consistency Audit

### What "same product" means

The three categories should pass this test: if a user moves from the milk page to the מעדנים page to the bread page, the UI should feel like they are browsing different shelves of the same well-edited store — not like they clicked from one website to another.

The test fails if:
- Row heights differ between categories
- Score chip styling differs
- Image crop rules differ
- Methodology placement or size differs
- Font choices differ

The test also fails if:
- One category feels more analytical (more data visible in collapsed row)
- One category feels more editorial (more text before products)
- One category feels more digital (more interactive elements)

---

### Per-category assessment

**חלב:**
- Small product set (~6 products) → the table is short, scrolls end quickly
- Risk: the brevity of the table creates pressure to add more elements (maps, comparison breakdowns) to "fill" the page
- This pressure should be resisted. A short, calm table is the milk standard. Do not pad it.
- Visual density: the lowest of the three categories — appropriate

**מעדנים:**
- 60+ products → long scrolling table
- Risk: the longer table creates more opportunities for inconsistent treatment (some rows with long ingredient overflow, some with unusual product names that wrap)
- The alternating background rhythm matters most here — it is the primary rhythm cue in a long list
- Score distribution is wider (26–70) than milk — score chips therefore communicate more information
- Visual density: medium, manageable with row rhythm spec applied

**לחם:**
- 81 products → longest table
- Risk: the fermentation filter dimension adds cognitive complexity not present in the other categories
- Risk: the bread data has more "degraded" products (INSUFFICIENT) — what happens to these rows? Recommendation: these should appear at the bottom of the table with a "נתונים לא מלאים" state — same row layout, but score chip replaced with "לא נוקד", insight line replaced with "אין מספיק מידע". They should NOT be hidden.
- Visual density: highest — needs the strictest application of the alternating background rhythm

---

### Unified design tokens

These values must be identical across all three categories. No category-specific overrides.

```
--row-height-mobile:        72px
--row-height-desktop:       80px
--row-padding-vertical:     14px
--row-padding-horizontal:   16px
--image-size:               56px
--image-border-radius:      6px
--image-background:         #F8F8F8
--chip-height:              28px
--chip-border-radius:       14px
--chip-background:          #F0F0F0
--chip-font-size:           13px
--chip-font-weight:         600
--chip-color:               #1A1A1A
--name-font-size:           15px
--name-font-weight:         500
--name-color:               #1A1A1A
--insight-font-size:        13px
--insight-font-weight:      400
--insight-color:            #666666
--row-bg-odd:               #FFFFFF
--row-bg-even:              #F9F9F9
--hover-bg:                 #F4F4F4
--methodology-font-size:    12px
--methodology-color:        #AAAAAA
--hero-image-height-mobile: 180px
--hero-sentence-font-size:  15px
--hero-score-font-size:     28px
```

Any deviation from these values requires explicit approval and a documented reason.

---

### Where categories legitimately differ

These differences are data-driven, not design decisions. They are expected and correct.

| Element | חלב | מעדנים | לחם |
|---|---|---|---|
| Table row count | ~6 | ~60 | ~81 |
| Filter dim 3 | none | — | תסיסה |
| Highlighted pair | yes | yes | yes |
| Grade range | B–D | E–B | D–A |
| Insight line subject | fat / pasteurization | additives / protein | fiber / fermentation |

These differences manifest in the content — not in the design system.

---

### The one design divergence risk

**Bread's fermentation filter requires explanation.** The label "עם מחמצת" is clear. "ללא מחמצת מזוהה" requires a tooltip because the user may think it means "has no sourdough" rather than "no fermentation signal detected."

The tooltip should be:
- Triggered by a ⓘ icon next to the filter label (not on the filter option itself)
- One sentence: "המוצר לא הכיל סמנים של תסיסת מחמצת ברשימת הרכיבים שנבדקה"
- Dismiss on tap anywhere
- This is the only tooltip in the entire product. It should not multiply.

If a second tooltip appears anywhere in the product for any reason — in milk, מעדנים, or bread — treat it as a drift event.

---

### Quieter = better: the final test

Before any UI element ships, apply this test:

> If this element were removed from the page, would the page feel incomplete or would it feel cleaner?

Elements that make the page feel cleaner when removed: remove them.

Examples of elements that consistently make pages feel cleaner when removed:
- Section headings ("המוצרים", "הסינון", "על הנתונים")
- Decorative dividers between table and methodology
- Score color coding (even subtle)
- Explainer text before the first product row
- Filter count badges

The product row is the product. Everything else is scaffolding.

---

## Implementation Priority Order

Apply in this sequence:

1. **Design tokens** — establish the shared token file. All three categories reference it. No overrides without approval. This is the single action most likely to create visual coherence immediately.

2. **Row rhythm** — apply the row specification to all three categories simultaneously. Verify row height, image size, chip design, and insight line weight are identical.

3. **Hero density** — enforce the 280px mobile maximum across all three heroes. Verify score is immediately visible on load with no animation.

4. **Insight line cleanup** — convert overweight T2 lines in מעדנים to T1. Verify mix ratios. Run grammar test on all lines.

5. **Mobile scroll check** — verify product rows appear before 400px scroll position in all three categories.

6. **Methodology treatment** — confirm no heading, no box, 12px type, #AAAAAA color across all three categories.

7. **Bread fermentation tooltip** — implement the single tooltip for "ללא מחמצת מזוהה." Confirm no other tooltips exist anywhere in the product.
