# Bread Blog Handoffs — v3 Editorial Rebuild
**Date:** 2026-05-26
**Data source:** `bread_retail_003` / curated retail bread dataset  
**Category scope:** 256 products scanned, 81 with enough data for reliable analysis, 31 selected for comparison display  
**Replaces:** all prior bread blog handoffs, including v2

---

## Why v2 Failed

The previous handoff produced pages that were structurally wrong even when the tone was roughly correct.

The problem was not color, spacing, or component polish.

The problem was editorial architecture:

- the shelf did not feel present
- products were treated like the article instead of evidence inside the article
- findings did not accumulate
- uncertainty did not recur often enough
- comparison moments were too sparse and too large
- the rhythm defaulted to CMS behavior: intro -> card grid -> table

This version fixes that.

---

## Core Rule

**Products are not the article. Products are evidence inside a category investigation.**

The protagonist of every bread blog is the supermarket shelf itself:

- the breadth of the category
- the patterns that emerged from many products
- the contradictions between naming and composition
- the zones where Bari could and could not verify

If a draft feels like a set of product cards, it has failed.

---

## Editorial Goal

All three bread blogs must feel like:

- investigative supermarket shelf analysis
- modern consumer journalism
- pattern-based reporting from a real dataset
- category storytelling with products as proof points

They must **not** feel like:

- SaaS CMS pages
- product collections
- wellness lifestyle posts
- "top products" lists
- recommendation pages

---

## Non-Negotiable Signals

Every article must make the reader feel, repeatedly, that:

- a large real shelf was examined
- many products were considered, not only the featured ones
- findings emerged progressively
- some things were verified and some were not
- the article is about patterns first, products second

That means the article must continuously surface:

- shelf context
- recurring statistics
- supporting product mentions
- compact comparisons
- uncertainty reminders

---

## Universal Architecture

Every bread article must follow this editorial spine.

### 1. Hero thesis

Open with one sharp consumer-facing observation.

Not a generic intro.
Not a mission statement.
Not "we analyzed bread products."

The hero must state the article's thesis in one line:

- what looked simple but turned out surprising
- what looked strong but turned out mixed
- what the shelf taught us that packaging alone would not

### 2. Shelf context, immediately

The article must establish the shelf before discussing any individual product.

This section must quickly ground:

- `256` scanned
- `81` validated for reliable analysis
- `46%` without enough information for a reliable score
- what breadth the category includes
- why the shelf matters to ordinary shoppers

The reader must understand that this is a category investigation, not a feature on a handful of products.

### 3. Investigation progression

The article must progressively reveal:

1. the assumption most shoppers would make
2. what the shelf data showed first
3. where the pattern broke
4. which products acted as the clearest evidence
5. where Bari could not verify enough
6. what the category-level takeaway actually is

The flow must feel like an investigation unfolding, not a component stack.

### 4. Evidence distribution

Each article must use all four layers of evidence:

- **hero evidence products:** `4-6` max
- **supporting inline mentions:** `8-15`
- **compact comparison moments:** `3-5`
- **continuous shelf observations:** recurring throughout

The shelf should always feel larger than the currently visible product.

### 5. Closing logic

The article must end by returning to the category, not by ending on a product.

The closing section should answer:

- what the shelf actually teaches
- what the reader should now understand differently
- where Bari is still uncertain

No ending should read like a product recommendation.

---

## Required Building Blocks

These are editorial primitives, not decorative UI widgets.

### A. ShelfContextBand

**Purpose:** Establishes scale and uncertainty immediately below the hero.

**Required contents:**

- `256 מוצרים נסרקו`
- `81 עם מספיק נתונים`
- `46% ללא ציון מהימן`
- `מדף שופרסל · מאי 2026`

**Rules:**

- always appears directly after the hero thesis
- compact and typographic, not celebratory
- must read like framing, not like stats decoration

### B. InsightInterruptionBlock

**Purpose:** Interrupt narrative flow with an authored editorial finding or uncertainty point.

**Required variants:**

- `מה הפתיע אותנו`
- `איפה הנתונים נחלשו`
- `פער בין השם לרכיבים`
- `מה לא הצלחנו לאמת`

**Rules:**

- use `2-4` per article
- each block must interrupt an active line of reasoning
- each block must carry a precise claim, not generic summary text
- these are the main rhythm breakers in the article

### C. CompactComparisonStrip

**Purpose:** A dense comparison moment. Never a giant card cluster.

**Format:**

- `2-3` rows max
- short editorial line above the strip
- short takeaway line below the strip
- dense facts inside the strip: score, fermentation, fiber, base grain, confidence, or one decisive evidence cue

**Rules:**

- `3-5` per article
- no heavy visual chrome
- comparison must serve the current section argument
- do not place all strips together; distribute them across the investigation

### D. EvidenceCase

**Purpose:** A focused product evidence block for a hero evidence product.

**Required contents:**

- small image only
- product name
- score and confidence
- one evidence line
- one Bari observation line tied to the article's argument

**Rules:**

- smaller than a feature card
- should feel like proof in a dossier
- not a promotional card
- do not place more than two large EvidenceCases back-to-back without narrative in between

### E. InlineEvidenceMention

**Purpose:** Keep the shelf alive inside paragraphs.

**Rules:**

- product names should appear naturally inside prose
- the mention must advance a finding, contrast, or uncertainty
- avoid isolated "also worth mentioning" filler

Example shape:

> `לחם אחיד פרוס קל` קיבל `73`, בזמן ש`לחם מחמצת אגוזים צימוקים` נשאר עם סיפור פרימיום חזק יותר מהמבנה שאפשר היה לאמת.

### F. ShelfStatisticCallout

**Purpose:** Recurring category-level reminder that the article is backed by a large shelf analysis.

**Examples:**

- `46% ללא ציון`
- `רק 81 מתוך 256`
- `מתוך 31 המוצרים שהוצגו`
- `בחלק מהמוצרים...`

**Rules:**

- use `2-3` per article
- should recur in different stages, not only near the top
- must reinforce the current point, not repeat the same stat without purpose

### G. SectionFinding

**Purpose:** Opens a section with an authored editorial sentence instead of a generic H2.

**Rules:**

- statement first, then a short scope note
- use when a finding is the reason the section exists
- not every section needs one, but every article needs several

---

## Density And Rhythm Rules

### Evidence cadence

The reader should never move through more than `140-180` words without at least one of the following:

- a named product
- a shelf statistic
- a comparison strip
- an insight interruption
- a category uncertainty note

### Visual rhythm

The page must avoid repeating identical blocks.

Use a mixed editorial cadence:

- short narrative section
- insight interruption
- compact comparison strip
- denser narrative
- evidence case pair
- shelf statistic callout
- micro reference section

Not:

- four equal cards
- then one table
- then three generic sections

### Spacing

The page should feel dense and authored.

- tighten vertical spacing between intro, evidence, and table sections
- do not leave large dead space around product evidence blocks
- tables and comparison strips should feel embedded in the article, not appended below it

### Composition

Allow:

- asymmetry
- short dense narrative passages
- interruptions
- alternating full-width and narrower sections

Avoid:

- perfect repeated grids
- decorative emptiness
- overly balanced landing-page symmetry

---

## Language Rules

Always write with:

- restraint
- observational specificity
- consumer clarity
- honest uncertainty

Never write:

- "best breads"
- "recommended"
- "top picks"
- "healthy choice"
- moralistic food language
- internal technical language

Preferred frame:

- "what the shelf showed"
- "what could be verified"
- "where the pattern held"
- "where the claim weakened"

---

## Article 1 Blueprint

# הלחם היומיומי שלכם

**URL slug:** `/blog/bread-everyday`  
**Core feeling:** mainstream products analyzed seriously  
**Editorial mode:** practical, shelf-familiar, mildly surprising  
**Main thesis:** simple does not automatically mean weak, and ordinary products deserve the same investigative reading as premium ones

### Hero thesis

The hero must say some version of:

> המדף היומיומי נראה פשוט, אבל דווקא בו התברר שהפער בין שם, מבנה ושקיפות מורכב יותר ממה שנדמה.

This article must feel immediately familiar to anyone who shops for ordinary bread.

### Category protagonist

The protagonist is the mainstream shelf:

- sliced bread
- branded everyday loaves
- pitas
- familiar products people buy without deliberation

### Hero evidence products

Use `4-6` from this pool:

- `לחם אחיד פרוס קל`
- `לחם ברמן אקטיב`
- `לחם אנג'ל חיטה מלאה`
- `לחם אנג'ל חצי מלא`
- `פיתה פיתה`
- `לחם חיטה מלא לילדים`

These are not a gallery. They are anchors inside the article.

### Supporting reference pool

Use `8-12` inline mentions from this wider pool:

- `לחם ירוק מקמח מלא`
- `לחם דגנים מלא`
- `לחם מחמצת אגוזים צימוקים`
- `לחם מחמצת קמח מלא`
- `לחם שיפון מלא מסטמכר`
- additional mainstream or adjacent products as needed

### Required comparison moments

Use `3-4` comparison strips:

1. `לחם אחיד פרוס קל` מול `לחם ברמן אקטיב`
2. `לחם אנג'ל חיטה מלאה` מול `לחם אנג'ל חצי מלא`
3. everyday bread מול one adjacent premium-looking product
4. scored mainstream product מול no-score mainstream product

### Required progression

#### Section 1 — The shelf first

Open with shelf context, not product hero cards.

Establish:

- this is where most actual buying happens
- many everyday products were scanned
- data availability itself shaped what Bari could say

Required interruption after this section:

- `InsightInterruptionBlock: איפה הנתונים נחלשו`

#### Section 2 — Simple does not mean weak

This is the article's central turn.

Show that:

- a straightforward product can still look structurally coherent
- the absence of grand claims can make interpretation easier
- "simple" is not the same as "bad"

Use:

- one EvidenceCase pair
- one CompactComparisonStrip
- several inline mentions of familiar products

#### Section 3 — Familiar names, real differences

Show that ordinary shelf products are not interchangeable.

This section must include:

- brand-internal contrast
- differences in fiber and structure
- at least one example where naming implies more than the data supports

Use:

- the `אנג'ל חיטה מלאה` / `אנג'ל חצי מלא` comparison
- one recurring shelf statistic

#### Section 4 — Where the shelf goes quiet

This section is about uncertainty.

It must explain:

- why products like pita still matter even when they cannot be scored reliably
- why lack of data is itself a consumer finding
- how uncertainty changes the interpretation of the category

Required interruption:

- `InsightInterruptionBlock: מה לא הצלחנו לאמת`

#### Section 5 — What this shelf teaches

End with category learning, not a product wrap-up.

The closing must say:

- mainstream bread deserves serious reading
- simple structure can be more credible than louder branding
- the consumer should read clarity and transparency before branding language

### Visual rhythm for Article 1

Use this cadence:

```text
[Hero thesis]
[ShelfContextBand]
[Narrative: mainstream shelf matters]
[Insight block: data weakness]
[Narrative]
[Comparison strip]
[Evidence case pair]
[Narrative with inline references]
[Shelf statistic callout]
[Comparison strip]
[Narrative]
[Insight block: what we could not verify]
[Micro shelf references]
[Closing category takeaway]
```

### What Article 1 must feel like

- practical
- surprising in a restrained way
- grounded in everyday shopping behavior

It must not feel like:

- a premium bread article in disguise
- a list of ordinary products

---

## Article 2 Blueprint

# המוצרים שבלטו בניתוח

**URL slug:** `/blog/bread-standouts`  
**Core feeling:** curated investigative dossier  
**Editorial mode:** measured, credible, restrained  
**Main thesis:** these are the strongest validated examples inside the shelf we actually analyzed, not "the best breads"

### Hero thesis

The hero must say some version of:

> המוצרים שבלטו כאן לא זכו כי הם נשמעו טוב, אלא כי הנתונים שלהם החזיקו טוב יותר מהמדף שסביבם.

### Category protagonist

The protagonist is not the winners.  
The protagonist is the standard of evidence:

- which products held up under scrutiny
- what kinds of structure repeated among standouts
- what stayed out because Bari could not validate enough

### Hero evidence products

Use `4-6` from this pool:

- `לחם ירוק מקמח מלא`
- `לחם מחמצת קמח מלא`
- `לחם שיפון מלא מסטמכר`
- `לחם מחמצת גרעינים`
- `לחם שיפון קל`
- `לחם דגנים מלא`
- `לחם חיטה מלא לילדים`

### Supporting reference pool

Use `8-12` inline mentions from:

- near-miss products
- adjacent mainstream products that help establish contrast
- products excluded for transparency reasons

At least one supporting reference should remind the reader that some strong-sounding products were excluded because the data was not enough.

### Required comparison moments

Use `3-4` compact strips:

1. two strongest grain-structure examples
2. two fermentation-backed examples
3. standout vs near-miss
4. validated standout vs excluded high-promise product

### Required progression

#### Section 1 — What "stood out" means here

Define the standard before showing products.

This section must establish:

- no recommendation framing
- no national ranking claim
- validation matters more than prestige

Required interruption:

- `InsightInterruptionBlock: מה הפתיע אותנו`

#### Section 2 — The recurring structure of standouts

This section identifies the pattern:

- clearer base grain
- stronger or more coherent fiber story
- in some cases verified fermentation

Use:

- one comparison strip
- one EvidenceCase pair
- multiple inline mentions

#### Section 3 — Different ways to stand out

This section prevents the article from collapsing into one formula.

It must show that standouts are not identical:

- some are strong through whole-grain clarity
- some through verified fermentation
- some through unusually coherent composition in an unexpected category

Use:

- another comparison strip
- one SectionFinding

#### Section 4 — Who almost made it

This is essential for credibility.

Show:

- products that stayed close
- products that sounded strong but lacked enough validation
- why exclusion matters to the trustworthiness of the article

Required interruption:

- `InsightInterruptionBlock: איפה הנתונים נחלשו`

#### Section 5 — What the dossier actually says

The closing should leave the reader with:

- a sense of pattern, not podium
- confidence in the restraint of the method
- understanding that standout status depends on what was verifiable

### Visual rhythm for Article 2

Use this cadence:

```text
[Hero thesis]
[ShelfContextBand]
[Narrative: what "stood out" means]
[Insight block: surprise pattern]
[Comparison strip]
[Evidence case pair]
[Narrative]
[Section finding]
[Comparison strip]
[Micro shelf references]
[Narrative: near-misses and exclusions]
[Insight block: transparency warning]
[Dense supporting table or strip]
[Closing category takeaway]
```

### What Article 2 must feel like

- curated
- restrained
- evidence-heavy
- careful with claims

It must not feel like:

- "best breads"
- awards content
- editorialized shopping advice

---

## Article 3 Blueprint

# מחמצת, כוסמין ו"לחמי בריאות"

**URL slug:** `/blog/bread-wellness-gap`  
**Core feeling:** expectation versus composition  
**Editorial mode:** strongest investigative piece of the three  
**Main thesis:** the premium signal is real, but it does not always come from where the name directs the shopper to look

### Hero thesis

The hero must say some version of:

> קטגוריית "לחמי הבריאות" לא מתפרקת לשקר מול אמת. היא מתפרקת למנגנונים שונים מאוד שמסתתרים מאחורי מילים דומות.

### Category protagonist

The protagonist is the tension inside the wellness shelf:

- expectation versus structure
- naming versus ingredient reality
- verified fermentation versus named fermentation
- white spelt versus whole-grain assumption
- seed halo versus actual base grain
- strong numbers versus unclear mechanism

### Hero evidence products

Use `5-6` from this pool:

- `לחם טחינה פרוס`
- `לחם דגנים לייט`
- `לחם כוסמין לבן`
- `לחם מחמצת מכוסמין`
- `לחם מחמצת אגוזים צימוקים`
- `לחם מחמצת קמח מלא`

### Supporting reference pool

Use `10-15` inline mentions from:

- `לחם לס פרוס קיטו`
- `לחם מחמצת גרעינים`
- `לחם שיפון מלא מסטמכר`
- `לחם ירוק מקמח מלא`
- `לחם ברמן אקטיב`
- additional verified-fermentation or wellness-ambiguity examples

### Required comparison moments

Use `4-5` compact strips:

1. `לחם מחמצת קמח מלא` מול `לחם מחמצת מכוסמין`
2. `לחם טחינה פרוס` מול `לחם דגנים לייט`
3. `לחם כוסמין לבן` מול stronger whole-grain control
4. seed-heavy premium-looking product מול structurally clearer product
5. optional uncertainty strip for high-fiber / unclear-source products

### Required progression

#### Section 1 — The category promise

Open with the language of the shelf:

- sourdough
- spelt
- grains
- wellness
- premium signaling

Then show why this shelf requires the slowest reading.

#### Section 2 — "מחמצת בשם בלבד"

This is the first major investigative turn.

The section must distinguish:

- verified fermentation in ingredients
- fermentation as branding language

Required interruption:

- `InsightInterruptionBlock: פער בין השם לרכיבים`

Use:

- one comparison strip
- recurring mention that the check is in the ingredients, not in the product name

#### Section 3 — Spelt is not automatically whole grain

This section must explicitly dismantle the shopper assumption that "spelt" equals "better by definition."

Show:

- white spelt versus whole-grain expectation
- why naming alone is not enough
- how current dataset examples complicate the category

Required shelf statistic recurrence:

- one recurring callout or sentence reminding the reader that only part of the shelf could be validated reliably

#### Section 4 — Seed halo and wellness ambiguity

This section must feel like investigative shelf reporting, not nutrition preaching.

Show:

- why seeds on packaging or in the name can create a health halo
- why the base grain still matters more
- how products can look premium while being structurally mixed

Required interruption:

- `InsightInterruptionBlock: מה הפתיע אותנו` or `מה לא הצלחנו לאמת`

#### Section 5 — Strong scores, different mechanisms

This section must explain that:

- not all high scores mean the same thing
- some strong products are strong through grain structure
- some through fermentation
- some through a different composition mechanism altogether

Use:

- `לחם טחינה פרוס` as a teaching case
- one comparison strip against a more whole-grain-anchored product

#### Section 6 — What this shelf actually teaches

The article must close by clarifying that:

- premium exists, but unevenly
- names guide expectations more aggressively than they guarantee structure
- Bari is tracking verifiable mechanisms, not accepting premium language at face value

End on the category, not on a hero product.

### Visual rhythm for Article 3

Use this cadence:

```text
[Hero thesis]
[ShelfContextBand]
[Narrative: wellness shelf promise]
[Insight block: name vs ingredients]
[Comparison strip]
[Narrative]
[Shelf statistic callout]
[Evidence case pair]
[Narrative]
[Comparison strip]
[Insight block: what surprised us / what weakened]
[Micro shelf references]
[Comparison strip]
[Narrative: strong scores, different mechanisms]
[Insight block: what we could not verify]
[Closing category takeaway]
```

### What Article 3 must feel like

- investigative
- shelf-specific
- tension-driven
- highly authored

It must not feel like:

- a wellness explainer
- a sourdough appreciation piece
- a collection of premium products

---

## Comparison Placement Logic

Comparison strips must not cluster together.

Distribute them according to the investigation:

1. early comparison: challenge the shopper's first assumption
2. middle comparison: show contradiction or split inside the category
3. later comparison: clarify what the broader pattern means
4. optional final comparison: expose uncertainty or near-miss logic

Each strip should do one of four jobs:

- clarify a pattern
- expose a mismatch
- separate two similar-looking products
- explain why one product is evidence and another is only suggestive

---

## Evidence Distribution Logic

### Hero evidence products

Use `4-6` maximum.

These are the products that receive dedicated visual treatment.
They must appear because they prove something essential, not because they are famous.

### Supporting references

Use `8-15` inline mentions.

These mentions are how the shelf stays alive.
They prevent the article from collapsing into only a few visible products.

### Comparison moments

Use `3-5`.

Short, dense, specific.
Never giant card rows.

### Shelf-level observations

Must recur throughout.

Examples:

- "מתוך 256 מוצרים..."
- "רק 81..."
- "בחלק מהמוצרים..."
- "דווקא בקטגוריה הזו..."

---

## Visual Composition Rules

These rules must be explicit because v2 failed here.

### Do

- alternate narrative widths
- interrupt body text with insight blocks
- use compact strips instead of grids
- let some sections be mostly text and others mostly evidence
- keep images smaller than product-card defaults
- make observations and context stronger than visual product presence

### Do not

- render a grid of equal product cards near the top
- place all hero evidence products in one uninterrupted block
- leave large whitespace between intro, evidence, and tables
- use product blocks as decoration
- let the article look component-led instead of authored

### One hard rule

If the page reads as "hero -> four cards -> table", the implementation failed.

---

## Universal Closing Disclosure

Every article must end with the same disclosure block:

> הניתוח מבוסס על מדף שופרסל (מאי 2026). 256 מוצרים נסרקו, 81 כללו מספיק נתונים לניתוח מהימן. זהו ניתוח של מדף שופרסל בלבד — לא סקר שוק ישראלי מלא. הציונים מבוססים על נתוני מדף זמינים, לא על בדיקת מעבדה.

---

## Hard Stops

Do not do any of the following:

- build the page around product cards
- write "best breads"
- turn the article into recommendations
- hide confidence or uncertainty language
- separate shelf statistics from the narrative for too long
- allow more than one identical evidence grid in the same article

---

## Final Cursor Brief

These three handoffs define **article architecture**, not just themes.

Cursor must understand that:

- the shelf is the protagonist
- products are evidence
- comparisons are compact and recurring
- insight interruptions are part of the reporting rhythm
- uncertainty is editorially visible
- density matters as much as styling

Do not default to generic blog structure.
Do not open with a grid of product cards.
Do not let the article feel like a component system rendering content.

Build the pages so they read like a modern investigative publication analyzing supermarket shelves.

---

*Bread Blog Handoffs v3 — 2026-05-26*  
*Primary dataset: curated retail bread dataset used by Bari's bread comparison and bread editorial routes*  
*Route targets: `/blog/bread-everyday`, `/blog/bread-standouts`, `/blog/bread-wellness-gap`*
