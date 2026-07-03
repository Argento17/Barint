# 7 — Voice-Match Gate (Tom / Bari Hebrew)

The pass/fail gate every draft clears before handoff. It sits **after** the
mechanical gates (leakage, claim, tone, nakdan in `5_…`) and answers one question:
**does this actually sound like Tom?**

Run it as a checklist; a draft passes only when every applicable item is "yes."

---

## Step 0 — Mode detection (do this first)
Identify the product's real profile from its data, then declare the mode. Writing
in the wrong mode is the most common failure.

- Long ingredient list + additives + high sugar/sat-fat, or "dessert in disguise" → **Critical**
- Short/clean list but low fiber/protein, mostly light carb → **Balanced**
- Simple list + real fiber/protein + low sugar, strong for the shelf → **Positive**

If you can't tell the mode from the data, you don't have enough data to write —
flag the gap, don't guess.

---

## Step 1 — The arc (structure)
1. ☐ Opens from a **real consumer situation** or a familiar product perception (not "המוצר מכיל…").
2. ☐ **Pivots** quickly from perception to evidence.
3. ☐ Cites **product-specific facts** (ingredient-list length, sugar/fat/fiber/protein, additives), numbers where available.
4. ☐ Ends with **הקשר במדף** — the shelf-context closing beat (Harvest #2, ruling #2). "שורת בארי" as a label is retired from the spine. The closing beat places the product in shelf context: standing, what it beats, what it doesn't. Not a verdict.

## Step 2 — The stance (voice values)
5. ☐ Does **not** moralize or shame the consumer.
6. ☐ Does **not** tell people what to eat (no מומלץ/להימנע without for-whom-and-why).
7. ☐ No unsupported health scare; any health-effect claim is flagged for Nutrition (file 5).
8. ☐ Distinguishes **"bad product" from "limited product"** — Balanced ≠ Critical.
9. ☐ Does **not** pretend every processed product is equally problematic, and gives a genuinely strong product real, bounded praise.
10. ☐ Treats additives/claims as part of the **whole picture**, never as a single-villain verdict.
11. ☐ **Residual-antithesis scan (all forms) = 0** except logged, carve-out-justified keeps — run all four patterns from `5_banned_phrases_and_claims.md` §1.5 (comma/dash לא-ולא, the **bare non-comma `ולא`**, standalone `אלא`, English "X, not Y"). A scan that checks only the comma form is not a completed check — this exact gap has recurred 4×+ (TASK-477 RT-M1, TASK-484, TASK-461, TASK-490).

## Step 3 — The texture (does it read like Tom)
12. ☐ Simple, conversational, second-person Hebrew. Short sentences; fragments allowed for punch.
13. ☐ Sounds like a sharp friend at the shelf — **not a dietitian brochure**.
14. ☐ Uses at least one signature move (situation opener, "X לא תמיד אומר Y", image-vs-structure, the "אז זהו" pivot) — without mechanically over-using one.
15. ☐ Em-dash used as a **pivot at most once per paragraph** (the §7 tension in `2_voice_fingerprint.md`); never stacked, never a list-connector.

---

## HARD FAILURES (production)

These are binary blocks. A single hard failure = the draft does not move forward.
No exceptions, no "mostly passes." Each item states the exact, checkable criterion.

---

### HF-1 — Repeated signature-phrase overuse

**Criterion:** The same Tom signature move appears in more than 2 out of every 5
consecutive reviews on the same shelf.

Signature moves subject to this rule (from `2_voice_fingerprint.md` §3):
- The "אז זהו — שלא תמיד" pivot (or close variants: "אז זהו.", "שלא תמיד.")
- The "X לא תמיד אומר Y" construction
- The image-vs-structure beat ("המראה ביתי. המבנה פחות." / "השם מוכר. המבנה פחות.")
- The "קינוח בתחפושת" naming-the-disguise beat
- The "הבעיה היא לא רכיב אחד. הבעיה היא התמונה הכוללת." framing

**How to count:** Lay the N reviews for a shelf side-by-side. For each signature
move, count how many of the 5-review sliding windows contain it more than twice.
If any window has the same move in positions 1, 2, and 3 out of 5 (or positions
2, 3, and 4, etc.) → FAIL. For a shelf with fewer than 5 reviews, threshold is
>1 occurrence of the same move across the full set.

**Failure signal:** "שורת בארי: המראה ביתי. המבנה פחות." appears in A2, A3,
and A4 of a 5-review set → FAIL. The phrase has become mechanical filler, not a
meaningful move.

**Fix signal:** Each signature move appears at most twice in any 5 reviews, and
the two appearances are in clearly different structural positions (opener vs.
closer, or Critical vs. Positive mode).

---

### HF-2 — Wrong mode

**Criterion:** The mode declared (or implied by tone) does not match the
product's data profile. Two detectable failure directions:

**Direction A — Critical mode applied to a clean product.**
Signal: The review contains any of the following when the product's ingredient
list is ≤8 items AND contains no coded additives (E-numbers) AND sugar ≤10g/100g:
  - "רשימת רכיבים ארוכה" — when it is not long
  - "תוספי מזון רבים" — when none are present
  - "מוצר מדף מתועש" — when the profile does not support this
  - Any use of the "הבעיה היא לא רכיב אחד" framing

Detection: read the claimed product facts in the review against the data fields.
If the review's framing implies degraded quality that the data does not support →
FAIL on Direction A.

**Direction B — Positive-mode product receives Balanced/Critical hedging.**
Signal: A product with ≥5g fiber/100g AND ≤8g sugar/100g AND ≥5g protein/100g
AND ≤8 ingredients receives a review that:
  - Uses "לא תמיד אומר" or "אבל" as its ONLY evaluative move (hedge without
    any positive claim)
  - Never states what the product does well in a concrete, product-specific term
  - Ends with a Balanced-mode הקשר במדף closer ("מוצר סביר הוא לא תמיד מוצר חזק")
    instead of naming the genuine strength

Detection: if the product data profile meets the "Positive" criteria (see Step 0)
but the שורת בארי closer is hedging language only, with no named concrete strength
→ FAIL on Direction B.

**Why this is a hard fail:** The voice's credibility depends on not crying wolf
(Critical for everything) and not hiding from a genuine finding (hedging a strong
product). Both directions erode trust in the shelf-level comparison.

---

### HF-3 — Generic review (the swap test)

**Criterion:** A review fails if the identical text could be transplanted onto
≥3 other products on the same shelf without changing any specific fact.

**The swap test — run it explicitly:**
1. Remove the product name from the review.
2. List the product-specific facts cited: actual ingredient count, actual named
   additives present on the label, actual g/100g values (sugar/fat/fiber/protein).
3. If the review contains zero product-specific facts (only category-level
   generalizations like "מוצר מדף עם רשימת רכיבים ארוכה" without a count), or
   if every stated fact applies equally to the majority of products on this shelf
   → FAIL.

**Failing signal:** "בחלק מהמוצרים שבדקנו מצאנו הרבה סוכר, רשימת רכיבים ארוכה,
ותוספי מזון" — this could be copy-pasted onto any critical product on any processed
shelf. No specific fact distinguishes this product from its neighbors.

**Passing signal:** "רשימת 14 רכיבים, ביניהם 3 מייצבים ומחמאה כרכיב השני" — this
fact set is specific enough that it would be wrong if applied to a different product
with a short list and no additives.

**Threshold:** At minimum 2 product-specific facts (either values or named
ingredients/additives present in the scrape) must appear in a review for it to
pass the swap test. Fewer than 2 specific facts = FAIL.

---

### HF-4 — Unverified fact

**Criterion:** Any product-specific factual claim that is NOT present in the
product's scraped data AND is NOT flagged with "דורש אימות לפני פרסום" (in draft
mode) = FAIL.

"Product-specific factual claim" means any statement that could be true of this
product and false of another: a specific ingredient name, a quantity per 100g, a
processing method attributed to this product, a label claim ("ללא גלוטן",
"עשיר בסיבים"), an additive code or count.

**Detection procedure:**
1. For each factual sentence in the review, identify the data field it draws from
   (sugar_per_100g, ingredient_list, label_claims, etc.).
2. Look up that field in the product's scrape record.
3. If the field is absent or the stated value does not match → the claim must
   carry a "דורש אימות" flag. If it does not → FAIL.

**Scope:** This hard fail applies even when the fact "sounds right" for the
category. The category's typical behavior is not a substitute for the product's
own data.

**Note:** This rule sequences with and extends the claim-control firewall in
`5_banned_phrases_and_claims.md` §2. That file governs Tier-B health-effect
claims. HF-4 extends coverage to all product-specific factual claims regardless
of tier.

---

### HF-7 — Brand-directed rhetoric, information-dumping, or nutrition-tail (Harvest #3 — ALL modes)

**Criterion:** Any consumer-facing text (insightLine, rowVerdict, comparisonContext, intro sentences) that contains any of the following = FAIL:

1. **Brand-directed dismissive rhetoric:** any pattern matching `"<brand-name>? תחשוב שוב"`, `"תחשבו שוב"`, or any sentence that attacks a brand's character by name. Detecting criterion: the brand/product name appears in the same sentence as a rhetorical dismissal. Applies to ALL shelf products regardless of how weak the score is.
2. **Information-dumping:** a bare juxtaposition of two facts without an interpretive connector that names the finding or the "so what." Example fail: `"הוויטמינים הוספו; הסיבים — לא"` — this is a data dump, not a verdict. Example pass: `"הוויטמינים הגיעו מתוספת חיצונית — הדגן שיספק סיבים לא נמצא כאן"` (names the structural absence as the finding).
3. **Nutrition-tail:** a `rowVerdict` or `insightLine` that ends with a standalone raw number in the format `"נתרן: X מיליגרם ל-100 גרם"` or `"סוכר: Y גרם ל-100 גרם"` — whether alone or as a comma-list. These numbers belong in the nutrition section, not the verdict. A number is allowed in a verdict only when it IS the finding (e.g., "435 מיליגרם נתרן — הגבוה ביותר בקטגוריה"), never as a trailing raw-data appendage.

**Detection:**
```
# Brand rhetoric
grep -E "(תחשוב שוב|תחשבו שוב)" <draft_file>
# Nutrition tail
grep -E "נתרן: [0-9]|סוכר: [0-9]" <rowVerdict_field>
```
Any match = FAIL.

**Fix signal:** Remove the trailing data tail entirely from the verdict; reframe any bare fact-pair as a named finding; replace brand-rhetoric with a product-composition statement.

---

### HF-8 — Internal product-ID tokens in consumer copy (Harvest #4, H4-1 — ALL modes)

**Criterion:** Any consumer-facing text (`insightLine`, `rowVerdict`, `comparisonContext`, intro/prologue sentences) that contains any internal product-ID token = FAIL. Banned token classes:
- Shelf-prefix IDs: `jc-NNN`, `snk-NNN`, `hc-NNN` (any `*-NNN` internal slug)
- Raw barcodes (8–13 digit numeric strings used as identifiers)
- Engine/scoring identifiers: `bsip1_*`, `bsip2_*`, corpus/run tokens (`run_005_headpin`, etc.)
- Any camelCase/snake_case product key from the JSON (`product_id`, `barcode` field value pasted as reference)

Siblings and shelf neighbors must be referenced by **Hebrew product name or a plain descriptor** — never by internal ID.

**Detection:**
```
grep -E "(jc-[0-9]+|snk-[0-9]+|hc-[0-9]+|bsip1_|bsip2_|[0-9]{8,13})" <consumer_copy_fields>
```
Any match in consumer-facing sections (not in the internal "מקורות" block) = FAIL.

**Failing signal:**
> "כמו snk-001 — סוכר גבוה ורשימת רכיבים ארוכה."
> "השוואה ל-jc-042 בקטגוריה."

**Corrected signal:**
> "כמו בר דגנים בדבש של המותג המוכר — סוכר גבוה ורשימת רכיבים ארוכה."
> "השוואה לבר הדגנים הטבעי בקטגוריה."

**Why this is a hard fail:** A shopper reading `snk-001` on a comparison page is looking at pipeline plumbing, not product language. Internal IDs are for the engine and the editorial workflow — they never belong in copy that names a neighbor product.

---

### HF-6 — Code-token leakage in consumer output (Harvest #2, ruling #1 — ALL modes)

**Criterion:** Any consumer-facing text (insight line, bullet, body paragraph, closing beat, headline) that contains any of the following = FAIL:
- The literal string `null` (the JSON null value rendered as text)
- Any field-path identifier: `d4_additives`, `expansion.nutrition`, `expansion.ingredients`, `expansion.X`, `_wholeGrainClaim`, `_isChildrens`, `insightLine`, `rowVerdict`, `confidence_level`, or any other camelCase/snake_case JSON field name
- Any backtick-wrapped token (e.g., `` `expansion.nutrition` ``)
- Any E-field reference embedded in consumer copy as a field identifier (e.g., "(d4_additives ריק)", "מקור: expansion.X")

**Detection:**
```
grep -E "(null|d4_|expansion\.|_whole|_isChild|insightLine|rowVerdict|`)" <draft_file>
```
Any match in consumer-facing sections (not in the internal "מקורות" block) = FAIL.

**Correct handling when data is absent:**
- Missing quantity: "לא צוין על האריזה" or "לא ידוע מהאריזה"
- Null ingredient list: "רשימת הרכיבים המלאה לא נקראה מהאריזה" — honest, not alarming
- Never: "כמות מדויקת null", "ללא תוספי מזון (d4_additives ריק)"

**Why this is a hard fail:** A shopper reading "d4_additives ריק" on a comparison page is looking at a broken internal artifact, not a Bari page. Code tokens in consumer copy are a first-order credibility failure. They also indicate the agent is reading from raw engine output rather than interpreting it into consumer language — the core job.

---

### HF-5 — User-facing clutter ("דורש אימות" in publication mode)

**Criterion:** Any review exported in PUBLICATION mode that contains the string
"דורש אימות" (or close variants: "לפני פרסום", "מקור: product scrape") in the
consumer-visible body text = FAIL.

**Two-mode distinction:**

**DRAFT mode** (working state, internal review, handoff to Tom-edit loop):
- "דורש אימות לפני פרסום: <exact fact>, מקור: <field>" MUST appear inline,
  after every unverified Tier-A fact and every Tier-B claim.
- The flag is visible to the reviewer. This is correct behavior in draft mode.
- Draft-mode reviews are NOT publication-ready and MUST NOT be copied into the
  frontend JSON.

**PUBLICATION mode** (output destined for frontend JSON, consumer page):
- Zero "דורש אימות" strings in the body text.
- All previously flagged facts must have been either: (a) verified against the
  product scrape and the flag removed, OR (b) removed from the copy entirely
  because the data was unavailable.
- Any remaining verification metadata moves to an INTERNAL review note field
  (outside the consumer-facing copy), never to the insightLine / rowVerdict /
  explanation fields consumed by the frontend.

**Detection:** `grep -c "דורש אימות" <review_file>` in publication output must
return 0. Any nonzero count = FAIL.

**Why this is a hard fail:** A consumer seeing "דורש אימות לפני פרסום" on a
product page is a credibility collapse. It also constitutes leakage of internal
process into consumer copy, which is a first-order failure of the Bari voice.

---

## Pass/Fail Rubric (compact, scannable)

| Status | Condition |
|---|---|
| **PASS** | All 15 checklist items "yes" AND all 8 hard-fail criteria clear (zero triggers) |
| **FAIL — HF-1** | Same signature move in >2/5 consecutive reviews on the shelf |
| **FAIL — HF-2A** | Critical framing applied to a product with ≤8 ingredients, no E-numbers, ≤10g sugar/100g |
| **FAIL — HF-2B** | Positive-threshold product (≥5g fiber, ≤8g sugar, ≥5g protein, ≤8 ingredients) reviewed with hedge-only language and no named concrete strength |
| **FAIL — HF-3** | Fewer than 2 product-specific facts; swap test passes for ≥3 shelf neighbors |
| **FAIL — HF-4** | Product-specific factual claim not in scrape data AND not flagged "דורש אימות" |
| **FAIL — HF-5** | "דורש אימות" appears in publication-mode output |
| **FAIL — HF-6** | Any `null`, field-path token (d4_additives, expansion.X, etc.), backtick, or JSON identifier in consumer-facing output |
| **FAIL — HF-7** | Brand-directed dismissive rhetoric, bare fact-dump without finding, or nutrition-tail in verdict |
| **FAIL — HF-8** | Internal product-ID token (jc-/snk-/hc-NNN, raw barcode, bsip1_*) in consumer-facing copy |
| **FAIL — Step 1–3** | Any checklist item "no" |
| **CONDITIONAL** | Borderline voice ("sounds off, can't name it") → route to C3 fresh-eyes read before deciding; C3 names failing lines, never rewrites |

---

## Worked Example — FAILING review and CORRECTED version

**Category:** Cereals. **Product (dummy):** דגני כוסמין עם דבש — an 8-ingredient
cereal, first ingredient whole wheat, sugar 14g/100g, fiber 6g/100g, protein 5g/100g,
no coded additives, one label claim "דגן מלא".

### FAILING version

> בוקר. ילד צריך לצאת, אתם צריכים קפה. דגני בוקר הם הפתרון הכי קל.
>
> אבל המדף הזה מבלבל. חלק מהמוצרים פשוטים יחסית. אחרים נראים כמו ארוחת בוקר,
> אבל מבחינת סוכר, סיבים ורשימת רכיבים — קרובים יותר לקינוח יבש בקופסה.
>
> דגני כוסמין עם דבש נופלים לקטגוריה הזו. המוצר נראה טבעי ופשוט, אבל בפועל מדובר
> במוצר מדף עם רשימת רכיבים ארוכה ותוספי מזון רבים.
>
> **שורת בארי:** אז זהו — שלא תמיד.
>
> **דורש אימות לפני פרסום:** רשימת הרכיבים, כמות הסוכר, נוכחות תוספי מזון. מקור: product scrape.

**Hard fails triggered:**
- **HF-2A (Wrong mode — Critical applied to clean product):** The product has 8
  ingredients, no E-numbers, and 14g sugar/100g. The review states "רשימת רכיבים
  ארוכה ותוספי מזון רבים" — neither is true for this product's data profile. The
  mode is Critical when the profile is Balanced.
- **HF-3 (Generic review):** Paragraphs 1 and 2 are lifted almost verbatim from
  Intro 4 (B.3) and could apply to any cereal on the shelf. The only
  product-specific sentence is the one with the false factual claims. No
  product-specific facts (actual counts, actual values) are cited. Fewer than 2
  specific facts present.
- **HF-5 (User-facing clutter):** "דורש אימות לפני פרסום" appears in the body.
  If this were exported as publication copy, it would reach consumers.

---

### CORRECTED version

> בוקר. ילד צריך לצאת, אתם צריכים קפה, וכולם צריכים משהו אמיתי לאכול.
>
> דגני כוסמין עם דבש עושים עבודה סבירה כאן. כוסמין מלא ראשון ברשימה, שמונה רכיבים
> בסך הכל, ושישה גרם סיבים ל-100 גרם — זה יתרון אמיתי יחסית למדף. הדבש מוסיף 14
> גרם סוכר ל-100 גרם, שזה לא נמוך. אבל זה גם לא מה שהופך מוצר ל"קינוח בקופסה".
>
> זה מוצר נקי שמוגבל קצת על-ידי המתיקות שלו. לא מורכב, לא בעייתי — פשוט לא הכי חזק
> שיש כשאתם מחפשים בסיס בוקר עם סוכר נמוך.
>
> **הקשר במדף:** כוסמין מלא עם סיבים טובים — תוספת הדבש מגבילה אותו קצת, אבל בתוך המדף הזה הוא בצד הנקי.

**How the corrected version clears each hard fail:**
- **HF-2A cleared:** Mode is now Balanced (short list, real fiber, moderate sugar) —
  consistent with the data. No Critical framing.
- **HF-3 cleared:** Two product-specific facts cited: 8 ingredients (specific count),
  6g fiber/100g (specific value), 14g sugar/100g (specific value). The swap test
  fails — these values would be wrong for a different product. Passes with 3 specific
  facts present.
- **HF-5 cleared:** No "דורש אימות" in the body. Facts are drawn from the scrape
  data. Any remaining unverified field would be removed before export, not flagged
  inline.
- **HF-4 cleared:** Every stated fact (ingredient count, fiber g/100g, sugar g/100g)
  is present in the product's scrape record.

---

## Integration point in the Content Agent workflow

Relative to the existing gate sequence in `5_banned_phrases_and_claims.md` §3:

```
1. Claim scan (Tier-A/B)
2. Leakage — hebrew_readability.is_clean
3. Tone — HebEMO anger+disgust
4. Form — DICTA Nakdan
5. Grammar/agreement — hebrew_grammar_gate.analyze(text).is_clean
   (high-confidence flags: auto_fix via hebrew_grammar_autofix; medium: human review)
6. [THIS FILE] Voice-match gate (checklist Steps 1–3)
   + HARD FAILURES (HF-1 through HF-8) ← run before handoff to Tom-edit loop
7. Tom-edit loop (file 8 logging)
```

**Where exactly to insert the hard-failure check:**

Run HF-1 through HF-8 at the end of Step 5 (this file), BEFORE the draft enters
the Tom-edit loop. Rationale: the Tom-edit loop is expensive (human time); the
hard-fail checks are mechanical and catch structurally broken drafts that do not
deserve a human review cycle. A draft that fails HF-3 (generic) or HF-4
(unverified fact) is not ready for editorial judgment — it is ready for a revision
cycle.

**Shelf-level HF-1 check timing:** HF-1 (phrase overuse) cannot be checked on a
single review — it requires the full shelf set. Run it once when the complete set
for a shelf is assembled, before any individual review is handed to the Tom-edit
loop. If HF-1 fires on the set, revise the flagged reviews before moving the set
forward.

**Publication-mode HF-5 check timing:** Run a final `grep -c "דורש אימות"`
pass at the point of export to frontend JSON (the data handoff to the frontend
pipeline), not earlier. The flag is correct and required during all earlier stages.

---

## Scoring
- **All applicable items "yes" + all 8 hard-fail criteria clear** → passes voice gate → handoff.
- **Any checklist "no"** → not done; revise. Note which item failed in the return block.
- **Any hard-fail triggered** → FAIL; revise before re-check. Note the specific HF number and the exact criterion that fired.
- **Borderline "sounds off but I can't say why"** → route to an independent fresh-eyes read (C3 / ChatGPT lane, manual paste) with the prompt: *"Does this sound like the Tom-Bari voice in `2_voice_fingerprint.md`, or like generic AI copy? Name the lines that break voice."* C3 reviews, never rewrites (cf. `c3_lane_chatgpt`).

## Relationship to the mechanical gates
This gate does **not** replace the file-5 firewalls. Order of operations:
1. Claim scan (Tier-A/B) → 2. Leakage (`hebrew_readability.is_clean`) →
3. Tone (HebEMO) → 4. Form (DICTA Nakdan) → 5. Grammar/agreement (`hebrew_grammar_gate.analyze(text).is_clean`) →
**6. This voice-match gate (Steps 1–3 + HF-1 through HF-8).**
A draft must pass all six.

Gate 5 — grammar/agreement — runs after the DICTA Nakdan form check (gate 4) and before
this voice-match gate. It catches noun-adjective and subject-verb gender/number mismatches.
High-confidence flags (`confidence="high"`) may be auto-fixed via
`hebrew_grammar_autofix.auto_fix(text)` before re-gating; medium-confidence flags must be
resolved by human review. A failed grammar gate is not-done; it does not reach this file.

HF-4 (unverified fact) sequences with and extends the §2 firewall in file 5.
They do not duplicate: file 5 §2 governs the Tier-B escalation path; HF-4 closes
the gap for Tier-A facts that are simply absent from the scrape. Both checks run.

## Logging
When a draft fails this gate and Tom (or a reviewer) supplies the fix, record the
before/after in `8_edit_feedback_log.md`. Repeated failures of the same hard-fail
item are a signal to sharpen the fingerprint or the scrape coverage, not just the
draft.

Hard-fail patterns to watch over time:
- Repeated HF-3 failures → scrape coverage is thin; reviews are forced to generalize.
- Repeated HF-2A failures → Content Agent is defaulting to Critical mode regardless of profile.
- Repeated HF-1 failures → signature-move inventory is too narrow; add moves from new Tom edits (file 8).
