---
task: TASK-490
title: Milk product-row antithesis + em-dash sweep — keep-vs-reword ledger
lane: content
base: origin/master (29795088)
scope_file: bari-web/src/data/comparisons/milk_frontend_v1.json
---

# TASK-490 ledger

## Scan method
Regex scan across every rendered product-row copy field (`rowVerdict`, `insightLine`,
`expansion.positiveSignals[]`, `expansion.limitingFactors[]`, `expansion.comparisonContext`)
in `milk_frontend_v1.json`, across ALL antithesis forms:
- `,\s*ו?לא\s` (comma + לא/ולא)
- `(?<!,)\s+ולא\s` (bare, non-comma ולא — the recurring miss)
- `\bאלא\b`
- `,\s*not\s` (English)

Result: **13 antithesis instances found, 13 rewritten. 0 residual (re-scanned after edit).**

Also checked the legacy `bari-web/src/data/milk-comparison.json` (consumerExplanation /
bariInterpretation / consumerTakeaway fields) — it DOES contain further antithesis
instances (~19, in `consumerExplanation.watchOut[]`), but traced every consumer of
`milkProducts` (home-flagship, blog `milk-analysis-content.ts` / `-chart-data.ts`,
`/hashvaot/supermarket`) and confirmed **none of them render `consumerExplanation`,
`bariInterpretation`, or `consumerTakeaway`** — those legacy consumers only use
`image_url`, `name_he` / `shortName` / `displayTitle`, `productTypeLabel`, `score`,
`grade`, `grade_label`, `barcode`. `milkComparisonPage` (the object carrying those
antithesis fields) is referenced nowhere outside `milk-page-data.ts` itself. Per task
scope ("if a rendered legacy row carries antithesis, include it; otherwise stay in
milk_frontend_v1.json") — legacy file is OUT OF SCOPE (unrendered) and was left
untouched.

## Rewrites (barcode-keyed)

### 7290019790259 — rowVerdict
- Before: "...זאת הבחירה למי שרוצה חלב פרה מלא בלי כוכביות, **ולא מוטרד** מאחוז שומן יחסית גבוה."
- After: "...זאת הבחירה למי שרוצה חלב פרה מלא בלי כוכביות **ומקבל בברכה** אחוז שומן יחסית גבוה."
- Fact preserved: same product = plain whole milk, same fat-tolerance framing, now positive.

### 7290114313865 — expansion.comparisonContext
- Before: "...ובתמורה מקבלים חלב מטופל ומועשר **ולא בסיסי לגמרי**."
- After: "...ובתמורה מקבלים חלב מטופל ומועשר, **מדרגת עיבוד מעבר לבסיסי**."
- Fact preserved: same tradeoff (higher protein vs. more processing).

### 7290116936116 — rowVerdict
- Before: "מה שמחזיק אותו באמצע הטבלה **ולא גבוה יותר** זו דווקא הדלילות **ולא איזה תוסף נסתר** — 32 קלוריות..."
- After: "מה שמחזיק אותו באמצע הטבלה **זו בעצם הדלילות עצמה**: 32 קלוריות..."
- Fact preserved: dilution/low-calorie-density is the real driver. Dropped the "not a
  hidden additive" clause — that was purely rhetorical negation with no independent
  fact (no additive was ever named), not a claim to preserve.

### 7290110325619 — rowVerdict
- Before: "...זה נשאר משקה דל בחלבון שמרביתו מים ופחמימה מהדגן — **מאוזן לשתייה יומיומית, לא מקור חלבון**."
- After: "...זה נשאר משקה דל בחלבון שמרביתו מים ופחמימה מהדגן, **מתאים בעיקר לשתייה יומיומית קלילה**."
- Fact preserved: low-protein profile; "not a protein source" replaced by the positive
  framing of its actual use-case (light everyday drink).

### 7290014760141 — expansion.limitingFactors[2]
- Before: "שקדים 4% בלבד — **נגיעת שקדים, לא בסיס שקדים** של ממש"
- After: "שקדים 4% בלבד: נגיעת טעם קלה בתוך משקה שמורכב בעיקר ממים וסוכר"
- Fact preserved: 4% almond content, water/sugar-dominant composition (same number,
  same real driver — now stated positively instead of via negation).

### 7394376620904 — expansion.limitingFactors[2]
- Before: "תחליף מעובד שתפקידו בקפה, **לא משקה תזונתי לשתייה**"
- After: "תחליף מעובד שתפקידו העיקרי הוא מרקם בקפה"
- Fact preserved: product's real functional role (coffee texture) stated directly.

### 7290119385560 — expansion.limitingFactors[2]
- Before: "...ולכן מקומו במכונת הקפה **ולא ככוס לשתייה ישירה**"
- After: "...ולכן מקומו הטבעי הוא במכונת הקפה"
- Fact preserved: same functional-use conclusion, stated positively.

### 7394376619939 — expansion.limitingFactors[0]
- Before: "1.1 ג׳ חלבון בלבד ל-100 מ״ל — דל בחלבון, **בעיקר משקה ולא מקור חלבון**"
- After: "1.1 ג׳ חלבון בלבד ל-100 מ״ל: דל בחלבון, בעיקר משקה שתפקידו במרקם הכוס"
- Fact preserved: same protein number, same "not a protein source" meaning now stated
  as what the product actually IS (a texture-role drink).

### 7394376619939 — expansion.limitingFactors[1]
- Before: "שמן קנולה ומווסת חומציות ברשימה — מוסיפים שומן ומרקם, **לא ערך תזונתי**"
- After: "שמן קנולה ומווסת חומציות ברשימה: מוסיפים שומן ומרקם, תפקידם התפקודי בלבד"
- Fact preserved: canola oil / acidity regulator add fat/texture, not nutrition — now
  said via "their role is purely functional" instead of negation.

### 7394376621451 — expansion.limitingFactors[1]
- Before: "שמן קנולה ומווסת חומציות ברשימה — לטובת מרקם והקצפה, **לא ערך תזונתי**"
- After: "שמן קנולה ומווסת חומציות ברשימה: תפקידם התפקודי הוא מרקם והקצפה"
- Fact preserved: same as above, sibling product (foam variant).

### 7394376621451 — expansion.limitingFactors[2]
- Before: "התאמה להקצפה היא יתרון בכוס בלבד, **לא שיפור תזונתי**"
- After: "התאמה להקצפה היא יתרון תפקודי בכוס, ללא שינוי בערך התזונתי"
- Fact preserved: foam-suitability is a cup-experience win, not a nutrition win.
  ("ללא שינוי" is a plain factual negative-existential, not an X-vs-Y antithesis —
  consistent with existing house style, e.g. "ללא סוכר" used throughout the corpus.)

### 8000215204219 — rowVerdict (2 instances: אלא)
- Before: "...מים, אורז, שמן חמניות, מלח ים. **אלא שהפשטות הזאת לא מתרגמת** לערך תזונתי אמיתי — ... הציון הנמוך כאן **נובע לא מרכיב נסתר אלא מהיעדר ערך**: ..."
- After: "...מים, אורז, שמן חמניות, מלח ים. **הפשטות הזאת נשארת רק על הנייר**: ... הציון הנמוך כאן **מקורו בהיעדר ערך תזונתי**: ..."
- Fact preserved: simple ingredient list does not translate to nutritional value; low
  score stems from absence of value, not a hidden ingredient — now both stated as
  direct positive claims.

### 5411188112709 — expansion.limitingFactors[0]
- Before: "שקדים 2.3% בלבד — **נגיעת טעם, לא בסיס שקדים** של ממש"
- After: "שקדים 2.3% בלבד: נגיעת טעם קלה בתוך משקה שרובו מים"
- Fact preserved: same 2.3% number, same "flavor touch not almond base" meaning,
  restated as what the drink actually consists of (mostly water).

## Kept as-is (no antithesis / no change needed)
No deliberate owner-voice rhetorical `לא` was identified in this file that needed to be
preserved as rhetoric — every instance found was define-by-negation copy from the
pre-overhaul style and was rewritten. Nothing logged under "KEEP."

## Em-dash
Em-dashes were reworded away (→ colon or restructured clause) in every line touched
above. No blanket em-dash removal was performed elsewhere in the file: a cross-category
census (`bari-web/src/data/comparisons/*.json`) shows em-dash is standing house style
across every already-overhauled category (range 5–583 occurrences per file); milk's
remaining count (72) sits mid-pack (juices 80, granola 68, cheese_v5 42) — consistent
with peers, not an outlier. Blanket removal beyond the antithesis-adjacent lines would
be scope creep beyond TASK-490's brief (which named the ולא-form miss specifically).

## Grade letter as crutch
No line in the 13 rewrites names a grade letter (A/B/C/D/E) as a crutch; verified by
inspection during rewrite.
