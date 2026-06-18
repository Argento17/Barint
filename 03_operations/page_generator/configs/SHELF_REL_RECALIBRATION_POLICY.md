# Shelf-relative recalibration policy

Bari uses a **hybrid shelf-relative policy**: new products are scored against the **pinned baseline** (`scoring.shelf_rel` median/scale values in each category config). Those stats are frozen at calibration time and are not recomputed automatically when the corpus grows or shrinks.

**Recalibration** (updating median/scale) happens only via an explicit review: produce a before/after movement report (rescore_all or shadow diff), review product-level grade changes, and publish updated stats only after approval. The conformance gate warns (SOFT-12) when live corpus size drifts more than 25% from a recorded `shelf_rel.calibration_n` — it does not change scores.
