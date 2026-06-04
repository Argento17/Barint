// Bari anonymous analytics — privacy-respecting event dispatcher.
//
// Privacy boundary (TASK-179R §3.4):
//   - No user ID, session ID, login state, or device fingerprint.
//   - No geographic location.
//   - No individual event sequences.
//   - Aggregate counts only — the raw event stream is not persisted.
//
// This module is the single dispatch point. To wire a real provider (Plausible,
// PostHog, Google Analytics), implement the provider and call it inside `fireEvent`.
// All calls in the UI should go through this module — never call a provider SDK
// directly from a component.
//
// Current state: console-only in dev; no-op in production until a provider is
// configured. Wiring a provider is a Data/Infrastructure task, not a Frontend task.

export type BariEventName =
  // Glass Box W2 additive panel engagement (TASK-179T / TASK-179R)
  | "additive_panel_open"
  | "additive_panel_close"
  | "tier_card_expand"
  | "tier_card_collapse"
  | "scroll_past_additive_panel"
  | "additive_panel_impression";

export type BariEventProperties = Record<string, string | number | boolean>;

/**
 * Fire a named event with optional properties.
 * Never include user identifiers — only aggregate, session-level signals.
 */
export function fireEvent(
  name: BariEventName,
  properties?: BariEventProperties
): void {
  if (process.env.NODE_ENV === "development") {
    console.debug("[bari:event]", name, properties ?? {});
  }

  // Provider hook — replace the body of this `if` block when wiring a real provider.
  // Example (Plausible):
  //   window.plausible?.(name, { props: properties });
  // Example (PostHog):
  //   posthog.capture(name, properties);
  // Example (GA4):
  //   window.gtag?.("event", name, properties);
  //
  // Until a provider is wired, events are silent in production.
}
