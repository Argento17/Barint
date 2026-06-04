// Bari frontend feature flags. Read once, statically, from build-time env so the
// flag can be statically inlined and tree-shaken.
//
// NEXT_PUBLIC_GLASSBOX_D5D6 — Glass Box W1 (D5/D6). SHIPPED 2026-06-04 (TASK-179, owner go-live).
// Default ON. Gates the Glass Box D5/D6 consumer presentation (the `ניתוח חלקי` demote flag +
// the `לא נוקד` withhold state + the plain-language disclosure note) on pilot pages
// (hummus + maadanim). Rollback: set NEXT_PUBLIC_GLASSBOX_D5D6=off in the hosting env.
export const GLASSBOX_D5D6_ON =
  process.env.NEXT_PUBLIC_GLASSBOX_D5D6?.toLowerCase() !== "off";

// NEXT_PUBLIC_GLASSBOX_W4 — Glass Box W4 (D3 de-moralization). DEFAULT OFF (TASK-181I).
// Gates the consumer/professional presentation of the engine's `d3_processing_signal` —
// the calm "how processed is this food" drilldown line (note_he / note_he_mobile). With
// the flag OFF the comparison pages are visually IDENTICAL to today (no D3 surface). The
// live flip to ON is a separate frozen-invariant owner go-live decision (W4 moves grades).
// Enable in the hosting env with NEXT_PUBLIC_GLASSBOX_W4=on.
export const GLASSBOX_W4_ON =
  process.env.NEXT_PUBLIC_GLASSBOX_W4?.toLowerCase() === "on";
