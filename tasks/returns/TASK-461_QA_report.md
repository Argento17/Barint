# TASK-461 — Adversarial QA / Red-Team Report (brined-cheeses copy overhaul)

Date: 2026-07-02  ·  Scope: 36 products, insightLine + rowVerdict re-authoring
Challenger: Adversarial QA Agent (Opus, independent of author lane)
Candidate: `brined_v2_copy_overhaul.json` sha256 `9ba7fc112fd43230aff032fe2aed986ecc117a755eaab6197c89a43f5886fe62`
Baseline: origin/master `brined_cheeses_frontend_v2.json` sha256 `583db15028fb2fc5c0df0e1c4d4ead2fa81c4bd48ce2522db443ef960ea8c339`

## VERDICT: GO

Track V (verification) is fully green. Track C (challenge) has **zero CRITICAL and zero HIGH findings**.
Every factual claim, superlative, ranking, twin-identity assertion, and editorial jab in the 36
re-authored blocks was independently re-derived from the candidate's own data and **confirmed true**.
The one production-copy error the author claims to have fixed (bc-035 false "14g fat") is confirmed
real and correctly removed. Findings below are MEDIUM/observational only — none block go-live.

Note on my authority: I verify and challenge; I do not fix or close. Proposing RETURNED to orchestrator.

---

## Track V — Deterministic Verification (all PASS)

**V1. Field isolation** — my own origin/master fetch vs candidate:
- 36/36 products: only `insightLine` + `rowVerdict` differ; all other fields byte-identical.
- `_meta` identical; `_hash_no_rank` identical on all 36; score/grade/rank identical on all 36.
- Both copy fields changed on every product (0 accidental no-ops, 0 partial).
- Non-copy product content byte-identical (stripped-dump comparison).
- Baseline freshness: my independent `git show origin/master:…` produced sha `583db15…`,
  exactly the author's baseline. Not stale.

**V2. Copy hygiene** (my own scan, not the author's `audit.py`):
- Em/en/horiz/figure dashes: **0** total. Clause-hyphen (` - `): 0.
- Banned engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/"N נקודות"): **0**.
  (One substring hit "מבנה" in bc-038 = "המבנה הדרוש לצלייה" — plain culinary Hebrew for grilling
  structure, NOT the engine's structural_class dimension. Not leakage. See M-2.)
- Antithesis (" ולא " / ", לא "): 0.
- Opening-3-words uniqueness: insightLine 36/36 unique, rowVerdict 36/36 unique.
- OFF references: 0 in copy. (`"off_used": false` in `_meta` is the correct provenance flag,
  byte-identical to baseline — not an OFF data reference.)
- Digit-bearing copy: 8/36 products, each justified as a fired-driver number (see V4).

**V3. Hebrew leakage gate** (`C:\Bari\integrations\clients\hebrew_readability.py`, the required instrument):
- All 72 strings: `is_clean = True`. Zero `leaks`, zero `flags`. Deterministic PASS.

**V4. Score distribution unchanged** (scores byte-identical, re-derived from candidate):
- n=36, min 47.1, max 82.7, median 66.15, mean 66.85, pop-stdev 8.11.
- Grades A:3 B:18 C:13 D:2. Duplicate scores: 82.7×2, 67.4×2, 64.7×2, 63.6×3.

---

## Track V — Independently-built rank tables (the audit backbone)

SODIUM high→low (mg): bc-036 1628 | bc-002 1550 | bc-024 1500 | bc-018 1400 | bc-017 1400 |
bc-007 1300 | bc-014 1300 | … | bc-013 720 | bc-004 600 | bc-005 600 (min, tied twins)
PROTEIN high→low (g): bc-039 24 | bc-038 22 | bc-041 22 | bc-007 21 | bc-044 21 | bc-002 20.5 |
bc-037 20 | … | bc-048 8 | bc-043 7.3 | bc-047 7 (min)
FAT high→low (%): bc-048 31 | bc-039 28 | bc-041/035/044 24 | bc-038 23 | … | fat==5 group ×14
KCAL high→low: bc-039 356 | bc-048 355 | bc-041 310 | … | bc-006/012/011 93 (min)
INGREDIENT-COUNT (top-level): bc-047 10 (unique max) | bc-043 7 | bc-031/010/016/048 6 | … | bc-036 2 (min)
PRESERVATIVE-FREE (ingredient string, no משמר): bc-013, bc-036, bc-038 = exactly 3
STABILIZERS (E406/E410): bc-016, bc-043, bc-047 = exactly 3
NITRATE (E252): bc-044 = only 1
BUTTER (חמאה in list): bc-010 = only 1
LACTIC-CULTURE declared (תרבית): bc-013 = only 1
GDL (E575): bc-009, bc-010 = 2
D grades: bc-043, bc-047 = exactly 2

---

## Claim-by-claim truth audit — every hot spot CONFIRMED

| Product | Claim | Verdict |
|---|---|---|
| bc-004 | "הכי פחות מלוחה במדף" / "הכבישה העדינה ביותר במדף" | TRUE — 600mg = shelf min (tied w/ its byte-identical twin bc-005; see M-1) |
| bc-036 | "המלוחה במדף כולו" (1,628 מ"ג) | TRUE — shelf max sodium |
| bc-002 | "שיא המלח של קבוצת ה-5%" (1,550) | TRUE — max sodium of fat==5 group AND 2nd of 36 |
| bc-002 | "חלבון שכמעט מוביל את קבוצת הרזות" | TRUE — 20.5g = 2nd of 14 in fat==5, 0.5 behind bc-007 |
| bc-007 | "אלופת החלבון של קבוצת ה-5%: 21 גרם … יותר מכל מתחרה רזה אחרת" | TRUE — 21g = unique max of fat==5; no leaner product beats it |
| bc-013 | "הבולגרית היחידה במדף שמצהירה על תרבית לקטית" | TRUE — only ingredient list containing תרבית |
| bc-013 | "אחת משלוש בלבד שמוותרות על חומר משמר" | TRUE — preservative-free set = {bc-013, bc-036, bc-038}, exactly 3 (verified at ingredient-string level; bc-014's empty d4 is a parse gap — its list DOES carry חומר משמר, correctly excluded) |
| bc-039 | "שיא החלבון של המדף" / "חלבון שמוביל את כל המדף" | TRUE — 24g = unique shelf max protein |
| bc-039 | "צפיפות קלורית מהגבוהות בו" (356) | TRUE — top-1/2 kcal (356 vs 355); hedged "מהגבוהות", no "highest" claim |
| bc-039 | "החלומי הכבד ביותר בו" | TRUE — fat 28 = halloumi max |
| bc-035 | "הבולגרית העשירה ביותר במדף" + "מוסיפה שמנת" | TRUE — fat 24 = unique max of bulgarit-named; שמנת present in list; panel fat = 24.0 (NOT the false 14g) |
| bc-035 | "מכפילה ויותר את הקלוריות" vs lean Tzfatit | TRUE — 274/117 = 2.34× |
| bc-017 | "התווית עצמה מדווחת 14 גרם שומן" | TRUE — panel fat = 14.0 (dry-matter 24% name hedged "ככל הנראה") |
| bc-044 | "היחיד במדף עם חומר משמר ממשפחת הניטראטים" | TRUE — E252 present only in bc-044 |
| bc-044 | "מתחת לאחיו" | TRUE — 57.7 below all 3 other halloumis (gap ≥5.9) |
| bc-001 | "פטת העיזים הטובה במדף" / "מעל כל שאר גבינות העיזים" | TRUE — top goat 76.1, gap 2.9 > 2-pt noise floor |
| bc-018 | "החלבון הכי גבוה בין גבינות העיזים" + "המלח הכי כבד ביניהן" | TRUE — 17g goat-max protein AND 1,400 goat-max sodium |
| bc-037 | "חלבון שמוביל את כל קבוצת ה-16%" + "מעט … נוגעות בעשרים גרם" | TRUE — 20g = max of fat==16; protein≥20 set is 7/36 |
| bc-029 | "המדורגת הגבוהה ביותר בין הפטות השמנות" + "מלח מהעדינים במדף" | TRUE — top fat-feta (gap 2.2); 770 = 4th-lowest sodium |
| bc-047 | "הרשימה הארוכה במדף" + "החלבון הנמוך במדף כולו" + "סוגרת את הדירוג" | TRUE — 10 items unique-longest; 7g min protein; rank 36 |
| bc-043 | "אחת משתי הגבינות היחידות שיורדות ל-D" | TRUE — D grades = {bc-043, bc-047} |
| bc-048 | "המוצר השמן ביותר במדף" + "חלבון מהנמוכים" + "המלח דווקא מרוסן" | TRUE — fat 31 max; protein 8 = 3rd-lowest; sodium 800 = 5th-lowest |
| bc-010 | "היחידה במדף שמכניסה חמאה לרשימה" + factory jab | TRUE — only butter-carrier; list also has milk proteins + E575 |
| bc-024 | "המלוחה בין הכבשים" | TRUE — 1,500 = max sodium of sheep set (next 1,100/930) |
| bc-016 | "מייצבים מאצות ומחרובים" | TRUE — E406/E410 present only in 3 of 36 |
| bc-038 | "החלומי המוביל במדף" + "בלי חומר משמר" | TRUE — top halloumi (gap 2.1); preservative-free |
| bc-009 | "מווסת חומציות … ייצור מזורז" | TRUE — E575 GDL present (function: acidity regulator) |
| bc-011 | "יד כבדה יותר על המלח" | TRUE — 1,200 = highest sodium of גד 5% siblings |
| bc-003/031 | "חלבון גבוה בין הרזות" (16 / 18.5g) | TRUE — 4th / 3rd of 14 in fat==5 |
| bc-006/032 | "פחות חלבון מרוב המדף" (10g) | TRUE — 29/36 have more |

**Twins / near-twins (numeric identity + noise-rule discipline):**
- bc-004/bc-005: nutrition + ingredients + score (82.7) byte-identical → presented as "same cheese." TRUE.
- bc-006/bc-012: nutrition identical, 1.8-pt gap → "too small to sway a purchase." Correct (< 2-pt floor).
- bc-027/bc-028: 0.1-pt gap → "same bottom line." Correct.
- bc-039/bc-041: 0.0-pt gap → "same score," bc-041 lower fat+kcal. TRUE and correctly framed.
- bc-024 vs sheep siblings (1.2–1.3 gap): no rank claim made; only the factual +sodium difference. Correct.

**Consistency:** No two products make conflicting superlatives. "Saltiest overall" (bc-036, whole shelf)
and "saltiest of the 5% group" (bc-002, scoped) are non-overlapping and both true. "Fattest overall"
(bc-048) vs "richest bulgarit" (bc-035, scoped) — distinct scopes, both true. No collision found.

**Confidence honesty:** All 36 are `confidence: verified`, sub_reason null. The only partial panels are
3 products with null sugar (bc-031, bc-037, bc-048) — **all three carry an explicit partial-panel
disclosure** ("לוח תזונה … חסר", "ההערכה זהירה", "הגיע … עם לוח תזונה חלקי"). No full-panel product
over-hedges; no partial-panel product hides it. No phantom confidence.

---

## Track C — Adversarial Challenge (per-dimension)

**C1. Does each line carry the engine's opinion (owner's bar)?** YES. Every insightLine opens with a
stance, not an ingredient count (0/36 open with a bare number or "N רכיבים"). rowVerdicts follow the
standing→why→catch contract. The copy consistently names the *fired driver* — sodium/brine for the
salt-limited products (bc-036, bc-002, bc-018, bc-024), fat choice for the rich ones (bc-035, bc-048,
the halloumis), processing shortcuts for the industrial ones (bc-009 GDL, bc-010 butter/proteins,
bc-016/043/047 stabilizers), and the protein return where it's the story (bc-007, bc-037, bc-039).

**C2. Is every editorial jab publicly defensible?** YES — the two sharpest jabs both sit on verifiable
facts: bc-010 "מריחה יותר ממפעל מאשר ממחלבה" (butter + milk proteins + E575 all literally in the list,
6 ingredients vs shelf median 3); bc-009 "מחמיץ במהירות תעשייתית" (E575 GDL present, function = acidity
regulator). bc-044's nitrate call-out is the single E252 on the shelf. All attackable claims held.

**C3. Confidence honesty:** PASS (see above).

**C4. Hebrew naturalness:** Strong across the board — reads as a knowledgeable friend, not a template.
Weakest 3 lines (still acceptable; flagged for fan-out learning, NOT blockers):
- bc-014 insight "של פעם ברוח הטובה … שמזכיר שכבשו אותה כמו פעם" — the doubled "פעם/כמו פעם" leans on
  the product name twice; slightly folksy, borderline filler.
- bc-030 insight "בולגרית אמצע הדרך במלוא מובן המילה" — "אמצע הדרך במלוא מובן המילה" is a near-cliché;
  the verdict recovers it, but the opener is the softest stance on the shelf.
- bc-015 verdict "משלם על הבחירה הזו בדירוג, ובשום דבר אחר" — the trailing "ובשום דבר אחר" flirts with
  the banned "X ולא Y" antithesis rhythm (it passed the literal gate; watch this pattern in fan-out).

**C5. Proportionality:** PASS. Every pair presented as "the same" is < 2-pt (0.0–1.8). The only pair
presented as a real defeat within a family is bc-044 vs its halloumi siblings (gap 5.9–8.0 ≥ 2). Tone
scales with the gap; no near-tie is dramatized as a meaningful loss.

**C6. Framing / lawyer risk:** Low. Claims are corpus-relative and hedged where appropriate
("מהגבוהות", "מהמלוחות", "ככל הנראה"). No health claim, no absolute nutritional assertion, no
comparative attack on a named competitor beyond what the label states. bc-035's dropping of the old
false "14g fat" *reduces* legal exposure vs production.

---

## Findings

### CRITICAL — none
### HIGH — none

### MEDIUM / observational (do NOT block launch)
- **M-1 (bc-004, note-only):** "הכי פחות מלוחה במדף" is a strict superlative, but sodium 600mg is
  *tied* with bc-005 (its byte-identical twin). Defensible because bc-005 is literally the same cheese
  (nutrition+ingredients+score identical) and bc-005's own copy says so — no third product is at 600.
  A hostile reader parsing "הכי" as strictly-unique could quibble; the twin framing neutralizes it.
  No change required. Routes to: content-agent (awareness only).
- **M-2 (bc-038, false-positive noted for the record):** "המבנה הדרוש [לצלייה]" contains "מבנה". This is
  culinary structure of a grilling cheese, not the engine's `structural_class`. Passed the leakage gate
  (`is_clean=True`). No action.
- **M-3 (fan-out learning, C4):** three softest lines (bc-014, bc-030, bc-015) — acceptable now,
  useful as negative examples when the pattern fans out to other categories. Routes to: content-agent.

## Cross-track self-check (independence seam)
Track V is green because the data is internally consistent *and* the underlying assumptions are correct:
scores are byte-identical to live production (I re-fetched origin/master myself), and every claim was
re-derived from the candidate's own nutrition/ingredient/additive fields, not from the author's scripts
or report. An outside reviewer re-running my rank tables would reach the same verdict. No case where a
"pass" rests on a wrong assumption.

## Note to orchestrator
This is a copy-only change to a consumer-facing artifact (go-live-adjacent, but this lane commits
nothing per the TASK-461 no-git ruling). Content sign-off hard rule: this report is the SECOND of the
two mandatory sign-offs. Both gates now green. The DoD item "run_gates G1–G8 with --baseline" is the
sibling git-owning lane's step at commit time and is out of this lane's scope. Proposing RETURNED.
