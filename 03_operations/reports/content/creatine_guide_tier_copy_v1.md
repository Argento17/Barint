# Creatine Guide — 4-Tier Recommendation Model — Content Copy (Gate 1 Draft)

**Task:** TASK-504 Wave 2 (מדריכים). **Author:** Content Agent. **Date:** 2026-07-04.
**Status:** GATE 1 DRAFT ONLY — requires Adversarial QA (gate 2) sign-off before anything
ships. This document authors copy only; no code, no `creatine-guide-data.ts`, no
`bucket_logic`, no bar states were touched.

**Grounded in:**
- `03_operations/reports/product/creatine_guide_recommendation_tiers_v1.md` — tier
  definitions (§3), per-product bar-state table (§4), the "0/18 Israeli
  `third_party_verification` = PASS" headline finding (§6 note 1), and the
  California Gold Nutrition `cannot_assess` ruling (§5).
- `01_framework/nutrition/creatine_guide_tier_cosign_v1.md` — Nutrition D7 co-sign,
  zero misassignments, headline finding confirmed exact (§2), and the required build
  correction that California Gold's price bar displays CANNOT-VERIFY, not a computed
  ₪ figure (§3) — copy below never states a price number for that product.
- `01_framework/nutrition/creatine_evidence_cosign_v1.md` — vetted claim tiers, dose
  criteria, and the standing constraint that no health/efficacy claim rides on the
  hero image or tier copy.
- `C:\bari_wt_t504\bari-web\src\lib\guides\magnesium-guide-data.ts` (read in full) —
  the shipped VM field names (`recommendationTierCaptions`, `headlineFinding`,
  `cannotAssessSectionIntroHe`, `expanderLabels`, `heroImage.alt`) and the exact house
  patterns this copy reuses: two-sentence "X. הוא/זהו אינו Y." data-gap framing
  (never comma+"לא"), and generic/product-agnostic phrasing in captions/section-intros
  so they don't go stale on rescore.
- `git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts` (997
  lines, read in full) — existing, live, two-gate-approved terminology reused
  verbatim: "אומת מול מאגר" (directory-verified) vs "מוצהר על-ידי היצרן"
  (manufacturer-stated, unverified) vs "לא נמצאה טענה" (no claim); "NSF Certified for
  Sport" kept untranslated (existing precedent, appears ~15× in the live file); and
  California Gold Nutrition's own existing row copy ("מספר הכמוסות היומי הנדרש...לא
  מפורט, כך שהמינון היומי בפועל לא ידוע") as the direct source for Slot 3's framing.

**Key structural difference from the shipped magnesium guide:** creatine displays
**all 6 bars** — none suppressed (Product doc §1: `dose_adequacy`, `form_absorption`,
`third_party_verification`, `price_fairness`, `safety`, `label_transparency` all have
mixed states across the 31-product corpus). So there is no "N bars not shown"
disclosure line for creatine, and captions do not scope themselves to "the bars this
guide displays" the way magnesium's did (magnesium suppressed 2 of 6). Also unlike
magnesium, the top tier (מומלץ מאוד) is **populated** (3 worldwide products: Thorne,
Momentous, BPN) — so there is no empty-top-tier state line for creatine; the
brief's headline-finding slot is a different structural fact instead (below).

---

## Slot 1 — Four tier caption lines

One short line per tier header, scoped to creatine's actual bar behavior (verified
against Product doc §4's per-product caveat sets, not assumed from the magnesium
precedent). No literal tier word appears in any caption's prose — the rendered tier
HEADING supplies the name, per EXCEPTION-003.

**מומלץ מאוד**
```
מוצרים שעומדים בכל ספי הקנייה במלואם, בלי אף הסתייגות.
```
Provenance: direct restatement of `clears_all_bars` (Product doc §3, confirmed
unchanged by Nutrition co-sign §1). Reuses the magnesium guide's own caption verbatim
— same predicate, and this is a genuinely populated tier for creatine (Thorne,
Momentous, BPN — Product doc §4, rows 19/20/22), so the line is written with no
assumption of emptiness. VM field: `recommendationTierCaptions.very_recommended`.

**מומלץ**
```
ההסתייגות היחידה אצל המוצרים האלה היא מינון שנמוך מהטווח שנחקר. אפשר להגיע
לטווח הזה על ידי לקיחת כמות יומית גדולה יותר.
```
Provenance: `dose_adequacy_sole_caveat` (Nutrition doc §1, BioSteel — the corpus's
sole מומלץ product, 2.5g vs the 3g floor, every other bar independently confirmed
PASS). Unlike the magnesium caption, this one drops the "מתוך הספים שהמדריך מציג"
scoping clause — magnesium needed it because 2 of 6 bars were suppressed; creatine
suppresses none (Product doc §1), so a scoping clause here would misstate the guide
as showing fewer bars than it does. VM field:
`recommendationTierCaptions.recommended`.

**טוב**
```
מוצרים שנושאים הסתייגות על המוצר עצמו, מעבר לשאלת המינון: בדיקת צד שלישי
שטרם אומתה מול מאגר עצמאי, הוגנות המחיר, ולעיתים גם מינון חלקי לצידן.
הסתייגות כזו לא משתנה כמה שלוקחים.
```
Provenance: `dose_adequacy_sole_caveat` — caveat set contains a non-dose bar (Product
doc §4, all 19 טוב rows). **Deliberately NOT copied from magnesium's טוב caption**,
which named form/safety/label — those are the bars that were actually flagged for
magnesium's טוב products. For creatine, an independent pass over all 19 טוב rows in
Product doc §4 shows the caveat is `third_party_verification` alone (7 rows),
`third_party_verification` + `price_fairness` together (8 rows), `price_fairness`
alone (3 rows: Klean Athlete, MegaFood, Sports Research), or
`dose_adequacy` + `third_party_verification` + `price_fairness` together in exactly one
row (MyProtein Creapure Micronised Capsules, row 14) — 7 + 8 + 3 + 1 = 19. `dose_adequacy`
therefore co-occurs in exactly one of the 19 rows. `form_absorption`
and `label_transparency` never appear as a טוב caveat in the current corpus (form
FLAG only occurs on the two לא מומלץ HCl products; label FAIL only on the four לא
מומלץ zero-quantification products) — so this caption names third-party verification
and price fairness specifically, and states the dose co-occurrence as occasional
("ולעיתים גם"), not as a given the way magnesium's caption did (where all three טוב
products carried dose too). VM field: `recommendationTierCaptions.good`.

**לא מומלץ**
```
מוצרים שנכשלים בלפחות אחד מספי הקנייה.
```
Provenance: direct restatement of `fails` (Product doc §3, unchanged). Same generic
line as magnesium's — the predicate is identical and geography/product-agnostic. VM
field: `recommendationTierCaptions.not_recommended`.

---

## Slot 2 — The headline finding

Creatine's headline is structurally different from magnesium's (an empty top tier).
Here the top tier is populated, but **only by worldwide reference brands** — the
honest structural fact is that the Israeli shelf cannot reach the top two tiers
today, for one specific, nameable reason. Framed to be honest without blame, and to
name the mechanism (a testing-infrastructure gap) rather than imply a quality
verdict on the products themselves.

**Title:**
```
אף מוצר מהמדף הישראלי לא אומת מול מאגר בדיקת צד שלישי.
```

**Body (2 short paragraphs):**
```
מתוך 18 תוספי קריאטין מהמדף הישראלי ו-13 מותגי ייחוס עולמיים שנבדקו, שבעה
מהמותגים העולמיים אומתו ישירות מול מאגר NSF Certified for Sport. אף אחד
מ-18 המוצרים הישראליים לא אומת מול מאגר כזה: חלקם מציגים טענת בדיקה בדף
המותג בלבד בלי אימות מול המאגר עצמו, וחלקם לא נושאים טענת בדיקה כלל.

בדיקת צד שלישי היא רק אחד מששה דברים שהמדריך בודק. מוצר מהמדף הישראלי
יכול להיות חזק מאוד במינון, בצורה הכימית ובשקיפות התיוג, ועדיין להישאר
מחוץ לבדיקה העצמאית פשוט כי אף גוף הסמכה עדיין לא בדק אותו. זהו פער
בתשתית הבדיקה של השוק הישראלי. הוא אינו ממצא על איכות המוצרים עצמם. ברגע
שמוצר מהמדף הישראלי יעבור בדיקה כזו ויאומת מול מאגר עצמאי, הוא יוכל לעמוד
באותם ספי קנייה כמו מותגי הייחוס העולמיים.
```
Provenance: the 0/18-vs-7/13 figures and the "mechanical consequence of the
certification data, not a Product judgment call" framing are Product doc §6 note 1,
independently re-confirmed exact by Nutrition co-sign §2 ("Confirmed exactly as
stated. This is the single most consumer-relevant fact in this guide and it is
accurately derived."). The constructive second paragraph does not invent a claim: it
restates the mechanism from Product doc §6 note 1 in the forward direction (a
verified Israeli product would clear the same bars) — a direct logical consequence
of the same rule, not a new assertion. The two-sentence "X. הוא אינו Y." pattern
matches the house style already shipped in `suppressedBarsDisclosureHe` and
`cannotAssessSectionIntroHe` (magnesium-guide-data.ts). No blame language, no "buy
imported" push — states the mechanism and stops. `third_party_verification` cert
language ("אומת מול מאגר") matches the exact term already live in
creatine-page-data.ts and the Product/Nutrition docs' own vocabulary. VM field: new
`headlineFinding.title` / `headlineFinding.body[0..1]` (parallel structure to
magnesium-guide-data.ts's `headlineFinding`, populated with creatine's own fact
rather than an empty-tier fact).

---

## Slot 3 — "לא ניתן להעריך" section line (California Gold Nutrition)

Written product-agnostic (no name, no count baked in), matching the magnesium
guide's own established practice for this exact slot (`cannotAssessSectionIntroHe`)
— the wording should still be correct if a second per-unit-dose product enters the
corpus on a future scrape.

```
מוצרים שמפרטים כמות קריאטין לכמוסה או למנה בודדת, אבל לא מציינים כמה
כמוסות או מנות לוקחים ביום. מוצרים כאלה לא נכנסים לאף אחת מארבע הקבוצות
למעלה. בלי מספר הכמוסות היומי אי אפשר לדעת כמה קריאטין מגיע בפועל ביום,
וגם אי אפשר לבדוק את הוגנות המחיר למנה יומית. זהו פער מידע על המוצר
עצמו. הוא אינו ממצא שפוסל אותו.
```
Provenance: Product doc §5 ruling (California Gold Nutrition's per-unit-dose /
undisclosed-daily-count pattern — the exact `cannot_assess` case, "no bar on this
product is FAIL... routes to `cannot_assess`... a genuine unknowable is never
presented as an actionable negative"), and Nutrition co-sign §3's required build
correction that `price_fairness` must also display CANNOT-VERIFY for this product
(the ₪0.97 figure is a different-question computation, not a valid price-fairness
answer) — hence this line explicitly states the price-fairness consequence
("וגם אי אפשר לבדוק את הוגנות המחיר למנה יומית"), not just the dose consequence,
so the copy doesn't imply a price figure exists when the ruling says it must not
display. The closing two-sentence pattern ("זהו פער מידע... הוא אינו ממצא...")
reuses the magnesium guide's own established `cannotAssessSectionIntroHe` pattern
verbatim in structure. The live product's own existing row copy
(`creatine-page-data.ts`: "מספר הכמוסות היומי הנדרש להגיע ל-3 גרם לא מפורט, כך
שהמינון היומי בפועל לא ידוע") is the direct source for the per-unit/no-daily-count
framing, generalized here to product-agnostic language. VM field: new
`cannotAssessSectionIntroHe`.

---

## Slot 4 — Hero mascot alt text

Asset TBD (owner-supplied, to be optimized + self-hosted per the magnesium
precedent). Alt text only — describes the character and scene, makes no health or
efficacy claim about creatine.

```
לומו, דמות בארי, בוחן דרך זכוכית מגדלת אבקת קריאטין וכמה מהצורות שלה,
כשמסביבו בקבוקוני תוספים, כפית מדידה וכמוסות קריאטין.
```
Provenance: mirrors the shipped magnesium hero alt structure exactly ("לומו, דמות
בארי, בוחן דרך זכוכית מגדלת [תחום] ... כשמסביבו/כשלצידו [סביבה]") — same character,
same "examining through a magnifying glass" framing (Character Bible: LUMO =
examination/scrutiny). "וכמה מהצורות שלה" (and some of its forms) reflects the real
form diversity in the corpus (powder, capsules, gummies, tablets — Product doc §4)
without naming any brand or claiming one form is better. No dosage, safety, or
efficacy claim anywhere in the sentence. VM field: `heroImage.alt` (new
`creatine-guide-data.ts`, parallel to `magnesium-guide-data.ts:433`).

---

## Slot 5 — Per-row expander label

Reuses the magnesium guide's "show the detail" pattern verbatim — same component
family (`GuideGaugeGeometry`/`GuideLadderGeometry`, generically "סולמות" — scales),
same two-state toggle text. No creatine-specific rewording needed since the label
describes the UI mechanism (expand/collapse the threshold visuals), not the bar
content itself, and that mechanism is identical across both guides.

**Collapsed state (click to open):**
```
הצג את הסולמות
```
**Expanded state (click to close):**
```
הסתר את הסולמות
```
Provenance: verbatim port of `expanderLabels` from `magnesium-guide-data.ts:531-532`
(magnesium_guide_tier_copy_v1.md Slot 4's own provenance note applies unchanged: the
term matches the existing internal gauge/ladder naming without exposing it as
jargon, and the site's other short verb-first micro-copy register). VM field:
`expanderLabels.{collapsed,expanded}`.

---

## Voice self-check

- **"X, not Y" antithesis:** zero instances anywhere in the delivered strings —
  confirmed by the deterministic gate (below), not a manual scan. One early draft of
  the cannot-assess line (Slot 3) did trip the gate on a comma-before-"לא" — see the
  gate re-run log below; the shipped version splits that into two sentences instead.
- **Em-dashes:** zero.
- **Banned engine jargon** (דירוג/ניקוד/NOVA/BSIP/cap/floor/מנוע/אלגוריתם): zero.
- **Literal tier words in prose** (מומלץ מאוד/מומלץ/טוב/לא מומלץ): zero — every
  caption describes its tier's qualifying condition without naming the tier; the
  tier HEADING (rendered separately, a field value, per EXCEPTION-003) supplies the
  name.
- **"סף/ספי הקנייה":** retained and used (Slots 1, 2) — approved guide-specific
  term, not banned.
- **"NSF Certified for Sport" untranslated:** kept as-is (advisory `english` leak
  only, never hard-fails) — matches the ~15 existing live instances in
  `creatine-page-data.ts`; translating it would break continuity with the
  cert-name-as-proper-noun convention already shipped.
- **No health/efficacy claim** anywhere in the 5 slots, including the hero alt text.
- **No fabricated fact:** every number (18, 13, 7) traces to Product doc §6 /
  Nutrition co-sign §2; every mechanism claim (why Israeli products cap at טוב, why
  California Gold Nutrition is cannot-assess, why its price also can't display)
  traces to a specific section cited above, not invented for the copy.

### Deterministic gate run — `hebrew_readability.py::analyze(text).is_clean`

Per the hard constraint, the FULL analyzer (not a substring scan) was run on every
one of the 11 delivered strings, loaded from a UTF-8 file to avoid the known
`python -c` Hebrew-corruption gotcha. First pass caught one real HARD failure
(antithesis, in the cannot-assess line's draft); fixed and re-run clean.

**First pass (draft):**

| String | is_clean | HARD leaks |
|---|---|---|
| cannot_assess_intro (draft) | **False** | `antithesis: ", לא"` (comma directly followed by "לא" at "...לוקחים ביום, לא נכנסים...") |
| all other 10 strings | True | none |

**Second pass (shipped version, after splitting the sentence in two):**

| String | is_clean | HARD leaks | ADVISORY leaks |
|---|---|---|---|
| tier_very_recommended | **True** | none | none |
| tier_recommended | **True** | none | none |
| tier_good | **True** | none | none |
| tier_not_recommended | **True** | none | none |
| headline_title | **True** | none | none |
| headline_body0 | **True** | none | `english: NSF, Certified, for, Sport` |
| headline_body1 | **True** | none | none |
| cannot_assess_intro | **True** | none | none |
| hero_alt | **True** | none | none |
| expander_collapsed | **True** | none | none |
| expander_expanded | **True** | none | none |

All 11 strings return `is_clean = True`. The only leaks of any kind are the 4
ADVISORY `english` tokens in `headline_body0` ("NSF Certified for Sport"), which
never affect `is_clean` (per the module's own `_ADVISORY_LEAK_KINDS`) and match
existing, already-shipped precedent for that exact cert-name phrase.

Commands run:
```
python run_creatine_gate.py
  (loads C:\Bari\integrations\clients\hebrew_readability.py by absolute path,
   registers it in sys.modules before exec_module to avoid a Python 3.14
   dataclass/importlib interaction bug, then calls analyze() on each of the
   11 strings in creatine_copy_strings.py)
```

---

## Return Contract

```json
{
  "task": "TASK-504-creatine-4tier-recommendation-content-gate1",
  "agent": "Content Agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\content\\creatine_guide_tier_copy_v1.md",
      "change": "New file. Gate-1 Hebrew copy draft for all 5 requested slots (4 tier captions, headline finding, cannot-assess line, hero alt text, expander labels). No code, rubric, or data file touched."
    }
  ],
  "counts": {
    "slots_authored": 5,
    "strings_delivered": 11,
    "strings_is_clean_true": 11,
    "strings_is_clean_false_in_final": 0,
    "hard_fails_found_and_fixed_during_drafting": 1,
    "banned_antithesis_instances_in_final": 0,
    "em_dash_instances_found": 0,
    "banned_jargon_instances_found": 0,
    "literal_tier_words_in_prose": 0,
    "advisory_english_leaks_in_final": 4,
    "source_docs_read": [
      "03_operations/reports/product/creatine_guide_recommendation_tiers_v1.md",
      "01_framework/nutrition/creatine_guide_tier_cosign_v1.md",
      "01_framework/nutrition/creatine_evidence_cosign_v1.md",
      "03_operations/reports/content/magnesium_guide_tier_copy_v1.md",
      "C:\\bari_wt_t504\\bari-web\\src\\lib\\guides\\magnesium-guide-data.ts (read in full)",
      "git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts @ 9546878cf90f069fe12c1467d8d12966b40221cf (997 lines, read in full)"
    ]
  },
  "commands_run": [
    {"cmd": "git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts > scratchpad/creatine-page-data.ts", "exit_code": 0},
    {"cmd": "python run_creatine_gate.py (against creatine_copy_strings.py, all 11 strings)", "exit_code": 0, "result": "ALL_CLEAN = True"}
  ],
  "not_done": [
    "No code or data-file (creatine-guide-data.ts does not exist yet) edit applied — draft only, per instruction",
    "Gate 2 (Adversarial QA) sign-off not yet requested",
    "Product Agent's own outstanding item — Nutrition D7 co-sign is now IN HAND (creatine_guide_tier_cosign_v1.md, co-signed with one non-tier-affecting price-display correction) — but the standing C3 independent-challenge pass on Product's bar-state assignments (Product doc §9.2) has not been confirmed complete; not this Content doc's scope to verify",
    "Hero mascot asset itself (image file) not created or sourced — alt text only, asset is TBD per the brief",
    "VM field names (headlineFinding, cannotAssessSectionIntroHe, heroImage.alt, expanderLabels, recommendationTierCaptions) are proposed by direct analogy to the shipped magnesium-guide-data.ts structure, not confirmed with Frontend for the not-yet-built creatine-guide-data.ts",
    "Per-product insightLine/rowVerdict copy for the 31 individual creatine products is NOT authored here — brief scoped this doc to the tier-layer + headline only, per-product copy already exists (gate-approved) in the live creatine-page-data.ts comparison page and was not touched"
  ],
  "acceptance_test": {
    "spec": "Author Hebrew copy for 4 tier captions (with מומלץ מאוד written as a populated, not empty, tier), the headline structural finding (0/18 Israeli third-party-verified, framed honestly and constructively), the California Gold Nutrition cannot-assess line, hero mascot alt text, and expander labels — matching Tom-Bari voice rules, grounded in the co-signed Product/Nutrition tier docs, with zero literal tier words in prose and is_clean=True run via the actual hebrew_readability.py analyzer (not a substring scan) on every delivered string.",
    "result": "PASS — all 5 slots authored (11 total strings) with per-slot provenance citing exact source doc/section; the τוב caption was independently re-derived from Product doc §4's actual 19-row caveat-set data (third-party + price, not form/label/safety, correcting for the real difference from magnesium's τוב drivers) rather than copied from the magnesium precedent; the headline finding states the 0/18-vs-7/13 fact from Product doc §6 / Nutrition co-sign §2 with a constructive, non-blaming second paragraph that is a direct logical consequence of the same cited mechanism, not an invented claim; the cannot-assess line correctly reflects Nutrition's required price-fairness CANNOT-VERIFY correction (§3 of the cosign doc); one real HARD antithesis failure was caught by the deterministic gate during drafting (not by manual scan) and fixed by splitting the sentence; final gate run over all 11 strings returns is_clean=True with zero HARD leaks, confirmed by an executed script, not eyeballed."
  }
}
```
