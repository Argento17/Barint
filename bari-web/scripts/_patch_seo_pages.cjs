const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");

// layout.tsx
const layoutPath = path.join(root, "src/app/layout.tsx");
let layout = fs.readFileSync(layoutPath, "utf8");
if (!layout.includes("JsonLdScript")) {
  layout = layout.replace(
    'import { cn } from "@/lib/utils";',
    'import { JsonLdScript } from "@/components/seo/json-ld-script";\nimport { buildSiteJsonLd } from "@/lib/seo/organization-schema";\nimport { cn } from "@/lib/utils";'
  );
  layout = layout.replace(
    "<body className=\"min-h-full flex flex-col\">",
    "<body className=\"min-h-full flex flex-col\">\n        {buildSiteJsonLd().map((schema) => (\n          <JsonLdScript key={schema[\"@type\"] as string} data={schema} />\n        ))}"
  );
  fs.writeFileSync(layoutPath, layout, "utf8");
  console.log("updated layout");
}

// fix comparison-page-seo unused import
const cps = path.join(root, "src/components/seo/comparison-page-seo.tsx");
let cpsText = fs.readFileSync(cps, "utf8");
cpsText = cpsText.replace('import { absoluteUrl } from "@/lib/site-url";\n', "");
fs.writeFileSync(cps, cpsText, "utf8");

const FAQ = {
  bread: "bread",
  "breakfast-cereals": "breakfast_cereals",
  "brined-cheeses": "brined_cheeses",
  "cookies-coffee": "cookies_coffee",
  granola: "granola",
  "hard-cheeses": "hard_cheeses",
  hummus: "hummus",
  juices: "juices",
};

const skip = new Set(["supermarket", "supplements", "personal-care", "raw-foods"]);

function patchHashvaot(slug) {
  const p = path.join(root, "src/app/hashvaot", slug, "page.tsx");
  if (!fs.existsSync(p)) return;
  let text = fs.readFileSync(p, "utf8");
  text = text.replace(/import \{ buildFaqScript \} from "@\/lib\/seo\/faq-schema";\r?\n/g, "");
  text = text.replace(/import rawFaqSchema from "@\/data\/seo\/[^"]+";\r?\n/g, "");
  text = text.replace(/\s*<script type="application\/ld\+json" dangerouslySetInnerHTML=\{\{ __html: buildFaqScript\(rawFaqSchema\) \}\} \/>\r?\n/g, "\n");
  text = text.replace(/return \(\s*<>\s*/g, "return (\n    ");
  text = text.replace(/\s*<\/>\s*\);/g, "\n  );");

  if (!text.includes("ComparisonPageSeo")) {
    text = text.replace(
      /import type \{ Metadata \} from "next";\r?\n\r?\n/,
      'import type { Metadata } from "next";\n\nimport { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";\n'
    );
  }

  const prodMatch = text.match(/products=\{(\w+)\}/);
  if (!prodMatch) {
    console.log("no products", slug);
    return;
  }
  const products = prodMatch[1];
  const pagePath = `/hashvaot/${slug}`;
  const faqKey = FAQ[slug];
  const faqAttr = faqKey ? ` faqKey="${faqKey}"` : "";

  if (!text.includes("searchParams")) {
    text = text.replace(
      /export default (async )?function (\w+)\([^)]*\) \{/,
      `export default async function $2({\n  searchParams,\n}: {\n  searchParams: Promise<{ product?: string }>;\n}) {\n  const params = await searchParams;\n  const initialExpandedProductId = params.product ?? null;\n`
    );
  }

  if (!text.includes("initialExpandedProductId=")) {
    text = text.replace(/(\n\s*)(\/>)(\s*\n\s*\);)/, `$1  initialExpandedProductId={initialExpandedProductId}\n$1$2$3`);
  }

  const seoLine = `    <ComparisonPageSeo pagePath="${pagePath}" products={${products}}${faqAttr} />\n`;
  if (!text.includes("ComparisonPageSeo")) {
    text = text.replace(/return \(\s*\n/, `return (\n${seoLine}`);
  } else if (!text.includes(`pagePath="${pagePath}"`)) {
    text = text.replace(/return \(\s*\n/, `return (\n${seoLine}`);
  }

  fs.writeFileSync(p, text, "utf8");
  console.log("patched hashvaot", slug);
}

for (const ent of fs.readdirSync(path.join(root, "src/app/hashvaot"), { withFileTypes: true })) {
  if (!ent.isDirectory() || skip.has(ent.name)) continue;
  patchHashvaot(ent.name);
}

// blog pages
const blogSeo = [
  { file: "hummus/page.tsx", url: "/blog/hummus" },
  { file: "milk-analysis/page.tsx", url: "/blog/milk-analysis" },
  { file: "yogurt/page.tsx", url: "/blog/yogurt" },
  { file: "lechem/page.tsx", url: "/blog/lechem" },
  { file: "shemen-zayit/page.tsx", url: "/blog/shemen-zayit" },
  { file: "bread-everyday/page.tsx", url: "/blog/bread-everyday" },
  { file: "bread-standouts/page.tsx", url: "/blog/bread-standouts" },
  { file: "bread-wellness-gap/page.tsx", url: "/blog/bread-wellness-gap" },
  { file: "bread-analysis/page.tsx", url: "/blog/bread-analysis" },
  { file: "sugar-alcohols/page.tsx", url: "/blog/sugar-alcohols" },
];

for (const { file, url } of blogSeo) {
  const p = path.join(root, "src/app/blog", file);
  if (!fs.existsSync(p)) continue;
  let text = fs.readFileSync(p, "utf8");
  if (text.includes("BlogArticleSeo")) continue;
  if (text.includes("redirect(")) {
    console.log("skip redirect blog", file);
    continue;
  }
  if (!text.includes("BlogArticleSeo")) {
    text = text.replace(
      /import type \{ Metadata \} from "next";\r?\n\r?\n/,
      'import type { Metadata } from "next";\n\nimport { BlogArticleSeo } from "@/components/seo/blog-article-seo";\nimport { absoluteUrl } from "@/lib/site-url";\n'
    );
  }
  const titleMatch = text.match(/title:\s*"([^"]+)"/);
  const descMatch = text.match(/description:\s*\n?\s*"([^"]+)"/);
  if (!titleMatch || !descMatch) {
    console.log("skip blog metadata", file);
    continue;
  }
  const title = titleMatch[1].replace(/\| Bari$/, "").trim();
  const description = descMatch[1];
  const block = `    <BlogArticleSeo\n      title={${JSON.stringify(title)}}\n      description={${JSON.stringify(description)}}\n      url={absoluteUrl("${url}")}\n    />\n`;
  text = text.replace(/return (\s*)<(\w+)/, `return (\n    <>\n${block}      <$2`);
  text = text.replace(/(\/>);\s*\n\}/, `$1\n    </>\n  );\n}`);
  fs.writeFileSync(p, text, "utf8");
  console.log("patched blog", file);
}

console.log("patch done");
