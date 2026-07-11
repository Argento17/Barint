# Magnesium Guide — Slot Copy v1 (TASK-504, Content Agent, gate 1 of 2)

**Status:** DRAFT — gate 1 (Content Agent) only. Goes to Adversarial QA / Red-Team for gate 2 before
this may replace any `// TODO CONTENT (two-gate)` placeholder in
`C:\bari_wt_t504\bari-web\src\lib\guides\magnesium-guide-data.ts`. This document does not edit that
file and does not close TASK-504.

**Grounded in:**
- `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` — `bucket_logic` (bucket definitions,
  evaluation order) and `display_suppression_rule` (the two-reason disclosure requirement).
- `03_operations/reports/product/magnesium_guide_bar_revision_call_v1.md` — calls A (price_fairness:
  data-acquisition gap, fast-follow), B (third_party_verification: market fact, no claims exist), D
  (bucket-header comprehension defect, directional draft only).
- `C:\bari_wt_t504\bari-web\src\lib\guides\magnesium-guide-data.ts` — live gate-1-approved
  `educationSpine`, `headlineFinding`, existing bucket/bar Hebrew labels, and the existing (unfinalized)
  `heroImage.alt` draft, for voice/register match.

---

## Slot 1 — Four bucket sub-captions

VM field: `bucketSubCaptions.{key}` (keys per the live data file: `clears_all`, `passes_with_flag`,
`fails`, `cannot_assess`).

### 1a. `bucketSubCaptions.clears_all`

```
מוצרים שעומדים בכל שישה הספים במלואם, בלי אף דגל ובלי שום כישלון.
```

**Provenance:** rubric `bucket_logic.buckets[clears_all_bars].definition` — "all 6 bars = PASS. Zero
FLAG, zero FAIL, zero CANNOT-VERIFY." This bucket is empty for magnesium (0/18, per
`magnesium_guide_bar_revision_call_v1.md` premise check and the guide's own `headlineFinding.title`),
so this sub-caption will not render for the current build — authored anyway per the task's instruction,
for the day a magnesium product clears all six, or for reuse on a future guide (e.g. creatine) where
the bucket is non-empty.

### 1b. `bucketSubCaptions.passes_with_flag`

**REVISED post-gate-2 (RT-1):** count dropped. The bucket re-flows on every rescore, so a hardcoded
number goes stale; Frontend binds the live bucket length separately. Final no-count string:

```
מוצרים שאף סף לא נכשל אצלם, כשלכל אחד לפחות דגל אחד לתשומת לב.
```

(Superseded gate-1 draft, for record: "חמישה מוצרים שאף סף לא נכשל אצלם, כשלכל אחד לפחות דגל אחד לתשומת לב.")

**Provenance:** rubric `bucket_logic.buckets[passes_with_flag].definition` — "no bar = FAIL, AND at
least one bar is FLAG or CANNOT-VERIFY." Refines Product's directional draft ("5 מוצרים בלי כישלון
בשום סף, כל אחד עם דגל אחד לפחות") into a standalone sub-caption line that states the inclusion rule
without implying an endorsement — this is the list the owner found confusing, so the rule ("no
failure," "at least one flag") is stated plainly. The count is now supplied at render time by the live
bucket length, not baked into the copy (gate-2 RT-1: re-flow-safety).

### 1c. `bucketSubCaptions.fails`

```
מוצרים שנכשלים בלפחות אחד משישה ספי הקנייה.
```

**Provenance:** rubric `bucket_logic.buckets[fails].definition` — "at least one bar = FAIL (any of the
6 — Safety FAIL is one instance of this, not a separate rule)."

### 1d. `bucketSubCaptions.cannot_assess`

```
אצל המוצרים האלה אי אפשר לקבוע כמה מגנזיום יסודי מגיע בפועל, ולכן אי אפשר להעריך אף אחד מהספים האחרים.
```

**Provenance:** rubric `bucket_logic.buckets[cannot_assess].definition` — "no bar = FAIL, AND
dose_adequacy = CANNOT-VERIFY (the foundational bar — if the actual delivered amount of the active
ingredient cannot be established at all, no other bar's state is meaningful as a buying signal)."
Matches the live data file's single `CANNOT` product (TRIOMAG, product 18) and its own `oneLinerHe`
framing ("כאן גם הצורה עצמה אינה ידועה... אין אפילו ממצא שלילי מוגדר... רק חוסר מידע מוחלט").

---

## Slot 2 — Suppressed-bars disclosure line

VM field: `suppressedBarsDisclosureHe`

**REVISED post-gate-2 (RT-2):** the dated promise "(זה יתעדכן בעדכון הבא)" over-promised a next-build
delivery; Product call A only characterizes Israeli pricing as a tracked fast-follow. Softened to
open-timing "כשהנתונים ייאספו". Final string:

```
שני דברים לא מוצגים כרגע בטבלה, אצל כל 18 המוצרים: הוגנות המחיר, כי עדיין לא נאספו נתוני מחיר למוצרי מגנזיום ונוסיף אותה כשהנתונים ייאספו, ובדיקת צד שלישי, כי אף מותג מגנזיום במדף לא פרסם טענת בדיקה כזו כלל.
```

(Superseded gate-1 draft, for record: "...כי עדיין לא נאספו נתוני מחיר למוצרי מגנזיום (זה יתעדכן בעדכון הבא), ובדיקת צד שלישי...")

**Provenance:** rubric `display_suppression_rule.what_still_happens_when_suppressed` — requires one
guide-level line naming which bars were suppressed, the count, and the two DISTINCT reasons: (1)
price_fairness — "not yet collected," a Bari data-acquisition gap, per Product's call A
(`magnesium_guide_bar_revision_call_v1.md` §A: "Israeli magnesium pricing collection is NOT in scope
for Wave 1... becomes a tracked fast-follow task"); (2) third_party_verification — "no claims exist in
this market to check," a corpus/market fact, per Product's call B (§B: "no product in the 18-product
corpus makes a certification claim at all... this is a market fact, not a Bari collection gap") and
the live `educationSpine` "בדיקת צד שלישי" section's own existing wording ("הסיבה לכך היא שאף מותג
מגנזיום במדף לא פרסם טענה כזו כלל"), reused here for consistency rather than re-invented. The 18-count
comes from `magnesium_guide_bar_revision_call_v1.md`'s premise check (thirdPartyVerification and
priceFairness both `cannot_verify` 18/18, parsed from `magnesium-guide-data.ts`).

---

## Slot 3 — Hero mascot alt text

VM field: `heroImage.alt` (image: `mascot-mg-magnesium-guide.webp`)

```
לומו, דמות בארי, בוחן דרך זכוכית מגדלת צורות שונות של תוסף מגנזיום, כשמסביבו בקבוקוני תוספים ומאכלים עתירי מגנזיום.
```

**Provenance:** finalizes the placeholder already present at
`magnesium-guide-data.ts` line 430 ("לומו, דמות בארי, בודק בקבוקוני תוסף מגנזיום ומאכלים עתירי מגנזיום
דרך זכוכית מגדלת"). Revised to lead with the actual depicted action per the task brief — Lumo examining
different magnesium supplement forms with a magnifying glass, with supplement bottles and
magnesium-rich foods as the surrounding scene — rather than leading with the bottles. Purely
descriptive of the visual asset; no health or product-efficacy claim (does not say the forms are
"better," "recommended," or "effective" — that judgment lives in the bar/bucket copy, not the alt
text).

---

## Voice self-check (owner hard rules)

**Define-by-negation antithesis scan** — searched all four slot strings above for the literal banned
constructions:
- `,לא` (comma directly followed by לא): **0 occurrences**.
- `אלא` (the "but rather" contrast word): **0 occurrences**.
- `ולא` (the "and-not" contrast word): **0 occurrences**.

Note: three plain factual negations appear in Slot 2 ("לא מוצגים," "לא נאספו," "לא פרסם") and one
in Slot 1d/1c-adjacent phrasing ("אי אפשר לקבוע... אי אפשר להעריך," "לא נכשל"). These state an
absence of fact (data not collected, no claim published, no failure present) — they are not
"X, not Y" identity-defining antithesis (e.g. "זה לא מדריך שמדרג, אלא מדריך שמסביר"). Slot 2's entire
content is inherently about two things not being shown, so stating that plainly is unavoidable and is
not the banned rhetorical pattern; flagging this distinction explicitly rather than silently asserting
compliance.

**Em-dash scan:** zero em-dashes (—) used in any of the four final strings. (Provenance notes above use
em-dashes for my own internal citation style only — not shipped copy.)

**Banned engine-jargon scan** (דירוג / מדורג / מקום N / ניקוד / ציון / סף-as-a-score / NOVA / BSIP /
cap / floor): **0 occurrences** in any of the four final strings. "סף" / "ספים" ("threshold(s)") is
used as a buying-bar concept consistent with the already-approved `educationSpine` and bucket
Hebrew labels (e.g. "עובר את כל ספי הקנייה") — not a score/rank term.

**Brand name check:** no instance of any non-בארי brand spelling used for Bari itself.

**Register match:** all four slots use the same short-sentence, plain-Hebrew, fact-first register as
the live `educationSpine`/`headlineFinding` copy (e.g. reusing "אף מותג מגנזיום במדף לא פרסם טענה כזו
כלל" verbatim from the approved "בדיקת צד שלישי" section rather than paraphrasing it differently).

---

```json
{
  "task": "TASK-504-magnesium-guide-slot-copy",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/reports/content/magnesium_guide_slot_copy_v1.md", "action": "created", "sha256": "PENDING — compute at commit time via Get-FileHash; not committed by this agent (draft-only, no commit per task instruction)"}
  ],
  "counts": {
    "copy_slots_authored": "4/4 (bucketSubCaptions.clears_all, bucketSubCaptions.passes_with_flag, bucketSubCaptions.fails, bucketSubCaptions.cannot_assess) plus 2 additional required slots (suppressedBarsDisclosureHe, heroImage.alt) = 6/6 total slots in this task's ask",
    "antithesis_construction_hits": "0/6 strings scanned (literal ',לא' / 'אלא' / 'ולא' substrings, checked against the 4 bucket sub-captions + disclosure line + alt text)",
    "em_dash_hits": "0/6 strings scanned",
    "banned_jargon_hits": "0/6 strings scanned (דירוג/מדורג/מקום N/ניקוד/ציון-as-score/NOVA/BSIP/cap/floor)",
    "passes_with_flag_product_count_cited": "5/18 (source: magnesium-guide-data.ts PW-bucket product entries 1-5, and headlineFinding.body[2])",
    "suppressed_bars_uniformity_cited": "18/18 for both thirdPartyVerification and priceFairness (source: magnesium_guide_bar_revision_call_v1.md premise-check parse of magnesium-guide-data.ts)"
  },
  "commands_run": [],
  "not_done": [
    "No file edit to magnesium-guide-data.ts — copy delivered as a standalone doc per task instruction (gate 1 draft only).",
    "No commit made.",
    "Gate 2 (Adversarial QA / Red-Team) sign-off not sought by this agent — required before any slot ships.",
    "sha256 of this returned doc not computed (draft handoff, not a closing artifact) — orchestrator/QA should hash at intake if needed for the return-contract chain."
  ],
  "self_check": "Acceptance test: zero occurrences of the banned antithesis substrings (,לא / אלא / ולא), zero em-dashes, and zero banned engine-jargon terms across all 6 shipped strings, verified by manual scan of each final string (shown above) rather than asserted; all 6 quantitative claims in prose (5-product count, 18/18 suppression counts) trace to a named artifact (magnesium-guide-data.ts or the Product Agent's premise-check report), not invented."
}
```
