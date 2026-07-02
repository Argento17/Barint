const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");
function w(rel, content) {
  const p = path.join(root, rel);
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, content, "utf8");
  console.log("wrote", rel);
}

w("src/lib/seo/public-corpus-registry.ts", `import type { ComparisonCorpusRaw } from "@/lib/comparisons/corpus";

import breadCorpus from "@/data/comparisons/bread_frontend_v3.json";
import breakfastCerealsCorpus from "@/data/comparisons/cereals_frontend_v2.json";
import brinedCheesesCorpus from "@/data/comparisons/brined_cheeses_frontend_v2.json";
import cakesCorpus from "@/data/comparisons/cakes_hard_cookies_frontend_v1.json";
import cheeseCorpus from "@/data/comparisons/cheese_frontend_v4.json";
import chocolateBarsCorpus from "@/data/comparisons/chocolate_bars_frontend_v1.json";
import chocolateTabletsCorpus from "@/data/comparisons/chocolate_tablets_frontend_v1.json";
import cookiesCoffeeCorpus from "@/data/comparisons/cookies_coffee_frontend_v2.json";
import granolaCorpus from "@/data/comparisons/granola_frontend_v1.json";
import hardCheesesCorpus from "@/data/comparisons/hard_cheeses_frontend_v2.json";
import hummusCorpus from "@/data/comparisons/hummus_frontend_v5.json";
import juicesCorpus from "@/data/comparisons/juices_frontend_v3.json";
import milkCorpus from "@/data/comparisons/milk_frontend_v1.json";
import proteinBarsCorpus from "@/data/comparisons/protein_combined_frontend_v2.json";
import snacksCorpus from "@/data/comparisons/snacks_frontend_v5.json";
import { magnesiumProducts } from "@/lib/comparisons/magnesium-page-data";

const CORPUS_BY_SLUG: Record<string, ComparisonCorpusRaw> = {
  bread: breadCorpus as ComparisonCorpusRaw,
  "breakfast-cereals": breakfastCerealsCorpus as ComparisonCorpusRaw,
  "brined-cheeses": brinedCheesesCorpus as ComparisonCorpusRaw,
  cakes: cakesCorpus as ComparisonCorpusRaw,
  cheese: cheeseCorpus as ComparisonCorpusRaw,
  "chocolate-bars": chocolateBarsCorpus as ComparisonCorpusRaw,
  "chocolate-tablets": chocolateTabletsCorpus as ComparisonCorpusRaw,
  "cookies-coffee": cookiesCoffeeCorpus as ComparisonCorpusRaw,
  granola: granolaCorpus as ComparisonCorpusRaw,
  "hard-cheeses": hardCheesesCorpus as ComparisonCorpusRaw,
  hummus: hummusCorpus as ComparisonCorpusRaw,
  juices: juicesCorpus as ComparisonCorpusRaw,
  magnesium: {
    _meta: {
      category: "magnesium",
      generated: "2026-06-23T00:00:00Z",
      product_count: magnesiumProducts.length,
    },
    products: magnesiumProducts,
  },
  "milk-comparison": milkCorpus as ComparisonCorpusRaw,
  "protein-bars": proteinBarsCorpus as ComparisonCorpusRaw,
  snacks: snacksCorpus as ComparisonCorpusRaw,
};

export function getCorpusBySlug(slug: string): ComparisonCorpusRaw | null {
  return CORPUS_BY_SLUG[slug] ?? null;
}

export function listPublicCorpusSlugs(): string[] {
  return Object.keys(CORPUS_BY_SLUG).sort();
}
`);

w("src/lib/seo/sitemap-paths.ts", `/** Stable, indexable public routes for sitemap generation. */
export const ALL_INDEXABLE_PATHS = [
  "/",
  "/hashvaot",
  "/hashvaot/bread",
  "/hashvaot/breakfast-cereals",
  "/hashvaot/brined-cheeses",
  "/hashvaot/cakes",
  "/hashvaot/cheese",
  "/hashvaot/chocolate-bars",
  "/hashvaot/chocolate-tablets",
  "/hashvaot/cookies-coffee",
  "/hashvaot/granola",
  "/hashvaot/hard-cheeses",
  "/hashvaot/hummus",
  "/hashvaot/juices",
  "/hashvaot/magnesium",
  "/hashvaot/milk-comparison",
  "/hashvaot/protein-bars",
  "/hashvaot/snacks",
  "/blog",
  "/blog/bread-analysis",
  "/blog/bread-everyday",
  "/blog/bread-standouts",
  "/blog/bread-wellness-gap",
  "/blog/hummus",
  "/blog/lechem",
  "/blog/milk-analysis",
  "/blog/shemen-zayit",
  "/blog/sugar-alcohols",
  "/blog/yogurt",
  "/research/glass-box",
  "/research/bread-transparency-shufersal",
  "/privacy",
  "/terms",
] as const;
`);

w("src/lib/seo/blog-rss.ts", `import { absoluteUrl } from "@/lib/site-url";

export type BlogRssEntry = {
  title: string;
  description: string;
  path: string;
  pubDate: string;
};

/** RSS entries for published blog articles (ISO 8601 pubDate). */
export const BLOG_RSS_ENTRIES: BlogRssEntry[] = [
  {
    title: "מה באמת קורה בחלב בישראל?",
    path: "/blog/milk-analysis",
    description:
      "ניתוח מעמיק על חלב ומוצרי חלב מעובדים בישראל — עקביות, טריות והשוואה אסטרטגית.",
    pubDate: "2026-05-01T08:00:00Z",
  },
  {
    title: "20 שמני זית. 10 מותגים.",
    path: "/blog/shemen-zayit",
    description: "סקירת שמני זית מרכזיים במדף הישראלי.",
    pubDate: "2026-06-01T08:00:00Z",
  },
  {
    title: "סוכרים אלכוהוליים בחטיפי חלבון",
    path: "/blog/sugar-alcohols",
    description: "מלטיטול וחבריו — מה מופיע על המדף ומה כדאי לדעת.",
    pubDate: "2026-06-15T08:00:00Z",
  },
  {
    title: "חומוס בשוק הישראלי",
    path: "/blog/hummus",
    description: "מפת חומוס מבוססת השוואת Bari.",
    pubDate: "2026-06-10T08:00:00Z",
  },
  {
    title: "יוגורט בישראל",
    path: "/blog/yogurt",
    description: "מה מבדיל בין יוגורטים במדף.",
    pubDate: "2026-06-08T08:00:00Z",
  },
  {
    title: "לחם בשוק הישראלי",
    path: "/blog/lechem",
    description: "סקירת לחמים ומה משפיע על הציון.",
    pubDate: "2026-06-05T08:00:00Z",
  },
  {
    title: "לחם יומיומי",
    path: "/blog/bread-everyday",
    description: "לחמים לשימוש יומיומי — ממצאים מהמדף.",
    pubDate: "2026-06-12T08:00:00Z",
  },
  {
    title: "לחמים בולטים",
    path: "/blog/bread-standouts",
    description: "מוצרים שבולטים לטובה ולרעה.",
    pubDate: "2026-06-12T09:00:00Z",
  },
  {
    title: "פער ה-wellness בלחם",
    path: "/blog/bread-wellness-gap",
    description: "פער בין שיווק wellness לבין הרכב בפועל.",
    pubDate: "2026-06-12T10:00:00Z",
  },
  {
    title: "ניתוח לחם (ארכיון)",
    path: "/blog/bread-analysis",
    description: "מפנה לסדרת מאמרי הלחם.",
    pubDate: "2026-06-01T08:00:00Z",
  },
];

export function blogRssAbsoluteUrl(path: string): string {
  return absoluteUrl(path);
}
`);

w("src/lib/seo/llms-content.ts", `import { listPublicCorpusSlugs } from "@/lib/seo/public-corpus-registry";
import { ALL_INDEXABLE_PATHS } from "@/lib/seo/sitemap-paths";
import { SITE_URL, absoluteUrl } from "@/lib/site-url";

export function generateLlmsTxtBody(): string {
  const slugs = listPublicCorpusSlugs();
  const dataEndpoints = slugs.map((slug) => absoluteUrl(\`/data/comparisons/\${slug}\`));

  const keyPages = ALL_INDEXABLE_PATHS.filter((p) => !p.startsWith("/data/")).map((p) =>
    absoluteUrl(p)
  );

  return [
    "# Bari — Food intelligence for the Israeli shelf",
    "",
    "> Bari publishes independent, label-based comparisons of packaged foods sold in Israel.",
    "> Scores and grades are editorial products of the Bari engine; ingredients and nutrition come from direct product labels only.",
    "",
    "## English",
    "",
    "- Site: " + SITE_URL,
    "- Comparisons hub: " + absoluteUrl("/hashvaot"),
    "- Blog: " + absoluteUrl("/blog"),
    "- Machine-readable comparison JSON (public, read-only):",
    ...dataEndpoints.map((u) => "  - " + u),
    "",
    "## עברית",
    "",
    "- אתר: " + SITE_URL,
    "- השוואות מוצרים: " + absoluteUrl("/hashvaot"),
    "- בלוג: " + absoluteUrl("/blog"),
    "- נתוני השוואה לקריאה בלבד (JSON):",
    ...dataEndpoints.map((u) => "  - " + u),
    "",
    "## Key URLs",
    ...keyPages.map((u) => "- " + u),
    "",
  ].join("\\n");
}
`);

w("src/app/llms.txt/route.ts", `import { generateLlmsTxtBody } from "@/lib/seo/llms-content";

export const revalidate = 86400;

export function GET() {
  const body = generateLlmsTxtBody();
  return new Response(body, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
`);

w("src/app/feed.xml/route.ts", `import { BLOG_RSS_ENTRIES, blogRssAbsoluteUrl } from "@/lib/seo/blog-rss";
import { SITE_URL, absoluteUrl } from "@/lib/site-url";

export const revalidate = 86400;

function escapeXml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

export function GET() {
  const items = BLOG_RSS_ENTRIES.map((entry) => {
    const link = blogRssAbsoluteUrl(entry.path);
    return [
      "    <item>",
      \`      <title>\${escapeXml(entry.title)}</title>\`,
      \`      <link>\${escapeXml(link)}</link>\`,
      \`      <guid isPermaLink="true">\${escapeXml(link)}</guid>\`,
      \`      <pubDate>\${new Date(entry.pubDate).toUTCString()}</pubDate>\`,
      \`      <description>\${escapeXml(entry.description)}</description>\`,
      "    </item>",
    ].join("\\n");
  }).join("\\n");

  const xml = \`<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Bari Blog</title>
    <link>\${escapeXml(absoluteUrl("/blog"))}</link>
    <description>Food intelligence articles from Bari</description>
    <language>he</language>
    <lastBuildDate>\${new Date().toUTCString()}</lastBuildDate>
\${items}
  </channel>
</rss>\`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/rss+xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
`);

w("src/app/data/comparisons/[slug]/route.ts", `import { NextResponse } from "next/server";

import { getCorpusBySlug, listPublicCorpusSlugs } from "@/lib/seo/public-corpus-registry";

export const revalidate = 3600;

type Params = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return listPublicCorpusSlugs().map((slug) => ({ slug }));
}

export async function GET(_request: Request, { params }: Params) {
  const { slug } = await params;
  const corpus = getCorpusBySlug(slug);
  if (!corpus) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  return NextResponse.json(corpus, {
    headers: {
      "Cache-Control": "public, max-age=3600",
    },
  });
}
`);

w("src/app/data/comparisons/[slug]/products/[productId]/route.ts", `import { NextResponse } from "next/server";

import { getCorpusBySlug } from "@/lib/seo/public-corpus-registry";

export const revalidate = 3600;

type Params = { params: Promise<{ slug: string; productId: string }> };

export async function GET(_request: Request, { params }: Params) {
  const { slug, productId } = await params;
  const corpus = getCorpusBySlug(slug);
  if (!corpus) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  const product = corpus.products.find((p) => p.id === productId);
  if (!product) {
    return NextResponse.json({ error: "Product not found" }, { status: 404 });
  }
  return NextResponse.json(product, {
    headers: {
      "Cache-Control": "public, max-age=3600",
    },
  });
}
`);

w("src/app/sitemap.ts", `import type { MetadataRoute } from "next";

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
`);

w("src/app/robots.ts", `import type { MetadataRoute } from "next";

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
`);

console.log("batch2 done");
