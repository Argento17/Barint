// Bari frontend feature flags. Read once, statically, from build-time env so the
// flag can be statically inlined and tree-shaken. Default OFF for every flag.
//
// NEXT_PUBLIC_GLASSBOX_D5D6 — TASK-179I Wave 1. Gates the Glass Box D5/D6 consumer
// presentation (the `ניתוח חלקי` demote flag + the `לא נוקד` withhold state + the
// plain-language disclosure note). OFF (default) → the comparison UI is byte-identical
// to today. This flag controls PRESENTATION ONLY; it never touches a live score or the
// published comparison JSON, and it does not flip anything live — it exists so the owner
// can SEE the glass-box surface before a go-live decision.
//
// Set to "on" to enable (anything else, incl. unset, is OFF).
export const GLASSBOX_D5D6_ON =
  process.env.NEXT_PUBLIC_GLASSBOX_D5D6?.toLowerCase() === "on";
