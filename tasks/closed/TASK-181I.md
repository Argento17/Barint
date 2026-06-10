---
id: TASK-181I
title: Glass Box W4 Frontend and Design surface d3_processing_signal plus note_he on professional and consumer surface
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-04
completed_at: 2026-06-04
depends_on: [TASK-181G]
blocks: []
category_id: null
close_reason: >
  CC close-readiness gate PASS (2026-06-04). D3 processing-signal surfaced as a calm
  drilldown line behind NEXT_PUBLIC_GLASSBOX_W4 (default OFF), reusing the existing Glass Box
  presentation pattern; three states render (NOVA-1 positive / NOVA 3–4 hedged verbatim /
  low-conf muted-gold provisional) + Candidate C mobile-compressed variant; OFF visually
  unchanged (10/10 Playwright smoke); build/lint/tsc clean; owner preview at
  /dev/glass-box-preview. No score/grade/published-JSON touched, approved Hebrew rendered
  verbatim, flag not flipped. Independent of the medium-band rework — it renders whatever
  note_he the engine emits, so the reworked engine (181K) needs no display change unless it
  introduces a new note string (none planned). Closing.
roadmap_impact: true
work_type: frontend
cc_reviewed: 2026-06-04
cc_comments:
  - flag: fyi
    note: >
      CC gate PASS (2026-06-04). D3 processing-signal surfaced as a calm drilldown line in
      the existing ExpansionSection (same pattern as the D5 note / W2 AdditivePanel), behind
      new NEXT_PUBLIC_GLASSBOX_W4 (default OFF — verified in feature-flags.ts). Three states
      render (NOVA-1 positive / NOVA 3–4 hedged verbatim / low-conf muted-gold provisional);
      Candidate C mobile-compressed variant used <sm via CSS. OFF = visually unchanged
      (10/10 Playwright smoke, mobile+desktop); build/lint/tsc clean. No score/grade changed,
      no published comparison JSON touched, approved Hebrew rendered verbatim, flag not
      flipped. Owner preview at /dev/glass-box-preview with the flag on. CLOSEABLE — held for
      owner go. NOTE: independent of the 181H net-downward finding (this just renders whatever
      note the engine emits); but W4 GO-LIVE stays blocked on that finding + Nutrition sign-offs.
summary: >
  Surface the reframed D3 signal per the wave plan (W4 = consumer/professional surfaces / view-model). Render note_he (Candidate A positive / B negative-hedged / C low-confidence; C has a mobile-compressed variant per spec 3.3) as a calm drilldown footnote / professional-surface field; present confidence honestly. Behind the W4 flag; no live consumer exposure until owner go-live. Design owns the visual + confidence hierarchy.
---

# TASK-181I — Glass Box W4 Frontend and Design surface d3_processing_signal plus note_he on professional and consumer surface

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
