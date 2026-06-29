import { BLOG_RSS_ENTRIES, blogRssAbsoluteUrl } from "@/lib/seo/blog-rss";
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
      `      <title>${escapeXml(entry.title)}</title>`,
      `      <link>${escapeXml(link)}</link>`,
      `      <guid isPermaLink="true">${escapeXml(link)}</guid>`,
      `      <pubDate>${new Date(entry.pubDate).toUTCString()}</pubDate>`,
      `      <description>${escapeXml(entry.description)}</description>`,
      "    </item>",
    ].join("\n");
  }).join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Bari Blog</title>
    <link>${escapeXml(absoluteUrl("/blog"))}</link>
    <description>Food intelligence articles from Bari</description>
    <language>he</language>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
${items}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/rss+xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
