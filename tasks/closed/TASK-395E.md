---
id: TASK-395E
title: De-chain baseline provenance repair (7 non-reproducing live categories + 3 uncovered)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-26
closed_at: 2026-07-01
depends_on: []
blocks: []
close_reason: >
  SUBSUMED by TASK-409's landed repro commit series (2026-07-01 reconciliation). The provenance
  repair for all 7 non-reproducing + 3 uncovered categories (bread/cakes D4, cereals/hard_cheeses/
  juices drift-pin, granola v1->v2 pointer, snacks re-pin to task362, chocolate-bars/tablets/
  protein-bars provenance) landed on origin as the repro commits (24dda6ccf, 931db01af, 5900cbb77,
  69f046a6d, d7c574f7f, e51db8d11, 7850a054a, c554c5e63) + merged PRs #30/#31/#32. Local ==
  origin (0/0). The forward C0 round-trip gate this backlink mentions is TASK-395F's scope (still
  open). No independent score-move introduced.
backlink: "BACKWARD REPAIR DELIVERED by TASK-406 (2026-06-26): provenance_manifest.json persisted (15 live files, resolved run_id+flag vector+source+status), BARI_D4_SCORE_V1 added to MANAGED_BARI_VARS in rescore_all.py+baseline_verify.py. REMAINING (de-chain chat): forward C0 round-trip gate + re-shadow; documented gaps (NULL _meta run_id resolvable from config; granola/protein config->served v1/v2 mismatch; stale cookies bsip1_dir)."
category_id: null
summary: >
  Reproducibility map (2026-06-26) found 5/12 live categories reproduce published scores exactly; 7 need repair before they can be shadowed. Dominant cause: D4 additive patch (BARI_D4_SCORE_V1, commit 361748722) applied to live files but never recorded in configs nor rescore_all MANAGED_BARI_VARS. Repairs: bread/cakes add D4=on + resolve 1-2 residual; cereals/hard_cheeses/juices pin the ~+-2 non-D4 post-publish drift (suspect b3319fede); granola fix baseline pointer v1->v2 (route serves v2, config/manifest say v1); snacks re-pin corpus to task362 build (only 12/21 overlap). Uncovered: chocolate-bars/tablets/protein-bars have live routes but no manifest/config (~106 products). NEVER override a mismatch.
---

# TASK-395E — De-chain baseline provenance repair (7 non-reproducing live categories + 3 uncovered)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
