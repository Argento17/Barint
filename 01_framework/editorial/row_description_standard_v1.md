# Bari Row Description Standard — v2 (Interpretive Verdict model)

**Status:** DRAFT — RETURNED for Nutrition + QA + orchestrator review (TASK-168E)
**Date:** 2026-06-02
**Owner:** Content Agent
**Scope:** Every per-product row description (`insightLine` / `rowVerdict`) across all live comparison categories
**Extends:** `insight_line_spec_v1.md` (base) · `assertive_writing_v1.md` (floor) · `editorial_intelligence_v3.md` (forbidden words) · `comparison-template-standard-v1.md` (page geometry)
**Pairs with:** Nutrition's per-category grounding guide (`row_description_grounding_v1.md`) — what each category's verdict may *truthfully* cite
**Supersedes:** v1's terse decision-driver single-line model (35–80 char tag). See §0 for the pivot.

> **v3 PATCH (2026-07-08, TASK-533 round 2, C3 ruling — binding):** this document's central "grade-as-earned-payoff" move (§0's "approved target voice," §2a, §32/§34 below) is **RETIRED.** Grade recitation in verdict prose ("עוצר ב-B כי…") is now banned outright — see §2a's replacement text and §5d. Everything else in this v2 model (standing → why → catch, anti-template rule, trace-anchor requirement, length gate) still stands; only the "name the grade" ending is gone. Read §2a and §5d before writing any verdict from this document.

---

## 0. Why this exists — and what changed in v2

**The v1 model (terse decision-driver tag) was rejected by the owner after the maadanim pilot.** A 35–80 char single fact ("בננה בשם, סוכר ברכיב השני") is correct information but reads *mechanical* — a label, not an assessment. The owner's words: *"I want the analysis of this product — the content writer should tell me 'we analyzed this; it's outstanding for the category, here's why (x, y, z); we did flag some issues like over-engineering, so we gave it B.'"*

**v2 pivots the collapsed row from a tag to a 2-line interpretive VERDICT.** The line is now a short piece of writing by a human assessor: where the product *stands* in its category, *why* (the real drivers), the honest *catch*, and the *grade as the conclusion of that reasoning*. The dropdown still carries the full analysis + nutrition; the collapsed line is the verdict that makes the reader trust the dropdown is worth opening.

**The approved target voice — יופלה GO 78/B:**
> מהבולטים בקטגוריה — 10 גרם חלבון מהחלב ושלושה רכיבים בלבד, נדיר במדף של ממתיקים ומייצבים. עוצר ב-B כי הבסיס בנוי על חלב ואבקת חלב מועשרים, לא על מבנה חלב שלם.

Read how it works: it *stands the product in the category* ("מהבולטים בקטגוריה"), gives the *real reasons* (10g protein from milk, 3 ingredients, rare on this shelf), then the *honest catch and the earned grade as its payoff* ("עוצר ב-B כי הבסיס בנוי על חלב ואבקת חלב מועשרים"). That is the bar every one of the 84 verdicts must clear.

> **TASK-175 correction (Nutrition, 2026-06-03):** the original example ended "עוצר ב-B כי הבסיס עדיין מעדן מתוק, לא מוצר חלבון" — an **un-grounded** catch. GO's sugar value is unavailable (null), its 3-ingredient list has no sweetener, and the trace shows `sweetener_detected=false` / 0 added-sugar markers / zero sugar penalty. The B is driven by `nutrient_density` (protein-only) and the **reconstituted/enriched dairy base** (NOVA 2; added חלבוני חלב + אבקת חלב; fails the intact-matrix A-condition, RULING-DAIRY-A-01 C4) — not by sweetness. The catch was rewritten to the real, trace-anchored reason. This is the canonical illustration of the §grounding rule below: **the catch must name a signal the trace actually fired.**

### What v2 keeps from v1 (still true)
- **Trace-anchored, always.** No invented number, ingredient, position, or claim. The grounding guide governs what is citable per category.
- **No wellness / moralizing / verdict words** (בריא, כדאי, מטעה, גרוע, איכותי…). Name the fact; never deliver a health verdict.
- **Decision-relevant lead.** The verdict still opens on what matters most for *this* product — now expressed as a standing/assessment, not a bare tag.
- **Plain shelf Hebrew, RTL phrasing.**

### What v2 reverses or relaxes from v1
- **Length:** the 35–80 char / ≤12 word gate is **retired**. New gate: a 2-sentence verdict that fits ~2 lines without truncation — **roughly ≤170 characters** (§3).
- **Grade restatement:** v1 *banned* naming the grade. v2 **reverses this into a grade-RATIONALE rule** — naming the grade as the earned payoff of a real reason ("עוצר ב-B כי…", "נשאר ב-D כי…") is now *correct and wanted*. Only *empty* restatement ("הציון משקף…", "ה-B מבוסס על…") stays banned (§2a).
- **One-fact discipline → reasoned mini-assessment.** v1 wanted one driver, full stop. v2 wants standing + reason(s) + catch + grade — a small argument, not a fragment.

**North star (sharpened):** the reader should feel *"a person assessed this product for me and told me straight,"* not *"software captioned a row."*
> "ברי בדקה את המוצר. הנה מה שמצאנו, וזה הציון — והנה למה."

---

## 1. The Verdict Rule (standing → why → catch → earned grade)

**The rule:** Each verdict is a short, human assessment of *this* product, built from up to four moves — written naturally, not as a fill-in template:

1. **STANDING** — where the product sits in its category. ("מהבולטים בקטגוריה" / "מהחלשים במדף" / "מהמעטים שדווקא…" / "אחד החריגים — …"). The standing is the reader's first orientation: is this near the top, the bottom, or an odd case?
2. **WHY** — the real driver(s) behind that standing, from this product's actual data: the protein and its source, the ingredient count, the defining sugar/sweetener, the name-vs-reality gap, a category-worst figure. Two or three concrete reasons, not a list.
3. **CATCH** — the honest complication that holds it back (or, for a strong product, the reason it isn't higher). Named, never moralized.
4. **EARNED GRADE** — the grade stated as the *conclusion of the reasoning*: "עוצר ב-B כי…", "נשאר ב-D כי…", "יורד ל-E בגלל…". The grade is the payoff of a real reason — never an empty restatement.

Not every verdict uses all four, and the *order can vary* — that is the point (§ anti-template). A category-worst might lead with the catch; a rare clean product might lead with its standing; an icon paradox might lead with the name-vs-grade gap. The four moves are a toolkit, not a sentence skeleton.

**The test for a finished verdict:** *"Does this read like a person who assessed the product and is telling me straight — its place on the shelf, the real reasons, the catch, and why that grade?"* If it reads like a caption or a label, it fails.

### Anti-template / differentiation rule (the core ask)

**Every verdict is a fresh reading of THAT product. No shared sentence skeleton across products.** Lead from whatever is *genuinely distinctive* about each one:

- For a high-protein clean cup → lead from the protein and the short list.
- For a famous icon that scores low → lead from the icon-vs-architecture paradox (the מילקי line).
- For a "ללא פירות" / "מעודנת" / "דיאט" label → lead from the name-vs-reality gap.
- For a fruit-concentrate dessert → lead from the standout figure (52g sugar in a 3-ingredient list).
- For an ordinary mid-shelf cup → an honest, quiet standing is correct; do **not** manufacture drama.

**Similar products may read similarly *only where they are genuinely similar*** (e.g. several near-identical גמדים cups). Everywhere else, differentiate the lead, the rhythm, and the catch. Write for the reader scanning the shelf, not for the rubric. If two verdicts could be swapped between products without anyone noticing, at least one is wrong.

### Don't bury the assessment

The failure mode is the same as v1's trivia-first, one level up: opening on a footnote ("כמות לא מצוינת על האריזה") instead of the standing and the real reason. Open on the assessment; let the footnote, if it earns a place, come after.

---

## 2. Hard Bans

These extend the existing forbidden lists in `insight_line_spec_v1` (§Tone) and `assertive_writing_v1` (§4). A line containing any of these does not publish.

### 2a. Grade-recitation ban (v3 reversal — C3 ruling, TASK-533 round 2, 2026-07-08)

**SUPERSEDED.** v1 banned naming the grade. v2 (below, kept for the historical record) reversed that into a "grade-as-earned-payoff" rule ("עוצר ב-B כי…"). **v3 reverses v2 back to a ban, and this time it is final.** The owner's live-review of the yogurt pages (TASK-533) found the v2 model — even executed well — reads as **the row captioning its own score chip**: the grade already sits beside the verdict as a badge (72/B); a verdict that also says "עוצר ב-B" is the UI restating itself in prose, and every verdict that leads with the grade-reason move starts sounding the same regardless of the product ("X. עוצר ב-B כי Y" is itself a template skeleton — see §5d Rule 1).

**BANNED — any verbal grade reference in `rowVerdict` / `consumerTakeaway` / `insightLine` / `expansion.consumerExplanation.whyRated`:**
```
נשאר ב-A / עוצר ב-B / יורד ב-D / נשאר ב-E
עוצר ב-B — זה מה שמעצב את הציון כאן
B הוא הציון שההרכב הזה מרוויח בפועל
זה הגורם המרכזי שממתן את הציון ל-C
הציון משקף… / ה-B מבוסס על הציון
```
The grade badge (72/B) is rendered beside the text by the UI. The verdict text says what's true about the **food**; it never states, restates, or leads to the letter. If a sentence would read differently depending on whether the grade were A or D, that dependency itself is the leak — write the same honest food-observation and let the badge carry the grade.

**Relative position remains allowed** (adds information the chip can't show, and never restates the grade itself):
- ALLOWED: "מהבולטים בקטגוריה" / "מהחלשים במדף המעדנים" / "הרשימה הקצרה ביותר במדף"
- ALLOWED: comparison to a *named peer* with the reason ("רשימה קצרה מהשוקולד הלאומי של הגולן").

<details>
<summary>v2 text (2026-06-02, RETIRED 2026-07-08 — kept for history, do not follow)</summary>

**v1 banned naming the grade. v2 reverses this.** Naming the grade as the **earned conclusion of a real reason** is now correct and wanted — it is the fourth move of the verdict (§1). The owner's example *requires* it: "עוצר ב-B כי הבסיס בנוי על חלב ואבקת חלב מועשרים."

**WANTED — grade as the payoff of a reason:**
```
עוצר ב-B כי [real reason]          ("…ושלושה רכיבים בלבד. עוצר ב-B כי הבסיס בנוי על חלב ואבקת חלב מועשרים.")
נשאר ב-D כי [real reason]
יורד ל-E בגלל [real reason]
מטפס ל-C על [real reason] — אבל [catch]
```
The grade names the conclusion the reasoning earned. This is the verdict landing.

**STILL BANNED — empty restatement (naming the grade with no reason, or echoing the chip's machinery):**
```
הציון משקף…             (the score "reflects" — circular, no information)
ה-B מבוסס על הציון / מבוסס על הציון
הציון נמוך/גבוה          (the score as the subject, with no driver)
זוכה ל-[grade]           (with no stated reason)
"כפי שמשקף הציון"        (appears in some live limitingFactors — never in a verdict)
```

**The test:** does the grade arrive *attached to a real, specific reason* the reader can act on? If yes → wanted. If it merely re-announces the chip or says the score "reflects" something → banned. The difference between "עוצר ב-B כי הבסיס מתוק" (wanted) and "ה-B משקף את ההרכב" (banned) is whether a reason is actually delivered.

</details>

**Relative position remains allowed** (adds info the chip can't show):
- ALLOWED: "מהבולטים בקטגוריה" / "מהחלשים במדף המעדנים" / "הרשימה הקצרה ביותר במדף"
- ALLOWED: comparison to a *named peer* with the reason ("רשימה קצרה מהשוקולד הלאומי של הגולן").

### 2b. INHERITED — wellness / moralizing / verdict words (already banned, restated for the at-speed writer)

From `insight_line_spec_v1` and `assertive_writing_v1` — do not use:
```
בריא / לא בריא / בריא יותר / בריא פחות
כדאי / מומלץ / לא מומלץ / כדאי להימנע
מטעה / מזויף / שקרי / תרמית / מסתיר / מניפולטיבי
גרוע / ירוד / מצוין / לא ראוי
איכותי / איכות נמוכה
"לכן" / "כי" / "משמע" followed by a conclusion the writer drew for the reader
```
Replace with the specific observable fact. The fact carries the line; the writer never delivers the verdict.

---

## 3. Length Gate (v2 — 2-line verdict)

**The verdict is two short sentences that fit ~2 lines on the row slot without truncation — roughly ≤170 Hebrew characters.** The old 35–80 char / ≤12 word gate is retired.

- **Target shape:** two sentences. Sentence 1 = standing + why; sentence 2 = catch + earned grade. (One dense sentence is allowed when the product is simple enough; three is too many.)
- **Soft target ~120–160 chars; hard ceiling ~170 chars** including spaces, excluding surrounding quotes used for label-claim citation. Above ~170 the verdict will wrap past two lines on a 280px mobile width and truncate.
- **No hard floor**, but a verdict under ~80 chars usually means a move is missing (no standing, or no reason behind the grade) — check it isn't just a v1 tag in disguise.

**Reference — the approved יופלה GO verdict is 158 characters and reads as 2 lines:**
> מהבולטים בקטגוריה — 10 גרם חלבון מהחלב ושלושה רכיבים בלבד, נדיר במדף של ממתיקים ומייצבים. עוצר ב-B כי הבסיס בנוי על חלב ואבקת חלב מועשרים, לא על מבנה חלב שלם.

**Checkable rule:** `len(verdict) ≤ ~170` and renders within 2 lines. A verdict that needs 3 lines is a fail — tighten the reasons, don't add a third clause.

---

## 4. Category-Native Voice

The same framework finding must be spoken in the vocabulary of *that shelf*. A buyer of bread weighs grain and fermentation; a buyer of yogurt weighs protein and sugar source; a buyer of a bar weighs protein quality. The driver is the same class of finding; the words are native to the category.

**Translation table** (framework finding → category-native line vocabulary):

| Framework finding | Bread / לחם | Dairy & spoon-desserts / מעדנים · יוגורט | Bars / חטיפים | Hummus / חומוס |
|---|---|---|---|---|
| Processing / additive load | "שמרים תעשייתיים ברשימה" · "משפר אפייה" | "מייצבים ברשימת הרכיבים" · "ממתיק מלאכותי" | "סירופ/דקסטרוז כרכיב מוקדם" | "חומר משמר" · "שמן במקום טחינה" |
| Primary-ingredient vs. name gap | "מחמצת בשם, שמרים תעשייתיים לפני" | "פרי בשם, ממתיקי טעם ברשימה" | "חלבון בשם, סוכר/סירופ לפניו" | "טחינה בשם, מים ושמן לפניה" |
| Strong macro | "X גרם סיבים ל-100 גרם" | "X גרם חלבון — מהחלב, לא מהתווית" | "X גרם חלבון, מקור [whey/סויה]" | "X גרם חלבון מהחומוס" |
| Defining sugar/sweetener | — (rare) | "הסוכר — הרכיב השני" · "ממתיק מלאכותי" | "סוכר/סירופ הרכיב הראשון" | — (rare) |
| Short / clean list | "3 רכיבים — קמח מלא, מים, מלח" | "3 רכיבים עיקריים בלבד" | "5 רכיבים, ללא ממתיקים" | "טחינה, חומוס, לימון — בלי תוספים" |
| Relative position | "הסיבים הגבוהים ביותר בקבוצה" | "ללא תוספים מזוניים — נדיר בקטגוריה" | "הציון הגבוה בין חטיפי החלבון" | "הרשימה הקצרה ביותר במדף" |

**Rule:** never carry one category's vocabulary into another (no "fermentation" language on a yogurt, no "protein quality" jargon on bread). When unsure which term is truthful for a category, that's a **Nutrition grounding-guide** question (§6), not a writer's guess.

---

## 5. Structure — the verdict shape, and varying it

### The default shape (vary it, don't template it)

`[standing] — [why: 1–2 real reasons]. [catch] — [earned grade] כי [reason].`

That is the *default*, not a mold. The §1 anti-template rule governs: the **order and the entry point change per product**. Valid variations seen in the pilot:

- **Catch-first** (category-worst): "52 גרם סוכר במנה — ... אבל רק שלושה רכיבים. נשאר ב-D כי ..."
- **Paradox-first** (icon): "הגביע המוכר במדף, ובכל זאת מהחלשים בו — ... יורד ל-D כי ..."
- **Name-gap-first** ("ללא פירות" / "דיאט" / "מעודנת"): "'לא מכיל פירות' בתווית — ... נשאר ב-D כי ..."
- **Standing-first** (clean leader): "מהבולטים בקטגוריה — ... עוצר ב-B כי ..."

### Two sentences, one of which lands the grade

Sentence 1 sets standing + why. Sentence 2 delivers the catch and the earned grade. Don't split into three; don't collapse the grade-reason into a bare chip echo. The complication is **named, never judged** (no מטעה / גרוע).

### Where the verdict STOPS

It stops on the **earned grade attached to its reason** — that *is* the conclusion the verdict is allowed to deliver (the §2a reversal). What it still may not do: moralize past the fact ("ולכן עדיף להימנע"), or draw a health conclusion. The grade-because-reason is the landing; nothing comes after it.

### The Publish Checklist (v2 — hard gate)

Run all eight on every verdict. Any **FAIL** blocks publication.

1. **Reads as an assessment** — standing + real reason(s) + catch + earned grade; sounds like a person who assessed it, not a caption? *(§1)*
2. **Differentiated** — fresh lead/shape for this product; not swappable with a neighbor unless genuinely identical? *(§1 anti-template)*
3. **Grade is earned, not echoed** — grade arrives attached to a real reason ("עוצר ב-B כי…"); no empty "הציון משקף / מבוסס על הציון"? *(§2a)*
4. **No banned wellness/verdict word** — clean against the §2b list? *(§2b)*
5. **Length** — ≤~170 chars, renders within 2 lines? *(§3)*
6. **Category-native voice** — this shelf's vocabulary, not another category's? *(§4)*
7. **Trace-anchored** — every number, ingredient, position, name-gap verifiable from *this product's* real data; respects the grounding limits (null sugar never cited, diet/light cup never "high protein", implausible sodium artifacts never cited)? *(§6, grounding_v1)*
8. **Stops at the earned grade** — no moralizing or health conclusion past it? *(§5)*

---

## 5b. Mandatory drivers — calorie density & sodium (added 2026-06-05, owner content review)

The owner's granola review exposed a systemic failure across the live pages: verdicts
that **name the grade with no real reason** ("עוצר ב-B כי גרנולה בכל זאת") and that
**ignore or misattribute the dimensions the engine actually scored** — above all
**calorie density**, the single biggest lever the copy was dropping (one granola was
hard-capped at 70 *by calories* while its verdict blamed sodium). This section is a hard
rule for **every** category, not just granola.

**Rule A — calorie density is a first-class citable driver.** kcal/100g is a scored
dimension (`calorie_density`, `lookup_calorie_density`) with hard caps (`SNACK_BAR_HIGH_CAL`,
`HIGH_CAL_*`). When calorie density is the binding cap or a material driver of the grade,
**the verdict must name it** ("…אבל 504 קק"ל ל-100 ג', מהצפופות במדף — הקלוריות מגבילות
אותה ל-B"). When a product is notably light for its shelf, that is equally citable as a
*strength*. Do **not** force calories where they are not the catch (a 362-kcal leader's
catch is processing, not calories) — §1 anti-template still governs.

**Rule B — the grade-reason must name a signal the trace actually fired.** Before writing
"עוצר ב-X כי …", confirm the reason is a dimension/penalty/cap the trace shows
(`dimension_scores`, `penalties_applied`, `caps_applied`). "Because it's granola/bread/a
bar anyway" is the banned empty restatement (§2a) — replace it with the real driver
(NOVA-3/4 processing → "מאפה מעובד, לא דגן בצורתו המלאה"; isolated protein → "חלבון מבודד,
לא מהדגן"; named penalties → glucose syrup / seed oil / long ingredient list).

**Rule C — sodium is cited as a FACT, never as a grade reason, *unless* the trace fires a
sodium signal.** As of 2026-06-05 the engine does not meaningfully penalise sodium in
several categories (e.g. granola: 700 mg trigger that real products never reach; frequent
null capture — see TASK-189). So a verdict **may** state a high sodium value as a displayed
fact and relative position ("394 מ"ג נתרן — גבוה למדף"), but **may not** place it inside a
"כי …" clause until a sodium penalty/cap actually fires for that product. Keep sodium in its
own sentence, after the grade-reason. When TASK-189 makes sodium a real driver for a
category, re-author that category's verdicts so the catch may cite sodium causally.

**Rollout:** the granola page (53 verdicts) is the reference implementation of this section
(`patch_granola_verdicts_v2.py`, 2026-06-05). All other live categories (bread, milk,
snacks, cheese, yogurt, hummus, maadanim, cereals) are to be re-audited against Rules A–C
and rebuilt to the same bar — each grounded in its own run's trace, not granola's.

---

## 5c. No UI-duplicate recitation + real limiting-factor driver (added 2026-07-08, owner ruling, TASK-533)

The 2026-07-08 owner review of the live yogurt pages rejected the copy wholesale on two grounds that generalize to every category, not just yogurt. Both are now hard rules.

**Rule A — a verdict never recites a number the row UI already displays.** The row shows a protein bar and a calorie/kcal chip next to the verdict text, not instead of it. A sentence like "10.5 גרם חלבון ל-100 גרם" sitting beside a protein bar that already reads 10.5 is not analysis — it is the UI captioning itself twice. A number earns a place in the verdict only when it is a **comparison**, a **verified rank/superlative** (checked against the full corpus for that shelf, not eyeballed), a **gap/contradiction**, or a **threshold finding that changes the reading of the product**. Test: delete the number — does the UI chip/bar still carry the exact same fact without it? If yes, cut the number or reframe it. This binds `insightLine`, `rowVerdict`, `consumerTakeaway`, and every `expansion.consumerExplanation` field — the rule follows the fact, not the field name.

**Rule B — a "limiting factor" names the real fired driver, never a category placeholder.** "רשימת הרכיבים ורמת העיבוד הם הגורם המגביל" fails on two axes at once: it is grammatically broken (a compound subject against the singular "הגורם"), and even if the grammar were fixed it says nothing — "the ingredient list" is a category-of-thing, not a finding. The catch must point at the actual dimension the trace fired lowest or the actual cap/penalty applied — a real compositional finding, in food language. **Correction (2026-07-08, §5d Principle A):** when the real limitation is a data-confidence gap rather than a compositional one, do **not** name the confidence/verification mechanism itself ("רמת העיבוד המדויקת לא מאומתת" is score-mechanism narration, not a food fact — see §5d). State the consumer-facing evidence boundary in food language instead: "בלי צילום תווית מלא לא נהפוך את זה להבטחה חזקה יותר." A product with a 3-ingredient, additive-free list does not get "the ingredient list" named as its own limiter; that is not what the data shows.

**These extend the existing rules, they don't replace them:** §6 Trace-Anchor Requirement already required every number to come from real data — Rule A adds that a *real* number can still be the wrong choice if it only duplicates what the UI already shows. §1 Rule B (mandatory drivers) already required naming a signal the trace actually fired — Rule B here closes the loophole where a category name ("ingredient list", "processing level") was used as if it were a signal.

**Publish Checklist additions (items 9–10):**
9. **No UI-duplicate numbers** — every number in the verdict is a comparison, verified rank, gap, or threshold finding, not a restatement of the protein bar / calorie chip / score chip? *(§5c Rule A)*
10. **Limiting factor is the real driver** — the catch names the specific dimension/cap/penalty/confidence-gap the trace actually shows, never a bare category label standing in for a finding? *(§5c Rule B)*

---

## 5d. Grade recitation ban + Principle A/B (C3 ruling, TASK-533 round 2, 2026-07-08)

The round-1 yogurt re-author fixed the §5c phrases but not the underlying pattern — Adversarial QA's independent challenge (GATE-2 Track C) failed it on voice for two reasons that generalize past yogurt. Full text lives in `editorial_intelligence_v3.md` §"Framework Invisibility" (Principle A / Principle B); this section is the verdict-copy-specific summary and is the authoritative pointer for §2a.

**Grade recitation is banned, full stop** — see §2a above (v3 reversal). The score chip renders the grade; the verdict text never does.

**Principle A — no score-mechanism narration.** A verdict may never explain *why the score is what it is* by describing Bari's own confidence classification, extraction method, or processing-level determination — even in plain Hebrew with zero Tier-4 vocabulary. "רמת העיבוד אינה מאומתת מהנתונים הזמינים" is the algorithm narrating itself just as much as "NOVA confidence: low" would be; only the vocabulary changed. The allowed move is the **evidence boundary in food language**: describe the product, then honestly bound the claim using ordinary shelf terms (a label photo, what the package states) — never the pipeline. This binds `insightLine`, `rowVerdict`, `consumerTakeaway`, `expansion.consumerExplanation.whyRated`, **and `bariInterpretation`** — any field that could be read as "why did this get its score."

**Principle B — cluster-honest, not fake-unique.** Zero byte-identical `consumerTakeaway` strings is the bar (RT-3), but the fix is never fabricated differentiation. Before varying a line, apply the test: *what verified fact about THIS product justifies writing it differently from its shelf neighbor?* Valid anchors: ingredients, added sugar/sweeteners, protein/calorie profile, fat level, milk source, lactose-free status, named additives, the product's own stated flavor, package/use-case, governed price. If no such fact exists, the products are a genuine cluster — write similar, honest cluster language for both; do not invent a nutritional distinction to force uniqueness.

**Publish Checklist additions (items 11–12):**
11. **No verbal grade** — zero instances of "נשאר/עוצר/יורד ב-[grade]" or any grade-restatement construction, in any of the four bound fields? *(§2a, §5d)*
12. **No score-mechanism narration** — the confidence/extraction/processing-classification mechanism is never named as a reason; any evidence limit is stated as a food-language boundary instead? *(§5d Principle A)*

---

## 6. Trace-Anchor Requirement

**Rule:** Every claim in a line must be verifiable from *that specific product's* real BSIP2 / canonical data — its ingredient list, its nutrition panel, its score record, or a category-level fact computed across the real set. **No invented numbers, ingredients, positions, or claims, ever.** If the data needed to make a line decision-first isn't present, the line falls back to the strongest *available* trace-anchored fact — it does **not** fabricate a stronger one.

Concretely, a line may cite:
- An ingredient or its **list position** only if it appears in that product's real `ingredients`.
- A **number** (protein, sugar, fiber, ingredient count) only if present in that product's real `nutrition` / panel. *(Note: where a panel value is `null` — e.g. several maadanim have `sugar: null` — the line may NOT assert that value. See יופלה GO: sugar is null, so its line correctly never cites a sugar number.)*
- A **claim/composition gap** only if both the name/front-of-pack claim and the contradicting ingredient are real.
- A **position** ("הגבוה ביותר", "נדיר בקטגוריה") only if it holds across the real displayed set.

**Dependency — Nutrition's per-category grounding guide.** This standard says *the line must be trace-anchored*; it does not by itself tell a writer *which signals each category may truthfully cite and in what words*. That is Nutrition's parallel deliverable. **The pilot needs, from Nutrition, the maadanim grounding guide specifying:**
- which nutrition fields are reliably populated vs. `null` for maadanim (so writers don't reach for an absent sugar value),
- the approved consumer wording for each citable signal (e.g. is "מייצבים" / "ממתיק מלאכותי" / "תוספים מזוניים" the truthful term for a given additive class),
- which "name-vs-composition" gaps are confirmed real (so a claim-gap line isn't asserted on a misread label).

Flagged below for the orchestrator.

---

## 7. Gold-Standard Examples — maadanim (pilot)

Six real verdicts from the rewritten set, chosen to show *differentiated leads and shapes* — no shared skeleton. Each is checklist-clean and trace-anchored.

**1. יופלה GO מועשר בחלבון** — 78/B · `protein 10.0` · `ingredients: חלב, חלבוני חלב (7.4%), אבקת חלב` · `sugar: null`
- **Shape:** standing-first (clean leader).
> מהבולטים בקטגוריה — 10 גרם חלבון מהחלב ושלושה רכיבים בלבד, נדיר במדף של ממתיקים ומייצבים. עוצר ב-B כי הבסיס בנוי על חלב ואבקת חלב מועשרים, לא על מבנה חלב שלם.
- *(Sugar `null` → never cited; and with no sweetener in the list and `sweetener_detected=false`, "sweet" cannot be the catch either. The grade is earned by a real, trace-fired signal: the reconstituted/enriched dairy base — NOVA 2, added חלבוני חלב + אבקת חלב — TASK-175.)*

**2. מילקי בטעם שוקולד** — 40/D · `protein 3.0` · five stabilizers · cream before sugar
- **Shape:** icon-paradox-first (the signature maadanim tension — icon ≠ architecture).
> הגביע המזוהה ביותר במדף, ובכל זאת מהחלשים בו — שמנת לפני הסוכר, חלבון של 3 גרם בלבד וחמישה מייצבים שבונים את המרקם. נשאר ב-D כי כמעט הכול כאן מבנה, לא חלב.

**3. דניאלה בטעם ענבים** — 49/D · label says "לא מכיל פירות" · flavor from חומרי טעם
- **Shape:** name-gap-first.
> "לא מכיל פירות" כתוב על האריזה עצמה — טעם הענבים כולו מחומרי טעם, על בסיס שמנת וסוכר עם ג'לטין ושני מייצבים. נשאר ב-D כי אין כאן מהפרי שבשם דבר.

**4. מעדן משמש** — 46/D · `sugar 52.0` · `ingredients: משמש (51%), ממיצי פירות מרוכזים, מיץ לימון`
- **Shape:** catch-first (the figure is the story; clean list can't rescue it).
> רשימה של שלושה רכיבים בלבד ו-51% משמש אמיתי — נדיר במדף — אבל 52 גרם סוכר ל-100 גרם, רובו ממיצי פירות מרוכזים. יורד ל-D כי זה ריכוז פרי מתוק מאוד, לא קינוח קל.

**5. מעדן חצילים** — 56/C · `protein 1.8` · `fat 11.5` · `sodium 394` · fried-eggplant savory spread
- **Shape:** odd-one-out-first (a savory product on a sweet shelf).
> חריג מלוח על מדף מתוק — חציל מטוגן 40% ורסק עגבניות במקום פרי וסוכר, אבל שמן סויה מופיע שלוש פעמים ו-394 מ"ג נתרן. עוצר ב-C כי התשתית בנויה על שמן ומלח.

**6. מעדן הגולן שוקולד** — 54/C · `sugar 14.5` · shorter list than its national peer
- **Shape:** named-peer-comparison-first.
> רשימה קצרה יותר מהשוקולד הלאומי של הגולן — חלב מפוסטר ראשון ופחות תוספים — אבל הסוכר עדיין הרכיב השני, 14.5 גרם. עוצר ב-C כי הקיצור אמיתי, אבל הבסיס נשאר מתוק.

Together these show **six different entry points** (standing, paradox, name-gap, figure, odd-one-out, peer-comparison) and a rhythm of peaks and plains — never one writer's template.

---

## 8. What this standard does NOT do

- It does **not** change any score or scoring code. It governs the `insightLine` / `rowVerdict` copy only.
- It does **not** replace `insight_line_spec_v1` (line types, tone, rhythm) — it sits on top as the enforced publish gate, now in the verdict model.
- It does **not** decide scores or what a score means — Content writes the verdict; Nutrition grounds the claim and verifies the reasoning is true; Product approves positioning.

---

*Row Description Standard v2 (Interpretive Verdict model). Supersedes v1's terse-tag model. Extends insight_line_spec_v1 (base), assertive_writing_v1 (floor). Pairs with row_description_grounding_v1 (Nutrition). RETURNED for Nutrition + QA + orchestrator review — do not mark CLOSED.*
