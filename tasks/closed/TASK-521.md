---
id: TASK-521
title: Launch /news (חדשות) section + first piece: shelved poultry-industry report
owner: orchestrator
status: CLOSED
priority: MEDIUM
created_at: 2026-07-08
closed_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
close_reason: >
  Shipped to live (origin/master @ 89b164d5, clean fast-forward from 22163fda). /news + /news/of-poultry-report live; חדשות appended to nav (השוואות·קטלוג·בלוג·מדריכים·חדשות — מדריכים preserved, additive only, verified via nav screenshot). Both mandatory gates passed: Content Agent authored + Adversarial QA/Red-Team PASS (zero CRITICAL/HIGH on final re-gate). Facts independently verified against primary sources (OECD-FAO, USDA/FSA/CDC/WHO/EFSA, plus Knesset MMM, PRTR 2024, Berman et al. 2023); owner-supplied AI research reports re-verified before citing (caught a Pakistani-data misattribution). Red-Team caught + closed a legal-misattribution (leak wrongly pinned on named co-authors). Sitemap updated, RSS untouched. Built green against live code in an isolated worktree; main tree untouched.
summary: >
  New standalone /news section (in nav) + first honest-broker piece on the shelved Ministry of Environmental Protection poultry report (ynet/Shomrim). Two-gate copy (Content + Adversarial QA). Facts independently verified; contested numbers flagged, not amplified.
---

# TASK-521 — Launch /news (חדשות) section + first piece: shelved poultry-industry report

Shipped 2026-07-08. Honest-broker fact-check format (claims-audit: מאומת/שנוי במחלוקת/לא אומת per-claim chips + inline sources) is the reusable template for future news pieces. See memory `news_section_launch`.
