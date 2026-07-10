# TASK-476d — Content Agent return (bread + crackers rescore movers)

## RT-1 fix (false double-sodium claim)
**Finding (Adversarial QA gate, upheld):** the original copy for crackers `7290018790328` claimed its 1200 mg sodium was "more than double" / "יותר מכפול" the next cracker. FALSE. Corpus-verified across all 19: #1 = 1200 mg (this product), #2 `7290011489595` קרקר טופז שומשום = **754 mg**, so 1200/754 = **1.59×**, not double. (The 507 mg I had referenced is the #5 product, not #2.) The TRUE part — sodium is the highest in the category by a clear margin — is retained; the false multiplier is removed.

**Corrected insightLine:** הנתרן כאן הוא 1200 מיליגרם ל-100 גרם, הגבוה ביותר במדף בפער גדול, על בסיס קמח לבן בלי דגן מלא.
**Corrected rowVerdict:** המלח הוא הסיפור: 1200 מיליגרם נתרן ל-100 גרם, הגבוה ביותר בכל ההשוואה ובפער ניכר מהקרקר הבא אחריו. הבסיס קמח חיטה לבן עם שמן דקל, עמילן תירס ושלושה מקורות סוכר, בלי גרם דגן מלא. הסיבים כאן 1.5 גרם בלבד, מהנמוכים בכל המדף.

Both strings switched to the honest qualitative "הגבוה ביותר במדף בפער גדול / בפער ניכר" framing; no specific multiplier cited (per the gate's steer, the qualitative form is cleaner than "~1.6×"). Corpus numbers confirmed as above (1200 vs 754 = 1.59×). Everything else in both strings left intact. Re-scanned both edited strings: no em-dash, no "X,לא Y" antithesis, no grade-letter/score naming. Crackers JSON re-validated as parseable. All other movers (bread ×4) unchanged from the original pass below. Proposed status: RETURNED (still a DRAFT pending QA re-check of this fix).

---

**Role:** Content Agent, FIRST of two required sign-offs. This copy is a DRAFT until the Adversarial QA gate signs off.
**Worktree:** `C:\bari_wt_t476` (no commit, no push, no merge — changes left in working tree).
**Files touched:**
- `bari-web/src/data/comparisons/bread_frontend_v4.json` (4 movers)
- `bari-web/src/data/comparisons/crackers_frontend_v1.json` (1 mover)

All 5 movers dropped a grade because their ingredient text became visible to the scorer, so previously-missed additive/processing penalties now fire. In every case the authored copy names the REAL new driver (the additive/processing tail, or the sodium spike), not the old grade.

---

## 1. bread `2079033` — לחם דגנים לייט — 78.6 / B (was A)
**insightLine:** בסיס דגן מלא אמיתי, שמונים אחוז ממנו חיטה ושיפון מלאים, ואחת מרשימות הסיבים הגבוהות במדף.
**rowVerdict:** הבסיס כאן חזק: שישים אחוז חיטה מלאה, עשרים אחוז שיפון מלא ותערובת דגנים וגרעינים, עם 14.2 גרם סיבים ונתרן נמוך יחסית של 304 מיליגרם. מה שמושך אותו למטה הוא זנב חומרי העזר: שני חומרים משמרים, מתחלב, מווסת חומציות וויטמין C לאפייה, מהרשימות הארוכות בקטגוריה.
**Driver named:** Strong whole-grain base (60% whole wheat + 20% whole rye of flour, fiber 14.2, sodium 304) offset by a long processing-aid tail — 2 preservatives (Ca-propionate + K-sorbate) + E481 emulsifier + citric acid + ascorbic acid. Numbers taken from record (fiber 14.2, sodium 304). That additive list is the reason it's no longer top-tier.

## 2. bread `2079927` — לחם דגנים מלא — 78.6 / B (was A)
**insightLine:** רוב הקמח כאן מלא, שמונים ושלושה אחוז חיטה מלאה, והחלבון 13.8 גרם נמנה עם הגבוהים במדף.
**rowVerdict:** פרופיל דגן חזק: שמונים ושלושה אחוז מהקמח חיטה מלאה, תערובת דגנים וגרעינים, וחלבון 13.8 גרם מהגבוהים בקטגוריה. הצד השני הוא רשימת עזר עמוסה, שני חומרים משמרים ושני מתחלבים, לצד נתרן של 400 מיליגרם.
**Driver named:** 83% whole-wheat flour + high protein 13.8, pulled down by two preservatives (Ca-propionate + K-sorbate) + two emulsifiers (E481 + E471); sodium 400. Numbers from record.

## 3. bread `2079996` — לחם אחיד פרוס קל — 77.6 / B (was A)
**insightLine:** הגרסה המשודרגת של לחם האחיד: תוספת סיבים מרימה אותם ל-10.4 גרם, אך הרכיב הראשון עודנו קמח חיטה כהה מזוקק.
**rowVerdict:** הגרסה ה'קל' של לחם האחיד, מדורגת מעל הבסיסית שלו: כאן נוספו סיבים תזונתיים שמטפסים ל-10.4 גרם, חלבון 12.5 גרם וגם מעט קמח חיטה ושיפון מלאים. עדיין, הרכיב הראשון הוא קמח חיטה כהה מזוקק, ולצדו נמתחת רשימת עזר של שני חומרים משמרים, מתחלב ומווסת חומציות.
**Driver named:** First ingredient is refined dark-wheat flour (whole flours appear low in the list); added fiber 10.4 and protein 12.56 lift it, but the refined base + additive tail (2 preservatives, E481, citric acid, ascorbic acid) hold it at B. Copy deliberately mirrors the shipped rank-14 sibling `לחם אחיד פרוס` (2079477), which already names the "קל" version as its upgraded counterpart with added whole flours + fiber. Consistent sibling framing.

## 4. bread `4685027` — לחם מחמצת וחיטה מלאה קל — 64.0 / C (was B)
**insightLine:** קמח מלא לכל אורכו ומחמצת שיפון אמיתית, ולצדם ערכת משפרי אפייה שלמה שמכבידה על הרשימה.
**rowVerdict:** הבסיס נשמע מבטיח: כל הקמח מלא, שילוב חיטה מלאה ושיפון מלא עם מחמצת שיפון אמיתית, 9 גרם סיבים ו-209 קלוריות בלבד. מה שמכביד עליו הוא הזנב הארוך של חומרי עזר, מתחלב, חומר משמר, מייצב קסנטן וויטמין C לאפייה, שמרחיק אותו מהמחמצות הנקיות שבראש המדף.
**Driver named:** 100% whole flour (76% whole wheat + 24% whole rye) + real rye sourdough + fiber 9.0 + only 209 kcal — a genuinely good base — but a 4-item processing-aid stack (E481 emulsifier + E282 preservative + E415 xanthan stabilizer + E300 ascorbic acid) is what separates it from the clean top-shelf sourdoughs. This is the biggest single-grade drop (B→C) and the additive stack is the honest reason.

## 5. crackers `7290018790328` — קרקר מרובע מלוח — 48.1 / D (was C)
**insightLine:** הנתרן כאן הוא 1200 מיליגרם ל-100 גרם, יותר מכפול מכל קרקר אחר בהשוואה, על בסיס קמח לבן בלי דגן מלא.
**rowVerdict:** המלח הוא הסיפור: 1200 מיליגרם נתרן ל-100 גרם, יותר מפי שניים מהקרקר המלוח הבא בתור. הבסיס קמח חיטה לבן עם שמן דקל, עמילן תירס ושלושה מקורות סוכר, בלי גרם דגן מלא. הסיבים כאן 1.5 גרם בלבד, מהנמוכים בכל המדף.
**Driver named:** Sodium 1200 mg/100g — by far the highest in the whole comparison (next highest is 507). This is the exact field the TASK-433 FIX2 sodium parser corrected (1.2→1200), so the honest story is the salt. Refined white base (no whole grain), palm oil, corn starch, three sugars, fiber only 1.5. Sits rank 18 among the D-grade cluster (rank 17 = 49.4, rank 19 = 44.5); "יותר מפי שניים מהקרקר המלוח הבא בתור" is corpus-checked against the 507 next-highest.

---

## Phrasing-rule self-scan (owner hard rules, enforced by QA gate)
- **"X, not Y" / define-by-negation (English + Hebrew `,לא` / `אלא` / grade-naming):** scanned all 5 authored pairs. None present. One early draft of #3's insightLine used "ולא מלא"; revised to the positive declarative "קמח חיטה כהה מזוקק" to avoid the `לא` form. Absence phrasing that remains ("בלי דגן מלא", "בלי גרם דגן מלא") is a positive statement of what the product is, matching the shipped rank-17/rank-19 crackers voice, not an antithesis construction.
- **Em-dash (`—`) minimized:** zero em-dashes in any of the 5 authored insightLine/rowVerdict strings. Used commas, colons, periods only. (Em-dashes elsewhere in the files are pre-existing non-mover copy, untouched.)
- **No grade letter / numeric score as a crutch:** verified. No "B"/"C"/"D"/"מגיע ל" or score number appears inside any authored insightLine/rowVerdict. The one number that does appear (1200 mg sodium) is a real nutrition datum, not the score.
- **No BSIP/NOVA/pillar/cap/dimension jargon:** verified. Consumer-plain Hebrew only.

## Stale-caveat scan (the 5 movers only)
Programmatic scan of all 5 records for "could not be read / insufficient ingredient data / רכיבים חסרים / לא ניתן" style strings: **NONE found** on any of the 5. All 5 carry only the generic `confidence_tooltip_he` = "חלק מהנתונים בבדיקה…" and all 5 have fully populated `expansion.ingredients`. No false "ingredients missing" caveat exists to correct. No other products' caveats touched.

## Also changed (in-scope structural fields that were literal "PENDING_COPY" and would leak to the UI/filters)
On the 5 mover records I also set the leaked `_website_cluster` values (were literal `"PENDING_COPY"`), from the products' own whole-grain evidence, to keep shelf filters correct:
- 2079033 → `wholegrain`; 2079927 → `wholegrain`; 2079996 → `everyday` (matches its sibling 2079477); 4685027 → `sourdough` (has real rye sourdough).
- crackers 7290018790328 → `refined_white` (white flour, 0% whole grain — matches the file's documented cluster rule: refined_white = 0% whole-grain flour).

## NOT DONE / flagged for orchestrator (out of my authored-copy scope)
- **`_hash_no_rank`** on the 4 bread movers is still literal `"PENDING_COPY"`. This is a pipeline-computed content hash, not authored copy — the data/generator layer must recompute it. Flagging so it is regenerated before go-live (leaving a literal string there will break any hash-based validation).
- **crackers 7290018790328 still has other PENDING fields I did NOT author** (out of the "insightLine + rowVerdict" scope I was given): `bariInterpretation` (`["PENDING_COPY"]`), `bestUseCases` (`["PENDING_COPY"]`), `consumerTakeaway`, and `expansion.consumerExplanation`. `consumerTakeaway` and `consumerExplanation` are consumer-facing prose and MUST be authored+two-gated before this crackers page ships. `bariInterpretation` is the per-dimension score/label array (derived from the BSIP2 trace, a Data-layer artifact, not free copy). Routing these back to the orchestrator: they need a follow-up content pass (takeaway/explanation) + a data regen (bariInterpretation from trace) before crackers go-live. The single row I was scoped to is complete and defensible.
- The bread page's two other pre-existing movers on this rescore are complete; only the crackers row carries the extra unfilled fields.

```json
{
  "task": "TASK-476d",
  "proposed_status": "RETURNED",
  "artifacts": [
    "C:\\bari_wt_t476\\bari-web\\src\\data\\comparisons\\bread_frontend_v4.json",
    "C:\\bari_wt_t476\\bari-web\\src\\data\\comparisons\\crackers_frontend_v1.json",
    "C:\\Bari\\tasks\\returns\\TASK-476d_content.md"
  ],
  "counts": {
    "movers_authored": 5,
    "pending_strings_replaced_insightLine": 5,
    "pending_strings_replaced_rowVerdict": 5,
    "pending_strings_replaced_total_named_scope": 10,
    "website_cluster_pending_fixed": 5,
    "stale_caveats_found": 0,
    "stale_caveats_corrected": 0,
    "phrasing_violations_found_in_authored_copy": 0
  },
  "commands_run": [
    "python -c json.load(bread_frontend_v4.json, crackers_frontend_v1.json) -> BOTH VALID JSON",
    "grep antithesis/em-dash/grade-naming tokens over both files -> hits only in pre-existing non-mover copy",
    "python stale-caveat scan over 5 movers -> NONE, ingredients populated on all 5"
  ],
  "not_done": [
    "_hash_no_rank still PENDING_COPY on 4 bread movers (pipeline-computed hash, not authored copy — data/generator layer must regenerate before go-live)",
    "crackers 7290018790328: bariInterpretation, bestUseCases, consumerTakeaway, expansion.consumerExplanation still PENDING_COPY — outside the insightLine+rowVerdict scope I was given; takeaway+explanation need a follow-up content pass, bariInterpretation needs data regen from the BSIP2 trace before crackers go-live",
    "no commit / no push / no merge (left in worktree working tree per instructions)"
  ],
  "self_check": "All 10 named PENDING_COPY strings (5 products x insightLine+rowVerdict) authored fresh, each grounded in that product's real record data (whole-grain %, fiber, protein, sodium, additive list) and naming the real new-grade driver (additive/processing tail for the 4 breads; 1200mg sodium for the cracker). No grade letter or score number used as a crutch. Antithesis / em-dash / grade-naming scan clean on all authored strings. Both JSON files re-validated as parseable. Stale ingredient-missing caveats: none present on the 5. DRAFT pending Adversarial QA sign-off (second of two required gates)."
}
```
