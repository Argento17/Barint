---
name: bari_comparison_template_v1
description: SUPERSEDED 2026-06-03 by comparison-template-standard-v1.md — original v1 comparison-page template; structure still valid, score chip now color-coded (Gen 1.1)
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Stabilized 2026-05-28. Replaces per-category architectural improvisation.

**SUPERSEDED 2026-06-03 (owner-approved consolidation).** The authoritative comparison template is now `C:\Bari\01_framework\frontend\comparison-template-standard-v1.md` (verified against live source; cites real components + the maadanim canonical reference; includes the Gen 1.1 color-coded chip). The old `comparison_template_v1.md` is now just a superseded stub — its unique conceptual material (Core Principle, copy rules, public-language rules, leakage/drift checklists, 8-step rollout workflow, governing principles) was folded into the standard as §20–26. The four-section structure + rules below still hold, EXCEPT the score-chip rule: the chip is now color-coded by grade (Gen 1.1: A=green / B=olive / C=gold / D=orange / E=red, via `gradePalette` in bari-comparison-tokens.ts) — the old "no color / no grade adjectives" is no longer current.

File (authoritative): `C:\Bari\01_framework\frontend\comparison-template-standard-v1.md`
File (superseded stub): `C:\Bari\01_framework\frontend\comparison_template_v1.md`

**Four-section structure (frozen):** Hero → Prologue → Product Table → Methodology. No additions permitted.

**Core principle:** "Someone carefully investigated this supermarket shelf for me." Not: "I am using food analytics software."

**Key rules:**
- Hero: compact, one sentence ≤12 words, score visible immediately (no animation), product packaging image only
- Prologue: 3–5 sentences hard limit, shelf observations only, no framework language, no bullet points
- Product table IS the main experience — rows are primary, everything else is support
- Collapsed row: image + name + score chip + one-line insight (≤12 words) + expand toggle ONLY
- Expanded row: nutrition 5-field + verbatim ingredients + data note + confidence state ONLY
- Highlighted comparison pair: ONE maximum, presented as table annotation (not narrative scene), optional — omit if no clear strongest pair
- Filters: collapsed by default, max 3 dimensions, single-select, Hebrew consumer labels (never framework terms)
- Methodology: 2–4 sentences, footer weight, no framework exposure

**Why:** Snack bar and מעדנים implementations both drifted toward dashboard/analytics register. This template freezes the restrained architecture.

**How to apply:** Follow content-generation workflow (8 steps) for each new category. Run leakage + drift checklists before launch. What changes per category: hero product, prologue, filter values, optional pair. What never changes: structure, row anatomy, language rules, drift-prevention rules.
