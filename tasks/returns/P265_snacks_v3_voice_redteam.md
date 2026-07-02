# P265 — Snacks v3 Voice Red-Team Report

**Shelf:** חטיפים (snacks_frontend_v3.json) · 18 products  
**Authored by:** Cursor (C1-CURSOR lane)  
**Reviewed against:** Tom Bari Voice v1.0 (Harvest #1–#4 encoded)  
**Date:** 2026-06-19  
**Mode:** READ-ONLY — no edits made

---

## VERDICT: NEEDS-FIX

Overall the shelf is structurally sound and shows real improvement over v2. The prologue framing is original and shelf-specific. The numeric discipline is mostly clean. However there are one CRITICAL failure, three HIGH failures, and seven MEDIUM issues that block publication as-is.

---

## CRITICAL FINDINGS (1 active; 1 retracted)

---

### CRIT-1 — HF-6 + HF-8: Code-token leakage in `comparisonContext` (snk-007 / Fitness שוקולד מריר, rank 15)

**Product:** פיטנס בר שוקולד מריר (snk-007, id: `snk-007`, score 27.3/E)  
**Field:** `expansion.comparisonContext`  
**Exact Hebrew snippet:**
> "34.1% דגן מלא — יותר מ-הגרסה הקלאסית של פיטנס הקלאסי (34.1% זהה). אבל 22 מרכיבים לעומת 16. שלושה מקורות סוכר לעומת אחד. שוקולד מריר מפצה חלקית."

The problem is not this line itself, but the `comparisonContext` for the Fitness bar product (snk-007, rank 15) at offset ~2489 references:
> "גרסת הגרנולה דומה שגם הוא E. 16 נקודות מתחת ל-**גרסת גרנולה דומה שגם הוא E**"

And the `comparisonContext` for snk-013 (קורני) reads:
> "16 נקודות מתחת ל-**גרסת גרנולה דומה שגם הוא E**."

The phrase "גרסת גרנולה דומה" is an internal cluster/category label used as a neighbor-reference, not a Hebrew product name or plain descriptor. It references a shelf neighbor by what is clearly an internal classification term ("גרסת גרנולה") rather than by product name.

**More seriously:** Multiple `comparisonContext` fields reference sibling products using the label pattern **"גרסת X"** (e.g., "גרסת השקדים", "גרסת הדבש", "גרסת הלוז", "גרסת השוקולד המריר", "גרסת הלוז", "גרסת הקלאסי") — these are shorthand internal variant labels, not consumer product names. While some ("גרסת השקדים") are borderline acceptable as informal Hebrew descriptors, others like "גרסת הגרנולה דומה" and references to "גרסת הקלאסי" for a specific product clearly name a sibling by an internal clustering label rather than by its real Hebrew name or a plain shelf descriptor.

**Specifically failing HF-8:** `comparisonContext` for snk-019 (פיטנס שיבולת שועל דבש) reads:
> "המרגרינה היא ההבדל המרכזי מחטיפי שיבולת שועל הגבוהים יותר."

And the snk-007 (Fitness מריר) `comparisonContext`:
> "34.1% זהה". "שלושה מקורות סוכר לעומת אחד."

But more critically the `comparisonContext` for snk-013 (`bottomLine` field, which is consumer-facing) contains:
> "16 נקודות מתחת ל-גרסת גרנולה דומה שגם הוא E"

"גרסת גרנולה דומה" is an internal cluster descriptor phrased as if it is a Hebrew product name. A reader has no way to identify which product this is.

**Rule broken:** HF-8 — internal product-ID tokens / clustering labels in consumer-facing copy; also violates the plain-Hebrew-name-only rule for sibling references.  
**Suggested direction:** Replace "גרסת גרנולה דומה" with the actual product's Hebrew name (e.g., "חטיפי הגרנולה בציפוי שוקולד מריר של נייצ'ר וואלי" or just "גרנולה נייצ'ר וואלי"). All "גרסת X" shorthand references to named products should be replaced with the actual Hebrew product name or a shelf descriptor that would be intelligible without knowing the internal variant structure.

---

### ~~CRIT-2~~ — Retracted after verification

**Retraction note:** CRIT-2 was drafted based on an incorrect grade-mismatch claim for snk-016. On verification, snk-016 (מרבה סלים טופינג אגוזי לוז) is grade C (51.1/C) and the rowVerdict correctly says "ציון C." The relevant D-verdict product (snk-011, פרי מארז תמרים ואגוזי לוז) correctly says "ציון D" and is grade D (44.0/D). No grade mismatch exists. CRIT-2 is voided; a related medium voice observation about snk-011's verdict structure is promoted to MED-7 below.

---

## HIGH FINDINGS (3)

---

### HIGH-1 — Red-label anchoring in `rowVerdict` / `comparisonContext` across multiple products (owner directive violated)

The owner's standing directive (memory: `redlabel_deanchor_directive`): verdicts must NOT be driven by binary "תווית אדומה" signals; severity expressed category-relative/continuous.

Several rowVerdicts use the red label as the primary explanatory frame:

**snk-008** (Marbeh Slim Delis לבן, rank 2):
> "99 קלוריות ל-100 גרם ו-0 גרם סוכר מוצהר מרימים אותו ל-B בתוך קטגוריה שמלאה בסוכר."

The B-grade is explained almost entirely by "absence of red labels" — "0 גרם סוכר מוצהר" and "99 קלוריות" — rather than by the product's structural qualities relative to the shelf. The red-label binary (present/absent) is doing the explanatory work here.

**snk-019** (פיטנס שיבולת שועל דבש):
> "מרגרינה (שמן קוקוס ותוספי מזון) כמרכיב 6 ו-19 מרכיבים עם דקסטרין ואינולין — הגורמים לציון E, לא הסוכר."

The explicit "לא הסוכר" de-anchor is good voice practice — the agent correctly named margarine as the driver. But then also in `consumerTakeaway`:
> "המרגרינה (שמן קוקוס+E471) ו-19 מרכיבים הם הגורם לציון E — לא הסוכר."

The E-number (E471) leaks into the consumer takeaway field here. H4-3 / P-4 prohibit E-numbers in verdict/takeaway prose.

**snk-015** (תמרים בוטנים):
> `expansion.bottomLine`: "63/C: הגרסה הבוטנים-עשירה — חלבון גבוה יותר (8.3גׅ), סוכר גבוה יותר (47.6גׅ). תווית אדומה מחויבת..."

`bottomLine` is consumer-facing. "תווית אדומה מחויבת" as an explanation anchor frames the grade via the binary regulatory signal rather than via the category-relative sugar severity.

**Rule broken:** Owner directive `redlabel_deanchor_directive` — stop anchoring scores on binary Israeli red-label caps; severity expressed category-relative/continuous.  
**Suggested direction:** Replace "תווית אדומה מחויבת" and "מחוץ לאזור התווית האדומה" with the continuous finding — e.g., "47.6 גרם סוכר — גבוה משמעותית בקטגוריה, גם לפרי-שלם כמקור" or "99 קלוריות — הנמוך ביותר בין החטיפים המצופים." Frame severity as shelf-relative percentile/comparison, not red-label presence/absence.

---

### HIGH-2 — E-number leak in consumer copy across multiple products (H4-3 / P-4 violation)

**Products affected:** snk-010 (Fitness קרמל), snk-019 (Fitness שיבולת שועל דבש), snk-007 (Fitness מריר)

**snk-010 `consumerTakeaway` (consumer-facing):**
> "צבע הקרמל (E150) מוסיף שאלה פתוחה על הסוג."

**snk-010 `expansion.consumerExplanation.takeaway` (consumer-facing):**
> "E150 (צבע קרמל) מוסיף שאלה שהתווית לא עונה עליה — הסוג לא מצוין."

**snk-010 `expansion.consumerExplanation.whyRated` (consumer-facing):**
> "19 מרכיבים וצבע קרמל (E150) ללא ציון הסוג — גורמים מגבילים."

**snk-019 `consumerTakeaway` (consumer-facing):**
> "מרגרינה (שמן קוקוס+E471) ו-19 מרכיבים הם הגורם לציון E"

**snk-019 `expansion.consumerExplanation.takeaway` (consumer-facing):**
> "המרגרינה (שמן קוקוס+E471) ו-19 מרכיבים הם הגורם לציון E — לא הסוכר."

**snk-007 `expansion.consumerExplanation.whyRated` (consumer-facing):**
> "34.1% דגן מלא — נקודה חיובית. שלושה מקורות סוכר (גלוקוזה+לבן+אינברטי), 22 מרכיבים, גליצרול ו-E476 — גורמים מגבילים לE."

In all cases, `consumerTakeaway`, `takeaway`, and `whyRated` are consumer-facing expansion panel fields. E-numbers (E150, E471, E476) and technical chemical abbreviations ("PGPR") appearing in those fields fail H4-3 and P-4. The `rowVerdict` fields for these products are clean (they generalize to "תוספי מזון") — the failure is specifically in the sub-expansion fields.

**Rule broken:** H4-3 (additive generalization — E-numbers in verdict/takeaway prose) and P-4 (additive mentions are whole-picture counts, never E-number codes in consumer copy). Note: E-numbers belong exclusively in the `d4_additives` sub-dropdown panel, not in `consumerTakeaway`, `takeaway`, or `whyRated`.  
**Suggested direction:**  
- snk-010: Replace "E150 (צבע קרמל)" → "צבע קרמל (הסוג לא מצוין על התווית)" in all three consumer fields.  
- snk-019: Replace "שמן קוקוס+E471" → "שמן קוקוס ותוספי מזון" in both takeaway fields.  
- snk-007: Replace "גליצרול ו-E476" → "גליצרול ותוספי מזון נוספים."

---

### HIGH-3 — HF-1: "אז זהו — שלא תמיד" pivot is absent across the shelf (opposite problem: complete suppression of all signature moves)

HF-1 tests for *overuse* of signature moves (>2/5 consecutive). The opposite failure is relevant here: across 18 products, the shelf has **zero occurrences** of any signature Tom move in insightLine or rowVerdict:

- "אז זהו — שלא תמיד" — 0 instances
- "X לא תמיד אומר Y" — 0 instances  
- "קינוח בתחפושת" — 1 instance (snk-020, the blueberry bar — correctly used and is the strongest line on the shelf)
- "הבעיה היא לא רכיב אחד. הבעיה היא התמונה הכוללת" — 0 instances

The prologue has one "לפעמים… לפעמים…" parallelism that is Tom-adjacent but not a registered signature move. The rowVerdicts and insightLines read as clean structured summaries — accurate and non-generic — but they consistently lack the Tom voice texture that the fingerprint requires (§3, checklist Step 3 item 13). 18 verdicts with a single signature-move instance is not a pass; it is a mechanical suppression of the voice's most distinctive quality.

This is not HF-1 (overuse) but fails Step 3 item 13 of the voice-match gate checklist: "Uses at least one signature move (situation opener, 'X לא תמיד אומר Y', image-vs-structure, the 'אז זהו' pivot) — without mechanically over-using one."

**Rule broken:** Voice-match gate Step 3 item 13 (signature move present on shelf without overuse).  
**Suggested direction:** The prologue is the natural place to anchor 1–2 signature moves. The product with the starkest image-vs-structure gap on the shelf — snk-007 (Fitness dark chocolate: "פיטנס" in the name, 22 ingredients, 3 sugar sources) — is the perfect candidate for the "השם מוכר. המבנה פחות." move or a gentle "אז זהו" pivot. The "קינוח בתחפושת" on snk-020 is correctly used and should be kept. No more than 2 additional signature moves should be inserted.

---

## MEDIUM FINDINGS (6)

---

### MED-1 — Prologue sentence 3: "נסרקנו 53 מוצרים" is functional but not Tom

**Field:** `snacksPrologueSentences[2]`  
**Exact snippet:**
> "נסרקנו 53 מוצרים. 18 נבחרו לתצוגה — כדי לראות איך הפערים במדף נראים מבפנים. אפילו החטיף החזק בקטגוריה הגיע רק ל-B."

This sentence is structural metadata ("corpus statistics") wearing prologue clothing. Tom's arc requires a **situation → familiar perception → pivot** structure (fingerprint §1). Sentence 3 skips the familiar perception and the pivot entirely — it jumps from the scene-opening (sentence 1–2) straight to methodology. "נסרקנו 53 מוצרים" is the Bari methodology line; it belongs in methodology, not in the prologue that is supposed to land the consumer in the moment before the evidence. The result is that the prologue has no pivot — no moment where the comfortable assumption is tested.

**Rule broken:** Fingerprint §1 arc step 3 (the pivot — "comfortable assumption gently broken"); voice-match gate Step 1 item 2.  
**Suggested direction:** Replace sentence 3 with a pivot that names what the shopper assumes at the impulse rack vs. what the shelf actually contains — e.g., something that sets up the surprise of "even the best bar here only reached B." Keep the corpus count in the methodology lines where it belongs.

---

### MED-2 — snk-002 (תמר קקאו 100%) `rowVerdict`: the הקשר במדף closer is missing the "what it beats / what it doesn't" dimension

**Product:** חטיף תמרים בציפוי שוקולד 100% קקאו (snk-002, rank 5)  
**Field:** `rowVerdict`  
**Exact snippet:**
> "שני מרכיבים בלבד — תמרים וציפוי 100% מוצקי קקאו ללא סוכר מוסף. הרשימה הקצרה ביותר בקטגוריה. ציפוי קקאו, גם נקי, מסמן שלב עיבוד נוסף על פני גרסת השקדים הגולמית. ציון C."

The closing beat does provide shelf context (compared to "גרסת השקדים") and that is correct. However "גרסת השקדים הגולמית" uses the internal variant shorthand rather than naming the product by its Hebrew name. And the verdict omits what the product beats — there are 5 D-products and 5 E-products it outranks. The closer is incomplete per fingerprint §1 step 7 ("what it beats, what it doesn't").

**Rule broken:** Fingerprint §1 step 7 (הקשר במדף must place product in shelf context: standing, what it beats, what it doesn't); HF-8 adjacent (informal sibling reference).  
**Suggested direction:** Add a brief shelf-standing sentence: e.g., "בין המוצגים, הוא נמצא בשלישיית החזקים — מעל כל חטיפי הדגנים המצופים שמחזיקים 6–22 מרכיבים." And replace "גרסת השקדים הגולמית" with "חטיף התמרים עם השקדים" or the product's Hebrew name.

---

### MED-3 — `expansion.bottomLine` in multiple products is consumer-facing but reads as internal pipeline notation

**Products affected:** snk-001, snk-008, snk-015, snk-004, snk-002, multiple others  
**Field:** `expansion.bottomLine`  
**Examples:**
- snk-001: `"70/B: הניקוד הגבוה ביותר בקטגוריה — הבסיס הנקי ביותר. מי שמתמקד בסוכר ידע: תמרים הם ~65% פחמימות"`
- snk-008: `"68/B: קלוריות נמוכות ואפס תויות אדומות הם הגורם. שוקולד לבן 73% עם שומן טרנס 0.5גׅ ושומן רווי 3.0גׅ מגבילים — זה פינוק, לא חטיף מזין."`
- snk-004: `"59/C: חטיף פשוט לקטגוריה, אבל שוקולד תעשייתי לפני דגן לא עולה מעל C"`

The "XX/G:" prefix format (score/grade colon) is a raw score-mechanic leakage pattern. File 5 explicitly bans "raw score mechanics ('68.2', '72/B')" from consumer copy. The `bottomLine` field is consumer-facing (it appears in the expansion panel). Displaying "68/B:" as a prefix in the sentence is exactly this banned pattern.

Additionally the tilde notation (`~65% פחמימות`) in snk-001 may be an approximation not directly in the scrape, borderline HF-4.

**Rule broken:** File 5 banned phrases: "ALL CAPS, raw score mechanics ('68.2', '72/B')"; fingerprint §5 ("Numbers when available, framed per-100g and tied to meaning, never raw mechanics").  
**Suggested direction:** Strip the "XX/B:" prefix from all `bottomLine` entries. The score/grade is already displayed elsewhere on the card; repeating it as a colon-prefix in prose is mechanic leakage. Begin the bottomLine with the finding, not the score.

---

### MED-4 — snk-018 (Corn Pops / קורני קלאסי) `comparisonContext` uses internal product reference label

**Product:** קורני קלאסי (rank ~14, snk-018)  
**Field:** `expansion.comparisonContext`  
**Exact snippet (from the Fitness מריר product, snk-007):**
> "34.1% זהה". "גרסת הקלאסי"

The label "גרסת הקלאסי" appears in snk-007's comparisonContext as a reference to snk-018. "הקלאסי" is an informal internal nickname. The product's actual Hebrew name should be used.

Similarly, snk-013 (קורני שוקולד מריר) `comparisonContext` references:
> "16 נקודות מתחת ל-גרסת גרנולה דומה שגם הוא E"

"גרסת גרנולה דומה" is an undefined shelf neighbor reference. No reader can identify this product.

**Rule broken:** HF-8 — sibling products referenced by informal internal label rather than Hebrew product name or plain descriptor.  
**Suggested direction:** Use the full Hebrew product name for any named comparison, e.g., "נייצ'ר וואלי צ'ואי" or "גרגירי גרנולה נייצ'ר וואלי שוקולד מריר" for the neighbor product, not "גרסת גרנולה דומה."

---

### MED-5 — snk-009 (Nature Valley Chocolate Peanut Bar) `insightLine` is accurate but has a tone register issue

**Product:** נייצ'ר וואלי בר שוקולד ובוטנים (snk-009, D-grade, rank ~11)  
**Field:** `insightLine`  
**Exact snippet:**
> "בוטנים קלויים 37.3%, 10 גרם חלבון — 18 מרכיבים סביבם"

And `rowVerdict`:
> "בוטנים קלויים 37.3% — החלבון (10 גרם) אמיתי. סביבם: 18 מרכיבים עם סירופ גלוקוזה, מלטודקסטרין, פרוקטוז וגליצרול. הפשרה שמגיעה עם כל חטיף פרוטאין. ציון D."

The phrase "הפשרה שמגיעה עם כל חטיף פרוטאין" is borderline H3-R2 (information-dump with a quasi-finding) — it generalizes across a product class ("כל חטיף פרוטאין") rather than grounding in this product's specific evidence. It is also mildly generic (could describe any protein bar). More importantly "מלטודקסטרין" and "פרוקטוז" and "גליצרול" are named chemical/ingredient terms dumped into the rowVerdict without generalization — this violates H4-3's direction to generalize to "תוספי מזון" or "מרכיבי עיבוד" in verdict prose.

**Rule broken:** H4-3 (additive generalization in verdict prose — "מלטודקסטרין, פרוקטוז וגליצרול" is a chemical roster, not a generalized finding).  
**Suggested direction:** Replace "סירופ גלוקוזה, מלטודקסטרין, פרוקטוז וגליצרול" with "סירופ גלוקוזה ומרכיבי עיבוד נוספים" or "ארבעה מרכיבי עיבוד נלווים" — keep the count (meaningful) without listing chemical names.

---

### MED-7 — snk-011 (פרי מארז תמרים ואגוזי לוז) `rowVerdict`: facts arrive before the structural finding

**Product:** snk-011 (rank 12, D-grade)  
**Field:** `rowVerdict`  
**Exact snippet:**
> "שישה מרכיבים עם אגוזי לוז 25% ממקור שלם. הסוכר (38.7 גרם) גבוה, מגיע מתמרים וצימוקים בלבד. 'חומרי טעם טבעיים' מסמנים עיבוד גם ברשימה אחרת נקייה. ציון D."

The third sentence does carry a finding ("מסמנים עיבוד גם ברשימה אחרת נקייה") so this does not reach HF-7. But the three-beat structure — positive fact, negative fact, processing signal — reads as a data tour rather than a verdict that leads with the structural insight. For a D-product, the lead should be the finding: this "natural-looking" bar has processing markers even in a short list. The positive framing of sentence 1 followed by the negative sugar sentence 2 creates a false balance before the actual verdict lands. The הקשר במדף (shelf standing vs. its neighbors) is also absent.

**Rule broken:** Voice-match gate Step 1 item 4 (הקשר במדף required); fingerprint §1 step 7 (the closing beat places the product in shelf context).  
**Suggested direction:** Lead with the structural finding (the "חומרי טעם טבעיים" as the marker that even a clean-looking short list carries a processing signal), then close with shelf context vs. neighbors.

---

### MED-6 — Category note (`snacksCategoryNote`) uses the word "מחויבת" in connection with scoring — borderline prescription

**Field:** `snacksCategoryNote` (rendered in the page header)  
**Exact snippet from the `editorial_note` in `_meta`:**
> "כשאתם בוחרים כאן, אתם בוחרים בין רמות של פינוק."

The final sentence of the `editorial_note` (which may render to consumers depending on the implementation) crosses from description into mild prescription. "אתם בוחרים בין רמות של פינוק" is editorially telling the consumer how to interpret their own choice ("you are choosing between levels of indulgence") — this is framing that could be read as shaming (implying snacks are always indulgence, not a legitimate shelf). File 5 and fingerprint §6 ("never shame the consumer") are the relevant standards.

The **published** `snacksCategoryNote` (the two-item array in the TS file) is clean and does not have this problem. This concern is specific to `_meta.editorial_note` in the JSON, which must be confirmed as internal-only vs. consumer-visible.

**Rule broken:** If consumer-visible: file 5 "never shame the consumer" / fingerprint §6; borderline blanket-category verdict.  
**Suggested direction:** Confirm that `_meta.editorial_note` is not consumer-rendered. If it is, replace with: "הציונים מבטאים מרחק מבסיס תזונה — גם הציון הגבוה ביותר כאן מתאר חטיף, לא ארוחה." This describes without framing the act of buying as an indulgence.

---

## 2–3 STRONGEST LINES ON THE SHELF

These pass the voice gate with distinction:

1. **snk-020 (blueberry bar) `rowVerdict`:**  
   "אוכמניות? רכז, אחרי שלושה ממתיקים. קינוח בתחפושת חטיף. ציון E."  
   — Textbook H4-4 punch. Short, evidenced, names the disguise without brand-attack. The best sentence on the shelf.

2. **snk-013 (קורני שוקולד) `insightLine`:**  
   "שוקולד לפני הדגן, 5 מקורות סוכר — 451 קלוריות, לא חטיף דגנים"  
   — Specific, verifiable, structurally damning without shaming. The "לא חטיף דגנים" flip at the end is exactly the image-vs-structure move done right.

3. **snk-001 (תמר שקדים) `rowVerdict`:**  
   "המוצר החזק בקטגוריה — לא כי הוא קסם תזונתי, אלא כי הוא הפשוט ביותר."  
   — The honest-positive mode done well. "לא קסם תזונתי" is the correct hedge. Un-hedged praise + honest limit in one beat.

---

## Summary Table

| # | Severity | Product/Field | Rule | Status |
|---|---|---|---|---|
| CRIT-1 | CRITICAL | Multiple `comparisonContext` — "גרסת גרנולה דומה", "גרסת הקלאסי" | HF-8 internal sibling label | BLOCKS |
| ~~CRIT-2~~ | ~~CRITICAL~~ | ~~snk-016 grade mismatch~~ | ~~Retracted — no mismatch found~~ | VOID |
| HIGH-1 | HIGH | snk-008, snk-015, snk-019 — red-label anchor in verdict | Owner directive redlabel_deanchor | FIX |
| HIGH-2 | HIGH | snk-019 `consumerTakeaway`, snk-007 `whyRated` — E-numbers in consumer copy | H4-3, P-4 | FIX |
| HIGH-3 | HIGH | Shelf-wide — zero signature moves in verdicts | Fingerprint §3, Gate Step 3 item 13 | FIX |
| MED-1 | MEDIUM | Prologue sentence 3 — methodology stat, no pivot | Fingerprint §1 arc | FIX |
| MED-2 | MEDIUM | snk-002 `rowVerdict` — הקשר במדף incomplete | Fingerprint §1 step 7 | FIX |
| MED-3 | MEDIUM | Multiple `bottomLine` — "XX/B:" prefix = raw score mechanic | File 5 banned phrases | FIX |
| MED-4 | MEDIUM | snk-007, snk-013 `comparisonContext` — unnamed sibling references | HF-8 | FIX |
| MED-5 | MEDIUM | snk-009 `rowVerdict` — chemical roster in verdict prose | H4-3 | FIX |
| MED-6 | MEDIUM | `_meta.editorial_note` — "בוחרים בין רמות של פינוק" | File 5 / Fingerprint §6 | VERIFY then fix if consumer-visible |
| MED-7 | MEDIUM | snk-011 `rowVerdict` — data-tour structure, הקשר במדף absent | Fingerprint §1 step 7, Gate Step 1 item 4 | FIX |

---

```json
{"snacks_verdict":"NEEDS-FIX","critical":1,"high":3,"medium":7}
```
