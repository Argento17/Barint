"use client";

/**
 * Vercel Web Analytics wrapper (TASK-522).
 *
 * Wraps the plain `<Analytics />` mount (previously inlined in layout.tsx)
 * to add a `beforeSend` filter. The consent posture is unchanged: cookieless,
 * no PII, deliberately NOT consent-gated — see the rationale comment at the
 * mount site in layout.tsx and privacy/page.tsx.
 *
 * `beforeSend` drops /admin pages and internal (owner/agent/dev) traffic so
 * the dashboard number reflects real visitors. Only automatic page views are
 * tracked here — no custom `track()` calls (that is a Pro-plan feature; this
 * project is on Hobby and adds no paid features).
 *
 * This must be a Client Component: `beforeSend` is a function, and a Server
 * Component (RootLayout) cannot pass a function prop across the server/client
 * boundary to a Client Component without it being a "use server" action.
 * Defining it here, inside client code, avoids that serialization entirely.
 */

import { Analytics } from "@vercel/analytics/next";
import { isInternalTraffic } from "@/lib/internal-traffic";

export function VercelAnalytics() {
  return (
    <Analytics
      beforeSend={(event) => {
        let pathname = event.url;
        try {
          pathname = new URL(event.url, "https://bari.digital").pathname;
        } catch {
          // event.url was already a bare pathname — use as-is.
        }
        if (pathname.startsWith("/admin")) return null;
        if (isInternalTraffic()) return null;
        return event;
      }}
    />
  );
}
