// Bari frontend feature flags. Read once, statically, from build-time env so the
// flag can be statically inlined and tree-shaken.
//
// NEXT_PUBLIC_GLASSBOX_D5D6 — Glass Box W1 (D5/D6). SHIPPED 2026-06-04 (TASK-179, owner go-live).
// Default ON. Gates the Glass Box D5/D6 consumer presentation (the `ניתוח חלקי` demote flag +
// the `לא נוקד` withhold state + the plain-language disclosure note) on pilot pages
// (hummus + maadanim). Rollback: set NEXT_PUBLIC_GLASSBOX_D5D6=off in the hosting env.
export const GLASSBOX_D5D6_ON =
  process.env.NEXT_PUBLIC_GLASSBOX_D5D6?.toLowerCase() !== "off";
