# Snacks Explanation Engine Review v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Explanation Quality Audit + Rebuild Design

---

## Part 1: Explanation Quality Audit

### Current Explanation Inventory

Every explanation in the current snacks corpus is classified below.

**Classification criteria:**
- **Strong:** Explains why the score is what it is. Names a specific mechanism. Supports a ranking claim. Would not apply to other products.
- **Plausible:** Directionally true but vague or unverifiable.
- **Generic:** Could be copied to any product in the category. Contains no product-specific information.
- **Unsupported:** Makes a claim that is not verifiable from available data.
- **Misleading:** Creates a false impression of what the score means.

---

### insightLine Audit

| Product | insightLine | Classification | Problem |
|---|---|---|---|
| snk-001 | 4 רכיבים בלבד, תמרים כרכיב ראשון וללא סוכר מוסף | Plausible | Reports the observation correctly. Does not explain why 70/B (vs 60/C). No mechanism for the grade level. |
| snk-004 | בסיס רב-דגן עם עיבוד בינוני; טוב יותר ממרבית המדף אך לא פשוט | Generic | "טוב יותר ממרבית המדף" is self-referential. Does not tell the consumer what specifically is better or what "לא פשוט" means. |
| snk-002 | בסיס תמרים פשוט עם ציפוי קקאו, ללא ריבוי ממתיקים | Plausible | Accurately describes the structure. Does not explain the 14-point gap from snk-001 with any specificity. |
| snk-015 | 5 רכיבים, בסיס תמרים-בוטנים נקי — 15 נקודות מתחת לגרסת השקדים | Strong | **One of the best in the corpus.** Gives the count, names the base, provides the gap number, names the comparison product. Specific and falsifiable. |
| snk-003 | שיבולת שועל בולטת אך עיבוד בינוני ותוספות מתונות מורידים ציון | Plausible | "תוספות מתונות" is vague. "עיבוד בינוני" is a classification label, not an explanation. Does not explain what "תוספות מתונות" means in practice. |
| snk-016 | גרסת הטופינג של מרבה סלים: אגוזי לוז על גבי בסיס דגן | Generic | Describes the product's marketing positioning. Contains no scoring information. This is a product description, not an explanation. |
| snk-009 | מיצוב פרוטאין עם מערכת רכיבים מהונדסת ועומק עיבוד גבוה | Plausible | "מערכת רכיבים מהונדסת" — what does this mean exactly? How many ingredients? What type of engineering? The consumer cannot verify this. |
| snk-005 | קמח + סירופ כבסיס, עיבוד מרבי וריבוי תוספות למרות מיצוב פיטנס | Strong | **Best explanation in the corpus.** Names the primary ingredients (flour + syrup), identifies the processing level, names the marketing contradiction. Specific, verifiable, and consumer-relevant. |
| snk-018 | גרסת השוקולד של קראנצ'י — שיבולת שועל ראשון, אבל חתיכות שוקולד מורידות 7 נקודות | Strong | Excellent sibling comparison. Names the parent product, acknowledges what's good (oats first), explains the penalty mechanism, gives the exact point gap. |
| snk-010 | אותו דפוס פרוטאין ממותג: עיבוד מרבי ועומס תוספות | Generic | "אותו דפוס" is a template phrase. This explanation is almost identical to snk-009's. They are two different products but receive essentially the same explanation. |
| snk-011 | תמרים בשם אך עומק עיבוד גבוה וסוכרים מוספים ברשימה | Plausible | The "name vs reality" contrast is the right frame. But "עומק עיבוד גבוה" for a date bar is surprising — what makes it highly processed? The explanation doesn't say. |
| snk-012 | מיצוב טבעי עם קקאו, אבל עיבוד מרבי ועומס סוכרים מאחורי הקלעים | Plausible | Similar to snk-011. "מאחורי הקלעים" is a colloquial phrase that obscures what is actually happening in the ingredient list. |
| snk-019 | שיבולת שועל ודבש בשם — עיבוד מרבי וסירופ גלוקוז-פרוקטוז בהרכב | Strong | **Third-strongest in corpus.** Names the marketing ingredients (oat, honey), then names the actual problematic ingredient (HFCS). Consumer can verify this if they read the label. Specific and falsifiable. |
| snk-017 | קו ה-Chewy של נייצ'ר וואלי — אותו מותג, 8 נקודות פחות מה-Protein | Plausible | Good sibling comparison. But "8 נקודות פחות" without explanation of what drives the gap is incomplete. Why is Chewy worse than Protein within the same brand? |
| snk-020 | גם מרבה סלים מגיע ל-E: קריספי עם סוכר גבוה ומרכיבים מפתיעים | Unsupported | "מרכיבים מפתיעים" — which ingredients? What is surprising? This phrase is a placeholder that signals knowledge without delivering it. |
| snk-007 | ציפוי שוקולד מעל בסיס מהונדס עם ריבוי ממתיקים | Generic | Template phrase. Same structure as snk-006 and snk-013. Interchangeable among three products. |
| snk-006 | אותו מדף גרנולה, אבל בסיס מהונדס מאוד עם עומס תוספות גבוה | Generic | "מאוד" and "גבוה" are intensity words without data. "אותו מדף" references another product without naming it (snk-007 presumably). |
| snk-013 | הציון הנמוך ביותר בקטגוריה: עיבוד מרבי, ריבוי ממתיקים ותוספות | Misleading | "הציון הנמוך ביותר בקטגוריה" is a ranking claim, not an explanation. It tells the consumer where the product sits, not why it sits there. The rest is a list of three generic labels. |

---

### Strong / Plausible / Generic Distribution

| Classification | Count | % |
|---|---|---|
| Strong | 4 (snk-005, 015, 018, 019) | 22% |
| Plausible | 8 | 44% |
| Generic | 4 | 22% |
| Unsupported | 1 (snk-020) | 6% |
| Misleading | 1 (snk-013) | 6% |

Only 22% of explanations are strong. The majority are plausible but vague. Every "generic" explanation could be removed and replaced with something specific without losing any information, because they contain no product-specific information.

---

### Pattern Analysis: Generic Phrases Currently Used

These phrases appear across multiple products and add no differentiation:

| Phrase | Products | Problem |
|---|---|---|
| "עיבוד מרבי" | 8+ products | Processing classification label. What does it mean for THIS product? |
| "בסיס מהונדס" | 3 products | Engineering label. What is engineered? How? |
| "ריבוי ממתיקים" | 5+ products | How many? Which ones? What does "ריבוי" mean (2? 3? 5?)? |
| "עומס תוספות" | 4+ products | Load is undefined. Same label applied to 17 and 29 scoring products. |
| "מיצוב פיטנס" | 5+ products | This is a marketing observation, not a nutritional explanation. |
| "בסיס שלם" | 3 products | The key claim that drives top scores — barely defined. |
| "5+ תוספות" | 3 products | This is slightly better — numeric. But which 5+ additives? |

---

## Part 2: Explanation Engine Rebuild Design

### Principle

Every explanation must answer six questions:

1. **Why this score?** — What is the primary mechanism that placed this product here?
2. **What helped?** — Name the specific structural or compositional element that benefited the score.
3. **What limited?** — Name the specific element that held the score back.
4. **What tradeoff?** — What does the consumer get and what do they pay for it?
5. **What should the consumer understand?** — The one sentence that changes how they think about this product.
6. **Why here vs neighbors?** — Why is this product above or below the nearest-scored product?

### Template Architecture

**insightLine (30–50 chars):** The one undeniable fact. The first ingredient. The single most important structural reality. Should be falsifiable by reading the product label.

> BAD: "עיבוד בינוני עם מיצוב פיטנס"  
> GOOD: "קמח חיטה לפני שיבולת שועל — המדף מוכר גרנולה, המרכיבים מוכרים קמח"

**positiveSignals:** Specific and verifiable. Not categories — facts.

> BAD: ["בסיס שלם", "עיבוד מינימלי"]  
> GOOD: ["שיבולת שועל כרכיב ראשון, לפני כל ממתיק", "6 מרכיבים בלבד"]

**limitingFactors:** The cost the consumer pays, in plain language.

> BAD: ["עיבוד מרבי", "5+ תוספות"]  
> GOOD: ["סירופ גלוקוז-פרוקטוז כממתיק שני אחרי הדבש", "28 גרם סוכר ל-100 גרם — כמו שוקולד חלב"]

**bottomLine:** The verdict sentence. Must include the score number, the grade, and one comparative reference.

> BAD: "מוצר פיטנס עם בסיס דגן — לא הבחירה הנקייה ביותר, אבל 58/C מעל ממוצע הקטגוריה"  
> GOOD: "שיבולת שועל מוכיחה את עצמה כרכיב ראשון — הסירופ שמאחוריה עולה 7 נקודות ומוריד מ-C ל-D"

**comparisonContext:** Name the nearest-scored sibling and state the gap mechanism explicitly.

> BAD: "חטיפי גרנולה ושיבולת שועל"  
> GOOD: "3 נקודות מתחת לקראנצ'י דבש (53/C): שוקולד מוסיף סוכר, מוריד דרגה"

---

### Rebuilt Examples

**snk-001 (70/B) — Current:**
> "4 רכיבים בלבד, תמרים כרכיב ראשון וללא סוכר מוסף."

**snk-001 (70/B) — Rebuilt:**
> insightLine: "4 מרכיבים: תמרים, שקדים, חמאת שקדים, קקאו — כל מה שיש על האריזה, יש בפנים."
> positiveSignals: ["4 מרכיבים בלבד — הרשימה הקצרה ביותר בקטגוריה", "תמרים הם המרכיב הראשי, לא ממתיק מוסף", "ללא ויטמינים, מייצבים, או תוספות"]
> limitingFactors: ["תמרים הם ~60% סוכר פשוט — מאכל מרוכז מבחינת אנרגיה"]
> bottomLine: "70/B — הציון הגבוה ביותר במדף. בסיס הנקי ביותר. אבל תמרים הם לא ירקות — הסוכר הטבעי שלהם ריאלי."
> comparisonContext: "גרסת הבוטנים (snk-015) מקבלת 55/C — 15 נקודות פחות, מאותם 5 מרכיבים עם שומן רווי מעט גבוה יותר."

---

**snk-005 (46/D) — Current (already strong):**
> "קמח + סירופ כבסיס, עיבוד מרבי וריבוי תוספות למרות מיצוב פיטנס."

**snk-005 (46/D) — Rebuilt:**
> insightLine: "קמח חיטה לפני כל שיבולת שועל — מה שנקרא 'פיטנס' מתחיל בבסיס קמחי."
> positiveSignals: ["דגנים ברשימה — לא רק קמח", "מוצר ממותג עם אחידות ייצור"]
> limitingFactors: ["קמח חיטה הוא מרכיב ראשון — לפני שיבולת שועל", "סירופ גלוקוז-פרוקטוז כממתיק מוסף", "מייצבים ומרככים ברשימה"]
> bottomLine: "46/D — מדף הפיטנס לא מבטיח בסיס דגן שלם. שם ה'פיטנס' עולה יותר מהמרכיבים."
> comparisonContext: "5 נקודות מתחת לגרסת שיבולת שועל-דבש (snk-019 41/D) — שתיהן Fitness, שתיהן D, אבל הקלאסי מגיע ממעמד גבוה יותר בגלל פחות ממתיקים."

---

**snk-013 (13/E) — Current:**
> "הציון הנמוך ביותר בקטגוריה: עיבוד מרבי, ריבוי ממתיקים ותוספות."

**snk-013 (13/E) — Rebuilt:**
> insightLine: "קורני שוקולד הוא ופל שוקולד עם מילוי קרם — לא חטיף, קינוח."
> positiveSignals: ["מוצר קינוח ידוע עם מחיר גלוי"]
> limitingFactors: ["30% מהמשקל הוא קרם מוגבה — מבנה קינוחי, לא חטיף", "4+ ממתיקים שונים ברשימה", "כוכב הרכיבים הוא שומן צמחי מוקשה, לא דגן"]
> bottomLine: "13/E — הציון הנמוך במדף. אם קונים קינוח, הציון אומר: קנו אחד קטן ותהנו. אם קונים 'חטיף' — זה לא חטיף."
> comparisonContext: "16 נקודות מתחת לפיטנס גרנולה (snk-006, 17/E) — שניהם E, אבל קורני הוא קינוח שלם, לא ניסיון כושל להיות חטיף."

---

### Summary: What the Explanation Engine Needs

1. **Replace category labels with specific ingredient facts** ("עיבוד מרבי" → "קמח חיטה לפני שיבולת שועל")
2. **Add numeric anchors** — calories, sugar grams, ingredient count (not approximations — only when data exists)
3. **Build the sibling comparison into every explanation** — every product should reference its nearest-scored neighbor
4. **Separate structural story from nutritional story** — clearly label when a claim is structural inference vs nutritional fact
5. **Make the grade defensible** — the bottomLine must explain why THIS grade (not D in general, but why 46/D not 40/D or 52/C)
6. **Include one consumer-decision sentence** — what does this mean for how I eat, not just what the product contains
