# Adversarial QA Report — TASK-461 Phase-2 #3: CHOCOLATE TABLETS copy overhaul

**Category:** chocolate_tablets (35 products) · **Route:** /hashvaot/chocolate-tablets
**Candidate:** `choctab_copy_overhaul.json` sha256 `e7cd57b6f2e28ef8d3d2b81398c30c437e8009a23a14f0ee08ca87c6f6efddfd` (matches spec)
**Baseline:** origin/master blob `45c962fe…` (independently fetched; extracted sha256 `34191fe5…`)
**Challenger:** adversarial-qa-agent (Opus, independent lane) · Date 2026-07-02

---

## VERDICT (original pass): GO_WITH_FIXES — SUPERSEDED, see "FIX RE-CHECK" section below for current GO
**0 CRITICAL · 0 HIGH · 3 MEDIUM.** Copy is trace-grounded, hygiene-clean, and holds the TASK-455
guardrail (co-leadership tie preserved, zero health-halo). The 3 MEDIUMs are a soft
recommendation-language drift on one line, a "full twin" over-claim on a near-twin pair, and a
routed pre-existing baseline-expansion defect. None blocks launch; all are documentable/monitorable.

**M1 and M2 were fixed by the author lane and re-verified — current verdict is GO (0/0/0 open).**
See the "FIX RE-CHECK" section for the independent re-derivation against the new artifact
(sha `c03cc84f…`). M3 remains routed and out-of-scope (unchanged, was never a blocker).

---

## TRACK V — VERIFICATION (PASS)

### V1 — Field isolation (PASS)
Independent re-derivation (`v_isolate.py`): only `insightLine` + `rowVerdict` changed, on **35/35**
products. Everything else byte-identical:
- `_meta` identical · all non-product top keys identical
- score/grade/rank mismatches: **0/35** · `_hash_no_rank` mismatches: **0/35**
- **expansion mismatches: 0/35** (confirms candidate did NOT touch expansion — relevant to M3 below)
- product order preserved; ID set identical.

### V2 — Claim-by-claim truth audit (35/35 TRUE on hotspots; 0 fabrications)
All orchestrator hotspots verified against independently-built rank tables (see appendix):

| Hotspot | Claim | Verdict |
|---|---|---|
| 2a co-leaders | ct-002 65.8 / ct-001 65.1, gap **0.7**; #3 is 9.8pt away | TRUE — genuine tie, no 3rd within 2pt |
| 2b density ct-003 | "הטבלה השמנה ביותר" = fat_g #1 (55g) | TRUE (correct axis: fat) |
| 2b density ct-017 | "צפוף קלורית יותר מה-90%" + "מהצפופות" = kcal #1 (610 > 607/592) | TRUE (correct axis: kcal) |
| 2c sugar min | ct-008 0.2g "הנמוך במדף כולו" | TRUE (#1, 0.2<0.3) |
| 2c sugar max | ct-031 65g "המתוקה ביותר" | TRUE (#1) |
| 2c sodium max | ct-032 357mg "שיא ובפער עצום"; gap #1-#2 = 142mg | TRUE |
| 2c fiber max | ct-002 25g "הגבוה במדף" | TRUE (#1) |
| 2c longest list | ct-010 "הרשימה הארוכה במדף כולו" (15 commas) | TRUE (#1) |
| 2c most additives | ct-016 "יותר תוספי מזון מכל מריר אחר" (3, scope=dark) | TRUE (#1 among מריר) |
| 2c protein | ct-012 "עשירת החלבון של המדף" (12.5g) | TRUE (#1) |
| 2c demerara | ct-012 "היחידה שממתיקה בסוכר דמררה" | TRUE (only "דמררה" in corpus) |
| 2c satfat min | ct-019 "שומן רווי הנמוך בקטגוריה" (11g) | TRUE (#1 lowest) |
| 2c percentages | 44/56/50/34/43/10/16/47/52/31/28% all in parsed list | TRUE (12/12) |
| 2d maltitol-order | ct-008 & ct-011 "ממתיק לפני קקאו"; ct-034 "קקאו ראשון" | TRUE (all 3 match parse) |
| 2e twins | ct-024 sodium 124 rank #3 "מהגבוהות" (hedged, not #1) | TRUE — see M2 for panel-identity |
| 2f white cocoa | "אפס מוצקי קקאו" / "קקאו רק כשומן" | TRUE — technically precise (butter≠solids) |
| 2g corrupted parse | ct-001/002/016 — no claim leans on corrupted segment | TRUE (verified each) |
| 2h tokens | PGPR×5, שמן מנטה, אבקת שומן קוקוס, קמח סויה, דבש×2, לקטוז, E500 | TRUE (all in list) |

**PGPR (2h):** exactly **5** products carry E476 in both the ingredient string AND `d4_additives`
(ct-016, ct-021, ct-022, ct-028, ct-033); copy names PGPR on exactly those 5. Spec guessed "×4?" —
actual is 5, fully grounded, no phantom.

### V3 — Hygiene (PASS)
- Em/en dashes: **0/70** · Engine-mechanic vocab (חציון/חיסרון/פרמטר/נקודות/NOVA/BSIP…): **0/70**
- Antithesis "ולא": **0** · Opening first-3-words: **70/70 unique** · OFF refs: **0**
- 5-gram repeats >2×: **0** · 4-gram repeats >2×: **0** (no stamped editorial phrase)
- Treat-framing distribution: "פינוק" 3× (ct-001/002/033 only — restrained, not stamped);
  "ממתק" 14× (the honest "this is candy" category truth, appropriately distributed) — NOT template drift.

### V2i — Baseline defects (routed, not introduced)
- **"פרמטרים" leak** existed on baseline ct-036 ("בכל שאר הפרמטרים") → **gone** in candidate. ✓
- **Stale "רק C" expansion** on ct-002/ct-001 (both now grade **B**): `comparisonContext` still says
  "וגם הוא רק C". Confirmed **pre-existing on baseline; candidate did NOT touch expansion**
  (byte-identical). This is M3 — a routed flag, not a blocker.

### V4 — hebrew_readability gate (70/70 analyzed; 2 flags, 1 false-pos, 1 → M1)
- ct-008: flag "הימנעו" → **FALSE POSITIVE** (substring of noun "ההימנעות" = avoidance, descriptive).
- ct-030: flag "כדאי לקנות" → **GENUINE** soft recommendation → **M1**.

---

## TRACK C — CHALLENGE

**Engine opinion with stance+driver:** every line leads with a finding and names its driver
(engineering vs concentration; sweetener-order; cocoa-% honesty; sodium/salt; nut/nougat share). No
number-recitation template. Voice matches the cereals-golden insight-first bar.

**Health-halo:** ZERO hits of בריא/בריאות/מזין/דל-שומן across all 70 strings. The two B-darks are
explicitly de-halo'd ("נשארת ממתק עתיר שומן וקלוריות", "פינוק להנאה מדודה ושום דבר מעבר", "לא 'בריא'").
Sugar-free products consistently attribute low sugar to *engineering* (ממתיקים/מהונדס), never to health.
**The TASK-455 relief framing is honored** — "stopped double-penalizing chocolate," never "dark is healthy."

**Co-leadership (the prior-QA hotspot):** both #1/#2 are written as a shared top
("אחת משתי הטבלות שחולקות את ראש הדירוג" / "השותפה השנייה בצמרת"), in *opposite logic* (engineering vs
90% concentration). No sole-leader overclaim reintroduced. Tie treated as a tie. ✓

**מריר-naming honesty:** ct-018 (43%), ct-023/024 (47%), ct-027 (50%), ct-019 (50%) each call out that
"מריר" on the pack outruns the cocoa reality, tied to a real sub-50% cocoa figure. Defensible, varied.

**E-grade proportionality:** 17 E-grades are differentiated (mint vs salt twin, Toblerone honey double-
sweetening, coconut-fat-powder oddity, nougat/pistachio/hazelnut share, white-choc last place). Not stamped.

### Findings

**MEDIUM — M1 (content-agent): soft recommendation-language on ct-030.**
"…וכדאי לקנות אותו בתור בדיוק זה" ("worth buying it as exactly that"). hebrew_readability flags it as
RECOMMENDATION language. Bari copy states the engine's opinion; a buy-verb crosses into advice.
ct-031 ("כדאי לקרוא לזה בשמו") and ct-032 ("כדאי להתייחס אליו") use "כדאי" as a *framing* device
(defensible), but ct-030 is a literal purchase suggestion. Route: soften to a framing, not a buy-instruction.

**MEDIUM — M2 (content-agent): "תאומה מלאה" over-claims panel identity on ct-024.**
ct-024 (salt) RV: "ההבדל היחיד מהמנטה הוא מלח ים… כל השאר זהה" and IL "תאומה מלאה". The panels are
**not** fully identical: satfat 20 vs 19, carbs 50 vs 51, sugar 48 vs 49, fiber 8.2 vs 8.3, protein
6.2 vs 6.3 (ct-024 vs ct-023). Only sodium (124 vs 13) is the material difference the copy names, and
the ±1 deltas are label rounding — so the *spirit* is defensible and the sodium call is correct — but
"כל השאר זהה / תאומה מלאה" is literally false against the panel. Route: hedge to "כמעט זהה" / name the
sodium as the one material difference without asserting full identity.

**MEDIUM — M3 (data-agent / content-agent): stale "רק C" expansion on the two B-grade products.**
ct-002 and ct-001 flipped C→B in TASK-455 but their `expansion.comparisonContext` still reads
"וגם הוא רק C". Pre-existing baseline defect, **outside this candidate's scope** (expansion byte-
identical). Additionally these expansion strings carry a baseline em-dash and "ולא דרך פשטות" antithesis —
also out of scope here. Route into a later expansion-field pass; do not let it block the copy handover.

### Weakest 3 lines (Track C, for author awareness — not blockers)
1. **ct-030 RV** — the "כדאי לקנות" buy-verb (M1).
2. **ct-024 RV** — "כל השאר זהה" literal over-claim (M2).
3. **ct-036 RV** — "והמדף מרוויח מזה שיש לקלאסיקה תחרות" ("the shelf benefits from the classic having
   competition") is a light editorial flourish that says little about the product itself; borderline
   filler versus the insight-first bar. Acceptable, weakest of the set.

---

---

## FIX RE-CHECK (targeted, not a full re-gate) — 2026-07-02

**Scope re-verified independently:** diffed `choctab_overhaul_v1_preQA.json` (sha `e7cd57b6…`, the
artifact this report originally gated) against the new `choctab_copy_overhaul.json`
(sha `c03cc84fccd91b8ac8d5e7aecfb55eb6dad2c2d3e57568cf7ac91144172d1236`). Diff is **exactly**
`ct-024:{insightLine,rowVerdict}`, `ct-030:{rowVerdict}` — matches the coordinator's claim, no other
product touched. Re-ran full isolation vs origin/master baseline: 0 non-allowed-field violations,
0 `_hash_no_rank`/score/grade/rank/expansion mismatches — clean, unchanged from the original pass.
The 33 untouched products and their prior verdict stand without re-derivation, per instruction.

### M1 (ct-030 buy-verb) — RESOLVED
Old: "...וכדאי לקנות אותו בתור בדיוק זה" (buy-verb "לקנות" governed by recommendation modal "כדאי").
New: "...וההגדרה הזו אומרת עליו הכל" ("and that description says it all") — a framing close, no verb
aimed at the reader. Buy-verb scan (כדאי/מומלץ/קנו/בחרו/...) on the new string: **0 hits**.
hebrew_readability on the new string: **is_clean = True** (previously flagged True-positive is gone).
No em-dash, no engine vocab, no new numbers introduced. **M1 closed.**

### M2 (ct-024 twin over-claim) — RESOLVED
Old: "תאומה מלאה... כל השאר זהה" (full twin / everything else identical) — literally false against
the panel (satfat, carbs, sugar, fiber, protein all differ by up to 1 unit from ct-023).
New: IL "אותו ממתק כמעט שורה בשורה, **ורק הנתרן** באמת זז" (almost line-for-line, **only** sodium
really moves) and RV "בשאר הלוח ההפרשים בין השתיים **קטנים מכדי להטריד מישהו**" (elsewhere on the
panel the gaps are **too small to bother anyone**). Re-derived deltas against my own rank tables:
kcal Δ0, fat Δ0, satfat Δ1.0 (19→20), carbs Δ-1.0, sugar Δ-1.0, fiber Δ-0.1, protein Δ-0.1, score gap
Δ-0.4 (both E, near-tie). Every non-sodium delta is ≤1 unit — the new wording asserts *near*-identity
and *immateriality* of the small deltas, not full identity, and both assertions are now literally true.
Sodium jump 13→124mg (Δ111) correctly named as "the real difference" / "among the highest on the
shelf" (ct-024 sodium rank #3/35, verified in the original pass). **M2 closed.**

### No new defects (3-block re-scan)
Em-dashes: 0/3 · engine vocab: 0/3 · new bare numbers introduced: 0/3 · hebrew_readability: 3/3 clean.
Shelf-wide re-scan post-fix: opening first-3-words **70/70 still unique**; 5-gram repeats >2×: **0**
(unchanged). No collateral drift from the two edits.

### Author-surfaced item (a): shared 5-gram "עיסת קקאו סוכר חמאת קקאו" (ct-013 / ct-035)
**ACCEPT.** Both ingredient strings genuinely open `עיסת קקאו, סוכר לבן, חמאת קקאו...` in that literal
order — this is a factual recitation of matching label order, not a stamped editorial phrase. It
occurs in exactly 2 products (not >2, the anti-template threshold), and the shelf-wide 5-gram scan
confirms **zero** phrases repeat more than twice anywhere in the 70 strings. Two independently-labeled
products that happen to share a real ingredient order are expected in a 35-product single-category
corpus; flagging this would punish accuracy, not enforce variety.

### Author-surfaced item (b): buyer-intent phrasing consistency (ct-027, ct-023) vs the ct-030 ruling
**Line confirmed, both ct-027 and ct-023 stand — no retroactive flag.** The dividing test: does the
sentence carry an **imperative/recommendation verb aimed at the reader** ("worth buying," "buy this"),
or does it **describe** the product/who it suits, leaving the decision to the reader?
- **ct-027** "הצורה והטעם הם **הסיבה לקנות**" (shape/taste are the reason [people] buy it) — frames
  *why the product sells* as an observation about the market, not an instruction to this reader. No
  second-person imperative. Closest remaining case to the line, but still descriptive framing, not advice.
- **ct-023** "מי שיודע את זה מראש **יקבל** בדיוק את מה שקנה" — third-person conditional describing an
  outcome for a hypothetical informed buyer; no verb directed at the reader.
- **ct-018/ct-034** "מי שקונה... עושה עסקה הוגנת" / "בחירה הגיונית למי ש..." — same third-person-conditional
  pattern: describes fit, not advice.
- **ct-031/ct-032** "כדאי לקרוא לזה בשמו" / "כדאי להתייחס אליו" — "כדאי" here governs a **framing verb**
  (name it, regard it), not the **purchase verb itself**. This is the precise distinction from the old
  ct-030: "כדאי **לקנות**" put the recommendation modal directly on the buy action; these two put it on
  an interpretive act instead.
- **Rule going forward (for the fan-out, not authored here):** "כדאי" + {לקרוא, להתייחס, לדעת, לזכור}
  = acceptable framing device. "כדאי"/"שווה" + {לקנות, לבחור, לרכוש} = recommendation drift, same class
  as the original ct-030 defect. Route this line to content-agent as a standing rule for future categories.

### Updated verdict: **GO**
0 CRITICAL / 0 HIGH / 0 open MEDIUM (M1, M2 resolved; M3 was always routed/out-of-scope, unchanged).
Both fixes are surgical, trace-accurate, and introduce no new defects. Shelf-wide hygiene and
isolation hold. Category clears the D10 challenge-gate condition (report exists, 0 open CRITICAL) —
go-live authority remains Product Agent's, not this gate's.

---

## Appendix — rank tables (per-100g, independently derived from candidate)
- **Sugar:** min ct-008 0.2 → max ct-031 65.0
- **SatFat:** min ct-019 11.0 → max ct-001 32.0
- **Fat_g:** min ct-019 27.0 → max ct-003 55.0
- **Kcal:** min ct-016 390 → max ct-017 610
- **Sodium:** min ct-019 0.0 → max ct-032 357.0 (#2 ct-025 215, #3 ct-024 124)
- **Protein:** min ct-031 4.2 → max ct-012 12.5
- **Fiber:** min (nonzero) ct-011 1.6 → max ct-002 25.0 (ct-016 22.0 #2)
- **Additives:** max 3 (ct-016, ct-032); PGPR/E476 in 5 products.
