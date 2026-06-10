---
id: TASK-181S
title: "Glass Box W5 Owner go-live gate: flip BARI_GLASSBOX_W4 + NEXT_PUBLIC_GLASSBOX_W4 + NEXT_PUBLIC_GLASSBOX_W5"
owner: owner
status: CLOSED
priority: HIGH
created_at: 2026-06-05
completed_at: 2026-06-05
depends_on: [TASK-181Q, TASK-181R]
blocks: []
category_id: null
roadmap_impact: true
work_type: objective
tripwire: "1 — consumer-facing irreversible grade moves (17 grade changes on hummus + maadanim)"
pre_authorized: true
pre_auth_condition: "TASK-181Q passes CC gate + all W5 content is live and verified; owner flips the flags"
cc_reviewed: 2026-06-05
close_reason: >
  CC close-readiness gate PASS (2026-06-05). Owner issued go-live (tripwire #1 pre-authorized
  2026-06-04). All pre-flip checklist items satisfied before flags were flipped:
  (1) 181Q CLOSED + CC gate PASS; (2) OFF parity verified 9/9 (181Q); (3) EV-042
  governing_principle row added (Nutrition Agent, pull-to-neutral framing, 2026-06-05);
  (4) EVIDENCE-GAP 4 filed in evidence registry Section E (Nutrition Agent, 2026-06-05);
  (5) W4 JSONs regenerated — hummus_frontend_v5.json (13 grade changes, 100% d3 coverage)
  + maadanim_frontend_v3.json (1 grade change, 100% d3 coverage) — build/tsc clean;
  imports updated. Three flags flipped atomically: BARI_GLASSBOX_W4 (engine default ON),
  NEXT_PUBLIC_GLASSBOX_W4 (frontend default ON), NEXT_PUBLIC_GLASSBOX_W5 (frontend default ON).
  Date placeholder in /research/glass-box updated to 5 ביוני 2026. Glass Box is live.
cc_comments:
  - flag: fyi
    note: >
      Actual grade moves at go-live: hummus 13 (1 A→B, 12 B→C), maadanim 1 (D→E).
      Total 14 vs. estimated 17. Delta explained: RECAL_P0=on baseline for hummus v4/v5
      had already moved some products away from the B/C boundary where W4 previously
      triggered crossings. Count is accurate and consistent with the QA reports.
  - flag: fyi
    note: >
      Research verification of 4 cited papers in glass_box_technical_methodology_v1.md
      (Monteiro 2019, Srour 2020 BMJ, IARC 2020, Chassaing 2021 / Bhattacharyya) is
      a pre-DISTRIBUTION gate for the NDA packet — not a go-live gate. Dispatch
      Research Agent before sharing the packet externally.
  - flag: fyi
    note: >
      EV-035–039 (D5/D6 evidence entries) are still in Draft pending Product D7 co-sign.
      Pre-existing state. Required before any future D5/D6 rule changes, not for this launch.
  - flag: fyi
    note: >
      D4 score-integration remains deferred — annotate-only is the current design.
      Future owner gate (tripwire #1) required to change this.
---

# TASK-181S — Glass Box W5: Owner go-live gate

Part of **TASK-181** (Glass Box program-of-record), Wave 5 — the consumer launch wave.

## This is the go-live tripwire

This task is the **owner's call** — tripwire #1 (consumer-facing irreversible grade moves). The owner pre-authorized the conditional on 2026-06-04 ("owner GO for W4 go-live is authorized CONDITIONAL on 181M landing + re-validation passing"). All conditions are now met.

**181S does not open until 181Q returns and passes the CC gate.** 181R is already CLOSED.

## What ships in this gate

When the owner executes, three flags flip simultaneously:

1. **`BARI_GLASSBOX_W4`** (engine) → default ON — activates the D3 de-moralization reframe (material/non-material split, HP de-amplification). Results in ~17 grade moves on hummus + maadanim (net-downward, all honest).
2. **`NEXT_PUBLIC_GLASSBOX_W4`** (frontend) → default ON — surfaces the D3 processing signal in the consumer drilldown on hummus + maadanim.
3. **`NEXT_PUBLIC_GLASSBOX_W5`** (frontend) → default ON — makes the `/research/glass-box` methodology page live and activates the MethodologyFooter "פירוט המתודולוגיה" links on hummus + maadanim.

The banked per-page methodology notes (TASK-181N) ship at the same time — Frontend wires them alongside the flip.

## What is already banked and ready

- **W4 engine**: TASK-181F–181M — CLOSED. Built, QA-verified, OFF-byte-identical. 17-down/3-up impact confirmed. F3 gate-guard live.
- **W4 frontend display**: TASK-181I — CLOSED. D3 drilldown line built behind the flag.
- **Per-page methodology notes**: TASK-181N — CLOSED/BANKED. Hebrew copy (hummus + maadanim variants) ready.
- **W5 methodology page copy**: TASK-181O — CLOSED. `methodology_glass_box_page_v1.md` ready.
- **W5 UX spec**: TASK-181P — CLOSED. `methodology_page_ux_spec_v1.md` ready.
- **W5 technical packet**: TASK-181R — CLOSED. `glass_box_technical_methodology_v1.md` ready (NDA/partners; Research verification recommended before distribution).
- **W5 frontend build**: TASK-181Q — IN_PROGRESS.

## Pre-flip checklist (CC executes at go-live)

Before confirming to the owner that the flip is ready:

- [ ] 181Q CLOSED (CC gate PASS)
- [ ] `NEXT_PUBLIC_GLASSBOX_W5=true` renders methodology page at expected route; 181N notes link to it
- [ ] OFF parity re-confirmed on the live build (not just dev)
- [ ] EV-042 "less punitive" → "pull-to-neutral in both directions" reword is in the registry (per Nutrition/Product finding from W4 review)
- [ ] EVIDENCE-GAP 4 (HP×WFI) logged in evidence registry (per 181R cc_comment)
- [ ] Research verification of 181R cited papers complete before packet is distributed externally (separate gate from go-live)

## Product "no silent flip" condition — fulfilled

The no-silent-flip condition (Product, W4 review) is met by:
- The banked per-page notes (181N) naming the fat+salt driver
- The public methodology page (181O) carrying the full "non-silent flip" narrative
- All three shipping simultaneously with the flag flips

## Post-flip

After go-live, the Glass Box program-of-record (TASK-181) umbrella can be closed. The ongoing obligations are:
- D4 maintenance cadence (annual + quarterly + 6 trigger events) per `additive_library_maintenance_protocol_v1.md`
- HP×WFI watch-item monitoring (EVIDENCE-GAP 4)
- EV-035–039 Product D7 co-sign completion (pre-existing pending; needed for any future D5/D6 rule changes)
- D4 score-integration decision deferred to future owner gate (tripwire #1)
