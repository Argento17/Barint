# Adversarial QA Report — TASK-461 Phase-2 #7: BREAD copy overhaul (23 products)

**Verdict: GO_WITH_FIXES** (0 CRITICAL / 0 HIGH / 3 MEDIUM — all advisory; none block handover)
**Proposed status: RETURNED**

Challenger: adversarial-qa-agent (Opus, independent lane). Own origin/master fetch, own rank tables,
own re-derivation. Author report NOT consulted for truth — re-derived from parse + trace + baseline.

- CANDIDATE sha256 `67cddb3c81b0b6f7e80d3c40ff06049e6b8fda23b55fb2401d0dbbd2cd07a56c` — **MATCHES brief.**
- BASELINE `bread_frontend_v4.json` fetched independently via `git show origin/master:...` (86,241 bytes).

---

## Track V — Verification

### V1. Field isolation — PASS (23/23)
- Only `insightLine` + `rowVerdict` differ. Key-sets identical 23/23.
- `_meta` byte-identical. `score`/`grade`/`rank`/`_hash_no_rank`/`confidence`/`confidence_level`: **zero mismatches** across all 23.
- Zero score movement; zero structural change. Non-copy surface untouched.

### V3. Hygiene — PASS
| Check | Baseline | Candidate | Verdict |
|---|---|---|---|
| em dashes | 47 | **0** | PASS |
| engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר…) | — | **0** | PASS |
| "ציון" stamp | 23/23 | **0/23** | PASS (full removal proven) |
| "נקודות"/literal score | — | **0** | PASS |
| antithesis "לא X אלא Y" | — | **0 real** (1 false-positive, see below) | PASS |
| R4 recommendation drift (כדאי/שווה+לקנות/לבחור/לרכוש) | — | **0** | PASS |
| OFF refs | — | **0** | PASS |
| openings unique (first 3 words) | — | **46/46 unique** | PASS |
| 5-gram repetition >2× | — | **NONE** (max ≤2) | PASS |
| panel numbers | — | **5** strings, each a fired driver (see V2) | PASS w/ note |

**Antithesis false-positive (r16 rowVerdict):** regex hit "מלא, אלא ש…" — this is the adjective מלא
("whole") followed by the connective אלא-ש ("except that / however"), NOT define-by-negation. Clean.

### V4. hebrew_readability (LIVE, offline) — 45/46 clean
- 1 hit: **r1 rowVerdict "27.5"** flagged `SCORE MECHANIC exposed: '27.5'`. This is the protein gram
  value ("27.5 גרם חלבון"), r1's verified shelf-MAX protein driver — a decimal-with-grams tripping the
  score-mechanic regex (known heuristic false-positive class). It is the story, not a bare score. See M2.

### Panel-number audit (5, each is the fired driver — brief expected 4; the 5th is defensible)
- r1 `27.5` = protein, verified shelf-MAX (driver). r7 `500` = sodium, verified shelf-MAX (driver).
- r8 `14` = "יותר מ-14 גרם סיבים" fiber 14.2, scoped shelf-high for wheat/rye (driver).
- r17 `23` = flax 23% (composition, the keto structural story). r20 `4` = "מתחת ל-4 גרם סיבים" fiber 3.9 (the catch).
- All 5 are drivers/composition, none are nutrition-panel recitation. Acceptable.

---

## Rank tables (my independent derivation, candidate)

**Sodium (ascending, mg):** 126(r1) · 288(r16) · 295(r13) · 298(r15) · 304(r8) · 340(r10) · 343(r3) ·
347(r21) · 352(r22) · 366(r12) · 380(r4,r5,r20) · 382(r2) · 385(r17) · 390(r6) · 400(r9,r11,r14) ·
404(r18) · 423(r19) · 434(r23) · **500(r7 MAX)**.
**Fiber (desc):** 18.5(r1) · 17.4(r17) · 14.2(r8) · 12.4(r6) · 11.4(r10) · … · 3.0(r13,r14) · **2.9(r15 MIN measured)** · [r23 null].
**Protein (desc):** 27.5(r1 MAX) · 23.7(r17) · 13.9(r22) · 13.8(r9) · … · **5.2(r7 MIN)**.
**Kcal (desc):** 266(r18 MAX) · 263(r23) · 259(r16) · … · 192(r1) · **191(r7 MIN)**.

---

## Claim-by-claim truth audit — 46/46, all hotspots TRUE

**(a) Emulsifier controversy ×4 — ALL CORRECTLY APPLIED.**
Every cited product has E471 מונו ודיגליצרידים tiered `contested` in its OWN `d4_additives`, and the
engine's own `explanation_he` for E471 states "קיים דיון מדעי על בטיחות השימוש בהם." Copy rides the
engine's classification — not an invented claim.
- r9 "שני המתחלבים, אחד מהם עדיין במחלוקת מחקרית" — has E481+E471(contested). ✓
- r10 "שני מתחלבים, אחד מהם שנוי במחלוקת" — E481+E471(contested). ✓
- r14 "אחד המתחלבים… עודנו שנוי במחלוקת" — E481+E471(contested). ✓
- r22 "שלושה מתחלבים… ביניהם מונו ודיגליצרידים שהמחקר עוד דן בו" — E481+E472e+E471(contested), names E471. ✓
- **Stamp risk: acceptable.** 4 occurrences, 4 genuinely distinct constructions; no verbatim repeat, no 5-gram flag.

**(b) Sodium triangle — mutually consistent.**
r1 "פחות ממחצית הנתרן של כל לחם אחר": 126 < ½·288(min-of-others=144). ✓ · r7 "500, הגבוה במדף כולו" =
verified MAX. ✓ · r23 challah "הנתרן מטפס כמעט לראש" = 434 = 2nd-highest of 23. ✓ All three consistent.

**(c) r1 (S 94.8):** "שיא החלבון 27.5" (MAX ✓) · "שיא הסיבים" (18.5 MAX ✓) · rank-1 ✓ · sodium min ✓.
"ראש המדף בפער גדול" — see M1 (2.1pt to r2 is the one soft over-claim).

**(d) r16 truth-fix REVERSAL — bulletproof.**
Parse: "קמח שיפון מלא (36% ממשקל הלחם, **80% ממשקל הקמחים**)" is the FIRST ingredient; wheat is 2nd.
BASELINE (live) copy claimed "**ארבעים אחוז קמח חיטה לבן הוא הרכיב הגדול / קמח לבן הוא הרכיב הדומיננטי**"
= FALSE (white is the minority flour). CANDIDATE: "ארבע חמישיות מהקמח… שיפון מלא" (=80% ✓) / "רוב מוחלט
של שיפון מלא" (✓). **Candidate matches the parse; baseline was wrong. Reversal correct.** Stale
contradiction in `expansion.comparisonContext` ("קמח חיטה לבן (40%)… כרכיב הדומיננטי") **verified
byte-identical/untouched** (out of copy scope, correctly routed).

**(e) Composition/percentage sweep — 13/13 TRUE vs parse:**
r3 ⅔ loaf whole (66% ✓) · r4 90% whole flours + 6% seeds + rye-sourdough (✓) · r5 40% white (✓) ·
r6 ⅔ wheat ⅓ rye, all whole (66/34 ✓) · r7 ½ cracked rye grains (50% ✓) · r8 80% whole flours (60+20 ✓) +
"14g שיא לחמי החיטה והשיפון" (scope excl r1 seed / r17 keto is legitimate; 14.2 = scoped max ✓) ·
r9 83% whole (✓) · r16 ⅘ rye + 2% mahmetzet + 3% nuts (80% / 2% / 3% ✓) · r17 23% flax keto, gluten-isolate
principal (✓) · r18 7% walnuts on white base (✓) · r19 70% spelt (✓) · r20 half-half, <4g fiber (50/50, 3.9 ✓) ·
r21 ¾ wheat ¼ rye, no white, "מפספס בכלום" 68.0 vs 69.0=1.0 tie (✓) · r22 ¼ seeds, 3 emulsifiers, protein top (25.4% / E481+E472e+E471 / 13.9 top-of-grain ✓).

**(f) 69.0 trio (r18/r19/r20):** all exactly 69.0; "שלושת הלחמים שקיבלו כאן תוצאה זהה" / "חולק את דירוגו
עם שני שכנים" — consistent, each names the shared result honestly. ✓
**(g) 83-knot (r8 83.1 / r9 83.0 / r10 83.0):** "שלישייה שנוגעת/צמודה" ✓; differentiated only by real
deltas (r9 protein 13.8, r10 inulin/fiber, r8 fiber 14.2 + low sodium). ✓
**(h) r2 "היחיד בחמישייה הפותחת בלי אף תוסף":** top-5 additive counts {r1:2, r2:0, r3:1, r4:1, r5:2} —
r2 is the sole 0-additive product in the top 5. ✓ · r15 "הנמוכים ביותר שנמדדו" fiber 2.9 MIN measured
(r23 null → "שנמדדו" hedge correct) ✓ · r13 "הסיבים נמוכים" (non-superlative) ✓ · r12 "מהנמוכים במדף"
fiber 3.3 (among lowest) ✓.
**(i) Soft truth fixes (r2/r7/r20/r21):** all new claims match parse; ✓.
**(j) Data flags:** uniform fat=0.25 on 16/23 — **verified: ZERO fat claims in any copy string** (fat
cited 0×). r11 d4 under-extraction and r23 disclaimer-tail in ingredients: **no copy claim leans on
either** (r23 copy uses sodium 434 + fiber-null, both real panel values). ✓
**(k) r3 kids-framing / r17 keto-framing:** r3 "מיתוג הילדים החלטה שיווקית, הפרופיל מתאים לכל שולחן" —
grounded (100% whole flour, minimal additives; brand claim is orthogonal to nutrition). r17 "מוצר הנדסי
שמתארח על מדף הלחם" — grounded (gluten isolate is the principal structural ingredient; not a grain bread). ✓

---

## Track C — the owner's bar

- **Stance + driver, all 46:** every line opens with an opinion/finding, lands a driver. No number-recitation
  templates. Insight-first standard met.
- **High-grade shelf without manufactured drama:** the 83-knot and 69-trio are framed AS ties ("נוגעת זו
  בזו", "תוצאה זהה", "מפספס בכלום"); clustering handled honestly; no invented differentiation. Sub-2pt gaps
  are called ties. This is the exact discipline the shelf required.
- **Brand-adversarial claims bulletproof + proportionate:** kids-marketing (r3), כוסמין-לבן health-sound
  de-halo (r12 "מי שהגיע בגלל צליל הבריאות של המילה כוסמין"), mini-mahmetzet 2% (r16 "המחמצת שבשם קיימת אבל
  זעירה, שני אחוזים") — each grounded in parse, none over-reach.
- **Natural Hebrew:** reads as a smart friend's verdict; RTL clean; no translationese.

**Weakest 3 (Track C):**
1. **r1 "ראש המדף בפער גדול"** — the 2.1pt gap to r2 is barely above the ≤2pt noise floor; "פער גדול"
   is a soft over-claim *against the adjacent product* (it is true against the whole shelf on substance:
   2.2× protein, 2.9× fiber). → **M1.**
2. **r1 rowVerdict "27.5"** — the sole hard-gate hit; defensible as the shelf-MAX protein driver, but it
   is the one string that trips hebrew_readability. → **M2.**
3. **r8 / r22 scoped superlatives** ("שיא לחמי החיטה והשיפון", protein "בצמרת") — TRUE only under a
   scope that silently excludes r1 (tahini/seed) and r17 (keto). Defensible and consistently applied, but
   the scope is implicit to the reader. → **M3.**

---

## Findings

### CRITICAL — none.
### HIGH — none.
### MEDIUM (advisory; do NOT block handover)
- **M1 (proportionality, Track C):** r1 "פער גדול" for a 2.1pt gap to r2 (noise floor is ≤2pt).
  True against the full shelf on substance; borderline against the neighbor. Routes to: content-agent (optional soften). Quote: "ראש המדף בפער גדול."
- **M2 (leakage heuristic, Track V):** r1 rowVerdict "27.5" is the single hebrew_readability hit
  (score-mechanic regex on decimal). Defensible driver-number (shelf-MAX protein). Routes to: content-agent (accept as-is or drop the decimal); note for TASK-453 false-positive backlog. Quote: "…מייצרים 27.5 גרם חלבון…"
- **M3 (scoped superlative, Track C):** r8 "שיא לחמי החיטה והשיפון" and r22 protein "בצמרת" rely on an
  implicit scope excluding r1/r17. Consistent + honest, but scope is unstated. Routes to: content-agent (monitor). 

### Pre-existing (NOT introduced — noted, not a finding against this candidate)
- r16 `expansion.comparisonContext` retains the stale "קמח לבן כרכיב הדומיננטי (40%)" contradiction —
  byte-identical to baseline, out of the 2-field scope, already routed. Verified untouched.

---

## Summary
Track V: **GREEN** (isolation 23/23, hygiene all-pass, 45/46 readability with 1 defensible FP).
Track C: **PASS** (46/46 stance+driver; ties honest; brand-adversarial claims grounded; 4× contested-
emulsifier claim all engine-backed; the load-bearing r16 reversal is correct and bulletproof).
No CRITICAL, no HIGH. 3 MEDIUM advisories, none blocking. **GO_WITH_FIXES → propose RETURNED.**
