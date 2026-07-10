# Adversarial QA Report — TASK-461 Phase-2 #9 GRANOLA copy overhaul

Date: 2026-07-02 · Scope: 22 products, /hashvaot/granola · Challenger: adversarial-qa-agent (Opus, independent lane)
Candidate: `granola_copy_overhaul.json` sha256 **f322a871829915c35929d64d9e616cc5c166a16e76d5dc807fc6a25819a815c2**
Baseline: origin/master `granola_frontend_v2.json` blob **60539d49** (independently fetched via `git show`, re-verified == `origin/master:bari-web/src/data/comparisons/granola_frontend_v2.json`)

## VERDICT: GO_WITH_FIXES (0 CRITICAL / 0 HIGH / 3 MEDIUM — all advisory; none block launch)

Every hotspot claim re-derived from the parse/rank tables holds. Field isolation is clean. The TASK-189
sodium guard is respected, the #19 three-way inconsistency is handled exactly as the spec required, and
all 5 claimed truth-fixes are verified real. The 3 MEDIUMs are consistency observations (2 residual grade
letters vs the program's grade-letters-0× bar, 1 label-declaration percentage) — none is a leak, a falsehood,
or an on-card contradiction. No rework is mandatory; the fixes are the author-lane's call.

---

## TRACK V — VERIFICATION

### V1. Field isolation — PASS (22/22)
- `_meta` byte-identical (sorted-key JSON compare == True). `off_used:false` preserved.
- Every non-copy field (`score`, `grade`, `rank`, `_hash_no_rank`, `expansion`, `d4_additives`, nutrition,
  confidence, ids, barcode) byte-identical across all 22. **ISOLATION issues = 0.**
- Key-sets identical product-for-product. Only `insightLine` (22/22 changed) and `rowVerdict` (22/22 changed).

### V2. Hygiene — PASS
| Check | Baseline | Candidate | Verdict |
|---|---|---|---|
| Em dashes (—) in copy | 52 | **0** | PASS (spec said "was 52" ✓) |
| En dashes (–) | — | 0 | PASS |
| Engine-mechanic vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטרים/NOVA/BSIP…) | — | **0** | PASS |
| Antithesis (ולא/אלא define-by-negation) | — | **0** | PASS |
| R4 recommendation-drift (כדאי/שווה+לקנות/לבחור/לרכוש) | — | **0** | PASS |
| Opening first-3-words unique across 44 | — | 44/44 unique | PASS |
| 5-gram repeated >2× (R3) | — | **0** (max repetition = 1) | PASS |
| Score literals (68.2 / 72/B) | — | 0 real (1 FP = "11.5%" nut share, #7) | PASS |
| OFF display-field references | — | **0** (all OFF markers inside `_meta` only) | PASS |
| Panel-number products | — | 2/22 (#5 kcal-max 504, #19 sugar-max 25 — both shelf extremes = the story) | PASS |
| Grade letters in copy | 14 | **2** (#5 "ובכל זאת C", #21 "גרנולות ה-E") | see M1 |

### V3. Hebrew readability gate — PASS (43/44 is_clean)
`hebrew_readability.analyze().is_clean` = 43/44. Sole flag: #7 IL "11.5" mis-flagged as SCORE-MECHANIC —
false positive; 11.5 is the nut share (`אגוזים 11.5%`, verified in parse), not a raw score. Same benign
decimal-FP class the program has repeatedly ruled non-blocking. No genuine leak.

### V4. OFF-in-_meta — PASS (documentation only)
OFF-removal markers ("OFF ban"×1, "TASK-238"×2, "panel_source"×1, "banned OFF"×1) live **exclusively in
`_meta`** (excluded_off_products.reason + provenance). 0 in the products/display block. Products block
contains no "Food Facts"/OFF reference. `_meta.off_used:false`. No OFF-derived display data.

### V5. #19 three-way inconsistency (7290011668587, "גרנולה עשירה") — HANDLED CORRECTLY
- **Baseline inconsistency confirmed exists:** score field 38.0 / grade field **D**, BUT `_meta.generated_from`
  claims TASK-385 refresh 38.0→33.0 D→E applied, AND the baseline expansion narrates grade **E** twice
  (`comparisonContext`: "ה-E משקף את כל אלה יחד"; `consumerExplanation`: "ציון E, הנמוך ביותר במדף").
  So: `_meta` says E-refresh done, score/grade fields say 38.0/D, expansion prose says E. Three-way, real.
- **Candidate copy uses NO grade letter** (no D, no E in IL or RV) and **leans on neither value** (no 33, no 38).
- **Rank-relative claims hold under BOTH candidate values:** the copy's only comparative claims are
  "המתוקה בקטגוריה" (sugar max = 25.0, strict ✓) and "הסיבים הנמוכים בקטגוריה" (fiber min = 5.7, strict ✓)
  — both nutrition-based, invariant to whether the score is 38.0/D or 33.0/E. Nothing breaks under 33.0/E.
  (Even the rank would only shift #19 from position 19 to 21 under 33.0 vs current #22=32.8 — still not last,
  and the copy makes no "last"/rank-position claim, so no exposure either way.)
- The stale expansion "ה-E"/"ציון E" prose remains (out of the 2-field scope) and still contradicts the D
  grade field — **pre-existing baseline defect, NOT candidate-introduced**, and it does not collide with the
  new rowVerdict (which makes no grade claim). Route to the expansion-pass accumulator (choctab רק-C, bread
  r16/r20, juices tails), NOT a blocker here.

### V6. Rank tables (independently derived from candidate nutrition)
```
RANK NAME                    SCORE/GR  SUGAR KCAL  NA    PROT FIB  FAT
 1  חמוציות ושקדים            69.7/B    9.6  386   10   11.4 14.5 14.8
 2  פרוטאין+שוקולד            69.3/B    8.0  411   71   20.7 12.3 11.4
 3  מייפל תמר פקאן            67.4/B   11.9  414    7   12.1  9.5 17.3
 4  לוז וקינמון               65.0/B    9.5  451    6   14.6 14.7 20.0
 5  מיקס קראנץ' מלוח          64.0/C    4.8  504  394   17.7 11.7 34.2
 6  חלבון שקד+חמוציות         63.1/C    8.8  411   56   23.6 12.8 11.5
 7  אגוזים חמוציות            61.3/C    9.9  440    9   11.8 14.4 19.3
 8  18% חלבון                 61.0/C   13.2  401   15   18.0  6.3 12.7
 9  פרוטאין+אגוזים            61.0/C    9.0  431   65   23.7  8.3 12.7
10  48% סופרפוד               60.4/C   13.5  410   69   12.0  9.4 17.2
11  מייפל פקאן                53.5/C   15.6  451    8   10.4  6.7 19.7
12  8% שוקולד מריר            51.1/C   13.4  416   99   11.0  6.5 14.0
13  חלבה תמר קשיו             47.0/D    9.3  432   16   13.0  8.2 19.2
14  שוקולד (פיטנס)            41.0/D   17.7  435   77    9.0  7.6 14.8
15  שוקולד קינואה (פיטנס)     41.0/D   17.9  443   89    9.1  7.3 16.4
16  דבש (פיטנס)               40.9/D   17.9  428   89    8.7  7.1 13.2
17  אגוזים (גרין)             40.0/D   18.0  415   40   10.0  7.0 13.0
18  פקאן (גרין)               39.4/D   17.0  414   40   10.0  7.0 12.0
19  עשירה                     38.0/D   25.0  423  195   11.2  5.7 17.2
20  אגוזים (שוק קולינרי)      37.0/D   20.0  371   20    9.0  6.0 13.1
21  פירות (גרין)              33.4/E   21.0  396   40    9.0  7.0 10.0
22  עם פירות (שוק קולינרי)    32.8/E   21.0  364   20    8.9  6.0 11.5
```
Extremes: SUGAR min 4.8 (#5) / max 25.0 (#19). KCAL min 364 (#22) / max 504 (#5) / 2nd 451 (#4,#11).
SODIUM min 6 (#4) / max 394 (#5) / 2nd-max 195 (#19). PROTEIN max 23.7 (#9), 23.6 (#6). FIBER min 5.7 (#19) / max 14.7 (#4).

### V7. Claim-by-claim truth audit — 44/44 strings TRUE against parse + tables
**Top pair (2a):** #1 "צמרת מתחלקת בין שתיים" (69.7 vs 69.3, 0.4pt; #3 is 2.3 away) ✓; #1 "אף תוסף ברשימה"
(d4_additives=[], no additive in parse) ✓; #1 fiber "שנייה אחרי שיא הסיבים" (14.5, 2nd after 14.7) ✓;
chicory-assist #1 & #7 (עולש in list + fiber high) ✓.
**Records (2b):** #5 "שיא הקלוריות 504" (kcal max ✓); #4 "מקפיצים...כמעט לשיא" (451, 2nd-max ✓); sugar min
4.8 #5 ✓; sugar max 25 #19 "המתוקה" ✓; protein "מתחלק בין שתי אחיות" #6(23.6)+#9(23.7) shared top ✓;
#19 "הסיבים הנמוכים" (5.7 strict min ✓) vs #8 "הסיבים מהנמוכים" (6.3, among-lowest hedge — scope-consistent ✓);
**sodium 394 stated as fact, TASK-189 guard PASS** (see V8).
**Sweetener-source counts (2c) — every count re-derived from parse:** #3 monk-fruit+maple-8% (no count claim) ✓;
#9 "שלושה ממתיקים: סירופ גלוקוז/סילאן/סוכר" (all 3 in parse ✓); #15 "ארבעה מקורות...עוד לפני נטיפים"
(סוכר/סירופ גלוקוז מיובש/סירופ סוכר אינברטי/רכז מיץ תמרים = 4, choc-sugar scoped separately ✓); #16
"ארבעה ממתיקים שהדבש אחרון" (4 in list, דבש 2.1% last-listed & smallest ✓); #17 "חמישה מקורות סוכר"
(סוכר/סירופ תמרים/סוכר חום/סירופ גלוקוז/דבש = 5 ✓); #19 "שלושה ממתיקים מוספים" (סוכר/איזוגלוקוז/סילאן
תמרים = 3 ✓); #22 "שלושה ממתיקים" + base 83% ✓; #11 "שלושה סירופים: מייפל/אגבה/סילאן" (3 ✓) + "הסוכר
הגבוה במשפחת שקד תבור" (15.6 = family max of #4/#5/#7/#11 ✓).
**Share claims (2d):** kinoa 2.9% ✓, honey 2.1% ✓, nuts 4.5% ×2 ✓, pecan/cranberry 5% ✓, אגוזים 11.5%+עולש 10% ✓,
לוז 11% ✓, שקדים 4.7% ✓, מייפל 8% (#3 & #11) ✓, choc 6.5% (#2) & 7.5% (#12) ✓, base 89% (#20) / 83% (#22) ✓,
oats 54% (#2) / 57% (#11) ✓, "כמעט רבע חלבון" #6 (23.6≈25%) ✓. All present in parse.
**Twins/families (2e):** fitness trio #14/#15 "עד לציון זהה" (both **41.0** — literally identical ✓; #16=40.9
sibling, not claimed identical); #17/#18 near-copy pair (both גרין, 0.6pt ✓); E-pair #21/#22 shared bottom
(0.6pt, ≤2pt noise band ✓); שקד-תבור "הסוכר הגבוה במשפחת" (#11=15.6 family max ✓).

### V8. TASK-189 sodium guard — PASS
#5 rowVerdict states "המלח שבשם מביא איתו 394 מ\"ג נתרן" as a plain FACT; #5 insightLine pins the C on
calorie density ("ובכל זאת C: ...504 קלוריות", "מי שסופר קלוריות"), NOT on sodium. No verb anywhere ties
sodium to the *score* going down. The engine under-penalizes granola sodium — the copy never implies it
punishes it. Guard respected.

### V9. Five claimed truth-fixes — ALL VERIFIED REAL
1. **#19 grade-letter contradiction removed:** baseline expansion said "ציון E"/"ה-E" against a D grade field;
   candidate copy carries **no grade letter anywhere** — the contradiction cannot appear on the new copy. ✓
2. **Sweetener undercount #19:** baseline "**שני** מקורות סוכר: סוכר ואיזוגלוקוז" → candidate "**שלושה**
   ממתיקים: סוכר, איזוגלוקוז, סילאן תמרים". Parse has all 3 added sweeteners. **Old wrong (2), new right (3).** ✓
3. **Sweetener undercount #9:** baseline "**שני** ממתיקים (סירופ גלוקוז וסוכר)" → candidate "**שלושה**:
   סירופ גלוקוז, סילאן, סוכר". Parse has all 3. **Old wrong (2), new right (3).** ✓
4. **#22 sole-lowest → shared bottom:** baseline "**הנמוכה ביותר** בקטגוריה" (0.6pt over #21) → candidate
   "תחתית המדף מתחלקת בין שתי גרנולות פירות". 0.6pt ≤ 2pt noise band → shared framing is the honest call. ✓
5. **#21 "all fruits candied" trimmed:** baseline "**כל הפירות** מסוכרים" (parse has 6 fruit entries; raisins
   & apple are NOT sugar-candied) → candidate names exactly the **4** that are (פפאיה/אננס/בננה/חמוציות),
   hedges preservative with "רובן" (banana has no sulfite). Precise. ✓

### V10. Data-flag / trap navigation — PASS
- #3 name "מייפל **תמר** פקאן" contains a date word but parse has **no date** — copy correctly avoids any
  date claim (mentions maple/monk-fruit/pecan/cranberry/coconut only). Missing-data trap avoided. ✓
- #5 pill "...סילאן — ללא סוכר מוסף" vs silan in parse: copy does NOT repeat the pill; it names silan as
  "ההמתקה יחידה" (the sole sweetener) — **more honest than the pill**, no on-card contradiction introduced. ✓
- Sulfite/"משמר גופריתי" claims: 2 explicit in copy (#19, #21), both parse-grounded (E220 in d4 + parse). ✓
- Maltitol #13 "כיתוב ללא תוספת סוכר נשען על מלטיטול": framed as a *label claim* ("כיתוב"), maltitol in
  parse (inside חלבה). Hedged and grounded. ✓

---

## TRACK C — CHALLENGE (the owner's bar)

Every one of the 44 strings opens with a stance/driver (insight-first), not an ingredient count. Reviewed
adversarially as the toughest critic would.

**Image-vs-label exposures — sharp, none snide, all proportionate:**
- #14 "מאפה בוקר ממותק שלובש בגדי ספורט" — pointed at the *fitness marketing gap*, grounded (fitness brand,
  sugar-heavy, real whole-grain base). Attacks the packaging story, not the eater. Sharp, fair, memorable.
- #13 "האריזה מספרת מה אין בפנים, והרשימה מוסיפה את מה שיש" — elegant, grounded in the ללא-תוספת-סוכר label
  vs maltitol/double-veg-oil reality. Not snide.
- #20 "השם מבטיח פיצוח, והרשימה מספקת בעיקר המתקה" & #10 "משאירים את הבידול על האריזה בלבד" — both grounded
  (4.5% nuts vs 3 sweeteners; protein/fiber = category average). Fair.

**No health-halo on clean high-calorie products (honest both ways):** #5 (cleanest list, 504 kcal, C) leads
with "ובכל זאת C" and pins it on calorie density — no halo. #4 (loz, clean-ish, high-cal, B) "עשירה באמת,
בשני המובנים" names both the good and the calorie catch. Balanced.

**Ties as ties:** top pair 69.7/69.3, protein 23.7/23.6, fitness twins 41.0/41.0, E-pair 33.4/32.8 (0.6pt),
#17/#18 (0.6pt) — all framed as ties/near-ties. No manufactured differentiation. No moralizing anywhere.
Natural Hebrew throughout (opinion-bearing, "smart friend" register).

**Weakest 3 lines (all still defensible):**
- **C-weak-1 #5 IL "ובכל זאת C:"** — cites the grade letter mid-sentence (see M1). Weakest of the 44.
- **C-weak-2 #14 "הצהרת 95% דגנים מלאים אמיתית"** — the 95% is a *package declaration* not in the ingredient
  parse; framed as "הצהרת" so it's honest, but "אמיתית" (real/true) endorses a label figure the parse can't
  independently confirm. See M2.
- **C-weak-3 #21 RV "גרנולות ה-E"** — the second residual grade-letter usage (see M1).

---

## FINDINGS BY SEVERITY

### CRITICAL — none.
### HIGH — none.

### MEDIUM (advisory — do not block launch)
**M1 — Two residual grade letters in copy vs the program's grade-letters-0× bar.**
Evidence: #5 IL "…ובכל זאת **C**: …" and #21 RV "אחת משתי גרנולות ה-**E** של המדף…". The overhaul program's
established bar (brined/cheese/protein gate-0 records: "grade letters 0×"; memory `bari_score_presentation_v1`:
copy carries insight, the chip carries the letter) treats grade letters as removed from copy. Baseline had
14; candidate cut to 2 — a large improvement, but not to 0. These are NOT leakage (the grade renders on the
card) and NOT false, so they are a **consistency deviation**, not a defect. Routes to: content-agent (author
lane's call — de-letter both, keeping the insight, if aligning to the program bar; both facts survive without
the letter, e.g. #5 "…ובכל זאת נשארת באמצע: …504 קלוריות", #21 "אחת משתי גרנולות תחתית המדף…").

**M2 — #14 "95% דגנים מלאים אמיתית" rests on a label declaration, not the parse.**
Evidence: parse for #14 contains no "95%"; the figure is the package's own whole-grain declaration (baseline
positiveSignal: "95% דגנים מלאים לפי ההצהרה"). The word "אמיתית" (real/true) reads as an engine endorsement
of a claim the ingredient parse cannot independently verify. Framed as "הצהרת" so it is not fabrication.
Routes to: content-agent (soften to attribute clearly, e.g. "הצהרת 95% דגנים מלאים על האריזה" without
asserting "אמיתית", per citation/attribution discipline). Advisory.

**M3 — Stale expansion prose on #19 still narrates grade "E" against the D grade field (pre-existing).**
Evidence: `expansion.comparisonContext` "ה-E משקף…" and `consumerExplanation` "ציון E, הנמוך ביותר במדף"
persist unchanged; grade field = D. This is a BASELINE defect inherited unchanged (out of the 2-field scope),
does NOT collide with the new rowVerdict, and the pending TASK-385 D→E refresh is the real resolution.
Routes to: data-agent / expansion-pass accumulator (with choctab רק-C, bread r16/r20, juices tails). Not
introduced by this candidate; noted so the sibling PR body carries it.

---

## MICRO RE-CHECK — M2 fix applied (post-gate, 2026-07-02)

New artifact `granola_copy_overhaul.json` sha256 **1d2fa0c66ecd7ac84d404e90aa2e59fcce8ec18a89c4ddb5fe0aa8ea859f61c5**
(pre-fix preserved as `granola_overhaul_v1_preQA.json`, re-hashed independently to
**f322a871829915c35929d64d9e616cc5c166a16e76d5dc807fc6a25819a815c2** — exact match to what this report gated).
Independently diffed old vs new: **diff scope = exactly `products[13].insightLine`** (barcode 7613035635845,
"גרנולה שוקולד" / fitness chocolate granola, product #14 in the shelf rank), `_meta` and all other
21 products byte-identical, `rowVerdict` on this same product also byte-identical (untouched).

**(1) M2 resolved — attribution replaces endorsement, and the claim remains true.** New IL: "על האריזה
**מוצהרים** 95% דגנים מלאים…" (the package **declares** 95% whole grain) — an attribution verb, not the old
"אמיתית" (true/real) endorsement. Confirmed the parse literally does **not** contain "95%" (it's a
package-only figure), so attributing rather than asserting it is now the correct register. The rest of the
line — "שלושה מקורות סוכר מוסף" (3 added-sugar sources), "שמן חמניות" (sunflower oil), "ועוד סוכר בתוך
השוקולד" (plus sugar inside the chocolate, scoped separately) — re-verified against parse: סוכר / סירופ
גלוקוז מיובש / סירופ סוכר אינברטי = 3 ✓, שמן חמניות present ✓, chocolate-chip sugar correctly scoped apart
from the 3. **M2 satisfied.**

**(2) rowVerdict "דגן מלא אמיתי בבסיס" — independently index-checked, PASS.** Parse comma-token order:
[0] פתיתי שיבולת שועל מלאה (42.8%) → [1] קמח חיטה מלא (14.1%) → [2] סוכר (first sugar). Both named whole
grains lead the list and sit strictly before the first sugar token. This claim describes the **ingredient
list's structure** (real whole grains genuinely lead), not the package's "95%" figure — a different claim
from the one M2 flagged. "אמיתי" here is parse-grounded (list-order fact), not a label-declaration echo.
No revision needed on this clause.

**(3) No new defects in the changed field.** Re-ran full hygiene on all 44 strings post-fix: em-dashes 0,
engine-vocab 0, opening first-3-words 44/44 unique (no collision introduced by the new IL opening
"על האריזה מוצהרים…").

**(4) M1 pair confirmed unchanged — exactly 2 grade-letter instances,** identical to the original gate:
#5 IL "…ובכל זאת **C**: …" (7290106773714) and #21 RV "…גרנולות ה-**E**…" (7290011131975). Per the
orchestrator ruling, M1 is accepted as pilot-register-consistent and stands untouched; re-confirmed at
exactly 2/44, no drift.

### Micro re-check verdict: **GO**

The single changed field resolves M2 cleanly (attribution, not endorsement, and still true against parse),
the adjacent rowVerdict clause the coordinator asked me to independently re-examine is itself parse-grounded
and needs no change, no new defects were introduced, and M1's count is unchanged at 2/44 as expected. Combined
with the original Track V/Track C clearance (0 CRITICAL / 0 HIGH throughout, M3 already routed to the
expansion-pass accumulator), **granola clears this adversarial QA gate as GO** on artifact sha256
`1d2fa0c66ecd7ac84d404e90aa2e59fcce8ec18a89c4ddb5fe0aa8ea859f61c5`. This agent does not approve launch or
close the task — routing the verdict back to the orchestrator/Product Agent for go-live action.

---

## Return contract

```json
{
  "task": "TASK-461 (Phase-2 #9 granola QA gate + M2 micro re-check)",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "scratchpad/TASK-461_granola_QA_report.md", "action": "modified", "sha256": "REPORT_SELF"},
    {"path": "scratchpad/granola_copy_overhaul.json (candidate v2, post-M2-fix, unmodified — verified only)", "action": "verified", "sha256": "1d2fa0c66ecd7ac84d404e90aa2e59fcce8ec18a89c4ddb5fe0aa8ea859f61c5"},
    {"path": "scratchpad/granola_overhaul_v1_preQA.json (candidate v1, pre-fix, unmodified — verified only)", "action": "verified", "sha256": "f322a871829915c35929d64d9e616cc5c166a16e76d5dc807fc6a25819a815c2"},
    {"path": "scratchpad/granola_baseline.json (origin/master blob 60539d49, git show)", "action": "created", "sha256": "ac543531ea543ceccbabbfa60e09f5ae07395e5a2a3c7ab8aedf8d0c6475fd23"}
  ],
  "counts": {
    "products: 22/22 (candidate products[])",
    "field_isolation_clean: 22/22 (non-copy fields byte-identical vs baseline; only insightLine+rowVerdict changed)",
    "insightLine_changed: 22/22, rowVerdict_changed: 22/22 (diff vs baseline, original gate)",
    "_meta_byte_identical: 1/1 (sorted-key JSON compare == True, both v1 and v2 vs baseline)",
    "em_dashes: baseline 52 -> candidate 0 (copy fields, 44 strings, unchanged after M2 fix)",
    "engine_vocab_hits: 0/44, antithesis_hits: 0/44, R4_drift_hits: 0/44 (candidate strings)",
    "openings_unique: 44/44, 5gram_repeat_over_2x: 0 (max repetition 1, re-verified post-M2-fix)",
    "grade_letters_in_copy: 2/44 (#5 'C' 7290106773714, #21 'E' 7290011131975; baseline had 14) — M1, re-confirmed unchanged post-fix",
    "panel_number_products: 2/22 (#5 kcal-max 504, #19 sugar-max 25; both shelf extremes)",
    "OFF_display_field_refs: 0 (all OFF markers inside _meta only; off_used=false)",
    "readability_is_clean: 43/44 (1 false-positive: #7 '11.5' = nut share, not a score)",
    "truth_claims_true: 44/44 (parse + rank tables)",
    "sweetener_counts_verified: 8/8 (incl. 2 undercount fixes #19 2->3, #9 2->3)",
    "claimed_truth_fixes_verified: 5/5",
    "TASK189_sodium_guard: PASS (394mg stated as fact, no score-punishment implication)",
    "score_dist: min=32.8 max=69.7 median=52.3 mean=51.70 stdev=12.49 most_common_score=61.0(x2)",
    "grade_dist: B=4 C=8 D=8 E=2 (22 total)",
    "M2_recheck_diff_scope: 1/1 field changed (products[13].insightLine only; _meta + all other 21 products + this product's rowVerdict byte-identical)",
    "M2_recheck_verdict: satisfied (attribution 'מוצהרים' replaces 'אמיתית' endorsement; 95% confirmed absent from parse; 3 sugar sources + sunflower oil re-verified)",
    "rowVerdict_index_order_check: PASS (oat-flakes idx0(42.8%) < whole-wheat idx1(14.1%) < first-sugar idx2, both grains precede first sugar token)",
    "new_defects_in_changed_field: 0 (em/vocab/opening-uniqueness re-run on all 44 post-fix)"
  ],
  "commands_run": [
    {"cmd": "git show 60539d49 > granola_baseline.json", "exit_code": 0},
    {"cmd": "git rev-parse origin/master:bari-web/src/data/comparisons/granola_frontend_v2.json (== 60539d49)", "exit_code": 0},
    {"cmd": "python -X utf8 verify.py (isolation + hygiene)", "exit_code": 0},
    {"cmd": "python -X utf8 tables.py / sweet.py / shares.py / twins.py / guards.py / off_fruit.py / undercount.py", "exit_code": 0},
    {"cmd": "python -X utf8 read_gate.py (hebrew_readability, em-dash counts)", "exit_code": 0},
    {"cmd": "python -X utf8 dist.py (distributions + sha256)", "exit_code": 0},
    {"cmd": "sha256sum granola_copy_overhaul.json granola_overhaul_v1_preQA.json (post-fix re-hash)", "exit_code": 0},
    {"cmd": "python -X utf8 recheck.py (old-vs-new diff scope, product[13] isolation)", "exit_code": 0},
    {"cmd": "python -X utf8 final_checks.py (M2 attribution check, index-order check, hygiene re-run, M1 count re-confirm)", "exit_code": 0}
  ],
  "not_done": [
    "run_gates.py G1-G8 not executed here (spec scoped this gate to copy verification + challenge; the git-owning sibling lane runs run_gates --baseline origin/master at handover, per program pattern). If required for this gate, dispatch separately.",
    "No browser/render verification (JSON-level gate; page not built in this lane)."
  ],
  "self_check": "Original acceptance test = 'independent field isolation 22/22 + claim-by-claim truth + TASK-189 guard + #19 dual-value robustness + OFF-in-meta-only' -> observed all PASS, VERDICT GO_WITH_FIXES (0C/0H/3M advisory). Micro re-check acceptance test = 'M2 fix diff-scoped to exactly 1 field, attribution-not-endorsement confirmed, index-order claim independently parse-verified, no new defects, M1 count unchanged at 2/44' -> observed all PASS on artifact sha256 1d2fa0c66ecd7ac84d404e90aa2e59fcce8ec18a89c4ddb5fe0aa8ea859f61c5. FINAL VERDICT: GO. Propose RETURNED."
}
```
