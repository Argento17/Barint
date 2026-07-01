# 10 — Translationese Taxonomy (Tom / Bari Hebrew) · v0.1

**Status: v0.1 — Phase 0 baseline of Project Tom's Voice (TASK-374).**
Built 2026-06-22 from **12 owner-labeled live examples** (cereals + chocolate-tablet
shelves) + **2 owner rewrites that "really work"** (protein bars). This is the
catalogue of *naturalness* failures — Hebrew that is grammatically clean,
leakage-clean, and passes every existing gate, but still reads translated/stilted.

**Why this file exists:** none of the failures below trip any current gate
(`5_banned_phrases_and_claims.md`, the 4 NLP gates, or the 8 hard-fails in
`7_voice_match_gate.md`). They are exactly the gap the Naturalness Gate (Phase 1)
must catch. This taxonomy is the gate's calibration target.

> Transcription note: Hebrew read from owner screenshots. Owner-quoted phrases are
> verified; fuller line transcriptions are best-read and may carry minor errors —
> confirm against the source JSON before promoting any pair to `3_before_after_pairs.md`.

---

## The meta-finding (owner, 2026-06-22)
**The closer / "finish line" is the systematic failure zone.** Across the cereals
shelf the body copy is acceptable but the closing beat (`הקשר במדף`) reliably
collapses into T1/T3 calques. The Naturalness Gate must weight the final beat
hardest, and the fingerprint's closer guidance needs repair.

---

## The tells

### T1 — The "X, לא Y" contrastive — the #1 tell
A direct calque of English "it's X, not Y." Owner flags it repeatedly and deletes
it on sight in his own rewrites.

| # | Failing | Owner fix / natural form |
|---|---|---|
| #27 | `ממתק ממולא בטעם נוגט-דבש, לא טבלת קקאו` | `מדובר בסך הכל בממתק נוגט דבש` |
| #3 | `הפסד בגלל הממתיק, לא בגלל הבסיס` | (recast; drop the contrast — see T7 `הפסד`) |
| #5 | `זו התמונה הכוללת — לא רכיב אחד` | (referent unclear; recast as a positive declarative) |
| protein | `המתיקות באה ממזון שלם ולא ממלטיטול` | `המתיקות אינה מגיעה ממלטיטול` |
| protein | `זה הטוב במדף מהונדס, לא מזון חזק` | **deleted entirely** |

**Rule:** resolve a contrast with `מדובר בסך הכל ב…`, `עדיין`, or a plain positive —
never the bare `X, לא Y` parallel. Owner deletes the X-not-Y closer every time.

### T2 — "X לא תמיד אומר Y" — a calque currently blessed as a signature move
`נקי לא תמיד אומר חזק` (#2). Calque of "X doesn't always mean Y." **This sits in
`2_voice_fingerprint.md` §3 and `4_approved_phrases.md` §C as a workhorse move** —
owner's flag means a blessed move is itself translationese. Pending owner ruling:
retire or repair (natural: `מוצר נקי הוא לא בהכרח מוצר חזק`).

### T3 — Dangling `גם` / staccato fragment finish
`הפקאן שם. הסוכר גם` (#1), `כאן הוא גם לא הסיפור` (#4). Ending on `גם` mimics
English trailing "…too." — flat/incomplete in Hebrew. Primary driver of the weak
closer meta-finding.

### T4 — Calqued metaphors
`המחיר שלו ברור` (#6 — reads as literal price), `נושאים את החלבון` (protein original
→ owner: `החלבון... מקורו מ…`), `עוצרים אותו בציון D` (#2), `נתרן נמוך מאוד לזכותו`
(#10, "to its credit"). Hebrew does not carry these English figures naturally.

### T5 — Passive nominalization
`הבחירה שנעשתה היא להוסיף` (#6, "the choice that was made is to add" → `בחרו להוסיף`),
`סוכר שמוסף` (#3 → `סוכר מוסף`). The hallmark LLM-Hebrew register.

### T6 — Untranslated English loanword
`מילק` (#9) → `שוקולד חלב`.

### T7 — Wrong-register single words / compressions
`הפסד` (#3, sports/gambling register), `סיבים יפים` (protein original → `עשיר בסיבים`),
`דבש בשם, 4% דבש בפועל` (#4, calqued "honey in name, X in practice" compression).

---

## T8–T14 — the contrastive-closer SIBLING family (milk shelf, 2026-06-25)

**Why this section exists (owner meta-finding, milk run 2026-06-25).** When the
owner rejected the `X, לא Y` closer (T1) and it was removed, the content lane reached
for a *cluster of sibling templates that read equally translated*. Banning T1 alone
made the author swap one calque for the next; the milk page took 5 revisions to
converge. The whole family is captured here so a future author avoids ALL of it up
front and a shelf converges fast. Each tell below is HIGH-weight at the **closer**.

### T8 — The "מה שמושיב אותו ... בראש/בתחתית המדף" seating calque
A direct calque of English "what *seats* it at the top/bottom of the ranking." The
verb `מושיב/מושיבה/להושיב` applied to a ranking position is not natural Hebrew — it
literally says "sits it down" on the shelf.

| Failing | Natural form |
|---|---|
| `מה שמושיב אותו בראש המדף` | explain the ranking plainly (`מה שמציב אותו בין הטובים במדף` only if a verb is needed — usually let the number imply it: `הרשימה הקצרה והשומן הטבעי הם הסיבה שהוא מוביל`) |
| `זה מה שמושיבה אותה בתחתית` | name the actual driver: `אחוז השקדים הנמוך הוא מה שמוריד אותה` / drop the seating verb entirely |

**Rule:** never use a "seating/placing" verb as the ranking metaphor. Explain the
rank by naming the driver, or let the number imply the position.

### T9 — "הצמרת הנקייה" / "צמרת נקייה" — the clean-cream compound
`צמרת` (cream/top-tier) + `נקייה` (clean) is not a natural Hebrew collocation — it's
an assembled compound that reads translated. (`צמרת` alone for "top tier" is fine.)

| Failing | Natural form |
|---|---|
| `הצמרת הנקייה של המדף` | `מהטובים במדף` / `מהנקיים במדף` |
| `נמצא בצמרת הנקייה` | `מהמובילים, עם רשימת רכיבים קצרה` (name the *why* of "clean") |

### T10 — Payment / price calque for a trade-off (`במחיר`, `משלמים על זה ב…`, `הם המחיר`, `היא משלמת ב…`)
A calque of the English "at the price of / you pay for it with…" trade-off-as-payment
metaphor. In Hebrew it reads as a literal monetary price (and pulls a raw figure into
a verdict, doubling as an H3-R3 fact-tail).

| Failing | Natural form |
|---|---|
| `חלבון גבוה, במחיר 8 גרם סוכר` | state the trade-off plainly: `חלבון גבוה, אבל גם 8 גרם סוכר` (and only if the number IS the finding) — better: `חזק בחלבון, פחות מרשים בסוכר` |
| `משלמים על זה בנתרן גבוה` | `הנתרן הגבוה הוא הצד השני` / name it as a plain catch |
| `הסוכר הוא המחיר של המרקם` | `המרקם בא עם סוכר גבוה` |

**Rule:** state a trade-off as a plain Hebrew catch, never as a "price you pay."
Don't smuggle a raw figure in via the payment metaphor.

### T11 — The contrastive-closer RHYTHM as shelf-wide monotony (T1 in disguise)
Not just `X, לא Y` but its disguises used as the **terminal beat** of a field across
many products: `X, אבל Y` · `X, אבל לא Y` · `X, פחות Y` · `X רק לא Y` · `X ולא Y`.
**Any single one of these conjunctions can be perfectly fine in isolation** — the
defect is the contrastive-closer *shape* becoming the DEFAULT terminal rhythm
**repeated across a shelf**. It's the same monotony T1 created, wearing a different
conjunction.

**Rule (shelf-level, not line-level):** vary the closer shape across the shelf —
close some on a **number**, some on a **use-case**, some on a **plain declarative**,
some on a **dry aside**, some on **who-it's-for**. If more than ~⅓ of a shelf's
closers are "positive-then-contrastive-catch," that is the tell, regardless of which
conjunction is used. (See carve-outs below — `אבל` resolving into a full clause is
fine; the ban is on the repeated terminal *shape*.)

### T12 — "נקי ונעים" / "נעים" as a positive verdict (F2 empty-positive)
`נעים` ("pleasant") says nothing actionable — it's the calm-trap / F2 neutral-bland
failure wearing a positive coat. `נקי ונעים` is the canonical empty pairing.

| Failing | Natural form |
|---|---|
| `מוצר נקי ונעים` | a concrete, product-specific positive: `רשימת רכיבים קצרה: חלב בלבד` / `שומן טבעי 4%, בלי תוספות` |
| `טעם נעים, מוצר נעים` | name what's actually good in the data, not a mood word |

### T13 — Passive nominalization at the closer (T5 sibling, LLM-Hebrew passive)
The T5 register specifically as it lands a closer: `הציפייה ... מושארת בחוץ`
("the expectation … is left outside"). Passive + nominalized expectation is pure
LLM-Hebrew.

| Failing | Natural form |
|---|---|
| `הציפייה לחלבון מושארת בחוץ` | active, plain: `כל עוד לא מצפים ממנו לחלבון` |
| `הבחירה שנעשתה מותירה את הסיבים בחוץ` | `בחרו לוותר על הסיבים` / `סיבים אין כאן` |

### T14 — Boilerplate `limitingFactors` pasted verbatim across products (+ factual hazard)
The same limiter string copy-pasted across many products' `limitingFactors` is a
translationese/automation tell — and a **factual hazard**: on the milk shelf a generic
"low protein / low fiber" limiter landed on the *top-scoring* products where it is
**false**.

**Rule:** `limitingFactors` must be **product-specific and factually true for THAT
product**. A limiter that does not apply to a given product (e.g. "low protein" on a
high-protein product) is a fabrication, not just a style tell — remove it. Verify each
limiter against that product's own scrape before it ships.

---

## CARVE-OUTS — legitimate Hebrew that must NOT be flagged (milk run, 2026-06-25)

The gate and future authors must **not over-correct into mush.** These read natural
and are explicitly preserved — distinguish the bare contrastive **closer** (banned,
T1/T11) from these (allowed):

1. **`לא X ולא Y`** (neither/nor) — legitimate, idiomatic Hebrew. Not a tell.
   ("לא חזק ולא חלש במיוחד" is fine.)
2. **A single in-prose `אבל`** that **resolves into a full clause** — fine. The ban
   (T11) is on the repeated terminal *shape* across a shelf, never on one connective
   `אבל` inside flowing prose.
3. **`לא X אלא Y`** (not X but rather Y) **naming the positive alternative** — this is
   the **APPROVED repair form**, not a tell. ("לא חטיף אלא מנת ביניים אמיתית.")

> ⚠️ The discriminator is the **bare contrastive CLOSER as a shelf-wide default**
> (banned) vs. **a resolved clause / neither-nor / not-X-but-Y naming a positive**
> (allowed). When in doubt, a closer that *adds a positive alternative or a full
> resolving clause* is fine; a closer that *only negates* and does so across the
> whole shelf is the tell.

---

## What "good" looks like (owner-validated calibration)

**#1 chocolate (kept as good):**
> `זה הצד הכי קרוב-לקפאה שיש כאן על המדף. … הקאץ' הוא הטעם: 90% מריר זה לא לכל חך, וזה עדיין מוצר עתיר שומן וקלוריות.`

Why it works: connected clauses (not staccato), a colloquial anchor (`הקאץ'`),
numbers integrated into sentences, contrast resolved with `עדיין` not X-not-Y.

**Protein-bar rewrite (owner):** plain sourcing (`החלבון במוצר מקורו מאגוזי לוז ושקדים`),
glossed jargon (`גליצרול (חומר משמר וממתיק)`), discourse connectors (`כלומר`, `וכן`),
X-not-Y deletions, weak closer deleted.

---

## RESOLVED (owner, 2026-06-22)
1. **Structure signal — RESOLVED: editing shorthand, keep prose.** The owner's
   יתרון/חיסרון labels in the protein rewrites were quick-edit shorthand, not a
   format direction. Final copy stays flowing prose (the #1-chocolate model). No
   frontend/design change. The *value* in the rewrites is the phrasing (T1/T4/T7
   deletions, jargon gloss, discourse connectors) — not the layout.
2. **T2 signature move — RESOLVED: repair the phrasing.** `X לא תמיד אומר Y` is
   repaired to **`X הוא לא בהכרח Y`** (e.g. `מוצר נקי הוא לא בהכרח מוצר חזק`).
   Applied to `2_voice_fingerprint.md` §2/§3 and `4_approved_phrases.md` §C
   (2026-06-22); logged in `8_edit_feedback_log.md`.

---

## Promotion path
Once transcriptions are confirmed: promote verified pairs into
`3_before_after_pairs.md`, add T1–T7 as a syntax sub-blacklist in
`5_banned_phrases_and_claims.md` (Phase 2), and encode T1–T7 + the closer
meta-finding as the Naturalness Gate's scoring rubric (Phase 1).
