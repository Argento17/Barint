(route: C3)

# P205 — C3 independent consult: OFF-eradication end-state + deep-cleanup line

You are an independent reviewer. You have NO repo access — all facts are below. Challenge the
reasoning; don't rubber-stamp. Two decisions need a second opinion before they're treated as final.

## Context (Bari = a food-scoring data/research monorepo + Next.js site at bari.digital)
- HARD RULE: Open Food Facts (OFF) is banned project-wide as a data source — every field, every
  category, forever. "Unknown is acceptable; OFF is not." Any OFF dependency is a launch blocker.
- This session: removed live OFF code from the BSIP0 scrape layer, merged 4 salvage branches to
  master, and is about to do a deep cleanup of "junk / stale / dormant" committed files.

## QUESTION 1 — Is the OFF-eradication END-STATE correct, or is there residual risk?
What was done in `03_operations/bsip0/scrape`:
- A *live* OFF fallback (`off.get_product()` populating nutrition+ingredients for empty-panel
  products, tagging provenance `off_api`) was DELETED from the Victory scraper → empty panels now
  stay NULL.
- 7 OFF-only / il_prices+OFF-hybrid scrapers were STUBBED with a module-level `raise RuntimeError`
  at import (carrefour_butter, yohananof_butter, yohananof_cheese×2, multiretailer_cereals×2, +
  yogurt stubs already present). The scraper *bodies* (dead code) were left below the raise.
- `shufersal_olive_oil`: removed only the OFF lookup branch; kept the il_gov_data identity source.
- LEFT IN PLACE on purpose: (a) `_shared/bsip0_gate.py` + `frozen_vegetables/05` retain OFF token
  strings as a *contamination DETECTOR* (they scan FOR off to reject it — not a data path);
  (b) `off_yogurt/raw/` ~60 cached OFF JSON files (raw provenance history, not read by live code);
  (c) the disabled OFF integration client `integrations/clients/open_food_facts.py`.

**Independent judgment needed:**
- Is "stub-with-raise + leave dead body below" defensible, or should OFF-only scrapers be DELETED
  outright (file removed) to eliminate any chance of someone deleting the raise and re-enabling?
- Is keeping ~60 cached OFF raw JSONs as "provenance" consistent with a hard ban, or is that
  exactly the kind of dormant OFF residue the rule wants gone? Same question for the disabled
  OFF client file.
- Any blind spot in defining "live OFF path" as "an OFF call reachable at runtime without hitting
  a raise first"? (e.g., a script that reads an OFF raw cache instead of calling the API.)

## QUESTION 2 — Where is the principled line for deleting "dormant" files in a research repo?
The owner directive: "clean C:\Bari from all the junk, stale and dormant files." Candidates include:
wiped/retired categories' lingering artifacts (butter, maadanim, olive_oil, old yogurts/salty-snacks
versions) — their BSIP0/BSIP1/BSIP2 run directories, superseded frontend JSON versions, bespoke
scripts — plus a retired `05_command_center/` subsystem and `_deprecated_off/` dead code.
Tension between two of the owner's own doctrines:
- "Systematic, not artisanal" + "missing-data-discard" + "delete is the default fallback" → delete aggressively.
- vs. research reproducibility / provenance / the ability to re-derive a score → preserve lineage.

**Independent judgment needed:**
- In a data/research monorepo that feeds a *published* scoring site, what's the right boundary
  between "dormant junk to delete" and "lineage/provenance to keep"? Propose a concrete test.
- Specifically: for a category that was REMOVED from the live site (page+route deleted), should its
  upstream BSIP run data + scored traces be deleted too, or archived (e.g., moved to an `_archive/`
  or a git tag) so the deletion is recoverable? Which is more defensible for a project whose
  credibility rests on traceable scores?
- What deletion would you consider IRREVERSIBLE and therefore gate behind a tag/branch first?

## Return format
For each question: your recommendation (pick one), the 2-3 strongest reasons, and the single
biggest risk if the team does the opposite. Flag anything in the framing above you think is wrong.
Evidence/reasoning only — you do not execute, approve, or close.
