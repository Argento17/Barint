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

**Tone safety valve:** any line *intended* as dry wit / light criticism must pass
the HebEMO anger + disgust gate (`LABEL_0` on both) before shipping
(`content-agent.md`). Aggression reads as shaming and fails the voice.

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
- sugar / saturated fat / fiber / protein per 100g *as parsed from the product*
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
6. **Voice-match gate** — `7_voice_match_gate.md`.

Fail any → not done.

---

## 4 — Publication-mode additional requirements

These rules govern the path from DRAFT to PUBLICATION. They are incremental to the gate order above — a review must first clear §3, then meet these requirements before handoff.

### P-1: All flagged claims must be resolved before publication

Every "דורש אימות לפני פרסום" flag must be closed individually. For each flagged item:
- Verify the figure from the product scrape → replace the flag with the verified figure and cite the source field; OR
- Confirm the data is absent → remove the claim entirely (never estimate, round, or fill from any external source including OFF).

A review with any surviving "דורש אימות" flag does not ship in publication mode.

### P-2: Every compositional claim must be per-100g and source-cited

Numeric claims (sugar, saturated fat, fiber, protein) must be stated per 100g and attributed to the product's own scraped panel. A parenthetical "(לוח ערכים תזונתיים)" is sufficient attribution, but a raw number with no referent fails the gate.

### P-3: "מתועש" and "מעובד" require a structural anchor in the same paragraph

If a review calls a product "מעובד" or "מתועש", the same paragraph (or the immediately prior sentence) must name the structural evidence: ingredient-list length and/or additive class presence from the scrape. Applied without anchor, these descriptors become unsupported verdicts.

### P-4: Additive mentions are whole-picture counts, never E-number disease annotations

In publication copy, additives appear as additive class and count only ("מספר מתחלבים ומייצבים" / "שלושה חומרים משמרים ברשימת הרכיבים"). No E-numbers surfaced to the consumer. No EFSA risk-tier annotations, disease associations, or OPENFDA adverse-event data surfaced to the consumer. The engine's additive-burden risk scoring informs the Bari score; it does not become copy.

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
