import type { MetadataRoute } from "next";

import { absoluteUrl } from "@/lib/site-url";

/**
 * SEO baseline (DEC-003 market-facing readiness). Public content is indexable;
 * internal / non-content surfaces are excluded. Platform-only — no scoring or
 * corpus impact.
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/api/", "/dev/"],
    },
    sitemap: absoluteUrl("/sitemap.xml"),
  };
}
