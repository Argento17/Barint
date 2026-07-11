"use client";

/**
 * GA4 consent-gated loader (strict opt-in posture).
 *
 * Sequence:
 *  1. On mount: initialise dataLayer + a *canonical* gtag stub (pushes the
 *     `arguments` object, which is what gtag.js expects when it later drains the
 *     queue — pushing a plain array silently breaks command processing) and set
 *     Consent Mode v2 defaults to denied. No gtag.js, no cookies yet.
 *  2. Read stored consent; subscribe to future CMP changes.
 *  3. Only once analytics consent is granted is the GA4 <Script> injected.
 *     Its `onLoad` — i.e. after the real library is present AND consent is
 *     granted — fires consent→granted, then `js`, then `config`. The first
 *     pageview hit is therefore sent deterministically, not via fragile
 *     queue-replay timing (the previous version queued `config` before the
 *     library loaded and no `/collect` hit ever fired).
 *  4. If consent is later withdrawn, push consent→denied (library stays loaded;
 *     Consent Mode suppresses further data).
 *  5. If GA_ID is absent → entire component is a no-op.
 *
 * anonymize_ip is set on config (no-op in GA4, which anonymises by default, but
 * kept explicit).
 */

import Script from "next/script";
import { useEffect, useState } from "react";
import { getStoredConsent, onConsentChange } from "@/lib/consent";
import { isInternalTraffic } from "@/lib/internal-traffic";

// GA4 Measurement ID. Default is the production property (bari.digital);
// a Vercel `NEXT_PUBLIC_GA_ID` env var overrides it if ever set. A GA
// Measurement ID is not a secret — it is exposed in every visitor's browser.
const GA_ID = process.env.NEXT_PUBLIC_GA_ID ?? "G-2KBNY4XZHS";

declare global {
  interface Window {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    gtag: (...args: any[]) => void;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    dataLayer: any[];
  }
}

export function GA4Script() {
  const [granted, setGranted] = useState(false);

  useEffect(() => {
    if (!GA_ID) return;

    // Canonical gtag stub — MUST push the `arguments` object, not a plain
    // array, or gtag.js will not process the queued commands.
    window.dataLayer = window.dataLayer ?? [];
    if (!window.gtag) {
      window.gtag = function gtag() {
        // eslint-disable-next-line prefer-rest-params
        window.dataLayer.push(arguments);
      };
    }

    // Consent Mode v2 — deny everything before any tag loads.
    window.gtag("consent", "default", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });

    // Apply the stored choice, then react to future CMP changes.
    const stored = getStoredConsent();
    if (stored?.analytics) setGranted(true);

    const unsub = onConsentChange((record) => {
      setGranted(record.analytics);
      if (!record.analytics && typeof window.gtag === "function") {
        window.gtag("consent", "update", { analytics_storage: "denied" });
      }
    });
    return unsub;
  }, []);

  if (!GA_ID || !granted) return null;

  return (
    <Script
      id="ga4-gtag"
      src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
      strategy="afterInteractive"
      onLoad={() => {
        // Library is loaded and consent is granted — send the first hit now.
        window.gtag("consent", "update", { analytics_storage: "granted" });
        window.gtag("js", new Date());
        // traffic_type: 'internal' (TASK-522) tags owner/agent/dev/preview
        // clients (see @/lib/internal-traffic) so a GA4 Admin-UI data filter
        // can exclude them later — the owner activates that filter; this is
        // just the parameter being sent. Absent entirely for real visitors.
        window.gtag("config", GA_ID, {
          anonymize_ip: true,
          ...(isInternalTraffic() ? { traffic_type: "internal" } : {}),
        });
      }}
    />
  );
}
