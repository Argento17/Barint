# TASK-461 Phase-2 #2 — Cookies/Coffee copy overhaul: Adversarial QA / Red-Team report

**Category:** cookies_coffee (117 products — largest live shelf)
**Target file (repo):** `bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json`
**Candidate artifact (current, post-M1-fix):** `cookies_coffee_copy_overhaul.json` sha256 `af492d788f0c03494e5d2e76018accc62163bb99481e96bfaa608152a8dceddc`
**Candidate artifact (original, gated below, superseded):** preserved as `cookies_overhaul_v1_preM1.json` sha256 `81ecc1faaba4728a87a061f9d48a68f6e2ea260e650673ea2cf91aa1def5c5f1`
**Baseline (independent):** `git show origin/master:...cookies_coffee_frontend_v2.json` blob `675eac00…` / sha256 `b718df15efdd96a8cdc3c6c6005c30a08cca613d47a9377f4041e654821f6c77` (matches author-reported baseline exactly)
**Gate:** Adversarial QA (Opus, independent lane). All rank tables, isolation, hotspots re-derived with my own scripts — author `verify_apply.py`/`metrics.py` treated as CLAIMS only.

---

## VERDICT (current, post-M1-recheck): GO

0 CRITICAL · 0 HIGH · 1 MEDIUM (M3, data-lane flag — unchanged, not a copy defect).
M1 (template drift, 13x verbatim clause) is **RESOLVED**. See "M1 RE-CHECK" section at the bottom
of this report for the full targeted re-verification (17 changed products; the other 100 are
untouched and the original verdict below stands unmodified for them, per coordinator scope).

---

## [SUPERSEDED BY M1 RE-CHECK] Original verdict on pre-M1 artifact (sha256 81ecc1fa…): GO_WITH_FIXES

0 CRITICAL · 0 HIGH · 3 MEDIUM (2 template/register advisories + 1 data-lane flag re-raised for tracking).

Track V is fully green (isolation clean, all hotspots TRUE, hygiene clean, machine parity byte-identical).
Track C: every one of the 117 verdicts is publicly defensible on the artifact evidence alone. The MEDIUMs
are quality/register observations that do NOT block launch and do NOT require a re-author. The "legal one"
(Quaker no-added-sugar) is **defensible as phrased** — no re-scrape is required before ship (details below).

---

## TRACK V — Deterministic verification

### V1. Field isolation (independent tree-walk, `v_isolation.py`)
Baseline vs candidate full-tree leaf diff: **11,923 leaves each; 234 changed; 100% = insightLine(117)+rowVerdict(117); non-copy changed = 0.** `_meta` byte-identical, `page_copy` byte-identical, no keys added/removed. **PASS.**

### V2. Machine parity (`v_table.py` / final parity script)
score/grade/rank mismatches vs baseline: **0/117.** Grade dist **C:9 D:27 E:81** (= baseline). Score min 10.0 / max 59.8 / median 23.0 / **stdev 13.03** / most-common 35.7 (4×). Scores/grades/ranks untouched. **PASS.**

### V3. Hygiene (`v_hygiene.py`)
- em/en dashes across all 234 strings: **0** (baseline 242). **PASS.**
- banned engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/נקודות/NOVA/cap/floor/router…): **0.** **PASS.**
- score-literal leaks (`\d/[A-E]`, "X נקודות"): **0 real** (1 regex hit = "נקודת פתיחה" = idiom "starting point", not a score). **PASS.**
- opening-3-words uniqueness: **IL 117/117, RV 117/117.** **PASS.**
- antithesis "X, ולא Y": **0.** OFF references: **0.** empty fields: **0.** **PASS.**

### V4. Leakage gate — `hebrew_readability.analyze()` on all 234 strings (brand-masked)
**233/234 is_clean.** The single non-clean flag (r80 ck-4820180816552 IL, `score_mechanic term='10.6'`) is a **confirmed FALSE POSITIVE**: "10.6%" is a real ingredient percentage — the parsed label literally contains "פתיתי שיבולת שועל … 10.6%". Known %-vs-score ambiguity in the gate (same class as the תנובה/'נובה' backlog item). **PASS (0 true leaks).**

### V5. Hotspot truth audit — all TRUE against my independent tables

| Hotspot | Claim | My verification | Verdict |
|---|---|---|---|
| **LEGAL — Quaker ck-7290119041350** | name = "ללא תוספת סוכר"; copy says scanned list has סוכר + אבקת סוכר; 23.2g panel; hedged | (i) parsed ING literally reads "…שומן צמחי מדקלים, **סוכר, אבקת סוכר**, שיבולת שועל…" — both present. (ii) panel sugar = **23.2** confirmed. (iii) both fields hedge: IL "רשימת הרכיבים **שנסרקה**", RV "הרשימה **שהגיעה בסריקה**" + "בארי מציגה אותו כפי שהוא". | **DEFENSIBLE AS PHRASED — no re-scrape needed pre-ship** (see finding M3) |
| Red-label consistency (all "מסומן אדום") | every red claim matches an ISRAELI_RED_* cap; every "בלי סימון אדום" matches a no-red trace | 89 products mention אדום; **0 mismatches** vs trace caps. r11 (רייפעת) "בלי סימון אדום" ✔ (trace has only NOVA_PROXY_3, no red cap). "שני סימונים" claims → all carry RED2PLUS. | **PASS** |
| Sodium max 730 (r6 zaatar) | shelf-max, "הרחק מעל" | 730 vs #2 510 → gap 220. HIGH_SODIUM_700MG cap present. | **TRUE** |
| Kcal max 562 (r78) / #2 544 | shelf-max energy; "השניות בגובהן" | 562 = max, 544 = #2 (Tulino). | **TRUE** |
| Sugar max 49 (r88 Oreo white) | shelf-max sugar | 49 = max (#2 = 47 ×2). | **TRUE** |
| SatFat max 17 tie (Hit וניל+שוקו) | tie stated as tie both products | genuine 17.0 = 17.0 tie; copy "בשותפות"/"שותפה לשיא". | **TRUE** |
| Protein max 15.4 (peanut) | "החלבון הגבוה בקטגוריה כולה" | 15.4 = shelf max (58% peanuts). | **TRUE** |
| Fiber max 17.0 (r13 אביבה) | "יותר סיבים מכל מוצר אחר…חלקם מוספים" | 17.0 = max; honest added-fiber disclosure. | **TRUE** |
| Na max among sweet 510 (Hit שוקו) | "הנתרן הגבוה ביותר בעוגייה מתוקה" | 730 is savory (zaatar); 510 = max sweet. Correctly scoped. | **TRUE** |
| Twin/family identity | Quaker trio, caramel quartet, נסיכה pair, Tulino pair | Quaker 3× panels byte-identical @20.1 ("אותו לוח…בעוד שתי עוגיות" ✔). Caramel 4× identical @18.4. All twin "עד הגרם" claims verified. | **TRUE** |
| Bottom joint-last | "חולק את המקום האחרון עם גרסת השוקו" | ck-354996 & ck-354972 exact tie 10.0, ranks 116/117; both narrate the tie. | **TRUE** |
| Ingredient %: 8% Quaker oats, 35% gandola oats, PGPR, CMC, sulfite, hydrogenated, agave, maltodextrin, "שליש ציפוי" | each vs parsed list | 8% ✔ (in ING); gandola "35% oats + whole flour first" ✔; **PGPR** ✔ (E476 in both ING); **CMC "שנוי במחלוקת"** ✔ (E466 in פתי-בר-ללא-גלוטן pair) and נסיכה "צבע סינתטי במחלוקת" = **E124/Ponceau-4R** ✔ (distinct, correctly typed as color not stabilizer); **sulfite** 8/8 ✔ (incl. ck-74184 where OCR split "סול פיט"); hydrogenated ✔; agave 2/2 ✔; "45%/36% cream" ✔. | **TRUE** |

### V6. Suspect per-serving products (author excluded from rank checks) — INDEPENDENTLY re-identified
kcal<120 filter → exactly **4**: ck-7290122781359 (93), ck-7290000061245 (97), ck-7290118423904 (94), ck-7290118422617 (92) — same 4 the author flagged (r7/r25/r39/r40). Their NEW copy makes **NO panel-magnitude claim** — only ingredient-% digits (61%, 36%, 45%, 45%), each present in the parsed label. No shelf-extreme superlative references these 4. **PASS (Hard Rule 13 satisfied).**

### V7. Missing-data discipline (Hard Rules 12/13)
- 5 partial-confidence products (sugar=None): ck-…453068, ck-…043149, ck-…962139, ck-7296073453857, ck-7296073453840 — **all 5 carry a "נשען על מה שאומת / לא הגיע בסריקה" disclosure.** No claim depends on the missing sugar value.
- 2 **verified** products missing satFat: `bsip1_cookies_80083764` (gandola, ING truncated) + `ck-311128` — **both explicitly disclose** the missing satFat ("נתון השומן הרווי חסר/לא הגיע בסריקה") and neither makes a satFat magnitude claim. Phantom-confidence-safe. **PASS.**
- The satFat *key* is absent (not null) on `bsip1_cookies_80083764` in BOTH baseline and candidate — a pre-existing data condition, not introduced here.

### V8. Truth-defect fixes vs live production copy — all 3 confirmed
1. **Grade-E-on-a-D-product (ck-7290018893845 פתי בר בטעם חמאה):** live copy states "מוריד ל-E"/"הציון נחת על E"; product is grade **D** (35.7). NEW copy carries no grade contradiction. **FIXED.**
2. **False clean-list (ck-7290119043149 לה פזואלוס חמאה):** live copy = "רשימה נקייה, ללא תוספים"; parsed list has "שמנים…(חלקם מוקשים)" + E450/E500, and live RV leaked "תקרת עיבוד". NEW copy names the hydrogenation + drops the vocab. **FIXED.**
3. **Unverifiable "six colors" (ck-46214930207 מרבה):** live claim "שישה צבעי מאכל"; parsed coating names ~5 colorants — count unsupported. NEW copy = "שורת צבעי מאכל" (no count). **FIXED.**

---

## TRACK C — Adversarial defensibility (the owner's bar)

The shelf is treated correctly as an **indulgence shelf**: the top product's verdict says outright "והיא עדיין עוגייה"; no product is health-washed; grade-E rulings (81 of them) each name a real driver from the trace (red caps / sugar-first list / margarine-hydrogenation / additive stack) and none is a stamped moral condemnation. The kids product (זoo biscuits, ck-313184) is **factual, not alarmist**: "נראית תמימה, והרשימה תעשייתית… חטיף מתוק מן השורה" — names sulfite + two sugars, no scare language. Confidence is honest (partial disclosed; verified-but-missing disclosed). Ties are ruled as ties. Every verdict I read (full 117 blocks) opens with an opinion, not a number, and lands a takeaway.

Under adversarial reading — a skeptical food scientist, a competitor, or the accused brand — **no verdict over-claims beyond what the artifact evidence supports.** The Quaker no-added-sugar verdict is the sharpest public claim and it is stated as a *scan finding* Bari presents "כפי שהוא," not as an accusation of fraud — the correct, defensible register.

### 3 weakest lines (for fan-out learning, NOT blockers)
1. **r79 טריפל שוקולד ציפס** — closes "משפחת מרבה כולה מדברת באותה שפה"; combined with the shared "…מסומנים שניהם אדום" clause the line leans on family boilerplate.
2. **r102 שוקוצ'יפס נוגטלי** — "מהמתוקות במשפחה שכולה מתוקה" is a near-tautology; least distinct verdict among the מרבה set.
3. **r109 שוקוצ'יפס קלאסי** — "ונכון לקרוא אותו כך" is a soft filler tail after an otherwise good observation.
These three sit inside the templated cohort (finding M1); tightening them is the fan-out lesson, not a defect.

---

## FINDINGS

### MEDIUM
**M1 — Template drift at volume (register). [RESOLVED — see M1 RE-CHECK section below]** The full 6-word clause **"סוכר ושומן רווי מסומנים שניהם אדום"** appeared **verbatim in 13 rowVerdicts** on the originally gated artifact (sha256 81ecc1fa…); "מסומן אדום" 36×, "סימון אדום" 24× across the shelf. Every use was factually correct (all 13 were genuine dual-red-label products; only 13 of 67 red2plus products used the exact clause, so 54 were already varied), and the opening-3-uniqueness gate passed — but at 13 identical mid-sentence clauses the red-label motif read *stamped* when scanning the shelf. Routed to **content-agent**; author lane fixed it in a targeted 17-product rework (new artifact sha256 af492d78…) — independently re-verified clean, see below.

**M2 — "אמון-vs-fact" disclosure clause is the right call but rides the same repetition line.** 7 disclosure clauses ("נשען על מה שאומת" family) — sanctioned by house rule R2 and correct, noted only so the fan-out reviewer counts it as *intended* repetition (exempt from M1).

**M3 — DATA-LANE re-flag (not a copy defect; re-raised for tracking).** Quaker ck-7290119041350 "ללא תוספת סוכר" name vs scanned list containing סוכר+אבקת סוכר and 23.2g sugar (identical to the regular Quaker ck-7290119041206). The copy handles this **correctly and defensibly** (hedged as a scan finding). BUT the underlying data ambiguity — real mislabeled product OR a scrape that crossed the two identical-panel variants — should be **verified by the Data Agent** as a data-integrity item, independent of this copy shipping. The author already flagged this to Data; I confirm the flag is warranted and the copy does NOT need to wait on it (the phrasing survives either resolution). Routes to: **data-agent**. Also worth a Data pass: the 4 per-serving panels stored as per-100g (servingNote "ל-100 גרם" on kcal 92–97 products) — copy is written safely around them, but the stored values are wrong.

### No CRITICAL, no HIGH.

---

## Gate note
Challenge gate expects `02_products/cookies_coffee/reports/red_team_cookies_*.md` for the current corpus with 0 open CRITICAL. This report satisfies the 0-CRITICAL condition; the git-owning lane must copy it to that path (read-only lane here — zero git writes performed).

---

## Return contract

```json
{
  "task": "TASK-461 (Phase-2 category #2: cookies_coffee) — Adversarial QA gate",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "SCRATCHPAD/TASK-461_cookies_QA_report.md", "action": "created", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/BASELINE_cookies_MINE.json", "action": "created", "sha256": "b718df15efdd96a8cdc3c6c6005c30a08cca613d47a9377f4041e654821f6c77"},
    {"path": "SCRATCHPAD/v_isolation.py", "action": "created", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/v_table.py", "action": "created", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/v_hygiene.py", "action": "created", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/v_readability.py", "action": "created", "sha256": "SEE_FINAL_MESSAGE"}
  ],
  "counts": {
    "candidate_sha256_match": "1/1 (81ecc1fa… == spec)",
    "baseline_sha256_indep_match": "1/1 (b718df15… == author-reported baseline)",
    "field_isolation": "234/234 changed leaves = insightLine|rowVerdict; non-copy diffs 0/11923 leaves (v_isolation.py)",
    "score_grade_rank_parity": "0/117 mismatches vs origin/master (parity script)",
    "grade_distribution": "C:9 D:27 E:81 (= baseline); score min10.0/max59.8/median23.0/stdev13.03/most-common 35.7(4x)",
    "em_dashes": "0/234 strings (v_hygiene.py; baseline 242)",
    "banned_engine_vocab": "0/117 (v_hygiene.py)",
    "opening3_unique": "IL 117/117, RV 117/117 (v_hygiene.py)",
    "antithesis_off_empty": "0/117 each (v_hygiene.py)",
    "readability_is_clean": "233/234 (v_readability.py); 1 confirmed false-positive (10.6% ingredient pct)",
    "red_label_claim_consistency": "0 mismatches vs trace caps (v_claims.py; 89 products mention אדום, all correct incl. negative claims)",
    "hotspot_claims_TRUE": "all audited hotspots TRUE (sodium730/kcal562/sugar49/satFat17-tie/protein15.4/fiber17.0/twins/joint-last/ingredient-%) (v_super.py, v_twins.py, v_ingr.py, v_families.py)",
    "suspect_perserving_products": "4/117 indep-identified (kcal<120), same set as author; 0 make panel-magnitude claims (v_claims.py)",
    "partial_confidence_disclosures": "5/5 present + 2/2 verified-missing-satFat disclosed (v.readability/partial script)",
    "truth_defect_fixes_confirmed": "3/3 (grade-E-on-D, false-clean-list+vocab-leak, six-colors) (v_truthfix.py)",
    "template_drift_clause_13x": "13/117 rowVerdicts share exact 6-word red-label clause (v_hygiene.py) — MEDIUM",
    "findings": "CRITICAL 0 / HIGH 0 / MEDIUM 3"
  },
  "commands_run": [
    {"cmd": "git rev-parse origin/master:bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json (==675eac00)", "exit_code": 0},
    {"cmd": "git show origin/master:...cookies_coffee_frontend_v2.json > BASELINE_cookies_MINE.json", "exit_code": 0},
    {"cmd": "python -X utf8 v_isolation.py", "exit_code": 0},
    {"cmd": "python -X utf8 v_table.py / v_suspect.py / v_captypes.py", "exit_code": 0},
    {"cmd": "python -X utf8 v_claims.py / v_super.py / v_twins.py / v_ingr.py / v_families.py", "exit_code": 0},
    {"cmd": "python -X utf8 v_hygiene.py", "exit_code": 0},
    {"cmd": "python -X utf8 v_truthfix.py", "exit_code": 0},
    {"cmd": "python -X utf8 vclean/v_readability.py (hebrew_readability gate)", "exit_code": 0}
  ],
  "not_done": [
    "run_gates G1-G8 not run (read-only copy lane; git-owning sibling runs them at commit with --baseline origin/master)",
    "Data-lane verification of Quaker no-added-sugar label + 4 per-serving panels (routed to data-agent, not this lane's job)",
    "No fix/edit/close performed — findings raised and routed only (Hard Rules 15/16)"
  ],
  "self_check": "Acceptance: (V) baseline-identical except insightLine/rowVerdict×117 AND (C) every claim defensible on artifact evidence. Observed: 234/234 changed leaves are copy fields, 0 non-copy diffs, score/grade/rank 0 mismatches; all audited hotspots TRUE incl. the Quaker legal claim (hedged, list confirms סוכר+אבקת סוכר, 23.2g); hygiene/leakage clean; 3 truth-defect fixes confirmed. Verdict GO_WITH_FIXES (0 CRITICAL / 0 HIGH / 3 MEDIUM)."
}
```

---
---

## M1 RE-CHECK (targeted, 17 products only — full corpus rank tables/verdicts above stand unmodified)

**Scope:** author lane fixed M1 (13× verbatim clause) plus 4 additional 3× 5-gram/4-gram chains its own census exposed. New artifact `cookies_coffee_copy_overhaul.json` sha256 `af492d788f0c03494e5d2e76018accc62163bb99481e96bfaa608152a8dceddc`, overwritten in scratchpad. Pre-M1 version preserved as `cookies_overhaul_v1_preM1.json` sha256 `81ecc1faaba4728a87a061f9d48a68f6e2ea260e650673ea2cf91aa1def5c5f1` (= exact artifact this report originally gated).

### R1. Independent diff, pre-M1 → post-M1 (`m1_diff.py`, full tree-walk, NOT trusting the coordinator's list)
Leaf counts identical (11,923 each). **18 leaves changed → 17 products**: 16 rowVerdict-only + 1 product (`ck-8710502139017`, rank 79) with **both** insightLine+rowVerdict changed. **0 non-copy leaves changed.** My independently-derived changed-id set is an **exact match** to the coordinator's 17-id list (including the ck-7290013740465 "chain-breaker" the coordinator's message didn't itself enumerate by id but whose rank-21 mapping I derived and confirmed). vs origin/master baseline: still 234 total changed leaves, 0 non-copy, `_meta`/`page_copy` byte-identical. **PASS — isolation holds.**

### R2. M1 verbatim-clause census (own script, not the author's)
`clause = "סוכר ושומן רווי מסומנים שניהם אדום"` → **0 carriers** (was 13). **Corpus-wide 5-gram census (my own, all 234 strings): 0 distinct 5-grams appear >2×.** Widened the check to 4-grams and 6-grams as an extra net the spec's 5-gram window could miss: 6-grams also 0 >2×; 4-grams found **3 distinct chains at exactly 3× each** ("אדום על שומן רווי,", "חוצים שניהם לסימון אדום,", "קמח לבן, סוכר ושמן") — below the ≥5-occurrence MEDIUM threshold used for M1, and these are shorter/more generic fragments (4 words) than the offending 6-word sentence-level clause, not a re-opening of the finding. **PASS — M1 resolved, no new template chain at reportable volume.**

### R3. Fact retention
**13 original carriers** (ck-4820180816590, ck-7290013740694, ck-7290119041206 [Quaker], ck-7296073162001, ck-7290119040803, ck-8710502139017, ck-8000500366073, ck-7622300356767, ck-61245, ck-8710502470028, ck-7290000075143, ck-7290101111986, ck-7290019816058) — **all 13 verified**: trace still shows `ISRAELI_RED_LABEL_1_SUGAR=True, ISRAELI_RED_LABEL_1_SAT_FAT=True, ISRAELI_RED_LABELS_2_PLUS=True` for every one (unchanged, as expected — trace is not touched), and I read all 13 new rowVerdicts in full: each now states both red flags in a **distinct construction** (13 different sentences, e.g. "גוררים כל אחד סימון אדום משלו" / "אוספת סימון אדום גם על הסוכר וגם על השומן הרווי" / "מסומנת אדום פעמיים, על הסוכר ועל השומן הרווי" / "האדום מגיע גם לשורת הסוכר וגם לשורת השומן הרווי") — zero verbatim repeats among the 13, fact preserved in all. The Quaker (ck-7290119041206) rewrite also still correctly carries the trio-family claim ("אותו לוח תזונה בדיוק מופיע בעוד שתי עוגיות במדף") — unchanged and still true.

**4 chain-breakers** (mapped via my own OLD rank table, not the author's prose labels: rank 21=ck-7290013740465 שושנים, rank 56=ck-7290119043798 אוזניות, rank 70=ck-311128 עוגיות בטעם חמאה, rank 100=ck-7290019816232 קראנץ סנדויץ שוקולד) — all 4 confirmed as surgical single-clause edits, byte-identical elsewhere: ck-311128's satFat-missing disclosure clause ("נתון השומן הרווי לא הגיע בסריקה") preserved verbatim, no phantom claim introduced; the other 3 kept their sodium-high / dual-red / disclosure facts, only the sentence construction changed. **PASS — 17/17 fact-retained.**

### R4. Hygiene on the 17 (own script)
em dashes: **0**. Banned engine vocab: **0**. Empty fields: **0**. No new panel-number recitation observed (spot-read all 17 — the only digits introduced are pre-existing ingredient-% facts already in the parsed labels, e.g. Quaker's "8%"). Opening-3-words uniqueness corpus-wide (post-fix): **IL 117/117, RV 117/117**, no dupes. **PASS.**

### R5. Isolation vs origin/master (final)
Score/grade/rank mismatches vs origin baseline: **0/117.** Grade dist unchanged **C:9 D:27 E:81**. **PASS.**

### R6. Track-C spot-check — stance + driver retained, not shuffled synonyms
Read all 17 rewrites in full. Each keeps (or, for r79, sharpens) a distinct opening finding and closing takeaway — e.g. r79's insightLine now leads with "הטריפל מתחיל בסוכר" (sugar-first finding) rather than the prior cocoa-forward opening, giving it a sharper, more distinct driver than before, not a weaker one. None of the 17 reads as reshuffled synonyms of a template; each is still a specific opinion about that product. **PASS.**

### M1 RE-CHECK VERDICT: **GO**
0 CRITICAL / 0 HIGH / 0 new MEDIUM from the rework. M1 is resolved. M3 (data-lane flag on the Quaker label + 4 per-serving panels) is unchanged and still routes to data-agent — it was never a copy defect and this rework didn't touch it. The other 100 untouched products retain their original PASS verdicts from the body of this report (unaffected by this targeted re-check, per coordinator scope).

### Updated return contract (M1 re-check)

```json
{
  "task": "TASK-461 (Phase-2 category #2: cookies_coffee) — Adversarial QA M1 re-check",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "SCRATCHPAD/TASK-461_cookies_QA_report.md", "action": "modified", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/m1_diff.py", "action": "created", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/m1_recheck.py", "action": "created", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/m1_facts.py", "action": "created", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/m1_changed_ids.json", "action": "created", "sha256": "SEE_FINAL_MESSAGE"}
  ],
  "counts": {
    "candidate_new_sha256_match": "1/1 (af492d78… == coordinator spec)",
    "candidate_preM1_sha256_match": "1/1 (81ecc1fa… == originally gated artifact, preserved)",
    "changed_products_indep_diff": "17/17 (m1_diff.py; exact match to coordinator's list, incl. 1 with both insightLine+rowVerdict = ck-8710502139017)",
    "non_copy_leaves_changed": "0/18 changed leaves (m1_diff.py); 0/234 vs origin baseline (isolation still copy-fields-only)",
    "m1_clause_carriers_now": "0/117 (was 13/117) (m1_recheck.py)",
    "fivegrams_over2x_corpuswide": "0 distinct (own census, m1_recheck.py); widened net: 6-grams 0, 4-grams 3 chains at exactly 3x (below ≥5 MEDIUM threshold)",
    "fact_retention_13_carriers": "13/13 still state both red flags truthfully, zero verbatim repeats among the 13 new constructions (m1_facts.py, manual read)",
    "fact_retention_4_breakers": "4/4 surgical single-clause edits, facts unchanged incl. ck-311128 satFat-missing disclosure preserved verbatim (m1_facts.py)",
    "hygiene_17_em_dashes": "0/17 (m1_recheck.py)",
    "hygiene_17_banned_vocab": "0/17 (m1_recheck.py)",
    "hygiene_17_empty_fields": "0/17 (m1_recheck.py)",
    "opening3_unique_postfix": "IL 117/117, RV 117/117 (m1_recheck.py)",
    "score_grade_rank_parity_postfix": "0/117 mismatches vs origin/master; grade dist C:9 D:27 E:81 unchanged",
    "trackC_stance_driver_retained": "17/17 read in full, each keeps a distinct opening finding + closing takeaway, none reshuffled-synonym (manual read)",
    "findings_new": "CRITICAL 0 / HIGH 0 / new MEDIUM 0; M1 resolved; M3 unchanged (data-lane, not a copy defect)"
  },
  "commands_run": [
    {"cmd": "Get-FileHash cookies_coffee_copy_overhaul.json (== af492d78…)", "exit_code": 0},
    {"cmd": "Get-FileHash cookies_overhaul_v1_preM1.json (== 81ecc1fa…)", "exit_code": 0},
    {"cmd": "python -X utf8 m1_diff.py", "exit_code": 0},
    {"cmd": "python -X utf8 m1_recheck.py", "exit_code": 0},
    {"cmd": "python -X utf8 m1_facts.py", "exit_code": 0}
  ],
  "not_done": [
    "Full 117-product re-gate NOT performed (out of scope per coordinator — targeted 17-product re-check only; original verdict for the other 100 stands)",
    "run_gates G1-G8 not re-run (still the git-owning sibling's job at commit time)",
    "No fix/edit/close performed — zero git writes, scratchpad only, no subagents used"
  ],
  "self_check": "Acceptance: M1 clause census = 0 carriers AND no new 5-gram chain >2x AND all 13+4 facts retained AND no new hygiene/isolation defect in the 17. Observed: 0 carriers, 0 five-grams >2x (3 four-grams at exactly 3x, below threshold), 17/17 facts retained with distinct phrasing, 0 em-dash/vocab/empty in the 17, isolation and parity unchanged. Verdict: GO (0 CRITICAL / 0 HIGH / 0 new MEDIUM)."
}
```
