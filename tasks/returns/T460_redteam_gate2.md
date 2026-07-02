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
