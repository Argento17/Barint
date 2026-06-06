# Bari Editorial Intelligence System — v3
**Date:** 2026-05-26
**Replaces:** editorial_intelligence_v2.md
**Evidence base:** Bread category — 256 scanned products, 81 with full data

---

## Table of Contents

0. [What Bari Does](#0-what-bari-does)
1. [Three Editorial Principles](#1-three-editorial-principles)
2. [Maximum Complexity Rules](#2-maximum-complexity-rules)
3. [Language Standard](#3-language-standard)
4. [What These Terms Actually Mean](#4-what-these-terms-actually-mean)
5. [Translation Reference](#5-translation-reference)
6. [Insight Cards](#6-insight-cards)
7. [What Bari Discloses](#7-what-bari-discloses)
8. [Next Categories](#8-next-categories)
9. [Simplicity Test](#9-simplicity-test)
- [Appendix: Internal Reference](#appendix-internal-reference)

---

## 0. What Bari Does

Bari is not a health scoring engine. Bari is an alignment platform.

The central question Bari asks about every product is not "is this healthy?" It is: **does what the product presents match what the product contains?**

"Healthy" is a judgment that requires knowing who is eating, for what purpose, in what context. Bari doesn't have that information and doesn't pretend to. What Bari does have is the ingredient list, the nutrition panel, and the label — and the ability to compare them carefully.

Alignment takes four forms:

**Name vs. ingredients.** Does the product name invoke a mechanism or quality — fermentation, whole grain, protein — that the ingredient list actually supports? When a bread is called "מחמצת" and the primary leavener is commercial yeast, that is a gap. Bari documents it.

**Marketing vs. composition.** Seeds on the front of a package are marketing. Seeds as a primary ingredient are composition. They are not the same thing.

**Consumer expectation vs. actual structure.** When consumers reach for a "whole grain" product, they carry an expectation about what that means. Bari examines whether the actual ingredient order and fiber source are consistent with that expectation — or whether the expectation was built by language and imagery without compositional support.

**Confidence vs. available data.** Bari only scores what can be verified. When data is missing, that gap is itself informative.

These four questions apply equally to bread, yogurt, cereals, and every category that follows. The mechanisms change. The question does not.

Bari does not tell consumers what to eat. Bari tells consumers what is and is not verifiable about what they are already choosing to eat. The score represents alignment, not prescription. A low score means the product is compositionally inconsistent with its positioning — not dangerous, not forbidden. A high score means the composition is consistent — not necessarily optimal for any given person.

Bari's editorial voice follows from this. Calm, because the findings speak. Precise, because vague claims produce vague trust. Bounded, because we only speak to what the label allows us to see.

---

## 1. Three Editorial Principles

These three principles govern every piece of consumer-facing output Bari produces. They exist at a level above language rules or card formats. When in doubt, return here.

---

### Insight-First

The consumer should encounter the finding before the explanation. The explanation should come before the method. The method, if it appears at all in consumer-facing output, comes last.

The wrong order: *"Bari's fermentation validation layer assesses whether sourdough markers appear in the ingredient list and how they relate to commercial yeast presence..."*

The right order: *"ברי מצאה ש-13 מוצרים מתוך 108 נושאים 'מחמצת' בשמם — ובכולם, שמרים תעשייתיים הם המחמיץ בפועל."*

Lead with what was found. Let the reader ask how. Answer only if asked.

---

### Framework Invisibility

The more sophisticated Bari's internal analysis becomes, the simpler it should feel from the outside.

The engine can track flour hierarchy, fermentation quality gradations, and grain structure scores. The consumer should never need to know any of those words. They should encounter a clear observation about a product they're looking at.

Framework visibility is a failure state, not a feature. When the reader notices the system, the system has gotten in the way of the insight.

This principle applies to UX, editorial copy, scoring explanations, and methodology pages alike. The measure of good methodology documentation is not completeness — it is whether a reader finishes it understanding Bari better, or understanding Bari's taxonomy better. Those are different outcomes.

---

### Consumer Attention Test

Before publishing any section of content, ask: would a normal, intelligent reader continue past this?

If the answer is *"this feels like documentation,"* simplify.
If the answer is *"this feels like investigative insight,"* keep it.

Documentation answers the question "how does this work?" Insight answers the question "what does this mean for me?" Bari's public-facing output should always be answering the second question.

---

## 2. Maximum Complexity Rules

Five hard rules for public-facing output. No exceptions.

1. **No internal code or classification label.** A consumer should never see FQC, GSS, structural class, archetype name, synthesis delta, or any other internal scoring term. If one of these appears in a draft, it must be replaced with a plain description before publishing.

2. **No methodology chain.** Never explain how Bari arrived at a finding in more than one sentence. If more explanation is needed, it belongs on a methodology page — not in an insight card or product description.

3. **No score without a plain sentence.** Every score that appears publicly must be accompanied by a human-language sentence explaining what it reflects. "ציון 82" with no sentence is incomplete. "ציון 82 — קמח מלא ראשון ברשימה, מחמצת ברכיבים" is complete.

4. **No classification without an observation.** Never describe a product using a category label alone. "Ambiguous wellness product" means nothing to a consumer. "חלק מהטענות ניתן לאמת, חלק לא" means something.

5. **Uncertainty is not a technical disclosure — it is an editorial position.** "לא ניתן לאמת" is not a legal disclaimer, it's a finding. Write it as one.

---

## 3. Language Standard

### Punctuation — Em-Dash Rule

**The em-dash "—" is overused. Hard limit: one em-dash per paragraph.**

The em-dash "—" is not a connector, not a sentence opener, and not a list separator. It is a parenthetical device for a sharp interruption or an appositive that earns a pause. Used more than once per paragraph, it becomes structural noise.

| Wrong — dash as connector | Right — full sentence |
|---|---|
| "פוליפנולים — לא מופיע על התווית" | "נתון הפוליפנולים אינו מופיע על התווית." |
| "יש הבדלים — אבל אין בסיס לנקד אותם" | "יש הבדלים. אין בסיס לנקד אותם." |
| "אף קמעונאי — לא עשה מאמץ" | "אף קמעונאי לא עשה מאמץ לגלות זאת." |

**Rule:** When the instinct is to write "—", write a period and start a new sentence. If two dashes appear in the same paragraph, one must go.

---

### Approved Phrases

**Ingredient observations:**

| Hebrew | When to use |
|---|---|
| מחמצת ברכיבים | Fermentation appears in the ingredient list |
| מחמצת בשם בלבד | Name claims מחמצת, ingredient list doesn't support it |
| קמח מלא ראשון ברשימה | Whole grain flour is the primary ingredient |
| קמח לבן כבסיס | Refined flour is the primary ingredient |
| מקור הסיבים | Lead-in before naming the fiber source specifically |
| מבנה פשוט | Short, recognizable ingredient list |
| גרעינים — מרכיב עיקרי | Seeds/grains in positions 1–3 |
| גרעינים — בכמות משנית | Seeds/grains in positions 4+ |
| שמרים תעשייתיים | Commercial yeast is the leavener |
| סיבים מהדגן | Fiber from whole grain structure |
| סיבים שנוספו בנפרד | Isolated fiber (inulin, psyllium, chicory) |
| פער בין השם לרכיבים | Any name-ingredient mismatch |
| הרכיבים עקביים עם המיצוב | Composition matches the positioning |
| ריבוי מרכיבים | High additive and ingredient count |

**Confidence and scope:**

| Hebrew | When to use |
|---|---|
| לא ניתן לאמת | A specific qualifier is missing from the label |
| לא ניתן לקבוע | Evidence insufficient for a claim |
| לפי רשימת הרכיבים | Attributing any compositional claim |
| אין מידע תזונתי | Nutrition panel absent |
| אין נתונים מספיקים | Product cannot be scored |

---

### Forbidden Phrases

**Moral and alarmist:**

| Forbidden | Replacement |
|---|---|
| רעיל | ריבוי מרכיבים תעשייתיים |
| מזויף | פער בין השם לרכיבים |
| מסוכן | לא מאומת |
| בריא / לא בריא | ציון גבוה / ציון נמוך |
| נקי / מלוכלך | מרכיבים מזוהים / ריבוי מרכיבים |
| אמיתי / לא אמיתי | מחמצת ברכיבים / מחמצת בשם בלבד |
| חייבים לדעת | State the finding. Remove the urgency. |
| הכי טוב בישראל | ציון גבוה מהממוצע בקטגוריה |

**Pseudo-technical (sounds authoritative, means nothing to a consumer):**

| Forbidden | Replacement |
|---|---|
| שלמות מבנית | הרכיבים עקביים עם המיצוב |
| ארכיטקטורה קומפוזיציונלית | הרכב הרכיבים |
| מחמצת תיאטרלית | מחמצת בשם בלבד |
| מחלקה הנדסית | ריבוי מרכיבים ותוספים |
| לא כנה מבחינה מבנית | פער בין המיצוב לרכיבים |
| עיבוד יתר | ריבוי מרכיבים / עיבוד תעשייתי גבוה |
| מטריצה מעובדת | בסיס קמח מעובד |

---

### Tone

**Bari sounds like:** an analyst presenting findings to an intelligent adult. A journalist who checked before publishing.

**Bari does not sound like:** a wellness influencer selling certainty. An app notification creating urgency. A nutritionist prescribing behavior.

Four active rules:

**State the observation. Let the reader decide.** "13 מוצרים מתוך 108 שנושאים 'מחמצת' בשמם — ושמרים תעשייתיים מופיעים לפני המחמצת ברכיבים" is a finding. "13 מוצרים שמטעים צרכנים" is a verdict. Bari issues findings.

**Scope every claim.** "לחמי הבריאות בסופרסל" is not the same as "לחמי הבריאות בישראל." Every claim needs a scope indicator: this product, this category, this dataset, this scan date.

**Name what you don't know first.** If fermentation percentage is unknown, say so before describing the fermentation signal. Missing data shapes the confidence of any finding.

**Quiet is stronger than loud.** The finding "פער של 9.3 נקודות בין לחמי בריאות ללחמים רגילים — שנעלם ברובו כשמסתכלים רק על מוצרים עם נתונים מלאים" is more credible than the same finding wrapped in alarm.

---

### Claim Boundaries

Bari may state: what appears in the ingredient list, what does not appear, ingredient positions, comparisons to other analyzed products, and patterns across the analyzed dataset with scope declared.

Bari may not state: health outcomes, manufacturer intent, that a product is "better for you," equivalence between analyzed and unanalyzed products, or generalizations to the full Israeli market.

---

## 4. What These Terms Actually Mean

Each entry below maps a common marketing term to what Bari actually checks. The format is insight-first: the finding from the bread category, then the mechanism behind the gap, then how to phrase it.

---

### מחמצת

In 13 out of 108 analyzed bread products, "מחמצת" appears in the product name while commercial yeast is the ingredient doing the leavening. Among the 32 products with full data, only 7 carry genuine fermentation in their ingredient lists. In the commodity segment, that drops to 10%. In wellness products it reaches 42% — fermentation is a positioning strategy, not a category standard.

The gap exists because "מחמצת" in a product name carries a strong consumer expectation — traditional fermentation, distinct flavor, potential digestibility benefits — that the ingredient list does not always support. Product names are marketing. Ingredient lists are evidence.

Bari checks whether מחמצת or שאור appears in the ingredient list. When commercial yeast also appears, Bari notes whether fermentation is leading the process or playing a minor role. When "מחמצת" appears only in the name, Bari cannot verify any fermentation process took place.

**How to phrase it:** "מחמצת ברכיבים" for verified fermentation. "מחמצת בשם בלבד" when the name claims what the ingredients don't.

---

### כוסמין

The word "כוסמין" carries a wellness signal regardless of how the grain was processed. But refined spelt flour and refined wheat flour have similar nutritional profiles. The distinction that matters — whole grain or refined — is captured in one word: "מלא."

The two highest-scoring crackers in the analyzed dataset are both spelt products: קרקר כוסמין מלא ושומשום (score=82, fiber=10g) and קרקר כוסמין אורגני (score=78, fiber=9.3g). Both explicitly carry the "מלא" qualifier. Spelt products without the qualifier score lower and cannot be assumed to offer whole-grain benefits.

Bari gives whole-grain credit only when "מלא" is explicitly stated, or when the whole grain form is listed before its refined equivalent.

**How to phrase it:** "כוסמין מלא — מאושר ברכיבים" when verified. "כוסמין — לא ניתן לאמת שמדובר במלא" when the qualifier is absent.

---

### מלא

A product can legally carry "מלא" in its name while refined flour is the primary ingredient. The law requires "מלא" to be present in some proportion — it does not regulate where the grain appears in the ingredient order.

Bari checks the position of whole grain flour in the ingredient list. Position 1 — the dominant ingredient — is very different from position 2 or 3. Bari also checks whether the product's fiber comes from the grain itself or was added separately from an isolated source. "לחם ירוק מקמח מלא" (score=80, fiber=6.4g) passes both checks. Many "מלא" products do not.

**How to phrase it:** "קמח מלא ראשון ברשימה" when confirmed. "קמח מלא מופיע אחרי קמח לבן" when the refined flour leads.

---

### עשיר בסיבים

A cracker can truthfully declare 9g of fiber per 100g while being made primarily from white flour. The fiber number is accurate. The implication — that the product is built from whole grains — is not what the ingredient list shows. In 4 out of 32 verified bread products, high fiber declarations are supported by added isolates (chicory root, psyllium, inulin), not by the grain base.

The declared fiber value is correct. The origin of that fiber is what changes the picture. Bari checks where the fiber comes from and names the source explicitly when it differs from what the product's positioning implies.

**How to phrase it:** "סיבים מהדגן" when grain-native. "סיבים שנוספו בנפרד" or specifically "מקור הסיבים: ציקוריה" when added.

---

### דגנים / גרעינים

14 out of 32 verified bread products show seeds prominently in their name or packaging but at positions 5–8 in the ingredient list. Those seeds are present. They are not central. The exception is קרקר כוסמין מלא ושומשום (score=82): whole spelt is position 1, sesame is structurally early in the list.

Ingredient list position is the only reliable signal for contribution. Seed visibility on packaging, in the product name, or in imagery is marketing — it does not determine how much of the product is actually composed of those ingredients.

**How to phrase it:** "גרעינים — מרכיב עיקרי" when in positions 1–3. "גרעינים — בכמות משנית" when later in the list.

---

### חלבון

"עשיר בחלבון" can mean grain-native protein from a whole food or added protein isolate (חלבון אפונה, חלבון חיטה מרוכז). These are compositionally different situations with different structural implications, even when the gram count is similar.

Bari notes whether protein is grain-native or was added as an isolate. The gram count is still reported. The context around it changes the interpretation.

**How to phrase it:** "חלבון מהדגן" when native. "בידוד חלבון שנוסף" when an isolate is listed in the ingredients.

---

### ללא סוכר / ללא תוספת סוכר

"No added sugar" is an accurate label claim that can coexist with a significant sweetener presence. The claim answers whether refined sugar was added — it does not address whether alternative sweeteners (סוכרלוז, סטיביה, מלטיטול) or natural sweeteners (תמרים, דבש) are in the ingredient list.

Bari checks the complete sweetener picture — all sweetener types, not just added sugar. If a "no added sugar" product contains multiple sweeteners, Bari names them.

**How to phrase it:** "ללא סוכר מוסף — מכיל [ממתיק ספציפי]" when alternative sweeteners are present.

---

## 5. Translation Reference

Three formats for communicating any observation: short (badge, ≤6 words), medium (card body, 1–2 sentences), tooltip (hover text, ≤15 words). The left column describes what was observed — no internal codes appear anywhere.

### Fermentation

| What was observed | Short | Medium | Tooltip |
|---|---|---|---|
| מחמצת ברכיבים, ללא שמרים | מחמצת ברכיבים | המוצר מתפח דרך תרבית מחמצת ברשימת הרכיבים, ללא שמרים תעשייתיים. | מחמצת ברכיבים, ללא שמרים |
| מחמצת לפני שמרים ברשימה | מחמצת עיקרית | מחמצת ושמרים מופיעים יחד — מחמצת מופיעה לפני השמרים. | מחמצת ושמרים יחד — מחמצת לפני |
| מחמצת ושמרים, סדר לא ברור | מחמצת ושמרים יחד | שני המרכיבים מופיעים ברשימה — לא ניתן לקבוע מה מוביל את ההתפחה. | מחמצת ושמרים — חלוקה לא ברורה |
| מחמצת אחרי השמרים ברשימה | מחמצת לטעם בלבד | מחמצת מופיעה אחרי השמרים — מוסיפה טעם, לא מובילה את ההתפחה. | שמרים עיקריים; מחמצת לטעם |
| "מחמצת" בשם, לא ברכיבים | מחמצת בשם בלבד | "מחמצת" בשם המוצר בלבד — לא מופיעה ברשימת הרכיבים. | שם כולל מחמצת — ברכיבים לא |
| שמרים בלבד ברשימה | שמרים תעשייתיים | המוצר מתפח בשמרים תעשייתיים בלבד. | ללא מחמצת ברכיבים |

---

### Grain & Flour

| What was observed | Short | Medium | Tooltip |
|---|---|---|---|
| קמח מלא — מרכיב ראשון | קמח מלא ראשון ברשימה | קמח מלא הוא המרכיב הראשון — הדגן המלא מהווה את עיקר הבסיס. | קמח מלא ראשון |
| קמח מלא דומיננטי, עם קצת לבן | בסיס דגן מלא בעיקר | הדגן המלא דומיננטי, עם כמות קטנה של קמח לבן. | בעיקר מלא |
| קמח מלא ולבן, שניהם מהותיים | קמח מלא ולבן יחד | גם קמח מלא וגם קמח לבן נוכחים משמעותית ברשימה. | מלא ולבן — חלוקה לא ברורה |
| קמח לבן עיקרי, תוספות מעליו | קמח לבן כבסיס | הבסיס הוא קמח לבן; מרכיבים נוספים הגיעו אחריו. | קמח לבן בבסיס |
| "רב-דגני" בשם, דגן עיקרי אחד | שם: רב-דגני. רכיבים: דגן אחד | שם המוצר מרמז על מגוון דגנים — רשימת הרכיבים מכילה בעיקר סוג אחד. | "רב-דגני" בשם — דגן עיקרי אחד ברכיבים |
| כוסמין עם ציון "מלא" | כוסמין מלא מאושר | קמח כוסמין מלא מפורש ברשימת הרכיבים. | כוסמין מלא — מאושר |
| כוסמין ללא ציון "מלא" | כוסמין — לא ניתן לאמת | "כוסמין" ברשימה ללא "מלא" — לא ניתן לאמת אם מדובר בגרסה המלאה. | כוסמין — לא ניתן לאמת |

---

### Fiber Source

| What was observed | Short | Medium | Tooltip |
|---|---|---|---|
| סיבים מגיעים מהדגן | סיבים מהדגן | הסיבים מגיעים ישירות מהדגן המלא. | סיבים מהדגן |
| חלק מהדגן, חלק נוסף בנפרד | חלק מהסיבים מהדגן | חלק מהסיבים מגיע מהדגן; חלק הוסף בנפרד. | גם סיבי דגן וגם סיבים מוספים |
| סיבים שנוספו בנפרד | סיבים שנוספו בנפרד | הסיבים הוספו כתוספת — ציקוריה, פסיליום, או אינולין. | סיבים מוספים |
| סיבים גבוהים, מקור הוא תוספת | הסיבים גבוהים — מקורם תוספת | כמות הסיבים גבוהה, אך הם מגיעים מחומרים שנוספו בנפרד, לא מהדגן. | סיבים גבוהים — מקור: תוספת |
| סיבים נמוכים, מהדגן עצמו | סיבים נמוכים — מהדגן | סיבים נמוכים, אך מגיעים מהדגן עצמו. | מעט סיבים, מהדגן |

---

### Seeds

| What was observed | Short | Medium | Tooltip |
|---|---|---|---|
| גרעינים במיקומים 1–3 | גרעינים — מרכיב עיקרי | הגרעינים בין המרכיבים הראשונים — הם חלק מהותי מהמוצר. | גרעינים — מרכיב עיקרי |
| גרעינים במיקומים 4–7 | גרעינים — בכמות משנית | הגרעינים מופיעים אחרי המרכיבים המרכזיים — הם נוכחים, בכמות קטנה. | גרעינים — בכמות קטנה |
| גרעינים בולטים בשם, מינוריים ברכיבים | גרעינים בולטים בשם, משניים ברכיבים | הגרעינים מובלטים בשם ובאריזה — ברשימת הרכיבים הם מינוריים. | גרעינים בחזית, קטנים ברכיבים |

---

### Processing

| What was observed | Short | Medium | Tooltip |
|---|---|---|---|
| רשימה קצרה, מרכיבים מוכרים | מרכיבים פשוטים ומוכרים | רשימה קצרה ממרכיבים מוכרים — קמח, שמן, מלח, שמרים. | מרכיבים מעטים ומוכרים |
| ריבוי תוספים ומייצבים | ריבוי תוספים | המוצר מכיל מספר חומרי תוסף ומייצבים. | ריבוי תוספים |
| עיבוד מינימלי | עיבוד מינימלי | המרכיבים הם המוצר — מינימום עיבוד. | עיבוד מינימלי |
| עיבוד תעשייתי גבוה | עיבוד תעשייתי גבוה | רשימה ארוכה עם מייצבים, חומרי טעם, ומרכיבים מעובדים. | עיבוד תעשייתי גבוה |
| חלבון גבוה + בידוד שנוסף | בידוד חלבון שנוסף | הטענה לחלבון גבוה נשענת על בידוד שנוסף — לא על הדגן. | חלבון מוסף — לא מהדגן |

---

### Data Confidence

| What was observed | Short | Medium | Tooltip |
|---|---|---|---|
| רכיבים + ערכים — שניהם זמינים | ציון מאושר | ציון מלא על בסיס רכיבים וערכים תזונתיים. | נתונים מלאים |
| רכיבים זמינים, ערכים לא | ציון חלקי | הציון מבוסס על רכיבים בלבד — ערכים תזונתיים לא זמינים. | חסרים ערכים תזונתיים |
| לא רכיבים ולא ערכים | אין נתונים מספיקים | אין רכיבים ואין ערכים — לא ניתן לנתח. | חסר מידע |
| מרכיב עם פרשנות לא חד-משמעית | מרכיב לא חד-משמעי | אחד מהרכיבים ניתן לפרש בכמה דרכים — ברי בוחרת בפרשנות המרסנת. | פרשנות מרסנת |
| הקמעונאי לא הציג רכיבים | הקמעונאי לא סיפק רכיבים | הדף הדיגיטלי לא כלל רשימת רכיבים. | רשימת רכיבים לא זמינה |

---

## 6. Insight Cards

Five reusable card types. Each type is described in one sentence of purpose, followed by a Hebrew example that should feel like the model. The example is more instructive than any specification.

---

### Expectation Gap

Documents the distance between what a name or label promises and what the ingredient list contains. Title is declarative (4–8 words). Body is 2–3 sentences: the finding, what Bari verified, the scope. No alarm — the gap is the story.

> **מחמצת בשם, שמרים ברכיבים**
>
> 13 מוצרים מתוך 108 שנותחו נושאים "מחמצת" בשמם — ושמרים תעשייתיים מופיעים לפני המחמצת ברשימת הרכיבים. ברי מאמתת את נוכחות המחמצת ברכיבים בלבד, לא בשם המוצר. הממצא מבוסס על מדגם מסופרסל, מאי 2026.

---

### Surprising Mainstream

Corrects the assumption that commodity products are compositionally inferior. Counterintuitive but not clickbait. Curious, not celebratory.

> **פער הציונים בין "בריאות" לרגיל: 9 נקודות**
>
> לחמי ה"בריאות" בסופרסל מקבלים בממוצע 60.0 לעומת 50.7 ללחמים הרגילים. אולם חלק גדול מהפער נובע ממוצרים רגילים ללא מידע תזונתי — לא מהבדל מבני ממשי. בין המוצרים עם נתונים מלאים, ההבדל בסיבים הוא 1.1 גרם בלבד לכל 100 גרם.

---

### Transparency

Tells consumers that a product wasn't scored because data is missing. The absence of a score is a finding, not an apology.

> **46% ללא ציון — כי אין נתונים**
>
> כמעט מחצית ממוצרי הלחם שנסרקו (118 מתוך 256) לא קיבלו ציון — לא בגלל ציון נמוך, אלא כי הקמעונאי לא הציג רכיבים או ערכים תזונתיים. ברי מנתחת רק מה שגלוי.

---

### Mechanism Explainer

Translates how something works — fermentation, fiber source, grain position — without dumbing it down. Answers "how do I check this on a label?"

> **מה ברי בודקת כשמדברים על מחמצת**
>
> תהליך מחמצת מסתמך על תרביות חיות שמתסיסות את הבצק לאורך שעות. כשמוסיפים שמרים תעשייתיים, הם מבצעים את רוב ההתפחה — גם כשמחמצת מופיעה ברכיבים. ברי בודקת האם "מחמצת" מופיעה ברשימת הרכיבים, ואם שמרים מופיעים לפניה. "לחם מחמצת קמח מלא" (ציון 77) עבר את הבדיקה.

---

### Category Pattern

A finding about the shelf as a whole, not a single product. Analytical register — like a market report paragraph.

> **מחמצת — תופעת "הבריאות", לא הממסד**
>
> מתוך 256 מוצרי לחם שנסרקו בסופרסל, 42% ממוצרי ה"בריאות" מכילים מחמצת ברכיבים — לעומת 10% מלחמי הממסד. זאת לא הפתעה: מחמצת אמיתית יקרה יותר לייצור ומצריכה זמן ארוך יותר. מחמצת היא אסטרטגיית מיצוב בקהל הבריאות — לא פרקטיקה שכיחה בקטגוריה הכללית.

---

## 7. What Bari Discloses

Bari's approach to missing data is an editorial position, not a disclaimer. We do not guess. We do not fill gaps. We say what is observable and where we stop.

---

### Three states of data

**ציון מאושר** — ingredient list and nutrition panel both present. Full score.

**ציון חלקי** — ingredient list present, nutrition panel absent. Score shown with: "חסרים ערכים תזונתיים."

**אין נתונים מספיקים** — no ingredient list, or data too sparse to analyze. No score. A transparent message appears instead.

In all three cases, the state is shown to the consumer. Bari does not interpolate from similar products, infer ingredients from product names, or assign scores based on brand.

In the bread category, 46% of scanned products reached the third state — primarily mainstream and challah products from major brands where digital product pages don't include ingredient panels. This is published as a shelf observation, not hidden.

---

### Ambiguity is handled conservatively

When an ingredient can be read in more than one way, Bari applies the interpretation that gives less credit, not more.

"כוסמין" without "מלא" cannot be verified as whole grain — it receives no whole-grain credit. "מחמצת" appearing alongside commercial yeast without declared proportions cannot be confirmed as the leavening agent — it is listed as "מחמצת ושמרים יחד, חלוקה לא ברורה." "שמן" without a type receives no premium oil credit.

The rule is consistent: less confidence, not more claim.

---

### Wording for specific situations

| Situation | What Bari says |
|---|---|
| Nutrition panel absent | "הערכים התזונתיים לא זמינים — הציון מבוסס על רכיבים בלבד" |
| Ingredient list absent | "רשימת הרכיבים לא הוצגה — לא ניתן לנתח" |
| Fermentation proportion unknown | "מחמצת מופיעה ברכיבים — שיעורה ביחס לשמרים אינו מוצהר" |
| Grain proportion unknown | "הרכב הדגנים לא מוצהר — ברי לא מניחה הנחות לגבי הפרופורציות" |
| Flour type unqualified | "סוג הקמח לא צוין — לא ניתן לאמת שמדובר בגרסה המלאה" |
| Data may be outdated | "הנתונים נסרקו ב[תאריך] — ייתכן שהמוצר שונה מאז" |

---

### Where disclosures appear

**On each product card:** one line noting data completeness ("ציון מאושר · רכיבים + ערכים זמינים" or the appropriate partial/insufficient equivalent).

**On each category page:** 2–3 sentences covering coverage percentage, scan date, retailer name, and data source. No technical terminology.

**On the methodology page:** full explanation of how Bari collects, analyzes, and scores — in plain language. This is the one place Bari explains its process in depth. Everywhere else, the process is invisible.

---

### Retailer limitation wording

**Badge:** "ברי מנתחת מידע דיגיטלי בלבד — חלק מהמוצרים לא מוצגים"

**Category page:** "הניתוח מבוסס על נתונים שנסרקו מ[שם קמעונאי] ב[תאריך]. [X]% מהמוצרים לא סיפקו רשימת רכיבים דיגיטלית — מוצרים אלו לא קיבלו ציון. ברי לא משלימה נתונים ממקורות חיצוניים."

**Disclosure line:** "ציון מבוסס על [תאריך] · [שם קמעונאי] · מידע דיגיטלי בלבד"

---

## 8. Next Categories

| # | Category | Why editorially strong | Key expectation gaps | Priority |
|---|---|---|---|---|
| 1 | **יוגורט** | Fermentation verification from bread applies directly. "פרוביוטי" is widespread and uneven. Sugar-protein tradeoffs are unintuitive. Wide compositional range in the Israeli market. | פרוביוטי vs. live cultures in ingredients · "0% שומן" + high sugar · "טבעי" + thickeners · Greek vs. strained definitions | **1** |
| 2 | **דגני בוקר / גרנולה** | "שיבולת שועל" is the strongest wellness halo in Israeli food. Sugar architecture in labeled "natural" cereals is one of the clearest expectation gaps available. | שיבולת שועל vs. refined grain base · Sugar as a primary ingredient in "natural" cereals · Fruit as sugar delivery · Granola as confection-adjacent | **2** |
| 3 | **מוצרי חלב — מתחרים לחלב** | Plant-based protein claims are frequently unsupported by actual content. Fortification vs. native nutrition is a clean, verifiable distinction. | "חלבון כמו חלב" vs. actual content · Fortification vs. natural · Sugar in flavored alternatives | **3** |
| 4 | **חטיפי חלבון / אנרגיה** | High consumer trust. High expectation gap. "Protein bar" spans legitimate sports nutrition to candy bars with a protein number. | Isolate vs. grain protein · "טבעי" + 15+ ingredients · "אנרגיה" = calories, not function | **4** |
| 5 | **שמנים ורטבים** | Olive oil provenance and cold-press claims are verifiable from the label. Simple category, high consumer interest. | "כתית מעולה" vs. blended · Cold-press claims · "דיאט" dressings + sugar substitution | **5** |

Not recommended: supplements (clinical claims, different framework), frozen meals (composite ingredients), processed meat (regulatory complexity).

---

## 9. Simplicity Test

Six questions. A "yes" on any of them means rewrite before publishing.

| # | Question | If yes |
|---|---|---|
| 1 | Would a normal, intelligent reader struggle to understand this? | Rewrite in plainer language |
| 2 | Does this use an internal term (FQC, GSS, structural class, archetype name, synthesis)? | Replace with the plain equivalent |
| 3 | Are we judging rather than describing? | Rewrite as an observation |
| 4 | Is this louder than a Bloomberg paragraph? | Reduce intensity. State the finding. |
| 5 | Does this imply intent or knowledge we don't have? | Replace with what is observable |
| 6 | Does this feel like documentation rather than insight? | Remove the scaffolding. Lead with the finding. |

---

## Appendix: Internal Reference

**For pipeline, scoring, and classification use only. Nothing below this line appears in consumer-facing output.**

---

### Framework Invisibility — Full Mapping

| Internal (engine only) | Consumer-Facing |
|---|---|
| FQC=1 | מחמצת ברכיבים |
| FQC=2 | מחמצת ושמרים — מחמצת עיקרית |
| FQC=3 | מחמצת ושמרים יחד — חלוקה לא ברורה |
| FQC=4 | מחמצת לטעם בלבד — שמרים מתפיחים |
| FQC=5 | מחמצת בשם בלבד |
| No fermentation | ללא מחמצת ברכיבים |
| GSS=100 | קמח מלא ראשון ברשימה |
| GSS=75–99 | בסיס דגן מלא בעיקר |
| GSS=40–74 | קמח מלא ולבן יחד |
| GSS=16–39 | קמח לבן כבסיס |
| Fiber: structural | סיבים מהדגן |
| Fiber: hybrid | חלק מהסיבים מהדגן, חלק נוסף בנפרד |
| Fiber: isolated | סיבים שנוספו בנפרד |
| High fiber + isolated | הסיבים גבוהים — מקורם תוספת |
| Seeds position 1–3 | גרעינים — מרכיב עיקרי |
| Seeds position 4+ | גרעינים — בכמות משנית |
| Structural class A–F | Not shown |
| Score synthesis delta | Not shown |
| Engineering type flag | Not shown |
| Archetype: Honest Simple | consumer sees: "מבנה פשוט" |
| Archetype: Halo Product | consumer sees: "פער בין המיצוב לרכיבים" |
| Archetype: Structurally Strong | consumer sees: "הרכיבים עקביים עם המיצוב" |
| Archetype: Ambiguous Wellness | consumer sees: "חלק מהטענות מאומתות" |
| Archetype: Transparency Failure | consumer sees: "אין נתונים מספיקים" |
| Archetype: Mechanism Mismatch | consumer sees: "פער בין [הטענה] לרכיבים" |
| Confidence: verified | ציון מאושר |
| Confidence: partial | ציון חלקי |
| Confidence: insufficient | אין נתונים מספיקים |

---

### Fermentation Quality Classes (FQC)
FQC=1: מחמצת/שאור in ingredients, no commercial yeast. FQC=2: מחמצת leads, שמרים minor support. FQC=3: both present, proportion undeclared. FQC=4: מחמצת מוגבשת minor, שמרים lead. FQC=5: name only, no fermentation ingredient.

### Grain Structure Score (GSS)
0–100 composite of flour hierarchy (ingredient position), whole grain qualifier, and fiber source quality. GSS=100 = whole grain dominant. GSS=16 = refined base + isolated fiber. Internal synthesis only. Not shown to consumers.

### Structural Classes (A–F)
A = Intact Whole Food · B = Lightly Transformed Traditional · C = Mechanically Fragmented · D = Industrially Reconstructed · E = Engineered Wellness System · F = Structurally Void System. Internal routing and score calibration only.

### Product Archetypes
Honest Simple · Halo Product · Structurally Strong · Ambiguous Wellness · Transparency Failure · Mechanism Mismatch. Consumer sees descriptive language from the mapping above, not the archetype name.

### Evidence Minimums (per signal)
Fermentation verified: מחמצת/שאור explicitly in ingredients. Whole grain credit: "מלא" qualifier present, or whole grain before refined equivalent. Fiber from grain: whole grain in top-3 AND fiber ≥ 4g/100g. Seeds minor: seeds in name AND at position ≥4. Protein isolate: explicit isolate/concentrate term in ingredients.

---

*Bari Editorial Intelligence System v3 — 2026-05-26*
*Evidence base: bread_retail_002_v2 (32 verified), bread_retail_003 (81 coherent / 256 in-scope).*
