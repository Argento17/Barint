---
id: TASK-467
title: Share-page feature + Bari community social links (site-wide)
owner: frontend-agent
status: CLOSED
close_reason: >
  Full DoD live in production, orchestrator-verified against served HTML (cache-busted fetches 2026-07-02):
  (1) share button "שיתוף" in served HTML on /hashvaot/brined-cheeses + /blog/yogurt (PR #48 → 1cb61bed);
  (2) community block live on homepage — "הקהילות של ברי" heading + all 3 owner links (WhatsApp Channel
  0029VbDGpnr7j6g4xM62910s / instagram.com/bari_nutrition / facebook profile 61591403370117) present in
  served HTML (PR #49 → 06f85de4, recovered the merge-race commit a9fbb86e);
  (3) comparison og:image emitted + resolving 200 image/webp (was absent entirely pre-task);
  (4) two-gate sign-off complete on all consumer strings (Content P477/P480 + Adversarial QA P478/P481
  GO_WITH_FIXES, all findings independently reproduced resolved); QA screenshots a–f in
  tasks/returns/TASK-467_qa_screenshots/. Residual follow-up routed to Design: 1200×630 og share image.
priority: HIGH
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: null
summary: >
  Add premium share-this-page affordance (native share + fallback) to comparison/blog pages and Bari community links (Instagram/Facebook/WhatsApp groups) in footer+header. Research-informed (best-practice scan), two-gate copy sign-off, GA4 events, OG image fix prerequisite. Blocked on owner group links for footer rollout.
---

# TASK-467 — Share-page feature + Bari community social links (site-wide)

## Status — 2026-07-02: OWNER PR OPEN, awaiting owner merge (tripwire 2)
- **PR #48: https://github.com/Argento17/Barint/pull/48** — branch `feat/task467-share-community` (11 commits, worktree C:\bari_wt_t467 off origin/master da637dca).
- Chain: research (P475, 7/7 questions, 8 sites primary-verified) → build (P476: 18/18 comparison + 10/11 blog + footer + mobile menu; tsc/build/lint/e2e 0) → Content gate 1 GO_WITH_FIXES (P477: share template rewritten `בדיקת X של ברי`→`ברי בדקה: X`, ungrammatical at 13/13 call sites) → Adversarial QA gate 2 NO_GO (P478: CRIT fallback menu unpaintable in comparison-card overflow-hidden + HIGH olive-oil 156ch share title + MED pre-consent dataLayer push) → fix round (P479: portal to body / shareTitle prop / consent gate, commits c2f150c0/19070a00/bedcbe8b) → dual re-gate (P480 Content FIXED olive-oil shareTitle `מה באמת קובע איכות בשמן זית` — overclaim caught; P481 QA GO_WITH_FIXES, all findings independently reproduced resolved, 1 new MED left-edge clip) → clamp fix (P482, c49a49a8, blog menu x=8 in-bounds, desktop alignment diff 0px).
- Two-gate sign-off COMPLETE on all consumer strings. QA screenshots: `tasks/returns/TASK-467_qa_screenshots/` (a–f).
- **✅ Community links LANDED (a9fbb86e, pushed to PR #48):** owner supplied 2026-07-02 — WhatsApp **Channel** (0029VbDGpnr7j6g4xM62910s; matches the research advisory), Instagram bari_nutrition, Facebook page 61591403370117. Build-verified: all 3 hrefs + "הקהילות של ברי" heading present in rendered homepage HTML (.next/server/app/index.html); tsc+build exit 0. Footer + mobile-menu block now ACTIVE on the branch.
- **✅ PR #48 MERGED (1cb61bed), production-verified:** share button "שיתוף" live in served HTML on /hashvaot/brined-cheeses AND /blog/yogurt (cache-busted fetch); comparison-page og:image now present (was missing entirely) w/ explicit 512×512 dims, asset resolves 200 image/webp.
- **⚠️ MERGE RACE (raised to owner immediately):** PR #48 merged at head c49a49a8 — the community-links commit a9fbb86e was pushed seconds before the merge click processed and was LEFT OUT of the merge (verified via API: head-at-merge c49a49a8; merge-base ancestor check exit 1). Production correctly shows NO community block (safe-hidden, not broken). **Recovery: PR #49 opened with exactly that 1 commit — https://github.com/Argento17/Barint/pull/49 — awaiting owner merge.** Task stays IN_PROGRESS until #49 is live + production-verified.
- **Follow-ups routed:** Design — dedicated 1200×630 ≤300KB og share image (current 512×512 works, suboptimal WhatsApp card); stale `.webp` logo refs on the MAIN tree (layout.tsx:44 / bari-brand-logo.tsx:49 / site-structured-data.tsx:21 vs uncommitted png swap) belong to the sibling logo-swap session — NOT part of this branch (consistent at origin/master).
