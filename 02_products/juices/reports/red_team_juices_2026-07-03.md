# TASK-461 Phase-2 #6 — JUICES copy overhaul — Adversarial QA report

**Category:** juices (`/hashvaot/juices`, `juices_frontend_v3.json`) · **Scope:** 17 products, 34 strings (17 insightLine + 17 rowVerdict)
**Challenger:** adversarial-qa-agent (Opus, independent lane) · **Date:** 2026-07-02
**Candidate:** `juices_copy_overhaul.json` sha256 `84b030f5b02aac6ead9b3657117b16716f1378878d25dae716f4747eaa6e4b29` (matches spec)
**Baseline:** independently fetched `git show origin/master:bari-web/src/data/comparisons/juices_frontend_v3.json` → blob `95c42010…` (matches spec), file sha256 `1dd4cfda…`

## FINAL VERDICT (post fix re-check): GO — 0 CRITICAL / 0 HIGH open / 3 MEDIUM (non-blocking)
Original pass (below) found 2 HIGH + 3 MEDIUM on artifact `84b030f5…`. Both HIGHs (RT-1 jc-018 superlative, RT-2
jc-021/jc-024 score-literal leak + contradiction) were fixed in overwritten artifact `9ba0dbca…` and independently
re-verified in the "FIX RE-CHECK" section at the bottom of this report — read that section for the current state.
The narrative below is preserved as the original-pass record.

## ORIGINAL VERDICT (superseded, artifact 84b030f5…): GO_WITH_FIXES — 0 CRITICAL / 2 HIGH / 3 MEDIUM
All 34 strings are trace-grounded, hygiene-clean, and the six-way A tie / free-sugar honesty are handled correctly.
Two HIGH findings — one is a real over-strong superlative in the *new* copy (jc-018); the other is a pre-existing
consumer-visible score-literal leak + on-card contradiction in the **untouched** expansion field (jc-021/jc-024),
surfaced but out of this task's 2-field scope. Neither is CRITICAL; neither blocks the isolation-correctness of the
overhaul. Recommend the jc-018 superlative be softened before ship; route the expansion defect to a follow-up pass.

---

## TRACK V — VERIFICATION

### V.1 Field isolation — PASS (17/17)
- Product count 17/17; id set + id order identical to baseline.
- Only `insightLine` + `rowVerdict` changed. **Zero** non-copy field changes (score/grade/rank/nutrition/d4/_meta/_hash_no_rank all byte-identical).
- Non-product top-level (`_meta`, `generatedAt`, `totalProducts`) byte-identical.
- Key-set identical per product; **all 17 carry rowVerdict** (no keys added/removed). No empty copy fields.
- Both fields changed value on all 17 (17 insightLine + 17 rowVerdict = 34 authored strings).

### V.2 Claim-by-claim truth audit — 34/34 strings assessed

**Rank tables (re-derived independently from the candidate artifact):**

*Score / grade (all 17):* 85/A ×6 (jc-003,006,001,005,011,002) → 49.1/D jc-017 → 39.9/D jc-019 → 39.8/D jc-018 →
38.1/D jc-020 → 37.4/D jc-021 → 36.9/D jc-022 → 35.4/D jc-024 → 33.4/E jc-025 → 33.3/E jc-026 → 30.3/E jc-023 → 28.5/E jc-027.

*Sugar g/100ml (desc):* 12.6 jc-006 | 11.4 jc-017 | 9.5 jc-026 | 9.4 jc-021 | 9.4 jc-022 | 9.3 jc-027 | 9.0 jc-024 |
8.7 jc-003 | 8.6 jc-002 | 8.2 jc-001 | 4.7 jc-018 | 4.5 jc-020 | 4.5 jc-023 | 4.4 jc-025 | 1.2 jc-019 · **MISSING: jc-005, jc-011**

*kcal/100ml (desc):* 54 jc-006, 54 jc-005 | 49 jc-017 | 47 jc-001 | 44 jc-011 | 43 jc-003, 43 jc-002 | 41 jc-022 |
40 jc-021, 40 jc-024, 40 jc-026 | 39 jc-027 | 20 jc-018/020/025/023 | 9 jc-019

*Additive count (d4, desc):* 8 jc-023 | 5 jc-018 | 5 jc-026 | 4 jc-020 | 4 jc-027 | 2 jc-019/021/024/025 | 1 jc-022 | 0 (all six A + jc-017)

*Sub-pools:* juice_100 = {003,006,001,005,011,002} · fruit_drink = {017,019,018,020,025,026,023,027} · nectar = {021,022,024}

*Sweeteners/sulfites:* sucralose (E955) in jc-019/018/023; sulfites (E220–E228) in jc-018/020/023; diet=jc-019 (sucralose+acesulfame-K).

**Hotspot verdicts (all TRUE unless noted):**

| # | Claim | Data | Verdict |
|---|---|---|---|
| 2a | Six-way A tie at 85 | exactly 6 at 85, all juice_100 | TRUE |
| 2a | Tie language honest across all six (none claims sole lead) | jc-003 "חולק את ראש הטבלה עם חמישה"; jc-001 "אחד מששת השווים"; jc-011 "שווה בין שווים"; jc-006/005/002 "קבוצת המובילים / שורת ה-A" | TRUE |
| 2a | 3 OJ panels near-identical | jc-001/002 "מיץ תפוזים", jc-003 "100% מיץ תפוזים סחוט טבעי"; jc-002 "זהה מילה במילה לתפוז של פרימור" | TRUE |
| 2a | jc-003 sole varietal-namer (ולנסיה) | no other A-product names a cultivar | TRUE |
| 2b | jc-006 12.6g = shelf-max sweetness measured | next is 11.4 (jc-017) | TRUE |
| 2b | jc-019 1.2g = shelf-min | min of all measured | TRUE |
| 2c | jc-005 54 kcal real; pomegranate-sweetness inference | 54 kcal confirmed; = jc-006 (measured pomegranate); hedged "סביר להניח… גם אם המספר עצמו חסר"; sugar genuinely NULL | DEFENSIBLE (see note) |
| 2d | jc-017 leads sweetened by notable gap | 49.1 vs next 39.9 = **9.2 pt** | TRUE |
| 2d | jc-017 "רובו מהסוכר המוסף" | sugar listed after 25% cranberry; not strictly derivable from artifact | **MEDIUM RT-3** |
| 2e | jc-025 pear 7.2% > 2× lemon 3.1% | 2.32× | TRUE |
| 2e | jc-018 2% grapes = **smallest fruit touch in whole review** | jc-025 lists grapefruit-components **1.6%** < 2% | **HIGH RT-1** |
| 2e | jc-020 apple 12% vs grapes 5%; 17% fruit "פי כמה" vs jc-018 2% | 12/5 confirmed; 17 vs 2 = 8.5× | TRUE |
| 2e | jc-026 sugar-before-fruit, 3.5% grapes, "פחות מעשירית פרי" | sugar item 2 (before fruit); grapes 3.5%; total fruit 9.1% <10% | TRUE |
| 2e | jc-027 water+sugar lead, "פחות מעשירית" fruit | water 1st, sugar 2nd; fruit 9.8% <10% | TRUE |
| 2e | jc-023 "רשימת התוספים הארוכה ביותר"; 11% grapefruit | d4=8=max; 6+5=11% | TRUE |
| 2f | Nectar trio noise-level chain | 21→22 = 0.5, 22→24 = 1.5 (adjacent <2pt); span 21→24 = 2.0 | TRUE |
| 2f | jc-024 "פחות פרי מאשר באפרסק ובתות-בננה"; "שישה רכיבים" | mango 25% < ~40% both; label = exactly 6 components | TRUE |
| 2f | jc-021 "כמעט שליש מחית אפרסק"; "מטפס ל-40%" | 31.5% purée; 31.5+8.5=40; largest single-fruit share | TRUE |
| 2f | jc-022 "התות תורם 3%"; 5 fruits on can; apple+orange most | strawberry 3%; 5 fruits; 14+12 dominate | TRUE |
| 2g | jc-021/jc-024 stale pre-de-anchor trio ordering FIXED in new copy | old jc-021 "הנמוך בציון" (now 37.4=top); old jc-024 mango "האמצעי" (now 35.4=bottom); new copy corrects both | TRUE (fix real) |
| 2g | jc-024 old copy leaked "35.4"/"35.3" — absent in new rowVerdict | confirmed present in baseline RV, absent in candidate RV | TRUE (fix real) |
| 2g | jc-023 old 19-vs-18 self-contradiction fixed | baseline IL "תשעה עשר" vs RV "שמונה עשר"; new copy drops literal count | TRUE (fix real) |
| 2h | No new claim leans on corrupted parse tails (jc-019/025/023) | new copy uses only clean head segments | TRUE |
| 2h | Stale expansion score-literals jc-021/024 remain byte-identical | expansion identical=True both; literals "35.3"/"35.4" untouched | TRUE untouched — but see **RT-2** |
| 2i | No health-halo on 6 A-products; each carries free-sugar caveat | jc-003 "סוכר חופשי בנוזל, בלי הסיבים"; all six honest | TRUE |
| 2i | Diet product not haloed for low sugar | jc-019 "יוצאת מדורגת מתחת לגרסה הרגילה… שמרה על המרחק מהפרי" | TRUE (anti-halo) |

*jc-005 inference note:* the copy stays on the right side of truth discipline — it names the missing datum, does not
assert a sugar number, and anchors on a **measured** 54 kcal equal to the known-measured pomegranate jc-006 (same fruit).
Hedged, material, disclosed by the confidence chip. R2 clause covers jc-005 (infers, discloses) and jc-011 (discloses, does not infer). PASS.

### V.3 Hygiene — PASS
- Em dashes **0** · en dashes **0** · engine/Tier-4 vocab **0** · antithesis "X-not-Y" **0** · R4 recommendation drift **0** · OFF refs **0**
- Opening-3-words: insightLine 17/17 unique, rowVerdict 17/17 unique, **all-34 34/34 unique**
- Panel-number strings = exactly the 4 justified extremes (jc-006 sugar-max, jc-017 sweetened-max, jc-019 sugar-min, jc-026) **+ 1 kcal (jc-005)** — matches spec allowance. All other digits are label fruit-% that ARE the story.
- 5-gram census: only repeats >2× are the R2-exempt sugar **unit** string `גרם סוכר ל-100 מ"ל` ×4 (jc-006/017/019/026) — measurement unit, not editorial phrasing. Missing-sugar disclosure `נתון הסוכר לא הופיע על האריזה` ×2 (jc-005/011), within ≤2 bar.
- "בסקירה" ×6 across 34 (18%): 5/6 anchor a **distinct verified superlative** (scope qualifier), 1 an "only-one-in-review" — semantic work, not stamping. **Not a finding.**

### V.4 Hebrew leakage/readability — 32/34 is_clean; 2 documented false-positives
`hebrew_readability.analyze` flags jc-006 "12.6" and jc-017 "11.4" as `score_mechanic`. Probed: the heuristic flags **any decimal**
(`\d+\.\d+`) — "54 קלוריות" (integer) passes, "12.6 גרם סוכר" fails purely for the decimal point. Both flagged strings carry
explicit `גרם סוכר ל-100 מ"ל` units and are the R2-exempt shelf sugar extremes (the fired driver). Known false-positive class
(TASK-453 backlog). **MEDIUM RT-4** (tooling), not a copy defect.

---

## TRACK C — CHALLENGE (the owner's bar)

Every string carries stance + driver; category tension (fruit juice = free sugars) is stated without moralizing and
without halo; the 100%-juice group is scored A yet each string still says "free sugar in a liquid, no fibre" honestly.
Ties are framed as ties (six-way A, nectar trio). Brand-adversarial name-vs-content claims (jc-018/025/026/027 "the name
promises fruit; the list opens with water and sugar") are proportionate and label-grounded. Hebrew reads natural, not translated.

**Weakest 3 strings:**
1. **jc-018 insightLine** — "2% ענבים… נגיעת הפרי הקטנה ביותר בסקירה **כולה**." The word "כולה" (the *whole* review) is an
   absolute superlative with a live counterexample (jc-025 grapefruit-components 1.6%). See RT-1.
2. **jc-017 rowVerdict** — "רובו מהסוכר המוסף" leans on external knowledge (cranberry is low-sugar) not derivable from the
   artifact. Directionally right, but a food scientist could ask for the basis. See RT-3.
3. **jc-005 rowVerdict** — the pomegranate-sweetness inference is the most inference-dependent line; it is well-hedged and
   anchored on measured kcal, so it holds, but it is the closest any string comes to narrating an unmeasured value.

---

## FINDINGS BY SEVERITY

### HIGH — should resolve before launch
**RT-1 (jc-018 superlative over-reach).** New insightLine: "כמות הענבים כאן, 2%, היא נגיעת הפרי הקטנה ביותר בסקירה כולה."
Evidence: full-corpus fruit-share census — jc-025 label lists "רכיבי אשכוליות (1.6%)", smaller than 2%. jc-025's own new
copy calls that 1.6% "וקורט אשכולית" (a pinch of grapefruit), i.e. treats it as a fruit touch. The absolute "smallest in the
**whole** review" is therefore not bulletproof under `superlative_claims_need_corpus_rankcheck`.
Implication: a competitor (Prigat) can point at 1.6% and call the claim false.
Routes to: **content-agent** — soften ("מהקטנות בסקירה" / scope to smallest single-fruit *juice* share, or drop "כולה"). No score/data impact.

**RT-2 (jc-021 / jc-024 stale expansion score-literals + on-card contradiction — PRE-EXISTING, out of scope).**
The **untouched** `expansion.comparisonContext` (a consumer-visible expansion string) still reads:
- jc-021: "הנמוך בציון מבין שלושת נקטרי ספרינג בסקירה **(35.3)**" — frames peach as lowest-of-trio at literal 35.3; current score is 37.4 (top/parity). The new rowVerdict now says the opposite → **the card contradicts itself**.
- jc-024: "האמצעי בציון… **(35.4)**… שני הנקטרים האחרים… מצדיקים את הפער" — frames mango as middle; current 35.4 = bottom.
Evidence: expansion byte-identical to baseline (candidate did NOT touch it); literals "35.3"/"35.4" present in both.
Implication: raw score-literal leak in consumer copy (same class as the tracked hard_cheeses "67 נקודות" leak) **plus** a
rowVerdict↔expansion contradiction the new copy sharpens. Not introduced by this candidate; outside the authorized 2-field scope.
Routes to: **content-agent + data-agent** — fold into a follow-up expansion pass (mirror the choctab "רק C" handling: sibling note + later pass). Does not block the 2-field overhaul.

### MEDIUM — document or monitor
**RT-3 (jc-017 "רובו מהסוכר המוסף").** Plausible from ingredient ordering (added sugar after 25% cranberry; cranberry naturally low-sugar) but not strictly derivable from the artifact; identical claim existed in baseline. Route to content-agent as monitor; acceptable as written.

**RT-4 (hebrew_readability false-positives).** jc-006/jc-017 fail `is_clean` only because the heuristic flags every decimal as `score_mechanic`; both are unit-bearing shelf-sugar extremes, not scores. Route to TASK-453 (tooling); not a copy defect.

**RT-5 ("בסקירה" ×6 / panel-unit 5-gram ×4).** Observational. "בסקירה" each time anchors a distinct verified superlative (not decorative); the ×4 5-gram is the R2-exempt sugar unit. Neither reads stamped. Monitor only; no rework.

---

## Summary Assessment
**Justified** for 32/34 strings and all three claimed truth-defect fixes (verified against baseline). **Plausible-but-unverifiable**: RT-3.
One **potentially-incorrect** superlative in the new copy: RT-1. One **pre-existing structural leak** surfaced but out of scope: RT-2.
No data-absent scoring buried (the two NULL-sugar products jc-005/jc-011 disclose the gap; jc-005's inference is hedged and disclosed).

## Verdict (superseded by Fix re-check below)
**GO_WITH_FIXES.** Recommend RT-1 (jc-018) softened before this category ships; RT-2 routed to a follow-up expansion pass
(pre-existing, do not block); RT-3/4/5 documented. Proposing task status **RETURNED** to orchestrator with these findings.

---

## FIX RE-CHECK (targeted, not a full re-gate) — 2026-07-02

**New artifact:** `juices_copy_overhaul.json` sha256 `9ba0dbcab35dc36774c6116f90befee85eb23c5002a64c4af5a66fba0ccc3ad9` (OVERWRITTEN in place)
**Pre-fix (the artifact this report originally gated):** sha256 `84b030f5b02aac6ead9b3657117b16716f1378878d25dae716f4747eaa6e4b29`
(re-verified from my own untouched `qj_run/CANDIDATE.json` copy, hash-confirmed unchanged since the first pass)

### Independent full-tree diff (own script, not author-report)
- **New vs origin/master:** exactly **36 leaves changed** — 34 copy fields (insightLine ×17 + rowVerdict ×17) +
  `products[10].expansion.comparisonContext` (jc-021) + `products[12].expansion.comparisonContext` (jc-024).
  Matches the coordinator's claim exactly; no other leaf differs (scores/grades/ranks/nutrition/d4/_meta untouched).
- **New vs my prior gate (84b030f5):** exactly **4 leaves changed** —
  `products[6].rowVerdict` (jc-017, RT-3), `products[8].insightLine` (jc-018, RT-1),
  `products[10].expansion.comparisonContext` (jc-021, RT-2), `products[12].expansion.comparisonContext` (jc-024, RT-2).
  Everything gated GO/GO_WITH_FIXES/PASS in the original report is **byte-identical and stands unchanged**.

### 1. RT-1 (jc-018) — RESOLVED
New insightLine: *"שני אחוזי ענבים הם כל הפרי שבבקבוק, פחות מכל מוצר אחר בסקירה"* (2% grapes is ALL the fruit in the
bottle — less than every other product in the review). Re-derived total-fruit-per-product census (sum of every fruit-
derived ingredient share, all 17 products): jc-018 = **2.0% total**, strictly the minimum. Next-lowest is jc-026 at
**9.1%** (apple 5.6 + grape 3.5) — matches the author's cited "next is 9.1%." jc-025's total is **7.2+3.1+1.6 = 11.9%**,
well above 2.0% — the prior 1.6%-component counterexample no longer applies because the claim is now correctly scoped
to *total* fruit content, not "smallest single ingredient touch." No surviving counterexample anywhere in the 17-product
corpus (checked all: 2.0 < 9.1 < 9.8 < 11.0 < 11.9 < 17.0 < 25.0 ≤ 25.0 ≤ 25.0 < 40.0 = 40.0 < 100 ×6). **TRUE, bulletproof.**

### 2. RT-3 (jc-017) — RESOLVED
Old (flagged): "...ורובו מהסוכר המוסף" (inference: "mostly added sugar," not artifact-derivable).
New: "...כשהסוכר ברשימה מגיע מיד אחרי החמוציות" (the sugar in the list comes immediately after the cranberries) — a
pure list-position fact. Verified against the parsed ingredient string `מים, מיץ חמוציות (25%) (עשוי מרכז), סוכר`:
sugar is indeed the 3rd/last-listed ingredient, immediately following the 25% cranberry concentrate. Fully derivable
from the artifact; the non-derivable inferential leap is gone. **TRUE, fully artifact-grounded.**

### 3. RT-2 exception (jc-021 / jc-024 comparisonContext) — RESOLVED, ruled shippable
- **Score literals:** confirmed **absent** in both new strings (regex swept for any `\d\d\.\d` pattern — zero hits;
  "35.3"/"35.4" gone).
- **Tail byte-preservation:** verified programmatically — `new_opening + old_tail == new_text` for both products; the
  entire tail after the rewritten opening clause is character-identical to the pre-fix text. Minimal-edit as claimed.
- **On-card contradiction: dead.** jc-021 (score 37.4, top of the noise-level trio): rowVerdict "נמצא בגובה אחד עם שאר
  נקטרי ספרינג, בהפרשים שברמת הרעש"; new expansion opening "קרוב בציון לשני נקטרי ספרינג האחרים, וההפרשים... קטנים" —
  both agree: tight cluster, no ranking claim. jc-024 (score 35.4, bottom of trio): rowVerdict "סוגר את שלישיית
  הנקטרים... במרחק קטן"; new expansion opening "אחרון בשלישיית נקטרי ספרינג בסקירה, במרחק קטן" — both agree: last,
  small gap. Both cards now self-consistent and consistent with the actual 0.5/1.5-pt adjacent gaps. **Confirmed dead.**
- **No engine vocab or purchase verbs** introduced in either edited opening (swept against the banned-term list and the
  R4 purchase-verb list — zero hits in all 4 edited leaves).

**Ruling (a) — residual tail text (em dashes + "מצדיקים את הפער בציון"):** `expansion.comparisonContext` was never
inside the em-dash-0 rule's scope in this program (that rule binds insightLine/rowVerdict; the choctab precedent left
an analogous expansion defect — "רק C" — untouched and routed as a sibling note rather than fixed inline). The RT-2
action was explicitly scoped as minimal-edit: kill the score-literal leak and the self-contradiction, touch nothing
else. **Ruling: acceptable to ship as-is.** The residual em-dashes (2 in jc-021, 1 in jc-024) and the pre-existing
phrase are lower-priority pre-existing debt, not a new defect, and the two things this exception was authorized to fix
(raw score leak, on-card contradiction) are both verifiably gone. Routed again, once, to the same follow-up expansion
pass already on record — not a new blocker, not escalating further.

**Ruling (b) — new inconsistency between edited openings and preserved tails:** checked both. jc-021's tail is
compositional (fruit%, sugar, distance-from-100%) and doesn't reference ranking, so it doesn't conflict with the new
ranking-neutral opening. jc-024's tail sentence ("the other two nectars' 40% fruit justifies the score gap") is
consistent with the new opening's "small distance" framing — both acknowledge a gap exists and attribute it to fruit%.
**No new inconsistency found.**

### 4. Corpus-wide regression sweep (all 34 authored strings, post-fix)
- Openings first-3-words: **34/34 unique** (unchanged from pre-fix; the 2 edited strings did not collide with any other).
- Em dashes across the 34 insightLine/rowVerdict fields: **0** (unchanged).
- Engine/Tier-4 vocab: **0** (unchanged).
- No new numeric claims introduced beyond the pre-existing justified set (jc-017's "11.4" and jc-021/jc-024's "40%/25%/9.4"
  were already present pre-fix; the edited clauses themselves introduce zero new digits).

### Updated Verdict
**GO.** All three targeted items (RT-1, RT-3, RT-2 exception) are resolved and independently re-verified against the
artifact, not the author's report. No new defects found anywhere in the 36-leaf changed surface or the untouched
remainder. RT-4 (hebrew_readability decimal false-positive, tooling/TASK-453) and RT-5 (observational, no action) stand
unchanged as documented, non-blocking MEDIUMs. **Proposing task status: RETURNED** (two-gate content sign-off complete
pending orchestrator verification) — this agent does not close.
