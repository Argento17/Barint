import { listPublicCorpusSlugs } from "@/lib/seo/public-corpus-registry";
import { ALL_INDEXABLE_PATHS } from "@/lib/seo/sitemap-paths";
import { SITE_URL, absoluteUrl } from "@/lib/site-url";

export function generateLlmsTxtBody(): string {
  const slugs = listPublicCorpusSlugs();
  const dataEndpoints = slugs.map((slug) => absoluteUrl(`/data/comparisons/${slug}`));

  const keyPages = ALL_INDEXABLE_PATHS.filter((p) => !p.startsWith("/data/")).map((p) =>
    absoluteUrl(p)
  );

  const lines = [
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
    "- AI index: " + absoluteUrl("/ai-index"),
    "- Product index (JSON): " + absoluteUrl("/data/products.json"),
    "- Machine-readable comparison JSON (public, read-only):",
    ...dataEndpoints.map((u) => "  - " + u),
    "",
    "## עברית",
    "",
    "- אתר: " + SITE_URL,
    "- השוואות מוצרים: " + absoluteUrl("/hashvaot"),
    "- בלוג: " + absoluteUrl("/blog"),
    "- מפת AI: " + absoluteUrl("/ai-index"),
    "- אינדקס מוצרים (JSON): " + absoluteUrl("/data/products.json"),
    "- נתוני השוואה לקריאה בלבד (JSON):",
    ...dataEndpoints.map((u) => "  - " + u),
    "",
    "## Key URLs",
    ...keyPages.map((u) => "- " + u),
    "",
  ];

  return lines.join("\n");
}
