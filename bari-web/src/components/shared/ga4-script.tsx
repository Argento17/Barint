"use client";

/**
 * GA4 consent-gated script loader.
 *
 * Strategy: Google Consent Mode v2 + deferred injection.
 *  1. On mount, set gtag consent defaults to denied (no cookies written).
 *  2. If the user already accepted analytics → inject the GA4 <Script> immediately
 *     and call gtag('consent','update',{analytics_storage:'granted'}).
 *  3. If the user later accepts via the CMP → inject the script dynamically and
 *     update consent state. No reload required.
 *  4. If NEXT_PUBLIC_GA_ID is absent → entire component is a no-op.
 *
 * anonymize_ip is always set to true.
 */

import Script from "next/script";
import { useEffect, useState } from "react";
import { getStoredConsent, onConsentChange } from "@/lib/consent";

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
  const [analyticsGranted, setAnalyticsGranted] = useState(false);

  useEffect(() => {
    if (!GA_ID) return;

    // Step 1 — initialise dataLayer + gtag stub before the script tag so that
    // consent defaults are set before any GA4 hit is sent.
    window.dataLayer = window.dataLayer ?? [];
    function gtag(...args: unknown[]) {
      window.dataLayer.push(args);
    }
    // Only assign if not already defined (e.g. by a prior render)
    if (!window.gtag) {
      window.gtag = gtag;
    }

    // Step 2 — set consent defaults (denied) unconditionally.
    window.gtag("consent", "default", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      wait_for_update: 500,
    });
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { anonymize_ip: true });

    // Step 3 — check existing consent and apply immediately if already granted.
    const stored = getStoredConsent();
    if (stored?.analytics) {
      setAnalyticsGranted(true);
      window.gtag("consent", "update", { analytics_storage: "granted" });
    }

    // Step 4 — listen for future consent updates.
    const unsub = onConsentChange((record) => {
      if (record.analytics) {
        setAnalyticsGranted(true);
        window.gtag("consent", "update", { analytics_storage: "granted" });
      } else {
        // User withdrew analytics consent — update mode but do NOT delete the
        // script (GA4 Consent Mode handles data suppression server-side).
        window.gtag("consent", "update", { analytics_storage: "denied" });
      }
    });

    return unsub;
  }, []);

  // Do nothing if GA_ID is absent
  if (!GA_ID) return null;

  // Only inject the actual GA4 <Script> after the user consented.
  // Until then the gtag stub + consent defaults are enough to satisfy
  // Google's "consent defaults must precede the gtag.js request" requirement.
  if (!analyticsGranted) return null;

  return (
    <Script
      src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
      strategy="afterInteractive"
    />
  );
}
