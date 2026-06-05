---
name: bari-bread-refinement-v1
description: "Bread blog stabilization refinement pass v1 — editorial compression, narrative flow, consumer translation, shelf intuition; 8 priority fixes + before/after examples; file at bread_blog_refinement_v1.md"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Built 2026-05-27. Master document at `C:\Bari\02_products\bread_retail_002\bread_blog_refinement_v1.md`.
Based on `bread_blog_v3.md`. Architecture unchanged — editorial refinement only.

**Why:** v3 architecture is correct but still reads as analytical system, not shelf investigation. Ten specific problems: section framing, ontology visibility, narrative flow, consumer translation, shelf intuition, AI writing moments, score explanation density, product groupings, cognitive load.

**How to apply:** This is the final refinement pass before bread category freeze. Apply all "Must apply" fixes before implementation. "Should apply" fixes before review. Architecture in v3.md remains canonical.

## Priority Fixes (must apply)

1. **Remove ScoreDriverTable as standalone section** — CompositionBreakdown already covers it; 13 analytical rows in sequence kills reading rhythm
2. **Rewrite editorial spines** — Article 1 spine has "ingredient list position" (analytical); Article 2 spine is a table of contents, not a spine
3. **Rewrite InsightCards Article 1** — Cards 1/3/4: "הבדיל יותר מכל גורם אחר", "הצדיקו", "יחסו ציונים" all analytical/awkward
4. **Rewrite InsightCards Article 2** — Cards 1/2/4/5: "המחמיץ הראשי", "גבול הנתונים" (apologetic), "מנגנון ההתפחה הדומיננטי"
5. **Add shelf segmentation to intros** — both articles need one sentence naming the real shelf types before InsightCards
6. **Rewrite BreadEverydayMap cluster labels** — "קמח מלא + סיבים מטריצה" → "שיפון / חיטה מלאה — הרכב ברור"
7. **Fix TakeawayList Bullet 2** — "כדאי לבדוק" is advisory/forbidden; rewrite as factual observation
8. **Fix SynthesisParagraph closing** — "המסקנה מהנתונים:" sounds like automated summary

## Key Editorial Problems Fixed

- "מנגנון ההתפחה הדומיננטי" → "מה שמתפיח את הלחם"
- "מטריצת הדגן" → "הדגן עצמו" (consumer-facing)
- "ניתוח שמרני" → "ברי מבססת על רשימת הרכיבים בלבד"
- "הנגזרת מהרכב הדגן" → "שנובעת מהרכב"
- ScoreDriverTable column "מגביר"/"מוריד" → removed (section removed)
- Card 3 Article 2: "הטוב ביותר" x2 → ranking language replaced
- Gap 3 in ThreeGapBreakdown: ⚠ symbol → removed
- fermentation_real=false in product evidence → replaced with Hebrew description

## Narrative Flow Fix

InsightCards currently front-load all findings before the investigation arc. Reader is told the conclusion, then shown evidence. Milk comparison worked because insights were revealed gradually.

Minimal fix (no architecture change): Rewrite Cards 3+4 (Article 1) and Cards 2,4,5 (Article 2) as entry points/questions that CompositionBreakdown and ThreeGapBreakdown answer — not as complete spoiler findings.

## Wording Substitution Table

| Analytical | Consumer-clear |
|---|---|
| מטריצת הדגן | הדגן עצמו |
| מחמיץ ראשי | מה שמתפיח |
| מנגנון ההתפחה | מה שמתפיח |
| מאומת/לא מאומת | מצוין ברשימה / לא מצוין |
| אינדיקטור | מה שמסביר |
| הנגזרת מהרכב | שנובעת מהרכב |
| ניתוח שמרני | מבוסס על רשימת הרכיבים בלבד |

[[bari-bread-blog-v3]]
[[bari-assertive-writing-v1]]
[[bari-editorial-intelligence-v1]]
