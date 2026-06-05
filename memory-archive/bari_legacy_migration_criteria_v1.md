---
name: bari_legacy_migration_criteria_v1
description: "Legacy migration criteria — 5 mandatory triggers (mobile auto-fail, ontology leakage, component incompatibility, major redesign, dashboard drift) + 3 elective triggers + leave-as-is conditions + decision matrix"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

File: `C:\Bari\01_framework\frontend\legacy_migration_criteria_v1.md`

**Why:** Separates triggers (when migration is considered) from eligibility (when migration is permitted, defined in legacy_isolation_policy_v1.md). A trigger enters the queue; eligibility determines whether it proceeds.

**5 mandatory triggers (migration required):**
1. Mobile auto-fail condition (any of the 10, newly triggered — not pre-existing)
2. Ontology leakage escalation (new framework term in consumer content from data/pipeline change)
3. Component incompatibility (canonical shared component cannot compose into legacy page without destructive change)
4. Major redesign (structural change to layout, interaction model, or filter architecture)
5. Dashboard drift event (new Gen 0 pattern added to legacy page post-original-build)

**3 elective triggers (migration eligible, not required):**
6. Filter rewrite (cannot be done additively)
7. Major content refresh (data adapter rebuild required)
8. Canonical precedent established (מעדנים live — opens eligibility gate #1)

**Leave-as-is conditions:** no mandatory trigger present; מעדנים not live; active editorial update in progress; debt predates canonical spec; routing change required; migration scope unbounded; only active page for category.

**Decision matrix:** mandatory trigger + eligibility met = migrate; mandatory trigger + eligibility not met = block additive changes + work toward eligibility (exception: ontology leakage hotfix permitted for specific leaked term only).

**Migration is NOT:** redesigning editorial content, changing URL, refactoring pipeline, incremental evolution. One output: canonical components + geometry checklist pass.

**Related:** [[bari_legacy_isolation_v1]] [[bari_architecture_generations_v1]] [[bari_frontend_integration_v1]]
