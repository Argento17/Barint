const fs = require("fs");
const path = require("path");
const p = path.join(__dirname, "..", "src/lib/seo/llms-content.ts");
const content = `import { listPublicCorpusSlugs } from "@/lib/seo/public-corpus-registry";
import { ALL_INDEXABLE_PATHS } from "@/lib/seo/sitemap-paths";
import { SITE_URL, absoluteUrl } from "@/lib/site-url";

export function generateLlmsTxtBody(): string {
  const slugs = listPublicCorpusSlugs();
  const dataEndpoints = slugs.map((slug) => absoluteUrl(\`/data/comparisons/\${slug}\`));

  const keyPages = ALL_INDEXABLE_PATHS.filter((p) => !p.startsWith("/data/")).map((p) =>
    absoluteUrl(p)
  );

  const lines = [
    "# Bari \u2014 Food intelligence for the Israeli shelf",
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
    "## \u05e2\u05d1\u05e8\u05d9\u05ea",
    "",
    "- \u05d0\u05ea\u05e8: " + SITE_URL,
    "- \u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea \u05de\u05d5\u05e6\u05e8\u05d9\u05dd: " + absoluteUrl("/hashvaot"),
    "- \u05d1\u05dc\u05d5\u05d2: " + absoluteUrl("/blog"),
    "- \u05e0\u05ea\u05d5\u05e0\u05d9 \u05d4\u05e9\u05d5\u05d5\u05d0\u05d4 \u05dc\u05e7\u05e8\u05d9\u05d0\u05d4 \u05d1\u05dc\u05d1\u05d3 (JSON):",
    ...dataEndpoints.map((u) => "  - " + u),
    "",
    "## Key URLs",
    ...keyPages.map((u) => "- " + u),
    "",
  ];

  return lines.join("\\n");
}
`;
fs.writeFileSync(p, content, "utf8");
console.log("llms fixed");

// sugar-alcohols cleanup
const sa = path.join(__dirname, "..", "src/app/blog/sugar-alcohols/page.tsx");
let saText = fs.readFileSync(sa, "utf8");
saText = saText.replace(/const pageTitle = metadata.title as string;\nconst pageDescription = metadata.description as string;\n\n/, "");
fs.writeFileSync(sa, saText, "utf8");

// faq-schema compat
const faq = path.join(__dirname, "..", "src/lib/seo/faq-schema.ts");
fs.writeFileSync(faq, `import { toJsonLdScript } from "@/lib/seo/json-ld";

/** @deprecated Use getFaqSchema + JsonLdScript or toJsonLdScript directly. */
export function buildFaqScript(raw: Record<string, unknown>): string {
  const { _bari_meta: _dropped, ...schema } = raw;
  void _dropped;
  return toJsonLdScript(schema);
}
`, "utf8");
