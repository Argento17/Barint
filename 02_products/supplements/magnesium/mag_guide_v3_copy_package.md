# Magnesium Guide v3 — Consumer Copy Package (Gate-1, Content Agent)

**Task:** TASK-577
**Governs:** the v3 readability rebuild of `bari-web/src/lib/guides/magnesium-guide-data.ts`
(the `useV3Layout` block, lines ~794-839 of the file as read for this task, plus new
page-metadata / market-gaps / disclosure fields the v3 restructure needs that do not
exist in the live TS file yet).
**Authored from:** `mag_guide_v3_structure_spec.md` (Nutrition **D6** + Product **D7**
co-signed, sha256 `cc0cc76fc147955b802befbad64ab3a479d152a76d1915d38dfcfb3ea5ab6a84`,
confirmed below) §A (precedence + full 18/18 table), §B (per-card facts), §C
(findings-box support), §D (deletion audit / minimal-survival list); `mag_guide_v2_copy_package.md`
(prior signed gate-1 package, for REUSED-v2 strings); the live TS data file (read in full,
both halves, for every currently-shipped consumer string and the provisional
`V3_GROUP_BY_BARCODE` mapping).
**Status:** GATE-1 DRAFT. Every string below is a proposal pending Adversarial QA
gate-2 and Nutrition + Product final sign-off. Nothing here ships to `bari-web/src/`
from this task — Frontend Agent integrates after gate-2 clears (standing two-gate rule).
**Voice law applied:** `content_voice/tom_bari_voice/` (all 9 files),
`01_framework/editorial/editorial_intelligence_v3.md`,
`01_framework/editorial/insight_line_spec_v1.md`, `assertive_writing_v1.md`.

Every Hebrew string that is a shipping candidate is wrapped in a fenced ```text``` block.
Self-check results (readability/leakage/antithesis + grammar-agreement) are reported per
slot and in the return-contract JSON.

---

## 0 — BLOCKING FLAG: live TS provisional grouping does not match the signed spec

Before any of this copy is wired, the orchestrator/Frontend must fix
`V3_GROUP_BY_BARCODE` in `magnesium-guide-data.ts` (lines 540-559). It currently
implements a **provisional cascade the file's own header comment admits was written
before `mag_guide_v3_structure_spec.md` existed** ("No `mag_guide_v3_structure_spec.md`
existed at build time... Expect this table to be replaced wholesale once Nutrition's
real v3 spec lands"). That real spec now exists and is D6+D7 signed, and its §A.3 table
disagrees with the live provisional mapping on two products:

| Product | Live TS `V3_GROUP_BY_BARCODE` | Signed spec §A.3 | Correct heading |
|---|---|---|---|
| #16 — Tink Oxide-520 | `g4` ("לא ניתן להבין מהתווית") | Heading **3** | "מבוססי אוקסיד" |
| #17 — Amorphicure pH Magnesium | `g4` | Heading **3** | "מבוססי אוקסיד" |

Per §A.2 Tier 1 (a known poor-absorption form is checked before a label-clarity
question), both #16 and #17 have a determinate, known form (oxide / carbonate) and
therefore belong in Heading 3, not Heading 4. Heading 4 is reserved for #18 alone
(the one product where the form itself is also undisclosed). The live file's g3=4/g4=3
split (6+5+**4**+**3**=18) must become g3=6/g4=1 (6+5+**6**+**1**=18) to match the
signed distribution. **The card one-liners in this package (§2, products #16/#17) are
written for their correct Heading-3 membership** — do not wire them under a g4 heading.

---

## 1 — Owner-dictated verbatim strings (fact-checked against the spec, not rewritten)

Per the dispatch: these ship exactly as given. My job is fact-check only. Two flags
raised below; both are for the owner/orchestrator to resolve, not silently patched.

### 1.1 — Intro sentence

```text
בדקנו 18 מוצרים מהמדף הישראלי. שלושה דברים חשובים במיוחד: כמות המגנזיום היסודי, הצורה הכימית ובהירות התווית.
```

**FLAG — HIGH, needs owner decision.** "מהמדף הישראלי" (from the Israeli shelf) is a
market-completeness claim. Nutrition's own v2 spec (§8) explicitly killed this exact
framing, and the v2 copy package's Slot 1 rewrite explicitly removed it for that reason
("Kills 'מהמדף הישראלי' as a market-completeness claim... states... 18 המוצרים שנבדקו").
The v3 structure spec does not re-open §8 — it inherits it unchanged. The owner's
dictated intro sentence reintroduces the exact phrase the standing rule removed. This
may be an intentional owner override (the dispatch says owner-dictated text ships
verbatim on my read), but since it directly contradicts a still-standing D6/D7-signed
rule, I'm flagging it rather than silently shipping past the conflict. Not rewritten.

### 1.2 — "מה גילינו" box (heading + 4 bullets)

```text
מה גילינו
```
```text
מספר גדול על האריזה לא תמיד מייצג את כמות המגנזיום בפועל.
```
```text
ציטראט הוא הצורה עם התמיכה הברורה ביותר מבין המוצרים שבדקנו.
```
```text
מוצרים רבים מבוססים על אוקסיד, שנספג פחות.
```
```text
בחלק מהמוצרים קשה להבין מהתווית כמה מגנזיום באמת מקבלים.
```

**Fact-check, bullet by bullet (spec §C):**
1. "לא תמיד מייצג" (not always the case) — accurately hedged. Spec finding 1 supports
   this for 2/18 products (#6, #8) plus a milder third case (#9). "Not always" is
   consistent with a minority-but-real pattern. No flag.
2. Scoped correctly with "מבין המוצרים שבדקנו" (among the products reviewed). Matches
   finding 2 (citrate = 2/18, the only Bucket-1 form present). No flag.
3. **FLAG — MEDIUM, needs owner decision.** "מוצרים רבים" (many products) describes
   6/18 (33%) — 5 literal oxide + 1 carbonate grouped by chemical-class analogy (spec
   §C finding 3, DEVIATION 3). The spec's own wording-hazard note for this exact
   finding says: *"the findings box gives exact numbers elsewhere... 'many' here
   should likewise be '6 of the 18' or 'a third,' not left vague."* The dictated bullet
   uses the vague framing the spec explicitly flagged as a hazard to avoid. Not
   rewritten (owner-dictated), but surfaced per the fact-check duty.
4. "בחלק מהמוצרים" (in some products) describes 4/18 (22%) — matches finding 4's
   count. Milder than bullet 3's vagueness issue; noting for completeness, not
   blocking.

### 1.3 — Four group headings

```text
ציטראט או ביסגליצינט עם תווית ברורה
```
```text
כמות נמוכה יחסית
```
```text
מבוססי אוקסיד
```
```text
לא ניתן להבין מהתווית
```

Fact-check: matches spec §A.1 exactly, in the dictated order. §A.4 DEVIATION 3 already
resolved the "מבוססי אוקסיד" / carbonate tension at the Product-D7 level (mandatory
card-level disambiguation on #17, not a heading-text edit) — see §2, product #17 below.
No new flag.

### 1.4 — "איך לקרוא תווית מגנזיום" (heading + 3 bullets)

```text
איך לקרוא תווית מגנזיום
```
```text
חפשו "מגנזיום יסודי", לא רק את משקל התרכובת.
```
```text
בדקו את הצורה: ציטראט, ביסגליצינט, אוקסיד וכדומה.
```
```text
בדקו כמה כמוסות נדרשות לקבלת הכמות הרשומה.
```

Fact-check: generic reading-tip guidance, not a per-product claim — does not conflict
with the D7 amendment that omits the per-card servings-per-day row (that amendment
bars a *fabricated per-product capsule count*; this bullet just tells the shopper to
look for that information themselves on whatever label they're holding). No flag.
(Note for the record, not a fix: bullet 1 trips the readability tool's antithesis
scanner, ', לא' — expected and exempt, owner-dictated text is exempt from the HARD
antithesis constraint per this task's own instructions.)

### 1.5 — Card eyebrow label

```text
מה חשוב לדעת:
```

Structural UI label (not a factual claim) — reused verbatim as instructed, prefixes
each of the 18 one-liners in §2.

---

## 2 — AUTHORED: 18 per-card "מה חשוב לדעת" one-liners

Each line is Tom-voice, one insight, grounded only in spec §B's factual basis for that
product — no number appears that isn't in service of a finding. Group/heading shown is
the **corrected** Heading (per §0 above), not the live TS's stale g3/g4 split. The
servings-per-day field is **not referenced anywhere below** — per D7's amendment, it is
fully absent from the card, never a placeholder.

**#1 — Supherb Citrate+B6 (250 mg, ציטראט) — Heading 1**
```text
ציטראט עם התמיכה המדעית הישירה ביותר לספיגה מבין 18 המוצרים שנבדקו, במינון שמגיע בדיוק לסף התשומת-לב העיכולית שקבעה EFSA (250 מ"ג).
```

**#2 — Altman Bisglycinate (250 mg, ביסגליצינט) — Heading 1**
```text
ביסגליצינט היא צורה נפוצה ומוכרת, אך הראיות הישירות לספיגה שלה עדיין מוגבלות מכדי לדרג אותה בביטחון מול ציטראט. המינון, 250 מ"ג, נמצא בדיוק בסף התשומת-לב העיכולית של EFSA.
```

**#3 — Altman Citrate 120 (200 mg, ציטראט) — Heading 1**
```text
ציטראט נקי לגמרי כאן: אין הסתייגות בטיחות או תיוג, והמינון (200 מ"ג) נמצא מעל החציון של המוצרים עם קריאה יסודית ברורה.
```

**#4 — Nutricare WELL (168 mg, ביסגליצינט) — Heading 1**
```text
ביסגליצינט נקי בבטיחות ובתיוג, במינון (168 מ"ג) שנמצא מתחת לחציון הקטגוריה. הראיות לדרג את הספיגה שלו בביטחון מול ציטראט עדיין מוגבלות.
```

**#5 — NT L.C. Anti Leg Cramps (190 mg, הידרוקסיד) — Heading 2**
```text
הידרוקסיד במינון בדיוק בחציון הקטגוריה (190 מ"ג), נקי בבטיחות ובתיוג. שם המוצר מתמקד בעוויתות שרירים, אבל סקירת קוקריין (Garrison et al., 2020, PMID 32956536) לא מצאה תמיכה קלינית מובהקת למגנזיום כתוסף מונע אצל מבוגרים עם עוויתות רגילות שאינן קשורות להריון או לפעילות גופנית.
```

**#6 — Full-Mag Hadas (122 mg, ביסגליצינט) — Heading 2**
```text
התווית כאן ברורה: אין בלבול בין 600 הכמוסות שבאריזה לבין כמות המגנזיום בפועל (122 מ"ג), שנמצאת ברבע התחתון של הטווח שנבדק.
```

**#7 — Tink Malate (136 mg, מלאט) — Heading 2**
```text
מלאט נקי בבטיחות ובתיוג, במינון (136 מ"ג) בחלק התחתון של הטווח שנבדק. סטנדרטי, בלי ממצא בולט מעבר לכך.
```

**#8 — Nutricare Malate (~135 mg, מלאט) — Heading 2**
```text
התווית מציינת רק את משקל התרכובת (700 מ"ג מלאט), בלי המרה לכמות היסודית בפועל (כ-135 מ"ג). זהו פער תיוג נפרד מהמינון הנמוך יחסית עצמו.
```

**#9 — Solgar Ca+Mg+D3 (100 mg, תערובת אוקסיד+ציטראט) — Heading 2**
```text
המינון היסודי (100 מ"ג) מצוין בבירור, אבל הצורה היא תערובת אוקסיד וציטראט ביחס לא מפורסם, כך שאי אפשר לדרג את הספיגה שלה בנפרד. סידן ו-D3 מופיעים גם הם בתווית, מעבר למגנזיום.
```

**#10 — Nutricare Taurate (76 mg, טאוראט) — Heading 2**
```text
76 מ"ג הוא המינון היסודי הנמוך ביותר מבין 18 המוצרים שנבדקו. הצורה, טאוראט, ידועה אך לא מדורגת בביטחון מול ציטראט.
```

**#11 — Nutricare Oxide-520 (520 mg, אוקסיד) — Heading 3**
```text
המינון הגבוה ביותר בקטגוריה (520 מ"ג) מגיע בצורת אוקסיד, הצורה עם הספיגה הפחות טובה מבין הצורות שנבדקו, וחוצה גם את סף הבטיחות היומי של 350 מ"ג שקבע ה-IOM.
```

**#12 — Altman Oxide-520 (520 mg, אוקסיד) — Heading 3**
```text
520 מ"ג מגנזיום יסודי בצורת אוקסיד: אותו מינון הגבוה ביותר בקטגוריה, וגם הוא חוצה את סף ה-350 מ"ג היומי של ה-IOM.
```

**#13 — Altman Magnesium UP (450 mg, אוקסיד) — Heading 3**
```text
450 מ"ג בצורת אוקסיד חוצה את סף הבטיחות היומי של 350 מ"ג ב-100 מ"ג נוספים, לצד מגבלת הספיגה הידועה של הצורה.
```

**#14 — Altman Magnesium Balance (450 mg, אוקסיד) — Heading 3**
```text
450 מ"ג בצורת אוקסיד, מעל סף הבטיחות היומי של 350 מ"ג. האריזה מוסיפה גם אשווגנדה וולריאן, שני רכיבים שלא נכללו בבדיקת המגנזיום כאן.
```

**#15 — Nutricare Nano Liposomal (88 mg, ביסגליצינט בסיס) — Heading 1**
```text
ביסגליצינט (צורת בסיס) עם תיוג ובטיחות נקיים, במינון (88 מ"ג) השני הנמוך ביותר מבין המוצרים עם קריאה יסודית ברורה. הכיתוב "נאנו ליפוזומלי" הוא טענת שיווק נפרדת: לא נמצאה במקורות שנבדקו עדות לספיגה משופרת מעבר לצורת הבסיס עצמה.
```

**#16 — Tink Oxide-520, 90 כמוסות (מינון לא ניתן לאימות, אוקסיד) — Heading 3 (corrected, see §0)**
```text
המספר 520 על האריזה לא מבהיר אם זו כמות מגנזיום יסודי או משקל התרכובת, כך שהמינון בפועל לא ניתן לאימות. הצורה כן ידועה: אוקסיד, מהצורות עם הספיגה הפחות טובה שנבדקו.
```

**#17 — Amorphicure pH Magnesium (מינון לא ניתן לאימות, קרבונט) — Heading 3 (corrected, see §0). Carries the D7-MANDATORY disambiguation clause.**
```text
התווית לא מציינת כמות מגנזיום יומית כלל. הצורה, קרבונט, מסווגת יחד עם אוקסיד כצורה בעלת ספיגה פחות טובה, על סמך דמיון כימי בין המלחים בלבד. ל-NIH ODS אין ציטוט ישיר על קרבונט, בשונה מאוקסיד.
```
This fulfills Product D7's mandatory amendment (spec §A.4 DEVIATION 3, upgraded from
discretionary to required): the card states, in its own line and not deferred to a
collapsed disclosure, that carbonate is grouped with oxide by chemical-class analogy
and does not carry oxide's direct NIH ODS citation.

**#18 — TRIOMAG (מינון לא ניתן לאימות, תערובת ציטראט/ביסגליצינט/טאוראט) — Heading 4**
```text
המוצר היחיד מתוך 18 שנבדקו שבו גם הצורה הכימית וגם המינון היסודי אינם ניתנים לקביעה מהתווית: שלוש צורות מגנזיום מעורבבות ביחס לא מפורסם.
```

---

## 3 — AUTHORED: page metadata description

**Maps to:** `bari-web/src/app/madrichim/magnesium/page.tsx`, `metadata.description`.
Supersedes the v2 4-criteria frame (which SLOT 10b of the v2 package wrote and which,
per this task's brief, "burned us in v2 gate-2"). Rewritten to the v3 3-thing frame
that item 1.1's intro sentence and the group-heading model both use.

```text
בארי בדקה 18 תוספי מגנזיום לפי שלושה דברים: כמות המגנזיום היסודי, הצורה הכימית ובהירות התווית, כדי להראות מה לחפש לפני שקונים.
```

126 characters — within the ≤160 SEO limit. Scoped to "18 תוספי מגנזיום... שבדקה," no
"מהמדף הישראלי" completeness claim (unlike the owner-dictated intro, this string is
mine to get right, so it stays scoped per the standing §8 rule rather than repeating
the flag raised in §1.1).

---

## 4 — AUTHORED: compact market-information-gaps copy

**Maps to:** `suppressedBarsDisclosureHe`-equivalent for v3. Condenses v2's Slot 3
(4 sentences) to 3 short sentences per the owner's "less text" direction, while keeping
every load-bearing distinction from the v2 rule: price is a Bari collection gap (not a
product fact), third-party is a market fact (zero certification found, dated), and
neither affects group placement.

```text
מחיר למנה עדיין לא נאסף על ידי בארי. בדיקת צד שלישי: לא אותר אישור הניתן לאימות פומבי בקרב 18 המוצרים שנבדקו, נכון ליולי 2026. שני הפערים האלה אינם חלק מהשיוך לקבוצות שלמטה.
```

---

## 5 — AUTHORED: collapsed-evidence section + disclosure labels

**Collapsed section title** (houses the merged dose/safety facts, the 3-bucket
absorption framework, and the sources list — the REUSED-v2 content named in §6 below,
per spec §D's instruction that these facts survive in exactly one place):
```text
לפרטים ומקורות
```

**Toggle labels:**
```text
לפרטים המלאים
```
```text
הסתר פרטים
```

These are generic, since the v2 `expanderLabels` ("הצג/הסתר את הסולמות" — "show/hide
the scales") named the gauge/ladder visuals specifically, and whether those survive
the v3 geometry rebuild is a Design/Frontend call outside this package's scope (per
spec §D item 4, gauge geometry is a Design/Frontend build item). If the v3 build keeps
the gauges, Frontend may prefer the v2 labels instead — flagging as an open choice, not
deciding it here.

---

## 6 — REUSED-v2 (verbatim, unchanged)

Per spec §D's "minimal set of facts that MUST survive somewhere," these v2-signed
strings are not re-authored — they are the correct, already-cleared content for the
collapsed "לפרטים ומקורות" section and are carried forward as-is:

- **Sources list** (3 sources: NIH ODS, Cochrane PMID 32956536, EFSA UL summary + URLs)
  and the closing methodology line ("בארי קוראת תוויות. בארי אינה בודקת במעבדה...") —
  v2 copy package Slot 8, unchanged.
- **Elemental-vs-compound-weight explainer** — v2 Slot 7 §1, unchanged.
- **Dose-in-context explainer** (corpus range 76-520 mg, median 190 mg, RDA
  310-420 mg "מכל המקורות יחד") — v2 Slot 7 §2, unchanged.
- **Merged safety/UL section** (350 mg IOM UL, 250 mg EFSA soft threshold, no
  capsule-stacking instruction) — v2 Slot 7 §4, unchanged.
- **"What magnesium does" + narrowed cramps finding** — v2 Slot 7 §5, unchanged.
- **`buyLinkDisclosureLine`** ("קישור קנייה אינו משפיע על הכללה, על השיוך לקבוצה או על
  סדר ההצגה") and **`updatedLabel`** ("18 מוצרים · יולי 2026") — v2 Slot 9, unchanged.

**Open, not decided here (spec §D flags this as "Content's call, not zero"):** the
3-bucket absorption framework (v2 Slot 7 §3) is still stated in full inside the
collapsed section AND, in compressed form, inside several of §2's per-card one-liners
above (e.g. #1/#11's "NIH ODS names oxide as less-absorbed" clause). Spec §D's
"repeated chemical-forms explainer" deletion target asked for exactly ONE canonical
derivation location; per-card one-liners are terse fact statements (form name +
evidence-tier judgement), not re-derivations of *why* — I read that as compliant with
the "terse per-card, full derivation once" split spec §D asks for, but flagging the
distinction explicitly since it's a judgement call, not a mechanical one.

---

## 7 — Group sub-captions: decision = NONE authored

Item 5 of the brief sets the default to no captions unless a heading needs one for
honesty. Reviewed against §A.5's hard requirement (Heading 1 must never imply citrate
and bisglycinate share equal absorption evidence, and must not drop the #1/#2
GI-tolerance flag):

- Every Heading-1 card (#1-#4, #6, #15) already states its own form's evidence tier
  individually in §2 above (citrate = direct NIH ODS support; bisglycinate = named,
  disclosed, evidence-limited) — the no-equal-evidence rule is satisfied per-card, not
  by an aggregate caption.
- #1 and #2's GI-tolerance flag is stated on those two cards specifically, not
  elsewhere.
- Heading 2's mixed composition (1 citrate, 4 evidence-limited forms, 1 undisclosed
  blend) is likewise carried by each member's own one-liner (#9's blend-ratio gap,
  #5/#7/#8/#10's evidence-limited note).

**Decision: no group captions authored for v3.** The honesty requirement §A.5 exists
to guard against is already met at the card level, and the owner's stated preference is
less text, not more. Logged per the autonomy mandate (a Content-lane call, no tripwire
tripped) — reversible if QA gate-2 finds a card-level gap this reasoning missed.

---

## 8 — Servings-per-day: explicitly no copy authored

Per Product D7's amendment (spec §4): the servings-per-day field is NULL for all 18
products (never parsed — a genuine data gap, not an oversight this package can fix) and
must be **fully absent from the card** — no row, no dash, no "לא זמין" placeholder.
No string is authored for this field anywhere in this package. This is a rendering
instruction for Frontend (the row must not exist in the DOM for any of the 18 cards),
not a copy gap.

---

## 9 — Self-check results

**Instruments run:** `integrations.clients.hebrew_readability.analyze()` and
`integrations.clients.hebrew_grammar_gate.analyze()`, invoked from `C:\Bari` with
`sys.path.insert(0, r"C:\Bari")` and package-qualified imports
(`from integrations.clients.hebrew_readability import analyze`) — not run from inside
`integrations/clients/` itself, to avoid the documented `http.py` stdlib-shadow bug.

**Readability / leakage / antithesis gate (HARD): 23/23 AUTHORED strings clean.**
One failure found and fixed before this file was written: product #17's first draft
tripped the antithesis scanner (", לא" — "...בלבד, לא בציטוט ישיר מ-NIH ODS"). Rewritten
into two sentences (see §2, #17) — re-run confirmed clean. Two AUTHORED one-liners
(#11, #12) carry an ADVISORY-only "long sentence" flag (29.0 and 23.0 words/sentence
respectively) — advisory does not fail `is_clean`; both still read as a single
information-dense but grammatical sentence and were left as-is rather than
artificially split, since splitting would have separated the dose figure from its two
attached findings (form + UL-crossing) that both need to land together for the line to
carry its full insight. No framework-leakage, score-mechanic, recommendation-language,
sodium-term, or brand-spelling hits anywhere in the 23 AUTHORED strings.

Two OWNER-DICTATED strings were also run for the record (informational, not gating,
per this task's explicit exemption): the intro sentence and howto-bullet-1 both use
constructions the antithesis scanner flags (owner text is exempt from the HARD
constraint; ships verbatim regardless of the scan result).

**Grammar/agreement gate (DictaBERT-morph): 14/23 AUTHORED strings fully clean; the
remaining 9 carry only `confidence="medium"` flags — zero `confidence="high"` flags.**
Per standing protocol, every medium flag was individually reviewed, not auto-accepted.
All 9 are the tool's documented "closest preceding NOUN/PRON" anchoring limitation,
in three recurring patterns already characterized in the v2 package's own self-check:
1. **Construct-chain misanchoring** (#1, #2: "תשומת-לב העיכולית" — the adjective
   correctly agrees with "תשומת" (fem), the true construct head, not "לב" (masc) the
   tool anchored to; #16: "כמות מגנזיום יסודי" — "יסודי" correctly modifies "מגנזיום"
   (masc), pre-existing standing terminology used dozens of times in the already-shipped
   v1/v2 copy; #17: "צורה בעלת ספיגה" — "בעלת" correctly agrees with "צורה" (fem);
   meta_description: same "מגנזיום יסודי" pattern as #16).
2. **VS word-order / non-adjacent true subject** (#13: "אוקסיד חוצה" — the real subject
   is "450 מ״ג", not the intervening "אוקסיד"; #15: "לא נמצאה... עדות" — the real
   (post-verbal) subject is "עדות" (fem), not "שיווק" (masc) the tool anchored to;
   #16: "האריזה לא מבהיר" — the real subject is "המספר" (masc), not the prepositional
   "האריזה"; #18: "18 שנבדקו" — "שנבדקו" agrees with the elided plural "מוצרים", not
   the singular "המוצר" earlier in the sentence; market_gaps_compact: "מחיר למנה...
   נאסף" — subject is "מחיר" (masc), not the prepositional "למנה" (fem)).
3. **Mixed/compound-subject default-plural** (#15: "תיוג ובטיחability נקיים" —
   standard Hebrew masc-plural default for a mixed-gender compound subject, exact
   precedent from the v2 self-check; #18: "גם...וגם...אינם" compound-via-"גם...וגם"
   correctly plural; #18: "שלוש צורות מגנזיום מעורבבות" — correctly agrees with the
   fem-plural "צורות", the construct head, not "מגנזיום" (masc) the tool anchored to).
4. **Pre-existing shipped terminology, not new** (`market_gaps_compact`: "בדיקת צד
   שלישי" — "שלישי" (masc) correctly agrees with "צד" (masc), the identical construct
   already live in `GUIDE_BAR_LABELS_HE.thirdPartyVerification` and multiple lines of
   the current TS file; already characterized as a false positive in the v2 package's
   own self-check, same pattern, not re-litigated here).

No genuine agreement error was found on manual review of any of the 9 flagged strings.
Full per-flag detail (issue_type, span, anchor, expected/observed) preserved at
`C:\Users\HP\AppData\Local\Temp\claude\c--Bari\0f46d4b5-5474-42df-8c7a-85343b95dcfd\scratchpad\gate_full_results.json`
for independent QA re-check.

---

## 10 — Open items for the orchestrator / next gate

1. **§0's blocking flag** — `V3_GROUP_BY_BARCODE` must be corrected (g3=6/g4=1, moving
   #16 and #17 out of g4) before this package's card copy is wired; wiring #16/#17's
   one-liners under the wrong heading would misrepresent their finding.
2. **§1.1's HIGH flag** — "מהמדף הישראלי" in the owner-dictated intro conflicts with
   the standing §8 market-scoping rule. Owner call, not mine to silently resolve.
3. **§1.2's MEDIUM flag** — "מוצרים רבים" in the owner-dictated findings bullet is the
   exact vague-count pattern the spec's own §C wording-hazard warned against for this
   finding (6/18 exact). Owner call.
4. **§5's open choice** — whether the v3 collapsed-section toggle reuses v2's
   gauge-specific labels or the generic ones authored here depends on whether the
   gauge/ladder visuals survive the v3 rebuild (Design/Frontend call, spec §D item 4).
5. **§6's judgement call** — terse per-card absorption mentions vs. the single full
   derivation in the collapsed section; flagged as a read, not a certainty.
6. Not authored in this package (out of Content's lane, per spec §D): the
   `GuideBucket`/`GuideV3Group` field-shape and rendering-path decisions for the
   corrected grouping, and the gauge-geometry rebuild itself.

---

## Return

```json
{
  "task": "TASK-577",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "02_products/supplements/magnesium/mag_guide_v3_copy_package.md", "action": "created", "sha256": "RECOMPUTE_AT_ACCEPT (see final chat message for the exact post-write hash)"}
  ],
  "counts": {
    "products_covered": "18/18 (all products in mag_guide_v3_structure_spec.md §A.3 / §B)",
    "slots_authored": "5 (18 card one-liners as one slot-group + metadata description + market-gaps compact copy + collapsed-section title/toggle labels + group-caption decision)",
    "owner_dictated_strings_included": "12 (intro sentence, 4 findings bullets incl. heading, 4 group headings, 3 howto bullets incl. heading, 1 card eyebrow label) — verbatim, fact-checked, not rewritten",
    "fact_check_flags_raised": "2 (HIGH: owner intro's 'מהמדף הישראלי' contradicts standing spec §8 market-scoping rule; MEDIUM: owner findings-bullet 3's 'מוצרים רבים' is the exact vague-count pattern spec §C flagged as a hazard for this finding, precise count is 6/18)",
    "blocking_structural_flag": "1 (live TS V3_GROUP_BY_BARCODE mismatches signed spec for products #16/#17 — both currently g4, must be g3; documented in §0)",
    "authored_strings_total": 23,
    "readability_leakage_antithesis_clean": "23/23 (hebrew_readability.analyze().is_clean, HARD gate) — 1 fix applied pre-delivery (product #17 antithesis rewrite)",
    "readability_advisory_flags": "2/23 (long-sentence advisory on #11, #12 — does not fail is_clean, left as-is per rationale in §9)",
    "grammar_fully_clean": "14/23 (hebrew_grammar_gate.analyze().is_clean)",
    "grammar_high_confidence_flags": "0/23",
    "grammar_medium_confidence_flags_reviewed": "9/23, all classified false-positive (closest-noun/VS-order/compound-subject tool limitations, one instance of pre-existing shipped terminology) — zero genuine agreement errors found",
    "d7_mandatory_amendment_fulfilled": "1/1 (#17 carries the mandatory carbonate/oxide disambiguation clause directly on-card, not deferred to a collapsed disclosure)",
    "servings_per_day_placeholders_authored": "0/18 (correctly omitted per D7 amendment — see §8)",
    "group_captions_authored": "0/4 (decision logged in §7: per-card facts already satisfy the honesty requirement; owner asked for less text)"
  },
  "commands_run": [
    {"cmd": "python gate_check_v3.py (initial readability+grammar pass, informational, encoding issue on first attempt)", "exit_code": 1},
    {"cmd": "python gate_check_v3.py (re-run with -X utf8 / PYTHONUTF8=1, from C:\\Bari)", "exit_code": 0},
    {"cmd": "python -c \"...\" (targeted re-check of product #17 fix, readability + grammar)", "exit_code": 0},
    {"cmd": "python gate_check_v3_full.py (final full-detail run over all 23 AUTHORED strings, writes gate_full_results.json)", "exit_code": 0}
  ],
  "not_done": [
    "V3_GROUP_BY_BARCODE correction in magnesium-guide-data.ts — not Content's lane, flagged in §0 for Frontend/orchestrator",
    "GuideBucket/GuideV3Group field-shape decisions for the corrected grouping — out of Content's lane per spec §D",
    "Gauge/ladder geometry rebuild for v3 — Design/Frontend build item, spec §D item 4",
    "Two fact-check flags (§1.1, §1.2) left as flags, not resolved — owner decision required, not Content's to silently patch owner-dictated text",
    "Adversarial QA / Red-Team gate-2 has not run against this package — nothing here ships until that clears plus Nutrition + Product final sign-off"
  ],
  "self_check": "Acceptance test: every AUTHORED Hebrew string clears hebrew_readability.is_clean (framework-leakage, score-mechanic, recommendation-language, sodium-term, brand-spelling, antithesis HARD gates) before handoff, and every grammar flag is either confidence=\"high\" (none found) or individually reviewed and classified (9/23 medium, all false-positive, reasoning recorded in §9). Observed: 23/23 readability-clean on final run (post #17 fix), 0/23 grammar high-confidence flags, 14/23 grammar fully clean, 9/23 reviewed-clean. Every dose/form/safety/label fact in the 18 one-liners was checked against spec §B's table before writing, not inferred; the D7-mandatory #17 disambiguation clause is present; no servings-per-day placeholder was authored anywhere. Two fact-check flags raised on owner-dictated text per the task's explicit instruction to flag rather than silently edit; one blocking structural flag raised on the live TS's stale provisional grouping, which is outside Content's lane to fix but directly affects whether this package's card copy renders under the correct heading."
}
```

---

## ADDENDUM (v3.1) — TASK-580, Gate-1: expanded intro, four measured dimensions

**Owner feedback (2026-07-10, verbatim intent):** "I also want in the intro to add
more details about the dimensions we are measuring. not good enough." The live
one-liner (§1.1 above) names three things. Per `mag_guide_v3_structure_spec.md` §B,
every card's disclosure actually assesses **four** bars: מינון, צורה וספיגה, בטיחות,
שקיפות תווית. This addendum expands the intro to explain what each dimension checks,
in consumer language, before the reader meets the first card — without turning it back
into the v2 methodology essay the owner already deleted once.

**Word budget:** hard cap ~70 words per the dispatch. Both intro variants below measure
in at 50 and 60 words respectively (full block, including the sentence(s) already in
§1.1) — verified by direct `len(text.split())` count, not estimated.

### v3.1-SLOT-1 — RECOMMENDED DEFAULT (does not touch owner's "שלושה" numeral)

Keeps §1.1's owner-dictated sentence exactly as-is (both its wording and its existing
HIGH flag on "מהמדף הישראלי" — that flag is inherited unchanged, not re-litigated
here) and appends three new authored sentences, one clause per dimension the owner's
sentence already names (dose, form, label clarity). Ships as a single intro block; the
appended portion is the only newly-authored text in this slot.

**Full rendered block (50 words):**
```text
בדקנו 18 מוצרים מהמדף הישראלי. שלושה דברים חשובים במיוחד: כמות המגנזיום היסודי, הצורה הכימית ובהירות התווית. כמות המגנזיום היסודי נמדדת מול טווח המוצרים שבדקנו, בין 76 ל-520 מ"ג ליחידה. הצורה הכימית קובעת כמה מגנזיום הגוף באמת סופג. ובהירות התווית בודקת אם אפשר לדעת מהאריזה כמה מגנזיום יסודי ובאיזו צורה מקבלים.
```

**Newly-authored portion only, for wiring if the owner's original two sentences are
kept as a separate string (34 words):**
```text
כמות המגנזיום היסודי נמדדת מול טווח המוצרים שבדקנו, בין 76 ל-520 מ"ג ליחידה. הצורה הכימית קובעת כמה מגנזיום הגוף באמת סופג. ובהירות התווית בודקת אם אפשר לדעת מהאריזה כמה מגנזיום יסודי ובאיזו צורה מקבלים.
```

**Residual honesty gap, disclosed not hidden:** this slot explains only the three
dimensions the owner's sentence names. The fourth assessed dimension (בטיחות) is left
unexplained by the intro even though every card carries a safety bar. That gap is what
Slot 2 exists to close — flagged as a decision, not silently resolved by picking Slot 1.

### v3.1-SLOT-2 — OPTIONAL, FLAGGED: modifies owner-dictated text (numeral + list)

The more honest option per the facts (four bars are actually assessed on every card),
but it changes "שלושה" to "ארבעה" and adds "הבטיחות" to the owner's dictated list.
**This is a modification of owner-authored text and requires the owner's explicit
acceptance before it ships — it is proposed here, not settled.** Same inherited HIGH
flag on "מהמדף הישראלי" applies, unchanged.

**Full rendered block (60 words):**
```text
בדקנו 18 מוצרים מהמדף הישראלי. ארבעה דברים חשובים במיוחד: כמות המגנזיום היסודי, הצורה הכימית, הבטיחות ובהירות התווית. כמות המגנזיום היסודי נמדדת מול טווח המוצרים שבדקנו, בין 76 ל-520 מ"ג ליחידה. הצורה הכימית קובעת כמה מגנזיום הגוף באמת סופג. הבטיחות בודקת אם המינון היומי חוצה סף עיכולי מוכר. ובהירות התווית בודקת אם אפשר לדעת מהאריזה כמה מגנזיום יסודי ובאיזו צורה מקבלים.
```

Fact basis for the added safety clause, checked against spec inputs before writing:
EFSA's 250 mg figure is a soft attention/tolerance threshold (digestive comfort), not
a toxicity limit — the IOM's separate 350 mg supplemental UL is the higher safety
ceiling. "סף עיכולי מוכר" (a known digestive threshold) states this without the banned
"not X but Y" construction and without naming a specific mg figure the intro doesn't
need to carry (the figures already live on-card and in the merged dose & safety
section, §6).

### v3.1-SLOT-3 — OPTIONAL bridge line for "מה גילינו." Default: unchanged, not wired.

Per the dispatch, the default is that the "מה גילינו" box (§1.2) needs no change. This
one-line bridge is authored only in case the orchestrator wants an explicit hand-off
sentence connecting the expanded intro to the findings box; it is not part of either
recommended slot above and should not be wired unless separately requested.

```text
כל אחד מהמימדים האלה מוסבר שוב, במילים פשוטות, ליד כל מוצר למטה.
```

### Self-check (this addendum only)

Instruments run: `hebrew_readability.analyze()` and `hebrew_grammar_gate.analyze()`,
invoked with `sys.path.insert(0, r"C:\Bari")` from
`C:\Users\HP\AppData\Local\Temp\claude\c--Bari\0f46d4b5-5474-42df-8c7a-85343b95dcfd\scratchpad\`
(outside `integrations/clients/`, dodging the documented `http.py` stdlib-shadow bug).

**Readability (HARD gate): 4/4 strings clean.** All four addendum strings
(Slot-1 full block, Slot-1 appended-only, Slot-2 full block, Slot-3 bridge) return
`is_clean: true` — zero framework-leakage, score-mechanic, recommendation-language,
sodium-term, or antithesis-pattern hits. Word counts verified by direct count: Slot-1
full = 50, Slot-2 full = 60, both under the ~70-word cap; Slot-3 bridge = 12.

**Grammar/agreement gate: 0/4 strings fully clean; 0/4 high-confidence flags; 8 total
medium-confidence flags across the 4 strings, all individually reviewed, all classified
false-positive** — no genuine agreement error found. Breakdown, matching the same tool
limitation patterns already characterized in this package's §9 and the v2 package:
- **Construct-chain misanchoring:** "היסודי" (×2, "כמות המגנזיום היסודי" — "יסודי"
  correctly modifies "מגנזיום," pre-existing shipped terminology, same as §9 pattern 1);
  "נמדדת" ("כמות... נמדדת" — the fem verb correctly agrees with "כמות" (fem), the true
  construct head, not "המגנזיום" (masc) the tool anchored to); "ובאיזו" ("ובאיזו צורה" —
  "איזו" is fem, correctly agreeing with "צורה" (fem)).
- **Non-adjacent true subject / partitive construction:** "הישראלי" ("מהמדף הישראלי" —
  masc-singular adjective correctly agrees with "המדף" (masc singular), not the earlier
  plural "מוצרים" the tool likely anchored to); "מוסבר" (Slot-3: "כל אחד...מוסבר" — the
  singular verb correctly agrees with "כל אחד" (the true singular head of the partitive
  "כל אחד מ-," not the plural "מהמימדים").
- **Impersonal-plural construction (standard Hebrew, not an error):** "מקבלים" (×2 flags
  on the same token — "...כמה מגנזיום יסודי ובאיזו צורה מקבלים" uses the generic
  impersonal plural, e.g. "כמה מקבלים" = "how much does one get," identical in kind to
  "אומרים ש..." — no explicit singular/plural subject to disagree with).

No genuine error found on manual review of any of the 8 flags. Full per-flag JSON at
`C:\Users\HP\AppData\Local\Temp\claude\c--Bari\0f46d4b5-5474-42df-8c7a-85343b95dcfd\scratchpad\gate_check_intro_addendum.py`
output, re-runnable for independent QA re-check.

### Return (this addendum, TASK-580)

```json
{
  "task": "TASK-580",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "02_products/supplements/magnesium/mag_guide_v3_copy_package.md", "action": "modified", "sha256": "d069e1424676d371fba9ac3734e288eb16c0b1394025915dd355127ac9624d17"}
  ],
  "counts": {
    "slots_authored": "3 (v3.1-SLOT-1 recommended default / v3.1-SLOT-2 optional flagged four-dimension revision / v3.1-SLOT-3 optional unused-by-default bridge line)",
    "authored_strings_total": 4,
    "word_counts": "Slot-1 full block = 50 words, Slot-1 appended-only = 34 words, Slot-2 full block = 60 words, Slot-3 bridge = 12 words — all under the ~70-word cap",
    "readability_leakage_antithesis_clean": "4/4 (hebrew_readability.analyze().is_clean, HARD gate)",
    "grammar_fully_clean": "0/4 (hebrew_grammar_gate.analyze().is_clean)",
    "grammar_high_confidence_flags": "0/4 strings, 0/8 total flags",
    "grammar_medium_confidence_flags_reviewed": "8/8, all classified false-positive (construct-chain misanchoring, non-adjacent true subject / partitive construction, impersonal-plural — zero genuine agreement errors found)",
    "owner_text_modification_flags_raised": "1 (v3.1-SLOT-2 changes the owner-dictated numeral 'שלושה'→'ארבעה' and adds 'הבטיחות' to his dictated list; proposed, not settled, requires explicit owner acceptance before it ships)",
    "inherited_open_flags": "1 (v3.1's §1.1-sourced 'מהמדף הישראלי' HIGH flag applies unchanged to both Slot-1 and Slot-2 full blocks; not re-litigated in this addendum, not resolved either)"
  },
  "commands_run": [
    {"cmd": "python -X utf8 gate_check_intro_addendum.py (readability + grammar gate over all 4 addendum strings, run from scratchpad, outside integrations/clients/)", "exit_code": 0}
  ],
  "not_done": [
    "Decision between Slot-1 (default, three-dimension, no owner-text change) and Slot-2 (four-dimension, requires owner acceptance of the numeral change) — left as a flagged choice, not decided here, per the standing rule that unilaterally editing owner-dictated consumer copy is out of Content's remit even under the autonomy mandate",
    "v3.1-SLOT-3 bridge line — authored but explicitly not recommended for wiring unless separately requested; default is the 'מה גילינו' box stays unchanged",
    "Adversarial QA / Red-Team gate-2 has not run against this addendum — nothing here ships until that clears plus Nutrition + Product final sign-off, same as the base package"
  ],
  "self_check": "Acceptance test: every AUTHORED addendum string clears hebrew_readability.is_clean before handoff, and every grammar flag is either confidence=\"high\" (none found) or individually reviewed and classified (8/8 medium, all false-positive, reasoning recorded above). Observed: 4/4 readability-clean, 0/8 grammar high-confidence flags, 8/8 medium flags reviewed and classified false-positive with zero genuine errors found. Word counts verified by direct len(text.split()) count against the ~70-word cap for both full-block variants (50 and 60). No em dash used in any string; no 'X, לא Y' construction; no data-state narration phrase from the banned list; no מומלץ/ladder language; every dose/range figure (76-520 mg) traces to mag_guide_v3_structure_spec.md §A.3, not invented. One owner-text-modification flag raised (Slot-2's numeral change) per the task's explicit instruction to flag rather than silently decide; this is not presented as settled and does not ship without owner acceptance."
}
```

---

## ADDENDUM (v3.2) — TASK-587, Gate-1: education-section heading + one-line teaser

**Owner problem (2026-07-10):** the owner could not find the deep content — the
elemental-vs-compound explainer, dose context, form/absorption evidence buckets,
safety thresholds, the cramps evidence review, and the clickable sources — because it
sits behind a quiet toggle at the page bottom whose current label is just "לפרטים
ומקורות." The section stays collapsed by default; the fix is to give it a heading a
scanning reader actually registers as "the full explanation lives here," plus a
one-line teaser stating exactly what opens, so nobody has to click blind.

**Factual basis, checked against the six live `educationSpine` sections in
`magnesium-guide-data.ts` before writing** (nothing below promises content that isn't
actually in the section):
1. "מגנזיום יסודי מול משקל התרכובת" — the elemental-vs-compound-weight distinction,
   which is also the plain-language basis for the labelTransparency criterion.
2. "המינון בהקשר" — dose context (corpus range 76-520 mg, median 190 mg, RDA
   310-420 mg from all sources).
3. "צורה כימית וספיגה" — the three absorption evidence buckets (NIH ODS-named
   better-absorbed forms, oxide/carbonate, evidence-limited forms).
4. "בטיחות" — the two precise numeric thresholds (IOM/NASEM 350 mg supplemental UL,
   EFSA 250 mg soft GI-tolerance line).
5. "מה מגנזיום עושה" — what magnesium does generally, plus the narrowed 2020 Cochrane
   cramps finding (PMID 32956536).
6. "מקורות" — 3 clickable sources (NIH ODS, Cochrane, EFSA), each with a one-line
   description of what it supports.

Sections 1-4 above are exactly the four assessed dimensions named in the brief (dose,
form, safety, label). Section 4's two numbers are exact, published thresholds, which is
the basis for calling them "מדויק" in the teaser below — not an inflated claim. The
teaser does not promise section 5 (cramps/what-magnesium-does) by name; that content is
real but outside the brief's ≤20-word budget and outside what the brief asked the
teaser to promise, so it is left implicit rather than listed and then broken by the
word cap.

### v3.2-SLOT-1 — Section heading (recommended default)

Replaces the current `MAG_V3_COLLAPSED_SECTION_TITLE_HE` value ("לפרטים ומקורות") with
a heading that states what the section actually is, not just that it exists. "לפרטים"
(details) is generic enough to read as boilerplate; "ההסבר המלא" (the full explanation)
is what a reader scanning past a wall of cards is actually looking for, and "ומקורות
המידע" keeps the sources half of the promise visible in the heading itself, matching
what section 6 delivers.

```text
ההסבר המלא ומקורות המידע
```

Single recommendation, not a menu, per standing practice — this is a Content-lane
wording call inside an existing field, not a strategic or scoring decision, so no
tripwire applies and no owner escalation is needed to ship the wording itself. Making
the section **visible with real heading hierarchy** (instead of a quiet toggle) is a
Design/Frontend structural change outside this addendum's scope — see Open items below.

### v3.2-SLOT-2 — One-line teaser (new field, no prior slot)

No `collapsedEvidenceSectionTeaserHe`-equivalent field exists yet in the copy package
or the TS data file — Item 5 of the base v3 package (§5 above) authored a title and two
toggle labels only, no teaser line. This addendum adds it. 15 words (`len(text.split())`
verified), under the 20-word cap.

```text
כאן מוסבר כל אחד מארבעת הדברים שבדקנו, כולל סף הבטיחות המדויק, ולצידם רשימת המקורות המדעיים.
```

Plain-language check against Hard Rule 9 (no data-state/confidence/provenance
narration): this line describes what a page section contains ("here's what four things
this explains, plus a source list"), the same register as any other section-heading
teaser on the page — it does not hedge a product's data confidence, does not use any
phrase from the banned list, and does not narrate how or whether anything was verified.

### Self-check (this addendum only)

Instruments run: `hebrew_readability.analyze()` and `hebrew_grammar_gate.analyze()`,
invoked with `sys.path.insert(0, r"C:\Bari")` from
`C:\Users\HP\AppData\Local\Temp\claude\c--Bari\0f46d4b5-5474-42df-8c7a-85343b95dcfd\scratchpad\`
(outside `integrations/clients/`, dodging the documented `http.py` stdlib-shadow bug).

**Readability (HARD gate): 2/2 strings clean.** Both the heading and the teaser return
`is_clean: true` — zero framework-leakage, score-mechanic, recommendation-language,
sodium-term, or antithesis-pattern hits. No em dash in either string; no "X, לא Y"
construction; no מומלץ/exclamation; no banned data-state phrase.

**Grammar/agreement gate: 1/2 strings fully clean (heading); 1/2 (teaser) carries 2
medium-confidence flags, both reviewed, both classified false-positive — zero
high-confidence flags, zero genuine agreement errors found.** Detail: the teaser flags
both anchor to "המדעיים" in "רשימת המקורות המדעיים" (issue_type
`noun_adj_gender_mismatch` and `noun_adj_number_mismatch`, both `confidence="medium"`).
"מקורות" (sources) is grammatically masculine plural despite its feminine-looking "-ות"
ending — an irregular Hebrew plural in the same family as מקומות/זמנים-type nouns — so
the correctly-agreeing masculine-plural adjective is "מדעיים," which is exactly what
was written. The tool's gender/number check appears to key off the "-ות" surface form
rather than the noun's true grammatical gender, the same class of construct-chain/
surface-morphology misanchoring already characterized in this package's §9 and the
v3.1 addendum's self-check (pattern 1: adjective correctly agrees with the true
construct head, tool anchors to a morphological cue instead). Per standing protocol,
this medium-confidence flag was individually reviewed, not auto-fixed and not
auto-accepted; no rewrite was made because the flagged text is already correct. Full
per-flag JSON at
`C:\Users\HP\AppData\Local\Temp\claude\c--Bari\0f46d4b5-5474-42df-8c7a-85343b95dcfd\scratchpad\gate_v32_results.json`.

### Open items for the orchestrator / next gate

1. **New field required.** `collapsedEvidenceSectionTeaserHe` (or equivalent name) does
   not exist yet in `GuidePageVM` / `magnesium-guide-data.ts` — Frontend Agent must add
   a render slot for it under the existing `collapsedEvidenceSectionTitleHe` heading.
   Not authored here: the field-shape/prop decision itself (out of Content's lane).
2. **Visibility change is structural, not just copy.** The brief's core ask — the
   section becomes a real, visible heading instead of a quiet bottom-of-page toggle —
   is a Design/Frontend layout change (hierarchy, position, possibly always-visible
   heading with only the body collapsed). This addendum supplies the strings; it does
   not decide or implement the visual treatment.
3. Adversarial QA / Red-Team gate-2 has not run against this addendum — nothing here
   ships until that clears plus Nutrition + Product final sign-off, same standing rule
   as every other slot in this package.

### Return (this addendum, TASK-587)

```json
{
  "task": "TASK-587",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "02_products/supplements/magnesium/mag_guide_v3_copy_package.md", "action": "modified", "sha256": "be91f6c1b5b73d8fc1ccaa897e8cca44023c94d93301c538eefb0545237217e3 (best-effort; this value is itself pre-image to the byte written for this JSON field, same self-reference limitation as the v3.1 addendum's embedded hash — authoritative final hash reported in the returning agent's chat message, recomputed after this write)"}
  ],
  "counts": {
    "slots_authored": "2 (v3.2-SLOT-1 section heading / v3.2-SLOT-2 one-line teaser, new field)",
    "authored_strings_total": 2,
    "word_counts": "SLOT-1 heading = 4 words, SLOT-2 teaser = 15 words (cap: teaser <=20 words per brief)",
    "readability_leakage_antithesis_clean": "2/2 (hebrew_readability.analyze().is_clean, HARD gate)",
    "grammar_fully_clean": "1/2 (heading; hebrew_grammar_gate.analyze().is_clean)",
    "grammar_high_confidence_flags": "0/2 strings, 0 total flags",
    "grammar_medium_confidence_flags_reviewed": "2/2 (both on teaser, same span 'המדעיים'), both classified false-positive (irregular masculine-plural noun 'מקורות' with feminine-looking '-ות' ending; tool keys off surface morphology, not true gender) — zero genuine agreement errors found",
    "fact_basis_sections_checked": "6/6 live educationSpine sections read and matched against the teaser's claim before writing; sections 1-4 map onto the brief's four assessed dimensions, section 4 grounds the 'safety threshold' claim in two exact published numbers (350mg IOM, 250mg EFSA), section 6 grounds the 'scientific sources' claim in 3 clickable citations",
    "banned_terms_hits": 0
  },
  "commands_run": [
    {"cmd": "python -X utf8 gate_check_v32.py (readability + grammar gate over both addendum strings, run from scratchpad, outside integrations/clients/)", "exit_code": 0}
  ],
  "not_done": [
    "New field wiring (collapsedEvidenceSectionTeaserHe or equivalent) in magnesium-guide-data.ts / GuidePageVM — Frontend Agent's lane, not Content's",
    "Visual/structural change making the section genuinely visible (heading hierarchy, position, always-visible vs. collapsed-body) — Design/Frontend build item, this addendum supplies strings only",
    "Adversarial QA / Red-Team gate-2 has not run against this addendum — nothing here ships until that clears plus Nutrition + Product final sign-off"
  ],
  "self_check": "Acceptance test: every AUTHORED string clears hebrew_readability.is_clean before handoff, and every grammar flag is either confidence=\"high\" (none found) or individually reviewed and classified (2/2 medium, both false-positive on the same irregular-plural-noun pattern, reasoning recorded above). Observed: 2/2 readability-clean, 0/2 grammar high-confidence flags, 2/2 medium flags reviewed with zero genuine errors found. Teaser word count verified by direct len(text.split()) = 15, under the 20-word cap. Heading and teaser both checked against all 6 live educationSpine sections before writing so the promise matches the actual content (four assessed dimensions covered in sections 1-4, exact safety numbers in section 4, source list in section 6) — nothing promised that isn't in the spine. No em dash, no 'X, לא Y' construction, no banned data-state-narration phrase, no מומלץ, no exclamation, in either string."
}
```

