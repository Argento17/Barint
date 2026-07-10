# Red-Team Challenge Report — TASK-503 creatine hub card (worktree `C:\bari_wt_t503`, commit `6b936782`)
Date: 2026-07-04   Scope: creatine featured card + supplements hub wiring + sitemap entry, `/hashvaot/supplements`   Challenger: adversarial-qa-agent

## Opening Finding — CRITICAL

**The two-gate content sign-off is incomplete.** `bari-web/src/app/hashvaot/supplements/page.tsx:27-32` labels `CREATINE_DESCRIPTION` itself: "DRAFT card description — pending Content Agent + Adversarial QA two-gate sign-off (same standing rule as every consumer-facing string)." This review supplies the Adversarial QA half. A repo-wide search (`grep -rn "TASK-503" C:\Bari`) returns only `tasks/TASK-503.md` and `tasks/DISPATCH_BOARD.md` — no Content Agent artifact exists anywhere for this blurb (unlike TASK-492C, which has `creatine_comparison_content_package_v2.md`, `creatine_comparison_redteam_v1.md`, etc. for the destination page itself). Per `C:\Bari\CLAUDE.md` ("Content sign-off HARD RULE") and memory `content_signoff_hard_rule`: nothing consumer-facing reaches the owner without BOTH sign-offs, no exceptions, forever. This is a process gate, not a copy-quality judgment — the copy itself checks out (see below), but that does not substitute for the missing Content Agent review. This alone blocks go-live under Hard Rule 10 regardless of how the rest of the review reads.

## Track V — Verification

| Check | Result | Observed value |
|---|---|---|
| `npx tsc --noEmit` | PASS | exit 0, no output |
| `npm run build` | PASS | exit 0; Turbopack compiled successfully; `/hashvaot/creatine` and `/hashvaot/supplements` both listed in route table (dynamic ƒ and static ○ respectively) |
| `npm run lint` | PASS | 0 errors, 18 warnings — all 18 warnings are in files outside this diff (pre-existing); none in `featured-creatine-intelligence-card.tsx`, `supplements/page.tsx`, or `sitemap-paths.ts` |
| No grade/score chip on card | PASS | `ComparisonIntelligenceHero` (the shared, frozen component both magnesium and creatine cards render through) has no grade-chip rendering path at all — it only renders `stats: {value, label}` pairs and a title/description string. Confirmed visually on `C:\Bari\tasks\returns\TASK-503_screenshots\supplements-mobile-375.png`: the creatine card shows "31 מוצרים נותחו · 10 מהמדף הישראלי במינון הוגן · 4 בלי מינון מפורט על האריזה · 7 אומתו מול מאגר תקנים" — no A–E letter, no numeric score anywhere |
| Design conformance vs frozen magnesium card | PASS with 1 finding (see H-2) | Same hero shell, badge, stat-row, and CTA styling as `featured-magnesium-intelligence-card.tsx`; only the `theme.accent` hex and the omission of `theme.photo` differ — no novel layout introduced |
| Link + sitemap | PASS | Card `href="/hashvaot/creatine"` (`supplements/page.tsx:64`); `/hashvaot/creatine` present in `ALL_INDEXABLE_PATHS` at `sitemap-paths.ts:15`, correctly alphabetically placed between `crackers` and `granola` |
| Score-propagation audit (card stats vs `creatine-page-data.ts`) | PASS numerically, FLAGGED for method (see H-1) | `creatineProducts.length` = 18+13 = 31 ✓; `honestDoseCount` (Israeli-only) = 10 ✓ (counted 10 `doseHonesty:"honest"` rows in `creatineIsraeliProductsRaw`); `undisclosedCount` = 4 ✓ (4 rows, all Israeli); `directoryVerifiedCount` = 7 ✓ (7 rows, all worldwide — Thorne, Momentous, Klean Athlete, BPN, MegaFood, Sports Research, BioSteel) |

## Track C — Copy Honesty Audit (`CREATINE_DESCRIPTION`, `supplements/page.tsx:33-34`)

| Claim in blurb | Verified against | Result |
|---|---|---|
| "18 תוספי קריאטין מהמדף הישראלי" / "13 מותגי ייחוס עולמיים" | `creatineIsraeliProducts.length`=18, `creatineWorldwideProducts.length`=13 | MATCH |
| "עשרה מוצרים ישראליים מצהירים על מינון הוגן בטווח שנחקר" | 10 `doseHonesty:"honest"` rows, Israeli only | MATCH — wording is verbatim-consistent with `creatinePrologueSentences[1]` |
| "ארבעה נושאים את המילה קריאטין על האריזה בלי לפרט כמה גרם יש במנה" | 4 `doseHonesty:"undisclosed"` rows (Super Effect ×2, Sport GS, MyProtein tablets), all Israeli | MATCH — near-verbatim to `creatinePrologueSentences[2]` |
| "שבע מנות ייחוס עולמיות אומתו ישירות מול מאגר NSF" | 7 `certTier:"directory_verified"` rows, all worldwide; this is the exact count that TASK-492C's RT-1 fix reconciled to (file header comment lines 19-26 of `creatine-page-data.ts`) | MATCH |
| "מוצרי המדף הישראלי מסתמכים כרגע על הצהרת היצרן בלבד" | 0/18 Israeli rows carry `certTier:"directory_verified"`; file comment confirms "0 Israeli products are directory-confirmed" | MATCH |
| "בלי ציון מספרי או דירוג אותיות" | `score: null, grade: null` on all 31 products | MATCH |
| Dose-honesty framing (undisclosed = can't verify, not "bad") | Blurb states the fact neutrally, no value judgment language ("bad"/"ineffective"/"פסול") | HONEST |
| OFF-ban | No OFF references anywhere in `creatine-page-data.ts` or the card | CLEAN |
| Antithesis guard (`,לא` / `ולא` / `אלא` / `ואילו` / `ה-[A-E]`) | Grepped `CREATINE_DESCRIPTION` — zero matches | CLEAN |
| Em-dash guard (new creatine copy only) | Grepped `—` in `page.tsx` — only hits are the pre-existing `MAGNESIUM_DESCRIPTION` (line 25) and the pre-existing intro paragraph (line 52), both out of scope per the delegation. Zero em-dashes inside `CREATINE_DESCRIPTION` | CLEAN |
| NOVA/BSIP/cap/floor/pillar/routing jargon | Grepped the full page.tsx for those terms plus `רצפה`/`תקרה` — zero matches | CLEAN |
| Hebrew naturalness | Read as a native speaker: reads fluently, no translationese, no grams-and-E-codes recitation | PASS (subjective; no naturalness-gate score run — note this if a formal gate exists) |

No CRITICAL or HIGH copy-content defect found in the blurb text itself. The blockers below are process and code-robustness findings, not copy-quality findings.

## Findings by Severity

### CRITICAL — must resolve before launch

**RT-1 (CRITICAL): Content Agent sign-off missing for `CREATINE_DESCRIPTION`.**
Evidence: `supplements/page.tsx:27-32` self-documents as pending both gates; no content-package artifact exists for TASK-503 anywhere under `C:\Bari\03_operations\reports\content\` or elsewhere (only the pre-existing TASK-492C artifacts, which cover the destination page's copy, not this hub blurb).
Implication: per the standing hard rule, this string cannot reach the owner. My review is one of two required signatures; the other is absent.
Routes to: `content-agent` (author the sign-off review of `CREATINE_DESCRIPTION`), then back through this gate if changes result.

### HIGH — should resolve before launch

**RT-2 (HIGH): Stat-source scope inconsistency in `featured-creatine-intelligence-card.tsx:19-27`.**
`honestDoseCount` is explicitly scoped to `creatineIsraeliProducts` (matches its label "מהמדף הישראלי במינון הוגן"), but `undisclosedCount` and `directoryVerifiedCount` are computed from the **combined** `creatineProducts` array (Israeli + worldwide) with no scope stated in their labels ("בלי מינון מפורט על האריזה", "אומתו מול מאגר תקנים") and no code comment explaining why the three stats use two different source arrays.
Evidence: today's numbers are correct only because zero worldwide products carry `doseHonesty:"undisclosed"` and zero Israeli products carry `certTier:"directory_verified"` — verified by manually enumerating all 31 rows in `creatine-page-data.ts`. This is a data coincidence, not an enforced invariant.
Implication: if a future corpus refresh adds an undisclosed-dose worldwide reference product, or an Israeli product later becomes directory-verified, this card will silently start blending Israeli-shelf and worldwide-benchmark counts under labels that (by pattern-matching the adjacent Israeli-scoped stat) a reader would reasonably assume are also Israeli-only — no test or lint would catch the drift.
Routes to: `frontend-agent` (scope all three filters consistently and comment the intended scope, or make the ambiguity impossible by construction).

**RT-3 (HIGH): Missing themed category photo — visual inconsistency with every other live card.**
`public/hashvaot/themes/` contains 22 stock category photos (one per live category: `bread.jpg`, `magnesium.jpg`, `hummus.jpg`, etc.) and its own README documents this as the standing pattern ("Each `/hashvaot` index card renders a stock category photo via `theme={{ photo: ... }}`"). `featured-creatine-intelligence-card.tsx:50` passes only `theme={{ accent: "#8C6B4A" }}` — no `photo` key — and no `creatine.jpg` exists in that folder. Confirmed on `TASK-503_screenshots\supplements-mobile-375.png`: the creatine card renders with only a flat tint wash directly beneath the magnesium card, which does show its themed photo — the asymmetry is immediately visible to anyone scrolling the hub.
Implication: this is not a code bug (the component contract explicitly allows omitting `photo` while "a category-true photo is being commissioned") but it is a real, documented gap against the standing visual-completeness convention, and it is visible in the exact screenshot meant to demonstrate this task is ready.
Routes to: `design-agent` (commission/select the stock photo per the existing README runbook — free-license stock preferred, AI generation only as a fallback with owner approval).

### MEDIUM — should document or monitor

**RT-4 (MEDIUM): Stale "DRAFT CONTENT" comment on the destination page, now more visible.**
`bari-web/src/app/hashvaot/creatine/page.tsx:6` still reads "DRAFT CONTENT — orchestrator gates (Content + Adversarial QA sign-off) before owner sees it," even though `tasks/closed/TASK-492C.md`'s `close_reason` confirms the page's own content already passed both gates (content authored + Adversarial QA red-team GO, RT-1 fixed, re-gated GO, merged to master 2026-07-04). This file is not touched by the TASK-503 diff, so it is out of this task's direct scope, but TASK-503's entire purpose is to raise this page's visibility (hub card + sitemap), so a stale comment claiming un-gated draft status is now more likely to mislead a future reviewer scanning the codebase.
Routes to: `frontend-agent` (comment cleanup only, non-blocking).

## Verdict

**NO-GO** — blocked on RT-1 (CRITICAL: Content Agent sign-off does not exist for the new consumer-facing string). Track V is fully green (build/tsc/lint clean, no grade/score leak, sitemap wired correctly, numeric claims in the blurb all verified against `creatine-page-data.ts`). Track C found the copy itself honest and clean of every checked guard (antithesis, em-dash, jargon, OFF), but the combined D10 gate requires zero open CRITICAL findings, and this pipeline is missing one of its two mandatory signatures entirely — not weak, not pending review, simply absent from the record.

Once RT-1 clears (Content Agent sign-off obtained), RT-2 and RT-3 should be explicitly acknowledged (per Hard Rule 10, HIGH requires acknowledgment, not necessarily resolution) before this becomes GO-WITH-FINDINGS. RT-4 is non-blocking.

Do not fix, approve, or close TASK-503. Proposed status: RETURNED.
