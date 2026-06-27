---
id: TASK-403
title: E133 (Brilliant Blue) false EU-warning claim — additive registry data-accuracy
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-26
depends_on: []
blocks: []
category_id: null
blocker: ""
dispatched: "2026-06-27 unattended orchestrate — native Data Agent (Sonnet), worktree-isolated, ground+audit+fix-at-source, NO deploy. Deploy + two-gate parked for owner supervised morning."
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
