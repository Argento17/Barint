import type { MetadataRoute } from "next";

import { absoluteUrl } from "@/lib/site-url";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: ["/", "/data/", "/llms.txt"],
      disallow: ["/api/", "/dev/", "/admin/", "/admin"],
    },
    sitemap: absoluteUrl("/sitemap.xml"),
  };
}
