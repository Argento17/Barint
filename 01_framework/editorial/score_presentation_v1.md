# Bari Score Presentation Philosophy — v1
**Date:** 2026-05-27
**Status:** Canonical. Supersedes any prior grade-label conventions.
**Applies to:** All consumer-facing score display — web, app, blog, API frontend

---

## The Problem This Document Solves

Labels like חזק, בינוני, חלש introduce a layer of judgment on top of a multidimensional composite score.

The problem is not aesthetic. It is epistemic.

"חזק" — strong in what sense? Strong grain structure? Strong fermentation evidence? Strong fiber density? Strong label transparency? The score encodes all four simultaneously. The label collapses them into a single sentiment that hides the reasoning instead of surfacing it.

Worse: it shifts Bari's posture from *interpretation* to *recommendation*. "חזק" implies someone decided this product is good. Bari does not decide that. Bari documents what is present, what is absent, and where the gap is.

The numeric score already performs the multidimensional interpretation. The presentation layer's job is to make that interpretation inspectable — not to simplify it further into a feeling.

---

## What the Score Encodes

The Bari score is a composite interpretation across four observable dimensions:

- **Grain structure** — flour hierarchy, whole grain qualifier, refinement level
- **Fiber source** — matrix-native versus matrix-added (e.g., inulin, chicory root)
- **Fermentation quality** — traditional culture versus commercial yeast, hybrid cases
- **Label alignment** — name-to-ingredient consistency, marketing-to-composition gap

The score is a finding. The grade is a range marker. Neither is a recommendation.

---

## Score Presentation Rules

### Rule 1 — Primary Display

**Format:** `[score] / [grade]`

**Example:** `72 / B`

Nothing else at this level. No label. No descriptor. No sentiment. No icon with emotional valence.

The grade letter is a range indicator, not a judgment. Its purpose is orientation — "where in the distribution does this fall" — not evaluation.

---

### Rule 2 — Grade Ranges

| Grade | Range | What it encodes |
|-------|-------|-----------------|
| A | 80–100 | Consistent alignment across most measured dimensions |
| B | 65–79 | Partial alignment; at least one dimension strongly evidenced |
| C | 50–64 | Mixed signals; label positioning outpaces ingredient evidence in at least one dimension |
| D | below 50 | Recurring gap between product presentation and ingredient reality |

**Critical:** These descriptions are factual, not evaluative. They describe what the data shows. They do not tell the consumer what to do with it.

Grade descriptions in this table are for internal understanding only. The grade letter `A / B / C / D` is the only consumer-facing element.

---

### Rule 3 — Secondary Display

When space allows, show 1–3 observable facts that account for the score.

**Format:** `[dimension]: [finding]`

These are evidence lines, not interpretations.

**Examples:**

```
סיבים: 6.2 גרם (ממקור מטריצה)
```
```
תסיסה: שמרים תעשייתיים בלבד
```
```
קמח: חיטה מלאה ראשון ברשימה
```
```
תסיסה: מחמצת + שמרים תעשייתיים
```
```
קמח: קמח לבן ראשון, כוסמין שלישי
```

Each line is a direct observation from the ingredient list or nutrition panel. Nothing inferred. Nothing evaluated.

Maximum 3 lines. Minimum 0. Do not pad to reach 3.

---

### Rule 4 — Contextual Insight (Optional)

One sentence. Editorial use only — article body, product dossier pages, insight cards. Not in list views or search results.

The sentence explains what the score reflects. It does not recommend.

**Approved:**
```
הציון משקף קמח מלא כראשון ברשימה ונוכחות מחמצת אמיתית בלי שמרים תעשייתיים.
```
```
הציון מוגבל על ידי שימוש בקמח לבן כבסיס, למרות שם המוצר שמרמז על כוסמין מלא.
```
```
הציון מייצג תסיסה מאומתת, אך מקור הסיבים מעורר שאלה — רובם ממחומי פסיליום ואינולין.
```

**Forbidden:**
```
מוצר חזק המומלץ לצרכנים המחפשים לחם איכותי.
```
```
ציון נמוך — עדיף להימנע.
```
```
בחירה טובה לארוחת בוקר בריאה.
```

The line test: does it describe the finding, or does it advise the consumer? If the latter — remove it.

---

### Rule 5 — Confidence Display

Three states. Always explicit. Never blank.

**Verified** — ingredients and nutrition available and internally consistent.

Display: score as-is.
```
72 / B
```

**Partial** — ingredients available, nutrition incomplete or unavailable.

Display: score with qualifier.
```
72 / B · ניתוח חלקי
```
Secondary line (mandatory when partial): state what is known and what is not.
```
ניתוח מבוסס על רשימת רכיבים בלבד. ערכי סיבים לא אומתו מלוח תזונה.
```

**Insufficient** — ingredients unavailable, unreadable, or insufficient for scoring.

Display: no score. Explicit explanation.
```
לא נוקד
```
Secondary line (mandatory): one sentence explaining the absence.
```
רשימת הרכיבים לא זמינה לאימות.
```

**Never:** `—`, `N/A`, blank field, question mark, or score displayed without confidence indication when data is partial.

The absence of a score is itself a finding. Treat it as one.

---

## What Never Appears

| Forbidden | Why |
|-----------|-----|
| חזק | Hides which dimension is "strong" and frames the score as approval |
| בינוני | Mid-range on which dimension? Collapses multidimensional data |
| חלש | Judgment without reference point; functions as a warning label |
| מצוין | Superlative implies recommendation |
| מומלץ | Explicit recommendation framing — not Bari's role |
| לא מומלץ | Negative recommendation — not Bari's role |
| ✓ טוב / ✓ בריא | Health claim outside Bari's scope |
| ⚠ הימנע | Avoidance directive |
| כדאי לקנות | Purchase advice |
| הכי טוב בקטגוריה | Ranking that implies a winner |
| Colored score backgrounds (red/yellow/green) | Color encodes judgment invisibly — same problem as the label |

**Note on color:** A green badge on a high score and a red badge on a low score are functionally identical to writing "חזק" and "חלש." The prohibition applies to visual encoding as much as to words.

---

## The Positioning Distinction

Bari score presentation should feel like:

> A well-researched analyst showing you what the data says.

Not like:

> A nutritionist telling you what to buy.

The analyst shows the finding and trusts you to use it. The nutritionist simplifies the finding into guidance. Bari is the former.

This is not a neutral distinction. It is strategic. The moment Bari's scores feel like recommendations, every low-scoring product becomes a product Bari is "against." That is a legal exposure, a commercial liability, and — most importantly — a misrepresentation of what the score actually encodes.

---

## Applying This to the Bread Dataset

**Current distribution** (bread_retail_002, 81 coherent products):

| Range | Count | What to display |
|-------|-------|-----------------|
| 80–100 | 1 | `82 / A` |
| 65–79 | 33 | `72 / B`, `71 / B`, etc. |
| 50–64 | 22 | `62 / C`, `56 / C`, etc. |
| below 50 | 25 | `48 / D`, `40 / D`, etc. |

**Not scored** (27 products): `לא נוקד` + reason.

No product in this dataset should carry a label. The numeric score and grade letter carry all the differentiation needed.

---

## The Core Rule

Bari shows what it found.
The consumer decides what to do with it.

The score is a finding.
The grade is a range marker.
The contextual insight is an interpretation.

None of these are recommendations.

When a display element pushes toward recommendation — remove it, regardless of how natural it feels.

---

## Relationship to Editorial Intelligence v3

This document governs score display mechanics.
Editorial Intelligence v3 governs language, insight cards, transparency disclosure, and editorial voice.

They are complementary. When score display intersects with editorial copy — insight card body text, contextual insight sentences, product dossier writing — both documents apply. Score display rules take precedence when there is a conflict on label use.
