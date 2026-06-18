// Bari frontend feature flags. Read once, statically, from build-time env so the
// flag can be statically inlined and tree-shaken.
//
// NEXT_PUBLIC_GLASSBOX_D5D6 — Glass Box W1 (D5/D6). SHIPPED 2026-06-04 (TASK-179, owner go-live).
// Default ON. Gates the Glass Box D5/D6 consumer presentation (the `ניתוח חלקי` demote flag +
// the `לא נוקד` withhold state + the plain-language disclosure note) on pilot pages
// (hummus + maadanim). Rollback: set NEXT_PUBLIC_GLASSBOX_D5D6=off in the hosting env.
export const GLASSBOX_D5D6_ON =
  process.env.NEXT_PUBLIC_GLASSBOX_D5D6?.toLowerCase() !== "off";

// NEXT_PUBLIC_GLASSBOX_W4 — Glass Box W4 (D3 de-moralization). SHIPPED 2026-06-05 (TASK-181S, owner go-live).
// Default ON. Gates the consumer presentation of the engine's `d3_processing_signal`
// (the D3 processing drilldown line on hummus + maadanim). ~13 grade moves live.
// Rollback: set NEXT_PUBLIC_GLASSBOX_W4=off in the hosting env.
export const GLASSBOX_W4_ON =
  process.env.NEXT_PUBLIC_GLASSBOX_W4?.toLowerCase() !== "off";

// NEXT_PUBLIC_GLASSBOX_W5 — Glass Box W5 (consumer launch). SHIPPED 2026-06-05 (TASK-181S, owner go-live).
// Default ON. Gates: (1) the /research/glass-box methodology page,
// (2) the inline "פירוט המתודולוגיה" link in the MethodologyFooter on hummus + maadanim.
// Rollback: set NEXT_PUBLIC_GLASSBOX_W5=off in the hosting env.
export const GLASSBOX_W5_ON =
  process.env.NEXT_PUBLIC_GLASSBOX_W5?.toLowerCase() !== "off";
