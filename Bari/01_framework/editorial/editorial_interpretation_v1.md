# Bari Editorial Interpretation Spec v1

**Purpose:** Rules for generating insight lines that feel intelligent, shelf-native, and consumer-readable — not algorithmic.

This spec governs how BSIP observations become editorial language. It does not change scoring. It changes how scored products are described.

---

## The Four-Level Insight Spectrum

Every insight line sits at one of four levels. **All published lines must reach Level 3 or 4.**

| Level | Definition | Example | Publish? |
|-------|------------|---------|----------|
| **1 — Raw Metric** | One number or fact, no interpretation | "18 גרם סוכר" | Only if number = insight |
| **2 — Benchmarked Metric** | Comparison to average or another product | "יותר סוכר מהממוצע" | Only if comparison = surprise |
| **3 — Structural Pattern** | Two observed facts creating a meaningful pattern | "מתיקות גבוהה לצד רשימת רכיבים ארוכה" | Yes |
| **4 — Compositional Character** | Describes what the product fundamentally IS | "מבוסס יותר על מרקם ומתיקות מאשר על חומרי גלם פשוטים" | Yes |

### When Level 1 or 2 is acceptable

Level 1 is acceptable only when the number itself carries the surprise:
- "26% פחות סוכר, 1.5 נקודות הפרש מהגרסה הרגילה" — the gap between the two numbers IS the insight.
- "10 גרם חלבון, 3 רכיבים עיקריים בלבד" — the combination of high protein and low ingredient count IS the structural insight.

Level 2 is acceptable only if the benchmark reveals something a shopper would not expect:
- "ללא חלב, ציון גבוה ממרבית מוצרי החלב" — the benchmark is surprising.
- "ציון נמוך מהממוצע" without a reason — not acceptable. Upgrade.

---

## The Shelf Test

Before publishing any insight line, ask:

> **Would a shopper at the shelf find this interesting — and does it change how they look at the product?**

- "Yes, and it makes me see the product differently" → publish
- "That's obvious from the label" → too weak, upgrade
- "I don't know what that means" → ontology leak, rewrite in consumer language
- "So what?" → no observation made, rewrite

---

## Character Rule

The strongest lines describe what a product IS, not what it contains.

| What it contains | What it IS |
|-----------------|------------|
| "שלושה מייצבים" | "המרקם בנוי על מייצבים — לא על ריכוז חלב" |
| "0.7% שומן, חומרי טעם וריח" | "הנמכת השומן הגיעה עם הוספת טעמי עזר" |
| "ממתיקים מלאכותיים" | "הסוכר הוחלף בממתיקים — התשתית לא השתנתה" |

The "what it IS" framing describes a trade-off, a production decision, or a gap between positioning and composition. The "what it contains" framing recites a fact.

---

## Anti-Pattern Library

Eight patterns that consistently produce Level 1–2 lines. Detect → upgrade.

### AP-1: Score Narration
**Pattern**: "ציון נמוך/גבוה בין מוצרי [category]"
**Why weak**: Explains the score, not the product. Every product has a position — the line must explain it.
**Upgrade formula**: Name what structural difference drives the position.
> OLD: "ציון נמוך בין מוצרי החלבון"
> NEW: "חלבון על האריזה, תשתית מעובדת יותר מ-GO"

### AP-2: Label Echo
**Pattern**: "[ingredient] בשם, [same ingredient or synonym] ברשימת הרכיבים"
**Why weak**: Tautological. Of course the named ingredient is in the list.
**Exception**: Use this pattern ONLY when the named ingredient is a functional claim (protein, calcium, fermentation) and the ingredient form reveals a gap between claim and delivery.
> VALID: "חלבון על האריזה, מגיע מחלבון חלב מעובד — לא מריכוז גולמי"
> WEAK: "תות בשם, תות ברשימת הרכיבים"

### AP-3: Empty Benchmark
**Pattern**: "ציון קרוב/נמוך/גבוה לממוצע/בקטגוריה/בסדרה" with no structural reason
**Why weak**: The category average is 43/D. Saying a product is average gives the reader nothing.
**Upgrade formula**: Say WHY it's average — what does it have and what does it lack.
> OLD: "ציון קרוב לממוצע הקטגוריה"
> NEW: "חלבון סביר, מרקם מעובד — מיקום ממוצע מסיבה ממוצעת"

### AP-4: Metric Gap Without Mechanism
**Pattern**: "ציון נמוך ב-X נקודות מ-Y"
**Why weak**: The gap is known from the score. The insight line should explain the gap, not repeat it.
**Exception**: If the GAP NUMBER reveals the paradox (e.g., "26% פחות סוכר, 1.5 נקודות הפרש" — the tiny gap is the insight).
**Upgrade formula**: Name what was added or changed between Y and this product.
> OLD: "ציון נמוך ב-12 נקודות מ-GO"
> NEW: "GO עם טעם אפרסק — הוסיפו סוכר ועמילן, איבדו 12 נקודות" (here the number supports, not carries)

### AP-5: Format Description
**Pattern**: "[brand] בפורמט [format]"
**Why weak**: Describes packaging, not composition.
**Upgrade formula**: If the format change drove a composition change, name the change.
> OLD: "יופלה בפורמט מוצצת"
> NEW: "פורמט מוצצת, תשתית שונה מ-GO — הציון מגלה שזה מוצר שונה"

### AP-6: Additive List
**Pattern**: "[additive A], [additive B], [additive C]"
**Why weak**: Reads like an audit, not an interpretation. A shopper doesn't know what E-numbers mean.
**Upgrade formula**: Identify what functional role those additives play.
> OLD: "שלושה מייצבים, חומרי טעם וריח, עמילן מעובד"
> NEW: "המרקם בנוי על שלושה מייצבים — לא על ריכוז חלב"

### AP-7: Rarity Without Content
**Pattern**: "הרכב יוצא דופן/נדיר בקטגוריה" alone
**Why weak**: Everything unusual is unusual. The insight is WHY it's unusual and what that means.
**Exception**: "ללא תוספים מזוניים מזוהים — נדיר בקטגוריה" works because the rarity claim has structural content.
> VALID: "ללא תוספים מזוניים מזוהים — נדיר בקטגוריה"
> WEAK: "הרכב יוצא דופן לקטגוריה"

### AP-8: The "ממוצע" Filler
**Pattern**: "ציון ממוצע" as the entire observation
**Why weak**: Editorial silence. If there's nothing specific to say, the insight line should be left empty (empty string renders no slot) rather than publishing a non-observation.
**Upgrade formula**: Find the one specific structural fact that explains the middling position.
> OLD: "ציון ממוצע בקטגוריה"
> NEW: "חלבון סביר, מייצב אחד — מיקום ממוצע מסיבה ברורה"

---

## Repetition Suppression Rules

Per category, across the full product list:

| Pattern | Maximum appearances |
|---------|---------------------|
| "ציון נמוך ב-X נקודות מ-Y" | 2 |
| "הנמוכה/הגבוהה ביותר ב-[scope]" | 2 |
| "[ingredient] בשם, [X] ברשימת הרכיבים" | 3 |
| "נדיר בקטגוריה" | 1 |
| "אותה תשתית" | 3 (max 1 per cluster) |
| Any identical phrase | 0 (no exact phrase repeats) |
| Any structural template in 3+ consecutive rows | 0 |

The rhythm rule from insight_line_spec_v1 applies: after 2 consecutive T2 lines (position/comparison), next must be T1 (fact) or T3 (contradiction).

---

## Category Shelf Lenses

Shelf lenses define the 3–5 questions a shopper naturally asks on a specific shelf. They frame editorial reasoning — not scoring categories.

Each lens is a real shopper question expressed as a Hebrew concept word. Products are described through these lenses, not through framework vocabulary.

---

### מעדנים — 5 Lenses

| Lens | Hebrew | Shopper question | Observable signal |
|------|--------|------------------|-------------------|
| מבנה פשוט | Simple structure | "Is this made from recognizable things?" | Ingredient count ≤ 5, no E-numbers |
| חלבון בפועל | Real protein | "Is there actual protein, or just the word?" | Protein source is milk/whey/casein, ≥ 8g/100g |
| מתיקות נשלטת | Controlled sweetness | "Is it sweet by category design, or over-engineered sweet?" | Sugar below category median (13g), no sweeteners |
| בסיס חלב נקי | Clean dairy base | "Is milk the foundation, or diluted?" | Milk as first ingredient, no water/starch in top 3 |
| ללא הנדסת מרקם | No texture engineering | "Was the texture built from dairy, or from stabilizers?" | Additive marker count ≤ 1 |

**Application notes:**
- מבנה פשוט is the most visible lens. When a product passes it, the insight line should note the rarity.
- חלבון בפועל drives the biggest contradictions — protein-labeled products often score D because they fail this lens.
- מתיקות נשלטת separates "dessert that is sweet" (expected) from "product engineered to maximize perceived sweetness."
- ללא הנדסת מרקם is the lens that separates יופלה GO (milk protein creates texture) from מילקי (four stabilizers create texture).

---

### לחם — 5 Lenses

| Lens | Hebrew | Shopper question | Observable signal |
|------|--------|------------------|-------------------|
| תסיסה אמיתית | Real fermentation | "Is this actual sourdough?" | Fermentation markers in ingredients: "מחמצת", "שאור", confirmed lactic fermentation |
| דגן שלם בפועל | Actual whole grain | "Is the whole grain the base, or a badge?" | Whole grain flour as first ingredient; not added as minor % |
| קצר ברכיבים | Short ingredient list | "Does this read like bread?" | ≤ 6 ingredients total |
| ללא שיפורי קמח | No flour improvers | "Is the flour standing alone?" | No emulsifiers (E471, E472, DATEM), no enzymes, no lecithin except sunflower |
| קמח כבסיס בלבד | Flour as the only base | "Is there one flour, or a blend designed to look better?" | Single flour type first; not wheat + bran + color additives |

**Application notes:**
- תסיסה אמיתית is the לחם equivalent of חלבון בפועל: the most commercially manipulated claim.
- ללא שיפורי קמח is what separates artisan-formula from industrial-formula even when fiber content is identical.
- Insight lines on לחם products should reference lenses 1 and 3 most often — these are the most legible to shoppers.

---

### דגני בוקר — 3 Lenses (preview)

| Lens | Hebrew | Shopper question |
|------|--------|------------------|
| יחס סוכר/דגן | Sugar-to-grain ratio | "How much of this is sweetness vs. grain?" |
| גרסה מלאה אמיתית | Real whole grain | "Is whole grain the base or the badge?" |
| בסיס לפני התוספות | Base before add-ins | "What is the grain, stripped of coatings and flavors?" |

---

### גבינות לבנות / קוטג׳ — 3 Lenses (preview)

| Lens | Hebrew | Shopper question |
|------|--------|------------------|
| שמנת כבסיס | Cream as base | "Is this fresh dairy, or cream-supplemented?" |
| חלבון ריכוז | Protein from concentration | "Does the protein come from concentrating milk, or from added protein?" |
| מרקם טבעי | Natural texture | "Is the texture from the dairy process?" |

---

### גבינות צהובות — 3 Lenses (preview)

| Lens | Hebrew | Shopper question |
|------|--------|------------------|
| אחוז חלב | Milk fraction | "What fraction of this is actual cheese?" |
| הבשלה | Aging/maturity | "Is there real aging, or simulated flavor?" |
| נתרן יחסי | Sodium relative to type | "Is the saltiness from the cheese or added?" |

---

## Contradiction Detection Rules

A contradiction line (T3 in insight line spec terminology) is appropriate when:

1. **Claim-composition gap**: Front-of-pack positions the product as healthy/natural/high-protein/diet, but the ingredient structure doesn't support the claim.
2. **Premium signal without structural advantage**: The product costs more, comes from an artisanal brand, or has a regional/biological frame — but the ingredient structure is identical to the national brand.
3. **Reductive claim that achieves less than promised**: "26% less sugar" → 1.5 point score difference. "Diet" → lower score than regular.

### Contradiction line formula

```
[What the packaging says] + [what the ingredients reveal]
```

No verdict. No "therefore." The reader draws the conclusion.

> "קולגן בתווית, כמות לא מצוינת על האריזה"  
> "מסומן 'דיאט', הסוכר הוחלף בממתיקים — התשתית לא השתנתה"  
> "26% פחות סוכר, 1.5 נקודות הפרש מהגרסה הרגילה"  
> "ציון גבוה מהשוקולד הלאומי — רשימת רכיבים קצרה יותר"

### Contradiction frequency rules

- Max 1 contradiction line per 5 products in the list (rhythm)
- Max 2 contradiction lines per cluster (cluster saturation)
- A contradiction line must be traceable to actual BSIP1 ingredient data
- Never invent a claim that isn't verifiable

---

## Insight Depth Calibration — Quick Reference

| If the line... | It is probably... | Action |
|----------------|-------------------|--------|
| Is one number | Level 1 | Upgrade unless number = surprise |
| Compares to "average" or another product | Level 2 | Upgrade unless comparison = surprise |
| Combines two observable facts | Level 3 | Publish |
| Describes what the product fundamentally is | Level 4 | Publish |
| Explains the score | Any level | Reject — describes the framework, not the product |
| Uses NOVA, cap, dimension names | Any level | Reject — ontology leak |
| Could apply to 5 other products unchanged | Level 1-2 | Upgrade — not specific enough |
| Tells the reader something surprising | Level 3-4 | Publish |

---

## Version

v1 — established 2026-05-28.  
Amends: `insight_line_spec_v1.md` (this document takes precedence on anti-patterns, levels, and lenses; rhythm rules remain in the parent spec).
