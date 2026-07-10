# TASK-461 Phase-2 #5 — SNACKS copy overhaul, author report (Content Agent)

**Status: DRAFT until Adversarial QA.** Proposed lifecycle: RETURNED.
Date: 2026-07-02. Author lane: Content Agent (this session, no subagents spawned).

## 1. Isolation proof (concurrency protocol)

- Baseline = **origin/master** via `git show origin/master:bari-web/src/data/comparisons/snacks_frontend_v5.json`
  (read-only; local tree NEVER read for data).
- Blob sha (git ls-tree): `4febff7befeed04274ae00113ea3de6ba771506c` (mode 100644, 92,268 bytes).
- Baseline file sha256: `afd691b4fe011cedc03448d9136d0b2f3c52f9618247504f485ee79ff45067dd`.
- Candidate artifact: `snacks_copy_overhaul.json`,
  sha256 `406d8363e40aa2d7473881b152b98ddd2fff16268c9622ee4d770530b5e968a8`.
- **Zero git writes; nothing under C:\Bari touched.** All git commands were read-only
  (`ls-tree`, `show`); all outputs live in the session scratchpad.
- JSON round-trip proven **byte-identical** before editing (`roundtrip_byte_identical: true`),
  so the candidate preserves origin formatting exactly.
- Structural walk over both trees: **42 changed leaf fields = 21 × {insightLine, rowVerdict};
  0 diffs anywhere else** (`isolation_bad_diffs: []`). Scores, grades, ranks, nutrition,
  `_meta`, `_hash_no_rank`, expansion blocks: byte-identical.

## 2. Metrics (script-derived, `build_snacks_copy.py`)

| Metric | Baseline | Candidate | Bar |
|---|---|---|---|
| Em/en dashes (both fields) | 55 | **0** | 0 |
| Engine vocabulary (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/נקודות) | present | **0 hits** | 0 |
| Buy-verb drift R4 (כדאי/שווה/לקנות/לבחור/לרכוש) | — | **0 hits** | 0 |
| Opening 3-word uniqueness | template-repetitive | **42/42 unique** (21 IL + 21 RV) | unique |
| Products with panel-number digits | 21/21 (100% recitation) | **4/21** | ≤4 |
| 5-gram census (R3) | — | **max repetition = 1**; no editorial phrase >1× | ≤2× |
| Grade distribution (unchanged) | B1 C2 D6 E12 | B1 C2 D6 E12 | identical |
| Score dist (unchanged) | n=21, min 14.1, max 66.9, median 32.4, stdev 15.38, most-common 66.9(×1) | same | identical |

Panel-number products, each a verified extreme (rule 2 justification):
1. **snk-001** — 23 g fiber /100g = shelf max (22.9 vs next 13.7) alongside shelf-min sugar (9.9 vs next 21.9).
2. **snk-012** — dual shelf max: protein 14 g (next 12.1) and 540 kcal (next 495).
3. **snk-017** — sodium 416 mg = shelf max (next 372).
4. **snk-021** — saturated fat 18 g = shelf max (18.1 vs next 16.2), in the last-ranked product.

## 3. Superlative rank-check table (all script-verified vs full 21-product corpus)

| Product | Claim in copy | Ground truth |
|---|---|---|
| snk-001 | שיא הסיבים; הסוכר הנמוך ביותר; "רחוק מתחת לכל מתחרה" | fiber 22.9 max (2nd: 13.7); sugar 9.9 min (2nd: 21.9) |
| snk-004 | החטיף המתוק ביותר; הרשימה הקצרה ביותר; sugar ≈ מחצית המשקל | sugar 50.5 max (2nd: 47.6); 2 ingredients vs 3 (Shaked-Tavor trio) / 4 (snk-002); 50.5 g/100g |
| snk-002 | תמרים שלושה רבעים מהחטיף; אפס ממתיק מוסף | label: תמרים 76%; "ללא תוספת סוכר" on label |
| snk-010 | מדורגת ראשונה מבין השלוש; שומן רווי הנמוך במשפחה | trio scores 47.0 > 41.6 > 33.0; sat 6.1 vs 7.1 / 16.2 |
| snk-008 | מעט יותר שומן רווי מגרסת השקדים | sat 7.1 vs 6.1 |
| snk-009 | פי שניים ויותר שומן רווי מאחיותיה; מהגבוהות בקטגוריה | 16.2 ≥ 2×7.1 and ≥ 2×6.1; shelf rank #2 sat |
| snk-005 | המוביל בחלבון מבין חטיפי התמרים | 9.6 vs next-in-family 8.3 (family = date-based: snk-002/003/004/005/008/009/010) |
| snk-006 | דבש 3%; סוכר לבן לפניו; שישים אחוז שיבולת שועל | label list order; 60% declared = highest grain share on shelf |
| snk-007 | תאום; מייפל 2%; פער קטן מכדי להכריע | scores 36.2 vs 36.1 (0.1 = tie honored); label 2% |
| snk-012 | שיא חלבון + שיא קלוריות; בוטנים ~40%; צמד סירופי סוכר | 14.0 max, 540 max; label 39%; אינוורטי + מלטוז |
| snk-013 | דבש 1% + מייפל 1%; שומן צמחי וסוכר שני ושלישי; סיבים מהדלים | label; fiber 5.0 = 2nd-lowest measured |
| snk-014 | 74% שוקולד; דגן ~חמישית; סוכר ראשון בשוקולד | label: 74% / 19%; sub-list opens with סוכר |
| snk-015 | אחת הרשימות הארוכות; מלח מהגבוהות; כמעט לשיא | sodium 372 = #2 (max 416); longest ingredient string on shelf (eyeball, hedged phrasing) |
| snk-016 | תאום הגרסה המרירה; 74% שוקולד חלב; סוכר פותח רכיביו | label: 74% / 19%; sub-list opens with סוכר |
| snk-017 | שיא המלח של המדף; חלבון בין הגבוהים; בוטנים ~שליש | sodium 416 max; protein 12.1 = #2; label 29.3% |
| snk-018 | פירות 1% + 1%; שני סוגי סוכר חום | label: צימוקים 1%, שזיפים 1%; סוכר חום + סוכר חום לא מזוקק |
| snk-019 | שלישי מהסוף; שוקולד ראשון; צמד סירופי גלוקוז | rank 19/21; label order; גלוקוז-פרוקטוז + גלוקוז |
| snk-020 | סיבים הדלים ביותר שנמדדו; דגן מלא עשירית | fiber 3.1 = min of 20 measured (snk-018 null excluded — hence "שנמדדו"); label 10% |
| snk-021 | שיא השומן הרווי; מקום אחרון; דגן מלא ~שמינית | sat 18.1 max (2nd: 16.2); rank 21/21; label 13% |

Deliberately NOT claimed: snk-018 sodium-min (panel value 0.2 mg suspect, see §6); any cross-pair
rank explanation for snk-003 vs snk-005 (near-identical panels but different trace categories —
copy differentiates by composition only); "snack-bar ceiling 70/B" (historical finding; current
artifact top is 66.9/B — copy references leadership only, no ceiling claim).

## 4. Family map (rule once, differentiate by real deltas)

| Family | Members | Rule / differentiators |
|---|---|---|
| Shaked Tavor coated trio (65/19/16 structure) | snk-010, snk-008, snk-009 | Formula ruled once at snk-010 ("הנוסחה של השלישייה"); differentiated ONLY by the paste: almond = lowest sat (6.1), cashew middle (7.1), coconut = outlier (16.2, "פי שניים ויותר") |
| Nature Valley crunchy twins | snk-006, snk-007 | Ruled at snk-006 (sugar-before-honey, 3%); snk-007 framed as twin, honest tie (Δscore 0.1), maple 2% |
| Nature Valley coated pair | snk-015, snk-017 | Differentiated by real deltas: snk-015 = engineered long list + sodium #2; snk-017 = sodium shelf-max + protein #2 |
| Slims Delis 74% twins | snk-014, snk-016 | Structure ruled at snk-014 (74/19 inversion); snk-016 framed as twin, differentiated by milk chocolate + kids branding |
| Korny trio | snk-019, snk-020, snk-021 | snk-019 = chocolate-first + sugar in every sub-component; snk-020 = fiber-min + 10% whole grain; snk-021 = sat-max + last place |
| HaShuk HaKulinari granola pair | snk-013, snk-018 | Same 1%-headline trick told differently: snk-013 = name-vs-taste providers; snk-018 = fine-print vs package name |
| FREE date mixes | snk-003, snk-005 | snk-003 = trail-mix composition/density; snk-005 = family protein leader; no rank comparison between them (see §3 note) |

## 5. Before/after ×4

**snk-001 (rank 1, B) — insightLine**
- Before: "החטיף היחיד במדף שמשאיר אתכם שבעים: 23 גרם סיבים ל-100 גרם, ובלי הסוכר שמלווה את כל היתר."
- After: "חריג לטובה במדף שרובו ממתק: שיא הסיבים של הקטגוריה, 23 גרם ל-100 גרם, לצד הסוכר הנמוך ביותר בה."

**snk-004 (rank 3, C) — rowVerdict**
- Before: "שני רכיבים, וזהו: 84% תמרים ו-16% שוקולד מריר ב-100% קקאו — בלי סירופ, בלי תוסף, בלי סוכר מוסף. זו ההרכבה הכי נקייה בקטגוריה, ועם 13.4 גרם סיבים היא גם מזינה יותר מרוב המדף. מה שמחזיק אותה באמצע ולא גבוה יותר הוא הסוכר: 50.5 גרם ל-100 גרם, כולו מהתמר, לצד 4 גרם חלבון בלבד. מזון אמיתי ומתוק מטבעו — לא נשנוש קליל."
- After: "הפשטות כאן אמיתית: רוב מוחלט של תמרים ומעליהם ציפוי מריר שאין בו גרם ממתיק. אותה פשטות גם קובעת את הגבול, כי התמר מביא איתו סוכר טבעי שמגיע לכמחצית ממשקל החטיף, יותר מכל מוצר אחר בקטגוריה. מזון אמיתי ומתוק מיסודו, מהסוג שנאכל נכון לאט ובמנות קטנות."

**snk-017 (rank 16, E) — insightLine**
- Before: "416 מ\"ג נתרן ל-100 גרם — הגבוה במדף — בחטיף שעל פניו נראה בריא."
- After: "שיא המלח של המדף כולו נמצא דווקא כאן: 416 מ\"ג נתרן ל-100 גרם, בחטיף שנשען על תדמית של שיבולת שועל ובוטנים."

**snk-020 (rank 20, E) — rowVerdict**
- Before: "נמכר כחטיף דגנים, אבל שוקולד החלב הוא הרכיב הראשון (24%) והדגנים רק שניים (19%). 34 גרם סוכר, ורק 3.1 גרם סיבים — מהנמוכים במדף. זה ממתק שוקולד עם פצפוצי דגנים, לא חטיף דגנים עם ציפוי."
- After: "המקום הראשון ברשימת הרכיבים שייך לשוקולד החלב, ואחריו קמחים ממותקים ושני סירופים. הדגנים המלאים נכנסים רק בעשירית מהמוצר, ותכולת הסיבים, הנמוכה ביותר שנמדדה בקטגוריה, מסגירה כמה מעט דגן באמת יש כאן. ממתק שוקולד במהותו, עם נגיעה דגנית בשוליים."

## 6. Data-lane flags (outside 2-field scope; NOT touched)

1. **snk-018 sodium = 0.2 mg/100g** — near-certain unit/parse error (product carries E500ii and
   glucose syrup; 0.2 mg is implausible). Copy makes NO sodium claim for this product, and the
   snk-020 fiber-min claim is phrased "שנמדדו" because snk-018's fiber is null.
2. **snk-014 / snk-016 ingredient strings contain "????"** (corrupted tail segments). All claims
   for these two rest on the clean leading segments (74%/19%, sugar-first sub-lists).
3. **Stray characters in parses**: snk-010 ("...(19%),nשוקולד"), snk-013 ("nסודיום ביקרבונייט") —
   cosmetic scrape artifacts, no copy impact.
4. **snk-018 dietary_fiber_g = null** on a "verified" panel (R2: not narrated — no fiber/sodium
   claim exists for this product; the confidence chip already discloses).

## 7. Register conformance notes

- Insight-first: every block opens on the engine's finding (identity, label-vs-reality,
  family position, extreme) — never an ingredient count or panel row.
- No antithesis ("X, not Y" define-by-negation): removed from all baseline carriers
  (e.g., old snk-020 "זה ממתק... לא חטיף דגנים" → positive declarative "ממתק שוקולד במהותו").
- Indulgence-adjacent stance: no moralizing; date-family products credited honestly for clean
  composition while density is stated as fact; no health-halo granted to "granola"/"oats" naming.
- R1 provenance: no provenance adjectives used anywhere (none are label-derivable here).
- R2 partial-panel: only snk-018 has a panel gap (fiber null); immaterial to its copy — not narrated.
- Sanctioned factual terms (ingredient names like שיבולת שועל מלאה, סירופ גלוקוז) recur as facts;
  the 5-gram census proves zero editorial-phrase repetition (max 5-gram count = 1).
