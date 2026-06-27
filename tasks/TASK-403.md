---
id: TASK-403
title: E133 (Brilliant Blue) false EU-warning claim — additive registry data-accuracy
owner: data-agent
status: RETURNED
priority: MEDIUM
created_at: 2026-06-26
returned_at: 2026-06-27
depends_on: []
blocks: []
category_id: cereals
blocker: ""
dispatched: "2026-06-27 unattended orchestrate — native Data Agent (Sonnet), worktree-isolated."
orchestrator_verification: >
  RETURNED + orchestrator-VERIFIED 2026-06-27. Worktree agent-a9b4737962e4b80e8, branch
  worktree-agent-a9b4737962e4b80e8, commit 80f9b183. Verified: (1) worktree diff is ONLY
  cereals_frontend_v2.json (surgical); (2) E133 blast radius = exactly 1 live file / 1 product
  (Trix 7613030979647) — confirmed by grep across live comparisons (E133 absent from the W2
  canonical registry; the false text was baked into the cereals JSON, not registry-sourced as the
  finding assumed); (3) new E133 text at :1240 cites Reg. 1333/2008 Annex V, false
  EFSA-hyperactivity + mandatory-warning claim removed; (4) remaining warning string at :1254 is
  E110 (Sunset Yellow — genuinely Southampton Six), correctly LEFT untouched. Grounding solid
  (McCann 2007 PMID 17825405; six = E102/104/110/122/124/129; E133 excluded).
  NOT CLOSED: consumer-facing copy → needs the two-gate (Content + Adversarial QA) + owner deploy.
  PARKED for owner supervised morning. Low-risk (1-product factual correction).
summary: >
  E133 (Brilliant Blue) false EU-warning claim — additive registry data-accuracy
---

# TASK-403 — E133 (Brilliant Blue) false EU-warning claim — additive registry data-accuracy

## Finding (surfaced by the cereals naturalness gate, 2026-06-26)
The d4_additives dropdown text for **E133 (כחול מבריק / Brilliant Blue)** asserts:
> "ה-EFSA מצא קשר אפשרי להיפראקטיביות בילדים; מחויב בסימון אזהרה באירופה."

This is **factually wrong.** The EU "may have an adverse effect on activity and
attention in children" warning (Reg. 1333/2008 Annex V, post-Southampton-2007)
applies ONLY to the **Southampton Six**: E102, E104, E110, E122, E124, E129.
**E133 (Brilliant Blue FCF) is NOT on that list** and carries no such EU warning
requirement. (For contrast, E129 Allura Red and E110 Sunset Yellow on the same
טריקס product ARE on the list — their copy is correct; the cereals naturalness
copy "שניים מתוך שלושה מחייבים" is therefore CORRECT and was left unchanged.)

## Scope
- This text is almost certainly **registry-sourced** (shared additive dictionary /
  w2_additive_copy), so it likely repeats on **every live product that shows E133**,
  not just טריקס on cereals. Find the source of `explanation_he` for E133 and audit
  all shelves for the same false claim.
- Pre-existing on origin/master (NOT introduced by the TASK-374 voice passes; the
  cereals deploy `3d295c4c2` did not touch d4_additives — byte-identical to live).

## DoD
- Correct the E133 `explanation_he` at its source: remove the false "מחויב בסימון
  אזהרה באירופה" + the unsupported EFSA-hyperactivity claim; state accurately
  (synthetic blue dye; NOT subject to the EU Southampton attention warning).
  Ground the correction (Research/Nutrition) — cite the Southampton-Six list.
- Sweep every live d4_additives instance of E133 and re-deploy any product whose
  displayed dropdown text changes.
- Verify no OTHER additive carries a mis-attributed Southampton warning (audit the
  full registry against the canonical six while in there).
- Citation discipline: name the regulation (1333/2008 Annex V) in the corrected text.
