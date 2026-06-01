# מעדנים — Category Analysis + Editorial Architecture v1

**Generated:** 2026-05-28  
**Source:** run_maadanim_001 — 200 Shufersal products, 169 scored  
**Stage:** Phase 3 (analysis) + Phase 4 (engine) + Phase 5 (blog) + Cursor handoff  

---

## Part 1 — Corpus Filter

### Products in editorial scope

The raw scrape captured 200 products using מעדנים keyword queries. Not all belong to the editorial category. The following product types are **excluded from editorial analysis** (routing artifacts or keyword false positives):

| Excluded type | Examples | Reason |
|---|---|---|
| Candy / mints | סוכריות מנטה, סוכריות לימון, סוכ.וורטר | keyword "ללא סוכר" overlap |
| Diet syrup | סירופ דיאט לימונענע, סירופ דיאט אשכוליות | keyword "מעדן" near category |
| Jam / spread | ריבת תות, קונפיטורה פירות יער, טרו ריבת משמש | keyword "לייט" proximity |
| Jelly packets | ג'לי בטעם ענבים, ג'לי תנובה | false positive on dessert queries |
| Protein noodles | נודלס חלבון בקר, עוף, סצואן | "חלבון" query bleed |
| Pancake mix | פנקייק מיקס | "ללת"ס" query bleed |
| Diet sugar substitute | סוכרה דיאט | "דיאט" query proximity |
| Carbonated drink | שוופס ללא סוכר | "ללא סוכר" query proximity |
| Tahini spread | ממרח טחינה שוקולד | chocolate query bleed |
| Cereal | ברנפלקס ללא תוספת סוכר | "ללא סוכר" proximity |
| Oat cookies | עוגיות קוואקר ללת"ס | cracker route, not dessert |
| White cheeses | בולגרית מעודנת, גבינה צפתית | dairy_protein routing, not מעדן |

**Editorial corpus (in scope):** approximately 125 products  
**BSIP2-scored within scope:** approximately 108 products with sufficient data

### Why 125 not 200

The scraper used broad Hebrew keyword queries to avoid missing edge cases. The false positive rate of ~37% is normal for a first-pass keyword scrape and does not indicate a data quality problem. The editorial analysis draws only from the in-scope cluster.

---

## Part 2 — Category Segmentation

Six distinct shelf clusters emerged from routing + score data. All segment assignments cite actual scored products.

### Cluster 1 — Milky-Style (מוצרי מילקי ודומיהם)

**Score range:** 26.6–45.6 / E–D  
**NOVA:** 100% NOVA4  
**Additive load:** 2–4 functional additive categories (stabilizers, flavor enhancers, emulsifiers)  

Representative products:
- מילקי קייק: **26.6/E** (additive-heavy, low protein, high calorie)
- מילקי שכבות שוקולד+קצפת: **30.7/E**
- מילקי שכבות שוקולד קוקוס: **30.6/E**
- מילקי טופ קורנפלקס: **30.6/E** (cornflake topping = texture without nutritional benefit)
- מילקי עם 26% פחות סוכר: **38.8/D** (reducing sugar did not reduce NOVA level)
- מילקי בטעם שוקולד: **40.3/D**
- מילקי אקסטרה קצפת: **37.2/D**
- מילקי טופ שוקולדה מגולגל: **45.6/D** (highest-scoring מילקי)
- יולו שכבות שוקולד: **39.7/D**
- מעדן מוו בטעם שוקולד: **38.3/D**

**What the data says:** The founding product family of the Israeli dairy dessert shelf is the lowest-scoring cluster. NOVA4 is the structural ceiling driver across all variants. The "26% less sugar" version (38.8/D) scores barely above the standard version (40.3/D) — reducing sugar without changing additive infrastructure has near-zero score impact.

### Cluster 2 — Protein-Forward (חלבון)

**Score range:** 42.6–69.6 / D–B  
**NOVA:** 3–4 split (the NOVA level is the main score differentiator within this cluster)  

Representative products:
- יופלה GO מועשר בחלבון: **69.6/B**, NOVA3, 0 additives detected, 10g protein/100g
- מעדן חלבון בטעם וניל: **54.4/C**, NOVA4, additive-loaded
- מעדן חלבון ללת"ס שוקולד: **42.6/D**, NOVA4, capped at 68
- דנונה פרו 20ג חלבון תות: **53.1/C**, NOVA4, cap=60
- דנונ.פרו ללא סוכר פיסטוק: **54.2/C**, NOVA4, cap=68

**What the data says:** The word "חלבון" on the label does not predict the score. The NOVA level does. יופלה GO earns its score through milk protein alone (whey + casein, 10g/100g), with no detected additives and 72 kcal. מעדן חלבון ללת"ס gets the same protein marketing but sits at NOVA4 with a cap-constrained score 27 points lower.

### Cluster 3 — Regional/Artisanal-Frame (מעדן הגולן)

**Score range:** 48.4–53.3 / D–C  
**NOVA:** mostly NOVA3  
**Binding cap:** 72 (NOVA3 + 3 additive categories)  

Representative products:
- מעדן הגולן שוקולד: **53.3/C**
- מעדן הגולן שוקולד מריר: **49.1/D**
- מעדן הגולן וניל: **48.4/D**

**What the data says:** The Golan brand's NOVA3 positioning produces a higher cap ceiling than the NOVA4 national brands on the same shelf. The "artisanal" positioning is not entirely without structural basis — lower additive load contributes to the NOVA classification. Still D–C range due to high sugar content in the dessert category.

### Cluster 4 — Fruit-Forward מעדן (מעדן פירות ומוצרים טבעיים)

**Score range:** 41.4–56.9 / D–C  
**NOVA:** 2–4 range  

Representative products:
- מעדן משמש: **56.9/C**, NOVA2 — fruit-forward, simple composition
- מעדן סויה ביו טבעי: **57.4/C**, NOVA3 — plant-based, low additive
- מעדן שיבולת שועל: **54.4/C**, NOVA4 — oat base with additive load
- מעדן תפוז: **47.9/D**, NOVA3 — fruit flavored
- מעדן חצילים: **49.0/D**, NOVA3 — eggplant-based (unusual formulation)
- ירח מתוק מעדן חלב+אורז: **41.4/D**, NOVA4 — milk+rice dessert

**What the data says:** The category's most compositionally honest segment. מעדן משמש (NOVA2) is the highest-scoring traditional מעדן — simple ingredients, no detected additives. The soy alternative (מעדן סויה ביו טבעי, 57.4/C) outscores most dairy מעדנים, not due to plant-based ideology but because its ingredient list is shorter and its NOVA level is lower.

### Cluster 5 — Pudding / Instant Desserts (פודינג)

**Score range:** 31.6–49.5 / E–D  
**NOVA:** 3–4 split  

Representative products:
- פודינג אינסטנט שוקולד: **49.5/D**, NOVA3
- אינסטנט פודינג שוקולד: **48.9/D**, NOVA3
- פודינג וניל צרפתי: **46.0/D**, NOVA3
- אינסטנט פודינג וניל: **46.0/D**, NOVA3
- פודינג וניל: **31.6/E**, NOVA4
- פודינג בטעם וניל: **31.6/E**, NOVA4
- פודינג טעם פרלין אספרסו: **35.2/D**, NOVA4

**What the data says:** Instant powder (mix-at-home) scores significantly better than ready-made pudding cup. The reason is NOVA level — powders tend to be NOVA3, ready cups tend to be NOVA4 due to preservation additives and shelf-stable emulsifiers. The consumer perception is often inverted: the ready cup feels more "premium" but has a more complex additive load.

### Cluster 6 — Soy / Plant Alternatives (סויה)

**Score range:** 42.3–57.4 / D–C  
**NOVA:** 3–4 range  

Representative products:
- מעדן סויה ביו טבעי: **57.4/C**, NOVA3 — cleanest formulation
- מעדן סויה ביו טעם תות: **46.4/D**, NOVA4
- מעדן סויה ביו אפרסק: **42.3/D**, NOVA4
- מעדן סויה עם שוקולד: **42.7/D**, NOVA4

**What the data says:** The "natural" soy variant (ביו טבעי) scores highest because it remains at NOVA3. Flavored soy variants drop to NOVA4 when flavoring and stabilizers are added — the same structural pattern as dairy: adding flavor to a dessert almost always increases processing depth.

---

## Part 3 — Shelf Contradictions

The following findings are directly verifiable from scored data. Each cites real products and real scores.

### Contradiction 1: The Icon Paradox

**מילקי קייק: 26.6/E — the lowest score on the shelf.**

מילקי is the product that gave the category its cultural name. Every Israeli child grew up with it. It is presented in refrigerators at eye level in every supermarket. Its score cluster (E: 26.6–40.3) is the lowest in the dataset.

The specific structural cause: NOVA4 cap (68), then additive-driven dimension compression on top. The מילקי products carry 2–4 functional additive categories (stabilizers, flavor enhancers) plus added sugar as the third or fourth ingredient. The whipped cream layer adds calorie density without protein or fiber.

The "26% less sugar" variant scores 38.8/D — barely 1.5 points above the standard (40.3/D). Reducing sugar alone, without changing the additive infrastructure or NOVA classification, has near-zero score effect.

**Editorial impact:** The most emotionally resonant shelf tension in the dataset. The product everyone knows scores worse than they expect. This is the opening sentence of the blog.

### Contradiction 2: "חלבון" is a 27-Point Spread

Same word on the label. 27-point score gap.

| Product | Score | Grade | NOVA | Key signal |
|---|---|---|---|---|
| יופלה GO מועשר בחלבון | 69.6 | B | 3 | 10g protein, 0 additives, 72 kcal |
| מעדן חלבון ללת"ס שוקולד | 42.6 | D | 4 | additive-loaded, NOVA4 cap |

Both products are positioned on the protein-dessert shelf. Both carry a "חלבון" positioning signal. The score gap comes entirely from structural differences: יופלה GO is NOVA3 with no detected additives; מעדן חלבון ללת"ס is NOVA4 with cap=68.

The consumer cannot detect this difference from the front of the package. "מועשר בחלבון" and "מעדן חלבון" are nearly indistinguishable claims.

### Contradiction 3: "Diet" Often Scores Worse Than Regular

| Product | Score | Grade | Positioning |
|---|---|---|---|
| מעדן משמש | 56.9 | C | No diet claim, simple fruit מעדן |
| מעדן דיאט שוקולד 0.2% | 35.0 | D | "Diet" positioned, sweetener-loaded |
| מעדן הגולן שוקולד | 53.3 | C | No diet claim |
| מילקי עם 26% פחות סוכר | 38.8 | D | Reduced sugar claim |

The "diet" positioning consistently underperforms because the mechanism used to reduce sugar (artificial sweeteners, sugar alcohols) does not remove the NOVA4 classification or the additive infrastructure that drives the cap.

מעדן דיאט שוקולד (35.0/D) scores 22 points lower than a plain fruit מעדן (מעדן משמש, 56.9/C) with no wellness claims at all.

### Contradiction 4: The Plant-Based Paradox

מעדן סויה ביו טבעי (57.4/C, NOVA3) outscores standard dairy מעדנים in the same price band. This is not because soy is inherently superior — the other soy variants (אפרסק, תות, שוקולד) score 42.3–46.4/D once flavoring is added. The gap comes from additive load: the plain soy variant has a shorter, cleaner ingredient list.

The practical insight: a plain soy dessert and a plain fruit מעדן both outperform flavored dairy מעדנים. The "plain" pattern is more predictive of score than the "dairy vs. plant-based" distinction.

### Contradiction 5: Pudding Inverts the Convenience Premium

Ready-made pudding (31.6–35.2/D–E, NOVA4) scores significantly lower than instant pudding powder (46–49.5/D, NOVA3). Consumers typically perceive the chilled ready cup as the premium product. The ingredient structure reverses this: ready cups require shelf-stable additives the powder does not.

---

## Part 4 — Comparison Pairs (Engine)

These are the five strongest editorial pairs for the comparison engine, ordered by narrative weight.

### Pair A — The Icon vs. The Challenger
**מילקי בטעם שוקולד 40/D vs. יופלה GO מועשר בחלבון 70/B**

- Same: chocolate dairy dessert, cold case, Israeli national brands
- Different: 30-point gap, NOVA4 vs. NOVA3, stabilizer-loaded vs. additive-free
- Ingredient contrast: מילקי carries E1442 (modified starch), carrageenan, sodium phosphate, polyphosphate, xanthan gum, flavor enhancers. יופלה GO carries milk and milk proteins only.
- Driver sentence: "אותה ארוחת צהריים, פער של 30 נקודות — החל מהרכיבים."

### Pair B — The Protein Split
**יופלה GO מועשר בחלבון 70/B vs. מעדן חלבון ללת"ס שוקולד 43/D**

- Same: both explicitly protein-positioned, cold dairy section, similar price point
- Different: NOVA3 vs. NOVA4, 10g real whey+casein vs. additive-delivered protein claim, 27-point gap
- Driver sentence: "שניהם כתוב עליהם 'חלבון'. רק לאחד הרכיבים מגבים את זה."

### Pair C — The Diet Trap
**מעדן הגולן שוקולד 53/C vs. מעדן דיאט שוקולד 35/D**

- Same: both chocolate dairy desserts
- Different: the "diet" product scores 18 points lower. NOVA3 vs. NOVA4. The label that implies health advantage has the lower score.
- Driver sentence: "המוצר שמסמן 'דיאט' מקבל ציון נמוך יותר מהשוקולד הרגיל."

### Pair D — The Quiet Fruit מעדן
**מעדן משמש 57/C vs. מילקי בטעם שוקולד 40/D**

- Same: both are dairy desserts, same shelf location, similar packaging format
- Different: no wellness claim on the apricot מעדן, yet 17-point higher score. NOVA2 vs. NOVA4.
- Driver sentence: "ללא שום תווית 'בריא', מעדן המשמש מנצח את הגביע המפורסם."

### Pair E — Instant vs. Ready
**פודינג אינסטנט שוקולד 49/D vs. פודינג וניל 32/E**

- Same: both are pudding desserts
- Different: the powder you make at home (NOVA3) scores higher than the ready cup (NOVA4). The convenience product has more additives.
- Driver sentence: "הפודינג שמכינים בבית מקבל ציון גבוה יותר מהגביע המוכן."

---

## Part 5 — Wellness Halo Patterns

### Pattern 1: "Protein" label does not predict score

Products with "חלבון" on the label span the range D to B. The score correlates with NOVA level (which reflects actual additive load), not the protein claim. A product with high protein and high NOVA4 processing remains capped at 68.

### Pattern 2: "ללא סוכר" / "דיאט" consistently underperforms expectations

Products with reduced-sugar or diet claims score lower than equivalent non-diet products in 4 out of 5 sampled comparisons. The mechanism: sweeteners do not reduce NOVA classification. A NOVA4 product that replaces sugar with aspartame is still NOVA4.

### Pattern 3: The "natural" frame (ביו, טבעי) does predict cleaner structure — when it holds

מעדן סויה ביו טבעי (NOVA3) outperforms standard dairy מעדנים. However, the flavored variants of the same brand (ביו תות, ביו אפרסק) drop to NOVA4 once flavoring is added. The "natural" label only holds for unflavored or simply-flavored variants.

### Pattern 4: "Enriched" (מועשר) is neutral

The word "מועשר" on its own (מעדן בטעם וניל מועשר, 43.4/D) predicts nothing. Enriched products span from D to B depending on what they are enriched with (vitamins vs. real protein) and how.

---

## Part 6 — Children's Dessert Pattern

Products in the children's zone (גמדים, באדי, דני) cluster at D (37–49). The pattern matches the adult mainstream cluster: NOVA4, moderate additive load, high sugar.

| Product | Score | Grade |
|---|---|---|
| גמדים תות בננה מארז | 53.2 | C |
| סופר גמדים תות בננה | 52.8 | C |
| גמדים לדרך תות בננה | 48.9 | D |
| באדי תות שדה 3% שומן | 49.5 | D |
| דני שוקולד 1.5% | 37.4 | D |

Gideons (גמדים) score C in multi-pack, D in single-serve. The multi-pack format appears to correlate with slightly more conservative formulation (or nutritional data differences by format). No children's product reaches B or above.

**Editorial caution:** Avoid moralizing about children's products specifically. The data shows the same structural pattern as adult products, not a distinct manipulation. Frame as: the child-targeted packaging is not structurally different from the adult mainstream — same NOVA level, similar additive load.

---

## Part 7 — Comparison Engine Architecture

The מעדנים comparison engine follows the milk-standard design: products first, everything else secondary.

### Page structure

```
[1] ShelfHero — single full-width image, one sentence, score revealed on scroll
[2] EditorialPrologue — 3-5 sentences max, no bullet points, no summary boxes
[3] ComparisonEngine — full product grid, default sort by score descending
[4] Methodology footnote — 2 sentences, linked to full framework page
```

No map. No dashboard. No cluster visualization. No "wellness halo" glossary. These belong in framework documentation, not consumer-facing editorial.

### ComparisonEngine specification

**Default view:** product cards sorted by score descending. Scores visible. Grade chips visible. Product images (packaging photography, 160px min) required.

**Filter panel:**
- Triggered by single "סינון" button (collapsed by default)
- Filter options: Cluster (6 values), NOVA level (1/2/3/4), Grade (B/C/D/E)
- Single-select per filter dimension
- Clear all in one tap
- No nested sub-filters

**Comparison mode:**
- User selects 2 products from grid → ComparisonMoment expands above grid
- ComparisonMoment layout: [Product A image | Score chip | Driver line | Score chip | Product B image]
- Driver line: ≤25 words, Hebrew, explains the most structurally significant difference
- Driver line is NOT a score explanation. It is the observation that produced the gap.

**Score display:**
- Primary: numeric (69) / grade chip (B) — no labels like "טוב" or "חלש"
- Do NOT show individual dimension scores in the engine grid
- Dimension scores available in product detail drawer (secondary disclosure level)

### ProductDetailDrawer specification

Opens on product card tap. Shows:
1. Full product name + brand
2. Score + grade + confidence state
3. Top 3 observed signals (not framework labels): e.g., "NOVA3 — no detected additives" / "10g protein/100g" / "162 kcal"
4. Ingredients list (verbatim from BSIP1)
5. Nutrition table (per 100g, from BSIP1)
6. Data confidence statement (e.g., "נתונים מ-Shufersal בלבד — ייתכנו הבדלים מהמוצר הפיזי")

Do NOT show: cap rules, framework architecture terms, dimension names ("processing_quality", "glycemic_quality"), additive category names in raw form.

---

## Part 8 — Blog Architecture

### ONE article: "הגביע שגידלנו איתו"

**Thesis:** The dairy dessert shelf reveals a gap between what products promise and what they contain — and the most famous product on the shelf is the most striking example.

**Structure (8 sections):**

```
[1] HERO — packaging image of מילקי (large), score revealed: 40/D
     One sentence: "הגביע הזה נמכר למיליוני ישראלים בכל שבוע. הציון שלו הוא D."

[2] SHELF INTRO — 2 paragraphs
     What is the Israeli dairy dessert shelf today? Who is on it?
     No bullet lists. No subheadings. Narrative only.
     Must cite: at least 3 real brands from the dataset.

[3] COMPARISON MOMENT 1 — The Icon vs. The Challenger
     מילקי בטעם שוקולד [image] 40/D [score chip]
     פסיק (—)
     יופלה GO מועשר בחלבון [image] 70/B [score chip]
     Driver line (Hebrew, ≤25 words): "שני מוצרים מאותו קיר קירור. ההבדל הוא לא הטעם — הוא מה שנמצא ברשימת הרכיבים."
     Followed by: 3 sentences narrative. No more.

[4] FINDING 1 — The protein spectrum (3 paragraphs)
     "חלבון" appears on multiple products. The word does not predict the score.
     Cite: יופלה GO (70/B) vs. מעדן חלבון ללת"ס (43/D).
     Do NOT mention NOVA by name. Say "רמת עיבוד" if needed.
     Do NOT use framework jargon.

[5] COMPARISON MOMENT 2 — The Protein Split
     יופלה GO [image] 70/B
     —
     מעדן חלבון ללת"ס שוקולד [image] 43/D
     Driver line: "שניהם מציגים 'חלבון'. רק אחד מגיע עם רשימת רכיבים שמגבה את זה."
     3 sentences narrative.

[6] FINDING 2 — The diet trap (2 paragraphs)
     "דיאט" or "ללא סוכר" on the label does not guarantee a higher score.
     Cite: מעדן דיאט שוקולד (35/D) vs. מעדן משמש (57/C).
     Tone: observational, not accusatory. Do not say "misleading" or "manipulative."

[7] QUIET MAP — one visual element (optional, collapsed by default)
     If a map is used: score distribution dots for the מעדנים cluster only.
     No cluster labels. No circles. No color-coded zones.
     A dot chart or simple scatter is acceptable.
     This section is OPTIONAL — if it adds noise, omit it entirely.

[8] SYNTHESIS + CTA — 3 sentences max
     What does the data actually suggest about this shelf?
     No advice. No "בחרו ב-". Observational close.
     Link to comparison engine: "ראו את כל המוצרים עם הציונים שלהם ↗"
```

### Hero image philosophy

- Primary image: product packaging only (no styled food photography)
- מילקי cup photographed against clean white background, label visible
- Score chip overlaid as a UI element (not photoshopped onto packaging)
- Score revealed after 0.5s scroll pause — not immediately visible on load
- No score-to-color mapping on hero image

### What to omit from the blog

- No glossary sidebar, footnote wall, or methodology section inside the article
- No breakdown charts (BarCompositionBreakdown is engine-only, product detail)
- No comparison tables in prose form (use ComparisonMoment component instead)
- No "what does this mean for you" advice sections
- No subheadings inside narrative paragraphs — each section is continuous prose

---

## Part 9 — Ontology Leakage Risks

The following framework terms must NOT appear in any public-facing editorial output.

| Internal term | Consumer-facing alternative |
|---|---|
| NOVA4 | "רמת עיבוד גבוהה" or "מוצר מעובד" |
| cap / binding_cap | never mentioned |
| additive_marker_count | "מספר תוספים מזוניים" |
| processing_quality dimension | "עיבוד" (if needed) |
| dairy_protein routing | not consumer-facing |
| structural_class F / "Structurally Void" | never mentioned |
| score_engine / BSIP2 | never mentioned |
| hard_anchor | never mentioned |
| dimension score (e.g., 35 for processing_quality) | never show individual dimension numbers |

**The framework is invisible infrastructure.** The blog and engine surface only: product name, score, grade, observed signals (ingredients, calories, protein), and confidence state.

---

## Part 10 — Dashboard Drift Risks

The following patterns represent drift toward the dashboard/analytics register and must be avoided.

| Drift pattern | What it looks like | Why it fails |
|---|---|---|
| Cluster map | Interactive bubble chart showing 6 clusters | Displaces products from the first screen |
| Score distribution histogram | Bell curve of all 125 products | Analytics register, no consumer utility |
| Brand performance table | Average score by brand | Invites brand-level argumentation, editorial claim too strong |
| Radar chart per product | Dimension breakdown spider | Exposes framework architecture |
| "Top 10 healthiest" ranking | Listicle format | Anti-investigation, kills curiosity |
| Summary stats box above fold | "67% of products are NOVA4" | Kills discovery, headline displaces products |

The comparison engine is a **calm archive** where products are the primary objects. Analytics belong in the methodology section of the framework documentation, not in the product discovery experience.

---

## Part 11 — Cursor Implementation Handoff

### Architecture

The מעדנים page follows the same component hierarchy as the snack bar editorial recovery design:
- `MaadanimPage` wraps `ShelfHero` + `EditorialBlog` + `ComparisonEngine`
- `ComparisonEngine` is the same component as the snack bar engine (parameterized by category)
- Blog and engine are **separate sections** on the same page — NOT the same experience

### New components required

#### `MaadanimShelfHero`
```
Props:
  - productName: "מילקי בטעם שוקולד"
  - productScore: 40
  - productGrade: "D"
  - imageSrc: packaging photograph URL
  - heroSentence: string (≤15 words)

Behavior:
  - Score hidden on initial load
  - Score animates in after 600ms or on scroll start (whichever comes first)
  - Score chip: white background, large numeric, grade badge
  - No color encoding on score chip
```

#### `ComparisonMoment` (already exists in snack bar implementation)
The מעדנים comparison moments use the identical component. Only the product data changes.

Required pairs to pre-configure:
1. מילקי בטעם שוקולד vs. יופלה GO מועשר בחלבון
2. יופלה GO מועשר בחלבון vs. מעדן חלבון ללת"ס שוקולד
3. מעדן הגולן שוקולד vs. מעדן דיאט שוקולד
4. מעדן משמש vs. מילקי בטעם שוקולד
5. פודינג אינסטנט שוקולד vs. פודינג וניל

#### `MaadanimProductGrid`
Standard ProductCardGrid parameterized with:
- `category: "dessert"`
- `defaultSort: "score_desc"`
- `filterDimensions: ["cluster", "nova", "grade"]`

Cluster filter values (Hebrew display names):
- `milky_style` → "מילקי ודומיהם"
- `protein_forward` → "מוצרי חלבון"
- `regional_artisanal` → "מעדן הגולן"
- `fruit_forward` → "מעדן פירות"
- `pudding` → "פודינג"
- `soy_alternative` → "סויה"

### Data source

BSIP2 traces: `C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001\products\`

Filter to editorial scope before loading into the engine. Exclude products with:
- `category` not in `["dessert", "dairy_protein"]` AND `product_name_he` not containing מעדן/מילקי/יופלה/פודינג/מלבי/קינוח
- `data_sufficiency == "insufficient"`
- `final_score_estimate == null`

### Build order

1. `MaadanimShelfHero` — standalone, no data dependency
2. `ComparisonMoment` pairs (5 pairs, hardcoded product IDs, data from BSIP2 traces)
3. `MaadanimProductGrid` — full engine with filter
4. `EditorialBlog` sections (narrative prose, no dynamic data)
5. `ProductDetailDrawer` — opens from grid card, loads full trace
6. `FilterPanel` (collapsed by default, triggered by "סינון" button)

### Failure modes to prevent

- **Score before product:** Never show aggregate stats or distribution before the first product appears on screen
- **Filter overcrowding:** Maximum 3 filter dimensions. If a 4th is added, remove one.
- **Comparison buried:** ComparisonMoment must appear in the first 60vh of the blog section, before any map or chart
- **Driver sentence as score explanation:** The driver sentence explains the structural difference, not the scoring methodology. Do NOT write "הציון נמוך יותר כי..."
- **Methodology section inside blog:** All methodology goes in a separate `/methodology` page. The blog links to it with one line, nothing more.

---

## Summary: What the מעדנים Shelf Actually Shows

**169 products scored. No S. No A. Four B grades.**

The four B grades are all in the protein-enriched yogurt cluster — products positioned as desserts but structurally closer to dairy_protein. The traditional מעדנים cluster (מילקי, יופלה Tube, pudding cups, מלבי) sits overwhelmingly at D, with the iconic products at E.

The shelf exhibits a structural pattern: 67% NOVA4, 88% capped. The ceiling constraint is almost universal. Products that escape it do so not through superior nutrition but through lower processing depth — יופלה GO's NOVA3 classification is the primary driver of its B grade, not exceptional macronutrient content.

The strongest editorial insight: **the most famous product on the shelf scores the lowest.** That is the beginning and end of the blog's job — reveal what the data says, let the reader draw their own conclusions.
