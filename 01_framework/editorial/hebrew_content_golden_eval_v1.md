# Bari Hebrew Content Golden Eval Framework — v1

**Author:** TASK-220  
**Status:** Draft  
**Companion to:** `assertive_writing_v1.md`, `score_presentation_v1.md`, `ui_language.md`, `bsip2_to_web_translation_contract_v1.md`  
**Applies to:** All AI-generated or editorially authored Hebrew content — comparison pages, caveat boxes, score explanations, ingredient explanations, additive annotations, category insights, blog posts, social comparison cards.

---

## 1. Purpose

Bari repeatedly suffers from weak AI-generated Hebrew content: inaccurate, generic, non-consumer-facing, or not aligned with Bari standards. Better prompting alone is not enough.

This framework defines a structured evaluation process using a small golden eval set that reviewers apply before shipping content. The set grows to 30–50 examples covering all content types.

**What this is:** A quality gate for Hebrew content — the equivalent of the BSIP2 golden corpus for scoring.  
**What this is not:** A style guide — existing editorial docs (`assertive_writing_v1.md`, `score_presentation_v1.md`, `ui_language.md`) define the how; this defines the pass/fail gate.

---

## 2. Evaluation Dimensions

### D1 — factual_accuracy

Is every statement verifiably correct based on the product data, BSIP2 trace, and ingredient panel?

| Score | Meaning | Example |
|-------|---------|---------|
| 3 | All claims match source data; no invented facts | Protein claim matches g/100g value in trace |
| 2 | Minor imprecision that does not mislead | "מכיל פחות סוכר" when the difference is 0.5g — technically true but low-signal |
| 1 | Factual error on a non-critical detail | Wrong additive category stated |
| 0 | Critical factual error | Claims product is NOVA 1 when trace says NOVA 4 |

### D2 — bari_standard_compliance

Does the content adhere to Bari editorial and governance standards?

| Score | Meaning | Violation examples |
|-------|---------|--------------------|
| 3 | Fully compliant — reads like Bari | Tone is investigative, precise, neutral; no forbidden terms; findings-first structure |
| 2 | Minor deviation — still acceptable | Slightly hedging language but not wrong; borderline generic term used |
| 1 | Notable violation | Moralizing ("בחירה חכמה"), generic wellness ("עשיר בנוגדי חמצון"), hedging cascade |
| 0 | Severe violation | Forbidden term ("סופר פוד", "מומלץ", "בריא"), health claim, recommendation language |

### D3 — consumer_usefulness

Would an Israeli consumer shopping for this product find the content actionable?

| Score | Meaning | Example |
|-------|---------|---------|
| 3 | Immediate shopping insight | "5 רכיבים בלבד — החלבון מגיע מהחלב, לא מתוספים" |
| 2 | Informative but not immediately actionable | General category background |
| 1 | Vague or generic | "מוצר איכותי במדף" — tells nothing specific |
| 0 | Useless or confusing | Jargon dump or AI boilerplate that obscures rather than clarifies |

### D4 — hebrew_rtl_quality

Is the Hebrew natural, correctly punctuated, properly formatted for RTL web display?

| Score | Meaning | Fail examples |
|-------|---------|---------------|
| 3 | Native-quality Hebrew | Flows naturally, correct construct state, natural word order |
| 2 | Readable but slightly off | Minor gender/number mismatch or mildly artificial phrasing |
| 1 | Clunky or clearly translated | AI-translation artifacts, non-idiomatic word order, wrong prepositions |
| 0 | Broken | Mixed LTR/RTL artifacts, wrong direction marks, incomprehensible |

---

## 3. Scoring Scale

| Value | Label | Meaning |
|-------|-------|---------|
| 3 | excellent | Meets standard fully; no changes needed |
| 2 | acceptable | Minor issues but shippable with optional touch-up |
| 1 | weak | Needs revision before shipping |
| 0 | fail | Must be rewritten |

---

## 4. Pass/Fail Rules

### Hard thresholds (all must pass):

| Dimension | Minimum score |
|-----------|---------------|
| factual_accuracy | **3** |
| bari_standard_compliance | **2** |
| consumer_usefulness | **2** |
| hebrew_rtl_quality | **2** |

### Automatic fail conditions (overrides all thresholds):

| Condition | Why |
|-----------|-----|
| Any out-of-scope health / medical causation claim | Bari does not make health claims or assert causation. A phrase like "תורם לבריאות הלב" or "עלול לגרום" medical causation = fail regardless of other scores. |
| Any contradiction of Bari scoring logic | Content must agree with the scored output. Saying a D-graded product is "מבנה תזונתי חזק" contradicts the score. |
| Any forbidden term from `ui_language.md` § forbidden language | "סופר פוד", "קלין איטינג", "נטול רגשות אשם", "דיטוקס", "מומלץ", "בריא", "מאושר תזונאים" and all variants. |

> **Precedence rule:** If any governance document conflicts with another,
> `ui_language.md` is the controlling authority for UI-language matters.
> The `assertive_writing_v1.md` tone rules, `score_presentation_v1.md`
> display rules, and this eval framework all defer to `ui_language.md`
> on forbidden terms, tone boundaries, and what constitutes a recommendation.

### Review outcome:

| Result | Meaning |
|--------|---------|
| **PASS** | All thresholds met, no automatic fail condition triggered. Content may ship. |
| **PASS WITH NOTES** | All thresholds met but minor suggestions recorded. Ship optional. |
| **FAIL — MUST REWRITE** | One or more thresholds not met, or automatic fail condition triggered. Blocked. |

---

## 5. Golden Dataset Structure

Target: 30–50 eval records. Records are authored in this document in JSON-like
form, and should later be exported to standalone JSON or JSONL files under
`01_framework/editorial/golden_eval/` for programmatic use (CI gates, automated
eval runners, regression checks). Each record has the following structure:

```json
{
  "id": "GOLDEN-HC-001",
  "content_type": "comparison_page_intro",
  "hebrew_text": "...",
  "expected_scores": {
    "factual_accuracy": 3,
    "bari_standard_compliance": 3,
    "consumer_usefulness": 3,
    "hebrew_rtl_quality": 3
  },
  "auto_fail_conditions": [],
  "expected_result": "PASS",
  "reviewer_notes": "..."
}
```

### 5.1 Content types (8)

| # | Content type | Description | Target count |
|---|-------------|-------------|--------------|
| 1 | comparison_page_intro | Prologue paragraph(s) for a category comparison page (hashvaot/) | 6–8 |
| 2 | yellow_caveat_box | Category-level yellow warning/caveat box (category_caveat_he) | 4–6 |
| 3 | product_score_explanation | Per-product score explanation (insightLine + positiveSignals + limitingFactors) | 6–8 |
| 4 | ingredient_concern_explanation | Explanation of a specific ingredient concern | 4–6 |
| 5 | additive_explanation | Per-additive Hebrew consumer copy (w2_additive_copy) | 4–6 |
| 6 | category_insight | Cross-category insight or trend finding | 3–4 |
| 7 | blog_paragraph | Paragraph from a category analysis blog post | 3–4 |
| 8 | social_comparison_card | Short copy for a card-comparison social post | 2–3 |

### 5.2 Record ID scheme

```
GOLDEN-{CATEGORY_ABBREV}-{NNN}

Primary calibration categories (starter set):
  MK  = milk (clean baseline)
  SN  = snack bars (stress test — processing, additives, marketing)

Secondary categories (future expansion):
  BR  = bread retail        CE  = cereals
  YG  = yogurt              MD  = maadanim
  HM  = hummus              CH  = cheese (general)
  HC  = hard cheeses        BL  = bread light
  J   = juices              SS  = salty snacks

Cross-category:
  GN  = general / cross-category
```

### 5.3 Record status

| Status | Meaning |
|--------|---------|
| `approved` | Human-reviewed and signed off as a reference-standard example |
| `failed` | Human-reviewed as a clear failure — useful as a negative reference |
| `borderline` | Near-threshold case — useful for calibration |
| `draft` | Written but not yet reviewed — placeholder for future review |

### 5.4 Future export format

When records are migrated to standalone files, each record becomes a JSON object
in a `.json` array or a `.jsonl` line. The schema mirrors the in-doc format above.
Recommended file layout:

```
01_framework/editorial/golden_eval/
├── golden_eval_manifest.json      # record index with ids, types, statuses
├── records/
│   ├── GOLDEN-MK-001.json
│   ├── GOLDEN-SN-001.json
│   └── ...
└── archive/                        # superseded or retired records
```

---

## 6. Example Eval Records

Calibration anchor categories: **Milk** (clean baseline — restraint, factual accuracy,
avoiding over-analysis) and **Snacks** (stress test — processing, additives, sodium,
marketing claims, avoiding moralizing language).

Hard cheese appears only as an optional future category-caveat type, not as a
calibration anchor.

### 6.1 Approved — milk score explanation (MK)

```json
{
  "id": "GOLDEN-MK-001",
  "content_type": "product_score_explanation",
  "status": "approved",
  "hebrew_text": "3.4% — ניקוד 85 (A). רכיב אחד: חלב. מפוסטר — לא ממותק, לא מועשר, לא מנורמל. מבנה חלבוני מלא עם 3.2 גרם חלבון ל-100 מ\"ל. רמת עיבוד מינימלית.",
  "expected_scores": {
    "factual_accuracy": 3,
    "bari_standard_compliance": 3,
    "consumer_usefulness": 3,
    "hebrew_rtl_quality": 3
  },
  "auto_fail_conditions": [],
  "expected_result": "PASS",
  "reviewer_notes": "Short, factual, restrained. Every claim is traceable: single ingredient is correct for whole milk, pasteurization is standard, protein count matches trace. No surplus language, no recommendation, no wellness framing. Consumer gets what they need: ingredient count tells them it's unblended; 'not sweetened, not fortified, not standardized' clarifies what it is NOT — useful for a category where many products add DHA or vitamins. Hebrew is clean. This is the baseline standard for the eval set."
}
```

### 6.2 Approved — snack bar comparison intro (SN)

```json
{
  "id": "GOLDEN-SN-001",
  "content_type": "comparison_page_intro",
  "status": "approved",
  "hebrew_text": "חטיפי אנרגיה וגרנולה מחולקים לשתי קבוצות עיקריות: חטיפים שמבוססים על תמרים ושקדים — 4–6 רכיבים, רמת עיבוד נמוכה יחסית; וחטיפים מבוססי דגנים מעובדים — 15–25 רכיבים, עם תוספות סוכר, מעבים וחומרי טעם. הפער במספר הרכיבים אינו מעיד בהכרח על טיב — הוא מעיד על מורכבות עיבוד.",
  "expected_scores": {
    "factual_accuracy": 3,
    "bari_standard_compliance": 3,
    "consumer_usefulness": 3,
    "hebrew_rtl_quality": 3
  },
  "auto_fail_conditions": [],
  "expected_result": "PASS",
  "reviewer_notes": "Structurally divides the category into two real archetypes — date-almond vs. processed grain — both grounded in the actual shelf. No value judgment on which is 'better'; instead states the observable difference (ingredient count, processing complexity). Consumer usefulness: immediately identifies the axis of variation in the category without oversimplifying. No recommendation, no moralizing, no forbidden terms. Hebrew is natural. The closing line ('doesn't necessarily indicate quality — it indicates processing complexity') is a signature Bari move: precise, non-hedged, epistemically honest."
}
```

### 6.3 Failed — milk comparison intro with overclaim (MK)

```json
{
  "id": "GOLDEN-MK-002",
  "content_type": "comparison_page_intro",
  "status": "failed",
  "hebrew_text": "חלב הוא אחד המזונות הטבעיים והמזינים ביותר. הוא מכיל סידן, חלבון וויטמינים החיוניים לגוף. חלב מלא טרי טעים יותר ובריא יותר — בחרו בטרי.",
  "expected_scores": {
    "factual_accuracy": 2,
    "bari_standard_compliance": 0,
    "consumer_usefulness": 1,
    "hebrew_rtl_quality": 2
  },
  "auto_fail_conditions": [
    "generic_wellness_overclaim"
  ],
  "expected_result": "FAIL — MUST REWRITE",
  "reviewer_notes": "'אחד המזונות הטבעיים והמזינים ביותר' — overclaim; Bari does not rank foods as 'most nutritious.' 'ויטמינים החיוניים לגוף' — leans toward health framing. 'בריא יותר' — forbidden comparative health framing. 'בחרו בטרי' — recommendation language. No factual errors (milk does contain calcium, protein, vitamins) but the framing is promotional, not investigative. The genre is comparison page intro, which should orient the consumer to the category, not pitch it. Rewrite as findings-first: observable facts about the shelf (pasteurization types, fat ranges, protein content differences), not value claims about milk itself."
}
```

### 6.4 Failed — snack bar ingredient explanation with moralizing (SN)

```json
{
  "id": "GOLDEN-SN-002",
  "content_type": "ingredient_concern_explanation",
  "status": "failed",
  "hebrew_text": "אחד המרכיבים הבעייתיים בחטיפי גרנולה הוא סירופ גלוקוזה — סוכר מעובד שמוסף בכמויות גדולות. יצרנים משתמשים בו כדי לשפר טעם ולחסוך בעלויות, על חשבון הבריאות של הצרכנים. עדיף לבחור חטיפים ללא תוספת סוכר.",
  "expected_scores": {
    "factual_accuracy": 2,
    "bari_standard_compliance": 0,
    "consumer_usefulness": 1,
    "hebrew_rtl_quality": 2
  },
  "auto_fail_conditions": [
    "manufacturer_moralizing"
  ],
  "expected_result": "FAIL — MUST REWRITE",
  "reviewer_notes": "'על חשבון הבריאות של הצרכנים' — moralizing, attributes negative intent to manufacturers. Bari does not assign motive. 'עדיף לבחור' — recommendation language. 'מרכיב בעייתי' — judgmental framing. 'כמויות גדולות' is vague. The factual kernel is correct (glucose syrup is added sugar) but the tone is consumer-advocacy, not investigative. Rewrite: state the observable fact (glucose syrup appears in X of Y products, typical position in ingredient list, typical g/100g range), let the data speak. No motive, no recommendation, no moral valence."
}
```

### 6.5 Borderline — milk comparison paragraph (MK)

```json
{
  "id": "GOLDEN-MK-003",
  "content_type": "comparison_page_intro",
  "status": "borderline",
  "hebrew_text": "חלב הוא מוצר בסיסי במדף הישראלי, וההבדלים בין סוגיו מצומצמים יחסית לקטגוריות אחרות. ההבדל העיקרי הוא בתכולת השומן: מחלב מלא (3.4%) דרך חלב 1.5% ועד חלב רזה (כ-0.5%). הניקוד הגבוה בקטגוריה (85, A) מגיע לחלב מלא 3.4% — מוצר בעל רכיב אחד ורמת עיבוד מינימלית.",
  "expected_scores": {
    "factual_accuracy": 3,
    "bari_standard_compliance": 2,
    "consumer_usefulness": 2,
    "hebrew_rtl_quality": 3
  },
  "auto_fail_conditions": [],
  "expected_result": "PASS WITH NOTES",
  "reviewer_notes": "Factual accuracy: correct. Numbers trace to run_005_headpin. Bari compliance: acceptable borderline — 'מוצר בסיסי במדף הישראלי' is slightly more informal than ideal Bari tone, and 'ההבדלים מצומצמים' has a whiff of framing. Not a violation, just not as tight as GOLDEN-MK-001. Consumer usefulness: good — immediately identifies the key axis (fat content range) and the top scorer. Hebrew: natural, reads well. PASS WITH NOTES — shippable, but prefer the sharper brevity of GOLDEN-MK-001 as the reference standard."
}
```

---

## 7. Expansion Plan (30–50 records)

Calibration anchors: **Milk** (clean baseline) and **Snacks** (stress test).
Hard cheese may appear as 1–2 caveat examples in later phases, but does not
anchor the golden set.

| Phase | Records | Focus | Timeline |
|-------|---------|-------|----------|
| 1 (this document) | 5 starter records | MK + SN core types, all 3 statuses | Current |
| 2 | 10 records | MK + SN: comparison_page_intro + product_score_explanation | Within 2 weeks |
| 3 | 10 records | Cross-category: yellow_caveat_box + ingredient_concern_explanation | Within 4 weeks |
| 4 | 10–15 records | additive_explanation + category_insight (across BR, CE, YG, HM) | Within 6 weeks |
| 5 | 5–10 records | blog_paragraph + social_comparison_card | Within 8 weeks |

Each record must be:
- Written or reviewed by a Hebrew-proficient human evaluator
- Traceable to an actual BSIP2 product trace or published comparison page
- Checked against the four eval dimensions before being marked `approved` or `failed`

---

## 8. Reviewer Instructions

### Who reviews
- Hebrew-proficient content reviewer (human)
- Familiar with Bari editorial standards (`assertive_writing_v1.md`, `ui_language.md`, `score_presentation_v1.md`)
- Not the person who wrote the content being evaluated

### Review process

1. **Read the content** — understand its type (caveat box vs. score explanation vs. blog), its placement, and its audience
2. **Score each dimension** — assign 0–3 per dimension with a brief justification
 3. **Check automatic fail conditions** — scan for out-of-scope health / medical causation claims, scoring contradictions, and forbidden terms
4. **Determine outcome** — PASS / PASS WITH NOTES / FAIL — MUST REWRITE
5. **Write reviewer notes** — explain what worked and what did not, with specific references

### What to look for per dimension

**factual_accuracy (must be 3):**
- Cross-check every number against the product trace or score data
- Verify category claims (e.g., "highest protein in category" must be true)
- Check that ingredient classifications are correct (e.g., "מעבה" vs "מתחלב")
- If not 3, identify the specific error — do not give a 3 with notes

**bari_standard_compliance (min 2):**
- Reject: recommendation language, moralizing, wellness framing, hedging cascades
- Reject: any term from `ui_language.md` forbidden list
- Check tone: investigative and neutral, not promotional or reassuring
- Check structure: finding-first, not burying the key insight

**consumer_usefulness (min 2):**
- After reading, could the consumer make a more informed choice?
- Does it tell them something specific about this product or category?
- Does it avoid overgeneralization?

**hebrew_rtl_quality (min 2):**
- Read aloud — does it sound like a native speaker wrote it?
- Check: gender agreement, number agreement, construct state (סמיכות)
- Check: no LTR artifacts, no orphaned punctuation
- If AI-translated, check for non-idiomatic preposition usage

### Automatic fail checklist

Check each before scoring:

- [ ] Any out-of-scope health / medical causation claim? ("תורם ל...", "עלול לגרום ל...", "מחזק...", any asserted benefit or harm to the body)
- [ ] Any contradiction of Bari scoring? (e.g., "ניקוד גבוה" for a D product)
- [ ] Any forbidden term? (from `ui_language.md` forbidden language list — the controlling authority)
- [ ] Any recommendation? ("מומלץ", "בחירה טובה", "עדיף לבחור")
- [ ] Any moralizing? (manufacturer intent attributions, "על חשבון הבריאות", consumer shaming)

If ANY of these is YES → **FAIL — MUST REWRITE** regardless of dimension scores.

### Calibration guide

| If the content... | Then it's probably... |
|-------------------|----------------------|
| States traceable facts in Bari tone without surplus | 3 across the board → PASS |
| Has a minor tone deviation (slightly conversational) but is otherwise correct | D2=2, others 3 → PASS WITH NOTES |
| Contains one generic phrase ("איכותי", "מזין") in an otherwise correct text | D2=1 → FAIL — MUST REWRITE |
| Is factually correct but reads like a generic AI output | D3=1 or D4=1 → FAIL — MUST REWRITE |
| Has one wrong fact (wrong NOVA level, wrong protein count) | D1=1 or 0 → FAIL — MUST REWRITE |
| Is basically correct but the Hebrew is clearly translated | D4=1 → FAIL — MUST REWRITE |
