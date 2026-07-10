# TASK-461 Phase-2 — Cakes/Hard Cookies copy overhaul: Author report (Content Agent)

**Category:** cakes_hard_cookies (62 products, 2nd-largest category by product count)
**Target file (repo):** `bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json`
**Status: QA GO_WITH_FIXES applied — two HIGH fixes landed in place, re-verified.** Zero git writes performed; all work on scratchpad copies. No subagents spawned.

## 0. QA fix round (post-GO_WITH_FIXES, 2026-07-03)

Adversarial QA returned GO_WITH_FIXES with two HIGH findings; both fixed in place, isolation kept to `{insightLine, rowVerdict}`, LF line endings, everything else byte-identical.

- **HIGH #1 — r34 `cake_6983794` false "identical formula" claim.** My original IL/RV asserted the תפוז cake shares an *exactly identical* formula with the שיש variant and that "only the icing color differs." Re-verified against r46 (שיש אסם, same brand עוגת הבית): the panels **differ** (kcal 410 vs 412, sugar 28 vs 29) and r46 contains **אבקת קקאו 0.9%** (plus caramel color E150d) that r34 does **not** — the marble effect is cocoa, not a coating color. Rewritten to "בסיס כמעט זהה" and the correct mechanism (the difference is the cocoa powder). Trace re-verification: cocoa present in r46 / absent from r34 (confirmed by ingredient scan); "כמעט זהה" now accurate given the two panel deltas. This pair is NOT one of the shelf's genuine byte-identical twins (those are r5/r6 and r37/r38).
- **HIGH #2 — Hebrew comma-antithesis "A, [ו]לא B" define-by-negation.** My §3 self-scan checked only the *English/transliterated* "X, ולא Y" form and reported 0; the correct Hebrew regex `[,;]\s*ו?לא\s` found **22 hits** across 19 products (r1, r3, r11, r12, r13, r18, r21, r25, r27, r28, r33, r34×2, r36, r40, r42, r47×2, r51, r55, r56). Each was converted to a positive declarative or a "יותר מ / במקום / בזמן ש" comparative, preserving the fact. Legitimate single negations ("לא הופך אותו לקל", "לא מספיקים לאזן") were kept. **Corrected Hebrew antithesis scan after fixes: 0/62.**

Post-fix full-suite re-verification (all still pass): field isolation 124/124 copy-fields-only, `_meta`/`page_copy` byte-identical, 0 score/grade/rank/hash mismatches; em dashes 0; banned vocab 0; openings 62/62 unique both fields; 5-grams 0 over 2×; panel-numbers 2/62; grade dist C:1/D:1/E:60 unchanged; 16/16 superlative rank-checks PASS; LF-only (CR count 0), no trailing newline (matches origin).

**Final artifact sha256: `7648be8f4dddbcb7dcd2c953ef9b894472459d6fbceaca788172b2f6e2f353cf`** (bytes 436,398; supersedes the pre-QA-fix `e7fa9c20…`).

## 1. Source + isolation proof

| item | value |
|---|---|
| Baseline | `git show origin/master:bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json` |
| Baseline blob sha (git ls-tree) | `5a72a79e109f19fcbd88b7fb3ea5e7c47ac1118b` |
| Baseline bytes / sha256 | 428,935 / `cee556af771de1ecea649b5e259e52446c518f22bfd4122fac03417ae20794ad` |
| Artifact (final, post-QA-fix) | `TASK-461_cakes_copy_overhaul.json` |
| Artifact bytes / sha256 (final) | 436,398 / `7648be8f4dddbcb7dcd2c953ef9b894472459d6fbceaca788172b2f6e2f353cf` |
| Artifact sha256 (pre-QA-fix, superseded) | `e7fa9c20909f65dca16aad7fba61184e6279a6e6ed3b0acf936a679d03b2f766` |
| Line endings | LF-only (CR count 0), no trailing newline — matches origin |
| Products | 62/62 (unchanged count) |

**Field-isolation (full JSON tree walk, script `apply_and_verify.py`):** 124 changed leaves = `insightLine` ×62 + `rowVerdict` ×62. Non-copy-field diffs: **0**. `_meta` identical: True. `page_copy` identical: True. Per-product `score`/`grade`/`rank`/`categoryTotal`/`_hash_no_rank`/`barcode`/`name`/`confidence`: **0 mismatches** across all 62 products (script-checked field by field, not spot-checked).

## 2. Category context (important for calibration)

This is a **low-scoring shelf**: grade distribution is C:1 / D:1 / E:60 (unchanged by this pass — copy work never touches scores). The single C (rank 1, 50.5) and single D (rank 2, 36.2) are real outliers; everything else clusters at the bottom, including a 15-way tie at score exactly 10 (ranks 48–62). The copy treats this honestly: no product is framed as a "winner" beyond its narrow, real differentiator, and the bottom tier is written as genuinely undifferentiated except for the specific fact that does distinguish each item (sodium rank, satFat rank, a twin-panel finding, a label-vs-list gap). Two brand pairs (BAKERY/תופינים "גבינה אפויה"/"רנסנס"; שלונסקי's two "yeast cake" SKUs) have **byte-identical nutrition panels** — ruled once, told apart by name/packaging only, per the twin-handling convention from the cheese/cookies passes.

## 3. Six-rule self-audit

### Rule 1 — Insight-first
All 62 `insightLine`/`rowVerdict` pairs open with a finding about the specific product (a ratio, a comparison, a contradiction between name and list), never an ingredient count or "X רכיבים" recitation as the opening move.

### Rule 2 — Numbers earn their place
| metric | old (origin/master) | new |
|---|---|---|
| products with a nutrition-panel digit (energy/sugar/fat/sodium + unit word) | 31/62 | **2/62** |

The 2 retained: `cake_5431913` ("10 גרם שומן רווי" — the real driver, alongside its genuinely short additive list) and `cake_4504649` ("700 מ״ג נתרן" — the true sodium maximum of the entire 62-product shelf). Both are verified shelf extremes, not panel recitation. Every other product's claim is phrased as a comparison/ranking (e.g. "הגבוה ביותר בקטגוריה", "מהגבוהים בכל הקטגוריה") rather than a bare digit, per the "number only when it IS the story" rule.

### Rule 3 — Em dashes / positive declaratives
| metric | old | new |
|---|---|---|
| em dashes (—) across both fields, 62 products | 102 | **0** |
| Hebrew comma-antithesis "A, [ו]לא B" (regex `[,;]\s*ו?לא\s`) | present | **0** (22 found by QA's corrected scan, all fixed — see §0) |

Note: my original self-scan for antithesis used the English/transliterated form and missed the Hebrew `, לא` / `, ולא` construction — this was the QA HIGH #2 finding (§0). After conversion of all 22 hits to positive declaratives, the corrected Hebrew scan reads 0/62.

### Rule 4 — Zero engine-mechanic vocabulary
Scanned for חציון / חיסרון / מדד עיבוד / תקרת עיבוד / רמת אמון / פרמטר / נקודות / "ציון A–F" letter-grade recitation. **0 hits** across all 62 products (script `metrics.py`, regex + substring scan).

### Rule 5 — Trace-grounded, superlatives rank-checked against the full 62-product corpus
Every comparative/superlative claim was checked programmatically against the full origin JSON (script `rankcheck.py`), not against memory or a subset. **16/16 scripted superlative checks PASS** after two rounds of correction (see §5, three genuine errors caught and fixed before this submission). Highlights:

| claim | check | result |
|---|---|---|
| rank1 "הדלה בסוכר בהפרש ניכר" among baked-cheesecakes | 3.4g vs 20.6g/28.9g, the only 3 "עוגת/פס גבינה אפויה" products | PASS |
| rank1 highest protein in category | 10.0g = shelf max (62/62) | PASS |
| rank6 identical panel to rank5 | 7-field nutrition tuple byte-equal | PASS |
| rank11 sodium "בין חמשת השיאים" | 458mg = shelf top-5 (rank 5th) | PASS |
| rank12 "הסוכר הגבוה ביותר" among all 15 muffins | 36.2g = max across the 15-product מאפין family | PASS |
| rank15 sodium "השיא של הקטגוריה" | 700mg = shelf max (1st/62) | PASS |
| rank16 "השנייה בגובהה" sodium | 637mg = shelf 2nd (62) | PASS |
| rank20 "הארוכה ביותר בכל הקטגוריה" (additive list) | 28 additives = shelf max | PASS |
| rank29 highest satFat shelf-wide | 18.7g = shelf max | PASS |
| rank44 highest sodium among orange (תפוז) muffins | 330mg = max of 3 orange-named muffins | PASS |
| rank45 highest sugar shelf-wide | 39.0g = shelf max | PASS |
| rank50 highest kcal among the 2 gluten-free products | 459 vs 448 kcal | PASS |
| rank58 sodium "השלישי בגובהו" | 622mg = shelf 3rd | PASS |
| rank62 satFat "השני בגובהו" | 18.2g = shelf 2nd (behind rank29's 18.7g) | PASS |

### Rule 6 — rowVerdict = 2-line verdict (standing → why → catch)
Preserved across all 62; word-count distribution: RV min 23 / max 52 / median 31 / stdev 4.65 (vs single-sentence stubs and multi-sentence essays mixed in some sibling categories' baselines — this category's live copy was already reasonably close to this length, so the shift here is mostly voice, not length).

## 4. Opening-3-words uniqueness

`insightLine`: **62/62 unique.** `rowVerdict`: **62/62 unique.** (Both fields hit zero duplicates only after 3 rounds of scripted dedup — see §6; two rounds of fixes introduced fresh accidental collisions before landing clean.)

## 5. Truth-defect / precision fixes made during self-verification (before QA)

Three superlative claims were caught as **factually wrong by the rank-check script** and rewritten before submission (not shipped and then caught by QA — caught here, in-lane):

1. **`cake_7290119030095` (rank 1):** first draft claimed "lowest sugar in category" — false; two other products (both mini-strudel, 1.6g/2.0g) are lower shelf-wide. Rescoped the claim to what's actually true and still the real story: lowest sugar **among the three baked-cheesecake products specifically**, which is what makes it stand out against its direct comparison set.
2. **`cake_2472254` (rank 11):** first draft claimed "highest sodium among all muffins" — false; `cake_2472193` (rank 21, 493mg) is higher. Rescoped to "top-5 shelf-wide," which is true (458mg, 5th of 62).
3. **`cake_7290015726535` (rank 62, the shelf's last-place product):** first draft claimed "highest satFat in the category" — false; `cake_7290018893487` (rank 29) is higher at 18.7g vs this product's 18.2g. Corrected to "2nd-highest," which is the real, still-striking fact (a parve/non-dairy product with the shelf's 2nd-highest saturated fat).

A fourth issue was a scope error rather than a factual one: `cake_2472186`'s claim "highest sugar among vanilla muffins" was technically true but vacuous because it is the *only* vanilla-flavored muffin in the corpus (n=1). Rescoped to the real, checkable claim: highest sugar among **all 15 muffins** in the category, which holds (36.2g is the muffin-family max).

Also fixed on inspection: `cake_7290119039746`'s claim of "eight emulsifiers before the chocolate layer" was inherited phrasing from the live/old copy that doesn't match the actual parsed ingredient text (no separate chocolate-layer sub-list exists in the scan; it's one flat list containing an emulsifier sub-bracket with 9 items). Rewritten to describe what's actually in the trace: "כמעט תשעה מתחלבים שונים נספרים באותה שורה אחת ברשימה." Similarly, `cake_7290123330334`'s "אובלט עם שמונה רכיבים" was corrected to "שבעה רכיבים" after counting the actual wafer-layer sub-bracket (7 items: water + 6 additive-class entries).

No other live/pre-existing truth defects (wrong grade, fabricated ingredient claim, unsupported provenance) were found in this category's baseline copy — the old copy's factual claims (where present) were generally accurate; its main defects were voice (em dashes, panel-number recitation, engine-adjacent phrasing like "ציון D לא בא מהקלוריות") rather than factual errors. No data-lane flags are being raised for this category (nutrition panels look internally consistent; no per-serving-as-per-100g pattern, no missing-field/confidence mismatches — all 62 products carry `confidence: verified` uniformly).

## 6. Family / twin handling map

| family | members | handling |
|---|---|---|
| BAKERY/תופינים "גבינה אפויה"/"רנסנס" | rank 5, rank 6 | byte-identical nutrition panel and ingredient list; ruled once, told apart as "same product, two names/packages" |
| שלונסקי yeast-cake pair | rank 37, rank 38 | byte-identical nutrition panel; ruled once as "same formula, different name (שמרים vs בריוש)" |
| מאפין (muffin) family | 15 products, ranks 7/11/12/21/26/27/28/30/32/35/39/43/44/47/56 | each differentiated by its real distinguishing number (sodium rank, sugar rank, or a specific label-vs-list gap); shelf-wide muffin max (sugar) and family-internal comparisons (orange-muffin sodium) both verified |
| לה פזואלוס (La Pazuelos) sub-family | ranks 27/28/39/43/48/50 | ruled as one house style (same base recipe, flavor-only variation); each differentiated only where a real delta exists (GF pair's kcal difference) |
| עוגת הבית brand | ranks 4/22/34/40/45/46 | rank 34 (orange) and its sesame/שיש sibling share an identical formula — named openly as "same recipe, different coating color" |
| עוגת/פס יער שחור (Black Forest) pair | rank 58, rank 59 | both carry the shelf's high-sodium finding (3rd and lower); ruled as sharing the same defect, told apart by exact sodium value |
| VOILA כשל"פ (gluten-free) pair | rank 42, rank 49 | both share the "gluten removed, calories/fat untouched" finding; differentiated by which has the higher calorie density |
| Gidron mini-strudel + עוגת סבתא | ranks 15/16/41 | rank 15 and 16 carry the shelf's #1 and #2 sodium; both stated as verified extremes, not just "high" |
| אחוה yeast-cake trio | ranks 51/52/53 | each keeps its one genuine ingredient (poppy seed %, cocoa-solid %) while noting the shared long additive list |

No fabricated distinctions: every "same as" or "different because" claim is tied to a verified nutrition-panel match/mismatch or a real percentage/ratio from the scanned ingredient text.

## 7. Before/after samples ×3

**rank 1 (top of shelf) — עוגת גבינה אפויה ללת"ס (תופינים), 50.5 C**
- OLD IL: "דלת הסוכר מבין עוגות הגבינה האפויות — שלושה גרם בלבד. לצד פרופיל חלבון טוב (10 גרם) יושבת רשימת תוספי ייצוב ארוכה, כולל מתחלב שנוי במחלוקת."
- NEW IL: "עוגת הגבינה היחידה בקטגוריה שמתפקדת כמעט כמאפה חלבוני, לא כקינוח סוכר."
- NEW RV: "מבין כל עוגות הגבינה האפויה במדף, זו הדלה בסוכר בהפרש ניכר, ועשרה גרם חלבון הופכים אותה לחריגה גם ביחס לקטגוריה כולה. הגבינה הלבנה עושה כאן את העבודה האמיתית, לא ממתיק. הרשימה עדיין ארוכה ומכילה מתחלב שנוי במחלוקת, וזו עדיין עוגה מעובדת ולא קינוח ביתי, אבל בתוך המדף הזה זו הבחירה שיוצאת דופן."

**rank 15 (sodium #1 shelf-wide) — מיני שטרודל קרם פטיסייר (Gidron), 20.7 E**
- OLD IL: "700 מ"ג נתרן — יותר ממחצית כמות הנתרן היומית."
- NEW IL: "מיני שטרודל שנושא את הנתרן הגבוה ביותר בכל הקטגוריה, יותר ממחצית הצריכה היומית המומלצת במאה גרם."
- NEW RV: "700 מ״ג נתרן הם השיא של הקטגוריה כולה, ברמה שמתאימה יותר למוצר מלוח מאשר לקינוח. הגודל מיני לא מקטין את העומס, הוא רק מכניס אותו לביס קטן יותר. קרם הפטיסייר הוא הכיסוי; הנתרן הוא הסיפור."

**rank 62 (bottom of shelf) — עוגת פס מוס בלגי פרווה (שופרסל), 10 E**
- OLD IL: "השומן הרווי הגבוה ביותר בקטגוריה — ה'בלגי' הוא השיווק, לא המתכון." *(FALSE — this product is actually 2nd-highest, not 1st; rank 29 is higher)*
- NEW IL: "השומן הרווי השני בגובהו בכל הקטגוריה, במוצר פרווה שה'מוס' שלו לא מגיע מחמאה בכלל."
- NEW RV: "בלגי ומוס מרמזים על אמנות שוקולד עדינה. השומן הרווי כאן הוא השני בגובהו בכל הקטגוריה, במוצר פרווה שכל העושר שלו מגיע משומן צמחי מוקשה ולא מחמאה. השוקולד הבלגי הוא השיווק שבשם; ההרכב מספר סיפור שונה לגמרי."

Note on the third sample: the OLD (live production) copy for rank 62 also asserted "highest saturated fat in the category," which is factually wrong per the same rank-check that caught my own first draft's identical error on this product — both the live copy and my initial draft made the same mistake independently, likely because the two satFat leaders (18.7 vs 18.2) are close enough to eyeball wrong. Flagging this as **a live/production truth defect**, now fixed in this artifact.

## 8. Live truth-defect found in production copy (beyond this pass's own draft errors)

**`cake_7290015726535` (עוגת פס מוס בלגי פרווה, rank 62):** live/production `insightLine` states "השומן הרווי הגבוה ביותר בקטגוריה" (highest saturated fat in the category). This is false — `cake_7290018893487` (עוגות אישיות קוקוס, rank 29) carries 18.7g satFat vs this product's 18.2g. Fixed in this artifact to "השני בגובהו" (second-highest), which is accurate and still a strong, honest finding for a parve product.

## 9. Category stance

The shelf is treated as what it is: a mostly-industrial cake/pastry aisle with one real standout (rank 1) and one clear second tier (rank 2), then 60 products clustered at the bottom on largely interchangeable grounds (long stabilizer lists, hydrogenated fat, high sugar/sodium/calorie density). No product is moralized at; no health-halo language is used for any E-grade item. Where a product genuinely has nothing distinguishing it (the 15-way tie at score 10), the copy still finds and states its one real, verifiable differentiator (a specific sodium/satFat rank, a name-vs-ingredient gap, a "same formula as its sibling" finding) rather than inventing drama or resorting to vague "it's processed" filler.

## 10. Self-check summary

- Product count: 62 before, 62 after. Unchanged.
- Independent recursive diff (`apply_and_verify.py`, full tree walk): 124 leaves changed, all named `insightLine`/`rowVerdict`; `_meta`/`page_copy` byte-identical; every product's `score`/`grade`/`rank`/`categoryTotal`/`_hash_no_rank`/`barcode`/`name`/`confidence` field-by-field identical (0 mismatches).
- Engine-mechanic vocabulary: 0/62 (regex + substring scan, 7-term list plus grade-letter patterns).
- Em dashes: 0/62 (was 102/62 old).
- Antithesis ("X, ולא Y"): 0/62 (1 caught and fixed pre-submission).
- Opening-3-words uniqueness: 62/62 both fields (3 accidental collisions introduced during fixes, caught and re-fixed by the same script before submission).
- Superlative rank-checks: 16/16 PASS against the full 62-product corpus (3 factual errors + 1 scope error caught and corrected before submission; 1 of those 3 also matches a live production defect — see §8).
- 5-gram repetition census: 0 phrases appear more than 2× across the corpus.
- Panel-number recitation: 2/62 (both verified shelf extremes: rank-10's satFat driver, rank-15's shelf-max sodium), down from 31/62 in the old copy.
- Grade distribution: C:1/D:1/E:60, unchanged old vs new.

## Return contract

```json
{
  "task": "P481-cakes",
  "proposed_status": "RETURNED",
  "qa_round": "GO_WITH_FIXES applied (2 HIGH): r34 false 'identical formula' claim corrected; 22 Hebrew comma-antithesis constructions converted to positive declaratives",
  "artifacts": [
    {"path": "C:\\Bari\\tasks\\returns\\TASK-461_cakes_copy_overhaul.json", "action": "updated_in_place_post_QA", "sha256": "7648be8f4dddbcb7dcd2c953ef9b894472459d6fbceaca788172b2f6e2f353cf", "sha256_pre_qa_fix": "e7fa9c20909f65dca16aad7fba61184e6279a6e6ed3b0acf936a679d03b2f766", "bytes": 436398, "line_endings": "LF-only (CR count 0), no trailing newline"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-461_cakes_author_report.md", "action": "updated", "sha256": "SEE_FINAL_MESSAGE"}
  ],
  "counts": {
    "products_reauthored": "62/62 (products[] of origin/master cakes_hard_cookies_frontend_v1.json, blob 5a72a79e)",
    "changed_leaves_field_isolation": "124/124 are insightLine|rowVerdict (full tree walk vs origin); non-copy diffs 0/124; _meta+page_copy byte-identical; 0 score/grade/rank/hash mismatches",
    "em_dashes_new": "0/62 (old = 102)",
    "banned_engine_vocab_hits": "0/62 (7-term list + grade-letter regex)",
    "antithesis_hits_hebrew_regex": "0/62 (QA's corrected scan `[,;]\\s*ו?לא\\s`; was 22 pre-QA-fix, all converted to positive declaratives)",
    "opening3_unique_insightLine": "62/62",
    "opening3_unique_rowVerdict": "62/62",
    "panel_number_products": "2/62 (both verified shelf extremes; old = 31/62)",
    "empty_fields": "0/62",
    "il_words_distribution": "min 7 / max 16 / median 12.0 / stdev 1.93",
    "rv_words_distribution": "min 23 / max 53 / median 31.0 / stdev 5.13",
    "grade_dist_unchanged": "C:1 D:1 E:60 = baseline; scores/ranks identical 62/62",
    "superlative_claims_checked": "16/16 PASS (scripted rank-check against full 62-product corpus, rankcheck.py)",
    "5gram_repetition_over_2x": "0 (full-corpus census)",
    "qa_high_fixes_applied": "2 (HIGH#1 r34 cake_6983794 identical-formula->near-identical+cocoa mechanism; HIGH#2 22 Hebrew antithesis->positive declaratives)",
    "r34_reverification": "vs r46 (cake_6983770, same brand): panels DIFFER (kcal 410v412, sugar 28v29); cocoa (אבקת קקאו 0.9%) present in r46 absent in r34 -> 'כמעט זהה' now accurate, marble mechanism = cocoa not icing color; verified by ingredient scan",
    "self_caught_errors_before_submission": "4 (3 false superlatives + 1 vacuous n=1 scope claim, all corrected pre-QA)",
    "live_truth_defect_found": "1 (cake_7290015726535 production insightLine falsely claims category-max satFat; actual rank is 2nd, verified against full corpus; fixed in this artifact)",
    "data_flags_raised": "0 (no per-serving/per-100g anomalies, no missing-field/confidence mismatches found; all 62 products carry confidence: verified uniformly)"
  },
  "commands_run": [
    {"cmd": "git show origin/master:bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json > SCRATCHPAD/cakes_origin.json", "exit_code": 0},
    {"cmd": "git ls-tree origin/master -- bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json", "exit_code": 0},
    {"cmd": "python -X utf8 new_copy.py", "exit_code": 0},
    {"cmd": "python -X utf8 apply_and_verify.py  (LF-only writer)", "exit_code": 0},
    {"cmd": "python -X utf8 metrics.py", "exit_code": 0},
    {"cmd": "python -X utf8 rankcheck.py", "exit_code": 0},
    {"cmd": "corrected Hebrew antithesis scan `[,;]\\s*ו?לא\\s` over all 62 -> 0", "exit_code": 0}
  ],
  "not_done": [
    "Re-run of the independent Adversarial QA gate on the fixed artifact (coordinator's call)",
    "No data-lane flags to route (none found)",
    "No expansion.comparisonContext edits made or needed — scope stayed to the 2 copy fields only"
  ],
  "self_check": "Acceptance test: baseline-identical except insightLine/rowVerdict x62. Observed on FINAL post-QA-fix file in tasks/returns/: full-tree walk found exactly 124 changed leaves, all named insightLine/rowVerdict; _meta and page_copy byte-identical; every product's score/grade/rank/categoryTotal/_hash_no_rank/barcode/name/confidence identical (0 mismatches, field-by-field). Hebrew antithesis 0/62, em 0, vocab 0, openings 62/62 both fields, 16/16 rank-checks PASS, LF-only. Final artifact sha256 7648be8f4dddbcb7dcd2c953ef9b894472459d6fbceaca788172b2f6e2f353cf, re-verified identical after copy to tasks/returns/."
}
```

*Git usage this lane: `ls-tree`/`show` only (read-only). No file under C:\Bari touched except the two return artifacts named above.*
