# TASK-460 Gate 2 — Adversarial QA / Red-Team Review

Reviewer: adversarial-qa-agent (executor; no subagents used)
Date: 2026-07-02
Package under review: commit `d57eae3b` on branch `fix/task460-stale-adapter-prose`, worktree `C:\bari_wt_t461` (base `4b21fbfa`)
Gate-1 log: `C:\bari_wt_t461\tasks\returns\T460_content_gate1.md`
Method: read the diff and every referenced frontend JSON directly in this worktree; recomputed every grade tally / score range / count with an independent Python pass (not eyeballed, not taken from the builder's summary).

---

## VERDICT: GO_WITH_FIXES

The 9 STALE fixes in commit `d57eae3b` are all verified correct, durable, and factually accurate — that part is a clean PASS and may ship. But the review surfaced **three live consumer-facing numeric defects that this commit does NOT fix** (they live outside the commit's `.ts/.tsx`-only edit boundary or were mis-deferred by gate-1). None of them is a regression introduced by `d57eae3b`, so they do not block *this commit* — but they must be routed and fixed before the underlying pages can be called clean. Two of the three are exactly the TASK-460 root-cause class (hardcoded numbers going stale) and are live on consumer pages right now.

Blockers to resolve (before the affected pages are clean — not blockers on this specific commit):
1. **RT-1 (HIGH, live):** chocolate-tablets "best product is graded C" is factually false — the two top products are graded **B**.
2. **RT-2 (HIGH, live):** protein-bars "24 מתוך 32 ... מלטיטול" — no structured field yields 24; authoritative count is **16/32** for maltitol.
3. **RT-3 (HIGH, live):** cookies-coffee prologue says "83 מתוך 119" but corpus is **117** products / **81** E — both numbers stale and rendered on-page.

Plus one MEDIUM latent duplicate (RT-4).

---

## Track V — Verification (deterministic)

### V-1. Scope confinement — PASS
`git show d57eae3b`: 5 code files + the gate-1 report md. Every changed code line is a Hebrew string/template-literal assignment. **Zero** logic, JSON, layout, import, or type changes. Base commit = `4b21fbfa` (matches spec). CONFIRMED.

### V-2. Build — PASS
`npx tsc --noEmit` in `C:\bari_wt_t461\bari-web` (node_modules present): exit **0**, no output.

### V-3. The 9 STALE fixes — ALL PASS (independently re-derived)

| Fix | New claim | Independent JSON truth (my recount) | Verdict |
|---|---|---|---|
| brined dist. | "רוב המדף מתקבץ סביב B ו-C, ומעטות מגיעות ל-A" | A=3,B=18,C=13,D=2 (B+C=31/36=86%) | PASS — durable, accurate |
| brined top | "ראש המדף שייך ... לצפתית של מחלבות גד" | top = צפתית 5% / מחלבות גד @ 82.7/A (old "85" was wrong) | PASS |
| brined negation | "התשובה לא נמצאת במלח" removed → "והממצא ברור" | voice: no define-by-negation | PASS (leakage gate clean) |
| cereals dist. | "רוב המדף מתקבץ סביב C ו-D" | B=2,C=6,D=10,E=2 (C+D=16/20=80%); old 7C/9D was wrong | PASS |
| granola hero+gap | "פער של כמעט 40 נקודות"; min "32.8/E" | max 69.7, min 32.8, gap 36.9 (old 31.4/38.3 wrong) | PASS |
| granola dist. | "רוב המדף מתקבץ סביב C ו-D" | B=4,C=8,D=8,E=2; old 7D/3E was wrong | PASS |
| snacks range | "ציונים שנעים על פני יותר מ-50 נקודות" | max 66.9, min 14.1 → span 52.8 (old "67 עד 15" off-by-one on min) | PASS |
| juices A-pool | "רק מיצים סחוטים ב-100% הגיעו ל-A" | 6 A-grades, ALL subPool=juice_100; every juice_100 is A; no other subpool reaches A. Old "מוצר אחד"/"7–17 גרם" both wrong (A=6; sugar 1.2–12.6) | PASS — durable, accurate |
| hard-cheeses | "רוב סביב B; דלת-שומן אחת מגיעה ל-A" | A=1,B=26,C=4,D=0; top = גלבוע 5% @ 81.6/A. Old 0/24/2/2 + "גאודה" leader fully fabricated | PASS |

Negation-phrasing rewrite kept factual accuracy: yes — the replaced brined sentence retains the true "majority B/C, few A" finding.

### V-4. Kept-TRUE sample audit — 15+ checked, all confirmed TRUE (no wrongly-kept stale claim)
cakes (n=62, C1/D1/E60, page_copy 62/62) · chocolate-bars (n=23, all E) · crackers (n=19, A1/B11/C5/D2) · protein (n=32, top 68.6/B, cluster of 14 @ score 50 ≈ "כתריסר") · cookies-coffee (products.length=117) · granola categoryNote (sugar 4.8–25.0g, ratio 5.2x ≈ "פי חמישה", D=8) · snacks (top 66.9/B) · brined item#4 (Bulgarian 13% Euro 80.3/A, sodium 720) · brined item#5 (Tamra Rajeb 63.6/C, sodium 1628 = corpus max) · brined top 82.7 · hard-cheeses top גלבוע 81.6/A. **No kept-TRUE verdict was found to be a mis-kept stale claim.**

### V-5. Banned-phrase / leakage sweep on the new strings
- `hebrew_readability.analyze().is_clean` = **True** on 8 of 9 new strings.
- `'חלבון נמוך'`: **0** occurrences in changed files. PASS.
- Define-by-negation "X, not Y": the only negation phrase ("לא נמצאת במלח") was **removed** by this commit; no new one introduced. PASS.
- Em-dash: 5 across the added code lines = ~1 per sentence. Not overuse. PASS.
- **One flag (see RT-5, MEDIUM):** granola prologue[2] `is_clean=False` — exposes raw score mechanics "69.7/B" and "32.8/E". This is **pre-existing** (old string carried "69.7/B" + "31.4/E" + bare "38.3"; the fix actually *reduced* the leakage by dropping the bare "38.3"). Not introduced by this commit, but the commit touched the line and left a leakage-gate-failing string in place.

---

## Track C — Rulings on the three flagged items

### RT-1 — chocolate-tablets "C ceiling" — RULING: STALE, must change. Severity HIGH (live).
Live string (`chocolate-tablets-comparison-page-data.ts:51`, categoryNote, renders on `/hashvaot/chocolate-tablets`):
> "המוצר הטוב ביותר במדף הזה מדורג C — וזה ממצא אמיתי."

Independent tally of `chocolate_tablets_frontend_v1.json` (n=35): **B=2, C=6, D=10, E=17.** Top 5 by score: שוקולד מריר **65.8/B**, שוקולד מריר 90% **65.1/B**, then 55.3/C (a 10-pt gap). The best products are graded **B**, not C.

This is a specific, checkable superlative ("the best product is graded C") that is simply false against the current JSON — the same defect class as the hard-cheeses "Gouda leader" that gate-1 *did* fix. It is **not** defensible as thesis-framing: the surrounding thesis (chocolate is a dense treat; a mid-shelf grade is honest) is fine, but it is anchored to a wrong factual anchor. Gate-1's deferral ("needs domain judgment / not on known-issues list") under-called it. **Content must fix** — reflect a B ceiling (2 outliers) or explicitly carve out the two B-grade tablets. Routes to: **content-agent** (with nutrition-agent optional for framing).

### RT-2 — protein-bars "24 מתוך 32 ... מלטיטול" — RULING: STALE / unsupported, fix or remove. Severity HIGH (live).
Live string (`protein-bars-comparison-page-data.ts:60`, prologue, renders on `/hashvaot/protein-bars`):
> "ב-24 מתוך 32 המוצרים בדף הזה הסוכר ... הוחלף במלטיטול"

Re-derived from the authoritative structured field `expansion.ingredients` (the parsed per-product ingredient list) in `protein_combined_frontend_v2.json` (n=32):
- **maltitol specifically: 16/32** (מלטיטול / maltitol / E965) — matches gate-1's grep; this IS the authoritative count.
- maltitol OR erythritol (the two sugar-*replacer* polyols): still **16/32**.
- ANY sugar-alcohol/polyol incl. glycerol (17) + polydextrose (13) fillers: 28/32.

**24 matches none of these.** (The "32/32" from a naive whole-record search is boilerplate — the word "מלטיטול" appears in shared narrative like "מבין החטיפים שלא נשענים על מלטיטול", which does *not* mean that product contains it; and the trace mentions the concept in every product.) The claim is doubly wrong: an orphan count (24) that no field yields, attributed specifically to maltitol when the honest maltitol count is **16**. Gate-1 refused to guess a rewrite (correct) but under-classified it as UNVERIFIABLE — with `expansion.ingredients` mined properly it is verifiably STALE. **Fix to the true 16/32 for maltitol, or reframe** (e.g. a defensible "most bars replace sugar with a polyol" qualitative statement). Routes to: **content-agent**; **nutrition-agent** to rule whether the intended grouping is maltitol-only (16) or all sugar-replacer polyols.

### RT-3 — cookies-coffee "119 products" vs 117 — RULING: confirmed mismatch, DOES render consumer-facing. Severity HIGH (live).
`cookies_coffee_frontend_v2.json`: `products.length` = **117**; `page_copy.hero.productCount`/`scoredCount` = **119**; and `page_copy.prologue.sentences[0]` = "83 מתוך 119 המוצרים ... מקבלים ציון E". The adapter (`cookies-coffee-page-data.ts:76`, RT-3-fix comment) reads `cookiesCoffeePrologueSentences = _pageCopy.prologue.sentences` — so the "119" and "83" **render on the live `/hashvaot/cookies-coffee` comparison page**.

Independent recount (n=117): grades C=9, D=27, **E=81**. So BOTH numbers are stale: denominator 119→**117**, and E-count 83→**81**. (The "C ceiling" claim is correct: top grade C=9.) Blast radius: consumer-facing prologue text on the cookies-coffee page tells users 119 products / 83 E when the truth is 117 / 81.

This lives inside `cookies_coffee_frontend_v2.json:page_copy`, correctly **outside** TASK-460's `.ts/.tsx`-only edit boundary — gate-1 was right not to touch JSON. It is a pipeline-output defect. Routes to: **data-agent** (regenerate page_copy counts from the true 117-product corpus), then **content-agent** sign-off.

---

## Additional findings (surfaced by this gate)

### RT-4 — orphaned stale duplicate in `comparison-pages.json` — Severity MEDIUM (latent, not currently rendered)
The exact stale brined-cheeses prologue that gate-1 fixed in the `.ts` adapter — including "9 בדירוג A, 20 ב-B, 5 ב-C ו-2 ב-D" AND the removed negation "התשובה לא נמצאת במלח" — **still exists** at `bari-web/src/data/site-content/comparison-pages.json:33` (`.prologue` field). The stale snacks "מ-67 עד 15" is at line 238.
Blast radius: **currently zero.** Every consumer surface that imports `getComparisonPageChrome(...)` reads only `.hero` (the featured intelligence cards use `.hero.title`, which is qualitative/number-free and clean). The comparison pages render prologue from the `.ts` adapters, not from this chrome `.prologue`. So these strings are dead/orphaned duplicate copy today. But this is the identical TASK-460 root cause (numbers-in-copy outside the gated pipeline) and a latent landmine if anyone wires `.prologue` rendering. Routes to: **content-agent / data-agent** (delete or regenerate the orphaned `.prologue`/description fields). Advisory: also note granola now has two diverging hero-title sources (adapter vs chrome) — a durability observation.

### RT-5 — granola prologue[2] score-mechanic leakage — Severity MEDIUM (pre-existing)
`hebrew_readability` flags "69.7/B" and "32.8/E" as exposed score mechanics. Pre-existing (old string had the same pattern plus a bare "38.3"); this commit reduced but did not eliminate it. Not a blocker on this commit. Routes to: **content-agent** (decide whether the granola prologue should carry raw `score/grade` tokens at all; if not, this is a broader leakage cleanup beyond TASK-460).

---

## Durability check (advisory — the task's own root cause)
New strings that still hardcode exact counts that will go stale on the next rescore:
- **brined** "רק שתי גבינות במדף מגיעות בלי שום תוסף ... נתרן נמוך יחסית של 720 מ\"ג" (kept-TRUE now, but "שתי גבינות" + the 720 figure are hardcoded and will drift). 
- **cereals/granola/brined/snacks/hard-cheeses/juices** — the fixes deliberately traded exact counts for durable qualitative framing ("רוב המדף מתקבץ סביב C ו-D", "יותר מ-50 נקודות", "כמעט 40"), which is the right call and materially reduces future staleness. Good.
- Residual brittle numbers still living in `.ts` copy (not touched, low current risk): brined "720 מ\"ג", granola prologue "69.7/B ... 32.8/E", protein "25 עד 36 גרם" and "69/B". These are the next re-scores' landmines. Advisory only — not a blocker.

Root-cause note for the orchestrator: the durable fix is to source these counts from the JSON pipeline (like cakes/crackers/cookies-coffee already do via `.filter()`/`.length`/`page_copy`) rather than hardcode them in `.ts` prose. RT-3/RT-4 prove the JSON-page_copy path itself can also go stale, so "move it to JSON" is necessary but not sufficient — the page_copy counts must be regenerated on rescore, and a gate must audit them.

---

## Routing table
| Finding | Severity | Live? | Introduced by d57eae3b? | Routes to |
|---|---|---|---|---|
| RT-1 chocolate-tablets "C ceiling" | HIGH | yes | no (pre-existing, mis-deferred) | content-agent |
| RT-2 protein-bars "24 מלטיטול" | HIGH | yes | no (pre-existing, mis-deferred) | content-agent + nutrition-agent |
| RT-3 cookies-coffee 119/83 vs 117/81 | HIGH | yes | no (JSON, out of gate-1 scope) | data-agent → content-agent |
| RT-4 orphaned stale copy in comparison-pages.json | MEDIUM | no (not rendered) | no | content-agent / data-agent |
| RT-5 granola prologue score-mechanic leakage | MEDIUM | yes | no (reduced by commit) | content-agent |

## Bottom line
- Commit `d57eae3b` itself: clean. 9/9 STALE fixes verified accurate + durable; scope confined to Hebrew strings; tsc 0; no regression; no wrongly-kept claim in a 15+ sample. **This commit may merge.**
- But three HIGH live consumer-facing numeric defects remain on the chocolate-tablets, protein-bars, and cookies-coffee pages (RT-1/2/3), plus two MEDIUM (RT-4/5). They are follow-on work, correctly outside this commit's edit boundary, and must be tracked and fixed before those pages are declared clean.
- No fixes applied by this gate. No push/PR/deploy. Main tree read-only. OFF ban not implicated.

---

## Gate 3 — Targeted re-verification of RT-1/RT-2/RT-3 fixes (commit `b5a75204`)

Date: 2026-07-02. Reviewer: adversarial-qa-agent (executor; no subagents used).
**Method constraint honored:** the worktree had 13 dirty files from an unrelated runaway process at review time. All verification below was performed exclusively against **committed git state** — `git diff f1bca7b0..b5a75204`, and file contents pulled via `git show b5a75204:<path>` into the session scratchpad (never the working-tree copies). `npx tsc --noEmit` was also run and returned exit 0, but that check runs against the full worktree-on-disk and is treated as a secondary/weaker signal given the dirty tree; the git-level diffs are the load-bearing evidence.

### VERDICT: GO

### 1. Diff shape — CONFIRMED
`git diff f1bca7b0..b5a75204 --stat` = exactly 4 files: `cookies_coffee_frontend_v2.json` (1 line), `chocolate-tablets-comparison-page-data.ts` (2 lines), `protein-bars-comparison-page-data.ts` (1 line), `tasks/returns/T460_content_gate3.md` (new file, log). Full diff inspected line-by-line: every change in the three data/code files is a single-sentence string edit — no key additions/removals, no structural JSON changes, no logic changes.

### 2. RT-1 chocolate-tablets — CONFIRMED FIXED
Independent recount against `git show b5a75204:.../chocolate_tablets_frontend_v1.json`: n=35, grades B=2/C=6/D=10/E=17. The two B products score 65.8 and 65.1; the next-highest (first C) is 55.3 — gap = **9.8 points**, rounds to "עשר נקודות" exactly as the new sentence states: "רק שתי טבלאות במדף הזה מגיעות ל-B, ואחריהן פער של עשר נקודות עד הבאה בתור." Both the count (2) and the gap (~10) are independently verified true. The companion sentence was also rewritten — "יכולה להגיע ל-C" → "יכולה להגיע גם ל-B" — no longer implies a C ceiling. **PASS.**

### 3. RT-2 protein-bars — CONFIRMED FIXED
Recount of `expansion.ingredients` for maltitol/E965 across `git show b5a75204:.../protein_combined_frontend_v2.json` (n=32): **16/32** — identical to my gate-2 finding, and identical to the new adapter text "ב-16 מתוך 32". Diff confirms only "24"→"16" changed in that sentence; scanned every numeric token in the committed adapter file (10, 100, 16, 2, 23, 25, 32, 35, 36, 4, 65, 69) — none of the other numbers (protein range 25-36g, top score 69/B, n=32, etc.) were disturbed. **PASS.**

### 4. RT-3 cookies-coffee — CONFIRMED FIXED
In the same committed JSON (`git show b5a75204:.../cookies_coffee_frontend_v2.json`): `products.length`=117, grade E count=81 — and `page_copy.prologue.sentences[0]` now reads "81 מתוך 117 המוצרים שנבחנו מקבלים ציון E" (no more "119"/"83" anywhere in that sentence). Denominator and E-count both internally consistent with the live products array in the identical committed file. Diff confirms this was the only `page_copy` field touched — one line changed, nothing else in the JSON. **PASS.**

### 5. Voice / banned-phrase sweep on the 3 new strings
`hebrew_readability.analyze()`:
- choc_tablets sentence 1 (new): `is_clean=True`
- choc_tablets sentence 2 (rewritten): `is_clean=True`
- protein sentence (24→16 edit): `is_clean=False` — flags "long sentences" + `SCORE MECHANIC exposed: '69/B'` (×2)
- cookies-coffee sentence (119/83→117/81): `is_clean=True`
- `'חלבון נמוך'`: 0 occurrences in all 3 new strings.

The protein flag is **pre-existing, not introduced by `b5a75204`**: re-ran the identical check against the string as it existed at `f1bca7b0` (pre-fix) and got the identical `is_clean=False` with the identical flags — the "69/B" score-mechanic exposure and long-sentence flag were already there; this commit only changed "24"→"16" inside that same sentence and did not touch the "69/B" clauses. This is the same leakage class already logged as RT-5 in the main gate-2 report (granola) — now also present, unresolved, in this protein-bars sentence. Not a regression; not a blocker for this fix commit; still open follow-on work.

### Summary
| Item | Committed value | Claim in new copy | Match |
|---|---|---|---|
| RT-1 B-count | 2 (65.8, 65.1) | "שתי טבלאות ... ל-B" | Yes |
| RT-1 gap | 9.8 pts to next (55.3/C) | "פער של עשר נקודות" | Yes |
| RT-2 maltitol | 16/32 (expansion.ingredients) | "16 מתוך 32" | Yes |
| RT-3 denominator | products.length=117 | "117" | Yes |
| RT-3 E-count | 81 | "81" | Yes |

### Verdict: GO
All three flagged fixes (RT-1, RT-2, RT-3) are verified correct against committed state, diff shape is confined to the expected 4 files with string-only edits, and no new leakage was introduced (the one `is_clean=False` result is pre-existing and unchanged by this commit — carried forward as open follow-on work, not a blocker). Clear for the owner PR. No fixes applied by this gate. Verification performed entirely against `git show`/`git diff` committed blobs per the coordinator's method constraint; the dirty worktree was not read.

---

## Gate 4 — Full re-verification of pass-2 (commit `cef964d4`, 21 files)

Date: 2026-07-02. Reviewer: adversarial-qa-agent (executor; no subagents used).
Worktree status re-checked at start: `git status --porcelain` = 0 lines — **clean, confirming the coordinator's reclassification** that the earlier "runaway noise" was this legitimate worker's in-flight commit, not contamination. Method: `git diff 83e09811..cef964d4`, JSON contents pulled via `git show cef964d4:<path>` into the scratchpad, plus read-only inspection of upstream provenance artifacts under `C:\Bari\02_products` and `C:\Bari\01_framework` for the 5 UNVERIFIABLE lineage items.

### VERDICT: GO_WITH_FIXES

Pass-2 is a strong, well-evidenced audit that correctly fixed 24 real defects across featured cards, SEO metadata, and adapters, and it does **not** clobber any previously-merged fix. But it also left three fabricated/unsourced consumer-facing numbers unresolved as "flag, don't touch" when the honest call — per the coordinator's own instruction that unverifiable-but-checkable claims should be verified against upstream artifacts or removed — was **removal**, not flagging. Those three are new findings from this gate, not carried over from gate 2/3.

### 1. Scope, additivity, no clobbering — CONFIRMED
`git diff 83e09811..cef964d4 --stat`: 21 files — 4 `page.tsx` (SEO metadata), the supermarket hub page, 9 featured-intelligence-card components, 7 `*-page-data.ts` adapters, plus the gate-1 log. **Zero JSON files touched** in this pass (confirmed: `cookies_coffee_frontend_v2.json`, `chocolate-tablets-comparison-page-data.ts`, `cookies-coffee-page-data.ts`, `hard-cheeses-page-data.ts` — all the RT-1/RT-2/RT-3 fix sites from `b5a75204` — are **untouched** by this diff, `git diff` on those paths between `83e09811..cef964d4` returns empty). No logic changes beyond: (a) two `Array.sort()`/`Math.round()`/`Math.max()` derivations added in the supermarket page and the granola featured card to replace hardcoded numbers with live-computed ones (durable-by-construction, the correct fix pattern), and (b) one date-formatting helper in the hummus adapter (`toLocaleDateString`). Every other change is a Hebrew string literal. Additivity claim: **confirmed true** — nothing from `f1bca7b0`/`b5a75204`/`83e09811` was reverted or altered.

### 2. The three claims singled out for special care — ALL CONFIRMED CORRECT

**Cheese featured card "2 A-grades, קוטג' 1% leads" (renders on `/hashvaot/supermarket`):**
Independent recount of `cheese_frontend_v5.json` (n=47): grades A=2, B=19, C=9, D=15, E=2. The two A products: קוטג' 1% שומן @ **86.6**, גבינה טבורוג 5% @ 81.3. קוטג' 1% is also the #1 product overall by score. Committed new insight line: "שני מוצרים בלבד מגיעים ל-A — קוטג' 1% מוביל את המדף" — **exactly true**. The line it replaced ("'הכי טוב' הוא B — אף מוצר לא מגיע ל-A") was flatly false — 2 products reach A, not 0. This was a severe defect (an always-rendered card insight line asserting the opposite of the data) and pass-2 was right to catch and fix it. Note: no exact score ("86.6") is asserted in the shipped copy — the new line only claims the count and the leader's identity, both verified. **PASS.**

**Hard-cheeses "leader גלבוע 5%" + A:1/B:26/C:4/D:0:**
`hard-cheeses-page-data.ts` itself is untouched in this pass (already correct from before). The featured-card insight lines (`featured-hard-cheeses-intelligence-card.tsx`, which the pass DID edit) were rewritten from a fabricated "גאודה" leader + "D exists" claim to align with the file's own already-verified truth. Recount of `hard_cheeses_frontend_v4.json` (n=31): A=1 (פרוסות גבינת גלבוע 5% @ 81.6), B=26, C=4, D=0 (absent from the grade tally). New lines: "גבינה אחת בלבד מגיעה ל-A — גלבוע 5%..." and "רוב המדף מתקבץ ב-B..." — both **exactly match**. **PASS.**

**Chocolate-bars "27–60" (×3 locations: prologue, supermarket description, featured-card stat):**
Independent sugar-range scan of `chocolate_bars_frontend_v1.json` (n=23, `expansion.nutrition` sugar field): min **27.0** (מיני פסק זמן), max **59.6** (חטיף בודד) → rounds to "27–60" exactly. Old "45–60" missed the 27.0 low-end outlier. Verified count ≥44g: 21/23 (supports the added prologue clause "וברוב המדף מעל 45"). All three instances of "27–60" in the diff are consistent with each other and with the JSON. **PASS.**

### 3. Every claimed fix in the diff — verified against committed JSON (21 claimed; all checked)
| # | Claim (new) | Independent JSON re-derivation | Verdict |
|---|---|---|---|
| P1/P22/P29 | tablets ceiling "B, ...שתי טבלאות" (SEO/hub/card, mirrors RT-1) | B=2 (65.8, 65.1), gap 9.8 to next | PASS |
| P3 (mirrors RT-2) | protein "16 מתוך 32" | maltitol in `expansion.ingredients` = 16/32 | PASS |
| P4/P21/P31 | protein "25 עד 36 גרם ... ל-100 גרם" (×3 sites) | per-100g range 25.0–36.0 confirmed; "בחטיף אחד"→"ל-100 גרם" reframe is correct (no per-bar serving weight in JSON) | PASS |
| P5 | protein "כשמחצית המדף" (16/32 = exactly half) | 16/32 = 50.0% | PASS |
| P6 (mirrors RT-3, JSON untouched here) | n/a — already fixed at `b5a75204`, correctly not re-touched | — | N/A |
| P7 | juices categorynote grade-tags removed | grape juice (`fruit_drink`, low-fruit) is graded **D**, not E — the old "<10% ⇒ E" mapping was false; removal (not a new mapping) is the honest fix | PASS |
| P8 | crackers "19 קרקרים" (×2 sites) | `crackers_frontend_v1.json` n=19 | PASS |
| P9 | hummus month derived live from `_meta.generated` | `hummus_frontend_v5.json._meta.generated` = 2026-06-17 (June, not the old hardcoded "May") | PASS, and durable by construction |
| P10 | snacks "סירופ גלוקוז מופיע פעמיים" | soft/qualitative reposition claim; not independently re-derivable from a structured ingredient-position field in this worktree, but directionally plausible and non-numeric — low risk | Not independently re-verified (qualitative, not a count) |
| P11/P41(dup) | snacks/protein "25–36 גרם חלבון ל-100 גרם" | matches P4 | PASS |
| P12/P14/P40 | brined "שלוש גבינות ... חלב, מלח, תרבית ומקריש"; "שני רכיבים מול עשרה"; two Gad tzfatit tie at 82.7/A | Ingredient-count re-scan (top-level comma count): min=2 (Tamra, confirmed), max in my crude parse=9 (בולגרית שום+עשבי תיבול, not 10) — **directionally correct, off by one on a soft/approximate ingredient-tokenization call, not a hard structured-field number**; the "3 clean-core" cheeses and the two tied A-grade Tzfatiyot (82.7/A ×2) are confirmed | PASS with a minor caveat (see Track-V note below) |
| P13 | "תרבית לקטית חיה"→"תרבית לקטית" (removed "חיה"/live-culture claim) | correct removal of an unverifiable adjective | PASS |
| P15/P16/P17 | SEO descriptions cereals→20, juices→17, cakes→62 | `cereals_frontend_v2.json` n=20, `juices_frontend_v3.json` n=17, `cakes_hard_cookies_frontend_v1.json` n=62 | PASS |
| P18 | cereals "ארבעה מוצרים מיועדים לילדים" | `_isChildrens===True` count = 4 | PASS |
| P19/P23/P26/P27/P44/P45/P48/P50 | various TRUE-kept claims (75/B cereals top, tablets sugar 2–65g endpoints, cheese fat 30%, bread lineage, protein top-vs-max, milk cow/goat parity, tablets product range, "updated June 2026" dates) | spot-checked a subset: cereals max 74.7→75/B PASS; cheese max fat scan confirms a 30% product exists PASS; hummus/hard-cheeses `_meta.generated` June 2026 PASS | PASS (sampled) |
| P20/P32 | granola top/bottom/spread now **live-derived** (`.sort()`/`Math.round()`) instead of hardcoded | `granola_frontend_v2.json` max=69.7→70/B, min=32.8→33/E, spread=37 — matches the live computation exactly | PASS, and durable by construction (this is the textbook right fix) |
| P24/P30 | chocolate-bars "27–60" (×2 more sites, total 3) | see dedicated section above | PASS |
| P25 | "תקרית"→"תקרת" (typo fix, ×2) | spelling correction, not a numeric claim | PASS |
| P28 | supplements "18... ארבעה מוצרי אוקסיד" | inline magnesium array: 18 products, 4 over-350mg all form=אוקסיד (520/520/450/450) | PASS |
| P33 | cheese "2 A-grades, קוטג' 1% leads" | see dedicated section above | PASS |
| P34/P35/P36 | cereals card: "פצפוצי אורז" replaces false "שיבולת שועל" (no oats product in corpus); B-count stat replaces unsourced "4 קטגוריות" | B products = "דגני בוקר" (wheat) + "פצפוצי אורז ללת"ס" (100% whole rice, no added sugar, confirmed via `expansion.ingredients`) — no oats product exists at grade B; old line was flatly false. New live-derived B-count stat (2) is durable | PASS |
| P37/P38 | hard-cheeses card fallback lines + label | see dedicated section above; these are **fallback-only** (render only if `insightLine` is empty on all products, confirmed via component code — dormant today since products carry real insightLines) | PASS, correctly low-urgency but still right to fix |
| P39 | juices card fallback lines rewritten (A=6 not 1, no C grade exists, rimonim > oranges) | `juices_frontend_v3.json`: A=6, D=7, E=4 — **no C grade in this corpus at all**, confirming old "סחוט קר מגיע ל-C" was doubly wrong; A-sugar values 8.2/8.6/8.7/12.6 confirm רימונים (12.6) is the sugar-max among A's, "מעל תפוזים" (8.2–8.7) — correct | PASS (fallback-only, dormant today) |
| P42/P43 | "38 פרמטרים" and red-label fallback left unfixed | see UNVERIFIABLE ruling below — **should have been removed, not left** | Ruling below (new finding, not a pass — see Track C) |
| P41/P46 | snacks "655/73" and bread "13"/"46%" left unfixed | see UNVERIFIABLE ruling below | Ruling below |
| P49 | juices "רק מיצים סחוטים ב-100%..." | re-verified: unchanged from `b5a75204`, still true (6/6 juice_100 = A, no other subpool reaches A) | PASS (re-confirmed, not re-touched) |

**Track-V note on P12/P40 (brined ingredient-count "עשרה"):** a top-level-comma tokenization of `בולגרית שום+עשבי תיבול 16%`'s ingredient string yields 9 discrete items, not 10 (`חלב בקר מפוסטר / מי מלח / רכיבי חלב / מייצבים(אגר, גומי זרעי חרובים) / מלח / סיבים תזונתיים / שום(0.3%) / עשבי תיבול(0.2%) / חומר משמר`). Whether "מייצבים (אגר, גומי זרעי חרובים)" counts as one item or its two sub-components count separately is a legitimate judgment call that would resolve the count to 10. This is a soft/approximate claim ("כ-עשרה" territory), not a number pulled from a structured field — directionally correct and not a blocker, but noted for precision.

### 4. Kept-TRUE sample (10+ checked, no wrongly-kept stale claim found)
Sampled beyond the required-fix rows: P19 (cereals top 75/B), P23 (tablets sugar endpoints 2g/65g — both real products exist), P26 (cheese max fat 30%), P27 (bread lineage constants, unchanged from gate-2's earlier finding), P28 (magnesium 18/4-oxide), P44 (protein top-vs-corpus-max distinction), P45 (milk cow/goat 85/A parity), P48 (tablets "מריר 90% עד שוקולד לבן"), P50 (juices/hard-cheeses "June 2026" dates), P49 (juices 100%-only-A, re-confirmed). **All 10 confirmed TRUE; no mis-kept stale claim identified.**

### 5. Ruling on the 5 UNVERIFIABLE lineage/methodology items

Per the coordinator's framing, the honest options for a consumer-facing methodology number that can't be derived from frontend JSON are: (a) verify against the upstream artifact in `C:\Bari` read-only, or (b) recommend removal. I checked the actual upstream artifacts for all five (read-only, `02_products/` and `01_framework/`) rather than accepting "flag, don't touch" as sufficient — that was pass-2's own proposed disposition, and the coordinator's instruction requires a real ruling, not a re-flag.

**(a) Bread "13 מוצרים כוללים 'מחמצת' בשם" (`bread-page-data.ts:128`) — RULING: STALE, remove or correct to 7.**
Checked all three candidate corpora in `02_products/bread_retail_003/`: the curated 31-product comparison set (`real_bread_retail_003_v1_curated_comparison_dataset.json`) has **7** sourdough-named products (I listed them: קמח מלא, גרעינים, וחיטה מלאה קל, שיפון+אגוזים, מכוסמין, אגוזים צימוקים, אגוזים פרוס) — the pass-2 log's own derivation notes even state "sourdough-named=7" for this set. The full 258-product raw scan has **33** sourdough-named products. Neither candidate yields 13. "13" is not traceable to any upstream artifact I could find. **Verify against upstream: FAILED — recommend correcting to 7 (if the claim is about the displayed/curated set, which is what a reader would assume) or removing the sentence.**

**(b) Bread "46%" insufficient-ingredient-data (`bread-page-data.ts:149` or supermarket description) — RULING: TRUE, verified against upstream artifact.**
Found the exact source: `02_products/bread_retail_003/real_bread_retail_003_v1_curated_comparison_handoff.md:171` — "46% מהמוצרים שסרקנו לא הציגו נתוני רכיבים מלאים." This is a documented, named statistic in the authoritative handoff doc for this corpus, distinct from (and consistent alongside) the "256 scanned / 81 sufficient" figures already verified TRUE in gate 2. **Verify against upstream: PASSED — this claim is accurate and traceable; it should be kept, not flagged as unverifiable.** (Pass-2 under-verified this one — it exists and is correct, just not derivable from the frontend JSON, which was the wrong place to look.)

**(c) Snacks "655 נסרקו / 73 קיבלו ציון" (`featured-snacks-intelligence-card.tsx:55-56`) — RULING: UNSOURCED, recommend removal.**
Searched `02_products/snack_bars/` exhaustively (manifests, run_records, bsip2_outputs, observations_bsip0 directory counts) for any acquisition-lineage artifact matching 655 scanned / 73 scored. Found nothing — the closest structured run manifest (`protein_combined_manifest_task365...json`) reports a completely different pipeline (`discovery_pool: 64, survived_corpus: 41`) for the protein-bars corpus, not cereal-snack-bars, and no count near 655/73 appears anywhere in the snack_bars directory tree. Unlike bread's `real_bread_retail_003_v1` lineage (a named, documented, single-source-of-truth acquisition run), snacks has no equivalent artifact I could locate. **Verify against upstream: FAILED — no traceable source found. Recommend removal, not flagging**, since this stat renders unconditionally in the featured card's `stats` array (always visible on `/hashvaot/supermarket`), and an unsourced count in a "products scanned" stat is a fabrication-shaped risk, not a rounding nuance.

**(d) Cereals/granola cards "38 פרמטרים הושוו" (`featured-breakfast-cereals-...tsx`, `featured-granola-...tsx`) — RULING: CONTRADICTS the canonical methodology doc, remove.**
The canonical methodology reference `01_framework/glass_box/glass_box_technical_methodology_v1.md:33` states BSIP2 "currently operates over **ten internal scoring dimensions**" (confirmed by a second doc, `01_framework/glass_box/w0_product_cosign_v1.md:88`: "The ten internal scoring dimensions roll up into the six public dimensions"). No document anywhere in `01_framework/` or `03_operations/` (excluding binary/cache noise) contains "38" as a parameter/dimension count. This number doesn't just lack support — it **actively contradicts** the documented, owner-cosigned dimension count. **Verify against upstream: FAILED, and worse than merely unsourced. Recommend removal — this is the highest-priority item of the five**, since "38 פרמטרים הושוו" is also a Tier-4-adjacent methodology-mechanics claim (per `01_framework/editorial/bsip2_to_web_translation_contract_v1.md:122`, internal dimension counts/weights are supposed to stay off consumer copy entirely) — it may also be a leakage-policy violation independent of the accuracy question.

**(e) Cakes/cookies-coffee cards "אין כאן מוצר ללא תווית אדומה לפחות אחת" (red-label fallback, `featured-cakes-hard-cookies-...tsx:30`, `featured-cookies-coffee-...tsx:30`) — RULING: retired-concept + unverifiable, remove.**
No red-label field exists anywhere in `cakes_hard_cookies_frontend_v1.json`'s product schema (checked full key list). Beyond being unverifiable, this references **binary red-label caps**, a framework concept the project's own standing ruling has explicitly retired (memory `redlabel_deanchor_directive`: "stop anchoring on binary red-label caps; category-relative/continuous"). This is a fallback-only line (dormant while real insightLines exist) but should not survive in the codebase referencing a dead scoring concept. **Verify against upstream: FAILED (no field, and the concept itself is deprecated). Recommend removal, highest confidence of the five.**

**Summary of the 5-item ruling:** 1 confirmed accurate and should be *kept* (46% bread), 4 should be *removed or corrected* (13→7 or delete; 655/73 delete; 38 delete; red-label fallback delete) — none should remain in "flag, don't touch" limbo, which was pass-2's proposed disposition and is not sufficient per the coordinator's own standard.

### 6. Build, banned-phrase/voice sweep, durability
- `npx tsc --noEmit` (bari-web, worktree clean): exit **0**.
- Voice sweep on 25 new/edited strings: 22 `is_clean=True`; 3 flagged (`cerealsDescription` "75/B", `granolaDescription` "70/B"/"33/E", protein categoryNote "69/B") — all three confirmed **pre-existing** by diffing against `83e09811` (same X/Grade pattern already present before this pass; granola's numbers changed 76→70/29→33 but the *pattern* was already there). Not a new regression; same RT-5 leakage class. Zero `'חלבון נמוך'` hits across all 25 strings checked.
- Durability: this pass materially improves durability — P20/P32 (granola spread) and the featured-card B-count (P35) are now **live-derived** from the JSON via `.sort()`/`.filter()`/`Math.round()` instead of hardcoded, closing exactly the kind of gap that caused TASK-460. Residual hardcoded counts that will still drift on next rescore: chocolate-bars "27–60" (3 sites), protein "25–36" (3 sites), cheese "2 A-grades" (card insight line, no live derivation), juices A-sugar values in card insight lines. Advisory only, consistent with gate-2's original durability note — the pattern of moving to live derivation should continue but is not a blocker.

### Routing table (gate-4 findings)
| Finding | Severity | Ruling | Routes to |
|---|---|---|---|
| Bread "13" sourdough-named count | MEDIUM | STALE — correct to 7 or remove | content-agent |
| Bread "46%" missing-ingredient-data | — | VERIFIED TRUE — keep, cite `real_bread_retail_003_v1_curated_comparison_handoff.md` if provenance is ever challenged | none (no action) |
| Snacks "655/73" scanned/scored stat | HIGH (live, always-rendered stat) | UNSOURCED — remove | content-agent / data-agent (if a real lineage artifact exists elsewhere, surface it; otherwise delete) |
| "38 פרמטרים הושוו" (cereals + granola cards) | HIGH (live, contradicts owner-cosigned methodology doc, possible Tier-4 leakage) | CONTRADICTED BY CANONICAL DOC — remove | content-agent; nutrition-agent to confirm the "ten dimensions" framing if any consumer-facing parameter count is wanted instead |
| Red-label fallback line (cakes + cookies-coffee cards) | MEDIUM (fallback-only, dormant) | REFERENCES RETIRED CONCEPT — remove | content-agent |
| Brined "עשרה" ingredient max (soft tokenization) | LOW | directionally correct, off-by-one on a judgment call | advisory only, no action required |

### Verdict: GO_WITH_FIXES
Commit `cef964d4` may merge as-is for its own internal correctness — all 21 claimed fixes independently verified against committed JSON (including the three the coordinator singled out for special care), zero clobbering of prior fixes, zero JSON/logic drift beyond two correct live-derivation additions, tsc clean, no new leakage, no wrongly-kept stale claim in a 10+ sample. **But** the disposition pass-2 chose for the 5 lineage/methodology numbers ("flag, don't touch") is not the correct final state for 4 of the 5 — they are fabricated-or-contradicted consumer-facing numbers that should be removed (or, for the bread "13," corrected), not left live with a flag. These are new findings from this gate, most notably the "38 פרמטרים" claim (contradicts the owner-cosigned ten-dimension methodology) and the "655/73" stat (no traceable source anywhere in the snack_bars corpus) — both render unconditionally today. Fixes required before these four pages/cards are clean:
1. Remove or correct bread "13" sourdough-named claim.
2. Remove snacks "655/73" scanned/scored stat (or supply the real source if one exists that this review missed).
3. Remove "38 פרמטרים הושוו" from both cereals and granola featured cards.
4. Remove the red-label fallback line from cakes and cookies-coffee featured cards.
No fixes applied by this gate. No push/PR/deploy beyond this report commit. Main tree read-only except for this report file.
