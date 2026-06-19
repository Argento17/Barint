# Nutrition Claim-Safety Review v1 — Tom-Bari Hebrew Voice System

**Reviewer:** Nutrition Agent  
**Date:** 2026-06-18  
**Scope:** Files 2 (voice fingerprint), 5 (banned phrases / claim control), 6 (dummy reviews)  
**Status:** PRE-PRODUCTION GATE — must pass before first production use  
**TASK:** TASK-337

---

## Executive Verdict

The Tom-Bari voice system is **architecturally sound** for nutrition-claim safety. The core
firewall (file 5) is correctly structured, the dummy reviews (file 6) consistently flag
Tier-B claims rather than stating them, and the voice fingerprint (file 2) bakes in the
"whole picture" anti-single-villain rule that prevents additive-disease linkage. No disease
language, toxicity language, or medical-advice language appears in any of the three reviewed
files.

Three gaps require closure before first production use: (a) two grey-zone descriptors in
file 6 lack a backing rule in file 5; (b) the disease-link phrase "קשר לסרטן" that exists
in cakes source data is confirmed blocked but the block is implicit — it should be explicit;
(c) the draft-to-publication tightening is under-specified.

The full analysis follows.

---

## 1. Health-Effect Leakage Scan

### 1.1 File 5 — Banned Phrases & Claim Control

**Findings:**

The file correctly bans:
- "גורם לסרטן / קשור לסרטן" — cancer linkage. Listed in the banned table with the
  required replacement ("דורש בדיקת ראיות לפני טענה כזו") and escalation instruction.
  This confirms that the E471 "קשר לסרטן" additive note that appears in the cakes source
  data (BSIP2 extractor additive-burden signal) **must never reach consumer copy**. The
  block is present but implicit — it appears as a row in a table without a standalone
  explanatory note explaining WHY the disease block applies even to per-ingredient additive
  metadata. See Recommendation R-1.

- "הורס את הבריאות / לא ראוי למאכל" — correctly banned (moral + scare).
- "מסוכן" — correctly banned.
- "רעל / מוצר רעיל / תחליף כימי / מלא כימיקלים" — correctly banned.

**Gap:** The Tier-B escalation list in §2 includes "any health *effect* or risk" but does
not cite the additive-burden signal by name. A content agent writing from additive-burden
data could innocently reproduce the E471 EFSA annotation without realising it falls under
Tier-B. The additive-burden data path needs an explicit rule. See Recommendation R-1.

**No health-effect leakage found in file 5 as written.** All known disease-adjacent phrases
are blocked.

---

### 1.2 File 6 — Dummy Reviews

All 10 reviews (A1–A10) reviewed line by line.

**Health-effect phrases found:** None. Confirmed zero disease, toxicity, or medical-advice
language.

**Borderline items that passed on scrutiny:**

| Location | Phrase | Assessment |
|---|---|---|
| A3 | "שמנים צמחיים, מחמאה, מייצבים ומתחלבים" | Safe — formulation description only, no health-effect claim |
| A8 | "נוכחות של רכיב מעובד כמו מתחלב" | Safe — structural signal, not a disease link |
| A5 (שורת בארי) | "מתועש מדי — שם מתחילה הבעיה" | Borderline — analysed fully in §2 (grey-zone descriptors) |
| B.3 Intro 2 | "שמנים צמחיים, מחמאה או מרגרינה, חומרי הלחה, מייצבים, מתחלבים, חומרי טעם, חומרים משמרים" | Safe — ingredient enumeration, not a health verdict |

**The dummy reviews are clean on health-effect leakage.** Every Tier-B-adjacent claim in
A1–A10 is flagged with a "דורש אימות לפני פרסום" note. None states a health effect.

---

### 1.3 File 2 — Voice Fingerprint

**Health-effect phrases found:** None.

The fingerprint correctly contains the rule "Never use a fear/health claim unless
Nutrition/Research approved" (§6). The "לא רכיב אחד — התמונה הכוללת" signature move
(§3) and the "Never make one additive the whole story" hard never (§6) are the most
important structural safety features of the voice: they prevent the content engine from
singling out E471 or any other additive and implying disease causation.

**One tension flagged:** §6 says "Never use a fear/health claim unless Nutrition/Research
approved" but does not define what counts as a fear/health claim at the phrase level. This
is left implicit. It should cross-reference file 5's Tier-B list explicitly. See
Recommendation R-2.

---

## 2. Grey-Zone Descriptor Rulings

Each descriptor is ruled on independently.

### 2.1 מעובד (processed)

**Category:** Descriptive — safe with a structural anchor.

"מעובד" describes a process, not a health effect. It is safe when it refers to an
observable property of the product (long ingredient list, industrial inputs, NOVA-proxy
signals) and is not presented as a harm verdict.

**Safe form:** "מוצר מעובד" is safe when the preceding sentence names the structural
evidence (e.g., "רשימת רכיבים ארוכה, תוספי מזון רבים"). Standing alone as a label
without structural evidence it becomes an unsupported assertion — not a health claim, but
a quality-claim that needs backing.

**Rule:** State "מוצר מעובד" only after naming the structural signal that qualifies it.
Never as the opening sentence of a review.

**Product-data backing required?** Yes — at minimum: ingredient-list length and presence
of at least one additive class, both from the product scrape.

---

### 2.2 מתועש (industrialized / highly processed)

**Category:** Borderline — safe only with strong structural backing; can shade into
implied harm.

"מתועש" is a stronger register than "מעובד." In consumer Hebrew it carries a mild negative
connotation. It is not a health claim, but it implies that the product's construction
method is distant from any natural analogue — a formulation statement, not a physiology
statement.

It appears in A5's שורת בארי: "מתועש מדי — שם מתחילה הבעיה." In context (a hypothetical
cake with a short ingredient list being praised) this is used as a *contrast* standard —
the product has not crossed into "מתועש" territory, which is what earns it the Positive
mode. This is a legitimate use: the descriptor defines the threshold being avoided, not an
accusation against the product.

**Safe form:** "מתועש" is safe when:
(a) it is grounded in a specific structural reading (very long ingredient list + multiple
additive classes + industrial fat sources); AND
(b) it describes the product's *construction method*, not its physiological effect.

**Unsafe form:** "מתועש ולכן מזיק" / any phrase that connects "מתועש" to a health outcome.

**Product-data backing required?** Yes — ingredient-list length + at minimum two
categories of industrial inputs from the scrape. "מתועש" applied to a product with a
three-ingredient list is an unsupported verdict.

---

### 2.3 שומן רווי גבוה (high saturated fat)

**Category:** Safe with product-data number; requires the number.

"שומן רווי גבוה" is a label-derivable, panel-based statement. It is a nutritional
composition descriptor, not a health claim. The Israeli red-label threshold provides
categorical context (>3.2 g/100g for חטיפים, category-specific elsewhere) but per the
standing red-label de-anchor directive the score architecture moves away from binary
threshold anchoring.

**Safe form:** "שומן רווי בכמות גבוהה" is safe when the per-100g figure from the
product scrape is cited or available for the reader to verify. Example: "שומן רווי של
X גרם ל-100 גרם — גבוה ביחס לקטגוריה."

**Unsafe form:** "שומן רווי גבוה גורם ל..." / any causal extension. Also unsafe: stating
"שומן רווי גבוה" without the product-scrape number when the number is knowable — this
creates a claim without a source (Tier-A violation).

**Product-data backing required?** Yes — the per-100g saturated-fat figure from the
product's own scraped panel.

**Scientific-source review required?** No. The claim is compositional (describing what
is in the product), not causal (claiming what it does to the body).

---

### 2.4 סוכר גבוה (high sugar)

**Category:** Safe with product-data number; same logic as שומן רווי גבוה.

"סוכר גבוה" is a panel-derivable compositional descriptor. When accompanied by the
per-100g figure from the scrape it is Tier-A. Without the figure it becomes an unsupported
claim.

**Safe form:** "סוכר של X גרם ל-100 גרם" or "סוכר גבוה יחסית למדף" with the figure
available. The phrase also works in the voice as a comparative: "הסוכר עדיין גבוה" (A10)
when prior context established the product's sugar level.

**Unsafe form:** "סוכר גבוה גורם ל-..." / any causal extension. Also: "סוכר גבוה" as
the sole line of a review with no number behind it.

**Product-data backing required?** Yes — per-100g sugar from the product scrape.

**Scientific-source review required?** No.

---

### 2.5 פחמימה ריקה (empty carb)

**Category:** Requires scientific-source review before use. Do not use in DRAFT without
a flag.

"פחמימה ריקה" is a nutritional-science concept (low-fiber, low-protein carbohydrate with
rapid glycaemic response) that is not panel-readable without additional data (GI/GL
testing). It implies a physiological mechanism — that the carbohydrate delivers energy
without satiety or micronutrient contribution — which moves it toward a health-effect claim
in its common usage.

In the dummy reviews the voice uses the safer equivalent: "בעיקר פחמימה קלה" (A7, Intro
5). This is the approved substitute — it describes the panel observation (low fiber, low
protein, high carbs) without implying a metabolic verdict.

**Safe replacement:** "בעיקר פחמימה קלה" or "פחמימה ללא סיבים / חלבון משמעותי" +
the backing numbers. Both are Tier-A when the fiber and protein figures come from the
scrape.

**"פחמימה ריקה" as a phrase is BANNED from consumer copy.** It is a scientific shorthand
that sounds like a health verdict in consumer Hebrew.

**Scientific-source review required?** The concept itself is well-established (KB-004
DIAAS protein quality; standard nutritional biochemistry), but the phrase requires Nutrition
Agent review before any use, and should be replaced with the safe form regardless.

---

### 2.6 חלש תזונתית (nutritionally weak)

**Category:** Safe as-is — it is the approved replacement for "לא בריא" and is already
listed in file 5's banned-phrase table as the correct alternative.

"חלש תזונתית" describes a product's nutritional profile relative to the category; it does
not attribute a health effect to the consumer. It is a score-describing phrase, not a
medical recommendation.

**Safe form:** As written. Works best when the specific weaknesses are named: "חלש
תזונתית — סיבים נמוכים, חלבון נמוך, סוכר גבוה." Naming the dimensions prevents it from
reading as a moral verdict.

**Product-data backing required?** Yes — at minimum the dimensions that make it "חלש"
(e.g., fiber < X g/100g, protein < Y g/100g) from the product scrape. Without backing
numbers it is an unsupported characterization.

**Scientific-source review required?** No.

---

### Grey-zone summary table

| Descriptor | Safe? | Backing needed | Safe form |
|---|---|---|---|
| מעובד | Yes — with structural anchor | Ingredient-list length + additive class from scrape | After naming the structural evidence |
| מתועש | Yes — with strong structural backing | Long list + ≥2 industrial input classes from scrape | Construction method only; never connect to health outcome |
| שומן רווי גבוה | Yes — with number | Per-100g saturated fat from scrape | "שומן רווי של X גרם ל-100 גרם" |
| סוכר גבוה | Yes — with number | Per-100g sugar from scrape | "סוכר של X גרם ל-100 גרם" or comparative with prior context |
| פחמימה ריקה | **No — banned** | N/A | Replace with "בעיקר פחמימה קלה" + fiber/protein numbers |
| חלש תזונתית | Yes — approved | Named dimensions from scrape | Name the specific weak dimensions |

---

## 3. Is "דורש אימות לפני פרסום" Sufficient for DRAFT Mode?

**Yes — sufficient for DRAFT mode, with one condition.**

The flag format defined in file 5 §2 ("דורש אימות לפני פרסום: \<exact fact/claim\>, מקור:
\<product scrape field / "pending Nutrition"\>") is correctly structured for DRAFT. It
serves three functions: (a) marks what has not been verified, (b) names the exact claim
requiring verification, and (c) names the source category (product scrape vs. Nutrition
Agent). All 10 dummy reviews carry this flag; all flag the right facts (ingredient counts,
macro figures, additive presence).

**The one condition:** the flag must name the exact claim. A generic "מקור: product
scrape" on a flag that covers multiple claims (e.g., A1 flags "מספר תוספי המזון, כמות
שומן רווי ל-100 גרם, רכיבי פרווה/שמנת צמחית" as a bundled list) is acceptable in draft
but each item must be verified individually before publication. A flag covering three
claims does not clear when one of the three is confirmed — all three need independent
verification.

**Draft mode rule:** A review with unflagged Tier-B claims does not advance to publication
review. A review with only flagged Tier-A items may circulate as DRAFT for editorial
feedback. This is already the rule in file 5 §3 (Gate Order: Claim scan is gate 1).

---

## 4. Does Publication Mode Need Stricter Wording?

**Yes.** Publication mode introduces five tightening requirements that do not apply in
DRAFT.

### 4.1 All "דורש אימות" flags must be resolved or the claim must be removed

In DRAFT, a flagged claim is a placeholder. In PUBLICATION, every flag must be closed with
one of:
- The verified figure from the product scrape, cited inline (e.g., "שומן רווי: 12 גרם
  ל-100 גרם — מתוך לוח הערכים התזונתיים").
- Removal of the claim if the scrape data is absent (per the missing-data discard rule:
  unknown is acceptable, fabrication is not).
- Promotion to Tier-B with explicit Nutrition Agent sign-off documented.

No "דורש אימות" flag may survive into a published review.

### 4.2 Numbers must be presented per-100g and tied to meaning

A publication review stating a raw figure without a referent fails the voice standard.
"שומן רווי: 12 גרם" without a per-100g framing or a category comparison is acceptable in
a draft flag but must be resolved to "שומן רווי של 12 גרם ל-100 גרם — גבוה ביחס
לקטגוריה" in publication.

### 4.3 "לא בריא" / "בריא" (blanket) must not appear

Already required by file 5, but enforced at publication via the claim scan (Gate 1) before
any handoff.

### 4.4 Additive mentions must be formulation-framed, never disease-framed

See §5 below. In DRAFT an additive may be named with a flag ("דורש אימות: נוכחות E471 —
מתחלב, בדיקה מפרטת המוצר"). In PUBLICATION the additive appears only as a formulation
signal within the whole-picture framing: "מספר מתחלבים ומייצבים ברשימת הרכיבים" — no
E-number singled out, no EFSA annotation surfaced to the consumer.

### 4.5 "מוצר היפותטי" markers must be removed or replaced

A5 in the dummy reviews is marked "(מוצר היפותטי — להחלפה במוצר אמיתי)." In publication
this placeholder must be replaced with a real-product review grounded in a real scrape.
Hypothetical products do not ship in publication mode.

### Draft → Publication tightening summary

| Dimension | DRAFT | PUBLICATION |
|---|---|---|
| Flagged Tier-A claims | Allowed with "דורש אימות" flag | Must be resolved — verify or remove |
| Tier-B claims | Must be flagged + "pending Nutrition" | Must have written Nutrition Agent sign-off |
| Blanket health descriptors | Flagged | Banned — no exception |
| Additive E-numbers | May appear in flag text | Must not appear in consumer copy |
| Hypothetical products | Allowed as examples | Must be replaced with real scrape |
| Per-100g grounding | Recommended | Mandatory for any numeric claim |

---

## 5. Additive Claims: Formulation Signal vs. Safety Verdict

**Confirmed rule:** Additives are framed as formulation signals (part of the whole picture),
never as safety or disease verdicts. The three files hold to this rule — analysis follows.

### 5.1 The rule as stated

File 2 §3 contains the signature move "לא רכיב אחד — התמונה הכוללת" and explicitly bans
"Never make one additive the whole story." File 5 §1 bans "גורם לסרטן / קשור לסרטן."
These two, together, create the correct architecture: an additive like E471 can appear as
part of a structural description ("מספר מתחלבים ברשימת הרכיבים") but cannot be presented
as "E471 — קשור לסרטן" even though that annotation exists in the BSIP2 additive-burden
signal data.

### 5.2 Do files 5/6/2 hold to it?

**File 5:** Yes. The Tier-B escalation requires Nutrition Agent sign-off for "any health
effect or risk." The banned phrase table explicitly catches "גורם לסרטן / קשור לסרטן."

**File 6:** Yes. In A3 (עוגת שוקולד פרווה), the review names "מייצבים ומתחלבים" as
part of the structural description without attaching a health verdict. In A8 (קורנפלקס
ללא גלוטן), "נוכחות של רכיב מעובד כמו מתחלב" is framed as a formulation observation.
The שורת בארי lines and the "דורש אימות" flags in A1–A10 do not mention E-numbers or
EFSA annotations. Clean across all 10 reviews.

**File 2:** Yes. §6 "Never make one additive the whole story" and the "anti-single-villain"
framing rule in §3 both enforce the formulation-signal frame.

### 5.3 Gap: the data-path risk

The additive-burden extractor (EV-003 / EV-019) carries structured additive records
including risk tiers and — in some cases — disease-association annotations from EFSA
evaluation pointers (e.g., "קשר לסרטן" for E471 in some interpretations of the animal
carcinogenicity literature). This annotation lives in the engine data layer and is used for
scoring, not for consumer copy. The risk is that a content agent calling the additive-burden
data to populate a product review could surface this annotation directly.

**File 5 currently blocks the output phrase but does not block the data path.** The
instruction to escalate "any health effect or risk" covers this, but only if the content
agent identifies the annotation as a health-effect claim before writing it.

See Recommendation R-1 for the explicit additive-data-path rule needed in file 5.

---

## 6. Classified Phrase Inventory

### Bucket 1: Approved — Safe as-is

Phrases from files 2/4/5/6 that require no additional verification or sign-off.

1. "אז זהו — שלא תמיד." (pivot)
2. "המראה ביתי. המבנה פחות." (image-vs-structure)
3. "השם של המוצר מוכר. המבנה שלו פחות." (image-vs-structure)
4. "זה לא אומר שאי אפשר לאכול את זה. זה כן אומר שכדאי לדעת מה קונים." (stance)
5. "הבעיה היא לא רכיב אחד. הבעיה היא התמונה הכוללת." (anti single-villain)
6. "כל רכיב כזה יכול להיות חוקי ומקובל. הבעיה היא התמונה הכוללת." (anti single-villain)
7. "נקי לא תמיד אומר חזק תזונתית." (workhorse X→Y)
8. "ללא גלוטן הוא מידע חשוב. הוא לא ציון תזונתי." (workhorse X→Y)
9. "מוצר חזק יחסית למדף, לא קסם תזונתי." (positive mode closer)
10. "מוצר סביר הוא לא תמיד מוצר חזק." (balanced mode closer)
11. "בארי לא שואלת אם 'מותר' לאכול את זה." (stance — non-prescribing)
12. "הצרכן לא צריך להיות כימאי כדי להבין מה הוא קונה." (respect line)
13. "חלש תזונתית" — when dimensions are named inline (approved replacement for "לא בריא")
14. "מוגבל תזונתית" (approved in file 5 as replacement)
15. "רשימת רכיבים ארוכה ותוספי מזון רבים" (approved replacement for "מלא כימיקלים")
16. "דורש תשומת לב" (approved replacement for "מסוכן")
17. "פער גדול בין הדימוי לבין הרכב המוצר" (approved replacement for "מזעזע")
18. "כדאי לדעת מה קונים" (approved replacement for "אסור לאכול")
19. "מתאים כ... / פחות מתאים כ..." (approved replacement for blanket "מומלץ / לא מומלץ")
20. "קינוח בתחפושת" (naming-the-disguise; formulation framing, not health claim)
21. "ילד לא אוכל אריזה. הוא אוכל את מה שיש בקערה." (kids framing — no health claim)
22. "בסיס טוב. עוד יותר טוב כשלא מתייחסים אליו כאל כל הארוחה." (positive closer)
23. "אם זה נשמע כמו קינוח, נראה כמו קינוח ומתוק כמו קינוח — קשה לקרוא לזה ארוחת בוקר." (mode closer — categorization, not health claim)
24. "מתועש מדי — שם מתחילה הבעיה." — **approved in context only** (as a contrast standard in a Positive-mode review where the product has NOT crossed into that territory; requires structural anchor when applied to a specific product in Critical mode)

---

### Bucket 2: Phrases Requiring Product-Data Verification

Safe only when the named figure appears in the product's own scraped panel.

| Phrase (as it appears) | Required data | Source |
|---|---|---|
| "שומן רווי בכמות גבוהה" | Per-100g saturated fat figure | Product scrape nutrition panel |
| "שומן רווי גבוה" | Per-100g saturated fat figure | Product scrape nutrition panel |
| "הרבה סוכר" / "סוכר גבוה" / "רמת הסוכר גבוהה" | Per-100g sugar figure | Product scrape nutrition panel |
| "חלבון סביר / נמוך / לא גבוה במיוחד" | Per-100g protein figure | Product scrape nutrition panel |
| "סיבים בכמות יפה / מעט סיבים / סיבים בכמות משמעותית" | Per-100g dietary fiber | Product scrape nutrition panel |
| "רשימת רכיבים ארוכה" | Ingredient-list count or observable length | Product scrape ingredient list |
| "תוספי מזון רבים / מספר מתחלבים / מספר מייצבים" | Named additive classes present in ingredient list | Product scrape ingredient list |
| "מוצר מעובד" (as a product-specific verdict) | Ingredient-list length + ≥1 additive class | Product scrape |
| "מתועש" (as a product-specific verdict) | Ingredient-list length + ≥2 industrial input classes | Product scrape |
| "חלש תזונתית" (as a product-specific verdict) | ≥2 named dimensions (low fiber, low protein, etc.) | Product scrape nutrition panel |
| "100% אורז מלא / ללא תוספת סוכר ומלח" | Label text confirming the claim | Product scrape label text |
| "חיטה מלאה בהתחלה" (ingredient order) | Ingredient order from label | Product scrape ingredient list |
| "בלי תוספת סוכר, בלי מלח ועם רכיב אחד בלבד" | Ingredient list count and label claim | Product scrape |
| "גם מוצר נקי יכול להיות תזונתית די שטוח" (product-specific) | Low fiber + low protein from panel | Product scrape nutrition panel |

---

### Bucket 3: Phrases Requiring Scientific-Source Review

Must have an EV-### citation or Nutrition Agent written sign-off before publication.

| Phrase | Why it needs review | Safe interim replacement |
|---|---|---|
| "פחמימה ריקה" | Implies metabolic/physiological verdict; not panel-readable | "בעיקר פחמימה קלה" + fiber/protein figures |
| "גורם לסרטן" / "קשור לסרטן" (re: any additive) | Disease-causation claim; requires peer-reviewed evidence + Nutrition Agent approval; current EFSA annotations are not consumer-ready claims | Not usable in consumer copy; rephrase as formulation signal |
| Any health effect of a specific additive named by E-number | EFSA evaluations are not consumer verdicts; the additive-burden data path must not surface annotations directly | Name the additive class and the whole-picture count ("מספר מתחלבים") |
| "מסרטן" | Disease claim | Blocked in file 5; no safe replacement — remove |
| Any cross-market / label-gap claim | D5 annotate-only territory; requires Nutrition Agent + Product Agent review | Flag as "pending review" and do not publish |

---

### Bucket 4: Banned or Replacement Wording

| Banned phrase | Reason | Safe replacement |
|---|---|---|
| רעל / מוצר רעיל | Fear / fabrication | רשימת רכיבים ארוכה ותוספי מזון רבים |
| תחליף כימי / מלא כימיקלים | Fear / fabrication | Same as above |
| מסוכן | Unsupported scare | דורש תשומת לב |
| גורם לסרטן / קשור לסרטן | Health claim — not approvable as consumer copy | Not replaceable; remove entirely; formulation signals only |
| הורס את הבריאות / לא ראוי למאכל | Moral + scare | (reframe as image-vs-contents gap) |
| מזעזע / זבל | Shaming / editorializing | פער גדול בין הדימוי לבין הרכב המוצר |
| אסור לאכול / להימנע | Prescribing diet | כדאי לדעת מה קונים |
| בריא (blanket) | Unprovable blanket claim | Name the specific strength (סיבים גבוהים, רשימה קצרה) |
| לא בריא (blanket) | Unprovable blanket claim | חלש תזונתית / מוגבל תזונתית (with named dimensions) |
| מומלץ / לא מומלץ (without for-whom-and-why) | Prescribing diet | מתאים כ... / פחות מתאים כ... + reason |
| תוספי תזונה (meaning additives) | Wrong term (means supplements) | תוספי מזון |
| פחמימה ריקה | Implies metabolic verdict; not panel-readable | בעיקר פחמימה קלה + backing numbers |
| <E-number> + disease annotation as consumer copy | Surfaces EFSA data that cannot be consumer-verified | מספר מתחלבים / מייצבים ברשימת הרכיבים (whole-picture count) |
| מסרטן | Disease claim | Remove; no replacement; never in consumer copy |

---

## 7. Final Publication-Safe Wording Rules

These rules govern the path from DRAFT to PUBLICATION for any review written in the
Tom-Bari voice.

### Rule P-1: All flagged claims must be resolved before publication

Every "דורש אימות לפני פרסום" flag must be closed individually. For each flagged item:
- Verify the figure from the product scrape → replace the flag with the verified figure
  and cite the source field; OR
- Confirm the data is absent → remove the claim entirely (never estimate, round, or fill
  from any external source including OFF).

A review with any surviving "דורש אימות" flag does not ship in publication mode.

### Rule P-2: Every compositional claim must be per-100g and source-cited

Numeric claims (sugar, saturated fat, fiber, protein) must be stated per 100g and
attributed to the product's own scraped panel. The citation need not be verbose — a
parenthetical "(לוח ערכים תזונתיים)" is sufficient — but a raw number with no referent
fails the gate.

### Rule P-3: "מתועש" and "מעובד" require a structural anchor in the same paragraph

If a review calls a product "מעובד" or "מתועש", the same paragraph (or the immediately
prior sentence) must name the structural evidence: ingredient-list length and/or additive
class presence from the scrape. Applied without anchor, these descriptors become
unsupported verdicts.

### Rule P-4: Additive mentions are whole-picture counts, never E-number disease annotations

In publication copy, additives appear as:
- Additive class and count: "מספר מתחלבים ומייצבים" / "שלושה חומרים משמרים ברשימת
  הרכיבים."
- No E-numbers surfaced to the consumer.
- No EFSA risk-tier annotations, disease associations, or OPENFDA adverse-event data
  surfaced to the consumer.
- The engine's additive-burden risk scoring informs the Bari score; it does not become
  copy.

### Rule P-5: No disease or toxicity language at any severity level

"קשר לסרטן", "מסרטן", "גורם לנזק", "הורס את הבריאות" and all equivalent phrases are
banned regardless of how hedged or sourced. The standing Nutrition Agent ruling: Bari
describes nutritional architecture and formulation quality. It does not publish health-
effect verdicts, even peer-reviewed ones, in consumer copy. Route any legitimate scientific
finding about an ingredient through the EV-### evidence registry; it informs scoring, not
copy.

### Rule P-6: Blanket health descriptors are banned; specificity is required

"בריא" and "לא בריא" may not appear as blanket verdicts. Approved alternatives:
- Instead of "בריא": name the specific strength. "סיבים גבוהים, רשימת רכיבים קצרה,
  סוכר נמוך."
- Instead of "לא בריא": "חלש תזונתית" with named dimensions.

### Rule P-7: Mode must be earned by the real product profile

Publication reviews must use the mode (Critical / Balanced / Positive) warranted by the
actual BSIP2 score and trace. A product that scores B cannot be written in Critical mode.
A product that scores E cannot be written in Positive mode. Mode assignment is not an
editorial choice in publication — it is derived from the engine output.

### Rule P-8: Hypothetical products are replaced with real scrape data

Any "מוצר היפותטי" placeholder (as in dummy review A5) must be replaced with a real
product and a real scrape before publication. The hypothetical frame is a development
tool, not a publishable review state.

### Rule P-9: Tier-B claims require written Nutrition Agent sign-off

Any claim about who should or should not consume a product, any health-effect claim, or
any claim about ingredient-level risk (beyond whole-picture formulation framing) requires
explicit written Nutrition Agent approval before publication. The approval must be
traceable — either to an EV-### evidence registry entry or to a dated written ruling.

### Rule P-10: The HebEMO anger+disgust gate is mandatory before publication

Any line intended as dry wit or criticism must pass the HebEMO anger + disgust gate
(`LABEL_0` on both) before the review ships. This gate is already specified in file 5 §1
but is re-stated here because it is the final tonal safety check before publication.

---

## 8. Recommendations (do not apply — for orchestrator routing)

These are recommended edits to `5_banned_phrases_and_claims.md`. The orchestrator decides
whether to apply or route them.

### R-1: Add an explicit additive-data-path rule to file 5

**Current gap:** File 5 bans "גורם לסרטן / קשור לסרטן" as output phrases but does not
explicitly address the data path — a content agent pulling additive-burden records from
the BSIP2 engine data layer (EV-003/EV-019) could encounter risk-tier annotations or EFSA
evaluation notes and reproduce them verbatim.

**Recommended addition** (to §2, Tier-B list, as a new bullet):

> - any additive risk-tier annotation, EFSA evaluation pointer, OPENFDA adverse-event
>   reference, or disease-association note sourced from the engine's additive-burden data
>   (EV-003/EV-019). These inform the Bari score; they are never consumer copy. Frame
>   additives as whole-picture counts (class + count from ingredient list) only.

### R-2: Cross-reference file 5 Tier-B from file 2 §6

**Current gap:** File 2 §6 says "Never use a fear/health claim unless Nutrition/Research
approved" without defining what a "fear/health claim" is at phrase level. A content agent
reading only file 2 may not recognise disease-association annotations as health claims.

**Recommended addition** (to file 2 §6, "Hard 'never's"):

> - Never surface additive risk-tier annotations, EFSA evaluation pointers, or any
>   disease-association note from engine data. See file 5 §2 Tier-B for the full list of
>   health-effect claim types requiring Nutrition Agent sign-off.

### R-3: Add "פחמימה ריקה" to the banned-phrase table in file 5 §1

**Current gap:** "פחמימה ריקה" is used informally in nutritional discourse but implies a
metabolic verdict not derivable from a label. It is not currently in the banned-phrase
table.

**Recommended addition** to file 5 §1 table:

| Banned | Why | Use instead |
|---|---|---|
| פחמימה ריקה | Implies metabolic verdict; not panel-readable; sounds like a health claim in consumer Hebrew | בעיקר פחמימה קלה + fiber/protein figures from scrape |

### R-4: Add draft-to-publication tightening rules to file 5

**Current gap:** File 5 specifies gate order (§3) but does not articulate the incremental
tightening that happens at publication versus draft. The P-1 through P-10 rules in §7
above should be added as a §4 "Publication-mode additional requirements" section.

---

## 9. Acceptance Test Results (5 checks)

| Check | Result |
|---|---|
| 1. Health-effect leakage in files 5/6/2 | PASS — zero disease, toxicity, or medical-advice language found in any of the three files as written |
| 2. Grey-zone descriptors ruled on each | PASS — all 6 descriptors ruled: מעובד (safe+anchor), מתועש (safe+strong anchor), שומן רווי גבוה (safe+number), סוכר גבוה (safe+number), פחמימה ריקה (BANNED, safe replacement defined), חלש תזונתית (safe+dimensions) |
| 3. "דורש אימות" flag sufficiency for DRAFT | PASS — yes, sufficient for draft; one condition (each bundled claim must be individually verified before publication) |
| 4. Publication mode tightening defined | PASS — Rules P-1 through P-10 defined in §7 |
| 5. Additive claims: formulation-signal rule checked across files 5/6/2 | PASS — all three files hold to the formulation-signal frame; data-path gap identified and addressed in Recommendations R-1 and R-2 |

**5 return buckets populated:**
- Bucket 1 (Approved): 24 phrases/constructions
- Bucket 2 (Product-data verification required): 14 phrase types
- Bucket 3 (Scientific-source review required): 5 phrase/claim types
- Bucket 4 (Banned or replacement): 13 banned phrases with replacements
- Bucket 5 (Publication-safe wording rules): Rules P-1 through P-10 (10 rules)

---

*End of review. Proposed status: RETURNED.*
