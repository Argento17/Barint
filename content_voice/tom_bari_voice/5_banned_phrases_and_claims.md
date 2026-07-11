# 5 — Banned Phrases & Claim Control (Tom / Bari Hebrew)

Two firewalls in one file:
1. **Phrase bans** — language that breaks Bari's non-shaming, non-prescribing voice.
2. **Claim control** — the rule that *no factual nutrition/health claim ships
   without a verifiable source, and the risky ones need Nutrition Agent sign-off.*

This file is a **hard gate**, not a style preference. A draft that violates it does
not ship.

---

## 1. Banned / risky phrases (avoid unless explicitly approved)

| Banned | Why | Use instead |
|---|---|---|
| רעל / מוצר רעיל / תחליף כימי / מלא כימיקלים | fear language, fabrication | רשימת רכיבים ארוכה ותוספי מזון רבים |
| מסוכן | unsupported scare | דורש תשומת לב |
| גורם לסרטן / קשור לסרטן | health claim — needs exact approved wording | דורש בדיקת ראיות לפני טענה כזו *(and escalate)* |
| הורס את הבריאות / לא ראוי למאכל | moral + scare | (reframe as image-vs-contents gap) |
| מזעזע / זבל | shaming, editorializing | פער גדול בין הדימוי לבין הרכב המוצר |
| אסור לאכול / להימנע | prescribing what to eat | כדאי לדעת מה קונים |
| בריא *(blanket)* | unprovable blanket claim | name the specific strength (סיבים גבוהים, רשימה קצרה) |
| לא בריא *(blanket)* | unprovable blanket claim | חלש תזונתית / מוגבל תזונתית |
| מומלץ / לא מומלץ *(without for-whom-and-why)* | Bari describes, never prescribes | "מתאים כ… / פחות מתאים כ…" + the reason |
| תוספי תזונה *(meaning additives)* | wrong term (means supplements) | תוספי מזון |
| ALL CAPS, raw score mechanics ("68.2", "72/B"), framework terms (NOVA, cap, floor, BSIP, dimension, pillar…) | leakage | — (rewrite) |
| פחמימה ריקה | implies metabolic verdict; not panel-readable; sounds like a health claim in consumer Hebrew | בעיקר פחמימה קלה + fiber/protein figures from scrape |
| **null** (the word "null"), field-path tokens (d4_additives, expansion.X, _wholeGrainClaim, backtick-wrapped paths), JSON/code identifiers of any kind | Harvest #2 ruling #1 — code language in consumer copy is a credibility collapse and a structural leakage failure | When data is absent: "לא צוין על האריזה" / "רשימת הרכיבים המלאה לא נקראה מהאריזה". Never state "null"; never expose a field name. |
| שורת בארי (as a section heading or structural closer label) | Harvest #2 ruling #2 — retired from the spine; הקשר במדף is the closing beat | Replace with הקשר במדף section |
| **"<מותג>? תחשוב שוב" / "תחשבו שוב" / any mocking or attacking of a brand by name** | Harvest #3 rule 1 — brand-directed dismissive rhetoric is banned; Bari critiques composition, never brand character. (Owner's example: "שוגי? תחשוב שוב" — "very negatively towards a brand, not where Bari wants to be.") | Critique the formulation directly: "קמח תירס מעובד בראש הרשימה ומליחות גבוהה — זה מה שיש כאן." (An ingredient proportion like "82% קמח תירס" stays legal; a panel figure like "435 מיליגרם נתרן" does not — §1.6 R1.) |
| **Bare juxtaposition of facts without the finding ("הוויטמינים הוספו; הסיבים — לא" standing alone)** | Harvest #3 rule 2 — information-dumping: facts side-by-side without the "so what" are not a verdict, they are data. Every line must carry the insight, not raw data. | Frame the finding: "הוויטמינים הוספו מבחוץ; הדגן המלא שיספק סיבים — לא נמצא כאן." |
| **Trailing nutrition-fact tails in insightLine / rowVerdict ("נתרן: 110 מיליגרם ל-100 גרם" / "סוכר: 22.4 גרם ל-100 גרם" appended to verdicts)** | Harvest #3 rule 3 — raw per-100g numbers recited at the end of a verdict are not insight, they are the nutrition section. A number appears in a verdict ONLY when it IS the finding (framed), never as a trailing data tail. Owner: "Why do we have still nutritional facts in the product description? we dont need that." | SUPERSEDED 2026-07-10 (§1.6 R1): nutrition figures never appear in consumer prose at all — not even framed as the finding. Describe the read in plain absolute words ("מלוח מאוד", "עשיר בסוכר"). Never append "נתרן: X, סוכר: Y" as a data tail. |
| **Technical additive dump in rowVerdict / insightLine (E-numbers, chemical names: "E471", "מונו- ודיגליצרידים של חומצות שומן", long additive laundry lists)** | Harvest #4 H4-3 — additive generalization: verdict prose is not the additive panel. Dumping codes or chemical names into the verdict is information noise and duplicates the sub-dropdown. | Generalize: "תוספי מזון" or "מספר תוספי מזון ברשימה". For contested-tier additives: "שחלקם שנויים במחלוקת". Per-additive names, codes, and tier detail live **only** in the additive sub-dropdown — never in insightLine / rowVerdict / comparisonContext. |
| **Verbal grade recitation ("נשאר ב-A", "עוצר ב-B כי…", "יורד ב-D", "B הוא הציון שההרכב מרוויח")** | TASK-533 round 2 / C3 ruling 2026-07-08 — the score chip (72/B) already renders the grade beside the text; a verdict that also states the letter is the UI captioning itself, and "X. עוצר ב-[grade] כי Y" is itself a template skeleton every product falls into. Full reversal of the 2026-06-02 grade-rationale rule — see `row_description_standard_v1.md` §2a. | State the food fact only; let the badge carry the grade. Naming the letter is banned, and since 2026-07-10 relative-standing claims ("מהבולטים בקטגוריה") are banned too (§1.6 R2). |
| **Score-mechanism narration in plain Hebrew ("הציון נשאר ב-A כי רשימת הרכיבים מבוססת על טקסט העמוד בלבד, ולכן רמת העיבוד אינה מאומתת", "לא ניתן לאמת את רמת העיבוד מהנתונים הזמינים")** | TASK-533 round 2 / C3 ruling (Principle A), 2026-07-08 — describing Bari's own confidence tier / extraction method / processing-classification mechanism is the algorithm narrating itself, even with zero Tier-4 vocabulary. Same failure class as raw score mechanics, just translated into words. | Describe the product in food language and stop: "יוגורט נקי ופשוט." A missing fact is stated as "לא צוין על האריזה" — never a sentence about Bari's own reading/verification. (The old suggested repair "בלי צילום תווית מלא…" is itself REVOKED — "צילום תווית" is hard-banned per the 2026-07-08 owner ruling, and narrating an ingredient COUNT is banned per H4-P2.) |

### Constructive-recommendation carve-out (Harvest #1, E009 — owner ruling 2026-06-19)

The blanket "מומלץ/להימנע" ban has ONE explicitly approved exception:
**Constructive-alternative recommendations** are permitted when the copy meets ALL THREE conditions:
1. Explicit non-prescriptive disclaimer first: "אנחנו לא אומרים ולעולם לא נאמר לכם מה לאכול."
2. Bounded if-clause: "אבל אם אתם בוחרים ב-X — Y עדיף / שווה לנסות."
3. A **constructive alternative** (not "don't eat X" but "try Y instead / try making it at home").

This carve-out does **not** permit: medical or dietary-restriction advice, health-effect claims, prescriptive "אסור/אל תאכלו/להימנע" language, or recommendations for specific subgroups (children, diabetics, etc.) without Nutrition Agent sign-off.

**Tone safety valve:** any line *intended* as dry wit / light criticism must pass
the HebEMO anger + disgust gate (`LABEL_0` on both) before shipping
(`content-agent.md`). Aggression reads as shaming and fails the voice.

---

## 1.5 Translationese syntax sub-blacklist (T1–T7) — TASK-374

These are **structural / syntactic** tells, not vocabulary. They are the defect no
earlier firewall caught: grammatical, leakage-clean Hebrew that still reads
*translated*. This is the human-facing mirror of the deterministic gate
`integrations/clients/naturalness_gate.py` and the taxonomy
`10_translationese_taxonomy.md`. A draft that trips a **HIGH** tell does not ship.

| # | Tell (banned) | Why | Natural form |
|---|---|---|---|
| **T1** | The `X, לא Y` contrastive **closer** ("…מבודדים, לא מזון שלם", "…תוצאה של מעבדה, לא של מזון") — comma/dash + `לא` + short phrase ending the line | #1 calque ("it's X, not Y"); was 18/90 of the live protein-bars copy | Resolve in flowing prose, or land on `מדובר בסך הכל ב…` / `עדיין`. An *earned* bare fragment ("לייט זה לא.") is fine; the comma-contrastive closer is not. |
| **T2** | `X לא תמיד אומר Y` (calque "doesn't always mean") | retired calque; owner flagged "נקי לא תמיד אומר חזק" | `X הוא לא בהכרח Y` ("מוצר נקי הוא לא בהכרח מוצר חזק"). `זה לא אומר Y` variant on watch. |
| **T3** | Dangling `גם` ending a sentence ("הסוכר גם.") | calque of trailing "…too." | Full clause. (`גם` mid-sentence is fine: "יש בו גם דבש".) |
| **T4** | Calqued metaphors ("המחיר שלו ברור", "נושא את החלבון", "לזכותו", "עוצר אותו בציון") | English figures that don't carry in Hebrew | Plain Hebrew ("מקורו מ…", "בזכות…"). |
| **T5** | Passive nominalization ("הבחירה שנעשתה היא להוסיף", "סוכר שמוסף") | LLM-Hebrew register | Active verb ("בחרו להוסיף", "סוכר מוסף"). |
| **T6** | Untranslated English loanword ("מילק") | breaks the Hebrew register | The Hebrew term ("שוקולד חלב"). |
| **T7** | Wrong-register word / compression ("הפסד" for a food tradeoff, "סיבים יפים", "דבש בשם, X%") | register mismatch / calqued compression | Correct-register word ("עשיר בסיבים"); state it in full. |

**T8–T14 — the contrastive-closer SIBLING family (milk shelf, 2026-06-25).** When the
owner rejected the T1 `X, לא Y` closer, the lane swapped in these siblings — each reads
equally translated. Banning T1 alone made the author cycle through the rest, costing 5
revisions. Avoid the whole family up front. (Full repair examples: `10_translationese_taxonomy.md` §T8–T14.)

| # | Tell (banned) | Why | Natural form |
|---|---|---|---|
| **T8** | "מה שמושיב אותו / מושיבה ... בראש/בתחתית/מעל/מתחת המדף" — the *seating* verb for a ranking position | calque of "what seats it at the top of the ranking"; `מושיב` ("sits it down") is not a natural ranking metaphor | Explain the rank by naming the driver, or let the number imply position ("הרשימה הקצרה היא הסיבה שהוא מוביל"). |
| **T9** | "הצמרת הנקייה" / "צמרת נקייה" — the clean-cream compound | assembled "clean-cream" compound; not a natural Hebrew collocation | "מהטובים במדף" / "מהנקיים במדף" (name the *why* of clean). |
| **T10** | Payment/price calque for a trade-off: "במחיר X", "משלמים על זה ב…", "הם המחיר", "היא משלמת ב…" | calqued "at the price of…" trade-off-as-payment; also smuggles a raw figure into a verdict (doubles as H3-R3 fact-tail) | State the trade-off as a plain catch ("חזק בחלבון, פחות מרשים בסוכר") — without the price figure. |
| **T11** | The contrastive-closer **RHYTHM** as shelf-wide monotony — T1's disguises as the *terminal beat* across many products: "X, אבל Y", "X, אבל לא Y", "X, פחות Y", "X רק לא Y", "X ולא Y" | a single conjunction is fine; the BAN is on the contrastive-catch *shape* being the DEFAULT closer repeated across a shelf (same monotony as T1) | **Shelf-level rule:** vary closer shapes — close on a number / a use-case / a plain declarative / a dry aside / who-it's-for. >~⅓ of a shelf closing "positive-then-catch" = the tell. |
| **T12** | "נקי ונעים" / "נעים" as a positive verdict | empty-positive (F2 calm-trap); "pleasant" says nothing actionable | A concrete, product-specific positive grounded in the data ("רשימת רכיבים קצרה: חלב בלבד"). |
| **T13** | Passive nominalization at the closer ("הציפייה ... מושארת בחוץ") | LLM-Hebrew passive register (T5 sibling) landing the final beat | Active, plain phrasing ("כל עוד לא מצפים ממנו לחלבון"). |
| **T14** | Boilerplate `limitingFactors` pasted verbatim across products | automation/translationese tell **+ factual hazard** — a generic "low protein/fiber" limiter landed on top-scoring products where it is **false** | `limitingFactors` must be **product-specific and factually true for THAT product**; an inapplicable limiter is a fabrication — remove it. Verify each vs the product's own scrape. |

**CARVE-OUTS — REVISED 2026-07-10 (owner overhaul; supersedes the milk-run 2026-06-25
carve-outs).** The gate and authors must not over-correct into mush, but two of the
old carve-outs are DEAD — the define-by-negation ban is now ZERO-EXCEPTION and
mechanically enforced (`copy_rules.ANTITHESIS_RE`: `,לא` / `ולא` / `אלא` anywhere):
- ~~`לא X ולא Y` (neither/nor)~~ — **REMOVED.** `ולא` hard-fires the gate wherever it
  appears. Restate positively, or split into two sentences.
- **A single in-prose `אבל`** that **resolves into a full clause** — still fine; T11 bans
  only the repeated terminal *shape* across a shelf, never one connective `אבל`.
- ~~`לא X אלא Y` naming the positive alternative~~ — **REMOVED** (owner ruling
  2026-07-10, zero exception; this exact carve-out caused 11/20 content_agent_v1 pilot
  products to fail the hard gate). `אלא` never appears in consumer copy. The repair is
  to state the positive directly, with no negation at all.
- "במקום Y" (instead-of) is the SAME banned family (`bimkom_define_by_negation_fires`);
  only the innocent spatial sense ("במקום אחד") passes.

**Two failure modes (owner ruling, file 8 H5-R3):** T1–T7 are the **F1
translationese-punch** axis. The opposite failure is **F2 neutral-bland** — no
verdict, hedge-only, "says nothing." Both are banned: the target is *opinionated
substance in natural connected Hebrew* (file 2 §0.5). `(!)` is seasoning used
sparingly and only when earned — more than once on a shelf is overuse.

> ⚠️ Calibration guards (do NOT over-flag): `אשר` is natural Hebrew, not a tell; an
> earned short-fragment closer is allowed; the ONE surviving carve-out (a single
> resolving in-prose `אבל`) is explicitly allowed — T11 is a **shelf-level monotony**
> check, not a line-level `אבל` ban. Only the patterns above fire.

---

## 1.6 Owner copy-law overhaul — 2026-07-10 rulings (HARD; supersede any contrary guidance elsewhere in this file)

Encoded for every consumer-copy author, including the `content_agent_v1` wired brief
(TASK-550 M2 voice fold). Each rule is mechanically gated where noted — a fire fails
the page, not just the review.

| # | Rule | Gate |
|---|---|---|
| **R1** | **No cited nutrition values in prose.** No grams / מ"ג / מיליגרם / קלוריות / קק"ל / nutrient-percent anywhere in consumer prose ("26 גרם", "660 מ\"ג", "32% שומן" — all dead). Translate the panel into PLAIN ABSOLUTE WORDS — "חלבון גבוה", "מלוח", "רזה", "עשיר בשומן"; naming the read in words is REQUIRED, only the figure is banned. Ingredient PROPORTIONS stay allowed ("40% טחינה", "95% חיטה", "69% חומוס") — they describe what the food is made of, not its panel. | `copy_rules.nutrition_value_citation_hard_fires` (HARD) |
| **R2** | **No corpus-relative rank / superlative / median findings in consumer prose.** "הכי", "ה… ביותר", "מהבולטים במדף", "נדיר במדף", "מוביל את המדף", "מעל/מתחת לחציון", what-it-beats framing — all dead. Describe the product ON ITS OWN TERMS: salty / rich / lean / clean. Retires the prose use of `superlatives_allowed` (the engine's RT-1 gate now expects ZERO superlatives). Internal scoring and QA rank checks are unaffected. | engine RT-1 + red-team |
| **R3** | **The anchor voice.** Owner calibration line: "גאודה הולנדית קלאסית, עשירה ומלוחה. היא מכילה חלבון גבוה אך גם שומן גבוה. מדובר במוצר יחסית נקי אבל יש לשים לב לכמות הנצרכת." Three beats: (1) identity + sensory/textural character → (2) nutritional read in plain absolute words → (3) practical takeaway. Short. Native. Own terms. | voice-match / naturalness judge |
| **R4** | **Define-by-negation: zero exception.** "X, לא Y", `ולא`, `אלא`, and "במקום Y" (instead-of) are banned with NO carve-out — the old "לא X אלא Y naming a positive" approval is REVOKED (it caused 11/20 pilot failures). Restate positively or split sentences. | `antithesis_hard_fires` + `bimkom_define_by_negation_fires` (HARD) |
| **R5** | **Cleanliness claims require the full additive picture.** Never "בלי תוספות נוספות" / "רשימה נקייה" while the list carries acidity regulators, stabilizers, emulsifiers, or seasoning blends beyond the base — counting only the preservative is a false claim (hummus RT-1 class). Generalized additive naming per H4-3 still applies. | red-team |
| **R6** | **No templated nutrient tail across products.** The same qualitative nutrient clause may not close more than a handful (working bar: 5) of products' lines on one shelf ("חלבון ונתרן סבירים" ×12 — the hummus RT-2 defect). Every line's closing read is specific to THAT product. | validate_copy_authored CHECK 2/4 + red-team |

---

## 2. Claim control — the firewall (mandatory)

**Principle (project-wide):** *"Unknown is acceptable; fabrication is not."* The
voice never invents, rounds, estimates, or "rounds out" a missing value. A
partially-known product is written partially; a missing field stays
"data could not be retrieved." (Mirrors `content-agent.md` Hard Rule 5, the OFF ban,
and `missing_data_discard_rule`.)

### Two tiers of factual content
**Tier A — verifiable from the product's own scraped data → may state directly,
with the source implied by the data:**
- ingredient-list length / presence of named additives that appear on the label
- sugar / saturated fat / fiber / protein per 100g *as parsed from the product* — the panel GROUNDS a plain-words read; since 2026-07-10 the figure itself never appears in consumer prose (§1.6 R1)
- "no added sugar" / "gluten-free" *if it's on the label*
- the Bari score/grade *as displayed* (never the raw mechanic)

**Tier B — needs Nutrition Agent sign-off BEFORE publication (escalate, don't write
around it):**
- any health *effect* or risk ("linked to…", "raises…", "harms…")
- any comparative health verdict beyond the displayed score
- any claim about who *should* / *should not* consume it (medical/dietary)
- any number not present in the scraped data (→ usually: don't state it at all)
- any cross-market / label-gap claim (D5 annotate-only territory)
- any additive risk-tier annotation, EFSA evaluation pointer, OPENFDA adverse-event reference, or disease-association note sourced from the engine's additive-burden data (EV-003/EV-019). These inform the Bari score; they are never consumer copy. Frame additives as whole-picture counts (class + count from ingredient list) only.

### The flag format (use in every draft)
Append to any review that contains a Tier-A fact that still needs verification, or
any Tier-B claim:

> **דורש אימות לפני פרסום:** <the exact fact/claim>, מקור: <product scrape field / "pending Nutrition">.

A draft with an unflagged Tier-B claim = automatic CHANGES_REQUESTED.

### Citations discipline
Every evidence/nutrition/consumer claim names its source inline (the product
scrape field, or an approved doc/URL). Vague provenance ("מקור מזון רשמי",
"מחקרים מראים") is banned (cf. `citations_discipline`). Israeli food blogs (S6) are
**register calibration only** — never a citable source for a fact.

---

## 3. Gate order (run before any handoff)
1. **Claim scan** — every factual sentence is Tier-A-verifiable or carries a "דורש אימות" flag. Tier-B → escalate to Nutrition.
2. **Phrase scan** — no banned phrase (§1); run `hebrew_readability.is_clean` (must be true).
3. **Tone scan** — any witty/critical line passes HebEMO anger+disgust.
4. **Form scan** — run hero/prologue/insight lines through DICTA Nakdan; garbled word = rewrite.
5. **Grammar/agreement scan** — run `hebrew_grammar_gate.analyze(text).is_clean` (must be true); gender/number agreement failure = not-done. High-confidence flags may be auto-fixed via `hebrew_grammar_autofix.auto_fix(text)`; medium-confidence flags require human review.
5.6. **Naturalness pre-filter (T1–T7, §1.5)** — run `naturalness_gate.analyze(text).is_clean` (must be true); any HIGH translationese tell = not-done. MEDIUM flags + `f2_signal` route to the independent judge (step 7).
6. **Voice-match gate** — `7_voice_match_gate.md`.
7. **Naturalness judge (two-axis, independent lane)** — `11_naturalness_gate.md`: F1 ≥ 4 AND F2 ≥ 4. Run by a lane that did NOT author the copy (Adversarial QA Track C). The author cannot self-clear it.

Fail any → not done.

---

## 4 — Publication-mode additional requirements

These rules govern the path from DRAFT to PUBLICATION. They are incremental to the gate order above — a review must first clear §3, then meet these requirements before handoff.

### P-1: All flagged claims must be resolved before publication

Every "דורש אימות לפני פרסום" flag must be closed individually. For each flagged item:
- Verify the figure from the product scrape → replace the flag with the verified figure and cite the source field; OR
- Confirm the data is absent → remove the claim entirely (never estimate, round, or fill from any external source including OFF).

A review with any surviving "דורש אימות" flag does not ship in publication mode.

### P-2: Compositional claims are per-100g-grounded — expression superseded 2026-07-10

The VERIFICATION basis is unchanged: every compositional read must be grounded in the product's own scraped per-100g panel. The EXPRESSION rule changed (§1.6 R1): the figure itself no longer appears in consumer prose — the panel grounds a plain-words read ("עשיר בסוכר", "מלוח"), and the numbers live only in the structured UI fields (nutrition table, chips).

### P-3: "מתועש" and "מעובד" require a structural anchor in the same paragraph

If a review calls a product "מעובד" or "מתועש", the same paragraph (or the immediately prior sentence) must name the structural evidence: ingredient-list length and/or additive class presence from the scrape. Applied without anchor, these descriptors become unsupported verdicts.

### P-4: Additive mentions are whole-picture counts, never E-number disease annotations

In publication copy, additives appear as additive class and count only ("מספר מתחלבים ומייצבים" / "שלושה חומרים משמרים ברשימת הרכיבים"). No E-numbers surfaced to the consumer. No EFSA risk-tier annotations, disease associations, or OPENFDA adverse-event data surfaced to the consumer. The engine's additive-burden risk scoring informs the Bari score; it does not become copy.

**Additive generalization in verdict prose (Harvest #4, H4-3):** `insightLine`, `rowVerdict`, and `comparisonContext` never dump technical additive names, E-numbers, or long additive laundry lists. Generalize to "תוספי מזון" (or class + count). When contested-tier additives are material to the finding, surface as "שחלקם שנויים במחלוקת" — not as a named chemical roster. Per-additive detail (name, code, tier) lives **only** in the additive sub-dropdown UI; the verdict carries the formulation finding, not the additive encyclopedia.

### P-5: No disease or toxicity language at any severity level

"קשר לסרטן", "מסרטן", "גורם לנזק", "הורס את הבריאות" and all equivalent phrases are banned regardless of how hedged or sourced. Bari describes nutritional architecture and formulation quality. It does not publish health-effect verdicts, even peer-reviewed ones, in consumer copy. Route any legitimate scientific finding about an ingredient through the EV-### evidence registry; it informs scoring, not copy.

### P-6: Blanket health descriptors are banned; specificity is required

"בריא" and "לא בריא" may not appear as blanket verdicts.
- Instead of "בריא": name the specific strength. "סיבים גבוהים, רשימת רכיבים קצרה, סוכר נמוך."
- Instead of "לא בריא": "חלש תזונתית" with named dimensions.

### P-7: Mode must be earned by the real product profile

Publication reviews must use the mode (Critical / Balanced / Positive) warranted by the actual BSIP2 score and trace. A product that scores B cannot be written in Critical mode. A product that scores E cannot be written in Positive mode. Mode assignment is derived from the engine output, not an editorial choice.

### P-8: Hypothetical products are replaced with real scrape data

Any "מוצר היפותטי" placeholder must be replaced with a real product and a real scrape before publication. The hypothetical frame is a development tool, not a publishable review state.

### P-9: Tier-B claims require written Nutrition Agent sign-off

Any claim about who should or should not consume a product, any health-effect claim, or any claim about ingredient-level risk (beyond whole-picture formulation framing) requires explicit written Nutrition Agent approval before publication. The approval must be traceable — either to an EV-### evidence registry entry or to a dated written ruling.

### P-10: The HebEMO anger+disgust gate is mandatory before publication

Any line intended as dry wit or criticism must pass the HebEMO anger + disgust gate (`LABEL_0` on both) before the review ships. This is the final tonal safety check before publication (see also §3 Gate 3 above).


<!-- Appended 2026-07-04 from the owner naturalness-labeling session (TASK-506) -->

### Banned / correct-me (for 5_banned_phrases_and_claims.md)
- **סודיום / סודים** — never; the Hebrew term for sodium is **נתרן**. (Now a HARD fail in hebrew_readability.)
- **ברי** as the brand name — the brand is spelled **בארי**. ('ברי' as the ordinary word, and goji berry, are fine.) (HARD fail when used as brand-subject.)
- **Restating the nutrition numbers** already shown in the values/table inside the prose (e.g. repeating '10.1 גרם חלבון', '31%'). Say what they mean, don't re-list them. **UPGRADED to HARD rule 2026-07-08 (TASK-533, owner ruling):** when the number duplicates a value the row UI already displays (protein bar, calorie chip, score chip) with no comparison/rank/gap attached, it is a hard fail, not an advisory flag. See `01_framework/editorial/row_description_standard_v1.md` §5c Rule A and `insight_line_spec_v1.md` Rule 6.
- **Over-using the em-dash (—)** as a structural crutch. Minimize; most can become a comma or a full stop. (Advisory flag.)
- **"X ו-Y הם הגורם המגביל" / any "limiting factor" sentence that names a bare category ("רשימת הרכיבים", "רמת העיבוד") instead of the real finding** — HARD fail 2026-07-08 (TASK-533, owner ruling): broken subject-verb agreement (compound subject vs. singular "הגורם") AND semantically empty even when grammatically fixed. Name the real fired driver from the trace, or state a genuine confidence gap ("לא ניתן לאמת את רמת העיבוד המדויקת מהנתונים הזמינים"). See `01_framework/editorial/row_description_standard_v1.md` §5c Rule B and `insight_line_spec_v1.md` Rule 7.

### H3 rulings (owner review of content_agent_v1, 2026-07-10, TASK-550 — see `8_edit_feedback_log.md` §H3 for full verbatim entries)

- **"קל מבחינה תזונתית" / "קל יחסית מבחינה תזונתית" (and feminine forms)** — HARD BAN (H3-R2). "קל" carries a positive, diet-adjacent connotation in Hebrew while the intended meaning is *nutritionally poor* — inverted valence, and not idiomatic. **Approved replacement construction (owner verbatim, use as the model):** "בתור מקור לארוחת בוקר, אתם לא מקבלים כאן הרבה ערכים תזונתיים." When a product is nutritionally thin, say so directly, in the second person, without euphemism.
- **Rank contradiction: describing the shelf's #1 (or any top-ranked) product's OVERALL profile as "בינוני/נמוך/חלש יחסית למדף"** — HARD BAN (H3-R1). A dimension score being mid (e.g. nutrient_density) does not license a shelf-relative mediocrity claim about the product's overall standing — dimension ≠ rank. "Best ≠ excellent" cuts the other way here: the honest construction names the frame explicitly — "top of *this* shelf, while the shelf itself is unremarkable in absolute terms" — never "מדורג/הפרופיל הכולל בינוני יחסית למדף" for the actual shelf leader. Per-dimension notes in `bariInterpretation` are unaffected (a genuinely mid dimension score is a true, dimension-scoped fact) — the ban is on generalizing it into an overall/shelf-rank claim in `insightLine`/`rowVerdict`/`consumerTakeaway`/`whyRated`/`watchOut`/`context`.
- **THE WORST PATTERN (owner's words, H3-R3): opening with "רשימת הרכיבים..." as the finding, then reciting ≥2 separate nutrition values** — each clause may individually pass the recite-vs-insight heuristic (the numbers do comparison work), yet the whole reads as a spec sheet with connectors, not a verdict. Lead with the FINDING; the ingredient list is evidence, never the opener. If two nutrition values must appear, they serve ONE point, not two consecutive recitations. Resolve contrasts in flowing prose — minimize the em-dash across the WHOLE product's copy (not merely ≤1 per paragraph); prefer zero.
