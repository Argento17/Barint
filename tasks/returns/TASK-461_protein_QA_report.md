# TASK-461 Phase-2 #8 — PROTEIN copy overhaul — Adversarial QA Report

Date: 2026-07-02  ·  Category: protein-bars (`protein_combined_frontend_v2.json`)  ·  Scope: 32 products, 64 copy strings
Challenger: adversarial-qa-agent (independent Opus lane) · Author lane = separate Claude (treated as CLAIMS, re-derived)

## VERDICT: GO_WITH_FIXES  (0 CRITICAL / 0 HIGH / 3 MEDIUM)

Track V (verification) is fully GREEN. Track C (challenge) surfaces one genuine superlative over-reach
(pb-005) plus two rhetorical-softness observations — all MEDIUM, none blocking. No CRITICAL, no HIGH.
Under the D10 gate this is not a launch blocker; the MEDIUM findings are advisory (author may tighten
pb-005 before handover, at orchestrator discretion — the copy remains truthful either way).

---

## Provenance (independence proof)
- Candidate `protein_copy_overhaul.json` sha256 `90ce9cd0…4c` — matches spec.
- Baseline fetched independently via `git show origin/master:…protein_combined_frontend_v2.json`;
  blob `4127b58965bebb689016ba58388eda39b312f9d7` — matches spec. Did NOT accept the author's baseline copy.
- All numbers below are re-derived by my own scripts against these two files, not from the author report.

---

## TRACK V — VERIFICATION (all PASS)

### V1. Field isolation — PASS 32/32
- Top-level keys identical (`_meta`, `products`); product count 32/32; id-set identical.
- `_meta` byte-identical baseline↔candidate.
- Per-product keyset identical 32/32; only-changed-field union across the entire corpus = exactly
  `{insightLine, rowVerdict}`. isolation_clean = 32/32.
- Byte-identity confirmed on: `score, grade, rank, categoryTotal, _scoring_trace, nutrition_per_100g,
  d4_additives, expansion, confidence, name, brand, barcode`. Ranks are 1..32 unique.
- **Note:** `expansion.{comparisonContext, positiveSignals, limitingFactors}` are byte-identical to baseline —
  UNTOUCHED. Any staleness there is pre-existing (not candidate-introduced) and out of the 2-field scope.

### V2. Claim-by-claim truth audit — 64/64 grounded (1 superlative flagged to Track C)
All orchestrator hotspots re-derived from my own rank tables (see Rank Tables §). Every numeric claim TRUE:

| Hotspot | Claim | Verdict |
|---|---|---|
| **2a collagen** pb-011/013/008/012/030 | collagen is a weak link / boosts label number over quality | **GROUNDED.** קולגן literally in each parsed ingredient list; engine `collagen_detected=True` + `collagen_detection_note` set; protein_quality dim depressed (pb-008/013/014=32.4; pb-011/012/030=68.8) vs 72.6–88.8 for wholefood. Engine DOES devalue collagen → editorial defensible. |
| 2b pb-002 | satFat min + sodium min of ALL 32 | TRUE (satfat 1.8 = strict min; sodium 29.0 = strict min) |
| 2b pb-002 | "17 גרם סוכר מהגבוהים" | TRUE (sugar 17.0 = #5/32; only 3 sugar-bombs + pb-005 above) |
| 2b pb-002 | pea-protein attribution (truth fix vs old hazelnut) | TRUE (families=['pea']; "חלבון אפונה" in ingr) |
| 2b pb-002 | "גליצרול עם חומר משמר" | TRUE (גליצרול + פוטסיום סורבט E202 in list) |
| 2c pb-003 | fiber max + sodium #2 ("רק שיאן המלח עוקף") | TRUE (fiber 19.0 max; sodium 387 = #2, only pb-033 396 above) |
| 2c pb-003 | protein "רק אח אחד משתווה" | TRUE (pb-003 & pb-004 both = 36.0, no others) |
| 2c pb-006 | 496 kcal max + "אין מוצר צפוף יותר בקלוריות או בשומן" | TRUE (kcal 496 max AND fat 29.5 max — both pb-006) |
| 2c pb-009 | satFat 13g max + "שום חטיף... אינו מתקרב" | TRUE max; margin to #2 = 2.0g/15% → **MEDIUM softness, see RT-2** |
| 2c pb-013 | sugar min 1.7g | TRUE (strict min; #2 = pb-014 2.3) |
| 2c pb-033 | double record 35g sugar + 396mg sodium + "שליש מהמוצר סוכר" | TRUE (both strict maxima; 35g/100g ≈ a third) |
| 2c pb-030 | "כמעט כל השומן רווי, יחס שאין דומה לו" | TRUE (satfat/fat = 0.827 = clear max; #2 = 0.645) |
| 2c pb-027 | fiber #2 "רק חטיף אחד עוקף" | TRUE (16.6 = #2, only pb-003 above) |
| 2c pb-020 | "שיא החלבון של קבוצת התחליפים" + "שמונה תוספים" | TRUE (34.8 = max of maltitol group; d4 count = exactly 8) |
| 2c pb-018 | "רק חמישה מוצרים מלוחים ממנו" | TRUE (sodium 352 = rank exactly 6 → exactly 5 above) |
| 2d pb-007 | "פיסטוק כשני אחוזים" + "צבע מאכל על בסיס נחושת" | TRUE (פיסטוק 2.8% in ingr; E141 copper-chlorophyll in d4) |
| 2d pb-010 | three-substitute trio (מלטיטול/סורביטול/סוכרלוז) | TRUE (מלטיטול+סורביטול in ingr; סוכרלוז via d4 E955 — full label, ingr text truncated at display) |
| 2d pb-024/026 | four-sweetener + four-protein-family | TRUE both (all 4 sweeteners literally listed; families = casein/soy/wheat/whey ×4) |
| 2d pb-028 | "מוותר על סוכרלוז" | TRUE (no E955, tierC=False, no סוכרלוז) |
| 2d pb-020/021 | sulfite allergen (משמר סולפיטי + חובת סימון) | TRUE (E224 potassium metabisulfite in both d4) |
| 2d pb-031 | "יותר מרבע חטיף סוכר" + "אפס סיבים" | TRUE (sugar 27% > 25%; fiber 0.0) |
| 2d pb-032 | sugar #2 + "רק עוגייה אחת עוקפת בשומן רווי" | TRUE (sugar 31 = #2; only pb-009=13>11, and pb-009 IS literally a cookie) |
| 2e Today ×6 | "משכפלת את עצמה שש פעמים" + per-flavor signatures | TRUE (exactly 6 products pb-017–022 share soy/wheat/whey 4-source skeleton) |
| 2e pb-018 | family sodium "גבוה בבירור מכל אחיו" | TRUE (352 vs next sibling ≤160 in the ×6 series) |
| 2e WIN pb-013/014 | "הבדלים זעירים" near-identity | TRUE (protein/fat/fiber/sodium identical; kcal±3, sugar±0.6, satfat±0.5) |
| 2e Max Brenner trio | "בלי תחליפים ובלי גליצרול" | TRUE all 3 (glycerol=False, maltitol=False, no גליצרול in ingr) |
| 2e pb-015/016 sisters | sodium up, fiber down | TRUE (279→300 sodium up; 3.8→3.0 fiber down) |
| 2f pb-002 | pea truth fix | TRUE (above) |
| 2f pb-026 | removed peanut implication | TRUE (families casein/soy/wheat/whey — no peanut) |
| 2g engine-vocab kill | 3 baseline leaks removed | Candidate engine-vocab = 0 (see V3); leaks absent. |

### V3. Hygiene — PASS (all targets met)
- **Em/en dashes: 0** (baseline = 54). ✓
- **Engine vocab (Tier-4): 0** — no חציון/פרמטר/תקרת עיבוד/NOVA/cap/penalty/polyol/isolate_stacking etc.
- **Antithesis "לא…אלא": 0.**  **R4 recommendation drift (כדאי/שווה+לקנות…): 0.**  **Buy-verbs: 0.**
- **Openings: 64/64 unique** (across all fields; also unique within IL-only and RV-only).
- **OFF references: 0.**
- **Grade letters mentioned: 0** — no "ציון X", no bare A/B/C/D/E, no "נקודות", no slash-grades.
- **5-gram repetition:** max = 2× (only "קזאין סויה חיטה ומי גבינה", in pb-024/pb-026 — the allowed
  factual family-composition per choctab precedent). No 5-gram ≥3×. ✓
- **Panel numbers: exactly 5 products** — pb-002 (17g sugar), pb-006 (496 kcal), pb-009 (13g satfat),
  pb-013 (1.7g sugar), pb-033 (35g/396mg). Each is a verified shelf extreme where the number IS the story. ✓
- No empty insightLine/rowVerdict.

### V4. hebrew_readability — PASS 64/64 clean
`hebrew_readability.analyze(...).is_clean == True` for all 64 strings; 0 failures, 0 errors.

### CONTEXT CAVEAT (TASK-457) — CLEAR
pb-029 and pb-030 copy makes **zero** reference to grade, points, "proportionality," or C/D. pb-029's
"פותח את החלק התחתון של הטבלה" is a legitimate RANK reference (it is genuinely rank 28), not a grade or
the trace's flipped D→C value. pb-030 leans purely on the satfat-ratio finding. Neither product's copy
leans on the held rescore. No grade letters anywhere in the corpus (V3).

---

## TRACK C — CHALLENGE (hostile reading)

Overall: the shelf thesis lands cleanly — "protein number ≠ quality; the surroundings score." pb-002
leads on wholefood character, not grams; pb-003 explicitly says 36g protein "רק אח אחד משתווה" yet sits
#2 because sodium/isolate drag it; pb-020 "שיא החלבון של קבוצת התחליפים" is framed as engineering, not
praise. No health-halo on "sugar-free" engineering — every maltitol product's copy names the swap as a
swap ("עבודת תחליפים", "לא היעלמות"). Ties handled as ties (WIN pair, Max Brenner trio, Today ×6).
Supplement-adjacent claims are label/trace-grounded and lawyer-defensible EXCEPT one superlative.

### MEDIUM findings (advisory, non-blocking)

**RT-1 (MEDIUM) — pb-005 "משחק הכי נקי בקטגוריה במחלקת ההמתקה" is a superlative tie, not a sole max.**
- Evidence: pb-005 has maltitol=False, tierC=False, real sugar. But pb-002 (dates, no maltitol, no
  artificial sweetener, sugar 17.0) and the three Max Brenner bars (pb-031/032/033, real sugar, no
  maltitol, no artificial) are EQUALLY "clean" on the sweetening axis. pb-002 arguably cleaner (whole-food
  date sweetening vs pb-005's added white sugar + glucose syrup).
- Implication: a hostile competitor for pb-002 or Max Brenner could say "your own page calls Nature Valley
  'THE cleanest sweetening' while it uses added sugar and glucose syrup, and you scored the date bar higher."
  "הכי" claims uniqueness that isn't strictly true.
- Routes to: content-agent. Suggested (not mandated): soften "הכי נקי" → "מהנקיים / בין הנקיים". Copy stays
  truthful; only the superlative degree is over-stated.

**RT-2 (MEDIUM, observational) — pb-009 "שום חטיף… אינו מתקרב" is the softest superlative in the set.**
- Evidence: satfat 13.0 is a true max, but the #2 (pb-032, 11.0, a Max Brenner bar) is 2.0g / ~15% away.
  "אינו מתקרב" (does not come close) reads stronger than a 15% gap warrants. The claim is scoped to bars
  ("כולל ממתקי השוקולד") and pb-009 frames itself as a cookie, so it is not false — just rhetorically warm.
- Implication: low; defensible as written. Monitor only.
- Routes to: content-agent (monitor / optional tightening).

**RT-3 (MEDIUM, language) — pb-021 "חלבון מולחם" is the weakest natural-Hebrew moment.**
- Evidence: "מולחם" (welded/soldered) as a metaphor for the fused 4-source isolate blend is evocative but
  slightly awkward register; reads as deliberate stylization rather than an error. hebrew_readability
  passes it (is_clean=True). Grounded — the label names 4 distinct protein ingredients.
- Implication: cosmetic; no truth or leakage issue. Monitor.
- Routes to: content-agent (optional).

### Weakest 3 strings (as requested)
1. **pb-005 RV** — "הכי נקי" superlative over-reach (RT-1). The only genuine defensibility gap.
2. **pb-009 RV** — "אינו מתקרב" over a 15% margin (RT-2). Warm but not false.
3. **pb-021 RV** — "חלבון מולחם" awkward word choice (RT-3). Cosmetic.

---

## RANK TABLES (my independent derivation, 32 products)

satFat desc: pb-009 **13.0** · pb-032 11.0 · pb-008 9.9 · pb-007 9.4 · pb-030 9.1 · pb-023 9.1  … min pb-002 1.8
satFat/fat ratio desc: pb-030 **0.827** · pb-003 0.645 · pb-017 0.637 · pb-004/018/019/021/022 0.636
sodium desc: pb-033 **396** · pb-003 387 · pb-004 385 · pb-005 375 · pb-006 354 · pb-018 352 … min pb-002 29
kcal desc: pb-006 **496** · pb-005 489 · pb-031/032 465 · pb-008 435 · pb-033 430
fat desc: pb-006 **29.5** · pb-005 28.3 · pb-031 24.0 · pb-032 23.0 · pb-009/008 22.0
sugar desc: pb-033 **35** · pb-032 31 · pb-031 27 · pb-005 17.2 · pb-002 17.0 … min pb-013 1.7
fiber desc: pb-003 **19.0** · pb-027 16.6 · pb-024 16.4 · pb-028 16.2 · pb-002 13.0
protein desc: pb-003/pb-004 **36.0** · pb-020 34.8 · (7 products at 34.0)
collagen_detected: pb-008, pb-011, pb-012, pb-013, pb-014, pb-030 (all with קולגן in parsed list)
maltitol group (replacement shelf) protein max: pb-020 34.8

---

## Routing summary
- content-agent: RT-1 (pb-005 superlative — recommend soften before handover), RT-2/RT-3 (monitor).
- No findings route to data / nutrition / frontend / design. Scores untouched, engine untouched, isolation clean.

## Proposed status: RETURNED — GO_WITH_FIXES (0C/0H/3M). No CRITICAL → does not block the D10 go-live gate.

---

## MICRO RE-CHECK — RT-1 targeted fix (2026-07-02, same QA lane, independent re-derivation)

**New artifact `protein_copy_overhaul.json` sha256 `962624c7d9a34ea4a182602bcdd451328217df1f31bd32d3320310c19a5aaf1b`**
(pre-fix preserved as `protein_overhaul_v1_preQA.json`, sha `90ce9cd0…` = exactly what I gated above).
Independently re-diffed v1→v2 myself (not accepting the author's diff claim): **changed set = exactly
`{pb-005: rowVerdict}`** — one field, one product, nothing else touched, `_meta` identical, pb-006
byte-identical. "משחק הכי נקי בקטגוריה במחלקת ההמתקה" (plays THE cleanest — sole-superlative framing) became
"נמנה עם הנקיים בקטגוריה במחלקת ההמתקה" (is counted among the clean ones — membership framing), closing
RT-1 exactly as flagged (over-claimed uniqueness, not falsity).

**Membership claim verified TRUE and precisely re-derived, independent of the author's roster.** Recomputing
the substitute-free set myself as {maltitol=False AND sweetener_tier_c=False} over all 32 products yields
`{pb-002, pb-003, pb-004, pb-005, pb-006, pb-031, pb-032, pb-033}` — **exact match to the author's claimed
8**, zero discrepancy either direction. pb-005 and pb-006 both genuinely belong (both maltitol=False,
tierC=False). On pb-003/pb-004 "looking odd": they ARE Today-brand, but they are NOT members of the
maltitol/isolate-stacking ×6 Today series (pb-017–022) flagged earlier as the "template family" — they are
a separate Today cluster using glycerol (an engineering marker, penalized on its own axis) but no
maltitol/artificial-sweetener substitution, so they are correctly, non-anomalously substitute-free. No
mislabeling. Regardless of the exact roster, the copy itself only asserts group membership for pb-005, not
a headcount — and the group is non-trivially plural (8 members), so "נמנה עם הנקיים" is a safely defensible
claim even under a stricter definition of "clean."

**No new defects introduced in the single changed field:** em/en-dashes 0, engine-vocab 0, antithesis
"לא…אלא" 0, R4 recommendation-drift 0, buy-verbs 0, grade/points mentions 0, `hebrew_readability.is_clean
== True`. Opening-3-words still 64/64 unique corpus-wide (only rowVerdict changed, opening words unchanged
regardless). No new 5-gram (≥3 repeats) introduced anywhere in the corpus by this edit.

**pb-006 confirmed untouched and carries no sole superlative:** byte-identical to v1 (both `insightLine` and
`rowVerdict` unchanged); scanned for "הכי"/"היחיד" — none present. Its only strong claims ("שיא האנרגיה,"
"אין במדף הזה מוצר צפוף יותר") are the kcal(496)/fat(29.5) strict-maxima already verified TRUE in the
original pass and are unaffected by the pb-005 edit.

### MICRO-VERDICT: GO
RT-1 is closed cleanly — the fix is precisely scoped, the membership claim is independently re-verified
true (exact roster match), no collateral defects were introduced, and pb-006 remains clean. **Full-category
verdict upgrades to GO (0 CRITICAL / 0 HIGH / 2 MEDIUM remaining — RT-2 pb-009 "אינו מתקרב" softness and
RT-3 pb-021 "חלבון מולחם" word-choice, both still advisory/monitor-only, unchanged by this fix.)**
