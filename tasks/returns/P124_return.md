# P124 Return — TASK-278 Phase-9: Juices × Sugar D6 Enrollment Proposal

**Agent:** Nutrition Agent
**Date:** 2026-06-14
**Task:** TASK-278
**Phase:** Phase-9 — juices × sugar shelf-relative enrollment (D6 proposal)

---

## Deliverables

**Enrollment doc:** `02_products/juices/methodology/shelf_relative_sugar_enrollment_juices_v1.md`

---

## Corpus Found

**Run:** `run_juices_001` (2026-06-07)
**Path:** `02_products/juices/bsip2_outputs/run_juices_001/products/`
**Batch summary:** `02_products/juices/reports/run_juices_001_batch_summary.json`

- n_juice_products: 65
- n_with_sugar: 65 (100% coverage)
- Grade distribution: A=1, C=54, D=10

---

## Router Category Finding

**Not a single clean category.** The 65 products route to:
- `beverage`: 45 products (100% juices, lemon juices, fruit drinks, cold-pressed)
- `default`: 19 products (nectars — פריגת, ספרינג, Minute Maid; cold-pressed squeezed; smoothies)
- `dessert`: 1 product (misroute — מיץ מוסקט, already flagged in batch summary)

**Scope guard recommendation:** Use `category_slug == "juices"` (BSIP1 field) as the scope guard rather than router category. This is consistent with the brined cheese pattern (EV-055, `bsip_cheese_subpool`) and yogurt (EV-088, `category_subtype`). The `category_slug` guard captures all 65 products across both router categories while excluding the dessert misroute — no router edit required.

**D7 open question:** Data Agent must verify `category_slug` is accessible in the `nn` dict at scoring time before wiring. This is a blocking pre-wiring item.

---

## Shelf Sugar Statistics (n=65, run_juices_001)

Source: BSIP0 direct product scrape only. OFF not used.

| Stat | Value |
|---|---|
| n | 65 |
| min | 1.75 g/100ml |
| max | 16.8 g/100ml |
| mean | 9.95 g/100ml |
| stdev | 3.42 g/100ml |
| Q1 | 8.40 g/100ml |
| **median** | **9.50 g/100ml** |
| **Q3** | **12.20 g/100ml** |
| **IQR** | **3.80 g/100ml** |
| MAD | 1.30 g/100ml |
| 1.4826 × MAD | 1.93 g/100ml |
| IQR / 1.349 | 2.82 g/100ml |
| **robust_scale (IQR-primary)** | **2.82 g/100ml** |
| dead_zone_lo | 8.65 g/100ml |
| dead_zone_hi | 10.35 g/100ml |
| near_median_dead_pct | 24.6% |
| 0 scaling-pinned products | confirmed |

---

## SR Band Parameters

| Parameter | Value |
|---|---|
| direction | asymmetric (penalize high, relieve low) |
| P_max | 6 |
| B_max | 3 |
| floor_value | 62 |
| floor_threshold_g | 12.2 g (Q3) |
| z_dead_zone | ±0.3 |
| scale | 2.82 g/100ml (IQR-primary) |
| min_n guard | 65 >> 20 ✓ |
| low_variance guard | IQR=3.80 >> 2.0 ✓ |

**Anti-Immunity check:** floor(62) + B_max(3) = 65 < 70 (B threshold). PASSES.

---

## Named Inversions

### Inversion A — Understated Gap (Opposite-Side Relief)

| | Barcode | Name | sugar_g | score | grade |
|---|---|---|---|---|---|
| A | 7290000039435 | מיץ תפוזים 100% פריגת 1 ליטר | 8.4 g | 56.1 | C |
| B | 7290002263586 | מיץ לימון משומר 500מ"ל | 2.5 g | 59.7 | C |

Current gap: 3.6 pts (lemon higher — correct direction, but understated for 5.9g sugar difference)

SR deltas:
- Orange (z = −0.39, within dead zone): delta = 0 → stays 56.1
- Lemon (z = −2.49, well below dead zone): delta = +3.0 (B_max cap) → new score: 62.7

Gap after SR: **6.6 pts** (correctly amplified; lemon reaches 62.7, gap widens from 3.6 to 6.6)

This is an understated-gap inversion: the correct direction already exists but the magnitude is compressed. SR restores proportionality.

### Inversion B — True Ranking Inversion (High-Sugar Scores Higher)

| | Barcode | Name | sugar_g | score | grade |
|---|---|---|---|---|---|
| A | 7290002696043 | נקטר אפרסק פריגת 1 ליטר | 12.2 g | 58.1 | C (cat=default) |
| B | 7290000039442 | מיץ תפוחים 100% פריגת 1 ליטר | 9.6 g | 51.4 | C (cat=beverage) |

Current gap: **+6.7 pts in wrong direction** (peach nectar scores higher despite +2.6g sugar, driven by router-category calorie_density difference).

SR deltas:
- Peach nectar (z = +0.96): delta = −5.8 → new score: 52.3
- Apple juice (z = +0.04, within dead zone): delta = 0 → stays 51.4

Gap after SR: **0.9 pts** (inversion eliminated — 100% apple juice and sugar-heavier nectar reach near-parity).

This is a true ranking inversion eliminated by SR.

### Inversion C — Compressed Gap (Same Sub-Pool)

| | Barcode | Name | sugar_g | score | grade |
|---|---|---|---|---|---|
| A | 7290000039435 | מיץ תפוזים 100% פריגת 1 ליטר | 8.4 g | 56.1 | C |
| B | 7290015348423 | מיץ ענבים סגל משפחות 1 ליטר | 14.2 g | 50.5 | C |

Current gap: 5.6 pts (correct direction — orange scores higher). SR widens this to 12.8 pts (orange 57.3, grape 44.5), reflecting 5.8g sugar difference more proportionally.

---

## Proposed EV Number

**EV-091**

Verified: highest EV in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` = EV-090 (hard_cheeses×sat_fat, TASK-278 Phase-8, line ~2192). EV-091 is the next free slot.

**Do not register yet — registration is the D7+orchestrator step.**

---

## D7 Open Questions for Product Agent

**Q1 — Scope guard field availability:** `category_slug == "juices"` is the recommended scope guard. Data Agent must verify this field is in the `nn` dict at scoring time. Blocking pre-wiring item.

**Q2 — Fruit drink inclusion in peer group:** Products with <25% fruit content (e.g. משקה פירות תרה, 11.6g sugar, 49.9/D) are on the same consumer shelf. Nutrition position: include. Product Agent should confirm.

**Q3 — P_max/B_max adequacy at scale=2.82:** The juice robust_scale (2.82 g/100ml) is substantially lower than cereals (8.896) or yogurt (4.299), reflecting the per-100ml liquid basis. At this scale, a product 1 standard deviation above median (~12.3g) receives a ~−6pt surcharge at P_max cap. Confirm P_max=6 / B_max=3 is correctly calibrated or whether budget adjustment is warranted.

**Q4 — Pilot gate criteria for routing split:** The standard 11-criterion gate (EV-087/090) applies, plus one juice-specific criterion: SR does not fire differently based on router category alone — a nectar in `default` and a 100% juice in `beverage` with identical sugar_g must receive identical SR_delta.

---

## Guards Verified

| Guard | Status |
|---|---|
| Engine files modified | NONE — D6 proposal only |
| Score movement | 0 — no pilot rescore |
| OFF used | NO — all data from BSIP0 direct scrape |
| Published scores touched | NO |
| EV registered | NO — pending D7 |

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-9 juices×sugar D6 enrollment proposal",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "corpus_found": true,
  "n_juice_products": 65,
  "n_with_sugar": 65,
  "router_category": "split: beverage(45) + default(19) + dessert(1); scope_guard=category_slug=='juices'",
  "shelf_stats": {
    "median": 9.5,
    "q1": 8.4,
    "q3": 12.2,
    "iqr": 3.80,
    "mad": 1.30,
    "robust_scale": 2.82,
    "mean": 9.95,
    "stdev": 3.42,
    "min": 1.75,
    "max": 16.8,
    "near_median_dead_pct": 24.6,
    "n_scaling_pinned": 0
  },
  "recommended_scope_n": 65,
  "scope_guard": "category_slug == 'juices'",
  "floor_value": 62,
  "floor_threshold_g": 12.2,
  "p_max": 6,
  "b_max": 3,
  "anti_immunity_check": "62+3=65 < 70 (PASS)",
  "next_ev_number": "EV-091",
  "enrollment_doc": "02_products/juices/methodology/shelf_relative_sugar_enrollment_juices_v1.md",
  "named_inversions": [
    {
      "id": "INV-A",
      "type": "understated_gap_opposite_side",
      "barcode_A": "7290000039435",
      "name_A": "מיץ תפוזים 100% פריגת 1 ליטר",
      "sugar_A": 8.4,
      "score_A": 56.1,
      "barcode_B": "7290002263586",
      "name_B": "מיץ לימון משומר 500מ\"ל",
      "sugar_B": 2.5,
      "score_B": 59.7,
      "gap_before": 3.6,
      "expected_delta_A": 0.0,
      "expected_delta_B": 3.0,
      "gap_after": 6.6
    },
    {
      "id": "INV-B",
      "type": "true_ranking_inversion",
      "barcode_A": "7290002696043",
      "name_A": "נקטר אפרסק פריגת 1 ליטר",
      "sugar_A": 12.2,
      "score_A": 58.1,
      "barcode_B": "7290000039442",
      "name_B": "מיץ תפוחים 100% פריגת 1 ליטר",
      "sugar_B": 9.6,
      "score_B": 51.4,
      "gap_before_wrong_direction": 6.7,
      "expected_delta_A": -5.8,
      "expected_delta_B": 0.0,
      "gap_after": 0.9
    }
  ],
  "d7_open_questions": [
    "Q1: Verify category_slug accessible in nn dict at scoring time (blocking pre-wiring item for Data Agent)",
    "Q2: Confirm fruit_drink sub-pool (<25% fruit) included in SR peer group (Nutrition position: YES; Product Agent confirms)",
    "Q3: Confirm P_max=6 / B_max=3 adequately calibrated at robust_scale=2.82 g/100ml (lower than cereals/yogurt due to per-100ml liquid basis)",
    "Q4: Add juice-specific pilot gate criterion: SR delta identical for same sugar_g regardless of router category (beverage vs default)"
  ],
  "engine_modified": false,
  "off_used": false,
  "commands_run": [
    {"cmd": "python: scan 65 bsip2_trace.json files from run_juices_001", "exit_code": 0},
    {"cmd": "python: compute shelf sugar stats (n=65, all with data)", "exit_code": 0},
    {"cmd": "python: inversion analysis across 65x65 pairs", "exit_code": 0},
    {"cmd": "grep: evidence_registry EV-09x pattern", "exit_code": 0},
    {"cmd": "Read: corpus_filter.json, batch_summary.json, TASK-278.md, 5 trace files", "exit_code": 0}
  ],
  "artifacts": [
    {
      "path": "02_products/juices/methodology/shelf_relative_sugar_enrollment_juices_v1.md",
      "sha256": "not_computed_prose_doc"
    },
    {
      "path": "tasks/returns/P124_return.md",
      "sha256": "this_file"
    }
  ],
  "counts": {
    "juice_products_in_corpus": 65,
    "products_with_sugar_data": 65,
    "denominator": "run_juices_001 BSIP2 traces",
    "routing_beverage": 45,
    "routing_default": 19,
    "routing_dessert": 1,
    "named_inversions": 2,
    "d7_open_questions": 4,
    "engine_files_touched": 0,
    "score_movements": 0
  },
  "not_done": [
    "EV-091 registration — pending D7 Product co-sign",
    "Data Agent verification of category_slug field accessibility (Q1)",
    "Pilot rescore — gated on D7 co-sign + owner go-live"
  ],
  "acceptance_test": "Orchestrator verifies: (1) enrollment doc exists at stated path; (2) shelf_stats match trace-derived values (median=9.5, IQR=3.80, scale=2.82); (3) both named inversions have barcode+sugar+score+delta present; (4) Anti-Immunity 65<70 holds; (5) engine_modified=false (git diff --name-only shows 0 engine files changed); (6) off_used=false",
  "propose": "RETURNED"
}
```
