# TASK-461 Phase-2 — Crackers (crackers_frontend_v1.json) copy overhaul — Author report

**Lane:** Content Agent (C1 native, Hebrew editorial). **Status: DRAFT — pending Adversarial QA gate.** Proposes RETURNED.
**Zero git writes:** only `git show` / `git ls-tree` / `git hash-object` (read-only) were run; no file under `C:\Bari` was touched except the two deliverables below. All working files live in scratchpad.

Note: this is a resume of a previously interrupted session (TASK-461.md dispatch log shows an earlier P461-CRACKERS-AUTHOR pass returned once and hit a session-limit interrupt before QA could complete, artifact sha `8570534d…`). That artifact was not found in `tasks/returns/` at resume time, so this pass re-derived the work from scratch, independently, against the same origin/master baseline blob (`784af259…`) — it is a fresh, self-contained author pass, not a continuation of unverified prior state.

## Artifacts
| File | What | Hash |
|---|---|---|
| `crackers_origin.json` (scratchpad) | Baseline, extracted from **origin/master** `bari-web/src/data/comparisons/crackers_frontend_v1.json` | git blob `784af2593a3c98d3cf08c9368c563239d8e7eb08` (verified: `git hash-object` of the scratchpad copy reproduces `git ls-tree origin/master`'s blob sha exactly); sha256 `a2f851e21c19db9a28d6d82bb52acef9beeecc85a175fb7cf7fd08aa5743ef4e`, 147,711 bytes |
| `TASK-461_crackers_copy_overhaul.json` | **Deliverable** — baseline with re-authored insightLine/rowVerdict on all 19 products (post-QA-fix, LF-only) | sha256 `bc2aa399b7768e4b8d57c294aa1a7eee3e0478902ec81e142b5706202a489a43`, 148,006 bytes |
| `authored_copy.py` (scratchpad) | The 19 authored pairs, keyed by barcode, with per-product grounding comments citing verified corpus extremes | — |
| `apply_and_audit.py` / `audit_out.txt` (scratchpad) | Injection + full self-audit (isolation, metrics) — deterministic, re-runnable | — |
| `ngram_census.py` / `ngram_out.txt` (scratchpad) | 4/5/6-gram repetition census across the corpus (house rule R3) | — |

Formatting note: a pure `json.load` → `json.dumps(ensure_ascii=False, indent=2)` roundtrip of the origin file is **byte-identical** (verified before injection: `roundtrip_byte_identical=True` in `audit_out.txt`), so every byte outside the two copy fields is preserved by construction.

## (a) Isolation proof — field-level diff
Recursive leaf-by-leaf diff of parsed baseline vs deliverable (`apply_and_audit.py`):
- **38 leaf diffs total = `products[i].insightLine` ×19 + `products[i].rowVerdict` ×19. Non-copy-field diffs: 0.**
- insightLine changed **19/19**; rowVerdict changed **19/19**.
- `_meta` identical: **True** (includes `categoryCaveat`, `exclusions`, `task433_data_rework`, `reflow` block — all untouched).
- Product count unchanged: **19 → 19**. All 19 barcodes covered, 0 missing.
- score / grade / rank / nutrition / d4_additives / confidence* / ids / imageUrl / expansion: untouched (covered by the 0-non-copy-diff result; expansion was NOT touched, per the task's hard constraint).

## (b) Audit metrics on the new copy (baseline badness in parentheses)

| Metric | New copy | Old copy |
|---|---|---|
| Em dashes (—) across all 38 fields | **0** | 34 |
| Banned engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/נקודות) | **0 hits** | 1 hit (rank 10 rowVerdict: "נותנים לו נקודות טובות" — killed) |
| Antithesis (", לא " / " ולא " / " אלא " define-by-negation) | **0 hits** | 4 hits |
| Opening-3-words uniqueness, insightLine | **19/19 unique** | not audited at time, but templated ("70% חיטה מלאה", "למרות השם/הסגנון" etc. shared frames) |
| Opening-3-words uniqueness, rowVerdict | **19/19 unique** | ditto |
| Max phrase repetition (4/5/6-gram census, full corpus) | **2× max** (house-rule R3 bar is >2×; clean) | not measured |
| Products carrying digits (label % or a verified shelf extreme) | **9/19** | 19/19 in some form (sodium/sugar/gram values recited near-universally) |
| Empty/short fields | none (all insight/verdict fields pass a 15/30-char floor) | — |

### Numbers-kept justification (9/19, each verified against the full 19-product corpus)
Crackers' own category caveat states the real editorial story is grain-quality percentage vs refined flour/starch fillers — so unlike most other categories, several kept numbers are **label composition percentages that ARE the point of the category**, not nutrition-panel recitation:

| Rank | Product | Number(s) kept | Why it's the story (verified) |
|---|---|---|---|
| 1 | קרקר כוסמין מלא ושומשום | 82% | Label ingredient %, first ingredient — the whole "4 real ingredients" thesis rests on it |
| 2 | קרקר כוסמין אורגני | 98% | Label ingredient % — sole shelf-max declared single-grain purity |
| 4 | קרקר דק רוזמרין פיטנס | 30.5% | Label %, needed to prove the "פיטנס"-name-vs-reality gap |
| 6 | קרקר כוסמין סלק | 1.3% | Label % (beet powder) — minor-ingredient disclosure, not nutrition |
| 8 | קרקר דק פיטנס בטטה | 31% | Label %, same name-vs-reality pattern as rank 4 |
| 15 | קרקר שומשום אסם | 84%, 6.6% | Label %s — 84% white flour dominance + the one positive (sesame) |
| 16 | קרקר טופז שומשום | 754 מ"ג | Verified shelf 2nd-highest sodium (sole 2nd; gap to #3 = 176mg) |
| 17 | קרקר מרובע מלוח | 1,200 מ"ג | Verified shelf-max sodium (sole max; gap to #2 = 446mg) — matches the product's own name "מלוח" |
| 19 | קרקר (ranked last) | 8.5 גרם | Verified shelf-max **measured** sugar (only 2/19 products carry a non-null sugar value; this is the higher of the two) |

Every other product's copy carries **zero** digit characters — the composition story (whole-grain share, filler type, additive count) is told in plain language without repeating panel numbers.

## (c) Superlative rank-check table (against the FULL 19-product corpus, `nutrition_dump.json`)

| Claim | Product(s) | Verification |
|---|---|---|
| "הציון הנמוך ביותר בהשוואה" (lowest score) | rank 19 (44.5) | Sole minimum; next is rank 18 at 49.6 — gap 5.1, real |
| "הנתרן הגבוה ביותר בכל ההשוואה" (highest sodium) | rank 17 (1,200mg) | Sole max; next is rank 16 at 754mg — gap 446mg, real |
| "הנתרן... השני בגובהו" (2nd-highest sodium) | rank 16 (754mg) | Sole 2nd; next is rank 14 at 578mg — gap 176mg, real |
| "הסוכר הנמדד כאן... הגבוה ביותר" (highest *measured* sugar, scoped) | rank 19 (8.5g) | Only 2/19 products have non-null sugar (rank 12 = 4.0g, rank 19 = 8.5g); rank 19 is the higher of the two — scoped correctly to "measured" since 17/19 are null on-label |
| "הקלוריות הגבוהות בכל ההשוואה" (highest kcal) | rank 14 (519 kcal) | Sole max; next is rank 19 at 488 — gap 31, real |
| "החלבון כאן מהגבוהים בהשוואה" (protein among-highest, NOT "sole") | ranks 1, 2, 5 | Ranks 1/2 tie at 16.0g (sole joint-max); rank 5 at 15.0g is 3rd. Copy correctly uses "among the highest," never claims a false sole lead on a tie |
| "שבעים אחוז חיטה מלאה... יותר דגן מלא מכל קרקר קמח-מעורב אחר" (rank 11: most whole-wheat vs every mixed_grain cracker) | rank 11 (70% wheat) | Verified against all 8 `mixed_grain`-cluster products' declared whole-wheat %: rank3=37%, rank4=30.5%, rank5=25.5%(of 66%), rank6=37%, rank7=25.5%(of 67%), rank8=31%, rank9=33.5%, rank10=30.5%. All below rank 11's 70% — claim holds against every member of the comparison set, not just its nearest neighbor (old copy's claim was narrower — see truth-fix list below) |
| Fiber "מהגבוהים בהשוואה" (ranks 1,2,3,6 — NOT "sole highest") | ranks 1 (10.0g), 2 (9.3g), 3 (10.5g), 6 (10.3g) | Ranks 3/6 are a near-tie (10.5 vs 10.3, gap 0.2) — copy never claims a sole fiber champion, only "among the highest," which is correct given the tie |
| Rank 6/7's "twin"/"family" framing | ranks 3&6 (spelt+olive-oil+seed family), ranks 5&7 (near-identical flour blend) | Verified via ingredients text: ranks 3/6 share the identical 37% spelt + olive oil + seed-mix structure differing only in beet powder vs extra seeds; ranks 5/7 share the identical 66%/67% flour blend + palm oil + quinoa structure, differing by ~1pt score and a rosemary/garlic tweak — twin framing is accurate, not manufactured |

**19/19 products read and independently verified against the trace before being finalized.**

## Live truth-defect found and fixed

**Rank 18 (בארקוד 74375, קרקר זהב אסם, grade D) — fiber claim on a NULL datum.**
The production `rowVerdict` and `consumerTakeaway` both state "והחלבון והסיבים מהנמוכים במדף" (protein AND fiber among the lowest on the shelf). The trace's `expansion.nutrition.fiber` field for this product is **`null`** — the fiber value was never parsed/extracted from this product's label (confirmed against `nutrition_dump.json`). Asserting "fiber is low" on a null datum is a fabrication: the honest state is "unknown," not "low." **Fixed:** the new copy for rank 18 makes a protein claim only (protein = 8.0g, verified low relative to the corpus — tied near the shelf-min of 7.8g), and drops the fiber assertion entirely.

No other null-datum-into-claim defects were found on this pass. Two near-misses were checked and ruled non-issues: ranks 16/17's old copy mentions "שני/שלושה מקורות סוכר" (2/3 sugar *sources*), which is a verified ingredient-list count (glucose syrup + invert sugar; sugar + grape/fructose respectively), not a gram-value claim on the null `sugar` field — that phrasing is legitimate and was kept.

### Other observations (not defects, informational)
- The `_meta.task433_data_rework` block already documents that copy fields were "preserved verbatim — NOT rewritten" through the prior TASK-433 data-layer rework, i.e. this is a genuinely young page whose copy had never been through an editorial pass before this one.
- `d4_additives` extraction looks consistent across the corpus for this pass — no under-extraction anomaly like the ones flagged in other categories' passes was found (spot-checked ranks with long ingredient lists against their d4 arrays; counts matched visible E-numbers in the text).

## (d) Before/after — 3 representative samples

**Rank 1 — קרקר כוסמין מלא ושומשום (A, 81.6 — top of shelf):**
- OLD IL: "ארבעה רכיבים: כוסמין מלא, שומשום, מלח, אורגנו — בלי מילוי עמילן." (em dash; label recitation, no opinion)
- NEW IL: "ארבעה רכיבים בסך הכול, וכולם אמיתיים: כוסמין מלא, שומשום, מלח ואורגנו."
- OLD RV: "מהקרקרים הפשוטים במדף: כוסמין מלא (82%), שומשום, מלח ואורגנו — ארבעה רכיבים, בלי מילוי עמילן. חלבון וסיבים מהגבוהים בקטגוריה." (em dash; restates the count twice)
- NEW RV: "כוסמין מלא (82%) ושומשום בונים קרקר בלי מילוי ובלי תוסף אחד, והחלבון שלו נמנה עם הגבוהים בהשוואה. הרשימה הקצרה הזו היא ממש הסיפור של המוצר."

**Rank 10 — קרקר דק כפרי פיטנס (B, 74.0 — mid-shelf, engine-vocab leak killed):**
- OLD IL: "קינואה ושומשום ברשימה — אך כשליש חיטה מלאה ושני תוספים שנויים במחלוקת." (em dash)
- OLD RV: "**קינואה ושומשום נותנים לו נקודות טובות**, וחיטה מלאה פותחת את הרשימה — אבל היא כשליש בלבד, הסיבים נמוכים, ויש כאן שני תוספים שנויים במחלוקת. מוצר שיושב בדיוק באמצע המדף." (scoring-mechanic leak: "gives it good points" — a literal reference to the scoring machinery; plus an em dash)
- NEW IL: "קינואה ושומשום מוסיפים גיוון, אך הבסיס עדיין כשליש חיטה מלאה עם שני תוספים שנויים במחלוקת."
- NEW RV: "חיטה מלאה פותחת, וקינואה ושומשום נותנים לו גיוון אמיתי. קמח אורז וחיטה לבנה משלימים את רוב הבסיס, הסיבים נמוכים, ושני תוספים שנויים במחלוקת מצטרפים לרשימה. קרקר שיושב באמצע המדף בכל מדד."

**Rank 17 — קרקר מרובע מלוח (C, 52.9 — verified shelf-max sodium, name-matches-reality):**
- OLD IL: "נתרן 1,200 מ\"ג ל-100 גרם — הגבוה ביותר במדף; קמח לבן ושלושה מקורות סוכר." (em dash; leads with the panel number, not an opinion)
- OLD RV: "הנתרן הגבוה ביותר בהשוואה — 1,200 מ\"ג ל-100 גרם, עקבי עם השם 'מלוח'. קמח לבן ושמן דקל, שלושה מקורות סוכר ורשימת תוספי מזון ארוכה שחלקם שנויים במחלוקת — התמונה הכוללת של מוצר מעובד." (2 em dashes)
- NEW IL: "הנתרן הגבוה ביותר בכל ההשוואה: 1,200 מיליגרם ל-100 גרם, תואם את השם 'מלוח'."
- NEW RV: "קמח לבן ושמן דקל, שלושה מקורות סוכר, ורשימת תוספי מזון מהארוכות בהשוואה מציירים תמונה של קרקר מעובד לגמרי. השם על האריזה לפחות לא מסתיר את המלח: זה באמת המלוח ביותר על המדף." (closes on the engine's opinion — the name is at least honest about the one thing it's honest about)

## Adversarial-QA fix pass (GO_WITH_FIXES → applied in place)
QA returned GO_WITH_FIXES with two findings; both applied to the deliverable in place, all other bytes byte-identical, isolation still {insightLine, rowVerdict} only.

1. **HIGH — rank 19 (5000396021202) insightLine — bare score-word "הציון" leak.** My original self-audit regex scanned for `חציון` (the compound "median") but not the standalone `ציון` (score), so it missed this Tier-4 leak. The bottom-of-shelf claim is TRUE (rank 19 is the sole lowest scorer, 44.5, gap 5.1 to next), so it was reframed as standing/composition without naming the score:
   - OLD: "הציון הנמוך ביותר בהשוואה: קמח לבן, סוכר 8.5 גרם ל-100 גרם, ובלי דגן מלא בשום מקום."
   - NEW: "התחתית של המדף: קמח לבן, סוכר 8.5 גרם ל-100 גרם, ובלי דגן מלא בשום מקום."

2. **MEDIUM — rank 4 (7290112963918) rowVerdict — bare decimal "30.5%" trips the deterministic leakage gate's `\b\d{2,3}\.\d+\b` score-mechanic pattern.** The line already carried "כשליש" for the same fact, so the bare decimal was redundant; replaced with a non-decimal form:
   - OLD: "הרכיב הראשון ברשימה הוא חיטה מלאה (30.5%), ואז קמח אורז וקמח חיטה לבנה משלימים את השאר: כשליש בלבד דגן מלא בפועל. יש כאן גם תוסף שנוי במחלוקת, והסיבים נשארים נמוכים לקטגוריה."
   - NEW: "הרכיב הראשון ברשימה הוא חיטה מלאה, כשליש מהבסיס, ואז קמח אורז וקמח חיטה לבנה משלימים את השאר. יש כאן גם תוסף שנוי במחלוקת, והסיבים נשארים נמוכים לקטגוריה."

**Full corpus re-sweep after fixes (`leak_sweep.py`, all 19 products):** bare-`ציון`/vocab hits **0**, grade-letter leaks **0**, bare 2–3-digit decimals (non-unit-anchored) **0**. (The remaining kept numbers — sodium 754/1,200 מ"ג, sugar 8.5 גרם, ingredient %s like 82%/98%/84%/6.6% — are all unit-anchored, so none trip the hard gate.) Em dashes still **0**; openings still **19/19 unique** both fields.

**Line-ending correction (found while recomputing sha):** the pre-fix artifact had been written with Windows CRLF line endings (a byte-level deviation from the LF-only origin baseline that would have failed the QA field-isolation byte-diff). The deliverable is now re-written LF-only, so every non-copy byte is identical to origin/master by construction. Roundtrip byte-identity of the origin re-confirmed (`origin roundtrip byte-identical: True`).

**Updated deliverable sha256: `bc2aa399b7768e4b8d57c294aa1a7eee3e0478902ec81e142b5706202a489a43`, 148,006 bytes (LF-only).**

## Self-check (per task instructions)
- (a) Product count unchanged: **19 → 19**. ✓
- (b) Recursive diff of deliverable vs origin/master: **only `insightLine`/`rowVerdict` differ** (38 leaf diffs = 19×2, 0 elsewhere; `_meta` identical; origin roundtrips byte-identically LF-only). ✓
- (c) Engine-mechanic vocabulary count in new copy: **0** old→new was 1→0 for "נקודות" at author time; the QA pass then caught + killed the bare "ציון" at rank 19 → full-corpus vocab sweep now **0/19**. ✓
- (d) Every superlative rank-checked against the full 19-product corpus: **8/8 superlative claims verified**, all hold; 2 near-ties (protein top, fiber top) correctly hedged to "among the highest" rather than a false "sole" claim. ✓

## Return contract

```json
{
  "task_id": "TASK-461",
  "sub_task": "P479-crackers",
  "agent": "content-agent",
  "proposed_status": "RETURNED",
  "closing_authority": "orchestrator",
  "artifacts": [
    {"path": "C:\\Bari\\tasks\\returns\\TASK-461_crackers_copy_overhaul.json", "sha256": "bc2aa399b7768e4b8d57c294aa1a7eee3e0478902ec81e142b5706202a489a43", "bytes": 148006, "line_endings": "LF-only (matches origin baseline)"},
    {"path": "SCRATCHPAD/crackers_origin.json", "git_blob_sha1": "784af2593a3c98d3cf08c9368c563239d8e7eb08", "sha256": "a2f851e21c19db9a28d6d82bb52acef9beeecc85a175fb7cf7fd08aa5743ef4e", "source": "origin/master:bari-web/src/data/comparisons/crackers_frontend_v1.json"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-461_crackers_author_report.md"},
    {"path": "SCRATCHPAD/crackers/authored_copy.py"},
    {"path": "SCRATCHPAD/crackers/apply_and_audit.py", "note": "deterministic re-runnable verifier; audit_out.txt is its output"},
    {"path": "SCRATCHPAD/crackers/ngram_census.py", "note": "5-gram repetition census, audit_out at ngram_out.txt"},
    {"path": "SCRATCHPAD/crackers/apply_qa_fixes.py", "note": "applied the 2 QA GO_WITH_FIXES in place + isolation re-proof"},
    {"path": "SCRATCHPAD/crackers/leak_sweep.py", "note": "full-corpus leak sweep: bare-ציון/vocab, grade-letters, bare decimals — all 0"}
  ],
  "qa_fixes_applied": {
    "verdict_in": "GO_WITH_FIXES (1 HIGH, 1 MEDIUM)",
    "fix1_HIGH": {"barcode": "5000396021202", "field": "insightLine", "issue": "bare score-word 'ציון' leak (self-audit scanned חציון not ציון)", "new_string": "התחתית של המדף: קמח לבן, סוכר 8.5 גרם ל-100 גרם, ובלי דגן מלא בשום מקום."},
    "fix2_MEDIUM": {"barcode": "7290112963918", "field": "rowVerdict", "issue": "bare decimal '30.5%' trips deterministic leakage gate \\b\\d{2,3}\\.\\d+\\b; replaced with non-decimal 'כשליש'", "new_string": "הרכיב הראשון ברשימה הוא חיטה מלאה, כשליש מהבסיס, ואז קמח אורז וקמח חיטה לבנה משלימים את השאר. יש כאן גם תוסף שנוי במחלוקת, והסיבים נשארים נמוכים לקטגוריה."},
    "full_corpus_resweep": {"bare_score_word_or_vocab": "0/19", "grade_letter_leaks": "0/19", "bare_nonunit_decimals": "0/19"},
    "line_ending_correction": "artifact re-written LF-only to match origin baseline (pre-fix had CRLF, a non-copy byte deviation); non-copy bytes now identical to origin by construction"
  },
  "claims_self_verified": {
    "isolation": {"leaf_diffs": 38, "insightLine_changed": "19/19", "rowVerdict_changed": "19/19", "non_copy_field_diffs": 0, "_meta_identical": true, "roundtrip_byte_identity_of_baseline": true, "product_count": "19 -> 19", "line_endings": "LF-only, matches origin"},
    "metrics": {
      "em_dashes": {"old": 34, "new": 0},
      "banned_vocab_hits": {"old": 2, "new": 0, "distribution_note": "old-copy total across 19 = 2 (rank10 'נקודות' + rank19-region baseline had no ציון, but my authored draft reintroduced 1 'ציון' at rank19 which QA caught); post-QA full-corpus sweep = 0/19 including bare ציון, חציון, נקודות, פרמטר"},
      "antithesis_hits": {"old": 4, "new": 0},
      "opening3_unique_insight": "19/19",
      "opening3_unique_verdict": "19/19",
      "max_ngram_repetition_corpuswide": "2x (house rule R3 bar is >2x; clean)",
      "panel_number_products": "9/19 (label composition %s or verified shelf extremes, all unit-anchored — see justification table)",
      "grade_letter_recitation": 0
    },
    "distributions": {"insight_len_chars_range": "48-95", "verdict_len_chars_range": "108-227", "corpus_grades": {"A": 1, "B": 10, "C": 6, "D": 2}, "corpus_score_range": "44.5-81.6", "confidence": {"partial_low_extraction": 19}},
    "rank_checks": "8/8 superlative-claim classes PASS vs full 19-product corpus (see rank-check table above); 2 near-ties correctly hedged (protein tie ranks1/2, fiber near-tie ranks3/6)",
    "tie_discipline": "protein tie (ranks1/2 both 16.0g) and fiber near-tie (ranks3/6, 10.5 vs 10.3) both phrased as 'among the highest', never a false sole claim"
  },
  "defects_found_in_production": [
    "rank10 (7290115205176) rowVerdict: engine-mechanic vocabulary leak 'קינואה ושומשום נותנים לו נקודות טובות' (literal scoring-machinery reference) - fixed by rewrite",
    "rank18 (74375) rowVerdict + consumerTakeaway: fiber claimed 'among the lowest' while expansion.nutrition.fiber is NULL for this product (never parsed) - fabrication on a null datum, fixed by dropping the fiber claim and keeping only the verified protein-low claim",
    "rank11 (7296073134442) old copy's whole-grain superlative was scoped narrowly ('more than the Swedish-style cracker beside it', i.e. one neighbor only); new copy verified and broadened the same claim to hold against all 8 mixed_grain-cluster products, which it does (70% vs a range of 25.5-37% declared whole-wheat share)"
  ],
  "constraints_respected": {"git_writes": 0, "files_touched_under_C_Bari_outside_returns": 0, "subagents_spawned": 0, "off_sources_used": 0, "scores_grades_ranks_changed": 0, "expansion_touched": false},
  "next_gate": "Adversarial QA GO_WITH_FIXES received and both fixes applied in place; back to QA for re-verify of the 2 fixed strings + isolation re-proof, then handover",
  "blockers": [],
  "not_done": ["QA re-verification of the 2 applied fixes (dispatched by orchestrator)", "No git branch/commit/PR created (this lane holds zero git writes per task's hard constraint)"]
}
```
