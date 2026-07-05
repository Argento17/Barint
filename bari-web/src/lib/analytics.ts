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
//
// Consent gate (TASK-467 RT-3): ga4-script.tsx installs the `window.gtag` stub
// unconditionally on mount (before any user consent choice, so Consent Mode v2
// defaults can be pushed). That means `typeof window.gtag === "function"` is
// true pre-consent too — checking only that would let a pre-consent event push
// into the local dataLayer. `getStoredConsent().analytics` is the single source
// of truth for "has the user actually granted analytics consent" (same read
// ga4-script.tsx and consent-manager.tsx use) — gated here so every caller of
// fireEvent is protected without each call site re-implementing the check.

import { getStoredConsent } from "@/lib/consent";

export type BariEventName =
  // Glass Box W2 additive panel engagement (TASK-179T / TASK-179R)
  | "additive_panel_open"
  | "additive_panel_close"
  | "tier_card_expand"
  | "tier_card_collapse"
  | "scroll_past_additive_panel"
  | "additive_panel_impression"
  // Share-page feature (TASK-467). `properties` carries { method, page_path }.
  | "share"
  // Newsletter — fired ONLY on a confirmed-successful API response (result.ok
  // === true), never on form_start/click. Distinguishes a real signup from
  // GA4 Enhanced Measurement's auto-detected `form_submit`, which is known to
  // be unreliable for forms that call preventDefault() + fetch() instead of
  // a native submit/navigation (this form's pattern) — see newsletter-signup.tsx.
  | "newsletter_signup";

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

  // GA4 provider (consent-gated). `window.gtag` is installed as a stub on mount
  // regardless of consent (see ga4-script.tsx), so its presence alone does not
  // mean consent was granted — the stored consent record is the real gate.
  if (
    typeof window !== "undefined" &&
    typeof window.gtag === "function" &&
    getStoredConsent()?.analytics === true
  ) {
    window.gtag("event", name, properties ?? {});
  }

  // Other providers (Plausible/PostHog) can be wired here following the same
  // consent-gated, optional-chained pattern. Until then they stay silent.
}
