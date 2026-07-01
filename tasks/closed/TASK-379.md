---
id: TASK-379
title: Blog: sugar alcohols / maltitol in protein bars (research-backed explainer)
owner: content-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-22
depends_on: []
blocks: []
category_id: null
summary: >
  New /blog article on sugar alcohols (maltitol) in protein bars: the 'less sugar on the package' substitution trick, backed by real sources (EFSA polyol opinion, glycemic/GI-tolerance data) + charts + corpus product examples. Two-gate sign-off (Content + Adversarial QA). Build as draft/PR; go-live owner-gated.
---

# TASK-379 — Blog: sugar alcohols / maltitol in protein bars (research-backed explainer)

Origin: owner praised the maltitol paragraph in the protein-bar comparison and asked for a research-backed blog on the subject. Angle (owner-chosen): focused on sugar alcohols / the "פחות סוכר על האריזה" substitution trick. Format: another entry in the existing /blog system, creative structure.

## Status: DRAFT COMPLETE — both gates passed; awaiting owner review + deploy decision (go-live owner-gated)

Route: `/blog/sugar-alcohols` (draft, not deployed).

### Lane ledger
- **Research Agent** → evidence pack `02_products/snack_bars/sugar_alcohols_blog_evidence_v1.md` (12 sources, 14 figures verified, 3 flagged unverified → not shipped).
- **Nutrition Agent (D13)** → claim lock `02_products/snack_bars/sugar_alcohols_blog_nutrition_spec_v1.md` (8 publish-safe claims, 4 dropped/softened, erythritol-2023 cardiac signal ruled OMIT, Israeli warning = cite EU rule only, chart data from corpus).
- **Content Agent** → Hebrew copy `02_products/snack_bars/sugar_alcohols_blog_copy_v1.md` (39 strings; readability 39/39 clean, 0 naturalness HIGH, 0 out-of-locked-set claims).
- **Frontend Agent** → page built: `bari-web/src/app/blog/sugar-alcohols/page.tsx` + `components/blog/sugar-alcohols-article.tsx`, `-chart1.tsx`, `-chart2.tsx`; content lib `lib/blog/sugar-alcohols-article-content.ts`; registered in `blog-index-content.ts` + `sitemap.ts`. Build clean, 6/6 product images resolve (corpus Cloudinary, OFF=0).
- **Adversarial QA (two-gate #2)** → PASS-WITH-FINDINGS: 0 CRITICAL, 0 HIGH, 6 MEDIUM. Naturalness PASS (F1≥4, F2≥4 all consumer strings — independent judge). All 24 chart values match corpus.

### Findings dispositioned
- M-1 (spec stale id pb-011→pb-013): FIXED in nutrition spec.
- M-2 (S-32 omitted pb-010 artificial sweetener): FIXED + re-judged (F1=5/F2=4).
- M-4 (S-34 overstated causality "בדיוק"→"המרכזית"): FIXED + re-judged (F1=5/F2=5).
- New (caught in re-judge): S-34 falsely claimed pb-002's 17g was "highest sugar in group B" while pb-033=35g same group → FIXED (now contrasts vs the maltitol bars, factually true). tsc clean.
- M-3 (GI gloss in chart), M-6 (scoring-rationale depth): advisory, left by design (scope/clarity).
- M-5 (pre-existing ESLint in unrelated files): routed to frontend-agent, not this article.

### Phase 2 (owner-requested 2026-06-23) — credible embed + strong per-bar evidence
- **EFSA independent-source card** added (owner chose card-only, no video). EUFIC was REJECTED on red-team: it is food-industry-funded/governed (Coca-Cola/Nestlé/PepsiCo members) → conflicts with Bari's אי-תלות. Anchored instead to EFSA (independent EU regulator), link efsa.europa.eu/cs/efsajournal/pub/2076. Component `sugar-alcohols-efsa-card.tsx`.
- **Owner's "do producers disclose? how do we know if >10%?" question → researched + answered.** Polyol grams are voluntary disclosure (EU 1169/2011) BUT the >10% rule is self-disclosing via the on-pack warning. Per-bar direct-Shufersal-scrape check (`sugar_alcohols_polyol_pct_check_v1.md`): WIN front "1.7g sugar" → 27g/100g total polyols + legal warning CONFIRMED (>10%); אול אין 4.6g → 34.1g + warning CONFIRMED; פרו שטראוס 3.7g → 24g, warning NOT confirmed online (honest "unconfirmed" state on page). Verified Israeli warning wording "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת" (תקנות התשע"ח-2018) — closes the earlier unverified-IL-wording gap.
- **STRONG version (owner-approved):** new front-vs-back centerpiece `sugar-alcohols-front-vs-back.tsx` (S-47..S-51); catch section made actionable; S-28 caveat corrected; takeaway adds on-pack cues. Nutrition D13 v2 lock (`sugar_alcohols_blog_nutrition_spec_v2.md`).
- **Two-gate Phase 2:** gate caught + we fixed: EFSA editorial-inside-blockquote false attribution (CRITICAL), then a regulatory CRITICAL ("עם ממתיק" ≠ >10% polyol signal — it's the any-sweetener flag). FINAL re-gate **PASS — 0 CRITICAL / 0 HIGH**, naturalness 3/3, per-bar figures 3/3 match, OFF=0, health-claim 0.

### Phase 3 — GO-LIVE (owner "go live yes", 2026-06-23)
- Deploy topology RESOLVED in practice: bari.digital is served from the **`Argento17/bari` deploy repo** (remote `bari`), ROOT layout, NOT the Barint monorepo. Confirmed (existing /blog/shemen-zayit + /blog index serve from it).
- Migrated the article into the deploy repo via isolated worktree `C:\bari_deploy_379` (off `bari/main`; main tree untouched). Reconciled one schema divergence: deploy repo's `BlogArticleCard` has no `stat` field (removed it). **Builds GREEN** in the deploy repo (`npm run build` ✓, route prerendered static, lint 0 errors). Additive only (new route + index card + sitemap), no data files.
- **Pushed to deploy `main`** (fast-forward `0745ac0dc..720450f51`, no protection). Commit 720450f51 is the verified tip of `bari/main`.
- ⚠️ **NOT LIVE YET:** after ~8 min bari.digital still 404s on /blog/sugar-alcohols. No `vercel.json` in the repo → production deploy is controlled by Vercel **dashboard settings** (branch/auto-deploy/promote) that the orchestrator cannot see or trigger. Needs: check Vercel deployment for commit 720450f51 (building / failed / awaiting manual promote). Code is correct + builds; the gap is the Vercel publish trigger only.

### Phase 3 correction (2026-06-23): publish via `publish/*` + PR flow (owner-confirmed)
- Vercel auto-previews every branch; production publishes via a `publish/<topic>` branch + merged PR (pattern: `publish/magnesium-supplements` PR #21). Direct `main` push does NOT flip production.
- Corrected: rewound `bari/main` back to clean base `0745ac0dc` (force-with-lease; live site unchanged), pushed **`publish/sugar-alcohols`** (commit `720450f51`) for a clean PR + preview. Redundant `blog/*` branch deleted.
- PR to open/merge: https://github.com/Argento17/bari/pull/new/publish/sugar-alcohols  (owner merges → live; the one step the orchestrator can't do — no `gh`, no Vercel dashboard).

### Phase 3 FIX (2026-06-23): deploy was targeting the WRONG repo
- Root cause (from owner's Vercel Deployments screenshot): bari.digital Production deploys from **`origin` = Argento17/Barint (the monorepo) `master`** branch, NOT from Argento17/bari. Confirmed: origin/master tip `2b179c3b5` == top Production row. The `Argento17/bari` repo (remote `bari`) is the dead standalone repo — all my earlier pushes/PR there had no effect on the live site. Cleaned up (stray branch deleted; its main was restored).
- Correct publish done: worktree off `origin/master`; copied the 6 article files (monorepo layout); registered the article in master's **data-driven** `bari-web/src/data/blog/blog-index.json` (master moved the index to JSON — diverged from the task-374 hardcoded array) + `sitemap.ts`. Builds GREEN on master, `/blog/sugar-alcohols` prerendered static.
- **`publish/sugar-alcohols` pushed to origin (Barint).** PR: https://github.com/Argento17/Barint/pull/new/publish/sugar-alcohols → merge to `master` = Production deploy (same proven flow as `publish/magnesium-supplements` #20/#21).

### Status: CLOSED — LIVE on bari.digital/blog/sugar-alcohols (2026-06-23)
Owner merged PR #22 (publish/sugar-alcohols → master); Production deployed. Live render VERIFIED: front-vs-back (WIN 1.7g front → 27g sugar alcohols + bowel-activity warning), EFSA card, 4-polyol comparison, corrected takeaway ("עם ממתיק" = weak signal). HTTP 200, content correct, nothing broken. Merged worktrees cleaned up.
close_reason: Deliverable live + render-verified in production; two-gate passed (0 CRITICAL/0 HIGH); all per-bar figures source-traced; OFF=0. Deploy path corrected to origin(Barint)/master after initial mis-target of dead Argento17/bari repo.
