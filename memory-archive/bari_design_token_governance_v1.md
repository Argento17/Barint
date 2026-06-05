---
name: bari_design_token_governance_v1
description: "Design token governance rules — allowed categories, naming conventions, override rules, deprecation policy, additive review process, duplicate prevention, category-specific prohibition"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

File: `C:\Bari\01_framework\frontend\design_token_governance_v1.md`  
Token file: `src/lib/design/bari-comparison-tokens.ts`

**Why:** Prevent uncontrolled token proliferation as categories scale. Every token must earn its place.

**Allowed top-level categories (7):** rows, score, typography, layout*, methodology*, insightLine*, gradePalette†  
(* = must be added; † = deprecated/legacy only)

**3 missing token groups to add before canonical build:**
- `layout`: rowHeightMobile=72px, rowImageSize=56px, scoreChipSize=28px, heroMaxHeight=280px, heroImageHeight=160px
- `insightLine`: fontSize=13px, color=#444444
- `methodology`: fontSize=12px, color=#AAAAAA

**Naming rules:** camelCase, no abbreviations (background not bg), values as strings with units ("72px"), colors as 6-digit uppercase hex.

**Override rules:** canonical components must read from token file — no hardcoded duplicates. Legacy components exempt (read-only quarantine). Value requires a token when it must be consistent across multiple components or categories.

**Deprecated tokens (4):** gradePalette (all), score.hero.labelSize, score.hero.labelClass, score.comparisonChip — all stay in file for legacy compatibility, must not be used in new code.

**Category-specific prohibition:** no per-category token keys (breadRows, maadanimScoreSize), no editorial decisions as tokens, no conditional tokens (single value only — viewport variation = component logic with Tailwind prefixes).

**Additive review (5 checks):** used in >1 component? design decision? not already exists? permitted category? category-agnostic? All 5 must pass. No speculative tokens.

**Duplicate prevention:** grep for value before adding; if found in token file, use the token; if found hardcoded elsewhere, add token and fix both locations.

**Related:** [[bari_component_build_sequence_v1]] [[bari_architecture_generations_v1]] [[bari_legacy_isolation_v1]]
