# TASK-461 Phase-2 #4 — HUMMUS copy overhaul, Author report (Content Agent)

**Status: DRAFT until Adversarial QA.** Re-authored `insightLine` + `rowVerdict` for the hummus page
(`bari-web/src/data/comparisons/hummus_frontend_v5.json`) in the owner-accepted register.

## 1. Isolation proof (zero git writes, origin/master only)

| item | value |
|---|---|
| baseline source | `git show origin/master:bari-web/src/data/comparisons/hummus_frontend_v5.json` |
| origin blob sha (git ls-tree) | `2fbd70fdc8368b93333d01b34fa3726397b380ad` |
| baseline copy (scratchpad) | `hummus_origin.json`, 280,410 bytes, sha256 `d5efee990356fb426b64205b47f6ceed57734581fb4a00e62815e19aa9c9ec29` |
| final artifact | `hummus_copy_overhaul.json`, 275,170 bytes, sha256 `50f4be85e91848c3c3224e65842adf6068ecffc04e393541b8220194325a24b6` |
| git ops used | `ls-tree`, `show` only. No add/commit/branch/checkout/stash/push. Nothing under `C:\Bari` written. |
| serialization | origin round-trips byte-identical with `json.dumps(ensure_ascii=False, indent=2)`; artifact written the same way |
| field isolation | structural walk origin↔new: **92 diffs, all `products[i]/insightLine|rowVerdict`; 0 illegal paths**; `_meta` byte-identical; (score, grade, rank) sequence identical 57/57 |

## 2. STRUCTURAL FINDING (for orchestrator/QA — decide before handover)

**22 of 57 products have NO `rowVerdict` key in production** — exactly the vegetable-spread types
(matbucha 10, eggplant 7, pepper 5; ranks 3,6,10,19,23–26,42,45–57 minus hummus-typed ones).
`rowVerdict` exists only for `hummus_spread` (33) + `masabacha` (2) = **35 products**.
I re-authored **92 strings (57 IL + 35 RV)** and did **NOT inject new keys** — adding a field the
renderer may conditionally display is a structural change beyond the 2-field copy mandate.
The task prompt assumed 114 strings; the artifact's real copy surface is 92.

## 3. Metrics (script-derived, `h_apply_audit.py` → `h_audit.txt`, 86 PASS / 0 FAIL)

| metric | old (origin) | new |
|---|---|---|
| em dashes (both fields) | **97** | **0** |
| "ולא" antithesis | 4 explicit (audit's 6 incl. אלא/לא-X variants) | **0** (define-by-negation variants also purged) |
| products reciting panel numbers | **43/57** | **6/57**, each a verified shelf extreme (table below) |
| engine vocabulary (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/נקודות) | present | **0** |
| opening 3-word uniqueness | template-heavy | **IL 57/57 unique, RV 35/35 unique** |
| 5-gram census (anti-template, cookies-M1 gate) | n/a | **max repetition = 1** across all 92 strings (gate allows ≤2) |
| partial-data hedge clause | inconsistent | exactly 2 uses of the one sanctioned clause ("הפירוט שהגיע בסריקה חלקי") on the 2 `confidence: partial` products (#2, #3) |
| mean words IL / RV | ~29.9 (all strings) | IL 17.7 (9–26, stdev 4.7); RV 29.3 (24–35, stdev 3.2) |

### Panel-number budget (6/57, each justified)
| rank | product | number | justification (script-checked) |
|---|---|---|---|
| 1 | חומוס מסעדות | 231 מ"ג נתרן | sole shelf minimum (next: 257) |
| 26 | סלט פלפלים קלויים | 32 קלוריות | sole shelf minimum kcal (next: 74) |
| 48 | סלט מטבוחה פיקנטי | 852 מ"ג | >2× shelf median (395); presented as twin+tie, not max |
| 49 | מטבוחה פיקנטית | 852 מ"ג | twin of #48, same basis |
| 55 | ממרח פלפלים קלויים | 852 מ"ג | same extreme tier; "בין המלוחים", not max (864 exists) |
| 56 | פלפל צ'ומה | 599 קלוריות | shelf max kcal (267 above runner-up); sodium-max stated qualitatively |

## 4. Truth defects in LIVE copy found & fixed (flag in PR)

1. **#57 (חציל על האש בטחינה) — live IL cites "20 גרם שומן שהם 81% מהקלוריות".** The page's own
   `_meta.nutrition_policy` suppresses fat entirely (HUM-001: Shufersal scraper captured the
   saturated-fat sub-row; Product ruling TASK-080 hides fat). Live copy builds a consumer claim on
   data the artifact itself rules corrupted. New copy carries **zero fat-gram claims shelf-wide**.
2. **Widespread "סלט" editorializing in live copy** ("מצדיק את הסלט שבשם", "נראה כסלט") against the
   owner boundary rule (memory `feedback_raw_vs_prepared_boundary`: never classify via "סלט").
   New copy uses "סלט" only inside quoted label ingredients/product names (5 occurrences, all
   listed in `h_audit.txt`, all quoted).

## 5. Data flags (Data lane, not fixed here — copy avoids reliance on them)

- **d4_additives under-extraction:** #10 list contains פוטסיום סורבט but d4 = [E330] only;
  #7 list contains חומצת לימון but d4 = [E500, E202]. Additive-count claims in my copy use d4 only
  where script-verified (#2, #21, #38, #39, #57); elsewhere text-based ("משמר", "מייצב").
- **`_meta.confidence_distribution` says `partial: 57`** while products carry verified 55 / partial 2
  — stale meta (outside 2-field scope; byte-preserved).
- **#2 protein 18.2g** is ~2× every other hummus tub, on a `partial` skeletal parse — copy
  deliberately does NOT repeat the protein claim (old copy trumpeted it twice).

## 6. Family map (ruled once, differentiated by real deltas only)

| family | members (rank) | treatment |
|---|---|---|
| אסלי pair | 4, 5 | identical list+panel+score → twin ruled once, #5 = mirror verdict |
| גלילי pair | 8, 9 | identical recipe, Δ0.1 → tie ("הפרש שאין לו משמעות") |
| מסעדה pair + variant | 12, 13 (identical), 29 (+soy oil) | pair ruled once; #29 differentiated by the one real delta (soy oil), rank drop noted without hard causal claim |
| the identical quad | 14, 15, 16, 17 | one recipe, four labels, Δ≤0.2 → "אותה כף חומוס בארבע תחפושות"; choose by price |
| מטבוחה twins + hot variant | 23, 24 (identical), 25 (jalapeño variant) | twins ruled once; #25 = the one real delta |
| אבו מרוואן pair | 27, 30 | same 26% recipe, Δ0.2 → "אפסי" |
| זעתר rivals (different recipes) | 33, 34 | differentiated by real deltas: zaatar 0.6% vs 0.17%+sumac; Δ0.2 = "קוסמטיים" |
| צנובר rivals | 21, 28 | real delta = roster 2 vs 3 additives; Δ1.7 < 2 → "קטן מכדי להכריע" |
| עם טחינה rivals | 38, 39 | both 5 additives, Δ0.1 → shared verdict, brand-preference framing |
| מסבחה pair (real gap) | 22, 41 | Δ4.5 ≥ 2 → ranked verdict: #22 more tahini + cleaner list; #41 starch+guar |
| פיקנטי twins | 48, 49 | identical incl. 852mg sodium → twin ruled once |
| E1422 matbucha pair | 45, 46 | near-identical, Δ0.5 → "צמד כמעט זהה" |

## 7. Superlative rank-check table (every superlative in the new copy, script-verified)

| claim (product) | check | result |
|---|---|---|
| #1 "הכי פחות מלוח בקטגוריה" | sodium min sole | PASS (231 < 257) |
| #2 "רשימת העזר הרזה ביותר בין ממרחי החומוס" | d4=1 unique among hummus_spread | PASS |
| #2 "המלח גבוה מכל ממרח חומוס אחר" | sodium max among hummus_spread | PASS (480 > 396) |
| #3 "המטבוחה במיקום הגבוה ביותר" | top matbucha, gap ≥2 | PASS (60.7 vs 57.2) |
| #6 "ממרח הפלפלים המוביל" + low-salt | top pepper, gap ≥2; sodium 2nd-lowest | PASS |
| #7 "אלוף הטחינה" + "הצנצנת הצפופה ביותר בין ממרחי החומוס" | tahini 40 max; kcal max among tubs | PASS |
| #10 "מהקלות במדף כולו" | kcal 2nd-lowest | PASS (74) |
| #19 "מדורג ראשון בקבוצתו" | top eggplant, gap ≥2 | PASS (56.4 vs 50.7) |
| #26 "הצנצנת הקלה ביותר במדף" | kcal min sole | PASS (32 < 74) |
| #32 "סגנית אלופת הטחינה" | tahini 37 = 2nd | PASS |
| #48/#49 "יותר מכפול מהמקובל במדף" | 852 > 2×median(395) | PASS |
| #52 "היחיד במדף שמוותר על חומר משמר" | "משמר" absent from list, sole | PASS ([52] only) |
| #55 "בין המלוחים במדף" (tie, not max) | 852 = ranks 2–4 | PASS |
| #56 "הצפוף והמלוח ביותר במדף" | kcal 599 max AND sodium 864 max | PASS |
| #57 "שורת העזר הארוכה במדף" | d4=6 unique max | PASS (next: 5) |
| #22 "הבכירה מבין שתי המסבחות... בפער ממשי" | gap ≥ 2 | PASS (4.5) |

All sub-2pt adjacencies are phrased as ties (script checks 5bb/5bc/5bd/5aw/5ax). The one real
grade-band cliff (#2→#3, 7.0pt) is the only place a between-product gap is asserted as decisive.

## 8. Before/after ×5

**#1 חומוס מסעדות (B)**
- OLD IL: "יחס טחינה חריג (31%) לצד 34% חומוס דוחף את החלבון ל-10.1 גרם — מהגבוהים בין הממרחים, עם נתרן מהנמוכים במדף. מהבולטים במדף בזכות הבסיס הטחיני-עשיר; שורת התוספים מותירה אותו ב-B ולא מעבר."
- NEW IL: "המוביל של המדף עושה את השילוב שכולם מפספסים: יד רחבה בטחינה ויד קמוצה במלח."

**#14 חומוס יום יום (C, quad member)**
- OLD IL: "ממרח יומיומי על מתכון הבסיס — 61% חומוס ו-15.5% טחינה, חלבון 7.9 גרם. סולידי אבל לא בולט: יחס טחינה ממוצע וחומר משמר ברשימה, בדיוק כמו רוב המדף."
- NEW IL: "אחד מארבעה: המתכון הזה בדיוק מופיע במדף תחת ארבעה שמות שונים, וזו האריזה הראשונה שלו בטבלה."

**#32 חומוס מועשר 40% עם חריף (C, label-vs-reality)**
- OLD IL: "טחינה כרכיב ראשון (37%) דוחפת את החלבון גבוה (10.6 גרם), עם תוספת פלפל חריף. הבסיס הטחיני-עשיר הוא היתרון; הרשימה הארוכה — מייצב וחומר משמר — היא מה שמחזיק אותו בבינוני."
- NEW IL: "על השם 40%, ברשימה 37%: תוספת החריף מדללת את הטחינה, והרשימה עצמה מסבירה את הפער."

**#52 ממרח פלפלים קלויים (D, honest-tension)**
- OLD IL: "ממרח פלפלים בן 13 רכיבים — 54% פלפל אדום, עגבניות מיובשות וסילאן. יורד ל-D כי ההרכב מהצפופים בקבוצה: ריבוי תוספים ומייצב על בסיס ירק, רחוק מסלט פלפלים פשוט."
- NEW IL: "היחיד במדף שמוותר על חומר משמר, והדירוג בכל זאת נמוך: שמן קנולה שלישי ברשימה, סילאן ממתיק את הפלפלים, ורשימת הרכיבים חוצה את עשרת הפריטים."

**#57 חציל על האש בטחינה (D, truth fix)**
- OLD IL: "הבסיס טוב — חציל קלוי 44% וטחינה גולמית 14% — אבל זה ממרח עתיר-שמן: 20 גרם שומן שהם 81% מהקלוריות... " *(fat claim on suppressed/corrupted data)*
- NEW IL: "סוגר את הטבלה עם שורת העזר הארוכה במדף: שישה רכיבי עזר שונים, מעמילן מעובד ועד צמד מייצבים, סביב חציל קלוי וטחינה שראויים ליותר."

## 9. QA hotspot suggestions (for the Adversarial gate)

#1 sole-minimum sodium + "כמעט שליש" tahini; #2 partial hedge + tub-max sodium; #7/#32 tahini
crown/runner-up pairing; #12↔#29 soy-oil delta framing; the quad's "one product" ruling; #35 nested
'סלט חומוס' 48% reading; #48/#49/#55 852mg tie handling vs #56's 864 max; #52 sole-no-preservative;
#56 canola-first + double-max; #57 six-additive max; boundary rule: all "סלט" occurrences quoted.

## Return contract

```json
{
  "task": "TASK-461 (Phase-2 #4, hummus)",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "SCRATCHPAD/hummus_copy_overhaul.json", "action": "created", "sha256": "50f4be85e91848c3c3224e65842adf6068ecffc04e393541b8220194325a24b6"},
    {"path": "SCRATCHPAD/hummus_origin.json", "action": "created", "sha256": "d5efee990356fb426b64205b47f6ceed57734581fb4a00e62815e19aa9c9ec29"},
    {"path": "SCRATCHPAD/h_copy.py", "action": "created", "sha256": "5ecb50c5c80d2ce7e1d0d0af1fe10fc516f98cda4529e32293d6fe7a5668e435"},
    {"path": "SCRATCHPAD/h_apply_audit.py", "action": "created", "sha256": "873136bddeafe7b4964255b66f5e5da6c3c3270662f89bf1e5a9762b6dbb321a"},
    {"path": "SCRATCHPAD/h_audit.txt", "action": "created", "sha256": "25c799377e54fdb1f3bcb5a13de256cdf3e305dc0a361670048ff131fe5be73c"},
    {"path": "SCRATCHPAD/TASK-461_hummus_author_report.md", "action": "created", "sha256": "SELF"}
  ],
  "counts": {
    "strings_reauthored": "92/92 (57 insightLine + 35 rowVerdict; 22 vegetable-spread products carry no rowVerdict key in origin blob 2fbd70fd — none added)",
    "field_isolation_diffs": "92/92 legal (structural walk, h_apply_audit.py check 3a/3b; illegal=0)",
    "scores_grades_ranks_changed": "0/57 (check 3d, tuple-sequence equality vs origin)",
    "em_dashes": "0 new vs 97 old (checks 4a; old from h_oldcopy.py)",
    "vela_antithesis": "0 new vs 4 old (check 4b)",
    "panel_number_products": "6/57, each a script-verified shelf extreme (check 4d + section 3 table)",
    "banned_engine_vocab": "0/92 (check 4c)",
    "opening_uniqueness": "IL 57/57, RV 35/35 (check 4f)",
    "five_gram_max_repetition": "1 (gate <=2), all 92 strings (check 4g)",
    "partial_hedge_clause": "2/2 on the 2 confidence=partial products (check 4h)",
    "superlative_rank_checks": "16/16 PASS (checks 5a-5bq subset, section 7 table)",
    "audit_checks_total": "86 PASS / 0 FAIL (h_audit.txt)",
    "words_IL": "min 9 / mean 17.7 / max 26 / stdev 4.7 (n=57)",
    "words_RV": "min 24 / mean 29.3 / max 35 / stdev 3.2 (n=35)"
  },
  "commands_run": [
    {"cmd": "git ls-tree origin/master -- bari-web/src/data/comparisons/hummus_frontend_v5.json", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/data/comparisons/hummus_frontend_v5.json > SCRATCHPAD/hummus_origin.json", "exit_code": 0},
    {"cmd": "python -X utf8 h_facts.py", "exit_code": 0},
    {"cmd": "python -X utf8 h_oldcopy.py", "exit_code": 0},
    {"cmd": "python -X utf8 h_apply_audit.py", "exit_code": 0}
  ],
  "not_done": [
    "rowVerdict NOT added to the 22 vegetable-spread products that lack the key in production (deliberate: field-addition is a structural change; orchestrator decision documented in section 2)",
    "Adversarial QA gate (independent lane) — this artifact is DRAFT until it passes",
    "data flags in section 5 routed, not fixed (d4 under-extraction #7/#10; stale _meta confidence_distribution; #2 protein outlier)"
  ],
  "self_check": "h_apply_audit.py full suite: 86 PASS / 0 FAIL; artifact sha256 50f4be85e91848c3c3224e65842adf6068ecffc04e393541b8220194325a24b6 reproduces from hummus_origin.json + h_copy.py deterministically"
}
```
