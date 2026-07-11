import type { MetadataRoute } from "next";

import { absoluteUrl } from "@/lib/site-url";

const DISALLOW = ["/api/", "/dev/", "/admin/", "/admin", "/internal/"];

const AI_AND_SEARCH_BOTS = [
  "Googlebot",
  "GPTBot",
  "Google-Extended",
  "ChatGPT-User",
  "anthropic-ai",
  "ClaudeBot",
] as const;

export default function robots(): MetadataRoute.Robots {
  const botAllow = ["/", "/data/", "/llms.txt", "/ai-index"];

  return {
    rules: [
      {
        userAgent: "*",
        allow: ["/", "/data/", "/llms.txt", "/ai-index", "/data/products.json"],
        disallow: DISALLOW,
      },
      ...AI_AND_SEARCH_BOTS.map((userAgent) => ({
        userAgent,
        allow: botAllow,
        disallow: DISALLOW,
      })),
    ],
    sitemap: absoluteUrl("/sitemap.xml"),
  };
}
