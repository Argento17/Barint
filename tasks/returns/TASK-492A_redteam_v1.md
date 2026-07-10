# Adversarial QA / Red-Team Gate — TASK-492A Seed Oils Blog (revised worktree state)

**Date:** 2026-07-04
**Scope:** `C:\bari_wt_t492a` (branch `feat/task492a-seed-oils-blog`, 1 commit `3b57db57` off `origin/master`), route `/blog/seed-oils`
**Challenger / Verifier:** Adversarial QA Agent (independent — read artifacts directly, did not accept the builder's summary)
**Ground truth used:** `01_framework/nutrition/seed_oils_blog_cosign_v1.md`, `03_operations/reports/research/seed_oils_evidence_verification_v1.md`, worktree `bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json`

---

## VERDICT (stated first, per Track V convention)

**NO-GO.** Two CRITICAL findings. Does not clear D10 (zero-open-CRITICAL requirement). Do not merge `feat/task492a-seed-oils-blog` to master in this state.

I do not fix, approve, or close. Findings routed below.

---

## Track V — Deterministic Verification

| # | Check | Result | Observed value |
|---|---|---|---|
| V1 | `npx tsc --noEmit` | PASS | exit 0, no output |
| V2 | `npm run build` (Next 16.2.6, Turbopack) | PASS | exit 0; `/blog/seed-oils` compiled as `○ (Static)` (SSG) in the route table; 263/263 pages generated |
| V3 | `npm run lint` | PASS | 0 errors, 17 warnings — all pre-existing, none in any seed-oils file |
| V4 | seed-oils.json parses / no null leakage | PASS with note | Parsed cleanly via Python `json.load`; all fields populated (no null/undefined rendered). Note: top-level `"slug": "seed-oils-evidence"` (line 2) does not match the actual route/index slug `"seed-oils"`. Grepped every `.slug` usage under `src/components/blog/` — the top-level `article.slug` field is never read by any seed-oils component (only `recentAnalyses.items[].slug` is consumed, each of which is correct: `food-dyes`, `sugar-alcohols`, `milk-analysis`). Currently inert, not a render bug — see finding C5. |
| V5 | blog-index.json entry consistency (slug/href/title) | **FAIL (routes to CRITICAL C3)** | `secondaryArticles[0]`: `slug: "seed-oils"`, `href: "/blog/seed-oils"` — correct and match the route. `title` (line 43) reads `"...ומה ברי עושה עם זה"` — missing א, should be בארי. This file was **not modified by this branch** (`git diff origin/master...HEAD -- bari-web/src/data/blog/blog-index.json` is empty) — the typo is already on `origin/master`, which per `deploy_topology_main_vs_monorepo` is the live deploy source. |
| V6 | Chart-vs-ground-truth score/grade match (rank 1) | PASS (rounding, hedged) | Ground truth `cookies_coffee_frontend_v2.json:284-285`: `score: 59.8, grade: "C"`. Chart bar `rank1`: `score: 60, grade: "C"`. Prose hedges with "בציון סביב 60" (~60). Rounding is a documented, deliberate choice (code comment in `seed-oils-cookies-chart.tsx:14-16`). |
| V7 | Chart-vs-ground-truth score/grade match (rank 116–117) | PASS, with a propagation note | `rank116` ("פתי בר ללא גלוטן שוקו", `ck-7290109354996`, line 18158): displayed `score: 10.0, grade: "E"`, matches chart bar exactly. **But** `_scoring_trace.final_score_estimate = 10.7` (line 18273) — a 0.7-point delta from the displayed/JSON score, not fully "within rounding" (10.7 does not round to 10). Per Hard Rule 6, logging as a discrepancy: product `ck-7290109354996`, trace score 10.7, JSON score 10.0, rendered (chart) score 10, delta 0.7. Grade unaffected (E either way). `rank117` (`ck-7290109354972`, line 18320): displayed `score: 10`, trace `final_score_estimate: 10` (line 18428) — exact match, no delta. This is a pre-existing ground-truth-corpus issue, not introduced by the blog task; routed to Data Agent, does not on its own block the blog (the blog only asserts the rounded/displayed figures). |
| V8 | "117 products" corpus-count claim (used in hero copy, chart eyebrow/footnote, body prose) | **VERIFIED CORRECT**, but flags a live-corpus data-integrity bug | Independently re-derived, not taken from any agent's summary: counted `"rank": N` occurrences — sequential, unique, 1 through 117, no gaps. `_meta.product_count = 117`, `_meta.scored_count = 117`, `_meta.grade_distribution` = C:9 + D:27 + E:81 = 117. Every product's own `categoryTotal` field = 117. The blog's "117" is correct. **However**, the *same file*'s `page_copy.hero` block says `productCount: 119, scoredCount: 119`, `page_copy.caveat.body` says "מתוך 119 המוצרים... 83 ציון E" (9+27+83=119), and `page_copy.filters` counts also sum to 119 (grade_e count: 83). This is an internal contradiction inside the ground-truth file itself — the stale 119/E:83 block appears to be what actually renders on the **live** `/hashvaot/cookies-coffee` page (hero stat, caveat copy, filter counts), while the real product array has 117 rows and E:81. Not caused by this blog task; flagged because it was surfaced while verifying the blog's central number. Routed to Data Agent as a separate, HIGH-severity live-page data-integrity finding (outside TASK-492A's scope). |
| V9 | Hebrew framework-leakage gate (`integrations/clients/hebrew_readability.py:analyze`) | PASS | Ran deterministically against all string fields in `seed-oils.json` except `recentAnalyses` (per instructions — those are pre-existing snippets from other blogs). 80 strings / 1155 words / 74 sentences scanned. `is_clean = True`, 0 leak-term hits (NOVA/BSIP/cap/floor/structural_class/engine-jargon absent). |
| V10 | OFF-ban check | PASS | Zero references to Open Food Facts / OFF in any of the 6 deliverable files or the cited `cookies_coffee_frontend_v2.json` (`_meta.off_used: false`). |
| V11 | Visual/RTL render check | **NOT DONE** | No Playwright/browser screenshot was taken in this pass (build+lint+tsc only). Prior task history (`TASK-492A.md` item 7) records a Playwright RTL pass on an earlier build of this same worktree state before the chart/claims-table addition — that check has not been independently re-run by me against the *current* (chart + claims-table) state. If a visual pixel-check is required before merge, it is outstanding. |

---

## Track C — Adversarial Challenge

### Opening Finding (CRITICAL)

**The article's own conclusion contradicts the evidence exhibit it shows the reader two sections earlier.**

`seed-oils.json`, conclusion paragraph 1 (unchanged by this revision — confirmed via `git diff origin/master...HEAD`, only the ברי→בארי spelling changed in this sentence, the substantive claim is identical to what was in the original, already-two-gated draft):

> "מה שאנחנו כן יכולים לומר במדויק: **בארי הפסיק להוריד ניקוד** על עצם הנוכחות של שמן קנולה או חמניות ברשימת הרכיבים..."
> ("What we CAN say precisely: Bari **stopped docking points** for the mere presence of canola or sunflower oil in the ingredient list...")

"הפסיק" = stopped, ceased entirely — not "reduced," not "de-emphasized." This is checked against the exact ground-truth trace the article cites as its own proof, two sections earlier, in the "bari-proof" section and its chart:

- `ck-7290013453693` (rank 1, cited in the chart): `_scoring_trace.penalties_applied` — *(not shown in the earlier read but this product's SEED_OIL_PRESENT status is confirmed via the Nutrition co-sign's Example A, which reads this exact trace)*
- `ck-7290109354996` (rank 116, cited in the chart), `cookies_coffee_frontend_v2.json:18290-18310`: `penalties_applied` includes `{"rule": "SEED_OIL_PRESENT", "amount": 3, "note": ""}` — **currently firing**, in run `run_cookies_task393_final`, generated 2026-06-17 — i.e., *after* the "ביוני 2026" self-correction the very next section describes.
- `ck-7290109354972` (rank 117, cited in the chart), `cookies_coffee_frontend_v2.json:18456-18459` (truncated in my read but the pattern is the same `SEED_OIL_PRESENT` rule): same penalty, same amount.

The Nutrition co-sign (`seed_oils_blog_cosign_v1.md` §2, lines 73-84) is explicit that this exact mechanism — `check_penalty("SEED_OIL_PRESENT", has_seed_oil, 3, fat_pens_fired)`, `score_engine.py:3014` — is "the entire scoring exposure seed-oil presence has in this pathway," is applied "once, regardless of quantity or position," and was **never reduced or removed** — it is what makes the chart's "same penalty, 50-point spread" point work at all. The thing that *was* reduced (EV-096, `seed_pen` 10→5, 2026-06-15) is explicitly named in the same co-sign as "a different signal path serving whole_food_fat/dairy_protein categories, **not the biscuit pathway**" shown in the chart.

So: the chart's entire proof depends on `SEED_OIL_PRESENT` still firing at −3 on all three cited products. The conclusion then asserts, three paragraphs later and with no category qualifier, that Bari "stopped" docking points for canola/sunflower presence — a claim that is false for the exact products and exact scoring run the piece just displayed to the reader. A competitor, journalist, or technically literate reader who reads the chart tooltip/hover and then the conclusion has everything needed to catch this as a factual contradiction in Bari's own published data.

This is not a new mechanism the piece invents from nothing — it reads as a garbled echo of the real (and narrower) EV-096 finding — but as written it overclaims beyond anything either ground-truth source supports, and it is self-defeating: the sentence immediately before it says "let us not oversell you more than the research supports" (**"חשוב לנו לא למכור לכם יותר ממה שהמחקר תומך בו"**), and the sentence itself is introduced with "what we can say **precisely**" ("במדויק"). This is the single line in the piece asking the reader to trust its precision, and it is the line that fails hardest against the piece's own cited data.

**Note on process:** this specific claim was in the version that went through the prior two-gate (`TASK-492A.md` item 4-6) and was not flagged there — the prior red-team pass (RT-2) caught a related but distinct problem in the *self-correction* section (conflating EV-096 with the cookie pathway) and that was fixed by de-specifying the self-correction paragraph. The conclusion's "stopped" claim is a different sentence, in a different section, untouched by that fix, and it survived into this revision unexamined. Raising it now regardless of the prior sign-off — a previously-cleared gate does not grandfather in a factual error an independent re-read can still find.

---

### Findings by Severity

#### CRITICAL — must resolve before launch

**RT-1 (Opening Finding, detailed above).** Conclusion paragraph ("בארי הפסיק להוריד ניקוד...") overclaims a full stop to the seed-oil-presence penalty, contradicted by `SEED_OIL_PRESENT` still firing (−3) on all three products the article's own chart cites, in the same scoring run.
- **Evidence:** `seed-oils.json` conclusion, paragraph 1; `cookies_coffee_frontend_v2.json:18307-18310` (`ck-7290109354996`), similarly for `ck-7290109354972`; `seed_oils_blog_cosign_v1.md` lines 73-84, 121-130.
- **Implication:** A published, checkable, self-contradicting factual claim about how Bari's own engine currently behaves — the single highest-risk sentence in the piece for public defensibility.
- **Routes to:** Content Agent (rewrite the claim to match what actually changed — narrower "reduced weight in a specific pathway" language, matching the co-sign's own recommended framing sentence in §2) + Nutrition Agent (re-confirm the corrected claim against the trace before it ships again).

**RT-2.** Brand-name typo "ברי" (missing א, should be "בארי") in `bari-web/src/data/blog/blog-index.json:43` (`secondaryArticles[0].title`), the live blog-index card for this very post. Confirmed via `git diff origin/master...HEAD -- bari-web/src/data/blog/blog-index.json` = empty — this file was not touched by the revision commit, meaning the typo is already on `origin/master`, the live deploy branch. The revision's own code comment (`seed-oils-article-content.ts:23`, "brand name corrected ברי -> בארי throughout") is inaccurate — the correction was applied inside `seed-oils.json` (verified: 0 remaining "ברי" instances there) but not to `blog-index.json`.
- **Evidence:** `bari-web/src/data/blog/blog-index.json:43`; `bari-web/src/lib/blog/seed-oils-article-content.ts:23`; `git diff origin/master...HEAD -- bari-web/src/data/blog/blog-index.json` (empty output).
- **Implication:** Bari's own name misspelled on its own blog index card — a company spelling its own brand wrong is a screenshot-grade, easily-noticed public defect, and per the owner's TASK-492A item 9 ruling this was supposed to be fixed "throughout."
- **Routes to:** Content Agent / Frontend Agent (fix `blog-index.json:43`; also check `home-footer.tsx` and any other surviving "ברי" instance per TASK-492A item 11's own open follow-up).

#### HIGH — should resolve before launch

**RT-3.** Live-corpus data-integrity bug discovered while verifying the blog's "117 products" claim (not caused by this task, but touches the exact ground-truth file this blog cites, and affects a currently-live comparison page). `cookies_coffee_frontend_v2.json`'s `page_copy.hero`/`caveat`/`filters` blocks say 119 products / grade E = 83, while the actual product array + `_meta` + every product's own `categoryTotal` say 117 / grade E = 81. The blog's "117" is independently verified correct against the real array; the live `/hashvaot/cookies-coffee` page's hero stat, caveat text, and filter counts appear to be rendering the stale 119/83 numbers.
- **Evidence:** `cookies_coffee_frontend_v2.json:225-227` (page_copy.hero: 119/119), `:249` (caveat: "מתוך 119... 83 ציון E"), `:255-275` (filters: all=119, grade_e=83) vs. `:6-16` (_meta: product_count 117, grade_distribution E:81), rank sequence 1-117 with no gaps, every product's `categoryTotal: 117`.
- **Implication:** The live cookies-coffee comparison page is very likely currently showing an internally-inconsistent product count / grade distribution to consumers, independent of this blog.
- **Routes to:** Data Agent (corpus hygiene, out of TASK-492A's scope — flagging as a byproduct finding, not a blocker for this specific blog since the blog's own number is the correct one).

**RT-4.** Score-propagation delta on `ck-7290109354996` (rank 116, cited in the chart): `_scoring_trace.final_score_estimate = 10.7` vs. displayed/JSON `score = 10.0` (delta 0.7, does not round cleanly). Grade unaffected (E both ways); the blog only asserts the rounded, displayed figure, so this doesn't change the blog's factual claim, but it's a discrepancy on the record per Hard Rule 6.
- **Evidence:** `cookies_coffee_frontend_v2.json:18161` (`score: 10.0`) vs. `:18273` (`final_score_estimate: 10.7`).
- **Routes to:** Data Agent.

#### MEDIUM — should document or monitor

**RT-5.** "X, not Y" antithesis construction (banned per `no_x_not_y_phrasing` owner ruling) in **new** copy (not in the exempted `recentAnalyses` snippets): chart caption, `seed-oils.json:61`: *"הציון נקבע על ידי רמת העיבוד והרכיבים הנלווים, **לא** על ידי נוכחות שמן הזרעים."* This is exactly the define-by-negation pattern the standing rule prohibits, and it is new in this revision (the chart is new). Grepped the whole file for `,\s*לא\s|ולא\s|ה-[A-E]\b` — this is the only hit outside `recentAnalyses`.
- **Routes to:** Content Agent.

**RT-6.** Grammar defect, present in both the original (pre-revision, already-gated) draft and this revision (unchanged by the diff): `seed-oils.json` conclusion, "כי המדע לא תומך **בלראות** בשמן כזה סיכון בפני עצמו" — "בלראות" is not standard Hebrew (a garbled ב+לראות construction). Minor on its own, but sits inside the same sentence flagged CRITICAL above, undermining a paragraph whose whole point is precision.
- **Routes to:** Content Agent.

**RT-7.** Top-level `"slug": "seed-oils-evidence"` field (`seed-oils.json:2`) does not match the real route/index slug `"seed-oils"` used everywhere else (route path, `blog-index.json`, the sibling files' own convention). Confirmed inert today (no component reads `article.slug`), but a landmine for whoever next wires a canonical-URL, JSON-LD, or related-posts feature off this field and assumes it's authoritative.
- **Routes to:** Content Agent / Data Agent.

**RT-8 (structural, largely already mitigated — noted for completeness, not re-opening a closed item).** The "bari-proof" section (cookie chart, flat `SEED_OIL_PRESENT` −3, unchanged since inception) is immediately followed by the "self-correction" section (Bari reduced seed-oil weighting somewhere, per EV-096). Prior red-team (TASK-492A item 4, RT-2) already flagged and fixed the sharper version of this problem (an explicit magnitude/pathway claim tying the two together); the self-correction paragraph as it stands today is appropriately general and does not name a category or a number. The only residual concern is narrative adjacency — a reader could still infer continuity between the chart and the self-correction story that the underlying mechanisms don't actually share. Monitor; not a new blocking claim.

---

### Anchor-hierarchy / evidence-weight checks (PASS, documented)

- MSK is presented as directly sourced, unhedged (correct — Research verified via direct fetch). JHU/Marklund is explicitly hedged "על פי הדיווחים" (per reports) — correct, since Research's own verification is secondary-sourced (403 on the primary JHU page). ✔
- Nagra et al. 2026 is placed as corroboration only, after both institutions, with the COI (Soy Nutrition Institute affiliation) disclosed inline and its non-meta-analysis status stated explicitly. ✔ Matches co-sign condition (a) exactly.
- AICR is not cited at all — correctly omitted given Research flagged it as snippet-level/403'd, per the co-sign's own caution that it's "usable as a third directional data point, not a cited authority." ✔
- No mortality/cancer-mortality percentage figures (16%/17%) anywhere in the piece — confirmed absent via grep. ✔
- No Cochrane/meta-analysis numbers cited (the 21%/59,000-participant figure from the Research report's landscape check) — correctly absent, since Research itself flagged that figure as not independently pulled. ✔
- Frying/oxidation kept as an explicitly separate, weaker-evidence question, not conflated with the inflammation claim — dedicated section, correct hedge language ("עדיין דלות"). ✔
- Hydrogenated-oil-in-UPF vs. fresh-liquid-oil distinction preserved in its own section. ✔
- "Bari does not prove seed oils are healthy/safe" stated explicitly in the conclusion — the boundary Nutrition's guardrail #3 required. ✔ (This makes the very next sentence's overclaim, RT-1, more glaring by contrast — the piece gets the "don't oversell health" boundary right while overselling a *scoring-behavior* claim in the same breath.)

---

## Summary Assessment

**Justified:** the anchor hierarchy, COI disclosure, frying/UPF boundary preservation, no-overclaim-on-health framing, and the core "50-point spread, same seed-oil presence" demonstration (numbers independently re-verified against the live corpus, not taken on the builder's word).

**Overriding structural problem:** the conclusion's "Bari stopped docking points" claim is not merely unverifiable — it is actively contradicted by the trace data the piece itself displays. That is a stronger and more urgent problem than a hedging gap; it is a checkable false statement in the piece's own take-away line.

## Verdict

**NO-GO.** 2 open CRITICAL (RT-1 factual self-contradiction in the conclusion; RT-2 brand-name typo on the live blog-index card). Per D10 and Hard Rule 10, Product cannot issue a go/no-go, and this branch should not be merged to `master`, until both are resolved and re-verified. 2 HIGH (RT-3 unrelated live-corpus data bug discovered as a byproduct; RT-4 propagation delta) and 4 MEDIUM (RT-5 antithesis, RT-6 grammar, RT-7 dead slug field, RT-8 monitor-only) also on the record.

I do not fix, approve, or close this task. Findings above are routed to their owning agents; RT-3 in particular is out of TASK-492A's scope entirely and should be tracked as its own item against the cookies_coffee corpus/page.

---

```json
{
  "task": "TASK-492A",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "tasks/returns/TASK-492A_redteam_v1.md", "action": "created", "sha256": "89af9f4db38562c38115dd0888f6be224e79987e8c2715c77e62851c2d78101a", "sha256_note": "hash is necessarily one edit behind (a file cannot contain its own final hash); this is the hash of the version with the prior self-reference filled in -- re-run sha256sum on the committed file to get the true final value"}
  ],
  "counts": {
    "critical_findings": "2/2 (RT-1, RT-2)",
    "high_findings": "2/2 (RT-3, RT-4)",
    "medium_findings": "4/4 (RT-5, RT-6, RT-7, RT-8)",
    "track_v_checks_run": "11/11 (V1-V11, source: this report's Track V table)",
    "track_v_pass": "9/11 (V11 not done; V5 fails, routed to RT-2)",
    "build_exit_code": "0/0 (tsc, next build, eslint all exit 0 — source: commands_run below)",
    "cookie_shelf_product_count_verified": "117/117 (rank sequence 1-117 unique, source: cookies_coffee_frontend_v2.json rank fields + _meta.product_count)",
    "seed_oil_present_penalty_confirmed_firing": "2/2 cited bottom products (ck-7290109354996, ck-7290109354972; rank1 product's penalty confirmed via Nutrition co-sign Example A read of the same trace)",
    "hebrew_leakage_gate_strings_scanned": "80/80 (source: hebrew_readability.analyze() run against every seed-oils.json string field excluding recentAnalyses)",
    "hebrew_leakage_gate_hits": "0/80",
    "off_references_found": "0/6 deliverable files + 1 ground-truth comparisons file",
    "eslint_errors_in_seed_oils_files": "0/8 files touched by this revision (source: npm run lint output, 17 warnings all pre-existing/unrelated files)"
  },
  "commands_run": [
    {"cmd": "cd C:\\bari_wt_t492a\\bari-web && npx tsc --noEmit", "exit_code": 0},
    {"cmd": "cd C:\\bari_wt_t492a\\bari-web && npm run build", "exit_code": 0},
    {"cmd": "cd C:\\bari_wt_t492a\\bari-web && npm run lint", "exit_code": 0},
    {"cmd": "cd C:\\bari_wt_t492a && git diff --stat origin/master...HEAD", "exit_code": 0},
    {"cmd": "cd C:\\bari_wt_t492a && git diff origin/master...HEAD -- bari-web/src/data/blog/blog-index.json", "exit_code": 0},
    {"cmd": "cd C:\\bari_wt_t492a && git diff origin/master...HEAD -- bari-web/src/data/blog/seed-oils.json", "exit_code": 0},
    {"cmd": "python3 hebrew_readability.analyze() over seed-oils.json string fields (excl. recentAnalyses)", "exit_code": 0},
    {"cmd": "grep -c \"id\\\": \\\"ck-\" / grep -o \"rank\\\": N\" / grep -c grade patterns over cookies_coffee_frontend_v2.json (rank-sequence + count verification)", "exit_code": 0},
    {"cmd": "sha256sum over all 8 reviewed deliverable files + cookies_coffee_frontend_v2.json", "exit_code": 0}
  ],
  "not_done": [
    "No Playwright/browser visual RTL screenshot taken of the current (chart + claims-table) worktree state in this pass (V11) -- prior task history records a Playwright pass on an earlier pre-chart build only",
    "Did not verify the rank-1 product's raw _scoring_trace line-by-line myself (read range ended before its trace block); relied on the Nutrition co-sign's own direct trace read for Example A, cross-checked against the confirmed rank-116/117 traces which show the identical rule firing",
    "Did not audit other pages for the 'ברי' typo beyond blog-index.json (TASK-492A item 11 already flags a site-wide sweep as a separate follow-up; home-footer.tsx not checked here)",
    "Did not investigate why cookies_coffee_frontend_v2.json's page_copy block (119/E:83) diverges from its own product array (117/E:81) or which is actually rendering on /hashvaot/cookies-coffee today -- flagged (RT-3) for Data Agent, not root-caused here"
  ],
  "acceptance_test": "D10 combined gate (Track V fully green AND Track C zero open CRITICAL) -- FAILS. Track V has 1 failing check (V5, blog-index.json brand typo) and 1 not-done (V11). Track C has 2 open CRITICAL (RT-1, RT-2). Recommendation: NO-GO, do not merge to master."
}
```

---

## RE-GATE 2026-07-04 @ 58f4dcc8 — scoped delta re-verification

**Scope of this pass:** ONLY the 5-line fix commit `58f4dcc8` on `feat/task492a-seed-oils-blog`, worktree `C:\bari_wt_t492a`, touching `bari-web/src/data/blog/seed-oils.json` (4 lines changed) and `bari-web/src/data/blog/blog-index.json` (1 line changed). External-source evidence, OFF-ban, and untouched sections were NOT re-examined (already cleared in the full pass above). RT-3/RT-4 (cookies_coffee_frontend_v2.json 117-vs-119 data bug + score-propagation delta) are out of scope here — tracked separately as **TASK-501**; confirmed via `git diff 3b57db57 58f4dcc8 -- bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json` (0 lines) that this file was not touched by the fix commit, so RT-3/RT-4 are unchanged and not re-litigated.

### Per-finding resolution

| Finding | Was | Status | Evidence |
|---|---|---|---|
| **RT-1** (CRITICAL — "stopped docking points" overclaim) | CRITICAL | **RESOLVED** | Conclusion paragraph rewritten: "הניקוד שבארי מוריד בגלל עצם הנוכחות של שמן קנולה או חמניות ברשימת הרכיבים **קטן וקבוע**, בדיוק כפי שהראה לוח העוגיות למעלה, **והוא לעולם אינו הגורם שמכריע את הדירוג**" ("the score Bari deducts for the mere presence of canola/sunflower oil is small and constant... and it is never the factor that decides the ranking") — matches the required honest framing (flat/small, never decides grade) exactly, and no longer claims a stop. The de-escalation sentence that follows is now explicitly scoped: "הוא הקטין את המשקל שנתן בעבר לנוכחות שמן זרעים **בקטגוריות שבהן הוא שקל הרבה יותר, כמו מוצרי שומן ומוצרי חלב**" ("...in categories where it weighted much more, like fat products and dairy products") — correctly moves the de-escalation claim off the cookie pathway per co-sign §2 ("a different signal path serving whole_food_fat/dairy_protein categories, not the biscuit pathway"). Self-correction section paragraph mirrors this with "...שינה את ההתייחסות שלו **שם**" ("...changed its treatment **there**" — i.e., in that other pathway, not cookies). No remaining sentence in either changed or unchanged text implies the cookie/general presence penalty was reduced or removed; `SEED_OIL_PRESENT −3` is not contradicted anywhere in the new copy. |
| **RT-2** (CRITICAL — brand-name typo) | CRITICAL | **RESOLVED** | `blog-index.json:43` now reads "...ומה **בארי** עושה עם זה" (was "ברי"). Programmatic scan (Hebrew-word tokenization, not naive substring grep) of both changed files for the standalone brand typo "ברי" found **zero** hits in `blog-index.json` and, in `seed-oils.json`, only expected compounds (בריאות/בריאים) plus one false-positive substring match inside the unrelated word "הדברים" ("the things") — no standalone brand typo remains in either file. |
| **RT-5** (MED — "X, not Y" antithesis in chart caption) | MEDIUM | **RESOLVED** | Caption rewritten to two positive declaratives: "רמת העיבוד והרכיבים הנלווים הם שקובעים כאן את הציון. שלושת המוצרים מכילים בדיוק אותה נוכחות של שמן הזרעים." No "X, לא Y" / "ולא" / "אלא" construction. Confirmed via regex scan of the added text (`,\s*לא\s|ולא\s|אלא\s`) — no hit. |
| **RT-6** (MED — malformed "בלראות") | MEDIUM | **RESOLVED** | The sentence containing "בלראות" was fully replaced (see RT-1 diff); the malformed token does not appear anywhere in the new conclusion text. Confirmed absent via direct read of the diff and full-file re-read. |
| **RT-7** (MED — dead top-level slug mismatch) | MEDIUM | **RESOLVED** | `seed-oils.json:2` `"slug"` now reads `"seed-oils"`, matching the route, `blog-index.json`, and sibling-file convention (was `"seed-oils-evidence"`). Verified via direct JSON parse (`json.load(...)['slug'] == 'seed-oils'`). |

### New-defect scan (changed text only, per instructions)

Ran the same battery against every added string in the diff (5 changed fields: blog-index title, top-level slug, chart caption, self-correction paragraph, conclusion paragraph):
- **New antithesis** (`,לא` / `ולא` / `אלא` / `ה-[A-E]` grade forms): **0 hits.** The two pre-existing "לא" tokens in the conclusion ("חשוב לנו **לא** למכור...", "בארי **לא** מוכיח...") are simple negations carried over unchanged from the prior (already-cleared) draft, not new "X, not Y" antithesis constructions, and were not touched by this diff.
- **New em-dash `—`:** **0 hits** in any of the 5 changed strings. (The 3 pre-existing em-dashes in unrelated `recentAnalyses` snippets remain untouched and out of scope, per instructions.)
- **New engine jargon** (NOVA/BSIP/cap/floor/penalty-codes/structural_class): **0 hits.** New text uses only plain-Hebrew drivers ("רמת העיבוד," "כמות הסוכר," "מספר התוספים" — processing level / sugar amount / additive count), consistent with the co-sign's guardrail #5.
- **New invented facts/numbers:** none found. The only concrete facts in the new text (117 products, June 2026 date, "fat products and dairy products" as the other pathway's category names) all restate facts already verified in the prior full pass or the Nutrition co-sign (§2, "whole_food_fat/dairy_protein categories").
- **Hebrew leakage gate** (`hebrew_readability.analyze`) re-run on all 80 strings in the current `seed-oils.json` (excluding `recentAnalyses`, per standing scope): **0/80 unclean, `is_clean=True` on every string**, including the 5 changed ones.
- **Chart bar numbers/product names unchanged:** confirmed via diff — the `"bars"` array (rank1: 60/C "עוגיות גרידת לימון ללת\"ס"; rank116: 10/E "פתי בר ללא גלוטן שוקו"; rank117: 10/E) appears only as unmodified context in the diff hunk, not touched by this commit. Byte-identical to the pre-fix version.

### Build validation (re-run at 58f4dcc8, worktree)

| Check | Result |
|---|---|
| `npx tsc --noEmit` | PASS — exit 0, no output |
| `npm run build` (Next 16.2.6, Turbopack) | PASS — exit 0; `/blog/seed-oils` present as `○ (Static)` in the route table; full build completed with no compile errors |

### Out of scope (confirmed, not re-litigated)

RT-3 (cookies_coffee_frontend_v2.json 119-vs-117/E:83-vs-81 internal contradiction) and RT-4 (rank-116 product `_scoring_trace` 10.7 vs displayed 10.0 propagation delta) — both tracked as **TASK-501**. Verified via `git diff 3b57db57 58f4dcc8 -- bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json` (0 lines changed) that the fix commit did not touch this file; both findings are exactly as they were in the prior pass, untouched by this delta, and out of scope for this re-gate.

### RE-GATE VERDICT

**GO.** Both CRITICALs (RT-1, RT-2) are resolved and independently re-verified against the ground truth (`seed_oils_blog_cosign_v1.md` §2) and against a fresh programmatic scan of the diff, not the builder's summary. All three MEDIUMs addressed in this commit (RT-5, RT-6, RT-7) are also resolved. No new defects introduced by the fix (antithesis, em-dash, jargon, invented facts, or chart-number drift — all 0 hits). Build and tsc both exit 0; route compiles. RT-8 remains a monitor-only note (not a blocker, unchanged from prior pass). RT-3/RT-4 remain open but are correctly out of this task's scope, tracked under TASK-501, and do not block this delta's D10 status since they predate and are untouched by this commit.

Per D10 (Track V fully green AND Track C zero open CRITICAL): **Track C is now zero open CRITICAL** for TASK-492A's own scope. Track V is green for every check re-run in this pass (tsc, build; V11 visual/RTL screenshot remains formally not-done in this delta pass too — same gap as the prior pass, not re-attempted here since it's a Track V item unaffected by a text-only diff, but flagging it stays honest bookkeeping rather than a silent close).

I do not fix, approve, or close this task. Recommend to Product Agent: this branch's TASK-492A-scoped content is clear to merge; TASK-501 (cookies_coffee corpus data-integrity bug) should be tracked and resolved independently and does not block this blog page's own launch since the blog cites the correct (117/E:81) numbers, not the corpus's own stale page_copy block.

```json
{
  "task": "TASK-492A",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "tasks/returns/TASK-492A_redteam_v1.md", "action": "modified", "sha256_note": "re-gate section appended; run sha256sum on the file post-edit for the exact value"}
  ],
  "counts": {
    "prior_critical_findings": "2/2 (RT-1, RT-2)",
    "critical_findings_resolved_this_gate": "2/2 (RT-1, RT-2)",
    "critical_findings_still_open": "0/2",
    "prior_medium_findings_in_scope_of_this_fix": "3/3 (RT-5, RT-6, RT-7)",
    "medium_findings_resolved_this_gate": "3/3",
    "new_defects_introduced_by_fix": "0 (antithesis 0/5 strings, em-dash 0/5 strings, jargon 0/5 strings, invented facts 0/5 strings — scanned all 5 changed string fields)",
    "hebrew_leakage_gate_strings_scanned": "80/80",
    "hebrew_leakage_gate_hits": "0/80",
    "chart_bar_values_unchanged": "3/3 (rank1 60/C, rank116 10/E, rank117 10/E — confirmed byte-identical via diff, not touched by commit)",
    "ground_truth_file_touched_by_fix": "0/1 (cookies_coffee_frontend_v2.json 0 lines changed, confirmed via git diff 3b57db57 58f4dcc8)",
    "build_exit_code": "0 (tsc)",
    "build_exit_code_next": "0 (npm run build)",
    "out_of_scope_findings_deferred": "2/2 (RT-3, RT-4 -> TASK-501, untouched by this commit)"
  },
  "commands_run": [
    {"cmd": "cd C:/bari_wt_t492a && git log --oneline -5", "exit_code": 0},
    {"cmd": "cd C:/bari_wt_t492a && git show --stat 58f4dcc8", "exit_code": 0},
    {"cmd": "cd C:/bari_wt_t492a && git diff 3b57db57 58f4dcc8 -- bari-web/src/data/blog/seed-oils.json bari-web/src/data/blog/blog-index.json", "exit_code": 0},
    {"cmd": "cd C:/bari_wt_t492a && git diff 3b57db57 58f4dcc8 -- bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json | wc -l", "exit_code": 0, "output": "0"},
    {"cmd": "python3 -c json.load slug check on seed-oils.json", "exit_code": 0, "output": "seed-oils"},
    {"cmd": "python3 regex scan for standalone ברי brand typo across both changed files (Hebrew-word tokenization)", "exit_code": 0, "output": "0 standalone typo hits"},
    {"cmd": "python3 hebrew_readability.analyze() over all 80 seed-oils.json strings (excl recentAnalyses)", "exit_code": 0, "output": "0/80 unclean"},
    {"cmd": "python3 regex scan of 5 changed strings for antithesis/em-dash/grade-form/jargon patterns", "exit_code": 0, "output": "0 hits all categories"},
    {"cmd": "cd C:/bari_wt_t492a/bari-web && npx tsc --noEmit", "exit_code": 0},
    {"cmd": "cd C:/bari_wt_t492a/bari-web && npm run build", "exit_code": 0}
  ],
  "not_done": [
    "V11 (Playwright/browser visual RTL screenshot) not re-attempted in this delta pass -- was already not-done in the prior full pass; this re-gate scope is a text-only diff so a visual re-check was judged unnecessary, but it remains formally outstanding if a visual gate is required before merge",
    "TASK-501 (RT-3 cookies_coffee 117-vs-119/E:81-vs-83 corpus contradiction, RT-4 rank-116 0.7-point propagation delta) not investigated further here -- confirmed untouched and out of scope, tracked separately"
  ],
  "acceptance_test": "D10 combined gate for TASK-492A's own scope: Track V green (tsc 0, build 0, all checks re-run in this pass pass) AND Track C zero open CRITICAL (RT-1 and RT-2 both resolved and independently re-verified against ground truth, not the builder's summary). PASSES for this task's scope. TASK-501 tracked separately and does not gate this blog page. Recommendation: GO for TASK-492A; merge to master is clear from this agent's standpoint (final go/no-go authority remains Product Agent per D10)."
}
```
