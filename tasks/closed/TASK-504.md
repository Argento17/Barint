---
id: TASK-504
title: Supplements re-direction: kill supplement rankings, launch guides (madrichim) category
owner: product-agent
status: CLOSED
priority: HIGH
closed_at: 2026-07-05
close_reason: >
  Owner "close this project" 2026-07-05. Both guides BUILT + Adversarial QA gate-2 GO (local
  sign-off, noindex), committed 8277450c on feat/task504-guides-template in worktree
  C:\bari_wt_t504 (LOCAL ONLY — not pushed). Final model: A/B/C/D BAND labels (owner "revert to
  ABCD, bands not per-product"); GATE-EXCL-1 + passes_with_flag_split_rule_v2 dual-keyed in
  supplement_guides_bar_rubric_v1.yaml. Creatine /madrichim/creatine = A:0/B:13/C:8/D:3/CA:2, 26
  available-in-Israel (12 shelf + 14 import) + 13 benchmark; Israeli finds added (Nutri Care,
  Extreme, Sunwarrior, GIAS D->C). Magnesium /madrichim/magnesium relabeled A/B/C/D, 2/3/12/1.
  Verified vs live DOM: distributions, images (self-hosted, OFF-clean), copy is_clean, routes 200.
  PARKED (owner's future call, tracked in memory supplements-guides-redirection): migration PR
  (301s /hashvaot->/madrichim + sitemap = consumer-facing deploy tripwire); per-product real
  descriptions under owner freeze + full creatine gate-2; minor residuals (terminology, stale
  comments, integrations/clients/http.py stdlib-shadow infra bug). TASK-504A (dairy pilot) is
  SEPARATE and remains open.
created_at: 2026-07-04
depends_on: []
blocks: []
category_id: null
summary: >
  Owner directive 2026-07-04: ranking supplements does not work (incl. doubts on magnesium). Replace supplement comparisons with a new guides category (madrichim): detailed guide + attribute-level product assessment (absorption, quantity, chemical compound), worldwide benchmark placement, pricing, buy button (dormant-link style), no grades. Strategy brief -> Product+Nutrition+RedTeam consult + C3 challenge -> concrete plan to owner. Supplements first; NO morph to other areas in v1.
---

## Plan APPROVED by owner 2026-07-04 → EXECUTION
Execution contract = `01_framework/product/supplement_guides_concrete_plan_v1.md` (synthesis of Product + Nutrition + strategy red-team + C3). Naming: **מדריכים** hub + "איך לבחור X" page titles (owner approved without override → recommendation stands). Magnesium numeric scores + 1–18 rank come DOWN in the migration (form-tiers + UL flags survive as bar-states).

Verdict model: per-attribute bar-states PASS/FLAG/FAIL/CANNOT-VERIFY across **6 bars** (dose adequacy · form/absorption · third-party verification · price fairness · safety · label transparency) → buckets (clears-all / passes-with-flag / fails / cannot-assess) + one transparent default-pick (cheapest per effective unit among all-clearers). Rubric = versioned config, never a composite score. Benchmark renders product-vs-external-standard (never product-vs-field). Buy button on every product, data-separated from verdicts. /madrichim + 301s in ONE migration PR.

### Build wave (dispatched 2026-07-04)
- **Wave 0 (pre-build, parallel):** Nutrition → versioned bar-rubric config (6 bars + thresholds + blend rule + bar-state logic) · Research → verify 3 magnesium form-ladder PMIDs · Frontend → guide template skeleton + /madrichim hub scaffold spike (worktree).
- **Wave 1:** magnesium golden guide (build to rubric) → gates.
- **Wave 2:** creatine guide (stamp template) → gates.
- **Wave 3:** ship together + hub + migration PR (301s, sitemap) → owner merge.
- Sub-tasks: TASK-504A (rubric), TASK-504B (magnesium guide), TASK-504C (creatine guide), TASK-504D (hub+migration) — allocated as waves land.

### Wave-0 returns
- **✅ Research (magnesium citations) RETURNED + verified** → `03_operations/reports/research/magnesium_form_ladder_verification_v1.md`. MATERIAL: the form-ladder evidence is weaker than the LIVE page claims. NIH ODS backs organic-vs-oxide directionally but names citrate/aspartate/lactate/chloride — **NOT bisglycinate**. Bisglycinate evidence weak/contested (PMID 39770988 2024 n=40 = no sig plasma response + undisclosed Lubrizol COI; PMID 7815675 1994 n=12 helped only most-malabsorptive; PMID 30761462 = mouse). UL verified (350 IOM / 250 EFSA, GI-tolerance). → **form bar must NOT co-equal citrate & bisglycinate; bisglycinate = organic-but-weaker-evidence tier.** Fed to the running rubric author (a5161dbe) mid-flight via SendMessage.
- **⚠️ LIVE-COPY ERROR (must-fix, do NOT carry into guide):** `magnesium-page-data.ts` cites **"EFSA (2021)" ×4 — no such opinion exists** (real: 2001 SCF / 2015 reaffirmation). Page is being replaced by the guide, so fix = ensure guide copy uses correct dates; the fabricated date must not survive migration. (Also disclosed: `integrations/clients/literature.py` DOI-extraction bug grabs wrong ArticleId for PMC-linked records — tooling backlog, no cited DOI affected.)
- **✅ Nutrition rubric (504A) RETURNED** → `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` + `..._companion_v1.md`. 6 bars deterministic; verification none=CANNOT-VERIFY, registry-checked-absent=FAIL; price-fairness reworked to per-disclosed-dose same-currency-pool (avoids banned adjusted-dose math → ₪ and $ don't inter-compare); blend rule; FAIL→fails-before-cannot-assess; anti-drift no-composite invariant. Research citation finding baked in (bisglycinate confidence split, buckets unchanged). 49/49 products classify deterministically.
  - **🔴 VALIDATION FINDING (plan-level):** **0 Israeli-shelf products clear all 6 bars** (missing price/cert → CANNOT-VERIFY) → the approved "clears-all-bars shortlist + single default-pick" is EMPTY for the Israeli shelf; currency-pool separation also breaks a single cross-shelf pick. Fails owner's "just tell me what to buy" harder than the old rank. **→ routed to Product (a7ba8911): resolve the decisiveness mechanism (redefine bucket as no-FAIL / split IL-vs-worldwide picks / honest "closest + what it's missing") + D7 co-sign + confirm this is in-model vs owner-decision.** Wave 1 (magnesium build) BLOCKED on this.
  - Also from rubric: unproven delivery-tech claims ("nano liposomal") → Product scope call; 3 data/copy corrections (California Gold dose tag, Naked cert severity, EFSA-2021 date) → fold into guide build.
- **✅ Frontend spike RETURNED** (commit `35545218`, worktree t504, NOT pushed; tsc/build/lint 0). Typed guide contract (`view-models/guide.ts`: 6 bars, 4 states, 4 buckets, buyUrl standalone-nullable, benchmark=product-vs-external-standard), `bar-state-badge` 4-state primitive (no grade/score), `components/guides/*` template (3 layers), `guide-buy-button` (dormant /catalog treatment), `/madrichim` hub scaffold + placeholder card, mock fixture, migration-TODO block. Screenshots in `tasks/returns/TASK-504_spike_screenshots/`. Design conformance pass NOT yet run (Wave-1 prereq) — HELD until Product resolves the bucket/default-pick mechanism so Design reviews the final template.
- **WAVE-0 COMPLETE.** Product D7 + empty-shortlist RESOLVED (a7ba8911): clears-all empty → honest headline + promote passes-with-flag; per-currency default-pick; nano-liposomal OUT; no owner escalation (0 tripwires). Owner FYI given.

### Wave 1 — magnesium golden guide (IN PROGRESS)
- **✅ Copy gate-1 authored + orchestrator-verified** → `03_operations/reports/content/magnesium_guide_copy_v1.md`. Verified clean: 0 antithesis (`,לא/ולא/אלא`), 0 "EFSA 2021", 0 "דירוג"/grades; bisglycinate correctly hedged (NIH sheet doesn't name it, direct-absorption studies weak → not equal-proof to citrate) in 3 places; honest label-game callouts ("600 caps doesn't change the daily dose is too small"); Cochrane-2020 cramps flag. Buckets: 0/18 clears-all, 5 passes-with-flag (Supherb citrate+B6 / Altman bisglycinate / Altman citrate 120 / Nutricare WELL / NT L.C. cramps), 12 fails, 1 cannot-assess (TRIOMAG).
- **🔵 Frontend integration RUNNING** (a2124001, worktree t504): magnesium-guide-data.ts (18 bar-states from validation table) + finalize template mechanism (empty-clears-all → headline + promote passes-with-flag, no default-pick) + port approved copy → `/madrichim/magnesium`; render-verify. NOT pushed.
- **✅ Frontend integration DONE + committed `b8dc6a20`** (worktree t504, NOT pushed). 18/18 bar-states match validation table (machine-diffed); copy ported verbatim (automated diff caught 2 dropped sentences + 62 quote-char mismatches → fixed); honest headline + passes-with-flag promotion + no default-pick; 0 grade/score chips, dormant buy buttons, product-vs-external benchmark; `/madrichim/magnesium` noindex until gate-2; tsc/build/lint 0, 266 routes; render-verified 8 screenshots.
  - **⚠️ GLITCH found+fixed (owner infra): `guard-two-gate-commit.ps1` had a false-positive scoping bug** — it gated commits on the whole main-tree `git status` (unstaged working-tree changes) instead of the commit's STAGED files, so the 4 pre-existing dirty frozen-description JSONs blocked ALL commits, incl. unrelated worktree ones. Fixed: gate on staged-only + scope to the commit's actual repo (payload cwd, worktree-aware) + markers stay in main registry. **Tested both ways: still exit-2 blocks a real un-signed comparison-JSON staged commit; exit-0 allows the unrelated magnesium worktree commit.** Guard is stronger (now worktree-aware), not weaker. Owner's frozen JSONs untouched — they still require sign-off markers at their own commit. Surfaced to owner.
- **🔴 Gate-2 red-team NO-GO (aff55209)** — engineering GO-quality (18/18 bar-states independently re-derived correct; buckets 0/5/12/1 exact; science all PASS — bisglycinate hedged, UL GI-tolerance, no EFSA-2021, OFF-clean; no stealth ranking). Blocking: **CRIT RT-1** verification-scaffolding leaked into "מקורות" copy (parenthetical about NIH page "blocked in verification env" → also fails hebrew_readability RECOMMENDATION gate) → content. **HIGH RT-2** metadata desc `page.tsx:27` "לא דירוג, לא ציון" = banned word + antithesis + inline-authored (bypassed gate-1) → content+frontend. MED: RT-3 typo ספף→סף · RT-4 "אלה הרשימה" agreement · RT-5 dangling colon in intro (relocated list items) · RT-6 bar-badge reuses A/C/E grade palette on no-grades guide (→ Design). LOW: RT-7 companion §3 summary line says fails-10/cannot-3 but table+page correct at 12/1 (doc-hygiene → Nutrition); RT-8 unused field; RT-9 name truncation.
- **🟡 Design vision-critic GO-WITH-FIXES (a3064b52):** CRIT = bar-state badge imports gradePalette.A/C/E byte-identical (reads as grade; converges w/ red-team RT-6). 3 HIGH measured WCAG fails (bucket count 2.67:1, heading 3.99:1, promoted count ~3.0:1). MED sectionEyebrow ~3.6:1 (TASK-494 systemic). Confirmed passing: RTL, no overflow, no ScoreChip, dormant buttons, non-podium empty-state.
- **✅ CONSOLIDATED FIX committed `2c0c3ac1`** (worktree t504): all 10 gate findings resolved — scaffolding removed (readability clean), metadata re-authored, palette de-graded (teal/indigo/berry/gray, 0 grade-hex collisions, AA 6.7–8.5:1), 3 WCAG-AA contrast fixes, sectionEyebrow local override; axe-core 0 contrast violations; tsc/build 0.
  - **Orchestrator verification caught 2 residuals → last fix batch running (a6370daf resumed):** (a) RT-3 incomplete — a SECOND `ספף` typo at magnesium-guide-data.ts:404 was missed; (b) the **/madrichim HUB itself** used banned framing (page.tsx:59 metadata "לא דירוג" + line 82 body "מדורג") — the hub retiring rankings can't say "ranked". Both being fixed → then scoped Adversarial QA re-gate → owner review of the golden guide.
  - Fix agent also flagged (out-of-scope, noted): pre-existing aria-prohibited-attr on guide-product-row image div (a11y backlog); copy-doc mirror is untracked in main repo (not in worktree commit).
  - **✅ Residuals fixed `e06eb420`:** all `ספף` gone; /madrichim hub metadata + body de-ranked to threshold framing ("מדריך קנייה בודק אם מוצר עומד בספים קבועים…"); 0 banned words/antithesis/em-dash, is_clean, tsc/build 0.
  - **✅ FINAL re-gate GO (aed9a4b6) @ e06eb420 — magnesium guide TWO-GATE SATISFIED.** All 10 findings resolved+independently verified (palette contrast recomputed 6.7–8.5:1, hexes disjoint from grade colors, buckets 0/5/12/1 + buyUrl/pricing null×18 byte-identical, axe 0 color-contrast, tsc/build 0, both routes 200). Orchestrator render-verified the desktop screenshot: honest headline + "הרשימה המעשית" promoted shortlist (5) + fails (12) + cannot-assess (1) + education spine; RTL clean, no grades, dormant buy buttons. Screenshots → `tasks/returns/TASK-504B_final_screenshots/`.
  - **⚠️ 3 PRE-EXISTING carry-forwards for Wave 3 (before public flip, NOT delta-introduced):** NEW-A HIGH aria-prohibited-attr on product-thumbnail div (guide-product-row); NEW-B HIGH 2 contrast fails on /madrichim hub "coming soon" card (shared hashvaot-category-box: #5E6560/#D8D5CD 4.08:1, #7A817C 3.32:1); NEW-C MED /madrichim hub is indexable w/ no robots override (confirm posture). Fold into Wave-3 migration.
  - **→ AT OWNER REVIEW: golden magnesium guide** (format + grade-free bar palette). On approval → Wave 2 (creatine stamps template) → Wave 3 (hub + migration PR + carry-forward a11y fixes, owner merge).
- **Doc-hygiene owed → Nutrition (RT-7):** `supplement_guides_bar_rubric_companion_v1.md` §3 summary line says fails-10/cannot-3 but its own table + the page are correct at 12/1 — fix the summary line + TASK-504A counts. Non-blocking (page correct).

# TASK-504 — Supplements re-direction: kill supplement rankings, launch guides (madrichim) category

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
