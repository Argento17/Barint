---
id: TASK-469
title: Community band in footer (TASK-467 visibility follow-up)
owner: frontend-agent
status: CLOSED
close_reason: >
  Live in production, orchestrator-verified against served HTML (cache-busted, 2026-07-03): community
  band renders on homepage — heading "רוצים להישאר מעודכנים?", subline "עקבו אחרי ברי...", WhatsApp CTA
  "הצטרפו בוואטסאפ" linking the Channel (0029VbDGpnr7j6g4xM62910s) all present. PR #52 merged (62eb5319).
  Deliverable: footer-top invitation band replacing the fine-print row (owner: prior links "really not
  visible enough"); WhatsApp filled-primary #167A58 (4.94:1 AA), IG/FB 44px circular icon buttons,
  right-aligned to footer convention (RTL), graceful-empty preserved. Gates: Content GO_WITH_FIXES
  (reframed one-way-Channel overclaim to honest follow/updates) + Design vision-critic GO_WITH_FIXES
  (0 CRIT/0 contrast fail; desktop association + 44px tap targets fixed; orchestrator caught+fixed an RTL
  justify regression). Diff = home-footer.tsx only; 0 data/score/product-copy touched. Screenshots in
  tasks/returns/TASK-469_screenshots/. Follow-up routed to Design: declare #167A58 CTA green as a token
  (pre-existing cross-component drift, out of scope here).
priority: HIGH
created_at: 2026-07-03
depends_on: []
blocks: []
category_id: null
summary: >
  Owner feedback: shipped community links read as legal fine print. Replace thin footer icon-row with a distinct community CTA band at footer top: invitation line + WhatsApp filled-primary button + Instagram/Facebook icon buttons. Owner chose 'community band' prominence level. New copy => two-gate; vision-grounded Design critic pass; render screenshots for owner before PR.
---

# TASK-469 — Community band in footer (TASK-467 visibility follow-up)

## Status — 2026-07-03: OWNER PR OPEN, awaiting inspection + merge
- **PR #52: https://github.com/Argento17/Barint/pull/52** — branch `feat/task469-community-band` (4 commits, worktree C:\bari_wt_t469 off origin/master @ 8dac7c2f). Diff = `home-footer.tsx` only.
- Trigger: owner said the TASK-467 community links were "really not visible enough" (read as legal fine print). Owner picked "community band" prominence (AskUserQuestion, over modest-chips / header-persistent).
- Chain: build (P483: footer-top invitation band, WhatsApp filled-primary #167A58 4.94:1 AA, IG/FB circular icon buttons, graceful-empty preserved) → Content gate 1 GO_WITH_FIXES (P484, a4c347c0: reframed "conversation"/"community" overclaim — WA link is a one-way Channel — to honest `רוצים להישאר מעודכנים?` / `עקבו אחרי ברי...`) → Design vision-grounded critic GO_WITH_FIXES (P485: 0 CRIT/0 contrast fail; flagged H1 desktop heading/button ~700px split + M1 40px tap targets) → fixes (P486, 29c0419b: justify-end+gap-10 assoc + size-11 44px) → orchestrator caught RTL regression (justify-end packs LEFT in RTL → band mis-aligned vs right-aligned footer siblings) → align fix (P487, 870329f4: justify-start, right-edge alignment verified in render at 1280/1440).
- Copy two-gate: Content GO_WITH_FIXES applied. (Design served as gate 2 here — visual/layout deliverable, no new data/score claims; Adversarial QA not required for a footer-chrome copy set already Content-signed + Design-verified.)
- Screenshots: tasks/returns/TASK-469_screenshots/ (band_desktop, band_desktop_1440, band_mobile, band_whatsapp_hover) — all final copy + fixes.
- **Pending owner:** inspect (Vercel branch preview on PR #52) + merge (tripwire 2).
- **Follow-up routed (non-blocking):** Design token-governance — `#167A58` filled-CTA green is an undeclared token shared across home-footer/newsletter-signup/home-final-cta (pre-existing drift; declare `--bari-green-cta` or migrate). Separate token task.
