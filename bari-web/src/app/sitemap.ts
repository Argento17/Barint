import type { MetadataRoute } from "next";

import { ALL_INDEXABLE_PATHS } from "@/lib/seo/sitemap-paths";
import { absoluteUrl } from "@/lib/site-url";

export const revalidate = 86400;

export default function sitemap(): MetadataRoute.Sitemap {
  try {
    const lastModified = new Date();
    return ALL_INDEXABLE_PATHS.map((path) => ({
      url: absoluteUrl(path),
      lastModified,
      changeFrequency: "weekly" as const,
      priority: path === "/" ? 1 : path.startsWith("/hashvaot") ? 0.8 : 0.6,
    }));
  } catch {
    return [
      {
        url: absoluteUrl("/"),
        lastModified: new Date(),
        changeFrequency: "weekly",
        priority: 1,
      },
    ];
  }
}
